---
type: entity
title: Redis
aliases: [레디스, Valkey]
tags: [저장, 캐시, 키-값]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 4-04 Redis 핵심 개념과 성능 요소]]"
  - "[[AI DE 강의 4-05 캐싱 레이어와 캐싱 전략]]"
  - "[[DB 면접 3 Lock과 동시성 제어]]"
---

# Redis

인메모리 key-value 저장소다. 값 하나를 꺼내는 캐시에 그치지 않고, 자료구조를 메모리에 올려 두고 직접 조작한다([[AI DE 강의 4-04 Redis 핵심 개념과 성능 요소]] p69). 초저지연 캐싱 아키텍처에서는 보통 원본 저장소(PostgreSQL·MySQL·MongoDB·BigQuery·S3) 앞의 캐시 계층으로 쓴다(p73). 캐싱 패턴은 [[캐싱]]에서 다룬다. [[NoSQL]]의 네 타입 가운데 Key-Value의 대표로 나온다.

여러 애플리케이션 인스턴스가 같은 자원을 두고 서로를 배제해야 할 때 분산 락 저장소로도 쓴다. [[DB 면접 3 Lock과 동시성 제어]] Q1-3(p35)의 Gold 답이 이 용도다. 락은 상호 배제만 줄 뿐 여러 시스템에 걸친 원자성은 주지 않고, lease가 만료되면 안전성이 깨질 수 있어 fencing token이 필요하다. 전문은 [[데이터베이스 락]]에 있다.

## 자료구조

| 자료구조 | 쓰임 |
|---|---|
| String | 단순 캐시, 토큰, 카운터 |
| Hash | 한 key 안에 field-value 여러 개. 프로필, 세션, 설정. 특정 필드만 고치는 객체에 String보다 효율적 |
| List | 큐, 최근 활동 목록 |
| Set | 태그, 권한, 사용자 그룹 |
| Sorted Set | 점수로 정렬되는 집합. 랭킹, 우선순위 큐, 시간 기반 정렬 |
| Stream | append-only 로그. 이벤트 기록, 메시지 스트림 |

강의 p70·p80의 정리다.

## 스레드 모델

강의는 "Redis는 싱글 스레드로 동작"하므로 명령 하나가 오래 걸리면 다른 모든 요청이 기다린다고 설명한다(p81). 명령 실행에 대해서는 지금도 맞다. 공식 문서는 "Redis serves all the requests using a single thread"라고 쓰고, 설정 파일은 "Redis is mostly single threaded"라고 쓴다. 다만 6.0부터 I/O 스레드가 소켓 읽기·쓰기와 프로토콜 파싱을 나눠 맡고, 8.0에서 이것을 다시 구현했다(8.0 릴리스 노트: "A new I/O threading implementation which enables throughput increase on multi-core environments"). [https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/ · https://raw.githubusercontent.com/redis/redis/8.0/00-RELEASENOTES , 2026-09-28 확인]

그래서 O(N) 명령이 위험하다. `GET`·`SET`·`HGET`은 O(1)이지만 `KEYS *`·`HGETALL`·`SMEMBERS`는 원소 수에 비례한다(p81). 문서도 `KEYS`를 흔한 지연 원인으로 경고한다.

## 성능 요소

강의 p79가 드는 요소는 자료구조 선택, 명령 시간 복잡도, 네트워크 왕복 횟수, key·value 크기, 동시 요청 패턴(connection pool), hot key, eviction, persistence, replication·cluster 구성이다.

- 파이프라이닝. 명령을 모아 한 번의 왕복으로 보내 RTT와 system call을 줄인다(p82–83). 서버 프로토콜 수준에서 원자적이지 않다. 원자성이 필요하면 `MULTI`/`EXEC`나 Lua 스크립트를 쓴다. 클라이언트마다 다른 점도 있다. redis-py의 `pipeline()`은 기본값으로 MULTI/EXEC 트랜잭션에 감싸진다("A pipeline actually executes as a transaction by default", https://redis.io/docs/latest/develop/clients/redis-py/transpipe/ , 2026-09-28 확인).
- Eviction. `maxmemory`에 닿으면 기존 key를 지운다(p88). LRU·LFU는 정확한 알고리즘이 아니라 표본으로 근사한다("LRU, LFU and minimal TTL algorithms are not precise algorithms but approximated", `redis.conf`, 2026-09-28 확인).
- Persistence. RDB 스냅샷은 fork로 자식 프로세스를 만들어 순간적으로 느려질 수 있다. AOF는 모든 쓰기를 기록하고, `appendfsync` 설정(always·everysec·no)이 성능과 안전성 사이를 정한다(p89). 기본값 everysec에서는 최대 1초 치를 잃을 수 있다. [https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/ , 2026-09-28 확인]

## 확장

강의는 성능 문제가 생겼다고 곧바로 cluster로 가지 말라고 한다(p93). 먼저 캐시 대상, hit ratio, TTL, eviction, hot key, large key, 파이프라이닝 필요성, 호출 횟수를 점검한다.

| 방식 | 효과 | 대가 |
|---|---|---|
| Scale-up | 더 큰 메모리·CPU. 구조가 단순하다 | 한 대의 한계 |
| Replica | 읽기 분산, 장애 대응 | 복제 지연, failover 전략 |
| Cluster | 샤딩으로 메모리·처리량 확장 | 운영 복잡성, multi-key 제약, shard 불균형, hot key |

표는 p94를 따랐다. 복제는 비동기이고, 이것이 아래 CAP 분류 문제로 이어진다. 복제 일반은 [[복제]]에 있다.

⚠️ 강의는 복제 역할을 "Master/Slave"로 부른다(p90). Redis는 5.0부터 `REPLICAOF` 명령과 master-replica 용어를 쓴다. [https://redis.io/docs/latest/commands/replicaof/ , 2026-09-28 확인]

## ❌ Redis는 CP 시스템이 아니다

[[AI DE 강의 4-02 CAP 정리와 분산 시스템의 한계]]는 Redis를 CP 예시로 든다(p43). 공식 문서와 맞지 않는다. Redis Cluster 문서는 "Redis Cluster does not guarantee strong consistency"라고 쓰고, 비동기 복제 때문에 확인 응답을 받은 쓰기도 잃을 수 있다고 밝힌다. 복제 문서는 `WAIT`로 복제본 확인을 기다려도 "it does not turn a set of Redis instances into a CP system with strong consistency"라고 적는다. [Cluster: https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/ · 복제·`WAIT`: https://redis.io/docs/latest/operate/oss_and_stack/management/replication/ , 2026-09-28 확인] 제품 분류의 문제 전반은 [[CAP 정리]]에서 다룬다.

같은 강의의 [[AI DE 강의 4-05 캐싱 레이어와 캐싱 전략]]은 결제 상태·포인트 차감·권한 데이터를 Redis에 적합하지 않은 데이터로 든다(p109). 이쪽이 Redis의 실제 보장과 맞는다. 두 소단원이 어긋난다는 것은 위키의 관찰이다.

## 지표

`INFO` 명령이 서버 상태와 통계를 준다(p91–92). hit ratio(`keyspace_hits`·`keyspace_misses`), `used_memory`·`maxmemory`·fragmentation, `evicted_keys`, `expired_keys`, `instantaneous_ops_per_sec`, `SLOWLOG`, `connected_clients`, p95·p99 지연이다.

## 라이선스와 Valkey

강의는 라이선스를 다루지 않는다. 아래는 위키가 보충한 연표다(2026-09-28 확인).

| 날짜 | 사건 |
|---|---|
| 2024-03-20 | Redis Ltd.가 7.4부터 BSD에서 RSALv2/SSPLv1 이중 라이선스로 바꾼다고 공지 [https://redis.io/blog/redis-adopts-dual-source-available-licensing/] |
| 2024-03-22 | 마지막 BSD 버전에서 포크한 Valkey 저장소 생성. Linux Foundation 산하 프로젝트다(2차 자료) |
| 2024-04-16 | Valkey 첫 GA 7.2.5 (BSD-3-Clause) |
| 2025-05-01 | Redis 8.0부터 AGPLv3를 세 번째 선택지로 추가한다고 공지. 8.0.0은 2025-05-02 [https://redis.io/blog/agplv3/] |

Valkey 날짜는 GitHub API(`valkey-io/valkey`)로 확인했고, Linux Foundation 편입 공지 날짜는 2차 자료로만 알고 있다.

## 관련

- [[캐싱]] · [[NoSQL]] · [[CAP 정리]] · [[복제]] · [[데이터베이스 락]](분산 락) · [[피처 스토어]](온라인 스토어 후보)

---
type: source
title: AI DE 강의 4-04 Redis 핵심 개념과 성능 요소
aliases: [AI DE 4-04]
tags: [AI-DE-강의, 캐시, 저장]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf"
---

# AI DE 강의 4-04 Redis 핵심 개념과 성능 요소

[[AI 데이터 엔지니어링 강의]] Part 4 Ch2 「초저지연 캐싱 아키텍처」의 첫 소단원이다. Redis가 어떤 저장소인지, 캐시로서의 역할, 성능에 영향을 주는 아홉 요소, 지표와 확장 방식을 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch2. 초저지연 캐싱 아키텍쳐: 1. Redis 핵심 개념과 성능 최적화 패턴 |
| 원본 파일 | `part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` p67–95 (29p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch1~4`, 챕터 `Ch2`와 소단원 번호 `1`은 표지 슬라이드 |

## 요약

### 01. Redis란 (p69–75)

- 행·테이블 중심이 아닌 key-value 저장소. String·Hash·List·Set·Sorted Set·Stream을 메모리에 올려 두고 조작한다(p69–71). Sorted Set은 점수로 자동 정렬돼 상위 N명 조회가 빠르다(p72).
- 역할은 원본 저장소(source of truth) 앞의 캐시 계층(p73). cache-aside 흐름 다섯 단계(p74).

### 02. Redis Cache (p76–78)

- 빠른 이유: 파일 시스템·디스크 I/O·버퍼 캐시·실행 계획을 거치지 않고 메모리의 key와 자료구조에 직접 접근한다(p76).
- cache-aside 외 패턴: write-through, prefetching. 선택 기준은 반복 조회면 cache-aside, 쓰기 직후 최신성이면 write-through, 대상이 예측 가능하면 prefetching(p77–78).

### 03. 성능 요소 (p79–90)

- 아홉 요소(p79): 자료구조, 명령 시간 복잡도, 네트워크 왕복, key·value 크기, 동시 요청, hot key, eviction, persistence, replication·cluster.
- 자료구조: 객체의 일부 필드만 고치면 Hash가 효율적(p80).
- 시간 복잡도: 싱글 스레드라 O(N) 명령(KEYS·HGETALL·SMEMBERS)이 전체를 막는다(p81).
- 네트워크 왕복: 파이프라이닝으로 1,000번의 SET을 한 번에(p82–83). 장점은 RTT·CPU 감소, 단점은 메모리 압박과 원자성 미보장.
- key·value 크기: 긴 key와 수십 MB JSON은 피하고 쪼갠다(p84). 동시 요청: connection pool(p85, [[커넥션 풀]]).
- Hot key: 트래픽이 90% 이상 몰리는 key는 클러스터에서도 한 노드에 있다(p86–87).
- Eviction: maxmemory 도달 시 LRU·LFU로 지우며 CPU를 쓴다(p88). Persistence: RDB fork, AOF fsync(p89). Replication·Cluster: 복제 부하, 다중 노드 연산 비용(p90).

### 04. 성능 지표 (p91–92)

- hit ratio, 메모리, eviction, 만료, ops/sec, SLOWLOG, 연결 수, p95·p99. INFO 명령. 단일 지표가 아니라 흐름을 보고, 캐시·애플리케이션·원본 DB 지표를 함께 본다.

### 05. Redis 확장 (p93–95)

- 곧바로 cluster로 가지 말고 캐시 대상·hit·TTL·eviction·hot key·large key·파이프라이닝·호출 횟수부터 점검한다. scale-up, replica, cluster의 맞교환.

## 핵심

- 성능 요소 아홉 개(p79)와 "cluster 전에 점검할 것"(p93)이 실무에 옮겨 쓰기 좋은 체크리스트다. Redis 자체는 [[Redis]], 캐싱 패턴은 [[캐싱]]에 모았다.
- 싱글 스레드 명령 실행(p81)이 O(N) 명령·large key·eviction·fork가 모두 지연 문제가 되는 공통 원인이다. 강의는 요소를 나열만 하고 이 공통 원인으로 묶지 않는다. 묶는 것은 위키의 정리다.

## 주의·결함

- ⚠️ "Redis는 싱글 스레드로 동작"(p81). 명령 실행은 지금도 메인 스레드 하나지만, 6.0부터 I/O 스레드가 소켓 읽기·쓰기와 파싱을 나눠 맡는다(8.0에서 재구현, 8.0 릴리스 노트의 "A new I/O threading implementation"). 공식 표현은 "mostly single threaded"다. [https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/ · https://raw.githubusercontent.com/redis/redis/8.0/00-RELEASENOTES , 2026-09-28 확인]
- ⚠️ 복제를 "Master/Slave"로 부른다(p90). Redis는 5.0부터 `REPLICAOF`와 master-replica 용어를 쓴다. [https://redis.io/docs/latest/commands/replicaof/ , 2026-09-28 확인]
- ⚠️ 파이프라이닝의 장점에 "데이터 무결성"을 넣는다(p83). 같은 슬라이드가 단점으로 원자성 미보장을 드는데, 파이프라이닝은 명령을 묶어 보낼 뿐이어서 무결성을 더해 주지 않는다. 위키의 판단이다. 클라이언트에 따라 다르다는 점도 있다. redis-py의 `pipeline()`은 기본값으로 MULTI/EXEC 트랜잭션에 감싸진다. [https://redis.io/docs/latest/develop/clients/redis-py/transpipe/ , 2026-09-28 확인]
- ⚠️ Hot key의 정의에 "90% 이상"(p86)이라는 수치를 넣지만 출처가 없다.
- p83의 "1,000번의 SET을 Redis는 1ms에 처리, 네트워크 대기는 1,000ms"는 RTT 1ms를 가정한 예시다. 가정은 슬라이드에 적혀 있지 않다.
- ✅ eviction(p88)과 persistence(p89) 서술은 문서와 맞다. LRU·LFU가 근사 알고리즘이라는 점은 강의에 없다([[Redis]]).
- 라이선스 변경(2024 RSALv2/SSPLv1, 2025 AGPLv3 추가)과 Valkey 포크를 다루지 않는다([[Redis]]).
- 머리글 잔재. p87은 목차 「03 Redis 성능을 위한 요소들」 절의 슬라이드인데 머리글이 「02. Redis Cache」이고 제목에 옛 번호 「6.」이 붙어 있다. p86과 본문이 같다.
- 중복 슬라이드. p70≈p71(그림 출처만 추가), p74=p75, p94=p95.
- p76의 "여로 구성요소"는 오탈자다.

## 관련

- 개념: [[캐싱]] · [[NoSQL]] · [[복제]] · [[지연 시간과 처리량]]
- 엔티티: [[Redis]]
- 이전 강의: [[AI DE 강의 4-03 고가용성·복제·합의]]
- 다음 강의: [[AI DE 강의 4-05 캐싱 레이어와 캐싱 전략]]

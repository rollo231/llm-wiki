---
type: entity
title: Redis
area: [data-engineering]
aliases: [레디스, Redis Cluster, Redis Sentinel]
tags: [data-engineering, redis, caching, in-memory, key-value, nosql]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch2 Redis and the caching layer]]", "[[AI DE Course - Part4 Ch2 Caching strategies and TTL]]"]
---

# Redis

**인메모리 key-value 자료구조 저장소.** 초저지연 캐싱 아키텍처에서 원본 저장소 앞의 캐시 계층으로
가장 널리 쓰인다.

> **"값 하나 꺼내는 캐시 레이어뿐 아니라, 데이터 구조를 메모리 안에 직접 올려두고 조작하는 저장소."**

전략과 패턴은 [[Caching strategies]], 여기는 **제품으로서의 Redis**를 다룬다.

## 자료구조 6종

| 구조 | 용도 |
|---|---|
| **String** | 단순 캐시, 토큰, 카운터 |
| **Hash** | 사용자 프로필, 세션 객체, 설정값 — **특정 필드만 수정할 때 메모리·속도 모두 유리** |
| **List** | 큐, 최근 활동 목록 |
| **Set** | 태그, 권한, 사용자 그룹 |
| **Sorted Set** | ⭐ **랭킹**, 우선순위 큐, 시간 기반 정렬 |
| **Stream** | append-only 로그. 이벤트 기록, 메시지 스트림 |

**Sorted Set 예:** 유저A 100점 / B 250점 / C 150점 → 자동으로 `[A, C, B]` 정렬 →
*"점수 상위 10명"* 요청이 매우 빠름.

> **Stream이 "append-only log에 가까운 자료구조"라는 점이 흥미롭다** — [[Apache Kafka]]의
> retained log 모델과 같은 발상이 Redis 안에도 있다. 다만 보관 규모와 소비 그룹 모델은 다르다.
> ([[Message broker]] 참조)

## ⭐ 성능을 결정하는 9가지

| # | 요소 | 핵심 |
|---|---|---|
| 1 | 자료구조 선택 | 단순 저장은 String, 객체 부분 수정은 **Hash** |
| 2 | **명령어 시간 복잡도** | ⭐ 아래 참조 |
| 3 | 네트워크 왕복 횟수 | **Pipelining** |
| 4 | 키·값 크기 | 긴 키 이름도 메모리 점유. 수십 MB JSON은 대역폭·처리 시간 잠식 |
| 5 | 동시 요청 패턴 | 수만 개 연결 유지가 메모리 소모 → **Connection Pool 필수** |
| 6 | **hot key** | 아래 참조 |
| 7 | eviction | 삭제 대상 선정(LRU/LFU)과 삭제가 CPU 소모 |
| 8 | persistence | RDB / AOF |
| 9 | replication·cluster | 복제 부하, multi-key 연산의 추가 네트워크 비용 |

### ⭐ 2. 싱글 스레드 + O(N) = 전체 정지

| | 명령어 |
|---|---|
| **O(1)** | `GET`, `SET`, `HGET` |
| **O(N)** | `KEYS *`, `HGETALL`, `SMEMBERS` |

> ⭐ **"Redis는 싱글 스레드로 동작한다. 하나의 명령어가 오래 걸리면 그동안 다른 모든 요청이
> 대기(Blocking) 상태가 된다. 운영 환경에서 O(N) 명령어를 잘못 사용하면 서비스 전체가 멈추는
> '장애'로 이어질 수 있다."**

**Redis 운영의 1번 함정이다.** (실무에서는 `KEYS` 대신 커서 기반 `SCAN`을 쓴다 — **강의에는
나오지 않는다.**)

### 3. Pipelining — RTT가 진짜 병목

> **"1,000번의 SET을 Redis는 1ms로 처리 가능하지만 네트워크 대기 시간은 1,000ms."**

여러 명령을 모아 한 번의 왕복으로 처리 → 시스템 콜 횟수 최소화.

| 장점 | 단점 |
|---|---|
| RTT 감소, CPU 부하 경감 | **메모리 압박, 원자성(Atomicity) 미보장** |

**"원자성 미보장"이 중요하다** — 파이프라인은 트랜잭션(`MULTI/EXEC`)이 아니다.

### ⭐ 6. Hot Key

> **수많은 키 중 특정 몇 개(예: '실시간 1위 상품')에만 트래픽이 90% 이상 몰리는 현상.**

클러스터로 서버를 나눠도 **특정 키는 물리적으로 한 대에만 존재**하므로 그 서버만 과부하가 걸린다.

> ⭐ **이것이 [[NoSQL]]의 "파티션 키가 시스템을 결정한다", [[Distributed processing]]의
> "샤딩 키 hotspot"과 같은 하나의 제약이다 — 접근이 몰리는 키가 있으면 분산이 안 된다.**

### 8. Persistence — 두 방식 모두 대가가 있다

| | 방식 | 대가 |
|---|---|---|
| **RDB** (Snapshotting) | 순간의 메모리 상태를 복사 | 자식 프로세스 생성(**Fork**) → 성능 저하 가능 |
| **AOF** (Append Only File) | 모든 쓰기 명령을 기록 | 디스크 I/O. **fsync 옵션에 따라 성능 vs 안전성 트레이드오프** |

## 운영 지표

> **"Redis 튜닝은 감으로 하면 안 된다."** `INFO` 명령으로 확인.

| 지표 | 필드 |
|---|---|
| Cache Hit Ratio | `keyspace_hits`, `keyspace_misses` |
| 메모리 | `used_memory`, `maxmemory`, fragmentation |
| Eviction | `evicted_keys` |
| 만료 key | `expired_keys` |
| 명령 처리량 | `instantaneous_ops_per_sec` |
| 느린 명령 | `SLOWLOG` |
| 연결 수 | `connected_clients` |
| 지연 | latency spike, p95, p99 |

> ⭐ **"중요한 것은 단일 지표가 아니라 흐름":**
> 배포 후 hit ratio가 떨어졌는가 · 특정 시간대에 miss가 증가하는가 ·
> **eviction 발생 뒤 DB 부하가 증가하는가** · **Redis 응답 시간은 짧은데 API latency가 긴가** ·
> hot key가 특정 shard를 압박하는가
>
> **네 번째가 [[Data SLA and observability]]의 "증상 지표 vs 원인 지표" 사고와 같다.**

## ⭐ 확장 — cluster로 바로 가지 마라

> **"Redis 성능 문제가 생겼다고 곧바로 cluster로 가는 것은 좋은 선택이 아닐 수 있다."**

**먼저 점검할 8가지:** 캐시 대상이 적절한가 · cache hit가 충분한가 · TTL이 적절한가 ·
eviction이 과도한가 · **hot key**가 있는가 · **large key**가 있는가 · pipelining이 필요한가 ·
Redis 호출 횟수가 너무 많은가.

| 방식 | 목적 | 대가 |
|---|---|---|
| **scale-up** | 더 큰 인스턴스 | 구조 단순, 운영 부담 낮음 |
| **Replica** | 읽기 분산 / 장애 대응 | **복제 지연과 failover 전략 필요** |
| **Cluster** | 샤딩으로 메모리·처리량 확장 | 운영 복잡성, **multi-key 제약**, shard 불균형 |

> **[[Distributed processing]]의 "필요한 축만 분산"과 같은 절제다.**

## ⚠️ Redis는 CP 시스템이 아니다

**강의 Part 4 Ch1-3은 Redis를 CP(일관성 + 파티션 내성)로 분류하고 "금융 거래·결제 시스템에 적합"
하다고 한다. 이 위키는 그 분류를 채택하지 않는다.**

**근거 — 같은 강의 안의 세 서술:**

| 위치 | 서술 |
|---|---|
| [[AI DE Course - Part4 Ch1 CAP theorem and system limits]] | Redis = CP, *"금융 거래, 결제 시스템 등 데이터의 정확성이 생명인 경우"* |
| [[AI DE Course - Part4 Ch2 Redis and the caching layer]] | 부적합 데이터 1번 = *"강한 정합성이 필요한 결제 상태"* |
| [[AI DE Course - Part4 Ch2 Caching strategies and TTL]] | Write-Behind — *"Redis 장애 시 DB에 반영되지 않은 데이터가 유실될 수 있다"*, *"정산·결제·주문 같은 강한 정합성 데이터에는 위험"* |

**Redis 기본 복제는 비동기이므로 [[Replication and consensus]]의 정의상 RPO > 0이다.**
failover 시 미전파 쓰기가 유실된다. **RPO > 0인 시스템을 "정확하지 않으면 응답하지 않는다"는 CP로
분류할 수 없다.** → [[CAP theorem]]

## 키 네이밍과 자료구조 매핑

```
user:session:{session_id}
product:detail:{product_id}
category:list
ranking:daily
recommend:user:{user_id}
feature:user:{user_id}:recent_activity
```

| 데이터 패턴 | 추천 자료구조 | 이유 |
|---|---|---|
| 세션 | String or Hash | TTL 관리 및 서버 간 공유 |
| 캐싱 | String (JSON) | RDB 쿼리 비용 절감 |
| 목록 | List or Set | 정적 목록의 빠른 반환 |
| 순위 | **Sorted Set** | 실시간 정렬 연산의 효율성 |
| 개인화/피처 | Hash or String | **무거운 연산 결과를 저장해 두었다가 즉시 서빙** |

> ⭐ **마지막 행이 곧 [[Feature store]]의 online store다.**

## 캐시로 쓸 것 / 쓰지 말 것

| 적합 | 부적합 |
|---|---|
| 반복 조회가 많다 | **강한 정합성이 필요한 결제 상태** |
| 원본 조회 비용이 크다 | **포인트 차감 같은 금전성 데이터** |
| TTL 동안 재사용 가능성이 높다 | **항상 최신이어야 하는 권한 데이터** |
| **약간의 지연된 데이터가 허용된다** | 한 번만 조회되고 다시 안 쓰이는 데이터 |
| key 기반 빠른 조회 가능 | 너무 큰 JSON blob |
| 데이터 크기가 적당 | **key cardinality가 커서 hit가 거의 안 나는 데이터** |

## 스트림 처리 상태 저장소로는?

[[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]]은 **"매 레코드 처리 시마다
외부 DB(Redis)에 접근하면 네트워크 지연으로 실시간성 확보 불가능"** 이라며 로컬 RocksDB를 권한다.

**모순이 아니라 접근 빈도의 차이다:**

| | 접근 패턴 | 적합 |
|---|---|---|
| **서빙 경로** | 요청당 수 회 | **Redis** (네트워크 홉 1회 감수) |
| **스트림 연산** | 레코드당 매번 | **로컬 embedded store** (RocksDB) |

## ⚠️ 강의가 다루지 않은 것

- **`SCAN`** — `KEYS *` 대신 쓰는 커서 기반 순회
- **Redis 7.x의 멀티스레드 I/O** — "싱글 스레드"를 무조건적 전제로 다룬다
- **Sentinel vs Cluster의 차이**, failover 절차
- **cache stampede 대응** (뮤텍스, TTL jitter) → [[Caching strategies]]에 정리
- **Redis Streams의 consumer group** — 자료구조로만 언급되고 소비 모델은 없다

## 관련 페이지

- [[Caching strategies]] — 전략·무효화·TTL
- [[Feature store]] — online store의 실제 구현
- [[CAP theorem]] — 위 분류 논란
- [[Replication and consensus]] — 비동기 복제와 RPO
- [[NoSQL]] — key-value 타입
- [[Distributed processing]] — hot key = 샤딩 키 hotspot
- [[Latency and throughput]] · [[Data SLA and observability]]

## 출처

- [[AI DE Course - Part4 Ch2 Redis and the caching layer]]
- [[AI DE Course - Part4 Ch2 Caching strategies and TTL]]

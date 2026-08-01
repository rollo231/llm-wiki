---
type: source
title: AI DE Course - Part4 Ch2 Redis and the caching layer
area: [data-engineering]
aliases: [Part4 Ch2-1,2, Redis 핵심 개념과 성능 최적화 패턴, Redis 캐싱 레이어]
tags: [data-engineering, course, fast-campus, redis, caching, in-memory, latency]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/Part 4_Ch 1~4.pdf (p67–110)"]
---

# AI DE Course - Part4 Ch2 Redis and the caching layer

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 4** Ch2 "초저지연 캐싱 아키텍처"의 소단원
**1 "Redis 핵심 개념과 성능 최적화 패턴"** + **2 "Redis 캐싱 레이어"**. 원본(로컬):
`raw/data-engineering/Part 4_Ch 1~4.pdf` **p67–110** (356p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> **두 소단원은 같은 대상을 반대 방향에서 본다.** 소단원 1은 **제품**(Redis는 무엇이고 무엇이
> 성능을 결정하나), 소단원 2는 **역할**(캐싱 레이어가 왜 필요하고 Redis가 왜 거기 맞나).
> 겹치는 슬라이드가 상당해서 한 페이지로 묶었다.

## 구성

소단원 1: `01 Redis란 · 02 Redis Cache · 03 Redis 성능을 위한 요소들 · 04 성능 지표 · 05 Redis 확장`
소단원 2: `01 캐싱 레이어 · 02 캐싱 레이어의 역할 · 03 Redis가 캐싱 레이어에 적합한 이유`

---

## Redis는 어떤 storage인가

> **"Redis는 관계형 데이터베이스처럼 행과 테이블 중심이 아님. key-value store 계열."**
>
> **"값 하나 꺼내는 캐시 레이어뿐 아니라, 데이터 구조를 메모리 안에 직접 올려두고 조작하는 저장소."**

### 자료구조 6종

| 구조 | 뜻 | 용도 |
|---|---|---|
| **String** | 가장 기본적인 값 저장 | 단순 캐시, 토큰, 카운터 |
| **Hash** | 하나의 key 안에 여러 field-value | 사용자 프로필, 세션 객체, 설정값 |
| **List** | 순서가 있는 값 목록 | 큐, 최근 활동 목록 |
| **Set** | 중복 없는 값 집합 | 태그, 권한, 사용자 그룹 |
| **Sorted Set** | 점수 기준 정렬 집합 | **랭킹**, 우선순위 큐, 시간 기반 정렬 |
| **Stream** | append-only 로그 형태 | 이벤트 기록, 메시지 스트림 |

Sorted Set 예: 유저A 100점 / B 250점 / C 150점 → 자동으로 `[A, C, B]` 정렬 →
**"점수 상위 10명 뽑아줘"** 같은 요청이 매우 빠름.

> **Stream이 "append-only log에 가까운 자료구조"라고 명시되는 게 눈에 띈다.** Ch3의 retained log
> 중심 브로커([[Apache Kafka]])와 같은 모델이 Redis 안에도 있다는 뜻인데, **강의가 이 연결을
> 만들지 않는다.**

## Redis가 빠른 이유

디스크 기반 저장소는 데이터를 읽기 위해 파일시스템 → 디스크 I/O → 버퍼 캐시 → 쿼리 실행 계획 같은
여러 단계를 거친다. Redis는 주로 **메모리 안의 key와 자료구조를 직접 접근**한다.

> **"하지만 정말 빠른 지연 시간을 위해서는 여러 구성 요소에 대해 신경 쓰고 조합해야 한다."**

이 단서가 소단원 1의 나머지 전부다.

## ⭐ Redis 성능을 결정하는 9가지 요소

| # | 요소 | 핵심 |
|---|---|---|
| 1 | **자료구조 선택** | 단순 넣고 빼기는 String이 빠름. **특정 필드만 수정하는 객체형은 Hash가 메모리·속도 모두 유리** |
| 2 | **명령어 시간 복잡도** | ⭐ **Redis는 싱글 스레드.** 하나의 명령어가 오래 걸리면 그동안 다른 모든 요청이 **Blocking** |
| 3 | **네트워크 왕복 횟수** | Pipelining |
| 4 | **키 크기와 값 크기** | 긴 키 이름은 그 자체로 메모리 점유. 수십 MB JSON은 대역폭·처리 시간 잠식 |
| 5 | **동시 요청 패턴** | 수만 개의 연결 유지 자체가 메모리 소모 → **Connection Pool 필수** |
| 6 | **hot key 여부** | 특정 키에 트래픽 집중 |
| 7 | **eviction 발생 여부** | 삭제 대상 선정(LRU/LFU)과 삭제가 CPU 소모 |
| 8 | **persistence 설정** | RDB / AOF |
| 9 | **replication 또는 cluster 구성** | 복제 부하, multi-key 연산의 추가 네트워크 비용 |

### 2. 시간 복잡도 — 싱글 스레드의 함정

| | 명령어 |
|---|---|
| **O(1)** | `GET`, `SET`, `HGET` — 데이터 양과 상관없이 즉시 |
| **O(N)** | `KEYS *`, `HGETALL`, `SMEMBERS` — 데이터 개수에 정비례 |

> ⭐ **"운영 환경에서 O(N) 명령어를 잘못 사용하면 서비스 전체가 멈추는 '장애'로 이어질 수 있다."**
>
> **싱글 스레드 + O(N) = 전체 정지.** 이 조합이 Redis 운영의 1번 함정이다.

### 3. Pipelining — RTT가 진짜 병목

> **"Redis의 명령어 처리 속도는 초당 수십만 건이지만 네트워크 왕복 시간(RTT) 때문에 실제 성능이
> 제한된다. 1,000번의 SET을 Redis는 1ms로 처리 가능하지만 네트워크 대기 시간은 1,000ms."**

**Pipeline** = 여러 명령을 모아 한 번의 왕복으로 처리. 응답 대기 없이 다음 명령을 즉시 전송 →
시스템 콜 횟수 최소화.

| 장점 | 단점 |
|---|---|
| RTT의 드라마틱한 감소, CPU 부하 경감 | **메모리 압박, 원자성(Atomicity) 미보장** |

> **"원자성 미보장"을 명시하는 게 좋다.** 파이프라인은 트랜잭션(`MULTI/EXEC`)이 아니다 —
> 중간에 실패해도 앞의 명령은 이미 적용된다.

### 6. Hot Key

> **Hot Key: 수많은 키 중 특정 몇 개(예: '실시간 1위 상품')에만 트래픽이 90% 이상 몰리는 현상.**

Redis를 클러스터로 구성해 서버를 여러 대로 나눠도 **특정 키는 물리적으로 한 대의 서버에만 존재**
하므로, 해당 서버에만 과부하가 걸린다.

> ⭐ **이것이 [[NoSQL]](Part 3)의 "파티션 키가 시스템을 결정한다"와 Ch1-2의 "샤딩 키 hotspot"과
> 정확히 같은 문제다.** 세 파트에서 세 번 나오는데 강의가 한 번도 잇지 않는다.

### 8. Persistence — 두 방식 모두 대가가 있다

| | 방식 | 대가 |
|---|---|---|
| **RDB** (Snapshotting) | 순간적으로 메모리 상태를 복사 | 자식 프로세스 생성(**Fork**) → 성능 저하 가능 |
| **AOF** (Append Only File) | 모든 쓰기 명령을 기록 | 디스크 I/O 발생. **fsync 옵션에 따라 성능 vs 안전성 트레이드오프** |

## 성능 지표 — 감으로 튜닝하지 않기

> **"Redis 튜닝은 감으로 하면 안 됨."**

| 지표 | 확인 항목 |
|---|---|
| Cache Hit Ratio | `keyspace_hits`, `keyspace_misses` |
| 메모리 | `used_memory`, `maxmemory`, fragmentation |
| Eviction | `evicted_keys` |
| 만료 key | `expired_keys` |
| 명령 처리량 | `instantaneous_ops_per_sec` |
| 느린 명령 | `SLOWLOG` |
| 연결 수 | `connected_clients` |
| 지연 시간 | latency spike, p95, p99 |

`INFO` 명령이 서버 상태·통계를 제공한다.

> ⭐ **"중요한 것은 단일 지표가 아니라 흐름."**
>
> - 배포 후 hit ratio가 떨어졌는가
> - 특정 시간대에 miss가 증가하는가
> - **eviction이 발생한 뒤 DB 부하가 증가하는가**
> - **Redis 응답 시간은 짧은데 API latency가 긴가**
> - hot key가 특정 shard를 압박하는가
>
> **"Redis 운영은 캐시 지표, 애플리케이션 지표, 원본 DB 지표를 함께 봐야 한다."**

**네 번째 항목이 특히 좋다** — Ch5의 "증상 지표와 원인 지표 분리"와 같은 사고이고,
[[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]에서 GPU 버전으로 반복된다.

## ⭐ 확장 — cluster로 바로 가지 마라

> **"Redis 성능 문제가 생겼다고 곧바로 cluster로 가는 것은 좋은 선택이 아닐 수 있다."**

먼저 점검할 것 8가지: 캐시 대상이 적절한가 · cache hit가 충분한가 · TTL이 너무 짧거나 긴가 ·
eviction이 과도한가 · hot key가 있는가 · large key가 있는가 · pipelining이 필요한가 ·
Redis 호출 횟수가 너무 많은가.

| 방식 | 목적 | 대가 |
|---|---|---|
| **scale-up** | 더 큰 메모리·CPU 인스턴스 | 구조 단순, 운영 부담 낮음 |
| **Replica** | 읽기 분산 또는 장애 대응 | **복제 지연과 failover 전략 필요** |
| **Cluster** | 데이터 샤딩으로 메모리·처리량 확장 | 운영 복잡성, **multi-key 제약**, shard 불균형 |

> **Ch1-2의 "필요한 축만 분산"과 정확히 같은 논지다** — 읽기 확장은 replica, 그 이상이 필요할 때만
> cluster. **이번에는 같은 파트 안이라 연결이 자연스럽다.**

---

## 소단원 2 — 캐싱 "레이어"로서의 관점

### 실시간 서비스의 요청은 단순하지 않다

한 번의 사용자 요청 안에 들어가는 조회들: 사용자 정보 · 상품 정보 · 추천 결과 · 권한 확인 ·
구독 상태 · 랭킹 · **피처 조회** · 이벤트 상태.

DB 직접 조회 시 발생하는 문제: 원본 DB 부하 증가 · 반복 조회 비용 · 복잡한 join/계산으로 인한 지연 ·
트래픽 급증 시 **DB connection 고갈** · 피크 시간대 p95/p99 악화.

> **"피처 조회"가 목록에 들어있는 게 중요하다.** [[AI DE Course - Part2 Ch3 Serving pipeline]]의
> **"Feature 조회가 병목"** 이 여기서 캐싱 문제로 연결된다. [[Feature store]]의 online store가
> 사실상 이 레이어다.

### 캐시가 효과적인 상황 — 4조건

1. 같은 데이터가 **반복 조회**된다
2. **원본 조회 비용이 크다**
3. **약간의 지연된 데이터가 허용된다**
4. TTL 동안 재사용될 가능성이 높다

> ⭐ **3번이 캐시 도입의 진짜 조건이다.** 1·2번만 보고 도입했다가 정합성 문제로 되돌리는 게 흔한
> 실패다.

### ⭐ 캐시는 원본을 대체하지 않고 보호한다

> **"원본 저장소는 데이터의 기준점(Source of Truth). 캐시는 자주 쓰는 데이터를 빠르게 반환하기 위한
> 보조 계층."**

캐싱 레이어의 역할 셋:

1. **응답 시간 단축**
2. **원본 저장소 부하 감소** — 반복 조회를 캐시에서 처리해 DB QPS와 connection 사용량 감소
3. **트래픽 급증 완충** — 이벤트·배포·캠페인·추천 피드 노출처럼 요청이 몰리는 상황에서 원본 보호

### 캐시의 위험성 5가지

- 오래된 데이터 반환
- 캐시와 원본 저장소 불일치
- **캐시 만료 시 원본 저장소 폭주** (thundering herd)
- hot key 집중
- 낮은 cache hit로 인한 효과 부족

> ⭐ **"캐싱 전략은 속도만의 문제가 아님. 성능·신선도·안정성·운영비용의 균형 문제."**

### Redis에 적합한 / 부적합한 데이터

| 적합 | 부적합 |
|---|---|
| 반복 조회가 많다 | **강한 정합성이 필요한 결제 상태** |
| 원본 조회 비용이 크다 | **포인트 차감 같은 금전성 데이터** |
| TTL 동안 재사용 가능성이 높다 | **항상 최신이어야 하는 권한 데이터** |
| 약간의 지연된 데이터가 허용된다 | 한 번만 조회되고 다시 쓰이지 않는 데이터 |
| key 기반으로 빠르게 조회 가능 | 너무 큰 JSON blob |
| 데이터 크기가 너무 크지 않다 | **key cardinality가 지나치게 커서 hit가 거의 안 나는 데이터** |

> ⚠️ **"강한 정합성이 필요한 결제 상태"를 부적합으로 분류하는 이 슬라이드가,
> [[AI DE Course - Part4 Ch1 CAP theorem and system limits]]에서 Redis를 CP(금융 거래·결제 시스템에
> 적합)로 분류한 것과 정면으로 충돌한다.** 같은 파트 안의 모순이다.

### 키 네이밍과 자료구조 매핑

```
user:session:{session_id}
product:detail:{product_id}
category:list
ranking:daily
recommend:user:{user_id}
feature:user:{user_id}:recent_activity
```

| 데이터 패턴 | 키 예시 | 추천 자료구조 | 핵심 이유 |
|---|---|---|---|
| 세션 | `user:session:*` | String or Hash | TTL 관리 및 서버 간 공유 |
| 캐싱 | `product:detail:*` | String (JSON) | RDB 쿼리 비용 절감 |
| 목록 | `category:list` | List or Set | 정적 목록의 빠른 반환 |
| 순위 | `ranking:daily` | **Sorted Set** | 실시간 정렬 연산의 효율성 |
| 개인화/특징 | `feature:user:*` | Hash or String | **무거운 연산 결과를 저장해 두었다가 즉시 서빙** |

> **마지막 행이 곧 [[Feature store]]의 online store다.** 강의가 "feature"라는 단어를 쓰면서도
> Part 2의 Feature Store 챕터와 연결하지 않는다.

## 기존 페이지와의 대조

- **새 concept:** [[Caching strategies]] (전략 상세는 다음 소단원)
- **새 entity:** [[Redis]]
- **[[Feature store]] 보강 필요** — online store의 물리적 구현이 사실상 Redis라는 점이 여기서
  구체화된다. Part 2 Ch5는 "offline/online 두 스토어"까지만 말했다.
- **[[AI DE Course - Part2 Ch3 Serving pipeline]]의 "Feature 조회가 병목"** 에 대한 대응책이 여기 있다.
- ⚠️ **파트 내부 모순 2건** (위 참조): Redis의 CP 분류, 결제 데이터 적합성.

## 자료 품질

- ✅ 성능 요소 9종이 **구체적이고 실무적** — 특히 싱글 스레드 + O(N), Pipeline의 원자성 미보장
- ✅ 지표 목록이 실제 Redis `INFO` 필드명(`keyspace_hits`, `evicted_keys`, `SLOWLOG`)
- ✅ **"cluster로 바로 가지 마라"** 는 절제 — Ch1-2의 "단일 서버부터"와 일관
- ✅ Redis 공식 자료를 근거로 prefetching 설명
- ⚠️ **중복 슬라이드 다수**: p70/p71(자료구조), p74/p75(cache-aside), p94/p95(확장),
  p109/p110(부적합 데이터) — 각각 완전 동일
- ⚠️ **p87의 섹션 헤더가 "02. Redis Cache"로 잘못 붙어 있다** (내용은 03의 Hot Key)
- ⚠️ **"초당 수십만 건"** 등 처리량 수치에 벤치마크 조건(파이프라인 여부, 값 크기, 인스턴스)이 없음
- ⚠️ Redis 7.x 이후의 멀티스레드 I/O, `SCAN`(KEYS 대안), `CLIENT NO-EVICT` 같은 **최신 완화책이
  전혀 없다** — "싱글 스레드"를 무조건적 전제로 다룬다

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Caching strategies]] · [[Feature store]] · [[Latency and throughput]] · [[NoSQL]] ·
  [[Distributed processing]]
- 도구: [[Redis]] · [[Apache Kafka]]
- 앞: [[AI DE Course - Part4 Ch1 HA replication and consensus]]
- 다음: [[AI DE Course - Part4 Ch2 Caching strategies and TTL]]

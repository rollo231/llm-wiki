---
type: concept
title: Stream processing semantics
area: [data-engineering]
aliases:
  - Windowing
  - Tumbling window
  - Sliding window
  - Session window
  - Watermark
  - Event time
  - Processing time
  - Stateful processing
  - Checkpointing
  - Exactly-once
  - 윈도우
  - 워터마크
  - 상태 관리
tags: [data-engineering, streaming, flink, spark, windowing, state, exactly-once]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Ch4-5,6 Stream processing engines]]"]
---

# Stream processing semantics

[[Apache Kafka]]가 데이터를 실어 오면, 처리는 스트림 프로세서(Flink·Spark Streaming)가 한다.
이 페이지는 **그 처리가 배치와 근본적으로 다른 이유**와 그 차이를 다루는 메커니즘이다.

## 세 가지 근본 난관

| | 배치 | 스트림 |
|---|---|---|
| 데이터 | **유한(bounded)** — 다 모인 뒤 처리 | **무한(unbounded)** — 시작은 있고 끝이 없다 |
| 순서 | 모두 준비된 후 처리 | 도착 순서 예측 불가 |
| 상태 | 잡이 끝나면 사라져도 됨 | 24/365 유지되어야 함 |

1. **무한성** — 전체를 다 모아 처리할 수 없으니 **적절한 시점에 결과를 내야 한다** → 윈도우.
2. **비동기성** — 생성 시간(event time)과 도착 시간(processing time)이 다르다 → 워터마크.
3. **상태 내구성** — 장애가 나도 계산 중간값을 잃지 않아야 한다 → 체크포인팅.

## 윈도우 — 무한한 흐름에 시간의 틀을 씌우기

분할 기준은 셋: **시간**(가장 일반적) · **개수**("100개 찰 때마다", 소요 시간 예측 불가) ·
**세션**(활동 기준).

### Tumbling Window (텀블링)

겹치지 않는 고정 크기. 하나의 데이터는 **오직 하나의 윈도우에만** 속한다.

- 중복 처리가 없어 **연산 비용이 가장 저렴하고 구현이 가장 간단**하다. 배치와 가장 비슷하다.
- ⚠️ **경계의 함정** — 패턴이 `12:04:59 ~ 12:05:01`에 걸쳐 발생하면 두 윈도우로 쪼개져 전체 맥락을
  놓친다.

### Sliding Window (슬라이딩)

**크기(size)** 와 **이동 간격(slide)** 두 파라미터를 갖고, 윈도우끼리 겹친다. 하나의 데이터가
여러 윈도우에 동시에 포함된다(중복 연산).

- 이동평균 같은 **추세 관찰**에 최적.
- "최근 5분간 에러율 급증" 같은 **실시간 경보**에 필수.

### Session Window (세션)

기계적 시간이 아니라 **활동이 이어지는 구간**을 하나로 묶는다. 일정 시간(session gap) 이상 활동이
없으면 종료. **시작·종료가 고정되어 있지 않고 사용자마다 크기가 제각각**이다.

단순 집계를 넘어 "사용자의 의도와 흐름"을 보는 데 쓴다 — 평균 체류 시간, 이탈 직전 행동,
플레이 세션당 획득 경험치.

## Event time vs Processing time

| | Event Time | Processing Time |
|---|---|---|
| 기준 | 데이터가 **실제로 발생**한 시각 (기기 타임스탬프) | 엔진에 **도착해 처리되는** 시각 (wall-clock) |
| 장점 | 네트워크 지연과 무관하게 **사건의 실제 순서** 반영 → 정확한 분석 | 지연이 적고 구현이 간단 |
| 단점 | 늦게 오는 데이터를 기다려야 한다 | 늦게 도착한 데이터로 **분석 결과가 왜곡** |

### Watermark — 그 격차를 관리하는 척도

**"12:00시까지의 데이터는 이제 다 도착했다"** 를 엔진에게 알려주는 표식. 이걸로 엔진이 늦게
도착하는 데이터를 더 기다릴지 결정한다. event time 처리의 핵심 장치다.

## Late Data 처리 전략 3종

| 전략 | 하는 일 | 대가 | 유스케이스 |
|---|---|---|---|
| **Drop** | 허용 시간(allowed lateness) 초과분을 버린다 | 구현 최단·최저비용 / **데이터 유실** | 실시간 대시보드 |
| **Update** | 이미 저장된 결과를 재계산해 갱신 | 정확성 확보(eventually correct) / **DB upsert 필요** | 정산·리포트 갱신 |
| **Side Output** | 늦은 데이터만 별도 경로(dead letter queue)로 빼둔다 | 유실 없음 + 메인 로직 보호 / **별도 보정 파이프라인 필요** | 로그 아카이빙·재처리 |

**혼합도 된다** — "1시간까지는 Update, 그 이후는 Side Output".

## Stateful Processing

| | Stateless | Stateful |
|---|---|---|
| 처리 | 들어온 데이터 하나만 독립적으로 | 과거의 결과·패턴을 저장해 맥락으로 사용 |
| 예시 연산 | Filter · Map · Parsing | Window · Join · Aggregation |
| 확장 | 매우 쉽다 | 상태를 같이 옮겨야 한다 |

### State의 종류

- **Keyed State** (가장 흔함) — 특정 Key 기준으로 파티셔닝된 상태. 각 Key가 독립적인 상태를 가져
  병렬 처리가 쉽다. 예: 사용자별 장바구니, 센서별 최근 1시간 평균 온도.
- **Operator State** — Key와 무관하게 연산자 인스턴스 단위로 관리. 예: Kafka consumer의 offset,
  파일 소스의 읽기 위치.

### State Backend — 어디에 두나

| | JVM Heap Memory | Embedded RocksDB |
|---|---|---|
| 속도 | 가장 빠름 | 느림 (직렬화 비용) |
| 한계 | 메모리 용량(OOM) — 대용량 부적합 | **테라바이트급 상태**를 안정적으로 관리 |

개발자는 "State 저장해줘"라고 선언만 하고, 메모리/디스크 관리는 엔진이 한다.

## Fault Tolerance — Checkpointing 4단계

```
1. State Tracking → 2. Snapshot → 3. Persist → 4. Recovery
   (State + Kafka      (일정 주기,    (HDFS·S3에      (최근 체크포인트
    offset 추적)        예: 10초)      비동기 저장)      로드 후 replay)
```

메모리의 State는 휘발성이므로, 주기적으로 **전체 시스템 상태를 순간 포착해 일관된 이미지**로
만들어 영구 저장소에 비동기로 쓴다. 장애 시 가장 최근 체크포인트를 로드해 그 시점부터 재처리한다.

**State + offset을 함께 스냅샷하는 것이 exactly-once의 핵심이다** — 상태만 복원하고 offset이
어긋나면 중복·유실이 난다.

## Flink vs Spark Streaming

| | **Apache Flink** | **Spark Streaming** |
|---|---|---|
| 처리 모델 | **Native Streaming** — 건별(row-by-row) 즉시 | **Micro-batching** — 초 단위로 묶어서 |
| Latency | 밀리초 | 초 |
| Throughput | — | 높고 안정적 |
| 상태 관리 | fine-grained 제어 | Spark RDD / SQL 기반 |
| 내결함성 | 분산 스냅샷(Chandy-Lamport)으로 exactly-once | RDD lineage 재계산 + WAL + checkpoint |
| 강점 | Event time + Watermark로 late data 정밀 보정 | **배치와 스트리밍에 동일한 코드·API**(DataFrame/SQL) |
| 운영 복잡도 | 높음 (세밀한 설정 필요) | 중간 (접근성 높음) |

> **선택 가이드:** 1초 미만 초저지연이 필수면 **Flink**, 대용량 처리 + 배치 코드 재사용이면 **Spark**.

## 링크
- 실어 오는 층: [[Apache Kafka]] — offset이 여기서 상태의 일부가 된다
- 왜 트레이드오프인가: [[Latency and throughput]] — 마이크로배치가 중간지대인 이유
- 도구 지도: [[Batch and stream processing]]
- 출처: [[AI DE Course - Ch4-5,6 Stream processing engines]]

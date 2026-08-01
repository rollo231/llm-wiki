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
  - Ingestion time
  - Allowed lateness
  - Append Upsert Update
tags: [data-engineering, streaming, flink, spark, windowing, state, exactly-once, watermark, event-time]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Ch4-5,6 Stream processing engines]]", "[[AI DE Course - Part4 Ch3 Event time watermarks and windows]]", "[[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]]"]
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

**Part 4가 축을 하나 더 준다 — 배포 형태.** [[Apache Flink]]와 [[Apache Spark]]는 별도 클러스터가
필요하지만 **Kafka Streams는 애플리케이션 안에서 동작하는 라이브러리**다. "Kafka to Kafka
파이프라인"과 마이크로서비스 내부 실시간 로직에는 클러스터를 세울 이유가 없다.

---

# Part 4가 채운 것

## ⭐ 세 개의 시각 — 수집 시각이 따로 있다

Part 1은 event time / processing time 둘로 갈랐다. **Part 4는 셋으로 나눈다:**

| 시각 | 뜻 | 예 |
|---|---|---|
| **발생 시각** (event time) | 이벤트가 실제로 일어난 순간 | 사용자가 결제 버튼을 누른 순간 |
| ⭐ **수집 시각** (ingestion time) | **브로커나 시스템이 받아 기록한 순간** | **Kafka 브로커가 메시지를 로그에 기록한 순간** |
| **처리 시각** (processing time) | 처리 엔진의 연산자가 계산한 순간 | — |

> ⭐ **수집 시각을 분리하는 것이 실무 디버깅의 열쇠다.** "브로커까지는 왔는데 엔진이 안 읽었다"와
> "브로커에도 안 왔다"를 구분해야 한다. [[Data SLA and observability]]의
> **`source ingestion lag` vs `stream processing lag`** 지표 분리가 정확히 이 구분이다.

**설계 순서 3단계:** ① 어떤 시간을 기준으로 계산할지 → ② 늦게 들어온 데이터를 어떻게 처리할지 →
③ **시간 구간 결과를 언제 확정할지.**

### 같은 데이터, 다른 답

| 이벤트 | 실제 발생 | 시스템 도착 |
|---|---|---|
| 결제 A | 10:02 | 10:02 |
| **결제 B** | **10:04** | **10:12** |
| 결제 C | 10:07 | 10:07 |

`10:00~10:10 결제 건수` → **처리 시각 기준 2건 / 이벤트 발생 시각 기준 3건.**

## ⭐⭐ 역할 3분할 — 넣기 / 닫기 / 내보내기

Part 1은 윈도우와 워터마크를 나란히 놓았다. **Part 4는 셋으로 쪼갠다 — 각각 독립적으로 설계·튜닝
할 수 있다는 게 요점이다.**

| 장치 | 질문 |
|---|---|
| **윈도우** | 이 이벤트를 **어느 계산 구간에 넣을 것인가** |
| **워터마크** | 이 시간 구간을 **언제 닫을 것인가** |
| ⭐ **출력 시점 규칙** | 중간 결과를 낼 것인가 / 최종 결과만 낼 것인가 / **늦게 온 데이터가 오면 다시 낼 것인가** |

## 워터마크는 정답 시계가 아니라 절충 기준

> ⭐ **"모든 데이터가 도착했다는 절대 보장이 아니다. 더 기다릴 것인가 결과를 낼 것인가의 기준이고,
> 정확성·지연·상태 비용 사이의 절충이다."**

**Spark의 정확한 보장:**

> **"설정한 지연 시간보다 덜 늦은 데이터는 집계 반영이 보장된다. 그보다 더 늦은 데이터는 반영될
> 수도 있고 안 될 수도 있다."**

> ⭐ **워터마크는 하한 보장(at-least)이지 상한 배제가 아니다.** "그 이후는 무조건 버림"으로
> 이해하는 것이 흔한 오해다.

**세 번째 역할이 비용 장치다** — 워터마크는 시간 구간을 닫고, 늦은 데이터를 판정하고,
⭐ **오래된 상태를 정리할 기준**을 준다. 워터마크가 없으면 상태가 무한히 자란다.

## ⭐ 결과 출력과 싱크 설계

늦은 데이터가 도착해 결과가 2건 → 3건으로 바뀔 때:

> ⭐ **"3건을 새 행으로 추가할 것인가, 기존 2건을 3건으로 갱신할 것인가, 2건과 3건을 모두
> 이벤트로 남길 것인가?"**

| 방식 | 동작 | 적합한 저장소 |
|---|---|---|
| **Append** | 확정된 결과만 추가 | 파일 저장소, 로그성 테이블. **결과 지연 가능** |
| **Upsert** | 같은 키의 결과를 덮어씀 | 실시간 대시보드, 집계 테이블. **윈도우 키와 집계 키 설계가 중요** |
| **Update** | 변경된 결과만 출력 | 집계 테이블 갱신. **싱크가 업데이트를 지원해야 함** |

> ⭐ **스트리밍 정합성은 엔진만의 문제가 아니라 싱크의 성질과 함께 정해진다.**
> 이것이 아래 exactly-once 경고의 "특정 sink 안에서"의 뜻이다.

## ⚠️ exactly-once의 범위 — Part 1 서술을 정정한다

위 § Checkpointing 절은 "State + offset을 함께 스냅샷하는 것이 exactly-once의 핵심"이라고 했다.
**맞지만 충분조건이 아니다.**

> ⚠️ **"exactly-once를 '외부 세계 전체에서 한 번만 처리된다'는 뜻으로 받아들이면 위험하다.
> 실제로는 특정 시스템 경계, 특정 조건, 특정 sink, 특정 transaction protocol 안에서 성립하는
> 경우가 많다."** ([[Message broker]])

**성립 조건 셋 — 하나라도 없으면 exactly-once가 아니다:**

1. **재읽기 가능한 입력 계층** — 복구 시 저장된 offset부터 다시 읽어야 하므로
   [[Apache Kafka]] 같은 retained log가 필요하다
2. **체크포인트** — 상태 + 입력 위치를 **함께** 저장
3. ⭐ **중복에 안전한 출력 저장소** — upsert 또는 트랜잭션 sink

> **1번이 "엔진만 있으면 브로커는 불필요하다"는 오해의 답이다.**
>
> **실무의 기본은 여전히 at-least-once + idempotent consumer다** — 장치 7종은 [[Message broker]].

## 설정값을 무엇으로 정하나

| 설정 | 결정 기준 |
|---|---|
| **윈도우 크기** | 비즈니스 지표의 시간 단위 · 결과 확인 주기 · **상태 크기와 계산 비용** |
| **이동 간격** | 갱신 주기 · **중복 계산 비용** · 대시보드 표시 주기 |
| **세션 간격** | "활동이 끊겼다"의 정의 · 도메인별 평균 행동 간격 · **과분할과 과병합의 균형** |
| **워터마크 지연** | ⭐ **실제 데이터 지연 분포** · 늦은 데이터 허용 범위 · 결과 지연 허용치 · 상태 저장 비용 |

> ⭐ **워터마크 지연을 감으로 정하지 말고 도착 지연의 p95/p99를 재서 정하라**는 뜻인데,
> ⚠️ **강의는 "분포를 어떻게 재는가"를 말하지 않는다.**

## Event time을 요구하는 것들

**event time은 선택이 아니라 아래 셋의 전제 조건이다:**

| 요구하는 것 | 왜 |
|---|---|
| ⭐ **[[Lambda and Kappa architecture]]의 카파** | 로그를 다시 읽어도 원래 결과가 나와야 한다. 처리 시각 기준이면 어제 사건이 오늘 구간에 들어간다 |
| **정산·분석·모델 학습 데이터** | *"늦게 온 데이터를 버리면 학습셋이 왜곡된다"* → [[Data drift and training-serving skew]]의 skew 패턴 1 |
| **모델 품질 모니터링** | `prediction_time`과 `label_event_time`을 분리해야 한다 → [[Data SLA and observability]] |

## 이론적 뿌리

**event time 문제는 [[Distributed system limits]]의 "전역 시계 부재"(Lamport)의 응용 계층
버전이다** — *"두 사건 중 무엇이 먼저 일어났는지 말하는 것이 때때로 불가능하다"*.
세 계층 모두 **"시각을 데이터에 실어 보내고, 언제까지 기다릴지 규칙을 정한다"** 는 같은 해법을 쓴다.

## ⚠️ 여전히 빈 곳

- ⭐ **워터마크 생성 방식** — bounded-out-of-orderness, periodic vs punctuated,
  **여러 파티션의 워터마크를 어떻게 합치는가(min 취하기)**
- ⭐ **idle partition 문제** — 한 파티션이 조용하면 워터마크가 안 올라가 전체 집계가 멈춘다.
  **실무에서 가장 자주 만나는 함정인데 강의에 없다**
- **워터마크 지연을 정하기 위한 지연 분포 측정 방법**
- **savepoint vs checkpoint** — 버전 업그레이드 시 핵심
- **two-phase commit sink** — exactly-once sink의 실제 구현

## 링크
- 실어 오는 층: [[Apache Kafka]] · [[Message broker]] — offset이 여기서 상태의 일부가 된다
- 엔진: [[Apache Flink]] · [[Apache Spark]]
- 왜 트레이드오프인가: [[Latency and throughput]] — 마이크로배치가 중간지대인 이유
- 도구 지도: [[Batch and stream processing]]
- 아키텍처: [[Lambda and Kappa architecture]] — 카파가 event time을 요구한다
- 이론: [[Distributed system limits]] — 전역 시계 부재
- 운영: [[Data SLA and observability]]
- 출처: [[AI DE Course - Ch4-5,6 Stream processing engines]] ·
  [[AI DE Course - Part4 Ch3 Event time watermarks and windows]] ·
  [[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]]

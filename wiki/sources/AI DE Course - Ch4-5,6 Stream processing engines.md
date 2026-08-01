---
type: source
title: AI DE Course - Ch4-5,6 Stream processing engines
area: [data-engineering]
aliases: [CH04-5 6 실시간 처리 엔진, Flink Spark Streaming 개념]
tags: [data-engineering, course, fast-campus, flink, spark, windowing, watermark, state]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/CH04-5, 6. 실시간 데이터 처리 엔진의 역할 (Flink, Spark Streaming 개념) 1, 2.pdf"]
---

# AI DE Course - Ch4-5,6 Stream processing engines

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 CH04-5,6**
"실시간 데이터 처리 엔진의 역할 (Flink, Spark Streaming 개념) (1)(2)". 원본(로컬):
`raw/data-engineering/CH04-5, 6. 실시간 데이터 처리 엔진의 역할 (Flink, Spark Streaming 개념) 1, 2.pdf`
(16p). 강의 홈: [[AI Data Engineering (Fast Campus course)]].

**Part 1의 마지막 기술 챕터이고, [[Batch and stream processing]]이 "Flink가 대표"라고만 적어둔
자리에 실제 의미론을 채운다.** 개념 정리는 [[Stream processing semantics]]에 옮겼다.

## 이 덱의 논지 — 스트리밍은 왜 어려운가

배치와 다른 세 가지 **본질적** 난관을 세운다. 도구 선택 이전의 문제라는 것이 논지다.

| | 배치 | 스트림 |
|---|---|---|
| 데이터 | **유한(bounded)** — 모든 데이터가 준비된 후 처리 | **무한(unbounded)** — 시작은 있고 끝이 없다 |
| 순서 | 보장됨 | **도착 순서 예측 불가** |
| 상태 | 잡이 끝나면 사라져도 됨 | 24/365 유지 + 장애 복구 필요 |

1. **무한성** — 전체를 다 모아 처리할 수 없으니 적절한 시점에 결과를 도출해야 한다 → **윈도우**
2. **비동기성** — 생성 시간(event time)과 도착 시간(processing time)이 다르다. 네트워크 지연으로
   뒤죽박죽 도착하는 순서를 어떻게 맞추나 → **워터마크**
3. **상태 보존** — 멈추지 않는 시스템에서 장애가 나도 중간값(state)을 잃지 않고 정확히 복구해야
   한다 → **체크포인팅**

**세 난관과 세 해법이 1:1로 대응하는 구조가 이 덱의 설계다.**

## 윈도우 3종 — 트레이드오프까지

| | Tumbling | Sliding | Session |
|---|---|---|---|
| 겹침 | 없음 | **있음** (중복 연산) | 없음 |
| 크기 | 고정 | 고정 (size + slide 2개 파라미터) | **동적** — 사용자마다 다르다 |
| 비용 | **가장 저렴, 구현 가장 간단** | 중복 처리로 높다 | — |
| 약점 | **경계의 함정** — 패턴이 `12:04:59~12:05:01`에 걸치면 두 윈도우로 쪼개져 맥락을 놓친다 | — | 종료 시점을 미리 알 수 없다 |
| 쓰는 곳 | 배치와 유사한 정기 집계 | 이동평균 추세, **"최근 5분간 에러율 급증" 경보** | UX·맥락 분석 |

- 분할 기준은 셋: **시간**(가장 일반적) · **개수**("100개 찰 때마다" — ⚠️ 시간이 얼마나 걸릴지
  예측 불가) · **세션**(활동 기준, session gap).
- 세션 윈도우가 답하는 질문: 한 번 방문하면 평균 얼마나 머무르나 / 이탈 직전에 어떤 행동을 했나 /
  플레이 세션당 획득 경험치.

## Event Time vs Processing Time, 그리고 워터마크

| | Event Time | Processing Time |
|---|---|---|
| 기준 | 데이터가 **실제로 발생**한 시각 (기기 타임스탬프) | 엔진에 **도착해 처리되는** 시각 (wall-clock) |
| 장점 | 네트워크 지연·서버 부하와 무관하게 **사건의 실제 순서** 반영 → 정확한 분석 | 지연 적고 구현 간단 |
| 단점 | 늦게 오는 데이터를 기다려야 한다 | 늦게 도착한 데이터로 **분석 결과 왜곡** |
| 성질 | Deterministic · Real-World | Low Latency · System-Dependent |

**해법: Watermark** — event time과 processing time 사이의 격차(lag)를 관리하는 척도.
**"12:00시까지의 데이터는 이제 다 도착했다"** 를 엔진에게 알려주어, 늦게 도착하는 데이터를
기다릴지 결정하게 한다.

## Late Data 처리 3전략 — 이 덱의 가장 실용적인 부분

| | Drop | Update | Side Output |
|---|---|---|---|
| 비유 | "수업 끝났어, 돌아가." | "어? 너 왔어? 고쳐줄게." | "일단 넌 따로 모아둘게." |
| 하는 일 | allowed lateness 초과분을 버린다 | 저장된 결과를 재계산해 갱신 | 늦은 데이터만 별도 경로(dead letter queue)로 |
| 얻는 것 | 구현 최단·최저비용 | 정확성(eventually correct) | 유실 없음 + 메인 로직 보호 |
| 잃는 것 | **데이터 유실 (정확도↓)** | DB upsert 지원 필요 | **별도 배치 보정 파이프라인 필요** |
| 쓰는 곳 | 실시간 대시보드 | 정산·리포트 갱신 | 로그 아카이빙·재처리 |

> **Tip: 혼합 전략도 가능하다** — "1시간까지는 Update하고, 그 이후는 Side Output으로 뺀다."

## Stateful Processing

| Stateless | Stateful |
|---|---|
| 들어온 데이터 하나만 독립 처리 | 과거의 결과·패턴을 저장해 맥락으로 사용 |
| "기억력이 없어(붕어 기억력) 구조가 단순" | 데이터 간 의존성이 존재 |
| **확장이 매우 쉽다** | 상태를 함께 옮겨야 한다 |
| Filter · Map · Parsing | Window · Join · Aggregation |

**핵심 과제: 메모리의 상태는 휘발성이다.** 서버 장애 시에도 유실 없이 복구하는 메커니즘이 필수.

### State 2종과 Backend 2종

- **Keyed State** (가장 흔함) — Key 기준 파티셔닝. 각 Key가 독립 상태를 가져 병렬 처리 용이.
  예: 사용자별 장바구니, 센서별 최근 1시간 평균 온도.
- **Operator State** — Key와 무관하게 연산자(task) 인스턴스 단위. 예: **Kafka Consumer의 Offset**,
  파일 소스의 읽기 위치.

| | JVM Heap Memory | Embedded RocksDB |
|---|---|---|
| 속도 | Ultra Fast | 느림 (직렬화 비용) |
| 한계 | 메모리 용량(OOM) — 대용량 부적합 | **테라바이트급 상태**를 안정적으로 |

> 개발자는 "State 저장해줘"라고 선언만 하고, 복잡한 메모리/디스크 관리는 엔진이 수행한다.

### Checkpointing 4단계

```
1. State Tracking → 2. Snapshot → 3. Persist → 4. Recovery
   State + Kafka       일정 주기(예: 10초)   HDFS·S3에      최근 체크포인트를
   Offset을 실시간      전체 시스템 상태를    비동기 저장     로드해 그 시점부터
   추적                순간 포착해                          재처리(Replay)
                      일관된 이미지
```

**State와 Kafka Offset을 함께 스냅샷하는 것이 exactly-once의 핵심이다** — 상태만 복원하고 offset이
어긋나면 중복·유실이 난다.

## Flink vs Spark Streaming — 이 코스의 유일한 엔진 비교

| | **Apache Flink** | **Spark Streaming** |
|---|---|---|
| 처리 모델 | **Native Streaming** — 건별(row-by-row) 즉시 | **Micro-batching** — 초 단위 묶음 |
| Latency | **Low (밀리초)** | High (초) |
| Throughput | — | 높고 안정적 |
| 상태 관리 | **Fine-grained Control** | Spark RDD / SQL 기반 |
| 내결함성 | **분산 스냅샷(Chandy-Lamport)** 으로 상태 일관성 완벽 보장 | **RDD Lineage** 재계산 + WAL + Checkpointing |
| Event Time | **Watermark로 late data 정밀 보정** | — |
| 개발 생산성 | — | **배치와 스트리밍에 동일 코드·API**(DataFrame/SQL) |
| 운영 복잡도 | **High** (세밀한 설정 필요) | Medium (접근성 높음) |

> **선택 가이드: 1초 미만 초저지연이 필수면 Flink, 대용량 처리 + 배치 코드 재사용이면 Spark.**

아키텍처 그림:
- **Flink**: `Source(Kafka) → Map → KeyBy → Window → Sink(DB·Dashboard)`, 중앙에 State & Checkpoint
- **Spark**: `Source(Kafka·HDFS) → DStream → RDD Ops → Result → Sink(Data Lake·S3)`,
  중앙에 Batch Interval(예: 1s)

## 기존 페이지와의 대조

- **일치** — Flink가 스트림 프로세서의 대표이고, Spark Structured Streaming이 대안이라는 구도가
  [[Batch and stream processing]]과 같다. Kafka Streams가 별개 라이브러리라는 구분도 유지된다.
- **보강(큼)** — 랜드스케이프 가이드는 Flink를 "필터·필드 매핑·윈도우 집계·중복 제거를 정의하면
  클러스터에서 끊임없이 돌린다"고만 요약했다. 이 덱이 **윈도우 3종의 트레이드오프**,
  **event time / watermark**, **late data 3전략**, **state 종류와 backend**,
  **checkpointing 4단계**, **Flink vs Spark 정면 비교**를 채운다.
  → 별도 개념 페이지 [[Stream processing semantics]]로 분리.
- **연결** — Operator State의 예로 Kafka offset이 나오면서 [[Apache Kafka]]의 오프셋 개념이
  스트림 프로세서의 상태 관리와 이어진다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Stream processing semantics]] (상세), [[Batch and stream processing]],
  [[Apache Kafka]], [[Latency and throughput]]
- 앞 챕터: [[AI DE Course - Ch4-3,4 EDA and Kafka]]
- 이어지는 챕터: [[AI DE Course - Data drift and training-serving skew]] — Part 1 후반부(운영)로 넘어간다

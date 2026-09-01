---
type: source
title: AI DE Course - Ch4-1,2 Batch vs Streaming
area: [data-engineering]
aliases: [CH04-1 2 Batch vs Streaming, Batch vs Streaming 아키텍처 차이]
tags: [data-engineering, course, fast-campus, batch, streaming, latency, throughput, lambda]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part1/13. CH04-1, 2. Batch vs Streaming 아키텍처 차이와 활용 사례 비교 1, 2.pdf"]
---

# AI DE Course - Ch4-1,2 Batch vs Streaming

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 CH04-1,2**
"Batch vs Streaming: 아키텍처 차이와 활용 사례 비교 (1)(2)". 원본(로컬):
`raw/data-engineering/ai-de-course/part1/13. CH04-1, 2. Batch vs Streaming 아키텍처 차이와 활용 사례 비교 1, 2.pdf` (22p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

이 덱의 미덕은 **배치/스트리밍을 "언제 처리하나"가 아니라 "왜 둘을 동시에 가질 수 없나"로
다시 묻는 것**이다. 개념 정리는 [[Latency and throughput]]에 옮겼다.

## 여는 질문 3개

- **왜 '시소' 같을까?** Latency를 줄이면 Throughput이 떨어지고 반대도 그렇다. 왜 필연적인가?
- **물리적 한계는 무엇인가?** 0.001초 응답과 페타바이트 처리를 동시에 못 하는 이유를 CPU·I/O
  레벨에서.
- **무엇을 선택해야 할까?** 정답은 없지만 기준은 있다.

## 아키텍처 대비

**배치 (Hadoop & DW)**

```
Data Sources → Scheduler → Data Lake → Batch Engine → Serving/BI
(로그·DB스냅샷)  (Airflow·Cron)  (HDFS·S3)   (Spark·Hive·      (Data Mart·
                주기적 pull                   MapReduce)         Dashboard)
```

**스트리밍 (Kafka & Flink)**

```
Event Sources → Message Broker → Stream Engine → Real-time Sink
(IoT·클릭로그·   (Kafka·Pulsar·   (Flink·Spark     (Redis·Slack·
 결제 트랜잭션)    Kinesis) 버퍼      Streaming)        Alert API)
                                 상태 관리·윈도우
```

**두 그림의 차이는 도구가 아니라 중간의 성격이다** — 배치는 *저장소*를 거치고, 스트리밍은
*버퍼*를 거친다.

## 이 덱 고유의 서술 — 물리 레벨 근거

강의가 세 층위에서 트레이드오프를 설명하고 수치까지 제시한다. (수치의 출처는 없다.)

| 층위 | 배치 | 스트리밍 |
|---|---|---|
| **CPU 효율** | 95% | 60% |
| **캐시 적중률** | 92% | 58% |
| **패킷 헤더 오버헤드** | < 1% | ~40% |
| **디스크** | 순차 I/O (high efficiency) | 랜덤 I/O (high latency cost) |
| 영향 | Throughput +500% | Latency -90% |

```
Throughput = (Actual Work Time) / (Total Time)
```

- **문맥 전환** — 작업을 바꿀 때마다 레지스터를 저장·복원하는 준비 시간. 순수 오버헤드.
- **캐시 지역성** — 연속 처리하면 L1/L2 적중률이 높다. 잦은 전환은 캐시를 차갑게 만든다
  (미스 한 번에 CPU 사이클 수백 개).
- **패킷 헤더** — 작은 데이터를 자주 보내면 실제 데이터보다 주소표가 더 많아진다.
- **seek time** — 디스크 헤드 이동이 가장 비싼 비용 중 하나.

> ⚠️ **강의 내부 모순:** 이 덱은 "스트리밍 = 랜덤 I/O"로 일반화하지만, 바로 다음 챕터
> [[AI DE Course - Ch4-3,4 EDA and Kafka]]는 Kafka가 **순차 쓰기(sequential I/O)** 를 써서
> "느린 하드 디스크에서도 메모리급 속도"를 낸다고 설명한다. 즉 **스트리밍이 곧 랜덤 I/O인 것이
> 아니라, 건별로 목적지에 직접 쓰면 랜덤 I/O가 되는 것**이다. append-only 로그로 받으면 스트리밍도
> 순차 쓰기다. 이 덱의 일반화는 과하다.

## 밀리초가 돈이 되는 3가지 사례

강의가 배치/스트리밍 선택을 "이미 늦었나"로 판정하는 방식.

| 사례 | 허용 지연 | 배치로 하면 | 스트리밍 파이프라인 |
|---|---|---|---|
| **자율주행** | < 100ms (E2E 목표 < 50ms) | "오늘 운행 기록을 밤에 분석" → **이미 사고 발생** | LiDAR/Camera(0ms) → Edge 추론 TensorRT·Flink(+15ms) → CAN Bus 제동(+30ms). Data Rate 1.2 GB/sec |
| **이상 거래 탐지 (FDS)** | < 500ms (결제 대기 한계) | "내일 아침 리포트로 확인" → **카드 한도 소진** | 결제 요청(0ms) → 피처 추출 Redis + LightGBM 스코어링(+200ms) → 승인 거절·본인 인증(+300ms) |
| **실시간 추천** | < 200ms (clickstream) | "지난달에 수영복 샀으니 수영복 추천" → **관심사 불일치, 낮은 CVR** | Kafka·App(0ms) → Flink·Redis 피처 추출·추론(+100ms) → 추천 목록 노출(+200ms). CVR +15% |

**세 사례 모두 파이프라인에 Redis와 [[Feature store]]가 들어간다** — 최근 행동 패턴을 밀리초에
조회하는 자리다. 자율주행 예시는 시나리오상 "50m 앞 장애물"이고, 강의는 이를
**mission critical system**(장애·지연이 인명 피해로 직결)으로 분류한다.

## 중간지대와 하이브리드

### 마이크로 배치 — "중용(Golden Mean)의 기술"

0.5초~수 초 모아 작은 덩어리로. 결과: **1~5초 지연 + near-batch 효율.**
준실시간성 · 시스템 안정성 · exactly-once를 함께 얻는다.

```scala
val query = streamingDF.writeStream
  .format("kafka")
  .trigger(Trigger.ProcessingTime("1 second"))
  .option("checkpointLocation", "/path/to/chk")
  .start()
```

> **완벽한 실시간이 필요 없다면 마이크로 배치가 비용 대비 최고 효율이다.**

### Lambda Architecture

- **Batch Layer** — immutable master dataset(Hadoop·S3)을 주기적으로 **전체 재처리**해 완벽한 정확성
- **Speed Layer** — 배치 완료 전까지의 최근 데이터(gap)를 Kafka·Flink로 처리. 정확도는 다소 낮음
- **Serving Layer** — Batch View + Real-time View를 **병합(merge)** 해 제공
- ⚠️ **단점: 배치·스트리밍 두 개의 코드베이스 유지보수**
- 대안: **Kappa Architecture** (stream only)

## 선택 기준 — 3축 결정 매트릭스

| 질문 | → Streaming | → Batch |
|---|---|---|
| 데이터 가치 소멸 시간? | 초 단위 (이상탐지·추천) | 일 단위 |
| 정확성 요구? | 허용 오차 있음 | **1원도 오차 불가** (금융 정산·감사) |
| 비용·운영 역량? (24x7 모니터링·고숙련 인력) | 고비용·전문 인력 | 저비용·일반 인력 |

> **Golden Rule:** 실시간성이 필수인 구간(경보·추천)에만 스트리밍을 도입하고, 나머지는 안정적인
> 배치를 기본으로. **Start Simple, Scale Later.**
>
> "모든 것을 실시간으로 처리할 필요는 없습니다. 비즈니스 가치와 비용의 균형점을 찾으세요."

## 기존 페이지와의 대조

- **일치** — 마이크로배치를 실시간 처리의 한 형태로 두는 분류가 [[Batch and stream processing]]과 같다.
  "Kafka는 처리를 안 한다 → 스트림 프로세서가 따로 필요하다"도 아키텍처 그림에서 그대로 확인된다.
- **보강** — **왜 반비례하나**의 물리 레벨 근거(문맥 전환·캐시·패킷 헤더·seek time), Lambda/Kappa,
  3축 선택 기준, 밀리초 사례의 구체적 지연 예산.
  랜드스케이프 가이드는 "스트리밍이 리소스 효율이 나을 수도 있다"고만 했다.
- **주의** — 위의 랜덤 I/O 일반화 문제.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Latency and throughput]] (상세), [[Batch and stream processing]], [[Feature store]],
  [[Apache Kafka]], [[Stream processing semantics]]
- 이어지는 챕터: [[AI DE Course - Ch4-3,4 EDA and Kafka]]

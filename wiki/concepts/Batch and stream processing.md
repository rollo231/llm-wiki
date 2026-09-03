---
type: concept
title: Batch and stream processing
area: [data-engineering]
aliases:
  - Batch processing
  - Stream processing
  - Realtime processing
  - Micro-batch
  - Event streaming platform
  - 배치 처리
  - 스트림 처리
  - 실시간 처리
  - Apache Beam
  - Beam
  - Apache StreamPark
  - StreamPark
tags: [data-engineering, batch, streaming, kafka, flink, airflow, orchestration, spark]
created: 2026-07-28
updated: 2026-09-03
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers", "[[AI DE Course - Ch4-1,2 Batch vs Streaming]]", "[[AI DE Course - Ch4-3,4 EDA and Kafka]]", "[[AI DE Course - Ch4-5,6 Stream processing engines]]"]
---

# Batch and stream processing

데이터를 **언제** 처리하는가의 축. 이 축이 어떤 툴을 쓸 수 있는지를 결정하고, 특히
**오케스트레이터가 어디까지 쓸 수 있는지**를 가른다.

> 오케스트레이터 자체는 [[Data orchestration]] · [[Apache Airflow]]. 이 페이지의 결론을 그쪽에서
> 뒤집어 말하면 — **실시간 경로는 스케줄 없이 스트림이 계속 돌고, 배치 경로만 DAG가 배치 단위로
> 맞춘다.**

- **배치 처리** — 큰 덩어리를 정기 간격으로 처리한다. 예: 달이 바뀌면 지난달 매출을 집계.
  시간에 민감하지 않다(몇 시간, 며칠 기다려도 된다). 큰 데이터를 다룬다.
- **실시간 처리** — 도착 즉시 처리하거나(**스트림 처리**) 아주 작은 배치로 묶어 처리한다
  (**마이크로배치**, 예: 20초마다). 속도가 중요한 파이프라인. 예: 웹사이트에서 봇을 최대한 일찍
  탐지해 차단, 카드 거래 사기 탐지.
- 둘 다 아닌 것도 있다 — **ad-hoc/탐색적 분석**은 자동화된 파이프라인이 아니라 분석가가 질문을
  들고 데이터를 뒤지는 일이다.

스트리밍을 고르는 이유는 결과의 시급성만이 아니다. 리소스 효율이 나을 수도 있고, **raw 페이로드를
어딘가 쟁여뒀다가 다음 배치를 기다릴 필요가 없어진다**는 이점도 있다.

## ⭐⭐ 엔진보다 먼저 정할 것 — 시간을 어떻게 자를지

> **"엔진 이름을 고르기 전에, 먼저 '시간을 어떻게 자를지'를 정하는 편이 낫다. 이 선택이 Spark·Flink
> 논쟁보다 먼저 와야 한다. 시간 모델을 정해야 엔진 비교가 의미를 갖는다."**

| | 시간 모델 | 성질 | 쓰는 곳 |
|---|---|---|---|
| 1️⃣ | **배치** | 하루·한 시간 단위. **단순하고 비용 예측이 쉽지만 결과가 늦다** | 늦게 조회되어도 되는 대용량 정리·리포트 |
| 2️⃣ | **마이크로배치** | 덩어리를 아주 짧게 쪼갠 준실시간 | 수분~수십 초 지연을 허용 |
| 3️⃣ | **이벤트 스트림** | 이벤트마다 상태를 갱신. **이벤트 타임** 기준 윈도우 | 초 단위 갱신 + 상태·늦은 데이터가 중요 |

⚠️ **처리 시각(프로세싱 타임)만 보면 결과가 어긋난다** — 늦게 도착한 데이터까지 고려해야 하면
**이벤트 타임까지 함께 설계**해야 한다. → [[Stream processing semantics]]

⭐ *"'진짜 실시간'이 필요한 구간만 스트림으로 두고 나머지는 배치로 두는 것이 비용과 운영 면에서 보통
더 안전하다."* [[Apache Map - Ch1 How to read this book]]이 레이크하우스 스택과 실시간 스택을 **함께**
쓰라고 한 이유가 이것이다.

### ⭐⭐ 논쟁을 끝내는 한 숫자 — 최대 허용 지연

> **"지연 허용 범위를 숫자로 정해 두면 기술 논쟁이 훨씬 짧아진다.
> SLA를 '평균'이 아니라 '최대 허용 지연'으로 정해 두면 배치와 스트림의 경계가 명확해진다."**

⭐ 이것이 이 축의 **측정 규칙**이다. [[Latency and throughput]]·[[Data SLA and observability]]가 이미
*평균이 아니라 p95/p99* 를 말하는데, 여기서는 그 숫자가 **엔진 선택의 경계선**으로 쓰인다 —
허용 지연이 24시간이면 1️⃣, 30초면 2️⃣, 1초면 3️⃣이고 **그 뒤에야 Spark냐 Flink냐가 의미를 갖는다.**

## 왜 둘 다 가질 수 없나 — 그리고 무엇을 고르나

이 축의 **선택**을 다루는 것이 이 페이지고, 그 **트레이드오프의 물리적 근거**(문맥 전환·캐시 지역성·
패킷 헤더·seek time)와 **Lambda/Kappa** 하이브리드는 [[Latency and throughput]]에 있다.

결정 매트릭스 3축([[AI DE Course - Ch4-1,2 Batch vs Streaming]]):

| 질문 | → Streaming | → Batch |
|---|---|---|
| 데이터 가치 소멸 시간? | 초 단위 (이상탐지·추천) | 일 단위 |
| 정확성 요구? | 허용 오차 있음 | **1원도 오차 불가** (금융 정산·감사) |
| 비용·운영 역량? | 고비용·전문 인력·24x7 모니터링 | 저비용·일반 인력 |

> **Golden Rule:** 실시간성이 필수인 구간(경보·추천)에만 스트리밍을 도입하고 나머지는 배치를 기본으로.
> **Start Simple, Scale Later.**

**배치가 대체 불가인 이유 두 가지** — ① **준비 비용의 규모의 경제**(양말 한 짝을 위해 세탁기를 돌리면
setup cost가 작업 가치보다 크다) ② **재작업 범위가 명확하다**(실시간은 복구가 어렵지만 배치는 문제된
구간만 re-run). 여기에 **Hot/Cold Path 분리** — 낮에는 고객 응대에 집중하고 무거운 분석은 새벽으로.

마이크로배치는 **"중용의 기술"** 이다: 0.5초~수 초 모아 처리해 **1~5초 지연 + near-batch 효율**을
얻고 exactly-once까지 챙긴다. Spark의 `Trigger.ProcessingTime("1 second")`가 그것.

## 이벤트 스트리밍 플랫폼 — Kafka

**Apache Kafka**. LinkedIn에서 나왔고 지금은 오픈소스. 하는 일은 단순하다 — producer에게서 이벤트를
받아 저장하고, consumer가 읽게 한다. 분산·내결함성을 갖춰서 스트림 파이프라인의 좋은 building
block이 된다.

> ⚠️ **메시지 큐와의 결정적 차이:** consumer 하나가 ack해도 **이벤트가 폐기되지 않는다.**
> 로그에 남아 있어서 다른 consumer(또는 같은 consumer)가 retention 규칙에 따라 만료될 때까지
> 몇 번이고 다시 읽을 수 있다.

> ⚠️ **Kafka 자체는 아무 처리도 하지 않는다.** 처리는 별도 워커가 하고, Kafka 입장에서 그 워커는
> 그냥 또 하나의 consumer다.

두 경고 모두 강의에서도 확인된다 → [[Apache Kafka]] (토픽·파티션·오프셋, 레플리케이션, 로그 컴팩션,
Zero-Copy, KRaft 전환, 그리고 강의가 명시하는 Kafka의 한계 3종).

이름이 비슷해 헷갈리는 두 가지:

- **Kafka Connect** — Kafka를 DB 등 다른 시스템에 연결하는 API.
- **Kafka Streams** — Java/Scala 스트림 처리 **라이브러리**. 상태 있는 변환, 윈도우 집계, 조인을
  다룬다. Flink와 취지는 비슷하지만 **당신의 앱 안에 임베드되어 돌고 Kafka에서만 동작**한다.

다른 이벤트 스트리밍 플랫폼: **Apache Pulsar**, **Redpanda**, **AWS Kinesis Data Streams**.

## 스트림 프로세서

Kafka가 처리를 안 하므로 처리기가 따로 필요하다. 커스텀 스크립트여도 되지만 보통은 전용 소프트웨어를
쓴다. **Apache Flink**가 대표. 이벤트를 어디서 받고 어떻게 처리할지(필터·필드 매핑·윈도우 집계·
중복 제거·목적지 쓰기) 정의를 주면 Flink가 클러스터에 배포해 **끊임없이** 돌린다.

대안: **Spark Structured Streaming**, **Google Cloud Dataflow**, **Azure Stream Analytics**.

**Flink vs Spark Streaming의 선택 기준과, 스트림 처리가 배치와 근본적으로 다른 이유**(무한성·
비동기성·상태 내구성 → 윈도우·워터마크·체크포인팅)는 [[Stream processing semantics]]에 있다.
한 줄 요약: **1초 미만 초저지연이 필수면 Flink, 대용량 처리 + 배치 코드 재사용이면 Spark.**

## 엔진 위·옆의 두 계층 — Beam과 StreamPark

엔진을 고른 뒤에도 두 가지 문제가 남는다: **코드를 엔진에 묶을 것인가**, 그리고 **그 앱을 어떻게
배포·감시할 것인가.**

### Apache Beam — 실행 환경을 바꿔 쓸 수 있는 파이프라인 모델

Spark·Flink가 *엔진*이라면 Beam은 **파이프라인을 표현하는 공통 프로그래밍 모델**이다. 한 번 작성한
로직을 Spark·Flink·클라우드 Dataflow 같은 여러 **runner**에서 돌린다. 배치와 스트림을 하나의 모델로
표현하고 **윈도우·워터마크·트리거를 표준화**한다.

푸는 문제: **"엔진이 바뀔 때마다 코드를 다시 짜는 비용."** 비즈니스 로직과 실행 환경을 분리한다.

⚠️ **그러나 추상화 단계가 하나 더 생긴다** — *"디버깅과 성능 튜닝 경로도 엔진 직접 사용보다 길어질 수
있다. 실행 환경을 바꿀 계획이 없으면 엔진 API를 직접 쓰는 편이 더 단순하다."*
⭐ 판단 문항 하나로 줄면: **"엔진을 바꿔도 같은 코드를 쓸 수 있는가"가 그 추상화 비용을 감수할 만큼
중요한가.**

### Apache StreamPark — 스트림 앱의 생명주기

*"Flink나 Spark로 스트림 앱을 만드는 것과, 그것을 여러 팀이 반복해서 배포·감시·롤백하는 것은 다른
문제다."* StreamPark는 엔진을 대체하지 않고 **엔진 위에서 돌아가는 앱의 생명주기를 표준화**한다
(개발 골격 · 배포·버전 · 상태·알람).

⭐ 도입 신호가 관찰 가능하다 — **"누가 어떤 잡을, 어떤 설정으로, 어디에 올렸는지"를 추적하기 어려워질
때**, 그리고 **배포 실수가 반복될 때.** ⚠️ *"작은 팀에서 잡 두세 개만 운영한다면 엔진 기본 도구만으로도
충분할 수 있다."*

⭐ **성능 도구가 아니라 일관성 도구다** — *"계산 성능 튜닝보다 **배포 실수와 설정 불일치**를 줄이는
도구로 이해하면 도입 판단이 쉬워진다."* → [[Data orchestration]] · [[Data and model versioning]]

## 대규모 분산 배치 처리

데이터가 한 대를 넘어서면 여러 대에 쪼개 병렬 처리한다.

- **Apache Hadoop** — 분산 처리의 원조. 지금은 레거시로 취급되지만 오래된 셋업에 남아 있다.
- **Apache Spark** — 현재의 사실상 표준. 로딩·변환·병렬화·최적화를 맡고, 사용자는 바인딩으로
  "무엇을 할지"만 쓴다. **PySpark**(Python, DataFrame API + pandas 호환 레이어), **SparkR**
  (*최근 deprecated*), Java·Scala 바인딩(Spark 자체가 Scala로 쓰였다). 앞서 다룬 거의 모든 저장소를
  읽고 쓸 수 있어서 **레이크의 쿼리 엔진으로도, 무거운 변환의 일꾼으로도** 쓰인다.
- **Dask** — pandas·numpy API에 가깝게 두고 Python 코드를 클러스터로 확장.
- **Ray** — 더 범용적인 분산 컴퓨트 프레임워크. ML 학습에 특히 인기.
- **Apache Flink** — 배치도 되지만 특기는 스트리밍.

## 오케스트레이션

dbt 변환, Spark 잡, 커스텀 스크립트가 뒤섞인 동물원이 되면 **오케스트레이터**가 필요해진다.

- 각 태스크가 무엇을 하고 무엇에 의존하는지 정의하면 오케스트레이터가 **DAG**(directed acyclic
  graph)를 만든다. 보통 코드로 정의하고 대개 Python이다.
- **오케스트레이터 자신은 데이터를 처리하지 않는다.** Spark 스크립트를 실행하고 dbt 변환을
  트리거하고 HTTP 엔드포인트를 호출할 뿐, 실제 일은 그것들이 한다.
- 트리거는 다양하다 — 스케줄, Kafka 이벤트, UI에서 수동, HTTP 요청, 플러그인 API로 직접 제작.
- 독립 태스크로 쪼개는 것의 이점: 의존 없는 태스크의 병렬 실행, **실패한 태스크만 재시도하고
  거기서부터 재개**(전체 재실행이 아니라).

> ⚠️ **오케스트레이터는 배치 전용이다.** 파이프라인을 시작부터 끝까지 돌리고 다음 트리거까지
> 멈추는 모델인데, 이건 *끝나지 않아야 하는* 스트림 처리에 맞지 않는다. 스트리밍 셋업에서는
> 오케스트레이터가 아니라 스트림 프로세서(Flink 등) 자체에 의존한다.

**Apache Airflow**가 생태계가 가장 넓고 널리 쓰인다. 그 외 **Dagster**, **Prefect**,
**Luigi**(오래됐고 지금은 덜 쓰인다).

> **주의:** 인제스트한 소스는 이 넷을 **비교하지 않는다** — 나열만 한다. 선택 기준은
> [[Data Engineering]] MOC의 열린 질문으로 남아 있다.

## 링크

- 트레이드오프의 근거: [[Latency and throughput]] — 시소의 법칙, Lambda/Kappa, 밀리초 사례
- 스트림 처리의 의미론: [[Stream processing semantics]] — 윈도우·워터마크·상태·exactly-once
- 이벤트를 실어 오는 층: [[Apache Kafka]]
- 파이프라인 전체 그림: [[ETL and ELT]], [[Change data capture]]
- Avro가 왜 스트리밍용인가: [[Columnar and in-memory data formats]]
- 결과가 착지하는 곳: [[Medallion architecture]], [[Analytical data storage tiers]]
- lineage 수집원: [[Data catalog and semantic layer]] — 오케스트레이터 DAG가 lineage의 주요 출처
- 적용: [[SpatialData as a data engineering substrate]] — Airflow + KubernetesPodOperator로
  "샘플 1개"를 작업 단위 삼는 coarse-grained fan-out
- 출처: [[Data landscape guide for developers]], [[AI DE Course - Ch4-1,2 Batch vs Streaming]],
  [[AI DE Course - Ch4-3,4 EDA and Kafka]], [[AI DE Course - Ch4-5,6 Stream processing engines]]

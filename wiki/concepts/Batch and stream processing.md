---
type: concept
title: Batch and stream processing
area: [data-engineering]
aliases:
  - Batch processing
  - Stream processing
  - Realtime processing
  - Micro-batch
  - Data orchestration
  - Orchestration
  - Event streaming platform
  - 배치 처리
  - 스트림 처리
  - 실시간 처리
  - 오케스트레이션
tags: [data-engineering, batch, streaming, kafka, flink, airflow, orchestration, spark]
created: 2026-07-28
updated: 2026-07-28
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers"]
---

# Batch and stream processing

데이터를 **언제** 처리하는가의 축. 이 축이 어떤 툴을 쓸 수 있는지를 결정하고, 특히
**오케스트레이터가 어디까지 쓸 수 있는지**를 가른다.

- **배치 처리** — 큰 덩어리를 정기 간격으로 처리한다. 예: 달이 바뀌면 지난달 매출을 집계.
  시간에 민감하지 않다(몇 시간, 며칠 기다려도 된다). 큰 데이터를 다룬다.
- **실시간 처리** — 도착 즉시 처리하거나(**스트림 처리**) 아주 작은 배치로 묶어 처리한다
  (**마이크로배치**, 예: 20초마다). 속도가 중요한 파이프라인. 예: 웹사이트에서 봇을 최대한 일찍
  탐지해 차단, 카드 거래 사기 탐지.
- 둘 다 아닌 것도 있다 — **ad-hoc/탐색적 분석**은 자동화된 파이프라인이 아니라 분석가가 질문을
  들고 데이터를 뒤지는 일이다.

스트리밍을 고르는 이유는 결과의 시급성만이 아니다. 리소스 효율이 나을 수도 있고, **raw 페이로드를
어딘가 쟁여뒀다가 다음 배치를 기다릴 필요가 없어진다**는 이점도 있다.

## 이벤트 스트리밍 플랫폼 — Kafka

**Apache Kafka**. LinkedIn에서 나왔고 지금은 오픈소스. 하는 일은 단순하다 — producer에게서 이벤트를
받아 저장하고, consumer가 읽게 한다. 분산·내결함성을 갖춰서 스트림 파이프라인의 좋은 building
block이 된다.

> ⚠️ **메시지 큐와의 결정적 차이:** consumer 하나가 ack해도 **이벤트가 폐기되지 않는다.**
> 로그에 남아 있어서 다른 consumer(또는 같은 consumer)가 retention 규칙에 따라 만료될 때까지
> 몇 번이고 다시 읽을 수 있다.

> ⚠️ **Kafka 자체는 아무 처리도 하지 않는다.** 처리는 별도 워커가 하고, Kafka 입장에서 그 워커는
> 그냥 또 하나의 consumer다.

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

- 파이프라인 전체 그림: [[ETL and ELT]]
- Avro가 왜 스트리밍용인가: [[Columnar and in-memory data formats]]
- 결과가 착지하는 곳: [[Medallion architecture]], [[Analytical data storage tiers]]
- lineage 수집원: [[Data catalog and semantic layer]] — 오케스트레이터 DAG가 lineage의 주요 출처
- 적용: [[SpatialData as a data engineering substrate]] — Airflow + KubernetesPodOperator로
  "샘플 1개"를 작업 단위 삼는 coarse-grained fan-out
- 출처: [[Data landscape guide for developers]]

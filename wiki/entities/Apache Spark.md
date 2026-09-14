---
type: entity
title: Apache Spark
aliases: [Spark, 스파크, Spark SQL, Spark Streaming, Structured Streaming, DStream]
tags: [도구, 처리, 배치, 스트리밍]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "[[AI DE 강의 1-03 기술 스택과 툴 생태계]]"
  - "[[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]]"
  - "[[AI DE 강의 1-09 비정형 데이터 수집과 전처리]]"
  - "[[AI DE 강의 1-10 배치 vs 스트리밍]]"
  - "[[AI DE 강의 1-12 실시간 처리 엔진]]"
---

# Apache Spark

JVM 기반 **분산 데이터 처리 엔진.** 배치·SQL·스트리밍·머신러닝을 하나의 엔진과 API로 다룬다. Part 1에서는 배치 엔진의
대표이자, 마이크로 배치 스트리밍 엔진으로 나온다.

## 특징 (강의 기준)

[[AI DE 강의 1-03 기술 스택과 툴 생태계]]:

- **Scala 기반** — 복잡한 변환 로직을 간결하게.
- **JVM 생태계** — 자바 라이브러리·하둡과 호환.
- **다목적 엔진** — SQL·스트리밍·머신러닝을 한 플랫폼에서.
- **Spark SQL vs ANSI SQL** — 표준 SQL이 추출·조작·트랜잭션이라면, Spark SQL은 대용량·분석·인메모리 연산.

## 배치 엔진으로

배치 아키텍처의 연산 칸: 소스 → 스케줄러(Airflow) → 레이크(HDFS·S3) → **Spark**·Hive·MapReduce → 데이터 마트
([[AI DE 강의 1-10 배치 vs 스트리밍]]).

- Parquet의 파티셔닝을 인식해 작업 노드에 데이터를 분배한다([[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]]).
- 단일 서버로 안 되는 대규모 비정형 전처리를 분산 처리한다(Dask와 함께 언급, [[AI DE 강의 1-09 비정형 데이터 수집과 전처리]]).

## 스트리밍 — 두 세대

| | Spark Streaming (DStream) | Structured Streaming |
|---|---|---|
| API | DStream, RDD 연산 | DataFrame·SQL(배치와 같은 API) |
| 상태 | **레거시** — 더 이상 업데이트되지 않는다 | 현행 |
| Part 1에서 | [[AI DE 강의 1-12 실시간 처리 엔진]]의 아키텍처 설명 | [[AI DE 강의 1-10 배치 vs 스트리밍]]의 마이크로 배치 코드 |

[Spark 문서 "Spark Streaming is the previous generation of Spark's streaming engine. There are no longer updates
to Spark Streaming and it's a legacy project. … You should use Spark Structured Streaming"
https://spark.apache.org/docs/latest/streaming-programming-guide.html , 2026-09-14 확인]

⚠️ **같은 코스의 두 덱이 서로 다른 세대의 Spark를 설명한다.**

마이크로 배치 예([[AI DE 강의 1-10 배치 vs 스트리밍]]):

```scala
val query = streamingDF.writeStream
  .format("kafka")
  .trigger(Trigger.ProcessingTime("1 second"))   // 1초마다 묶어서 처리
  .option("checkpointLocation", "/path/to/chk")
  .start()
```

결과는 1~5초 지연에 배치에 가까운 효율. 장애 복구는 체크포인트와 WAL로 한다.

## Flink와 비교

| | Spark | [[Apache Flink]] |
|---|---|---|
| 스트리밍 모델 | 마이크로 배치 | 네이티브(레코드 단위) |
| 지연 | 초 단위(트리거 간격에 따라) | 밀리초 |
| 강점 | 배치 코드 재사용, 높은 처리량, 접근성 | 초저지연, 세밀한 상태 제어 |

강의의 선택 가이드: 1초 미만이 필수면 Flink, 대용량 처리와 배치 코드 재사용이면 Spark. → [[스트림 처리]]

## 주의

- "하둡 대비 속도" 같은 비교 수치는 Part 1에 나오지 않는다.

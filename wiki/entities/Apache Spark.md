---
type: entity
title: Apache Spark
aliases: [Spark, 스파크, Spark SQL, Spark Streaming, Structured Streaming, DStream, Real-Time Mode, 출력 모드, Output mode]
tags: [도구, 처리, 배치, 스트리밍]
created: 2026-09-14
updated: 2026-09-28
sources:
  - "[[AI DE 강의 1-03 기술 스택과 툴 생태계]]"
  - "[[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]]"
  - "[[AI DE 강의 1-09 비정형 데이터 수집과 전처리]]"
  - "[[AI DE 강의 1-10 배치 vs 스트리밍]]"
  - "[[AI DE 강의 1-12 실시간 처리 엔진]]"
  - "[[AI DE 강의 4-01 분산 처리의 등장과 도입 판단]]"
  - "[[AI DE 강의 4-07 메시지 브로커와 스트림 처리 엔진]]"
  - "[[AI DE 강의 4-09 워터마크와 윈도우 연산]]"
  - "[[AI DE 강의 4-14 RAPIDS 가속 ETL]]"
---

# Apache Spark

JVM 기반 분산 데이터 처리 엔진이다. 배치·SQL·스트리밍·머신러닝을 하나의 엔진과 API로 다룬다. Part 1에서는 배치 엔진의 대표이자, 마이크로 배치 스트리밍 엔진으로 나온다.

## 등장

[[AI DE 강의 4-01 분산 처리의 등장과 도입 판단]]은 Spark(2010)를 Hadoop MapReduce의 느린 속도, 특히 단계마다 디스크에 썼다가 다시 읽는 비용을 풀기 위해 나온 엔진으로 소개한다(p13). 반복 알고리즘과 대화형 데이터 마이닝처럼 데이터를 메모리에 유지하면 빨라지는 문제를 겨냥했고, 인메모리 처리와 DAG(작업 경로 전체를 미리 그리는 지연 실행)를 핵심으로 든다.

⚠️ 강의의 "하둡보다 특정 작업에서 최대 100배 빠르다"는 옛 공식 홈페이지 문구다. 2016년 사이트는 "Run programs up to 100x faster than Hadoop MapReduce in memory, or 10x faster on disk"라고 적었다(Wayback Machine). 지금 홈페이지에는 이 문구가 없고 "Accelerates TPC-DS queries up to 8x"(AQE 기준)만 있다. [https://spark.apache.org/ , 2026-09-28 확인] "메모리는 디스크보다 수천 배 빠르다"도 지연인지 대역폭인지, HDD인지 NVMe인지에 따라 차이가 10배에서 10만 배까지 벌어지는 수사다.

## 특징 (강의 기준)

[[AI DE 강의 1-03 기술 스택과 툴 생태계]]:

- Scala 기반: 복잡한 변환 로직을 간결하게 쓴다.
- JVM 생태계: 자바 라이브러리·하둡과 호환된다. [[JVM]] 위에서 돌기 때문에 executor의 GC 멈춤이 운영 문제가 된다([[가비지 컬렉터]]). 이 연결은 위키가 붙였다.
- 다목적 엔진: SQL·스트리밍·머신러닝을 한 플랫폼에서 다룬다.
- Spark SQL vs ANSI SQL: 표준 SQL이 추출·조작·트랜잭션용이라면, Spark SQL은 대용량·분석·인메모리 연산용이다.

## 배치 엔진으로

배치 아키텍처의 연산 칸: 소스 → 스케줄러(Airflow) → 레이크(HDFS·S3) → Spark·Hive·MapReduce → 데이터 마트([[AI DE 강의 1-10 배치 vs 스트리밍]]).

- Parquet의 파티셔닝을 인식해 작업 노드에 데이터를 분배한다([[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]]).
- 단일 서버로 안 되는 대규모 비정형 전처리를 분산 처리한다(Dask와 함께 언급, [[AI DE 강의 1-09 비정형 데이터 수집과 전처리]]).

## 스트리밍 — 두 세대

| | Spark Streaming (DStream) | Structured Streaming |
|---|---|---|
| API | DStream, RDD 연산 | DataFrame·SQL(배치와 같은 API) |
| 상태 | 레거시. 더 이상 업데이트되지 않는다 | 현행 |
| Part 1에서 | [[AI DE 강의 1-12 실시간 처리 엔진]]의 아키텍처 설명 | [[AI DE 강의 1-10 배치 vs 스트리밍]]의 마이크로 배치 코드 |

[Spark 문서 "Spark Streaming is the previous generation of Spark's streaming engine. There are no longer updates to Spark Streaming and it's a legacy project. … You should use Spark Structured Streaming" https://spark.apache.org/docs/latest/streaming-programming-guide.html , 2026-09-14 확인]

⚠️ 같은 코스의 두 덱이 서로 다른 세대의 Spark를 설명한다. Part 4의 [[AI DE 강의 4-07 메시지 브로커와 스트림 처리 엔진]]은 Structured Streaming("실시간 입력을 계속 늘어나는 표로 보는 엔진", p172)으로 설명해 Part 1의 DStream 서술을 말없이 대체한다.

### Real-Time Mode

Structured Streaming은 더 이상 마이크로 배치 전용이 아니다. Spark 4.1.0(2025-12-16)이 Real-Time Mode를 공식 지원했고(SPARK-53736, Scala의 stateless 질의부터), 4.2.0(2026-07-14)이 PySpark 지원을 더했다(SPARK-54660). 릴리스 노트는 "First official support for Structured Streaming queries running in real-time mode… single-digit milliseconds"라고 적는다. [https://spark.apache.org/releases/spark-release-4.1.0.html · https://spark.apache.org/releases/spark-release-4-2-0.html , 2026-09-28 확인] 실험적 Continuous Processing(2.3부터, at-least-once)은 그 전부터 있었다. ⚠️ Part 4(2026-05 작성)는 여전히 "기본 실행 방식은 작은 배치를 매우 짧은 간격으로 연속 실행"이라고만 쓴다(p172).

### 출력 모드와 워터마크

출력 모드는 Append(확정된 행만), Update(바뀐 행만), Complete(결과 표 전체) 셋이다. ⚠️ [[AI DE 강의 4-09 워터마크와 윈도우 연산]]은 이것을 Append·Upsert·Update로 적는다(p213). Upsert는 싱크 쪽 반영 방식이다([[스트림 처리]]). 워터마크의 보장은 문서와 강의가 같다. 워터마크 지연보다 덜 늦은 데이터는 반영이 보장되고, 더 늦은 데이터는 반영될 수도 안 될 수도 있다(p209, 문서 인용은 [[스트림 처리]]).

마이크로 배치 예([[AI DE 강의 1-10 배치 vs 스트리밍]]):

```scala
val query = streamingDF.writeStream
  .format("kafka")
  .trigger(Trigger.ProcessingTime("1 second"))   // 1초마다 묶어서 처리
  .option("checkpointLocation", "/path/to/chk")
  .start()
```

결과는 1~5초 지연에 배치에 가까운 효율이다. 장애 복구는 체크포인트와 WAL로 한다.

## Flink와 비교

| | Spark | [[Apache Flink]] |
|---|---|---|
| 스트리밍 모델 | 마이크로 배치 | 네이티브(레코드 단위) |
| 지연 | 초 단위(트리거 간격에 따라) | 밀리초 |
| 강점 | 배치 코드 재사용, 높은 처리량, 접근성 | 초저지연, 세밀한 상태 제어 |

강의의 선택 가이드는 1초 미만이 필수면 Flink, 대용량 처리와 배치 코드 재사용이 중요하면 Spark다. 엔진 비교는 [[스트림 처리]]에도 있다.

## JVM 메모리

드라이버의 `collect()`와 큰 파티션은 「입력에 비례해 한 번에 올리기」 안티패턴의 분산판이다. 안티패턴 목록은 [[객체 수명과 메모리 상한]]에 있다.

## GPU 가속

Spark SQL·DataFrame 연산을 GPU로 옮기는 RAPIDS Accelerator for Apache Spark가 있다. 플러그인 jar와 설정만 더하면 물리 실행 계획의 지원 연산을 GPU 연산으로 바꾸고, 미지원 연산은 CPU로 되돌린다. 자세한 내용과 한계는 [[RAPIDS]]와 [[AI DE 강의 4-14 RAPIDS 가속 ETL]]에 있다.

## 주의

- "하둡 대비 속도" 같은 비교 수치는 Part 1에 나오지 않는다. Part 4의 "최대 100배"는 위의 「등장」 절에 적었다.

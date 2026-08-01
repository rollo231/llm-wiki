---
type: entity
title: Apache Spark
area: [data-engineering]
aliases: [스파크, Spark, Spark SQL, Spark Structured Streaming, PySpark, RDD, DAG]
tags: [data-engineering, spark, distributed-systems, batch, streaming, dag, in-memory]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch1 Distributed processing basics]]", "[[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]]", "[[AI DE Course - Part4 Ch4 GPU in data engineering and RAPIDS]]", "[[AI DE Course - Ch4-5,6 Stream processing engines]]"]
---

# Apache Spark

**In-Memory + DAG 실행으로 [[Apache Hadoop]] MapReduce의 디스크 I/O 한계를 푼 분산 처리 엔진
(2010).** 배치 ETL의 사실상 표준이자, Structured Streaming으로 스트림까지 같은 모델로 다룬다.

## 왜 등장했나

> **"하둡의 느린 속도를 해결하기 위해 등장한 것이 Spark."**

원논문의 동기: *iterative algorithms, interactive data mining tools* — **"데이터를 메모리에
유지하면 성능이 크게 향상될 수 있는 문제들"** 에 디스크 중심 프레임워크는 비효율적이다.

| 핵심 | 내용 |
|---|---|
| **In-Memory 처리** | 데이터를 디스크가 아닌 RAM에 올려서 처리 |
| **DAG** (Directed Acyclic Graph) | 하둡처럼 단계별로 하지 않고 **전체 작업 경로를 미리 그려서 최적화된 경로로 한 번에 처리** (Lazy Execution) |

> ⚠️ **"하둡보다 특정 작업에서 최대 100배 빠르다"** 는 Spark 프로젝트 자체의 초기 마케팅
> (로지스틱 회귀 반복 벤치마크)에서 온 수치다. **"특정 작업에서"라는 단서가 붙어야 성립하고,
> 일반적인 ETL에서 100배는 나오지 않는다.** 강의는 출처 없이 인용한다.

## 실행 구조

```
Driver Program ─── SparkContext ──┬── Cluster Manager
                                  │
                                  ├── Worker Node ── Executor ── Task, Task
                                  │                     └─ Cache
                                  └── Worker Node ── Executor ── Task, Task
                                                        └─ Cache
```

**Cluster Manager**로 Standalone / YARN / Kubernetes / Mesos를 쓴다.
[[Distributed processing]]의 **계산 분산**의 대표 구현이다 — executor가 여러 task를 병렬 수행.

## Spark Structured Streaming

> **"실시간 입력을 계속 늘어나는 표처럼 보고 계산하는 Spark 기반 스트림 처리 엔진."**

| 특징 |
|---|
| **Spark SQL 엔진 위에서 동작** |
| 배치 계산과 비슷한 방식으로 스트림 계산 작성 가능 |
| 입력을 **"계속 추가되는 표"**, 결과를 **"계속 갱신되는 표"** 로 이해하는 모델 |
| 집계, 시간 구간 계산, 조인 지원 |
| **체크포인트 + 기록 저장(WAL)** 을 통한 장애 복구 |
| 기본 실행 방식은 **작은 배치를 매우 짧은 간격으로 연속 실행** (micro-batch) |

**잘 맞는 문제:** SQL/DataFrame 중심 조직 · 기존 Spark 배치 파이프라인과의 통합 ·
**배치와 스트림을 같은 개발 모델로** 다루고 싶은 환경 · 데이터 플랫폼 팀이 이미 Spark 생태계에 익숙.

### vs [[Apache Flink]]

| | Spark Structured Streaming | Flink |
|---|---|---|
| **실행 모델** | **Micro-batch** | 진정한 스트리밍 |
| **지연** | Flink보다 약간 김 | 더 낮음 |
| **강점** | ⭐ **기존 Spark SQL 및 배치 에코시스템과의 완벽한 통합** | ⭐ **세밀한 상태 관리와 시간 제어** |
| **워터마크** | 늦게 도착한 데이터 허용 범위를 정해 오래된 상태 정리 | 시간 진행의 신호로 사용 |

> **Spark의 워터마크 보장이 정확하게 기술되어 있다:**
> **"설정한 지연 시간보다 덜 늦은 데이터는 집계 반영이 보장된다. 그보다 더 늦은 데이터는 반영될
> 수도 있고 안 될 수도 있다."** — 하한 보장이지 상한 배제가 아니다.
> ([[Stream processing semantics]] 참조)

## GPU 가속 — Spark RAPIDS

**[[NVIDIA RAPIDS]]의 플러그인으로 Spark 연산을 GPU에서 실행한다.**

| | 내용 |
|---|---|
| **적용 방식** | **플러그인 — Spark 코드를 수정할 필요가 없다.** `spark-submit` 시 RAPIDS `.jar`를 포함하고 설정만 켬 |
| **메커니즘** | ⭐ **Catalyst Optimizer 개입** — Spark의 **물리적 실행 계획 단계를 가로채서** CPU에서 실행되던 Sort/Join/Aggregate를 GPU 연산으로 대체 |
| **셔플 최적화** | **UCX / RDMA**를 활용해 노드 간 셔플의 네트워크 병목 감소 |

| 가속 가능성이 큰 영역 | 가속 제한 영역 |
|---|---|
| Spark SQL · DataFrame API | ⚠️ **RDD 직접 조작** |
| 컬럼형 연산, scan/filter/projection | 미지원 SQL 연산 |
| join, aggregation, sort 일부 | **일부 UDF** |
| **Parquet / ORC 기반 처리** | 복잡한 row 기반 처리 |
| GPU shuffle 사용 시 대규모 이동 최적화 | **CPU fallback이 많은 plan** |

> ⭐ **"CPU Spark 클러스터를 전부 버리지 않고 GPU 가속 구간부터 적용 가능"** 이 Spark RAPIDS의
> 실무적 매력이고, 동시에 **"RDD 직접 조작 중심의 오래된 코드는 가속 효과가 제한적"** 이라는 것이
> 도입 판단의 핵심이다. → [[NVIDIA RAPIDS]]

## 병목 지표

[[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]은 **Spark shuffle spill**을
배치 지연의 대표 **원인 지표**로 든다. [[Distributed processing]]의 병목 판정 표에서
"디스크: spill file" / "네트워크: shuffle read/write"가 여기에 대응한다.

## 이 위키에서 Spark가 등장하는 자리

| 맥락 | 페이지 |
|---|---|
| 하둡 계보의 후계 | [[Apache Hadoop]] · [[Distributed processing]] |
| 스트림 처리 엔진 | [[Message broker]] · [[Stream processing semantics]] · [[Apache Flink]] |
| 배치/스트림 통합 축 | [[Lambda and Kappa architecture]]의 **Unified Path** |
| GPU 가속 ETL | [[NVIDIA RAPIDS]] · [[GPU architecture]] |
| 레이크하우스 컴퓨트 | [[Analytical data storage tiers]] · [[Table formats]] |

## ⚠️ 이 위키에 아직 없는 것

- **RDD → DataFrame → Dataset의 API 계보**와 Catalyst/Tungsten 최적화 상세
- **AQE (Adaptive Query Execution)**, 동적 파티션 프루닝
- **Spark on Kubernetes의 실무** — executor 동적 할당, shuffle service
- **Photon·Databricks Runtime 같은 상용 엔진과의 차이**
- **Kafka Streams와의 비교 축** — 강의는 "별도 클러스터가 필요한가"로만 가른다

## 관련 페이지

- [[Apache Hadoop]] — 무엇을 극복했나
- [[Apache Flink]] — 스트림 처리의 경쟁자
- [[NVIDIA RAPIDS]] — GPU 가속
- [[Stream processing semantics]] · [[Message broker]] · [[Batch and stream processing]]
- [[Lambda and Kappa architecture]] · [[Distributed processing]]
- [[Columnar and in-memory data formats]] — Parquet/Arrow와의 궁합

## 출처

- [[AI DE Course - Part4 Ch1 Distributed processing basics]]
- [[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]]
- [[AI DE Course - Part4 Ch4 GPU in data engineering and RAPIDS]]
- [[AI DE Course - Ch4-5,6 Stream processing engines]] (Part 1)

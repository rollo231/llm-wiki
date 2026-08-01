---
type: entity
title: AI Data Engineering (Fast Campus course)
area: [data-engineering]
aliases: [AI DE 강의, Fast Campus 데이터 엔지니어링 강의, AI 데이터 엔지니어링 강의, AI DE Course]
tags: [data-engineering, course, fast-campus]
created: 2026-07-19
updated: 2026-08-01
sources: []
---

# AI Data Engineering (Fast Campus course)

패스트캠퍼스(Fast Campus)의 데이터 엔지니어링 강의. AI 시대에 맞춰 기존 DE(정형 데이터·DW·BI)에서
AI DE(모델 학습·추론 지원, 비정형 데이터)로의 전환을 다룬다. **5개 파트 / 41개 슬라이드 덱 /
약 1,155페이지.** 파트별로 강사와 슬라이드 양식이 다르다.

이 페이지가 **챕터 트래커**다. 각 주제 단위로 `wiki/sources/` 페이지를 만들며, 아래 표의 체크 상태가
인제스트 진행도다.

**진행: Part 1 ✅(16/16) · Part 2 ✅(10/10) · Part 3~5 대기 (~744p).**

## 자료 이름 규칙 주의

파일명 규칙이 **파트마다 다르고 파트 표기가 없어서** 순서가 헷갈린다. 실제 순서는 아래와 같다.

| 파일명 형태 | 예시 | 실제 소속 |
|---|---|---|
| `CH0N-M.` 접두 | `CH02-7. 데이터의 시간 여행…` | Part 1 전반부(CH01~CH04) |
| **번호만** `N.` 접두 | `4. 데이터 엔지니어의 약속 SLA…` | **Part 1 후반부** (CH04 다음) |
| `Part2_Ch N` / `Part 3_Ch N` / `Part 4_Ch N` | `Part 3_Ch 2.pdf` | 표기 그대로 |
| `01.` / `1.` + LLM·RAG 주제 | `01. LLM과 RAG.pdf` | Part 5 |

- 번호만 붙은 `1.`~`10.` 파일이 Part 1 소속인 근거: **`10.` 파일 제목이 "및 Part 1 정리"**.
  단 해당 덱 안에 정리 절은 실제로 없고 케이스 스터디로 끝난다 → 제목만 그렇게 붙은 것으로 보인다.
- 이 파일들에는 챕터 번호가 파일명에도 본문에도 없다. 아래 표의 **CH05~CH08은 추론**이다
  (CH04 다음이라는 순서만 확실하다).
- **Part 1 자체의 공식 제목은 자료 어디에도 없다.** 표의 제목은 내용 기반 추론.
- Part 5 소속도 슬라이드에 표기가 없다 — 사람의 배치 판단(2026-08-01).

## Part 1 — AI 데이터 엔지니어링 기초 *(제목 추론)* · ~205p

| 챕터 | 주제 | source 페이지 | 상태 |
|---|---|---|---|
| CH01-1 | [OT] 기존 DE vs AI DE | [[AI DE Course - Ch1-1 OT]] | ✅ |
| CH01-2,3 | 핵심 마인드셋: Latency와 Versioning | [[AI DE Course - Ch1-2,3 Latency and Versioning]] | ✅ |
| CH01-4 | 필수 기술 스택 및 툴 생태계 | [[AI DE Course - Ch1-4 Tech stack and tooling]] | ✅ |
| CH02-1,2,3 | 저장소의 진화: DW → Data Lake → Lakehouse | [[AI DE Course - Ch2-1,2,3 Storage evolution]] | ✅ |
| CH02-4,5,6 | Parquet·Avro와 Columnar Storage의 원리 | [[AI DE Course - Ch2-4,5,6 Parquet and Avro]] | ✅ |
| CH02-7 | 데이터의 시간 여행: Delta Lake와 ACID | [[AI DE Course - Ch2-7 Delta Lake and ACID]] | ✅ |
| CH03-1,2 | 수집 패턴 I: Batch 처리와 ETL | [[AI DE Course - Ch3-1,2 Batch and ETL]] | ✅ |
| CH03-3,4 | 수집 패턴 II: CDC | [[AI DE Course - Ch3-3,4 CDC]] | ✅ |
| CH03-5,6 | 비정형 데이터(PDF·이미지) 수집과 전처리 | [[AI DE Course - Ch3-5,6 Unstructured data ingestion]] | ✅ |
| CH04-1,2 | Batch vs Streaming 아키텍처 | [[AI DE Course - Ch4-1,2 Batch vs Streaming]] | ✅ |
| CH04-3,4 | EDA와 Kafka (Topic·Partition·Offset) | [[AI DE Course - Ch4-3,4 EDA and Kafka]] | ✅ |
| CH04-5,6 | 실시간 처리 엔진 (Flink·Spark Streaming) | [[AI DE Course - Ch4-5,6 Stream processing engines]] | ✅ |
| CH05?(1~3) | AI 모델의 적: Data Drift와 Training-Serving Skew | [[AI DE Course - Data drift and training-serving skew]] | ✅ |
| CH06?(4~6) | 데이터 엔지니어의 약속: 데이터 SLA와 모니터링 | [[AI DE Course - Data SLA and pipeline monitoring]] | ✅ |
| CH07?(7~9) | 데이터 거버넌스와 카탈로그 | [[AI DE Course - Data governance and catalog]] | ✅ |
| CH08?(10) | [Case Study] AI 데이터 파이프라인 구축 사례 | [[AI DE Course - AI pipeline case studies]] | ✅ |

## Part 2 — AI 학습/추론 중심 데이터 파이프라인 설계 · 206p ✅ 완료

강사: **Habi** (데이터 엔지니어 / MLOps 엔지니어 / 데이터 사이언티스트). 슬라이드에 강사 소개가
있는 유일한 파트.

**Part 1과 결이 다르다.** Part 1이 *"무엇인가"*(파이프라인 어휘)라면 Part 2는
*"어떻게 짓고 운영하는가"*(시스템 설계 결정)다. DE의 책임 범위에 **연산의 배치**가 들어온다.

**분할 단위 주의:** 파일은 챕터당 1개지만, 각 PDF 안에 **번호 붙은 소단원**(별도 타이틀 슬라이드)이
있고 그게 Part 1의 덱 하나에 해당한다. **소단원을 source 페이지 단위로 삼았다** → 5개 파일 →
10개 페이지.

| 챕터 | 소단원 | 주제 | 범위 | source 페이지 | 상태 |
|---|---|---|---|---|---|
| Ch1 | 1,2 | 데이터 파이프라인의 진화 과정과 데이터 엔지니어 | 30p | [[AI DE Course - Part2 Ch1 Pipeline evolution and the DE role]] | ✅ |
| Ch2 | 1,2 | MLOps의 핵심 개념과 생애주기 | p1–18 | [[AI DE Course - Part2 Ch2 MLOps and the ML lifecycle]] | ✅ |
| Ch2 | 3 | LLMOps로의 변화와 추가 고려사항 | p19–33 | [[AI DE Course - Part2 Ch2 LLMOps]] | ✅ |
| Ch3 | 1 | ML 데이터 파이프라인의 특징과 구조 | p1–17 | [[AI DE Course - Part2 Ch3 ML data pipeline]] | ✅ |
| Ch3 | 2 | 서빙 파이프라인 설계 및 요구사항 | p18–36 | [[AI DE Course - Part2 Ch3 Serving pipeline]] | ✅ |
| Ch3 | 3 | **Training-Serving Skew의 이해와 예방** ⭐ | p37–51 | [[AI DE Course - Part2 Ch3 Training-serving skew patterns]] | ✅ |
| Ch4 | 1 | Batch vs Online 서빙 아키텍처 비교 | p1–16 | [[AI DE Course - Part2 Ch4 Serving architecture]] | ✅ |
| Ch4 | 2,3 | 서빙 플랫폼 선택 기준 및 기술 스택 | p17–60 | [[AI DE Course - Part2 Ch4 Serving platforms]] | ✅ |
| Ch4 | 4 | 서빙 환경에서의 CPU/GPU 가속 활용 방안 | p61–77 | [[AI DE Course - Part2 Ch4 CPU and GPU inference]] | ✅ |
| Ch5 | 1 | Feature Store의 기본 개념과 필요성 | 15p | [[AI DE Course - Part2 Ch5 Feature store in practice]] | ✅ |

**Part 2의 최대 수확:** Ch3-3의 **skew 4패턴**(시간 기준 · 집계 범위 · 결측 처리 · 스케일링)과
원칙 **"Training은 Serving을 따라가야 한다"**. Part 1의 일화 하나가 진단 틀이 됐다.

**Part 2가 새로 만든 페이지 12개** — concept 7: [[MLOps]] · [[LLMOps]] · [[Context engineering]] ·
[[ML data pipeline]] · [[Batch and online serving]] · [[Model serving platforms]] ·
[[Inference optimization]] / entity 5: [[FastAPI]] · [[TorchServe]] · [[BentoML]] ·
[[NVIDIA Triton Inference Server]] · [[ONNX]].
**[[FastAPI]]가 이 위키의 첫 `programming` 영역 페이지다.**

## Part 3 — 시맨틱 & 컨텍스트 기반 데이터 설계 · 273p

| 챕터 | 주제 | 분량 | 상태 |
|---|---|---|---|
| Ch1 | 스키마 중심 모델과 시맨틱 (RDBMS·정규화·스키마 설계의 약점) | 59p | ⬜ |
| Ch2 | Graph에 대한 이해 | 74p | ⬜ |
| Ch3 | 온톨로지 및 지식그래프 (RDF·RDFS·OWL) | 65p | ⬜ |
| Ch4 | Graph-RAG | 49p | ⬜ |
| Ch5 | 그래프 데이터베이스 실습 | 26p | ⬜ |

## Part 4 — 실시간 & 대규모 데이터 분산처리 설계 · 431p

Ch1~Ch4가 **356페이지 단일 PDF**다. 챕터 경계는 아래 페이지 범위.

| 챕터 | 주제 | 분량 | 상태 |
|---|---|---|---|
| Ch1 | 분산처리의 필요성과 주의사항 (GFS·MapReduce·Hadoop·Spark·합의) | p2–66 | ⬜ |
| Ch2 | 초저지연 캐싱 아키텍처 (Redis 등) | p67–132 | ⬜ |
| Ch3 | 스트리밍 데이터 처리 | p133–240 | ⬜ |
| Ch4 | GPU 워크로드 전략 | p241–356 | ⬜ |
| Ch5 | 시스템 운영 및 최적화 (SLA/SLO/SLI·Error Budget) | 75p | ⬜ |

## Part 5 — LLM·RAG *(파트 번호·제목 미표기)* · 40p

| 주제 | 분량 | 상태 |
|---|---|---|
| LLM에 대한 기본 이해 (Transformer·N-gram·토큰화) | 16p | ⬜ |
| LLM과 RAG | 15p | ⬜ |
| RAG의 진화: Hybrid Search와 Reranking | 9p | ⬜ |

## 다루는 개념

**Part 1** — 파이프라인 어휘:

- 직무·방식: [[Traditional data engineering]] · [[AI data engineering]]
- 저장: [[Analytical data storage tiers]] · [[Columnar and in-memory data formats]] · [[Table formats]]
- 수집: [[ETL and ELT]] · [[Change data capture]] · [[Unstructured data ingestion]]
- 처리: [[Batch and stream processing]] · [[Stream processing semantics]] · [[Apache Kafka]]
- 운영·품질: [[Data drift and training-serving skew]] · [[Data SLA and observability]] ·
  [[Feature store]] · [[Data catalog and semantic layer]]
- 설계 축: [[Latency and throughput]] · [[Data and model versioning]]

**Part 1이 새로 만든 페이지 9개** — [[Change data capture]] · [[Latency and throughput]] ·
[[Apache Kafka]] · [[Stream processing semantics]] · [[Unstructured data ingestion]] ·
[[Data drift and training-serving skew]] · [[Data SLA and observability]] · [[Feature store]] ·
[[Data and model versioning]]. 나머지 7개는 [[Data landscape guide for developers]]에서 세운 것을
강의 관점으로 보강했다.

**Part 2** — 학습·추론 시스템:

- 운영 체계: [[MLOps]] · [[LLMOps]] · [[Context engineering]]
- 데이터 생산: [[ML data pipeline]] · [[Feature store]]
- 서빙: [[Batch and online serving]] · [[Model serving platforms]] · [[Inference optimization]]
- 도구: [[FastAPI]] · [[TorchServe]] · [[BentoML]] · [[NVIDIA Triton Inference Server]] · [[ONNX]]

## 이 코스에 대한 주의

- ⚠️ **출처 없는 수치가 상습적이다.** "데이터의 80%가 비정형", "배치가 워크로드의 80%",
  "탐색에 80% 시간", "데이터 준비 70%+", "개발 시간 70% 단축", "PSI > 0.2",
  그리고 Part 2의 **"온프레미스 시대 인프라 관리에 70% 이상"**.
  → [[AI DE Course - AI pipeline case studies]]의 '검증 필요' 절.
- **출처가 표기된 드문 인용 3건** (1차 자료 인제스트 후보):
  - Chip Huyen, *Designing Machine Learning Systems* — ML 라이프사이클 Fig 2-2 (Part 2 Ch2·Ch3)
  - "Do you really need a feature store?" (Medium/Data Science) — Part 2 Ch5
  - tiangolo의 FastAPI 성능 도식 — Part 2 Ch4

## 링크

- 영역 MOC: [[Data Engineering]]

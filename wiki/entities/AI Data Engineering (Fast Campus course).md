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

**진행: Part 1 ✅(16/16) · Part 2 ✅(10/10) · Part 3 ✅(15/15) · Part 4 ✅(15/15) ·
Part 5 대기 (40p).**

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

## Part 3 — 시맨틱 & 컨텍스트 기반 데이터 설계 · 273p ✅ 완료

**Part 1이 "무엇인가"(파이프라인 어휘), Part 2가 "어떻게 짓고 운영하는가"(시스템 설계)였다면
Part 3는 "무엇을 의미하는가"(의미 모델링)다.** 논지 한 줄:
**스키마는 형식을 잡지만 의미는 별도 계층이 필요하다 → 그 계층이 시멘틱 → 그 구현이 그래프·온톨로지
→ 그 활용이 GraphRAG.**

**분할 단위:** Part 2와 같이 **소단원(별도 타이틀 슬라이드)을 기본 단위**로 하되, 제목이 같은 연속
소단원(Ch1의 NoSQL 1·2)과 짧은 챕터(Ch5, 26p)는 합쳤다 → **17 소단원 → 15개 페이지.**

| 챕터 | 소단원 | 주제 | 범위 | source 페이지 | 상태 |
|---|---|---|---|---|---|
| Ch1 | 1 | 전통적 스키마 설계와 RDBMS | p2–19 | [[AI DE Course - Part3 Ch1 Schema design and RDBMS]] | ✅ |
| Ch1 | 2,3 | RDBMS의 한계와 NoSQL의 등장 | p20–48 | [[AI DE Course - Part3 Ch1 RDBMS limits and NoSQL]] | ✅ |
| Ch1 | 4 | **Semantic이란?** ⭐ | p49–59 | [[AI DE Course - Part3 Ch1 Semantics]] | ✅ |
| Ch2 | 1 | Graph 기초·종류·지식그래프·DE에게 Graph | p1–20 | [[AI DE Course - Part3 Ch2 Graph fundamentals]] | ✅ |
| Ch2 | 2 | Property Graph vs RDF | p21–35 | [[AI DE Course - Part3 Ch2 Property graph vs RDF]] | ✅ |
| Ch2 | 3 | 실무에서의 Graph (메타데이터·리니지·추천·검색) | p36–51 | [[AI DE Course - Part3 Ch2 Graph in practice]] | ✅ |
| Ch2 | 4 | AI와 Graph (GNN·LLM 결합 3패턴·GraphRAG 예고) | p52–74 | [[AI DE Course - Part3 Ch2 Graph and AI]] | ✅ |
| Ch3 | 1 | 온톨로지 개요 및 기본 아키텍처 (RDF·RDFS·OWL) | p1–15 | [[AI DE Course - Part3 Ch3 Ontology basics]] | ✅ |
| Ch3 | 2 | **클래스·속성·관계 정의의 실무 원칙** ⭐ | p16–29 | [[AI DE Course - Part3 Ch3 Ontology design principles]] | ✅ |
| Ch3 | 3 | 데이터 수집부터 그래프 생성까지의 파이프라인 | p30–45 | [[AI DE Course - Part3 Ch3 Knowledge graph pipeline]] | ✅ |
| Ch3 | 4 | SHACL을 이용한 그래프 검증과 데이터 계약 | p46–65 | [[AI DE Course - Part3 Ch3 SHACL and graph data contracts]] | ✅ |
| Ch4 | 1 | **RAG에 대한 이해와 한계점** ⭐ | p1–14 | [[AI DE Course - Part3 Ch4 RAG and its limits]] | ✅ |
| Ch4 | 2 | Graph-RAG의 개념과 사례1 (MS 논문·4패턴·사례) | p15–33 | [[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]] | ✅ |
| Ch4 | 3 | Graph-RAG의 개념과 사례2 (변형·제품화) | p34–49 | [[AI DE Course - Part3 Ch4 GraphRAG variants and products]] | ✅ |
| Ch5 | 1,2 | 그래프 데이터베이스 (특징 + 제품 비교) | p1–26 | [[AI DE Course - Part3 Ch5 Graph databases]] | ✅ |

**Part 3의 최대 수확 세 가지:**

1. ⭐ **"테이블 = 클래스, 컬럼 = 속성, FK = 관계로 그대로 옮기는 것이 가장 흔한 실수."**
   운영 DB 스키마는 저장 효율용, 온톨로지는 의미 해석용 — 목적이 다르다.
   **"온톨로지 설계는 스키마 복사가 아니라 의미 구조를 다시 세우는 작업이다."** (Ch3-2)
2. ⭐ **"검색 단위는 chunk인데 질문 단위는 structure다."** RAG 한계의 첫 줄이자 GraphRAG 존재
   이유의 요약. (Ch4-1)
3. ⭐ **"NoSQL이면 확장성이 자동 해결될까? 아니다."** 파티션 키가 시스템을 결정하고, 일관성 완화는
   애플리케이션 복잡도로 전가되며, **운영 포인트는 줄지 않고 분산된다.** (Ch1-3)

**Part 3가 새로 만든 페이지 16개** — concept 10: [[Schema-centric data modeling]] · [[NoSQL]] ·
[[Data semantics]] · [[Graph data model]] · [[Graph database]] · [[Knowledge graph]] ·
[[Ontology]] · [[Knowledge graph pipeline]] · [[Retrieval-augmented generation]] · [[GraphRAG]] /
entity 6: [[Neo4j]] · [[Amazon Neptune]] · [[ArangoDB]] · [[JanusGraph]] · [[DataHub]] ·
[[Microsoft GraphRAG]].

### ⚠️ Part 3의 자료 결함 (챕터별)

| 위치 | 문제 |
|---|---|
| Ch3-3 | **파이프라인 단계 수 불일치** — 개요는 1~7단계, 바로 다음 상세는 1~10단계 |
| Ch4-3 | **타이틀 번호 중복** — 소단원 2·3이 모두 "2. Graph-RAG의 개념과 사례". 목차 04·05는 소단원 1 목차의 복붙 잔재로 **본문에 없다** |
| Ch5 | **제목이 "실습"인데 실습이 없다** — 코드·스크린샷·설치 절차 전무, 26p 전부 개념 |
| Ch1-1 · Ch2-4 · Ch3-1 · Ch3-4 | **완전 동일한 중복 슬라이드** 다수. 특히 Ch3-4는 20p 중 접두사 설명이 3연속 반복 |
| Ch2 전반 | **인용 이미지 출처 미표기가 많다** — 특히 Ch2-3의 컬럼 lineage UI 스크린샷은 어느 제품인지 불명 |

**다만 Part 3는 Part 1보다 출처 표기가 뚜렷이 낫다** — RAG 원논문, RAG Survey(arXiv 2312.10997),
*Lost in the Middle*, MS *From Local to Global*, Neo4j 고객사례 2건, AWS 블로그·문서.
**1차 자료 인제스트 후보가 크게 늘었다.**

## Part 4 — 실시간 & 대규모 데이터 분산 처리 설계 · 431p ✅ 완료

**Part 1이 "무엇인가"(어휘), Part 2가 "어떻게 짓는가"(시스템 설계), Part 3가 "무엇을
의미하는가"(의미 모델링)였다면 Part 4는 "물리적으로 어디서 막히는가"다.**
노드·네트워크·메모리 대역폭·GPU 코어 같은 하드웨어 제약이 전면에 나온다.
Part 1의 [[Latency and throughput]] "시소의 법칙"이 여기서 **CAP · Roofline · PCIe 병목**으로
구체화된다.

**자료 구성:** Ch1~Ch4가 **356페이지 단일 PDF**(`Part 4_Ch 1~4.pdf`), Ch5는 별도 75p.
**분할 단위:** 21개 소단원을 기본으로 하되 **주제가 밀착·중복된 것 6쌍을 묶어 15장**
(Part 3와 같은 밀도, 약 29p/장).

| 챕터 | 소단원 | 주제 | 범위 | source 페이지 | 상태 |
|---|---|---|---|---|---|
| Ch1 | 1,2 | 분산처리 개념·역사·필요성 | p2–31 | [[AI DE Course - Part4 Ch1 Distributed processing basics]] | ✅ |
| Ch1 | 3 | **CAP와 분산시스템의 근본 한계** ⭐ | p32–50 | [[AI DE Course - Part4 Ch1 CAP theorem and system limits]] | ✅ |
| Ch1 | 4 | 고가용성·복제·합의 | p51–66 | [[AI DE Course - Part4 Ch1 HA replication and consensus]] | ✅ |
| Ch2 | 1,2 | Redis와 캐싱 레이어 | p67–110 | [[AI DE Course - Part4 Ch2 Redis and the caching layer]] | ✅ |
| Ch2 | 3 | 캐싱 전략·무효화·TTL 설계 | p111–132 | [[AI DE Course - Part4 Ch2 Caching strategies and TTL]] | ✅ |
| Ch3 | 1 | 메시지 브로커의 종류와 전달 보장 | p133–151 | [[AI DE Course - Part4 Ch3 Message brokers]] | ✅ |
| Ch3 | 2 | 브로커 vs 스트림 처리 엔진 | p152–175 | [[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]] | ✅ |
| Ch3 | 3,4 | Event time·워터마크·윈도우 | p176–216 | [[AI DE Course - Part4 Ch3 Event time watermarks and windows]] | ✅ |
| Ch3 | 5 | 람다·카파·현대 아키텍처 | p217–240 | [[AI DE Course - Part4 Ch3 Lambda Kappa and modern architecture]] | ✅ |
| Ch4 | 1,2 | **GPU 아키텍처와 CUDA** ⭐ | p241–277 | [[AI DE Course - Part4 Ch4 GPU architecture and CUDA]] | ✅ |
| Ch4 | 3 | GPU 할당 아키텍처 설계 (MIG·MPS) | p278–301 | [[AI DE Course - Part4 Ch4 GPU allocation architecture]] | ✅ |
| Ch4 | 4,5 | DE의 GPU 활용과 RAPIDS | p302–356 | [[AI DE Course - Part4 Ch4 GPU in data engineering and RAPIDS]] | ✅ |
| Ch5 | 1 | AI 시스템 지표와 SLA (SLI/SLO/Error Budget) | p1–21 | [[AI DE Course - Part4 Ch5 AI system metrics and SLA]] | ✅ |
| Ch5 | 2 | 모니터링 대시보드·알람 | p22–47 | [[AI DE Course - Part4 Ch5 Monitoring dashboards and alerts]] | ✅ |
| Ch5 | 3,4 | **트러블슈팅·GPU 스케줄링** ⭐ | p48–75 | [[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]] | ✅ |

**Part 4의 최대 수확 다섯 가지:**

1. ⭐ **"분산 도입의 출발점은 '데이터가 크다'가 아니라 '단일 서버로도 감당 가능한가'."**
   AWS U7i(32TiB/1920vCPU)·I4i(30TB NVMe)를 근거로 단일 서버를 재평가한다.
   **분산 처리 챕터를 분산 반대 논변으로 여는 구성.** (Ch1-2)
2. ⭐ **Brewer의 2012년 정정을 직접 인용한다.** "C, A, P 중 2개를 고른다"는 통념을 소개한 **직후에**
   저자 본인의 반박으로 무너뜨린다 — 선택은 fine granularity로 일어나고 C/A는 이분법이 아니라
   **정도의 문제**. **CAP의 C ≠ ACID의 C**도 분리한다. (Ch1-3)
3. ⭐ **GPU 3축 해석표** — 사용률 × Queue × Latency의 조합으로 병목을 판정한다. 특히
   **"사용률 낮음 + latency 높음 = GPU 앞단 병목"** 이 Part 2의 "GPU는 마지막 수단"에 진단 도구를
   붙인다. (Ch5-3)
4. ⭐ **"컬럼 기반 포맷이 GPU와 어울리는 이유는 연속된 메모리 접근(coalescing)"** —
   Part 1의 [[Columnar and in-memory data formats]]와 GPU 시대를 잇는 가장 강한 고리. (Ch4-2)
5. ⭐ **`offline-online skew`를 SLI로, `mismatch 0.1% 이하`를 SLO로** 세운다. Part 2가 열어놓기만
   했던 "두 스토어 간 일치"가 **측정 대상으로 승격**된다. (Ch5-1)

**Part 4가 새로 만든 페이지 15개** — concept 9: [[Distributed processing]] · [[CAP theorem]] ·
[[Distributed system limits]] · [[Replication and consensus]] · [[Caching strategies]] ·
[[Message broker]] · [[Lambda and Kappa architecture]] · [[GPU architecture]] ·
[[GPU resource allocation]] / entity 6: [[Redis]] · [[Apache Hadoop]] · [[Apache Spark]] ·
[[Apache Flink]] · [[CUDA]] · [[NVIDIA RAPIDS]].
**기존 페이지 대폭 보강 6개:** [[Data SLA and observability]] · [[Inference optimization]] ·
[[Stream processing semantics]] · [[Apache Kafka]] · [[Latency and throughput]] ·
[[Columnar and in-memory data formats]].

### ⚠️ Part 4의 자료 결함

| 위치 | 문제 |
|---|---|
| **Ch1-3 vs Ch2** | ⚠️⚠️ **파트 내부 모순 — Redis의 CAP 분류.** Ch1-3은 Redis를 **CP**("금융 거래·결제 시스템에 적합")로 분류하는데, Ch2-2는 부적합 데이터 1번이 **"강한 정합성이 필요한 결제 상태"**, Ch2-3은 **"Redis 장애 시 데이터 유실"·"정산·결제·주문에는 위험"**. Redis 기본 복제는 비동기라 **RPO > 0**이므로 CP가 아니다 |
| **Ch4-5** | ⚠️⚠️ **사례 수치 모순** — 같은 사례의 AS-IS는 "전처리에 4시간", TO-BE는 "8시간에서 15분으로 단축". **연속된 두 슬라이드에서 4h vs 8h가 어긋난다** |
| **Ch3-2 · Ch5-1 · Ch2-3** | **목차 복붙 잔재 3건** — Ch3-2 목차의 `05 합의의 대가`(Ch1-4 것), Ch5-1 목차의 `05 GPU 데이터 파이프라인 설계 판단 기준`(Ch4-5 것), Ch2-3 목차의 05 번호 중복. **모두 본문에 없다** |
| **Ch1-1** | **섹션 헤더 불일치** — 목차는 "04. Hadoop / 05. Apache Spark"인데 슬라이드 헤더는 "02. 분산처리의 기반개념들". 이전 버전 잔재 |
| **Ch4-2 vs Ch4-3** | **MIG 지원 장비 불일치** — Ch4-3 본문은 A100/A30·H100/H200·**B200**·RTX PRO Blackwell, 비교표는 "A100, H100 전용". Ch4-2 GPU 스펙 표에는 B200이 아예 없다 |
| **Ch4-3 ↔ Ch5-4** | **큰 폭의 중복** — GPU 할당 방식·K8s NodePool·Spot/On-Demand·클라우드 quota가 양쪽에. 서로 보완 관계인데 **교차 참조가 없어 둘 다 읽어야 전체 그림이 나온다** |
| **전반** | **중복 슬라이드 다수** — p6/p7, p10~12, p21/p22, p34/p35, p70/p71, p74/p75, p94/p95, p109/p110, p115/p116, p168/p169, p343/p344, p58/p59, p73/p74 |
| **Ch5** | **관측 도구가 하나도 안 나온다** — Prometheus·Grafana·OpenTelemetry·Datadog 전무. `Karpenter`만 알람 예시에 이름이 나온다 |

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

**Part 3** — 의미 모델링:

- 출발점: [[Schema-centric data modeling]] · [[NoSQL]] → 둘 다 못 하는 것 → [[Data semantics]]
- 그래프: [[Graph data model]] · [[Graph database]] · [[Knowledge graph]]
- 의미 계층: [[Ontology]] · [[Knowledge graph pipeline]]
- 활용: [[Retrieval-augmented generation]] · [[GraphRAG]]
- 도구: [[Neo4j]] · [[Amazon Neptune]] · [[ArangoDB]] · [[JanusGraph]] · [[DataHub]] ·
  [[Microsoft GraphRAG]]

**Part 4** — 물리적 제약:

- 분산의 근본: [[Distributed processing]] → [[CAP theorem]] · [[Distributed system limits]] →
  [[Replication and consensus]]
- 지연 줄이기: [[Caching strategies]] · [[Redis]]
- 스트리밍 실무: [[Message broker]] · [[Stream processing semantics]] ·
  [[Lambda and Kappa architecture]]
- GPU: [[GPU architecture]] · [[GPU resource allocation]] · [[CUDA]] · [[NVIDIA RAPIDS]]
- 운영: [[Data SLA and observability]] (SLI/SLO/Error Budget·대시보드·알람으로 대폭 확장)
- 엔진: [[Apache Hadoop]] · [[Apache Spark]] · [[Apache Flink]] · [[Apache Kafka]]

## 이 코스에 대한 주의

- ⚠️ **출처 없는 수치가 상습적이다 (Part 1·2).** "데이터의 80%가 비정형", "배치가 워크로드의 80%",
  "탐색에 80% 시간", "데이터 준비 70%+", "개발 시간 70% 단축", "PSI > 0.2",
  그리고 Part 2의 **"온프레미스 시대 인프라 관리에 70% 이상"**.
  → [[AI DE Course - AI pipeline case studies]]의 '검증 필요' 절.
- ⚠️ **Part 3는 성격이 다르다 — 출처는 있지만 벤더 자료다.**
  Neo4j 고객사례의 "time-to-insight 10배 · analyst time 92% 감소 · 150명"과
  Microsoft의 "LazyGraphRAG 인덱싱 비용 = full GraphRAG의 0.1%".
  **강의가 후자에 대해 "자사 비교", "주장"이라고 명시하는 점은 Part 1보다 낫다.**
- ⚠️ **Part 4는 갈린다 — 이론 파트는 최고, 사례 파트는 최악.**
  - ✅ **Ch1-3(CAP)은 이 코스 전체에서 출처가 가장 좋다** — Brewer 2000·**Brewer 2012 정정**·
    Gilbert & Lynch·Lamport·FLP. **출처 없는 수치가 하나도 없다.**
  - ✅ **GPU 스펙(Ch4-2)이 검증 가능하고 실제와 일치한다** — T4 320GB/s, A100 ~2TB/s,
    H100 3.3TB/s, MIG 최대 7개, A100 SM 108개, AWS/GCP 인스턴스 매핑.
    Ch1-2의 AWS U7i·I4i 스펙도 맞다. **Part 1의 "출처 없는 80%"와 뚜렷이 다르다.**
  - ⚠️ **반면 Ch4-5의 RAPIDS 사례 3건은 출처가 전혀 없고 내부 모순까지 있다** —
    "8시간 → 15분"(AS-IS는 4시간), "50대 CPU → A100 1장", "TCO 70~80% 절감".
    **NVIDIA 마케팅 형태의 수치인데 벤더 주장이라고 밝히지 않는다 — Part 3보다 후퇴했다.**
  - ⚠️ 기타 출처 없는 수치: "하둡보다 100배"(Spark 자체 주장), "메모리는 디스크보다 수천 배",
    "0.5초 이내 추천 갱신".
- **출처가 표기된 인용 (1차 자료 인제스트 후보):**
  - Chip Huyen, *Designing Machine Learning Systems* — ML 라이프사이클 Fig 2-2 (Part 2 Ch2·Ch3)
  - "Do you really need a feature store?" (Medium/Data Science) — Part 2 Ch5
  - tiangolo의 FastAPI 성능 도식 — Part 2 Ch4
  - *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* — RAG 원논문 (Part 3 Ch4)
  - *RAG for Large Language Models: A Survey* — `arxiv.org/pdf/2312.10997` (Part 3 Ch4)
  - *Lost in the Middle: How Language Models Use Long Contexts* (Part 3 Ch4)
  - *From Local to Global: A Graph RAG Approach to Query-Focused Summarization* — Microsoft
    (Part 3 Ch4) → [[Microsoft GraphRAG]]
  - ⭐ **Part 4 Ch1-3의 분산 시스템 정전(canon) 5건** — Brewer의 CAP(2000)와
    **본인의 정정(2012)** · Gilbert & Lynch의 형식화 ·
    Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System* ·
    Fischer/Lynch/Paterson의 **FLP 불가능성**. → [[CAP theorem]] · [[Distributed system limits]]
  - Part 4 Ch3-5 — Nathan Marz(람다), **Jay Kreps**의 재처리 흐름 → [[Lambda and Kappa architecture]]
  - Part 4 Ch1-4 — **Google Cloud PostgreSQL HA 문서** → [[Replication and consensus]]
  - ⚠️ 다만 **논문의 연도·저널이 표기되지 않는다** (Lamport 1978 CACM, FLP 1985 JACM,
    Gilbert & Lynch 2002 SIGACT News, Raft: Ongaro & Ousterhout 2014).

## 링크

- 영역 MOC: [[Data Engineering]]

---
type: source
title: AI DE Course - Part3 Ch4 GraphRAG concepts and cases
area: [data-engineering, programming]
aliases: [Part3 Ch4-2, Graph-RAG의 개념과 사례1]
tags: [data-engineering, course, fast-campus, graphrag, rag, knowledge-graph, neo4j]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part3/04. Ch4. Graph-RAG.pdf (p15–33)"]
---

# AI DE Course - Part3 Ch4 GraphRAG concepts and cases

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch4 "Graph-RAG"의 소단원 **2**
"Graph-RAG의 개념과 사례1". 원본(로컬): `raw/data-engineering/ai-de-course/part3/04. Ch4. Graph-RAG.pdf` **p15–33** (19p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

## 구성

`01 GraphRAG · 02 From Local to Global · 03 현실세계의 GraphRAG · 04 GraphRAG가 RAG 한계를 넘는 방식
· 05 GraphRAG 대표패턴과 사례`

## 왜 별도 주제인가

기존 RAG는 문서 조각 검색 중심 구조라 다음에서 한계가 드러난다 — 코퍼스 전체를 묻는 질문 · 문서 간
관계를 따라가야 하는 질문 · 다중 hop 연결이 필요한 질문 · **전역 요약과 국소 탐색이 동시에 필요한 질문.**

> **Microsoft GraphRAG 논문의 출발점: "기존 RAG는 private / unseen corpus에 답하는 데 유용하지만,
> '이 데이터셋 전체의 핵심 주제는 무엇인가' 같은 global question에는 실패한다."**

출처: *From Local to Global: A Graph RAG Approach to Query-Focused Summarization* — Microsoft.

## Microsoft GraphRAG 제안

> **Key Concept: 나무가 아닌 숲을 보는 RAG.**
> 기존 RAG의 한계 = 특정 키워드 중심의 파편화된 정보 검색(**point-lookup**).
> GraphRAG의 해법 = 데이터 간 관계를 그래프로 구조화하고 **계층적으로 요약**하여 전역적(Global)
> 통찰 도출.

논문 파이프라인 다이어그램(2-column layout)이 나오고 구성 요소를 하나씩 설명한다:

| 구성 요소 | 뜻 |
|---|---|
| **Source Documents & Text Chunks** | 원본 문서와 처리 가능한 크기의 조각. **RAG와 동일** |
| **Element Instances** | 텍스트 내에서 누구(Who)·무엇(What)을 추출(Entity)하고 연결 고리(Relationship)를 정의한 상태. **지식 그래프의 노드와 간선** |
| **Element Summaries** | 각 노드와 간선이 어떤 맥락에서 등장했는지 LLM이 짧게 요약. **단순한 이름 이상의 의미 정보** |
| **Graph Communities** | 알고리즘(예: **Leiden**)으로 긴밀하게 연결된 노드들을 하나의 그룹으로 묶은 것 |
| **Community Summaries** | 각 커뮤니티가 전체적으로 어떤 주제·내용을 다루는지 LLM이 생성한 고수준 요약 |

### Step 1. Indexing Time (Top-Down)

추출(Extraction) → 구조화(Structuring) → 추상화(Abstraction).

> **결과물: 질문이 들어오기 전에 이미 "데이터 전체는 A, B, C라는 주요 주제(커뮤니티)로 구성되어
> 있다"는 지도가 완성된다.**

### Step 2. Query Time (Bottom-Up)

병렬 검색(Parallel Retrieval — 관련된 여러 커뮤니티 요약본을 동시에 참조) → 중간 답변 생성
(Community Answers — 각 커뮤니티 관점에서 조각조각 생성) → 최종 합성(Global Answer).

## ⭐ 현실세계의 GraphRAG — 넓은 정의

> **"실무와 업계에서는 GraphRAG를 더 넓게 사용한다. retrieval 단계가 graph structure를 활용하면
> GraphRAG라고 부르는 경우가 많다."**

넓은 의미의 GraphRAG 패턴: knowledge graph를 직접 탐색해 retrieval · vector search 후 graph
traversal로 주변 사실 확장 · graph community를 이용한 global summary retrieval · subgraph를 LLM의
컨텍스트로 전달.

> **"논문형 GraphRAG는 하나의 대표 구현이고, 실무형 GraphRAG는 그보다 넓은 graph-aware retrieval
> architecture로 이해하는 편이 좋다."**

### 검색 대상이 chunk에서 structure로

기존 RAG의 기본 retrieval object는 text chunk. GraphRAG에서는 **entity · relationship · subgraph ·
community summary · graph path** 같은 구조화된 단위가 retrieval 대상으로 들어온다.

> ⭐ **"GraphRAG의 본질은 그래프 DB 사용 여부가 아니라, 검색 가능한 지식의 단위를 문서 조각에서
> 구조화된 의미 단위로 바꾼 것이다. 검색 가능한 대상이 넓어진 것."**
>
> **이 문장이 이 소단원의 핵심**이고, "GraphRAG = Neo4j 쓰는 것"이라는 오해를 정확히 막는다.

## RAG 한계 4종과의 대응표

| 기존 RAG의 한계 | GraphRAG의 대응 | 핵심 메커니즘 |
|---|---|---|
| 파편화된 정보 도출 | 지식의 구조화 & 시각화 | **Entity Graph** |
| 전역적 질문(Global Q) 취약 | 계층적 요약 경로 확보 | **Community Summary** |
| 복잡한 다단계 추론 약화 | 연결 경로 추적 및 확장 | **Graph Traversal** |
| 긴 컨텍스트의 불안정성 | 구조적 선별 및 압축 | **Subgraph Selection** |

**한계 4종은 [[AI DE Course - Part3 Ch4 RAG and its limits]]에서 세운 것**이고, 이 표가 두 소단원을
잇는다. 다만 **표의 4항목과 앞 소단원의 4항목이 정확히 1:1 대응하지는 않는다** — 앞은
(검색단위 불일치 / retrieval-generation mismatch / Lost in the Middle / 고정 k)였고 여기는
(파편화 / 전역질문 / multi-hop / 긴 컨텍스트)다. 2번(mismatch)이 빠지고 multi-hop이 추가됐다.

### 세 가지 가치

1. **설명 가능성** — 왜 이 답이 나왔는지 entity path, subgraph, source link로 설명하기 쉽다
2. **복잡한 도메인 질의 대응** — 고객-상품-브랜드, 계정-기기-IP, **Dataset-Job-Dashboard**처럼 관계
   중심 질문에 강함
3. **구조화 데이터와 비구조화 문서 결합** — 기존 knowledge graph, metadata graph, enterprise graph까지
   함께 활용 가능

> **"문서 QA 개선 기술이라기보다 기업 지식을 구조화해서 더 신뢰 가능한 검색·질의 시스템을 만드는
> 패턴으로 받아들여진다."**

## ⭐ 4가지 패턴 — 이 소단원의 최대 수확

> **"GraphRAG는 하나의 제품명이 아니라 graph를 retrieval에 넣는 여러 설계 패턴의 묶음이다."**

| 패턴 | 핵심 메커니즘 | 활용 사례 |
|---|---|---|
| **P1. 논문형 (Full-Extract)** MS GraphRAG 스타일 | 모든 문서에서 Entity/Relation 추출, 전역 요약(Community Summary) 사전 생성 | 거대 문서군에 대한 전역적 통찰 (수천 장의 시장 분석 보고서 요약) |
| **P2. 하이브리드 확장 (Search & Expand)** | Vector Search로 관련 청크를 먼저 찾고, 그 청크 내 엔티티의 인접 노드(k-hop)를 그래프에서 추가 호출 | 특정 인물/사건 중심 심층 조사 (수사·법률 문서 내 인물 관계 추적) |
| **P3. 엔터프라이즈 그라운딩 (Legacy Integration)** | 문서에서 엔티티를 뽑는 대신 **기존 마스터 데이터(CRM, ERP)나 메타데이터 그래프를 RAG의 기준점으로** | 데이터 신뢰성이 최우선인 기업 내부 데이터 (제품 매뉴얼 + 실제 재고/사양 DB) |
| **P4. NL2Query (Text-to-Graph)** | 질문을 Cypher/Gremlin 같은 그래프 쿼리로 변환해 정형 관계를 즉시 조회 | 정형+비정형 결합 조회 ("A 제품을 구매한 고객 중 B 지역에 사는 사람들의 불만 사항은?") |

**P3의 설명이 특히 좋다:** **"LLM이 추출한 그래프가 정확해?"라는 불신을 해결한다.** 문서에
"A배터리"라고 적혀 있다면 이를 기업 DB의 `P-1004` 모델 노드와 연결하여 **hallucination을 원천 차단.**

**P4:** **LLM을 검색기가 아니라 쿼리 생성기로 사용.** 결과값이 **결정론적(Deterministic)** 이어야
하는 정형 관계 분석에 최적화.

> **P3가 [[Knowledge graph pipeline]]과 직결된다** — Ch3에서 만든 메타데이터 그래프가 그대로
> GraphRAG의 grounding 소스가 된다. 강의는 두 챕터를 잇지 않는다. **위키가 붙인 연결.**

## 사례 2건

| 사례 | 내용 |
|---|---|
| **Technology Media Company** ([[Neo4j]] + Deloitte 공개) | 대형 gaming/technology media 기업이 Neo4j GraphRAG + Amazon Bedrock 등으로 자연어 분석 플랫폼 구축. **GraphRAG를 문서 QA가 아니라 games·promotions·market events·revenue 같은 business entity 중심의 기업 분석 world model로 사용.** 아키텍처: Neo4j(Graph Analytics·Graph Database·Bloom) ↔ LangChain ↔ Amazon SageMaker / Amazon Bedrock / Snowflake / Claude |
| **DUCK / Kiku AI** | 고객 대화·리뷰·커뮤니티 데이터를 Neo4j knowledge graph로 연결. 자연어 질의로 고객 인텔리전스 탐색. **공개 인용 기준으로 그래프를 foundation of facts로 두고 LLM은 그 위에서 reasoning하는 구조.** AWS·Amazon Bedrock 기반. 아키텍처: Facebook/Reddit/Instagram/YouTube posts → Neo4j EE Cluster(EC2) → 전략/전술/전사 산출물 |

> ⚠️ **첫 사례의 수치는 벤더 자료다.** "기존 대비 time-to-insight 10배 개선, routine request에 대한
> analyst time 92% 감소, 150명 이상 비즈니스 사용자 활용 중" — 출처가 **Neo4j 고객사례 페이지**
> (`neo4j.com/customer-stories/technology-media-company`)다. 수치의 측정 방법·기준선이 없다.
> **Part 1의 "출처 없는 80%"와는 다르다(출처는 있다) 하지만 마케팅 자료라는 점은 밝혀야 한다.**

두 사례의 공통 메시지: **GraphRAG를 문서 QA가 아니라 비즈니스 엔터티 중심 구조화에 쓴다.**

## 기존 페이지와의 대조

- **[[GraphRAG]]에 통합** / **새 entity:** [[Microsoft GraphRAG]] · [[Neo4j]]
- **[[AI DE Course - Part3 Ch2 Graph and AI]]와 중복** — Ch2-4의 04절이 이 내용의 축약판이다.
  Ch2가 예고편, Ch4가 본편.
- **[[Knowledge graph pipeline]]과 연결** — P3(엔터프라이즈 그라운딩).

## 자료 품질

- 논문·고객사례 URL 표기 있음. **아키텍처 다이어그램 2장은 출처 표기 없음**(AWS 구성도, Neo4j EE
  Cluster 구성도) — 다만 문맥상 해당 고객사례 페이지 자료로 보인다.
- 중복 슬라이드 없음.
- **⚠️ 벤더 수치 3건**(10배 / 92% / 150명).

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[GraphRAG]] · [[Retrieval-augmented generation]] · [[Knowledge graph]] ·
  [[Knowledge graph pipeline]] · [[Graph database]]
- 도구: [[Microsoft GraphRAG]] · [[Neo4j]] · [[Amazon Neptune]]
- 앞: [[AI DE Course - Part3 Ch4 RAG and its limits]]
- 다음: [[AI DE Course - Part3 Ch4 GraphRAG variants and products]]

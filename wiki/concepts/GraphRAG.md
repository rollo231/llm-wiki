---
type: concept
title: GraphRAG
area: [data-engineering, programming]
aliases: [Graph-RAG, 그래프 RAG, LazyGraphRAG, DRIFT Search, GNN, Graph Neural Network, NL2Cypher]
tags: [data-engineering, graphrag, rag, llm, knowledge-graph, retrieval, gnn]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]]", "[[AI DE Course - Part3 Ch4 GraphRAG variants and products]]", "[[AI DE Course - Part3 Ch2 Graph and AI]]"]
---

# GraphRAG

**retrieval 단계에서 그래프 구조를 활용하는 RAG 패턴군.**
[[Retrieval-augmented generation|RAG]]가 부딪힌 **구조적 한계**에 대한 대응이다.

> ⭐ **"GraphRAG의 본질은 그래프 DB 사용 여부가 아니라, 검색 가능한 지식의 단위를 문서 조각에서
> 구조화된 의미 단위로 바꾼 것이다."**

기존 RAG의 retrieval object는 보통 text chunk다. GraphRAG에서는 **entity · relationship ·
subgraph · community summary · graph path** 같은 구조화된 단위가 retrieval 대상으로 들어온다.

## 왜 별도 주제인가

기존 RAG는 문서 조각 검색 중심 구조이기 때문에 다음에서 한계가 드러난다:

- 코퍼스 **전체**를 묻는 질문
- 문서 **간 관계**를 따라가야 하는 질문
- **다중 hop 연결**이 필요한 질문
- **전역 요약과 국소 탐색이 동시에** 필요한 질문

> Microsoft GraphRAG 논문의 출발점:
> **"기존 RAG는 private/unseen corpus에 답하는 데 유용하지만, '이 데이터셋 전체의 핵심 주제는
> 무엇인가' 같은 global question에는 실패한다."**

## 논문형 GraphRAG — From Local to Global

Microsoft, *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*.

> **Key Concept: 나무가 아닌 숲을 보는 RAG.**
> 기존 RAG의 한계는 특정 키워드 중심의 파편화된 정보 검색(point-lookup).
> GraphRAG의 해법은 데이터 간 관계를 그래프로 구조화하고 **이를 계층적으로 요약해 전역적 통찰을
> 도출**하는 것.

파이프라인은 **두 시점**으로 나뉜다.

```
Indexing Time                          Query Time
─────────────                          ──────────
Source Documents                       Global Answer
   ↓ text extraction and chunking          ↑ query-focused summarization
Text Chunks                            Community Answers
   ↓ domain-tailored summarization         ↑ query-focused summarization
Element Instances                      Community Summaries
   ↓ domain-tailored summarization         ↑ domain-tailored summarization
Element Summaries ──community detection→ Graph Communities
```

| 구성 요소 | 뜻 |
|---|---|
| **Source Documents & Text Chunks** | 원본 문서와 처리 가능한 크기로 자른 조각. RAG와 동일 |
| **Element Instances** | 텍스트 내에서 누구(Who)·무엇(What)을 추출(Entity)하고 그들 사이 연결 고리(Relationship)를 정의한 상태. **지식 그래프의 노드와 간선** |
| **Element Summaries** | 추출된 각 노드와 간선이 어떤 맥락에서 등장했는지 LLM이 짧게 요약. 단순한 이름 이상의 의미 정보 |
| **Graph Communities** | 알고리즘(예: **Leiden**)으로 그래프 내에서 긴밀하게 연결된 노드들을 하나의 그룹으로 묶은 것 |
| **Community Summaries** | 각 커뮤니티가 전체적으로 어떤 주제·내용을 다루는지 LLM이 생성한 고수준 요약 |

### Step 1. Indexing Time (Top-Down) — 지식의 구조화

1. **추출(Extraction)** — 문서를 청크로 나누고, 그 안에서 개체와 관계를 추출
2. **구조화(Structuring)** — 뽑아낸 개체들을 연결하여 거대한 지식 그래프를 형성
3. **추상화(Abstraction)** — 그래프를 분석해 커뮤니티를 찾아내고, 커뮤니티별 요약본을 생성

> **결과물: 질문이 들어오기 전에 이미 "데이터 전체는 A, B, C라는 주요 주제로 구성되어 있다"는 지도가
> 완성된다.**

### Step 2. Query Time (Bottom-Up) — 추론 및 합성

1. **병렬 검색(Parallel Retrieval)** — 질문이 들어오면 관련된 여러 커뮤니티 요약본을 동시에 참조
2. **중간 답변 생성(Community Answers)** — 각 커뮤니티 관점에서 질문에 대한 답변을 조각조각 생성
3. **최종 합성(Global Answer)** — 흩어진 중간 답변들을 하나의 완성된 논리로 정리

### local 질문 vs global 질문

| | 질문 | 방식 |
|---|---|---|
| **로컬** | 특정 엔터티·사건·문서 조각에 대한 질문 ("이 인물과 직접 관련된 사건은?", "이 장애와 연결된 특정 시스템은?") | **local search** — 특정 엔터티 주변 1~2 hop, 관련 chunk 몇 개, exact relation 중심 |
| **글로벌** | 문서 집합 전체의 주제·공통 패턴·주요 갈등축 ("이 데이터셋의 핵심 테마는?", "전체 회의록에서 반복 등장한 리스크는?") | **global search** — community summaries, higher-level report, corpus-level synthesis |

## GraphRAG가 RAG 한계를 넘는 방식

| 기존 RAG의 한계 | GraphRAG의 대응 | 핵심 메커니즘 |
|---|---|---|
| 파편화된 정보 도출 (문서 조각 단위 검색으로 구조적 연결성 부족) | 지식의 구조화 & 시각화 (Entity 간 관계를 그래프로 명시화) | **Entity Graph** |
| 전역적 질문(Global Q) 취약 (전체 말뭉치를 아우르는 요약 불가) | 계층적 요약 경로 확보 (커뮤니티 단위의 사전 요약본 활용) | **Community Summary** |
| 복잡한 다단계 추론 약화 (Multi-hop 관계 추적 시 정보 손실) | 연결 경로 추적 및 확장 (그래프 탐색을 통한 연쇄적 정보 도출) | **Graph Traversal** |
| 긴 컨텍스트의 불안정성 (무의미한 정보 주입으로 노이즈 발생) | 구조적 선별 및 압축 (필요한 서브그래프와 요약본만 선택) | **Subgraph Selection** |

현실에서 받아들여지는 세 가지 가치:

1. **설명 가능성** — 왜 이 답이 나왔는지 entity path, subgraph, source link로 설명하기 쉽다
2. **복잡한 도메인 질의 대응** — 고객-상품-브랜드, 계정-기기-IP, Dataset-Job-Dashboard처럼 관계 중심
   질문에 강함
3. **구조화 데이터와 비구조화 문서 결합** — 문서 검색만이 아니라 기존 knowledge graph, metadata
   graph, enterprise graph까지 함께 활용 가능

> **"문서 QA 개선 기술이라기보다 기업 지식을 구조화해서 더 신뢰 가능한 검색·질의 시스템을 만드는
> 패턴으로 받아들여진다."**

## ⭐ 현실의 4가지 패턴

> **"GraphRAG는 하나의 제품명이 아니라 graph를 retrieval에 넣는 여러 설계 패턴의 묶음이다."**

| 패턴 | 핵심 작동 메커니즘 | 주요 활용 사례 |
|---|---|---|
| **P1. 논문형 (Full-Extract)** — Microsoft GraphRAG 스타일 | 모든 문서에서 Entity/Relation을 추출하고, 전역적 요약(Community Summary)을 사전 생성 | 거대 문서군에 대한 전역적 통찰 (수천 장의 시장 분석 보고서 요약) |
| **P2. 하이브리드 확장 (Search & Expand)** | Vector Search로 관련 청크를 먼저 찾고, 해당 청크 내 엔티티의 인접 노드(k-hop)를 그래프에서 추가 호출 | 특정 인물/사건 중심의 심층 조사 (수사/법률 문서 내 인물 관계 추적) |
| **P3. 엔터프라이즈 그라운딩 (Legacy Integration)** | 문서에서 엔티티를 뽑는 대신, **기존의 마스터 데이터(CRM, ERP)나 메타데이터 그래프를 RAG의 기준점으로 활용** | 데이터 신뢰성이 최우선인 기업 내부 데이터 (제품 매뉴얼 + 실제 재고/사양 DB 연결) |
| **P4. NL2Query (Text-to-Graph)** | 사용자의 질문을 Cypher/Gremlin 같은 그래프 쿼리로 변환하여 정형화된 관계를 즉시 조회 | 정형 데이터와 비정형 데이터의 결합 조회 ("A 제품을 구매한 고객 중 B 지역에 사는 사람들의 불만 사항은?") |

**패턴별 특징:**

- **P1** — 비정형 텍스트를 구조적 데이터로 **완전히 재설계**하는 방식. 인덱싱 시점에 모든 관계를
  정의하므로 비용이 많이 들 수 있다. 대신 질문 시점에 문서 전체를 보지 않아도 Community Summary로
  답변, **포괄적인 질문에 가장 정확.**
- **P2** — 기존 Vector RAG의 유사도 기반 검색에 그래프의 연결성을 덧붙인 방식. 벡터로 찾은 텍스트
  조각에 "이 프로젝트 담당자가 누구지?"라는 정보가 없더라도, 그래프를 통해 담당자 엔티티를 추가
  확장(multi-hop expansion)해 retrieval. **컨텍스트의 밀도가 비약적으로 향상.**
- **P3** — **"LLM이 추출한 그래프가 정확해?"라는 불신을 해결.** 이미 검증된 기업 내부 KG를 그대로
  활용한다. 문서에 "A배터리"라고 적혀 있다면 이를 기업 DB의 `P-1004` 모델 노드와 연결하여
  **hallucination을 원천 차단.**
- **P4** — **LLM을 검색기가 아니라 쿼리 생성기로 사용.** 그래프 DB의 스키마를 프롬프트에 제공하고
  LLM이 이를 바탕으로 Cypher 등을 생성. 결과값이 **결정론적(Deterministic)** 이어야 하는 정형 관계
  분석에 최적화.

## 논문 이후 — 왜 후속 변형이 계속 나왔나

> **"GraphRAG의 후속 진화는 성능 욕심이 아니라 비용·질문 유형·도메인 적응 문제를 해결하려는 과정이다."**

세 가지 운영 문제:

1. **인덱싱 비용이 크다** — entity 추출, 관계 정리, community summary 생성까지 사전 작업이 많음
2. **질문 유형이 다르다** — global question에는 강하지만 local question에는 과하거나 비효율적
3. **도메인 적응이 어렵다** — 뉴스 문서용 prompt와 extraction 규칙이 다른 도메인에서 그대로 맞지 않음

### 변형 1 — Auto-Tuning (도메인 적응)

GraphRAG의 핵심 추출 프롬프트는 도메인에 민감하다. 기본 prompt가 특정 도메인에 최적화되어 있으면
다른 도메인에서는 entity type과 relation type이 빈약하게 추출될 수 있다.

**해결:** 샘플 문서를 보고 도메인을 식별하고, **persona와 few-shot prompt를 자동 생성**해
entity/relationship extraction과 summary generation을 더 도메인 친화적으로 만든다.

> ⭐ **"GraphRAG의 품질은 그래프 질의 전에, 무엇을 entity와 relation으로 뽑아내느냐에서 이미 갈린다."**

### 변형 2 — DRIFT Search (질문 유형 분기)

모든 질문을 한 방식으로 처리하면 비효율적이다. **Global Search는 넓게 보지만 비싸고, Local Search는
깊게 보지만 전역 맥락이 약할 수 있다.**

**DRIFT(Dynamic Reasoning with Fine-grained Information Tree)** — 상위 community report를 먼저 사용해
넓은 초기 답과 follow-up question을 만들고, 그 다음 local search 방식으로 세부를 파고드는 구조.

### 변형 3 — LazyGraphRAG (비용 구조 재설계)

**문제:** Full GraphRAG는 query 전에 많은 요약과 구조화를 미리 만들어야 하므로 선행 인덱싱 비용이
높다.

**해결:** 사전 요약을 크게 줄이고, **질의 시점에 더 많은 relevance test와 query refinement를 수행.**
즉 upfront indexing cost를 줄이고 질의 시점에 계산을 더 집중.

프로세스: Build Index (개념 추출·그래프 최적화) → Refine Query (서브쿼리 식별·정제) →
Match Query (텍스트 청크 랭킹·평가) → Map Answers (관련 claim 추출·그룹화) → Reduce Answers (최종 답변).

> ⚠️ **Microsoft는 자사 비교에서 LazyGraphRAG indexing cost가 vector RAG와 같고 full GraphRAG의
> 0.1% 수준이라고 설명하고, 일부 설정에서 global/local 질의 품질을 유지하거나 능가하면서 비용을 크게
> 낮췄다고 주장한다. 자사 벤치마크이므로 그대로 인용하기 전 검증이 필요하다.**

**"GraphRAG는 무조건 무거운 구조가 아니라 비용을 어떻게 배분할지에 따라 다시 설계될 수 있다"** 는
결론 자체는 타당하다.

## 제품화

**GraphRAG가 더 이상 연구 데모가 아니라 managed service로 운영 가능해졌다.**

- **AWS Bedrock Knowledge Bases GraphRAG** — 문서로부터 entity·fact·relationship을 자동 추출해
  **Neptune Analytics**에 그래프와 벡터를 함께 저장. 검색 시 vector similarity search와 graph
  traversal을 결합.
- **AWS GraphRAG Toolkit** (오픈소스) — 비정형 데이터로부터 graph와 vector embeddings를 자동 구성하고,
  graph를 질의하는 question-answering 전략을 프레임워크 형태로 제공.

> **"실무형 GraphRAG는 논문 구현보다 도구화와 조립 가능성이 훨씬 중요해지고 있다."**

## AI에서 그래프가 쓰이는 세 층위

GraphRAG는 이 중 세 번째다.

| 층위 | 뜻 |
|---|---|
| **Graph as Data** | 입력 자체가 그래프 구조 — 추천, 지식그래프, 메타데이터, 분자구조, 소셜네트워크 |
| **Graph as Model** | 그래프 구조를 학습하는 모델 — **GNN**. 노드/엣지/이웃 구조를 따라 representation 학습 |
| **Graph as Retrieval / Memory / Reasoning Layer** | LLM이 private corpus나 enterprise knowledge를 다룰 때 문서 집합에서 entity graph를 만들고 그 위에 retrieval·summarization·provenance 추적을 수행 — **GraphRAG** |

### GNN 한 줄

CNN이 이미지에서, LSTM이 시계열에서 특징을 추출하듯 **GNN은 그래프 구조를 활용해 특징을 추출한다.**
전제는 **"노드는 고립된 점이 아니라 주변 이웃과의 관계를 통해 의미가 달라진다"** 는 것 — 노드 표현은
자기 자신의 feature만이 아니라 **이웃 노드와 연결 구조를 함께 반영**해 학습해야 한다.

### LLM과 Graph의 결합 3패턴

| 패턴 | 구조 |
|---|---|
| **GNN-driving-LLM** | LLM이 그래프 학습을 돕는다. 노드 분류·링크 예측·그래프 예측은 그래프 모델이 수행하고, **LLM이 좋은 텍스트 의미 정보를 넣어주는 역할** (노드 설명 텍스트에서 의미 벡터 추출, pseudo-label 추정, sparse한 속성 보강) |
| **LLM-driving-GNN** | 그래프를 LLM의 **입력 문맥**으로 바꿔 LLM이 직접 추론. 그래프는 학습 대상이 아니라 입력 컨텍스트로 동작 |
| **GNN-LLM-co-driving** | 구조는 GNN이, 의미는 LLM이. ① LLM 임베딩을 GNN 입력 feature로 ② dual encoder(텍스트/그래프 인코더 따로 두고 concat·attention·gating) ③ **공동 추론 파이프라인**(그래프가 subgraph/candidate retrieval → GNN이 구조 기반 score → LLM이 후보를 읽고 설명/재랭킹) |

세 번째의 ③번이 **production system에서 자주 나오는 형태**이고, 추천·enterprise search·RAG에서 자주
활용된다.

**그래프를 LLM 입력으로 넣는 네 가지 방법:**

1. **Triple로 제공** — `User_A viewed Item_X` / `Item_X belongs_to Category_Books`.
   관계 정보를 비교적 자세히 보존
2. **인접 관계 요약 형태** — 특정 노드 중심으로 local graph를 요약. 질문 중심으로 필요한 관계만 짧게
3. **Path 중심 표현** — `raw_orders → daily_sales_etl → sales_summary → sales_dashboard`.
   **"중요한 건 연결 한 개가 아니라 연결이 이어져서 어떤 의미 있는 경로를 만드는가"**
4. **JSON / structured prompt** — 필드 구조로 정리. 파싱이 쉽고 출력 구조화에 유리

## ⭐ DE 관점 — 모델보다 먼저 컨텍스트 레이어

> **"Graph + AI의 첫 번째 가치는 모델 고도화가 아니라 컨텍스트 정렬이다.
> LLM이 바로 답을 잘 만드는 것이 핵심이 아니라, LLM이 읽을 수 있는 구조화된 컨텍스트를 누가 어떻게
> 만들 것인가가 핵심이다."**
>
> **데이터 엔지니어의 역할은 문서 조각을 많이 넣는 것이 아니라, 데이터셋·잡·런·대시보드·차트·오너·
> 용어집·품질 상태·정책·엔터티 관계를 연결해 AI가 근거와 맥락을 함께 읽게 만드는 것.**
>
> **"Graph + AI의 성패는 모델 성능보다, AI가 읽는 운영 컨텍스트를 얼마나 정확하고 최신으로
> 구조화했는가에 달려 있다. 그 컨텍스트를 가장 잘 만들 수 있는 역할이 데이터 엔지니어다."**

이 문장이 [[Context engineering]](Part 2)의 직계 후속이고, **Part 3 전체가 DE에게 무엇을 요구하는지의
답이다.**

## 사례

| 사례 | 내용 |
|---|---|
| **Technology Media Company** (Neo4j + Deloitte 공개) | 대형 gaming/technology media 기업이 [[Neo4j]] GraphRAG + Amazon Bedrock으로 자연어 분석 플랫폼 구축. GraphRAG를 문서 QA가 아니라 **games·promotions·market events·revenue 같은 business entity 중심의 기업 분석 world model**로 사용 |
| **DUCK / Kiku AI** | 고객 대화·리뷰·커뮤니티 데이터를 Neo4j knowledge graph로 연결하고 자연어 질의로 고객 인텔리전스를 탐색. **그래프를 foundation of facts로 두고 LLM은 그 위에서 reasoning하는 구조.** AWS·Amazon Bedrock 기반 |

> ⚠️ 첫 사례의 **"time-to-insight 10배 개선, routine request에 대한 analyst time 92% 감소, 150명
> 이상 비즈니스 사용자"** 는 **Neo4j 고객사례(벤더 마케팅 자료)의 수치**다. 인용 시 출처를 밝혀야
> 한다.

## 관련 페이지

- [[Retrieval-augmented generation]] — 대응 대상인 한계 4종
- [[Knowledge graph]] · [[Graph data model]] — 구조화의 수단
- [[Knowledge graph pipeline]] — P3(엔터프라이즈 그라운딩)의 앞단
- [[Graph database]] — retrieval 백엔드
- [[Neo4j]] · [[Amazon Neptune]] · [[Microsoft GraphRAG]]
- [[Context engineering]] — **"모델보다 먼저 컨텍스트"**
- [[LLMOps]] — 운영 관점

## 출처

- [[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]]
- [[AI DE Course - Part3 Ch4 GraphRAG variants and products]]
- [[AI DE Course - Part3 Ch2 Graph and AI]]

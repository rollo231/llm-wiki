---
type: source
title: AI DE Course - Part3 Ch2 Graph and AI
area: [data-engineering, programming]
aliases: [Part3 Ch2-4, Graph에 대해 이해하기4, AI와 Graph, GNN]
tags: [data-engineering, course, fast-campus, graph, gnn, llm, graphrag, context]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part3/02. Ch2. Graph에 대한 이해.pdf (p52–74)"]
---

# AI DE Course - Part3 Ch2 Graph and AI

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch2의 소단원 **4**
"Graph에 대해 이해하기4". 원본(로컬): `raw/data-engineering/ai-de-course/part3/02. Ch2. Graph에 대한 이해.pdf` **p52–74** (23p).
**Ch2에서 가장 긴 소단원.** 강의 홈: [[AI Data Engineering (Fast Campus course)]].

## 구성

`01 AI와 Graph · 02 Graph Neural Network란 · 03 LLM과 Graph의 결합 · 04 GraphRAG · 05 데이터 엔지니어
관점에서 본 Graph + AI`

> **Ch4(Graph-RAG, 49p)와 겹친다.** 여기 04절은 GraphRAG의 예고편이고, Ch4가 본편이다.
> 반대로 **02·03절(GNN, LLM+Graph 결합 패턴)은 여기에만 있다.**

## AI 시대에 Graph가 다시 중요해진 이유

> **"LLM은 텍스트 의미를 강하게 다룬다. 하지만 AI 시스템이 실제 업무에서 부딪히는 문제는 텍스트
> 의미만으로 끝나지 않는다."**

- 문서 조각을 단순 벡터로만 찾는 방식은 **"전체 데이터셋의 핵심 주제는 무엇인가" 같은 전역 질문에
  약할 수 있다**
- 반대로 그래프는 엔터티와 관계를 구조화하고, **커뮤니티 단위로 요약을 만들며, 국소 탐색과 전역
  요약을 분리해 다룰 수 있다**

## AI에서 Graph가 쓰이는 세 층위

| 층위 | 뜻 |
|---|---|
| **Graph as Data** | 입력 자체가 그래프 구조 — 추천, 지식그래프, 메타데이터, 분자구조, 소셜네트워크 |
| **Graph as Model** | 그래프 구조를 학습하는 모델 — **GNN**. 노드·엣지·이웃 구조를 따라 representation 학습 |
| **Graph as Retrieval / Memory / Reasoning Layer** | LLM이 private corpus나 enterprise knowledge를 다룰 때 문서 집합에서 entity graph를 만들고 그 위에 retrieval·summarization·**provenance 추적**을 수행 |

**이 3분법이 이 소단원의 뼈대**이고, 세 번째가 GraphRAG다.

## GNN

CNN이 이미지에서, LSTM이 시계열에서 특징을 추출하듯 **GNN은 그래프 구조를 활용해 특징을 추출한다.**

> **"노드는 고립된 점이 아니다. 주변 이웃과의 관계를 통해 의미가 달라진다.
> 따라서 노드 표현은 자기 자신의 feature만이 아니라 이웃 노드와 연결 구조를 함께 반영해 학습해야 한다."**

예: 사용자 프로필만 보면 정보가 부족한데, 어떤 상품을 봤는지 · 누구와 비슷한 행동을 했는지 ·
어떤 커뮤니티에 속하는지까지 보면 더 풍부한 표현이 생긴다.

> **깊이는 3페이지 수준이다.** message passing의 수식이나 GCN/GAT/GraphSAGE 같은 변종 구분은 없다.
> **"이웃 정보를 수치 표현으로 집계하는 모델"** 정도로 이해하고 넘어가는 게 강의의 의도로 보인다.

## ⭐ LLM과 Graph의 결합 3패턴

> **"그래프에는 구조는 있는데 텍스트 의미가 약하다. LLM에는 의미는 있는데 구조 추적이 약하다.
> 그럼 둘을 결합하면 더 좋아지지 않을까?"**

### 패턴 1 — GNN-driving-LLM (LLM이 그래프 학습을 돕는다)

노드 분류·링크 예측·그래프 예측은 **그래프 모델이 수행**하고, LLM이 좋은 텍스트 의미 정보를 넣어주는
역할.

예시가 구체적이다 — 기업 지식 그래프에서 노드는 문서·팀·서비스·테이블·대시보드(각 노드에 설명
텍스트가 존재), 엣지는 `owned_by` `depends_on` `documented_by` `upstream_of`.
노드 설명 텍스트(문서 제목, 테이블 설명, 위키 본문, 서비스 설명)를 **bag-of-words 수준으로 쓰기엔
의미 손실이 크다.** LLM을 활용해: 노드 설명 텍스트에서 의미 벡터 추출 · 비슷한 노드끼리 semantic
feature 생성 · 사람이 안 단 라벨을 **pseudo-label**로 추정 · 노드 설명 문장 정리 · sparse한 속성 보강.

### 패턴 2 — LLM-driving-GNN (그래프를 LLM 입력 문맥으로)

그래프를 text prompt나 graph prompt로 변환해 LLM이 직접 추론. **그래프는 학습 대상이 아니라 입력
컨텍스트로 동작.** GNN이나 전통적 graph algorithm만으로는 한계인 것에 LLM이 강하다 — 사람이
이해하기 쉬운 설명 생성 · 관계 기반 자연어 QA · 여러 hop을 따라가며 맥락 기반 추론 · 부분 그래프 요약
· **provenance를 포함한 답변 생성.**

**그래프를 입력으로 넣는 네 가지 방법:**

| | 형태 | 특징 |
|---|---|---|
| 1 | **Triple** — `User_A viewed Item_X` / `Item_X belongs_to Category_Books` | 관계 정보를 비교적 자세히 보존 |
| 2 | **인접 관계 요약** — `Node: sales_summary` + `produced_by: daily_sales_etl` `consumed_by: sales_dashboard` `owned_by: data_platform_team` | 특정 노드 중심 local graph를 요약. 질문 중심으로 필요한 관계만 짧게 |
| 3 | **Path 중심** — `raw_orders → daily_sales_etl → sales_summary → sales_dashboard` | ⭐ **"중요한 건 연결 한 개가 아니라 연결이 이어져서 어떤 의미 있는 경로를 만드는가"** |
| 4 | **JSON / structured prompt** | 파싱이 쉽고 출력 구조화에 유리 |

**이 네 가지 표현 전략이 이 소단원의 가장 실용적인 부분**이다. GraphRAG를 직접 구현할 때 바로 쓰인다.

### 패턴 3 — GNN-LLM-co-driving

**구조는 GNN이(structure 담당), 텍스트 의미는 LLM이(semantics 담당).** 세 가지 구조:

- **구조 A: LLM 임베딩을 GNN 입력으로** — 텍스트를 LLM으로 인코딩 → 노드의 semantic embedding 생성
  → 이를 노드 feature로 GNN에 투입 → neighborhood message passing → prediction.
  **LLM은 feature extractor, GNN은 구조 학습기.**
- **구조 B: Dual encoder** — 텍스트 인코더와 그래프 인코더를 따로 두고 출력을 concat·attention·gating
  으로 합침. **멀티모달 모델과 비슷하다** — 한쪽은 의미 벡터, 한쪽은 구조 벡터.
- **구조 C: 공동 추론 파이프라인** — 학습기를 하나로 합치지 않고 시스템 차원에서 협업.
  그래프가 subgraph/candidate retrieval → GNN이 구조 기반 score 계산 → LLM이 후보를 읽고 설명/재랭킹
  → 최종 output. **production system에서 자주 나오는 형태**이고 추천·enterprise search·RAG에서 활용.

## GraphRAG (예고편)

일반 RAG는 질문과 가까운 문서 조각을 검색해 답변을 생성한다. GraphRAG는 문서 집합에서 entity
knowledge graph를 먼저 구성 → 관련 엔터티를 community로 묶고 community summaries를 미리 생성 →
질문이 오면 국소 정보와 전역 요약을 함께 활용.

구성 5단계와 local/global 질문 구분은 **Ch4에서 같은 내용이 더 자세히 반복된다.**
→ [[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]]

## ⭐⭐ DE 관점 — 모델보다 먼저 컨텍스트 레이어

**Part 3에서 데이터 엔지니어에게 하는 가장 강한 주장.**

> **"Graph + AI의 첫 번째 가치는 모델 고도화가 아니라 컨텍스트 정렬이다.
> LLM이 바로 답을 잘 만드는 것이 핵심이 아니라, LLM이 읽을 수 있는 구조화된 컨텍스트를 누가, 어떻게
> 만들 것인가가 핵심이다.
>
> 데이터 엔지니어의 역할은 문서 조각을 많이 넣는 것이 아니라 —
> 데이터셋, 잡, 런, 대시보드, 차트, 오너, 용어집, 품질 상태, 정책, 엔터티 관계를 연결해
> AI가 근거와 맥락을 함께 읽게 만드는 것.
>
> Graph + AI의 성패는 모델 성능보다, AI가 읽는 운영 컨텍스트를 얼마나 정확하고 최신으로 구조화했는가에
> 달려 있다. 그 컨텍스트를 가장 잘 만들 수 있는 역할이 데이터 엔지니어다."**

> **[[Context engineering]](Part 2)의 직계 후속이다.** Part 2가 "Feature가 있던 자리를 컨텍스트가
> 대체한다"였다면, Part 3는 **"그 컨텍스트를 무엇으로 만드나 — 그래프로"** 라고 답한다.
> 두 파트가 강사도 다르고 서로를 인용하지도 않는데 논지가 이어진다.

## 기존 페이지와의 대조

- **[[GraphRAG]]에 통합** — 세 층위, GNN, 3결합 패턴, 4가지 입력 표현, DE 관점이 그 concept로 들어갔다.
- **[[Context engineering]] 보강** — "컨텍스트를 무엇으로 구조화하나"에 답이 생긴다.
- **Ch4와 중복** — GraphRAG 절(04)은 Ch4의 축약판이다.

## 자료 품질

- ⚠️ **중복 슬라이드가 많다.** 패턴2 슬라이드가 2번(p60·p61), 패턴3 구조C가 2번(p68·p69) 반복된다.
- 인용 이미지 대부분 출처 미표기 (GNN 논문 도식, LLM-GNN 결합 구조도, RAG 개념도).
  GNN 도식은 학술 논문 figure로 보이는데 인용 표기가 없다.
- 출처 없는 수치 없음.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[GraphRAG]] · [[Knowledge graph]] · [[Graph data model]] · [[Context engineering]] ·
  [[Retrieval-augmented generation]] · [[LLMOps]]
- 앞: [[AI DE Course - Part3 Ch2 Graph in practice]]
- 다음: [[AI DE Course - Part3 Ch3 Ontology basics]]
- 본편: [[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]]

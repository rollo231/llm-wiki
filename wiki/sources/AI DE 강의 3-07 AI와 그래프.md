---
type: source
title: AI DE 강의 3-07 AI와 그래프
aliases: [AI DE 3-07]
tags: [AI-DE-강의, 그래프, LLM, GNN]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part3/02. Ch2. Graph에 대한 이해.pdf"
---

# AI DE 강의 3-07 AI와 그래프

[[AI 데이터 엔지니어링 강의]] Part 3 Ch2의 마지막 소단원. AI 시대에 그래프가 다시 중요해진 이유를 들고, AI에서 그래프가 쓰이는 세 층위(데이터·모델·검색), 그래프 신경망(GNN), LLM과 그래프를 결합하는 세 패턴, GraphRAG의 개요를 차례로 다룬 뒤 "모델보다 먼저 컨텍스트 레이어"라는 데이터 엔지니어 관점으로 맺는다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 3 「시멘틱 & 컨텍스트 기반 데이터 설계」 |
| 덱 제목 | Ch2. Graph에 대한 이해: 4. Graph에 대해 이해하기 4 |
| 원본 파일 | `part3/02. Ch2. Graph에 대한 이해.pdf` p51–74 (24p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-04-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch2`, 소단원 번호 `4`는 표지 슬라이드. Ch2의 네 소단원은 제목이 모두 「Graph에 대해 이해하기 N」이라, 위키가 주제로 이름을 붙여 나눴다(사용자 결정) |

## 요약

### 01. AI와 그래프 (p53–54)

- LLM은 텍스트 의미에 강하지만, 문서 조각을 벡터로만 찾는 방식은 "전체 데이터셋의 핵심 주제는 무엇인가" 같은 전역 질문에 약할 수 있다. 그래프는 엔터티와 관계를 구조화하고, 커뮤니티 단위로 요약을 만들고, 국소 탐색과 전역 요약을 나눠 다룰 수 있다.
- AI에서 그래프가 쓰이는 세 층위:

| 층위 | 내용 |
|---|---|
| Graph as Data | 추천, 지식 그래프, 메타데이터, 분자 구조, 소셜 네트워크처럼 입력 자체가 그래프 |
| Graph as Model | 그래프 구조를 학습하는 모델. 대표가 GNN |
| Graph as Retrieval / Memory / Reasoning Layer | 문서 집합에서 entity graph를 만들고 그 위에서 retrieval, 요약, provenance 추적 |

### 02. 그래프 신경망 (p55–57)

GNN은 그래프로 표현할 수 있는 데이터를 처리하는 신경망이다. 강의는 CNN이 이미지에서, LSTM이 시계열에서 특징을 뽑듯 GNN은 그래프 구조에서 특징을 뽑는다고 비유한다. 노드의 의미는 이웃과의 관계로 달라지므로, 노드 표현은 자기 feature와 이웃·연결 구조를 함께 반영해 학습한다. 예: 사용자 프로필만으로는 부족하고, 어떤 상품을 봤는지, 누구와 비슷하게 행동했는지, 어떤 커뮤니티에 속하는지까지 보면 표현이 풍부해진다.

### 03. LLM과 그래프의 결합 세 패턴 (p58–69)

"그래프에는 구조가 있는데 텍스트 의미가 약하고, LLM에는 의미가 있는데 구조 추적이 약하다."

| 패턴 | 누가 예측·추론하나 | 강의의 예 |
|---|---|---|
| 1. GNN-driving-LLM | 그래프 모델(노드 분류, 링크 예측). LLM은 노드 설명 텍스트의 의미 정보를 넣어 준다 | 기업 지식 그래프: 문서·팀·서비스·테이블 노드의 설명을 LLM이 읽어 의미 벡터, pseudo-label, 설명 정리, sparse 속성 보강 |
| 2. LLM-driving-GNN | LLM. 그래프는 학습 대상이 아니라 입력 컨텍스트 | 설명 생성, 자연어 QA, 여러 hop 추론, 부분 그래프 요약, provenance를 포함한 답변 |
| 3. GNN-LLM-co-driving | 둘이 함께. 구조는 GNN, 의미는 LLM | 구조 A(LLM 임베딩을 GNN 노드 feature로, [[임베딩]]), 구조 B(dual encoder로 의미 벡터와 구조 벡터를 합침), 구조 C(시스템 차원의 공동 추론) |

패턴 2에서 그래프를 LLM 입력으로 넣는 방법은 네 가지다.

| 방식 | 모양 | 특징 |
|---|---|---|
| Triple | `User_A viewed Item_X` | 관계를 그대로 reasoning 재료로. 국소 그래프의 관계를 자세히 보존 |
| 인접 관계 요약 | `Node: sales_summary` 아래 `produced_by`, `consumed_by`, `owned_by`, `documented_by` | 질문 중심으로 필요한 관계만 짧게 |
| Path 중심 | `raw_orders -> daily_sales_etl -> sales_summary -> sales_dashboard` | 연결이 이어져 만드는 경로의 의미를 살림 |
| JSON / structured prompt | `{"entity": ..., "relations": {...}, "question": ...}` | 파싱이 쉽고 출력 구조화에 유리 |

구조 C(그래프가 subgraph·후보를 retrieval → GNN이 구조 기반 점수 → LLM이 읽고 설명·재랭킹 → 최종 출력)를 강의는 "production system에서 자주 나오는 형태"로, 추천·enterprise search·RAG에서 자주 쓴다고 한다.

### 04. GraphRAG 개요 (p70–73)

일반 RAG가 질문과 가까운 문서 조각을 찾는다면, GraphRAG는 문서 집합에서 entity knowledge graph를 먼저 만들고 커뮤니티로 묶어 요약을 미리 만든 뒤 국소 정보와 전역 요약을 함께 쓴다. 구성 다섯 단계(chunk 분할 → 개체·관계 추출 → entity graph → 커뮤니티 요약 → 질의 시 subgraph·요약 전달)와, 로컬 질문(특정 엔터티 주변 1~2 hop)과 글로벌 질문(community summaries, corpus-level synthesis)의 분기를 소개한다.

### 05. 데이터 엔지니어 관점 (p74)

"Graph + AI의 첫 번째 가치는 모델 고도화가 아니라 컨텍스트 정렬." 핵심은 LLM이 바로 답을 잘 만드는 것이 아니라, LLM이 읽을 구조화된 컨텍스트를 누가 어떻게 만드느냐다. 데이터 엔지니어의 역할은 문서 조각을 많이 넣는 것이 아니라 데이터셋, 잡, 런, 대시보드, 차트, 오너, 용어집, 품질 상태, 정책, 엔터티 관계를 연결해 AI가 근거와 맥락을 함께 읽게 하는 것이다.

## 핵심

- 패턴 1·2의 이름은 슬라이드 설명과 나란히 보면 반대로 읽히기 쉽다. "LLM이 그래프 학습을 돕는" 쪽이 GNN-driving-LLM이다. 슬라이드가 틀린 것은 아니다. 출처로 보이는 You et al., "Large Language Models Meet Graph Neural Networks: A Perspective of Graph Mining"(arXiv 2412.19211, 2024-12-26; *Mathematics* 13(7):1147, 2025)도 같은 매핑을 쓴다. 이 서베이에서 GNN-driving-LLM은 GNN이 중심 처리기로 최종 예측을 하고 LLM이 텍스트 속성을 해석해 임베딩을 공급하는 방식이고, LLM-driving-GNN은 그래프를 텍스트로 바꿔 LLM이 직접 예측·추론하는 방식이다. 즉 이름의 앞쪽이 최종 예측을 맡는 주체다. GNN-driving-LLM은 "GNN이 주도하고 LLM을 부품으로 쓴다"로 읽으면 맞고, 슬라이드처럼 "LLM이 돕는 경우"를 먼저 떠올리면 헷갈린다. [https://arxiv.org/abs/2412.19211 , 2026-09-28 확인] 슬라이드에는 이 서베이 출처가 없다. 다른 서베이들은 LLM이 맡는 역할로 나눈다. Li et al.(arXiv 2311.12399)은 enhancer·predictor·alignment component, Jin et al.(arXiv 2312.02783)은 LLM as Predictor·Encoder·Aligner다(두 초록, 2026-09-28 확인). You et al. 초록의 세 번째 범주 표기는 GNN-LLM-co-driving이다.
- 패턴 2의 네 입력 방식은 GraphRAG에서 검색한 서브그래프를 프롬프트에 넣는 방법과 같다. 강의가 둘을 잇지는 않지만, 이 표가 [[GraphRAG]]의 "subgraph를 LLM 컨텍스트로 전달" 단계의 구체적인 모양이다. 이 연결은 위키의 관찰이다.
- 마지막 슬라이드의 "컨텍스트 레이어"는 Part 2가 [[LLMOps]]에서 말한 컨텍스트 엔지니어링과 같은 방향이다. Part 2는 프롬프트에 넣을 문서의 버전·권한을 다뤘고, 여기서는 그 문서들 사이의 관계(메타데이터 그래프)를 데이터 엔지니어의 산출물로 든다([[데이터 거버넌스와 카탈로그]], [[지식 그래프]]).
- GraphRAG 부분의 전문은 [[GraphRAG]]에 있다. 여기서는 개요만 나오고, 본격적인 설명은 [[AI DE 강의 3-13 GraphRAG 개념과 사례]]에 있다.

## 주의·결함

- 중복 슬라이드가 셋이다. p55와 p56(GNN 정의, p56은 "인공신공망" 오타), p60과 p61(패턴 2), p68과 p69(구조 C)가 같은 내용이다.
- p60의 "GNN이나 전통적 graph algorithm만으로는 한게"는 "한계"의 오타다.
- GNN은 CNN·LSTM과의 비유와 "이웃 정보를 수치 표현으로 집계한다"까지만 설명한다. message passing은 p66에 단어로만 나오고, 어떤 GNN 계열(GCN, GraphSAGE 등)이 있는지는 없다.
- GraphRAG가 이 소단원(p70–73)과 Ch4에 두 번 나오지만, 두 강의는 서로를 참조하지 않는다. p70–73의 설명은 Microsoft GraphRAG 논문의 구조인데 논문 이름을 대지 않는다.
- 슬라이드 전체에 출처 표기가 없다.

## 관련

- 개념: [[GraphRAG]] · [[지식 그래프]] · [[그래프 데이터 모델]] · [[검색 증강 생성]] · [[LLMOps]] · [[데이터 거버넌스와 카탈로그]] · [[임베딩]]
- 엔티티: [[Microsoft GraphRAG]]
- 이전 강의: [[AI DE 강의 3-06 그래프의 실무 활용]]
- 다음 강의: [[AI DE 강의 3-08 온톨로지와 RDFS·OWL]]

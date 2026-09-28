---
type: source
title: AI DE 강의 3-13 GraphRAG 개념과 사례
aliases: [AI DE 3-13]
tags: [AI-DE-강의, RAG, 그래프, LLM]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part3/04. Ch4. Graph-RAG.pdf"
---

# AI DE 강의 3-13 GraphRAG 개념과 사례

[[AI 데이터 엔지니어링 강의]] Part 3 Ch4의 소단원 2·3 「Graph-RAG의 개념과 사례 1·2」를 묶은 페이지다(같은 제목의 연속 소단원은 묶는다는 분할 규칙). 앞 절반은 Microsoft GraphRAG 논문의 인덱싱·질의 파이프라인과 실무에서 넓게 쓰이는 네 가지 GraphRAG 패턴, 뒤 절반은 논문 이후의 변형(Auto-Tuning, DRIFT, LazyGraphRAG)과 제품 사례(Neo4j 고객 사례, AWS Bedrock, AWS GraphRAG Toolkit)를 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 3 「시멘틱 & 컨텍스트 기반 데이터 설계」 |
| 덱 제목 | Ch4. Graph-RAG: 2. Graph-RAG의 개념과 사례 1 (p15–33) · 사례 2 (p34–49) |
| 원본 파일 | `part3/04. Ch4. Graph-RAG.pdf` p15–49 (35p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-04-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch4`, 소단원 번호 `2`는 표지 슬라이드. 두 표지 모두 번호가 `2`이고 끝의 "1"·"2"로만 구분한다 |

## 요약

### 01. GraphRAG가 별도 주제인 이유 (p17)

기존 RAG는 문서 조각 검색이 중심이라, 코퍼스 전체를 묻는 질문, 문서 간 관계를 따라가야 하는 질문, 다중 hop 질문, 전역 요약과 국소 탐색이 함께 필요한 질문에서 한계가 드러난다. 강의는 Microsoft 논문의 출발점("이 데이터셋 전체의 핵심 주제는 무엇인가 같은 global question에는 실패한다")을 옮긴다.

### 02. From Local to Global: Microsoft GraphRAG (p18–21)

"나무가 아닌 숲을 보는 RAG". 파이프라인은 두 시점으로 나뉜다.

| 시점 | 단계 | 내용 |
|---|---|---|
| Indexing Time (지식의 구조화) | 추출 | 문서를 청크로 나누고 개체와 관계를 추출(Element Instances) |
| | 구조화 | 개체를 이어 지식 그래프를 만들고, 각 노드·간선이 어떤 맥락에서 나왔는지 LLM이 짧게 요약(Element Summaries) |
| | 추상화 | Leiden 같은 알고리즘으로 커뮤니티를 찾고 커뮤니티마다 고수준 요약 생성(Community Summaries) |
| Query Time (추론 및 합성) | 병렬 검색 | 관련 커뮤니티 요약을 동시에 참조 |
| | 중간 답변 | 커뮤니티 관점마다 부분 답변(Community Answers) |
| | 최종 합성 | 부분 답변을 모아 하나의 답(Global Answer) |

강의는 인덱싱을 "Top-Down", 질의를 "Bottom Up"이라고 부르고, 인덱싱이 끝나면 "데이터 전체는 A, B, C라는 주요 주제로 구성되어 있다"는 지도가 미리 생긴다고 설명한다.

### 03. 현실 세계의 GraphRAG (p22–23)

실무에서는 retrieval 단계가 그래프 구조를 쓰면 GraphRAG라고 부르는 경우가 많다. 지식 그래프를 직접 탐색하는 retrieval, 벡터 검색 뒤 그래프 순회로 주변 사실을 확장하는 방식, 커뮤니티 요약을 쓰는 방식, 서브그래프를 LLM 컨텍스트로 넘기는 방식이 모두 넓은 의미의 GraphRAG다. 강의의 요약: "GraphRAG의 본질은 그래프 DB 사용 여부가 아니라 검색 가능한 지식의 단위를 문서 조각에서 구조화된 의미 단위로 바꾼 것." retrieval 대상이 chunk에서 entity, relationship, subgraph, community summary, graph path로 넓어진다.

### 04. GraphRAG가 RAG 한계를 넘는 방식 (p24–25)

| 기존 RAG의 한계 | GraphRAG의 대응 | 핵심 메커니즘 |
|---|---|---|
| 파편화된 정보(구조적 연결성 부족) | 개체 간 관계를 그래프로 명시화 | Entity Graph |
| 전역 질문 취약 | 커뮤니티 단위 사전 요약 | Community Summary |
| 다단계 추론 약화 | 그래프 탐색으로 연쇄적 정보 도출 | Graph Traversal |
| 긴 컨텍스트의 불안정성 | 필요한 서브그래프와 요약만 선택 | Subgraph Selection |

현실에서 받아들여지는 가치는 세 가지다. 설명 가능성(entity path, subgraph, source link), 관계 중심 도메인 질의(고객-상품-브랜드, 계정-기기-IP, Dataset-Job-Dashboard), 구조화 데이터와 비구조화 문서의 결합.

### 05. 네 가지 대표 패턴 (p26–29)

| 패턴 | 작동 | 활용 예 |
|---|---|---|
| P1 논문형(Full-Extract) | 모든 문서에서 개체·관계를 추출하고 커뮤니티 요약을 사전 생성 | 거대 문서군의 전역 통찰 |
| P2 하이브리드 확장(Search & Expand) | 벡터 검색으로 청크를 찾고, 그 청크 속 개체의 k-hop 이웃을 그래프에서 추가 조회 | 특정 인물·사건 중심 심층 조사 |
| P3 엔터프라이즈 그라운딩 | 문서에서 개체를 새로 뽑는 대신 기존 마스터 데이터(CRM, ERP)나 메타데이터 그래프를 기준점으로 | 신뢰성이 최우선인 사내 데이터 |
| P4 NL2Query(Text-to-Graph) | 질문을 Cypher·Gremlin 같은 그래프 쿼리로 변환해 정형 관계를 조회 | 정형·비정형 결합 조회 |

P2의 "하이브리드"는 벡터 검색 + 그래프 순회다. Part 5(5-04)의 [[하이브리드 검색]]은 BM25 + 밀집 검색이라 이름만 같다.

P1은 인덱싱 비용이 크지만 포괄적 질문에 가장 정확하고, P3는 "LLM이 추출한 그래프가 정확해?"라는 불신을 검증된 사내 그래프로 푼다(문서의 "A배터리"를 DB의 P-1004 노드에 연결). P4는 LLM을 검색기가 아닌 쿼리 생성기로 쓰며 결과가 결정론적이어야 하는 분석에 맞는다.

### 06. 사례 (p30–33)

- Neo4j·Deloitte가 공개한 technology media 기업 사례: Neo4j GraphRAG와 Amazon Bedrock으로 자연어 분석 플랫폼을 만들어 time-to-insight 10배 개선, 반복 요청의 분석가 시간 92% 감소, 150명 이상의 비즈니스 사용자. 게임·프로모션·시장 이벤트·매출 같은 비즈니스 엔터티를 중심에 둔 분석용 world model이라는 점을 강조한다.
- DUCK / Kiku AI: 고객 대화·리뷰·커뮤니티 데이터를 Neo4j 지식 그래프로 연결하고, 그래프를 "foundation of facts"로 두고 LLM이 그 위에서 추론한다.

### 07. 논문 이후의 확장 (p36–38)

후속 변형이 나온 이유로 세 가지 운영 문제를 든다. 인덱싱 비용이 크다, 질문 유형마다 맞는 방식이 다르다(local 질문에는 과하다), 도메인 적응이 어렵다. 확장 방향으로는 질문 유형별 검색 전략 분화, 도메인별 인덱싱 자동화, global search 비용 절감, dynamic community 선택, "개발자 사용성을 높인 1.0 정리"를 든다.

### 08. 변형들 (p39–45)

- GraphRAG Auto-Tuning: 샘플 문서로 도메인을 식별하고 persona와 few-shot 프롬프트를 자동 생성한다. "GraphRAG의 품질은 그래프 질의 전에 무엇을 entity와 relation으로 뽑아내느냐에서 이미 갈린다."
- Global Search와 Local Search의 분기, 그리고 둘을 잇는 DRIFT Search: 상위 community report로 넓은 첫 답과 follow-up 질문을 만든 뒤 local search로 세부를 판다.
- LazyGraphRAG: 사전 요약을 크게 줄이고 질의 시점의 relevance test와 query refinement에 계산을 몰아준다. Microsoft는 인덱싱 비용이 vector RAG와 같고 full GraphRAG의 0.1% 수준이라고 설명한다. p45의 그림은 Build Index → Refine Query → Match Query → Map Answers → Reduce Answers의 깔때기다.

### 09. 제품 사례 (p46–49)

- AWS Bedrock Knowledge Bases GraphRAG: 문서에서 entity·fact·relationship을 자동 추출해 Neptune Analytics에 그래프와 벡터를 함께 저장하고, 검색 시 벡터 유사도 검색과 그래프 순회를 결합한다. 강의는 "managed service 형태로 운영 가능해졌다"는 점을 짚는다.
- AWS GraphRAG Toolkit: 오픈소스 Python 프레임워크. 비정형 데이터에서 그래프와 벡터 임베딩을 자동 구성하고 질의응답 전략을 제공한다.
- 맺음: "실무형 GraphRAG는 논문 구현 복제가 아니라 문제 구조에 맞는 graph-aware retrieval 패턴 선택."

## 핵심

- GraphRAG의 정의, 논문형과 넓은 의미의 구분, 네 패턴의 전문은 [[GraphRAG]]에, Microsoft 구현과 그 변형·연표는 [[Microsoft GraphRAG]]에 모았다.
- 강의의 가장 쓸모 있는 문장은 "검색 가능한 지식의 단위를 바꾼 것"이다. [[AI DE 강의 3-12 RAG의 이해와 한계]]의 한계 1번(검색 단위는 chunk, 질문 단위는 structure)에 대한 직접적인 답이고, P3 엔터프라이즈 그라운딩은 Ch3에서 만든 [[지식 그래프]]와 Ch2의 메타데이터 그래프([[데이터 거버넌스와 카탈로그]])를 그대로 검색 기반으로 쓰는 경로다. 이 연결은 위키의 관찰이다.
- P3와 P4는 LLM이 그래프를 만드는 쪽이 아니라 이미 있는 그래프를 쓰는 쪽이다. 데이터 엔지니어가 가장 직접 기여하는 것도 이쪽이라는 점은 [[AI DE 강의 3-07 AI와 그래프]]의 맺음("모델보다 먼저 컨텍스트 레이어")과 같은 이야기다.

## 주의·결함

- ❗ p42는 DRIFT를 "Dynamic Reasoning with Fine-grained Information Tree"로 풀고 제목도 "DRFIT"로 적었다. Microsoft의 공식 약자는 "Dynamic Reasoning and Inference with Flexible Traversal"이다(Microsoft Research 블로그, 2024-10-31). 동작 설명(community report로 넓은 첫 답과 follow-up 질문, 이어서 local search)은 블로그와 맞다. [https://www.microsoft.com/en-us/research/blog/introducing-drift-search-combining-global-and-local-search-methods-to-improve-quality-and-efficiency/ , 2026-09-28 확인]
- ✅ LazyGraphRAG 수치는 원문 그대로다: "data indexing costs are identical to vector RAG and 0.1% of the costs of full GraphRAG"(2024-11-25). 다만 2026-09 기준 `microsoft/graphrag` 저장소에는 LazyGraphRAG 질의 엔진이 없고, 관련 인덱싱 방식(`graphrag index --method fast`)만 들어가 있다. 강의는 이것이 오픈소스로 쓸 수 있는지 말하지 않는다. 자세한 것은 [[Microsoft GraphRAG]].
- ✅ 논문의 "실패" 표현은 원문 그대로다. Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization"(arXiv 2404.16130, v1 2024-04-24, v2 2025-02-19)의 초록은 "RAG fails on global questions directed at an entire text corpus, such as 'What are the main themes in the dataset?'"라고 쓴다. p19의 단계 이름(Element Instances, Element Summaries)은 v1 용어이고, v2 그림은 Entities & Relationships → Knowledge Graph로 바뀌었다. [https://arxiv.org/abs/2404.16130 , 2026-09-28 확인]
- ✅ Neo4j 고객 사례의 수치(10x faster time-to-insight, 92% reduction in analyst time on routine data requests, 150+ business users daily)는 사례 페이지와 맞다. 단, 사례 페이지는 제목의 "Technology media company"와 달리 부제에서 이 회사를 "Gaming giant"로 부르고, 본문도 게임 프로모션 의사결정 이야기다. 같은 페이지에 "2-3 weeks now complete in seconds"라는 인용도 있다. [https://neo4j.com/customer-stories/technology-media-company/ , 2026-09-28 확인] 수치는 벤더 사례 페이지의 자기 보고다.
- DUCK은 스웨덴 기술 에이전시이고, Kiku AI는 Reddit·Facebook 대화를 Neo4j 그래프로 모아 대화형으로 질의하는 netnography 플랫폼이다. Cypher와 GDS의 FastRP를 쓰고 Amazon Bedrock으로 PoC를 만들었다("graph as our foundation of facts, and LLMs for… reasoning"). [https://neo4j.com/customer-stories/duck/ , 2026-09-28 확인] p33의 DUCK 슬라이드는 URL로 technology-media-company 페이지를 단다(p30의 URL을 옮긴 잔재로 보인다).
- ✅ Bedrock Knowledge Bases GraphRAG는 프리뷰 뒤 2025-03-07 GA다. 발표 페이지는 벡터 임베딩과 개체·관계 그래프를 Neptune Analytics에 자동 생성·저장하고 "combines vector similarity search with graph traversal"이라고 쓴다. 프리뷰가 re:Invent 2024에서 발표됐다는 것은 검증 보고에 기댄 것이고 확인하지 못했다. [https://aws.amazon.com/about-aws/whats-new/2025/03/amazon-bedrock-knowledge-bases-graphrag-generally-available , 2026-09-28 확인] AWS GraphRAG Toolkit은 `awslabs/graphrag-toolkit`(Apache-2.0)이고, 첫 GitHub release는 v1.0.0(2024-11-28)이다. 지금은 `graphrag-lexical-graph/v3.x`처럼 패키지별 태그를 쓴다. [https://github.com/awslabs/graphrag-toolkit , 2026-09-28 확인]
- p29의 "NL2Cypher"는 일반 명칭이다. Neo4j 제품 용어로는 Text2Cypher다(`neo4j-graphrag-python`의 `Text2CypherRetriever`). [https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html , 2026-09-28 확인]
- p36은 "RAPTOR 같은 인접 기법과 무엇이 다른지"를 예고하지만 본문에 RAPTOR가 없다. RAPTOR(Sarthi et al., ICLR 2024)는 청크를 임베딩·클러스터링·요약하기를 재귀적으로 반복해 아래에서 위로 요약 트리를 만들고, 질의 때 여러 추상화 수준에서 함께 검색한다. [https://arxiv.org/abs/2401.18059 , 2026-09-28 확인]
- p35 목차에는 「04 RAG의 한계」, 「05 RAG의 진화」가 있는데 본문에는 없다. 소단원 1의 목차(p2) 뒤 두 줄을 옮긴 잔재다. 실제 본문은 「03 제품 사례들」에서 끝난다.
- p39와 p40은 거의 같은 슬라이드다(p40에 "핵심 메시지" 머리만 더 붙었다). p31, p43, p45는 텍스트 없는 그림 슬라이드다. p43은 DRIFT의 트리 그림인데 설명이 없다.
- p37의 "개발자 사용성을 높인 1.0 정리"는 2024-12의 이정표다. 슬라이드 작성 시점(2026-04)에 저장소는 이미 2.x·3.x였고, 2026-09 현재 최신은 v3.2.0이다([[Microsoft GraphRAG]]).
- GraphRAG는 [[AI DE 강의 3-07 AI와 그래프]](Ch2 p70–73)에서 먼저 짧게 나오지만, 두 강의는 서로를 참조하지 않는다.

## 관련

- 개념: [[GraphRAG]] · [[검색 증강 생성]] · [[지식 그래프]] · [[그래프 데이터 모델]] · [[그래프 데이터베이스]] · [[데이터 거버넌스와 카탈로그]]
- 엔티티: [[Microsoft GraphRAG]] · [[Neo4j]] · [[Amazon Neptune]]
- 이전 강의: [[AI DE 강의 3-12 RAG의 이해와 한계]]
- 다음 강의: [[AI DE 강의 3-14 그래프 DB의 특징]]

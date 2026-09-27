---
type: concept
title: GraphRAG
aliases: [Graph RAG, Graph-RAG, 그래프 RAG, NL2Cypher, Text2Cypher, 그래프 기반 검색]
tags: [LLM, 검색, RAG, 그래프]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 3-07 AI와 그래프]]"
  - "[[AI DE 강의 3-12 RAG의 이해와 한계]]"
  - "[[AI DE 강의 3-13 GraphRAG 개념과 사례]]"
---

# GraphRAG

검색 단계에서 그래프 구조를 쓰는 [[검색 증강 생성]]이다. 좁게는 Microsoft 연구진의 논문(Edge et al. 2024)과 그 구현인 [[Microsoft GraphRAG]]를 가리키고, 넓게는 retrieval에 그래프를 넣는 설계 패턴의 묶음을 가리킨다. [[AI DE 강의 3-13 GraphRAG 개념과 사례]]는 넓은 쪽을 권한다: "GraphRAG는 하나의 제품명이 아니라 graph를 retrieval에 넣는 여러 설계 패턴의 묶음."

## 무엇을 바꾸나: 검색의 단위

[[AI DE 강의 3-12 RAG의 이해와 한계]]가 드는 RAG의 첫 번째 한계는 검색 단위(chunk)와 질문 단위(개체, 사건, 관계)가 다르다는 것이다. 장애 원인은 A 문서, 영향 범위는 B 문서, 복구 이력은 C 문서에 있으면 chunk 검색은 셋을 따로 찾는다.

GraphRAG는 검색 대상을 chunk에서 entity, relationship, subgraph, community summary, graph path로 넓힌다. 3-13의 표현으로 "본질은 그래프 DB 사용 여부가 아니라 검색 가능한 지식의 단위를 문서 조각에서 구조화된 의미 단위로 바꾼 것"이다. 그래서 그래프 DB 없이도(파일로 된 그래프와 요약으로도) GraphRAG일 수 있고, 그래프 DB를 써도 chunk만 검색하면 GraphRAG가 아니다. 이 마지막 문장은 위키의 정리다.

3-13이 정리한 한계와 대응:

| RAG의 한계 | GraphRAG의 대응 | 메커니즘 |
|---|---|---|
| 파편화된 정보 | 개체 간 관계를 그래프로 명시 | Entity Graph |
| 전역 질문 취약 | 커뮤니티 단위 사전 요약 | Community Summary |
| 다단계 추론 약화 | 그래프 탐색으로 연쇄 도출 | Graph Traversal |
| 긴 컨텍스트의 노이즈 | 필요한 서브그래프와 요약만 선택 | Subgraph Selection |

## 로컬 질문과 글로벌 질문

| | 로컬 질문 | 글로벌 질문 |
|---|---|---|
| 예 | 이 장애와 연결된 시스템은 무엇인가 | 전체 회의록에서 반복되는 리스크는 무엇인가 |
| 검색 | 특정 엔터티 주변 1~2 hop, 관련 chunk 몇 개 | community summaries, corpus 수준 종합 |
| 벡터 RAG | 대체로 잘 한다 | 약하다 |

벡터 RAG가 글로벌 질문에 약한 이유는, "핵심 주제가 무엇인가"의 답이 어느 한 chunk에도 들어 있지 않기 때문이다. 논문은 이를 query-focused summarization 과제로 본다([[Microsoft GraphRAG]]). 로컬과 글로벌을 잇는 방식으로 DRIFT Search가 있다.

## 네 가지 패턴

[[AI DE 강의 3-13 GraphRAG 개념과 사례]]의 분류다.

| 패턴 | 그래프의 출처 | 작동 | 맞는 곳 |
|---|---|---|---|
| P1 논문형(Full-Extract) | 문서에서 LLM이 추출 | 개체·관계 추출, 커뮤니티 요약 사전 생성 | 거대 문서군의 전역 통찰 |
| P2 하이브리드 확장 | 문서에서 추출 | 벡터 검색으로 chunk를 찾고 그 안 개체의 k-hop 이웃을 추가 | 특정 인물·사건 중심 조사 |
| P3 엔터프라이즈 그라운딩 | 기존 마스터 데이터·메타데이터 그래프 | 문서의 언급을 검증된 사내 그래프 노드에 연결 | 신뢰성이 최우선인 사내 데이터 |
| P4 NL2Query | 기존 그래프 DB | LLM이 스키마를 보고 Cypher·Gremlin 쿼리를 생성 | 결과가 결정론적이어야 하는 정형 분석 |

- P1·P2는 LLM이 그래프를 만든다. 추출 품질이 곧 그래프 품질이라, 3-13은 "GraphRAG의 품질은 그래프 질의 전에 무엇을 entity와 relation으로 뽑아내느냐에서 이미 갈린다"고 한다. 인덱싱 비용도 여기서 생긴다.
- P3·P4는 이미 있는 그래프를 쓴다. Part 3의 Ch1~3이 설계하는 것([[시맨틱 계층]], [[온톨로지]], [[지식 그래프]])이 그대로 이 패턴의 재료이고, 데이터 엔지니어의 몫이 가장 크다. 이 연결은 위키의 관찰이다.
- P4의 Neo4j 제품 용어는 Text2Cypher다(`neo4j-graphrag-python`의 `Text2CypherRetriever`가 스키마로 프롬프트를 만들고 LLM이 생성한 Cypher를 실행한다). NL2Cypher는 일반 명칭이다. [https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html , 2026-09-28 확인]

AWS Bedrock Knowledge Bases GraphRAG(2025-03-07 GA)는 위키가 분류하기에 P2를 관리형 기능으로 만든 예다. 문서에서 개체·관계를 자동 추출해 [[Amazon Neptune]] Analytics에 그래프와 벡터를 함께 두고, 검색 때 벡터 유사도와 그래프 순회를 결합한다. [https://aws.amazon.com/about-aws/whats-new/2025/03/amazon-bedrock-knowledge-bases-graphrag-generally-available , 2026-09-28 확인]

## LLM과 그래프를 결합하는 다른 축

[[AI DE 강의 3-07 AI와 그래프]]는 AI에서 그래프가 쓰이는 층위를 셋으로 나눈다(데이터, 모델, 검색·기억·추론 계층). GraphRAG는 세 번째 층위다. 같은 강의의 GNN·LLM 결합 세 패턴(You et al. 2024의 분류)과는 축이 다르다.

| 패턴 | 누가 최종 예측을 하나 | GraphRAG와의 관계 |
|---|---|---|
| GNN-driving-LLM | GNN. LLM은 노드 텍스트의 임베딩을 공급 | 그래프 학습. GraphRAG와 별개 |
| LLM-driving-GNN | LLM. 그래프는 텍스트로 바꾼 입력 컨텍스트 | GraphRAG의 생성 단계가 이 모양이다 |
| GNN-LLM-co-driving | 둘이 함께 | 구조 C(그래프 retrieval → GNN 점수 → LLM 재랭킹·설명)는 GraphRAG의 한 구현이 될 수 있다 |

LLM-driving-GNN에서 그래프를 LLM에 넣는 네 방식(triple, 인접 관계 요약, path, JSON)은 GraphRAG가 검색한 서브그래프를 프롬프트에 넣을 때의 선택지와 같다. 표의 셋째 열은 위키의 정리다.

## 언제 쓰지 않나

강의는 GraphRAG의 비용을 인덱싱 쪽에서만 말한다. 위키가 보기에 판단 기준은 [[그래프 데이터베이스]]를 들일지와 비슷하다. 질문이 대부분 로컬이고 한 문서 안에서 답이 나오면 벡터 RAG로 충분하다. 문서 간 관계나 전역 요약이 핵심이거나, 이미 검증된 그래프(메타데이터 그래프, 마스터 데이터)가 있을 때 GraphRAG의 값이 커진다. [[Microsoft GraphRAG]]의 후속 변형(LazyGraphRAG, DRIFT)이 이 비용 문제를 줄이려는 시도다.

## 관련

- [[검색 증강 생성]] — 바탕이 되는 RAG의 구조와 한계
- [[Microsoft GraphRAG]] — 논문형 구현과 후속 변형
- [[지식 그래프]] · [[그래프 데이터 모델]] · [[그래프 데이터베이스]] · [[Neo4j]] · [[Amazon Neptune]]
- [[데이터 거버넌스와 카탈로그]] — P3의 재료가 되는 메타데이터 그래프
- [[LLMOps]] — 컨텍스트 엔지니어링

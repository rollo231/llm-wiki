---
type: entity
title: Microsoft GraphRAG
aliases: [MS GraphRAG, LazyGraphRAG, DRIFT Search, GraphRAG Auto-Tuning]
tags: [도구, LLM, RAG, 그래프]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 3-07 AI와 그래프]]"
  - "[[AI DE 강의 3-13 GraphRAG 개념과 사례]]"
---

# Microsoft GraphRAG

Microsoft Research의 GraphRAG 논문과 그 오픈소스 구현(`microsoft/graphrag`, Python)이다. 문서 집합에서 LLM으로 지식 그래프를 만들고 커뮤니티마다 요약을 미리 만들어 두어, 벡터 RAG가 약한 "코퍼스 전체"에 대한 질문에 답한다. [[GraphRAG]]라는 이름을 널리 알린 구현이고, [[AI DE 강의 3-13 GraphRAG 개념과 사례]]의 "P1 논문형" 패턴이 이것이다.

## 논문

Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", arXiv 2404.16130(v1 2024-04-24, v2 2025-02-19). 출발점은 초록의 문장이다: "RAG fails on global questions directed at an entire text corpus, such as 'What are the main themes in the dataset?'" 이런 질문은 검색 과제가 아니라 query-focused summarization(QFS) 과제라서다. [https://arxiv.org/abs/2404.16130 , 2026-09-28 확인]

## 파이프라인

| 시점 | v1 용어(강의가 쓰는 것) | v2 그림의 용어 | 하는 일 |
|---|---|---|---|
| 인덱싱 | Source Documents → Text Chunks | Text Chunks | 문서를 청크로 자른다 |
| | Element Instances | Entities & Relationships | LLM이 개체와 관계를 추출한다 |
| | Element Summaries | Knowledge Graph | 노드·간선마다 등장 맥락을 요약해 그래프를 만든다 |
| | Graph Communities | Graph Communities | Leiden 알고리즘을 계층적으로 적용해 커뮤니티로 묶는다 |
| | Community Summaries | Community Summaries | 커뮤니티마다 고수준 요약(community report)을 만든다 |
| 질의(글로벌) | Community Answers | Community Answers | 관련 커뮤니티 요약마다 부분 답을 병렬로 만든다(map) |
| | Global Answer | Global Answer | 부분 답을 모아 하나로 합친다(reduce) |

v1과 v2 용어의 행 맞춤은 위키가 한 것이다(v2 그림은 단계를 다르게 묶는다). [[AI DE 강의 3-13 GraphRAG 개념과 사례]]는 v1 용어로 설명한다. 인덱싱이 끝나면 "데이터 전체는 A, B, C라는 주요 주제로 구성되어 있다"는 지도가 질문 전에 이미 있다는 것이 강의의 비유다.

## 검색 방식

2026-09 저장소의 `structured_search/`에는 네 가지가 있다: basic, local, global, drift.

- Global Search는 community report로 코퍼스 전체의 주제·패턴을 답한다. 넓지만 비싸다.
- Local Search는 특정 엔터티 주변의 개체·관계·청크로 답한다. 깊지만 전역 맥락이 약하다.
- DRIFT Search(2024-10-31 블로그)는 둘을 잇는다. 공식 약자는 "Dynamic Reasoning and Inference with Flexible Traversal"이다. primer 단계에서 관련도 top-K community report로 넓은 첫 답과 follow-up 질문을 만들고(HyDE 사용), follow-up을 local search로 실행한다. 기본 반복은 2회다. 강의(p42)는 약자를 "Dynamic Reasoning with Fine-grained Information Tree"로 잘못 적었다. [https://www.microsoft.com/en-us/research/blog/introducing-drift-search-combining-global-and-local-search-methods-to-improve-quality-and-efficiency/ , 2026-09-28 확인]

## 후속 변형

| 이름 | 날짜 | 푸는 문제 | 내용 |
|---|---|---|---|
| Auto-Tuning | 2024-09-09 블로그 | 도메인 적응 | 샘플 문서로 도메인 persona, few-shot 예시, entity type을 자동 생성해 추출 프롬프트를 맞춘다 |
| DRIFT Search | 2024-10-31 블로그 | 질문 유형 | 글로벌과 로컬을 잇는 검색 |
| LazyGraphRAG | 2024-11-25 블로그 | 인덱싱 비용 | 사전 요약을 줄이고 질의 시점의 relevance test·query refinement에 계산을 몰아준다 |

- LazyGraphRAG 블로그의 수치: "data indexing costs are identical to vector RAG and 0.1% of the costs of full GraphRAG". 글로벌 질의에서 GraphRAG Global Search와 비슷한 품질을 700배 넘게 낮은 질의 비용으로 내고, Global Search 비용의 4%로는 로컬·글로벌 모두에서 경쟁 방법보다 크게 낫다고 주장한다. Microsoft 자사 비교다. [https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ , 2026-09-28 확인]
- ⚠️ LazyGraphRAG는 2026-09 기준 오픈소스 저장소에 질의 엔진으로 들어가 있지 않다. 들어간 것은 관련 인덱싱 방식 `graphrag index --method fast`(FastGraphRAG, LLM 대신 NLP 명사구 추출)뿐이고, 코드 주석에 LazyGraphRAG 첫 벤치마크에 쓴 추출기라는 언급이 있다. 블로그의 2025-06-06 편집 노트는 Microsoft Discovery와 Azure Local에 통합됐다고만 적는다. 검증 과정에서 저장소를 clone해 확인했다(2026-09-28). 강의는 LazyGraphRAG를 쓸 수 있는지 말하지 않는다.

## 릴리스

| 버전 | 날짜 | 비고 |
|---|---|---|
| v1.0.0 | 태그 2024-12-11, 블로그 2024-12-16 | Typer CLI(시작 148초 → 2초), `init` 명령, 데이터 모델 정리(디스크 43% 감소), 워크플로 88개 → 11개, 증분 `update` 명령 |
| v3.2.0 | 2026-09-24 | 2026-09 현재 최신 |

강의(p37)의 "개발자 사용성을 높인 1.0 정리"는 2024-12의 이정표다. 슬라이드 작성 시점(2026-04)에는 이미 그 뒤 메이저 버전이 나와 있었다. [https://www.microsoft.com/en-us/research/blog/moving-to-graphrag-1-0-streamlining-ergonomics-for-developers-and-users/ , 2026-09-28 확인]

## 비용과 한계

[[AI DE 강의 3-13 GraphRAG 개념과 사례]]는 후속 변형이 나온 이유로 세 가지를 든다. 인덱싱 비용이 크다(개체 추출, 관계 정리, 커뮤니티 요약을 모두 LLM으로 미리 한다), 로컬 질문에는 과하다, 뉴스 문서용 추출 프롬프트가 다른 도메인에 잘 맞지 않는다. 위의 세 변형이 각각 하나씩에 대응한다. 이 대응 관계는 위키의 정리다.

## 관련

- [[GraphRAG]] — 넓은 의미의 패턴군, 이 구현의 위치
- [[검색 증강 생성]] — 벡터 RAG와 그 한계
- [[지식 그래프]] — 이 구현이 LLM으로 만드는 것
- 강의: [[AI DE 강의 3-07 AI와 그래프]] · [[AI DE 강의 3-13 GraphRAG 개념과 사례]]

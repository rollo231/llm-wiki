---
type: entity
title: Microsoft GraphRAG
area: [data-engineering, programming]
aliases: [MS GraphRAG, From Local to Global, LazyGraphRAG, DRIFT Search, GraphRAG Auto-Tuning]
tags: [data-engineering, graphrag, rag, llm, microsoft, knowledge-graph]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]]", "[[AI DE Course - Part3 Ch4 GraphRAG variants and products]]"]
---

# Microsoft GraphRAG

**[[GraphRAG]]라는 이름을 만든 Microsoft의 논문이자 구현체.**

논문: *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*

## 출발점

> **"기존 RAG는 private / unseen corpus에 답하는 데 유용하지만,
> '이 데이터셋 전체의 핵심 주제는 무엇인가' 같은 global question에는 실패한다."**

**Key Concept: 나무가 아닌 숲을 보는 RAG.** 기존 RAG의 한계는 특정 키워드 중심의 파편화된 정보
검색(point-lookup)이고, 해법은 데이터 간 관계를 그래프로 구조화하고 **계층적으로 요약**해 전역적
통찰을 도출하는 것.

## 파이프라인

**Indexing Time** (Top-Down) — 추출(Extraction) → 구조화(Structuring) → 추상화(Abstraction).
Leiden 같은 알고리즘으로 community를 찾고 community별 요약본을 미리 생성한다.

**Query Time** (Bottom-Up) — 병렬 검색(Parallel Retrieval) → 중간 답변(Community Answers) →
최종 합성(Global Answer).

→ 상세 다이어그램과 구성 요소는 [[GraphRAG]].

## 논문 이후의 확장

초기 논문형의 핵심은 문서에서 entity knowledge graph를 만들고 community summary를 생성한 뒤
global/local 질문에 대응하는 것이었다. 이후 확장 방향:

- 질문 유형별 검색 전략 분화
- domain-specific indexing 자동화
- global search 비용 절감
- dynamic community 선택
- graph 구축 비용과 품질의 trade-off 최적화
- **개발자 사용성을 높인 1.0 정리**

## 세 가지 변형

| 변형 | 해결하려는 문제 |
|---|---|
| **Auto-Tuning** | 도메인 적응 — 샘플 문서로 도메인을 식별하고 persona와 few-shot prompt를 자동 생성 |
| **DRIFT Search** (Dynamic Reasoning with Fine-grained Information Tree) | 질문 유형 분기 — 상위 community report로 넓은 초기 답과 follow-up question을 만들고, 그 다음 local search로 세부를 파고듦 |
| **LazyGraphRAG** | 비용 구조 — 사전 요약을 크게 줄이고 질의 시점에 relevance test와 query refinement를 집중 |

> **"GraphRAG의 후속 진화는 성능 욕심이 아니라 비용·질문 유형·도메인 적응 문제를 해결하려는 과정이다."**

### ⚠️ LazyGraphRAG 수치는 자사 벤치마크

Microsoft는 LazyGraphRAG indexing cost가 vector RAG와 같고 **full GraphRAG의 0.1% 수준**이라고
설명하고, 일부 설정에서 global/local 질의 품질을 유지하거나 능가하면서 비용을 크게 낮췄다고 주장한다.
**자사 비교이므로 그대로 인용하기 전 검증이 필요하다.**

## 실무형 GraphRAG와의 관계

> **"논문형 GraphRAG는 하나의 대표 구현이고, 실무형 GraphRAG는 그보다 넓은 graph-aware retrieval
> architecture로 이해하는 편이 좋다."**

[[GraphRAG]]의 4패턴 중 **P1(논문형 Full-Extract)** 이 이 구현에 해당한다. 비정형 텍스트를 구조적
데이터로 **완전히 재설계**하므로 인덱싱 비용이 크지만, 질문 시점에 문서 전체를 보지 않아도 Community
Summary로 답할 수 있어 **포괄적인 질문에 가장 정확**하다.

## 링크

- [[GraphRAG]] — 개념·4패턴·변형 상세
- [[Retrieval-augmented generation]] — 대응 대상인 RAG 한계
- [[Knowledge graph]] — 산출되는 entity graph
- [[Amazon Neptune]] — 경쟁하는 제품화 경로(AWS Bedrock Knowledge Bases GraphRAG)
- 강의: [[AI Data Engineering (Fast Campus course)]]

## 1차 자료

- *From Local to Global: A Graph RAG Approach to Query-Focused Summarization* — Microsoft.
  **인제스트 후보.**

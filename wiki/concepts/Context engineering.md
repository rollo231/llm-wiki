---
type: concept
title: Context engineering
area: [data-engineering]
aliases:
  - 컨텍스트 엔지니어링
  - Token budget
  - 토큰 예산
tags: [data-engineering, llmops, llm, rag, prompt, context]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part2 Ch2 LLMOps]]"]
---

# Context engineering

**LLM 서비스에서 성능을 좌우하는 것은 모델이 아니라 입력 구성(컨텍스트)이라는 관점.**
기존 ML의 Feature Engineering이 있던 자리를 대체한다.

| | 기존 ML | LLM |
|---|---|---|
| 성능을 좌우하는 것 | **Feature** | **컨텍스트** |
| 엔지니어가 만드는 것 | 파생 변수, 집계, 스케일링 | 무엇을 · 얼마나 · 어떤 순서로 · 얼마나 압축해서 넣을지 |

> **"LLM의 성능은 모델보다 컨텍스트 설계에 의해 더 크게 변한다."**

## 결정해야 할 4가지

| 결정 | 파라미터 | 트레이드오프 |
|---|---|---|
| **무엇을 넣는가** | source 선택 | 관련 없는 소스는 노이즈이자 [[LLMOps\|prompt injection]] 통로 |
| **얼마나 넣는가** | **top-k, token budget** | 많이 넣으면 recall↑·**비용↑**·noise↑ |
| **어떤 순서로 넣는가** | ranking (rerank) | 순서가 답변에 영향을 준다 |
| **얼마나 압축할 것인가** | summarization | 압축하면 싸지지만 근거가 흐려진다 |

**네 결정이 전부 품질과 비용을 동시에 움직인다.** [[LLMOps]]의 비용 통제 수단
(토큰 예산·캐싱·모델 라우팅·컨텍스트 압축) 중 세 개가 여기서 나온다 — **비용 문제와 품질 문제가
같은 다이얼**이라는 것이 이 개념의 실무적 무게다.

## 왜 Feature Engineering의 자리인가

[[Feature store]]가 관리하던 것이 *"어떤 값이 모델에 들어가는가"* 였다면, 컨텍스트 엔지니어링이
관리하는 것도 같은 질문이다. 다만 값이 숫자에서 **텍스트 덩어리**로 바뀌었을 뿐.

그래서 문제의 구조도 물려받는다:

- **버전 관리 대상이다** — chunking 전략·top-k·rerank 설정·프롬프트 템플릿이 전부 결과를 바꾼다
  → [[Data and model versioning]]
- **드리프트가 있다** — 검색 품질이 떨어지면 답변 품질이 떨어진다(Context Drift).
  피처 분포 모니터링이 하던 일을 retrieval 품질 모니터링이 한다
  → [[Data drift and training-serving skew]]
- **일관성 문제가 있다** — 같은 질문에 다른 컨텍스트가 붙으면 다른 답이 나온다

## 데이터 엔지니어의 지분

컨텍스트를 만드는 파이프라인이 곧 DE의 일이다 — 지식 소스 수집·정제, chunking·embedding,
Vector DB 인덱스 설계, 권한 기반 필터링. [[Unstructured data ingestion]]의 4단계가 그 실행이다.

## 열린 질문

- **"컨텍스트 설계가 모델보다 중요하다"의 근거** — 강의는 주장만 하고 비교 실험이나 인용을 대지
  않는다. 어느 정도 범위에서 참인지(작은 모델에서도? 긴 컨텍스트 모델에서도?) 확인이 필요하다.
- **top-k와 압축의 실무 기준** — 몇 개를 넣고 얼마나 줄일지의 출발점이 없다.
- **순서(ranking)가 답변에 미치는 영향의 크기** — "영향이 있다"까지만 나온다.
- Part 5(**RAG의 진화: Hybrid Search와 Reranking**)가 이 중 일부에 답할 가능성이 있다
  → [[AI Data Engineering (Fast Campus course)]]

## 링크

- 상위: [[LLMOps]]
- 대응하는 기존 개념: [[Feature store]] (피처 대 컨텍스트)
- 파이프라인: [[Unstructured data ingestion]]
- 출처: [[AI DE Course - Part2 Ch2 LLMOps]]

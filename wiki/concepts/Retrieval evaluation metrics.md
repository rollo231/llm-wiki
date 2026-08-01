---
type: concept
title: Retrieval evaluation metrics
area: [data-engineering]
aliases: [검색 평가지표, Recall@K, MRR, NDCG, NDCG@K, 검색 품질 측정]
tags: [evaluation, metrics, retrieval, rag, sli, data-engineering]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part5 Hybrid search and reranking]]"]
---

# Retrieval evaluation metrics

**검색 품질을 숫자로 재는 지표들. RAG에서는 "답변이 좋았다"는 인상 대신 검색단을 따로 측정할 수 있게
해 준다.**

| 지표 | 정의 | 무엇을 보나 |
|---|---|---|
| **Recall@K** | K개 결과 안에 관련 문서가 얼마나 들어왔나 | **놓치지 않았는가** |
| **MRR** | 첫 정답의 역순위 평균 (1위면 1, 3위면 1/3) | **정답에 얼마나 빨리 닿나** |
| **NDCG@K** | 순위의 질까지 반영한 종합 점수 | **잘 세웠는가** |

## ⭐ 단계마다 다른 지표를 쓴다

> **"Recall@K는 초기 검색, NDCG@K는 최종 품질 평가에 사용."** — 강의

이 한 줄이 [[Hybrid search and reranking]]의 Two-Stage 구조와 정확히 대응한다:

| | 목표 | 지표 |
|---|---|---|
| **Stage 1** (하이브리드 검색, Top-200) | 후보를 **놓치지 않는 것** | **Recall@K** |
| **Stage 2** (Cross-Encoder 리랭킹, Top-20) | **순서를 잘 세우는 것** | **NDCG@K** |

**Stage 1에서 놓친 문서는 Stage 2가 되살릴 수 없다.** 리랭킹은 주어진 후보 안에서만 순서를 바꾼다 —
그래서 앞단은 recall로, 뒷단은 순위 품질로 재는 것이 논리적으로 맞다.

> **거꾸로 말하면: 답변이 나쁠 때 "검색이 못 찾은 것"과 "찾았는데 순서가 나쁜 것"은 다른 문제이고,
> 두 지표가 그것을 갈라 준다.**

## NDCG를 조금 더

강의는 정의 한 줄로 끝내지만(수식 없음), 최소한 이 정도는 알아야 쓸 수 있다:

- **DCG** — 상위에 있는 관련 문서일수록 높은 점수를 주되, **순위가 내려갈수록 로그로 할인**한다
- **IDCG** — 이상적으로 정렬됐을 때의 DCG
- **NDCG = DCG / IDCG** → 0~1로 정규화되어 질의 간 비교가 가능해진다

**Recall과 달리 NDCG는 "관련도의 등급"을 반영할 수 있다** — 완전 관련/부분 관련을 구분해서 잰다.

## 운영 지표로 올리기

> **[[Data SLA and observability]]와 이어지는 지점.** Part 4가 `offline-online skew`를 SLI로
> 승격시켰듯, **RAG 시스템에서는 Recall@K·NDCG@K가 SLI 후보다.**

- **평가셋이 있어야 잴 수 있다** — 질문과 정답 문서의 쌍. 이것을 만들고 유지하는 것이 실제 일이며,
  [[ML data pipeline]]의 라벨링 문제와 같은 성격이다
- **인덱스·임베딩 모델·청킹 전략을 바꿀 때마다 재평가**해야 회귀를 잡는다
  ([[Data and model versioning]])
- 검색 지표가 좋아도 답변이 나쁠 수 있다 — **retrieval–generation mismatch**
  ([[Retrieval-augmented generation]]). **검색 지표는 검색만 증명한다**

⚠️ **강의는 목표값을 제시하지만**(`Recall@10 95%`, `MRR 0.85`, `NDCG@10 0.90`) **출처가 없고,
도메인·평가셋에 따라 크게 달라지는 값이라 그대로 쓰면 안 된다.** 자기 평가셋에서 기준선을 잡는 것이
먼저다.

## 관련 페이지

- [[Hybrid search and reranking]] — 이 지표들이 붙는 2단계 구조
- [[Retrieval-augmented generation]] — 검색 품질이 답변 품질로 자동 이어지지 않는 이유
- [[Data SLA and observability]] — SLI/SLO로 올리는 틀
- [[Vector database]] — 인덱스 설정(정확도↔지연)이 이 지표를 직접 움직인다

## 출처

- [[AI DE Course - Part5 Hybrid search and reranking]] (Fast Campus, Part 5)

---
type: concept
title: Hybrid search and reranking
area: [data-engineering]
aliases: [하이브리드 검색, Hybrid Search, 리랭킹, Reranking, 재랭킹, BM25, RRF, Reciprocal Rank Fusion, Cross-Encoder, Bi-Encoder, Two-Stage Retrieval, Sparse Retrieval, Dense Retrieval]
tags: [hybrid-search, bm25, rrf, reranking, cross-encoder, rag, retrieval, data-engineering]
created: 2026-08-01
updated: 2026-08-19
sources: ["[[AI DE Course - Part5 Hybrid search and reranking]]"]
---

# Hybrid search and reranking

**키워드 검색(sparse)과 벡터 검색(dense)을 함께 돌려 순위를 융합하고, 살아남은 소수만 정밀 모델로
다시 정렬하는 검색 구조.** 2026년 RAG 검색단의 실무 표준이다.

> ⭐ **한 줄 요약: 둘을 합치는 이유는 성능을 더하기 위해서가 아니라 서로의 실패를 덮기 위해서다.**

## 왜 — Dense-only의 실패 모드 3종

| 실패 | 증상 |
|---|---|
| **어휘적 정밀도 부족** | `"GPT-4"` ↔ `"GPT4"`, `"AWS"` ↔ `"Amazon Web Services"`, `"Python3.11"` ↔ `"Python 3.11"`을 놓친다 |
| **시맨틱 드리프트** | 도메인 밖 데이터에서 의미가 떠밀린다. 유사 의미 과적합, 의도와 다른 문서 |
| ⭐ **정보 압축 병목** | 768차원에 눌러 담으면서 **수치·스키마·식별자가 사라진다** |

**셋의 귀결:** 리콜 저하 → 컨텍스트 품질 악화 → **환각 증가**.

> ⭐ **"의미는 남고 식별자는 사라진다."** 임베딩이 버리기 쉬운 것이 하필 정확히 맞아야 하는
> 값들(버전·코드·금액)이다. → [[Text embeddings]]

**[[Retrieval-augmented generation]]의 한계 4종과 층위가 다르다.** 저쪽은 *시스템 수준*
(검색 단위 불일치·retrieval–generation mismatch·Lost in the Middle·고정 top-k),
이쪽은 *retriever 내부*. **두 목록은 보완적이다.**

## 구조

```
Query
  ├── BM25 (Sparse)  — 키워드·식별자 매칭  ┐
  └── Dense (Vector) — 의미·패러프레이즈    ┘  병렬 실행
              ↓
         RRF 융합 (순위 기반)
              ↓
      Cross-Encoder 재정렬
              ↓
          Top-K 결과
```

## BM25 — sparse 쪽

> **BM25가 사는 곳은 [[Apache Lucene]]이다** — 역색인·토큰화·스코어링을 제공하는 라이브러리이고,
> Solr·Elasticsearch·OpenSearch가 그 위에 분산·API를 얹은 서버다. 이 페이지의 sparse 절반은
> 곧 Lucene 계열의 기능이다.

```
score(q, d) = Σ  IDF(t) ·        f(t,d) · (k₁ + 1)
             t∈q            ─────────────────────────────────
                            f(t,d) + k₁ · (1 − b + b · |d|/avgdl)
```

두 개의 장치가 전부다:

| 파라미터 | 장치 | 의미 |
|---|---|---|
| `k₁ ≈ 1.2~2.0` | **TF 포화** | 같은 단어가 반복될수록 **점수 증가율이 둔화**된다. 키워드 도배로 점수를 못 올린다 |
| `b ∈ [0,1]` | **길이 정규화** | 긴 문서가 단어를 많이 포함한다는 이유만으로 유리해지지 않도록 페널티 |

| ✅ 강점 | ❌ 한계 |
|---|---|
| 희귀 토큰·신조어 매칭 | **동의어 인식 불가** (`"휴대폰"` ≠ `"스마트폰"`) |
| 제품 코드 (`RTX-4090`, `ERR_502`) | **철자 오류에 취약** — 오타 시 점수 급감 |
| 고유명사 | 어순·문맥 무시 |

⭐ **Dense와 정확히 반대의 실패 모드다.** Dense는 오타·표기 변형에 강하고 식별자에 약하다.
**BM25는 "구식"이 아니라 상보재다** — [[Large language model]]의 NLP 발전사가 통계 기반을
과거형으로 그리는 것과 어긋나는 지점.

## RRF — 융합

```
RRF_score(d) = Σ      1
              m∈M  ─────────
                   k + r_m(d)
```

`k` = 보정 상수(원 논문 및 관례 **60**, 실무 권장 40~80) · `r_m(d)` = 검색기 m에서의 순위.

> ⭐⭐ **"스케일 정규화 불필요"가 존재 이유 전부다.**
> BM25 점수(위로 열린 실수)와 코사인 유사도(−1~1)는 **같은 자로 잴 수 없다.** 점수를 정규화해서
> 더하려면 분포 가정을 깔아야 하는데, **RRF는 점수를 버리고 순위만 써서 그 문제를 통째로 우회한다.**

성질: 파라미터 민감도가 낮고 노이즈에 강하다. 실무에서는 **상위 N개만 융합**해 비용을 줄인다.

**계산 예시** (k=60, 강의 표 — 직접 검산해 정확함을 확인했다):

| 문서 | BM25 순위 | Dense 순위 | RRF 점수 | 최종 |
|---|---|---|---|---|
| d1 | 1 | 3 | 0.0323 | **1** |
| d2 | 5 | 2 | 0.0315 | 2 |
| d3 | 2 | 7 | 0.0310 | 3 |

**한쪽에서만 1위인 문서보다 양쪽에서 고르게 상위인 문서가 이긴다.**

## Two-Stage Retrieval — 리랭킹

| | 목표 | 방법 | 규모 |
|---|---|---|---|
| **Stage 1** | **Recall** (놓치지 않기) | 하이브리드 검색 | Top-**200** |
| **Stage 2** | **Precision** (잘 세우기) | **Cross-Encoder** | Top-**20** |

> ⭐ **[[Caching strategies]]·[[Inference optimization]]과 같은 논리다** — 싸고 거친 필터를 앞에
> 두고, 비싼 정밀 연산은 살아남은 소수에만. **Part 4의 "GPU는 마지막 수단"과 같은 형태의 판단.**

### Bi-Encoder vs Cross-Encoder

| | **Bi-Encoder** | **Cross-Encoder** |
|---|---|---|
| 입력 | 쿼리·문서를 **독립** 인코딩 | `[CLS] Query [SEP] Doc [SEP]` **결합** |
| 속도 | 매우 빠름 (사전 계산된 벡터 비교) | **매우 느림** (쿼리마다 문서별 재계산) |
| 정확도 | 복잡한 의미 관계 포착 부족 | **미세한 논리·근거 일치 판단에 강함** |
| 단계 | 1단계 검색 | 2단계 리랭킹 |

> ⭐⭐ **차이의 뿌리는 "미리 계산할 수 있는가"다.**
> Bi-Encoder는 문서 벡터를 **인덱싱 시점에** 만들어 두므로 질의 시점 비용이 벡터 비교뿐이다.
> Cross-Encoder는 쿼리와 문서를 **함께** 넣어야 하므로 질의 시점에 **문서 수만큼 forward pass**가
> 필요하다. **정확도의 대가가 사전 계산 불가능성이다.**

**둘 다 encoder 계열 모델([[BERT]] 계보)이다.** RAG는 encoder(검색·리랭킹)와
decoder(생성, [[GPT]] 계보)를 함께 운영한다 → [[Model serving platforms]]의 대상이 하나가 아니다.

### ⚠️ 비용

**리랭킹은 RAG 지연·비용의 주요 원인이다.** Top-K가 20이면 질의마다 모델 추론 20회다.
강의는 *"배치/캐싱으로 P95 최소화"* 한 줄로 넘어가지만, 실제로는
[[Inference optimization]]의 dynamic batching·모델 크기 선택·[[GPU resource allocation]]이
그대로 걸리는 문제다.

## 무엇으로 측정하나

→ [[Retrieval evaluation metrics]]. 요약하면 **Stage 1은 Recall@K로, Stage 2는 NDCG@K로 잰다.**

## 관련 페이지

- [[Retrieval-augmented generation]] — 이 검색단이 들어가는 시스템, 그리고 시스템 수준의 한계
- [[Text embeddings]] · [[Vector database]] — dense 쪽 구성요소
- [[Retrieval evaluation metrics]] — 단계별 측정
- [[GraphRAG]] — **다른 축의 진화.** 이쪽은 *어떻게 검색을 제어하나*, 저쪽은 *무엇을 인덱싱하나*
- [[Inference optimization]] — 리랭킹 비용을 다루는 곳
- [[Caching strategies]] — 같은 형태의 2단계 판단

## 출처

- [[AI DE Course - Part5 Hybrid search and reranking]] (Fast Campus, Part 5) — **Part 5에서 가장 질이 높은 덱**
- 원 출처(강의는 인용하지 않는다, 1차 자료 후보): RRF — Cormack, Clarke & Büttcher,
  *Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods* (SIGIR 2009)

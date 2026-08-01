---
type: source
title: AI DE Course - Part5 Hybrid search and reranking
area: [data-engineering]
aliases: [Part5 하이브리드 검색, RAG의 진화, Hybrid Search와 Reranking, BM25, RRF, Two-Stage Retrieval, Agentic RAG]
tags: [data-engineering, course, fast-campus, rag, hybrid-search, bm25, rrf, reranking, cross-encoder, evaluation, agentic-rag]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/1. RAG의 진화 Hybrid Search와 Reranking 핵심 개념 요약.pdf (p2–9)"]
---

# AI DE Course - Part5 Hybrid search and reranking

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 5**(LLM·RAG) 셋째 덱
**"RAG 시스템의 진화: 하이브리드 검색과 리랭킹"**. 원본(로컬):
`raw/data-engineering/1. RAG의 진화 Hybrid Search와 Reranking 핵심 개념 요약.pdf` **p2–9** (9p 중).
PDF 작성일 2026-04-27. 강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐⭐ **Part 5의 세 덱 중 질이 확연히 다르다.** 앞의 두 덱이 출처 없는 배지로 채워진 개요라면,
> **이 덱은 BM25와 RRF의 수식을 파라미터 의미까지 제시하고 계산 예시를 붙인다.**
> **RRF 예시 수치를 검산했는데 전부 정확하다**(아래). 9페이지짜리 가장 짧은 덱인데
> **Part 5의 실질적 수확이 여기 다 있다.**

## 구성

`Naive RAG의 한계(Dense-only) · 하이브리드 검색 개요 · BM25 · RRF · Two-Stage Retrieval ·
Bi-Encoder vs Cross-Encoder · 검색 평가지표 · 3세대 RAG(Agentic·Adaptive)`

---

## ⭐ Dense-only가 놓치는 것 3종

**[[Retrieval-augmented generation]](Part 3 Ch4)의 한계 4종과 층위가 다르다.**
그쪽이 *시스템 수준*(검색 단위 불일치·retrieval–generation mismatch·Lost in the Middle·고정 top-k)
이라면, **이쪽은 retriever 내부 — 밀집 벡터 검색 자체의 실패 모드**다. **두 목록은 보완적이다.**

### 1. 어휘적 정밀도 부족

고유명사·제품코드·약어를 정확히 인식하지 못한다.

| 질의 | 문서 |
|---|---|
| `"GPT-4"` | `"GPT4"` (철자 변형) |
| `"AWS"` | `"Amazon Web Services"` (약어) |
| `"Python3.11"` | `"Python 3.11"` (버전 표기) |

### 2. 시맨틱 드리프트

**도메인 외 데이터에서 의미가 떠밀리는 현상.** 유사 의미 과적합 · 의도와 다른 문서 검색 ·
맥락 외 데이터 노이즈.

### 3. 정보 압축 병목

> **고정 벡터 차원의 정보 압축으로 세부 속성이 손실된다.** `768차원 → 정보 손실` ·
> **수치/스키마 정보 누락** · 세부 특징 압축.

⭐ **세 번째가 가장 중요하다.** 문서 하나를 768개 실수로 눌러 담으면 **어느 정보를 버릴지는 임베딩
모델이 정한다.** 버려지기 쉬운 것이 하필 정확히 맞아야 하는 값들(버전 번호·금액·에러 코드)이다.
**"의미는 남고 식별자는 사라진다"** — 이것이 BM25가 2026년에도 필요한 이유다.

**세 한계의 귀결:** 리콜 저하(정확한 문서 검색 실패) → 컨텍스트 품질 악화 → **환각 발생**(근거 없는
생성 증가).

## 하이브리드 검색 — Sparse + Dense

> **"정확한 키워드 매칭과 의미적 유사성을 동시에 활용."**

```
Query  "Python 3.11 API"
  ↓  (병렬 검색)
BM25 (Sparse) — 키워드 매칭 ┐
Dense (Vector) — 의미 검색  ┘
  ↓
RRF 융합 — 순위 기반 통합
  ↓
Cross-Encoder — 정밀 재정렬
```

| 축 | 담당 |
|---|---|
| **정확한 키워드 매칭** | BM25로 고유명사/코드/약어 인식 |
| **의미적 유사성** | Dense 임베딩으로 동의어/패러프레이즈 |
| **결합 전략** | RRF로 결과 융합 및 재정렬 |

## ⭐ BM25 (Sparse Retrieval)

```
score(q, d) = Σ  IDF(t) ·        f(t,d) · (k₁ + 1)
             t∈q            ─────────────────────────────────
                            f(t,d) + k₁ · (1 − b + b · |d|/avgdl)
```

| 기호 | 의미 |
|---|---|
| `f(t,d)` | 문서 내 용어 빈도 (Term Frequency) |
| `\|d\|`, `avgdl` | 현재 문서 길이 / 평균 문서 길이 |
| `k₁ ≈ 1.2 ~ 2.0` | **TF 포화도를 조절하는 상수** |
| `b ∈ [0, 1]` | **길이 정규화 영향 조절 상수** |

### 두 장치의 의미

**1. 단어 빈도 포화 (TF Saturation)**

> **"단순 TF는 단어 출현 횟수에 비례하여 점수가 무한히 증가한다. BM25는 k₁ 파라미터를 통해 특정
> 단어가 흔하게 반복되더라도 점수 증가율이 점차 둔화(Saturation)되도록 설계되어 노이즈를 방지한다."**

**2. 문서 길이 정규화 (Length Normalization)**

> **"긴 문서는 짧은 문서보다 자연스럽게 더 많은 단어를 포함한다. b 파라미터는 평균 길이 대비 현재
> 문서의 길이를 계산하여, 불필요하게 긴 문서에 페널티를 부여함으로써 검색의 공정성을 확보한다."**

### 강점과 한계

| ✅ 어휘적 정밀도 | ❌ 시맨틱 이해 부재 |
|---|---|
| **희귀 토큰 매칭** — 사전에 없는 특수 용어·신조어에 매우 강력 | **동의어 인식 불가** — `"휴대폰"`과 `"스마트폰"`을 다른 문서로 간주 |
| **정확한 코드 식별** — `"RTX-4090"`, `"ERR_502"` 매칭 우수 | **철자 오류 취약** — 오타 시 점수가 급감해 리콜 저하 |
| **고유명사 탐지** — 사용자 이름·회사명 | |

> **"→ 결론: Dense Retrieval과 결합한 하이브리드 전략 필수."**

⭐ **Dense와 Sparse의 실패 모드가 정확히 반대다.** Dense는 오타·표기 변형에 강하고 식별자에 약하다.
BM25는 그 반대다. **둘을 합치는 이유는 성능을 더하기 위해서가 아니라 서로의 실패를 덮기 위해서다.**

## ⭐ RRF (Reciprocal Rank Fusion)

**이기종 점수 체계를 순위 기반으로 융합한다.**

```
RRF_score(d) = Σ      1
              m∈M  ─────────
                   k + r_m(d)
```

`k` = 보정 상수(**일반적으로 60**) · `r_m(d)` = m번째 검색기에서 문서 d의 순위 · `M` = 검색기 집합.

| 순위 기반 통합의 장점 | 실무 적용 시 주의사항 |
|---|---|
| ⭐ **스케일 정규화 불필요 (순위만 사용)** | k값은 **40~80 범위** 권장 |
| 파라미터 민감도 낮음 | 상위 N개 문서만 융합하여 효율성 확보 |
| 노이즈에 강인한 융합 | 결과 재정렬 시 RRF 점수 기준 적용 |

> ⭐⭐ **"스케일 정규화 불필요"가 RRF의 존재 이유 전부다.** BM25 점수(무한대까지 열린 실수)와
> 코사인 유사도(−1~1)는 **애초에 같은 자로 잴 수 없다.** 점수를 정규화해 더하려는 시도는 분포
> 가정을 깔게 되는데, **RRF는 점수를 버리고 순위만 쓰는 것으로 그 문제를 통째로 우회한다.**

### 계산 예시 (k = 60) — ✅ 검산 완료

| 문서 | BM25 순위 | Dense 순위 | BM25 기여 | Dense 기여 | RRF 점수 | 최종 순위 |
|---|---|---|---|---|---|---|
| **d1** | 1 | 3 | 0.0164 | 0.0159 | **0.0323** | **1** |
| **d2** | 5 | 2 | 0.0154 | 0.0161 | **0.0315** | **2** |
| **d3** | 2 | 7 | 0.0161 | 0.0149 | **0.0310** | **3** |

**직접 계산해 확인했다:** `1/(60+1) = 0.01639` · `1/(60+3) = 0.01587` → 합 `0.03226` ✅ ·
`1/65 = 0.01538`, `1/62 = 0.01613` → `0.03151` ✅ · `1/62 + 1/67 = 0.01613 + 0.01493 = 0.03105` ✅.
**세 행 모두 표기값과 일치한다. 이 코스에서 수치를 검산해 맞은 첫 사례다.**

⭐ **예시 자체가 잘 골라져 있다.** d1은 BM25 1위 / Dense 3위, d2는 BM25 5위 / Dense 2위 —
**어느 한쪽에서만 1위인 문서보다 양쪽에서 고르게 상위인 문서가 이긴다는 성질**을 보여준다.

## ⭐ Two-Stage Retrieval

> **"1단계에서 빠른 후보 생성, 2단계에서 정밀 재정렬."** 속도(Recall)와 정확도(Precision)를 모두
> 잡기 위한 **실무 표준 워크플로우**.

| | 단계 | 방법 | 규모 | 목표 |
|---|---|---|---|---|
| **Stage 1** | Recall (속도) | Hybrid Search (BM25 + Dense) | **Top-200** | 빠른 후보 생성 |
| **Stage 2** | Precision (정확도) | **Cross-Encoder** 정밀 재정렬 | **Top-20** | 최종 결과 |

지연 최적화: **배치/캐싱으로 P95 최소화** · 쿼리 캐싱.

⚠️ 붙어 있는 수치(`95% Recall@200` · `0.92 NDCG@20` · `45ms Latency`)는 **출처 없는 예시값**이다.
반면 **200 → 20이라는 규모 감소의 자릿수는 실무 관행과 일치한다.**

> ⭐ **이 2단계 구조가 [[Caching strategies]]·[[Inference optimization]]과 같은 논리다** —
> 싸고 거친 필터를 앞에 두고, 비싼 정밀 연산을 살아남은 소수에만 적용한다.
> **Part 4의 "GPU는 마지막 수단"과 정확히 같은 형태의 판단이다.**

## ⭐ Bi-Encoder vs Cross-Encoder

| | **Bi-Encoder** (1단계 검색용) | **Cross-Encoder** (2단계 리랭킹용) |
|---|---|---|
| **입력 구조** | **독립적 인코딩** (Query Vector ↔ Doc Vector) | **결합 인코딩** (`[CLS] Query [SEP] Doc [SEP]`) |
| **시간 복잡도** | 매우 빠름 (미리 계산된 벡터 간 코사인 유사도) | **매우 느림** (쿼리마다 N개 문서 전체 재계산) |
| **강점·한계** | 대규모 확장에 유리하나, 복잡한 의미 관계 포착 부족 | 높은 정확도, **대규모 인덱스 탐색 불가** |
| **적합 단계** | 1단계 검색 (Top-N 추출) | 2단계 리랭킹 (Top-K 정제) |

> **Bi-Encoder** — 쿼리와 문서를 **독립적으로** 임베딩해 코사인 유사도로 매칭. 대규모 인덱스에서
> **사전 계산된** 벡터 검색에 최적화. 거친 필터링(Coarse Filter)에 적합.
> **Cross-Encoder** — `[CLS]` 토큰을 활용해 쿼리+문서를 결합하여 **Full Self-Attention** 수행.
> 미세한 논리·근거 일치 판단에 매우 강력. **소수의 후보(Top-K)에만 적용하는 것이 실무 표준.**

⭐⭐ **차이의 뿌리는 "미리 계산할 수 있는가"다.** Bi-Encoder는 문서 벡터를 **인덱싱 시점에** 만들어
두므로 질의 시점 비용이 벡터 비교뿐이다. Cross-Encoder는 쿼리와 문서를 **같이** 넣어야 하므로
**질의 시점에 문서 수만큼 forward pass**가 필요하다. **정확도의 대가가 사전 계산 불가능성이다.**

**이 구분이 [[AI DE Course - Part5 LLM foundations and NLP history|덱 1의 BERT vs GPT]]와 이어진다** —
둘 다 encoder 계열이며, RAG 시스템은 **encoder(검색·리랭킹) + decoder(생성)를 함께 쓴다.**

## 검색 평가지표

| 지표 | 정의 | 실무 활용 |
|---|---|---|
| **Recall@K** | K개 결과 내 관련 문서 비율 | **초기 검색 품질 평가** |
| **MRR** | 첫 정답의 역순위 평균 | 정답 도달 속도 측정 |
| **NDCG@K** | 순위 품질을 고려한 정밀도 | **최종 검색 품질 평가** |

> **"Recall@K는 초기 검색, NDCG@K는 최종 품질 평가에 사용."**

⭐ **이 한 줄이 Two-Stage 구조와 정확히 대응한다** — Stage 1은 후보를 놓치지 않는 것이 목표이므로
Recall로 재고, Stage 2는 순서를 잘 세우는 것이 목표이므로 NDCG로 잰다. **단계마다 다른 지표를 쓴다.**

> **[[Data SLA and observability]]와의 연결:** Part 4가 `offline-online skew`를 SLI로 승격시켰듯,
> **RAG 시스템에서는 Recall@K와 NDCG@K가 SLI 후보다.** 강의는 여기까지 가지 않는다.

## 3세대 RAG — Agentic · Adaptive

> **"자율적 계획, 실행, 평가, 반복을 통한 지능형 검색."**

```
Query Analysis  →  Strategy Selection  →  Dynamic Adjustment
의도 분석            검색기 선택              동적 조정
```

- **자율적 계획** — 쿼리 분석 및 검색 전략 수립
- **동적 실행** — 다중 검색기 병렬 실행
- **결과 평가** — 관련성 및 정확성 검증
- **반복 개선** — **실패 시 재검색**

키워드: `Tool Orchestration` · `Multi-Agent` · `Self-Correction`.

⭐ **이것이 [[Retrieval-augmented generation]]의 한계 4번(고정 top-k)에 대한 직접적 대응이다.**
그 페이지는 *"모든 질문이 같은 retrieval budget을 가져야 하는 것은 아니다 — retrieval should be
adaptive"*로 끝났는데, **이 슬라이드가 그 "adaptive"의 이름과 구성요소를 준다.**

⚠️ **다만 세대 구분이 Part 3와 어긋난다.** Part 3 Ch4는 `Naive RAG → Advanced RAG → 구조화된
RAG(GraphRAG)`로 진화를 그렸고, 이 덱은 `Naive → (하이브리드·리랭킹) → 3세대 Agentic·Adaptive`로
그린다. **GraphRAG가 이 계보에 없고, Agentic RAG가 저쪽 계보에 없다.** 두 축은 사실 직교한다 —
*무엇을 인덱싱하나*(청크 vs 그래프)와 *어떻게 검색을 제어하나*(고정 vs 적응). **강의는 서로를
참조하지 않는다.**

## ⚠️ 이 덱의 문제

**앞의 두 덱과 비교하면 문제가 적다.** 남은 것:

| 문제 | 내용 |
|---|---|
| **출처 없는 예시 수치** | `95% Recall@10` · `0.85 MRR` · `0.92 NDCG@10` · `45ms Latency` · `95% Recall@200`. **개념 설명은 수식으로 뒷받침되는데 성능 숫자만 근거가 없다.** 예시값으로 읽으면 무해하지만 명시가 없다 |
| **출처 표기 없음** | BM25(Robertson & Walker 계열)도 **RRF(Cormack, Clarke & Büttcher, SIGIR 2009)**도 인용이 없다. 수식을 정확히 쓰면서 원 출처를 안 밝힌다 |
| **`k값 40~80 권장`의 근거 없음** | 원 논문의 k=60은 밝히면서(*"일반적으로 60"*) 권장 범위의 출처는 없다 |
| **평가지표에 수식이 없다** | BM25·RRF는 수식을 주면서 NDCG는 정의 한 줄뿐이다. **DCG·IDCG·할인 계수가 없어 "순위 품질을 고려"가 어떻게 계산되는지 알 수 없다** |
| **비용 이야기가 없다** | Cross-Encoder 리랭킹은 **Top-K만큼 모델 추론을 돌린다** — GPU 비용과 P95 지연의 주 원인인데, "배치/캐싱으로 최소화" 한 줄이 전부다. [[Inference optimization]]과 이어야 할 지점 |
| **GraphRAG와의 관계 없음** | 위 참고 |

## 링크

- 개념: [[Hybrid search and reranking]] · [[Retrieval evaluation metrics]]
- 보완 관계: [[Retrieval-augmented generation]] — 시스템 수준 한계 4종 ↔ 여기의 retriever 내부 한계 3종
- 다른 축의 진화: [[GraphRAG]]
- 앞 단계: [[AI DE Course - Part5 Embeddings and vector search]] · [[Vector database]]
- 같은 형태의 판단: [[Caching strategies]] · [[Inference optimization]] (싼 필터 먼저, 비싼 연산은 소수에)
- 측정: [[Data SLA and observability]]
- 코스: [[AI Data Engineering (Fast Campus course)]]

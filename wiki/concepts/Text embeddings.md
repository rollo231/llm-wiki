---
type: concept
title: Text embeddings
area: [data-engineering]
aliases: [임베딩, Embedding, 텍스트 임베딩, 벡터 임베딩, 임베딩 모델, Word2Vec, GloVe, FastText, CLIP]
tags: [embedding, vector-search, nlp, semantic-search, multimodal, data-engineering]
created: 2026-08-01
updated: 2026-09-03
sources: ["[[AI DE Course - Part5 Embeddings and vector search]]", "[[AI DE Course - Part5 Transformer internals]]", "[[AI DE Course - Ch3-5,6 Unstructured data ingestion]]"]
---

# Text embeddings

**텍스트를 의미가 보존되는 숫자 벡터로 바꾸는 것. 비슷한 뜻이면 벡터 공간에서 가깝게 놓이도록
학습된다.**

```
"강아지" = [0.8, 0.6, 0.3]      "고양이" = [0.7, 0.5, ...]

강아지 ↔ 고양이   유사도 0.85
강아지 ↔ 자동차   유사도 0.15
```

**글자가 같은지가 아니라 뜻이 가까운지로 검색할 수 있게 만드는 것** — 의미 기반 검색의 전제이며
[[Retrieval-augmented generation|RAG]] 파이프라인의 3단계다.

## ⚠️ 먼저 — 같은 단어의 두 층위

강의는 "임베딩"을 두 덱에서 다른 뜻으로 쓴다. **구분해야 한다.**

| | **Embedding Layer** (모델 내부) | **Embedding Model** (파이프라인 부품) |
|---|---|---|
| 입력 | 토큰 ID 하나 | 문장·문서 전체 |
| 출력 | 그 토큰의 벡터 | **하나의 대표 벡터** |
| 쓰임 | [[Transformer architecture]]의 첫 층 | 벡터 DB에 넣을 값 |
| 예 | GPT 내부의 임베딩 행렬 | SBERT, OpenAI embedding API |

**이 페이지는 주로 후자를 다룬다.** RAG에서 "임베딩한다"고 할 때의 그것이다.

## ⭐ 알고리즘 계보 — 축은 "맥락 반영" 하나

| 알고리즘 | 맥락 | 특징 |
|---|---|---|
| **Word2Vec** | **정적** | 주변 단어 예측. 빠르고 가벼움 |
| **GloVe** | **정적** | 전역 동시 등장 통계. 아날로지에 강함 |
| **FastText** | **정적** | **서브워드 단위** → 희귀어·신조어에 강함 |
| **BERT** | **문맥** | 트랜스포머 양방향. **동적 임베딩** |
| **SBERT** | **문맥** | **문장 임베딩 특화.** 의미 유사도에 강함 |
| **CLIP** | **멀티모달** | 이미지-텍스트 공동 임베딩 |

### 정적 vs 문맥의 실제 차이

**정적 벡터는 `"배"`가 어느 문장에 있든 같은 벡터를 준다.** 과일인지 선박인지 신체인지 구분하지
못한다. 문맥 반영 모델은 문장마다 다른 벡터를 준다.

> **RAG의 문서 임베딩에 SBERT 계열이 쓰이는 이유:** 순수 BERT는 토큰별 벡터를 주기 때문에
> **문장 하나를 대표하는 벡터**를 얻으려면 별도 학습이 필요하다. SBERT가 그 학습을 한 판본이고,
> [[Hybrid search and reranking]]의 **Bi-Encoder가 정확히 이 구조**다.

⚠️ **강의의 알고리즘 비교표에는 "성능 %" 열이 있지만 버려야 한다** — 벤치마크가 명시되지 않았고,
CLIP(이미지-텍스트 검색)과 Word2Vec(단어 임베딩)처럼 **같은 과제를 풀지 않는 모델을 단일 숫자로
서열화**한다. 나머지 열은 정확하다.

## 벡터의 성질

- **차원** — 특징의 수. 흔히 **384, 768**. 크면 표현력이 늘지만 저장·검색 비용도 는다
- **유사도** — 코사인 유사도(방향) 또는 유클리드 거리
- **의미 공간** — `왕 : 여왕 = 남자 : 여자` 같은 관계가 벡터 연산으로 나타난다

## ⚠️ 임베딩이 버리는 것

[[Hybrid search and reranking]]이 지적하는 **정보 압축 병목**이 이 페이지의 가장 중요한 경고다.

> **문서 하나를 768개 실수로 눌러 담으면, 무엇을 버릴지는 임베딩 모델이 정한다.**
> 버려지기 쉬운 것이 하필 **정확히 맞아야 하는 값들** — 버전 번호, 제품 코드, 에러 코드, 금액.
>
> ⭐ **"의미는 남고 식별자는 사라진다."**

그래서 `"GPT-4"`와 `"GPT4"`, `"Python3.11"`과 `"Python 3.11"`이 어긋나고, **키워드 검색(BM25)을
함께 돌려야 한다.** 임베딩은 만능이 아니라 **한쪽 실패 모드를 가진 도구**다.

## 운영에서 결정할 것

강의가 다루지 않지만 실무에서 먼저 부딪히는 것들:

| 결정 | 왜 |
|---|---|
| **모델 선택** | 한국어 성능이 크게 갈린다 → [[Tokenization]] |
| **차원** | 저장·메모리·검색 지연에 직접 영향 → [[Vector database]] |
| **정규화** | 코사인 유사도를 쓸 거면 벡터를 정규화해 두는 편이 낫다 |
| ⚠️ **모델 교체** | **임베딩 모델을 바꾸면 인덱스 전체를 다시 만들어야 한다.** 질의 벡터와 문서 벡터가 같은 공간에 있어야 하기 때문 — 무중단 교체는 별도 설계가 필요하다 |
| **버전 관리** | 어떤 모델·버전으로 만든 인덱스인지 기록 → [[Data and model versioning]] |

**모델 교체 항목이 [[Data drift and training-serving skew]]와 같은 종류의 문제다** —
학습(인덱싱)과 서빙(질의)이 다른 함수를 쓰면 조용히 망가진다.

## 관련 페이지

- [[Vector database]] — 만든 벡터를 담고 찾는 곳
- [[Hybrid search and reranking]] — 임베딩만으로 안 되는 지점과 그 보완
- [[Unstructured data ingestion]] — 임베딩 앞단(OCR·정제·PII)
- [[Retrieval-augmented generation]] — 이 벡터가 쓰이는 시스템
- [[Transformer architecture]] · [[BERT]] — 문맥 임베딩을 만드는 구조
- [[Data semantics]] — 의미를 다루는 다른 접근(정의·온톨로지). **임베딩은 의미를 통계로, 시멘틱은
  의미를 명시적 구조로 다룬다**

## 출처

- [[AI DE Course - Part5 Embeddings and vector search]] (Fast Campus, Part 5) — 알고리즘 비교표
- [[AI DE Course - Part5 Transformer internals]] — 모델 내부 임베딩 레이어
- [[AI DE Course - Ch3-5,6 Unstructured data ingestion]] (Part 1) — 한국어 모델 선정 경고

---
type: concept
title: Tokenization
area: [data-engineering, programming]
aliases: [토큰화, 토큰, Token, BPE, Byte Pair Encoding, 서브워드]
tags: [tokenization, bpe, llm, nlp, korean, cost, data-engineering, programming]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part5 Transformer internals]]"]
---

# Tokenization

**텍스트를 모델이 다루는 단위(토큰)로 쪼개는 전처리 단계.**
그리고 **토큰은 곧 비용의 단위이자 컨텍스트 한도의 단위다** — DE가 이 페이지를 봐야 하는 이유.

```
원문    "안녕하세요. 오늘 날씨 어때요?"
토큰화  ["안녕하세요", ".", "오늘", "날씨", "어때요", "?"]
BPE     ["안녕", "하세요", ".", "오", "늘", "날씨", "어때", "요", "?"]
```

## BPE (Byte Pair Encoding)

- 자주 등장하는 글자 쌍을 하나의 새 단위로 **병합**해 어휘를 만든다
- **자주 쓰이는 어휘는 한 토큰으로, 드문 단어는 여러 토큰으로** 표현된다
- 결과적으로 어휘 크기를 고정하면서 **미등록 단어(OOV)를 없앤다** — 어떤 문자열도 쪼개면 표현된다

> 단어 단위 토큰화는 신조어·오타에서 무너지고, 문자 단위는 시퀀스가 너무 길어진다.
> **서브워드는 그 사이의 타협이다.**

## ⭐ 한국어의 문제

> `"자동차가"` → `"자동차"` + `"가"` **(조사 분리)**
>
> **"한국어는 영어보다 조사나 어미 변형이 많기 때문에, 이를 적절히 분리해 주는 것이 모델 학습에
> 중요하다."** — 강의

**같은 뜻의 문장이라도 한국어는 영어보다 토큰 수가 많아지기 쉽다.** 어간에 조사·어미가 붙어
형태가 계속 바뀌는데, 토크나이저가 그 경계를 잘 못 잡으면 한 단어가 여러 조각으로 흩어진다.

그 결과 셋:

| | |
|---|---|
| **비용** | 토큰 단가 과금이므로 **같은 문서가 더 비싸진다** → [[LLMOps]] |
| **컨텍스트** | 같은 윈도우에 **더 적은 내용**이 들어간다 → [[Context engineering]] |
| **검색 품질** | 임베딩·BM25 모두 토큰 경계 위에서 동작한다 → [[Text embeddings]] · [[Hybrid search and reranking]] |

**[[Unstructured data ingestion]]의 *"한국어에 최적화된 임베딩 모델 선정이 필수"*가 결국 이 문제의
아랫단이다.** 모델 선택 이전에 토크나이저 선택이 있다.

## 파이프라인에서 토큰이 등장하는 지점

```
문서 → 정제 → [청킹]  →  [임베딩]  →  벡터 DB
                ↑           ↑
           토큰 수로 자른다   토큰 경계로 인코딩
                                        ↓
                        검색 → [프롬프트 조립] → [생성]
                                    ↑             ↑
                              토큰 예산 배분    출력 토큰당 과금·지연
```

**청킹 단위를 "글자 수"가 아니라 "토큰 수"로 잡아야 하는 이유**가 여기 있다 — 임베딩 모델과 LLM의
입력 한도가 토큰 단위이기 때문이다. 강의는 청킹을 *"의미 단위로 청킹, 오버랩 설정"* 두 줄로만
다루고 이 연결을 하지 않는다.

## 강의가 다루지 않은 것

- **토크나이저 종류** — BPE 외에 WordPiece·SentencePiece·Unigram
- **어휘 크기 트레이드오프** — 크면 시퀀스가 짧아지지만 임베딩 행렬이 커진다
- **특수 토큰** — `[CLS]`·`[SEP]`·EOS. `[CLS]`는 [[Hybrid search and reranking]]의 Cross-Encoder
  설명에 갑자기 등장하는데 정의가 어디에도 없다
- **토큰 수 측정** — 실무에서 비용 추정의 첫 단계

## 관련 페이지

- [[Transformer architecture]] — 토큰이 들어가는 곳
- [[Large language model]] — 토큰 하나씩 생성하는 자가회귀
- [[Text embeddings]] — 토큰 → 벡터
- [[LLMOps]] — 토큰 단가와 비용 관리
- [[Context engineering]] — 토큰 예산 배분

## 출처

- [[AI DE Course - Part5 Transformer internals]] (Fast Campus, Part 5)

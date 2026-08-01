---
type: concept
title: Transformer architecture
area: [data-engineering, programming]
aliases: [Transformer, 트랜스포머, Self-Attention, Multi-Head Attention, Attention, Positional Encoding, FFN]
tags: [transformer, attention, llm, nlp, deep-learning, data-engineering, programming]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part5 Transformer internals]]", "[[AI DE Course - Part5 LLM foundations and NLP history]]"]
---

# Transformer architecture

**모든 토큰이 다른 모든 토큰과의 관련성을 한 번에 계산하는 구조. 순차 처리를 버려서 병렬성을 얻고,
잃어버린 순서를 위치 인코딩으로 되사 왔다.**

> ⭐ **한 줄 요약: 속도를 얻고 순서를 잃은 뒤 다시 사 온 구조.**
> RNN은 순서대로 읽어서 순서를 알지만 병렬화가 안 됐고, Transformer는 전부 동시에 보므로 병렬화되지만
> 순서를 따로 주입해야 한다.

## Self-Attention

각 토큰이 문장 내 다른 모든 토큰과의 관련성을 계산해 문맥에 맞는 표현을 만든다. 세 벡터를 쓴다:

| Query | Key | Value |
|---|---|---|
| 현재 토큰 | 비교 대상 | 실제 값 |

```
Attention(Q, K, V) = softmax(Q·Kᵀ / √d_k) · V
```

1. **Q·Kᵀ** — 유사도 계산
2. **/ √d_k** — 스케일링(안정화)
3. **softmax** — 확률 분포로 변환
4. **· V** — Value에 가중치 적용

### Multi-Head

여러 개의 독립적인 Attention을 **병렬로** 수행한다.

> **"하나의 Attention만으로는 문장 내 복합 관계(의존/동의어/참조)를 포착하기 어렵다."**
> 문법 관계, 의미 관계, 대용어 참조를 서로 다른 head가 나눠 본다.

## 블록 구조

```
[입력 임베딩 + Positional Encoding]
            ↓
    Multi-Head Attention      ← 문맥적 중요도 계산
            ↓
    Residual + LayerNorm
            ↓
        FFN (비선형 변환)
            ↓
    Residual + LayerNorm
            ↓
        (블록 반복)
```

| 요소 | 역할 |
|---|---|
| **FFN** | 각 토큰에 **독립적으로** 적용되는 비선형 변환 (선형 → 활성화 → 선형) |
| **Residual Connection** | 입력을 출력에 직접 더함 → **기울기 소실 완화, 정보 보존, 학습 안정성** |
| **LayerNorm** | 각 층의 출력 분포를 안정화 |

## Positional Encoding

**어텐션 자체는 순서를 모른다.** 위치 정보를 별도로 주입해야 한다.

- **방식** — 사인/코사인 함수로 위치를 벡터로 변환해 임베딩에 더한다
- **효과** — 상대적 거리를 인식

⚠️ **강의는 사인/코사인만 다룬다.** 현행 LLM이 널리 쓰는 RoPE·ALiBi 계열은 나오지 않는다.
긴 컨텍스트 확장과 직결되는 주제라 **여기가 이 위키의 공백이다.**

## 인코더와 디코더

| | 역할 | 대표 |
|---|---|---|
| **Encoder** | 문맥 인코딩 — 입력 전체를 양방향으로 읽어 **표현**을 만든다 | [[BERT]] |
| **Decoder** | 텍스트 생성 — 왼쪽만 보며 다음 토큰을 예측 | [[GPT]] |

**RAG 시스템은 둘 다 쓴다** — encoder로 검색·리랭킹하고 decoder로 답변을 만든다.
→ [[Hybrid search and reranking]]의 Bi-Encoder / Cross-Encoder

## ⭐ DE가 알아야 할 세 가지 귀결

### 1. 병렬성 — GPU와 궁합이 맞는 이유

RNN과 달리 시퀀스 전체를 동시에 계산할 수 있어 **GPU의 수천 개 코어를 채울 수 있다**.
[[GPU architecture]]의 SIMT 모델과 맞는 구조이고, H100의 **Transformer Engine**이 겨냥하는
연산이 바로 이것이다.

### 2. 비용 — 시퀀스 길이에 제곱

모든 토큰 쌍의 관련성을 계산하므로 **연산량·메모리가 시퀀스 길이의 제곱으로 늘어난다.**

> **"긴 입력이 가능하다고 했지, 성능이 더 좋다고 한 적은 없다."**
> ([[Retrieval-augmented generation]]의 *Lost in the Middle* 절)

**컨텍스트를 늘리는 것이 왜 비용 결정인지의 근거**가 여기 있다 → [[Context engineering]].

### 3. 자가회귀 — 생성은 병렬화되지 않는다

구조는 병렬적이지만 **생성은 한 토큰씩** 진행된다. 학습·프리필은 병렬, 디코딩은 순차.
[[Inference optimization]]과 [[Batch and online serving]]의 물리적 전제.

## 강의가 다루지 않은 것

| 빠진 것 | 왜 중요한가 |
|---|---|
| **원논문 인용** | *Attention Is All You Need*(Vaswani et al., 2017). 수식을 쓰면서 출처가 없다 |
| **차원 설명** | `d_k`가 무엇인지, Q/K/V가 학습되는 선형 사영이라는 것, head 수와 차원의 관계 |
| **제곱 복잡도** | 위 2번. 코스 전체에서 [[Retrieval-augmented generation]]에만 한 줄 있다 |
| **현대적 변형** | GeLU/SwiGLU, RMSNorm, RoPE/ALiBi, KV 캐시, FlashAttention, MoE |
| **KV 캐시** | 자가회귀 생성의 메모리 사용을 지배하는 요소. 서빙 비용의 핵심인데 코스에 없다 |

**1차 자료 인제스트 후보:** *Attention Is All You Need* (2017).

## 관련 페이지

- [[Large language model]] — 이 구조 위에 세워진 것
- [[Tokenization]] · [[Text embeddings]] — 이 구조에 들어가기 전의 두 변환
- [[GPU architecture]] — 병렬성이 실제로 쓰이는 곳
- [[Inference optimization]] · [[Batch and online serving]] — 자가회귀 생성의 운영 결과
- [[GPT]] · [[BERT]] — decoder 계열과 encoder 계열

## 출처

- [[AI DE Course - Part5 Transformer internals]] (Fast Campus, Part 5)
- [[AI DE Course - Part5 LLM foundations and NLP history]] — 개요 슬라이드

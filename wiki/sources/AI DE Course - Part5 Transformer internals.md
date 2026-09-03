---
type: source
title: AI DE Course - Part5 Transformer internals
area: [data-engineering, programming]
aliases: [Part5 Transformer 내부, 토큰화와 BPE, Multi-Head Self-Attention 심화, FFN과 Residual]
tags: [data-engineering, programming, course, fast-campus, transformer, attention, tokenization, bpe, embedding]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part5/01. LLM에 대한 기본 이해.pdf (p11–16)"]
---

# AI DE Course - Part5 Transformer internals

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 5**(LLM·RAG) 첫 덱
**"LLM에 대한 기본 이해"의 후반부**. 원본(로컬): `raw/data-engineering/ai-de-course/part5/01. LLM에 대한 기본 이해.pdf`
**p11–16** (16p 중). PDF 작성일 2026-04-21. 강의 홈: [[AI Data Engineering (Fast Campus course)]].

전반부는 [[AI DE Course - Part5 LLM foundations and NLP history]]. 앞이 *"어떻게 여기까지 왔나"*
라면 여기는 **"입력 한 줄이 실제로 어떤 변환을 거치나"**다.

> ⭐ **이 덱은 코스 전체에서 유일하게 모델 내부를 연다.** 나머지 파트는 모델을 블랙박스로 두고
> 그 주변(데이터·서빙·자원)을 다뤘다. **DE에게 중요한 것은 여기서 나오는 세 단어다 —
> 토큰 · 임베딩 · 컨텍스트 길이. 셋 다 파이프라인 비용의 단위이기 때문이다.**

## 구성

`토큰화와 BPE · Embedding Layer · Multi-Head Self-Attention 심화 · FFN과 Residual 연결 ·
Positional Encoding · 모델 실제 동작 과정`

---

## 1. 토큰화와 BPE

**토큰화는 텍스트를 작은 단위(토큰)로 나누는 과정.** 컴퓨터가 텍스트를 분석 가능한 단위로 인식하게
하는 필수 전처리 단계다.

```
원문    "안녕하세요. 오늘 날씨 어때요?"
토큰화  ["안녕하세요", ".", "오늘", "날씨", "어때요", "?"]
BPE     ["안녕", "하세요", ".", "오", "늘", "날씨", "어때", "요", "?"]
```

**BPE(Byte Pair Encoding)의 원리:**

- 자주 등장하는 글자 쌍을 하나의 새로운 문자로 치환
- 텍스트를 점점 더 적은 단위로 쪼개 나가는 방식
- **자주 쓰이는 어휘는 한 토큰으로, 드물게 등장하는 단어는 여러 토큰으로**

### ⭐ 한국어 BPE

> `"자동차가"` → `"자동차"` + `"가"` **(조사 분리)**
>
> **"한국어는 영어보다 조사나 어미 변형이 많기 때문에, 이를 적절히 분리해 주는 것이 모델 학습에
> 중요함."**

**이 한 줄이 이 덱에서 실무로 직결되는 가장 중요한 문장이다.** 같은 문장이라도 한국어는 영어보다
토큰 수가 많아지고, 토큰 수는 곧 **비용([[LLMOps]]의 토큰 단가)이자 컨텍스트 한도**다.
[[Unstructured data ingestion]]이 *"한국어에 최적화된 임베딩 모델 선정이 필수"*라고 한 것과
같은 문제의 앞단이다.

## 2. Embedding Layer

**토큰 ID를 고차원 벡터(수백~수천 차원)로 매핑한다.**

```
[1, 45, 23, 89]  →  벡터 변환  →  [0.2, 0.5, -0.3, ...]
```

목표: **비슷한 의미를 가진 단어들은 벡터 공간에서 가깝게, 다른 단어들은 멀리** 위치하도록 학습.

```
"왕"   [0.2, 0.5, -0.3]      "여왕"  [0.3, 0.6, -0.2]
"남자" [0.1, 0.4, -0.1]      "여자"  [0.2, 0.6, -0.2]
```

유사도는 **코사인 유사도**로 계산.

> ⚠️ **주의 — 여기의 "임베딩"은 모델 내부의 임베딩 레이어**다.
> [[AI DE Course - Part5 Embeddings and vector search|덱 2의 임베딩]]은 **문장/문서 전체를 하나의
> 벡터로 만드는 임베딩 모델**을 말한다. **두 덱이 같은 단어를 다른 층위로 쓴다** — 강의는 이를
> 구분하지 않는다. → [[Text embeddings]]에서 정리했다.

## 3. Multi-Head Self-Attention

**각 단어가 다른 모든 단어와의 관련성을 계산해 문맥에 맞게 표현한다.** 이를 위해 세 벡터를 쓴다:

| Query | Key | Value |
|---|---|---|
| 현재 단어 | 비교 대상 | 실제 값 |

```
Score = softmax(Q·Kᵀ / √d_k) · V
```

계산 4단계:

1. **Query-Key Dot Product** — Q와 K의 유사도 계산
2. **Scaling** — `√d_k`로 나누어 안정화
3. **Softmax** — 확률 분포로 변환
4. **Value Weighting** — V에 가중치 적용

### 왜 Multi-Head인가

> **"하나의 Attention만으로는 문장 내 복합 관계(의존/동의어/참조)를 포착하기 어렵습니다.
> 여러 Head를 통해 다양한 관점에서 문맥을 분석합니다."**

여러 개의 독립적인 Attention을 **병렬로** 수행해 문법·의미·대용어 등 다양한 관계를 동시에 포착한다.

## 4. FFN과 Residual 연결

| | |
|---|---|
| **FFN (Feed Forward Network)** | 각 토큰에 **독립적으로** 적용되는 비선형 변환. 2개의 선형 변환 + ReLU |
| **Residual Connection** | 입력을 출력에 직접 더해 **기울기 소실 완화·정보 보존** |

Transformer 블록 구조:

```
문맥적 중요도 계산 (Attention)
        ↓
Residual + LayerNorm
        ↓
비선형 변환 (FFN)
        ↓
Residual + LayerNorm
```

핵심 특징: 기울기 소실 완화 · 정보 보존 · **학습 안정성 향상**.

## 5. Positional Encoding

> **"Transformer는 어텐션 메커니즘을 사용하여 단어들 간의 관계를 계산하지만, 순서 정보를 가지고
> 있지 않기 때문에 위치 정보를 별도로 인코딩해야 합니다."**

- **필요성** — 어텐션 자체는 순서를 모른다
- **방식** — 사인/코사인 함수로 위치 정보를 벡터로 변환
- **효과** — 상대적 거리를 인식하여 문맥 이해 개선

> ⭐ **"순서를 모른다"가 Transformer의 병렬성과 같은 동전의 양면이다.** RNN은 순서대로 읽어서
> 순서를 알지만 병렬화가 안 됐고, Transformer는 전부 동시에 봐서 병렬화되지만 순서를 따로
> 주입해야 한다. **속도를 얻고 순서를 잃은 뒤 다시 사 온 것.**

## 6. 전체 동작 과정

```
1. 입력      →  2. 토큰화     →  3. 임베딩      →  4. 트랜스포머  →  5. 출력
사용자 입력      텍스트 분할       벡터 변환         문맥 학습        결과 생성
```

| 입력 처리 | 출력 생성 |
|---|---|
| 사용자 입력: `"안녕하세요. 오늘 날씨 어때요?"` | **언어 모델 헤드** — 다음에 올 단어의 확률 분포 계산 |
| 토큰화 | **오토레그레시브** — 한 토큰씩 생성, 새 토큰을 입력 시퀀스에 추가 |
| 임베딩 — 고차원 벡터화 | **종료 조건** — 더 이상 생성할 필요가 없을 때 멈춤 |
| **포지셔널 인코딩** — 순서 정보 포함 | |

> **"오토레그레시브: 한 토큰씩 생성, 새 토큰을 입력 시퀀스에 추가"** —
> ⭐ **이 한 줄이 [[Inference optimization]]과 [[Batch and online serving]]의 물리적 근거다.**
> 출력 토큰 수만큼 forward pass를 반복하므로 **생성 길이가 곧 latency**이고, 각 스텝이 이전
> 스텝에 의존하므로 **한 요청 안에서는 병렬화할 수 없다.** 강의는 이 연결을 하지 않는다.

## ⚠️ 이 덱의 문제

| 위치 | 문제 |
|---|---|
| 전반 | **출처 없음** — *Attention Is All You Need*(Vaswani et al., 2017)를 인용하지 않는다. Attention 수식을 그대로 쓰면서 원논문을 언급하지 않는 것은 이례적이다 |
| Attention | **차원 설명이 없다** — `d_k`가 무엇인지, Q/K/V가 어디서 오는지(학습되는 선형 사영), head 수와 차원의 관계가 없다. 수식만 놓여 있다 |
| Attention | **계산 복잡도가 없다** — 시퀀스 길이 제곱 증가는 컨텍스트 비용의 핵심인데 여기서 안 나온다. 코스 전체에서 이 사실은 [[Retrieval-augmented generation]](Part 3 Ch4, *Lost in the Middle* 절)에만 한 줄 있다 |
| FFN | **"2개의 선형 변환과 ReLU"** — 현대 LLM은 GeLU/SwiGLU가 표준. 2017년 원논문 기준 서술 |
| Positional Encoding | **사인/코사인만 다룬다** — RoPE·ALiBi 등 현행 LLM이 실제로 쓰는 방식이 없다. 긴 컨텍스트 확장과 직결되는 주제인데 빠졌다 |
| 임베딩 | **덱 2와 용어 충돌** — 위 "주의" 참고 |

## 링크

- **앞** — [[AI DE Course - Part5 LLM foundations and NLP history]]
- 개념: [[Transformer architecture]] · [[Tokenization]] · [[Text embeddings]]
- 비용으로 이어지는 곳: [[LLMOps]] (토큰 단가) · [[Context engineering]] (컨텍스트가 다이얼)
- 하드웨어: [[GPU architecture]] — H100의 **Transformer Engine**이 겨냥하는 연산이 여기 있다
- 서빙: [[Inference optimization]] · [[Batch and online serving]] — 자가회귀 생성의 결과
- 코스: [[AI Data Engineering (Fast Campus course)]]

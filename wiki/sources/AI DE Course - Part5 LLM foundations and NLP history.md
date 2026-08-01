---
type: source
title: AI DE Course - Part5 LLM foundations and NLP history
area: [data-engineering, programming]
aliases: [Part5 LLM 기초, LLM에 대한 기본 이해, LLM 이란, NLP 발전 역사]
tags: [data-engineering, programming, course, fast-campus, llm, nlp, transformer, gpt, bert, n-gram, rnn]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/01. LLM에 대한 기본 이해.pdf (p2–10)"]
---

# AI DE Course - Part5 LLM foundations and NLP history

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 5**(LLM·RAG) 첫 덱
**"LLM에 대한 기본 이해"의 전반부**. 원본(로컬): `raw/data-engineering/01. LLM에 대한 기본 이해.pdf`
**p2–10** (16p 중). PDF 작성일 2026-04-21. 강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⚠️ **Part 5는 파트 번호도 챕터 번호도 자료에 없다.** 세 덱의 파일명이 `01.` · `01.` · `1.`로
> 전부 1번이고, 덱 간 순서 표기도 없다. 이 페이지의 "Part 5", "전반부/후반부" 구분은
> **위키의 정리 판단**이다.

> ⭐ **이 덱이 코스 전체에서 "LLM 자체"를 처음 설명한다.** Part 1~4는 LLM을 계속 전제로 놓고
> (비정형 수집의 종착점, [[LLMOps]]의 관리 대상, [[GPU architecture|GPU]]의 워크로드,
> [[Retrieval-augmented generation|RAG]]의 generator) **정작 그것이 무엇인지는 다루지 않았다.**
> Part 5는 그 빈칸을 뒤늦게 채우는 파트다.

## 구성

`LLM 이란? · N-gram · RNN과 LSTM · NLP 발전 역사 · Transformer 핵심 개념 · 사전학습과 파인튜닝 ·
GPT · GPT 진화와 능력 · BERT vs GPT`

슬라이드는 전부 **좌: 정의 + 핵심 원리 / 우: 도식 또는 예시** 2단 인포그래픽 양식이다.

---

## LLM이란

> **"대규모 텍스트 데이터로 학습된 거대한 딥러닝 언어 모델. Transformer 아키텍처를 기반으로 하며,
> 문맥을 보고 다음에 올 단어의 확률을 예측하는 방식으로 동작한다."**

핵심 원리 셋:

| | |
|---|---|
| **문맥 기반 예측** | 이전 단어들을 보고 다음에 올 단어를 예측 |
| **자가회귀(Autoregressive)** | 생성된 토큰을 다시 입력으로 사용 |
| **확률 분포** | 모든 가능한 단어에 대한 확률을 계산 |

동작 흐름: `토큰화 + 임베딩 → Self-Attention → 확률 계산 → 토큰 예측`
규모 축: **수십억~수천억 파라미터**.

> **"LLM은 2017년 Transformer 아키텍처 등장 이후 급격히 발전했습니다."** — 덱이 두 번 반복하는 문장.

## 언어 모델의 계보 — 무엇을 못해서 다음이 나왔나

덱은 세 세대를 순서대로 놓는다. **각 세대의 "한계" 칸이 다음 세대의 존재 이유다.**

### 1. N-gram — 통계적 언어 모델(SLM)

**N개의 연속된 단어 묶음으로 다음 단어의 확률을 추정한다.**

| N | `"나는 오늘 사과를 먹는다"` |
|---|---|
| 1-gram | `["나는", "오늘", "사과를", "먹는다"]` |
| 2-gram | `["나는 오늘", "오늘 사과를", "사과를 먹는다"]` |
| 3-gram | `["나는 오늘 사과를", "오늘 사과를 먹는다"]` |

| 장점 | 한계 |
|---|---|
| 단순하고 빠름 | **고정 길이 문맥** |
| 적은 데이터로 가능 | **희소성 문제** |
| 구현이 쉬움 | 긴 문장 처리 어려움 |

### 2. RNN / LSTM — 순환 신경망

**이전 정보를 은닉 상태(hidden state)에 저장하며 순차적으로 처리한다.** 단어를 하나씩 순서대로
읽고, 앞서 본 단어의 정보를 은닉 상태에 반영한다.

| 장점 | 한계 |
|---|---|
| 순차 데이터 처리 | **장기 의존성 문제** |
| 가변 길이 입력 | **기울기 소실/폭발** |
| 문맥 정보 활용 | ⭐ **병렬화 어려움** |

> ⭐ **마지막 한계가 Transformer의 존재 이유다.** 순차적으로만 계산할 수 있으면 GPU를 채울 수 없다.
> [[GPU architecture]]의 SIMT 관점에서 보면 RNN은 하드웨어와 궁합이 나쁜 구조다.

### 3. Transformer — Attention 기반

**어텐션으로 순차 처리를 버리고 병렬 처리를 얻었다.** 자세한 내부는
[[AI DE Course - Part5 Transformer internals]]에서 다룬다. 이 덱의 개요 슬라이드가 짚는 셋:

- **병렬 처리 가능** → 학습 속도 비약적 향상
- **긴 문맥 처리** → Attention으로 장거리 의존성 해결
- **위치 정보 보존** → Positional Encoding 활용

## NLP 발전 역사

```
BoW  →  TF-IDF  →  Word2Vec  →  RNN/LSTM  →  Transformer  →  BERT/GPT
단어 빈도   단어 중요도    단어 임베딩      순차·문맥 처리     Attention      Pre-training
기초 모델   가중치 반영    의미 부여                        혁신 아키텍처    대규모 모델 시대
```

네 시기로 묶는다: **통계 기반**(BoW·TF-IDF) → **신경망 기반**(RNN·LSTM) →
**Attention 기반**(Transformer) → **대규모 모델**(GPT·BERT).

> **BoW·TF-IDF가 여기 있는 것이 [[AI DE Course - Part5 Hybrid search and reranking|덱 3]]과 연결된다.**
> 통계 기반 시대의 유물처럼 배치돼 있지만, **BM25는 TF-IDF 계열의 직계 후손이고 2026년에도 하이브리드
> 검색의 절반을 담당한다.** 이 덱의 선형 발전사 서술은 그 점을 놓친다 —
> **밀려난 것이 아니라 역할이 나뉜 것이다.**

## 사전학습과 파인튜닝

| | |
|---|---|
| **사전학습(Pre-training)** | 대규모 **비지도/자가지도** 데이터로 언어의 일반적 패턴과 규칙을 학습 |
| **파인튜닝(Fine-tuning)** | 사전학습 모델을 특정 태스크의 소량 레이블 데이터로 미세 조정 |

사전학습의 핵심 원리: **자가지도 학습**(레이블 없는 데이터로 스스로 학습) · **대규모
데이터**(수십억~수천억 토큰) · 일반화된 언어 이해 · **Transfer Learning**.

파인튜닝 3단계:

```
1. 사전학습된 모델 로드   — 거대 데이터로 학습된 베이스 모델
2. 특정 태스크 데이터 준비 — 목표 태스크에 맞는 소량의 레이블 데이터
3. 모델 미세 조정        — 학습률을 낮춰 특정 태스크에 최적화
```

이점: 빠른 학습 · 적은 리소스 · 전문성(도메인 최적화).

> **DE 관점의 함의:** 파인튜닝은 **"소량의 레이블 데이터"를 만드는 일**이 대부분이다.
> 그 생산 라인이 [[ML data pipeline]]이고, 학습 시점의 데이터를 재현하는 문제가
> [[Data and model versioning]]이다. **강의는 이 연결을 하지 않는다.**

## GPT — 생성형 트랜스포머

**Transformer Decoder 기반의 자가회귀 언어 모델.** 이전 토큰들을 보고 다음 토큰을 예측한다.

```
"나는 오늘"  →  "날씨가"  →  "좋다"  →  "."
토큰을 하나씩 생성하고, 새로 생성된 토큰을 다시 입력으로 사용
```

구조: **Transformer Decoder**(Self-Attention + FFN) · Autoregressive · 대규모 파라미터 ·
대규모 텍스트 사전학습.

### GPT 진화

| | GPT-1 | GPT-2 | GPT-3 | GPT-4 |
|---|---|---|---|---|
| 파라미터 | 1.17억 | 15억 | 1750억 | **1.76조** ⚠️ |
| 특징 | 언어 모델의 가능성 증명 | 자연스러운 텍스트 생성 | 대규모 모델, **Few-shot** | 멀티모달, 추론 능력 향상 |

> ⚠️ **GPT-4의 "1.76조 파라미터"는 확인되지 않은 수치다.** OpenAI는 GPT-4의 파라미터 수를 공개한 적이
> 없다. 널리 퍼진 추정치를 **확정 사실처럼 표에 넣었다.** GPT-1~3은 논문에 공개된 값이라 맞다.

## BERT vs GPT

| 항목 | GPT | BERT |
|---|---|---|
| 구조 | **Decoder** 기반 | **Encoder** 기반 |
| 방향성 | 단방향 (좌→우) | **양방향** |
| 학습 방식 | 다음 단어 예측 | **마스크드 언어 모델(MLM)** |
| 주력 | 텍스트 **생성** | 텍스트 **이해** |
| 활용 | 대화, 생성, 요약 | 분류, QA, NER |
| 파라미터 | 1750억 (GPT-3) | 3.4억 (BERT-base) |

> **"GPT와 BERT는 각각 생성과 이해에 특화된 모델입니다."**

⭐ **이 구분이 다음 두 덱으로 이어진다.** BERT 계열(encoder)은 생성이 아니라 **표현을 만드는 데**
쓰인다 — [[AI DE Course - Part5 Embeddings and vector search|임베딩 모델]]의 SBERT,
[[AI DE Course - Part5 Hybrid search and reranking|리랭킹]]의 Cross-Encoder가 모두 encoder 계열이다.
**RAG 시스템에는 GPT 계열과 BERT 계열이 함께 들어간다.**

## ⚠️ 이 덱의 문제

| 위치 | 문제 |
|---|---|
| RNN 슬라이드 | ⚠️⚠️ **연도 오류** — "RNN은 **2014년 LSTM의 등장**으로 장기 의존성 문제를 일부 해결했습니다". LSTM은 **1997년** Hochreiter & Schmidhuber. 2014년은 GRU(Cho et al.)와 seq2seq의 해다 |
| GPT 진화 표 | ⚠️ **GPT-4 1.76조 파라미터** — OpenAI 미공개. 추정치를 확정 사실로 표기 (위 참고) |
| GPT 진화 표 | **GPT-4 이후가 없다** — PDF 작성일이 2026-04인데 모델 계보가 GPT-4에서 끝난다. o1/o3 계열의 추론 모델, 경쟁 모델(Claude·Gemini·Llama)이 전혀 없다 |
| 전반 | **출처가 하나도 없다** — Transformer 논문(*Attention Is All You Need*), BERT 논문, GPT 논문 중 어느 것도 인용되지 않는다. Part 3·Part 4 Ch1과 비교하면 후퇴 |
| 발전사 슬라이드 | **선형 대체 서사** — BoW·TF-IDF가 Transformer로 "대체됐다"는 인상을 주지만, 같은 Part 5의 덱 3이 **BM25(TF-IDF 계열)를 현역 필수 요소로 다룬다.** 파트 내부에서 서로 어긋난다 |

## 링크

- **다음** — [[AI DE Course - Part5 Transformer internals]] (같은 덱의 후반부, 내부 구조)
- 개념: [[Large language model]] · [[Transformer architecture]]
- 모델: [[GPT]] · [[BERT]]
- 되돌아오는 곳: [[LLMOps]] — 이 모델을 운영에 올릴 때의 관리 대상
- 하드웨어: [[GPU architecture]] — "병렬화 어려움"이 왜 치명적인지의 근거
- 코스: [[AI Data Engineering (Fast Campus course)]]

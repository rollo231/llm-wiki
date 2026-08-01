---
type: entity
title: GPT
area: [programming, data-engineering]
aliases: [Generative Pre-trained Transformer, GPT-3, GPT-4, ChatGPT 모델, 생성형 트랜스포머]
tags: [gpt, llm, transformer, decoder, openai, autoregressive, programming, data-engineering]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part5 LLM foundations and NLP history]]"]
---

# GPT

**Generative Pre-trained Transformer — [[Transformer architecture|Transformer]] **Decoder** 기반의
자가회귀 언어 모델 계열.** OpenAI가 만들었다.

```
"나는 오늘"  →  "날씨가"  →  "좋다"  →  "."
생성한 토큰을 다시 입력에 붙여 다음 토큰을 예측
```

## 구조

| | |
|---|---|
| **Decoder-only** | Self-Attention + FFN. 인코더 없이 디코더 블록만 쌓는다 |
| **단방향** | 왼쪽 문맥만 본다 (좌→우) |
| **자가회귀** | 이전 토큰으로 다음 토큰 예측 |
| **사전학습** | 대규모 텍스트로 일반 언어 패턴 학습 → [[Large language model]] |

## 세대

| | GPT-1 | GPT-2 | GPT-3 | GPT-4 |
|---|---|---|---|---|
| 파라미터 | 1.17억 | 15억 | 1750억 | ⚠️ **미공개** |
| 의의 | 언어 모델의 가능성 증명 | 자연스러운 텍스트 생성 | **Few-shot 학습** | 멀티모달, 추론 능력 |

⚠️ **강의는 GPT-4를 "1.76조 파라미터"로 표기하지만 OpenAI는 공개한 적이 없다** — 널리 퍼진
추정치를 확정 사실처럼 실었다. GPT-1~3은 논문 공개값이라 정확하다.

⚠️ **강의의 계보는 GPT-4에서 끝난다.** PDF 작성일이 2026-04인데 이후의 추론 모델 계열과 경쟁
모델(Claude·Gemini·Llama)이 전혀 없다. **모델 목록으로 읽으면 안 되고, decoder 계열의 원형을
설명하는 자료로 읽어야 한다.**

## 위키에서의 위치

**"생성" 쪽 계보의 대표.** 이해 쪽은 [[BERT]]다.

| | GPT | [[BERT]] |
|---|---|---|
| 구조 | **Decoder** | Encoder |
| 방향성 | 단방향 | 양방향 |
| 주력 | 텍스트 **생성** | 텍스트 **이해** |

**RAG 시스템에서 GPT 계열은 generator 자리에 온다** — 검색과 리랭킹은 encoder 계열이 맡는다
([[Hybrid search and reranking]]).

## 관련 페이지

- [[Large language model]] · [[Transformer architecture]]
- [[BERT]] — 같은 Transformer의 반대쪽 절반
- [[Retrieval-augmented generation]] — GPT 계열이 generator로 들어가는 시스템
- [[Inference optimization]] · [[Batch and online serving]] — 자가회귀 생성의 서빙 비용
- [[LLMOps]] — 운영 관점

## 출처

- [[AI DE Course - Part5 LLM foundations and NLP history]] (Fast Campus, Part 5)

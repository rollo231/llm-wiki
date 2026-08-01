---
type: concept
title: Large language model
area: [data-engineering, programming]
aliases: [LLM, 대규모 언어 모델, 거대 언어 모델, 언어 모델, Language model, Autoregressive]
tags: [llm, nlp, transformer, gpt, bert, pretraining, fine-tuning, data-engineering, programming]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part5 LLM foundations and NLP history]]", "[[AI DE Course - Part5 Embeddings and vector search]]"]
---

# Large language model

**대규모 텍스트로 학습된 딥러닝 언어 모델. 문맥을 보고 다음에 올 토큰의 확률 분포를 계산하고, 뽑은
토큰을 다시 입력에 붙여 반복한다.**

> **모델이 하는 일은 하나다 — 다음 토큰의 확률을 내놓는 것.**
> 요약·번역·코드 생성은 전부 그 하나를 반복해 얻는 부산물이다.

이 위키에서 LLM은 **Part 1~4 내내 전제로만 존재했다** — [[Unstructured data ingestion]]의 종착점,
[[LLMOps]]의 관리 대상, [[GPU architecture]]의 워크로드, [[Retrieval-augmented generation]]의
generator. **Part 5에서 처음 대상 자체로 다뤄진다.**

## 세 가지 핵심 성질

| | |
|---|---|
| **문맥 기반 예측** | 이전 토큰들을 보고 다음 토큰을 예측 |
| **자가회귀(Autoregressive)** | 생성한 토큰을 다시 입력으로 사용 — 한 스텝씩 |
| **확률 분포** | 어휘 전체에 대한 확률을 계산한 뒤 샘플링 |

### ⭐ 자가회귀가 시스템에 미치는 영향

**출력 토큰 하나당 forward pass 한 번.** 그래서:

- **생성 길이가 곧 latency다.** 입력 길이가 아니라 출력 길이가 응답 시간을 지배한다.
- **한 요청 안에서는 병렬화할 수 없다.** 다음 토큰은 이전 토큰이 정해져야 계산된다.
- 처리량은 **요청을 모아서**(배칭) 올릴 수밖에 없다 → [[Inference optimization]]의 dynamic batching.

**[[Latency and throughput]]의 "시소의 법칙"이 LLM 서빙에서 취하는 형태**가 이것이다.

## 계보 — 무엇을 못해서 다음이 나왔나

| 세대 | 방식 | 결정적 한계 |
|---|---|---|
| **N-gram** (통계) | N개 연속 단어로 다음 단어 확률 추정 | **고정 길이 문맥**, 희소성 |
| **RNN / LSTM** (신경망) | 은닉 상태에 과거를 누적하며 순차 처리 | 장기 의존성, 기울기 소실, ⭐ **병렬화 불가** |
| **Transformer** (Attention) | 모든 토큰 쌍의 관련성을 한 번에 계산 | 시퀀스 길이에 **제곱**으로 늘어나는 비용 |

> ⭐ **RNN의 "병렬화 불가"가 Transformer를 불러왔다.** 순차적으로만 계산되는 구조는 GPU를 채울 수
> 없다([[GPU architecture]]의 SIMT). **모델 구조의 전환이 하드웨어 활용률 문제였다는 점**이
> DE에게 중요한 대목이다.

전체 흐름: `BoW → TF-IDF → Word2Vec → RNN/LSTM → Transformer → BERT/GPT`
(통계 기반 → 신경망 기반 → Attention 기반 → 대규모 모델).

⚠️ **이 발전사는 "대체"가 아니다.** 통계 기반의 후손인 **BM25는 2026년에도 현역**이며
[[Hybrid search and reranking]]의 절반을 담당한다. 밀려난 것이 아니라 역할이 나뉘었다.

## 두 갈래 — 생성과 이해

| | [[GPT]] 계열 | [[BERT]] 계열 |
|---|---|---|
| 구조 | **Decoder** | **Encoder** |
| 방향성 | 단방향 (좌→우) | **양방향** |
| 학습 | 다음 단어 예측 | 마스크드 언어 모델(MLM) |
| 주력 | 텍스트 **생성** | 텍스트 **이해**(표현 생성) |
| 활용 | 대화·생성·요약 | 분류·QA·NER·**임베딩·리랭킹** |

> ⭐ **RAG 시스템에는 둘 다 들어간다.** 검색용 임베딩(SBERT)과 리랭킹(Cross-Encoder)은 encoder
> 계열이고, 답변 생성은 decoder 계열이다. **"LLM을 쓴다"는 말은 보통 두 종류의 모델을 운영한다는
> 뜻이다** — [[Model serving platforms]]의 관점에서는 서빙 대상이 하나가 아니다.

## 사전학습과 파인튜닝

| | |
|---|---|
| **사전학습** | 대규모 **자가지도** 데이터로 일반적인 언어 패턴을 학습. 레이블 불필요 |
| **파인튜닝** | 소량의 태스크별 레이블 데이터로, **학습률을 낮춰** 미세 조정 |

**DE 관점의 함의:** 파인튜닝 작업의 대부분은 모델이 아니라 **"소량의 레이블 데이터"를 만드는
일**이다. 그 생산 라인이 [[ML data pipeline]](라벨링·검증·분할)이고, 학습 시점을 재현하는 문제가
[[Data and model versioning]]이다.

**그리고 실무의 첫 선택은 보통 파인튜닝이 아니라 [[Retrieval-augmented generation|RAG]]다** —
지식을 넣는 문제라면 재학습보다 검색이 싸고 빠르며 출처가 남는다.

## 규모

| | GPT-1 | GPT-2 | GPT-3 | GPT-4 |
|---|---|---|---|---|
| 파라미터 | 1.17억 | 15억 | 1750억 | ⚠️ **미공개** |

⚠️ **강의는 GPT-4를 "1.76조"로 적지만 OpenAI는 공개한 적이 없다.** 널리 퍼진 추정치다.
GPT-1~3은 논문 공개값이라 정확하다.

## 이 페이지가 다루지 않는 것

- 내부 구조(Attention·FFN·Positional Encoding) → [[Transformer architecture]]
- 입력이 토큰으로 쪼개지는 방식과 그 비용 → [[Tokenization]]
- 운영·비용·프롬프트 관리 → [[LLMOps]] · [[Context engineering]]
- 외부 지식 연결 → [[Retrieval-augmented generation]]
- 추론 자원과 서빙 → [[Inference optimization]] · [[Batch and online serving]] · [[GPU architecture]]

## 관련 페이지

- [[Transformer architecture]] — 이 모델을 가능하게 한 구조
- [[Tokenization]] — 입력의 단위이자 비용의 단위
- [[Text embeddings]] — 같은 기술이 "생성"이 아니라 "표현"에 쓰일 때
- [[AI data engineering]] — 이 모델을 지원하는 것이 DE의 새 일이 됐다

## 출처

- [[AI DE Course - Part5 LLM foundations and NLP history]] (Fast Campus, Part 5)
- [[AI DE Course - Part5 Embeddings and vector search]] — 디코딩(Top-k 샘플링) 언급

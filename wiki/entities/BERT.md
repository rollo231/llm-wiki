---
type: entity
title: BERT
area: [programming, data-engineering]
aliases: [Bidirectional Encoder Representations from Transformers, SBERT, Sentence-BERT, 마스크드 언어 모델, MLM]
tags: [bert, sbert, llm, transformer, encoder, embedding, reranking, programming, data-engineering]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part5 LLM foundations and NLP history]]", "[[AI DE Course - Part5 Embeddings and vector search]]", "[[AI DE Course - Part5 Hybrid search and reranking]]"]
---

# BERT

**[[Transformer architecture|Transformer]] **Encoder** 기반의 양방향 언어 모델.**
생성이 아니라 **표현을 만드는** 쪽 계보의 원형이다.

## 구조

| | |
|---|---|
| **Encoder-only** | 인코더 블록만 쌓는다 |
| **양방향** | 좌우 문맥을 동시에 본다 |
| **MLM (마스크드 언어 모델)** | 문장의 일부를 가리고 그것을 맞히도록 학습 |
| 규모 | BERT-base 3.4억 파라미터 |

주력: **분류 · QA · NER** — 그리고 이 위키에서 더 중요한 것, **임베딩과 리랭킹**.

## ⭐ RAG 파이프라인에서 BERT 계열이 서는 두 자리

**Part 5를 읽고 나면 BERT는 "옛날 모델"이 아니라 검색단의 현역이다.**

| 자리 | 형태 | 페이지 |
|---|---|---|
| **문서·질의 임베딩** | **SBERT** (Sentence-BERT) — 문장 하나를 대표 벡터로. Bi-Encoder | [[Text embeddings]] |
| **리랭킹** | **Cross-Encoder** — `[CLS] Query [SEP] Doc [SEP]`로 결합해 Full Self-Attention | [[Hybrid search and reranking]] |

> **순수 BERT는 토큰별 벡터를 준다.** 문장 하나를 대표하는 벡터를 얻으려면 별도 학습이 필요하고,
> **SBERT가 그 학습을 한 판본이다.**

⭐ **같은 encoder 구조가 두 방식으로 쓰인다는 점이 핵심이다** —
쿼리와 문서를 **따로** 넣으면 Bi-Encoder(빠름, 사전 계산 가능), **같이** 넣으면
Cross-Encoder(정확함, 사전 계산 불가). **구조가 아니라 입력 방식이 두 단계를 가른다.**

## GPT와의 대비

| 항목 | BERT | [[GPT]] |
|---|---|---|
| 구조 | **Encoder** | Decoder |
| 방향성 | **양방향** | 단방향 (좌→우) |
| 학습 | 마스크드 언어 모델 | 다음 단어 예측 |
| 주력 | 텍스트 **이해** | 텍스트 **생성** |
| 활용 | 분류·QA·NER·**임베딩·리랭킹** | 대화·생성·요약 |

> **RAG 시스템은 둘 다 운영한다** — encoder로 찾고 정렬한 뒤, decoder로 답한다.
> [[Model serving platforms]]의 관점에서 서빙 대상이 하나가 아니라는 뜻이다.

## 관련 페이지

- [[Transformer architecture]] · [[Large language model]]
- [[Text embeddings]] — SBERT가 문맥 반영 임베딩의 대표로 등장
- [[Hybrid search and reranking]] — Bi-Encoder / Cross-Encoder
- [[GPT]] — 반대쪽 절반
- [[Vector database]] — SBERT가 만든 벡터가 담기는 곳

## 출처

- [[AI DE Course - Part5 LLM foundations and NLP history]] — BERT vs GPT 비교표
- [[AI DE Course - Part5 Embeddings and vector search]] — 임베딩 알고리즘 비교(BERT·SBERT)
- [[AI DE Course - Part5 Hybrid search and reranking]] — Cross-Encoder

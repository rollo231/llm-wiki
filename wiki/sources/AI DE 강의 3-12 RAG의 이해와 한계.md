---
type: source
title: AI DE 강의 3-12 RAG의 이해와 한계
aliases: [AI DE 3-12]
tags: [AI-DE-강의, RAG, LLM]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part3/04. Ch4. Graph-RAG.pdf"
---

# AI DE 강의 3-12 RAG의 이해와 한계

[[AI 데이터 엔지니어링 강의]] Part 3 Ch4의 첫 소단원. RAG가 왜 나왔고 어떻게 생겼는지를 원 논문(Lewis et al. 2020)에서 시작해 설명하고, 실무 RAG의 한계 네 가지를 든 뒤 GraphRAG를 "자연스러운 진화 방향"으로 예고한다. Part 5에 RAG 전용 덱이 따로 있지만, 강의 전체에서 RAG의 구조를 처음 정식으로 다루는 곳은 여기다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 3 「시멘틱 & 컨텍스트 기반 데이터 설계」 |
| 덱 제목 | Ch4. Graph-RAG: 1. RAG에 대한 이해와 한계점 |
| 원본 파일 | `part3/04. Ch4. Graph-RAG.pdf` p1–14 (14p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-04-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch4`, 소단원 번호 `1`은 표지 슬라이드 |

## 요약

### 01. RAG가 필요하게 된 이유와 기본 구조 (p3–5)

- LLM은 지식을 파라미터에 저장하지만, 필요한 때 정확한 사실을 꺼내고 최신 정보를 반영하고 출처를 함께 대는 데 한계가 있다. 그렇다고 매번 재학습할 수는 없다.
- RAG는 질문과 관련된 외부 정보를 먼저 검색하고, 그 결과를 컨텍스트로 넣어 LLM이 답하게 하는 구조다. 강의는 원 논문의 표현("pre-trained parametric memory + non-parametric memory의 결합")을 옮기고 "기억만으로 답하는 방식이 아니라 찾아보고 답하는 방식"이라고 푼다.
- Naive RAG의 네 단계: 질문 입력 → Retriever가 외부 지식 저장소에서 검색 → 검색 문서를 프롬프트에 삽입 → Generator가 답변 생성(p5, AWS 설명 페이지 그림).

### 02. 핵심 구성 요소 (p6–7)

- 논문 기준 두 축은 Retriever와 Generator다. 강의는 "검색은 답변을 만드는 것이 아니라 후보 근거를 공급하는 단계"라고 강조하고, 성능은 찾는 단계와 읽고 답하는 단계의 결합 품질에 달렸다고 한다.
- RAG-Sequence는 생성 전체에 같은 검색 문서를 쓰고, RAG-Token은 토큰마다 다른 문서를 쓸 수 있다. 강의의 해석: RAG는 처음부터 "문서를 몇 개 붙일까"가 아니라 "생성과 retrieval을 어떻게 결합할까"의 문제였다.

### 03. 실무의 RAG 분해 (p8–9)

| 단계 | 요소 |
|---|---|
| 검색 이전 | 문서 분할, chunk size 결정, 메타데이터 설계, 임베딩 생성, 인덱싱 |
| 검색 | 질문 임베딩, nearest neighbor retrieval, hybrid search, 필터링 |
| 검색 이후 | reranking, deduplication, compression, context ordering |
| 생성 | prompt assembly, citation strategy, answer control |

RAG가 잘 동작하는 이유로는 네 가지를 든다. 학습하지 않은 private corpus에 접근할 수 있고, 근거를 연결하기 쉽고, 재학습 없이 인덱스로 지식을 갱신할 수 있고, 더 specific·diverse·factual한 출력이 나온다. 맺음은 "모델을 더 똑똑하게 만드는 기술이라기보다 외부 지식을 더 잘 쓰게 만드는 기술"이다.

### 04. RAG의 한계 (p10–13)

1. 검색 단위와 의미 단위가 다르다. 검색은 chunk 단위인데 질문은 개체·사건·원인-결과·문서 간 관계 같은 구조 단위인 경우가 많다. 예: 장애 원인은 A 문서, 영향 범위는 B 문서, 복구 이력은 C 문서.
2. 검색과 생성의 정합성. retriever와 generator의 목적 함수가 달라서, recall이 높아도 generator가 그 문서를 근거로 쓴다는 보장이 없다.
3. Lost in the Middle. 관련 정보가 입력 중간에 있으면 앞이나 뒤에 있을 때보다 성능이 떨어진다. 대응으로 압축·제거·리랭킹으로 정답 문서를 처음이나 끝으로 옮기라고 한다.
4. 고정된 top-k. 검색이 필요 없는 질문에도 문서를 붙이고, 관련도가 낮은 문서도 개수를 채우려고 들어가 noise가 된다. "retrieval should be adaptive."

### 05. RAG의 진화 (p14)

"Naive RAG → Advanced RAG → 구조화된 RAG". 고도화 기법으로 reranking, query rewriting, adaptive retrieval, compression, self-reflection을 들고, 문서를 더 많이 넣는 방향에서 더 잘 구조화하는 방향으로 옮겨 간다고 한다. Graph-RAG는 그 연장선이다.

## 핵심

- RAG의 정의·구성·한계의 전문은 [[검색 증강 생성]]에 모았다. 이 강의의 쓸모는 한계 1번(검색 단위 ≠ 의미 단위)이 Part 3 전체의 동기와 이어진다는 점이다. Ch1~3이 스키마로는 담기지 않는 "의미"와 "관계"를 설계하는 법을 다뤘고, 여기서 그것이 검색 품질 문제로 돌아온다([[시맨틱 계층]], [[지식 그래프]]). 이 연결은 위키의 관찰이다.
- 슬라이드의 3단계 진화 틀은 출처로 단 Gao et al. 서베이와 다르다. 서베이의 세 번째 단계는 "구조화된 RAG"가 아니라 Modular RAG다(아래 결함).
- 한계 4번의 "retrieval should be adaptive"는 연구 흐름과 맞다. Self-RAG(Asai et al., ICLR 2024)는 필요할 때만 검색하고("adaptively retrieves passages on-demand"), Adaptive-RAG(Jeong et al., NAACL 2024)는 질의 복잡도로 검색 안 함·단일 단계·반복 검색을 고른다. [https://arxiv.org/abs/2310.11511 · https://arxiv.org/abs/2403.14403 , 2026-09-28 확인] 슬라이드에는 출처가 없다.

## 주의·결함

- ❗ p14의 "구조화된 RAG"는 서베이의 용어가 아니다. p8이 출처로 다는 Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey"(arXiv 2312.10997, v1 2023-12-18, 개정 2024-03-27)는 Naive RAG, Advanced RAG, Modular RAG의 세 단계로 나눈다. [https://arxiv.org/abs/2312.10997 , 2026-09-28 확인]
- ❗ p12는 Lost in the Middle 설명 옆에 "Transformer는 시퀀스 길이에 따라 메모리와 연산량이 제곱으로 증가"를 붙여, 이것이 원인인 것처럼 읽힌다. 논문(Liu et al., arXiv 2023-07, TACL vol.12 2024 pp.157–173)의 서론에 그 문장이 있기는 하지만, 예전 모델의 컨텍스트 창이 짧았던 배경 설명이다. 논문은 U자 성능의 원인으로 primacy·recency 편향, 모델 구조(encoder-decoder가 더 견고), query-aware contextualization, instruction tuning을 분석하고, self-attention이 기술적으로는 어느 위치의 토큰이든 똑같이 꺼낼 수 있는데도 이 현상이 나타난다고 적는다. 후속 연구 Hsieh et al., "Found in the Middle"(ACL Findings 2024)은 원인을 U자형 위치 attention 편향으로 짚고 보정하면 나아진다고 보였다. 2024~2025년 모델에서 이 현상이 얼마나 남았는지 정량으로 확인한 1차 자료는 찾지 못했다. [https://aclanthology.org/2024.tacl-1.9/ · https://arxiv.org/abs/2406.16008 , 2026-09-28 확인]
- ✅ 원 논문 서술은 맞다. Lewis et al., NeurIPS 2020. parametric memory는 사전학습 seq2seq(BART), non-parametric memory는 DPR로 검색하는 Wikipedia dense index이고, RAG-Sequence와 RAG-Token의 구분도 논문과 같다. p9의 "더 specific, diverse, factual한 출력"은 초록의 "RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline"에서 왔다(arXiv API로 초록 확인). [https://arxiv.org/abs/2005.11401 , 2026-09-28 확인]
- p12의 논문은 제목만 있고 저자·연도가 없다. p5 그림은 AWS 한국어 설명 페이지 URL만 단다.
- 슬라이드 머리글은 "시멘틱"과 표지의 "시맨틱"이 섞여 있다. Part 3 전체의 표기 혼용이다([[AI 데이터 엔지니어링 강의]]).

## 관련

- 개념: [[검색 증강 생성]] · [[GraphRAG]] · [[비정형 데이터 파이프라인]] · [[LLMOps]] · [[지식 그래프]] · [[시맨틱 계층]] · [[하이브리드 검색]] · [[리랭킹]]
- Part 5에서 다시 나오는 RAG: [[AI DE 강의 5-03 LLM의 한계와 RAG]]와 [[AI DE 강의 5-04 하이브리드 검색과 리랭킹]]이 RAG를 다시 다루지만 이 강의를 참조하지 않는다. 5-04는 세 번째 단계에 「구조화된 RAG」 대신 Agentic·Adaptive RAG를 놓는다([[검색 증강 생성]]의 「세대」 이름의 불일치 절).
- 이전 강의: [[AI DE 강의 3-11 SHACL 검증]]
- 다음 강의: [[AI DE 강의 3-13 GraphRAG 개념과 사례]]

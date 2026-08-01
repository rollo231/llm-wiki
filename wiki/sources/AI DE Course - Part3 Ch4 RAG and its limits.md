---
type: source
title: AI DE Course - Part3 Ch4 RAG and its limits
area: [data-engineering, programming]
aliases: [Part3 Ch4-1, RAG에 대한 이해와 한계점]
tags: [data-engineering, course, fast-campus, rag, llm, retrieval, lost-in-the-middle]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/Part 3_Ch 4.pdf (p1–14)"]
---

# AI DE Course - Part3 Ch4 RAG and its limits

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch4 "Graph-RAG"의 소단원 **1**
"RAG에 대한 이해와 한계점". 원본(로컬): `raw/data-engineering/Part 3_Ch 4.pdf` **p1–14** (49p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐ **이 코스에서 출처 표기가 가장 촘촘한 소단원이다.** RAG 원논문, RAG Survey(arXiv 번호까지),
> Lost in the Middle, AWS 문서 — 네 건이 명시된다. Part 1의 "출처 없는 80%" 관행과 뚜렷이 다르다.

## 구성

`01 RAG (Retrieval-Augmented Generation) · 02 RAG를 이루는 핵심 구성요소 · 03 RAG 분해 ·
04 RAG의 한계 · 05 RAG의 진화`

## 정의

> **"모델이 모든 지식을 내부 파라미터에만 의존하지 않고, 외부 지식 저장소에서 관련 정보를 검색한 뒤
> 그 정보를 근거로 답변을 생성."**
> **"기억만으로 답하는 방식이 아니라 찾아보고 답하는 방식."**

원 논문(*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*)의 표현으로는
**pre-trained parametric memory + non-parametric memory의 결합.**

Naive RAG 4단계: 질문 입력 → Retriever가 외부 지식 저장소에서 관련 문서 검색 → 검색된 문서를 프롬프트
컨텍스트에 삽입 → Generator가 답변 생성.

## 두 축과 그 사이의 틈

| | 역할 |
|---|---|
| **Retriever** | 질문과 관련 있는 문서를 external memory에서 검색 |
| **Generator** | 검색된 문서와 질문을 함께 보고 답변 생성 |

> ⭐ **"검색은 답변을 만드는 것이 아니라, 답변 생성을 위한 후보 근거를 공급하는 단계다.
> 즉 RAG의 성능은 찾는 단계와 읽고 답하는 단계의 결합 품질에 달려 있다."**

### RAG-Sequence와 RAG-Token

논문은 RAG를 한 가지 방식으로만 제안하지 않았다 — **RAG-Sequence**(생성 전체 동안 같은 retrieved
passages 사용) vs **RAG-Token**(생성 토큰마다 다른 passages 사용 가능).

> **"RAG는 처음부터 '문서를 몇 개 붙일까' 수준의 문제가 아니라, 생성과 retrieval의 결합 방식을
> 어떻게 설계할까의 문제였다."**
>
> 이 관찰이 좋다. 대부분의 RAG 소개가 top-k 문서 붙이기로 시작하는데, **원논문이 이미 더 넓은
> 설계 공간을 열어뒀다**는 걸 짚는다.

## 실무의 RAG 분해

| 검색 이전 | 검색 단계 | 검색 이후 | 생성 단계 |
|---|---|---|---|
| 문서 분할 · chunk size 결정 · 메타데이터 설계 · 임베딩 생성 · 인덱싱 | 질문 임베딩 · nearest neighbor retrieval · hybrid search · 필터링 | reranking · deduplication · compression · context ordering | prompt assembly · citation strategy · answer control |

출처: *Retrieval-Augmented Generation for Large Language Models: A Survey*,
`https://arxiv.org/pdf/2312.10997`

## 왜 잘 동작하나 — 네 가지

1. 모델이 학습하지 않은 **private corpus**에도 접근 가능
2. 외부 문서를 보여주므로 **답변 근거를 연결하기 쉽다**
3. 도메인 문서를 인덱스로 관리하면 **모델 재학습 없이 지식 업데이트** 가능
4. 파라미터 내부 지식만으로 답할 때보다 더 **specific, diverse, factual**한 출력

> **"모델을 더 똑똑하게 만드는 기술이라기보다 모델이 외부 지식을 더 잘 쓰게 만드는 기술."**

## ⭐ 한계 4종 — Ch4 전체의 논거

### 1. 검색 단위와 의미 단위가 일치하지 않는다

> ⭐⭐ **"RAG의 첫 번째 문제는 검색 단위가 보통 chunk인데, 질문 단위는 structure인 경우가 많다는 것."**

사용자가 궁금한 것은 종종 chunk가 아니라 **개체, 사건, 원인-결과, 정책-예외, 문서 간 관계** 같은 더
큰 의미 단위다.

예: 장애 원인은 A 문서에, 영향 범위는 B 문서에, 복구 이력은 C 문서에.
**"하지만 검색은 각 조각을 따로 찾는다."**

**이 한 줄이 GraphRAG가 존재하는 이유의 전부다.**

### 2. 검색–생성 정합성 문제

**retriever와 generator의 목적 함수가 다르다.** retriever는 유사한 문서를 찾고 generator는 답변을
만든다. **"retriever가 높은 recall을 보였다고 해도 generator가 그 문서를 잘 읽고 정답 근거로
사용한다는 보장은 없다."**

실무 증상: 관련 문서를 가져왔는데 답변이 틀림 · 불필요한 문서가 많아 오히려 답변이 흐려짐 ·
정답 문서가 포함돼도 generator가 엉뚱한 문장을 근거로 삼음.

> **"RAG의 품질 문제는 retrieval failure뿐 아니라 retrieval–generation mismatch 문제다."**

### 3. Lost in the Middle

> "그러면 검색 결과를 더 많이 넣으면 되지 않나?" → **아니다.**

관련 정보가 입력의 앞이나 뒤에 있을 때보다 **중간**에 있을 때 성능이 크게 떨어질 수 있다.
**"긴 context window가 있어도 모델이 그 안의 정보를 고르게 잘 쓰는 것은 아니다."**

> **"긴 입력이 가능하다고 했지, 성능이 더 좋다고 한 적은 없다.
> 입력이 길면 비싼 비용 지불, 성능 향상 없음."**

대응: 정답 문서를 가운데에 두지 않기 — 처음이나 끝으로 옮기기(압축·제거·리랭킹).

출처: *Lost in the Middle: How Language Models Use Long Contexts*.
**정확도 vs 문서 위치 그래프(gpt-3.5-turbo-0613, 20 documents ~4K tokens)까지 인용한다.**

### 4. 고정된 k개 문서 검색

두 문제: ① 어떤 질문은 retrieval이 거의 필요 없는데도 무조건 문서를 붙여 응답을 흐릴 수 있다
② 검색된 문서 중 일부가 relevance가 낮아도 고정된 수만큼 강제로 들어가면 noise가 된다.

> **"모든 질문이 같은 retrieval budget을 가져야 하는 것은 아니다 — retrieval should be adaptive."**

## 진화

```
Naive RAG → Advanced RAG → 구조화된 RAG
```

고도화된 RAG: reranking · query rewriting · adaptive retrieval · compression · self-reflection.

> **"문서를 더 많이 넣는 방향에서, 문서를 더 잘 구조화하고 그 구조를 검색·요약·추론에 쓰는 방향으로
> 이동. Graph-RAG는 기존 RAG가 부딪힌 구조적 한계를 해결하려는 자연스러운 진화 방향."**

## 기존 페이지와의 대조

- **새 concept:** [[Retrieval-augmented generation]]
- ⚠️ **[[Unstructured data ingestion]](Part 1 CH03-5,6)의 RAG 서술이 얕았다는 게 드러난다.**
  Part 1은 RAG를 "비정형 파이프라인 4단계의 종착점(OCR → 임베딩 → Vector DB → RAG)"으로만 다뤘고
  **한계는 한 줄도 없었다.** 모순은 아니지만 깊이 차이가 크다 — Part 1 페이지에 이 페이지로의 링크를
  달아야 한다.
- **[[LLMOps]]의 미해결 질문에 부분 답** — MOC에 남긴 *"retrieval 품질을 무엇으로 재나"* 는 **여전히
  안 나온다.** recall@k·MRR·nDCG 같은 지표는 여기서도 언급되지 않는다. 다만 **무엇이 실패하는지**
  (4종)는 이제 안다.
- **[[Context engineering]]과 연결** — Lost in the Middle은 "컨텍스트를 많이 넣으면 좋다"는 가정에
  대한 실증적 반박이다.

## 자료 품질

**Part 3에서 가장 출처가 좋은 소단원.**

- 인용 4건: RAG 원논문 · RAG Survey(arXiv 2312.10997) · Lost in the Middle · AWS RAG 설명 페이지
- 그래프 인용 시 논문 제목 명기
- 중복 슬라이드 없음, 14페이지 전부 내용 있음
- **출처 없는 수치 없음**

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Retrieval-augmented generation]] · [[GraphRAG]] · [[Unstructured data ingestion]] ·
  [[LLMOps]] · [[Context engineering]]
- 앞: [[AI DE Course - Part3 Ch3 SHACL and graph data contracts]]
- 다음: [[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]]

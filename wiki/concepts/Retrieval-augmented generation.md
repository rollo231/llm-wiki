---
type: concept
title: Retrieval-augmented generation
area: [data-engineering, programming]
aliases: [RAG, 검색 증강 생성, Naive RAG, RAG-Sequence, RAG-Token, Lost in the Middle]
tags: [data-engineering, rag, llm, retrieval, vector-search, llmops]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part3 Ch4 RAG and its limits]]", "[[AI DE Course - Part5 Hybrid search and reranking]]", "[[AI DE Course - Part5 RAG pipeline and LangChain]]"]
---

# Retrieval-augmented generation

**모델이 모든 지식을 내부 파라미터에만 의존하지 않고, 외부 지식 저장소에서 관련 정보를 검색한 뒤 그
정보를 근거로 답변을 생성하는 구조.**

> **기억만으로 답하는 방식이 아니라 찾아보고 답하는 방식.**
> 원 논문(*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*)의 표현으로는
> **pre-trained parametric memory + non-parametric memory의 결합.**

[[Unstructured data ingestion]]이 RAG를 파이프라인 4단계의 종착점으로 소개했다면, 이 페이지는
**RAG 자체의 구조와 한계**를 다룬다.

## 왜 필요해졌나

LLM은 많은 지식을 파라미터 안에 저장하지만 **필요한 시점에 정확한 사실을 꺼내고, 최신 정보를
반영하고, 출처를 함께 제시하는 데 한계**가 있다. 그렇다고 매번 재학습할 수는 없다.

## 기본 구조 (Naive RAG)

```
1. 사용자 질문 입력
2. Retriever가 외부 지식 저장소에서 관련 문서 검색
3. 검색된 문서를 프롬프트 컨텍스트에 삽입
4. Generator가 답변 생성
```

논문 기준으로 RAG는 두 축으로 나뉜다:

| | 역할 |
|---|---|
| **Retriever** | 질문과 관련 있는 문서를 external memory에서 검색 |
| **Generator** | 검색된 문서와 질문을 함께 보고 답변 생성 |

> ⭐ **"검색은 답변을 만드는 것이 아니라 답변 생성을 위한 후보 근거를 공급하는 단계다."**
> 즉 **RAG의 성능은 찾는 단계와 읽고 답하는 단계의 결합 품질**에 달려 있다.

### RAG-Sequence와 RAG-Token

논문은 RAG를 한 가지 방식으로만 제안하지 않았다.

- **RAG-Sequence** — 생성 전체 동안 같은 retrieved passages를 사용
- **RAG-Token** — 생성 토큰마다 다른 retrieved passages를 사용할 수 있음

정답이 하나의 문서 안에 있을 때와 생성 중간에 필요한 근거가 달라질 때 **최적 retrieval 전략이 다를
수 있음을 처음부터 보여준다.**

> **"RAG는 처음부터 '문서를 몇 개 붙일까' 수준의 문제가 아니라 생성과 retrieval의 결합 방식을
> 어떻게 설계할까의 문제였다."**

## 실무의 RAG — 단계별 분해

| 검색 이전 | 검색 단계 | 검색 이후 | 생성 단계 |
|---|---|---|---|
| 문서 분할 | 질문 임베딩 | reranking | prompt assembly |
| **chunk size 결정** | nearest neighbor retrieval | deduplication | citation strategy |
| 메타데이터 설계 | hybrid search | compression | answer control |
| 임베딩 생성 | 필터링 | **context ordering** | |
| 인덱싱 | | | |

## 왜 잘 동작하나

파라미터 밖의 지식을 끌어오기 때문이다. 강점은 단순히 최신 정보를 더 넣는 데 있지 않다:

1. 모델이 학습하지 않은 **private corpus**에도 접근 가능
2. 외부 문서를 보여주므로 **답변 근거를 연결하기 쉽다**
3. 도메인 문서를 인덱스로 관리하면 **모델 재학습 없이 지식 업데이트** 가능
4. 파라미터 내부 지식만으로 답할 때보다 더 **specific·diverse·factual**한 출력

> **"모델을 더 똑똑하게 만드는 기술이라기보다 모델이 외부 지식을 더 잘 쓰게 만드는 기술."**

## ⭐ RAG의 한계 4종

### 1. 검색 단위와 의미 단위가 일치하지 않는다

> ⭐ **"검색 단위는 보통 chunk인데, 질문 단위는 structure인 경우가 많다."**

많은 RAG 시스템은 긴 문서를 chunk로 나눈 뒤 검색한다. 하지만 사용자가 궁금한 것은 종종 chunk가
아니라 **개체·사건·원인-결과·정책-예외·문서 간 관계** 같은 더 큰 의미 단위다.

예) 장애 원인은 A 문서에, 영향 범위는 B 문서에, 복구 이력은 C 문서에 있다. **하지만 검색은 각 조각을
따로 찾는다.**

**이 한 줄이 [[GraphRAG]]가 존재하는 이유의 전부다.**

### 2. 검색–생성 정합성 문제 (retrieval–generation mismatch)

검색을 잘했다고 답변이 자동으로 좋아지지는 않는다. **retriever와 generator의 목적 함수가 다르기
때문이다.** retriever는 유사한 문서를 찾고, generator는 답변을 만든다. **retriever가 높은 recall을
보였다고 해서 generator가 그 문서를 잘 읽고 정답 근거로 사용한다는 보장은 없다.**

실무에서 흔한 증상: 관련 문서를 가져왔는데 답변이 틀림 · 불필요한 문서가 많아 오히려 답변이 흐려짐 ·
정답 문서가 포함돼도 generator가 엉뚱한 문장을 근거로 삼음.

> **"RAG의 품질 문제는 retrieval failure뿐 아니라 retrieval–generation mismatch 문제다."**

### 3. Lost in the Middle

> 그러면 검색 결과를 더 많이 넣으면 되지 않나? → **아니다.**

관련 정보가 입력의 **앞이나 뒤**에 있을 때보다 **중간**에 있을 때 성능이 크게 떨어질 수 있다.
긴 context window가 있어도 모델이 그 안의 정보를 고르게 잘 쓰는 것은 아니다.

- 정답과 관련 깊은 문서가 가운데 있을수록 성능 저하, 초반/후반일수록 성능 상승
- Transformer는 시퀀스 길이에 따라 메모리·연산량이 제곱으로 증가
- **긴 입력이 가능하다고 했지, 성능이 더 좋다고 한 적은 없다**

대응: 압축 · 제거 · 리랭킹으로 **정답 문서를 가운데에 두지 않는 것.**

출처: *Lost in the Middle: How Language Models Use Long Contexts* — 강의가 그래프까지 인용한 드문
1차 자료.

### 4. 고정된 top-k 검색의 문제

기본 RAG는 질문마다 top-k 문서를 검색해 모두 넣는다. 두 가지 문제:

1. 어떤 질문은 retrieval이 거의 필요 없는데도 무조건 문서를 붙여 응답을 흐릴 수 있다
2. 검색된 문서 중 일부가 relevance가 낮아도 **고정된 수만큼 강제로 들어가면 noise**가 된다

> **"모든 질문이 같은 retrieval budget을 가져야 하는 것은 아니다 — retrieval should be adaptive."**

## ⭐ 한 층 아래의 한계 3종 — retriever 내부 (Part 5)

위의 넷이 **시스템 수준**의 한계라면, Part 5가 **밀집 검색 자체의 실패 모드**를 따로 짚는다.
**두 목록은 보완적이다** — 층위가 다르다.

| 실패 | 증상 |
|---|---|
| **어휘적 정밀도 부족** | `"GPT-4"` ↔ `"GPT4"`, `"AWS"` ↔ `"Amazon Web Services"`를 놓친다 |
| **시맨틱 드리프트** | 도메인 밖에서 의미가 떠밀린다 — 유사 의미 과적합 |
| ⭐ **정보 압축 병목** | 768차원에 눌러 담으면서 **수치·스키마·식별자가 사라진다** |

> ⭐ **"의미는 남고 식별자는 사라진다."** 임베딩이 버리기 쉬운 것이 하필 정확히 맞아야 하는
> 값들(버전·제품 코드·금액)이다. **BM25를 함께 돌려야 하는 이유가 여기 있다.**

→ [[Hybrid search and reranking]] · [[Text embeddings]]

## RAG의 진화

```
Naive RAG  →  Advanced RAG  →  구조화된 RAG
```

- **초기 RAG** — 검색하고 붙이고 생성
- **고도화된 RAG** — reranking · query rewriting · adaptive retrieval · compression ·
  self-reflection
- **구조화** — 텍스트를 단순 검색 대상이 아니라 **구조화 대상까지 확장**

> **"문서를 더 많이 넣는 방향에서, 문서를 더 잘 구조화하고 그 구조를 검색·요약·추론에 쓰는 방향으로
> 이동."**
> **[[GraphRAG|Graph-RAG]]는 기존 RAG가 부딪힌 구조적 한계를 해결하려는 자연스러운 진화 방향이다.**

### Agentic · Adaptive RAG (Part 5)

**한계 4번(고정 top-k)에 대한 직접적 대응.** 위에서 *"retrieval should be adaptive"*로 끝냈던 그
방향에 이름과 구성요소가 붙는다.

```
Query Analysis  →  Strategy Selection  →  Dynamic Adjustment
의도 분석            검색기 선택              동적 조정
```

- **자율적 계획** — 쿼리를 분석해 검색 전략 수립
- **동적 실행** — 다중 검색기 병렬 실행
- **결과 평가** — 관련성·정확성 검증
- **반복 개선** — **실패 시 재검색**

키워드: `Tool Orchestration` · `Multi-Agent` · `Self-Correction`.

> ⚠️ **두 진화 계보는 서로를 참조하지 않지만 사실 직교한다.**
> Part 3는 `Naive → Advanced → 구조화(GraphRAG)`로, Part 5는 `Naive → 하이브리드·리랭킹 →
> Agentic·Adaptive`로 그린다. **전자는 *무엇을 인덱싱하나*(청크 vs 그래프), 후자는 *어떻게 검색을
> 제어하나*(고정 vs 적응)** — 같은 축의 경쟁이 아니라 다른 축이다. 함께 쓸 수 있다.

## 관련 페이지

- [[GraphRAG]] — 위 한계 4종에 대한 그래프 기반 대응
- [[Hybrid search and reranking]] — 한계 3종(retriever 내부)에 대한 검색단 대응. **BM25 + Dense +
  RRF + Cross-Encoder**
- [[Retrieval evaluation metrics]] — 검색 품질을 따로 재는 지표. **검색 지표는 검색만 증명한다**
- [[Text embeddings]] · [[Vector database]] — 검색단의 두 부품
- [[Unstructured data ingestion]] — RAG로 가는 앞단 파이프라인(OCR·임베딩·Vector DB)
- [[LangChain]] — 이것을 조립하는 프레임워크
- [[LLMOps]] — RAG를 운영에 올릴 때의 관리 대상
- [[Context engineering]] — 컨텍스트 품질과 비용이 같은 다이얼
- [[Knowledge graph]] — 구조화된 retrieval의 대상
- [[Large language model]] — generator 자리에 오는 것

## 인용 자료

- *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* — RAG 원 논문
- *Retrieval-Augmented Generation for Large Language Models: A Survey* —
  `https://arxiv.org/pdf/2312.10997`
- *Lost in the Middle: How Language Models Use Long Contexts*
- AWS — `https://aws.amazon.com/ko/what-is/retrieval-augmented-generation/`

**세 논문 모두 1차 자료 인제스트 후보.** 이 코스에서 출처가 이렇게 촘촘한 챕터는 드물다.

## 출처

- [[AI DE Course - Part3 Ch4 RAG and its limits]] — 구조와 한계 4종 (주 출처)
- [[AI DE Course - Part5 Hybrid search and reranking]] — retriever 내부 한계 3종, Agentic·Adaptive
- [[AI DE Course - Part5 RAG pipeline and LangChain]] — 구축 5단계 (⚠️ Part 3보다 얕다)

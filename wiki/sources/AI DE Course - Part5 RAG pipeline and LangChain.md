---
type: source
title: AI DE Course - Part5 RAG pipeline and LangChain
area: [data-engineering, programming]
aliases: [Part5 RAG 파이프라인, RAG란 무엇인가, 왜 RAG가 필요한가, RAG 활용 사례, LangChain 소개]
tags: [data-engineering, programming, course, fast-campus, rag, llm, langchain, chunking]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/01. LLM과 RAG.pdf (p10–15)"]
---

# AI DE Course - Part5 RAG pipeline and LangChain

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 5**(LLM·RAG) 둘째 덱 **"LLM과 RAG"의 후반부**.
원본(로컬): `raw/data-engineering/01. LLM과 RAG.pdf` **p10–15** (15p 중). PDF 작성일 2026-05-05.
강의 홈: [[AI Data Engineering (Fast Campus course)]].

전반부는 [[AI DE Course - Part5 Embeddings and vector search]].

> ⚠️⚠️ **이 페이지는 위키에서 RAG의 주 페이지가 아니다.** RAG의 구조·한계·진화는 이미
> [[AI DE Course - Part3 Ch4 RAG and its limits]](Part 3 Ch4)가 **원논문·Survey·*Lost in the Middle*을
> 인용하며** 훨씬 깊게 다뤘다. **파트 순서로는 이 덱이 뒤인데 내용은 후퇴한다.**
> 이 페이지는 **그 후퇴를 기록하고, 이 덱에만 있는 두 가지(구축 5단계·LangChain)를 남기는** 역할이다.

## 구성

`LLM의 한계와 문제점 · RAG란 무엇인가 · 왜 RAG가 필요한가 · RAG 작동 원리 · RAG 활용 사례 ·
LangChain 소개`

---

## LLM의 한계와 문제점

| 문제 | 강의의 서술 | 해결 방안 |
|---|---|---|
| **최신 정보 부족** | 훈련 데이터에 한정, 도메인 최신 정보 미반영 | RAG 시스템 도입 |
| **환각(Hallucination)** | 사실과 다른 답변을 **자신있게** 제공 | 출처 제공과 사실 확인 |
| **컨텍스트 제한** | 긴 문서 제한, 출처 제시 어려움, 비용/지연 이슈 | 벡터 DB 활용 |

배지로 `30% 환각률` · `2K 토큰 제한`이 붙어 있다. **둘 다 문제가 있다 — 아래 참고.**

## RAG란

> **"검색(Retrieval)과 생성(Generation)을 결합한 기술로, 외부 지식을 검색해 LLM에 제공하여 더
> 정확하고 최신 정보를 반영한 답변을 생성하는 방식."**

```
사용자 질문 → 임베딩 → 벡터 DB 검색 → Top-K 관련 문서 → 프롬프트 → LLM 생성
              1. 질문 분석      2. 문서 검색            3. 답변 생성
```

세 축: **검색(Retrieval)** — 외부 지식베이스에서 관련 문서 검색 / **생성(Generation)** — 검색된
정보 바탕으로 답변 / **결합(Augmented)** — 검색된 근거를 활용.

필요성 넷: **최신성 확보** · **정확성 향상**(환각 감소) · **도메인 특화**(사내 문서·매뉴얼) ·
**출처 제공**(근거 문서 표시).

**Part 3 Ch4와 내용상 어긋나지 않는다. 다만 그쪽이 "왜 안 되는가"까지 갔다면 여기는 "왜 좋은가"에서
멈춘다.**

## ⭐ RAG 구축 5단계 — 이 덱의 실질적 기여

**Part 3 Ch4가 RAG를 *구조*(Retriever/Generator)로 봤다면, 이 덱은 *만드는 순서*로 본다.**
DE에게는 이쪽이 작업 목록에 가깝다.

```
1. 문서 로딩·전처리   2. 청킹·분할      3. 임베딩 생성    4. 벡터 DB 저장   5. 검색·생성
PDF/TXT/MD 파일 로드   의미 단위로 청킹   임베딩 모델 적용   벡터 인덱싱      Top-K 문서 검색
텍스트 추출 및 정제     오버랩 설정        벡터 변환        유사도 검색 준비   LLM 답변 생성
```

> **"의미 단위로 청킹" + "오버랩 설정"** — 코스 전체에서 청킹 전략이 언급되는 유일한 지점이다.
> **다만 판단 기준(chunk size를 어떻게 정하나, overlap을 몇 %로 두나)은 없다.**
> [[Retrieval-augmented generation]]의 *"검색 단위는 chunk인데 질문 단위는 structure"*가 바로 이
> 2단계에서 결정되는 문제인데, 이 덱은 두 문장으로 지나간다.

**1~4단계가 [[Unstructured data ingestion]](Part 1)의 파이프라인과 정확히 겹친다.** 그쪽은
OCR·PII 비식별화·수명주기까지 다루므로 더 두껍다. **이 덱은 그것을 RAG 관점으로 압축한 판본이다.**

## RAG 활용 사례 4종

| 사례 | 내용 |
|---|---|
| **문서 검색/QA** | 내부 지식 베이스에서 문서 기반 답변 |
| **고객지원 챗봇** | 매뉴얼·FAQ 기반, 24/7 자동 응대 |
| **검색 엔진 보강** | 의미 기반 재랭킹, 사용자 의도 반영 |
| **규정/정책 준수 도우미** | 법적 근거와 출처를 포함한 답변 |

⚠️ **네 사례 모두 배지 수치가 붙지만 실제 사례가 아니다** — 회사명·기간·규모가 없는 유형 나열이다.
[[AI DE Course - AI pipeline case studies]](Part 1)나 [[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]]의
Neo4j 고객 사례와 달리 **검증할 대상 자체가 없다.**

## LangChain

> **"LLM을 활용한 애플리케이션 개발을 위한 프레임워크로, 데이터 연결, 검색 기능, 메모리 시스템,
> 에이전트 기능 등을 제공."**

| 구성 요소 | 역할 |
|---|---|
| **Prompts** | 프롬프트 템플릿과 관리 |
| **LLMs** | 다양한 LLM 모델 연동 |
| **Chains** | 작업 체인 구성 |
| **Agents** | 자율적 에이전트 |

기능 축 넷: 데이터 연결 · 검색 기능 · **메모리 시스템**(대화 기록·컨텍스트 관리) · 에이전트.
이점: 코드 재사용성 · 직관적 인터페이스 · 폭넓은 통합성.

통계 배지: `50K+ GitHub Stars` · `1M+ 월간 다운로드` · `100+ 통합 모델` · `200+ 통합 도구`
— ⚠️ **기준 시점이 없다** (아래 참고).

**코스에서 LangChain이 실체로 다뤄지는 유일한 지점이다.** Part 3의 Neo4j 사례 아키텍처 도식에
이름만 등장한 적이 있다. → [[LangChain]]

## ⚠️ 이 덱의 문제

| 문제 | 내용 |
|---|---|
| ⚠️⚠️ **`2K 토큰 제한`** | **2026년 기준 명백히 낡았다.** GPT-3.5 초기(4K)보다도 작은 수치다. 현행 주요 모델은 100K~1M+ 컨텍스트를 지원한다. **"컨텍스트 제한"이라는 문제 자체는 여전히 유효하지만**(길다고 잘 쓰는 건 아니다 — *Lost in the Middle*), **2K라는 숫자는 사실이 아니다** |
| ⚠️⚠️ **`30% 환각률`** | 출처 없음. 환각률은 **태스크·모델·평가 기준에 따라 크게 달라지는 값**이라 단일 숫자로 제시할 수 없다 |
| ⚠️ **활용 사례의 배지 전부** | `95% 정확도` `3x 검색 속도` `80% 응답률` `-60% 처리시간` `+45% 정확도` `100% 출처 표시` `99% 정확도` — 사례가 특정되지 않아 검증 불가 |
| ⚠️ **`99% 정보 정확도` `100% 출처 표시`** | RAG의 *이점* 슬라이드에 붙은 값. **RAG는 환각을 줄이지 제거하지 않는다** — Part 3 Ch4가 명시한 retrieval–generation mismatch가 정확히 이 주장의 반례다. **같은 코스 안에서 어긋난다** |
| **LangChain 통계에 시점 없음** | `50K+ stars`가 언제 기준인지 없다. 라이브러리 통계는 시점 없이는 무의미하다 |
| **RAG 한계가 없다** | Part 3 Ch4의 한계 4종에 해당하는 내용이 전무하다. **RAG를 도입 근거만으로 소개하는 구성** |

## 링크

- **주 페이지** — [[Retrieval-augmented generation]] (구조와 한계는 여기)
- **앞** — [[AI DE Course - Part5 Embeddings and vector search]]
- **다음(깊이)** — [[AI DE Course - Part5 Hybrid search and reranking]]
- 더 깊은 판본: [[AI DE Course - Part3 Ch4 RAG and its limits]]
- 파이프라인 앞단: [[Unstructured data ingestion]]
- 도구: [[LangChain]]
- 운영: [[LLMOps]] · [[Context engineering]]
- 코스: [[AI Data Engineering (Fast Campus course)]]

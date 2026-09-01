---
type: source
title: AI DE Course - Part3 Ch4 GraphRAG variants and products
area: [data-engineering, programming]
aliases: [Part3 Ch4-3, Graph-RAG의 개념과 사례2, LazyGraphRAG, DRIFT Search]
tags: [data-engineering, course, fast-campus, graphrag, microsoft, aws, bedrock]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part3/04. Ch4. Graph-RAG.pdf (p34–49)"]
---

# AI DE Course - Part3 Ch4 GraphRAG variants and products

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch4의 세 번째 소단원.
원본(로컬): `raw/data-engineering/ai-de-course/part3/04. Ch4. Graph-RAG.pdf` **p34–49** (16p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⚠️ **타이틀 슬라이드에 번호가 "2. Graph-RAG의 개념과 사례2"로 적혀 있다.** 앞 소단원도 "2. …사례1"
> 이므로 **번호가 중복**된다(1 · 2 · 2). 3이어야 할 자리다.
>
> ⚠️ **목차 슬라이드의 04·05(RAG의 한계 · RAG의 진화)는 소단원 1의 목차를 복붙한 잔재로, 본문에
> 존재하지 않는다.** 실제 내용은 01~03뿐이다.

## 구성 (실제)

`01 GraphRAG 이후 · 02 GraphRAG 변형들 · 03 제품 사례들`

## 왜 후속 변형이 계속 나왔나 — 세 가지 운영 문제

> ⭐ **"GraphRAG의 후속 진화는 성능 욕심이 아니라 비용, 질문 유형, 도메인 적응 문제를 해결하려는
> 과정이다."**

1. **인덱싱 비용이 크다** — entity 추출, 관계 정리, community summary 생성까지 사전 작업이 많음
2. **질문 유형이 다르다** — global question에는 강하지만 **local question에는 과하거나 비효율적**
3. **도메인 적응이 어렵다** — 뉴스 문서용 prompt와 extraction 규칙이 다른 도메인에서 그대로 맞지 않음

**이 프레이밍이 이 소단원의 가장 좋은 부분이다.** 세 변형이 각각 이 세 문제에 1:1 대응한다.

논문 이후 확장 방향: 질문 유형별 검색 전략 분화 · domain-specific indexing 자동화 · global search 비용
절감 · dynamic community 선택 · graph 구축 비용과 품질의 trade-off 최적화 · **개발자 사용성을 높인
1.0 정리.**

## 변형 1 — Auto-Tuning (도메인 적응)

GraphRAG의 핵심 추출 프롬프트는 도메인에 민감하다. 기본 prompt가 특정 도메인에 최적화되어 있으면
**다른 도메인에서는 entity type과 relation type이 빈약하게 추출될 수 있다.**

**해결:** 샘플 문서를 보고 도메인을 식별하고, **persona와 few-shot prompt를 자동 생성**해
entity/relationship extraction과 summary generation을 더 도메인 친화적으로 만든다.

다이어그램: `Sample Text Units from Raw Input Text → Use LLM to Generate Persona, Domain, Roles` →
세 갈래(Entity/Relationship Extraction · Entity/Relationship Summarization · Community Reports)로
각각 프롬프트 생성.

> ⭐ **"GraphRAG의 품질은 그래프 질의 전에, 무엇을 entity와 relation으로 뽑아내느냐에서 이미 갈린다."**
>
> 이 문장이 좋다. [[Knowledge graph pipeline]] 2단계("초기 오염은 크게 확산된다")와 같은 이야기를
> LLM 추출 맥락에서 반복한다 — **앞단이 뒤를 결정한다.**

## 변형 2 — DRIFT Search (질문 유형 분기)

> **"모든 질문을 한 방식으로 처리하면 비효율적이다.
> Global Search는 넓게 보지만 비싸고, Local Search는 깊게 보지만 전역 맥락이 약할 수 있다."**

| | 적합한 질문 |
|---|---|
| **Global Search** | 코퍼스 전체의 주제·패턴·리스크처럼 전역 의미를 묻는 질문 |
| **Local Search** | 특정 개체·특정 사건·특정 문서 근처 사실처럼 국소 정보를 묻는 질문 |

**DRIFT (Dynamic Reasoning with Fine-grained Information Tree)** — 상위 community report를 먼저
사용해 넓은 초기 답과 **follow-up question**을 만들고, 그 다음 local search 방식으로 세부를 파고드는
구조.

> 슬라이드는 큰 트리 시각화 2장(A·B·C 레이블)을 보여주지만 **DRIFT의 실제 동작을 설명하지는 않는다.**
> 이미지 출처도 없다. 개념 한 문단이 전부다.

## 변형 3 — LazyGraphRAG (비용 구조 재설계)

**문제:** Full GraphRAG는 query 전에 많은 요약과 구조화를 미리 만들어야 하므로 **선행 인덱싱 비용이
높다.**

**해결:** 사전 요약을 크게 줄이고, **질의 시점에 더 많은 relevance test와 query refinement를 수행.**
즉 upfront indexing cost를 줄이고 질의 시점에 계산을 집중.

프로세스 퍼널: **Build Index**(개념 추출·그래프 최적화) → **Refine Query**(서브쿼리 식별·정제) →
**Match Query**(텍스트 청크 랭킹·평가) → **Map Answers**(관련 claim 추출·그룹화) →
**Reduce Answers**(LLM으로 최종 답변 생성).

> ⚠️ **"Microsoft는 자사 비교에서 LazyGraphRAG indexing cost가 vector RAG와 같고 full GraphRAG의
> 0.1% 수준이라고 설명하고, 또 일부 설정에서 global/local 질의 품질을 유지하거나 능가하면서 비용을
> 크게 낮췄다고 주장한다."**
>
> **강의가 "자사 비교"와 "주장"이라는 단어를 쓴다.** Part 1의 무비판적 수치 인용과 비교하면 태도가
> 낫다. 그래도 **0.1%는 벤치마크 조건 없이 인용하면 안 되는 숫자**다.

**결론 자체는 타당하다:** *"GraphRAG는 무조건 무거운 구조가 아니라 비용을 어떻게 배분할지에 따라
다시 설계될 수 있다."*

## 제품 사례

### AWS Bedrock Knowledge Bases GraphRAG

**AWS가 GraphRAG를 제품 기능으로 넣었다.** Bedrock Knowledge Bases가 문서로부터 entity·fact·
relationship을 자동 추출해 **[[Amazon Neptune|Neptune Analytics]]에 그래프와 벡터를 함께 저장**하고,
검색 시 **vector similarity search와 graph traversal을 결합**한다.

> **"GraphRAG가 더 이상 연구 데모가 아니라 managed service 형태로 운영 가능해졌다는 점.
> 실무에서는 GraphRAG를 직접 다 구현하기보다 관리형 기능으로 도입하는 흐름도 강해지고 있다."**

출처: `https://aws.amazon.com/ko/blogs/machine-learning/announcing-general-availability-of-amazon-bedrock-knowledge-bases-graphrag-with-amazon-neptune-analytics`

### AWS GraphRAG Toolkit (오픈소스)

비정형 데이터로부터 graph와 vector embeddings를 자동 구성하고, graph를 질의하는 question-answering
전략을 프레임워크 형태로 제공.

> **"GraphRAG가 이제 개념 연구가 아니라 개발자가 직접 조립하고 실험할 수 있는 구현 프레임워크가 됨.
> 실무형 GraphRAG는 논문 구현보다 도구화와 조립 가능성이 훨씬 중요해지고 있다."**

### 마지막 슬라이드 — Vector RAG vs Graph RAG 한 장 비교

AWS 자료 이미지. 질문: *"What are the sales prospects for Example Corp in the UK?"*

- **Vector RAG** — "Example Corp sells Widgets, partnered with AnyCompany Logistics"와
  "Huge Christmas demand for Widgets in UK"라는 **유사 정보(similar information)** 만 보고
  → **"Sales are Marvelous"**
- **Graph RAG** — 거기에 "AnyCompany Logistics cutting shipping times via Fictitious Canal"과
  "Fictitious Canal blocked, causing delays"라는 **연관 정보(related information)** 까지 따라가서
  → **"Actually, sales are likely to be negatively impacted by logistics issues"**

> **이 한 장이 Ch4 전체를 요약한다.** 유사도로는 닿지 않고 **관계를 따라가야만 닿는 사실**이 답을
> 뒤집는다. [[AI DE Course - Part3 Ch4 RAG and its limits]]의 한계 1번("검색 단위는 chunk, 질문
> 단위는 structure")이 구체적 시나리오로 나타난 것.

## 기존 페이지와의 대조

- **[[GraphRAG]]에 통합** / **[[Microsoft GraphRAG]]** entity에 변형 3종 기록
- **[[Amazon Neptune]]** — GraphRAG 제품화의 저장 계층으로 등장
- **[[LLMOps]]의 미해결 질문** — retrieval 품질 지표는 **여기서도 안 나온다.** LazyGraphRAG가 "품질을
  유지하거나 능가"한다는데 **무엇으로 쟀는지 밝히지 않는다.**

## 자료 품질

- ⚠️ **타이틀 번호 중복**("2. …사례2"), **목차 04·05가 본문에 없는 복붙 잔재**
- 이미지 5장 중 출처 표기는 AWS 블로그 URL 1건뿐. **DRIFT 트리 시각화 2장과 LazyGraphRAG 퍼널은 출처
  없음**
- **DRIFT는 이미지만 있고 설명이 없다** — 이 파트에서 가장 부실한 대목
- ⚠️ **벤더 수치 1건**(LazyGraphRAG "0.1%") — 다만 강의가 "자사 비교", "주장"이라고 명시한다

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[GraphRAG]] · [[Retrieval-augmented generation]] · [[Knowledge graph pipeline]]
- 도구: [[Microsoft GraphRAG]] · [[Amazon Neptune]] · [[Neo4j]]
- 앞: [[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]]
- 다음: [[AI DE Course - Part3 Ch5 Graph databases]]

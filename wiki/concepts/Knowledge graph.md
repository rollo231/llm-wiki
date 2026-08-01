---
type: concept
title: Knowledge graph
area: [data-engineering]
aliases: [지식그래프, 지식 그래프, KG, Knowledge Graph, 메타데이터 그래프, Metadata graph]
tags: [data-engineering, knowledge-graph, graph, metadata, lineage, search, recommendation]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part3 Ch2 Graph fundamentals]]", "[[AI DE Course - Part3 Ch2 Graph in practice]]"]
---

# Knowledge graph

**entity와 그들 사이의 사실 관계를 구조화한 그래프.** 사람·장소·조직·제품·작품·개념 같은 개체와,
그 사이의 사실을 명시적으로 표현한다. 형태상으로는 **heterogeneous [[Graph data model|그래프]]** 다.

> **"단순 키워드 저장이 아니라, 이것이 무엇이며 다른 것과 어떤 관계를 갖는가를 명시적으로 표현한 것."**

기본 단위는 사실(fact)이고, RDF로 쓰면 triple이 된다:

```
"서울은 대한민국의 수도다"
  subject:   서울
  predicate: 수도이다
  object:    대한민국
```

Google의 공식 도움말은 Knowledge Graph를 *people, places, things*에 대한 *billions of facts*를 담은
데이터베이스로 설명한다.

## 실서비스에서 — Google Search의 Knowledge Panel

사용자가 특정 entity를 검색했을 때 관련 사실 정보를 구조화해 보여주는 대표 사례.

> **중요한 건 화면의 박스가 아니라 그 박스를 가능하게 하는 데이터 모델이다.**
> 검색어를 단순 문자열로 처리하지 않고, **사람·장소·사물·조직 같은 entity와 그 관계를 기준으로
> 이해한다는 점.**

이미 대규모 검색 시스템에서 **factual information organization**과 **entity-centric retrieval**의
기반으로 쓰이는 실전 기술이다.

## ⭐ 데이터 엔지니어에게 — 메타데이터 그래프와 리니지

**DE 관점에서 가장 직관적인 그래프 활용처는 메타데이터 관리다.** 데이터 엔지니어링 환경 자체가
그래프에 매우 적합한 도메인이다.

노드로 둘 것: `Dataset` `Column` `ETL Job` `DataFlow` `Dashboard` `Chart` `Metric` `Owner` `Team`
`Tag`
엣지로 둘 것: `upstream` `downstream` `owns` `documents` `uses` `transforms`

그러면 단순 메타데이터 저장을 넘어 **영향도 분석과 탐색**이 가능해진다:

- 이 컬럼이 바뀌면 **어떤 대시보드가 깨지는가**
- 이 데이터셋은 **어떤 잡이 만들었는가**
- 이 리포트는 어떤 테이블과 어떤 팀에 연결되는가
- 이 모델 feature는 **어떤 원천 데이터에서 왔는가**

대표 도구: **[[DataHub]]**

### 왜 그래프여야 하나

> **"정답이 한 개 문서 안에 있지 않다. 여러 자산 사이 관계를 따라가야만 답할 수 있다."**

"이 대시보드는 어떤 데이터셋 쓰나요?", "이 컬럼은 어느 파이프라인에서 만들어졌나요?" — 이런 질문은
단순 검색이 아니라 **컨텍스트**를 요구한다.

메타데이터 그래프는 다섯 가지를 동시에 가능하게 한다:
탐색형 질의 · 연관 자산 추천 · 영향도 분석 · **변경 안전성 판단** · 지식 축적.

### 리니지가 문서에서 도구가 되는 지점

> **"lineage는 그래프로 모델링할 때 비로소 '정적 문서'가 아니라 탐색 가능한 운영 도구가 된다."**

lineage는 본질적으로 **경로 정보**다 — `source → transformation → model → dashboard`.
"이 테이블 수정하니까 대시보드 에러나요"가 lineage 질문이다.

→ [[Data catalog and semantic layer]]의 lineage 서술을 **그래프라는 구현 형태**로 구체화한 것.

## 추천과 검색

### 추천 — 다단계 연결과 cold-start

사용자–상품 직접 관계만 보는 게 아니라 `사용자–상품–카테고리`, `사용자–상품–다른 사용자–다른 상품`
같은 다단계 연결을 자연스럽게 탐색한다. 추천은 결국 사용자의 현재 행동과 과거 행동을 연결하고,
다른 사용자와의 유사성을 연결하고, 상품 속성 및 지식 정보를 연결하는 문제다.

**cold-start** — 사용자 로그가 적거나 신규 아이템이라 상호작용 기록이 부족한 상황. 이때 그래프
접근은 **단순 행동 이력 부족을 주변 관계 신호로 보완**하는 데 유리하다.

### 검색 — 문자열 매칭을 넘어

전통적 검색은 문서/상품 설명 텍스트에서 질의어와 일치하는 문자열을 찾는다. 그래프가 결합되면:

질의어가 **어떤 엔터티를 의미하는지** 파악 → 연관 엔터티와의 관계를 탐색 → 사용자 의도와 맥락을
보강 → 더 적절한 결과와 **설명**을 제시.

Knowledge Graph의 역할: 엔터티와 사실 관계를 구조화 · 의미 기반 검색 지원 · 지식 패널 생성 ·
질문 응답 정확도 향상 · **동의어와 표기 변형을 넘어 같은 대상을 연결.**

## 언제 그래프를 고려할까

**그래프가 잘 맞는 문제의 공통점:**

- **엔터티보다 관계가 더 중요** — 사용자-상품, 테이블-잡, 대시보드-데이터셋, 계정-기기-결제수단
- **질문이 1-hop에서 끝나지 않음**
- **재귀적 탐색 또는 패턴 탐색이 필요** — 순환 관계, 공통 연결점, n-hop 이웃, 경로 탐색
- **스키마가 고정되어 있더라도 연결 구조가 계속 진화** — 새 이벤트 타입, 새 관계, 새 자산 유형 추가

**굳이 쓰지 않아도 되는 문제:** 단순 집계와 리포팅 중심 · 행 단위 CRUD 위주 · 관계보다 속성 필터가
핵심 · 한두 번의 정형 join이면 충분한 경우.

**설계 전 다섯 질문:**

1. 이 도메인의 **핵심 객체**는 무엇인가 (User, Product, Query, Dataset, Job, Dashboard)
2. 객체 사이 관계가 **방향성**을 가지는가 (생성함, 참조함, 사용함, 구매함)
3. **관계 자체에 속성**이 붙는가 (클릭 횟수, confidence, 생성 시각, rank score)
4. 업무 질문이 **2-hop, 3-hop, n-hop 탐색**으로 바뀌는가
5. 스키마보다 **연결 구조의 해석**이 더 중요한가

## 관련 페이지

- [[Graph data model]] — 표현 수단
- [[Ontology]] — 지식그래프의 스키마·규칙 계층
- [[Knowledge graph pipeline]] — **원천 데이터에서 지식그래프를 실제로 만들어내는 파이프라인**
- [[Graph database]] — 저장·질의 엔진
- [[GraphRAG]] — 지식그래프를 retrieval에 쓰는 것
- [[Data catalog and semantic layer]] — lineage·거버넌스의 상위 맥락
- [[DataHub]] — 메타데이터 그래프의 대표 구현
- [[Data semantics]] — 왜 이 계층이 필요한가

## 출처

- [[AI DE Course - Part3 Ch2 Graph fundamentals]]
- [[AI DE Course - Part3 Ch2 Graph in practice]]

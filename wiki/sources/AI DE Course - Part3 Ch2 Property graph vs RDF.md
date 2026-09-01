---
type: source
title: AI DE Course - Part3 Ch2 Property graph vs RDF
area: [data-engineering]
aliases: [Part3 Ch2-2, Graph에 대해 이해하기2, Property Graph와 RDF의 차이]
tags: [data-engineering, course, fast-campus, graph, rdf, property-graph, cypher, sparql]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part3/02. Ch2. Graph에 대한 이해.pdf (p21–35)"]
---

# AI DE Course - Part3 Ch2 Property graph vs RDF

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch2의 소단원 **2**
"Graph에 대해 이해하기2". 원본(로컬): `raw/data-engineering/ai-de-course/part3/02. Ch2. Graph에 대한 이해.pdf` **p21–35** (15p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

## 이 소단원의 가치

**"그래프"라는 한 단어가 두 개의 다른 모델을 가리킨다**는 것을 분명히 하고, 선택 기준을 준다.
Part 3에서 실무 결정에 가장 직접 쓰이는 대목 중 하나다.

구성: `01 Graph 모델의 설계 방향 · 02 Property Graph · 03 RDF · 04 Property Graph와 RDF의 차이 ·
05 Property Graph vs RDF 판단`

## 두 모델

- **Property Graph** — 개체를 node로, 연결을 relationship으로 표현하고 **node와 relationship 모두에
  property를 직접 부여**하는 그래프 모델
- **RDF** — 모든 정보를 **subject–predicate–object 형태의 triple**로 표현하는 그래프 모델

> 이 선택이 **모델링 단위 · 스키마 표현 방식 · 질의 방식 · 추론 가능성 · 도구 생태계 · 성능 특성까지
> 전부 연결**된다는 게 01절의 요지다.

### 같은 사실을 다르게 본다

```
Property Graph 사고            RDF 사고
사람이라는 노드가 있고          사람A가 영화B에 출연했다
영화라는 노드가 있고            사람A의 이름은 무엇이다
ACTED_IN 관계가 있으며          영화B의 제목은 무엇이다
그 관계에 역할(role) 속성이 붙는다  → 각 사실을 triple 단위로 분해
```

## Property Graph — 질의는 pattern matching

Property Graph 질의의 핵심은 **pattern matching**. 어떤 연결 모양을 찾고 싶은가를 선언적으로 표현.

- **패턴 매칭** — `(노드A)-[관계]→(노드B)` 형태로 시각적으로 묘사
- **경로 탐색(Pathfinding)** — 노드 사이 경로를 찾거나 특정 Hop만큼 떨어진 노드를 탐색
- **속성 필터링** — 노드나 엣지의 속성을 조건으로

예: "A와 친구인 사람 중, 서울에 사는 사람의 친구 목록", "내가 구매한 상품과 비슷한 항목을 구매한
사용자의 또 다른 추천 상품은?"

## RDF가 단순한 triple 저장이 아닌 이유

강의가 네 가지를 든다:

| | 내용 |
|---|---|
| **Semantic Connectivity** | 고유 식별자(**URI**)로 자원을 정의하고 연결. 단순 문자열 저장과 달리 **'무엇'에 대한 '어떤 정보'인지를 기계가 문맥적으로 안다** |
| **Graph Model** | 트리플이 개별적으로 존재하지 않고 서로 연결되어 거대한 그래프 구조를 형성. **분산된 데이터를 하나의 통합 지식 베이스로 연결하는 데 최적** |
| **Reasoning & Interoperability** | RDFS·OWL과 결합해 스키마와 논리 규칙을 정의. **새로운 사실을 추론**하고 서로 다른 도메인 데이터를 통합 |
| **Standardized Representation** | **W3C 표준.** 사람과 기계 모두 이해할 수 있는 방식으로 교환 |

## 네 축의 비교

| | Property Graph | RDF |
|---|---|---|
| 기본 단위 | node · relationship · property | **triple** |
| 스키마 | Schema-less / Schema-flexible. 넣을 때 엄격한 정의 불필요, 속성 동적 추가 가능 | **RDFS·OWL로 클래스·관계·제약을 엄격하게 정의** |
| 메타데이터 | 노드/엣지 속성(K-V) 안에 저장 — **데이터와 메타데이터가 함께 위치** | 데이터 자체를 기술하는 트리플로 다룸. **SHACL**로 구조 정의·검증 |
| 질의 언어 | **Cypher** 계열 — 그래프 패턴을 시각적으로 기술 | **SPARQL** — triple pattern 조합 |

Cypher vs SPARQL 코드 비교 이미지가 나온다(Johan의 친구의 친구 중 서핑이 취미인 사람 찾기).

## ⭐ 판단 6문항

| 질문 | 방향 |
|---|---|
| 내 문제의 핵심은 **경로 탐색**인가 | Property Graph 쪽이 더 자연스러울 가능성이 큼 |
| 데이터 출처가 매우 다양하고 **의미 표준화**가 핵심인가 | RDF 쪽을 우선 검토 |
| **데이터와 스키마를 같은 형식**으로 다루고 싶은가 | RDF의 장점이 커짐 |
| **관계 자체에 속성을 많이 붙이고** 실용적으로 탐색하는가 | Property Graph가 더 직관적 |
| 추론·ontology·semantic interoperability가 필요한가 | RDF/RDFS/OWL 방향이 적합 |
| 운영팀·개발팀이 빠르게 모델링하고 질의해야 하는가 | **Property Graph의 학습 곡선이 보통 더 완만** |

**PG가 잘 맞는 곳:** 추천, fraud, lineage, impact analysis, dependency graph. 도메인 엔터티 구조가
분명(User·Product·Order·Dataset·Job·Dashboard)하고, 관계 자체에 속성이 많이 붙고(클릭 시각·구매
수량·confidence·rank), 개발자와 분석가가 빠르게 모델링해야 할 때.

**RDF가 잘 맞는 곳:** 데이터가 매우 heterogeneous해 테이블화가 어렵고, 출처마다 구조와 용어가 다르고,
데이터와 메타데이터를 같은 형식으로 다루고 싶고, 자동 추론이 필요하고, ontology와 표준 vocabulary로
의미를 공유하고 싶을 때. **의료 지식, 학술 지식, 공공 데이터 통합.**

## 기존 페이지와의 대조

- **[[Graph data model]]에 통합** — 이 소단원 내용이 그 concept의 후반부다.
- **Ch3과 겹침** — RDFS·OWL·SHACL은 여기서 언급만 되고 [[AI DE Course - Part3 Ch3 Ontology basics]]
  에서 본격 설명된다. **두 챕터가 같은 스택을 두 번 다룬다.**
- **Ch5와 겹침** — 질의 언어(Cypher/Gremlin/SPARQL)는 Ch5에서 다시 나온다.

## 자료 품질

- Property Graph 다이어그램에 출처 URL 표기 있음(dataversity.net, 2025/09).
- RDF triple 다이어그램·Cypher/SPARQL 비교표는 출처 표기 없음.
- **PG 쪽 서술이 RDF 쪽보다 얕다** — RDF는 네 가지 근거를 대며 설명하는데 PG는 요소 나열 수준.
  균형이 RDF로 기울어 있다.
- 출처 없는 수치 없음.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Graph data model]] · [[Ontology]] · [[Graph database]] · [[Knowledge graph]]
- 앞: [[AI DE Course - Part3 Ch2 Graph fundamentals]]
- 다음: [[AI DE Course - Part3 Ch2 Graph in practice]]

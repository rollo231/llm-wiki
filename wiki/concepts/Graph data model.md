---
type: concept
title: Graph data model
area: [data-engineering]
aliases: [그래프 데이터 모델, Graph, Property Graph, RDF, 프로퍼티 그래프, 트리플, Triple, Cypher, SPARQL]
tags: [data-engineering, graph, rdf, property-graph, cypher, sparql, data-modeling]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part3 Ch2 Graph fundamentals]]", "[[AI DE Course - Part3 Ch2 Property graph vs RDF]]"]
---

# Graph data model

**관계를 1급 데이터로 보는 데이터 모델.** 개체 자체보다 개체 사이의 연결이 더 중요할 때 쓴다.

> **"무엇이 있는가" → "무엇과 어떻게 연결되는가."**
> 속성 중심 데이터 이해에서 **관계 중심 데이터 이해**로.

## 구성 요소

| | 정의 | 예 |
|---|---|---|
| **Node** | 개체를 표현하는 기본 단위 | 사람, 상품, 카테고리, 검색어, 테이블, 컬럼, DAG, 대시보드, ML Feature, 모델 버전 — **모든 실체가 node가 될 수 있다** |
| **Edge (Relationship)** | 두 개체 사이 연결 | `PURCHASED`, `VIEWED`, `BELONGS_TO`, `DEPENDS_ON`, `GENERATED_BY`, `OWNED_BY` |
| **Property** | 노드와 관계에 붙는 key-value 속성 | 상품 가격, 생성 시각, **관계 신뢰도**, 클릭 횟수, 유사도 점수 |
| **Label / Type** | 노드나 관계의 종류 분류 | `:User`, `:Product`, `:Dataset`, `:Dashboard` / `CLICKED`, `PRODUCED`, `DOWNSTREAM_OF` |

## 그래프를 읽는 단위

- **Path** — 노드와 관계가 이어져 만들어지는 연결 경로.
  예) `Dashboard → Chart → Dataset → ETL Job → Source Table`
- **Hop** — 한 노드에서 다음 노드로 이동하는 한 단계. 1-hop은 직접 연결, 2-hop은 한 단계 더,
  3-hop 이상은 다단계 연결.
- **Pattern** — 그래프에서 찾고 싶은 연결 구조 자체.
  예) "특정 사용자가 본 상품과 같은 카테고리의 인기 상품", "이 지표를 깨뜨릴 수 있는 upstream asset
  조합", "같은 브랜드를 반복 조회한 사용자 패턴"

**질의의 사고 단위가 다르다.** SQL이 "어떤 테이블을 JOIN할까"라면 그래프는 **"어떤 관계를 몇 hop
따라갈까"** 다.

## 그래프의 종류

| 축 | 종류 | 특징 |
|---|---|---|
| 방향 | **Directed** | 관계 방향이 중요. DAG, "A가 B를 참조/생성/호출함". **파이프라인 lineage·dependency·ownership은 대부분 방향성이 중요하다** |
| | **Undirected** | 연결 사실 자체가 중요. 공동 구매, 공동 저자, 네트워크 연결, 유사 그룹 |
| 가중치 | **Weighted** | 관계의 강도·빈도·중요도를 수치로. 클릭 횟수, 공구매 빈도, similarity/confidence score |
| 타입 다양성 | **Homogeneous** | 노드·관계 종류가 단순. 사용자 노드와 친구 관계만 있는 소셜 구조 |
| | **Heterogeneous** | 여러 종류의 노드와 관계가 함께. **현실의 서비스 데이터는 대부분 이쪽** — User/Product/Query/Brand/Category/Seller/Review × VIEW/CLICK/BUY/BELONGS_TO/WRITES/SEARCHES |

## ⭐ 두 가지 그래프 모델 — Property Graph vs RDF

같은 "그래프"라는 말이 **두 개의 다른 모델**을 가리킨다. 이 구분이 도구·질의 언어·확장 방식까지
전부 결정한다.

| | **Property Graph** | **RDF** |
|---|---|---|
| 기본 단위 | node · relationship · property | **triple** (subject–predicate–object) |
| 표현 방식 | 개체를 node로, 연결을 relationship으로, **둘 다에 property를 직접 부여** | 모든 정보를 주어–서술어–목적어의 사실 단위로 분해 |
| 스키마 | Schema-less / Schema-flexible. 넣을 때 엄격한 정의 불필요, 속성 동적 추가 가능 | **RDFS·OWL로 클래스·관계·제약을 엄격하게 정의** |
| 메타데이터 | 노드/엣지의 속성(K-V) 안에 저장 — **데이터와 메타데이터가 함께 위치** | 데이터 자체를 기술하는 트리플로 다룸. **SHACL**로 구조 정의·검증 |
| 질의 언어 | **Cypher** 계열 — 그래프 패턴을 시각적으로 기술, 경로/이웃 탐색이 자연스러움 | **SPARQL** — triple pattern을 조합해 질의 |
| 식별자 | 내부 ID/속성 | **URI** — 자원을 전역 식별하고 연결 |

같은 사실을 두 모델이 다르게 본다:

```
Property Graph 사고          RDF 사고
사람 노드가 있고             사람A가 영화B에 출연했다
영화 노드가 있고             사람A의 이름은 무엇이다
ACTED_IN 관계가 있으며        영화B의 제목은 무엇이다
그 관계에 role 속성이 붙는다   → 각 사실을 triple 단위로 분해
```

### RDF가 단순한 triple 저장이 아닌 이유

- **Semantic Connectivity** — URI로 자원을 정의·연결. 문자열 저장과 달리 **'무엇'에 대한 '어떤
  정보'인지를 기계가 문맥적으로 안다.**
- **Graph Model** — 트리플이 개별로 존재하지 않고 서로 연결되어 거대한 그래프를 형성.
  분산된 데이터를 **하나의 통합 지식 베이스**로 연결하는 데 최적.
- **Reasoning & Interoperability** — RDFS·OWL과 결합해 스키마와 논리 규칙을 정의하고 **새로운 사실을
  추론**. 서로 다른 도메인 데이터를 통합.
- **Standardized Representation** — W3C 표준. 직렬화는 RDF/XML · **Turtle** · N-Triples · N-Quads.

### 어느 쪽을 고를까 — 판단 6문항

| 질문 | 방향 |
|---|---|
| 내 문제의 핵심은 **경로 탐색**인가 | → Property Graph |
| 데이터 출처가 매우 다양하고 **의미 표준화**가 핵심인가 | → RDF |
| **데이터와 스키마를 같은 형식**으로 다루고 싶은가 | → RDF |
| **관계 자체에 속성을 많이 붙이고** 실용적으로 탐색하는가 | → Property Graph |
| **추론·ontology·semantic interoperability**가 필요한가 | → RDF/RDFS/OWL |
| 운영팀·개발팀이 **빠르게 모델링하고 질의**해야 하는가 | → Property Graph (학습 곡선이 더 완만) |

**Property Graph가 특히 잘 맞는 곳** — 추천, fraud, lineage, impact analysis, dependency graph.
도메인 엔터티 구조가 비교적 분명하고(User·Product·Order·Dataset·Job·Dashboard), 관계 자체에 속성이
많이 붙고(클릭 시각·구매 수량·confidence·rank), 개발자와 분석가가 빠르게 모델링해야 할 때.

**RDF가 특히 잘 맞는 곳** — 이질적 데이터 통합과 의미 표현이 핵심일 때. 데이터가 매우
heterogeneous해서 테이블화가 어렵고, 출처마다 구조와 용어가 다르고, 자동 추론이 필요하고, ontology와
표준 vocabulary로 의미를 공유하고 싶을 때. **의료 지식, 학술 지식, 공공 데이터 통합.**

## 관련 페이지

- [[Graph database]] — 이 모델을 실제로 저장·질의하는 엔진
- [[Knowledge graph]] — 이 모델로 entity와 fact를 구조화한 것
- [[Ontology]] — RDF 쪽의 스키마·규칙 계층(RDFS·OWL·SHACL)
- [[Schema-centric data modeling]] — 조인 폭발이라는 출발점
- [[NoSQL]] — 4타입 중 Graph의 자리
- [[Data semantics]] — 그래프가 봉사하는 상위 목적

## 출처

- [[AI DE Course - Part3 Ch2 Graph fundamentals]]
- [[AI DE Course - Part3 Ch2 Property graph vs RDF]]

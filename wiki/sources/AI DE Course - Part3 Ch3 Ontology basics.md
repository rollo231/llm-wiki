---
type: source
title: AI DE Course - Part3 Ch3 Ontology basics
area: [data-engineering]
aliases: [Part3 Ch3-1, 온톨로지 개요 및 기본 아키텍처]
tags: [data-engineering, course, fast-campus, ontology, rdf, rdfs, owl, semantics]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part3/03. Ch3. 온톨로지 및 지식 그래프.pdf (p1–15)"]
---

# AI DE Course - Part3 Ch3 Ontology basics

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch3 "온톨로지 및 지식 그래프"의 소단원
**1** "온톨로지 개요 및 기본 아키텍처".
원본(로컬): `raw/data-engineering/ai-de-course/part3/03. Ch3. 온톨로지 및 지식 그래프.pdf` **p1–15** (65p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

## 구성

`01 온톨로지 · 02 온톨로지의 핵심 구성요소 · 03 온톨로지와 RDF, RDFS, OWL · 04 온톨로지의 존재 여부 판단`

## 정의

> **온톨로지: {철학} 존재론. 특정 도메인 내의 개념, 클래스, 속성, 그리고 이들 간의 관계를 컴퓨터가
> 이해하고 처리할 수 있는 형태로 명확하게 정의한 지식 체계.**
>
> **"단순한 테이블 스키마가 '어떤 컬럼이 있는가'를 정의한다면, 온톨로지는 '이 데이터가 현실 세계에서
> 무엇을 의미하는가'까지 표현한다."**
>
> **"핵심은 데이터 값을 저장하는 것이 아니라, 데이터의 의미와 관계를 기계가 이해할 수 있게 만드는 것."**

### 필요성

현실의 데이터는 여러 시스템에 흩어져 있고 **같은 대상을 서로 다른 이름과 구조로 표현하는 경우가
대다수**다. 단순 스키마만으로는 "값이 같은 개념인가?", "어떤 관계를 맺는가?", "어떤 제약과 규칙을
따라야 하는가?"를 설명하기 어렵다.

**온톨로지는 개념을 통일하고 관계를 명시하며 서로 다른 데이터 소스를 의미 중심으로 통합한다.**

### 스키마와의 차이

`orders` 테이블에 `order_id`, `user_id`, `product_id`는 표현 가능하다. 하지만 **주문이 비즈니스적으로
무엇인지 · 사용자와 상품이 어떤 의미 관계를 가지는지 · 다른 시스템의 개념과 어떻게 매핑되는지는 설명
불가능**하다.

온톨로지는 `Order`라는 개념, `User`라는 개념, "주문은 사용자가 생성한다", "주문은 상품을 포함한다"
같은 **의미적 관계**를 모델링한다.

## 핵심 구성 요소

클래스(Class) · 인스턴스(Instance) · 속성(Property) · 관계(Relation) · **제약(Constraint)**.
제약의 예: "모든 주문은 반드시 한 명의 구매자와 연결되어야 한다".

## RDF · RDFS · OWL

> **"온톨로지가 '무엇을 정의할 것인가'라면, RDF는 '그 정의와 데이터를 어떻게 표현할 것인지'다."**

W3C 시멘틱 웹 스택 다이어그램이 반복해서 나온다:
`Ontologies: OWL / Rules: RIF·SWRL / Validation: SHACL` 위층, `Taxonomies: RDFS`,
`Data Interchange: RDF`, `Data Representations: RDF/XML · Turtle · N-Triples · N-Quads`,
그리고 왼쪽에 `Querying: SPARQL`.

### RDFS 5요소

`rdfs:Class` · `rdfs:subClassOf` · `rdf:Property` · `rdfs:domain` · `rdfs:range`.

예시가 명확하다:

```
Person은 클래스다 / Employee는 클래스다 / Employee는 Person의 하위 클래스다
Organization은 클래스다 / worksAt는 속성이다
worksAt의 domain은 Person이다 / worksAt의 range는 Organization이다
──────
실제 데이터:  Jeff - type - Employee
             Jeff - worksAt - Amazon
```

### OWL

RDFS보다 강한 표현력. 표현 가능한 규칙: 두 클래스는 동일하다 · 서로 배타적이다 · 어떤 속성은
역관계다 · 대칭적이다 · **추이적이다** · 어떤 클래스는 특정 조건을 만족하는 개체들의 집합이다 ·
어떤 속성은 반드시 하나만 가져야 한다.

## ⭐ "OWL을 꼭 사용해야 할까?" — 이 챕터에서 가장 좋은 절

> **"현실적으로는 — RDF는 꽤 자주 유용하다. RDFS도 메타모델링에 꽤 유용하다.
> OWL은 필요한 경우가 제한적이다."**

OWL이 필요한 경우는 **규칙 기반 의미 추론이 실제 가치가 있을 때**:
동일 개체 판별 규칙이 중요할 때 · 상속/배타 규칙이 실제 품질 검증에 쓰일 때 · 정책/권한/도메인 규칙을
논리적으로 검증해야 할 때 · **Graph RAG에서 개체 타입/관계 추론이 중요할 때.**

> **"반대로 단순 메타데이터 수집, lineage 시각화, 태그 검색 정도면 OWL까지 가는 순간 오히려 과설계가
> 된다."**

**이 절제가 이 챕터의 신뢰도를 만든다.** 시멘틱 웹 스택을 다 소개해놓고 "대부분은 여기까지 안 가도
된다"고 말하는 건 흔치 않다. Part 2 Ch5의 "Feature Store가 불필요한 경우"와 같은 태도다.

## 온톨로지가 있는가 — 판단 3문항

1. **이 시스템에는 개념 정의서가 있는가?** 단순 테이블명이 아니라 — `User`란 무엇인가,
   `Customer`와 `Subscriber`는 어떻게 다른가, `Product`와 `Content`는 어떤 관계인가
2. **관계가 단순 컬럼 연결이 아니라 의미로 정의되어 있는가?** `Owns`, `subscribesTo`, `Fulfills`,
   `derivedFrom` — 이런 관계 이름과 의미가 명확한지
3. **기계가 읽고 검증하거나 활용할 수 있는가?** 문서에만 있는 것보다 시스템이 읽어 검증·매핑·추론·
   검색 확장·의미 기반 질의를 할 수 있으면 온톨로지 가능성

**결론적으로 온톨로지란:** 도메인 개념 체계가 있고 · 개념 간 관계가 정의되어 있고 · 속성과 제약이
명시되어 있고 · 사람과 시스템이 그 정의를 공유하며 · **실제 검증/검색/추론/통합의 기준으로 쓰이는 경우.**

> 이 3문항이 실무에서 바로 쓸 수 있는 진단 도구다. "우리도 온톨로지 해야 하나"에 대한 답이 아니라
> **"우리에게 이미 있나"** 를 묻는다는 점이 좋다.

## 기존 페이지와의 대조

- **새 concept:** [[Ontology]] — 이 소단원 + Ch3-2 + Ch3-4를 통합했다.
- **[[Data semantics]]의 스펙트럼 오른쪽 끝**에 해당한다.
- **Ch2-2와 중복** — RDF·RDFS·OWL·SHACL은 [[AI DE Course - Part3 Ch2 Property graph vs RDF]]에서
  이미 언급됐다. 여기가 본격 설명이지만 **두 챕터가 같은 스택을 두 번 다루는 구조**다.

## 자료 품질

- ⚠️ **p5와 p6이 완전히 동일**(온톨로지와 일반 스키마의 차이), **p12와 p13도 완전히 동일**
  (OWL을 꼭 사용해야 할까). 15페이지 중 2페이지가 순수 중복이다.
- 손그림 마인드맵 이미지(OD 중심)가 4장 반복 사용되는데 **출처 표기 없음**이고 슬라이드 내용과의
  관련성도 약하다.
- 시멘틱 웹 스택 다이어그램도 출처 표기 없음(W3C 표준 도식으로 보인다).
- 출처 없는 수치 없음.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Ontology]] · [[Data semantics]] · [[Knowledge graph]] · [[Graph data model]]
- 앞: [[AI DE Course - Part3 Ch2 Graph and AI]]
- 다음: [[AI DE Course - Part3 Ch3 Ontology design principles]]

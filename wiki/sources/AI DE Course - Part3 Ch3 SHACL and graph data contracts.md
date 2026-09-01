---
type: source
title: AI DE Course - Part3 Ch3 SHACL and graph data contracts
area: [data-engineering]
aliases: [Part3 Ch3-4, SHACL을 이용한 그래프 검증과 데이터 계약, Turtle]
tags: [data-engineering, course, fast-campus, shacl, rdf, turtle, data-contract, validation]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part3/03. Ch3. 온톨로지 및 지식 그래프.pdf (p46–65)"]
---

# AI DE Course - Part3 Ch3 SHACL and graph data contracts

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch3의 소단원 **4**
"SHACL을 이용한 그래프 검증과 데이터 계약".
원본(로컬): `raw/data-engineering/ai-de-course/part3/03. Ch3. 온톨로지 및 지식 그래프.pdf` **p46–65** (20p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

## 이 소단원의 자리

> **"이번 파트의 질문은 다르다. 만들어진 그래프가 정말 우리가 기대한 구조와 의미를 만족하는가.
> 즉 생성이 아니라 검증의 문제."**

앞 소단원들이 "원천 데이터를 어떻게 수집하고 온톨로지와 매핑해 그래프로 만드는가"였다면, 여기는
**만들어진 결과를 검사하는 별도 축**이다.

구성: `01 SHACL을 통한 검증 · 02 SHACL의 핵심 구조 · 03 Turtle · 04 간단한 SHACL 예시`

## ⭐ SHACL = 그래프용 테스트 코드

> **"SHACL은 RDF graph를 어떤 조건 집합에 대해 검증하는 언어.
> 이 조건 집합은 또 다른 RDF graph 형태로 표현된다 — 즉 규칙도 그래프, 검사 대상도 그래프."**
>
> **"⇒ SHACL은 그래프용 테스트 코드에 가깝다."**

| 용어 | 뜻 |
|---|---|
| **data graph** | 실제로 검증할 대상 데이터 그래프 |
| **shapes graph** | 그 데이터를 검사하는 규칙 그래프 |

**관계형과의 대응이 명확하다** — 관계형에서 `NOT NULL`, datatype check, referential integrity,
row-level quality rule로 하던 검사를 그래프에서 수행한다: 노드가 어떤 타입인지 · 필수 속성이 있는지 ·
관계가 몇 개 이상인지 · 값 타입이 맞는지 · **특정 경로가 존재하는지.**

> **"실무적으로는 이 규칙 묶음을 그래프용 데이터 계약처럼 운영할 수 있다."**
>
> ⭐ **[[Data SLA and observability]]의 계약·품질 게이트 개념이 그래프로 옮겨온 것이다.**
> Part 1이 "데이터 계약"을 말할 때는 테이블 스키마와 신선도·완전성·정확성이었는데, 여기서 **그래프
> 형태의 계약**이라는 구체적 형태가 처음 등장한다. 강의는 두 파트를 잇지 않는다 — **위키가 붙인 연결.**

## 핵심 구조 4요소

| | 뜻 | 예 |
|---|---|---|
| **Shape** | 검증 규칙 묶음 | |
| **Target** | 어떤 노드에 이 규칙을 적용할지 정하는 기준 | `sh:targetClass ex:Customer` |
| **Node Shape** | 노드 자체에 대한 규칙 | Customer 노드는 Customer 타입이어야 함 |
| **Property Shape** | 노드의 특정 속성이나 경로에 대한 규칙 | Customer의 email은 문자열 / Order의 containsProduct는 최소 1개 |

## Turtle

**"RDF를 사람이 읽기 쉽게 적는 문법."** RDF graph는 triple의 집합이고, Turtle은 이 triple을 짧고 읽기
쉽게 적도록 돕는다.

| 기호 | 뜻 |
|---|---|
| `a` | `rdf:type`의 축약형 ("이것은 무슨 타입이다") |
| `@prefix` | 접두사 선언 |
| `;` | 같은 주어(subject)를 반복할 때 |
| `,` | 같은 주어/술어에서 object를 여러 개 적을 때 |
| `.` | 한 triple 문장의 끝 |
| `[...]` | 이름 없는 임시 노드(blank node) |

세 접두사의 역할도 나눠 설명한다 — `ex:`는 예시용 네임스페이스(`ex:Customer`는 개념적으로
`http://example.com/Customer`), `sh:`는 SHACL 표준 용어(`sh:NodeShape` `sh:targetClass`
`sh:property` `sh:path` `sh:minCount`), `xsd:`는 데이터 타입(`xsd:string` `xsd:dateTime`
`xsd:integer` `xsd:boolean`).

## 예시 — 고객과 주문

```turtle
@prefix ex:  <http://example.com/> .
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:CustomerShape
    a sh:NodeShape ;
    sh:targetClass ex:Customer ;
    sh:property [ sh:path ex:customerId ; sh:minCount 1 ; sh:maxCount 1 ; ] ;
    sh:property [ sh:path ex:email ; sh:datatype xsd:string ; sh:minCount 1 ; ] .

ex:OrderShape
    a sh:NodeShape ;
    sh:targetClass ex:Order ;
    sh:property [ sh:path ex:orderId ; sh:minCount 1 ; ] ;
    sh:property [ sh:path ex:createdAt ; sh:datatype xsd:dateTime ; ] ;
    sh:property [ sh:path ex:orderedBy ; sh:class ex:Customer ; sh:minCount 1 ; ] .
```

말로 풀면 — 고객은 `customerId`가 반드시 하나만 있어야 하고 `email`이 반드시 있고 문자열이어야 한다.
주문은 `orderId`가 반드시 있고, `createdAt`이 있다면 날짜/시간 형식이어야 하고, `orderedBy`가 반드시
있으며 **Customer 타입 노드를 가리켜야** 한다.

> **"즉 고객 노드는 최소 이 정도 정보는 갖춰야 고객으로 인정, 주문 노드는 최소 이 정도는 갖춰야
> 주문으로 인정 — 이라고 정해둔 것."**

**통과하는 데이터:**

```turtle
ex:customer_1001 a ex:Customer ;
    ex:customerId "1001" ;
    ex:email "alice@example.com" .

ex:order_2001 a ex:Order ;
    ex:orderId "2001" ;
    ex:createdAt "2026-04-09T10:00:00"^^xsd:dateTime ;
    ex:orderedBy ex:customer_1001 .
```

**위반하는 데이터** — `orderedBy`가 없어 `sh:minCount 1`을 어긴다:

```turtle
ex:order_9999 a ex:Order ;
    ex:orderId "9999" .
```

## 기존 페이지와의 대조

- **[[Ontology]]에 통합** — 이 소단원이 그 concept의 "SHACL — 그래프용 데이터 계약" 절이다.
- **[[Data SLA and observability]]와 연결** — 데이터 계약의 그래프 버전.
- **[[Knowledge graph pipeline]] 7단계**의 구현 수단.

## 자료 품질

⚠️ **Part 3에서 자료 낭비가 가장 심한 소단원이다. 20페이지 중 실질 내용은 절반 정도.**

- **접두사 설명 슬라이드가 `xsd:` 하나로 3번 연속 반복**(p58·p59·p60, 완전 동일)
- **CustomerShape 슬라이드가 2번 반복**(p61·p62, 본문은 제목 한 줄뿐)
- 오른쪽에 같은 Turtle 코드 블록이 **p53부터 p63까지 11장 내내 붙어 있다** — 설명이 왼쪽에서 조금씩
  바뀌는데 코드는 그대로다
- p61·p63은 왼쪽에 `CustomerShape`, `OrderShape`라는 **단어 하나만** 있다

내용 자체(SHACL을 데이터 계약으로 보는 관점, Turtle 최소 문법, 통과/위반 예시)는 좋은데 **전달이
느슨하다.**

- 출처 없는 수치 없음. 인용 이미지 없음(코드 블록만).

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Ontology]] · [[Knowledge graph pipeline]] · [[Data SLA and observability]] ·
  [[Graph data model]]
- 앞: [[AI DE Course - Part3 Ch3 Knowledge graph pipeline]]
- 다음: [[AI DE Course - Part3 Ch4 RAG and its limits]]

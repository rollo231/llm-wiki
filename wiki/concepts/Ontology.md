---
type: concept
title: Ontology
area: [data-engineering]
aliases: [온톨로지, RDFS, OWL, SHACL, 온톨로지 설계, Web Ontology Language, Shapes Constraint Language]
tags: [data-engineering, ontology, rdf, rdfs, owl, shacl, semantics, data-contract]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part3 Ch3 Ontology basics]]", "[[AI DE Course - Part3 Ch3 Ontology design principles]]", "[[AI DE Course - Part3 Ch3 SHACL and graph data contracts]]"]
---

# Ontology

**특정 도메인 안의 개념·클래스·속성, 그리고 이들 간의 관계를 컴퓨터가 이해하고 처리할 수 있는
형태로 명확하게 정의한 지식 체계.** 어원은 철학의 존재론.

> **"핵심은 데이터 값을 저장하는 것이 아니라, 데이터의 의미와 관계를 기계가 이해할 수 있게 만드는 것."**

[[Data semantics]] 스펙트럼의 오른쪽 끝이고, [[Knowledge graph]]의 스키마·규칙 계층이다.

## 스키마와 무엇이 다른가

단순 테이블 스키마가 **어떤 컬럼이 있는가**를 정의한다면, 온톨로지는 **이 데이터가 현실 세계에서
무엇을 의미하는가**까지 표현한다.

`orders` 테이블은 `order_id`, `user_id`, `product_id`를 표현할 수 있다. 하지만 주문이 비즈니스적으로
무엇인지, 사용자와 상품이 어떤 의미 관계를 가지는지, **다른 시스템의 개념과 어떻게 매핑되는지**는
설명하지 못한다. 온톨로지는 `Order`라는 개념, `User`라는 개념, "주문은 사용자가 생성한다", "주문은
상품을 포함한다" 같은 **의미적 관계**를 모델링한다.

## 핵심 구성 요소

| | 정의 | 예 |
|---|---|---|
| **클래스(Class)** | 개념의 유형 | 사람, 회사, 주문, 상품 |
| **인스턴스(Instance)** | 실제 개별 대상 | Blake, 아마존, 주문 12345 |
| **속성(Property)** | 개체가 가진 정보 | 사람의 이름, 상품의 가격 |
| **관계(Relation)** | 개체와 개체 사이의 연결 | 사람은 회사를 다닌다, 주문은 상품을 포함한다 |
| **제약(Constraint)** | 모델이 따라야 하는 규칙 | 모든 주문은 반드시 한 명의 구매자와 연결되어야 한다 |

## RDF · RDFS · OWL — 무엇을 정의하고 어떻게 표현하나

> **온톨로지가 "무엇을 정의할 것인가"라면, RDF는 "그 정의와 데이터를 어떻게 표현할 것인가"다.**

W3C 시멘틱 웹 스택은 층으로 쌓인다:

```
                Ontologies: OWL │ Rules: RIF/SWRL │ Validation: SHACL
  Querying:     ─────────────────────────────────────────────────────
  SPARQL                        Taxonomies: RDFS
                ─────────────────────────────────────────────────────
                        Data Interchange: RDF
                ─────────────────────────────────────────────────────
          Data Representations: RDF/XML, Turtle, N-Triples, N-Quads
```

### RDFS — 기본 스키마 정보

RDF만으로 트리플 표현은 가능하지만, 개념 간 계층 구조나 규칙을 설명하려면 추가 언어가 필요하다.

| 용어 | 정의하는 것 | 예 |
|---|---|---|
| `rdfs:Class` | 개념의 유형 | Person, Organization, Order, Product |
| `rdfs:subClassOf` | 클래스 간 상하위 관계 | Employee는 Person의 하위 클래스 |
| `rdf:Property` | 속성이나 관계 | worksAt, hasPrice, orderedBy |
| `rdfs:domain` | 해당 속성이 **주로 어떤 주어 클래스**에 적용되는지 | worksAt의 domain은 Person |
| `rdfs:range` | 해당 속성의 **목적어가 어떤 클래스/타입**이어야 하는지 | worksAt의 range는 Organization |

```
스키마:  Person은 클래스다 · Employee는 클래스다 · Employee는 Person의 하위 클래스다
        Organization은 클래스다 · worksAt는 속성이다
        worksAt의 domain은 Person이다 · worksAt의 range는 Organization이다
데이터:  Jeff - type - Employee
        Jeff - worksAt - Amazon
```

### OWL — 논리 관계와 제약

RDFS보다 강한 표현력. 클래스와 속성을 정의하는 것을 넘어 **개념 간의 정교한 논리 관계와 제약**을
명시한다. 표현 가능한 규칙: 두 클래스는 동일하다 · 서로 배타적이다 · 어떤 속성은 역관계다 ·
대칭적이다 · 추이적이다 · 어떤 클래스는 특정 조건을 만족하는 개체들의 집합이다 · 어떤 속성은 반드시
하나만 가져야 한다.

### ⚠️ OWL을 꼭 써야 할까 — 대체로 아니다

> **"RDF는 꽤 자주 유용하다. RDFS도 메타모델링에 꽤 유용하다. OWL은 필요한 경우가 제한적이다."**

OWL이 필요한 경우는 **규칙 기반 의미 추론이 실제 가치가 있을 때**:

- 동일 개체 판별 규칙이 중요할 때
- 상속/배타 규칙이 실제 품질 검증에 쓰일 때
- 정책/권한/도메인 규칙을 논리적으로 검증해야 할 때
- [[GraphRAG|Graph RAG]]에서 개체 타입/관계 추론이 중요할 때

> **반대로 단순 메타데이터 수집, lineage 시각화, 태그 검색 정도면 OWL까지 가는 순간 오히려
> 과설계가 된다.**

이 절제된 태도가 이 챕터에서 가장 실무적인 대목이다.

## 온톨로지가 있는가 — 판단 3문항

"우리 시스템에 온톨로지가 있나?"를 판단하는 기준:

1. **개념 정의서가 있는가** — 단순 테이블명이 아니라: `User`란 무엇인가, `Customer`와 `Subscriber`는
   어떻게 다른가, `Product`와 `Content`는 어떤 관계인가
2. **관계가 단순 컬럼 연결이 아니라 의미로 정의되어 있는가** — `owns`, `subscribesTo`, `fulfills`,
   `derivedFrom` 같은 관계 이름과 의미가 명확한지
3. **기계가 읽고 검증하거나 활용할 수 있는가** — 문서에만 있는 것보다, 시스템이 이를 읽어 검증·매핑·
   추론·검색 확장·의미 기반 질의를 할 수 있으면 온톨로지 가능성

**결론적으로 온톨로지란:** 도메인 개념 체계가 있고 · 개념 간 관계가 정의되어 있고 · 속성과 제약이
명시되어 있고 · 사람과 시스템이 그 정의를 공유하며 · **실제 검증/검색/추론/통합의 기준으로 쓰이는
경우.**

---

# 설계의 실무 원칙

> **"온톨로지 설계가 어려운 이유는 문법이 어려워서가 아니다.
> 무엇을 클래스, 무엇을 속성, 무엇을 관계로 둘지 경계가 애매하기 때문이다."**
>
> 이 판단이 흔들리면 뒤의 지식 그래프·시맨틱 ETL·검증 규칙까지 함께 흔들린다.

## 모델은 질의와 활용 시나리오에서 출발한다

실제 사용 질문에서 시작한다 — "이 상품은 어떤 브랜드에 속하는가", "이 Dataset은 어떤 Job이
만들었는가", "이 Dashboard는 어떤 테이블을 사용하는가".

| 질문에서의 등장 방식 | 후보 |
|---|---|
| 반복적으로 **독립 개체**로 등장 | 클래스 후보 |
| 개체의 **설명값**으로만 등장 | 속성 후보 |
| 두 개체를 잇는 **의미 있는 연결**로 반복 | 관계 후보 |

> 쉽게: **클래스는 명사형 개체, 관계는 동사형 연결, 속성은 설명 값.**

## 클래스

기준: **"이것은 ~의 한 종류인가"** 라고 말할 수 있으면 클래스 후보다.
(PremiumCustomer는 Customer의 한 종류 / FactTable은 Dataset의 한 종류)

**주의:** 클래스는 개별 행을 직접 표현하지 않는다. 개별 행이나 실제 객체는 인스턴스가 되는 경우가
많다. `Customer`는 클래스, `customer_1001`은 인스턴스. `DatasetType`은 클래스,
`dataset_sales_daily`는 인스턴스.

> 반복해서 재사용되는 개념 이름이면 클래스일 가능성이 크고, 운영 중 실제 식별자와 함께 관리되는
> 대상이면 인스턴스일 가능성이 크다.

### Granularity — 어디까지 나눌 것인가

**지식 그래프가 실제 세상을 얼마나 상세하고 밀도 있게 표현하는지**를 정하는 수준.

- 이커머스에서 `Product`만 관리하면 충분한가, **SKU**까지 구분해야 하는가?
  → 사이즈·색상·옵션별 재고를 다루면 SKU 수준까지 내려가야 한다.
- 데이터 플랫폼에서 `Job`만 보면 충분한가, **Run**까지 봐야 하는가?
  → 장애 분석·재처리·실행 이력 추적이 중요하면 Run까지 분리해야 한다.

### 새 클래스로 둘까, 속성값으로 둘까

모델링에서 가장 흔한 고민. 상품 상태(판매중/품절/예약판매)를 단순 문자열 속성으로 둘 수도 있고,
데이터셋 중요도를 high/medium/low 문자열로 둘 수도 있다.

> **판단 기준: 다른 규칙과 관계를 바꾸면 클래스 후보, 단순 설명만 하면 속성값 후보.**
> (중요도별 승인 절차·품질 기준·모니터링 정책이 달라진다면 단순 값보다 명시적 개념 체계가 필요하다)

## 속성

속성은 어떤 대상을 설명하는 값이다. **두 종류로 나누는 편이 안전하다:**

| | 연결 대상 | 예 |
|---|---|---|
| **Data Property** | 대상과 **값** | `hasEmail`, `hasPrice`, `createdAt` |
| **Object Property** | 대상과 **다른 대상** | `placesOrder`, `belongsToBrand`, `usesDataset` |

쉽게 구분: 문자열·숫자·날짜면 보통 Data Property, **독립 식별자가 있는 다른 대상이면 Object
Property.**

## 관계

> **"관계는 선 하나가 아니라, 왜 연결되었는가까지 담는 의미 계약이다."**

좋은 관계 이름의 조건: 방향이 분명 · 업무 의미가 분명 · **이름만 봐도 주어와 목적어가 떠오른다.**

| 좋은 예 | 나쁜 예 |
|---|---|
| `produces`, `usesDataset`, `belongsToBrand`, `ownedBy` | `relatedTo`, `linkedTo`, `hasInfo` |

### ⭐ 관계에 정보가 많이 붙으면 그건 독립 개체다

실무에서는 관계가 단순 연결로 끝나지 않는 경우가 많다.

- 고객과 상품 사이에는 단순 "구매했다"만 있는 게 아니라 **구매 시각·수량·결제수단·할인·주문상태**가
  함께 붙는다 → `Customer -buys-> Product`보다 **`Order`라는 별도 개체**를 두는 편이 자연스럽다.
- `Job -produces-> Dataset`만으로 부족할 수 있다. 실행 시각·run id·소스 환경·품질 결과까지
  중요하면 **`Run`이나 `LineageEvent` 같은 중간 개체**가 필요하다.

> **"관계에 설명해야 할 정보가 많아질수록 그 관계는 독립 개체일 가능성이 크다."**

## domain과 range

관계가 **보통 어디서 시작해 어디로 가는가**.

- `domain` = 이 관계를 쓰는 **시작 쪽** 대상
- `range` = 이 관계가 가리키는 **도착 쪽** 대상

예) `produces` → domain = `Job`, range = `Dataset`. `placesOrder` → 보통 Customer에서 시작해 Order로.

## ⭐ 가장 흔한 실수

> **테이블 = 클래스, 컬럼 = 속성, FK = 관계로 그대로 옮기는 것.**

- `orders` 테이블이 있다고 `Order`가 반드시 단순 클래스인 것은 아니다
- `brand_name` 컬럼이 있다고 `Brand`를 문자열로만 둬야 하는 것도 아니다
- `owner_email` 컬럼이 있다고 `Owner`를 값으로만 봐야 하는 것도 아니다

**운영 DB 스키마는 저장과 처리 효율을 위한 구조이고, 온톨로지는 의미 해석과 재사용을 위한 구조다 —
목적이 다르다.**

물어야 할 것: 이건 **독립적으로 식별되는 대상**인가 단순 값인가 · 이 연결은 **구현 디테일**인가
의미 있는 관계인가.

> **"온톨로지 설계는 스키마 복사가 아니라 의미 구조를 다시 세우는 작업이다."**

## 설계 체크리스트

| **클래스 체크** | **속성 체크** |
|---|---|
| 이 개념은 독립적으로 재사용되는가 | 이건 값인가, 다른 대상을 가리키는가 |
| 하위 클래스로 나눌 이유가 분명한가 | 문자열로 두면 나중에 확장에 막히지 않는가 |
| 실제 한 건과 개념 유형이 섞이지 않았는가 | 값 타입은 명확한가 |

| **관계 체크** | **운영 체크** |
|---|---|
| 방향이 분명한가 | 사람이 읽을 label과 설명이 있는가 |
| 이름만 보고 의미가 드러나는가 | 활용 질문에 실제로 답할 수 있는가 |
| 관계에 시간·상태·출처 같은 정보가 많이 붙지 않는가 | 모델을 바꿔도 유지보수 가능한가 |

---

# SHACL — 그래프용 데이터 계약

> ⭐ **"SHACL은 그래프용 테스트 코드에 가깝다."**

앞의 내용이 "원천 데이터를 어떻게 수집하고 온톨로지와 매핑해 그래프로 만드는가"(생성)였다면,
SHACL의 질문은 다르다 — **만들어진 그래프가 정말 우리가 기대한 구조와 의미를 만족하는가**(검증).

## SHACL이란

**RDF 그래프를 규칙으로 검사하는 언어.** 조건 집합 자체가 또 다른 RDF graph로 표현된다 —
**규칙도 그래프, 검사 대상도 그래프.**

| 용어 | 뜻 |
|---|---|
| **data graph** | 실제로 검증할 대상 데이터 그래프 |
| **shapes graph** | 그 데이터를 검사하는 규칙 그래프 |

관계형 데이터에서 `NOT NULL`, datatype check, referential integrity, row-level quality rule로 하던
검사를 그래프에서 수행한다: 노드가 어떤 타입인지 · 필수 속성이 있는지 · 관계가 몇 개 이상인지 ·
값 타입이 맞는지 · 특정 경로가 존재하는지.

> **실무적으로는 이 규칙 묶음을 그래프용 데이터 계약처럼 운영할 수 있다.**
> → [[Data SLA and observability]]의 계약·게이트 개념이 그래프로 옮겨온 것.

## 핵심 구조

| | 뜻 | 예 |
|---|---|---|
| **Shape** | 검증 규칙 묶음 | |
| **Target** | 어떤 노드에 이 규칙을 적용할지 정하는 기준 | `sh:targetClass ex:Customer` |
| **Node Shape** | 노드 자체에 대한 규칙 | Customer 노드는 Customer 타입이어야 함 |
| **Property Shape** | 노드의 특정 속성이나 경로에 대한 규칙 | Customer의 email은 문자열이어야 함 / Order의 containsProduct는 최소 1개 |

## Turtle 문법 최소 지식

Turtle은 RDF를 사람이 읽기 쉽게 텍스트로 적는 방식이다.

| 기호 | 뜻 |
|---|---|
| `a` | `rdf:type`의 축약형 ("이것은 무슨 타입이다") |
| `@prefix` | 접두사 선언 (`ex:` 예시 네임스페이스, `sh:` SHACL 표준 용어, `xsd:` 데이터 타입) |
| `;` | 같은 주어(subject)를 반복할 때 |
| `,` | 같은 주어/술어에서 object를 여러 개 적을 때 |
| `.` | 한 triple 문장의 끝 |
| `[...]` | 이름 없는 임시 노드(blank node) |

## 예시

```turtle
@prefix ex:  <http://example.com/> .
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:CustomerShape
    a sh:NodeShape ;
    sh:targetClass ex:Customer ;
    sh:property [
        sh:path ex:customerId ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ] ;
    sh:property [
        sh:path ex:email ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
    ] .

ex:OrderShape
    a sh:NodeShape ;
    sh:targetClass ex:Order ;
    sh:property [
        sh:path ex:orderId ;
        sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path ex:createdAt ;
        sh:datatype xsd:dateTime ;
    ] ;
    sh:property [
        sh:path ex:orderedBy ;
        sh:class ex:Customer ;
        sh:minCount 1 ;
    ] .
```

읽으면: **"고객 노드는 최소 이 정도 정보를 갖춰야 고객으로 인정, 주문 노드는 최소 이 정도를 갖춰야
주문으로 인정"** 이라고 정해둔 것.

통과하는 데이터:

```turtle
ex:customer_1001 a ex:Customer ;
    ex:customerId "1001" ;
    ex:email "alice@example.com" .

ex:order_2001 a ex:Order ;
    ex:orderId "2001" ;
    ex:createdAt "2026-04-09T10:00:00"^^xsd:dateTime ;
    ex:orderedBy ex:customer_1001 .
```

위반하는 데이터 — `orderedBy`가 없어 `sh:minCount 1`을 어긴다:

```turtle
ex:order_9999 a ex:Order ;
    ex:orderId "9999" .
```

## 관련 페이지

- [[Data semantics]] — 온톨로지가 속한 스펙트럼
- [[Knowledge graph]] — 온톨로지가 스키마 역할을 하는 대상
- [[Knowledge graph pipeline]] — **온톨로지를 실제 그래프로 구현하는 파이프라인** (SHACL 검증 포함)
- [[Graph data model]] — RDF와 Property Graph의 차이
- [[Schema-centric data modeling]] — **여기 스키마를 그대로 옮기는 것이 가장 흔한 실수다**
- [[Data SLA and observability]] — 데이터 계약·품질 게이트의 상위 개념

## 출처

- [[AI DE Course - Part3 Ch3 Ontology basics]]
- [[AI DE Course - Part3 Ch3 Ontology design principles]]
- [[AI DE Course - Part3 Ch3 SHACL and graph data contracts]]

---
type: source
title: AI DE 강의 3-11 SHACL 검증
aliases: [AI DE 3-11]
tags: [AI-DE-강의, 시맨틱, SHACL, 품질, 계약]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part3/03. Ch3. 온톨로지 및 지식 그래프.pdf"
---

# AI DE 강의 3-11 SHACL 검증

[[AI 데이터 엔지니어링 강의]] Part 3의 Ch3 소단원 4다. 앞 강의가 그래프를 어떻게 만드는가를 다뤘다면, 이 강의는 만들어진 그래프가 기대한 구조와 의미를 만족하는가를 묻는다. SHACL의 개념(data graph·shapes graph), 핵심 구조, 규칙을 적는 Turtle 문법을 설명하고, 고객·주문 두 shape와 데이터 두 개로 예시를 보인다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 3 「시멘틱 & 컨텍스트 기반 데이터 설계」 |
| 덱 제목 | Ch3. 온톨로지 및 지식 그래프: 4. SHACL을 이용한 그래프 검증과 데이터 계약 |
| 원본 파일 | `part3/03. Ch3. 온톨로지 및 지식 그래프.pdf` p46–65 (20p). p61–65의 코드는 이미지 슬라이드 |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-04-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch3`, 소단원 번호 `4`는 표지 슬라이드 |

## 요약

### 01. SHACL을 통한 검증 (p48–50)

- 앞 파트는 생성의 문제였고 이번 질문은 검증의 문제다. "만들어진 그래프가 정말 우리가 기대한 구조와 의미를 만족하는가."
- SHACL은 RDF 그래프를 조건 집합에 대해 검증하는 언어이고, 조건 집합도 RDF 그래프로 표현된다. 검증 대상은 data graph, 규칙은 shapes graph다. 강의의 비유: "SHACL은 그래프용 테스트 코드에 가까움".
- 관계형 데이터의 NOT NULL, datatype check, 참조 무결성, 행 단위 품질 규칙에 해당하는 것을 그래프에서 검사한다. 노드 타입, 필수 속성, 관계 개수, 값 타입, 특정 경로의 존재.
- "실무적으로는 이 규칙 묶음을 그래프용 데이터 계약처럼 운영할 수 있음."(p50)

### 02. 핵심 구조 (p51–52)

| 용어 | 뜻 | 예 |
|---|---|---|
| Shape | 검증 규칙 묶음 | `CustomerShape` |
| Target | 규칙을 적용할 노드를 정하는 기준 | `sh:targetClass ex:Customer` |
| Node Shape | 노드 자체에 대한 규칙 | Customer 노드는 Customer 타입 |
| Property Shape | 노드의 특정 속성이나 경로에 대한 규칙 | Customer의 email은 문자열, Order의 containsProduct는 최소 1개 |

### 03. Turtle (p53)

RDF를 텍스트로 적는 문법이다. `a`는 `rdf:type`의 축약, `@prefix`는 접두사 선언, `;`는 같은 주어 반복, `,`는 같은 주어·술어의 object 여러 개, `.`는 트리플 문장의 끝, `[...]`는 이름 없는 노드(blank node).

### 04. SHACL 예시 (p54–65)

설명 슬라이드(p54–55)가 말하는 규칙: 고객은 customerId가 반드시 하나만 있고 email이 반드시 있으며 문자열이다. 주문은 orderId가 반드시 있고, createdAt이 있다면 날짜·시간 형식이며, orderedBy가 반드시 있고 Customer 타입 노드를 가리킨다. p56–60은 세 접두사(`ex:`, `sh:`, `xsd:`)를 하나씩 설명한다.

shapes graph (p61–63 이미지, 세 슬라이드에 같은 코드가 있다. 슬라이드에 적힌 그대로):

```turtle
@prefix ex: <http://example.com/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
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

"실제 동작" 데이터 1 (p64):

```turtle
@prefix ex: <http://example.com/> .

ex:customer_1001 a ex:Customer ;
    ex:customerId "1001" ;
    ex:email "alice@example.com" .

ex:order_2001 a ex:Order ;
    ex:orderId "2001" ;
    ex:createdAt "2026-04-09T10:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> ;
    ex:orderedBy ex:customer_1001 .
```

"실제 동작" 데이터 2 (p65):

```turtle
@prefix ex: <http://example.com/> .

ex:order_9999 a ex:Order ;
    ex:orderId "9999" .
```

슬라이드에는 두 데이터의 검증 결과가 없다.

### 위키가 실행한 결과

위의 세 코드 블록을 그대로 파일로 저장해 pyshacl 0.40.1(`pyshacl -s shapes.ttl data.ttl`)로 검증했다(2026-09-28).

| 데이터 | 결과 |
|---|---|
| 데이터 1 (p64) | `Conforms: True` |
| 데이터 2 (p65) | `Conforms: False`, 위반 1건 (아래) |
| 데이터 1에 email을 하나 더 넣은 것 (`ex:email "alice@example.com", "alice2@example.com"`) | `Conforms: True` |
| 데이터 1의 createdAt을 타입 없는 `"2026-04-09"`로 바꾼 것 | `Conforms: False`, "Value is not Literal with datatype xsd:dateTime" |

데이터 2의 위반 보고:

```
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ sh:class ex:Customer ; sh:minCount Literal("1", datatype=xsd:integer) ; sh:path ex:orderedBy ]
	Focus Node: ex:order_9999
	Result Path: ex:orderedBy
	Message: Less than 1 values on ex:order_9999->ex:orderedBy
```

데이터 2에는 createdAt도 없지만 위반은 orderedBy 하나뿐이다. createdAt shape에는 `sh:minCount`가 없어서, 값이 있을 때만 타입을 검사한다. 설명 슬라이드의 "createdAt이 있다면 날짜/시간 형식"과 맞는다.

## 핵심

- "SHACL은 그래프용 테스트 코드", "규칙 묶음을 그래프용 데이터 계약처럼 운영"이라는 두 문장이 이 강의에서 가장 쓸모 있다. shapes graph를 버전 관리하고 파이프라인의 게이트로 두면, 관계형 쪽의 스키마 테스트·[[데이터 SLA]]의 정확성 검사와 같은 자리에 선다. 계약 전반은 [[데이터 계약]]에 모았다.
- RDFS의 domain·range와 SHACL의 역할이 여기서 갈린다. [[AI DE 강의 3-08 온톨로지와 RDFS·OWL]]은 range를 "~이어야 한다"로 설명했지만 RDFS는 위반을 오류로 보지 않고 타입을 추론한다. "이어야 한다"를 실제로 검사하는 것은 SHACL의 `sh:class`·`sh:datatype`이다. 위 실행 결과의 마지막 줄이 그 예다([[온톨로지]] · [[SHACL]]).
- SHACL은 닫힌 세계처럼 검사하지만 기본은 열려 있다. shape에 적지 않은 속성은 얼마든지 붙어도 통과한다(`sh:closed true`를 써야 막힌다). 위키가 명세에 비춰 보탠 설명이다.

## 주의·결함

- ❗ 설명과 코드가 다르다. p52의 CustomerShape 설명은 "email은 최대 1개"라고 하는데, p62의 코드에는 email에 `sh:maxCount 1`이 없다. 위 실행 결과처럼 email이 두 개인 고객도 통과한다. p54의 규칙 목록에는 "최대 1개"가 없으므로 p52만 코드와 어긋난다. 설명대로 동작시키려면 email property shape에 `sh:maxCount 1 ;`을 더해야 하고, 그렇게 고치면 email 두 개인 데이터에서 "More than 1 values on ex:customer_1001->ex:email" 위반이 난다(위키가 실행해 확인).
- p52는 OrderShape에 "containsProduct는 최소 1개"를 넣지만 코드의 OrderShape에는 containsProduct가 없고 대신 orderedBy가 있다. p51의 Property Shape 예도 containsProduct다.
- p64·65의 "실제 동작"은 데이터만 보여 주고 검증 결과(conforms 여부, 위반 보고)를 보이지 않는다. 두 번째 데이터가 무엇을 위반하는지는 청중이 추론해야 한다.
- p61–63은 같은 코드 이미지를 세 번 쓰고 왼쪽 제목만 CustomerShape(p61·62)와 OrderShape(p63)로 바꾼다. 텍스트 추출로는 p61이 제목뿐인 슬라이드처럼 보이지만, 이미지로 보면 코드가 있다(위키가 확인). p58–60은 같은 슬라이드(xsd 접두사)가 세 번 반복된다.
- 소단원 제목의 "데이터 계약"은 p50의 한 줄("그래프용 데이터 계약처럼 운영할 수 있음")에만 나온다. 계약에 무엇을 적는지, 누가 소유하는지, 위반하면 어떻게 하는지는 없다.
- SHACL은 2017-07-20 W3C Recommendation이고, SHACL 1.2 Core는 2026-09 현재 Working Draft다(https://www.w3.org/TR/shacl/ · https://www.w3.org/TR/shacl12-core/ , 2026-09-28 확인). 강의는 버전을 말하지 않는다.

## 관련

- 엔티티: [[SHACL]]
- 개념: [[데이터 계약]] · [[온톨로지]] · [[지식 그래프]] · [[그래프 데이터 모델]] · [[데이터 SLA]] · [[스키마 진화]]
- 이전 강의: [[AI DE 강의 3-10 지식 그래프 파이프라인]]
- 다음 강의: [[AI DE 강의 3-12 RAG의 이해와 한계]]

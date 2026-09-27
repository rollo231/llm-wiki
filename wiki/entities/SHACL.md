---
type: entity
title: SHACL
aliases: [Shapes Constraint Language, Shapes graph, 셰이프 그래프]
tags: [표준, 그래프, 품질, 계약]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 3-10 지식 그래프 파이프라인]]"
  - "[[AI DE 강의 3-11 SHACL 검증]]"
  - "[[AI DE 강의 3-05 Property Graph와 RDF]]"
---

# SHACL

Shapes Constraint Language. RDF 그래프가 조건 집합을 만족하는지 검사하는 W3C 표준 언어다. 2017-07-20에 W3C Recommendation이 되었고, SHACL 1.2 Core는 2026-09 현재 Working Draft다(https://www.w3.org/TR/shacl/ · https://www.w3.org/TR/shacl12-core/ , 2026-09-28 확인).

## 무엇을 하나

- 검증 대상은 data graph, 규칙은 shapes graph다. 규칙도 RDF 그래프로 적는다.
- 규칙 단위는 shape다. Node Shape는 노드 자체에, Property Shape는 노드의 속성·경로에 건다. Target(`sh:targetClass` 등)이 규칙을 적용할 노드를 고른다.
- 자주 쓰는 제약: `sh:minCount`·`sh:maxCount`(개수), `sh:datatype`(리터럴 타입), `sh:class`(가리키는 노드의 타입. `rdf:type/rdfs:subClassOf*` 경로로 확인), `sh:closed`(적지 않은 속성 금지).
- 결과는 conforms 여부와 위반 보고(focus node, path, 위반한 제약, 메시지)다.

[[AI DE 강의 3-11 SHACL 검증]]은 SHACL을 "그래프용 테스트 코드"에 비유하고, 규칙 묶음을 "그래프용 데이터 계약"처럼 운영할 수 있다고 한다([[데이터 계약]]). 강의 예제의 shapes와 데이터, 위키가 pyshacl로 실행한 결과(설명과 코드가 어긋난 email 최대 개수 포함)는 그 source 페이지에 있다.

## RDFS·OWL과의 관계

RDFS의 domain·range와 OWL은 기본적으로 새 사실을 끌어내는 추론 쪽이고, 위반을 오류로 내지 않는다. SHACL은 주어진 그래프를 규칙에 대 보고 통과·실패를 낸다. "주문의 orderedBy는 Customer여야 한다"를 강제하는 것은 `rdfs:range`가 아니라 `sh:class`다. 자세한 대비는 [[온톨로지]]에 있다.

## 파이프라인에서의 자리

[[AI DE 강의 3-10 지식 그래프 파이프라인]]은 RDF 생성 뒤의 검증 단계에 SHACL을 두고 "단순 파이프라인보다 검증이 더 중요"하다고 한다. 데이터셋 스키마가 바뀔 때 graph validation을 다시 돌리라는 운영 규칙도 같은 강의에 있다. 관계형 파이프라인의 스키마 테스트·품질 검사([[데이터 SLA]])와 같은 역할을 그래프 쪽에서 맡는다는 것은 위키의 정리다.

Property Graph 쪽에는 SHACL처럼 널리 쓰이는 표준 검증 언어가 없고, DB가 제공하는 제약에 기댄다. Neo4j의 제약은 속성 유일성, 속성 존재, 속성 타입, 키 제약 네 가지이고 유일성을 뺀 셋은 Enterprise Edition 전용이다(https://neo4j.com/docs/cypher-manual/current/schema/constraints/ , 2026-09-28 확인). [[AI DE 강의 3-05 Property Graph와 RDF]]가 RDF 쪽 검증 수단으로 SHACL을 짧게 언급한다. 두 모델의 비교는 [[그래프 데이터 모델]]에 있다.

## 관련

- [[온톨로지]] · [[지식 그래프]] · [[그래프 데이터 모델]] · [[데이터 계약]] · [[데이터 SLA]]

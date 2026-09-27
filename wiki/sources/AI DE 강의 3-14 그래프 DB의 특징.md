---
type: source
title: AI DE 강의 3-14 그래프 DB의 특징
aliases: [AI DE 3-14]
tags: [AI-DE-강의, 그래프, 데이터베이스]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part3/05. Ch5. 그래프 데이터베이스 실습.pdf"
---

# AI DE 강의 3-14 그래프 DB의 특징

[[AI 데이터 엔지니어링 강의]] Part 3의 마지막 덱(Ch5) 첫 소단원이다. 그래프가 무엇인지는 앞 덱들이 다뤘으니, 여기서는 왜 RDB만으로는 불편해지는지, 그래프 DB가 관계를 어떻게 저장하고 탐색하는지, 언제 RDB 대신 그래프 DB를 쓰는지를 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 3 「시멘틱 & 컨텍스트 기반 데이터 설계」 |
| 덱 제목 | Ch5. 그래프 데이터베이스 실습: 1. Graph DB의 특징 |
| 원본 파일 | `part3/05. Ch5. 그래프 데이터베이스 실습.pdf` p1–11 (11p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 (Part 3에서 가장 늦음) |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch5`, 소단원 번호 `1`은 표지 슬라이드 |

## 요약

### 01. 관계 탐색을 위한 DB (p3–4)

- 그래프 데이터를 테이블에 저장하는 것은 가능하다. 회원-주문-상품-카테고리-추천 관계도 테이블로 분해할 수 있다.
- 문제는 다단계 관계 탐색이 핵심이 될 때다. 친구의 친구, 이 계정과 연결된 다른 의심 계정, 이 테이블 변경의 downstream 영향 같은 질문은 JOIN 체인이 길어진다.
- self join, recursive join, 경로 탐색 로직이 쌓이면 쿼리를 읽기 어렵고, 디버깅이 어렵고, 설계 의도가 SQL 안에 묻힌다.

### 02. 핵심 특징 (p5–8)

관계를 계산하느냐, 저장하느냐의 차이로 설명한다.

| | RDB | Graph DB |
|---|---|---|
| 엔터티 | 테이블·행 | node |
| 관계 | foreign key, bridge table, join table | relationship(edge). 관계 자체가 저장 대상이고 타입·방향·속성을 가진다 |
| 탐색 | 인덱스 lookup → JOIN → 필요하면 self join·recursive join | 시작 노드 선택 → 관계 타입을 따라 hop traversal → 패턴 매칭 |

- 그래서 그래프 질의는 "어떤 테이블을 JOIN할까"보다 "어떤 관계를 몇 hop 따라갈까"에 가깝다.
- "빠르다"의 뜻을 한정한다(p7). 모든 질의가 빠른 것이 아니라 관계 중심 탐색에서 인접 노드 접근 비용을 낮추도록 설계됐다는 뜻이다. index-free adjacency는 다음 노드로 갈 때마다 별도 JOIN이나 인덱스 탐색을 줄인다는 의미다. 하지만 전체 질의가 O(1)은 아니다. hop 수가 늘면 건드리는 부분 그래프가 커지고, high-degree node가 많으면 path explosion이 생기고, 선택도 높은 조건이 약하면 그래프도 느려진다.
- 트랜잭션(p8). "NoSQL이라서 트랜잭션이 없다"가 아니다. Neo4j는 그래프·인덱스·스키마 접근을 트랜잭션에서 수행하고 ACID를 보장하며 기본 격리 수준은 read-committed, 필요하면 명시적 락으로 더 강한 격리를 얻는다. Neptune은 동시성 높은 OLTP를 지향하고, 여러 mutation 쿼리를 한 트랜잭션으로 묶으면 원자적으로 성공하거나 실패한다.

### 03. 질의 언어 (p9–10)

- SQL은 table·predicate·join·aggregation 중심이고, 그래프 질의는 node·edge·path·pattern matching 중심이다.
- 대표 언어로 Cypher, Gremlin, GQL을 든다. 언어가 여러 개인 이유는 모델이 다르면 질의 사고도 달라지기 때문이다.

| 언어 | 대상 | 방식 |
|---|---|---|
| openCypher | property graph | 선언형. SQL과 비슷해 개발자에게 친숙 |
| Gremlin | property graph | traversal language. step-by-step으로 따라감 |
| SPARQL | RDF graph | graph pattern matching. triple과 named graph 질의 |

### 04. 언제 RDB, 언제 Graph DB (p11)

강의는 둘을 경쟁 관계가 아니라 질문 유형이 다른 두 엔진으로 본다.

| RDB가 적합 | Graph DB가 적합 |
|---|---|
| 정형 스키마가 안정적 | 질문의 핵심이 "누가 누구와 어떻게 연결되는가" |
| CRUD·집계·리포팅 중심 | self join·recursive join이 반복 |
| 재무·재고·주문 원장처럼 record correctness가 핵심 | fraud, recommendation, lineage, entity resolution이 중요 |
| 복잡한 multi-hop traversal이 핵심이 아님 | relationship-heavy OLTP 또는 graph analytics가 필요 |

## 핵심

- "관계를 계산하느냐, 저장하느냐"가 이 소단원의 설명 틀이다. RDB는 질의 시점에 JOIN으로 관계를 다시 만들고, 그래프 DB는 관계를 저장해 두고 따라간다. 전문은 [[그래프 데이터베이스]]에 모았다.
- p7의 단서가 이 덱에서 가장 쓸모 있다. index-free adjacency는 hop 하나의 비용을 낮출 뿐이고, 질의 전체의 비용은 건드리는 부분 그래프의 크기로 정해진다. 슈퍼노드(팔로워가 수백만인 계정 같은 high-degree node)를 지나는 순간 탐색이 폭발하는 것은 그래프 DB에서도 그대로다. 슈퍼노드 예시는 위키가 덧붙인 것이다.
- p8은 [[AI DE 강의 3-02 RDBMS의 한계와 NoSQL]]의 "NoSQL은 일관성을 완화한다"는 일반화에 단서를 단다. 그래프 DB는 NoSQL로 분류되지만 대표 제품은 ACID 트랜잭션을 준다. 두 소단원을 잇는 연결은 위키의 관찰이다.
- 질의 언어 표에서 openCypher·Gremlin·SPARQL은 [[그래프 데이터 모델]]의 두 갈래(property graph와 RDF)를 그대로 따른다([[AI DE 강의 3-05 Property Graph와 RDF]]).

## 주의·결함

- ❗ 덱 제목은 「그래프 데이터베이스 실습」인데 실습이 없다. 설치, 데이터 적재, Cypher·Gremlin 쿼리 예제가 하나도 없고 26쪽 전부 개념·비교 슬라이드다. 소단원 1의 "JOIN 체인이 길어진다"도 SQL과 Cypher를 나란히 보여 주지 않는다.
- p9는 대표 언어로 GQL을 들지만 설명하지 않는다. GQL은 ISO/IEC 39075:2024로 2024년 4월에 발행된 property graph 질의 표준이다. Neo4j 문서는 "Cypher now accommodates most mandatory GQL features and a substantial portion of its optional ones"라고 적는다. 별도 언어를 새로 지원한다기보다 Cypher가 GQL 적합성 쪽으로 수렴하는 방식이다. [https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance/ , 2026-09-28 확인]
- ✅ p8의 Neo4j 서술은 맞다. 운영 매뉴얼이 트랜잭션을 ACID로, read-committed를 기본 격리 수준으로 적는다. [https://neo4j.com/docs/operations-manual/current/database-internals/concurrent-data-access/ , 2026-09-28 확인] Neptune 서술도 맞다. 문서가 ACID와 트랜잭션 의미론을 명시하고, 여러 mutation을 한 트랜잭션으로 원자적으로 처리한다([[Amazon Neptune]], 2026-09-28 확인).
- p10의 표에는 Cypher가 아니라 openCypher가, p9 목록에는 SPARQL 없이 GQL이 있다. 같은 절 안에서 언어 목록이 다르다.

## 관련

- 개념: [[그래프 데이터베이스]] · [[그래프 데이터 모델]] · [[관계형 데이터베이스]] · [[NoSQL]]
- 엔티티: [[Neo4j]] · [[Amazon Neptune]]
- 이전 강의: [[AI DE 강의 3-13 GraphRAG 개념과 사례]]
- 다음 강의: [[AI DE 강의 3-15 그래프 DB 제품 비교]]

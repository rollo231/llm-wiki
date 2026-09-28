---
type: entity
title: Neo4j
aliases: [네오포제이, Infinigraph, Neo4j Infinigraph]
tags: [도구, 데이터베이스, 그래프]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 3-14 그래프 DB의 특징]]"
  - "[[AI DE 강의 3-15 그래프 DB 제품 비교]]"
---

# Neo4j

property graph 모델의 native [[그래프 데이터베이스]]다. 저장 레벨부터 노드·관계·속성을 중심에 두고, 선언형 질의 언어 Cypher를 중심으로 설계됐다. [[AI DE 강의 3-15 그래프 DB 제품 비교]]는 네 제품 가운데 Neo4j를 기준점으로 삼는다(소단원 제목이 「Neo4j vs 다른 DB」다).

## 강의가 드는 특징

- native graph database. 노드, 관계, 속성을 직접 다룬다.
- Cypher: SQL과 비슷하지만 그래프에 최적화된 선언형 패턴 매칭 언어.
- 운영 DBMS 기능: ACID 트랜잭션, cluster support, runtime failover, index, constraint.
- 그래프·인덱스·스키마 접근은 트랜잭션 안에서 수행하고, 기본 [[트랜잭션 격리 수준|격리 수준]]은 read-committed, 필요하면 명시적 락으로 더 강하게 격리한다([[AI DE 강의 3-14 그래프 DB의 특징]] p8).
- 확장은 native graph storage와 클러스터링 중심이고 Enterprise와 Infinigraph 방향으로 넓힌다.
- 우선 검토 대상: 실시간 추천, 사기 탐지, 마스터 데이터 관리, [[GraphRAG]] 백엔드.

Part 3의 GraphRAG 사례(Neo4j·Deloitte의 technology media company, DUCK / Kiku AI)도 Neo4j 고객 사례다([[AI DE 강의 3-13 GraphRAG 개념과 사례]]).

## 확인한 사실 (2026-09-28)

- ✅ ACID와 기본 격리 수준 read-committed는 운영 매뉴얼에 명시돼 있다. [https://neo4j.com/docs/operations-manual/current/database-internals/concurrent-data-access/]
- Infinigraph는 2025-09-04에 발표된 분산 아키텍처다. property sharding 방식으로, 그래프 토폴로지는 graph shard 하나에 두고 속성만 여러 property shard에 나눈다. 100TB+ 규모에서 운영(OLTP)과 분석 워크로드를 한 시스템에서 처리한다고 내세운다. 운영 매뉴얼에는 "Introduced in 2025.12, Not available on Aura"로 적혀 있고, GA 블로그는 2026-01-27에 나왔다. [https://neo4j.com/docs/operations-manual/current/scalability/sharded-property-databases/overview/ · https://www.prnewswire.com/news-releases/neo4j-launches-infinigraph-the-most-scalable-graph-database-for-unified-operational-and-analytical-workloads-at-100tb-scale-302545785.html]
- Cypher와 GQL: ISO/IEC 39075:2024(GQL)가 2024년 4월에 발행됐고, Neo4j 문서는 "Cypher now accommodates most mandatory GQL features and a substantial portion of its optional ones"라고 적는다. [https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance/]
- 강의는 Community Edition과 Enterprise Edition의 차이를 다루지 않는다. 운영 매뉴얼에 따르면 Community Edition은 단일 인스턴스용으로 GPLv3 오픈소스이고, Enterprise Edition은 여기에 백업·클러스터링·failover 같은 기능을 더한다. Infinigraph는 자동 샤딩에 의한 수평 확장을 더한 특별한 Enterprise Edition이다. 강의가 드는 cluster support와 runtime failover(p16)는 Enterprise 쪽 기능이다. [https://neo4j.com/docs/operations-manual/current/introduction/ , 2026-09-28 확인]

## 관련

- [[그래프 데이터베이스]] · [[그래프 데이터 모델]] · [[GraphRAG]] · [[지식 그래프]]
- 비교 대상: [[Amazon Neptune]] · [[ArangoDB]] · [[JanusGraph]]

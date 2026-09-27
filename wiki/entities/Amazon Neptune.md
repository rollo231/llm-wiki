---
type: entity
title: Amazon Neptune
aliases: [Neptune, AWS Neptune, Neptune Analytics]
tags: [도구, 데이터베이스, 그래프, 관리형]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 3-14 그래프 DB의 특징]]"
  - "[[AI DE 강의 3-15 그래프 DB 제품 비교]]"
---

# Amazon Neptune

AWS의 완전 관리형 [[그래프 데이터베이스]] 서비스다. 고연결성 데이터셋을 저장하고 질의하도록 최적화됐고, property graph와 RDF를 모두 지원한다. [[AI DE 강의 3-15 그래프 DB 제품 비교]]는 Neptune을 "그래프 DB 제품군 안에서 운영 부담을 줄이는 관리형 선택지"로 둔다.

## 강의가 드는 특징

- [[그래프 데이터 모델]]의 두 갈래를 모두 지원하고, 각각에 맞는 질의 언어를 준다. property graph에는 Gremlin과 openCypher, RDF에는 SPARQL.
- 그래프 DB를 직접 운영하지 않고도 고가용성, 백업, 복제 같은 관리형 이점을 얻는다. 확장도 AWS가 인프라 운영을 대신하는 모델이다.
- 동시성 높은 OLTP를 지향하고 ACID를 제공한다. 여러 mutation 쿼리를 한 트랜잭션으로 묶으면 원자적으로 성공하거나 실패한다([[AI DE 강의 3-14 그래프 DB의 특징]] p8).
- 우선 검토 대상: AWS 안의 managed knowledge graph, RDF와 property graph 혼합, AWS 기반 고연결성 애플리케이션과 소셜 네트워킹.

Part 3의 GraphRAG 제품 사례인 Amazon Bedrock Knowledge Bases GraphRAG는 그래프와 벡터를 Neptune Analytics에 함께 저장한다([[AI DE 강의 3-13 GraphRAG 개념과 사례]]).

## 확인한 사실 (2026-09-28)

- ✅ Gremlin, openCypher, SPARQL 지원은 공식 문서에 적혀 있다. [https://docs.aws.amazon.com/neptune/latest/userguide/intro.html]
- Neptune Analytics는 Neptune Database와 별개인 인메모리 분석 엔진이다. 강의 Ch5는 Neptune Analytics를 따로 구분하지 않는다. 같은 이름의 두 서비스라서 "Neptune"이 어느 쪽을 가리키는지 문맥으로 확인해야 한다.
- ✅ 강의의 트랜잭션 서술(p8)은 맞다. 「Transaction Semantics in Neptune」은 "Because ACID support and well-defined transaction guarantees can be very important, we enforce strict semantics to help avoid data anomalies"라고 쓴다. 격리 수준은 질의 종류마다 다르다. 읽기 전용 질의는 MVCC 기반 snapshot isolation으로 돌고, mutation 질의 안의 읽기는 READ COMMITTED이되 레코드·범위 잠금으로 non-repeatable read와 phantom read까지 막는다. 세미콜론으로 이어 보낸 여러 SPARQL mutation은 한 트랜잭션으로 원자적으로 성공하거나 실패한다. [https://docs.aws.amazon.com/neptune/latest/userguide/transactions.html · https://docs.aws.amazon.com/neptune/latest/userguide/transactions-neptune.html , 2026-09-28 확인]

## 관련

- [[그래프 데이터베이스]] · [[그래프 데이터 모델]] · [[지식 그래프]] · [[GraphRAG]]
- 비교 대상: [[Neo4j]] · [[ArangoDB]] · [[JanusGraph]]

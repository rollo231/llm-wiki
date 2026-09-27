---
type: entity
title: JanusGraph
aliases: [Janus Graph]
tags: [도구, 데이터베이스, 그래프, 분산]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 3-15 그래프 DB 제품 비교]]"
---

# JanusGraph

분산 저장소 위에 올라가는 오픈소스 그래프 엔진이다. 저장과 인덱스를 외부 백엔드에 맡기고, 질의는 Apache TinkerPop의 Gremlin으로 한다. [[AI DE 강의 3-15 그래프 DB 제품 비교]]는 JanusGraph를 단일 완성형 제품보다 "분산 스토리지 위에 올라가는 graph database engine"에 가깝다고 설명한다.

## 강의가 드는 특징

- 저장 백엔드: Cassandra, HBase, BerkeleyDB 가운데 선택.
- 인덱스 백엔드: Elasticsearch, Solr, Lucene 조합.
- 질의: TinkerPop Gremlin 중심. step-by-step traversal.
- OLTP와 Hadoop 기반 OLAP 분석 워크플로를 함께 염두에 둔다.
- 확장: scale-out을 storage layer에 기댄다. 수십억 개 이상의 노드와 엣지를 목표로 한다.
- 우선 검토 대상: 초대규모 분산 그래프, 기존 Cassandra·HBase·Elasticsearch 인프라 재활용. 운영 복잡도를 감수하고 최대 scale-out을 원하는 팀.

## 확인한 사실 (2026-09-28)

- 강의의 저장 백엔드 셋은 공식 문서가 "JanusGraph is distributed with 3 supporting backends"라고 적는 셋(Cassandra, HBase, Berkeley DB Java Edition)과 같다. 문서의 저장 백엔드 목록에는 이 밖에 ScyllaDB, Google Cloud Bigtable, InMemory도 있다. 같은 문서는 BerkeleyDB JE가 분산 DB가 아니어서 주로 테스트와 탐색에 쓴다고 적는다. 초대규모 분산 그래프라는 강의의 자리매김에 맞는 백엔드는 Cassandra·HBase(와 ScyllaDB·Bigtable) 쪽이다. [https://docs.janusgraph.org/ , 2026-09-28 확인]
- 최신 릴리스는 v1.1.0(2024-11-09)이다. 저장소는 보관(archived)되지 않았고 커밋은 2026-09 말까지 이어지지만, 2년 가까이 새 릴리스가 없다. 제품을 고를 때 이 릴리스 주기를 확인할 필요가 있다는 점은 위키의 관찰이다. [https://api.github.com/repos/JanusGraph/janusgraph/releases]
- 저장 백엔드로 드는 Cassandra·HBase는 wide-column 저장소다. 강의 Ch1은 이들을 "열 기반 저장"이라고 하는데 분석용 열 기반 저장과는 다른 개념이다([[NoSQL]], [[행 기반과 열 기반 저장]]).

## 관련

- [[그래프 데이터베이스]] · [[NoSQL]]
- 비교 대상: [[Neo4j]] · [[Amazon Neptune]] · [[ArangoDB]]

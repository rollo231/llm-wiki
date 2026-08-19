---
type: entity
title: JanusGraph
area: [data-engineering]
aliases: [야누스그래프, Gremlin]
tags: [data-engineering, graph, database, distributed, janusgraph, gremlin]
created: 2026-08-01
updated: 2026-08-19
sources: ["[[AI DE Course - Part3 Ch5 Graph databases]]"]
---

# JanusGraph

**초대규모 분산 그래프를 위한 graph engine.**

> **단일 완성형 제품보다 분산 스토리지 위에 올라가는 graph database engine에 가깝다.**

이게 다른 [[Graph database|그래프 DB]]와의 결정적 차이다 — 저장 계층을 **직접 갖지 않고 조립한다.**

## 구성

| 계층 | 선택지 |
|---|---|
| **저장 백엔드** | Cassandra · HBase · BerkeleyDB 등 |
| **인덱스 백엔드** | Elasticsearch · Solr · Lucene 등 |
| **질의** | **Apache TinkerPop Gremlin** 중심 |
| **워크로드** | OLTP와 Hadoop 기반 OLAP 분석 워크플로를 함께 염두 |

**확장 방식:** 애초에 Cassandra/HBase 같은 분산 저장소를 백엔드로 두는 방식이라 **scale-out을 storage
layer에 기대는 구조.** [[NoSQL]]의 Wide-column 저장소 위에 그래프 엔진을 얹는 셈이다.

## 잘 맞는 곳

- **수십억 개 이상의 노드와 엣지** 규모
- 기존 Cassandra/HBase/Elasticsearch **분산 스토리지 생태계를 재활용**
- Gremlin/TinkerPop 중심 운영을 감당할 수 있는 팀
- 초대형 소셜 그래프, 초대규모 지식그래프
- **운영 복잡도를 감수하고 최대 scale-out을 원할 때**

## 링크

- [[Graph database]] — 제품 비교의 다섯 축 (저장 철학 축에서 **engine + backend** 자리)
- [[NoSQL]] — Wide-column 저장소(Cassandra·HBase)가 백엔드
- [[Neo4j]] · [[Amazon Neptune]] · [[ArangoDB]]
- 강의: [[AI Data Engineering (Fast Campus course)]]

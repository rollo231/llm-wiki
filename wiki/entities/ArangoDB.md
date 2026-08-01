---
type: entity
title: ArangoDB
area: [data-engineering]
aliases: [아랑고DB, AQL, SmartGraphs]
tags: [data-engineering, graph, database, multi-model, arangodb, aql]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part3 Ch5 Graph databases]]"]
---

# ArangoDB

**멀티모델 유연성이 강한 [[Graph database|그래프 DB]] 선택지.**
**native multi-model database** — key-value · document · graph를 **한 엔진 안에서** 함께 다룬다.

그래프만 위한 DB라기보다 **문서와 그래프를 함께 다뤄야 하는 복합 애플리케이션**에 강점이 있다.

## 특징

- **AQL 하나로** 문서 질의와 그래프 traversal을 함께 처리
- **named graph**와 **edge collection** 기반 graph 모델 지원
- **shortest path · k shortest paths · traversals**를 AQL에서 직접 수행 가능
- **확장** — 클러스터와 **SmartGraphs**를 통해 value-based sharding으로 **traversal locality**를
  높이는 방식. (같은 값 기준으로 샤딩해 탐색이 노드를 넘나드는 것을 줄인다)

## 잘 맞는 곳

- 문서 + 그래프 + 키값을 한 DB에서 다루고 싶음
- AQL 하나로 복합 질의를 처리하고 싶음
- 문서형 데이터와 그래프형 데이터가 함께 있고, 두 모델을 한 DB에서 일관되게 다루고 싶은 팀

## 링크

- [[Graph database]] — 제품 비교의 다섯 축 (저장 철학 축에서 **multi-model** 자리)
- [[NoSQL]] — Document / Key-Value / Graph 세 타입을 한 엔진에서
- [[Neo4j]] · [[Amazon Neptune]] · [[JanusGraph]]
- 강의: [[AI Data Engineering (Fast Campus course)]]

---
type: entity
title: ArangoDB
aliases: [Arango, AQL, SmartGraphs]
tags: [도구, 데이터베이스, 그래프, 멀티모델]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 3-15 그래프 DB 제품 비교]]"
---

# ArangoDB

키-값, 문서, 그래프를 한 엔진에서 다루는 native multi-model 데이터베이스다. [[AI DE 강의 3-15 그래프 DB 제품 비교]]는 그래프 전용 DB라기보다 문서와 그래프를 함께 다뤄야 하는 복합 애플리케이션에 강한 선택지로 소개한다.

## 강의가 드는 특징

- 질의 언어 AQL 하나로 문서 질의와 그래프 traversal을 함께 처리한다.
- named graph와 edge collection 기반 그래프 모델을 지원하고, shortest path, k shortest paths, traversal을 AQL에서 바로 수행한다.
- 확장: 클러스터와 SmartGraphs. SmartGraphs는 값 기준 [[샤딩]](value-based sharding)으로 서로 연결된 노드를 같은 샤드에 모아 traversal locality를 높인다.
- 우선 검토 대상: 문서형 데이터와 그래프형 관계를 한 엔진에서 같이 다뤄야 하는 애플리케이션.

## 확인한 사실 (2026-09-28)

강의에는 없는 라이선스와 회사 변화가 선택에 영향을 준다.

- 라이선스: 3.12부터 소스 코드가 Apache 2.0에서 BSL 1.1로 바뀌었고(2024-02 발표), 4년 뒤 Apache 2.0으로 전환된다. BSL은 ArangoDB를 관리형 서비스로 제공하는 것만 막는다. 바이너리 Community Edition은 ArangoDB Community License를 따르며, 3.12 이후 버전을 상업적 목적으로 쓰거나 데이터셋이 100 GiB를 넘으면 라이선스가 필요하다("You still need a license to use version 3.12 or later for commercial purposes or for a dataset size over 100 GiB"). [https://arangodb.com/2024/02/update-evolving-arangodbs-licensing-model-for-a-sustainable-future/ · https://docs.arango.ai/arangodb/stable/release-notes/version-3.12/whats-new-in-3-12/ , 2026-09-28 확인]
- SmartGraphs: 3.12.4까지는 Enterprise 전용이었고, 3.12.5부터 Community Edition에도 Enterprise 기능 전체가 들어가면서 SmartGraphs도 포함됐다. [https://docs.arango.ai/arangodb/stable/release-notes/version-3.12/whats-new-in-3-12/ · https://docs.arango.ai/arangodb/stable/graphs/smartgraphs/]
- 이름: 2025-10-23 회사명이 ArangoDB에서 Arango로 바뀌었고 "Arango AI Data Platform"이 출시됐다. 데이터베이스 제품 이름은 ArangoDB 그대로다. 슬라이드(2026-05)는 이 변화를 반영하지 않는다. [https://arango.ai/blog/the-next-evolution-of-arango-powering-the-age-of-contextual-ai]

## 관련

- [[그래프 데이터베이스]] · [[NoSQL]]
- 비교 대상: [[Neo4j]] · [[Amazon Neptune]] · [[JanusGraph]]

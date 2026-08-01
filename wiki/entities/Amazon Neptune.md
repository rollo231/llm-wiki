---
type: entity
title: Amazon Neptune
area: [data-engineering]
aliases: [Neptune, AWS Neptune, Neptune Analytics]
tags: [data-engineering, graph, database, aws, managed-service, rdf, property-graph]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part3 Ch5 Graph databases]]", "[[AI DE Course - Part3 Ch4 GraphRAG variants and products]]"]
---

# Amazon Neptune

**AWS의 완전관리형 [[Graph database|그래프 DB]] 서비스.** highly connected datasets를 저장하고
질의하도록 최적화된 엔진.

## 두 가지 특징

1. **Property Graph와 RDF Graph를 모두 지원** — [[Graph data model]]의 두 모델을 한 서비스에서
2. **각각에 맞는 질의 언어를 지원** — property graph는 **Gremlin**과 **openCypher**, RDF는 **SPARQL**

- **트랜잭션** — highly concurrent OLTP workloads over data graphs 지향. ACID와 well-defined
  transaction semantics 제공. 여러 mutation query를 한 트랜잭션으로 묶으면 atomic unit으로 성공/실패.
- **확장** — AWS가 인프라 운영을 대신하는 **관리형 scale 모델.**

> **"그래프 DB를 직접 운영하고 싶지 않지만 그래프 질의, graph API, 고가용성, 백업, 복제 같은 관리형
> 운영 이점을 원할 때 매력적인 선택지."**
> 그래프 DB라는 제품군 안에서 **운영 부담을 줄이는 관리형 선택지**에 가깝다.

## 잘 맞는 곳

- AWS 안에서 빠르게 관리형 그래프를 쓰고 싶음
- **RDF와 property graph를 둘 다 고려**
- 인프라 운영보다 서비스 통합이 더 중요
- AWS 기반의 고연결성 데이터 애플리케이션, 소셜 네트워킹

## GraphRAG 제품화의 저장 계층

**Neptune Analytics** 가 **AWS Bedrock Knowledge Bases GraphRAG**의 백엔드다. Bedrock Knowledge
Bases가 문서로부터 entity·fact·relationship을 자동 추출해 Neptune Analytics에 **그래프와 벡터를 함께
저장**하고, 검색 시 vector similarity search와 graph traversal을 결합한다.

> **GraphRAG가 연구 데모가 아니라 managed service로 운영 가능해졌다는 신호.**
> `https://aws.amazon.com/ko/blogs/machine-learning/announcing-general-availability-of-amazon-bedrock-knowledge-bases-graphrag-with-amazon-neptune-analytics`

## 링크

- [[Graph database]] — 제품 비교의 다섯 축
- [[Graph data model]] — Property Graph와 RDF
- [[GraphRAG]] — 제품화 절
- [[Neo4j]] · [[ArangoDB]] · [[JanusGraph]]
- 강의: [[AI Data Engineering (Fast Campus course)]]

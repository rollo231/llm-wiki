---
type: entity
title: Neo4j
area: [data-engineering]
aliases: [네오포제이, Cypher, openCypher]
tags: [data-engineering, graph, database, neo4j, cypher]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part3 Ch5 Graph databases]]", "[[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]]"]
---

# Neo4j

**native graph + Cypher 중심의 대표 [[Graph database|그래프 DB]].**

- **native graph database** — 저장 레벨부터 graph model을 중심에 둔 DBMS.
  nodes · relationships · properties를 직접 다룬다.
- **Cypher** — 선언형 그래프 질의 언어. 공식 문서는 *SQL과 유사하지만 graph에 최적화된 선언형 언어*로
  설명한다. 표준화된 변형이 **openCypher**.
- **운영 기능** — ACID transactions · cluster support · runtime failover · indexes · constraints.
  **관계 탐색뿐 아니라 운영 DBMS로서의 기능도 갖췄다.**
  기본 격리 수준은 read-committed, 필요 시 명시적 락으로 더 강한 격리 효과.
- **확장** — native graph storage와 클러스터링 중심. Enterprise·Infinigraph 방향에서 scale 확장.

## 잘 맞는 곳

- 관계와 경로 탐색이 **제품의 중심**
- Cypher 중심 생산성이 중요
- 운영형 그래프 애플리케이션을 빠르게 만들고 싶음
- 실시간 추천 · 사기 탐지(fraud) · 마스터 데이터 관리 · **[[GraphRAG]] 백엔드**

## GraphRAG 백엔드로

Part 3의 GraphRAG 사례 두 건이 모두 Neo4j 기반이다.

- **Technology Media Company** (Neo4j + Deloitte) — Neo4j GraphRAG + Amazon Bedrock으로 자연어 분석
  플랫폼. business entity 중심의 기업 분석 world model.
  `https://neo4j.com/customer-stories/technology-media-company`
- **DUCK / Kiku AI** — 고객 대화·리뷰·커뮤니티 데이터를 knowledge graph로 연결. 그래프를 foundation
  of facts로 두고 LLM이 그 위에서 reasoning.
  `https://neo4j.com/customer-stories/duck`

> ⚠️ 두 사례 모두 **Neo4j 자사 고객사례 페이지**가 출처다. 수치("time-to-insight 10배",
> "analyst time 92% 감소")는 벤더 마케팅 자료로 취급해야 한다.

## 다른 그래프 DB와의 자리

| | 강점 |
|---|---|
| **Neo4j** | 관계 탐색 중심 애플리케이션과 분석 기능 |
| [[Amazon Neptune]] | AWS 기반 관리형 그래프 운영 |
| [[ArangoDB]] | 문서 + 그래프 혼합형 프로젝트 |
| [[JanusGraph]] | 초대규모 분산 그래프 엔진 |

## 링크

- [[Graph database]] — 제품 비교의 다섯 축과 선택 기준
- [[Graph data model]] — Property Graph 모델, Cypher vs SPARQL
- [[GraphRAG]] · [[Knowledge graph]]
- 강의: [[AI Data Engineering (Fast Campus course)]]

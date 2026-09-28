---
type: source
title: AI DE 강의 3-15 그래프 DB 제품 비교
aliases: [AI DE 3-15]
tags: [AI-DE-강의, 그래프, 데이터베이스, 도구-비교]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part3/05. Ch5. 그래프 데이터베이스 실습.pdf"
---

# AI DE 강의 3-15 그래프 DB 제품 비교

[[AI 데이터 엔지니어링 강의]] Part 3의 마지막 소단원이다. Neo4j, Amazon Neptune, ArangoDB, JanusGraph를 저장 철학·그래프 모델·질의 언어·확장 방식·운영 방식으로 비교하고, 프로젝트 유형별로 무엇을 먼저 검토할지 정리한다. Part 3는 이 소단원으로 끝난다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 3 「시멘틱 & 컨텍스트 기반 데이터 설계」 |
| 덱 제목 | Ch5. 그래프 데이터베이스 실습: 2. Neo4j vs 다른 DB: 프로젝트별 선택 가이드 |
| 원본 파일 | `part3/05. Ch5. 그래프 데이터베이스 실습.pdf` p12–26 (15p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 (Part 3에서 가장 늦음) |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch5`, 소단원 번호 `2`는 표지 슬라이드 |

## 요약

### 01. 비교가 필요한 이유 (p14–15)

- 그래프 DB라고 모두 같은 방식으로 동작하지 않는다. native graph storage를 강점으로 두는 제품, 클라우드 관리형 운영을 강점으로 두는 제품, 문서·키값·그래프를 함께 다루는 멀티모델, 분산 스토리지 위에 얹는 graph engine이 있다.
- 강의의 표현: "Graph DB 선택은 그래프 모델 선택이 아니라 저장 구조, 질의 언어, 확장 방식, 운영 방식의 선택".
- 비교 기준 다섯 가지:
  1. 저장 철학: native graph인가, multi-model인가, engine + backend 구조인가
  2. 지원 그래프 모델: property graph 중심인가, RDF까지 포함하는가
  3. 질의 언어: Cypher, Gremlin, SPARQL, AQL 중 무엇인가
  4. 확장 방식: 단일 엔진 확장, 클러스터·[[샤딩]], 외부 분산 저장소 의존
  5. 운영 방식: 직접 운영형인가, 관리형 서비스인가

### 02. 대표 DB들 (p16–20)

| 제품 | 저장 철학 | 그래프 모델 | 질의 언어 | 강의가 드는 특징 |
|---|---|---|---|---|
| [[Neo4j]] | native graph | property graph | Cypher | ACID, cluster, runtime failover, index, constraint. 운영 DBMS 기능까지 갖춤 |
| [[Amazon Neptune]] | AWS 완전 관리형 | property graph + RDF | Gremlin, openCypher, SPARQL | 고가용성·백업·복제를 AWS가 맡음 |
| [[ArangoDB]] | native multi-model | 문서·키값·그래프 | AQL | named graph, edge collection, shortest path·k shortest paths·traversal을 AQL에서 수행 |
| [[JanusGraph]] | 분산 스토리지 위 graph engine | property graph | Gremlin(TinkerPop) | 저장 백엔드 Cassandra·HBase·BerkeleyDB, 인덱스 백엔드 Elasticsearch·Solr·Lucene, Hadoop 기반 OLAP |

### 03. 관점별 비교 (p21–22)

| 제품 | 확장성 | 질의 언어 |
|---|---|---|
| Neo4j | native graph storage와 클러스터링 중심. Enterprise와 Infinigraph 방향으로 확장 | Cypher 중심. 패턴 매칭과 선언형 질의 |
| Neptune | AWS가 인프라 운영을 대신하는 관리형 scale | openCypher·Gremlin·SPARQL을 한 서비스에서 |
| ArangoDB | 클러스터와 SmartGraphs의 value-based sharding으로 traversal locality를 높임 | AQL 하나로 문서 질의와 그래프 traversal 통합 |
| JanusGraph | Cassandra·HBase 같은 분산 저장소를 백엔드로 두고 scale-out을 storage layer에 기댐 | Gremlin 중심. TinkerPop 생태계에 익숙한 팀 |

### 04. 선택의 기준 (p23–26)

p25의 선택 가이드:

| 프로젝트 유형 | 예 | 우선 검토 |
|---|---|---|
| 관계형 recommendation·fraud·lineage·graph grounding | 실시간 추천, 사기 탐지, 마스터 데이터 관리, GraphRAG 백엔드 | Neo4j |
| AWS 안의 managed knowledge graph, RDF + property graph 혼합 | AWS 기반 고연결성 데이터 애플리케이션, 소셜 네트워킹 | Neptune |
| 문서형 데이터와 그래프 관계를 한 엔진에서 | 문서와 그래프 기능이 동시에 필요한 복합 애플리케이션 | ArangoDB |
| 초대규모 distributed graph, 기존 Cassandra·HBase 인프라 재활용 | 수십억 노드·엣지 규모의 소셜 그래프, 지식 그래프 | JanusGraph |

정리(p26): Neo4j는 관계 탐색 중심 애플리케이션과 분석, Neptune은 AWS 기반 관리형 운영, ArangoDB는 문서 + 그래프 혼합, JanusGraph는 초대규모 분산 그래프 엔진에 강점이 있다.

## 핵심

- 비교 축 다섯 가지는 쓸 만한 틀이다. 네 제품은 서로 다른 축에서 대표로 뽑혔다. native storage(Neo4j), 관리형 운영(Neptune), 멀티모델(ArangoDB), 외부 분산 저장소(JanusGraph). 같은 기준에서 순위를 매긴 비교가 아니라 축마다 한 제품씩 고른 구성이라는 점은 위키의 관찰이다.
- 선택 가이드의 첫 줄에 "GraphRAG 백엔드"가 들어 있다. Part 3 앞부분의 [[GraphRAG]]와 [[지식 그래프]]가 여기서 저장소 선택으로 이어진다([[AI DE 강의 3-13 GraphRAG 개념과 사례]]의 Neo4j 고객 사례들).
- 제품별 전문과 현재 상태(라이선스, 새 아키텍처, 릴리스)는 각 엔티티 페이지에 두고, 개념 비교는 [[그래프 데이터베이스]]에 둔다.

## 주의·결함

- ❗ 덱 제목의 「실습」에 해당하는 내용이 이 소단원에도 없다. 제품을 설치하거나 같은 질의를 네 제품에서 돌려 보는 슬라이드가 없고, 비교는 전부 정성적이다. 성능 수치나 벤치마크도 없다.
- 비교 기준에 라이선스와 비용이 없다. 실제 선택에서는 자주 결정적인 축인데, 네 제품은 이 점에서 크게 다르다. Neo4j는 Community와 Enterprise가 갈리고, ArangoDB는 3.12부터 소스가 Apache 2.0에서 BSL 1.1로 바뀌었다(2024-02 발표). 이 지적은 위키의 관찰이고 세부는 [[ArangoDB]]에 있다.
- 슬라이드 작성(2026-05) 시점 기준으로 낡거나 빠진 서술이 있다.
  - ArangoDB: 2025-10-23 회사명이 Arango로 바뀌고 "Arango AI Data Platform"이 나왔다(제품 DB 이름은 ArangoDB 그대로). SmartGraphs는 3.12.5부터 Community Edition에도 들어갔다. [https://arango.ai/blog/the-next-evolution-of-arango-powering-the-age-of-contextual-ai · https://docs.arango.ai/arangodb/stable/release-notes/version-3.12/whats-new-in-3-12/ , 2026-09-28 확인]
  - JanusGraph: 저장 백엔드 셋은 문서가 기본 지원으로 드는 셋과 같지만 전부는 아니다. 문서에는 ScyllaDB, Google Cloud Bigtable, InMemory도 있고, BerkeleyDB JE는 분산 DB가 아니라 주로 테스트용이라고 적는다. 최신 릴리스는 v1.1.0(2024-11-09)이고 그 뒤로 2년 가까이 새 릴리스가 없다. 저장소는 보관되지 않았고 커밋은 이어진다. [https://docs.janusgraph.org/ · https://api.github.com/repos/JanusGraph/janusgraph/releases , 2026-09-28 확인]
- ✅ Neo4j의 Infinigraph 언급(p21)은 맞다. 2025-09-04에 발표된 분산 아키텍처다([[Neo4j]]).
- ✅ Neptune이 Gremlin·openCypher·SPARQL을 지원한다는 서술은 맞다([[Amazon Neptune]]).
- 번호가 중복된다. p23과 p24가 둘 다 「프로젝트별 선택 가이드1」이고 p25가 「…2」다.
- p22의 ArangoDB 칸 끝에 `\` 문자가 남아 있다. 편집 잔재로 보인다.
- p15 비교 기준의 질의 언어 목록에 AQL이 들어 있어 소단원 1의 "대표 언어"(Cypher·Gremlin·GQL)와 다르다. AQL은 ArangoDB 전용 언어다.

## 관련

- 개념: [[그래프 데이터베이스]] · [[그래프 데이터 모델]] · [[지식 그래프]] · [[GraphRAG]]
- 엔티티: [[Neo4j]] · [[Amazon Neptune]] · [[ArangoDB]] · [[JanusGraph]]
- 이전 강의: [[AI DE 강의 3-14 그래프 DB의 특징]]
- 다음 강의: [[AI DE 강의 4-01 분산 처리의 등장과 도입 판단]] (Part 4)

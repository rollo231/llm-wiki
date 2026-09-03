---
type: source
title: AI DE Course - Part3 Ch5 Graph databases
area: [data-engineering]
aliases: [Part3 Ch5, 그래프 데이터베이스 실습, Graph DB의 특징, Neo4j vs 다른 DB]
tags: [data-engineering, course, fast-campus, graph, database, neo4j, neptune, arangodb, janusgraph]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part3/05. Ch5. 그래프 데이터베이스 실습.pdf (p1–26)"]
---

# AI DE Course - Part3 Ch5 Graph databases

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch5 "그래프 데이터베이스 실습".
원본(로컬): `raw/data-engineering/ai-de-course/part3/05. Ch5. 그래프 데이터베이스 실습.pdf` **p1–26** — **Part 3에서 가장 짧은 챕터.**
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> **분할 주의:** 소단원 2개(`1. Graph DB의 특징` p1–11 / `2. Neo4j vs 다른 DB: 프로젝트별 선택 가이드`
> p12–26)를 **한 장으로 합쳤다.** 26p이고 "엔진의 원리 → 제품 선택"으로 한 흐름이기 때문이다.

## ⚠️ 제목이 "실습"인데 실습이 없다

**코드도, 스크린샷도, 설치 절차도, Cypher 예제 실행도 없다.** 26페이지 전부 개념 설명과 제품 비교
슬라이드다. Part 3에서 유일하게 **제목이 내용을 오도하는** 챕터다.

(첫 슬라이드에 Ontotext **GraphDB** 로고가 붙어 있는데, 본문은 "GraphDB"를 일반명사로 쓴다.
제품 GraphDB에 대한 설명은 없다.)

## 소단원 1 — Graph DB의 특징

`01 GraphDB · 02 GraphDB의 핵심특징 · 03 Graph DB 질의언어 · 04 언제 RDB쓰고, 언제 GraphDB를 쓸까`

### 왜 RDB만으로는 불편해지나

테이블에 그래프 데이터를 저장하는 것은 **가능하다.** 회원-주문-상품-카테고리-추천 관계를 테이블로
분해할 수 있다. 문제는 **다단계 관계 탐색이 핵심이 되는 순간**이다.

> "친구의 친구", "이 계정과 연결된 다른 의심 계정", "이 테이블 변경의 downstream 영향" 같은 질문은
> **JOIN 체인이 길어진다.** self join, recursive join, 경로 탐색 로직이 누적되면서
> **쿼리 가독성이 떨어지고, 디버깅이 어려워지고, 설계 의도가 SQL 안에 묻힌다.**

마지막 항목("설계 의도가 SQL 안에 묻힌다")이 좋다 — Ch1의 "SQL이 비즈니스 로직이 된다"와 같은 진단의
그래프 버전이다.

### ⭐ 관계를 계산하느냐, 저장하느냐

> **"RDB는 관계를 foreign key + JOIN으로 계산하고, Graph DB는 관계를 node 간 연결로 저장한다."**
> **"RDB는 JOIN을 조합하고, Graph DB는 traversal을 수행한다."**

| | RDB | Graph DB |
|---|---|---|
| 엔터티 | 테이블/행 | node |
| 관계 | foreign key, bridge table, join table로 표현 | relationship/edge로 **저장**, 타입과 방향을 가짐 |
| 관계의 속성 | — | **관계도 속성을 가질 수 있음** |
| 탐색 | 인덱스 lookup → JOIN → 필요 시 recursive join | 시작 노드 선택 → 관계 타입을 따라 hop traversal → 패턴 매칭 |

> **"Graph Query는 어떤 테이블을 JOIN할까보다 어떤 관계를 몇 hop 따라갈까에 가깝다."**

### ⭐ "Graph DB가 빠르다"의 정확한 의미

> **"Graph DB는 모든 질의가 빠른 것이 아니라, 관계 중심 탐색에서 인접 노드 접근 비용을 낮추도록
> 설계됐다."**

**index-free adjacency** — 관계를 따라 다음 노드로 갈 때 매번 별도 JOIN/인덱스 탐색을 줄인다.

**하지만:** 전체 질의가 무조건 O(1)인 것은 아니다 · hop 수가 늘면 **touched subgraph가 커진다** ·
high-degree node가 많으면 **path explosion** 가능 · **selective predicate가 약하면 그래프도 느려진다.**

> **이 정직한 단서가 이 챕터에서 가장 값진 부분이다.** 그래프 DB 소개 자료 대부분이 "JOIN보다
> 1000배 빠르다"류로 끝나는데, 여기는 **어떤 조건에서 안 빠른지**를 말한다.

### Graph DB에도 트랜잭션이 있다

> **"Graph DB는 NoSQL이라서 트랜잭션이 없는 것이 아니라, 관계 중심 OLTP를 위해 트랜잭션을 제공한다."**

- **[[Neo4j]]** — 그래프·인덱스·스키마 접근을 트랜잭션에서 수행. **ACID 보장**, 기본 격리 수준
  read-committed, 필요 시 명시적 락.
- **[[Amazon Neptune]]** — highly concurrent OLTP workloads over data graphs 지향. ACID와
  well-defined transaction semantics. 여러 mutation query를 한 트랜잭션으로 묶으면 atomic unit.

**흔한 오해를 정면으로 다룬다.** [[NoSQL]] = 일관성 포기라는 도식이 그래프 DB에는 잘 맞지 않는다.

### 질의 언어

> **"SQL은 집합 결합, Graph Query는 패턴 매칭."**

openCypher(property graph용 선언형, SQL과 비슷해 친숙) · Gremlin(property graph용 traversal
language, **step-by-step**) · SPARQL(RDF graph용 pattern matching) · GQL.

> **"모델이 다르면 질의의 사고도 달라진다."**

### 언제 무엇을

> **"RDB와 Graph DB는 경쟁 관계가 아니라 질문 유형이 다른 두 엔진이다."**

| RDB가 적합 | Graph DB가 적합 |
|---|---|
| 정형 스키마가 안정적 | 질문의 핵심이 **"누가 누구와 어떻게 연결되는가"** |
| 강한 CRUD/집계/리포팅 중심 | self join / recursive join이 반복 |
| 재무·재고·주문 원장처럼 **record correctness**가 핵심 | fraud, recommendation, lineage, entity resolution |
| 복잡한 multi-hop traversal이 핵심이 아님 | relationship-heavy OLTP 또는 graph analytics |

## 소단원 2 — 제품 비교

`01 비교가 필요한 이유 · 02 대표 DB들 · 03 여러 관점들에서의 비교 · 04 선택의 기준`

### 다섯 축

> **"Graph DB라고 해서 모두 같은 방식으로 동작하지 않는다. 제품 철학의 차이."**
> **"Graph DB 선택은 그래프 모델 선택이 아니라 저장 구조, 질의 언어, 확장 방식, 운영 방식의 선택이다."**

저장 철학(native graph / multi-model / engine+backend) · 지원 그래프 모델(PG 중심 / RDF 포함) ·
질의 언어(Cypher / Gremlin / SPARQL / AQL) · 확장 방식(단일 엔진 / 클러스터·샤딩 / 외부 분산 저장소
의존) · 운영 방식(직접 / 관리형).

### 네 제품

| | 한 줄 | 확장 방식 |
|---|---|---|
| **[[Neo4j]]** | native graph + Cypher 중심의 대표 그래프 DB | native graph storage와 클러스터링 중심. Enterprise·Infinigraph 방향 |
| **[[Amazon Neptune]]** | 완전관리형. **Property Graph와 RDF를 모두 지원** | AWS가 인프라 운영을 대신하는 관리형 scale |
| **[[ArangoDB]]** | native multi-model — key-value·document·graph를 한 엔진에서. AQL 하나로 문서 질의와 graph traversal | 클러스터와 **SmartGraphs**로 value-based sharding하여 **traversal locality**를 높임 |
| **[[JanusGraph]]** | 단일 완성형 제품보다 **분산 스토리지 위에 올라가는 graph database engine** | 애초에 Cassandra/HBase를 백엔드로 두어 **scale-out을 storage layer에 기댐** |

**확장 방식 비교가 이 소단원의 핵심**이다 — 네 제품이 scale 문제를 네 가지 다른 층위에서 푼다.

### 프로젝트별 선택

| 상황 | 우선 검토 |
|---|---|
| 관계형 recommendation / fraud / lineage / graph grounding — 실시간 추천, 사기 탐지, 마스터 데이터 관리, **GraphRAG 백엔드** | [[Neo4j]] |
| AWS 안의 managed knowledge graph / RDF + property graph 혼합, 고연결성 데이터 애플리케이션, 소셜 네트워킹 | [[Amazon Neptune]] |
| 문서형 데이터와 그래프형 관계를 한 엔진에서 같이 다뤄야 하는 복합 애플리케이션 | [[ArangoDB]] |
| 초대규모 distributed graph, 기존 Cassandra/HBase 인프라 재활용, 수십억 노드/엣지 규모 | [[JanusGraph]] |

## 기존 페이지와의 대조

- **새 concept:** [[Graph database]] / **새 entity 4종:** [[Neo4j]] · [[Amazon Neptune]] ·
  [[ArangoDB]] · [[JanusGraph]]
- **[[NoSQL]]과 연결** — "Graph DB에도 트랜잭션이 있다"가 NoSQL=일관성 포기 도식을 교정한다.
  JanusGraph는 Wide-column 저장소(Cassandra/HBase) 위에 얹히므로 두 타입이 실제로 겹친다.
- **Ch2-2와 중복** — 질의 언어(Cypher/SPARQL) 설명이 반복된다.
- **[[Schema-centric data modeling]]** — "설계 의도가 SQL 안에 묻힌다"가 Ch1의 조인 폭발과 이어진다.

## 자료 품질

- ⚠️ **제목이 "실습"인데 실습이 전혀 없다.** Part 3의 가장 큰 라벨 오류.
- 4개 제품 로고 콜라주 이미지가 슬라이드 대부분에 반복 배치돼 텍스트를 가린다(p14~p26).
- 중복 슬라이드는 없음. 26페이지가 얇지만 낭비는 적다.
- Neo4j·Neptune·ArangoDB·JanusGraph 서술이 **공식 문서 문구를 그대로 옮긴 티가 난다**
  ("native graph database, ACID transactions, cluster support, runtime failover" 등) — 강의도
  "Neo4j 공식 문서는 …를 명시하고"라고 밝힌다. **벤더 문서 기반이라는 뜻이므로 비교의 중립성은
  기대하기 어렵다.**
- 출처 없는 수치 없음.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Graph database]] · [[Graph data model]] · [[NoSQL]] ·
  [[Schema-centric data modeling]] · [[GraphRAG]]
- 도구: [[Neo4j]] · [[Amazon Neptune]] · [[ArangoDB]] · [[JanusGraph]]
- 앞: [[AI DE Course - Part3 Ch4 GraphRAG variants and products]] — **Part 3의 마지막 챕터**
- 다음 파트: [[AI Data Engineering (Fast Campus course)]] Part 4 (실시간 & 대규모 데이터 분산처리 설계)

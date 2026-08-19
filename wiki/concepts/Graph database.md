---
type: concept
title: Graph database
area: [data-engineering]
aliases: [그래프 DB, 그래프 데이터베이스, Graph DB, index-free adjacency, GraphDB, Apache TinkerPop, TinkerPop, Apache HugeGraph, HugeGraph]
tags: [data-engineering, graph, database, neo4j, traversal, oltp]
created: 2026-08-01
updated: 2026-08-19
sources: ["[[AI DE Course - Part3 Ch5 Graph databases]]"]
---

# Graph database

**[[Graph data model|그래프 모델]]을 저장하고 질의하는 엔진.** 모델이 "무엇을 표현하나"라면 이
페이지는 **"어떻게 저장하고 어떻게 따라가나"** 다.

## 왜 RDB만으로는 불편해지나

테이블에 그래프 데이터를 저장하는 것은 **가능하다.** 회원–주문–상품–카테고리–추천 관계를 테이블로
분해할 수 있다. 문제는 **다단계 관계 탐색이 핵심이 되는 순간**이다.

"친구의 친구", "이 계정과 연결된 다른 의심 계정", "이 테이블 변경의 downstream 영향" 같은 질문은
JOIN 체인이 길어진다. self join · recursive join · 경로 탐색 로직이 누적되면서:

- 쿼리 가독성이 떨어지고
- 디버깅이 어려워지고
- **설계 의도가 SQL 안에 묻힌다**

> ⚠️ **"JOIN이 많아지면 Graph를 쓴다"는 기준이 아니다.**
> 단순 JOIN 횟수가 아니라 **문제의 의미가 다단계 연결 탐색일 때**가 기준이다.
>
> | RDB가 잘하는 질문 | Graph가 더 자연스러운 질문 |
> |---|---|
> | 어제 주문 건수는 몇 건인가 | 이 지표가 깨졌을 때 어떤 잡과 어떤 소스까지 영향이 전파되는가 |
> | 카테고리별 매출 합계는 얼마인가 | 이 상품을 본 사용자와 유사 행동을 보인 다른 사용자들은 무엇을 구매했는가 |
> | 상위 10개 상품은 무엇인가 | 같은 전화번호·기기·주소를 공유한 계정 묶음은 무엇인가 |

## ⭐ 핵심 차이 — 관계를 계산하느냐, 저장하느냐

| | **RDB** | **Graph DB** |
|---|---|---|
| 엔터티 | 테이블/행 | node |
| 관계 | foreign key, bridge table, join table로 **표현** | relationship/edge로 **저장** |
| 관계의 지위 | 질의 시점에 JOIN으로 **다시 연결** | **관계 자체가 저장 대상**이며 타입과 방향을 가짐 |
| 관계의 속성 | 별도 컬럼/테이블 필요 | **관계도 속성을 가질 수 있음** |
| 탐색 방식 | 인덱스 lookup → JOIN → (필요 시) recursive join | 시작 노드 선택 → 관계 타입을 따라 **hop traversal** → 패턴 매칭 |

> **RDB는 JOIN을 조합하고, Graph DB는 traversal을 수행한다.**

## "Graph DB가 빠르다"의 정확한 의미

> ⭐ **모든 질의가 빠른 것이 아니다. 관계 중심 탐색에서 인접 노드 접근 비용을 낮추도록 설계됐을
> 뿐이다.**

**index-free adjacency** — 관계를 따라 다음 노드로 갈 때 매번 별도 JOIN/인덱스 탐색을 하지 않으므로
연결된 데이터 탐색에 유리하다.

**하지만 전체 질의가 무조건 O(1)인 것은 아니다:**

- hop 수가 늘면 **touched subgraph가 커진다**
- high-degree node가 많으면 **path explosion** 가능
- selective predicate가 약하면 그래프도 느려진다

이 정직한 단서가 중요하다 — 그래프를 은탄환으로 팔지 않는다.

## Graph DB에도 트랜잭션이 있다

**"NoSQL이라서 트랜잭션이 없다"는 오해다.** 관계 중심 OLTP를 위해 트랜잭션을 제공한다.

- **[[Neo4j]]** — 그래프·인덱스·스키마 접근을 트랜잭션에서 수행. **ACID 보장**, 기본 격리 수준은
  read-committed, 필요 시 명시적 락으로 더 강한 격리 효과.
- **[[Amazon Neptune]]** — highly concurrent OLTP workloads over data graphs 지향. ACID와
  well-defined transaction semantics 제공. 여러 mutation query를 한 트랜잭션으로 묶으면 atomic
  unit으로 성공/실패.

→ ACID 자체는 [[Schema-centric data modeling]] 참고. **관계형만의 것이 아니다.**

## 질의 언어

**SQL은 집합 결합, Graph Query는 패턴 매칭.** Graph Query 언어는 JOIN 순서보다 **그래프 패턴을
표현**하는 데 초점이 있다.

| 언어 | 모델 | 성격 |
|---|---|---|
| **openCypher** | property graph | 선언형. SQL과 비슷한 형태라 개발자에게 친숙 |
| **Gremlin** | property graph | traversal language. **step-by-step**으로 그래프를 따라감 |
| **SPARQL** | RDF | graph pattern matching. RDF triple과 named graph 질의에 적합 |
| **GQL** | — | 표준화 흐름 |

**언어가 여러 개인 이유는 모델이 다르면 질의의 사고도 달라지기 때문이다.**
→ Cypher vs SPARQL 예시는 [[Graph data model]].

## 언제 RDB를 쓰고 언제 Graph DB를 쓰나

> **경쟁 관계가 아니라 질문 유형이 다른 두 엔진이다.**

| **RDB가 적합** | **Graph DB가 적합** |
|---|---|
| 정형 스키마가 안정적 | 질문의 핵심이 "누가 누구와 어떻게 연결되는가" |
| 강한 CRUD/집계/리포팅 중심 | self join / recursive join이 반복됨 |
| 재무·재고·주문 원장처럼 **record correctness**가 핵심 | fraud, recommendation, lineage, entity resolution이 중요 |
| 복잡한 multi-hop traversal이 핵심이 아님 | relationship-heavy OLTP 또는 graph analytics가 필요 |

## ⭐ 질의 언어의 표준 계층 — TinkerPop

**Apache TinkerPop**은 특정 데이터베이스가 아니라 **Gremlin 질의 언어를 중심으로 한 표준**이다 —
*"여러 그래프 저장소가 같은 질의 언어를 쓰게 만드는 표준."* 정점·간선 모델과 API를 정의하고,
**온라인 탐색과 대규모 그래프 분석에 쓰는 API 모델을 함께** 제공한다.
⚠️ **완결된 분산 DB 제품이 아니다.**

**Apache HugeGraph**가 그 표준을 구현한 분산 그래프 DB다 — 스키마를 정한 뒤 정점·간선을 넣고
경로·이웃·패턴을 조회하며, **OLTP(온라인 탐색)와 OLAP(배치 그래프 분석)를 함께** 지원한다.
지식 그래프·추천·보안 분석처럼 **관계 탐색이 곧 서비스**인 팀이 검토한다. → [[Knowledge graph]]

⭐ **이 "표준/이식 계층"은 데이터 스택에서 반복되는 패턴이다** — 그래프 질의의 TinkerPop, SQL 파싱의
[[Apache Calcite]], 처리 엔진의 Beam([[Batch and stream processing]]), 메모리의 Arrow
([[Columnar and in-memory data formats]]), 저장소의 OpenDAL. **하나같이 설치 목록에는 잘 오르지 않고,
"엔진을 바꿔도 같은 것을 쓸 수 있는가"를 파는 계층이다.**

⚠️ 그리고 아래 §언제 RDB를 쓰고 언제 Graph DB를 쓰나와 같은 경고가 붙는다 — *"모든 관계형 문제를
그래프로 옮길 필요는 없다. **키가 분명한 조회는 [[Apache Cassandra]]·관계형 DB가, 집계 리포트는
OLAP·웨어하우스가** 더 적합하다."* → [[Consumption layer]]

## 제품 비교 — 다섯 축

**Graph DB라고 해서 모두 같은 방식으로 동작하지 않는다.** 제품 철학이 다르다.

| 축 | 갈림 |
|---|---|
| **저장 철학** | native graph인가 · multi-model인가 · engine + backend 구조인가 |
| **지원 그래프 모델** | property graph 중심인가 · RDF까지 포함하는가 |
| **질의 언어** | Cypher · Gremlin · SPARQL · AQL 중 무엇 |
| **확장 방식** | 단일 엔진 확장 · 클러스터/샤딩 · 외부 분산 저장소 의존 |
| **운영 방식** | 직접 운영형 · 관리형 서비스 |

> **"Graph DB 선택은 그래프 모델 선택이 아니라 저장 구조·질의 언어·확장 방식·운영 방식의 선택이다."**

| 제품 | 한 줄 | 강점 |
|---|---|---|
| **[[Neo4j]]** | native graph + Cypher 중심의 대표 그래프 DB | 관계 탐색 중심 애플리케이션과 분석 기능 |
| **[[Amazon Neptune]]** | 완전관리형 그래프 DB 서비스 (PG + RDF 모두) | AWS 기반 관리형 그래프 운영 |
| **[[ArangoDB]]** | key-value·document·graph를 한 엔진에서 (native multi-model) | 문서 + 그래프 혼합형 프로젝트 |
| **[[JanusGraph]]** | 분산 스토리지 위에 올라가는 graph engine | 초대규모 분산 그래프 엔진이 필요한 프로젝트 |

**확장 방식이 특히 갈린다** — Neo4j는 native graph storage와 클러스터링 중심(Enterprise·Infinigraph
방향), Neptune은 AWS가 인프라 운영을 대신하는 관리형 scale, ArangoDB는 클러스터와 SmartGraphs로
value-based sharding하여 **traversal locality**를 높이는 방식, JanusGraph는 애초에 Cassandra/HBase
같은 분산 저장소를 백엔드로 두고 **scale-out을 storage layer에 기댄다.**

### 프로젝트별 우선 검토

| 상황 | 우선 검토 |
|---|---|
| 실시간 추천, 사기 탐지, 마스터 데이터 관리, **GraphRAG 백엔드** | [[Neo4j]] |
| AWS 기반 고연결성 데이터 애플리케이션, RDF + property graph 혼합, 소셜 네트워킹 | [[Amazon Neptune]] |
| 문서형 데이터와 그래프형 관계를 한 엔진에서 같이 다뤄야 하는 복합 애플리케이션 | [[ArangoDB]] |
| 수십억 개 노드/엣지 규모의 초대형 소셜 그래프·지식그래프, 기존 Cassandra/HBase 재활용 | [[JanusGraph]] |

## 관련 페이지

- [[Graph data model]] — 무엇을 표현하나 (node/edge/property, PG vs RDF)
- [[Knowledge graph]] · [[Ontology]] — 그 위에 얹는 의미 계층
- [[GraphRAG]] — 그래프 DB가 retrieval 백엔드가 되는 자리
- [[NoSQL]] — 4타입 중 Graph의 자리, 그리고 분산 운영의 현실
- [[Schema-centric data modeling]] — 조인 폭발이라는 출발점

## 출처

- [[AI DE Course - Part3 Ch5 Graph databases]]

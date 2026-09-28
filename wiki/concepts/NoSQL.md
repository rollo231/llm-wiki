---
type: concept
title: NoSQL
aliases: [Not only SQL, 키-값 저장소, Key-Value Store, 문서 저장소, Document Store, 와이드 컬럼 저장소, Wide-column Store, 핫 파티션, Hot partition, Aggregate 지향, Aggregate-oriented, 집합 지향 모델, 액세스 패턴 중심 설계]
tags: [저장, 분산, 정합성]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 3-02 RDBMS의 한계와 NoSQL]]"
  - "[[AI DE 강의 4-02 CAP 정리와 분산 시스템의 한계]]"
  - "[[DB 면접 5 NoSQL과 RDBMS 비교]]"
---

# NoSQL

관계형 모델과 강한 트랜잭션 대신 더 단순한 데이터 모델, 선택 가능한 일관성, 쉬운 샤딩·복제를 택한 저장소들의 묶음이다. [[AI DE 강의 3-02 RDBMS의 한계와 NoSQL]]은 이것을 [[관계형 데이터베이스]]의 세 한계(스케일업, 스키마 변경, 분산 일관성 비용)에 대한 응답으로 소개하고, 곧바로 "NoSQL은 확장성을 자동 제공하지 않는다"(p37)는 반론을 붙인다.

## 등장 배경

강의는 새 서비스가 요구한 네 가지 변화를 든다(p29). 트래픽 급증으로 수평 확장이 기본 전제가 됐고, 반정형·비정형 이벤트가 폭증해 스키마가 자주 바뀌고, 24/7 가용성 때문에 부분 실패를 허용해야 하고, 스키마 마이그레이션 비용이 개발 속도의 병목이 됐다. 예로 Facebook·Instagram의 피드 이벤트와 LinkedIn의 관계 탐색을 든다(p28).

## 네 타입

| 타입 | 대표 | 데이터 모델 | 맞는 워크로드 |
|---|---|---|---|
| Key-Value | [[Redis]], DynamoDB | 키 하나에 값 하나 | 캐시, 세션, 랭킹, 단순 조회 |
| Document | MongoDB, Couchbase, DocumentDB | JSON 문서, 스키마 유연 | 필드 구성이 자주 바뀌거나 중첩된 데이터 |
| Wide-column | Cassandra, HBase, ScyllaDB | 파티션 키 아래 여러 열을 가진 행 | 대량 쓰기, 시계열·로그, 타임라인 |
| Graph | Neo4j, Amazon Neptune | 노드·엣지·속성 | 다단계 관계 탐색 |

표는 강의(p30–34)를 따랐고 "데이터 모델" 열의 wide-column 설명은 아래 정정을 반영해 위키가 고쳐 쓴 것이다. 그래프는 Part 3의 본론이라 [[그래프 데이터 모델]]과 [[그래프 데이터베이스]]에서 따로 다룬다.

### ❗ Wide-column은 열 기반 저장이 아니다

강의는 wide-column을 "열(Column) 기반 저장. 쓰기 성능에 최적화"(p33)라고 설명한다. 이름에 column이 들어 있어 생기는 흔한 혼동이다.

- Cassandra 문서는 자신을 "a partitioned wide-column storage model"로 부른다. 문서가 이 말을 풀어 쓰지는 않는데, 파티션 키로 데이터를 나누고 한 파티션 안에 여러 행을 모아 두는 모델로 읽힌다(이 풀이는 위키의 것이다). 같은 문서가 설계 목표로 "Linear throughput increase with each additional processor"를 적으므로, 노드 추가 시 선형 확장이라는 강의 서술은 맞다. [https://cassandra.apache.org/doc/latest/cassandra/architecture/overview.html , 2026-09-28 확인]
- Kleppmann의 『Designing Data-Intensive Applications』 3장은 Cassandra·HBase의 column family를 두고 column-oriented라고 부르면 크게 오해를 산다고 쓴다. 한 column family 안에서는 한 행의 모든 열을 row key와 함께 저장하고 열 압축도 쓰지 않으므로 여전히 대체로 행 지향이라는 것이다. 이 서술은 검색으로 찾은 2차 발췌로 확인했고 책 원문은 열어 보지 않았다(2026-09-28).

그래서 Parquet 같은 분석용 열 기반 저장([[행 기반과 열 기반 저장]])과 wide-column은 다른 축이다. "쓰기 최적화"라는 강의 서술은 맞다. Cassandra의 저장 엔진 문서가 "optimized for high performance, write-oriented workloads"라고 쓰고, 그 이유로 B-tree 대신 append-only 방식의 Log Structured Merge(LSM) 트리를 든다. 쓰기 최적화는 열 배치가 아니라 이 쓰기 경로에서 온다. [https://cassandra.apache.org/doc/latest/cassandra/architecture/storage-engine.html , 2026-09-28 확인]

## 확장성은 자동이 아니다

[[AI DE 강의 3-02 RDBMS의 한계와 NoSQL]] 소단원 3(p37–44)의 운영 현실 세 가지다.

1. 파티션 키가 시스템을 결정한다. 한 번 정하면 바꾸기 어렵다. 특정 키에 트래픽이 몰리는 핫 파티션, 시간 기반 키로 최신 파티션에만 쓰기가 몰리는 경우, 일부 노드가 과부하되고 노드를 추가해도 병목이 풀리지 않는다.
2. 일관성 완화의 비용은 애플리케이션이 진다. 재시도 설계, 중복 처리(idempotency), 순서 꼬임 처리, 보정 배치 운영(p40). 이 목록은 Part 1이 CDC·스트림 처리에서 at-least-once 전달 때문에 요구한 것과 거의 같다([[멱등성]]). 원인은 다르지만(저장소의 일관성 모델 대 전달 보장) 대응은 같다. 이 연결은 위키의 관찰이다.
3. 백업·복구·관측이 어렵다. 여러 노드의 백업 시점을 맞추기 어렵고, 리밸런싱 중 성능이 떨어지고, 장애가 전체가 아닌 일부 파티션에서 나타난다. 봐야 할 지표는 partition hotness/skew, replication lag, timeout, leader change다. "운영 포인트가 줄어드는 것이 아니라 분산됨"(p42).

## 설계 방식: 데이터 중심과 액세스 패턴 중심

[[DB 면접 5 NoSQL과 RDBMS 비교]] Q1-1(p75)의 Gold 답은 설계 순서가 반대라고 정리한다. RDBMS는 데이터 중심으로, 먼저 정규화해 중복을 없애고 나중에 어떤 쿼리든 조인으로 대응한다. NoSQL은 액세스 패턴 중심으로, "어떤 쿼리를 날릴 것인가"를 먼저 정하고 그에 맞게 비정규화해 저장한다. 조인이 없으므로 필요한 데이터를 한 번의 조회로 가져오게 설계한다. 위 「확장성은 자동이 아니다」의 파티션 키 선택이 바로 이 액세스 패턴 설계의 한 부분이다. 이 연결은 위키가 했다.

### Aggregate 지향

같은 자료의 Q1-3(p81)은 NoSQL이 "집합 지향 모델"이라 연관 데이터가 함께 저장되고, 그래서 다른 샤드에서 조인할 필요가 없어 스케일 아웃에 유리하다고 쓴다. 원어는 Martin Fowler와 Pramod Sadalage(『NoSQL Distilled』)의 aggregate-oriented다. 한국어로는 「애그리거트」로 옮기는 경우가 많고 「집합」은 set과 헷갈린다. 번역에 대한 평은 위키의 것이다.

Fowler는 네 부류 가운데 앞의 셋만 aggregate 지향으로 묶는다: "key-value, document, column-family, and graph. Looking at this list, there's a big similarity between the first three". [https://martinfowler.com/bliki/AggregateOrientedDatabase.html , 2026-09-28 확인] 그래프 DB는 관계 자체를 저장하므로 aggregate 단위로 나누기 어렵다. 그래서 "NoSQL은 샤딩이 쉽다"는 그래프 DB에는 해당하지 않는다([[샤딩]] · [[그래프 데이터베이스]]).

### ❗ "NoSQL은 변경이 적은 데이터에 맞다"는 틀린 일반화

같은 자료의 Q1(p72) Gold 답은 RDBMS가 "변경이 빈번"한 데이터에, NoSQL이 "조인이 적고 변경이 적은 데이터"에 맞다고 쓴다. 조인이 적다는 쪽은 맞지만 변경 빈도는 기준이 되지 못한다. 위 「네 타입」의 정정에서 본 것처럼 Cassandra는 append-only LSM 트리로 쓰기에 최적화되어 있다("The core storage engine consists of memtables for in-memory data and immutable SSTables"). [https://cassandra.apache.org/doc/latest/cassandra/architecture/storage-engine.html , 2026-09-28 확인] 선택 기준은 변경 빈도가 아니라 액세스 패턴이 미리 정해지는가, 조인과 여러 행에 걸친 트랜잭션이 얼마나 필요한가다. 이 기준은 위키가 자료의 Q1-1 답에서 끌어온 것이다.

### RDBMS도 Scale-Out을 한다

"RDBMS는 Scale-Up만, Scale-Out은 NoSQL만"을 자료는 "흔한 오해"로 부른다(p77). 읽기는 Read Replica로([[복제]]), 쓰기는 샤딩으로([[샤딩]]) 나눌 수 있고, 다만 샤드를 넘는 조인·트랜잭션 때문에 "불가능한 건 아니지만 비용이 크다"(p78). 이 결론은 [[AI DE 강의 3-02 RDBMS의 한계와 NoSQL]]이 RDBMS의 첫 한계로 든 스케일업 의존과 방향이 같고, 강도가 다르다. AI DE 강의는 한계를 강조하고, 면접 자료는 가능하다는 쪽을 강조한다. 이 비교는 위키가 했다.

## CAP

강의는 일관성 완화의 trade-off를 설명하는 대표 개념으로 CAP를 든다(p41). 네트워크 단절(Partition)은 피할 수 없고, 그때 일관성(C)과 가용성(A)을 동시에 완벽히 만족시키기 어렵다는 것이다. 강의는 C를 "모든 노드가 같은 시점에 같은 값을 봄"으로 풀었는데, 원래 정의(linearizability)를 비형식적으로 옮긴 부정확한 풀이다. 같은 슬라이드가 C·A·P를 나란한 세 특성으로 나열해 "셋 중 둘을 고른다"로 읽힐 여지도 남긴다.

Part 4의 [[AI DE 강의 4-02 CAP 정리와 분산 시스템의 한계]]가 CAP를 소단원 하나로 다시 다루며 C를 single-copy consistency로 정의하고 Brewer의 2012년 정정까지 옮긴다. 정의, 정정, 제품을 CP·AP로 분류하는 일의 문제는 [[CAP 정리]]에 모았다.

## 저장 기술과 의미는 다른 문제

강의는 NoSQL 이야기를 "RDBMS/NoSQL은 저장·확장·성능 문제를 다룰 뿐, 이 데이터가 무엇을 의미하는가는 답하지 못한다"(p45)로 닫고 [[시맨틱 계층]]으로 넘어간다.

## 관련

- [[관계형 데이터베이스]] · [[그래프 데이터베이스]] · [[행 기반과 열 기반 저장]] · [[멱등성]] · [[시맨틱 계층]] · [[샤딩]] · [[복제]] · [[CAP 정리]]
- 면접 자료: [[DB 면접 5 NoSQL과 RDBMS 비교]]
- [[피처 스토어]]: 온라인 스토어로 Redis·DynamoDB·Cassandra가 나온다([[AI DE 강의 2-10 Feature Store 기본 개념]])

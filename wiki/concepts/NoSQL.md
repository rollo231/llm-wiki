---
type: concept
title: NoSQL
aliases: [Not only SQL, 키-값 저장소, Key-Value Store, 문서 저장소, Document Store, 와이드 컬럼 저장소, Wide-column Store, CAP, CAP 정리, CAP theorem, 핫 파티션, Hot partition]
tags: [저장, 분산, 정합성]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 3-02 RDBMS의 한계와 NoSQL]]"
---

# NoSQL

관계형 모델과 강한 트랜잭션 대신 더 단순한 데이터 모델, 선택 가능한 일관성, 쉬운 샤딩·복제를 택한 저장소들의 묶음이다. [[AI DE 강의 3-02 RDBMS의 한계와 NoSQL]]은 이것을 [[관계형 데이터베이스]]의 세 한계(스케일업, 스키마 변경, 분산 일관성 비용)에 대한 응답으로 소개하고, 곧바로 "NoSQL은 확장성을 자동 제공하지 않는다"(p37)는 반론을 붙인다.

## 등장 배경

강의는 새 서비스가 요구한 네 가지 변화를 든다(p29). 트래픽 급증으로 수평 확장이 기본 전제가 됐고, 반정형·비정형 이벤트가 폭증해 스키마가 자주 바뀌고, 24/7 가용성 때문에 부분 실패를 허용해야 하고, 스키마 마이그레이션 비용이 개발 속도의 병목이 됐다. 예로 Facebook·Instagram의 피드 이벤트와 LinkedIn의 관계 탐색을 든다(p28).

## 네 타입

| 타입 | 대표 | 데이터 모델 | 맞는 워크로드 |
|---|---|---|---|
| Key-Value | Redis, DynamoDB | 키 하나에 값 하나 | 캐시, 세션, 랭킹, 단순 조회 |
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

## CAP

강의는 일관성 완화의 trade-off를 설명하는 대표 개념으로 CAP를 든다(p41). 네트워크 단절(Partition)은 피할 수 없고, 그때 일관성(C)과 가용성(A)을 동시에 완벽히 만족시키기 어렵다는 것이다.

두 가지를 보충한다.

- C의 정의. 강의는 "모든 노드가 같은 시점에 같은 값을 봄"이라고 풀지만, Gilbert–Lynch(2002)의 증명에서 C는 atomic, 곧 linearizable consistency다. 모든 연산에 전체 순서가 있고 각 연산이 한 시점에 일어난 것처럼 보여야 한다. 쉽게 말해 읽기가 가장 최근에 완료된 쓰기를 보고, 시스템이 사본 하나처럼 동작한다. [Gilbert & Lynch, "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services", SIGACT News 33(2), 2002, https://www.comp.nus.edu.sg/~gilbert/pubs/BrewersConjecture-SigAct.pdf , 2026-09-28 확인]
- "셋 중 둘" 틀. Brewer 본인이 2012년에 "The '2 of 3' formulation was always misleading"이라고 썼다. 파티션이 없을 때는 C와 A를 함께 가질 수 있고, 선택은 파티션이 났을 때만 생긴다. [Eric Brewer, "CAP Twelve Years Later: How the 'Rules' Have Changed", IEEE Computer, 2012-02, https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/ , 2026-09-28 확인] 강의도 "네트워크 단절을 완전히 피할 수 없고 이 상황에서" C와 A를 동시에 완벽히 만족시키기 어렵다고 써서(p41) 선택을 파티션 상황에 둔다. 다만 같은 슬라이드가 C·A·P를 나란한 세 특성으로 나열해, "셋 중 둘을 고른다"로 읽힐 여지를 남긴다.

## 저장 기술과 의미는 다른 문제

강의는 NoSQL 이야기를 "RDBMS/NoSQL은 저장·확장·성능 문제를 다룰 뿐, 이 데이터가 무엇을 의미하는가는 답하지 못한다"(p45)로 닫고 [[시맨틱 계층]]으로 넘어간다.

## 관련

- [[관계형 데이터베이스]] · [[그래프 데이터베이스]] · [[행 기반과 열 기반 저장]] · [[멱등성]] · [[시맨틱 계층]]
- [[피처 스토어]]: 온라인 스토어로 Redis·DynamoDB·Cassandra가 나온다([[AI DE 강의 2-10 Feature Store 기본 개념]])

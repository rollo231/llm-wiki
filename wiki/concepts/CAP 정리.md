---
type: concept
title: CAP 정리
aliases: [CAP, CAP theorem, CAP 이론, 최종 일관성, Eventual consistency]
tags: [분산, 정합성]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 3-02 RDBMS의 한계와 NoSQL]]"
  - "[[AI DE 강의 4-02 CAP 정리와 분산 시스템의 한계]]"
  - "[[DB 면접 5 NoSQL과 RDBMS 비교]]"
---

# CAP 정리

네트워크 분할(Partition)이 일어날 수 있는 분산 저장소는 분할이 났을 때 일관성(Consistency)과 가용성(Availability)을 동시에 강하게 보장할 수 없다는 정리다. [[AI DE 강의 4-02 CAP 정리와 분산 시스템의 한계]]는 CAP를 "모든 분산 시스템의 모든 속성을 다루는 만능 법칙"이 아니라 "네트워크 분할이 가능한 환경에서 읽기/쓰기 서비스가 어디까지 강한 보장을 할 수 있는가를 묻는 정리"로 소개한다(p36). 더 넓은 맥락은 [[분산 시스템]]에 있다.

## 기원

- 2000년 Eric Brewer가 PODC 기조연설에서 추측(conjecture)으로 제시했다(p37).
- 2002년 Gilbert와 Lynch가 형식화해 증명했다. 강의가 쓰는 safety/liveness 틀(일관성은 "나쁜 일이 일어나지 않는다"는 안전성, 가용성은 "결국 좋은 일이 일어난다"는 생명성, p37)은 Brewer 2012 글에는 없고 Gilbert와 Lynch의 2012년 글 「Perspectives on the CAP Theorem」의 것이다. 이 출처 구분은 위키가 확인한 것이다. [Gilbert & Lynch, IEEE Computer 45(2), 2012, https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf : "Consistency (as defined in the CAP Theorem) is a classic safety property… classic liveness property: eventually, every request receives a response." 2026-09-28 확인]

## 세 성질의 정의

| 성질 | 정의 | 강의 |
|---|---|---|
| C | 원 증명에서는 atomic(= linearizable) 일관성. 모든 연산이 요청과 응답 사이의 한 시점에 일어난 것처럼 보인다. 시스템이 사본 하나처럼 동작한다 | "single-copy consistency", 모든 클라이언트가 하나의 최신 복사본을 보는 것에 가까운 의미(p38) |
| A | 장애가 나지 않은 노드가 받은 모든 요청은 결국 응답을 받는다. 실패 응답이라도 응답이어야 한다 | 너무 늦은 응답은 응답이 없는 것과 같다(p39) |
| P | 네트워크가 메시지를 임의로 잃거나 늦출 수 있다는 가정. 서비스의 태도가 아니라 환경의 속성이다 | 메시지 손실과 지연은 구별하기 어렵다(p40) |

[Gilbert & Lynch 2012: "A web service is atomic if, for every operation, there is a single instant in between the request and the response at which the operation appears to occur." 같은 URL, 2026-09-28 확인]

### Part 3와 Part 4의 정의

[[AI DE 강의 3-02 RDBMS의 한계와 NoSQL]]는 C를 "모든 노드가 같은 시점에 같은 값을 봄"(p41)으로 풀었다. 흔히 쓰는 비형식적 풀이라 틀렸다기보다 부정확하다. linearizability는 노드들의 상태가 한순간에 같다는 조건이 아니라 연산의 순서와 실시간성에 대한 조건이기 때문이다. Part 4의 "single-copy consistency"(p38)가 원래 정의에 더 가깝다. 코스가 같은 개념을 두 번 정의하면서 서로를 참조하지 않는다는 점은 [[AI 데이터 엔지니어링 강의]]의 경향과 같다. 두 정의의 비교는 위키가 한 것이다.

## "셋 중 둘"이 아니다

Brewer는 2012년 글에서 자신의 원래 표현을 고쳤다. 강의 p44–45가 이 정정을 옮긴다.

- "The '2 of 3' formulation was always misleading." 분할은 고르는 것이 아니라 일어나는 사고다.
- 분할은 드물다. 분할이 없을 때는 C와 A를 포기할 이유가 없다.
- 선택은 시스템 전체가 아니라 아주 세밀한 단위(서브시스템, 연산, 데이터)에서 일어난다.
- 세 성질은 이분법이 아니라 정도의 문제다("All three properties are more continuous than binary").

[Eric Brewer, "CAP Twelve Years Later: How the 'Rules' Have Changed", IEEE Computer, 2012-02, https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/ , 2026-09-28 확인]

## CAP의 C는 ACID의 C가 아니다

ACID의 C는 unique key 같은 데이터베이스 규칙, 곧 불변식(invariant)을 지키는 것이고, CAP의 C는 single-copy consistency다. Brewer는 "the C in CAP refers only to single-copy consistency, a strict subset of ACID consistency"라고 쓴다. 분할에서 복구할 때 ACID 쪽 불변식도 따로 복원해야 할 수 있고, serializable 격리는 통신이 필요해 분할 중에는 그대로 유지하기 어렵다(p46, 같은 출처). 그래서 "우리 DB는 ACID니까 CAP의 C도 만족한다"는 말은 성립하지 않는다. ACID는 [[관계형 데이터베이스]]에서 다룬다.

## ❗ 제품을 CA·CP·AP로 분류하기

강의 p41–43은 CAP 조합마다 제품 예시를 단다. 위키가 1차 자료와 대조한 결과는 다음과 같다(2026-09-28 확인).

| 강의 분류 | 제품 | 판정 |
|---|---|---|
| CA | 전통 RDBMS (Oracle, MySQL, PostgreSQL) | ⚠️ 단일 노드는 분산 시스템이 아니어서 CAP가 다루는 대상이 아니다. 복제를 붙이는 순간 분할이 나면 C나 A를 골라야 한다. 강의 스스로도 p41에 "분산 시스템에서는 구현하기 어려운 조합"이라는 단서를 달고, p44에서 "C, A, P 중 2개를 고른다는 것이 가장 큰 오해"라고 쓴다 |
| AP | Cassandra, DynamoDB, CouchDB | ⚠️ DynamoDB는 기본은 eventually consistent 읽기지만 strongly consistent 읽기를 고를 수 있다. 순수 AP로 부를 수 없다 |
| CP | HBase, MongoDB, Redis, ZooKeeper | ❌ Redis는 CP가 아니다. MongoDB는 read/write concern 설정에 따라 다르다 |

- Redis. 공식 문서가 "Redis Cluster does not guarantee strong consistency"라고 쓰고, 확인 응답을 받은 쓰기도 잃을 수 있다고 밝힌다. 복제 문서는 `WAIT`를 써도 "it does not turn a set of Redis instances into a CP system with strong consistency"라고 적는다. [Cluster: https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/ · 복제·`WAIT`: https://redis.io/docs/latest/operate/oss_and_stack/management/replication/ , 2026-09-28 확인] 자세한 내용은 [[Redis]].
- MongoDB. linearizable read concern은 primary에서 단일 문서에만 쓸 수 있다. [https://www.mongodb.com/docs/manual/reference/read-concern-linearizable/ , 2026-09-28 확인]
- DynamoDB. [https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html : "eventually consistent (default) and strongly consistent reads", 2026-09-28 확인]

Martin Kleppmann은 2015년 글에서 CP·AP 칸 나누기 자체를 그만두자고 제안했다("we should stop putting datastores into the 'AP' or 'CP' buckets"). 대부분의 저장소가 설정과 연산에 따라 두 칸 사이를 오가고, CAP의 C(linearizability)와 A(모든 비장애 노드의 응답)는 둘 다 실제 시스템이 잘 제공하지 않는 강한 정의이기 때문이다. [https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html , 2026-09-28 확인] 제품 분류표보다 강의 p45의 "선택은 연산·데이터 단위로 세밀하게 일어난다"가 실무에 쓸모 있다. 이 평가는 위키의 것이다.

### 면접 자료도 같은 분류를 쓴다

[[DB 면접 5 NoSQL과 RDBMS 비교]](인프런 DB 면접 강의)의 Gold 답은 "C·A·P 3가지를 모두 만족할 수 없다", "P는 사실상 필수라 C와 A 중 하나를 고른다", "CP는 MongoDB처럼, AP는 Cassandra처럼"이라고 쓴다(p87). Silver 답의 예시도 같다(p86). 위의 정정과 어긋나므로 명시해 둔다. AI DE 강의와 달리 이 자료는 Brewer 2012의 정정을 옮기지 않는다.

- "P는 사실상 필수"는 위 「"셋 중 둘"이 아니다」와 방향이 같다. 다만 자료는 선택을 시스템 전체의 일로 말하고, Brewer는 연산·데이터 단위의 일로 말한다.
- MongoDB. 기본 read concern인 `local`은 과반에 기록됐다는 보장 없이 읽으므로, 나중에 롤백될 데이터를 읽을 수 있다("no guarantee that the data has been written to a majority of the replica set members (i.e. may be rolled back)"). 기본 설정의 MongoDB를 CP라 부르기 어렵다. [https://www.mongodb.com/docs/manual/reference/read-concern-local/ , 2026-09-28 확인]
- Cassandra. 요청마다 일관성 수준(ONE, QUORUM, ALL 등)을 고르는 tunable consistency다. 읽기와 쓰기를 둘 다 QUORUM으로 두면 분할 때 과반에 닿지 못한 쪽은 요청에 실패하므로 AP라 부르기 어렵다. 이 추론은 위키의 것이다. [https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html , 2026-09-28 확인] Kleppmann도 같은 글에서 Cassandra가 어느 칸인지는 "It depends on your settings"라고 답한다.
- 같은 자료의 꼬리 질문(p90)은 결제·재고는 일관성, SNS 좋아요 수는 가용성을 고르라고 한다. 이것은 제품이 아니라 데이터 단위로 고르는 이야기라 Brewer의 틀과 맞는다. 자료가 앞의 제품 분류와 이 답을 잇지 않는다는 관찰은 위키의 것이다.

### 최종 일관성

AP 쪽을 고를 때 쓰는 보장이 최종 일관성(eventual consistency)이다. Werner Vogels의 정의는 새 갱신이 없으면 결국 모든 접근이 마지막 값을 돌려준다는 것이다("if no new updates are made to the object, eventually all accesses will return the last updated value"). 정의에 시한이 없다. 장애가 없을 때에만 불일치 구간의 최대 크기를 추정할 수 있다고 같은 글이 덧붙인다. [Werner Vogels, "Eventually Consistent - Revisited", 2008-12, https://www.allthingsdistributed.com/2008/12/eventually_consistent.html , 2026-09-28 확인] [[DB 면접 5 NoSQL과 RDBMS 비교]]의 "Eventual Consistency는 '언제' 수렴되는지 보장하지 않는다"(p90)는 이 정의와 맞다.

## 실무에서의 모습

- 합의 기반 시스템(etcd·Consul·ZooKeeper)은 과반(quorum)을 잃으면 스스로 가용성을 포기한다. 강의 p65가 이것을 "과반수의 역설"로 부른다([[합의 알고리즘]]).
- 동기 복제는 C 쪽으로, 비동기 복제는 A와 지연 쪽으로 기운다([[복제]]).
- [[NoSQL]]이 일관성을 완화한 대가(재시도, 중복 처리, 보정 배치)는 애플리케이션이 진다.

## 관련

- [[분산 시스템]] · [[복제]] · [[합의 알고리즘]] · [[NoSQL]] · [[관계형 데이터베이스]] · [[Redis]] · [[샤딩]]
- 면접 자료: [[DB 면접 5 NoSQL과 RDBMS 비교]]

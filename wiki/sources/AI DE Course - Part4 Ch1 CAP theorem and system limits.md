---
type: source
title: AI DE Course - Part4 Ch1 CAP theorem and system limits
area: [data-engineering]
aliases: [Part4 Ch1-3, CAP 정리와 분산시스템의 근본적 한계]
tags: [data-engineering, course, fast-campus, cap-theorem, distributed-systems, flp, lamport, consistency]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/Part 4_Ch 1~4.pdf (p32–50)"]
---

# AI DE Course - Part4 Ch1 CAP theorem and system limits

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 4** Ch1의 소단원 **3**
"CAP 정리와 분산시스템의 근본적 한계". 원본(로컬):
`raw/data-engineering/Part 4_Ch 1~4.pdf` **p32–50** (356p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐ **Part 4에서 출처가 가장 좋은 소단원이다.** Brewer의 2000년 제안과 **2012년 본인의 정정**,
> Gilbert & Lynch의 형식화, Lamport의 *Time, Clocks, and the Ordering of Events*, FLP 불가능성
> 정리 — 분산 시스템 이론의 정전(canon)을 짚는다. Part 1의 "출처 없는 80%"와 같은 코스라고 믿기
> 어려운 수준이다.

## 구성

`01 CAP 이론 · 02 Consistency · 03 Availability · 04 Partition Tolerance · 05 CAP의 오해 ·
06 분산시스템의 한계`

## 출발점 — 구현 난이도만의 문제가 아니다

> **"아무리 잘 만들어도 동시에 완전히 만족시킬 수 없는 성질이 존재한다."**

분산 처리의 근본적 한계 넷:

- 일부 노드만 실패 가능
- 네트워크는 지연되거나 끊길 수 있음
- **모든 노드가 같은 "현재"를 공유하지 않음**
- 한 노드에서 본 상태와 다른 노드에서 본 상태가 순간적으로 다를 수 있음

## CAP의 범위 — 만능 법칙이 아니다

> **"CAP는 모든 분산 시스템의 모든 속성을 다루는 만능 법칙이 아님. 네트워크 분할이 가능한 환경에서
> 읽기/쓰기 서비스가 어디까지 강한 보장을 할 수 있는가를 묻는 정리."**

2000년 **Eric Brewer**가 처음 제안. 강의는 이를 **안전성(Safety) vs 생명성(Liveness)** 의 상충으로
번역한다 — 이 프레이밍이 Gilbert & Lynch 계열이다.

| | 뜻 | CAP에서 |
|---|---|---|
| **안전성 (Safety)** | 나쁜 일이 절대 일어나지 않음을 보장 | **일관성** — 모든 응답이 정확함 |
| **생명성 (Liveness)** | 결국에는 좋은 일이 일어남을 보장 | **가용성** — 모든 요청에 결국 응답이 돌아옴 |
| **불안정성 (Unreliable)** | 네트워크 파티션, 메시지 손실, 충돌 장애, 악의적 공격 | 환경 조건 |

## 세 성질

### Consistency (일관성)

- **모든 서버가 각 요청에 대해 올바른 응답을 반환**
- 모든 클라이언트가 **하나의 최신 복사본**을 보는 것에 가까운 의미 — **single-copy consistency**
- 어떤 노드에서 데이터가 변경되면 다른 모든 노드에서도 일관적으로 변경
- 사용자가 어떤 노드와 통신하는지 상관없이 같은 데이터를 조회할 수 있어야 함

### Availability (가용성)

- **모든 요청에 결국 응답이 돌아오는 것**
- ⭐ **"실제 시스템에서는 너무 늦은 응답은 발생하지 않은 응답과 마찬가지로 간주."**
- Gilbert & Lynch의 classic liveness property — *every request receives a response*
- **작업이 실패하더라도 실패했다는 응답이 필요**

### Partition Tolerance (파티션 내성)

> ⭐ **"서비스의 태도가 아니라 환경의 속성에 가깝다."**

- 서버들 간 통신이 신뢰할 수 없고, 서로 통신할 수 없는 그룹들로 나뉠 수 있다는 **가정**
- 메시지가 지연되거나 영원히 손실될 수 있음
- **충분히 오래 지연된 메시지는 손실된 것으로 간주**
- **메시지 손실과 메시지 지연은 구별하기 어렵다**

마지막 줄이 FLP(아래)로 이어지는 다리다.

## 세 조합 — 그리고 왜 이 프레이밍이 틀렸나

강의는 먼저 통상적인 CA/AP/CP 3분류를 소개하고, **바로 다음 슬라이드에서 그것이 오해라고 반박한다.**
소단원 제목이 "**05. CAP의 오해**"인 것이 의도적이다.

| 조합 | 작동 방식 | 강의가 든 예 |
|---|---|---|
| **CA** | 데이터는 항상 일치하고 서버는 항상 응답하지만, **서버 간 통신이 끊기면 시스템 전체가 마비** | 전통적 RDBMS (Oracle, MySQL, PostgreSQL) |
| **AP** | 네트워크가 끊겨도 일단 응답. 데이터가 최신이 아닐 수 있음을 감수 → **Eventual Consistency** | Cassandra, DynamoDB, CouchDB |
| **CP** | 노드 간 동기화가 불가능하면 잘못된 데이터를 내보내지 않고 **에러를 뱉거나 응답을 거부** | HBase, MongoDB, **Redis**, ZooKeeper |

CA에 대해서는 스스로 단서를 단다: **"현대의 분산 환경에서는 네트워크 장애(P)가 필연적이므로, 엄밀히
말해 분산 시스템에서는 구현하기 어려운 조합."**

> ⚠️ **CP 예시의 Redis는 의심스럽다 — 그리고 이 강의 내부와 모순된다.**
> Redis는 기본이 **비동기 복제**라 primary 장애 시 미전파 쓰기가 유실된다. ZooKeeper(Zab 합의)나
> HBase와 나란히 둘 물건이 아니다. 결정적으로 **같은 Part 4 Ch2가 정반대를 말한다** —
> [[AI DE Course - Part4 Ch2 Caching strategies and TTL]]의 Write-Behind 절은 *"Redis 장애 시 DB에
> 반영되지 않은 데이터가 유실될 수 있다"* 고 경고하고, Ch1-4는 *"비동기식 복제는 RPO > 0"* 이라고
> 명시한다. **RPO > 0인 시스템을 CP로 분류할 수 없다.**
> → [[CAP theorem]]에 이 모순을 기록해뒀다.

## ⭐⭐ 오해하지 말아야 할 것 — 이 소단원의 핵심

> ⭐ **"가장 큰 오해는 C, A, P 중 2개를 고른다고 생각하는 것."**
>
> **Partition Tolerance는 우리가 '선택'하는 것이 아니라 벌어지는 사고다.**
>
> **진짜 CAP의 의미: 평소(네트워크 정상)에는 C와 A를 모두 누리다가, 네트워크 단절(P)이라는 사고가
> 터졌을 때 — 서비스의 응답성(A)을 포기할 것인가, 데이터의 정확성(C)을 포기할 것인가?**

### Brewer의 정정 (2012)

강의는 Brewer 본인의 12년 후 정정을 직접 인용한다: **"이 표현은 오해를 부릅니다(Misleading)."**

| 정정 내용 |
|---|
| **네트워크 단절은 드물다** (Partitions are rare) — 평소에는 C와 A를 포기할 이유가 없음 |
| 선택은 시스템 전체가 아니라 **'매우 세밀하게(Fine Granularity)'** 일어난다 — 서브시스템, 연산, 데이터의 성격마다 다른 선택 가능 |
| **C와 A는 이분법(Binary)이 아니라 정도(Degree)의 문제** |
| CP vs AP는 상황에 따라 둘 사이에서 균형을 맞추는 문제 |

> **이것을 다루는 강의가 흔치 않다.** "CAP 중 2개 고르기"로 끝내는 교재가 대부분인데, 이 소단원은
> 그 통념을 소개한 **직후에** 저자 본인의 반박으로 무너뜨린다. 구성이 좋다.

### ⭐ CAP의 C ≠ ACID의 C

> **"우리 DB는 ACID니까 CAP의 C도 만족한다"는 말은 성립하지 않는다."**

| | 뜻 |
|---|---|
| **ACID의 C** | unique key 같은 **database rules = invariants** 보존 |
| **CAP의 C** | **single-copy consistency** |

Brewer의 추가 지적 두 가지:

- ACID consistency도 **partition recovery 과정에서 별도로 복원되어야 할 수 있다**
- **Isolation의 serializability는 communication이 필요**하므로 partition across system에서는 그대로
  유지되기 어렵다

> **이 구분을 명시적으로 다루는 것이 이 소단원의 두 번째 수확이다.** [[Table formats]](Part 1)에서
> Delta Lake의 ACID를 배웠는데, **그 ACID가 CAP의 C를 보장하지 않는다**는 것을 여기서 알게 된다.

## 분산 시스템의 세 가지 근본 한계

### 1. 부분 실패 (Partial Failure)

단일 서버에서 실패는 비교적 단순하다 — 프로세스가 죽거나, 머신이 죽거나, 디스크가 망가진다.
분산 시스템은 애매하다:

- 어떤 노드는 살아있고, 어떤 노드는 죽음
- 네트워크는 일부 링크만 느려질 수 있음
- 메시지는 아주 늦게 도착할 수 있음
- ⭐ **관찰자마다 누가 죽었는지 다르게 보인다**

> **"부분적으로 실패한 세계에서 전체가 하나처럼 행동하게 만드는 것."**

### 2. 전역 시계 부재 — Lamport

**Leslie Lamport**, *Time, Clocks, and the Ordering of Events in a Distributed System*.

> **"분산 시스템에서는 두 사건 중 무엇이 먼저 일어났는지 말하는 것이 때때로 불가능하다."**

이유: 메시지 전달 지연이 무시할 수 없고, 모든 노드가 동일한 시계를 공유하지 않는다.

결과:
- **"먼저 쓴 값"을 정의하기가 어려움**
- 로그 정렬, 충돌 해결, 복제 순서 결정이 어려움
- 트랜잭션 외부 일관성(external consistency)을 얻으려면 추가 장치 필요

> ⭐ **이것이 Ch3의 Event Time 논의와 같은 문제다.**
> [[AI DE Course - Part4 Ch3 Event time watermarks and windows]]의 "발생 시각 vs 도착 시각"은
> Lamport 문제의 애플리케이션 계층 버전이다. **강의는 두 챕터를 잇지 않지만 같은 뿌리다.**

### 3. FLP 불가능성

**Fischer, Lynch, Paterson** — 완전 비동기 모델에서 **프로세스 하나만 실패할 수 있어도**
deterministic consensus protocol이 항상 결정을 내리도록 보장할 수 없다.

강의의 번역:
> **"단 1대의 고장만 있어도 언제나 완벽하게 작동하는 합의 방식은 존재하지 않는다. 따라서 이런 통신
> 환경에서는 완벽한 합의를 이끌어내는 문제를 아예 풀 수가 없다."**

전제 조건 셋: ① 네트워크 지연 상한이 없고 ② 시계 동기화도 없고 ③ 실패 감지도 확실하지 않다면 —
**언젠가 반드시 모두가 합의하게 만드는 것은 이론적으로 불가능.**

### ⭐ 실무의 회피 — 부분 동기성

> **"실무 시스템은 FLP를 무시하지 않는다. 대신 완전 비동기 모델을 버리고, 어느 정도의 synchrony
> 가정을 도입한다."**

현실 시스템은 — **timeout을 둔다 · leader를 선출한다 · 일정 시간 이후 네트워크가 안정될 것이라고
기대한다.**

> **이 문단이 Ch1-4로 넘어가는 다리다.** timeout·leader election이 곧 Raft의 election timeout과
> leader이고, "불가능성을 현실적으로 회피"하는 방식이 곧 [[Replication and consensus]]다.

## 기존 페이지와의 대조

- **새 concept:** [[CAP theorem]] · [[Distributed system limits]]
- ⚠️ **[[NoSQL]](Part 3)의 CAP 서술과 겹치는데 이쪽이 훨씬 정확하다.** Part 3 Ch1-3은 CAP를
  NoSQL 설명의 배경으로만 짧게 다뤘고 **Brewer의 정정은 나오지 않았다.** 모순은 아니지만
  **Part 3 페이지에서 이쪽으로 링크해야 한다.**
- **[[Latency and throughput]]과의 연결** — "너무 늦은 응답 = 발생하지 않은 응답"은 Part 1의
  타임아웃 논의와 같은 이야기다.
- **[[Table formats]]** — ACID의 C와 CAP의 C 구분이 여기 적용된다.

## 자료 품질

**이 코스 전체에서 가장 좋은 소단원 중 하나.**

- ✅ **1차 자료 5건**: Brewer 2000 · Brewer 2012 정정 · Gilbert & Lynch · Lamport
  (*Time, Clocks, and the Ordering of Events in a Distributed System* — 제목 전체 표기) ·
  Fischer/Lynch/Paterson
- ✅ **통념을 소개한 뒤 저자 본인의 반박으로 무너뜨리는 구성**
- ✅ **출처 없는 수치가 하나도 없다**
- ⚠️ **CP 예시의 Redis** — 위 참조. 파트 내부 모순
- ⚠️ 중복 슬라이드: p34/p35 완전 동일
- ⚠️ 논문 인용에 **연도와 저널/학회가 없다** — Lamport(1978, CACM), FLP(1985, JACM),
  Gilbert & Lynch(2002, SIGACT News)를 찾으려면 검색이 필요하다

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[CAP theorem]] · [[Distributed system limits]] · [[Distributed processing]] ·
  [[Replication and consensus]] · [[NoSQL]] · [[Table formats]]
- 앞: [[AI DE Course - Part4 Ch1 Distributed processing basics]]
- 다음: [[AI DE Course - Part4 Ch1 HA replication and consensus]]

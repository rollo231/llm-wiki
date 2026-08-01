---
type: concept
title: CAP theorem
area: [data-engineering]
aliases: [CAP, CAP 정리, CAP 이론, 브루어의 정리, Brewer's theorem, PACELC]
tags: [data-engineering, distributed-systems, cap-theorem, consistency, availability, partition-tolerance]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch1 CAP theorem and system limits]]"]
---

# CAP theorem

**네트워크 분할이 가능한 환경에서 읽기/쓰기 서비스가 어디까지 강한 보장을 할 수 있는가를 묻는 정리.**

2000년 **Eric Brewer**가 제안하고 Gilbert & Lynch가 형식화했다.

> ⭐ **"CAP는 모든 분산 시스템의 모든 속성을 다루는 만능 법칙이 아니다."**

## 세 성질

| | 뜻 | 성질 |
|---|---|---|
| **Consistency** (일관성) | 모든 서버가 각 요청에 대해 올바른 응답을 반환. 모든 클라이언트가 **하나의 최신 복사본**을 보는 것 — **single-copy consistency** | **안전성 (Safety)** — 나쁜 일이 절대 일어나지 않음 |
| **Availability** (가용성) | 모든 요청에 결국 응답이 돌아옴 (*every request receives a response*). 실패도 **"실패했다"는 응답**이 필요 | **생명성 (Liveness)** — 결국에는 좋은 일이 일어남 |
| **Partition Tolerance** (파티션 내성) | 서버들 간 통신이 신뢰할 수 없고, 서로 통신할 수 없는 그룹들로 나뉠 수 있다는 **가정** | **환경의 속성** |

> ⭐ **"실제 시스템에서는 너무 늦은 응답은 발생하지 않은 응답과 마찬가지로 간주된다."**
> 가용성은 이진값이 아니라 타임아웃과 함께 정의된다.

> ⭐ **Partition Tolerance는 "서비스의 태도가 아니라 환경의 속성"이다.**
> 그리고 **"메시지 손실과 메시지 지연은 구별하기 어렵다"** — 이 사실이
> [[Distributed system limits]]의 FLP 불가능성으로 이어진다.

## ⭐⭐ 가장 큰 오해 — "셋 중 둘을 고른다"

> **"가장 큰 오해는 C, A, P 중 2개를 고른다고 생각하는 것."**
>
> **Partition Tolerance는 우리가 '선택'하는 것이 아니라 벌어지는 사고다.**
>
> ⭐ **진짜 CAP의 의미: 평소(네트워크 정상)에는 C와 A를 모두 누리다가, 네트워크 단절(P)이라는
> 사고가 터졌을 때 — 서비스의 응답성(A)을 포기할 것인가, 데이터의 정확성(C)을 포기할 것인가?**

### Brewer 본인의 정정 (2012)

Brewer는 12년 뒤 **"이 표현은 오해를 부릅니다(Misleading)"** 라고 정정했다.

| 정정 |
|---|
| **네트워크 단절은 드물다** (Partitions are rare) — 평소에는 C와 A를 포기할 이유가 없다 |
| 선택은 시스템 전체가 아니라 **'매우 세밀하게(Fine Granularity)'** 일어난다 — 서브시스템, 연산, 데이터의 성격마다 다른 선택 가능 |
| ⭐ **C와 A는 이분법(Binary)이 아니라 정도(Degree)의 문제** |
| CP vs AP는 상황에 따라 둘 사이에서 균형을 맞추는 문제 |

**실무적 함의:** 같은 서비스 안에서도 결제 경로는 CP로, 조회수 카운터는 AP로 설계할 수 있다.
"우리 시스템은 AP다"라는 문장 자체가 대개 너무 거칠다.

## 통상적 3분류 — 그리고 그 한계

| 조합 | 작동 방식 | 흔히 드는 예 |
|---|---|---|
| **CA** | 데이터는 항상 일치하고 서버는 항상 응답하지만, **통신이 끊기면 시스템 전체가 마비** | 전통적 RDBMS (Oracle, MySQL, PostgreSQL) |
| **AP** | 네트워크가 끊겨도 일단 응답. 최신이 아닐 수 있음을 감수 → **Eventual Consistency** | Cassandra, DynamoDB, CouchDB |
| **CP** | 동기화 불가능 시 잘못된 데이터를 내보내지 않고 **에러를 뱉거나 응답을 거부** | HBase, MongoDB, ZooKeeper |

**CA는 사실상 분산 시스템에서 구현 불가능하다** — 네트워크 장애(P)가 필연적이기 때문이다.
"CA 시스템"은 대개 "단일 노드 시스템" 또는 "P를 무시하기로 한 시스템"을 뜻한다.

> ⚠️ **강의는 CP 목록에 [[Redis]]를 넣는데, 이 위키는 그 분류를 채택하지 않는다.**
> Redis 기본 복제는 **비동기**라 primary 장애 시 미전파 쓰기가 유실된다(**RPO > 0**).
> **RPO > 0인 시스템을 "정확하지 않으면 응답하지 않는다"는 CP로 분류할 수 없다.**
>
> **같은 강의 안에서도 서술이 충돌한다:**
> - [[AI DE Course - Part4 Ch1 CAP theorem and system limits]] — Redis는 CP, *"금융 거래·결제
>   시스템 등 데이터의 정확성이 생명인 경우"* 에 적합
> - [[AI DE Course - Part4 Ch2 Caching strategies and TTL]] — *"Redis 장애 시 DB에 반영되지 않은
>   데이터가 유실될 수 있다"*, *"정산·결제·주문 같은 강한 정합성 데이터에는 위험"*
> - [[AI DE Course - Part4 Ch2 Redis and the caching layer]] — 부적합 데이터 목록 1번이
>   *"강한 정합성이 필요한 결제 상태"*
>
> **후자 둘이 맞다.** Redis Sentinel/Cluster의 failover는 손실 가능한 failover다.

## ⭐ CAP의 C ≠ ACID의 C

> **"우리 DB는 ACID니까 CAP의 C도 만족한다"는 말은 성립하지 않는다.**

| | 뜻 |
|---|---|
| **ACID의 C** | unique key 같은 **database rules = invariants** 보존 |
| **CAP의 C** | **single-copy consistency** — 모든 노드가 같은 최신 값을 본다 |

Brewer의 추가 지적:

- ACID consistency도 **partition recovery 과정에서 별도로 복원되어야 할 수 있다**
- **Isolation의 serializability는 communication이 필요**하므로 partition across system에서는 유지가
  어렵다

> **[[Table formats]]의 Delta Lake ACID가 CAP의 C를 보장하지 않는 이유가 이것이다.**
> 테이블 포맷의 ACID는 단일 스토리지 위의 트랜잭션 보장이지, 지역 간 복제의 일관성이 아니다.

## 실무에서 이 정리를 쓰는 법

**CAP은 제품을 고르는 표가 아니라 질문 목록이다:**

1. **이 연산에서** 네트워크 분할이 일어나면 무엇을 포기할 것인가? (시스템 전체가 아니라 연산별로)
2. 그 선택이 사용자에게 어떻게 보이는가? — 에러인가, 오래된 값인가?
3. 분할이 복구된 뒤 **불일치를 어떻게 수렴시킬 것인가?** (충돌 해결 규칙)
4. **"너무 늦은 응답"의 기준은 몇 ms인가?** (가용성의 실질적 정의)

3번이 특히 자주 빠진다 — AP를 고르면 **수렴 전략(last-write-wins, CRDT, 애플리케이션 병합)** 이
설계의 일부가 된다. **[[NoSQL]]의 "일관성 완화는 애플리케이션 복잡도로 전가된다"가 이 지점이다.**

## ⚠️ 이 위키에 아직 없는 것

- **PACELC** — CAP의 확장. *분할(P) 시에는 A와 C 중, 그렇지 않을 때(E, Else)에는 지연(L)과
  일관성(C) 중* 선택한다는 프레임. **평상시의 트레이드오프**를 다루므로 CAP보다 실무에 가깝다.
  **강의에 나오지 않는다.**
- **일관성 모델의 스펙트럼** — linearizability, sequential, causal, eventual.
  강의는 "C냐 아니냐"의 이분법에 머문다 (Brewer의 "정도의 문제"를 인용하면서도 정도를 나누지 않는다).

## 관련 페이지

- [[Distributed system limits]] — 부분 실패, 전역 시계 부재, FLP. **CAP보다 더 근본적인 한계**
- [[Replication and consensus]] — CAP의 선택을 실제로 구현하는 층. **"과반수의 역설"** 이 CP의 실물
- [[Distributed processing]] — 왜 분산하는가
- [[NoSQL]] — AP 계열 저장소의 실무적 대가
- [[Table formats]] — ACID의 C
- [[Redis]] — 위 분류 논란의 대상

## 출처

- [[AI DE Course - Part4 Ch1 CAP theorem and system limits]]

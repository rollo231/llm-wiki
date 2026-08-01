---
type: concept
title: Replication and consensus
area: [data-engineering]
aliases: [복제와 합의, 고가용성, High Availability, HA, Raft, Paxos, RTO, RPO, quorum, split brain]
tags: [data-engineering, distributed-systems, replication, consensus, raft, high-availability, quorum]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch1 HA replication and consensus]]"]
---

# Replication and consensus

**[[Distributed system limits]]을 현실적으로 회피해 고가용성을 만드는 두 층.**

> ⭐ **고가용성은 목표, 복제는 데이터 수단, 합의는 제어 수단.**
> **이 셋은 서로 대체 관계가 아니라 계층 관계다.**

## 왜 복제만으로는 안 되나

> **"복제본을 여러 개 두면 장애에 강해진다?"**

복제본이 있어도 결정해야 할 것이 남는다:

- 누가 현재 **primary**인지
- 어떤 복제본이 **가장 최신**인지
- 네트워크가 끊겼을 때 **어느 쪽이 계속 쓰기를 받아도 되는지**
- 장애 후 **라우팅을 어디로 바꿔야 하는지**

> ⭐ **"복제는 상태를 늘려줄 뿐이고, 그 상태를 안전하게 제어하는 규칙은 따로 필요하다."**

## 고가용성 — RTO와 RPO

HA는 **"인프라 장애에 대한 시스템 회복력"** 이고, 운영의 핵심 목표는 **Failover**다.

| 지표 | 질문 | 뜻 |
|---|---|---|
| **RTO** (Recovery Time Objective) | **얼마나 빨리?** | 장애 발생 후 서비스가 다시 살아날 때까지의 시간 |
| **RPO** (Recovery Point Objective) | **얼마나 적게?** | 장애 시 허용 가능한 최대 데이터 손실량 |

> ⭐ **"고가용성은 단순히 '복제본이 있다'가 아니라 얼마나 빨리 전환되는가, 얼마나 적게 잃는가까지
> 포함한 운영 목표."**

RTO/RPO는 [[Data SLA and observability]]의 SLO 언어가 인프라 계층에 나타난 형태다.

### HA 아키텍처의 최소 구성 요소 4가지

1. **실패를 감지하는 메커니즘**
2. **standby를 primary로 승격하는 failover 절차**
3. ⭐ **애플리케이션 요청을 새 primary로 보내는 query routing 전환**
4. 필요하면 기존 primary를 안전하게 복귀시키는 **fallback 절차**

> **3번이 빠져서 나는 사고가 흔하다** — "DB는 failover 됐는데 앱이 여전히 옛 primary를 본다".
> 복제와 합의만으로는 부족하고 **라우팅 계층까지 설계에 포함**해야 한다.

### 대표 구현

| 시스템 | 구조 |
|---|---|
| **PostgreSQL** | primary + standby, 필요 시 standby 승격 → 빠른 takeover + read scaling |
| **Kubernetes** | Control Plane HA. **stacked control plane vs external etcd** — external etcd는 한 노드 손실의 영향을 줄이지만 **더 많은 서버가 필요** |
| **Vault** | Raft 기반으로 모든 노드에 데이터 복제 |

## 복제 — 동기식 vs 비동기식

**목적 셋:** 장애 시 대체본 확보 · 읽기/지역 분산 · 데이터 손실 위험 감소.

> **핵심 축: "클라이언트에게 커밋 완료를 반환하는 시점을 언제로 정의하는가."**

| | **동기식 (Synchronous)** | **비동기식 (Asynchronous)** |
|---|---|---|
| **메커니즘** | Primary가 커밋 완료를 반환하기 전, 최소 1개 이상의 Standby가 데이터를 수신·**디스크에 flush**했음을 ACK할 때까지 대기 | Primary가 로컬 WAL 기록 후 Standby와 **무관하게 즉시** 반환 |
| **내구성** | **RPO = 0** | **RPO > 0** — failover 시 미전송 트랜잭션 유실 |
| **지연** | Standby 응답 대기로 commit latency 증가 | 매우 낮음 |
| **위험** | ⭐ **Standby 장애 시 Primary의 쓰기까지 블로킹될 수 있음** | 데이터 손실 |
| **기본값** | — | **PostgreSQL 등 대부분의 RDBMS 기본** |

> ⭐ **동기식의 역설: 가용성을 높이려고 넣은 복제본이 가용성을 떨어뜨린다.**
> [[CAP theorem]]의 C↔A 트레이드오프가 복제 설정 한 줄에서 실제로 일어난다.

> **대부분의 RDBMS 기본값이 비동기라는 사실이 중요하다.** "복제를 켰다"는 것이
> "데이터 손실이 없다"를 뜻하지 않는다. **[[Redis]]가 CP로 분류되면 안 되는 이유이기도 하다** —
> [[CAP theorem]] 참조.

## 합의 — 무엇에 동의하게 만드나

> **"합의 알고리즘은 '리더 한 명 뽑기'?"** — 아니다. 다음 넷을 노드들이 동의하게 만든다:

1. **어떤 로그 엔트리가 유효한지**
2. **어떤 순서로 적용되는지**
3. **언제 committed로 간주되는지**
4. **membership이 어떻게 바뀌는지**

> ⭐ **"합의는 분산 시스템의 컨트롤 타워 — 복제된 상태 머신이 동일한 순서로 전개되도록 만드는
> 장치."**

| 알고리즘 | 설명 |
|---|---|
| **Raft** | replicated log를 관리하기 위한 합의 알고리즘. 이해 가능성을 목표로 설계 |
| **Paxos** (Lamport) | 여러 서버가 같은 *sequence of state machine commands*를 실행하도록 **separate instances of consensus**를 사용 |

### Raft — 세 상태

| 상태 | 역할 |
|---|---|
| **리더 (Leader)** | 클라이언트의 모든 요청을 혼자 처리하고 다른 노드에 명령. 주기적으로 **하트비트** 전송 |
| **팔로워 (Follower)** | 평소의 모든 노드 상태. 리더의 명령을 수동적으로 저장. 클라이언트 요청은 리더에게 **Redirect** |
| **후보자 (Candidate)** | 리더가 죽었다고 판단될 때 후보 지원 |

**선거 흐름:**

1. **선거 타임아웃** — 팔로워가 일정 시간 하트비트를 못 받으면 리더가 죽었다고 판단
2. **선거 출마** — 타임아웃이 가장 먼저 끝난 팔로워가 후보자로 전환, 자신에게 한 표
3. **과반수 득표 (Quorum)** — 전체 노드의 과반수 찬성을 얻은 후보가 새 리더 (예: **5대 중 3대**)

> ⭐ **선거 타임아웃이 곧 [[Distributed system limits]]의 FLP 회피 장치다.**
> "완전 비동기에서는 합의가 불가능하다" → **타임아웃을 두어 부분 동기를 가정한다.**
>
> **과반수 규칙이 split brain 방지 장치다** — 분할된 양쪽이 동시에 과반수를 가질 수는 없다.

## ⭐ 합의의 대가 — 세 가지

> **"HA와 Consensus는 단순히 '더 좋은 구조'를 의미하지 않는다."**

| # | 대가 | 제품 | 딜레마 |
|---|---|---|---|
| **1** | **응답 지연 증가** | PostgreSQL | 완벽한 Durability를 원할수록 느려진다 |
| **2** | **운영 비용 및 쓰기 실패율 증가** | [[Apache Kafka]] | `Replication Factor`·`min.ISR`·`acks=all`을 높이면 **저장 비용 급증**, **조건 미달 시 쓰기 실패** |
| **3** | ⭐⭐ **과반수(Quorum)의 역설** | Consul / etcd | **합의는 네트워크 파티션 시 일관성(C)을 지키기 위해 가용성(A)을 스스로 포기한다.** Quorum Loss 시 **클러스터가 스스로 Unavailable 상태로 전환** |

> ⭐⭐ **3번이 [[CAP theorem]]을 실물로 보여준다.** "가용성을 위해 합의를 도입했는데 합의가 가용성을
> 포기한다" — CP 시스템의 정의 그 자체다.
>
> **etcd quorum loss = Kubernetes control plane 정지**이므로, 실무에서 가장 자주 만나는 CAP 사례다.
> 3노드 etcd에서 2대가 죽으면 남은 1대는 **읽기도 쓰기도 거부한다.** 이것이 버그가 아니라 설계다.

**2번도 실무에서 자주 놓친다** — `acks=all`은 "안전하게 쓴다"가 아니라 **"안전하게 못 쓰면
실패한다"** 는 뜻이다. ISR이 `min.ISR` 아래로 떨어지면 프로듀서가 예외를 받는다.

## 세 계층의 조합 — 실무 패턴 3종

| 패턴 | 구성 | 세 계층의 역할 |
|---|---|---|
| **1. RDBMS 고가용성** | Primary-Standby + **동기식 복제** + **Patroni**(또는 pg_auto_failover) + Load Balancer | 복제=PostgreSQL / 합의=Patroni가 쓰는 DCS(etcd·Consul) / 라우팅=LB |
| **2. 분산 로그·메시징** | 다중 브로커 + `Replication Factor=3` + `min.ISR=2` + `acks=all` | 복제=파티션 replica / 합의=컨트롤러(KRaft) / 라우팅=클라이언트 메타데이터 |
| **3. 제어-데이터 분리** | 다중 Control Plane 노드 + **External etcd** | 복제=etcd Raft / 합의=Raft / 라우팅=API server LB |

> **패턴 1이 세 계층 조합의 가장 명확한 예다.** Patroni 자체가 etcd/Consul/ZooKeeper를 DCS로 써서
> 리더를 결정하고, PostgreSQL은 복제만 담당한다 — **복제와 합의가 물리적으로 다른 시스템이다.**
> (강의는 Patroni를 구성 요소로 나열만 하고 이 구조를 설명하지 않는다.)

## ⚠️ 이 위키에 아직 없는 것

- **Raft의 로그 복제 상세** — 강의는 리더 선출까지만 다루고, log matching·commit index·
  스냅샷·membership change(joint consensus)를 다루지 않는다.
- **Paxos와 Raft의 실제 차이** — Paxos는 한 줄 인용뿐이라 비교가 아니라 나열이다.
- **witness / quorum device** — 2노드 구성에서 tie를 깨는 실무 장치.
- **비동기 복제에서의 failover 안전장치** — fencing, STONITH.
- 논문 서지 — Raft(Ongaro & Ousterhout, 2014).

## 관련 페이지

- [[CAP theorem]] — 합의가 무엇을 포기하는지
- [[Distributed system limits]] — FLP와 부분 실패. **합의가 회피하는 대상**
- [[Distributed processing]] — 장애 허용 분산
- [[Data SLA and observability]] — RTO/RPO와 SLO
- [[Apache Kafka]] — `acks=all`·`min.ISR`의 대가
- [[Message broker]] — 브로커의 복제 모델

## 출처

- [[AI DE Course - Part4 Ch1 HA replication and consensus]]

---
type: source
title: AI DE Course - Part4 Ch1 HA replication and consensus
area: [data-engineering]
aliases: [Part4 Ch1-4, 고가용성 복제와 합의 알고리즘, HA Replication Consensus]
tags: [data-engineering, course, fast-campus, high-availability, replication, consensus, raft, quorum, rto-rpo]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf (p51–66)"]
---

# AI DE Course - Part4 Ch1 HA replication and consensus

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 4** Ch1의 소단원 **4**
"고가용성, 복제(Replication)와 합의 알고리즘(Consensus)". 원본(로컬):
`raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` **p51–66** (356p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐ **이 소단원의 뼈대는 한 문장이다: "고가용성은 목표, 복제는 데이터 수단, 합의는 제어 수단."**
> 세 개념을 **대체 관계가 아니라 계층 관계**로 놓는 것이 핵심이고, 이 프레이밍 덕분에 "복제본을
> 여러 개 두면 장애에 강해진다"는 통념이 왜 부족한지가 바로 보인다.

## 구성

`01 세 개념의 관계 · 02 고가용성(High Availability) · 03 복제(Replication) · 04 합의(Consensus) ·
05 합의의 대가`

## ⭐ 세 개념의 관계

> **"복제본을 여러 개 두면 장애에 강해진다?"**
>
> 복제본이 있어도 결정해야 할 것이 남는다 — 누가 현재 primary인지, 어떤 복제본이 가장 최신인지,
> 네트워크가 끊겼을 때 어느 쪽이 계속 쓰기를 받아도 되는지, 장애 후 라우팅을 어디로 바꿔야 하는지.

| | 역할 |
|---|---|
| **고가용성** | **목표** — 장애가 나도 서비스가 중단되지 않거나 빠르게 복구되는 상태 |
| **복제** | **데이터 수단** — 데이터를 여러 노드에 유지하는 방법 |
| **합의** | **제어 수단** — 어느 복제본이 대표인지 결정하는 규칙 |

> ⭐ **"복제는 상태를 늘려줄 뿐이고, 그 상태를 안전하게 제어하는 규칙은 따로 필요하다."**
> **"이 셋은 서로 대체 관계가 아니라 계층 관계."**

근거로 든 제품: **PostgreSQL**(서버들이 함께 동작해 primary 장애 시 빠르게 takeover),
**Consul**(log entry의 authoritative order와 quorum으로 일관된 상태 유지).

## 고가용성 — RTO와 RPO

Google Cloud의 PostgreSQL HA 문서를 인용해 HA를 **"인프라 장애에 대한 시스템 회복력"** 으로 정의한다.

운영의 핵심 목표는 **Failover(빠른 전환)** 이고, 두 지표로 잰다:

| 지표 | 질문 | 뜻 |
|---|---|---|
| **RTO** (Recovery Time Objective) | **얼마나 빨리?** | 장애 발생 후 서비스가 다시 살아날 때까지의 시간 |
| **RPO** (Recovery Point Objective) | **얼마나 적게?** | 장애 시 허용 가능한 최대 데이터 손실량 |

> ⭐ **"고가용성은 단순히 '복제본이 있다'가 아니라 얼마나 빨리 전환되는가, 얼마나 적게 잃는가까지
> 포함한 운영 목표."**

RTO/RPO는 [[Data SLA and observability]]의 SLA 논의와 같은 계열의 언어이고,
**Ch5의 SLI/SLO/SLA 4단계**와 직접 이어진다.

### HA 아키텍처의 최소 구성 요소 4가지

1. **실패를 감지하는 메커니즘**
2. **standby를 primary로 승격하는 failover 절차**
3. **애플리케이션 요청을 새 primary로 보내는 query routing 전환**
4. 필요하면 기존 primary를 안전하게 복귀시키는 **fallback 절차**

> **3번을 명시하는 게 좋다.** "DB가 failover 됐는데 앱이 여전히 옛 primary를 본다"는 실무 사고가
> 여기서 나온다.

### 대표 HA 예시

| 시스템 | 구조 |
|---|---|
| **PostgreSQL** | primary + standby. 필요 시 standby를 새 primary로 승격 → 빠른 takeover, read scaling |
| **Kubernetes** | Control Plane HA. **stacked control plane vs external etcd** 토폴로지 비교 — external etcd는 control plane과 etcd를 분리해 한 노드 손실의 영향을 줄이지만 **더 많은 서버가 필요** |
| **Vault** | Raft 기반으로 모든 노드에 데이터를 복제 |

> **"단순히 노드를 늘리는 것이 아니라 어떤 구조로 failover와 redundancy를 보장할지 선택이 필요."**

## 복제 — 동기식 vs 비동기식

복제의 목적 셋: 장애 시 대체본 확보 · 읽기 분산 또는 지역 분산 · 데이터 손실 위험 감소.

근거 제품: **PostgreSQL**(WAL shipping + streaming replication), **Kafka**(각 토픽 파티션의 로그를
여러 서버에 복제해 자동 failover).

> **핵심 축: "클라이언트에게 커밋 완료를 반환하는 시점을 언제로 정의하는가."**

| | 동기식 (Synchronous) | 비동기식 (Asynchronous) |
|---|---|---|
| **메커니즘** | Primary가 커밋 완료를 반환하기 전, 최소 1개 이상의 Standby가 데이터를 수신하고 **로컬 디스크에 기록(Flush)** 했음을 ACK할 때까지 대기 | Primary가 로컬 WAL 기록 후 Standby와 **무관하게 즉시** 커밋 완료 반환 |
| **장점** | 강력한 내구성 — Primary 장애에도 Standby에 데이터가 완벽히 보존, **RPO = 0** | 성능 최적화 — 네트워크·Standby I/O가 응답 시간에 영향 없음. 매우 낮은 지연 |
| **단점** | Standby 응답 대기로 전체 트랜잭션 지연. **최악의 경우 Standby 장애 시 Primary의 쓰기까지 블로킹** | Failover 시 미전송 트랜잭션 유실. **RPO > 0** |
| **기본값** | — | **PostgreSQL 등 대부분의 RDBMS 기본 설정** |

> ⭐ **"동기식의 최악의 경우 — Standby 장애가 Primary 쓰기를 막는다."**
> 가용성을 높이려고 넣은 복제본이 가용성을 떨어뜨리는 역설이다. Ch1-3의 CAP가 여기서 구체화된다.

## 합의 — 복제 이후에 남는 것

복제본이 여러 개 있다고 곧바로 안전한 HA가 되지 않는다:

- 어떤 replica를 승격할지
- 어느 노드가 **가장 최신 WAL 위치**를 가졌는지
- 네트워크 분할 중 양쪽이 동시에 primary라고 믿는 **split brain**을 어떻게 막을지
- 애플리케이션 트래픽을 새 primary로 어떻게 바꿀지

### 합의 알고리즘이 결정하는 것

> **"합의 알고리즘은 '리더 한 명 뽑기'?"** — 아니다. 다음 넷을 노드들이 동의하게 만든다:
> 어떤 로그 엔트리가 유효한지 · 어떤 순서로 적용되는지 · 언제 committed로 간주되는지 ·
> membership이 어떻게 바뀌는지.

| 알고리즘 | 설명 |
|---|---|
| **Raft** | replicated log를 관리하기 위한 합의 알고리즘 |
| **Paxos** (Lamport) | 여러 서버가 같은 *sequence of state machine commands*를 실행하도록 **separate instances of consensus**를 사용 |

> ⭐ **"합의는 분산 시스템의 컨트롤 타워 — 복제된 상태 머신이 동일한 순서로 전개되도록 만드는 장치."**

### Raft — 세 상태와 선거

| 상태 | 역할 |
|---|---|
| **리더 (Leader)** | 클라이언트의 모든 요청을 혼자서 처리하고 다른 노드에 명령. 살아있음을 알리기 위해 주기적으로 **하트비트(Heartbeat)** 전송 |
| **팔로워 (Follower)** | 평소의 모든 노드 상태. 리더의 명령을 수동적으로 받아 저장. 클라이언트 요청이 오면 리더에게 **Redirect** |
| **후보자 (Candidate)** | 리더가 죽었다고 판단될 때 후보 지원 |

선거 흐름:

1. **선거 타임아웃** — 팔로워가 일정 시간 하트비트를 못 받으면 리더가 죽었다고 판단
2. **선거 출마** — 타임아웃이 가장 먼저 끝난 팔로워가 후보자로 전환, 자신에게 한 표를 던지고 다른
   노드에 표를 요청
3. **과반수 득표 (Majority/Quorum)** — 전체 노드의 과반수 찬성표를 얻은 후보자가 새 리더로 당선
   (예: **5대 중 3대 이상**)

> **Ch1-3의 FLP 회피가 여기서 구체적으로 보인다.** "선거 타임아웃"이 곧 FLP를 우회하는 synchrony
> 가정이고, "과반수"가 split brain 방지 장치다.

## ⭐ 합의의 대가 — 세 가지 트레이드오프

> **"HA와 Consensus는 단순히 '더 좋은 구조'를 의미하지 않는다."**

| # | 대가 | 제품 | 딜레마 |
|---|---|---|---|
| **1** | **응답 지연 증가** | PostgreSQL | 완벽한 데이터 보존(Durability)을 원할수록 시스템은 느려진다. 비동기 = 낮은 지연 + 손실 위험, 동기 = 완벽한 내구성 + Commit Latency 증가 |
| **2** | **운영 비용 및 쓰기 실패율 증가** | Kafka | 강력한 내구성을 위해 `Replication Factor`·`min.ISR`·`acks=all`을 높게 설정하면 **저장 공간 비용 급증**, 여러 노드의 확인 필요, **조건 미달 시 쓰기 작업 실패** |
| **3** | ⭐ **과반수(Quorum)의 역설** | Consul / etcd | **합의는 네트워크 파티션 시 일관성(C)을 지키기 위해 가용성(A)을 스스로 포기한다.** 전체 노드 Quorum Loss 발생 시 **클러스터는 스스로 Unavailable 상태로 전환** |

> ⭐⭐ **3번이 Ch1-3의 CAP를 실물로 보여준다.** "가용성을 위해 합의를 도입했는데 합의가 가용성을
> 포기한다" — CP 시스템의 정의 그 자체다. **etcd quorum loss는 곧 Kubernetes control plane 정지**를
> 뜻하므로 실무에서 가장 자주 만나는 CAP 사례이기도 하다.

## 세 계층의 조합 — 실무 패턴 3종

| 패턴 | 구성 |
|---|---|
| **1. RDBMS 고가용성** (PostgreSQL 생태계) | Primary-Standby DB + **동기식 복제** + **Patroni** (또는 pg_auto_failover) + Load Balancer |
| **2. 분산 로그 및 메시징** (Kafka 클러스터) | 다중 브로커 + `Replication Factor=3` + `min.ISR=2` + `acks=all` |
| **3. 제어-데이터 분리** (Kubernetes HA) | 다중 Control Plane 노드 + **External etcd** (외부 분리형) |

> **패턴 1에서 Patroni가 처음 등장한다.** "복제(PostgreSQL) + 합의(etcd/Consul을 통한 리더 선출) +
> 라우팅(LB)"이 실제로 세 계층 조합임을 보여주는 좋은 예인데, **강의가 Patroni의 내부 동작은
> 설명하지 않는다** (Patroni 자체가 DCS로 etcd/Consul/ZooKeeper를 쓴다는 점이 빠져 있어, 왜 이게
> "세 계층 조합"인지가 슬라이드만으로는 안 보인다).

## 기존 페이지와의 대조

- **새 concept:** [[Replication and consensus]]
- **[[Apache Kafka]] 보강** — `acks=all` / `min.ISR` / `Replication Factor`의 **트레이드오프**가
  Part 1 CH04-3,4에는 없었다. Part 1은 "복제하면 안전하다"까지였고, 여기는 **"조건 미달 시 쓰기가
  실패한다"** 는 비용까지 말한다.
- ⚠️ **[[AI DE Course - Part4 Ch1 CAP theorem and system limits]]의 CP 분류와 이 페이지가 충돌한다** —
  Ch1-3은 Redis를 CP로 분류했는데, 이 소단원은 **"비동기식 복제는 RPO > 0"** 이라고 명시한다.
  Redis 기본 복제는 비동기이므로 두 서술이 양립하지 않는다.
- **[[Data SLA and observability]]와 RTO/RPO** — SLA 언어가 인프라 계층에서 처음 나온다.

## 자료 품질

- ✅ 근거 제품이 구체적: PostgreSQL(WAL shipping), Kafka(min.ISR), Kubernetes(stacked vs external
  etcd), Vault(Raft), Consul(quorum), Patroni
- ✅ **Google Cloud PostgreSQL HA 문서**를 명시적으로 인용
- ✅ Raft/Paxos를 이름만 대지 않고 **"무엇에 동의하게 만드는가"** 4항목으로 정의
- ✅ 출처 없는 수치 없음
- ⚠️ Raft 논문(Ongaro & Ousterhout, 2014)과 Paxos 논문의 서지 정보 없음
- ⚠️ **Paxos 설명이 한 줄뿐** — Raft는 세 상태와 선거 절차까지 다루면서 Paxos는 인용문 한 줄로
  끝난다. 비교가 아니라 나열이다.
- ⚠️ Patroni가 왜 세 계층 조합인지 설명이 없음(위 참조)

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Replication and consensus]] · [[CAP theorem]] · [[Distributed system limits]] ·
  [[Distributed processing]] · [[Data SLA and observability]]
- 도구: [[Apache Kafka]]
- 앞: [[AI DE Course - Part4 Ch1 CAP theorem and system limits]]
- 다음: [[AI DE Course - Part4 Ch2 Redis and the caching layer]]

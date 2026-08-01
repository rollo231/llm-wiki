---
type: concept
title: Distributed system limits
area: [data-engineering]
aliases: [분산 시스템의 한계, 부분 실패, Partial Failure, FLP, 전역 시계 부재, Lamport]
tags: [data-engineering, distributed-systems, flp, lamport, partial-failure, consensus]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch1 CAP theorem and system limits]]"]
---

# Distributed system limits

**[[CAP theorem]]보다 더 근본적인, 분산 시스템이 이론적으로 넘을 수 없는 세 가지 한계.**

> **"구현 난이도만의 문제가 아니다. 아무리 잘 만들어도 동시에 완전히 만족시킬 수 없는 성질이
> 존재한다."**

전제 넷: 일부 노드만 실패 가능 · 네트워크는 지연되거나 끊길 수 있음 ·
**모든 노드가 같은 "현재"를 공유하지 않음** · 한 노드에서 본 상태와 다른 노드에서 본 상태가
순간적으로 다를 수 있음.

## 1. 부분 실패 (Partial Failure)

| | 실패의 모습 |
|---|---|
| **단일 서버** | 비교적 단순 — 프로세스가 죽거나, 머신이 죽거나, 디스크가 망가진다 |
| **분산 시스템** | 애매하다 |

분산 시스템에서 애매한 이유:

- 어떤 노드는 살아있고, 어떤 노드는 죽음
- 네트워크는 **일부 링크만** 느려질 수 있음
- 메시지는 아주 늦게 도착할 수 있음
- ⭐ **관찰자마다 누가 죽었는지 다르게 보인다**

> **"부분적으로 실패한 세계에서 전체가 하나처럼 행동하게 만드는 것."**

**마지막 항목이 핵심이다.** "A가 죽었다"는 사실조차 합의의 대상이 된다 — 이것이
[[Replication and consensus]]에서 split brain이 발생하는 이유다.

**실무적 함의:** 장애 대응에서 **"어느 관측 지점에서 본 상태인가"** 를 항상 명시해야 한다.
[[Data SLA and observability]]의 label 설계(`gpu_node`, `service`)가 이 문제의 관측 측 대응이다.

## 2. 전역 시계 부재 — Lamport

**Leslie Lamport**, *Time, Clocks, and the Ordering of Events in a Distributed System*.

> ⭐ **"분산 시스템에서는 두 사건 중 무엇이 먼저 일어났는지 말하는 것이 때때로 불가능하다."**

**이유:** 메시지 전달 지연이 무시할 수 없고, 모든 노드가 동일한 시계를 공유하지 않는다.

**결과:**

- **"먼저 쓴 값"을 정의하기가 어렵다**
- 로그 정렬, 충돌 해결, 복제 순서 결정이 어렵다
- 트랜잭션 외부 일관성(external consistency)을 얻으려면 **추가 장치**가 필요하다

### ⭐ 같은 문제가 애플리케이션 계층에서 반복된다

**[[Stream processing semantics]]의 event time 문제가 Lamport 문제의 응용 계층 버전이다.**

| 계층 | 문제 | 대응 |
|---|---|---|
| **시스템** | 두 사건 중 무엇이 먼저인가 | 논리 시계(Lamport clock), 벡터 시계, 하이브리드 시계 |
| **스트림 처리** | 이 이벤트는 어느 시간 구간에 속하는가 | **event time + 워터마크** |
| **모델 모니터링** | 이 예측과 이 라벨은 언제의 것인가 | **`prediction_time`과 `label_event_time` 분리** |

**세 층 모두 "시각을 데이터에 실어 보내고, 언제까지 기다릴지 규칙을 정한다"는 같은 해법을 쓴다.**
[[AI DE Course - Part4 Ch3 Event time watermarks and windows]] 참조.

## 3. FLP 불가능성

**Fischer, Lynch, Paterson** — 완전 비동기 모델에서 **프로세스 하나만 실패할 수 있어도**
deterministic consensus protocol이 항상 결정을 내리도록 보장할 수 없다.

> **"단 1대의 고장만 있어도 언제나 완벽하게 작동하는 합의 방식은 존재하지 않는다. 따라서 이런
> 통신 환경에서는 완벽한 합의를 이끌어내는 문제를 아예 풀 수가 없다."**

**전제 조건 셋:**

1. 네트워크 지연 상한이 없고
2. 시계 동기화도 없고
3. **실패 감지도 확실하지 않다면**

→ **언젠가 반드시 모두가 합의하게 만드는 것은 이론적으로 불가능.**

**3번이 [[CAP theorem]]의 "메시지 손실과 메시지 지연은 구별하기 어렵다"와 같은 사실이다.**
"응답이 없다"가 "죽었다"인지 "느리다"인지 구별할 수 없으면 실패 감지가 확실할 수 없다.

## ⭐ 실무의 회피 — 부분 동기성

> **"실무 시스템은 FLP를 무시하지 않는다. 대신 완전 비동기 모델을 버리고, 어느 정도의 synchrony
> 가정을 도입한다."**

| 현실 시스템이 하는 일 | FLP의 어느 전제를 깨나 |
|---|---|
| **timeout을 둔다** | ① 지연 상한이 없다 → **있다고 가정한다** |
| **leader를 선출한다** | 결정 주체를 하나로 좁혀 비결정성을 줄인다 |
| **일정 시간 이후 네트워크가 안정될 것이라고 기대한다** | 부분 동기 모델(partial synchrony) |

> ⭐ **"현실적인 방식으로 불가능성을 회피한다."**

**이것이 Raft의 election timeout이 존재하는 이유다.** [[Replication and consensus]]의
"선거 타임아웃 → 후보 → 과반수 득표"는 FLP 회피의 구체적 구현이다.

**그리고 이 타협에는 대가가 있다:** timeout이 너무 짧으면 살아있는 리더를 죽었다고 판단해
불필요한 선거가 반복되고, 너무 길면 장애 감지가 느려진다. **RTO가 결국 이 값에 묶인다.**

## 이 한계들을 실무에서 만나는 지점

| 증상 | 뿌리 |
|---|---|
| **split brain** — 양쪽이 동시에 primary라고 믿음 | 부분 실패 + 실패 감지 불확실성 |
| **로그 순서가 노드마다 다름** | 전역 시계 부재 |
| **etcd quorum loss로 클러스터 전체가 정지** | FLP 회피의 대가 — 과반수 없이는 진행 불가 |
| **"타임아웃 값을 몇 초로 할까"라는 끝없는 논쟁** | 부분 동기성 가정의 튜닝 문제 |
| **늦게 온 이벤트가 집계를 틀어놓음** | 전역 시계 부재의 애플리케이션 버전 |

## ⚠️ 이 위키에 아직 없는 것

- **Lamport clock / vector clock의 실제 동작** — 강의는 논문을 인용만 하고 논리 시계를 설명하지
  않는다.
- **TrueTime / HLC (Hybrid Logical Clock)** — Spanner가 "추가 장치"로 시계 불확실성 구간을 어떻게
  다루는지. **강의에 없다.**
- **비잔틴 장애** — 강의는 "악의적인 공격"을 불안정성 목록에 한 번 넣고 다루지 않는다.
- 논문 서지 정보 — Lamport(1978, CACM), FLP(1985, JACM), Gilbert & Lynch(2002, SIGACT News).
  **강의는 저자 이름만 표기한다.**

## 관련 페이지

- [[CAP theorem]] — 이 한계들 위에서 무엇을 포기할지 고르는 정리
- [[Replication and consensus]] — 한계를 현실적으로 회피하는 구현
- [[Distributed processing]] — 왜 이런 시스템을 만드는가
- [[Stream processing semantics]] — 전역 시계 부재의 응용 계층 버전
- [[Data SLA and observability]] — 부분 실패를 관측하는 법

## 출처

- [[AI DE Course - Part4 Ch1 CAP theorem and system limits]]

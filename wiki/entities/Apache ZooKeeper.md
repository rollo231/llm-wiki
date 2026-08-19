---
type: entity
title: Apache ZooKeeper
area: [data-engineering]
aliases: [ZooKeeper, 주키퍼, 코디네이션, coordination service, 리더 선출, leader election, Apache Ratis, Ratis, 분산 락, distributed lock]
tags: [data-engineering, apache, zookeeper, consensus, coordination, distributed-systems]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch2 Distributed foundations]]"]
---

# Apache ZooKeeper

**분산 시스템의 공동 상태 관리자이자 조정자.** 작은 설정 정보와 상태 값을 안전하게 보관하고,
여러 서버가 동시에 바꾸려 할 때 **순서를 정한다.**

⭐ **데이터 자체보다 "누가 무엇을 맡는지"를 맞추는 계층이다.**

> 서버가 한 대일 때는 *"누가 책임자인지", "지금 설정값이 무엇인지"* 를 묻지 않아도 된다. 여러 대가
> 되면 **이 약속이 어긋나면 데이터가 두 벌로 갈라지거나, 같은 작업을 두 리더가 동시에 처리하는 사고가
> 난다.**

## 하는 일 넷

| | |
|---|---|
| **리더 선출** | 여러 서버 중 누가 지휘를 맡을지 정한다 |
| **설정 공유** | 모든 노드가 같은 설정값을 읽게 한다 |
| **생존 확인** | 어떤 서버가 살아 있는지 추적한다 |
| **잠금·순서** | 동시에 일어나면 안 되는 작업을 줄 세운다 |

전통적으로 [[Apache Kafka]] · [[Apache HBase]] · [[Apache Hadoop]] 클러스터가 오랫동안 여기에 기대 왔다.

## ⭐⭐ 합의 계층은 선택이 아니라 형태만 선택이다

> **"분산 시스템에서 '한 대의 진실'을 여러 대가 공유하려면, ZooKeeper 같은 외부 서비스든 Ratis 같은
> 내장 라이브러리든 합의 계층이 필요하다."**

| | 형태 | 성격 |
|---|---|---|
| 🔹 **ZooKeeper** | **완성된 코디네이션 서비스** | 애플리케이션이 붙여 쓰는 **외부 중재자**. 운영할 클러스터가 하나 더 늘어난다 |
| 🔸 **Apache Ratis** | **Raft 구현 라이브러리** | **제품 코드에 넣어 쓰는 재료.** 외부 의존은 없어지고 합의 운영이 제품 안으로 들어온다 |

**Ratis**는 Raft를 구현해 여러 노드가 같은 로그를 복제하고 리더를 선출하도록 돕는다.
*"'리더는 누구인가', '이 쓰기를 과반수가 받아들였는가'를 매번 처음부터 구현하기는 어렵다"* — 그 뼈대다.
Apache **Ozone** 등이 Ratis로 고가용 메타데이터·복제 계층을 구성한다.

⭐ 사용자 입장에서 외울 것은 API가 아니라 문장 하나다 — **"이 시스템이 Raft로 상태를 맞춘다."**
→ [[Replication and consensus]]

## ⚠️ 외부 → 내장으로 옮겨 가는 흐름

> *"요즘 일부 시스템은 ZooKeeper 없이 자체 합의 계층으로 넘어가기도 한다."*

⭐ **[[Apache Kafka]]의 KRaft 전환이 정확히 이 축의 이동이다** — 외부 ZooKeeper 앙상블을 걷어내고
Raft를 브로커 안에 넣었다. 즉 위 표의 🔹 → 🔸 이동이고, **얻는 것은 운영 컴포넌트 하나 감소, 내는 것은
합의 장애가 제품 장애와 한 몸이 된다는 점**이다.

그래도 ZooKeeper를 알아야 하는 이유는 남는다 — **분산 시스템이 어떻게 하나의 상태에 합의하는지**를
이해하는 가장 짧은 길이고, 눈에 잘 띄지 않는 **기반 계층의 대표**이기 때문이다.
→ [[Apache Map - Ch1 How to read this book]]의 5역할에서 *가로지르는 기반 계층*

## 위키 안에서의 위치

- [[Replication and consensus]] — Raft·과반수의 원리. **이 페이지는 그 원리를 어디에 두는지**를 다룬다.
- [[Distributed system limits]] — 전역 시계 부재·FLP. 합의 계층이 존재해야 하는 이유의 밑바탕.
- [[Cluster resource scheduling]] — *"YARN이 자원을 나눈다면 ZooKeeper는 그 위에서 상태를 맞춘다."*
- [[Apache Kafka]] · [[Apache HBase]] · [[Apache Hadoop]] — 오래 기대 온 쪽.
- [[CAP theorem]] — 합의는 가용성을 일부 내주고 일관성을 사는 장치다.

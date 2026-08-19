---
type: concept
title: Cluster resource scheduling
area: [data-engineering]
aliases:
  - 클러스터 리소스 스케줄링
  - 리소스 스케줄러
  - resource scheduler
  - Apache Hadoop YARN
  - YARN
  - ResourceManager
  - NodeManager
  - ApplicationMaster
  - Apache YuniKorn
  - YuniKorn
  - 큐
  - queue
  - 공정 분배
  - fair share
tags: [data-engineering, scheduling, yarn, kubernetes, yunikorn, resource-management]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch2 Distributed foundations]]"]
---

# Cluster resource scheduling

**클러스터의 CPU·메모리는 한정되어 있고, 작업이 한꺼번에 몰리면 "누가 먼저, 얼마나 쓸지"를 정해야
한다.** 정하지 않으면 **어떤 작업은 자원을 독식하고 어떤 작업은 끝없이 기다린다.**

[[Data orchestration]]이 *"언제, 어떤 순서로"* 를 맡는다면, 이 층은 *"어떤 자원으로"* 를 맡는다 —
[[Apache Map - Ch1 How to read this book]]의 5역할에서 **가로지르는 기반 계층**이다.

## ⭐⭐ YARN이 한 일 — 저장과 처리의 결합을 풀었다

> "YARN이 생기기 전 Hadoop은 **저장(HDFS)과 처리(MapReduce)가 더 단단히 묶여 있었다.** YARN이
> 등장하면서 **'저장은 그대로 두고, 위에서 돌아가는 엔진은 다양하게'** 라는 구조가 가능해졌다."

그래서 [[Apache Spark]]처럼 MapReduce가 아닌 엔진도 **같은 클러스터 위에서** YARN의 자원을 받아
실행하게 됐다. **한 클러스터를 여러 엔진이 공유하는 토대**다.

⭐ **이건 레이크하우스가 한 일과 같은 움직임이 한 세대 먼저, 한 층 아래에서 일어난 것이다.**

| | 무엇을 떼어냈나 |
|---|---|
| **YARN** (2010년대 초) | 저장(HDFS) ↔ **처리 엔진** |
| **레이크하우스 / 테이블 포맷** | 저장(오브젝트 스토리지) ↔ **쿼리 엔진** |

→ [[Analytical data storage tiers]]의 *쿼리 엔진 결합 축* · [[Table formats]] · [[SQL execution layer]].
**"결합을 풀면 그 자리에 선택 문제가 생긴다"** 는 것도 두 번 다 같다.

### YARN의 3 컴포넌트

| | 역할 |
|---|---|
| 1️⃣ **ResourceManager** | 클러스터 전체의 CPU·메모리를 파악하고 나눈다 |
| 2️⃣ **NodeManager** | 각 서버에서 실제 **컨테이너를 띄우고 감시**한다 |
| 3️⃣ **ApplicationMaster** | 개별 애플리케이션이 필요한 자원을 **요청**한다 |

⭐ 실무 진입점은 진단이다 — **"이 작업이 왜 대기열에 걸려 있지?"** 라는 질문의 **원인 추적 출발점**이
이 세 컴포넌트다. 클라우드·K8s가 보편화된 지금도 온프레미스 Hadoop이나 EMR·Dataproc 같은 관리형
클러스터에서 자주 만난다.

## ⭐⭐ K8s 기본 스케줄러는 데이터 작업에 애매하다 — YuniKorn

> **"기본 Kubernetes 스케줄러는 일반적인 서비스 Pod에는 잘 맞지만, 데이터 작업처럼 이벤트나 배치 기반
> 패턴에 쓰기에는 애매한 경우가 있다."**

**Apache YuniKorn**은 YARN의 생각을 클라우드 네이티브로 가져온 스케줄러다. Kubernetes나 YARN 위에서
배치·스트리밍 작업이 자원을 놓고 다툴 때 조율한다.

가져온 개념 셋: **큐(queue)** · **공정 분배** · **애플리케이션 단위 스케줄링**.
Spark on Kubernetes처럼 **큰 작업이 공존하는 환경**에 특히 맞는다.

### ⭐ 도입 신호가 구체적이다

검토할 때:

- 배치와 스트리밍이 **한 클러스터에서 자원을 나눠 쓸 때**
- **팀·큐별로 사용량을 제한**하거나 우선순위를 주고 싶을 때
- YARN에서 익숙한 스케줄링 방식을 Kubernetes로 옮기고 싶을 때

⭐⭐ 그리고 **관찰 가능한 증상 하나**를 판단 기준으로 준다 —
**"데이터 작업이 자원을 독점해 서비스 Pod가 자원을 배정받지 못하는 현상이 반복된다면."**

⚠️ **모든 조직의 기본값은 아니다. 작은 규모에서는 K8s 기본 스케줄러로도 충분할 수 있다.**

> **"스케줄러는 제품이 바뀌어도 하는 일의 본질은 같다."**

### 위키의 기존 공백과의 관계

[[GPU resource allocation]] §이 위키에 아직 없는 것이 **gang scheduling(Kueue·Volcano)** 을 공백으로
지목했다. YuniKorn의 **"애플리케이션 단위 스케줄링"** 이 같은 축으로 보이지만, ⚠️ **소스가 gang
scheduling이라는 말을 쓰지 않으므로 동일하다고 단정하지 않는다** — 확인이 필요하다.

그 페이지의 K8s 정책 6종(node label · taint/toleration · nodeSelector/affinity · **priorityClass** ·
**namespace quota** · resource request/limit)과 이 페이지의 **큐·공정 분배**는 층이 다르다:
전자는 *"어디에 놓을지"*, 후자는 *"누가 얼마나 받을지"*.

## 정리

| 층 | 무엇을 정하나 | 대표 |
|---|---|---|
| **오케스트레이션** | 언제, 어떤 순서로 | [[Apache Airflow]] → [[Data orchestration]] |
| **리소스 스케줄링** | **누가 얼마나 쓸지** | YARN · YuniKorn · K8s scheduler |
| **코디네이션** | 누가 리더이고 상태가 무엇인지 | [[Apache ZooKeeper]] |

⭐ *"YARN이 자원을 나눈다면, ZooKeeper는 그 위에서 상태를 맞추는 코디네이션 계층이다."*
그리고 **저장과 스케줄이 나란히 있어야 클러스터가 돌아간다.**

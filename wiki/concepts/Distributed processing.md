---
type: concept
title: Distributed processing
area: [data-engineering]
aliases: [분산 처리, 분산처리, Distributed System, 분산 시스템, 암달의 법칙, Amdahl's law]
tags: [data-engineering, distributed-systems, scalability, sharding, hadoop, spark]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch1 Distributed processing basics]]"]
---

# Distributed processing

**데이터와 계산을 여러 노드에 분산시키고, 네트워크를 통해 이들을 조정하여 "하나의 시스템"처럼
동작하게 만드는 처리 방식.**

> ⭐ **"분산 도입의 출발점은 '데이터가 크다'가 아니라 '단일 서버로도 감당 가능한가'이다."**

이 페이지는 **분산이 왜 필요한가**와 **언제 필요하지 않은가**를 함께 다룬다. 분산의 *대가*는
[[CAP theorem]] · [[Distributed system limits]] · [[Replication and consensus]]에서 이어진다.

## 왜 등장했나 — 구글의 세 논문

| 연도 | 논문 | 기여 |
|---|---|---|
| 2003 | **GFS** (Google File System) | 큰 파일을 64MB 청크로 쪼개 수천 대의 저가형 서버에 분산 저장. 각 청크를 **3군데 이상 복제** |
| 2004 | **MapReduce** | Map(로컬 계산) → Shuffle(정렬·병합) → Reduce(통합) |
| 2006 | **BigTable** | 대규모 분산 데이터베이스 |

> ⭐ **GFS의 설계 철학: "하드웨어는 언제든 고장 날 수 있다는 전제하에 소프트웨어로 신뢰성을
> 보장한다."** 이 전제가 분산 시스템 전체의 출발점이다.
>
> ⭐ **MapReduce의 전략: "데이터를 계산기로 가져오지 말고, 계산기를 데이터가 있는 곳으로 보내자."**

이 논문들을 보고 더그 커팅이 [[Apache Hadoop]]을 만들었고, 하둡의 디스크 I/O 한계를 극복하기 위해
[[Apache Spark]]가 나왔다(In-Memory + DAG). 계보는 [[Apache Hadoop]] 페이지 참조.

## ⭐ 분산의 대상 4종

"분산 = 서버 여러 대"라는 뭉뚱그림을 깨는 분류다.

| 대상 | 뜻 | 예 |
|---|---|---|
| **데이터 분산** | 하나의 큰 데이터를 여러 노드에 나누어 저장 | [[Apache Kafka]]의 topic partition, HDFS block, 샤딩된 테이블 |
| **계산 분산** | 입력을 여러 조각으로 나누고 각 노드가 일부를 병렬 처리 | [[Apache Spark]] executor가 여러 task를 병렬 수행 |
| **상태 분산** | 집계·세션·윈도우·캐시·중간 결과를 여러 노드에 나눠 보관 | [[Apache Flink]]의 stateful stream processing |
| **장애 허용 분산** | 한 노드가 실패해도 다른 노드가 이어받도록 복제본과 재실행 경로를 둠 | Kafka replication, PostgreSQL standby |

**이 4분류가 실무의 축과 대응한다** — 데이터 분산은 파티셔닝 전략, 상태 분산은
[[Stream processing semantics]], 장애 허용 분산은 [[Replication and consensus]].

## 단일 서버 vs 분산

| | 단일 서버 처리 | 분산 처리 |
|---|---|---|
| | 한 머신 안에서 저장·계산·상태 관리가 대부분 이뤄짐 | 여러 머신에 데이터와 계산이 나뉨 |
| | 메모리·디스크·CPU·프로세스 경계가 단순 | 노드 간 통신과 동기화 필요 |
| | **디버깅과 운영 구조가 명확** | **일부 노드 실패를 전제로 설계** |
| | 장애 시 영향 범위가 한 노드에 집중 | 결과를 하나의 일관된 시스템처럼 보이게 만들어야 함 |

### ⭐ 단일 서버는 더 이상 작은 장난감이 아니다

| AWS 계열 | 스펙 |
|---|---|
| **U7i** (고메모리) | 최대 **32 TiB 메모리 / 1920 vCPU** — 대형 인메모리 데이터베이스 용도 |
| **I4i** (스토리지 최적화) | 최대 **30 TB 로컬 NVMe SSD** — 높은 I/O, 낮은 지연 변동성 |

단일 서버로 커버 가능한 범위: 대용량 배치 · 일부 피처 생성 · 중간 규모 OLAP ·
캐시/검색용 상태 저장 · 로컬 데이터셋 기반 분석.

### 그럼에도 남는 단일 서버의 한계 4가지

**CPU나 메모리 숫자가 부족하다는 뜻이 아니다:**

1. **장애 도메인이 하나** — 서버가 멈추면 그 위의 계산·상태·캐시·서비스가 함께 멈춤
2. **자원 확장의 결합** — 메모리만 더 필요해도 CPU·스토리지·네트워크를 함께 사야 함
3. **병렬성의 상한** — 하나의 OS, 하나의 메모리 공간 위에서는 무한정 선형 확장 불가
4. **복구가 무거움** — 거대해질수록 재기동·상태 재적재·캐시 warm-up 비용이 커짐

> **2번이 [[Analytical data storage tiers]]의 "저장·컴퓨트 분리"와 같은 뿌리다.**

## ⭐ 도입 판단 — 세 축이 동시에 정렬될 때만

| 축 | 물어야 할 것 |
|---|---|
| **요구사항** | 처리량·지연시간·가용성·정합성 중 무엇이 핵심인가 |
| **병목** | CPU·메모리·디스크·네트워크·동시성·state 크기 중 어디가 실제 문제인가 |
| **운영비용** | 장애 분석·재처리·데이터 재배치·복제·상태 복구 부담을 감수할 가치가 있는가 |

### 숨은 변수 3가지

**1. 데이터 응집도 (Data Affinity)**

- **Join 의존성** — 노드 간 과도한 Network Shuffle을 유발하는 쿼리 패턴이 있는가?
- **샤딩 키 선정** — 특정 노드에 트래픽이 몰리는 **Hotspot** 가능성은?
- **트랜잭션 범위** — 분산 트랜잭션(2PC) 없이도 비즈니스 무결성을 유지할 수 있는가?

> **판단 기준: 데이터를 독립적인 Silo로 격리할 수 있다면 분산 적합도가 매우 높다.**
>
> ⭐ **이것이 [[NoSQL]]의 "파티션 키가 시스템을 결정한다"와 [[Redis]]의 hot key 문제와 같은
> 이야기다.** 세 곳에서 다른 이름으로 나타나는 하나의 제약: **접근이 몰리는 키가 있으면 분산이
> 안 된다.**

**2. 선형 확장성 — 암달의 법칙**

> **"서버가 2배가 된다고 처리량이 2배가 되지는 않는다."**

- **병렬화 불가능 영역** — 전체 로직 중 순차 처리가 강제되는 구간의 비중 `(1-p)`
- **분산 오버헤드** — 데이터 복제, 합의 알고리즘, 네트워크 직렬화 비용
- **판단 기준** — 노드 추가에 따른 성능 향상 곡선이 정체되는 지점이 비즈니스 요구치를 충족하는가?

**3. 운영 성숙도와 가시성**

> **"보이지 않는 문제는 해결할 수 없다."**

- **분산 추적** — 여러 노드를 거치는 요청 흐름을 한눈에 파악할 수 있는가?
- **부분 장애 대응** — 한 노드의 장애가 **Cascading Failure**로 번지지 않도록 격리(Bulkhead)
  되어 있는가?
- **자동화 수준** — 장애 노드 교체, 데이터 재배치(Rebalancing)가 수동 작업 없이 가능한가?

> ⭐ **"인프라 자동화와 모니터링 체계가 구축되지 않은 상태에서의 분산 도입은 '운영 재앙'이다."**

### 병목을 무엇으로 판정하나

| 자원 | 확인 지표 |
|---|---|
| **CPU** | 계산량이 실제로 포화 상태인지 |
| **메모리** | OOM, spill, GC 증가, working set 초과 |
| **디스크** | temp usage, spill file, I/O wait, queue depth |
| **네트워크** | shuffle read/write, remote fetch, cross-node traffic 비중 |

## ⭐ 실용적 분산 — 필요한 축만

> **"최근의 변화는 분산이 사라진 것이 아니라, 분산 복잡성을 사용자가 직접 떠안지 않아도 되는
> 방향으로 진화 중이다."**

대표 흐름: 강력한 단일 서버 · 저장과 컴퓨트 분리 · 관리형 분석 엔진 · 필요한 축만 분산.

| 필요 | 수단 |
|---|---|
| 읽기 확장 | **replica** |
| 비동기 decoupling | **broker** ([[Message broker]]) |
| 대규모 batch | **distributed compute** ([[Apache Spark]]) |
| 스트리밍 정합성 | **stateful streaming engine** ([[Apache Flink]]) |

> **"나머지는 가능한 단순하게 유지. 거대한 자체 분산 시스템보다는 필요한 축만 분산하고 나머지는
> 단순화가 더 현실적."**

**같은 절제가 이 위키의 다른 곳에서도 반복된다:**

- [[Redis]] — *"성능 문제가 생겼다고 곧바로 cluster로 가는 것은 좋은 선택이 아닐 수 있다"*
- [[Inference optimization]] — *"GPU는 마지막 수단"*
- [[Feature store]] — *"공용 변환 로직 → Feature Contract → (필요시) Feature Store"*
- [[Ontology]] — *"OWL은 대체로 과설계"*

**네 페이지 모두 "쓰지 마라"가 아니라 "먼저 해볼 것이 있다"는 순서 규칙이다.**

## GPU에서 반복되는 같은 판단

[[GPU resource allocation]]의 **scale-out vs scale-up** 시나리오가 이 판단의 GPU 버전이다 —
장애 도메인 분산(여러 대의 작은 GPU) vs locality(한 대의 큰 GPU를 MIG로 분할).
**"단일 서버로 충분한가"가 "단일 GPU 노드로 충분한가"로 반복된다.**

## 관련 페이지

- **대가** — [[CAP theorem]] · [[Distributed system limits]] · [[Replication and consensus]]
- **수단** — [[Message broker]] · [[Caching strategies]] · [[Stream processing semantics]]
- **설계 축** — [[Latency and throughput]] · [[NoSQL]] · [[Analytical data storage tiers]]
- **도구** — [[Apache Hadoop]] · [[Apache Spark]] · [[Apache Flink]] · [[Apache Kafka]] · [[Redis]]
- **GPU 버전** — [[GPU resource allocation]] · [[GPU architecture]]

## 출처

- [[AI DE Course - Part4 Ch1 Distributed processing basics]]

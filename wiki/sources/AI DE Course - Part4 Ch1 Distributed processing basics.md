---
type: source
title: AI DE Course - Part4 Ch1 Distributed processing basics
area: [data-engineering]
aliases: [Part4 Ch1-1,2, 분산처리의 개념 이해, 분산 처리의 필요성]
tags: [data-engineering, course, fast-campus, distributed-systems, hadoop, spark, gfs, mapreduce, amdahl]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf (p2–31)"]
---

# AI DE Course - Part4 Ch1 Distributed processing basics

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 4 "실시간 & 대규모 데이터 분산 처리 설계"**
Ch1 "분산 처리의 필요성과 주의사항"의 소단원 **1 "분산처리의 개념 이해"** + **2 "분산 처리의 필요성"**.
원본(로컬): `raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` **p2–31** (356p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐ **이 두 소단원은 방향이 정반대다.** 소단원 1은 "왜 분산이 등장했나"(GFS→MapReduce→Hadoop→Spark)
> 를 정직한 역사로 훑고, 소단원 2는 **"그런데 정말 필요한가"** 로 되받는다. 분산 처리 챕터를
> **분산 반대 논변으로 여는 구성**이 이 코스에서 드물게 좋은 판단이다.

## 구성

소단원 1: `01 분산 처리의 등장 배경 · 02 GFS · 03 Map Reduce · 04 Hadoop · 05 Apache Spark`
소단원 2: `01 분산처리는 꼭 필요할까? · 02 단일서버 · 03 분산 처리 · 04 분산 처리의 필요성과 판단
기준 · 05 최근의 분산 시스템`

---

## 소단원 1 — 계보 (p2–14)

### 등장 배경

과거에는 기업 내부 DB 정도만 관리하면 됐지만 인터넷·모바일 보급으로 데이터가 기하급수적으로 늘어
**단일 서버(scale-up)로는 수십 TB~PB를 저장·처리하는 것이 물리적으로 불가능**해졌다.

세 가지 문제로 정리한다:

- 큰 데이터를 빠르게 읽고 써야 하는 문제
- **여러 머신 중 일부가 항상 고장 날 수 있다는 현실**
- 대규모 계산을 사람이 직접 병렬화·재시도·복구하기 어려운 문제

### 구글의 세 논문

| 연도 | 논문 | 내용 |
|---|---|---|
| 2003 | **GFS** (Google File System) | 거대한 데이터를 분산 저장하는 방법 |
| 2004 | **MapReduce** | 흩어진 데이터를 병렬 처리(Map)하고 합치는(Reduce) 알고리즘 |
| 2006 | **BigTable** | 대규모 분산 데이터베이스 |

> **"이 논문들이 자극제가 되어 오픈소스 프로젝트인 Hadoop이 탄생."**

### GFS

- 하나의 큰 파일을 **64MB 단위의 청크(Chunk)** 로 쪼개 수천 대의 저가형 서버에 분산 저장
- **복제(Replication)**: 각 청크를 기본 **3군데 이상**의 서로 다른 서버에 복사
- 한 대가 고장 나도 서비스 가능

> ⭐ **"하드웨어는 언제든 고장 날 수 있다는 전제하에 소프트웨어로 신뢰성을 보장."**
>
> 이 한 줄이 분산 시스템 설계 철학의 출발점이고, Ch1-3(CAP)과 Ch1-4(복제·합의) 전체의 전제다.

원논문의 Figure 1 (GFS Architecture — GFS master / chunkserver / client의 control message vs
data message 분리)을 그대로 인용한다.

### MapReduce

> ⭐ **"데이터를 계산기로 가져오지 말고, 계산기를 데이터가 있는 곳으로 보내자."**

`Map`(각 서버가 가진 데이터를 로컬에서 먼저 계산) → `Shuffle`(중간 결과를 네트워크로 정렬·병합) →
`Reduce`(최종 통합).

> **의의: "복잡한 병렬 프로그래밍을 몰라도 개발자가 함수 두 개(Map, Reduce)를 통해 수천 대의
> 컴퓨터를 동시에 돌릴 수 있게 만들었다."**

원논문의 execution overview 그림(User Program → fork → Master → assign map/reduce → worker →
intermediate files on local disks → output files)을 인용.

### Hadoop (2006)

구글 논문을 보고 **더그 커팅(Doug Cutting)** 이 자바로 구현한 오픈소스. HDFS = GFS 구현,
Hadoop MapReduce = MapReduce 구현.

**한계:** 단계마다 결과를 디스크(HDD/SSD)에 썼다가 다시 읽어야 한다. **작업이 수십 단계면 수십 번의
디스크 I/O가 발생.**

### Apache Spark (2010)

- **In-Memory 처리** — 데이터를 디스크가 아닌 RAM에 올려서 처리. "메모리는 디스크보다 수천 배 빠른
  것에 착안"
- **DAG (Directed Acyclic Graph)** — 하둡처럼 단계별로 하지 않고 전체 작업 경로를 미리 그려서
  최적화된 경로로 한 번에 처리 (**Lazy Execution**)
- 원 논문의 동기를 인용: *iterative algorithms, interactive data mining tools* — "데이터를 메모리에
  유지하면 성능이 크게 향상될 수 있는 문제들"에 디스크 중심 프레임워크는 비효율적

> ⚠️ **"하둡보다 특정 작업에서 최대 100배 빠르며"** — 출처 없음. 이 수치는 Spark 프로젝트의 초기
> 마케팅(로지스틱 회귀 반복 벤치마크)에서 온 것으로 알려져 있고, **"특정 작업에서"라는 단서가
> 붙어야만 성립한다.** 일반적인 ETL에서 100배는 나오지 않는다.

Spark 아키텍처 도식(Driver Program/SparkContext ↔ Cluster Manager ↔ Worker Node/Executor/Task/Cache)
과 Hadoop 에코시스템 전체도(ZooKeeper·Storm·Hive·Pig·HBase·Cassandra·YARN·HDFS·Kafka)를 인용한다.

---

## 소단원 2 — ⭐ 그런데 정말 필요한가 (p15–31)

### 통념 뒤집기

> ⭐ **"분산이 멋져 보이는가가 아니라 단일 서버로도 충분한가."**

최근 하드웨어 발전으로 단일 서버의 처리 가능 범위가 확대됐다. 하지만 남는 문제 넷: 단일 장애 도메인 ·
독립적 확장 불가 · 상태 복구와 고가용성 · 대규모 병렬 스트리밍 처리.

### 단일 서버 재평가 — 구체적 스펙으로

> **"단일 서버는 더 이상 작은 장난감이 아님."**

| 계열 | 스펙 | AWS의 포지셔닝 |
|---|---|---|
| **U7i** (고메모리) | 최대 **32 TiB 메모리 / 1920 vCPU** | 대형 인메모리 데이터베이스 |
| **I4i** (스토리지 최적화) | 최대 **30 TB 로컬 AWS Nitro SSD** | 높은 I/O 성능, 낮은 지연, 낮은 지연 변동성 |

단일 서버로 해결 가능한 범위: 대용량 배치 · 일부 피처 생성 · 중간 규모 OLAP · 캐시/검색용 상태 저장 ·
로컬 데이터셋 기반 분석.

> ⭐⭐ **"분산 도입의 출발점은 '데이터가 크다'가 아니라 '단일 서버로도 감당 가능한가'."**

**이 수치들은 검증했다 — 실제와 맞는다.** Part 1의 출처 없는 "80%" 관행과 다르게, 벤더 인스턴스
스펙이라는 확인 가능한 근거를 든다.

### 단일 서버의 물리적 한계 — CPU/메모리 숫자 문제가 아니다

1. **장애 도메인이 하나** — 서버가 멈추면 그 위의 계산·상태·캐시·서비스가 함께 멈춤
2. **자원 확장의 결합** — 메모리만 더 필요해도 CPU·스토리지·네트워크를 함께 사야 함
3. **병렬성의 상한** — 하나의 OS, 하나의 메모리 공간, 하나의 로컬 디스크 경로 위에서는 무한정 선형
   확장 불가
4. **복구가 무거움** — 거대해질수록 장애 시 재기동·상태 재적재·캐시 warm-up·로컬 스토리지 재동기화
   비용이 커짐

> **2번이 특히 실무적이다.** "메모리만 더 필요한데 인스턴스 타입을 통째로 올려야 하는" 상황은
> [[Analytical data storage tiers]]의 **저장·컴퓨트 분리** 논지와 같은 뿌리다.

### 분산 처리의 정의와 ⭐ 분산의 대상 4종

> **"하나의 일을 여러 노드가 나눠 맡고, 그 결과를 다시 하나의 시스템처럼 동작하게 만드는 방식."**

| 대상 | 뜻 | 예 |
|---|---|---|
| **데이터 분산** | 하나의 큰 데이터를 여러 노드에 나누어 저장 | [[Apache Kafka]]의 topic partition, HDFS block, 샤딩된 테이블 |
| **계산 분산** | 입력을 여러 조각으로 나누고 각 노드가 일부를 병렬 처리 | Spark executor가 여러 task를 병렬 수행 |
| **상태 분산** | 집계·세션·윈도우·캐시·중간 결과를 여러 노드에 나눠 보관 | Flink의 stateful stream processing |
| **장애 허용 분산** | 한 노드가 실패해도 다른 노드가 이어받도록 복제본과 재실행 경로를 둠 | Kafka replication, PostgreSQL standby |

> ⭐ **이 4분류가 Part 4 전체의 목차와 같다.** 데이터 분산 → Ch1, 상태 분산 → Ch3(스트림 상태),
> 장애 허용 분산 → Ch1-4(복제·합의). **"분산 = 서버 여러 대"라는 뭉뚱그림을 깨는 게 목적이다.**

단일 서버 처리 vs 분산 처리의 대비도 명확하다 — 전자는 "디버깅과 운영 구조가 명확, 장애 시 영향
범위도 한 노드에 집중", 후자는 "일부 노드 실패를 전제로 설계, 결과를 하나의 일관된 시스템처럼 보이게
만들어야 함".

### ⭐ 도입 판단 — 세 축이 동시에 정렬될 때만

> **"요구사항 · 병목 · 운영비용, 이 세 축이 동시에 정렬될 때만 분산 도입이 설계적으로 정당화된다."**

| 축 | 물어야 할 것 |
|---|---|
| **요구사항** | 처리량·지연시간·가용성·정합성 중 무엇이 핵심인가 |
| **병목** | CPU·메모리·디스크·네트워크·동시성·state 크기 중 어디가 실제 문제인가 |
| **운영비용** | 분산 도입으로 생기는 장애 분석·재처리·데이터 재배치·복제·상태 복구 부담을 감수할 가치가 있는가 |

### 숨은 변수 3가지

**1. 데이터 응집도 (Data Affinity)**

- **Join 의존성**: 노드 간 과도한 네트워크 통신(Network Shuffle)을 유발하는 쿼리 패턴이 있는가?
- **샤딩 키 선정**: 특정 노드에 트래픽이 몰리는 **Hotspot** 가능성은?
- **트랜잭션 범위**: 분산 트랜잭션(2PC 등) 없이도 비즈니스 무결성을 유지할 수 있는가?

> **판단 기준: "데이터를 독립적인 Silo로 격리할 수 있다면 분산 적합도가 매우 높음."**

이것이 [[NoSQL]](Part 3)의 **"파티션 키가 시스템을 결정한다"** 와 같은 이야기다. **강의가 두 파트를
잇지 않지만 같은 논지다.**

**2. 선형 확장성 — 암달의 법칙과 ROI**

> **"서버가 2배가 된다고 처리량이 2배가 되지는 않는다."**

- **병렬화 불가능 영역 파악**: 전체 로직 중 순차 처리가 강제되는 구간의 비중 `(1-p)` 계산
- **분산 오버헤드**: 데이터 복제, 합의 알고리즘(Consensus), 네트워크 직렬화에 소모되는 비용
- **판단 기준**: 노드 추가에 따른 성능 향상 곡선이 정체되는 지점이 비즈니스 요구치를 충족하는가?

**3. 운영 성숙도와 가시성 (Visibility)**

> **"보이지 않는 문제는 해결할 수 없다."**

- **분산 추적(Distributed Tracing)**: 여러 노드를 거치는 요청 흐름을 한눈에 파악할 수 있는가?
- **부분 장애 대응**: 한 노드의 장애가 **Cascading Failure**로 번지지 않도록 격리(Bulkhead)되어
  있는가?
- **자동화 수준**: 장애 노드 교체, 데이터 재배치(Rebalancing)가 수동 작업 없이 가능한가?

> ⭐ **판단 기준: "인프라 자동화와 모니터링 체계가 구축되지 않은 상태에서의 분산 도입은
> '운영 재앙'이다."**

### 기술적 지표 — 무엇을 보고 병목을 판정하나

| 자원 | 확인 지표 |
|---|---|
| **CPU** | 계산량이 실제로 포화 상태인지 |
| **메모리** | OOM, spill, GC 증가, working set 초과 |
| **디스크** | temp usage, spill file, I/O wait, queue depth 증가 |
| **네트워크** | shuffle read/write, remote fetch, cross-node traffic 비중 |

### 최근의 분산 시스템 — 직접 운영이 줄고 있다

> **"최근의 변화는 분산이 사라진 것이 아니라, 분산 복잡성을 사용자가 직접 떠안지 않아도 되는
> 방향으로 진화 중."**

대표 흐름: 강력한 단일 서버 · **저장과 컴퓨트 분리** · 관리형 분석 엔진 · 필요한 축만 분산하는 구조.

> ⭐ **실용적 분산 — 축별 처방:**
>
> | 필요 | 수단 |
> |---|---|
> | 읽기 확장 | replica |
> | 비동기 decoupling | broker |
> | 대규모 batch | distributed compute |
> | 스트리밍 정합성 | stateful streaming engine |
>
> **"나머지는 가능한 단순하게 유지. 거대한 자체 분산 시스템보다는 필요한 축만 분산하고 나머지는
> 단순화가 더 현실적."**

이 표가 사실상 **Part 4 나머지 챕터의 안내도**다 — replica는 Ch1-4, broker는 Ch3-1, stateful
streaming engine은 Ch3-2~4.

## 기존 페이지와의 대조

- **새 concept:** [[Distributed processing]]
- **새 entity:** [[Apache Hadoop]] · [[Apache Spark]]
- **[[Latency and throughput]](Part 1)의 물리적 근거가 여기서 확장된다.** Part 1은 "CPU·네트워크·
  디스크" 세 축을 들었고, 여기는 거기에 **암달의 법칙과 분산 오버헤드**를 더한다.
- ⚠️ **Part 1 CH02-1,2,3([[AI DE Course - Ch2-1,2,3 Storage evolution]])과 겹치지만 각도가 다르다.**
  Part 1은 저장소 관점(사일로→DW→Lake→Lakehouse)에서 하둡을 다뤘고, 여기는 **계산 모델 관점**
  (GFS→MapReduce→Spark)이다. 모순은 아니고 보완이다.
- **[[NoSQL]](Part 3)과의 연결을 강의가 놓친다** — 샤딩 키/hotspot 논의가 두 파트에 나뉘어 있는데
  서로 인용하지 않는다.

## 자료 품질

**Part 1보다 확연히 낫다.**

- ✅ 구글 3논문의 **연도와 이름을 정확히** 밝히고, GFS·MapReduce **원논문의 그림을 그대로 인용**
- ✅ AWS 인스턴스 스펙(U7i 32TiB/1920vCPU, I4i 30TB)이 **검증 가능하고 실제와 맞음**
- ✅ Hadoop 아키텍처 그림에 출처 URL 표기 (geeksforgeeks)
- ⚠️ **"하둡보다 최대 100배"** — 출처 없음 (Spark 프로젝트 자체 주장)
- ⚠️ **"메모리는 디스크보다 수천 배 빠르다"** — 어느 계층(L1? DRAM?) 대비 어느 디스크(HDD? NVMe?)인지
  없음. NVMe 대비 DRAM은 수천 배가 아니라 수백 배 수준이다.
- ⚠️ **중복 슬라이드**: p6/p7 완전 동일(GFS), p10/p11/p12 거의 동일(Hadoop), p13/p14 거의 동일(Spark),
  p21/p22 완전 동일, p94/p95 완전 동일
- ⚠️ **섹션 헤더 불일치**: p11~p14의 헤더가 "02. 분산처리의 기반개념들"인데 목차와 다른 슬라이드
  헤더는 "04. Hadoop" / "05. Apache Spark"다. **이전 버전 목차의 잔재**로 보인다.
- ⚠️ 오타: p4 **"단일 서버(Sacle-up)"** → Scale-up

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Distributed processing]] · [[Latency and throughput]] · [[NoSQL]] ·
  [[Analytical data storage tiers]] · [[Batch and stream processing]]
- 도구: [[Apache Hadoop]] · [[Apache Spark]] · [[Apache Kafka]]
- 앞: [[AI DE Course - Part3 Ch5 Graph databases]] (Part 3 마지막)
- 다음: [[AI DE Course - Part4 Ch1 CAP theorem and system limits]]

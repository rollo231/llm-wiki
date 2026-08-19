---
type: source
title: Apache Map - Ch2 Distributed foundations
area: [data-engineering]
aliases: [Apache 지도 Ch2, Apache 지도 분산 시스템을 떠받치는 기반, Apache Map Ch2]
tags: [data-engineering, apache, distributed-systems, consensus, scheduling, hdfs, book]
created: 2026-08-19
updated: 2026-08-19
sources: [raw/data-engineering/apache/apache-book-full-spread.pdf]
---

# Apache Map - Ch2 Distributed foundations

『Apache로 읽는 데이터 기술의 지도』(이현수, 2026) **Ch2. 분산 시스템을 떠받치는 기반** — 개념 7개,
PDF pp.10–17. 트래커: [[Apache data technology map (book)]].

**[[Replication and consensus]]가 Raft를 원리로는 알지만 구현체 이름을 모르던 구간이다.**
[[Apache Map - Ch1 How to read this book]]의 5역할에서 *가로지르는 기반 계층* — *"평소에는 존재를 잊고
지내다가 문제가 생겼을 때 드러나는 부분."*

## ⭐⭐ 논지 (개념 7) — 합의는 선택이 아니라 형태만 선택이다

읽는 규칙대로 마지막 개념이 장을 닫는다.

> **"분산 시스템에서 '한 대의 진실'을 여러 대가 공유하려면, ZooKeeper 같은 외부 서비스든 Ratis 같은
> 내장 라이브러리든 **합의 계층이 필요하다.**"**

| | 형태 | 대가 |
|---|---|---|
| 🔹 **ZooKeeper** | 완성된 코디네이션 서비스 — **애플리케이션이 붙여 쓰는 외부 중재자** | 운영할 클러스터가 하나 더 |
| 🔸 **Ratis** | 제품 코드에 넣어 쓰는 **Raft 라이브러리** | 합의 장애가 제품 장애와 한 몸 |

⭐ 그리고 외울 것을 문장 하나로 준다 — *"제품 이름보다 **'이 시스템이 Raft로 상태를 맞춘다'**는 문장을
이해하는 편이 낫다."* [[Apache data technology map (book)]] §읽는 규칙 3(*문장으로 적어 고정하라*)이
여기서도 반복된다.

장의 순서 자체가 설계된 것도 밝힌다 — *"ZooKeeper → YARN/HDFS → Ozone → YuniKorn → BookKeeper →
Ratis로 내려온 이유는, **눈에 보이는 분석 도구 아래에서 움직이는 기반을 순서대로** 보여 주기 위해서."*

## 개념 7개

| # | Tier | 개념 | 요지 |
|---|---|---|---|
| 1 | 🔹 | **ZooKeeper** | 리더 선출·설정 공유·생존 확인·잠금·순서. **"데이터 자체보다 누가 무엇을 맡는지를 맞추는 계층"** → [[Apache ZooKeeper]] |
| 2 | 🔹 | **YARN** | ResourceManager·NodeManager·ApplicationMaster. **저장과 처리의 결합을 풀었다** → [[Cluster resource scheduling]] |
| 3 | 🔸 | **HDFS** | 블록 + 복제, NameNode(메타)/DataNode(데이터). **"메타는 중앙에서, 데이터는 분산해서"** → [[Apache Hadoop]] |
| 4 | 🔸 | **Ozone** | 볼륨 → 버킷 → 키. HDFS의 한계(작은 파일·네임스페이스 규모)에 대한 대응 → [[Object storage layout]] |
| 5 | 🔸 | **YuniKorn** | K8s 시대의 배치 인식 스케줄러. 큐·공정 분배·앱 단위 → [[Cluster resource scheduling]] |
| 6 | 🔸 | **BookKeeper** | 레저·북키·복제·순차 로그. **Pulsar의 저장 엔진** → [[Message broker]] |
| 7 | 🔸 | **Ratis** | Raft를 **라이브러리로**. Ozone이 이걸로 HA 메타데이터를 구성 → [[Apache ZooKeeper]] |

## ⭐⭐ 이 장의 가장 큰 수확 — YARN이 한 일

> "YARN이 생기기 전 Hadoop은 **저장(HDFS)과 처리(MapReduce)가 더 단단히 묶여 있었다.** YARN이
> 등장하면서 **'저장은 그대로 두고, 위에서 돌아가는 엔진은 다양하게'** 라는 구조가 가능해졌다."

⭐⭐ **이것은 레이크하우스가 한 일과 같은 움직임이 한 세대 먼저, 한 층 아래에서 일어난 것이다.**

| | 무엇을 떼어냈나 | 그 자리에 생긴 문제 |
|---|---|---|
| **YARN** | 저장(HDFS) ↔ **처리 엔진** | 어떤 엔진을 쓸까 + **누가 얼마나 자원을 쓸까** |
| **레이크하우스 / 테이블 포맷** | 저장(오브젝트) ↔ **쿼리 엔진** | 어떤 엔진을 쓸까 → [[SQL execution layer]] |

**"결합을 풀면 그 자리에 선택 문제가 생긴다"** 는 것까지 두 번 다 같다.
[[Analytical data storage tiers]]가 *쿼리 엔진 결합 축이 실무에서 가장 자주 놓치는 지점* 이라고 한 것의
계보가 여기까지 올라간다.

## ⭐⭐ 실제 스택에 걸리는 것 — YuniKorn

당신 스택(K8s · Airflow · MinIO · Postgres)에서 이 장의 유일한 실전 항목이다.

> **"기본 Kubernetes 스케줄러는 일반적인 서비스 Pod에는 잘 맞지만, 데이터 작업처럼 이벤트나 배치 기반
> 패턴에 쓰기에는 애매한 경우가 있다."**

가져온 개념 셋: **큐 · 공정 분배 · 애플리케이션 단위 스케줄링.** Spark on Kubernetes처럼 큰 작업이
공존하는 환경에 맞는다.

⭐⭐ 그리고 **관찰 가능한 증상**을 판단 기준으로 준다 — 이 책에서 드문 형태다.

> **"데이터 작업이 자원을 독점해 서비스 Pod가 자원을 배정받지 못하는 현상이 반복된다면, YuniKorn을
> 검토하면 된다."**

⚠️ *"모든 조직의 기본값은 아니다. 작은 규모에서는 Kubernetes 기본 스케줄러로도 충분할 수 있다."*

[[GPU resource allocation]] §이 위키에 아직 없는 것이 지목한 **gang scheduling(Kueue·Volcano)** 공백과
같은 축으로 보이는데, ⚠️ **소스가 그 용어를 쓰지 않으므로 동일하다고 단정하지 않았다** — 확인 필요로
남겼다.

## Ozone — 결론은 "우리에겐 해당 없음"

트래커 §실제 스택에 걸리는 항목이 Ozone을 올려 뒀지만, **이 장이 스스로 제외한다.**

> ⚠️ **"이미 클라우드 오브젝트 스토리지를 쓰고 있다면 굳이 중복으로 둘 이유가 적다."**
> 검토 대상은 *"Hadoop 기반 데이터 플랫폼을 오래 운영하면서 HDFS의 한계(작은 파일, 네임스페이스 규모)를
> 느끼는 조직"* 이다.

MinIO가 이미 S3 호환 오브젝트 스토리지이므로 **해당 없음**이다. 다만 남는 것 하나 —
⭐ *"저장 계층을 고를 때는 **파일 모델이 필요한지, 오브젝트 모델이 필요한지**를 먼저 따져 보면 선택이
쉬워진다."* [[Object storage layout]]의 전제(*오브젝트 스토리지엔 디렉토리가 없다*)가 **온프레미스에서는
고를 수 있는 것**이라는 점이 명시됐다.

## HDFS — "메타는 중앙에서, 데이터는 분산해서"

블록 단위로 쪼개고 여러 **DataNode**에 복제, 이름과 위치는 **NameNode**가 관리.

⭐⭐ **이 패턴이 이 위키 전체에서 반복된다.**

| | 메타 | 데이터 |
|---|---|---|
| **HDFS** | NameNode | DataNode 블록 |
| [[Table formats]] | 매니페스트·스냅샷 | Parquet 파일 |
| [[Apache Polaris]] | 카탈로그 | 오브젝트 |
| [[Spatial omics platform roadmap]] | Postgres 카탈로그 | MinIO store |

**HDFS가 그 패턴의 첫 대표다** — [[Apache Hadoop]]에 적어 두었다. 그리고 소스도 계보를 인정한다:
*"레이크하우스의 Parquet 파일도 결국 어떤 분산 저장소 위에 올라가느냐의 문제이고, HDFS는 그 문제를 푸는
초기의 대표 방식이었다."*

## BookKeeper — Kafka와 Pulsar의 구조적 차이가 여기서 설명된다

레저(순서대로 이어지는 기록의 단위) · 북키(바이트를 담는 저장 노드) · 복제 · 순차 로그.
**Pulsar가 메시지를 오래 보관할 때 쓰는 저장 엔진**이고, *"Kafka의 로그 세그먼트와 역할은 닮았지만
BookKeeper는 그 밑 단계의 공용 원장"* 이다 — *"눈에 보이는 토픽 UI 아래에서 실제로 바이트를 저장하는
계층."*

⭐ [[Message broker]] §대표 제품 표가 Kafka와 Pulsar를 나란히 두고도 **구조 차이를 말하지 않았는데**,
그 차이가 이것이다: **Kafka는 저장을 브로커가 직접 하고, Pulsar는 저장을 BookKeeper로 분리했다.**
컴퓨트/스토리지 분리라는 같은 패턴이 메시징 층에서 반복되고, 대가도 같다 — **탄력성을 얻고 운영
컴포넌트를 하나 더 얻는다.**

## 👍 강점 · ⚠️ 약점

**강점**

- 출처 없는 수치 **0건** — 7장 연속.
- ⭐ **이 장은 예외적으로 "구성 요소"를 준다.** YARN 3종, HDFS 4종, BookKeeper 4종.
  6장 연속 *"내부 동작이 없다"* 고 적었는데 **Ch2는 부분적으로 다르다** — 컴포넌트 이름과 역할까지는 온다.
- ⭐ YuniKorn의 **관찰 가능한 도입 신호**는 이 책 전체에서 가장 실행 가능한 판단 기준 중 하나다.

**약점**

- ⚠️ **여전히 메커니즘은 없다.** ZooKeeper의 ZAB 프로토콜·znode·watch, Ratis의 로그 복제 상세,
  YARN 스케줄러 종류(Capacity vs Fair), HDFS의 NameNode HA·EC(erasure coding)가 전부 없다.
  [[Replication and consensus]] §이 위키에 아직 없는 것의 **"Raft의 로그 복제 상세"** 는 그대로 남는다.
- ⚠️ **ZooKeeper의 운영 난점이 없다** — 앙상블 홀수 대수, GC/디스크 지연이 세션 타임아웃을 유발하는
  문제, watch의 one-shot 성질. *"눈에 잘 띄지 않는다"* 고만 말하고 왜 그게 장애 때 문제가 되는지는
  말하지 않는다.
- ⚠️ **비교 절이 없다** — Ch6~Ch10에는 매 장 비교 절이 있었는데 Ch2에는 없다. ZooKeeper vs etcd,
  YARN vs K8s scheduler vs YuniKorn, HDFS vs S3가 모두 비교표가 될 수 있었는데 서술로만 흩어져 있다.
  (개념 4와 7이 부분적으로 대비표를 갖지만 독립 절은 아니다.)

## 위키에 들어온 것

| | 페이지 |
|---|---|
| 새 개념 | **[[Cluster resource scheduling]]** — YARN 3종 + 결합 해제의 계보 + YuniKorn 도입 신호 |
| 새 엔티티 | **[[Apache ZooKeeper]]**(Ratis 흡수 — 같은 축의 두 형태) |
| 갱신 | [[Replication and consensus]] — **합의 계층을 어디에 두나: 외부 서비스 vs 내장 라이브러리** |
| | [[Apache Hadoop]] — HDFS 구성 4종 + *메타는 중앙, 데이터는 분산* + YARN 절 |
| | [[Object storage layout]] — **파일 모델 vs 오브젝트 모델**(Ozone) |
| | [[Message broker]] — BookKeeper 절 + **Kafka/Pulsar 구조 차이** + 별칭(Pulsar·BookKeeper·RocketMQ·ActiveMQ) |
| | [[Apache Kafka]] — KRaft 전환 = **축의 이동** |
| | [[GPU resource allocation]] — gang scheduling 공백에 YuniKorn을 인접 항목으로 |

**승격 판단**: **ZooKeeper** ✅(Tier 1 · Kafka·HBase·Hadoop·Replication이 이미 이름으로 가리킴 ·
**Ratis는 별칭으로 흡수** — 둘이 한 축의 두 형태라 떼면 대비가 부서진다) ·
YARN·YuniKorn ⏸(**지식의 단위가 "누가 얼마나 쓸지"라는 축** → [[Cluster resource scheduling]]) ·
HDFS·Ozone ⏸([[Apache Hadoop]]·[[Object storage layout]]이 집) ·
BookKeeper ⏸([[Message broker]]에 흡수).

## 다음

- **Ch11**(특화 분석·공통 라이브러리) — 남은 최대 공백 7/9. **Sedona**(대용량 지리공간)만 이 위키에
  직접 걸리고 나머지(Mahout·MADlib·SINGA·OpenNLP·DataSketches·Commons Math)는 주변부다.
- **Ch3·Ch4·Ch5** — 공백 0~2개. [[Apache Kafka]]·[[Apache Spark]]·[[Apache Flink]]·
  [[Columnar and in-memory data formats]]가 이미 덮고 있어 **보정·확인 목적**의 인제스트가 된다.
  Ch5의 Arrow Flight SQL·CarbonData, Ch4의 Beam·StreamPark가 실제 신규 항목이다.

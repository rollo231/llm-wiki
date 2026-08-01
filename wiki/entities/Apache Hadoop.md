---
type: entity
title: Apache Hadoop
area: [data-engineering]
aliases: [하둡, Hadoop, HDFS, MapReduce, GFS, Google File System, YARN]
tags: [data-engineering, hadoop, hdfs, mapreduce, distributed-systems, big-data]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch1 Distributed processing basics]]", "[[AI DE Course - Ch2-1,2,3 Storage evolution]]"]
---

# Apache Hadoop

**구글의 GFS·MapReduce 논문을 더그 커팅(Doug Cutting)이 자바로 구현한 오픈소스 프로젝트 (2006).**
분산 처리의 상용화 출발점이자, 이후 거의 모든 데이터 인프라가 참조하는 계보의 뿌리.

## 계보 — 구글의 세 논문에서

| 연도 | 논문 | 내용 | Hadoop 구현 |
|---|---|---|---|
| **2003** | **GFS** (Google File System) | 큰 파일을 **64MB 청크**로 쪼개 수천 대의 저가형 서버에 분산 저장. 각 청크를 **3군데 이상 복제** | **HDFS** |
| **2004** | **MapReduce** | Map(로컬 계산) → Shuffle(정렬·병합) → Reduce(통합) | **Hadoop MapReduce** |
| **2006** | **BigTable** | 대규모 분산 데이터베이스 | (HBase가 대응) |

### GFS의 설계 철학

> ⭐ **"하드웨어는 언제든 고장 날 수 있다는 전제하에 소프트웨어로 신뢰성을 보장한다."**

**이 전제가 [[Distributed processing]] 전체의 출발점이다.** 비싼 하드웨어로 고장을 막는 대신,
싼 하드웨어가 고장 나는 것을 전제하고 소프트웨어로 복구한다.

**아키텍처:** GFS master(파일 네임스페이스, 청크 위치)와 chunkserver를 분리하고,
**control message와 data message 경로를 나눈다** — 마스터는 메타데이터만 다루고 실제 데이터는
클라이언트가 chunkserver에서 직접 읽는다.

### MapReduce의 전략

> ⭐ **"데이터를 계산기로 가져오지 말고, 계산기를 데이터가 있는 곳으로 보내자."**

| 단계 | 동작 |
|---|---|
| **Map** | 각 서버가 가진 데이터를 **로컬에서** 먼저 계산 (예: 각 서버 문서에서 '사과' 개수 세기) |
| **Shuffle** | 중간 결과를 **네트워크를 통해** 정렬하고 병합 |
| **Reduce** | 최종 통합 (예: 모든 서버의 '사과' 개수 합산) |

> **의의: "복잡한 병렬 프로그래밍을 몰라도 개발자가 함수 두 개(Map, Reduce)를 통해 수천 대의
> 컴퓨터를 동시에 돌릴 수 있게 만들었다."**

**Shuffle이 병목이라는 사실은 20년째 유효하다** — [[NVIDIA RAPIDS]]의 GPU shuffle 최적화가
같은 문제를 다시 푼다.

## 구성 요소

| 컴포넌트 | 역할 |
|---|---|
| **HDFS** | 분산 파일 시스템. NameNode(마스터, 메타데이터) + DataNode(슬레이브, 블록 저장) |
| **MapReduce** | 분산 계산 프레임워크 |
| **YARN** | 클러스터 자원 관리. ResourceManager(마스터) + NodeManager(슬레이브) |

**에코시스템:** ZooKeeper · Storm · Solr/Lucene · Mahout · **Hive** · **Pig** · **HBase** ·
Cassandra · **Spark**(YARN 위에서도 실행) · Kafka · Sqoop.

## ⭐ 한계 — 왜 Spark가 나왔나

> **"하둡의 MapReduce는 단계마다 결과를 디스크(HDD/SSD)에 썼다가 다시 읽어야 하는 문제.
> 작업이 수십 단계면 수십 번의 디스크 I/O가 발생한다."**

이 한계가 [[Apache Spark]]의 In-Memory 처리와 DAG 실행을 낳았다.

**두 번째 한계는 지연이다.** [[Lambda and Kappa architecture]]가 지적하듯, 2010년대 초반의
하둡은 **"계산은 정확하지만 결과가 나오기까지 몇 시간, 며칠"** 이었다. 이것이 람다 아키텍처의
배치 레이어가 존재한 이유이고, **동시에 람다가 무거웠던 이유**다.

## 지금 어떤 위치인가

**직접 운영하는 하둡 클러스터는 크게 줄었지만, 그 개념은 곳곳에 남아 있다:**

| 하둡의 것 | 현재의 형태 |
|---|---|
| HDFS 블록 분산 저장 | 객체 스토리지(S3) + [[Table formats]] |
| MapReduce의 shuffle | [[Apache Spark]]의 shuffle, [[NVIDIA RAPIDS]]의 GPU shuffle |
| "계산을 데이터로" | 데이터 로컬리티, [[GPU resource allocation]]의 locality 논의 |
| 3중 복제 | 클라우드 스토리지의 내구성 보장, [[Replication and consensus]] |
| YARN | Kubernetes |

> **[[Distributed processing]]의 "최근의 변화는 분산이 사라진 것이 아니라, 분산 복잡성을 사용자가
> 직접 떠안지 않아도 되는 방향으로 진화 중"이라는 문장이 하둡의 현재 위치를 요약한다.**

**[[Analytical data storage tiers]](Part 1)의 "Data Lake" 절이 이 이야기의 저장소 관점 버전이다** —
하둡이 데이터 레이크의 첫 구현이었고, 거버넌스 부재로 "늪"이 되면서 레이크하우스가 나왔다.

## ⚠️ 이 위키에 아직 없는 것

- **HDFS의 NameNode SPOF와 HA 구성** — 강의가 다루지 않는다
- **Hive vs Presto/Trino** — 에코시스템 그림에 로고로만 등장
- **YARN vs Kubernetes** — 자원 관리 계층의 세대 교체가 언급되지 않는다

## 관련 페이지

- [[Distributed processing]] — GFS 철학과 분산의 대상
- [[Apache Spark]] — 하둡의 디스크 I/O 한계를 푼 후계
- [[Lambda and Kappa architecture]] — 하둡의 지연이 만든 아키텍처
- [[Analytical data storage tiers]] — Data Lake 관점
- [[Replication and consensus]] — 3중 복제
- [[Apache Kafka]] · [[Apache Flink]] · [[NVIDIA RAPIDS]]

## 출처

- [[AI DE Course - Part4 Ch1 Distributed processing basics]]
- [[AI DE Course - Ch2-1,2,3 Storage evolution]] (Part 1, 저장소 관점)

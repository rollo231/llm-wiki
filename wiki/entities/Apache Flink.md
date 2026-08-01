---
type: entity
title: Apache Flink
area: [data-engineering]
aliases: [플링크, Flink, Kafka Streams, RocksDB state backend, CEP]
tags: [data-engineering, flink, streaming, stateful, checkpoint, event-time, watermark, rocksdb]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]]", "[[AI DE Course - Part4 Ch3 Event time watermarks and windows]]", "[[AI DE Course - Ch4-5,6 Stream processing engines]]"]
---

# Apache Flink

**상태(State)와 시간(Time) 제어를 엔진의 중심 개념으로 삼은 분산 스트림 처리 엔진.**

> **"상태를 크게 들고, 시간 기준까지 정교하게 다루는 분산 스트림 처리 엔진."**

## 특징

| |
|---|
| **끝이 없는 데이터와 끝이 있는 데이터 모두 처리** (bounded / unbounded) |
| ⭐ **상태 기반 계산을 엔진의 중심 개념으로 취급** |
| **이벤트 발생 시각 기준 처리** 지원 |
| **늦게 도착한 데이터 처리** 기능 강조 |
| **체크포인트를 통해 장애 후 일관된 복구** 지원 |

**잘 맞는 문제:** 사용자별 상태 유지 · 긴 시간 구간 집계 · **늦게 도착한 데이터가 많은 환경** ·
**상태 크기가 큰 실시간 계산** · 정교한 시간 기준이 중요한 분석과 탐지.

> **"세밀한 상태 관리와 시간 제어 능력이 압도적. 대규모 실시간 이상 탐지, 복잡한 이벤트
> 처리(CEP)의 표준."**

## ⭐ 상태 관리 — 왜 로컬 저장소인가

> **"매 레코드 처리 시마다 외부 DB([[Redis]], MySQL)에 접근하면 네트워크 지연으로 실시간성 확보가
> 불가능하다. 스트림 엔진은 상태를 계산 노드 내부 디스크/메모리에 직접 저장하는 '로컬 저장소'
> 방식을 채택한다."**

| State Backend | 특징 |
|---|---|
| **HashMap 기반 (Memory)** | 자바 객체로 메모리에 저장. 속도가 극도로 빠르나 **상태 크기가 메모리 용량으로 제한** |
| **RocksDB 기반 (Embedded DB)** | 로컬 디스크(SSD)에 **LSM-Tree** 구조로 저장. **메모리보다 큰 상태(수 TB)** 를 다룰 때 유리, 효율적 직렬화 |

> **이것이 [[Caching strategies]]와 헷갈리기 쉬운 지점이다 — 접근 빈도의 차이다.**
> 서빙 경로(요청당 수 회)는 Redis, 스트림 연산(레코드당 매번)은 로컬 embedded store.

## 시간과 워터마크

Flink는 **이벤트 시각 기반 처리**를 위해 각 데이터에 시각 정보를 요구하고,
**워터마크를 통해 시간 진행 정도를 엔진에 알린다.**

- 워터마크 = **시간 진행의 신호**
- 시간 구간을 언제 닫을지, 얼마나 늦은 데이터까지 반영할지, 오래된 중간 상태를 언제 지울지 결정

상세는 [[Stream processing semantics]] 참조.

## 체크포인트 — 상태 + 입력 위치

> ⭐ **"Flink는 체크포인트를 통해 각 연산자의 상태와 입력 위치를 함께 저장한다. 실패 시 이 지점부터
> 일관되게 다시 시작할 수 있다."**
>
> **"제대로 보장하기 위해 다시 읽을 수 있는 입력 계층과 상태 저장 공간이 필요하다."**

**이 한 줄이 "엔진만 있으면 브로커는 불필요"라는 오해의 답이다.** 복구 시 저장된 입력 위치부터
다시 읽어야 하므로 **재읽기 가능한 브로커([[Apache Kafka]])가 없으면 exactly-once가 성립하지
않는다.** → [[Message broker]]

## 세 엔진 비교

| | **Flink** | **[[Apache Spark]] Structured Streaming** | **Kafka Streams** |
|---|---|---|---|
| **한 줄** | **상태와 시간 제어를 전면에 둔 엔진** | **Micro-batch.** 배치 에코시스템과의 통합이 강점 | **애플리케이션 내부에서 동작하는 처리 라이브러리** |
| **배포 형태** | 별도 클러스터 | 별도 클러스터 | ⭐ **별도 클러스터 불필요** |
| **잘 맞는 곳** | 대규모 실시간 이상 탐지, CEP, 늦은 데이터 많은 환경, 큰 상태 | SQL/DataFrame 중심 조직, 기존 Spark 배치와 통합 | Kafka가 이미 핵심 입력 계층, 마이크로서비스 내부 실시간 로직 |
| **상태 복구** | 체크포인트(상태 + 입력 위치) | 체크포인트 + WAL + 재처리 가능 입력 + 중복 안전 sink | **changelog topic**에서 state store 복원 |

> ⭐ **Kafka Streams가 축을 하나 더 만든다 — "클러스터를 세우지 않는 선택지".**
> Java/Scala 애플리케이션 안에서 동작하며, 계산 흐름을 **프로세서 토폴로지**로 정의하고
> **state store**를 사용한다. Kafka to Kafka 파이프라인과 서비스 내부 실시간 로직에 유리하다.
>
> **Part 1([[AI DE Course - Ch4-5,6 Stream processing engines]])이 "Flink vs Spark = 지연 vs
> 통합성" 2축이었다면, Part 4는 "상태 관리 능력 vs 에코시스템 vs 배포 형태" 3축으로 늘렸다.**

## ⚠️ 이 위키에 아직 없는 것

- **Flink의 지연 수치** — "Spark보다 낮다"는 정성적 서술뿐. Spark의 기본 트리거 간격이나 Flink의
  실제 p99가 없다
- **워터마크 생성 방식** — bounded-out-of-orderness, periodic vs punctuated,
  ⭐ **여러 파티션의 워터마크를 어떻게 합치는가(min 취하기)**, **idle partition 문제**
  (한 파티션이 조용하면 워터마크가 안 올라감 — 실무 최대 함정)
- **Flink SQL / Table API** — 언급되지 않는다
- **savepoint vs checkpoint** — 버전 업그레이드 시 핵심인데 없다
- **exactly-once sink 구현** (two-phase commit sink)
- **Flink의 배치 모드** — bounded stream 처리를 언급만 하고 [[Lambda and Kappa architecture]]의
  **Unified Path**와 잇지 않는다

## 관련 페이지

- [[Stream processing semantics]] — 상태·시간·윈도우·워터마크
- [[Message broker]] — 운반 계층과의 경계
- [[Apache Spark]] · [[Apache Kafka]]
- [[Lambda and Kappa architecture]] — 카파의 계산 엔진
- [[Batch and stream processing]] · [[Distributed processing]] (상태 분산)
- [[Redis]] — 상태 저장소로 쓰지 않는 이유

## 출처

- [[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]]
- [[AI DE Course - Part4 Ch3 Event time watermarks and windows]]
- [[AI DE Course - Ch4-5,6 Stream processing engines]] (Part 1)

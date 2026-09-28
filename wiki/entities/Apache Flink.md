---
type: entity
title: Apache Flink
aliases: [Flink, 플링크, FlinkCEP, ForSt]
tags: [도구, 처리, 스트리밍]
created: 2026-09-14
updated: 2026-09-28
sources:
  - "[[AI DE 강의 1-03 기술 스택과 툴 생태계]]"
  - "[[AI DE 강의 1-10 배치 vs 스트리밍]]"
  - "[[AI DE 강의 1-12 실시간 처리 엔진]]"
  - "[[AI DE 강의 1-16 AI 파이프라인 구축 사례]]"
  - "[[AI DE 강의 4-07 메시지 브로커와 스트림 처리 엔진]]"
  - "[[AI DE 강의 4-10 람다·카파와 현대 아키텍처]]"
---

# Apache Flink

네이티브 스트리밍 처리 엔진이다. 데이터를 모으지 않고 들어오는 대로 레코드 단위로 처리하며, 상태(state)와 이벤트 시간을 일급으로 다룬다. Part 1에서 [[스트림 처리]]의 대표 엔진으로 나온다.

## 특징 (강의 기준)

[[AI DE 강의 1-12 실시간 처리 엔진]]:

| 특징 | 내용 |
|---|---|
| 네이티브 스트리밍 | 레코드 단위 처리, 밀리초 단위 지연 |
| 이벤트 시간과 워터마크 | 데이터 생성 시각 기준으로 처리하고, 워터마크로 늦게 온 데이터를 보정 |
| exactly-once 상태 | 분산 스냅샷(강의 표기: Chandy-Lamport 알고리즘)으로 장애 시에도 상태 일관성 보장 |
| 상태 종류 | Keyed State(키별, 예: 사용자별 장바구니), Operator State(연산자 인스턴스 단위, 예: Kafka 오프셋) |
| 상태 백엔드 | JVM 힙(가장 빠르지만 메모리 한계) vs 내장 RocksDB(로컬 디스크에 저장, TB급 상태) |

[[AI DE 강의 4-07 메시지 브로커와 스트림 처리 엔진]]은 Flink를 "상태와 시간 제어를 전면에 둔 엔진"으로 요약한다(p168–171). 잘 맞는 문제로 사용자별 상태 유지, 긴 시간 구간 집계, 늦게 도착한 데이터가 많은 환경, 큰 상태, 정교한 시간 기준이 필요한 분석·탐지를 든다.

[[AI DE 강의 1-03 기술 스택과 툴 생태계]]는 Java·Scala를 일급으로 지원하는 [[JVM]] 엔진이라는 점을 강조한다.

## 상태 백엔드와 Flink 2.0

| 백엔드 | 저장 위치 | 특징 |
|---|---|---|
| HashMapStateBackend | TaskManager JVM 힙 | 가장 빠르다. 상태 크기가 메모리에 묶인다 |
| EmbeddedRocksDBStateBackend | 로컬 디스크의 RocksDB(LSM-Tree) | 메모리보다 큰 TB급 상태 |
| ForSt (Flink 2.0) | 원격 저장소(disaggregated state) | 계산과 상태 저장을 분리. 문서상 아직 실험 단계 |

Flink 2.0은 2025-03-24에 나왔다. ForSt 기반 disaggregated state를 도입하고 옛 `FsStateBackend`·`MemoryStateBackend`를 없앴다. [https://flink.apache.org/2025/03/24/apache-flink-2.0.0-a-new-era-of-real-time-data-processing/ , 2026-09-28 확인] 현재 문서는 ForSt를 "still in the experimental stage and is not fully available for production"이라고 적는다(https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/state_backends/ , 2026-09-28 확인). Part 4(2026-05 작성)는 앞의 두 백엔드만 다룬다.

## Spark Streaming과의 비교

| | Flink | [[Apache Spark]] (Streaming) |
|---|---|---|
| 처리 모델 | 네이티브 스트리밍(레코드) | 마이크로 배치 |
| 지연 | 낮음(밀리초) | 높음(초) |
| 상태 관리 | 세밀한 제어 | RDD·SQL 기반 |
| 운영 복잡도 | 높음(세밀한 설정 필요) | 중간(접근성 높음) |
| 고를 때 | 1초 미만 초저지연이 필수일 때 | 대용량 처리와 배치 코드 재사용이 중요할 때 |

## 등장하는 사례

- 스트리밍 아키텍처의 엔진 칸: 브로커(Kafka) → Flink → 실시간 싱크(Redis·알림)([[AI DE 강의 1-10 배치 vs 스트리밍]]).
- 실시간 추천: 클릭 로그 → Kafka → Flink(실시간 피처 추출·추론) → Redis.
- Netflix Keystone: 메시지 버스 Kafka + 스트림 처리 엔진 Flink([[AI DE 강의 1-16 AI 파이프라인 구축 사례]]).

## 주의

- ⚠️ [[AI DE 강의 4-07 메시지 브로커와 스트림 처리 엔진]]은 Flink를 "복잡한 이벤트 처리(CEP)의 표준"이라고 쓴다(p168). CEP 라이브러리는 있지만("FlinkCEP is the Complex Event Processing (CEP) library implemented on top of Flink", https://nightlies.apache.org/flink/flink-docs-stable/docs/libs/cep/ , 2026-09-28 확인) "표준"이라는 근거는 없다. 주관적 과장이다.
- 위 비교표의 "Spark = 마이크로 배치, 초 단위"는 Spark 4.1의 Real-Time Mode 이전의 기본 설정 기준이다([[Apache Spark]]).

- ⚠️ [[AI DE 강의 1-10 배치 vs 스트리밍]]의 자율주행 슬라이드는 차량 내 엣지 추론 칸에 Flink를 넣는다. 차량 제동 제어 루프는 Flink를 둘 자리가 아니라는 것이 위키의 판단이다.

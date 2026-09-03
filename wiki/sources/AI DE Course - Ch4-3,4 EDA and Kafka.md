---
type: source
title: AI DE Course - Ch4-3,4 EDA and Kafka
area: [data-engineering]
aliases: [CH04-3 4 EDA와 Kafka, 이벤트 기반 아키텍처와 카프카 핵심 개념]
tags: [data-engineering, course, fast-campus, kafka, eda, event-driven, topic, partition, offset]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part1/14. CH04-3, 4. 이벤트 기반 아키텍처(EDA)와 Kafka의 핵심 개념 (Topic, Partition, Offset) 1, 2.pdf"]
---

# AI DE Course - Ch4-3,4 EDA and Kafka

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 CH04-3,4**
"이벤트 기반 아키텍처(EDA)와 Kafka의 핵심 개념 (Topic, Partition, Offset) (1)(2)". 원본(로컬):
`raw/data-engineering/ai-de-course/part1/14. CH04-3, 4. 이벤트 기반 아키텍처(EDA)와 Kafka의 핵심 개념 (Topic, Partition, Offset) 1, 2.pdf`
(24p). 강의 홈: [[AI Data Engineering (Fast Campus course)]].

**Kafka 내부 정리는 [[Apache Kafka]] 엔티티 페이지로 옮겼다.** 여기는 이 덱의 논지와 EDA 부분을 남긴다.

## 논지 — Data at Rest → Data in Motion

강의가 세우는 4단 서사:

1. **과거: Request-Response (동기)** — 클라이언트 요청 시에만 DB 조회. 단순하지만 대기 시간 발생.
2. **현재: 데이터 폭증과 병목** — 모바일·IoT로 데이터 쓰나미. **동기식 처리가 시스템 과부하의 주범.**
3. **전환: Data at Rest → Data in Motion** — 고여있는 데이터에서 끊임없이 흐르는 데이터로 관점 이동.
4. **해법: Event-Driven Architecture** — 이벤트 발생 즉시 반응·전파하는 비동기 구조.

## Kafka 탄생 배경 — 기능을 뺀 것이 설계다

이 덱에서 가장 유용한 서술.

- 2010년경 LinkedIn 내부 프로젝트. 하루 수십억 건의 활동 추적 이벤트를 감당할 파이프라인이 필요.
- **기존 MQ(ActiveMQ·RabbitMQ)의 한계** — 메시지의 '전달 보장'과 '복잡한 기능'에 집중하느라
  **처리 속도(throughput)가 느려** 폭증하는 실시간 트래픽을 감당할 수 없었다.
- **Kafka의 과감한 선택** — **"무거운 기능은 다 빼버리자."** 오직 압도적 throughput과 수평 확장성에만
  집중한 로그 기반의 단순한 아키텍처.
- 2011년 오픈소스 → 사실상의 표준 (강의: Fortune 500의 80% 이상 사용).

> **"기능을 더해서가 아니라 빼서 이겼다"** 는 것이 Kafka를 이해하는 열쇠다. 그래서 Kafka는
> 처리를 하지 않고, 그래서 스트림 프로세서가 따로 필요하다 → [[Stream processing semantics]]

## EDA 심화 — 직접 호출 vs 이벤트

| Direct Communication (강결합) | | Event-Driven (느슨한 결합) |
|---|---|---|
| 주문 서비스가 배송 API를 직접 호출. 배송의 IP·API 스펙이 바뀌면 주문도 수정 | 결합도 | "주문 발생" 이벤트만 던질 뿐 누가 받는지 모름. **독립적 배포 가능** |
| 배송 서비스가 다운되면 주문도 타임아웃. **하나의 장애가 전체 마비** | 장애 | 배송이 죽어도 이벤트는 Kafka에 안전히 저장. 복구 후 이어서 처리, **유실 없음** |
| 요청 완료까지 클라이언트 대기. 트래픽 폭주 시 병목 | 확장 | 컨슈머 서버만 늘리면 됨(scale-out) |

> **Architect's Note: MSA의 복잡성을 해결하는 핵심 열쇠는 서로의 존재를 모르게 하는 비동기 이벤트
> 통신이다.**

## Hub & Spoke — N×M을 1:N으로

Kafka를 중앙 허브로 두면 소스와 타겟이 직접 연결된 **N×M 구조**를 **1:N 구조**로 바꿔
**spaghetti code를 방지**한다.

```
INPUT                          CENTRAL HUB              TARGET
Web Access Logs (Beats)   ┐                    ┌→ Real-time Dashboard (ES·Kibana)
Database CDC (Debezium)   ├→   Apache Kafka   ─┼→ Data Lake / DW (S3·Hadoop·Snowflake)
IoT Sensors (MQTT)        ┘   Decoupling       └→ AI Model & Alert (Anomaly Detection)
                              Buffering
                              Replayability
```

**Database CDC(Debezium)가 input source 중 하나로 명시된다** — [[Change data capture]]의 Transport
층이 여기다.

## 메시지 브로커 vs 이벤트 스트리밍

기존 페이지와 **정확히 일치하는** 지점이고 Kafka 이해의 핵심이다.

| 전통 브로커 (RabbitMQ·ActiveMQ) | | Kafka |
|---|---|---|
| 전달되면 큐에서 **즉시 삭제** (휘발성) | 보존 | 컨슈머가 읽어가도 디스크에 **보관** (retention). CCTV 녹화 영상처럼 |
| **스마트 브로커** — 브로커가 누구에게 줄지 결정하고 push | 모델 | **스마트 컨슈머** — 컨슈머가 자기 속도로 pull, 오프셋을 직접 관리 |
| 처리된 메시지는 사라져 **재처리·과거 분석 불가** | 재생 | **Replayability** — 오프셋을 되감아 처음부터 다시. 버그 수정 후 재처리에 강력 |

> **Key Takeaway: replayability는 단순 메시징을 넘어 데이터 파이프라인의 복원력과 유연성을 보장하는
> 핵심 기능이다.**

## 강의가 명시하는 Kafka의 한계 3종

나열형 덱에서 드물게 **한계를 짚는다.**

- **운영 복잡도** — 브로커·주키퍼(또는 KRaft)·스키마 레지스트리 등 관리 요소가 많다. Kafka 내부
  동작을 이해하는 전문 엔지니어링 리소스 확보가 필수.
- **실시간성 한계** — Kafka는 **'Near Real-time'** 에 최적화되어 있다. 마이크로초 단위 초저지연이
  요구되는 미사일 요격이나 **초단타 매매(HFT)** 같은 시스템에는 적합하지 않을 수 있다.
- **순서 보장 이슈** — 전체 데이터가 아니라 파티션 내부에서만 순서를 보장한다. 정교한 키 설계와
  파티셔닝 전략이 선행되어야 한다.

## 기존 페이지와의 대조

- **일치(중요)** — [[Batch and stream processing]]이 랜드스케이프 가이드에서 얻은 두 경고가 그대로
  확인된다: **① 컨슈머가 ack해도 이벤트가 폐기되지 않는다(retention·replay)**,
  **② Kafka 자체는 아무 처리도 하지 않는다.** Kafka Connect / Kafka Streams 구분도 동일.
- **보강(큼)** — 탄생 배경(왜 기능을 뺐나), 토픽·파티션·오프셋의 정확한 의미와 제약
  (**파티션은 줄일 수 없다**, 오프셋은 파티션 내부에서만 유일), **순서 보장 범위와 키 해법**,
  레플리케이션(리더에서만 읽기/쓰기), **로그 컴팩션**, **Zero-Copy**, KRaft 전환, 컨슈머 그룹 리밸런싱.
  → [[Apache Kafka]] 엔티티 페이지로 분리.
- **연결** — 로그 컴팩션된 토픽이 사실상 key-value store라서 **CDC로 DB 현재 스냅샷을 구성할 때
  필수적**이라는 서술이 CH03-3,4와 이 덱을 잇는다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념·엔티티: [[Apache Kafka]] (상세), [[Batch and stream processing]],
  [[Change data capture]], [[Latency and throughput]], [[Stream processing semantics]]
- 앞 챕터: [[AI DE Course - Ch4-1,2 Batch vs Streaming]] — 이 덱의 순차 쓰기 서술이 앞 덱의
  "스트리밍 = 랜덤 I/O" 일반화와 충돌한다
- 이어지는 챕터: [[AI DE Course - Ch4-5,6 Stream processing engines]]

---
type: entity
title: Apache Kafka
aliases: [Kafka, 카프카, 로그 컴팩션, Log Compaction, KRaft, 컨슈머 그룹, Kafka Streams, min.insync.replicas]
tags: [도구, 처리, 메시징, 스트리밍]
created: 2026-09-14
updated: 2026-09-28
sources:
  - "[[AI DE 강의 1-03 기술 스택과 툴 생태계]]"
  - "[[AI DE 강의 1-08 CDC]]"
  - "[[AI DE 강의 1-10 배치 vs 스트리밍]]"
  - "[[AI DE 강의 1-11 EDA와 Kafka]]"
  - "[[AI DE 강의 1-16 AI 파이프라인 구축 사례]]"
  - "[[AI DE 강의 4-03 고가용성·복제·합의]]"
  - "[[AI DE 강의 4-06 메시지 브로커의 종류와 전달 보장]]"
  - "[[AI DE 강의 4-07 메시지 브로커와 스트림 처리 엔진]]"
---

# Apache Kafka

분산 이벤트 스트리밍 플랫폼이다. 메시지를 디스크의 로그에 순서대로 추가하고 보존하며, 컨슈머가 자기 속도로 가져간다. Part 1에서 가장 자주 등장하는 도구로, CDC의 운반층, 스트리밍 아키텍처의 브로커, 이벤트 기반 아키텍처의 허브로 나온다. 브로커는 Scala·Java로 쓰여 [[JVM]] 위에서 돈다(이 연결은 위키가 붙였다).

## 탄생

2010년경 LinkedIn이 하루 수십억 건의 사용자 활동·지표를 처리하려 했는데, 기존 메시지 큐(ActiveMQ·RabbitMQ)는 전달 보장과 복잡한 기능 때문에 처리량이 부족했다. 그래서 "무거운 기능은 다 빼자"는 방향으로, 처리량과 수평 확장에 집중한 로그 기반 설계를 했다. 2011년 오픈소스로 공개됐다([[AI DE 강의 1-11 EDA와 Kafka]]).

## 구성과 데이터 모델

| 개념 | 정의 |
|---|---|
| 프로듀서 | 토픽·파티션을 정해 보낸다. 직렬화하고, 일정량을 모아 배치 전송하고, 키로 파티션을 고정한다 |
| 브로커 | 받은 메시지를 디스크에 순차 쓰기로 저장·보존. 3대 이상 클러스터, 복제 |
| 컨슈머 | Pull 방식으로 자기 처리 능력만큼 가져간다(배압). 여러 시스템이 같은 데이터를 동시에 소비 |
| 토픽 | 논리적 채널(폴더·테이블과 유사) |
| 파티션 | 토픽의 물리적 분할. 병렬 처리의 단위이자 순서 보장의 단위. 늘릴 수는 있어도 줄일 수 없다 |
| 오프셋 | 파티션 안 메시지의 순차 번호. 컨슈머가 커밋한 위치부터 재시작 |
| 컨슈머 그룹 | 파티션을 나눠 맡는다. 한 컨슈머가 죽으면 리밸런싱으로 재분배 |
| 복제 | 읽기·쓰기는 리더 파티션만, 팔로워는 복제. 리더 장애 시 팔로워 승격 |

## 설계의 요점

브로커는 단순하게 두고 판단은 컨슈머에게 맡긴다. 이 요약은 위키가 정리한 것이다.

- 브로커가 로그에 추가하고 보관만 하니 순차 I/O와 zero-copy(sendfile: 커널 페이지 캐시에서 소켓으로 직접 전송)로 빠르다. 단 TLS를 켜면 암호화가 사용자 공간에서 일어나 sendfile을 쓰지 않는다. [Kafka 문서 "Design": "TLS/SSL libraries operate at the user space (in-kernel `SSL_sendfile` is currently not supported by Kafka). Due to this restriction, `sendfile` is not used when SSL is enabled." https://kafka.apache.org/documentation/#design , 2026-09-14 확인]
- 읽은 위치를 컨슈머가 오프셋으로 관리하니, 오프셋을 되감아 재처리(replay)할 수 있다. 전달하면 삭제하는 전통 브로커와 가장 크게 다른 점이다([[이벤트 기반 아키텍처]]).
- 파티션 단위로 컨슈머를 붙여 수평 확장한다. 다만 한 컨슈머 그룹 안의 병렬도는 파티션 수를 넘지 못한다.

## 큐가 아니라 보관되는 로그

[[AI DE 강의 4-06 메시지 브로커의 종류와 전달 보장]]은 Kafka를 retained log 중심 브로커로 분류한다(p145). 전통 큐가 "이 작업을 어떤 worker가 처리할 것인가"를 묻는다면 Kafka는 "이 이벤트를 얼마나 오래 보관하고, 어떤 consumer group이 어느 offset부터 읽을 것인가"를 묻는다(p146). 메시지는 소비 후에도 보관 기간 동안 남고, consumer group마다 offset을 따로 관리하므로 여러 downstream이 같은 스트림을 독립적으로 읽고, 새 consumer를 붙여 과거부터 backfill할 수 있다(p147). 분류 축 전체는 [[메시지 브로커]]에 있다.

## 내구성 설정

[[AI DE 강의 4-03 고가용성·복제·합의]]는 분산 로그의 HA 패턴으로 브로커 여러 대 + replication factor 3 + `min.insync.replicas=2` + `acks=all`을 든다(p66). 내구성 조건을 높일수록 저장 비용이 늘고, 조건을 못 채우면 쓰기가 실패한다(p65).

- `acks=all`인 쓰기는 ISR(동기화된 복제본)이 `min.insync.replicas`보다 적으면 NotEnoughReplicas 오류로 거부된다. Kafka 소스의 설정 설명이 "A typical scenario would be to create a topic with a replication factor of 3, set min.insync.replicas to 2, and produce with acks of "all""라고 적는다. [apache/kafka `TopicConfig.java`, 2026-09-28 확인] 복제본 셋 가운데 하나가 죽어도 쓰기를 계속 받고, 둘이 죽으면 가용성 대신 내구성을 택한다([[복제]]).
- 프로듀서 기본값은 Kafka 3.0.0에서 `acks=1`에서 `acks=all`과 idempotence 활성화로 바뀌었다("idempotence is enabled and acks is set to all instead of 1", https://kafka.apache.org/30/documentation.html#upgrade_300_notable , 2026-09-28 확인). 다만 설정을 명시하지 않으면 idempotence가 켜지지 않는 버그(KAFKA-13598, 영향 버전 3.0.0·3.1.0)가 있어, 실제로 적용된 것은 3.0.1·3.1.1·3.2.0부터다(https://issues.apache.org/jira/browse/KAFKA-13598 , 2026-09-28 확인).

## Kafka Streams

Kafka 토픽을 읽고 처리해 다시 Kafka로 쓰는 처리 라이브러리다. 별도 클러스터 없이 Java·Scala 애플리케이션 안에서 돈다([[AI DE 강의 4-07 메시지 브로커와 스트림 처리 엔진]] p174). 처리 흐름을 처리 단계 그래프(processor topology)로 정의하고, 집계·조인·시간 구간 계산을 상태 저장소로 한다. 상태 저장소의 변경 이력을 별도 Kafka 토픽(changelog)에 남겨, 장애 뒤에는 그 토픽을 다시 읽어 상태를 복원한다(p167). 브로커가 처리 엔진의 복구 수단까지 겸하는 셈이다. Kafka가 핵심 입력인 환경, Kafka to Kafka 파이프라인, 마이크로서비스 내부의 실시간 로직에 맞는다고 강의는 정리한다(p175). Flink·Spark와의 비교는 [[스트림 처리]]에 있다.

## 순서와 키

⚠️ **토픽 전체의 순서는 보장되지 않는다. 파티션 안에서만 보장된다.** 순서가 중요한 엔티티(사용자·주문·Row ID)는 키를 지정해 같은 파티션으로 보내야 한다. 입금·출금 순서가 뒤바뀌는 문제([[AI DE 강의 1-08 CDC]])의 해법이다.

## 로그 컴팩션

기간 기반 보존(예: 7일 뒤 삭제) 대신 키별 최신 값만 남긴다. 컴팩션된 토픽은 사실상 키-값 저장소이고, CDC로 DB의 현재 스냅샷을 구성할 때 필수다([[변경 데이터 캡처]]).

## ZooKeeper와 KRaft

과거에는 메타데이터 관리를 위해 별도 ZooKeeper 앙상블이 필요했다(외부 의존, 이중 관리, 파티션이 매우 많으면 컨트롤러 병목). KRaft 모드는 브로커끼리 Raft 합의로 메타데이터를 직접 관리한다.

- KRaft는 3.3.x부터 production ready로 선언됐다(3.3.1, 2022-10-03).
- Kafka 4.0(2025-03-18)이 ZooKeeper 모드를 제거했다. 4.0부터는 KRaft만 지원한다. 2026-09-27 기준 최신 지원 릴리스는 4.3.1(2026-06-25)이고, ZooKeeper 모드는 돌아오지 않았다(https://kafka.apache.org/community/downloads/). [https://kafka.apache.org/40/getting-started/upgrade/ , https://kafka.apache.org/blog/2025/03/18/apache-kafka-4.0.0-release-announcement/ , 2026-09-14 확인]
- ⚠️ [[AI DE 강의 1-11 EDA와 Kafka]](2026-02 작성)는 이를 "향후 제거 예정"으로 쓴다.

## Part 1에서의 쓰임

| 역할 | 출처 |
|---|---|
| CDC의 운반층(버퍼·금고). 없으면 타깃 장애가 CDC 전체를 멈춘다 | [[AI DE 강의 1-08 CDC]] |
| 스키마 레지스트리와 함께 Avro 바이너리 + 스키마 ID 전송 | [[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]] |
| 스트리밍 아키텍처의 브로커(Kafka → Flink → Redis) | [[AI DE 강의 1-10 배치 vs 스트리밍]] |
| 피처 스토어의 스트림 소스 | [[AI DE 강의 1-13 Skew와 Drift]] |
| 비정형 데이터의 실시간 수집 | [[AI DE 강의 1-09 비정형 데이터 수집과 전처리]] |
| Netflix Keystone의 메시지 버스 | [[AI DE 강의 1-16 AI 파이프라인 구축 사례]] |

Part 4에서는 retained log의 대표([[AI DE 강의 4-06 메시지 브로커의 종류와 전달 보장]]), 복제·내구성 패턴의 예([[AI DE 강의 4-03 고가용성·복제·합의]]), 카파 아키텍처의 재생 가능한 로그([[람다 아키텍처와 카파 아키텍처]])로 나온다.

## 도입 시 고려사항

운영 복잡도(브로커·KRaft·스키마 레지스트리, 전문 인력), 실시간성 한계(Near Real-time에 최적화되어 마이크로초 단위 초단타 매매 등에는 부적합), 순서 보장을 위한 키·파티셔닝 설계.

## 주의

- ⚠️ 강의는 "Fortune 500대 기업의 80% 이상"이라고 쓰지만, 공식 사이트는 "More than 80% of all **Fortune 100** companies"다. [https://kafka.apache.org/ , 2026-09-14 확인]
- ⚠️ 강의는 zero-copy로 "CPU 사용량 약 60% 감소"라고 쓰지만, 널리 인용되는 IBM developerWorks 글(2008)은 전송 시간 약 65% 감소를 보고한다. 자세한 내용은 [[AI DE 강의 1-11 EDA와 Kafka]]에 있다.

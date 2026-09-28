---
type: source
title: AI DE 강의 4-06 메시지 브로커의 종류와 전달 보장
aliases: [AI DE 4-06]
tags: [AI-DE-강의, 스트리밍, 메시징]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf"
---

# AI DE 강의 4-06 메시지 브로커의 종류와 전달 보장

[[AI 데이터 엔지니어링 강의]] Part 4 스트리밍 챕터(Ch3)의 첫 소단원이다. 실시간 파이프라인의 출발점을 메시지 브로커로 놓고, 브로커가 왜 필요한지, 제품명이 아니라 소비 의미론으로 어떻게 분류하는지, 전달 보장을 어떻게 설계하는지를 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch3. 스트리밍 데이터 처리: 1. 메시지 브로커의 종류와 특징 |
| 원본 파일 | `part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` p133–151 (19p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch1~4`, 챕터 `Ch3`와 소단원 번호 `1`은 표지 슬라이드 |

## 요약

### 01. 스트리밍 데이터 (p135–136)

- 실시간 파이프라인은 생산자, 브로커, 처리 엔진, 저장소, 모델 서빙이 분리된 구조로 동작하고, 브로커는 데이터가 처리되기 전에 거치는 완충 지점이자 재전달 지점이다.
- 스트리밍 데이터는 끝이 정해지지 않은 이벤트의 연속(unbounded)이다. 클릭, 결제, 센서 값, CDC 변경 이벤트, 모델 추론 로그가 예다.
- Kafka 관점에서 record는 topic에 append되는 단위이고 partition 안에서 offset으로 식별된다. Flink 관점에서 stream은 bounded 또는 unbounded다.

### 02. 메시지 브로커 (p137–141)

- 생산자와 소비자를 직접 연결하면 규모가 커질수록 네 문제가 생긴다(p137–138). 속도 불일치(초당 수만 건 vs 수천 건), 장애 전파(소비자 장애 때 생산자가 재시도·임시 저장·중복 전송을 떠안음), fan-out 복잡도(producer가 feature store·monitoring·warehouse·재학습 파이프라인을 모두 알아야 함), 재처리 불가능성이다.
- p139–140은 그림뿐이다. DB·앱 여러 개가 Hadoop·검색 엔진·모니터링·DW에 거미줄처럼 직접 연결된 그림과, 가운데 Kafka 하나를 두고 정리된 그림을 나란히 놓는다.
- 정의(p141): 생산자와 소비자 사이에서 수신, 저장, 라우팅, 전달, 확인 응답, 재전달, 부하 분산을 맡는 중간 시스템이다. 역할로 decoupling, 임시 보관 또는 영속 저장, 처리 성공 추적, 실패 시 재전달, consumer group·subscription 기반 병렬 소비, backpressure 완충, replay·retry 지점을 든다.

### 03. 메시지 브로커 분류 (p142–147)

- 제품명이 아니라 소비 의미론으로 나눈다(p142). 축은 여섯이다. 소비 후 삭제되는가 retention 동안 남는가, 소비 상태를 ack/delete로 관리하는가 offset/cursor로 관리하는가, 한 consumer만 처리하는가 여러 subscriber가 독립적으로 처리하는가, 과거 메시지를 다시 읽을 수 있는가, ordering 단위가 전체인가 partition·key·message group인가, 목적이 task distribution인가 event history 보존인가.
- 큐 중심(RabbitMQ, p143): 핵심은 작업 분배다. 여러 worker가 같은 queue를 나눠 읽는다. 이미지 리사이징, 비동기 이메일, 추론 후처리, background processing이 예다.
- Pub/Sub 중심(Google Cloud Pub/Sub, p144): 한 topic에 subscription을 여러 개 붙이고 각자 독립적으로 받는다. 추론 로그 한 건을 모니터링·경보·적재가 각각 받는 식이다.
- Retained log 중심(Kafka, p145): 읽었는지와 관계없이 보관 기간 동안 남고, offset으로 다시 읽는다. CDC 수집, 새 downstream의 과거 데이터 재적재, 잘못 계산된 집계의 재처리가 예다.
- 두 질문의 대비(p146–147): 전통 queue는 "이 작업을 어떤 worker가 처리할 것인가", Kafka는 "이 이벤트를 얼마나 오래 보관하고 어떤 consumer group이 어느 offset부터 읽을 것인가"를 묻는다.

### 04. 대표 메시지 브로커 (p148–149)

| 제품 | 강의의 설명 |
|---|---|
| RabbitMQ | 전통 메시지 큐, routing에 강한 범용성 |
| Amazon SQS | 관리형 queue. Standard는 높은 처리량·at-least-once·best-effort ordering, FIFO는 message group 기반 순서와 deduplication |
| Google Pub/Sub | 관리형 pub/sub. 서비스 분리, streaming analytics, data integration |
| Apache Kafka | partitioned retained log 기반 이벤트 스트리밍 플랫폼. replay와 다중 downstream |
| Apache Pulsar | subscription type으로 fan-out과 queueing 의미론을 유연하게 구성, durable cursor |

선택 기준은 task dispatch인가 event fact 보존인가, replay·backfill이 필요한가, 여러 downstream이 독립 소비하는가, 순서 보장 단위, 자체 운영인가 managed service인가다.

### 05. 전달 보장과 중복 처리 (p150–151)

- At-most-once는 유실 가능, 중복 최소. At-least-once는 유실은 줄지만 중복 가능이고 대부분의 실무 시스템이 전제로 삼는 모델이다.
- Exactly-once를 "외부 세계 전체에서 한 번"으로 받아들이면 위험하다고 경고한다. 실제로는 특정 시스템 경계, 특정 sink, 특정 transaction protocol 안에서만 성립하는 경우가 많다(p150).
- 실무 설계의 기본은 at-least-once를 전제로 한 idempotent consumer다. idempotency key, deduplication table, upsert sink, transactional write, retry count, dead-letter queue, poison message 격리를 든다(p151).

## 핵심

- 브로커를 제품이 아니라 "소비 후 무엇이 남는가"로 가르는 분류 축 여섯 개(p142)가 이 소단원의 틀이다. 전문은 [[메시지 브로커]]에 모았다.
- p150의 exactly-once 경고는 Part 1이 흐리게 남긴 부분을 정확히 짚는다. 엔진의 exactly-once가 상태 반영에 한정된다는 근거는 [[스트림 처리]]에, 멱등 반영의 수단은 [[멱등성]]에 있다.
- 직접 연결의 네 한계(p137–138)는 [[AI DE 강의 1-11 EDA와 Kafka]]의 허브 앤 스포크(N×M → 1:N)를 한 번 더 설명한 것이다. Part 4는 여기에 "재처리 불가능성"을 넷째 한계로 더한다. 두 강의를 잇는 연결은 위키의 관찰이다([[이벤트 기반 아키텍처]]).

## 주의·결함

- ✅ p148의 SQS 서술은 맞다. AWS 문서가 Standard 큐를 "ensure at-least-once message delivery"와 "best-effort attempt to maintain the order"로, FIFO 큐의 중복 제거를 "within the 5-minute deduplication interval"로 적는다. 다만 FIFO의 "exactly-once processing"은 AWS가 붙인 이름이고, 실제로는 5분 창 안에서 전송 중복을 막는 것이다. 소비 쪽 처리 완료는 여전히 visibility timeout과 소비자 코드에 달려 있다. [https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues.html , 2026-09-28 확인]
- ✅ p149의 Pulsar 서술은 맞다. 문서가 "There are four subscription types in Pulsar: exclusive, shared, failover, key_shared"라고 적고, cursor는 BookKeeper에 durable하게 저장된다. [https://pulsar.apache.org/docs/next/concepts-messaging/ , 2026-09-28 확인]
- p147의 "Queue 중심 모델 = ack/delete, visibility timeout"은 SQS의 용어이고, RabbitMQ는 visibility timeout 대신 unacked 메시지를 연결이 끊기면 다시 넣는다. 강의는 두 제품의 방식을 한 목록에 섞는다. 위키의 관찰이다.
- 강의는 Part 1의 [[AI DE 강의 1-11 EDA와 Kafka]](전통 브로커 vs 이벤트 스트리밍 표)를 참조하지 않는다. 같은 대비가 두 번 나오면서 Part 4 쪽이 더 정교하다(삭제 여부 외에 소비 상태 관리·순서 단위 축이 있다).

## 관련

- 개념: [[메시지 브로커]] · [[이벤트 기반 아키텍처]] · [[멱등성]] · [[스트림 처리]]
- 엔티티: [[Apache Kafka]]
- 이전 강의: [[AI DE 강의 4-05 캐싱 레이어와 캐싱 전략]]
- 다음 강의: [[AI DE 강의 4-07 메시지 브로커와 스트림 처리 엔진]]

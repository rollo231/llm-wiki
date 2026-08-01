---
type: concept
title: Message broker
area: [data-engineering]
aliases: [메시지 브로커, 메시지 큐, Message Queue, Pub/Sub, 전달 보장, delivery semantics, idempotent consumer]
tags: [data-engineering, message-broker, kafka, pubsub, queue, delivery-semantics, idempotency, streaming]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch3 Message brokers]]", "[[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]]"]
---

# Message broker

**생산자와 소비자 사이에 위치하여 메시지의 수신·저장·라우팅·전달·확인응답·재전달·부하분산을 담당하는
중간 시스템.**

> ⭐ **분류는 제품명이 아니라 소비 의미론(consumption semantics)으로 한다.**

## 브로커가 없을 때 — 직접 연결의 4가지 한계

| # | 문제 | 내용 |
|---|---|---|
| **1** | **속도 불일치** | 생산자 초당 수만 건 vs 소비자 수천 건. **중간 버퍼가 없으면 소비자 장애가 곧 생산자 장애로 전파** |
| **2** | **장애 전파** | 소비자 장애 시 생산자가 재시도·임시 저장·중복 전송·실패 복구를 직접 처리 |
| **3** | **fan-out 복잡도** | 하나의 이벤트를 feature store·monitoring·warehouse·retraining이 동시에 소비해야 하면 **producer가 downstream 의존성을 모두 알아야 함** |
| **4** | **재처리 불가능성** | **새 downstream이 생겼을 때 과거 이벤트를 다시 읽을 수 없음** |

> **3번의 downstream 목록이 AI 파이프라인 그대로다.** 브로커는 일반 EDA 장치이면서 동시에
> **ML 시스템의 fan-out 지점**이다.
>
> **4번이 [[Lambda and Kappa architecture]]의 전제다.**

## ⭐⭐ 분류 축 6가지

| 축 | 질문 |
|---|---|
| **보관** | 메시지는 소비 후 삭제되는가, retention 기간 동안 남는가 |
| **소비 상태** | ack/delete로 관리되는가, **offset/cursor**로 관리되는가 |
| **팬아웃** | 한 consumer만 처리하는가, **여러 subscriber가 독립적으로** 처리하는가 |
| **재생** | **과거 메시지를 다시 읽을 수 있는가** |
| **순서** | ordering 보장이 전체 단위인가, **partition/key/message group 단위**인가 |
| **목적** | **task distribution**인가, **event history 보존**인가 |

**제품을 외우는 대신 이 축으로 판단한다.** [[Graph data model]]의 "Property Graph vs RDF 판단
6문항"과 같은 서술 방식이다.

## 세 가지 모델

| 모델 | 기본 질문 | 대표 | 용도 |
|---|---|---|---|
| **Queue 중심** | **"이 메시지를 누가 가져가서 처리할 것인가"** | RabbitMQ, SQS | 이미지 리사이징, 비동기 이메일, **모델 추론 후처리**, 배치 job trigger, retry 가능한 task dispatch |
| **Pub/Sub 중심** | 하나의 이벤트를 여러 시스템이 **각각 독립적으로** 받는다 | Google Pub/Sub | **모델 추론 로그 1건 → 모니터링 + 경보 + 적재 시스템이 각각 수신** |
| **Retained log 중심** | **"얼마나 오래 보관하고, 어떤 consumer group이 어느 offset부터 읽을 것인가"** | [[Apache Kafka]] | CDC 수집, 클릭 로그, feature event, **새 downstream 추가 후 과거 데이터 재적재**, **잘못 계산된 집계의 재처리** |

### ⭐ Queue vs Kafka log — 무엇을 빼고 무엇을 얻었나

| Queue 중심 모델 | Kafka log 중심 모델 |
|---|---|
| 메시지 처리 성공 후 **삭제** | **retention 기간 동안 보관** |
| ack/delete, visibility timeout | **consumer group별 offset 관리** |
| 작업 분배와 retry에 적합 | 여러 downstream이 동일 stream을 **독립적으로** 소비 |
| worker pool 확장에 자연스러움 | **replay, backfill, new consumer 추가에 유리** |

> **[[Batch and stream processing]]의 "Kafka는 기능을 빼서 이겼다"가 여기서 정확해진다 —
> 삭제를 빼고 replay를 얻었다.**

## 대표 제품

| 제품 | 특징 |
|---|---|
| **RabbitMQ** | 전통적 메시지 큐, **routing에 강한 범용성** |
| **Amazon SQS** | 관리형. **Standard** = 높은 처리량·at-least-once·**best-effort ordering**. **FIFO** = message group 기반 순서 + deduplication |
| **Google Pub/Sub** | 관리형 pub/sub. topic + subscription |
| **[[Apache Kafka]]** | **partitioned retained log.** offset·partition·consumer group |
| **Apache Pulsar** | **subscription type으로 fan-out과 queueing 의미론을 유연하게 구성.** durable cursor |

**선택 기준 5문항:** task dispatch인가 event fact 보존인가 · **replay와 backfill이 필요한가** ·
여러 downstream이 독립 소비하는가 · 순서 보장은 어디까지 필요한가 · 자체 운영인가 managed인가.

## ⭐ 전달 보장 3종

| 보장 | 뜻 |
|---|---|
| **At-most-once** | 유실 가능, 중복은 최소화 |
| **At-least-once** | 최소 한 번 전달. **중복 처리 가능.** **대부분의 실무 시스템의 기본** |
| **Exactly-once** | ⚠️ 아래 참조 |

> ⭐⭐ **"exactly-once를 '외부 세계 전체에서 한 번만 처리된다'는 뜻으로 받아들이면 위험하다.
> 실제로는 특정 시스템 경계, 특정 조건, 특정 sink, 특정 transaction protocol 안에서 성립하는
> 경우가 많다."**

**그 "경계"가 무엇인지는 [[Stream processing semantics]]에서 구체화된다** — **재읽기 가능한 입력
계층 + 체크포인트(상태 + 입력 위치) + 중복에 안전한 출력 저장소**의 조합이 성립할 때만 유효하다.
셋 중 하나라도 없으면 exactly-once가 아니다.

### 실무의 기본 — at-least-once + idempotent consumer

> **"실무 설계의 기본은 at-least-once를 전제로 한 idempotent consumer."**

| 장치 | 역할 |
|---|---|
| **idempotency key** | 같은 메시지를 두 번 받아도 한 번만 반영 |
| **deduplication table** | 처리한 키를 기록해 중복 판정 |
| **upsert sink** | 재실행해도 같은 결과가 되는 쓰기 |
| **transactional write** | 처리와 오프셋 커밋을 한 트랜잭션으로 |
| **retry count** | 무한 재시도 방지 |
| **dead-letter queue** | 실패 메시지 격리 |
| **poison message 격리** | 반복 실패로 파이프라인을 막는 메시지 분리 |

**[[Change data capture]]의 "멱등하게 설계해야 한다"에 대한 구체적 장치 목록이다.**

## ⭐ 브로커 vs 스트림 처리 엔진 — 경계는 상태에 있다

> **"이 구분이 흐려지면 Kafka만 두고도 실시간 집계가 끝난다고 오해하거나, 반대로 Flink나 Spark만
> 붙이면 메시징 계층이 없어도 된다고 착각한다."**

| | 중심 질문 |
|---|---|
| **브로커 (운반 계층)** | 이벤트를 **어떻게 안전하게 흘리고 보관**할 것인가 |
| **엔진 (계산 계층)** | 계속 들어오는 이벤트를 **어떤 시간 기준과 상태 기준으로 계산**할 것인가 |

### 경계선의 정확한 위치

| | 구현 |
|---|---|
| **Stateless** — 각 레코드를 독립 처리 (필터링, 포맷 변환) | **브로커에 연결된 단순 Consumer app으로 충분** |
| **Stateful** — 여러 이벤트의 관계 파악 (윈도우 집계, 패턴 탐지, 스트림 조인) | ⭐ **엔진이 필요하다** |

> **"데이터 간의 관계를 파악하려면 반드시 '기억(State)'이 필요하다."**

### 왜 엔진만으로도 안 되나

> **"제대로 보장하기 위해 다시 읽을 수 있는 입력 계층과 상태 저장 공간이 필요하다."**

체크포인트는 **각 연산자의 상태와 입력 위치를 함께** 저장한다. 복구 시 그 입력 위치부터 다시
읽어야 하므로, **재읽기 가능한 브로커가 없으면 exactly-once 복구가 성립하지 않는다.**

**이것이 "브로커는 불필요하다"는 오해의 답이다.**

## 관련 페이지

- [[Apache Kafka]] — retained log 모델의 대표 구현
- [[Apache Flink]] · [[Apache Spark]] — 계산 계층
- [[Stream processing semantics]] — 상태·시간·체크포인트
- [[Batch and stream processing]] — 언제 스트림인가
- [[Lambda and Kappa architecture]] — replay가 아키텍처가 되는 지점
- [[Change data capture]] — 멱등 소비
- [[Distributed processing]] — "비동기 decoupling은 broker"

## 출처

- [[AI DE Course - Part4 Ch3 Message brokers]]
- [[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]]

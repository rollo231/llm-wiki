---
type: source
title: AI DE Course - Part4 Ch3 Message brokers
area: [data-engineering]
aliases: [Part4 Ch3-1, 메시지 브로커의 종류와 특징]
tags: [data-engineering, course, fast-campus, message-broker, kafka, pubsub, delivery-semantics, idempotency]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf (p133–151)"]
---

# AI DE Course - Part4 Ch3 Message brokers

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 4** Ch3 "스트리밍 데이터 처리"의 소단원 **1**
"메시지 브로커의 종류와 특징". 원본(로컬): `raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` **p133–151**
(356p 중). 강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐ **이 소단원의 최대 수확은 분류 축이다.** 제품명(RabbitMQ / Kafka / SQS…)이 아니라
> **소비 의미론(consumption semantics)** 으로 브로커를 가른다. Part 1 CH04-3,4가 *"Kafka는 메시지
> 큐가 아니다"* 까지 갔다면, 여기는 **왜 다른지를 6개 축으로 분해**한다.

## 구성

`01 스트리밍 데이터 · 02 메시지 브로커 · 03 메시지 브로커 분류 · 04 대표 메시지 브로커 ·
05 전달 보장과 중복 처리`

## 스트리밍 데이터란

> **"끝이 정해지지 않은 이벤트의 연속 (Unbounded Data)."**

| | 뜻 |
|---|---|
| **배치 데이터** | 이미 모인 데이터를 한 번에 처리 |
| **스트리밍 데이터** | 클릭·결제·센서값·**CDC 변경 이벤트**·**모델 추론 로그** — 계속 발생하고 계속 유입 |

두 관점의 정의를 병기한다:

- **Kafka 관점** — event/record는 topic에 append되는 데이터 단위. 각 record는 partition 안에서
  순서를 가지며 **offset**으로 식별
- **Flink 관점** — stream은 bounded 또는 unbounded data stream. **unbounded stream은 종료 지점이
  없는 입력**

> **이 두 관점의 병기가 소단원 2(브로커 vs 엔진)의 복선이다** — 같은 "스트림"을 브로커는 저장 단위로,
> 엔진은 계산 대상으로 본다.

## ⭐ 브로커가 없을 때 — 직접 연결의 4가지 한계

| # | 문제 | 내용 |
|---|---|---|
| **1** | **속도 불일치** | 생산자는 초당 수만 건, 소비자는 수천 건만 처리 가능. **중간 버퍼가 없으면 소비자 장애·지연이 곧 생산자 장애로 전파** |
| **2** | **장애 전파** | 소비자 장애 시 생산자가 재시도·임시 저장·중복 전송·실패 복구를 **직접** 처리해야 함 |
| **3** | **fan-out 복잡도** | 하나의 이벤트를 feature store, monitoring, notification, warehouse, model retraining pipeline이 동시에 소비해야 하면 **producer 코드가 downstream 의존성을 모두 알아야 함** |
| **4** | **재처리 불가능성** | 소비자가 잘못 처리했거나 **새로운 downstream이 생겼을 때 과거 이벤트를 다시 읽을 수 없음** |

> ⭐ **3번의 downstream 목록이 AI 파이프라인 그대로다** — feature store, monitoring, retraining.
> 일반 EDA 설명이 아니라 **ML 시스템 맥락에서 브로커를 정당화**한다.
>
> **4번이 Ch3-5(카파 아키텍처)의 전제가 된다.** "과거를 다시 읽을 수 있다"가 곧 재처리 가능성이다.

## 메시지 브로커의 정의

> **"생산자와 소비자 사이에 위치하여 메시지의 수신·저장·라우팅·전달·확인응답·재전달·부하분산을
> 담당하는 중간 시스템."**

제공하는 것 8가지: producer-consumer decoupling · 메시지 임시 보관 또는 영속 저장 · consumer 처리
성공 여부 추적 · 실패 시 재전달 · consumer group 또는 subscription 기반 병렬 소비 ·
topic/queue/routing key/subscription 기반 전달 제어 · **backpressure 완충 지점** ·
**replay 또는 retry 지점**.

## ⭐⭐ 분류 축 — 제품명이 아니라 소비 의미론으로

> **"제품명 기준보다 소비 의미론 기준으로 분류."**

| 축 | 질문 |
|---|---|
| **보관** | 메시지는 소비 후 삭제되는가, retention 기간 동안 남는가 |
| **소비 상태** | ack/delete로 관리되는가, **offset/cursor**로 관리되는가 |
| **팬아웃** | 하나의 메시지는 한 consumer만 처리하는가, **여러 subscriber가 독립적으로** 처리하는가 |
| **재생** | **과거 메시지를 다시 읽을 수 있는가** |
| **순서** | ordering 보장은 전체 단위인가, **partition/key/message group 단위**인가 |
| **목적** | 주요 목적은 **task distribution**인가, **event history 보존**인가 |

> ⭐ **이 6축이 이 소단원을 다른 브로커 소개 자료와 구별한다.** 제품을 외우는 대신 축으로 판단하게
> 만든다. Part 3의 "Property Graph vs RDF 판단 6문항"과 같은 서술 방식이고, 이 강의가 잘하는 패턴이다.

## 세 가지 모델

### 1. 큐 중심 (Queue) — 작업 분배

> **"이 메시지를 누가 가져가서 처리할 것인가."** 기본적으로 FIFO.

RabbitMQ의 queue는 메시지를 쌓아두는 대기열. 여러 처리 프로그램이 같은 queue를 함께 읽으면서 일을
나눠 갖는다.

용도: 이미지 리사이징 · 비동기 이메일 발송 · **모델 추론 후처리** · 배치 job trigger ·
API 요청 후 background processing · 실패 시 retry 가능한 task dispatch.

### 2. Pub/Sub 중심 — 독립적 팬아웃

하나의 이벤트를 여러 시스템이 **각각 독립적으로** 받는 구조. 보내는 쪽이 topic에 올리고, 받는 쪽은
**subscription**을 만들어 각자 수신. 한 topic에 여러 Sub을 붙일 수 있고 각 Sub은 독립적.

> 예: **"모델 추론 로그 1건이 들어오면 모니터링 시스템도 받고, 경보 시스템도 받고, 데이터 적재
> 시스템도 받는다."**

### 3. Retained log 중심 — 지우지 않고 보관

> **"Queue와 다른 점은 읽고 사라지지 않는다."**

Kafka에서 데이터가 topic에 추가되면 topic은 여러 **partition**으로 나뉜 로그 형태로 저장.
각 메시지는 partition 안에서 순서를 가지며 **offset**으로 위치가 구분. **메시지는 읽었는지와
관계없이 설정된 보관 기간 동안 유지.**

용도: CDC 데이터 수집 · 클릭 로그 분석 · feature event 저장 · 모델 모니터링 로그 ·
**새 downstream 시스템 추가 후 과거 데이터 다시 적재** · **잘못 계산된 집계의 재처리**.

### ⭐ Kafka와 전통 메시지 큐 — 기본 질문이 다르다

> **전통 queue의 기본 질문: "이 작업을 어떤 worker가 처리할 것인가?"**
>
> **Kafka의 기본 질문: "이 이벤트를 얼마나 오래 보관하고, 어떤 consumer group이 어느 offset부터
> 읽을 것인가?"**

| Queue 중심 모델 | Kafka log 중심 모델 |
|---|---|
| 메시지 처리 성공 후 삭제 또는 완료 처리 | **retention 기간 동안 보관** |
| ack/delete, visibility timeout 중심 | **consumer group별 offset 관리** |
| 작업 분배와 retry에 적합 | 여러 downstream이 동일 event stream을 **독립적으로** 소비 |
| worker pool 확장에 자연스러움 | **replay, backfill, new consumer 추가에 유리** |

> **Part 1 CH04-3,4([[AI DE Course - Ch4-3,4 EDA and Kafka]])의 "Kafka는 기능을 빼서 이겼다"가
> 여기서 정확해진다.** Part 1은 "Kafka ≠ 메시지 큐"를 선언했고, 여기는 **무엇을 빼고 무엇을
> 얻었는지**(삭제를 빼고 replay를 얻었다)를 설명한다.

## 대표 제품 5종

| 제품 | 특징 |
|---|---|
| **RabbitMQ** | 전통적인 메시지 큐와 **routing에 강한 범용성** |
| **Amazon SQS** | 관리형 queue. **Standard**는 높은 처리량·at-least-once·**best-effort ordering**. **FIFO**는 message group 기반 순서와 **deduplication** 강화 |
| **Google Pub/Sub** | 관리형 pub/sub. 비동기 서비스 분리, streaming analytics, data integration, service integration, task parallelization |
| **Apache Kafka** | **partitioned retained log** 기반 이벤트 스트리밍 플랫폼. offset·partition·consumer group 중심. replay와 다중 downstream 소비에 적합 |
| **Apache Pulsar** | pub/sub 기반. **subscription type을 통해 fan-out과 queueing 의미론을 유연하게 구성 가능**, durable cursor 기반 소비 위치 관리 |

**선택 기준 5문항:**

1. task dispatch인가, **event fact 보존**인가
2. **replay와 backfill이 필요한가**
3. 여러 downstream이 독립적으로 소비해야 하는가
4. 순서 보장은 partition / key / message group 중 어디까지 필요한가
5. 자체 운영할 것인가, managed service를 쓸 것인가

> **Pulsar의 포지셔닝이 정확하다** — "queue냐 log냐"의 이분법을 subscription type으로 우회하는
> 제품이라는 점을 짚는다. 다만 **BookKeeper 기반 저장/서빙 분리 구조는 언급되지 않는다.**

## ⭐ 전달 보장 3종 — exactly-once에 대한 경고

| 보장 | 뜻 |
|---|---|
| **At-most-once** | 메시지가 유실될 수 있지만 중복 전달은 최소화. 장애 시 데이터 손실 가능 |
| **At-least-once** | 최소 한 번 전달. 유실 가능성은 줄지만 **중복 처리 가능**. **대부분의 실무 메시징 시스템의 기본** |
| **Exactly-once** | ⚠️ **"말 그대로 '외부 세계 전체에서 한 번만 처리된다'는 뜻으로 받아들이면 위험"** |

> ⭐⭐ **"실제로는 특정 시스템 경계, 특정 조건, 특정 sink, 특정 transaction protocol 안에서 성립하는
> 경우가 많다."**
>
> **이 경고가 Part 1보다 명백히 낫다.** [[Stream processing semantics]](Part 1 CH04-5,6)는
> exactly-once를 기능 목록처럼 다뤘는데, 여기는 **그 보장이 어디까지 유효한지**를 못 박는다.

### 실무 설계의 기본 — at-least-once + idempotent consumer

> **"실무 설계의 기본은 at-least-once를 전제로 한 idempotent consumer."**

장치 7가지: **idempotency key** · **deduplication table** · **upsert sink** · transactional write ·
retry count · **dead-letter queue** · **poison message 격리**.

> **이 목록이 Part 1 [[Change data capture]]의 "멱등성" 논의와 정확히 이어진다.** CDC 페이지에서
> "재전송 시 중복이 생기므로 멱등하게 설계"까지 갔다면, 여기는 **구체적 장치 7종**을 준다.

## 기존 페이지와의 대조

- **새 concept:** [[Message broker]]
- **[[Apache Kafka]] 보강** — 소비 의미론 6축과 "queue vs log" 대비표를 추가해야 한다.
- ⚠️ **[[Batch and stream processing]](Part 1)의 "Kafka ≠ 메시지 큐"가 여기서 확장된다.**
  모순은 아니고 정밀화다. Part 1 페이지에서 이쪽으로 링크가 필요하다.
- **[[Stream processing semantics]] 보강** — exactly-once의 범위 한정 경고를 반영해야 한다.
  **현재 위키 서술이 강의 Part 1을 따라 다소 낙관적이다.**
- **[[Change data capture]]** — idempotent consumer 장치 7종.

## 자료 품질

- ✅ **분류 축 6개 + 선택 기준 5문항** — 제품 나열이 아니라 판단 프레임
- ✅ **exactly-once에 대한 정직한 경고** — 이 코스에서 드문 절제
- ✅ Kafka/Flink 공식 문서의 용어 정의를 각각 인용
- ✅ SQS Standard vs FIFO의 실제 차이(best-effort ordering, message group, deduplication)가 정확
- ⚠️ **Pulsar의 BookKeeper 구조, Kafka의 KRaft/tiered storage 같은 아키텍처 차이는 없음** — 소비
  의미론 축은 잘 다루지만 **저장 계층 축은 비어 있다**
- ⚠️ p139·p140이 이미지 전용 슬라이드(텍스트 없음)
- ⚠️ **처리량·지연 수치가 하나도 없다** — 다섯 제품을 비교하면서 성능 축이 없다. (없는 것이 있는데
  틀린 것보다는 낫지만, "언제 무엇을 쓰나"의 절반이 빈다)

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Message broker]] · [[Batch and stream processing]] · [[Stream processing semantics]] ·
  [[Change data capture]] · [[Distributed processing]]
- 도구: [[Apache Kafka]] · [[Redis]]
- 앞: [[AI DE Course - Part4 Ch2 Caching strategies and TTL]]
- 다음: [[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]]

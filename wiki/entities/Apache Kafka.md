---
type: entity
title: Apache Kafka
area: [data-engineering]
aliases:
  - Kafka
  - 카프카
  - KRaft
  - Log compaction
  - Consumer group
  - min.ISR
  - acks=all
  - Retained log
  - Apache Kafka Connect
  - Kafka Connect
tags: [data-engineering, kafka, streaming, event-driven, message-broker, replication]
created: 2026-08-01
updated: 2026-08-19
sources: ["[[AI DE Course - Ch4-3,4 EDA and Kafka]]", "https://sinja.io/blog/data-landscape-guide-for-developers", "[[AI DE Course - Part4 Ch3 Message brokers]]", "[[AI DE Course - Part4 Ch1 HA replication and consensus]]"]
---

# Apache Kafka

분산 이벤트 스트리밍 플랫폼. **producer가 이벤트를 보내고 broker가 디스크에 저장하고 consumer가
가져간다** — 이게 전부다. 처리는 하지 않는다.

## 탄생 배경 — 기능을 뺀 것이 설계다

2010년경 LinkedIn 내부 프로젝트. 하루 수십억 건의 활동 추적 이벤트를 감당할 파이프라인이 필요했는데
기존 MQ(ActiveMQ·RabbitMQ)는 **'전달 보장'과 '복잡한 기능'에 집중하느라 처리 속도가 느렸다.**

Kafka의 선택은 **"무거운 기능은 다 빼버리자"** 였다 — 오직 높은 throughput과 수평 확장성만 남긴
로그 기반 아키텍처. 2011년 오픈소스화, 지금은 사실상의 표준(강의: Fortune 500의 80% 이상).

## 3대 구성 요소

| | 역할 | 비유 |
|---|---|---|
| **Producer** | 데이터를 생성해 특정 토픽으로 전송. **라우팅의 주체** | 보내는 사람 |
| **Broker** | 디스크에 저장하고 요청 시 전달. 영속성 책임 | 우체국·물류센터 |
| **Consumer** | 능동적으로 **가져와서**(pull) 처리 | 직접 수령하는 수신인 |

- **Producer의 4가지 결정** — 어느 토픽/파티션인지(라우팅), 직렬화, 배치 전송(네트워크 오버헤드
  최소화), **키 지정**(순서 보장·파티션 몰아주기).
- **Broker** — 메모리가 아니라 **디스크**에 저장하되 **순차 쓰기(sequential I/O)** 를 써서 "느린
  하드 디스크에서도 메모리급 속도"를 낸다. 3대 이상을 묶어 클러스터로 운영하고, 복제로 HA를 확보한다.
- **Consumer는 pull 모델** — broker가 밀어넣지(push) 않는다. 컨슈머가 자기 처리 능력만큼만 가져가므로
  **배압(backpressure)** 이 자연스럽게 걸리고 과부하 셧다운을 막는다.

## 데이터 모델 3종 — 토픽 · 파티션 · 오프셋

### 토픽 (Topic)

데이터가 흐르는 **논리적 채널**. 파일시스템의 폴더나 DB의 테이블에 가깝다. 클러스터 하나에 수천~
수만 개를 만들 수 있다. 네이밍 예: `order.completed` · `user.payment` · `click.log`.

### 파티션 (Partition)

토픽을 **물리적으로 분할**한 것. 확장성과 병렬 처리의 열쇠 — 파티션 수만큼 컨슈머를 붙일 수 있고
처리 속도가 그만큼 선형 확장된다.

> ⚠️ **파티션 개수는 한 번 늘리면 절대 줄일 수 없다.** 초기에 트래픽을 예측해 신중히 정해야 한다.

### 오프셋 (Offset)

파티션 **내부**에서 각 메시지에 순차 부여되는 고유 정수(0부터 1씩 증가).

- **파티션 내부에서만 유일하다** — 토픽 전체 기준이 아니다.
- 컨슈머가 "5번까지 읽었어"라고 **커밋**하면, 시스템이 재시작해도 정확히 6번부터 이어서 처리한다.
- **한 번 부여되면 불변** — 오래된 데이터가 삭제되어도 번호는 재사용되지 않는다.

## 가장 자주 하는 실수 — 순서 보장의 범위

> ⚠️ **토픽 전체(global) 순서는 보장되지 않는다. 파티션 내부에서만 보장된다.**

여러 파티션에 나뉜 데이터를 컨슈머가 병렬 처리하므로 **나중에 들어온 데이터가 먼저 처리될 수 있다.**
은행 거래처럼 순서가 중요한 로직에서는 치명적이다 — "입금(2)"보다 "출금(3)"이 먼저 실행되면
잔액 부족 에러.

**해결책은 키(Key)** — 메시지에 Key(user ID·order ID)를 지정하면 Kafka는 **같은 Key를 무조건 같은
파티션에 할당**한다. 그 파티션 안에서는 순차 쓰기이므로 순서가 보장된다.

## 신뢰성 — 레플리케이션

- 파티션마다 **Leader와 Follower**가 있고, **모든 읽기·쓰기는 Leader에서만** 일어난다.
  Follower는 끊임없이 복제해 싱크를 맞춘다(passive).
- 리더 브로커가 죽으면 살아있는 팔로워 중 하나가 **즉시 새 리더로 승격**되어 서비스가 끊기지 않는다.

## 로그 컴팩션 (Log Compaction)

두 가지 보관 정책의 대비:

| | Retention (기간 기반) | **Compaction (상태 기반)** |
|---|---|---|
| 기준 | 설정 기간(예: 7일) 지나면 삭제 | **Key 기준으로 중복 제거** |
| 남는 것 | 그 기간의 모든 변경 이력 | 각 Key의 **가장 최신 값만** |

**컴팩션된 토픽은 사실상 key-value store다.** 그래서 [[Change data capture]]에서 DB의 현재
스냅샷을 구성할 때 필수적이다 — 변경 이력 전체가 아니라 "지금 상태"를 복원해야 하기 때문.
디스크를 절약하고 재구동 시 최신 스냅샷을 빠르게 복원한다.

## 파티션 수 — 병렬도의 상한

> **"파티션 수는 병렬도의 상한과 비슷하다. 너무 적으면 처리가 한곳에 몰리고, 너무 많으면 운영 복잡도가
> 올라간다. 처음에는 요구 처리량에 맞춰 작게 시작하고 늘리는 편이 안전하다."**

⚠️ 늘리는 것은 되지만 **줄이는 것은 사실상 어렵다**(위 §확장 한계의 컨트롤러 병목과 같은 방향의 비용).

⭐ 그리고 이 부품 이름들이 **장애 대화의 어휘**다 — *"장애가 났을 때 **'어느 파티션의 어느 오프셋까지
처리됐는가'**를 묻는 습관만 들여도 운영 대화가 구체적이 된다."*

## Kafka Connect — 허브에 외부를 붙이는 다리

매번 커스텀 프로듀서·컨슈머를 짜지 않고 **검증된 커넥터**로 넣고 뺀다.

| | 방향 |
|---|---|
| 1️⃣ **Source** | 외부 시스템 → Kafka 토픽 (DB 변경 · 로그 파일 · 오브젝트 스토리지의 새 객체) |
| 2️⃣ **Kafka** | 이벤트를 보관하고 여러 소비자가 읽음 |
| 3️⃣ **Sink** | Kafka 토픽 → 외부 시스템 (웨어하우스 · 검색 엔진 · 오브젝트 스토리지) |

⭐ **작업 순서가 명시된다** — *"커넥터 목록을 먼저 살펴보고, **없을 때만 직접 프로듀서를 작성**하는
순서가 실무에서 흔하다."*

⚠️ **복잡한 변환이나 상태 기반 처리는 [[Apache Flink]]·[[Apache Spark]] 쪽이 적합하다.**
[[Change data capture]]의 Flink CDC와 고를 때: **Connect는 연결과 전달, Flink CDC는 변화 감지와 처리.**

⚠️ **운영 관측 규칙 하나** — *"커넥터 실패와 토픽 적체가 한 쌍으로 보이므로, 모니터링도
**Source·Sink·토픽 지연을 함께** 보면 된다."* → [[Data SLA and observability]]

## Zookeeper → KRaft

| | Zookeeper Mode (~2.x) | **KRaft Mode** (Kafka Raft) |
|---|---|---|
| 의존성 | 별도 Zookeeper 앙상블 필수 | **없음** — 브로커끼리 Raft 합의로 메타데이터 관리 |
| 관리 포인트 | 이중(브로커 ↔ 주키퍼 동기화 이슈) | 단일 프로세스 |
| 확장 한계 | 파티션 수십만 개 넘으면 컨트롤러 병목 | 메타데이터를 메모리 캐싱 + 이벤트 로그 |
| 장애 복구 | 느린 컨트롤러 페일오버 | 거의 즉시 |

**Kafka 3.3+ 부터 KRaft가 production ready이고, 주키퍼는 완전 제거 예정이다.**

⭐ **이 전환은 Kafka만의 사건이 아니라 축의 이동이다** — 합의 계층을 **외부 서비스**에 두는 방식에서
**제품 내장 라이브러리**로 옮기는 흐름이고, 얻는 것은 운영 컴포넌트 하나 감소, 내는 것은 **합의 장애가
제품 장애와 한 몸이 된다**는 점이다. → [[Apache ZooKeeper]] · [[Replication and consensus]]

⚠️ 그래도 ZooKeeper를 알아야 하는 이유는 남는다 — **분산 시스템이 하나의 상태에 합의하는 방식**을
이해하는 가장 짧은 길이기 때문이다.
(강의 기준 서술 — 실제 제거 시점은 확인 필요.)

## 컨슈머 그룹

같은 group ID를 가진 컨슈머들이 파티션을 **분담**한다.

- **스케일 아웃** — 파티션 개수만큼 컨슈머를 늘려 선형 확장.
- **리밸런싱** — 컨슈머 하나가 죽으면 Kafka가 즉시 감지해 남은 컨슈머에게 파티션을 자동 재분배.

그리고 **그룹이 다르면 같은 데이터를 각자 처음부터 소비한다.** 주문 이벤트 하나를 배송 시스템
(Group A)과 마케팅 시스템(Group B)이 동시에 받는 "One Data, Multi Use"가 여기서 나온다.

## 속도의 비밀 — Zero-Copy

Java 기반인데도 하드웨어 레벨 성능을 내는 핵심.

- **일반 전송** — 디스크 → 커널 → 유저(App) → 커널 → 네트워크. 데이터 복사 4회 + 컨텍스트 스위칭 4회.
- **Zero-Copy (`sendfile`)** — 커널의 PageCache에서 NIC 버퍼로 **직접** 전송. 복사 2회, 스위칭 2회.
  데이터가 User Space를 아예 거치지 않는다.
- 효과: **CPU 사용량 약 60% 감소**, 네트워크 대역폭 한계까지 성능을 끌어올림.

## 메시지 브로커와 다른 점

랜드스케이프 가이드와 강의가 **일치하는** 지점이고, Kafka를 이해하는 핵심이다.

| | 전통 브로커 (RabbitMQ·ActiveMQ) | **Kafka** |
|---|---|---|
| 전달 후 | 큐에서 **즉시 삭제** (휘발성) | 디스크에 **보관** (retention policy) |
| 모델 | 스마트 브로커 (push) | 스마트 컨슈머 (pull, 오프셋 자체 관리) |
| 과거 추적 | 불가 | **재생 가능(replayability)** — 오프셋을 되감아 처음부터 다시 |

**replayability가 단순 메시징을 넘어서는 지점이다** — 버그를 고친 뒤 과거 데이터를 재처리할 수 있다.

## 도입 시 고려사항 (강의가 명시하는 한계)

- **운영 복잡도** — 브로커·KRaft·스키마 레지스트리 등 관리 요소가 많고 전문 인력이 필요하다.
- **실시간성 한계** — Kafka는 **near real-time**에 최적화되어 있다. 마이크로초 단위 초저지연이
  필요한 HFT(초단타 매매)류에는 부적합할 수 있다.
- **순서 보장 이슈** — 위의 파티션 제약. 정교한 키 설계가 선행되어야 한다.

## 이름이 비슷해 헷갈리는 것

- **Kafka Connect** — Kafka를 외부 시스템에 연결하는 API. [[Change data capture]]의 Debezium이
  이 위에서 돈다. Sink 커넥터로 Elasticsearch·Redis 동기화를 코드 없이 붙일 수 있다.
- **Kafka Streams** — Java/Scala 스트림 처리 **라이브러리**. 앱에 임베드되어 돌고 Kafka에서만 동작.
  → [[Apache Flink]]의 "세 엔진 비교" 참조. **별도 클러스터가 필요 없다**는 것이 축이다.

---

# Part 4가 채운 것

## ⭐ "기능을 뺀 것이 설계다"의 정확한 내용

위 § 탄생 배경이 "무거운 기능을 다 뺐다"였다면, [[Message broker]]의 분류 축이 **무엇을 빼고
무엇을 얻었는지**를 명확히 한다 — **삭제를 빼고 replay를 얻었다.**

> **전통 queue의 기본 질문: "이 작업을 어떤 worker가 처리할 것인가?"**
> **Kafka의 기본 질문: "이 이벤트를 얼마나 오래 보관하고, 어떤 consumer group이 어느 offset부터
> 읽을 것인가?"**

| Queue 중심 모델 | Kafka log 중심 모델 |
|---|---|
| 처리 성공 후 **삭제** | **retention 기간 동안 보관** |
| ack/delete, visibility timeout 중심 | **consumer group별 offset 관리** |
| 작업 분배와 retry에 적합 | 여러 downstream이 동일 stream을 **독립적으로** 소비 |
| worker pool 확장에 자연스러움 | **replay, backfill, new consumer 추가에 유리** |

**Kafka를 고를지 판단하는 6축은 [[Message broker]]** — 보관 / 소비 상태 / 팬아웃 / 재생 / 순서 /
목적.

## ⚠️ 복제의 대가 — `acks=all`은 "안전"이 아니라 "안전하지 않으면 실패"

위 § 신뢰성 절은 Leader-Follower 구조까지만 다뤘다. **[[Replication and consensus]]가 그 비용을
말한다:**

> ⚠️ **"강력한 내구성을 위해 `Replication Factor`·`min.ISR`·`acks=all`을 높게 설정하면
> 저장 공간 비용이 급증하고, 여러 노드의 확인이 필요해 조건 미달 시 쓰기 작업이 실패한다."**

**ISR이 `min.ISR` 아래로 떨어지면 프로듀서가 예외를 받는다.** 이것이 버그가 아니라 설계이고,
[[CAP theorem]]에서 **일관성을 위해 가용성을 포기하는** 선택이다.

**권장 조합:** 다중 브로커 + `Replication Factor=3` + `min.ISR=2` + `acks=all`.
(3대 중 2대가 살아 있어야 쓰기가 가능 — 1대 장애는 감내, 2대 장애는 쓰기 중단.)

## exactly-once에 대한 경고

Kafka는 트랜잭션과 멱등 프로듀서를 제공하지만:

> ⚠️ **"exactly-once를 '외부 세계 전체에서 한 번만 처리된다'는 뜻으로 받아들이면 위험하다.
> 실제로는 특정 시스템 경계, 특정 조건, 특정 sink, 특정 transaction protocol 안에서 성립하는
> 경우가 많다."**

**실무 기본은 at-least-once + idempotent consumer**이고, 장치 7종(idempotency key ·
deduplication table · upsert sink · transactional write · retry count · DLQ · poison message 격리)은
[[Message broker]]에 정리했다.

## Kafka가 다른 페이지에서 하는 역할

| 맥락 | 역할 |
|---|---|
| [[Distributed processing]] | **데이터 분산**의 예 (topic partition) + **장애 허용 분산**의 예 (replication) |
| [[Stream processing semantics]] | ⭐ **재읽기 가능한 입력 계층** — 없으면 체크포인트 복구가 성립하지 않는다 |
| [[Lambda and Kappa architecture]] | **카파의 전제** — 불변 이벤트 로그, 오프셋 되감기 |
| [[Message broker]] | retained log 모델의 대표 구현 |
| [[Redis]] | Redis Stream이 "append-only log에 가까운 자료구조"로 같은 발상을 보인다 |

## ⚠️ 강의가 다루지 않은 것

- **tiered storage** — [[Lambda and Kappa architecture]]의 "수년치 보관" 비용 문제의 현대적 해법
- **Pulsar와의 아키텍처 비교** — BookKeeper 기반 저장/서빙 분리
- **처리량·지연 수치** — 브로커 5종을 비교하면서 성능 축이 없다

## 링크

- 상위 축: [[Batch and stream processing]] — Kafka는 저장·전달만, 처리는 스트림 프로세서 몫
- 분류: [[Message broker]] — 소비 의미론 6축, 전달 보장 3종
- 왜 near real-time인가: [[Latency and throughput]]
- 처리 쪽: [[Stream processing semantics]] · [[Apache Flink]] · [[Apache Spark]]
- 실어 보내는 것: [[Change data capture]] — CDC의 Transport 층
- 포맷: [[Columnar and in-memory data formats]] — Avro + Schema Registry
- 복제의 대가: [[Replication and consensus]] · [[CAP theorem]]
- 아키텍처: [[Lambda and Kappa architecture]] · [[Distributed processing]]
- 출처: [[AI DE Course - Ch4-3,4 EDA and Kafka]] · [[Data landscape guide for developers]] ·
  [[AI DE Course - Part4 Ch3 Message brokers]] ·
  [[AI DE Course - Part4 Ch1 HA replication and consensus]]

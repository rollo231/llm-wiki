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
tags: [data-engineering, kafka, streaming, event-driven, message-broker]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Ch4-3,4 EDA and Kafka]]", "https://sinja.io/blog/data-landscape-guide-for-developers"]
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

## Zookeeper → KRaft

| | Zookeeper Mode (~2.x) | **KRaft Mode** (Kafka Raft) |
|---|---|---|
| 의존성 | 별도 Zookeeper 앙상블 필수 | **없음** — 브로커끼리 Raft 합의로 메타데이터 관리 |
| 관리 포인트 | 이중(브로커 ↔ 주키퍼 동기화 이슈) | 단일 프로세스 |
| 확장 한계 | 파티션 수십만 개 넘으면 컨트롤러 병목 | 메타데이터를 메모리 캐싱 + 이벤트 로그 |
| 장애 복구 | 느린 컨트롤러 페일오버 | 거의 즉시 |

**Kafka 3.3+ 부터 KRaft가 production ready이고, 주키퍼는 완전 제거 예정이다.**
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

## 링크

- 상위 축: [[Batch and stream processing]] — Kafka는 저장·전달만, 처리는 스트림 프로세서 몫
- 왜 near real-time인가: [[Latency and throughput]]
- 처리 쪽: [[Stream processing semantics]] — Flink·Spark Streaming의 윈도우·상태·exactly-once
- 실어 보내는 것: [[Change data capture]] — CDC의 Transport 층
- 포맷: [[Columnar and in-memory data formats]] — Avro + Schema Registry
- 출처: [[AI DE Course - Ch4-3,4 EDA and Kafka]], [[Data landscape guide for developers]]

---
type: concept
title: Change data capture
area: [data-engineering]
aliases:
  - CDC
  - Change Data Capture
  - Debezium
  - Apache Flink CDC
  - Flink CDC
  - 변경 데이터 캡처
  - 로그 기반 복제
tags: [data-engineering, cdc, debezium, kafka, ingestion, streaming]
created: 2026-08-01
updated: 2026-08-19
sources: ["[[AI DE Course - Ch3-3,4 CDC]]", "https://sinja.io/blog/data-landscape-guide-for-developers"]
---

# Change data capture

DB의 변경(insert·update·delete)을 **트랜잭션 로그 수준에서** 포착해 다른 시스템으로 즉시 흘려보내는
기술. [[ETL and ELT]]의 Extract 단계를 배치 조회에서 **스트림**으로 바꾸는 부품이다.

## 왜 로그를 읽나 — polling과의 갈림길

추출의 제1원칙은 **"소스 시스템에 부하를 주지 말라"** 다. 변경분을 찾는 방법이 둘 있다.

| | polling (조회 기반) | **CDC (로그 기반)** |
|---|---|---|
| 방식 | `SELECT * WHERE updated_at > …` 를 반복 | DB가 이미 쓰고 있는 트랜잭션 로그를 구독 |
| 소스 DB 부하 | 쿼리 엔진(CPU·메모리)을 직접 소모 | 쿼리 엔진을 거의 쓰지 않음 (네트워크 대역폭만) |
| 놓치는 것 | 두 폴링 사이의 중간 상태, **delete** | 없음 — 모든 변경이 로그에 남는다 |
| 지연 | 폴링 주기 | 초 단위 이하 |

핵심 아이디어는 **"DB의 일기장을 몰래 읽는다"** 다. 트랜잭션 로그는 "누가·언제·무엇을·어떻게
바꿨는지"가 순차적으로 기록된 파일이고, DB마다 이름이 다르다.

| DB | 로그 이름 |
|---|---|
| MySQL / MariaDB | binlog (binary log) |
| PostgreSQL | WAL (write-ahead log) — logical decoding |
| Oracle | redo log (LogMiner) |
| MongoDB | oplog |

**포착 방법의 트릭:** CDC 도구는 DB에 데이터를 요청하지 않는다. **자신을 replica로 등록해서**
(replication protocol) 복제 스트림을 받아낸다. "나도 너의 가족이야"라고 속이는 셈이고, 그래서
소스의 쿼리 엔진을 우회한다.

## 3단계 파이프라인

```
Capture ─────────→ Transport ─────────→ Apply
(로그 구독·파싱)      (Kafka 등 버퍼)        (타겟에 반영)
```

1. **Capture** — 로그를 구독하고 바이너리를 표준 포맷(JSON·Avro)으로 파싱, 메타데이터(시간·트랜잭션
   ID) 추출.
2. **Transport** — 캡처된 이벤트를 메시지 큐에 담아 순서대로·유실 없이 배달. 여기서 버퍼링과
   **배압(backpressure)** 이 걸린다.
3. **Apply** — 타겟 시스템 특성에 맞게 최종 반영.

**엔지니어의 실제 일은 연결이 아니라 3단계 각각에서 유실(loss)·순서 뒤바뀜(out-of-order)·
중복(duplication)을 막는 것이다.** 이 셋이 CDC 품질의 전부다.

### Transport에 Kafka를 끼우는 이유

CDC 도구를 타겟 DB에 **직접** 연결하면 타겟이 죽을 때 CDC 전체가 멈춘다.
[[Apache Kafka]]를 중간에 두면 폭주 시 데이터를 가둬두는 **댐**이자 유실을 막는 **금고**가 된다
(디스크에 persist).

- **토픽 설계** — 가능하면 `1 table = 1 topic`.
- **순서 보장은 파티션 안에서만** 성립한다. 같은 row(PK)는 반드시 같은 파티션으로 가야 한다 →
  **키 기반 파티셔닝**. 입금·출금 순서가 뒤바뀌면 잔액 부족 에러가 나는 식의 사고가 여기서 난다.
- **전달 보장은 at-least-once** 가 현실적 기본값 — 유실은 막되 중복은 허용한다. 그래서 타겟 쪽을
  **멱등(idempotent)** 하게 구현해야 한다 (upsert).

## 타겟 반영 전략 4종

| 전략 | 하는 일 | 쓰는 곳 |
|---|---|---|
| **Append-only** | 덮어쓰지 않고 새 행으로 계속 쌓아 이력 보존 | DW, 감사 로그 |
| **Mirroring / Sync** | I/U/D를 그대로 반영해 항상 최신 상태 유지 | 검색 엔진, 캐시 |
| **Soft delete** | 실제로 안 지우고 `deleted=true` 플래그만 | 물리 삭제가 비싼 HDFS·S3 |
| **Upsert** | PK 기준으로 덮어쓰기 | 일반적인 정합성 유지 |

체크리스트: **upsert key 선정** · **재처리(reprocessing) 시 멱등성** ·
**event time 기준 최신값만 반영**(순서가 뒤바뀌어도 정합성 유지).

## 스키마 변경 — CDC가 조용히 죽는 지점

운영 DB에서 `ALTER TABLE ... RENAME COLUMN` 한 줄이면 준비되지 않은 CDC 커넥터는 즉시 멈춘다
(`Schema mismatch! Field not found in row schema`). 위험한 변경: 컬럼 이름 변경·삭제, 타입 변경,
default 없는 신규 컬럼 추가.

해법은 **Schema Registry** — 메시지 구조를 별도 저장소에서 버전별로 관리하고, Kafka에는
`데이터 + 스키마 ID`만 보낸다. 호환성 모드는 [[Columnar and in-memory data formats]]의 Avro 절과
같은 규칙(backward / forward / full)을 쓴다.

## Debezium — 오픈소스 사실상의 표준

- **Kafka Connect 기반** — 코딩 없이 JSON/YAML 설정으로 동작하고, Connect 플랫폼의 고가용성·확장성을
  물려받는다.
- **광범위한 DB 지원** — MySQL·PostgreSQL·Oracle·SQL Server·MongoDB·Cassandra.
- **스냅샷 + 스트리밍** — 최초 실행 시 기존 데이터를 스냅샷으로 한 번 옮기고, 완료되면 자동으로
  실시간 로그 읽기 모드로 전환한다. **이게 CDC 도구를 처음 붙일 때 가장 중요한 동작이다.**
- 스키마 변경 시 **별도 토픽으로 메타데이터 이벤트를 발행**하므로 그걸 모니터링해 대응한다.
- Red Hat 주도. 강의는 네이버·카카오·쿠팡이 표준으로 채택했다고 서술한다.

## Apache Flink CDC — Debezium 옆의 다른 경로

Debezium이 커넥터로 Kafka에 붙는 쪽이라면, **Flink CDC는 CDC를 [[Apache Flink]] 파이프라인 안으로
가져온다.** 위 3단계와 같은 구조를 Flink 잡 하나로 표현한다.

- **스냅샷 → 로그 추적** — 처음에는 전체 스냅샷으로 맞추고 이후 변경 로그만 따라간다.
- 하류로 Kafka · Iceberg · Hudi · Paimon · 검색 인덱스에 분배 → [[Table formats]]
- **Flink가 이미 팀의 스트림 엔진이면 학습 곡선이 완만하다** — 선택이 기존 스택의 함수다.

⚠️ 소스는 한계를 넷으로 못 박는다 — **스키마 변경 · 대량 백필 · 권한 · PII 취급은 별도 설계가
필요하고, 소스 DB 부하도 함께 살펴야 한다.** 앞 절의 *스키마 변경*·*소스 부하* 는 이 페이지가 이미
다루지만 **권한과 PII는 별개의 축**이다: CDC는 운영 DB의 **모든** 컬럼을 그대로 하류로 흘리므로,
마스킹·컬럼 필터를 파이프라인 안에 넣지 않으면 분석 저장소가 원본과 같은 등급의 민감 데이터를 갖게 된다.
→ [[Data catalog and semantic layer]]의 거버넌스

## 대표 유스케이스

- **MSA 데이터 동기화** — 주문 서비스가 배송 서비스의 존재를 모른 채 DB에 저장만 하면 이벤트가
  전달된다. 결합도 감소 · 비동기 확장성 · 장애 격리.
- **실시간 검색·캐시 갱신** — 상품 가격/재고 변경을 Elasticsearch 인덱스와 Redis 캐시에 즉시 반영.
  Kafka Connect **Sink** 커넥터로 코드 없이 붙일 수 있다.
- **레이크하우스 실시간 동기화** — OLTP(행 기반)에서 OLAP(컬럼너)으로 흘려보내는 통로
  → [[Analytical data storage tiers]]

## 링크

- 상위: [[ETL and ELT]] — CDC는 Extract 단계의 한 방식
- 실어 보내는 곳: [[Apache Kafka]] — 파티션·오프셋·로그 컴팩션. **로그 컴팩션된 토픽은 사실상
  key-value store라서 CDC로 DB 현재 스냅샷을 구성할 때 필수적이다**
- 포맷: [[Columnar and in-memory data formats]] — Avro와 Schema Registry
- 언제 처리하나: [[Batch and stream processing]]
- 출처: [[AI DE Course - Ch3-3,4 CDC]], [[Data landscape guide for developers]]

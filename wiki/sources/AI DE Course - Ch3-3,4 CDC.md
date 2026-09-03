---
type: source
title: AI DE Course - Ch3-3,4 CDC
area: [data-engineering]
aliases: [CH03-3 4 CDC, 데이터 수집 패턴 II, CDC 기술의 개념과 필요성]
tags: [data-engineering, course, fast-campus, cdc, debezium, kafka]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part1/11. CH03-3, 4. 데이터 수집 패턴 II CDC(Change Data Capture) 기술의 개념과 필요성 1, 2.pdf"]
---

# AI DE Course - Ch3-3,4 CDC

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 CH03-3,4**
"데이터 수집 패턴 II: CDC(Change Data Capture) 기술의 개념과 필요성 (1)(2)". 원본(로컬):
`raw/data-engineering/ai-de-course/part1/11. CH03-3, 4. 데이터 수집 패턴 II CDC(Change Data Capture) 기술의 개념과 필요성 1, 2.pdf`
(18p). 강의 홈: [[AI Data Engineering (Fast Campus course)]].

**개념 정리는 [[Change data capture]]에 옮겼다.** 여기는 이 덱 고유의 서술과 사례를 남긴다.

## 여는 사례 — 주문 취소

배치와 CDC의 차이를 타임라인으로 보여준다.

| 시각 (배치) | | 시각 (CDC) | |
|---|---|---|---|
| 10:00 AM | 고객이 '주문 취소' 클릭 | 10:00:00 | 고객이 '주문 취소' 클릭 |
| 10:00 AM | 주문 DB에만 '취소' 상태 저장 | 10:00:01 | CDC가 DB 로그에서 취소 이벤트 캡처·전송 |
| **02:00 PM** | **배송 팀은 취소 사실 모름 → 상품 포장·발송** | 10:00:02 | 배송 시스템에 '발송 중단' 알림 |
| 익일 09:00 | 배치 후 뒤늦게 확인 → 반품 비용 & 고객 불만 | 10:00:05 | 즉시 환불 완료 & 배송비 절감 |

**CDC의 가치를 "빠르다"가 아니라 "시스템 간 상태 불일치가 만드는 실제 비용"으로 설명하는 것이
이 덱의 접근이다.**

## 이 덱 고유의 서술

### 용어 3분할

강의가 명시적으로 나누는 세 층위 — 혼용하기 쉬운 지점이다.

1. **캡처(Capture)** — 변경 이벤트를 실시간으로 감지해 '낚아채는' **행위**.
   단순 조회가 아닌 **능동적 포착**이 핵심.
2. **로그 마이너(Log Miner)** — 기계어(binary) 로그에서 필요한 정보만 뽑아 사람이 읽을 수 있는
   형태(JSON 등)로 변환하는 **도구**.
3. **CDC (Pipeline)** — 단순 캡처를 넘어 가공(format)·필터링(filter)·전송(transport)하는
   **전체 파이프라인**.

> 강의의 암기 문장: *"어두운 로그 광산에서 로그 마이너가 열심히 일해서 변경 사항을 캡처하고,
> 그걸 CDC 파이프라인에 태워서 안전하게 보낸다."*

### 배치 → CDC 전환의 3축

| 배치 (legacy) | | CDC (modern) |
|---|---|---|
| 주기적 일괄 처리 (하루 1회, 새벽) | 실시간성 | 변경 즉시 감지, 1초 이내 반영 |
| "어제 데이터"만 조회 가능 | 지연 | 초 이하 |
| `SELECT *` 반복으로 **DB 성능 저하** | 부하 | 로그를 **비동기**로 읽어 본체 트랜잭션에 거의 영향 없음 |
| 전체 재전송 | 전송량 | 변경분(delta)만 → 네트워크 대역폭 효율 |

진화 경로: **Batch → Near Real-time → Real-time.**

### CDC의 4가지 가치

1. **실시간 의사결정** — 1초 전 데이터까지 반영된 대시보드
2. **시스템 부하 감소** — polling 쿼리 대신 로그를 비동기로. 소스 DB의 CPU·메모리를 거의 안 쓴다
3. **확장성·탄력성** — Kafka와 결합해 트래픽 폭주 시 **backpressure** 조절
4. **정확성 향상** — 변경분만 전송하므로 중복 처리 방지, 휴먼 에러·누락 리스크 감소

### 순서가 뒤바뀌면 생기는 재앙 (강의 사례)

은행 입출금에서 네트워크 지연으로 순서가 뒤바뀌면:

- 정상(1→2): 입금 +100만 → 출금 -50만 = **잔액 50만 (OK)**
- 장애(2→1): 잔액 0원 상태에서 출금이 먼저 처리 = **잔액 부족 에러 (Fail)**

→ 해법은 **키 기반 파티셔닝**(같은 row는 같은 파티션) + **멱등성**(upsert).
전달 보장은 **at-least-once** 를 택하고 중복은 허용한다.

### 스키마 변경으로 CDC가 죽는 순간

```
DB Admin:  ALTER TABLE Orders RENAME COLUMN shipping_addr TO addr;
           ADD COLUMN priority INT DEFAULT 0;

CDC Log:   FATAL: ConnectException: Schema mismatch!
           Field 'shipping_addr' not found in row schema.
```

해법 2단: **Schema Registry**(버전별 관리, Kafka에는 데이터 + 스키마 ID만) +
**호환성 모드**(backward를 필수 권장).
운영 팁: **Debezium은 스키마 변경 시 별도 토픽으로 메타데이터 이벤트를 발행**하므로 이를
모니터링해 즉시 대응한다.

### 2대 유스케이스

**MSA 데이터 동기화** — 주문 서비스(MySQL) → CDC → Kafka Topic → 배송 서비스(Postgres)

- **결합도 감소** — 주문 서비스는 배송 서비스의 존재를 몰라도 된다. API 호출 없이 DB에 저장만 하면
  나머지는 이벤트가 전달한다
- **비동기 확장성** — 주문이 폭주해도 배송 시스템은 자기 속도로 처리(lag)하므로 전체가 안 죽는다
- **장애 격리** — 배송 DB 점검 중에도 주문 서비스는 정상. 점검 후 쌓인 이벤트를 처리해 정합성 맞춤

**실시간 검색·캐시 갱신** — 상품 관리(MySQL) → CDC → Kafka → Elasticsearch 인덱스 + Redis 무효화

- MD가 가격을 수정하는 즉시 검색 결과에 반영 → 검색 가격과 상세 페이지 가격 불일치 방지
- 품절 상품이 검색에서 즉시 사라져 '헛걸음' 경험 방지
- 구현 팁: Kafka Connect **Sink**로 코드 없이 ES 동기화 / 문서 전체 덮어쓰기보다 **변경 필드만**
  부분 업데이트 / 캐시 갱신 시 **TTL 재설정**

## 마무리 문장

> 데이터 엔지니어의 핵심 역량은 단순히 데이터를 옮기는 것이 아니라,
> **비즈니스 가치를 실시간으로 전달하는 파이프라인을 설계하는 것**이다.

## 기존 페이지와의 대조

- **[[ETL and ELT]] 보강** — 랜드스케이프 가이드는 CDC를 한 단락("replication log를 읽는다,
  독립 부품은 Debezium")으로만 다뤘다. 이 덱이 **로그 이름(binlog/WAL/redo/oplog)**,
  **replication protocol로 replica를 위장하는 트릭**, 3단계 파이프라인, 순서·중복 처리,
  스키마 변경 대응, 타겟 반영 전략 4종까지 채운다. → 별도 개념 페이지 [[Change data capture]]로 분리.
- **[[Apache Kafka]]와의 접점** — "Kafka가 없으면 CDC 툴과 타겟 DB가 직접 연결되어 타겟 장애 시
  CDC 전체가 멈춘다"는 설명이 Kafka를 버퍼로 두는 이유를 명확히 한다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Change data capture]] (상세), [[ETL and ELT]], [[Apache Kafka]],
  [[Columnar and in-memory data formats]] (Avro·Schema Registry)
- 앞 챕터: [[AI DE Course - Ch3-1,2 Batch and ETL]]

---
type: source
title: AI DE 강의 1-08 CDC
aliases: [AI DE 1-08]
tags: [AI-DE-강의, 수집, CDC]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/data-engineering/ai-de-course/part1/11. CH03-3, 4. 데이터 수집 패턴 II CDC(Change Data Capture) 기술의 개념과 필요성 1, 2.pdf"
---

# AI DE 강의 1-08 CDC

[[AI 데이터 엔지니어링 강의]] Part 1의 수집 파트 두 번째 강의. DB 트랜잭션 로그를 읽어 변경만 실시간으로
흘려보내는 CDC를 원리·파이프라인·운영·사례 순으로 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 1 |
| 덱 제목 | 데이터 수집 : CDC (파일명: 데이터 수집 패턴 II CDC(Change Data Capture) 기술의 개념과 필요성 1, 2) |
| 원본 파일 | `part1/11. CH03-3, 4. 데이터 수집 패턴 II CDC(Change Data Capture) 기술의 개념과 필요성 1, 2.pdf` (18p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-02-19 |
| URL | 없음 (유료 강의 자료) |

## 요약

### 정의와 동기 (p2–7)

- **정의** — DB의 변경(Insert·Update·Delete)을 **로그 수준에서** 실시간으로 포착해 필요한 시스템으로 전달하는 기술.
- **주문 취소 사례** — 배치: 10시에 취소해도 배송팀은 모르고 발송 → 다음 날 아침 배치에서 확인, 반품 비용.
  CDC: 1초 뒤 로그에서 취소 이벤트를 잡아 2초 뒤 발송 중단 알림 → 즉시 환불.
- **트랜잭션 로그 = DB의 일기장** — Oracle Redo Log, MySQL·MariaDB Binlog, PostgreSQL WAL, MongoDB Oplog.
  무거운 SELECT로 DB를 괴롭히지 않고 일기장만 읽는다.
- **용어** — 캡처(변경을 능동적으로 낚아채는 행위), 로그 마이너(바이너리 로그에서 필요한 정보를 사람이 읽는
  형태로 뽑는 도구), CDC 파이프라인(가공·필터링·전송까지 전체).
- **배치(폴링) vs CDC** — 정해진 시간에 `SELECT *`를 반복해 DB에 부하를 주고 "어제 데이터"만 보는 방식에서,
  로그를 비동기로 읽어 부하 없이 변경분만 1초 안에 흘리는 방식으로.

### 3단계 파이프라인 (p8–12)

| 단계 | 하는 일 | 세부 |
|---|---|---|
| Capture | 로그를 감지·파싱해 표준 이벤트로 변환 | 복제 프로토콜로 "나도 replica야"라고 등록해 로그 스트림을 받는다(MySQL binlog, PostgreSQL WAL logical decoding, Oracle LogMiner). JSON·Avro로 번역 |
| Transport | 메시지 큐(Kafka)에 담아 순서대로 배달 | 버퍼링과 배압, 디스크 영속으로 유실 방지, 파티션으로 확장. 가능하면 1 테이블 = 1 토픽. **Kafka가 없으면 타깃 DB 장애 시 CDC 전체가 멈춘다** |
| Apply | 타깃 특성에 맞춰 반영 | Sink Connector, I·U·D 반영, 정합성 검증 |

엔지니어의 핵심 미션은 연결이 아니라 **유실·순서 뒤바뀜·중복을 막는 것**이다.

- **순서** — 입금(+100만) 뒤 출금(-50만)이 네트워크 지연으로 뒤바뀌면 잔액 부족 에러. Kafka는 파티션 안에서만
  순서를 보장하므로 **같은 Row ID는 같은 파티션으로**(키 기반 파티셔닝).
- **중복** — at-least-once는 유실을 막는 대신 중복을 허용한다 → 두 번 처리해도 결과가 같게(**멱등성**, upsert).
- **타깃 반영 전략**

| 전략 | 방식 | 용도 |
|---|---|---|
| Append-only | 변경·삭제도 새 행으로 쌓아 이력 보존 | DW·감사 로그(Snowflake·BigQuery) |
| Mirroring / Sync | I·U·D를 그대로 반영해 최신 상태 유지 | 검색 엔진·캐시(Elasticsearch·Redis) |
| Soft Delete | 실제로 지우지 않고 `deleted=true` | 물리 삭제가 어렵거나 비싼 HDFS·S3 |

  설계 체크리스트: upsert 키(PK) 선정, 재처리 시에도 안전한 멱등 설계, **이벤트 시간 기준으로 최신만 반영**.

### 스키마 변경 (p13)

운영 DB에서 `ALTER TABLE … RENAME COLUMN`이 실행되면 준비 안 된 파이프라인은 즉시 멈춘다
(`FATAL: ConnectException: Schema mismatch!`). 해법은 스키마 레지스트리(데이터 + 스키마 ID만 전송)와 호환성
모드, 그리고 Debezium이 스키마 변경 시 별도 토픽으로 내보내는 이벤트를 감시하는 것.

### Debezium (p14)

Kafka Connect 기반, 주요 DB 대부분 지원, 설정 파일만으로 동작, 최초 스냅샷 후 실시간 로그 읽기로 자동 전환,
스키마 변경 대응. Red Hat 주도. → [[Debezium]]

### 사례 (p15–16)

- **MSA 데이터 동기화** — 주문 서비스(MySQL) → CDC → Kafka → 배송 서비스(PostgreSQL). 주문 서비스는 배송
  서비스를 몰라도 되고(결합도 감소), 주문 폭주에도 배송은 자기 속도로 처리하고(비동기), 배송 DB 점검 중에도
  주문은 정상 동작한다(장애 격리). 팁: 멱등성, 계약 기반 스키마, 재발행 가능한 재처리 시나리오.
- **실시간 검색·캐시 갱신** — 상품 관리(MySQL) → CDC → Kafka → Elasticsearch 인덱스 갱신 + Redis 캐시 무효화.
  가격·재고를 즉시 반영해 검색 결과와 상세 페이지 가격이 일치한다. 팁: Sink Connector, 변경 필드만 부분 갱신,
  캐시 TTL 재설정.

## 핵심

- CDC는 [[AI DE 강의 1-07 배치 처리와 ETL·ELT]]의 원칙 **"소스 시스템에 절대 부하를 주지 말라"**의 해법이자,
  [[AI DE 강의 1-04 저장소의 진화 DW에서 Lakehouse까지]] 설계 5단계의 하이브리드(OLTP → OLAP 동기화)를 실제로
  잇는 선이다. → [[변경 데이터 캡처]]
- 정합성은 **세 장치가 한 세트**다: 키 기반 파티셔닝(순서) + 멱등 upsert(중복) + 이벤트 시간 기준 반영(늦게 온
  변경). 하나라도 빠지면 조용히 틀린다.
- CDC를 붙이는 순간 **운영 DB의 스키마가 하류 전체와의 계약이 된다** — `ALTER TABLE` 한 줄이 파이프라인을
  멈춘다. → [[스키마 진화]]

## 주의·결함

- ⚠️⚠️ **호환성 모드의 정의가 뒤바뀌었다.** 덱은 "Backward: 구버전 컨슈머가 신버전 스키마 데이터를 읽을 수 있게
  함", "Forward: 신버전 컨슈머가 구버전 스키마 데이터를 읽을 수 있게 함"이라고 쓴다. Confluent 문서의 정의는 정반대다 —
  **BACKWARD는 새 스키마를 쓰는 컨슈머가 옛 스키마로 쓰인 데이터를 읽는 것**, FORWARD는 옛 스키마를 쓰는 컨슈머가
  새 스키마로 쓰인 데이터를 읽는 것이다. 덱의 "Backward" 설명은 FORWARD의 정의다.
  [Confluent "Schema Evolution and Compatibility" — "Backward - consumers using new schema can read data written
  with old schema … Forward - consumers using old schema can read data written with new schema",
  https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html , 2026-09-14 확인]
  - **실무 영향** — Confluent의 기본값은 BACKWARD이고 이때는 **컨슈머를 먼저 업그레이드**해야 한다(FORWARD는
    프로듀서 먼저). 덱의 정의대로 이해하면 배포 순서를 거꾸로 잡는다.
  - **코스 내부 모순** — [[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]](덱 08)는 바르게 정의한다.
- **"중복 방지"와 "중복 허용"의 긴장** — p7은 "변경된 데이터만 전송하므로 중복 데이터 처리를 방지"한다고 하고,
  p11은 at-least-once에서 중복이 발생할 수 있으니 멱등성으로 막으라고 한다. 후자가 맞다.
- "국내 주요 테크 기업(네이버·카카오·쿠팡)도 표준으로 채택"은 출처가 없다.
- 로그 기반 CDC의 운영 부담은 다루지 않는다 — 예를 들어 CDC가 오래 멈추면 PostgreSQL은 WAL이 쌓여 디스크가 찰 수
  있고, MySQL은 binlog가 삭제돼 커넥터가 위치를 잃는다. *(위키 메모)* → [[변경 데이터 캡처]]

## 관련

- 개념·도구: [[변경 데이터 캡처]] · [[Debezium]] · [[Apache Kafka]] · [[스키마 진화]] · [[이벤트 기반 아키텍처]]
- 이전 강의: [[AI DE 강의 1-07 배치 처리와 ETL·ELT]]
- 다음 강의: [[AI DE 강의 1-09 비정형 데이터 수집과 전처리]]

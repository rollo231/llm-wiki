---
type: entity
title: Debezium
aliases: []
tags: [도구, 수집, CDC]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "[[AI DE 강의 1-08 CDC]]"
  - "[[AI DE 강의 1-11 EDA와 Kafka]]"
---

# Debezium

오픈소스 **로그 기반 [[변경 데이터 캡처]](CDC) 도구.** DB의 트랜잭션 로그를 읽어 행 변경(Insert·Update·
Delete)을 이벤트로 만들고 [[Apache Kafka]]로 보낸다. [[AI DE 강의 1-08 CDC]]는 이를 "오픈소스 CDC의
사실상 표준"으로 소개한다.

## 특징 (강의 기준)

| 항목 | 내용 |
|---|---|
| 실행 기반 | Kafka Connect 위의 플러그인. 코드 없이 JSON·YAML 설정으로 동작하고, Kafka Connect의 고가용성·확장성을 얻는다 |
| 지원 DB | MySQL, PostgreSQL, Oracle, SQL Server, MongoDB, Cassandra 등 |
| 스냅샷 + 스트리밍 | 처음 실행 시 기존 데이터를 스냅샷으로 옮기고, 끝나면 자동으로 실시간 로그 읽기로 전환 |
| 스키마 변경 | 테이블 구조 변경을 감지해 버전을 관리하고, 스키마 변경 이벤트를 별도 토픽으로 발행 |
| 주도 | Red Hat |

## 동작 방식

- **복제본인 척한다** — MySQL에서는 복제 프로토콜로 자신을 replica로 등록해 binlog 스트림을 받는다. DB의 쿼리
  엔진을 거의 쓰지 않는다.
- **로그를 번역한다** — 바이너리 로그(MySQL binlog, PostgreSQL WAL의 logical decoding, Oracle redo log)를
  JSON·Avro 이벤트로 변환한다.
- [[AI DE 강의 1-11 EDA와 Kafka]]의 허브 앤 스포크 그림에서 "Database CDC — MySQL Binlog (Debezium)"로
  Kafka에 들어가는 입력 중 하나로 나온다.

## 운영 체크리스트 (강의)

토픽 네이밍 규칙, 커넥터 설정 최적화, 모니터링 알람. 스키마 변경 이벤트 토픽을 감시해 즉시 대응한다.

## 주의

- "네이버·카카오·쿠팡 등 국내 주요 테크 기업이 표준으로 채택"([[AI DE 강의 1-08 CDC]])은 출처가 없다.

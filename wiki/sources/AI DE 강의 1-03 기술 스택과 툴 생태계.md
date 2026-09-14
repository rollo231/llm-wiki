---
type: source
title: AI DE 강의 1-03 기술 스택과 툴 생태계
aliases: [AI DE 1-03]
tags: [AI-DE-강의, 개요, 도구]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/data-engineering/ai-de-course/part1/03. CH01-4. AI 엔지니어링 필수 기술 스택 및 툴 생태계.pdf"
---

# AI DE 강의 1-03 기술 스택과 툴 생태계

[[AI 데이터 엔지니어링 강의]] Part 1의 세 번째 강의. AI DE에게 필요한 기술 스택을 목록으로 소개한다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 1 |
| 덱 제목 | AI 엔지니어링 필수 기술 스택 및 툴 생태계 |
| 원본 파일 | `part1/03. CH01-4. AI 엔지니어링 필수 기술 스택 및 툴 생태계.pdf` (8p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-02-19 |
| URL | 없음 (유료 강의 자료) |

## 요약

"현업 채용 공고(JD)로 보는 필수 역량" 네 가지(p4):

| 영역 | 내용 |
|---|---|
| 클라우드 플랫폼 | AWS·Azure·GCP에서의 데이터 저장·처리·보안, 인프라 운영 |
| 데이터베이스 | SQL(필수) + NoSQL(선택), 쿼리 최적화 |
| 프로그래밍 언어 | Python(데이터 처리), Java/Scala(분산 처리) |
| 파이프라인·오케스트레이션 | Apache Kafka(실시간), Airflow(워크플로우) |

이어서 도구마다 한 장씩:

- **Python 생태계** — Pandas(DataFrame 조작, 결측치·필터·GroupBy, CSV·Excel·SQL 입출력),
  PyTorch(텐서 연산과 GPU 가속, 동적 그래프로 쉬운 디버깅).
- **SQL** — ANSI SQL(표준 문법, 추출·조작·트랜잭션) vs Spark SQL(대용량 처리, 분석, 인메모리 연산).
- **Java·Scala가 여전히 강한 이유**
  - [[Apache Spark]] — Scala 기반, JVM·하둡 생태계 호환, SQL·스트리밍·머신러닝을 한 엔진에서.
  - [[Apache Flink]] — 저지연·고처리량 스트리밍, exactly-once 상태 관리, Java·Scala 모두 일급 지원.
  - [[Apache Kafka]] — 분산 시스템의 "혈관"(데이터 흐름·버퍼링), Scala로 코어 구현, Kafka Streams.
- **인프라** — Docker(로컬과 프로덕션의 일관성, Docker Compose), AWS(S3 중심 분석 생태계, 관리형 서비스),
  Azure(MS Office·AD 연동, Synapse Analytics, 하이브리드 클라우드), GCP(BigQuery, GKE, Vertex AI).

## 핵심

- AI DE 스택이라고 소개하지만 실제 목록은 **기존 DE 스택(클라우드·SQL·JVM 엔진·Kafka·Airflow)에
  PyTorch를 더한 것**이다. 피처 스토어·벡터 DB 같은 AI 쪽 부품은 이 덱에 없고 뒤 강의에서 나온다
  ([[피처 스토어]] · [[비정형 데이터 파이프라인]]).
- Java·Scala를 따로 한 장 할애하는 이유가 곧 Part 1 후반의 주인공들이다 — Spark·Flink·Kafka는
  [[AI DE 강의 1-10 배치 vs 스트리밍]]부터 [[AI DE 강의 1-12 실시간 처리 엔진]]까지 계속 등장한다.

## 주의

- "채용 공고 분석"이라고 하지만 표본(어느 회사, 몇 건)이 없다.
- 8p 전체가 목록형 소개라 **언제 무엇을 고르는지**에 대한 기준은 없다.
- p3 "데이터 사이언티스트 VS 데이터 엔지니어"는 타이틀만 있고 비교 내용이 없다.

## 관련

- 이전 강의: [[AI DE 강의 1-02 AI DE 마인드셋 Latency와 Versioning]]
- 다음 강의: [[AI DE 강의 1-04 저장소의 진화 DW에서 Lakehouse까지]]

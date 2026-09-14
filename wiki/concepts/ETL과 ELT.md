---
type: concept
title: ETL과 ELT
aliases: [ETL, ELT, Extract Transform Load, Extract Load Transform]
tags: [수집]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "[[AI DE 강의 1-04 저장소의 진화 DW에서 Lakehouse까지]]"
  - "[[AI DE 강의 1-07 배치 처리와 ETL·ELT]]"
---

# ETL과 ELT

데이터를 원천에서 분석 저장소로 옮기는 두 순서.

- **ETL (Extract → Transform → Load)** — 별도 서버에서 정제·가공한 뒤 **완성된 데이터만** 적재한다.
- **ELT (Extract → Load → Transform)** — **원본 그대로** 먼저 적재하고, 필요할 때 웨어하우스 내부에서 SQL로
  변환한다. 철학은 "Load First, Think Later".

## 비교

| | ETL | ELT |
|---|---|---|
| 변환 위치 | 별도 ETL 서버 | DW 내부(In-DB Processing, SQL·dbt) |
| 적재 속도 | 느림 | 매우 빠름 |
| 보존 | 정제 데이터만 | 원본 + 정제 |
| 유연성·재현성 | 낮음 — 원본이 사라진다 | 높음 — 로직을 고쳐 과거 데이터로 재계산 |
| 병목 | ETL 서버(단일 장애 지점, 확장 한계) | DW의 연산 비용 |
| 강의의 비유 | 요리사(냄비에 넣기 전에 손질을 끝낸다) | 이사(박스째 옮기고 새 집에서 푼다) |

## 왜 ETL에서 ELT로 옮겨 갔나

[[AI DE 강의 1-07 배치 처리와 ETL·ELT]]의 서사는 **"무엇이 비싼가"의 역전**이다.

1. 20년 전에는 스토리지가 비쌌다 → 넣기 **전에** 줄이는 ETL이 생존 전략이었다.
2. 데이터가 늘자 ETL 서버가 병목이 됐다.
3. 클라우드 오브젝트 스토리지로 저장 비용이 급락하고, MPP 웨어하우스(Snowflake·BigQuery·Redshift)가 연산을
   수백 노드로 나눴다 → 일단 넣고 안에서 가공하는 ELT가 가능해졌다.

같은 전환이 저장소 쪽에서는 **schema-on-write → schema-on-read**로 나타난다
([[AI DE 강의 1-04 저장소의 진화 DW에서 Lakehouse까지]]).

## 언제 무엇을

- **ETL** — 금융·의료처럼 규제(GDPR·HIPAA·신용정보법)가 있는 곳. PII는 **적재 전에** 마스킹·암호화·토큰화해야
  한다. 최소 권한 원칙에 따라 불필요한 민감 정보는 들여오지 않는다.
- **ELT** — 스타트업·이커머스·게임처럼 민첩성이 중요한 곳. 구조가 자주 바뀌는 로그, "로그 하나도 버리지 마".

## 도구

Fivetran(관리형 EL) · Airbyte(오픈소스 통합) · dbt(SQL 변환) · Apache Airflow(오케스트레이션)

## 연결

- 비정형 데이터 파이프라인의 "처리" 단계(OCR·정제·PII 비식별화·임베딩)는 ETL의 Transform에 해당한다.
  → [[비정형 데이터 파이프라인]]
- ELT로 원본을 쌓으면 레이크에 PII가 그대로 들어간다. 이를 찾아 태깅하고 접근을 통제하는 일은
  [[데이터 거버넌스와 카탈로그]]로 넘어간다. *(위키의 연결)*
- Extract 단계의 "소스 시스템에 부하를 주지 말라"는 원칙의 고급 해법이 [[변경 데이터 캡처]]다.

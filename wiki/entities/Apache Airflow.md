---
type: entity
title: Apache Airflow
area: [data-engineering]
aliases: [Airflow, Airflow DAG, Directed Acyclic Graph, 오케스트레이터, orchestrator, 백필, backfill]
tags: [data-engineering, apache, airflow, orchestration, dag, scheduling, batch]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch7 Ingestion and orchestration]]"]
---

# Apache Airflow

**파이프라인을 DAG(방향 있는 비순환 그래프)로 정의하고 스케줄·의존·재시도를 맡는 오케스트레이터.**
데이터 오케스트레이션 생태계의 **사실상 표준**이다.

> **데이터를 옮기는 도구와, 그 작업을 "언제·어떤 순서로·실패 시 어떻게" 돌릴지는 다른 문제다.**

⭐ **Airflow는 무엇을 하는지 모른다.** 각 태스크가 무엇을 하는지는 Spark·dbt·NiFi·API 호출이 담당하고,
Airflow는 **순서를 맞추고 결과를 지켜본다.**

> *"'데이터를 어떻게 변환하나'보다 **'전체 파이프라인을 어떻게 신뢰성 있게 만드나'** 를 맡는 역할."*

## 구성 요소

| | |
|---|---|
| **DAG** | 태스크와 의존 관계를 그래프로 정의 (Python 코드) |
| **스케줄** | 주기·트리거로 실행 시점을 관리 |
| **재시도·알림** | 실패를 재시도·알림으로 **운영 가능하게** 처리 |
| **센서** | 외부 조건(파일 도착 등)이 충족될 때까지 대기 |
| **백필** | 과거 구간을 다시 실행 |
| **생태계** | 다양한 연산자·프로바이더로 외부 시스템 연결 |

전형적 워크로드: 수집 · 변환 · 적재 · **품질 검사** · 모델 학습처럼 단계가 많은 **배치** 작업.
[[Apache Map - Ch1 How to read this book]]의 레이크하우스 기본 스택에서 **"일정"** 칸이 이것이다.

## ⚠️ Airflow가 하지 않는 것

- **스트림 엔진을 대체하지 않는다.** 초저지연 이벤트 처리는 [[Apache Flink]]·[[Apache Kafka]] 경로가
  담당하고, Airflow는 **그 주변의 배치·점검·운영 작업을 묶는다.**
  → [[Batch and stream processing]]의 *오케스트레이터는 배치 전용* 이라는 경계
- **데이터를 옮기거나 가공하지 않는다.** *"오케스트레이터는 NiFi나 Spark를 대신하지 않는다."*
  → [[Data integration tools]]
- 실시간 경로는 **스케줄 없이** 스트림이 계속 돌고, 배치 경로만 DAG가 하루·한 시간 단위로 맞춘다.

## 고르는 축은 팀의 운영 방식이다

Airflow vs DolphinScheduler는 성능 비교가 아니다 → [[Data orchestration]]

| | 맞는 팀 |
|---|---|
| 🔹 **Airflow** | 엔지니어가 **Git으로 파이프라인을 관리**하고 로컬 테스트·CI가 중요하다. 코드 리뷰 중심 |
| 🔸 DolphinScheduler | 운영자·분석 엔지니어가 **UI에서 작업을 조립**하고 대량 스케줄 실행 화면이 중심 |

생태계·클라우드 관리형 옵션·커뮤니티 자료량은 **대체로 Airflow 쪽이 훨씬 넓다.**
⚠️ 이미 하나를 표준으로 쓰고 있다면 **특별한 이유 없이 둘을 병행하지 않는다.**

## 위키 안에서의 위치

- [[Data orchestration]] — 이 층 전체와 도구 선택 축.
- [[Batch and stream processing]] — 배치 전용이라는 경계.
- [[ETL and ELT]] · [[ML data pipeline]] — Airflow가 지휘하는 대상.
- [[Data SLA and observability]] — 재시도·알림·센서가 SLA를 지키는 장치다. ⚠️ 다만 **DAG 성공이
  데이터 건강을 증명하지 않는다**(그 페이지의 *침묵의 실패*).
- [[Apache Spark]] · [[Table formats]] — 태스크로 호출되는 쪽.

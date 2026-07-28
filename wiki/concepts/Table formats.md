---
type: concept
title: Table formats
area: [data-engineering]
aliases:
  - Table format
  - Apache Iceberg
  - Iceberg
  - Delta Lake
  - Apache Hudi
  - 테이블 포맷
  - 오픈 테이블 포맷
tags: [data-engineering, lakehouse, iceberg, delta-lake, hudi, acid, storage]
created: 2026-07-28
updated: 2026-07-28
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers"]
---

# Table formats

**쿼리 엔진과 raw 파일 사이에 앉아 데이터가 어떻게 저장되는지를 관리하는 층.**
[[Analytical data storage tiers|데이터 레이크]] 위에 이 층을 얹으면 레이크하우스가 된다 —
그래서 테이블 포맷은 레이크하우스를 정의하는 블록이다. 이 층이 있으면 저장소가 "파일 더미"에서
"관습적인 데이터베이스"에 한 걸음 가까워진다.

대표 3종: **Apache Iceberg** · **Delta Lake** · **Apache Hudi**.

## 이 층이 얹어주는 것

- **ACID** — 가장 두드러진 기능. 여러 애플리케이션이 같은 데이터를 동시에 다뤄도 깨지지 않는다.
  동시 쓰기 관리, 쓰기 도중 에러 처리를 테이블 포맷이 책임진다.
- **스키마 강제** — 레이크보다 엄격하다. 반정형(JSON 등)도 담을 수 있지만 **어떤 필드를 가져야
  하는지 정의해야 하고**, 레이크하우스가 그걸 강제한다.
- **스키마 진화(schema evolution)와 버저닝** — 스키마가 시간에 따라 바뀔 수 있고, 그 변경 이력을
  추적한다.
- **파티셔닝·인덱스 최적화** — 데이터와 스키마를 통제하니 인덱스를 만들고 파티셔닝을 조정해
  쿼리를 빠르게 할 수 있다.
- **time travel** (일부 구현) — 특정 시점의 스냅샷에 쿼리를 실행한다.

## 왜 이게 아키텍처를 바꾸는가

웨어하우스는 저장과 쿼리 엔진을 함께 관리하며 **강결합**이다. 테이블 포맷은 그렇지 않다 —
**쿼리 엔진을 특정 벤더에 묶지 않는다.** 결과적으로:

- 같은 데이터에 Spark·Trino·DuckDB 등 다른 엔진을 붙일 수 있다.
- **레이크하우스와 웨어하우스의 비용을 1:1로 비교할 수 없다.** 레이크하우스는 저장만 값을
  매기고 컴퓨트는 별도이기 때문. 워크로드에 따라 (레이크하우스 + 컴퓨트)가 웨어하우스보다
  크게 쌀 수 있다.

## 매니지드 제품

- **Google's Lakehouse for Apache Iceberg** (구 BigLake)
- **Databricks** — Delta Lake 기반
- **IBM watsonx.data** — Iceberg 기반

## 이 페이지가 아직 답하지 못하는 것

인제스트한 소스([[Data landscape guide for developers]])는 **세 포맷을 비교하지 않는다** —
이름만 나열하고 넘어간다. 그래서 아직 근거가 없는 것들:

- Iceberg vs Delta vs Hudi의 **선택 기준** (어느 것이 어떤 워크로드에 맞는지).
- 셋 중 **어느 것이 time travel을 지원하는지** — 원문은 "some lakehouses also support time travel"
  이라고만 쓴다.
- **스냅샷·매니페스트·트랜잭션 로그의 실제 온디스크 구조.**
  [[SpatialData as a data engineering substrate]]가 Iceberg를 카탈로그·gold 층으로 전제하고 설계를
  세우는데, 그 설계를 검증하려면 이 수준의 지식이 필요하다.

→ Iceberg 1차 문서(스펙·docs)를 인제스트하면 위 세 가지가 모두 풀린다. [[Data Engineering]] MOC의
열린 질문 참조.

## 링크

- 상위: [[Analytical data storage tiers]] — 레이크 위에 이 층을 얹은 것이 레이크하우스
- 혼동 주의: **테이블 포맷 ≠ 파일 포맷.** Parquet은 파일 하나의 레이아웃이고, 테이블 포맷은
  *여러 Parquet 파일을 하나의 테이블로 묶는 규약*이다 → [[Columnar and in-memory data formats]]
- 혼동 주의: **테이블 포맷 ≠ 카탈로그** → [[Data catalog and semantic layer]]
- 적용: [[SpatialData as a data engineering substrate]]
- 출처: [[Data landscape guide for developers]]

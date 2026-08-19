---
type: entity
title: Apache Polaris
area: [data-engineering]
aliases: [Polaris, Iceberg REST catalog, REST 카탈로그, 레이크 카탈로그, Apache Gravitino, Gravitino]
tags: [data-engineering, apache, catalog, iceberg, lakehouse, governance]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch10 Governance and BI]]"]
---

# Apache Polaris

**Iceberg 중심 데이터 레이크 카탈로그.** 여러 엔진이 같은 테이블 정의를 안전하게 공유하게 한다.

풀려는 문제가 정확하다 — **"Iceberg 테이블이 늘어나면 파일 경로만으로는 '어느 스냅샷이 공식
테이블인가'를 합의하기 어렵다."**

⭐ 이것이 [[Apache Map - Ch1 How to read this book]]에서 지적한 빈칸이다. 그 책의 "레이크하우스 기본
스택" 다섯 이름(Spark·Parquet·Iceberg·Airflow·Superset)에 카탈로그가 없었고, **Polaris가 그 자리다.**

## 하는 일

- Iceberg 테이블의 **메타데이터 · 네임스페이스 · 권한**을 관리한다.
- Spark·Trino·[[Apache Flink]] 같은 엔진이 **카탈로그 API**로 테이블을 찾고, 같은 정의와 권한
  기준으로 읽기·쓰기를 조율한다.
- ⭐ **"예전 Hive Metastore가 맡던 역할을 Iceberg REST 카탈로그 방식으로 이어가는 흐름."**
  → [[Data catalog and semantic layer]] §Hive가 남긴 질문

⚠️ **한계 — 모든 저장소·비Iceberg 자산의 만능 카탈로그가 아니다.** 더 넓은 통합은 **Gravitino**
쪽이다(아래).

## Polaris vs Gravitino — 같은 "카탈로그"의 다른 범위

| | 범위 |
|---|---|
| **Polaris** | **Iceberg 생태계에 맞춘 특화 카탈로그** |
| **Gravitino** | 파일·테이블·**모델** 등 여러 자산 유형, 여러 엔진·여러 카탈로그가 섞인 환경의 **통합** |
| Atlas | 설명·분류·계보 중심의 **전통 카탈로그**(사람용에 가깝다) |

⭐⭐ **"카탈로그도 단일 제품이 아니라 역할 구조로 설계된다."** 그래서 물어야 할 것은 제품 이름이 아니다 —
**"우리 테이블의 공식 정보가 어디에 등록되는가."**

⚠️ Gravitino는 **아직 모든 조직의 기본값이 된 제품이 아니다.** 기존 Metastore·Unity Catalog·Polaris와의
역할 경계와 **운영 성숙도**를 보고 검토한다.

⚠️ 이미 다른 카탈로그를 쓰고 있다면 **같은 테이블을 두 곳에 등록해 정보가 어긋나지 않도록 역할을
나눈다** — [[Data integration tools]]·[[Data orchestration]]에서 반복된 *경계를 문서에 고정하라* 와 같은 규칙.

## 실제 스택과의 관계

⭐ [[Spatial omics platform roadmap]] §2.2가 카탈로그 저장소를 Iceberg → **Postgres**로 정정했는데,
**Polaris는 그 결정을 뒤집지 않고 확인해 준다** — Polaris는 *Iceberg 테이블의* 카탈로그다. 공간 오믹스
산출물(SpatialData Zarr)은 쿼리 엔진이 읽는 Iceberg 테이블이 아니라 **불투명 blob**이므로 Polaris가
관리할 대상이 아니다.

> **판단 규칙: 관리 대상이 Iceberg 테이블이면 Polaris(또는 호환 REST 카탈로그), 불투명 산출물이면
> 카탈로그를 직접 만든다.** → [[Object storage layout]] · [[Table formats]]

## 위키 안에서의 위치

- [[Table formats]] — Polaris가 관리하는 대상. *"파일과 스냅샷"* 과 *"누가 테이블을 등록·공유하는가"* 는
  다른 문제다.
- [[SQL execution layer]] — 3단계 중 **1️⃣ 테이블 규칙**을 실제로 성립시키는 것.
- [[Data catalog and semantic layer]] — metastore(기계용) 칸의 현대 구현.
- ⭐ *"거버넌스는 정책뿐 아니라 **카탈로그 설계**이기도 하다."*

---
type: entity
title: Apache Sedona
area: [data-engineering, bioinformatics]
aliases: [Sedona, 지리공간 처리, geospatial, 공간 인덱스, spatial index, spatial join, 공간 조인]
tags: [data-engineering, apache, geospatial, spark, flink, spatial-join, bioinformatics]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch11 Specialized analytics and libraries]]"]
---

# Apache Sedona

**Spark·Flink 위에서 대용량 지리공간 데이터를 처리하는 엔진.**

> **"위치는 평범한 숫자 두 개가 아니다. 점·선·면의 거리, 포함, 교차 같은 **공간 관계**가 비즈니스
> 질문이 된다."**

- **공간 연산** — 거리·포함·교차 등 지리 관계를 계산한다.
- **공간 인덱스**를 활용해 *"이 영역 안의 이벤트"*, *"가장 가까운 매장"* 같은 질의를 **클러스터에서**
  실행한다.
- **분산 처리** — 수십억 건의 좌표·폴리곤을 [[Apache Spark]]·[[Apache Flink]] 규모로 조인·집계한다.
- **레이크 연동** — 결과를 다시 레이크 테이블이나 지도 시각화로 내보낸다.

⭐ 갈리는 축이 명확하다 — **"기존 GIS 도구가 단일 머신·중규모에 강하다면, Sedona는 레이크·스트림 규모의
공간 ETL·분석에 맞춰져 있다."**

⚠️ **한계 두 가지가 명시된다** — 완성형 지도 서비스·내비게이션 엔진이 아니고,
**"단순 위경도 필터만 필요하면 일반 SQL로도 충분한 경우가 많다."**
전형적 도입 영역: 물류 · 도시 데이터 · 이동통신 · 리테일 입지.

## ⭐⭐ 공간 오믹스에서의 자리 — [[Spatial aggregation]]의 제약과 정확히 맞물린다

[[Spatial aggregation]]이 기록한 제약이 이것이다.

> ⚠️ **"points → shapes 집계는 모든 점을 메모리에 올린다.** docstring이 직접 경고하며
> [issue #210](https://github.com/scverse/spatialdata/issues/210)을 가리킨다. **전사체 단분자
> 규모에서는 실질적인 제약이다."**

⭐ **그 연산의 정체가 point-in-polygon 공간 조인이고, Sedona가 하는 일이 정확히 그것이다** —
공간 인덱스를 써서 클러스터에 분산한다. [[Xenium]]·[[MERSCOPE]]의 단분자 좌표를
[[SpatialData Shapes element]]의 세포 폴리곤에 붙이는 작업이 [[SpatialData elements]] 안에서는
단일 프로세스 메모리에 묶여 있다.

⚠️ **다만 직접 연결되지는 않는다** — Sedona는 Spark/Flink DataFrame의 geometry 타입을 다루고,
[[SpatialData]] store는 쿼리 엔진이 읽지 못하는 **불투명 blob**이다([[Object storage layout]]).
그래서 경로는 이렇게 된다(⚠️ **미검증 설계 — 실제로 해 본 것이 아니다**):

1. points를 **(Geo)Parquet으로 내보낸다** → [[Columnar and in-memory data formats]]
2. shapes 폴리곤도 같은 방식으로 내보낸다
3. Sedona로 **분산 공간 조인**
4. 결과 cell × gene 표를 Table로 되돌린다 → [[SpatialData elements]]

⭐ 즉 **[[Spatial aggregation]]을 대체하는 게 아니라, 그 함수가 못 버티는 규모에서 우회하는 경로**다.
판단 기준은 소스가 준 것과 같다 — **한 store가 단일 머신에서 처리되면 그대로 두고, 레이크 규모
(플랫폼 전체·다수 슬라이드 배치)가 되면 검토한다.**
→ [[SpatialData as a data engineering substrate]] · [[Spatial omics platform roadmap]]

## 그래프와의 대비

> *"그래프가 개체 간 **연결**을 다룬다면, Sedona는 **위치 기반 공간 관계**를 다룬다."*

[[Graph database]]가 *"관계를 계산하느냐 저장하느냐"* 로 RDB와 갈렸던 것처럼, 공간도 같은 형태의
문제다 — **공간 관계를 매번 계산하느냐(일반 SQL의 위경도 연산), 인덱스로 미리 조직하느냐(Sedona).**

## 위키 안에서의 위치

- [[Spatial aggregation]] · [[Spatial queries in SpatialData]] — 같은 연산의 단일 머신 버전.
- [[SpatialData as a data engineering substrate]] — 이 위키에서 공간 데이터를 DE 관점으로 읽는 노트.
- [[Apache Spark]] · [[Apache Flink]] — 올라가는 엔진.
- [[Consumption layer]] — 공간 질의도 조회 형태 하나다(표에는 없는 일곱 번째 칸).

---
type: entity
title: Apache Sedona
area: [data-engineering, bioinformatics]
aliases: [Sedona, 지리공간 처리, geospatial, 공간 인덱스, spatial index, spatial join, 공간 조인, SedonaSpark, SedonaFlink, SedonaSnow]
tags: [data-engineering, apache, geospatial, spark, flink, spatial-join, bioinformatics]
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[Apache Map - Ch11 Specialized analytics and libraries]]"
  - "[[Apache Sedona docs - Spatial join execution]]"
  - "[[Apache Sedona docs - Storage and formats]]"
  - "[[Apache Sedona docs - Runtimes and GeoStats]]"
  - "docs/experiments/spatialdata-sedona/ (자체 실측, 2026-08-19)"
---

# Apache Sedona

**공간 데이터를 1급 시민으로 다루는 엔진 계열.** 최신 릴리스 **1.9.1** (2026-08-05).

> **"위치는 평범한 숫자 두 개가 아니다. 점·선·면의 거리, 포함, 교차 같은 **공간 관계**가 비즈니스
> 질문이 된다."**

- **공간 연산** — 거리·포함·교차 등 지리 관계를 계산한다.
- **공간 인덱스**를 활용해 *"이 영역 안의 이벤트"*, *"가장 가까운 매장"* 같은 질의를 실행한다.
  실행 구조는 [[Spatial join execution]].
- **분산 처리** — 수십억 건의 좌표·폴리곤을 [[Apache Spark]]·[[Apache Flink]] 규모로 조인·집계한다.
- **레이크 연동** — 결과를 다시 레이크 테이블이나 지도 시각화로 내보낸다.

## 런타임 4종 — "Spark·Flink 위"는 이제 부분집합이다

| 런타임 | 실체 | 자리 |
|---|---|---|
| **SedonaSpark** | Spark 3.4 / 3.5 / 4.0 / 4.1 확장 | 대용량 배치 |
| **SedonaFlink** | Flink 1.19 Table API / SQL | 스트림, 저지연 |
| **SedonaSnow** | Snowflake 7+ 네이티브 | 창고 안에서 |
| **[[SedonaDB]]** | Rust + [[Columnar and in-memory data formats\|Arrow]] + [[Apache DataFusion]], **단일 노드** | 클러스터 없이 |

> 🔄 **정정 (2026-08-19, 공식 문서 인제스트).** 이 페이지의 초판은 책에서 옮긴 갈림축
> — *"기존 GIS 도구가 단일 머신·중규모에 강하다면, Sedona는 레이크·스트림 규모의 공간 ETL·분석"* —
> 을 적었다. **[[SedonaDB]]가 그 축을 무효화한다.** Sedona가 단일 머신 자리를 직접 차지했으므로,
> 선택은 "GIS 도구 vs Sedona"가 아니라 **"어느 Sedona 런타임인가"** 다. Flink 문서가 직접 적는다 —
> *"For small datasets, you may not need a distributed cluster and can use SedonaDB."*

⚠️ **책이 준 한계 두 가지는 유효하다** — 완성형 지도 서비스·내비게이션 엔진이 아니고,
**"단순 위경도 필터만 필요하면 일반 SQL로도 충분한 경우가 많다."**
전형적 도입 영역: 물류 · 도시 데이터 · 이동통신 · 리테일 입지.

## 실행 구조 — 격자 ≠ 인덱스 ≠ refine

책이 주지 않은 층이고 공식 문서가 채운다. 상세는 [[Spatial join execution]] ·
[[Apache Sedona docs - Spatial join execution]].

- **격자**(`sedona.join.gridtype`, 기본 `kdbtree`) — 무엇이 같은 파티션에 가는가. 파티셔닝은
  **객체를 복제한다**
- **인덱스**(`sedona.global.indextype`, 기본 `rtree`) — 파티션 안에서 MBR로 후보를 좁힌다
- **refine** — 살아남은 쌍만 JTS로 실제 술어를 계산한다
- 물리 연산자 3종: `RangeJoin`/`DistanceJoin` · `BroadcastIndexJoin`(셔플 없음) ·
  `BroadcastNestedLoopJoin`(최악)

⚠️ **함정 셋**: `LEFT JOIN`은 최적화되지 않는다(inner join으로 우회) · 거리 단위는 좌표계 단위다 ·
KNN 조인은 필터 위치가 질문을 바꾼다(`barrier()`).

## 저장 층이 성능을 만든다

- GeoParquet **bbox 메타데이터로 파일 스킵**. 살리는 조건은 **쓰기 시점의 공간 정렬**
  (`ORDER BY ST_GeoHash(geom, 5)`)
- covering 컬럼(GeoParquet 1.1) 자동 생성 · **Box2D row-group pushdown**(1.9.1)
- ⚠️ 문서가 스스로 vanilla GeoParquet의 한계(트랜잭션·DML·동시성)를 인정하고 **Iceberg v3**를 권한다
  → [[Table formats]], [[Apache Sedona docs - Storage and formats]]

## 벡터 밖의 층 — GeoStats

**DBSCAN · Local Outlier Factor · Getis-Ord Gi/Gi\* · Moran's I · 거리 가중 행렬.**
공간 오믹스 분석의 표준 통계와 같은 계열이다 →
[[SpatialData and Sedona interop]] §GeoStats.

## ⭐⭐ 공간 오믹스에서의 자리 — [[Spatial aggregation]]의 제약과 정확히 맞물린다

[[Spatial aggregation]]이 기록한 제약이 이것이다.

> ⚠️ **"points → shapes 집계는 모든 점을 메모리에 올린다.** docstring이 직접 경고하며
> [issue #210](https://github.com/scverse/spatialdata/issues/210)을 가리킨다. **전사체 단분자
> 규모에서는 실질적인 제약이다."**

⭐ **그 연산의 정체가 point-in-polygon 공간 조인이고, Sedona가 하는 일이 정확히 그것이다.**
[[Xenium]]·[[MERSCOPE]]의 단분자 좌표를 [[SpatialData Shapes element]]의 세포 폴리곤에 붙이는
작업이 [[SpatialData elements]] 안에서는 단일 프로세스 메모리에 묶여 있다.

> 🔄 **정정 (2026-08-19).** 이 페이지의 초판은 *"[[SpatialData]] store는 쿼리 엔진이 읽지 못하는
> **불투명 blob**이다"* 라고 적고 (Geo)Parquet 내보내기를 포함한 **미검증 4단계 경로**를 제시했다.
> **그 전제가 틀렸다** — SpatialData는 points와 shapes를 **이미 Parquet/GeoParquet으로 쓴다.**
> 내보내기 단계가 애초에 없고, 리더 소스 확인 결과 **좌표변환 이음새도 이 연산에서는 문제가 되지
> 않는다.** 경로·근거·남은 미검증 목록은 전부 **[[SpatialData and Sedona interop]]** 으로 옮겼다.
> (초판이 인용한 [[SpatialData as a data engineering substrate]] §2는 처음부터 정확히
> *"DuckDB/Trino가 `shapes.parquet`·`points/*.parquet`는 읽는다"* 고 적어 뒀다 — 그 노트를
> 참조하지 않고 쓴 것이 원인이다.)

판단 기준도 갱신됐다 — **문턱이 "레이크 규모"에서 "issue #210이 터지는 순간"으로 내려왔다.**
[[SedonaDB]]는 클러스터가 아니라 `pip install`이기 때문이다.

✅ **실행해서 확인했다 (2026-08-19)** — SedonaDB의 조인 결과가 `aggregate()`와 **비트 단위로 같고**,
50M transcript에서 **48배 빠르다**(94.1s → 1.97s, peak RSS 10.6GB → 1.4GB).
⚠️ 대가는 함정 둘 — `crs: null`로 인한 **CRS 불일치 조인 거부**, dictionary 컬럼 **GROUP BY 파괴**.
→ [[SpatialData and Sedona interop]] §3·§7 · `docs/experiments/spatialdata-sedona/` ·
[[SpatialData as a data engineering substrate]] · [[Spatial omics platform roadmap]]

## 그래프와의 대비

> *"그래프가 개체 간 **연결**을 다룬다면, Sedona는 **위치 기반 공간 관계**를 다룬다."*

[[Graph database]]가 *"관계를 계산하느냐 저장하느냐"* 로 RDB와 갈렸던 것처럼, 공간도 같은 형태의
문제다 — **공간 관계를 매번 계산하느냐(일반 SQL의 위경도 연산), 인덱스로 미리 조직하느냐(Sedona).**

## 위키 안에서의 위치

- [[SpatialData and Sedona interop]] — ⭐ **이 엔티티가 공간 오믹스에 닿는 지점 전체.**
- [[Spatial join execution]] — 실행 구조(격자·인덱스·refine)를 엔진 중립으로 정리한 개념 페이지.
- [[Spatial aggregation]] · [[Spatial queries in SpatialData]] — 같은 연산의 단일 머신 버전.
- [[SpatialData as a data engineering substrate]] — 이 위키에서 공간 데이터를 DE 관점으로 읽는 노트.
- [[SedonaDB]] — 단일 노드 런타임. 별도 repo·별도 버전 체계.
- [[Apache Spark]] · [[Apache Flink]] · [[Apache DataFusion]] — 올라가는 엔진들.
- [[Consumption layer]] — 공간 질의도 조회 형태 하나다(표에는 없는 일곱 번째 칸). S2 근사 조인은
  그 페이지의 **오차 다이얼**과 같은 형태다.
- 소스: [[Apache Map - Ch11 Specialized analytics and libraries]](배치) ·
  [[Apache Sedona docs - Spatial join execution]] · [[Apache Sedona docs - Storage and formats]] ·
  [[Apache Sedona docs - Runtimes and GeoStats]](구조)

---
type: source
title: Apache Sedona docs - Storage and formats
area: [data-engineering]
aliases:
  - Sedona GeoParquet
  - Sedona 저장 포맷 문서
  - GeoParquet covering
  - Box2D pushdown
tags: [data-engineering, apache, sedona, geoparquet, parquet, iceberg, predicate-pushdown, geospatial]
created: 2026-08-19
updated: 2026-08-19
sources:
  - "https://sedona.apache.org/latest/tutorial/files/geoparquet-sedona-spark/"
  - "https://sedona.apache.org/latest/api/sql/Optimizer/"
  - "https://sedona.apache.org/latest/blog/2025/09/09/spatial-tables-lakehouse/"
---

# Apache Sedona docs - Storage and formats

## 인용

| 항목 | 값 |
|---|---|
| 출처 | Apache Sedona 공식 문서 + 공식 블로그 |
| 페이지 | `tutorial/files/geoparquet-sedona-spark.md` (370줄) · `api/sql/Optimizer.md` 의 pushdown 3절 · `blog/posts/spatial-tables-lakehouse.md` (§Iceberg v3 spec) |
| 버전 핀 | tag `sedona-1.9.1` (2026-08-05 릴리스) |
| 라이선스 | Apache-2.0 |
| 접근일 | 2026-08-19 |
| 표준 URL | https://sedona.apache.org/latest/tutorial/files/geoparquet-sedona-spark/ |
| 스냅샷 | `raw/data-engineering/apache-sedona-docs/` |

## 요약

[[Apache Sedona]]의 **성능은 조인 알고리즘이 아니라 저장 레이아웃에서 상당 부분 결정된다.**
이 문서 묶음은 그 층 — GeoParquet의 bbox 메타데이터, covering 컬럼, Box2D row-group pushdown —
과 **문서가 스스로 GeoParquet을 버리라고 권하는 대목**(Iceberg v3)을 담는다.

## 핵심 takeaway

### 1. 파일 스킵 — bbox 메타데이터가 하는 일

GeoParquet 파일마다 geometry 컬럼의 bbox가 메타데이터에 있다. 공간 술어가 그 bbox와 겹치지
않으면 **파일을 통째로 읽지 않는다**.

문서 예시에서 3개 파일 중 1개만 스캔한다:

```
|{geometry -> {WKB, [Point], [2.0, 1.0, 3.0, 3.0], null, NULL}}|
|{geometry -> {WKB, [Point], [7.0, 1.0, 8.0, 2.0], null, NULL}}|
|{geometry -> {WKB, [Point], [5.0, 4.0, 6.0, 5.0], null, NULL}}|   ← 질의 창이 여기만 걸린다
```

Optimizer 문서는 6개 중 1개 스캔 그림을 든다. 기본 활성이고
`spark.sedona.geoparquet.spatialFilterPushDown = false`로 끈다.

### 2. ⭐ 이 최적화를 살리는 것은 **쓰기 시점의 정렬**이다

> To maximize the performance of Sedona GeoParquet filter pushdown, we suggest that you
> **sort the data by their geohash values** and then save as a GeoParquet file.

```sql
SELECT col1, col2, geom, ST_GeoHash(geom, 5) AS geohash
FROM spatialDf
ORDER BY geohash
```

공간적으로 가까운 행이 같은 파일에 모이면 파일별 bbox가 좁아지고, 좁은 bbox만이 프루닝을
만든다. **정렬하지 않은 GeoParquet은 파일마다 bbox가 전체 범위에 가까워 프루닝이 사실상 0이다.**

⭐ 이건 [[Object storage layout]]이 세운 규칙(*"경로는 권한과 생애주기만 답한다"*)의 짝이다 —
공간 프루닝은 경로가 아니라 **파일 내부 정렬**로 만든다. Hive 파티셔닝의 자리가 아니다.

⚠️ `ST_GeoHash`는 경위도를 전제한다. 임의 평면 좌표계에서는 다른 정렬 키가 필요하다(미확인).

### 3. covering 컬럼 — bbox를 메타데이터에서 컬럼으로 끌어내린다

GeoParquet 1.1의 `covering` 필드. `xmin`/`ymin`/`xmax`/`ymax`를 담은 **top-level struct 컬럼**을
가리켜 검색을 가속한다. v1.6.1부터 쓰기 지원, **v1.9.0부터 기본 자동 생성**:

- `<geometryColumnName>_bbox`가 이미 있고 유효하면 재사용
- 없으면 쓰기 시점에 생성
- `geoparquet.covering.mode`: `auto`(기본) / `legacy`(비활성)
- 명시 옵션 `geoparquet.covering.<geomCol>`이 우선

수동으로 만들려면:

```scala
val df_bbox = df.withColumn("bbox", expr(
  "struct(ST_XMin(geometry) AS xmin, ST_YMin(geometry) AS ymin, " +
  "ST_XMax(geometry) AS xmax, ST_YMax(geometry) AS ymax)"))
```

### 4. ⭐ Box2D pushdown — 파일 단위에서 row group 단위로 (1.9.1 신규)

`Box2D` 타입 컬럼에 `ST_Intersects`/`ST_Contains`를 걸면 Sedona가 술어를 **네 leaf 컬럼의 부등식
연립으로 번역**해 `ParquetInputFormat.setFilterPredicate`로 내려보낸다. Parquet의 row-group
통계가 그 부등식으로 row group을 건너뛴다 — **파일 메타데이터 스캔조차 필요 없다.**

| 술어 | 내려가는 연립 |
|---|---|
| `ST_Intersects(box_col, lit)` | `box.xmax >= lit.xmin AND box.xmin <= lit.xmax AND box.ymax >= lit.ymin AND box.ymin <= lit.ymax` |
| `ST_Contains(box_col, lit)` | `box.xmin <= lit.xmin AND box.xmax >= lit.xmax AND …` |
| `ST_Contains(lit, box_col)` | 부등호 방향이 뒤집힌 형태 |

⚠️ **함정이 명시돼 있다** — 자동 생성되는 `<geom>_bbox`는 평범한 `struct<xmin,…>`이고
**`Box2D`가 아니다.** GeoParquet 1.1 covering 계약은 만족하지만 Box2D pushdown의 대상이 되지
않는다. row-group 프루닝을 원하면 `ST_Box2D(geom)`으로 **명시적으로** 컬럼을 써야 한다.

게이트가 둘이다: `spark.sedona.geoparquet.spatialFilterPushDown`(Sedona 마스터 토글) **AND**
`spark.sql.parquet.filterPushdown`(Spark). 둘 중 하나만 꺼도 죽는다.

⚠️ 뒤집힌 경계(`xmin > xmax`)는 pushdown하지 않고 행별 평가로 떨어뜨린다 — 스칼라 계약과 같은
`IllegalArgumentException`을 사용자가 보게 하려고 일부러 그렇게 한다.

### 5. Box2D 조인은 기하 조인과 같은 연산자를 탄다

두 `Box2D` 컬럼 사이의 `ST_Intersects`/`ST_Contains`는 `Geometry` 짝과 **동일한 물리 연산자**로
간다. 실행기 경계에서 각 Box2D 행을 사각 폴리곤으로 물질화하고, 그 뒤 *"the partitioner, R-tree
index, and refine evaluator run unchanged"*. JTS가 축 정렬 사각형 술어를 `RectangleIntersects`/
`RectangleContains`로 단축하므로 refine 비용은 double 4개 비교뿐이다.

⚠️ 의미론 주의 — Box2D 간 `ST_Contains`는 조인 층에서 **`COVERS` 의미**를 쓴다. JTS `contains`는
strict interior라 변을 공유하는 쌍을 거부하기 때문이다.

### 6. ⚠️ 문서가 스스로 GeoParquet을 버리라고 권한다

**장점** (행 지향 대비): 컬럼 프루닝 · row group 필터링 · footer 스키마 · 압축률.

**한계** — 그대로 옮긴다:

> * They don't support reliable transactions
> * Some DML operations (e.g., update, delete) are not supported
> * No concurrency protection
> * Poor performance compared to databases for certain operations

결론부의 처방:

> Iceberg provides many useful open table features and is **almost always a better option than
> vanilla GeoParquet** (except for single file datasets that will never change or for compatibility
> with other engines).

⭐ 이건 [[Table formats]]가 세운 층위 논리(*파일 포맷 ≠ 테이블 포맷*)를 공간 데이터에서 그대로
반복한다. 그리고 **[[SpatialData as a data engineering substrate]]의 §2 "트랜잭션 로그 없음"과
정확히 같은 진단이다** — SpatialData의 `shapes.parquet`도 vanilla GeoParquet이다.

### 7. Iceberg v3의 geometry / geography 컬럼

블로그가 [iceberg PR #10981](https://github.com/apache/iceberg/pull/10981)을 가리키며 v3 스펙이
컬럼당 저장하는 것 둘을 적는다:

- **CRS** (미지정이면 `OGC:CRS84`)
- **bounding box (bbox)**

스펙 인용:

> Geospatial features from OGC – Simple feature access. **Edge-interpolation is always
> linear/planar.** See Appendix G. Parameterized by CRS C.

⭐ 즉 Iceberg는 GeoParquet이 파일 메타데이터로 갖던 bbox를 **테이블 통계로 승격**시킨다.
프루닝이 파일 목록 스캔이 아니라 매니페스트 층에서 일어난다는 뜻이다(⚠️ 추론 — 매니페스트
구조는 이 블로그가 다루지 않는다. [[Table formats]]가 남긴 *"Iceberg 1차 문서 필요"* 는 유효).

## 발췌 (원문)

```
Spatial predicate push-down to GeoParquet is enabled by default. Users can manually disable it by
setting the Spark configuration `spark.sedona.geoparquet.spatialFilterPushDown` to `false`.
```

```
Sedona's auto-generated `<geom>_bbox` covering column is written as a plain
`struct<xmin, ymin, xmax, ymax>` — it satisfies the GeoParquet 1.1 covering-bbox contract but is
**not a `Box2D`**, so the Box2D pushdown does not target it directly.
```

## 기존 페이지와의 관계

- **확장** — [[Table formats]]에 Iceberg v3 geometry/geography 컬럼 항목이 없었다.
- **확장** — [[Columnar and in-memory data formats]]가 세운 Parquet 프루닝(row group 통계) 논리가
  공간 술어까지 이어지는 실례.
- **확장** — [[Object storage layout]]의 *"경로로 찾으려 하지 말라"* 에 짝이 되는 처방
  (프루닝은 파일 내부 정렬로 만든다).
- ⭐ **직접 응용** — [[SpatialData and Sedona interop]]: SpatialData의 `shapes.parquet`이
  **정렬도 covering 컬럼도 없는 단일 GeoParquet**이라는 사실이 여기서 의미를 갖는다.

## 링크

- 자매 소스: [[Apache Sedona docs - Spatial join execution]],
  [[Apache Sedona docs - Runtimes and GeoStats]]
- 엔티티: [[Apache Sedona]], [[SedonaDB]]
- DE 개념: [[Table formats]], [[Columnar and in-memory data formats]], [[Object storage layout]],
  [[Analytical data storage tiers]]
- 응용: [[SpatialData and Sedona interop]]
- 영역 MOC: [[Data Engineering]]

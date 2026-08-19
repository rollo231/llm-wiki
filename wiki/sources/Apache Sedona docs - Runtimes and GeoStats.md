---
type: source
title: Apache Sedona docs - Runtimes and GeoStats
area: [data-engineering, bioinformatics]
aliases:
  - SedonaDB 문서
  - Sedona 런타임
  - Sedona GeoStats
  - sedonadb-zarr
tags: [data-engineering, apache, sedona, sedonadb, geostats, geopandas, rust, datafusion, gpu, zarr]
created: 2026-08-19
updated: 2026-08-19
sources:
  - "https://sedona.apache.org/latest/sedonaspark/"
  - "https://sedona.apache.org/latest/sedonaflink/"
  - "https://sedona.apache.org/latest/setup/modules/"
  - "https://sedona.apache.org/latest/api/stats/sql/"
  - "https://sedona.apache.org/latest/tutorial/geopandas-api/"
  - "https://sedona.apache.org/latest/community/geopandas/"
  - "https://sedona.apache.org/latest/blog/"
  - "https://sedona.apache.org/sedonadb/"
---

# Apache Sedona docs - Runtimes and GeoStats

## 인용

| 항목 | 값 |
|---|---|
| 출처 | Apache Sedona 공식 문서 + 공식 블로그 |
| 페이지 | `sedonaspark.md` · `sedonaflink.md` · `setup/modules.md` · `api/stats/sql.md` · `tutorial/geopandas-api.md` · `community/geopandas.md` · `setup/release-notes.md` · `blog/posts/intro-sedonadb.md` · `blog/posts/intro-sedonadb-0-4.md` · `blog/posts/raybooster-gpu-spatial-join.md` |
| 버전 핀 | tag `sedona-1.9.1` (2026-08-05 릴리스). SedonaDB는 별도 repo `apache/sedona-db`, 최신 태그 `apache-sedona-db-0.4.0` |
| 라이선스 | Apache-2.0 |
| 접근일 | 2026-08-19 |
| 표준 URL | https://sedona.apache.org/latest/ · https://sedona.apache.org/sedonadb/ |
| 스냅샷 | `raw/data-engineering/apache-sedona-docs/` |

## 요약

**"Sedona = Spark·Flink 위의 공간 엔진"이라는 정의가 낡았다는 것**이 이 묶음의 결론이다.
런타임이 넷이고, 그중 [[SedonaDB]]는 **클러스터를 요구하지 않는 Rust 단일 노드 엔진**이다.
그리고 문서에는 벡터 연산 밖의 층이 하나 더 있다 — **GeoStats**(DBSCAN·LOF·Getis-Ord·Moran's I).

## 핵심 takeaway

### 1. 런타임 4종

| 런타임 | 실체 | 자리 |
|---|---|---|
| **SedonaSpark** | Spark 3.4 / 3.5 / 4.0 / 4.1 확장 | 대용량 배치 |
| **SedonaFlink** | Flink 1.19 Table API / SQL | 스트림, 저지연 |
| **SedonaSnow** | Snowflake 7+ 네이티브 | 창고 안에서 |
| **[[SedonaDB]]** | Rust + [[Apache Arrow]] + [[Apache DataFusion]], 단일 노드 | 클러스터 없이 |

Java 요구사항이 Spark 버전에 묶인다 — Spark 3.4/3.5는 Java 11, **Spark 4.0/4.1은 Java 17**.
1.7.2가 *"the last release on Java 8"* 이었다.

SedonaFlink 문서가 자기 자리를 직접 정리한다:

> For **small datasets**, you may not need a distributed cluster and can use **SedonaDB**.
> For **large batch pipelines**, you can use **SedonaSpark**.

Spark Structured Streaming과의 대비도 명시적이다 — *"Spark Streaming uses micro-batches, whereas
Flink processes events one at a time"*, 그리고 *"Use Spark if you're already invested in the Spark
ecosystem and the Spark Structured Streaming latency is sufficiently low"*. ⭐ 도입 근거를 성능이
아니라 **이미 무엇에 투자했는가**로 놓는다.

언어·API 가용성 행렬(Spark):

| | Core/RDD | DataFrame/SQL | Viz RDD/SQL |
|---|:---:|:---:|:---:|
| Scala/Java | ✅ | ✅ | ✅ |
| Python | ✅ | ✅ | SQL only |
| R | ✅ | ✅ | ✅ |

### 2. ⭐⭐ SedonaDB — 단일 노드가 1급 시민이 됐다

> SedonaDB is the **first open-source, single-node analytical database engine that treats spatial
> data as a first-class citizen.** […] Written in Rust, SedonaDB is lightweight, blazing fast, and
> spatial-native.

```python
# pip install "apache-sedona[db]"   또는   conda install -c conda-forge sedonadb
import sedona.db
sd = sedona.db.connect()
sd.sql("SELECT … FROM cities JOIN countries WHERE ST_Intersects(…)").show()
```

- [[Apache DataFusion]] 기반 벡터화 엔진, GeoArrow·GeoParquet·GeoPandas와 직접 물린다
- SQL + Python + R(dplyr) + Rust API. 0.4.0에서 **Python DataFrame API** 추가
  (Ibis·DuckDB relational API·PySpark·DataFusion Python에서 착안했다고 명시)
- 조인 전략을 **런타임에 입력 샘플로 결정**한다 — *"leveraging spatial indices where beneficial
  and dynamically adapting join strategies at runtime using input data samples"*
- ⚠️ 초기 릴리스는 벡터 전용이었고 래스터는 "future versions". 0.4.0에서 래스터가 들어왔다.

**SpatialBench 자체 벤치마크의 결론**(SF1·SF10, Q1–12):

> SedonaDB demonstrates **balanced performance** across all query types […] **DuckDB excels at
> spatial filters and some geometric operations but faces challenges with complex joins and KNN
> queries.** GeoPandas […] requires manual optimization and parallelization to handle larger
> datasets.

⚠️ 자기 제품 벤치마크다. 다만 **경쟁 제품의 강점을 명시**하는 형태라,
[[AI Data Engineering (Fast Campus course)]]류의 출처 없는 수치와는 성격이 다르다.
수치는 인용하지 않고 축만 옮겼다.

### 3. ⭐⭐⭐ `sedonadb-zarr` — 쿼리 엔진이 Zarr를 읽는다 (0.4.0)

이 위키에서 가장 큰 함의를 갖는 항목이다.

> In 0.4.0, SedonaDB's raster type goes natively **N-dimensional**, and the new **`sedonadb-zarr`
> extension reads Zarr groups straight into a queryable raster column.**

```python
# pip install sedonadb-zarr
import sedonadb_zarr
sd.register(sedonadb_zarr.ZarrExtension())

spec = sedonadb_zarr.Zarr().with_options({"arrays": ["rain_ok"]})
cube = sd.read(url, format=spec)
cube.select(
    cube.raster.rst.num_dimensions().alias("ndim"),
    cube.raster.rst.dim_names().alias("dims"),      # → [year, y, x]
    cube.raster.rst.shape().alias("shape"),         # → [1, 128, 128]
    cube.raster.rst.srid().alias("srid"),
).show(1)
```

설계가 명확하다:

> `sedonadb-zarr` emits **one row per Zarr chunk**, so the storage layout *is* the data layout.
> SedonaDB stays **lazy about pixels**: reading the group and inspecting its dimensions […] touches
> only the group schema, which is a small metadata round-trip, **with no pixel bytes fetched.**

- `RS_DimNames`·`RS_Shape`·`RS_DimSize`·`RS_NumDimensions` — 메타데이터만 건드린다
- `RS_Slice` — 질의가 닿는 청크만 해석해서 자른다
- `RS_Envelope` — **청크 하나를 그 경계 기하로 바꾼다.** 픽셀을 디코딩하지 않고 청크 격자를
  지도에 그릴 수 있다
- `.show(5)`는 정확히 5개 청크만 건드린다

⭐ **청크 = 행**이라는 매핑이 요점이다. 이건 [[Object storage layout]]의 ⑤*"한 prefix 아래 객체가
수백만 개"* 문제를 **테이블로 다시 정의한 것**이다 — 청크 목록이 `list-objects`가 아니라 스캔 가능한
관계가 된다.

⚠️ **미확인 (중요)**: 예시는 CRS(EPSG:3857)를 가진 지리 datacube다. [[OME-NGFF]]/[[SpatialData]]의
래스터는 CRS가 없고 축이 `c,y,x`(마이크론·픽셀)이며 multiscale 피라미드 그룹 구조를 갖는다.
`sedonadb-zarr`가 그 레이아웃을 읽는지는 **전혀 확인되지 않았다.** 상세는
[[SpatialData and Sedona interop]] §래스터.

### 4. GPU 공간 조인 — RayBooster (VLDB 2026)

> Gaming GPUs contain dedicated **ray tracing cores** designed for video game lighting — and they
> **sit idle during database queries.** Spatial joins are about finding intersecting geometries,
> which maps naturally onto ray tracing primitives.

구성 4요소:

1. **GPU 친화 저장 레이아웃** — WKB(스트림 지향) 대신 Structure of Arrays로 offsets·vertices·types를
   분리 → 임의 기하에 O(1) 접근
2. **단일 거대 인덱스** — 수백만 개의 작은 트리 대신 *Z-stacking*: 기하 ID를 ray tracing scene의
   미사용 Z축에 인코딩하고 배치 전체에 **BVH 하나**를 만든다
3. **범용 술어 엔진** — `RelateEngine`이 RT 코어에서 **DE-9IM 행렬**을 계산한다.
   *"one code path that resolves any geometry/predicate combination instead of hardcoding 500+
   kernel variants"*
4. **메모리 인식 실행** — 스케줄링·스필 층으로 GPU 메모리 예산 안에 조인을 묶는다

활성화는 `ctx.sql("SET gpu.enable = true")` 한 줄. ⚠️ 성능 수치는 자체 SpatialBench 측정이라
옮기지 않는다. 다만 하나는 축으로 의미가 있다 — **RT 코어가 없는 H100보다 소비자용 RTX 3090이
일부 질의에서 빨랐다**고 명시한다. [[GPU architecture]]의 *"연산 유닛이 문제 형태에 맞는지"* 축에
걸리는 사례다.

### 5. ⭐⭐ GeoStats — 벡터 연산 밖의 층

`api/stats/sql.md`. Scala/Java와 Python 양쪽 제공.

| 함수 | 위치(python) | 파라미터 |
|---|---|---|
| **DBSCAN** | `sedona.stats.clustering.dbscan.dbscan` | `epsilon`, `min_pts`, `geometry`, `include_outliers`, `use_spheroid` |
| **Local Outlier Factor** | `sedona.stats.outlier_detection.local_outlier_factor` | — |
| **Getis-Ord Gi / Gi\*** | `sedona.stats.hotspot_detection.getis_ord.g_local` | `x`, `weights`, `star` |
| **Moran's I** | (stats 모듈) | 1.9.1에서 정수 값 지원 추가 |
| **거리 가중 행렬** | `sedona.stats.weighting.add_distance_band_column` | `threshold`, `binary`, `alpha`, `include_self`, `self_weight`, `use_spheroid` |

공통 계약: **geometry 컬럼이 하나 이상 있어야 하고 행이 유일해야 한다.** 둘이면 `'geometry'`라는
이름의 컬럼이 쓰이고, 셋 이상이면 이름을 명시해야 한다. DBSCAN은 `cluster` 컬럼을 붙이고
outlier는 `-1`이다.

Getis-Ord는 **이웃 배열을 먼저 만들어야** 한다 — `weights` 컬럼이 `{value, neighbor}` struct의
배열이고, `star=true`면 자기 자신을 이웃 배열에 포함시켜 Gi\*가 된다. 출력 컬럼은
`G, E[G], V[G], Z, P`.

⭐ **이 다섯은 공간 오믹스에서 쓰는 통계와 같은 계열이다** — 공간 자기상관·핫스팟·밀도 클러스터링.
[[SpatialData and Sedona interop]] §GeoStats 참고.

### 6. GeoPandas 호환 API

```python
import sedona.spark.geopandas as sgpd    # 관례 약칭 (gpd 에 s 를 붙인 것)
```

`GeoDataFrame`/`GeoSeries`가 **`pyspark.pandas`의 `ps.DataFrame`/`ps.Series`를 상속**한다.
`import` 만으로 PySpark 기본 세션을 쓰고 Sedona 함수를 자동 등록한다 — `SedonaContext.create()`
호출이 불필요.

변환 메서드: `to_geopandas()` · `to_geoframe()` · `to_spark_pandas()` · `to_spark()` · `to_frame()`.

⚠️ **기여자 문서가 대가를 솔직하게 적는다** (사용자 문서엔 없는 내용):

- **`sjoin`은 순서를 보존하지 않는다** — *"This follows the same convention as traditional PySpark
  Pandas. The user can always post-sort using `sort_index()`."*
- **`crs` 조회가 비싸다** — *"Sedona's implementation for getting the `crs` […] requires us to run
  an eager `ST_SRID()` query. If we eagerly query for the crs in every initialization of
  `GeoSeries`, all of our function calls would also become eager."* → lazy를 지키려고 GeoPandas의
  CRS 검증들을 포기했다.
- 디버깅 수단: `geoseries.area.to_frame().spark.explain(extended=True)`

1.9.x에서 대거 확장됐다 — `dissolve`, `clip`, `cx`, affine 변환(rotate/translate/scale/skew),
`concave_hull`, `voronoi_polygons`, `delaunay_triangles`, `minimum_rotated_rectangle` 등.

### 7. 버전 상태 (접근일 2026-08-19)

| 버전 | 릴리스 | 주요 내용 |
|---|---|---|
| **1.9.1** | 2026-08-05 | **Geography 타입**(핵심 SQL 함수 + 브로드캐스트 조인) · **Box2D/Box3D 타입**(+ Parquet row-group pushdown) · `geotiff.metadata`·`netcdf.metadata` 데이터소스 · **래스터 거리 조인** · Raster Python UDF(`RS_MapAlgebra` deprecated) · 중국어 문서 |
| 1.9.0 | 2026-04-23 | Spark 4.1 · **proj4sedona** CRS 전환 · Bing Tile 함수 · `RS_AsCOG` · **GeoTiff 자동 타일링 리더**(Spark 2GB 레코드 한계 우회) · GeoParquet 1.1 covering 자동 생성 |
| 1.8.1 | 2026-01-09 | — |
| 1.8.0 | 2025-09-13 | GeoPandas 호환 API · PyFlink · Java 11 · Spark 4.0 · vectorized UDF · Moran's I |
| 1.7.0 | 2024-12-02 | **KNN join** · **GeoStats 모듈** · Shapefile/GeoPackage DataFrame 리더 |

⚠️ **repo의 `docs/index.md`는 낡았다** — 최신 항목이 1.8.0이다. 라이브 사이트는 1.9.1을 알린다.
버전 상태는 릴리스 API로 확인해야 한다.

## 기존 페이지와의 관계

**정정 2건.**

1. ⚠️ [[Apache Sedona]]의 *"Spark·Flink 위에서"* 정의 → 런타임 4종. SedonaDB가 **단일 머신
   자리를 직접 차지**하므로 책이 준 갈림축(*"기존 GIS는 단일 머신, Sedona는 레이크 규모"*)이
   무효화된다.
2. ⚠️ [[SpatialData as a data engineering substrate]] §2의 *"DuckDB/Trino가 Zarr 래스터는 의미
   있게 못 읽는다"* → **`sedonadb-zarr`가 반례를 만든다.** 단 SpatialData 레이아웃에서 되는지는
   미확인. → [[SpatialData and Sedona interop]]

**확장** — [[GPU architecture]](RT 코어를 DB 연산에), [[Apache DataFusion]](SedonaDB의 기반),
[[MLOps]](GeoStats는 "SQL 안의 ML" 갈래에 가깝다).

## 링크

- 자매 소스: [[Apache Sedona docs - Spatial join execution]],
  [[Apache Sedona docs - Storage and formats]]
- 엔티티: [[Apache Sedona]], [[SedonaDB]], [[Apache Spark]], [[Apache Flink]],
  [[Apache DataFusion]]
- 응용: [[SpatialData and Sedona interop]]
- 개념: [[Spatial join execution]], [[GPU architecture]], [[MLOps]], [[Object storage layout]]
- 영역 MOC: [[Data Engineering]], [[Bioinformatics]]

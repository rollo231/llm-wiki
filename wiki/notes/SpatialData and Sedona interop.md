---
type: note
title: SpatialData and Sedona interop
area: [bioinformatics, data-engineering]
aliases:
  - SpatialData Sedona
  - Sedona 공간 오믹스
  - SpatialData 분산 공간 조인
  - spatialdata sedona 연동
  - point-in-polygon 분산
tags: [spatial-omics, data-engineering, sedona, sedonadb, geoparquet, zarr, spatial-join, aggregate, xenium, merscope]
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[Apache Sedona docs - Spatial join execution]]"
  - "[[Apache Sedona docs - Storage and formats]]"
  - "[[Apache Sedona docs - Runtimes and GeoStats]]"
  - "[[SpatialData source - ShapesModel and shapes IO]]"
  - "[[SpatialData source - Shapes conversion and aggregation ops]]"
  - "https://github.com/scverse/spatialdata/blob/v0.8.0/src/spatialdata/_io/io_points.py"
  - "https://github.com/scverse/spatialdata-io/blob/v0.7.1/src/spatialdata_io/readers/xenium.py"
  - "https://github.com/scverse/spatialdata-io/blob/v0.7.1/src/spatialdata_io/readers/merscope.py"
---

# SpatialData and Sedona interop

**질문:** [[SpatialData]]와 [[Apache Sedona]]는 정확히 어디서 만나고 어디서 어긋나는가?
[[Spatial aggregation]]의 issue #210(*points → shapes 집계가 모든 점을 메모리에 올린다*)을 Sedona로
우회할 수 있는가?

**답:** 만나는 지점은 **이미 디스크에 있다** — SpatialData가 points와 shapes를 Parquet/GeoParquet으로
쓴다. 내보내기(export) 단계가 애초에 없다. 그리고 우려했던 **좌표변환 이음새는 이 연산에서는 문제가
되지 않는다** — 소스를 읽어 확인했다.

> ⚠️ **근거 구분.** §0~§3은 소스 코드로 확인한 사실이다. §4~§6은 설계 판단(의견)이고,
> §7이 남은 미검증 목록이다. **실행해 본 것은 아무것도 없다.**

## 0. 정정 — "불투명 blob"은 틀렸다

[[Apache Sedona]] 초판(Ch11 인제스트, 2026-08-19 오전)이 적은 것:

> ⚠️ *"Sedona는 Spark/Flink DataFrame의 geometry 타입을 다루고, SpatialData store는 쿼리 엔진이
> 읽지 못하는 **불투명 blob**이다([[Object storage layout]])."*

**틀렸다.** element 종류마다 상태가 전혀 다르고, 하필 필요한 두 종류가 이미 열려 있다.

| element | 온디스크 실물 | 쿼리 엔진이 읽는가 |
|---|---|---|
| **Shapes** | `shapes/<name>/shapes.parquet` — `geopandas.to_parquet()`, 즉 **GeoParquet** (`WKB` 기본 / `geoarrow` 선택) | ✅ **Sedona가 그대로 읽는다** |
| **Points** | `points/<name>/points.parquet` — dask `to_parquet()`, **평범한 Parquet** (`x`·`y`·`z` 컬럼, geometry 타입 아님) | ✅ 읽는다. `ST_Point(x, y)` 한 번 |
| **Images·Labels** | Zarr 청크 배열 ([[OME-NGFF]]) | ⚠️ 이론상 `sedonadb-zarr`. **미검증** (§6) |
| **Tables** | `AnnData` (Zarr 그룹) | ❌ |

근거: `io_shapes.py` / `io_points.py` (spatialdata v0.8.0) —
[[SpatialData source - ShapesModel and shapes IO]], 그리고 이번에 추가로 읽은 `io_points.py`.

⭐ 그리고 [[SpatialData as a data engineering substrate]] §2가 이미 정확하게 적어 뒀다 —
*"DuckDB/Trino가 `shapes.parquet`·`points/*.parquet`는 읽지만 Zarr 래스터는 의미 있게 못 읽는다."*
**Sedona 페이지가 그 노트를 참조하지 않고 쓰여서 생긴 모순이다.**

## 1. 진짜 이음새 — 좌표변환은 Parquet 안에 없다

두 writer가 **좌표변환을 명시적으로 지운 뒤** Parquet을 쓴다.

```python
# io_points.py — write_points()
points_without_transform = points.copy()
del points_without_transform.attrs["transform"]     # ← 지운다
points_without_transform.to_parquet(path)
...
overwrite_coordinate_transformations_non_raster(group=group, axes=axes, transformations=transformations)
#                                                              ↑ zarr 그룹 메타데이터에 따로 쓴다
```

`write_shapes()`도 같다(`to_parquet()` 직전에 `attrs["transform"]`을 일시 삭제 후 복원).

**결론: Parquet 안의 좌표는 intrinsic 좌표계다.** global 좌표계로 정렬된 값이 아니다.
→ **Parquet만 아는 도구는 좌표변환을 못 본다.** Sedona가 정확히 그 도구다.

## 2. ⭐⭐ 그런데 이 연산에서는 문제가 되지 않는다 — 리더 소스로 확인

우려의 핵심은 *"points와 shapes의 transform이 다르면 조인이 조용히 틀린다"* 였다.
[[spatialdata-io]] 리더 두 개를 읽어 확인했다.

### [[Xenium]] (`xenium.py` v0.7.1)

```python
# transcripts (points)
transform = Scale([1.0 / specs["pixel_size"], 1.0 / specs["pixel_size"]], axes=("x", "y"))
points = PointsModel.parse(table, coordinates={...}, feature_key=FEATURE_NAME,
                           instance_key=CELL_ID, transformations={"global": transform}, sort=True)

# cell_boundaries / nucleus_boundaries (shapes)
scale = Scale([1.0 / specs["pixel_size"], 1.0 / specs["pixel_size"]], axes=("x", "y"))
return ShapesModel.parse(geo_df, transformations={"global": scale})

# cell_circles (shapes) — 같은 Scale
# labels (masks) — Identity()
# morphology image — Identity() 또는 정렬 파일이 있으면 Affine(alignment)
```

### [[MERSCOPE]] (`merscope.py` v0.7.1)

```python
microns_to_pixels = Affine(np.genfromtxt(images_dir / TRANSFORMATION_FILE),
                           input_axes=("x", "y"), output_axes=("x", "y"))
transformations = {"global": microns_to_pixels}
...
points[f"{dataset_id}_transcripts"] = _get_points(transcript_path, transformations)   # ← 같은 dict
shapes[f"{dataset_id}_polygons"]   = _get_polygons(boundaries_path, transformations)  # ← 같은 dict
```

**두 플랫폼 모두 points와 shapes에 동일한 transform을 넣는다.** 이유가 구조적이다 — 둘은 같은
장비 좌표 공간(µm)에서 나오고, transform의 임무는 **그 둘을 이미지 픽셀 격자에 맞추는 것**이다.
따라서 서로 어긋날 이유가 없다.

### ⭐ 그래서 위상 술어는 불변이다

⚠️ **아래는 소스가 말한 것이 아니라 기하로부터의 추론이다** (다만 초등적이다):

가역 affine 변환은 **포함·교차 관계를 보존한다.** 양쪽에 같은 변환이 걸려 있으면 그 변환을 적용하기
전에 조인해도 결과 쌍이 같다.

| 술어 | intrinsic 공간에서 조인해도 되는가 |
|---|---|
| `ST_Within` · `ST_Contains` · `ST_Intersects` · `ST_Covers` | ✅ **불변** |
| `ST_DWithin` · `ST_Distance` | ⚠️ Xenium(균등 Scale)은 상수배 — 임계값을 `/pixel_size` 해서 넘기면 된다. MERSCOPE(일반 Affine)는 **방향에 따라 배율이 다르다** |
| `ST_Area` · 부분 겹침 면적비(`fractions`) | ⚠️ `|det A|` 배. 비율만 쓰면 상쇄되지만 절대 면적은 틀린다 |
| points/shapes ↔ **labels·image** 조인 | ❌ transform이 다르다(Identity vs Scale/Affine). **여기가 진짜 위험 지대** |

**즉 issue #210이 걸리는 그 연산 — transcript를 세포 폴리곤에 붙이는 point-in-polygon — 은
좌표변환을 재구성하지 않고 raw Parquet에서 바로 해도 된다.**

⚠️ 단 이건 **이 두 리더에서 확인한 것**이다. 리더 13종 전부가 그렇다는 보장은 없고, 사용자가 직접
`transformations=`를 준 store도 예외다. **파이프라인이라면 조인 전에 양쪽 `.zattrs`의
`coordinateTransformations`가 같은지 단언(assert)해야 한다** — 검사는 싸고 실패는 조용하다.

## 3. 4단계 경로가 이렇게 줄었다

[[Apache Sedona]] 초판의 미검증 4단계:

```
1. points를 (Geo)Parquet으로 내보낸다        ← 삭제. 이미 Parquet이다
2. shapes 폴리곤도 같은 방식으로 내보낸다      ← 삭제. 이미 GeoParquet이다
3. Sedona로 분산 공간 조인
4. 결과 cell × gene 표를 Table로 되돌린다
```

수정된 경로:

```
① (검사) 양쪽 .zattrs 의 coordinateTransformations 가 동일한지 단언한다
② SedonaDB / Sedona 로 두 parquet 을 직접 읽는다 — ST_Point(x, y) 로 points 를 기하화
③ ST_Within 조인 → GROUP BY cell, gene → COUNT
④ 결과를 TableModel 계약(region · region_key · instance_key)에 맞춰 AnnData 로 되돌린다
```

⚠️ **미실행 스케치**:

```python
import sedona.db
sd = sedona.db.connect()

base = "s3://omics/silver/S0142/v3.1.0/sample.zarr"
pts = sd.read(f"{base}/points/transcripts/points.parquet").alias("p")
shp = sd.read(f"{base}/shapes/cell_boundaries/shapes.parquet").alias("c")

sd.sql("""
SELECT c.cell_id, p.feature_name, COUNT(*) AS n
FROM p JOIN c ON ST_Within(ST_Point(p.x, p.y), c.geometry)
GROUP BY 1, 2
""")
```

⚠️ 스케치의 미확인 지점: `shapes.parquet`의 **인덱스가 어떤 컬럼명으로 나오는가.** Xenium 리더는
XOA 버전에 따라 `label_index`(int)를 인덱스로 쓰고 `cell_id`를 컬럼으로 두거나, `cell_id`(str)를
인덱스(`index.name = "cell_id"`)로 둔다 — pandas 인덱스가 Parquet에서 어떤 이름을 갖는지는 실물
확인 필요.

### ⭐ 그런데 이 조인이 필요한 경우가 언제인지 짚어둘 필요가 있다

Xenium 리더는 points에 `instance_key=CELL_ID`를 넣는다 — **벤더의 `transcripts.parquet`에 이미
`cell_id` 컬럼이 있다.** 즉 10x가 자기 세그멘테이션으로 이미 할당을 해뒀고, 그 경우 cell × gene
행렬은 조인 없이 `GROUP BY cell_id, feature_name` 하나로 나온다.

**공간 조인이 실제로 필요한 것은 경계가 새로 생겼을 때다** — 커스텀/재세그멘테이션, 다른 반경의
circle, 조직 구조·니치 같은 상위 영역, 다른 element로 정의된 ROI. `aggregate()`의 존재 이유가
그것이고, issue #210이 아픈 것도 그때다.

## 4. `aggregate()`가 조용히 해주던 것들 — 무엇을 잃는가

| | `spatialdata.aggregate()` | Sedona 경로 |
|---|---|---|
| 연산 정체 | point-in-polygon sjoin + groupby | 같음 |
| [[Spatial join execution\|① 격자]] | ❌ | ✅ (분산 시) |
| ② 인덱스 | ✅ geopandas `sindex` | ✅ R-tree/quadtree |
| ③ refine | ✅ shapely | ✅ JTS |
| 메모리 | ⚠️ **전량 `.compute()`** (issue #210) | 파티션/스트리밍 |
| 좌표계 정렬 | ✅ `target_coordinate_system`으로 양쪽 자동 `transform()` | ❌ **§1·§2가 사용자 책임** |
| circle 처리 | ✅ `to_polygons()`로 `buffer_resolution=16` 다각형화 | ❌ Sedona는 `radius` 컬럼을 모른다. `ST_Buffer` 직접 |
| `fractions` 부분 겹침 | ✅ `overlay(how="intersection")` | ❌ `ST_Intersection` + `ST_Area` 직접 |
| `value_key` 3경로 | ✅ dataframe 컬럼 / table `obs` / table `var`(=`X` 열) | ❌ Parquet 컬럼만. table은 별도 조인 |
| 반환 | `SpatialData` 객체(by shapes + 연결된 table) | 그냥 표. ④ 조립이 필요 |
| 예약 컬럼 충돌 검사 | ✅ `__ones_column` 등 assert | ❌ |

⭐ **한 줄 요약: Sedona는 규모를 주고 계약을 뺀다.** `aggregate()`가 문서화해 둔 금지 조합
(`fractions=True` + points → 전부 0, categorical + `mean` → 무의미)도 전부 사용자가 지켜야 한다
— [[Spatial aggregation]]에 그 목록이 있다.

## 5. ⭐⭐ 예상 밖의 수확 — GeoStats

Sedona `stats` 모듈이 제공하는 것: **DBSCAN · Local Outlier Factor · Getis-Ord Gi/Gi\* ·
Moran's I · 거리 가중 행렬(distance band)**.

이건 공간 전사체 분석의 표준 통계와 같은 계열이다 — 공간 자기상관, 핫스팟, 밀도 기반 클러스터링.
그리고 입력이 **geometry 컬럼을 가진 DataFrame**, 즉 `shapes.parquet` 그 자체다. `use_spheroid=False`
(기본)면 평면 좌표에서 동작한다.

⚠️ **유리하다고 단정할 수 없는 이유**:

- Sedona의 이 함수들은 **단변량**이다(`x` 컬럼 하나). 유전자 수천 개에 대해 Moran's I를 돌리려면
  반복이고, squidpy류가 벡터화로 하는 일이다. **한 슬라이드 안에서는 이길 이유가 없다.**
- 유리해지는 쪽은 **여러 슬라이드·샘플을 가로지르는 통계** — 배치 전체에 대해 한 번에 도는 형태.
  ⚠️ 미측정.
- Getis-Ord는 이웃 배열(`weights`)을 **먼저 만들어야** 한다 — `add_distance_band_column`.
  그 자체가 self distance join이고, 그건 Sedona가 잘하는 일이다.

## 6. 래스터 — 유일하게 남은 진짜 미지

[[SedonaDB]] 0.4.0의 `sedonadb-zarr`가 **Zarr 그룹을 질의 가능한 래스터 컬럼으로** 읽는다.
청크 하나가 행 하나이고, 픽셀은 lazy다. SpatialData의 이미지도 Zarr다. 그럼 되는가?

**전부 미확인이고, 확인해야 할 것은 명확하다:**

- [[OME-NGFF]] **multiscale 그룹 구조**(`0/`·`1/`… 피라미드)를 인식하는가, 아니면 배열 하나만 받는가
- **CRS/SRID가 없는 배열**을 받는가. 블로그 예시는 `srid = 3857`을 반환한다
- 축 이름이 `c,y,x`일 때 `RS_Envelope`가 무엇을 반환하는가 (채널 축을 공간 축으로 오해하지 않는가)
- OME-NGFF의 `coordinateTransformations`(스케일)을 읽는가 — **§1과 같은 문제가 래스터에도 있을 것이다**

⭐ **된다면 얻는 것이 크다.** [[SpatialData as a data engineering substrate]] §4가 카탈로그
컬럼으로 물질화하려던 것들 — `extent`, `chunks`, `n_objects`, `shape` — 이 **store를 열지 않고
SQL로 얻어진다.** 카탈로그 설계의 상당 부분이 "미리 계산해 박아두기"에서 "그냥 질의하기"로 바뀐다.
[[Object storage layout]] ⑤의 *"수백만 객체를 `list-objects`로 열거하는 게 불가능하다"* 도
**청크 = 행** 매핑으로 우회된다.

## 7. 판단 기준 — 갱신

기존 기준(책 인제스트 때):

> *"한 store가 단일 머신에서 처리되면 그대로 두고, 레이크 규모(플랫폼 전체·다수 슬라이드 배치)가
> 되면 검토한다."*

**여전히 맞지만 문턱이 내려갔다.** [[SedonaDB]]는 클러스터가 아니라 `pip install`이고, 읽는 파일이
이미 store 안에 있다. **"레이크 규모"를 기다릴 이유가 없어졌다.**

새 3단:

| 상황 | 선택 |
|---|---|
| points가 메모리에 올라간다 | `aggregate()` 그대로. **아무것도 바꾸지 않는다** |
| **한 store의 points가 메모리를 넘는다** | **SedonaDB.** 클러스터 없이, 같은 parquet을 읽고, transform 동일성만 단언 |
| 여러 store를 가로질러야 한다 | SedonaSpark + 카탈로그([[SpatialData as a data engineering substrate]] §4) |

⚠️ 그리고 [[Apache Sedona]]가 옮긴 책의 경고는 그대로 유효하다 —
*"단순 위경도 필터만 필요하면 일반 SQL로도 충분한 경우가 많다."* 여기서는:
**cell_id가 이미 있으면 `GROUP BY`로 끝난다.**

## 8. 좌표계 — CRS는 필요 없다

Sedona 문서: *"Sedona uses the Euclidean distance between two objects so the distance unit has the
same CRS of the original coordinates."*

⭐ **뒤집어 읽으면 CRS가 없어도 된다.** 마이크론·픽셀 좌표를 위경도로 위장할 필요가 없고,
`ST_Within`·`ST_Intersects`·`ST_DWithin`·`ST_Area`가 그대로 동작한다. 이게 §3 경로의 전제다.

⚠️ 반대로 **못 쓰는 기능 목록** (전부 경위도·구면을 전제한다):

| 기능 | 왜 못 쓰나 |
|---|---|
| `ST_GeoHash` 정렬 트릭 | geohash는 경위도 정의. GeoParquet 프루닝 극대화 처방을 그대로 쓸 수 없다 |
| S2 근사 equi-join | 지구 구면 셀 |
| Geography 타입(1.9.1) · `ST_DistanceSphere`/`Spheroid` | 측지 |
| `RS_DWithin` | 양쪽을 WGS84로 투영한 뒤 미터로 계산한다 |

⚠️ 그런데 GeoParquet 프루닝은 애초에 큰 문제가 아니다 — element마다 **`shapes.parquet` 파일이
하나**라서 파일 스킵의 대상이 없다. points는 dask가 파티션별 파일을 쓰므로 다수지만,
**bbox covering 컬럼이 없다**(SpatialData가 그런 옵션을 쓰지 않는다). 즉 프루닝을 쓰려면
**중간 GeoParquet을 다시 쓰는 단계가 필요**하고, 그건 §3이 없앤 export 단계를 되살리는 셈이다.
→ 한 store 안의 단발 조인에는 불필요하고, **여러 store를 반복 질의하는 gold 층에서만 값을 한다.**

## 9. 미검증 — 실측 우선순위

1. **⭐ 리더 13종의 transform이 points/shapes에서 정말 항상 같은가** — Xenium·MERSCOPE는 확인됐다.
   **나머지는 소스 읽기로 답이 난다**(`spatialdata_io/readers/*.py`). 파이프라인 assert의 근거가
   되므로 1순위.
2. **`shapes.parquet`·`points.parquet`의 실제 컬럼 스키마** — 특히 pandas 인덱스가 어떤 이름으로
   나오는지. 실물 store 하나로 확인된다.
3. **SedonaDB가 실제로 이 두 파일을 읽는가.** GeoParquet `crs: null`을 받아들이는지, WKB 인코딩을
   자동 인식하는지. 실행 필요.
4. **issue #210이 터지는 실제 규모** — 이건 책 인제스트 때도 "다음 소스 우선순위"에 있었다.
   기준선이 없으면 §7의 3단이 언제 2단으로 넘어가는지 알 수 없다.
5. **`sedonadb-zarr` × OME-NGFF** (§6). 되면 카탈로그 설계가 바뀐다.
6. ④ 단계(결과를 `TableModel` 계약으로 되돌리기)의 실제 코드 — `region`/`region_key`/
   `instance_key` 조립. [[SpatialData elements]]의 세 키 규칙을 따르면 되지만 미작성.
7. Sedona GeoStats의 단변량 제약이 유전자 수천 개 규모에서 실용적인가 (§5).

## 링크

- **자매 노트** — [[SpatialData as a data engineering substrate]]: 포맷이 무엇을 주고 안 주는가.
  이 노트는 그 §2의 *"SQL 엔진 없음"* 항목에 **엔진 이름을 붙인다.**
  · [[Spatial omics platform roadmap]]: 도입 순서
- 연산: [[Spatial aggregation]], [[Spatial join execution]], [[Rasterization and vectorization]]
- 좌표: [[Coordinate systems and transformations]] — §1·§2의 배경
- 포맷: [[SpatialData Shapes element]], [[SpatialData Zarr format versions]],
  [[SpatialData elements]], [[Columnar and in-memory data formats]]
- 엔진: [[Apache Sedona]], [[SedonaDB]], [[Apache Spark]]
- 소스: [[Apache Sedona docs - Spatial join execution]],
  [[Apache Sedona docs - Storage and formats]], [[Apache Sedona docs - Runtimes and GeoStats]],
  [[SpatialData source - ShapesModel and shapes IO]],
  [[SpatialData source - Shapes conversion and aggregation ops]]
- 플랫폼: [[Xenium]], [[MERSCOPE]], [[Visium HD]] · 리더: [[spatialdata-io]]
- 영역 MOC: [[Bioinformatics]], [[Data Engineering]]

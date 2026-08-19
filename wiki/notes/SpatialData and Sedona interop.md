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
  - "spatialdata-io v0.7.1 readers/*.py (15개 전수)"
  - "docs/experiments/spatialdata-sedona/ (자체 실측, 2026-08-19)"
---

# SpatialData and Sedona interop

**질문:** [[SpatialData]]와 [[Apache Sedona]]는 정확히 어디서 만나고 어디서 어긋나는가?
[[Spatial aggregation]]의 issue #210(*points → shapes 집계가 모든 점을 메모리에 올린다*)을 Sedona로
우회할 수 있는가?

**답:** 만나는 지점은 **이미 디스크에 있다** — SpatialData가 points와 shapes를 Parquet/GeoParquet으로
쓴다. 내보내기(export) 단계가 애초에 없다. 좌표변환 이음새는 이 연산에서 **상쇄된다**(리더 15종 전수
조사 + 실행 검증). ⭐ **결과가 `aggregate()`와 완전히 일치하고, 50M transcript에서 48배 빠르다.**
⚠️ 대가는 함정 두 개(CRS·dictionary)와 `aggregate()`가 해주던 계약의 상실이다.

> **근거 구분.** §0~§3은 소스 코드로 확인하고 **실행해서 검증했다** — 결과가 `aggregate()`와
> 비트 단위로 같고(§3), 규모 곡선도 실측했다(§7). §4~§6은 설계 판단(의견)이며 §6(래스터)은 미확인이다.
> §9가 검증 현황이다.
> 재현 스크립트: `docs/experiments/spatialdata-sedona/`.

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

### ⚠️⚠️ 리더 15종 전수 조사 — 반례가 있다 (2026-08-19)

`spatialdata-io` v0.7.1의 리더 15개를 전부 읽었다. **points와 shapes를 함께 만드는 것은 4개뿐**이고,
그중 하나가 어긋난다.

| 리더 | points transform | shapes transform | 같은가 |
|---|---|---|---|
| **xenium** | `Scale(1/pixel_size)` | `cell_boundaries`·`nucleus_boundaries`·`cell_circles` 전부 같은 `Scale` | ✅ |
| **merscope** | `{"global": microns_to_pixels}` | **같은 dict 객체** | ✅ |
| **stereoseq** | (인자 없음 → `Identity`) | `_circles`·`_polygons` 둘 다 인자 없음 → `Identity` | ✅ |
| **seqfish** | `{x: Identity()}` | circles `{x: Identity()}` ✅ / **segmentation polygons `{x: scaled[x]}`** ❌ | ⚠️ **혼재** |

⚠️⚠️ **seqfish가 반례다.** transcripts는 `Identity`인데 **세포 경계 폴리곤은 `Scale`**(DAPI 이미지의
스케일 팩터)을 갖는다. 하필 조인하고 싶은 element가 어긋난 쪽이다. circle 근사로 조인하면 맞고
폴리곤으로 조인하면 **조용히 틀린다.**

나머지 11개:

- **shapes만** (points 없음): `codex` · `curio` · `dbit` · `generic` · `visium` · `visium_hd`
  (visium_hd는 shapes 4종이 모두 같은 dict를 공유한다 ✅)
- **points만** (shapes 없음): `cosmx` — 세그멘테이션이 **Shapes가 아니라 Labels**다. points와 같은
  per-FOV affine을 갖지만, `aggregate()`가 지원하지 않는 조합(Labels × Points)이라 먼저 벡터화해야 한다.
  ⚠️ 그리고 **FOV마다 다른 affine**이라 FOV를 넘나드는 조인은 intrinsic 공간에서 불가능하다.
- **둘 다 없음** (images/labels 전용): `iss` · `macsima` · `mcmicro` · `steinbock`

> ⭐ **결론: assert가 선택이 아니라 필수다.** 3/4는 안전하지만 반례가 실재하고, 그 반례는 에러 없이
> 틀린 답을 낸다. 조인 전에 양쪽의 `coordinateTransformations`가 같은지 단언한다.
>
> ⚠️ **경로 정정**: spatialdata 0.8.0은 **Zarr v3**로 쓴다 — 읽어야 할 파일은 `.zattrs`가 아니라
> **`<element>/zarr.json`** 이고 변환은 `attributes.coordinateTransformations`에 있다(§실측 확인).

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
① (검사) 양쪽 <element>/zarr.json 의 coordinateTransformations 가 동일한지 단언한다
② SedonaDB / Sedona 로 두 parquet 을 직접 읽는다 — ST_Point(x, y) 로 points 를 기하화
③ ST_Within 조인 → GROUP BY cell, gene → COUNT
④ 결과를 TableModel 계약(region · region_key · instance_key)에 맞춰 AnnData 로 되돌린다
```

### ✅ 실행해서 확인했다 (2026-08-19)

`spatialdata 0.8.0` + `sedonadb 0.4.0`(apache-sedona 1.9.1), Python 3.12, macOS.
Xenium 형태의 합성 store(`Scale(1/0.2125)`를 points·shapes 양쪽에)를 만들어 돌렸다.
**결과가 `aggregate()`와 완전히 일치한다.**

```
SedonaDB join : 9,999 (cell, gene) pairs, 88,464 assigned transcripts
aggregate()   : table (400, 25),          88,464 assigned transcripts
sedona-only rows 0 · aggregate-only rows 0 · count mismatches 0   ==> IDENTICAL ✅
```

**작동하는 쿼리** (⚠️ 두 군데가 스케치와 다르다 — 아래 함정 참고):

```python
import sedona.db
sd = sedona.db.connect()
base = "…/sample.zarr"
sd.read_parquet(f"{base}/points/transcripts/points.parquet").to_view("pts", overwrite=True)
sd.read_parquet(f"{base}/shapes/cell_boundaries/shapes.parquet").to_view("shp", overwrite=True)

sd.sql("""
    SELECT c.cell_id AS cell_id,
           CAST(p.feature_name AS VARCHAR) AS gene,     -- ← 함정 ②
           COUNT(*) AS n
    FROM pts p JOIN shp c
      ON ST_Within(ST_SetSRID(ST_Point(p.x, p.y), 4326), c.geometry)   -- ← 함정 ①
    GROUP BY 1, 2
""").to_pandas()
```

### 실측한 온디스크 스키마

```
sample.zarr/
├─ zarr.json                                        # zarr_format: 3
├─ points/transcripts/
│  ├─ points.parquet/part.0.parquet                 # ← 디렉토리다 (dask 파트)
│  └─ zarr.json                                     # coordinateTransformations + feature_key
└─ shapes/cell_boundaries/
   ├─ shapes.parquet                                # ← 단일 파일
   └─ zarr.json
```

| | 컬럼 | 타입 |
|---|---|---|
| **points.parquet** | `x`, `y` | `double` |
| | `feature_name` | **`dictionary<values=string, indices=int8>`** ⚠️ |
| | 기타 벤더 컬럼(`qv` 등) | 그대로 |
| | **`__null_dask_index__`** | `int64` — dask 인덱스가 컬럼으로 새어 나온다 |
| **shapes.parquet** | `geometry` | `binary` + `ARROW:extension:name = geoarrow.wkb` |
| | **인덱스 이름 그대로** (`cell_id`) | `large_string` |

⭐ **인덱스 컬럼명 질문의 답**: pandas 인덱스는 **`index.name`을 그대로 컬럼명으로** 갖는다.
Xenium 리더가 `geo_df.index.name = "cell_id"`를 설정하는 분기에서는 `cell_id`, 이름을 주지 않는
`label_index` 분기에서는 pandas 관례상 `__index_level_0__`이 된다(⚠️ 후자는 미확인 — 실제 XOA store
필요). **`pandas` 메타데이터의 `index_columns`가 그 답을 들고 있으니 코드로 읽으면 된다.**

`geo` 메타데이터 실측:

```json
{"primary_column": "geometry",
 "columns": {"geometry": {"encoding": "WKB", "crs": null,
                          "geometry_types": ["Polygon"], "bbox": [5.0, 5.0, 595.0, 595.0]}},
 "version": "1.0.0", "creator": {"library": "geopandas", "version": "1.1.4"}}
```

⭐ **GeoParquet 1.0.0이고 `crs: null`, bbox는 있다.** §8의 추론이 맞았다 — **covering 컬럼이 없다**
(그건 1.1 기능이고 SpatialData는 그 옵션을 쓰지 않는다).

### ⚠️ 함정 ① — CRS 불일치로 조인이 **거부된다**

SedonaDB는 GeoParquet의 `crs: null`을 읽고 컬럼을 **`geometry<WkbView(ogc:crs84)>`** 로 태깅한다.
반면 `ST_Point(x, y)`가 만드는 기하는 CRS가 **없다**. 그래서:

```
SedonaError: type_coercion
caused by Error during planning: Mismatched CRS arguments: None vs ogc:crs84
Use ST_Transform() or ST_SetSRID() to ensure arguments are compatible.
```

⭐ **조용히 틀리지 않고 계획 단계에서 실패한다** — 좋은 설계다. 우회 두 가지가 **같은 답**을 준다:

- `ST_SetSRID(ST_Point(p.x, p.y), 4326)` — 점 쪽을 맞춘다
- `ST_SetSRID(c.geometry, 0)` — 폴리곤 쪽 CRS를 지운다

⚠️ 다만 기록해 둘 것: **마이크론 좌표가 `ogc:crs84`(경위도)로 라벨링된다.** 평면 술어에는 무해하지만
`ST_Transform`·Geography 타입·`ST_DistanceSphere`를 쓰면 의미가 틀어진다. §8의 "못 쓰는 기능" 목록이
왜 필요한지가 여기서 구체화된다.

### ⚠️ 함정 ② — dictionary 컬럼으로 GROUP BY 하면 조인이 깨진다

```
SedonaError: Dictionary key bigger than the key type
```

원인을 좁혔다 — **조인 + dictionary 컬럼 GROUP BY 조합에서만** 난다:

| 쿼리 | 결과 |
|---|---|
| `SELECT COUNT(*) FROM pts` | ✅ |
| `SELECT feature_name FROM pts LIMIT 3` | ✅ |
| `SELECT feature_name, COUNT(*) FROM pts GROUP BY 1` (조인 없음) | ✅ |
| 조인 + `GROUP BY cell_id` (dictionary 아님) | ✅ |
| **조인 + `GROUP BY cell_id, feature_name`** | ❌ |
| 조인 + `GROUP BY cell_id, CAST(feature_name AS VARCHAR)` | ✅ |

⚠️ **규모에 의존한다** — 200k행/25유전자에서는 나지 않았고 **1M행/100유전자에서 났다.** dictionary가
배치별로 존재하고 병합될 때 int8 인덱스 범위(±127)를 넘는 것으로 보인다(⚠️ 추정).
`io_points.py`의 주석이 경고한 바로 그 지점이다:

> *"This step is crucial when the number of categories exceeds 127, as pyarrow defaults to int8 for
> unknown categories which can only hold values from -128 to 127."*

⭐ **실제 Xenium 패널은 300~5,000 유전자다 — 반드시 걸린다.** 처방은 토큰 하나:
**`CAST(feature_name AS VARCHAR)`**. 비용은 측정하지 않았다.

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

## 7. ⭐⭐ issue #210이 어디서 터지는가 — 실측 곡선

**측정 환경**: MacBook, 32GB RAM / 10 코어. `spatialdata 0.8.0` · `sedonadb 0.4.0`.
셀 3,600개(정사각형 폴리곤) × 유전자 100종, transcript 수만 바꿨다. 엔진별로 **별도 프로세스**에서
돌려 peak RSS(`ru_maxrss`)를 깨끗하게 재고, 결과의 동등성을 매 규모에서 확인했다.

| transcript | `aggregate()` 시간 | `aggregate()` peak RSS | SedonaDB 시간 | SedonaDB peak RSS | 시간 배수 | 결과 |
|---:|---:|---:|---:|---:|---:|:---:|
| 1M | 0.86 s | 829 MB | 0.06 s | 311 MB | 14× | ✅ 일치 |
| 5M | 3.77 s | 2,847 MB | 0.22 s | 485 MB | 17× | ✅ 일치 |
| 20M | 19.65 s | 8,961 MB | 0.89 s | 818 MB | 22× | ✅ 일치 |
| 50M | **94.10 s** | 10,605 MB | 1.97 s | 1,364 MB | **48×** | ✅ 일치 |

⭐ **읽는 방법은 RSS가 아니라 시간의 기울기다.**

- `aggregate()` 시간: ×5 데이터에 ×4.4 → ×4 데이터에 ×5.2 → **×2.5 데이터에 ×4.8**.
  **20M→50M에서 초선형으로 꺾인다.** RSS는 9.0→10.6GB로 1.2배밖에 안 늘었는데 시간이 4.8배다 —
  메모리 압박이 스와핑·GC로 나타나는 전형적 모양이다.
- SedonaDB 시간: ×5에 ×3.7 → ×4에 ×4 → ×2.5에 ×2.2. **선형 이하로 유지된다.**
- ⚠️ **store를 *쓰는* 것도 같은 벽에 부딪힌다** — 50M store를 만드는 build 단계가 peak **9.6GB**를
  썼다. `aggregate()`만 문제가 아니라 **pandas 경로 전체가 그렇다.**

**실제 규모와의 거리**: [[Xenium]] 한 런은 수억 transcript다 —
[[SpatialData as a data engineering substrate]] §4.5의 예시 행이 4.2억이다. 이 곡선이면 **`aggregate()`로는 자체 워크스테이션에서 불가능**하고,
SedonaDB는 같은 하드웨어에서 선형 구간에 남아 있다.

⚠️ **합성 데이터의 한계를 분명히 해 둔다** — 균일 난수 좌표, 겹치지 않는 정사각형 셀, 균등 유전자
분포다. 실제 조직은 공간적으로 뭉치고(파티션 skew) 폴리곤은 볼록하지 않으며 경계가 접한다.
**refine 비용과 skew 대응은 이 실험이 재지 않았다.** 배수의 절대값을 인용하지 말 것 — 읽어야 할 것은
**기울기의 형태**다.

## 7-b. 판단 기준 — 갱신

기존 기준(책 인제스트 때):

> *"한 store가 단일 머신에서 처리되면 그대로 두고, 레이크 규모(플랫폼 전체·다수 슬라이드 배치)가
> 되면 검토한다."*

**문턱이 내려갔고, 이제 숫자가 붙는다.** [[SedonaDB]]는 클러스터가 아니라 `pip install`이고, 읽는
파일이 이미 store 안에 있다.

| 상황 | 선택 |
|---|---|
| transcript ~수백만 이하 (peak RSS 수 GB) | `aggregate()` 그대로. **아무것도 바꾸지 않는다** |
| **수천만 이상 — 시간이 초선형으로 꺾이는 구간** | **SedonaDB.** 클러스터 없이, 같은 parquet, transform 동일성만 단언 |
| 여러 store를 가로질러야 한다 | SedonaSpark + 카탈로그([[SpatialData as a data engineering substrate]] §4) |

⚠️ 그리고 [[Apache Sedona]]가 옮긴 책의 경고는 그대로 유효하다 —
*"단순 위경도 필터만 필요하면 일반 SQL로도 충분한 경우가 많다."* 여기서는:
**cell_id가 이미 있으면 `GROUP BY`로 끝난다.**

⭐ **덤으로 얻은 판단**: 성능 차이(14~48×)가 **함정 두 개를 감수할 값이 되는가**가 실제 질문이다.
`ST_SetSRID`와 `CAST(... AS VARCHAR)`는 각각 토큰 하나이고, 그 대가로 `aggregate()`가 해주던 계약
(§4)을 잃는다. **작은 store에서 바꿀 이유는 없다.**

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

## 9. 검증 현황 — 무엇이 닫혔고 무엇이 남았나

### ✅ 닫힌 것 (2026-08-19)

1. ~~**리더 13종의 transform**~~ → **15종 전수 조사 완료.** points+shapes를 함께 만드는 것은 4개뿐이고
   **seqfish가 반례**다 (§2). ⭐ assert가 필수라는 결론.
2. ~~**parquet 컬럼 스키마**~~ → **실측 완료** (§3). 인덱스는 `index.name`을 그대로 컬럼명으로 갖고,
   `pandas` 메타데이터의 `index_columns`가 답을 들고 있다. `__null_dask_index__`가 points에 새어 나온다.
3. ~~**SedonaDB가 이 두 파일을 읽는가**~~ → **읽는다.** `geo` 메타데이터로 `geometry` 타입을 인식한다.
   ⚠️ 함정 둘을 발견했다 — **CRS 불일치로 조인 거부** · **dictionary GROUP BY에서 조인 파괴** (§3).
4. ~~**issue #210이 터지는 규모**~~ → **곡선을 실측했다** (§7). 자체 워크스테이션 기준
   **20M transcript ≈ 9GB**, 50M ≈ 22GB. 실제 Xenium 규모(수억)는 단일 머신 범위 밖이다.
5. **결과 동등성** → `aggregate()`와 **비트 단위로 같다.** 1M·5M·20M·50M 전부 `assigned` 일치 (§7).

### ⚠️ 남은 것

1. **⭐ `sedonadb-zarr` × [[OME-NGFF]]** (§6). 되면 카탈로그 설계가 바뀐다. 이제 1순위.
2. **실제 XOA store에서의 인덱스 컬럼명** — `label_index` 분기(인덱스에 이름 없음)가 정말
   `__index_level_0__`이 되는지. 합성 store로는 재현하지 않았다.
3. ④ 단계(결과를 `TableModel` 계약으로 되돌리기)의 실제 코드 — [[SpatialData elements]]의 세 키
   규칙을 따르면 되지만 미작성.
4. **`CAST(... AS VARCHAR)`의 비용** — 함정 ②의 우회가 큰 패널에서 얼마나 비싼가. 미측정.
5. Sedona GeoStats의 단변량 제약이 유전자 수천 개 규모에서 실용적인가 (§5).
6. **분산(SedonaSpark) 구간** — 단일 노드 곡선만 재봤다. 여러 store를 가로지르는 경우는 미측정.
7. ⚠️ **합성 데이터의 한계** — 균일 난수 좌표, 겹치지 않는 정사각형 셀, 유전자 균등 분포다. 실제
   조직은 공간적으로 뭉치고(skew) 폴리곤은 볼록하지 않으며 셀 경계가 접한다. **격자 파티셔닝의
   skew 대응이나 refine 비용은 이 실험으로 측정되지 않았다.**

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

---
type: concept
title: SpatialData Shapes element
area: [bioinformatics]
aliases: [Shapes, ShapesModel, Circles, 셰이프스, 도형 엘리먼트]
tags: [spatial-omics, data-model, geopandas, geoparquet, shapes, regions]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[SpatialData source - ShapesModel and shapes IO]]", "[[SpatialData docs - Design doc]]", "[[SpatialData source - Spatial and relational queries]]"]
---

# SpatialData Shapes element

[[SpatialData elements]] 5종 중 하나. **벡터 형태의 영역(region)** 을 담는다 —
`geopandas.GeoDataFrame`, 2D. [[SpatialData Zarr format versions|저장 시]]에는
`shapes/<이름>/` Zarr 그룹이 된다.

`Labels`(픽셀 마스크)와 함께 **Regions** 의 두 구현 중 벡터 쪽이다. `Tables` 가
`region`/`region_key`/`instance_key` 로 가리키는 대상이 될 수 있다.

## 들어갈 수 있는 것: 두 형태뿐

| 형태 | shapely 타입 | `geometry` 코드 | 추가 필수 컬럼 |
|---|---|---|---|
| **Circles** | `Point` | `0` | `radius` |
| **Polygons** | `Polygon` | `3` | — |
| **MultiPolygons** | `MultiPolygon` | `6` | — |

**circle 은 원 도형이 아니라 중심점 + 반지름이다.** [[Visium]] spot, [[Visium HD]] bin,
[[Xenium]] `cell_circles` 가 모두 이 형태로 저장된다. 세포·핵 경계나 임상 주석 ROI 는
polygon 쪽이다.

**한 element 안에서 두 계열을 섞을 수 없다** — Point 만이거나, Polygon/MultiPolygon 만이거나.
(단, 아래 "검증의 구멍" 참고.)

이 외에 임의의 컬럼을 **주석으로 직접 담을 수 있다**. `Tables` 없이도 shape 별 값을 가질 수 있다는
뜻이다(예: [[Xenium]] 리더가 polygon GeoDataFrame 에 `cell_id` 컬럼을 함께 넣는다).

## `ShapesModel` 계약

`ShapesModel.validate()` 가 강제하는 것:

- `geometry` 컬럼이 **존재**하고, `GeoSeries` 이고, **비어 있지 않을 것**
- 첫 원소가 `Point` | `Polygon` | `MultiPolygon` 일 것
- `Point` 라면 `radius` 컬럼이 있고 **모든 값이 양수**일 것
- `attrs["transform"]` 이 존재하고 **빈 dict 가 아닐 것** (최소 1개 좌표변환 필요)

경고에 그치는 것 (에러 아님):

- `radius` 에 NaN/inf → 경고. **다음 릴리스에서 `ValueError` 로 승격 예정**. 과거에 저장된
  [[Xenium]] 데이터에서 발생할 수 있다
  ([discussion #657](https://github.com/scverse/spatialdata/discussions/657)).
- geometry 가 3D → 경고 + `force_2d()` 권고. 설계 문서의 "Shapes 는 2D" 는 **강제가 아니다**.

### 검증의 구멍

`validate()` 는 **첫 행의 타입만** 본다. 타입 혼합 검사는 별도 메서드
`validate_shapes_not_mixed_types()` 에 분리되어 있고, 비용(전체 `geom_type.unique()` 계산) 때문에
**기본 검증 경로에서 호출되지 않는다**. 즉 Point 로 시작해 Polygon 이 섞인 GeoDataFrame 은
`validate()` 를 통과한다. 규칙 위반이 조용히 넘어갈 수 있는 지점이라, 외부에서 만든 GeoDataFrame 을
넣을 때는 직접 호출해 확인하는 편이 낫다.

## 만드는 법: `ShapesModel.parse()`

입력 타입에 따라 `singledispatchmethod` 로 갈린다.

| 입력 | 필요한 인자 | 비고 |
|---|---|---|
| `GeoDataFrame` | — | **권장 경로**. `geometry` 컬럼 필수, Point 면 `radius` 필수 |
| `numpy.ndarray` | `geometry`(0/3/6), polygon 이면 `offsets`, circle 이면 `radius` | ragged array 표현에서 직접 초기화 |
| `str` / `Path` | circle 이면 `radius` | GeoJSON 파일. **최상위가 `GeometryCollection` 이어야 한다** |

공통 선택 인자: `index`, `transformations`.

```python
# circles — Xenium 리더의 실제 패턴: 면적에서 반지름 역산
radii = np.sqrt(adata.obs["cell_area"].to_numpy() / np.pi)
circles = ShapesModel.parse(xy, geometry=0, radius=radii,
                            transformations={"global": scale}, index=cell_ids)

# polygons — GeoDataFrame 경로
gdf = ShapesModel.parse(geo_df, transformations={"global": scale})

# ROI — GeoJSON 경로
sdata["my_rois"] = ShapesModel.parse("rois.geojson")
```

**좌표변환**: 아무것도 주지 않으면 `{"global": Identity()}` 가 자동으로 붙는다. 반대로 GeoDataFrame
의 `attrs` 와 `transformations` 인자에 **둘 다** 있으면 중복 지정으로 에러가 난다.
자세히는 [[Coordinate systems and transformations]].

**`index` 주의**: docstring 은 `str` 타입이어야 한다고 적지만 코드는 검사하지 않고, 실제로
[[Xenium]] 리더는 polygon 에 정수 인덱스를 쓴다.

## 디스크에 어떻게 쓰이나

`shapes/<이름>/` Zarr 그룹 하나가 element 하나. 내용은 포맷 버전에 따라 완전히 다르다.

### v0.2 · v0.3 (현행) — GeoParquet

```
shapes/<이름>/
├─ zarr.json (또는 .zattrs)   # spatialdata_attrs: {version}, coordinateTransformations, axes
└─ shapes.parquet             # GeoDataFrame 전체 (geometry + radius + 사용자 컬럼 + 인덱스)
```

- **`shapes.parquet` 은 Zarr 계층의 일부가 아니다.** zarr 는 group/array/메타데이터만 인식하므로,
  이 파일은 그룹 디렉토리 안에 얹혀 있을 뿐이다 — 코드 주석이 명시적으로 경고한다.
- geometry 인코딩은 `spatialdata.settings.shapes_geometry_encoding` 으로 정한다:
  `"WKB"`(기본) 또는 `"geoarrow"`.
- **좌표변환은 parquet 에 들어가지 않는다.** 쓰기 직전 `attrs["transform"]` 을 일시적으로 제거했다가
  복구하고, 변환은 zarr 그룹 메타데이터의 `coordinateTransformations` 로 따로 기록한다.
- 그룹 타입은 `"ngff:shapes"`.

### v0.1 (레거시) — ragged array

geopandas 없이 shapely 의 ragged array 표현을 zarr 배열로 풀어서 저장했다.

```
shapes/<이름>/
├─ coords          # 좌표 배열
├─ offset0, offset1, …   # polygon 경계 오프셋 (polygon 계열만)
├─ Index           # 인덱스 (문자열이면 VLenUTF8 코덱)
├─ radius          # POINT 일 때만
└─ .zattrs         # spatialdata_attrs: {geos: {name, type}, version}
```

geometry 타입이 `geos: {name, type}` 로 메타데이터에 박혀 있다 — v0.2 부터는 parquet 자체가
타입을 담으므로 이 메타데이터가 사라졌다. 읽기는 지금도 지원된다.

버전 체계 전반은 [[SpatialData Zarr format versions]].

## 관련 연산

- **표현 변환** — `to_circles()` / `to_polygons()` / `rasterize()` / `rasterize_bins()`:
  [[Rasterization and vectorization]]
- **집계** — `aggregate()`: [[Spatial aggregation]]
- **공간 질의** — `polygon_query()` / `bounding_box_query()`: [[Spatial queries in SpatialData]].
  Shapes 는 `sindex` R-tree 로 후보를 거른 뒤 `intersects` 로 판정한다 — **걸치기만 해도 포함**되고,
  `clip=True` 를 주면 circle 이 폴리곤으로 변환된 뒤 잘린다.
- **관계 질의** — `join_spatialelement_table()` / `get_values()`:
  [[Relational queries in SpatialData]]. Shapes 는 조인 5종을 모두 지원한다
  (단 `left_exclusive` 에 미해결 인덱스 버그가 있다).
- 기타: `get_centroids()`, `get_extent()`, `transform()`

주의: `to_polygons()`·`aggregate()`·`rasterize()` 는 모두 내부에서 circle 을 폴리곤으로
buffer 한다. 근사 품질이 `buffer_resolution`(기본 16)에 걸려 있다.

## 링크

- 상위: [[SpatialData elements]] · 프레임워크: [[SpatialData]]
- 좌표: [[Coordinate systems and transformations]]
- 저장: [[SpatialData Zarr format versions]] · 사양: [[OME-NGFF]]
- 이 형태를 만들어내는 리더: [[spatialdata-io]] → [[Visium]], [[Visium HD]], [[Xenium]], [[MERSCOPE]]
- 출처: [[SpatialData source - ShapesModel and shapes IO]], [[SpatialData docs - Design doc]]
- 영역 MOC: [[Bioinformatics]]

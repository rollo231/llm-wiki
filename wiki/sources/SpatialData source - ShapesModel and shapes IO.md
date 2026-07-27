---
type: source
title: SpatialData source - ShapesModel and shapes IO
area: [bioinformatics]
aliases: [ShapesModel source, spatialdata models.py, spatialdata format.py, io_shapes.py]
tags: [spatial-omics, data-model, geopandas, geoparquet, zarr, shapes, api]
created: 2026-07-27
updated: 2026-07-27
sources:
  - "https://github.com/scverse/spatialdata/blob/v0.8.0/src/spatialdata/models/models.py"
  - "https://github.com/scverse/spatialdata/blob/v0.8.0/src/spatialdata/_io/io_shapes.py"
  - "https://github.com/scverse/spatialdata/blob/v0.8.0/src/spatialdata/_io/format.py"
---

# SpatialData source - ShapesModel and shapes IO

## 인용

| 항목 | 값 |
|---|---|
| 출처 | `scverse/spatialdata` Python 패키지 소스 |
| 파일 | `src/spatialdata/models/models.py` (1389줄), `src/spatialdata/_io/io_shapes.py` (182줄), `src/spatialdata/_io/format.py` (448줄) |
| 버전 핀 | tag `v0.8.0` (2026-07-02 릴리스) |
| 라이선스 | BSD-3-Clause |
| 접근일 | 2026-07-27 |
| 표준 URL | https://spatialdata.scverse.org/en/stable/api/models.html · [`.../api/data_formats.html`](https://spatialdata.scverse.org/en/stable/api/data_formats.html) |

**왜 소스를 읽었나.** 사이트의 API 페이지가 이 내용의 표준 위치지만, 두 가지 이유로 문서를
직접 인제스트할 수 없다.

1. 렌더된 사이트는 Cloudflare 봇 차단(HTTP 429) — [[SpatialData docs - Design doc]] 때와 동일.
2. repo 의 `docs/api.md` 는 11줄짜리 toctree, `docs/api/models.md` 는 `.. autoclass:: ShapesModel`
   같은 autodoc 지시자뿐이다. **본문은 빌드 시점에 Python docstring 에서 생성**된다. 즉 API 페이지의
   실제 내용 = 이 소스 파일들. ([[spatialdata-io]] 문서도 같은 구조였다.)

## 요약

`Shapes` element 의 **계약**(무엇이 유효한 Shapes 인가)과 **저장 방식**(디스크에 어떻게 쓰이나)을
규정하는 세 파일. 파생 페이지는 [[SpatialData Shapes element]]와
[[SpatialData Zarr format versions]].

- `models.py` — 5개 element 모델(`Image2DModel`·`Image3DModel`·`Labels2DModel`·`Labels3DModel`·
  `ShapesModel`·`PointsModel`·`TableModel`)의 `validate()`/`parse()`. 이번엔 `ShapesModel` 중심으로 읽었다.
- `io_shapes.py` — `_read_shapes()` / `write_shapes()`. Zarr 그룹에 shapes 를 쓰고 읽는 실제 코드.
- `format.py` — element 종류별 포맷 버전 클래스 체계와 컨테이너-element 조합 제약.

## 핵심 takeaway

### 1. Shapes 는 두 형태뿐이고, 섞을 수 없다

`geometry` 컬럼에 `Point`(=circle) 또는 `Polygon`/`MultiPolygon` 만 올 수 있다. `parse()` 의
`geometry` 인자는 shapely 의 `GeometryType` 값을 그대로 쓴다 — `0: Circles`, `3: Polygon`,
`6: MultiPolygon`.

**circle 은 도형이 아니라 `Point` + `radius` 컬럼으로 표현된다.** 이것이 Visium spot 이나
Xenium `cell_circles` 가 저장되는 방식이다.

### 2. `validate()` 는 첫 행만 본다 — 타입 혼합은 잡히지 않는다

```python
geom_ = data[cls.GEOMETRY_KEY].values[0]
if not isinstance(geom_, Polygon | MultiPolygon | Point):
```

타입 혼합 검사는 **별도 메서드** `validate_shapes_not_mixed_types()` 에 있고, docstring 이 이유를
명시한다: *"This function is not called by ShapesModel.validate() because computing the unique
types by default could be expensive."* → 규칙상 금지지만 기본 검증 경로로는 통과할 수 있는
구멍이다.

### 3. `radius` 의 NaN/inf 는 다음 릴리스에서 에러로 승격 예정

현재는 `logger.warning`. 코드 주석이 못 박아 둔다: *"this warning will be turned into a ValueError
in the next code release"*. 과거에 저장된 [[Xenium]] 데이터를 읽을 때 뜰 수 있고,
[discussion #657](https://github.com/scverse/spatialdata/discussions/657) 로 안내한다. 음수·0 은
지금도 즉시 `ValueError`.

### 4. 3D geometry 는 에러가 아니라 경고

`geometry.iloc[0]._ndim != 2` 면 `UserWarning` + `force_2d()` 권고. 설계 문서의 "Shapes 는 2D"는
**강제가 아니라 권고**에 가깝다.

### 5. 좌표변환은 필수, 없으면 자동으로 채운다

`attrs["transform"]` 이 없거나 빈 dict 면 `validate()` 가 거부한다. 다만 `parse()` 를 거치면
`_parse_transformations()` 가 아무것도 안 준 경우 `{"global": Identity()}` 를 넣어준다. 반대로
element 의 attrs 와 `transformations` 인자에 **둘 다** 들어 있으면 에러 — 중복 지정 금지.

### 6. 온디스크: `shapes.parquet` 는 Zarr 계층의 일부가 아니다

`write_shapes()` docstring 이 명시한다:

> Note that the parquet file is not recognized as part of the zarr hierarchy as it is not a valid
> component of a zarr store, e.g. group, array or metadata file.

즉 `shapes/<name>/` 그룹 안에 zarr 가 모르는 파일이 하나 얹혀 있는 구조다.

또 하나: `to_parquet()` 호출 직전에 `attrs["transform"]` 을 **일시적으로 지웠다가 되돌린다**
(직렬화 문제 회피). 좌표변환은 parquet 이 아니라 zarr 그룹 메타데이터에 따로 쓰인다.

### 7. GeoParquet 인코딩은 설정으로 바뀐다

`spatialdata.settings.shapes_geometry_encoding` — `"WKB"`(기본) 또는 `"geoarrow"`.

## 발췌 (원문)

`ShapesModel` 의 키 정의:

```python
class ShapesModel:
    GEOMETRY_KEY = "geometry"
    GEOS_KEY = "geos"
    TYPE_KEY = "type"
    NAME_KEY = "name"
    RADIUS_KEY = "radius"
    TRANSFORM_KEY = "transform"
    ATTRS_KEY = ATTRS_KEY          # = "spatialdata_attrs"
```

포맷 버전 매핑 (`format.py`):

```python
CurrentRasterFormat = RasterFormatV03
CurrentShapesFormat = ShapesFormatV03
CurrentPointsFormat = PointsFormatV02
CurrentTablesFormat = TablesFormatV02
CurrentSpatialDataContainerFormat = SpatialDataContainerFormatV02
```

## 기존 페이지와의 관계

**모순은 없고, 두 군데를 확장한다.**

- [[SpatialData elements]] 의 "Shapes = (multi)polygon·circle, GeoDataFrame, 2D" 는 그대로 맞다.
  이 소스는 그 아래 층 — 필수 컬럼, 검증 규칙, 저장 레이아웃 — 을 채운다.
- [[SpatialData]] 의 "온디스크: Zarr + Parquet(points·shapes)" 도 맞다. 정확히는 Shapes 포맷
  **v0.2 이상**에서만 그렇고, v0.1 은 ragged array 를 zarr 배열로 직접 저장했다.

## 문서/코드 불일치

`docs/api/data_formats.md` (v0.8.0) 가 나열하는 클래스는 다음이 전부다:

```
CurrentRasterFormat, RasterFormatV01, CurrentShapesFormat,
ShapesFormatV01, ShapesFormatV02, CurrentPointsFormat,
PointsFormatV01, CurrentTablesFormat, TablesFormatV01
```

코드에 있으나 **문서에서 빠진 것**: `RasterFormatV02`, `RasterFormatV03`, `ShapesFormatV03`,
`PointsFormatV02`, `TablesFormatV02`, 그리고 `SpatialDataContainerFormatV01`/`V02` 전체.
하필 빠진 쪽이 대부분 **현행 포맷**이라, API 문서만 보면 Shapes 최신 포맷이 V02 라고 오해하게 된다.
[[spatialdata-io]] 에서 발견한 doc/code drift(`iss`·`macsima` 리더 누락)와 같은 패턴이다.

또 `ShapesModel.parse()` docstring 은 `index` 를 *"must be of type `str`"* 이라고 적지만, 코드는
`geo_df.index = index` 로 그대로 대입할 뿐 타입을 검사하지 않는다. 실제로 [[Xenium]] 리더는
polygon 에 정수 `label_index` 를 인덱스로 넣는다.

## 링크

- 파생 개념: [[SpatialData Shapes element]], [[SpatialData Zarr format versions]]
- 상위 개념: [[SpatialData elements]], [[Coordinate systems and transformations]]
- 프레임워크: [[SpatialData]] · 사양: [[OME-NGFF]]
- 이 계약을 지키는 리더: [[spatialdata-io]] → [[Visium]], [[Visium HD]], [[Xenium]], [[MERSCOPE]]
- 영역 MOC: [[Bioinformatics]]

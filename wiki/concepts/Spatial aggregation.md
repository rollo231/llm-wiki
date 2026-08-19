---
type: concept
title: Spatial aggregation
area: [bioinformatics]
aliases: [aggregate, spatialdata aggregate, 공간 집계, 영역별 집계]
tags: [spatial-omics, aggregation, geopandas, shapes, tables]
created: 2026-07-27
updated: 2026-08-19
sources: ["[[SpatialData source - Shapes conversion and aggregation ops]]"]
---

# Spatial aggregation

**"어떤 영역 안에 무엇이 얼마나 있는가"** 를 계산하는 연산. [[SpatialData]]의 `aggregate()` 는
`values`(집계할 것)를 `by`(영역)로 묶는다.

공간 오믹스에서 가장 흔한 용례가 이것이다 — transcript 점들을 세포 경계로 묶어 **cell × gene
행렬**을 만드는 일. [[Xenium]]·[[MERSCOPE]] 같은 in situ 기술의 표준 전처리 단계다.

```python
result = aggregate(values=sdata["transcripts"], by=sdata["cell_boundaries"],
                   value_key="feature_name", agg_func="count")
table = result.tables["table"]     # cell × gene
```

## 반환값이 표가 아니라 `SpatialData` 다

`aggregate()` 는 **`by` shapes 와 집계 table 을 함께 담은 새 `SpatialData` 객체**를 돌려준다.
표만 필요하면 `.tables` 에서 꺼내야 한다. 표는 이미 `by` 를 주석하도록 연결된 상태다 —
기본 `region_key="region"`, `instance_key="instance_id"` 로, [[spatialdata-io]] 의 관례와 같다.

반환된 shapes 는 기본적으로 원본의 **deepcopy** 다. 큰 multiscale labels 라면 `deepcopy=False` 로
lazy dask 표현을 유지하라고 docstring 이 권고한다.

## 지원하는 조합은 둘뿐

| `by` (영역) | `values` (집계 대상) |
|---|---|
| Shapes | Points 또는 Shapes |
| Labels 2D | Image 2D |

그 외는 `NotImplementedError`. 같은 element 를 자기 자신으로 집계하는 것도 미지원이다.

**Shapes 경로의 실제 동작**: 양쪽 모두 [[Rasterization and vectorization|`to_polygons()`]] 로
변환한 뒤 geopandas 로 조인한다. 즉 circle 은 `buffer_resolution`(기본 16) 만큼의 정확도로
다각형화된 다음 계산된다.

- `fractions=False` 이거나 values 가 점이면 → `sjoin()` (더 빠름)
- `fractions=True` 이고 values 가 폴리곤이면 → `overlay(how="intersection")`

## `value_key`: 무엇을 집계하는가

세 곳 중 어디든 가리킬 수 있다.

- dataframe 컬럼 (points 의 Dask DataFrame, shapes 의 GeoDataFrame)
- 연결된 table 의 `obs` 컬럼
- 연결된 table 의 `var` — 즉 `X` 행렬의 열

지정하지 않으면 **1로 채운 열**과 같아진다(= 개수 세기). points 의 경우
`attrs["spatialdata_attrs"]["feature_key"]`(보통 유전자 이름 컬럼)가 기본값으로 쓰인다.

`agg_func` 는 `pandas.DataFrame.groupby.agg` 로 넘어간다 — `"sum"`, `"mean"`, `"count"` 등.
(Labels × Image 경로는 대신 `xrspatial.zonal_stats` 로 간다.)

## `fractions`: 부분 겹침을 어떻게 셀 것인가

`by` 영역과 `values` 영역이 **일부만 겹칠 때**의 처리 방식이다.

- `False` (기본) — 겹치면 값을 통째로 센다.
- `True` — `교집합 면적 / values 영역 면적` 비율을 곱한다.

금지 조합이 명시돼 있다.

| 조합 | 왜 |
|---|---|
| `fractions=True` + points | 점은 면적이 0 → 전부 0이 된다 |
| `fractions=True` + categorical + `count` | 의미 없는 결과. `"sum"` 을 쓸 것 |
| categorical + `mean` | 의미 없는 결과 |

`fractions=False` 일 때는 categorical 에 대해 `count` 와 `sum` 이 같지만, `True` 면 달라진다.

## 알려진 제약

- **points → shapes 집계는 모든 점을 메모리에 올린다.** docstring 이 직접 경고하며
  [issue #210](https://github.com/scverse/spatialdata/issues/210) 을 가리킨다. 전사체 단분자
  규모에서는 실질적인 제약이다.
  - ⭐ **이 연산의 정체는 point-in-polygon 공간 조인이고, 그걸 하는 전용 엔진이 있다** —
    [[Apache Sedona]] / [[SedonaDB]]. 구조는 [[Spatial join execution]].
  - 🔄 **정정 (2026-08-19).** 이 항목의 초판은 *"SpatialData store를 직접 읽지 못하므로
    (Geo)Parquet 경유가 필요하다"* 고 적었다. **틀렸다** — `points.parquet`·`shapes.parquet`은
    **이미 Parquet/GeoParquet이라 엔진이 그대로 읽는다.** 리더 소스 확인 결과 좌표변환도 이
    연산에서는 상쇄된다. → [[SpatialData and Sedona interop]]
  - ✅ **실측 (2026-08-19)**: 32GB 워크스테이션, 셀 3,600 × 유전자 100 기준 —
    **1M**(0.86s / 829MB) → **5M**(3.8s / 2.8GB) → **20M**(19.7s / 9.0GB) → **50M**(94s / 10.6GB).
    ⭐ **20M→50M 에서 시간이 초선형으로 꺾인다**(데이터 2.5배에 시간 4.8배). 같은 구간에서 SedonaDB 는
    1.97s / 1.4GB 로 선형을 유지하고 **결과가 완전히 일치한다.**
    → [[SpatialData and Sedona interop]] §7 · `docs/experiments/spatialdata-sedona/`
  - ⚠️ **store 를 *쓰는* 것도 같은 벽이다** — 50M store 생성이 peak 9.6GB 를 썼다. 이 함수만의
    문제가 아니라 pandas 경로 전체가 그렇다.
  - **문턱**: 수백만 이하면 이 함수를 그대로 쓴다 → 수천만 이상이면
    [[SedonaDB]](클러스터 불필요) → 여러 store 를 가로지르면 SedonaSpark + 카탈로그.
  - ⚠️ **대신 잃는 것**: 좌표계 자동 정렬, circle 다각형화(`buffer_resolution`), `fractions`,
    `value_key` 3경로, `SpatialData` 객체 조립 — 전부 사용자 코드가 된다.
- 좌표계가 다르면 `target_coordinate_system`(기본 `"global"`)으로 양쪽을 먼저 `transform()` 한다.
  [[Coordinate systems and transformations]] 참고.
- 내부 예약 컬럼명: `__ones_column`, `__areas_column`, `__index`, `__ones_column_aggregate`.
  같은 이름이 데이터에 있으면 assert 로 막힌다.

## 다른 연산이 이 함수를 쓴다

`to_circles(labels)` 가 label 별 면적을 구할 때 `aggregate()` 를 호출한다 — 1로 채운 이미지를
labels 로 집계해 픽셀 수를 세는 방식. 표현 변환과 집계가 한 덩어리로 얽혀 있다는 신호다.

## 링크

- 분산 우회: [[SpatialData and Sedona interop]] · [[Spatial join execution]] · [[Apache Sedona]]
- 자매 연산: [[Rasterization and vectorization]]
- 대상: [[SpatialData Shapes element]], [[SpatialData elements]]
- 좌표: [[Coordinate systems and transformations]] · 프레임워크: [[SpatialData]]
- 적용 사례: [[Xenium]], [[MERSCOPE]], [[Visium HD]]
- 출처: [[SpatialData source - Shapes conversion and aggregation ops]]
- 영역 MOC: [[Bioinformatics]]

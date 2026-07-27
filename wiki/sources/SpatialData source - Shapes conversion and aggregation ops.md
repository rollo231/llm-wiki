---
type: source
title: SpatialData source - Shapes conversion and aggregation ops
area: [bioinformatics]
aliases: [spatialdata vectorize.py, spatialdata rasterize.py, spatialdata aggregate.py, rasterize_bins source]
tags: [spatial-omics, rasterization, vectorization, aggregation, datashader, shapes]
created: 2026-07-27
updated: 2026-07-27
sources:
  - "https://github.com/scverse/spatialdata/blob/v0.8.0/src/spatialdata/_core/operations/vectorize.py"
  - "https://github.com/scverse/spatialdata/blob/v0.8.0/src/spatialdata/_core/operations/rasterize.py"
  - "https://github.com/scverse/spatialdata/blob/v0.8.0/src/spatialdata/_core/operations/rasterize_bins.py"
  - "https://github.com/scverse/spatialdata/blob/v0.8.0/src/spatialdata/_core/operations/aggregate.py"
---

# SpatialData source - Shapes conversion and aggregation ops

## 인용

| 항목 | 값 |
|---|---|
| 출처 | `scverse/spatialdata` Python 패키지 소스, `src/spatialdata/_core/operations/` |
| 파일 | `vectorize.py` (302줄), `rasterize.py` (761줄), `rasterize_bins.py` (287줄), `aggregate.py` (493줄) |
| 버전 핀 | tag `v0.8.0` (2026-07-02 릴리스) |
| 라이선스 | BSD-3-Clause |
| 접근일 | 2026-07-27 |
| 표준 URL | https://spatialdata.scverse.org/en/stable/api/operations.html |

[[SpatialData source - ShapesModel and shapes IO]]와 같은 이유로 소스를 읽었다 — API 문서 페이지는
autodoc 스텁이고 본문은 docstring 에서 생성된다.

**범위**: `_core/operations/` 중 Shapes 와 직접 얽힌 4개. 같은 디렉토리의 `transform.py`(26KB)·
`map.py`(11KB)·`_utils.py`, 그리고 `_core/query/` 의 `spatial_query.py`(41KB)·
`relational_query.py`(48KB)는 **읽지 않았다** — 질의는 별개 개념이라 다음 인제스트로 미뤘다.

## 요약

Shapes 를 다른 표현으로 **바꾸는** 연산과, Shapes 를 기준으로 값을 **모으는** 연산.
파생 페이지는 [[Rasterization and vectorization]]과 [[Spatial aggregation]].

| 파일 | 공개 API | 한 줄 |
|---|---|---|
| `vectorize.py` | `to_circles`, `to_polygons` | 벡터 표현 사이 변환, 그리고 Labels → Shapes |
| `rasterize.py` | `rasterize` | 무엇이든 → Image/Labels. shapes·points 는 **datashader** 경유 |
| `rasterize_bins.py` | `rasterize_bins`, `rasterize_bins_link_table_to_labels` | 격자형 bin 전용 고속 경로 ([[Visium HD]]) |
| `aggregate.py` | `aggregate` | 영역(`by`)별로 값(`values`)을 집계 → `SpatialData` 반환 |

## 핵심 takeaway

### 1. 세 연산이 서로를 부른다

독립적인 API 처럼 보이지만 내부적으로 얽혀 있다.

- `to_circles(labels)` → **`aggregate()` 를 호출**해 각 label 의 픽셀 수(=면적)를 구한 뒤
  `r = √(area/π)` 로 반지름을 역산한다.
- `aggregate(values, by)` → 양쪽 모두 **`to_polygons()` 로 변환**한 뒤 geopandas 로 조인한다.
- `rasterize(shapes)` → datashader 에 넘기기 전에 **`to_polygons()`** 로 변환한다.

즉 **circle 은 어디서든 polygon 으로 buffer 된 뒤 계산된다.** 정확도가 `buffer_resolution`
(기본 16, `quad_segs`)에 달려 있다는 뜻이다.

### 2. `to_polygons()` 는 mixed-type 검사를 실제로 호출하는 드문 지점

[[SpatialData Shapes element]]에 적은 "검증의 구멍" — `ShapesModel.validate()` 는 첫 행만 본다 —
의 예외다. `to_polygons()` 의 GeoDataFrame 분기는 `ShapesModel.validate_shapes_not_mixed_types(gdf)`
를 명시적으로 부른다. 파서보다 이 변환 함수가 더 엄격하다.

(같은 분기에 중복된 `isinstance(..., Point)` 검사가 이중으로 들어가 있어 뒤쪽 `assert` 구문이
도달 불가능하다 — 동작에는 영향 없는 죽은 코드.)

### 3. Labels → Polygons 는 청크 병렬이고, 스레드가 아니라 프로세스를 원한다

`to_polygons(labels)` 는 dask 청크마다 skimage `regionprops` + `find_contours(mask, 0.5)` 로
윤곽을 따고, 청크 경계에 걸친 같은 label 조각을 `dissolve()` 로 합친다. docstring 이 명시적으로
권고한다:

> For optimal performance ... it is recommended to configure `Dask` to use 'processes' rather than
> 'threads'. `dask.config.set(scheduler='processes')`

**3D labels 는 `to_circles`·`to_polygons` 둘 다 미지원**(명시적 `RuntimeError`), Images 도 불가.

### 4. Points → Polygons 는 막혀 있고, 에러가 우회법을 알려준다

```
Cannot convert points to polygons. To overcome this you can construct circles from points
with `to_circles()` and then call `to_polygons()`.
```

`to_circles(points)` 는 `radius` 를 인자로 받거나 컬럼으로 갖고 있어야 한다.

### 5. `rasterize()` 는 기본적으로 Labels 를 Image 로 바꿔 버린다

`return_regions_as_labels` 기본값이 `False` 라, Labels 를 rasterize 하면 `(c,y,x)` **이미지**가
나온다. Labels 로 받으려면 명시해야 하고, 그때는 **uint16 제한(최대 65535)** 이 걸린다.
반환 라벨은 1부터 연속이고(0=배경), 원래 카테고리 매핑은
`returned.attrs["label_index_to_category"]` 에 실린다.

multiscale 입력은 **항상 single-scale 로 떨어진다.**

### 6. shapes·points 래스터화는 datashader 이고, 기본 reduction 이 타입마다 다르다

| `value_key` | 대상 | `return_single_channel` | datashader reduction |
|---|---|---|---|
| `None` | Points | — | `count` |
| `None` | Shapes | `True` | `first` |
| `None` | Shapes | `False` | `count_cat` |
| categorical | — | `True` / `False` | `first` / `count_cat` |
| int·float | — | — | `sum` |

Shapes 기본값이 `first` 인 이유: **인덱스를 categorical 로 해석해** 픽셀마다 겹치는 shape 중
하나를 고른다. 즉 기본 동작이 "세그멘테이션 마스크 만들기"다. `count_cat` 은 카테고리마다 채널을
분리하므로 `return_single_channel=True` 나 labels 반환과 함께 쓸 수 없다.

### 7. `rasterize_bins()` 는 Visium HD 격자의 회전을 affine 으로 되돌린다

docstring 이 못 박는다 — *"grid-like bins (e.g. Visium HD data, **but not Visium data**)"*.
[[Visium]] 의 spot 격자는 대상이 아니다.

bin 의 (row, col) 정수 인덱스에서 실제 좌표로 가는 affine 을, **무작위 20개 bin 을 뽑아
`skimage.transform.estimate_transform("affine")` 로 추정**한다(최소 6개 필요). Visium HD 격자가
살짝 회전돼 있기 때문이며, 추정된 변환이 결과 이미지를 원래 데이터 방향에 맞춰준다.

제약이 여럿이고 전부 에러로 막힌다: table 이 **단일 region** 만 주석해야 하고, `region_key` 는
**category dtype** 이어야 하며, sparse `X` 는 **`csc_matrix`** 여야 한다.

### 8. `aggregate()` 는 표가 아니라 `SpatialData` 를 반환한다

`by` shapes + 집계 결과 table 을 담은 새 `SpatialData` 객체다. 표만 원하면 `.tables` 로 꺼내야
한다. 지원 조합은 **둘뿐**:

- `by`=Shapes, `values`=Points | Shapes
- `by`=Labels2D, `values`=Image2D

그 외는 `NotImplementedError`. 자기 자신으로 집계하는 것도 미지원.

기본 `region_key="region"`, `instance_key="instance_id"` — [[spatialdata-io]] 의 관례와 일치한다
(설계 문서에서 "권장이지만 강제 아님"이라던 그 이름이 여기서는 기본값으로 박혀 있다).

### 9. points 를 shapes 로 집계하면 전부 메모리에 올라간다

docstring 이 직접 경고하고 [issue #210](https://github.com/scverse/spatialdata/issues/210) 을
가리킨다. 전사체 단분자 수준([[Xenium]]·[[MERSCOPE]])에서 실질적인 제약이다.

## 발췌 (원문)

`to_circles(labels)` 의 반지름 역산 — [[Xenium]] 리더가 손으로 하던 것과 같은 공식:

```python
aggregated = aggregate(values=ones, by=element_single_scale, agg_func="sum")["table"]
areas = aggregated.X.todense().A1.reshape(-1)
aobs["radius"] = np.sqrt(areas / np.pi)
```

`aggregate()` 의 조인 전략 선택:

```python
# when values are points, we need to use sjoin(); when they are polygons and fractions is True,
# we need to use overlay() also, we use sjoin() when fractions is False and values are polygons,
# because they are equivalent and I think that sjoin() is faster
if fractions is False or isinstance(values.iloc[0].geometry, Point):
    joined = by.sjoin(values)
else:
    overlayed = gpd.overlay(by, values, how="intersection")
```

## 기존 페이지와의 관계

**모순 없음.** 확장·확인되는 지점:

- [[SpatialData Shapes element]]의 "관련 연산" 목록이 이름만 있었는데 실제 동작으로 채워진다.
- [[Visium HD]]에 이미 적어 둔 `rasterize_bins()` 사용(`annotate_table_by_labels=True` 경로)의
  내부 동작과 제약이 드러난다.
- [[Xenium]] 리더가 `radius = √(cell_area/π)` 로 반지름을 만들던 것이 **라이브러리의 공식 근사와
  동일한 공식**임이 확인된다.
- [[Coordinate systems and transformations]]: 모든 연산이 `target_coordinate_system` 을 받고,
  필요하면 내부적으로 `transform()` 을 먼저 건다.

## 링크

- 파생 개념: [[Rasterization and vectorization]], [[Spatial aggregation]]
- 대상 element: [[SpatialData Shapes element]], [[SpatialData elements]]
- 좌표: [[Coordinate systems and transformations]] · 프레임워크: [[SpatialData]]
- 관련 플랫폼: [[Visium HD]], [[Xenium]], [[MERSCOPE]]
- 자매 소스: [[SpatialData source - ShapesModel and shapes IO]]
- 영역 MOC: [[Bioinformatics]]

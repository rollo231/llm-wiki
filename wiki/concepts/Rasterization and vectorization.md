---
type: concept
title: Rasterization and vectorization
area: [bioinformatics]
aliases: [rasterize, vectorize, to_circles, to_polygons, rasterize_bins, 래스터화, 벡터화]
tags: [spatial-omics, rasterization, vectorization, datashader, shapes, labels]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[SpatialData source - Shapes conversion and aggregation ops]]"]
---

# Rasterization and vectorization

[[SpatialData]]에서 **Labels(픽셀 마스크)** 와 **Shapes(벡터 도형)** 는 같은 영역을 다른 방식으로
표현한 것이고, 서로 변환할 수 있다. 변환하는 이유는 대개 **특정 기능을 쓰기 위해서, 또는 계산을
빠르게 하기 위해서**다.

```
Labels ──to_polygons()──▶ Shapes(Polygon)
Labels ──to_circles()───▶ Shapes(Circle)
Shapes ──rasterize()────▶ Image / Labels
Points ──to_circles()───▶ Shapes(Circle) ──to_polygons()──▶ Shapes(Polygon)
Points ──rasterize()────▶ Image / Labels
```

## 벡터화: `to_circles()` · `to_polygons()`

### `to_circles(data, radius=None)`

**면적을 보존하는 원 근사**다. 중심(centroid)과 면적을 구한 뒤 같은 면적의 원으로 바꾼다 —
`r = √(area / π)`.

| 입력 | 동작 |
|---|---|
| Labels 2D | 내부적으로 [[Spatial aggregation\|aggregate()]] 로 label 별 픽셀 수를 세어 면적을 구한다. 배경(0) 제외 |
| Shapes (Polygon) | `geometry.area` 로 계산 |
| Shapes (Point) | 그대로 반환 (이미 원) |
| Points | `radius` 인자 또는 `radius` 컬럼 **필수** |
| Labels 3D · Images | **미지원** — `RuntimeError` |

[[Xenium]] 리더가 `radius = √(cell_area/π)` 로 `cell_circles` 를 만드는 것과 **같은 공식**이다.

### `to_polygons(data, buffer_resolution=16)`

| 입력 | 동작 |
|---|---|
| Labels 2D | dask 청크별 skimage `regionprops` + `find_contours(0.5)`, 청크 경계에 걸친 label 은 `dissolve()` 로 병합 |
| Shapes (Point) | `buffer(radius, quad_segs=buffer_resolution)` 로 원을 다각형화 |
| Shapes (Polygon) | 그대로 반환 |
| Points | **불가** — `to_circles()` 를 먼저 거치라고 에러가 안내 |
| Labels 3D · Images | **미지원** |

- **성능**: Labels 변환은 `dask.config.set(scheduler='processes')` 권고 (docstring 명시).
  스레드 스케줄러로는 이득이 적다.
- **정확도**: `buffer_resolution` 이 원의 다각형 근사 품질을 정한다. 크면 정확하지만 폴리곤이
  복잡해지고 계산이 늘어난다.
- 이 함수는 [[SpatialData Shapes element#검증의 구멍|`validate_shapes_not_mixed_types()`]] 를
  실제로 호출한다 — 라이브러리에서 그 검사가 불리는 드문 지점이다.

**circle 은 결국 어디서든 polygon 이 된다.** `aggregate()` 도 `rasterize()` 도 내부에서
`to_polygons()` 를 거치므로, `buffer_resolution` 은 시각화뿐 아니라 **집계 결과의 정확도에도**
영향을 준다.

## 래스터화: `rasterize()`

```python
rasterize(data, axes, min_coordinate, max_coordinate, target_coordinate_system, ...)
```

바운딩 박스(`min`/`max` + `axes`)와 목표 해상도를 받아 격자로 굽는다. 해상도는
`target_unit_to_pixels` / `target_width` / `target_height` / `target_depth` 중 **정확히 하나**를
지정해야 한다.

입력에 따라 두 경로로 갈린다.

- **Images / Labels** → 리샘플링
- **Shapes / Points** → **datashader** 캔버스에 그리기

### 반환 타입이 함정이다

기본은 **항상 이미지** `(c, y, x)` 다. **Labels 를 rasterize 해도 기본값으로는 이미지가 나온다.**
Labels 로 받으려면 `return_regions_as_labels=True`:

- dtype 은 **uint16** — 라벨 최댓값 **65535 초과 시 에러**
- 라벨은 1부터 연속 (0 = 배경)
- 원래 카테고리 매핑은 `result.attrs["label_index_to_category"]`

multiscale 입력은 **항상 single-scale 로 떨어진다.** `SpatialData` 객체 전체를 넣으면 element 마다
`<이름>_rasterized_<타입>` 이름으로 새 객체가 나온다.

### 기본 집계 함수 (shapes·points)

| `value_key` | 대상 | `return_single_channel` | reduction |
|---|---|---|---|
| `None` | Points | — | `count` |
| `None` | Shapes | `True` (기본) | `first` |
| `None` | Shapes | `False` | `count_cat` |
| categorical | — | `True` / `False` | `first` / `count_cat` |
| int·float | — | — | `sum` |

- **Points 기본** = 픽셀별 점 개수. transcript 밀도 맵이 공짜로 나온다.
- **Shapes 기본** = shape 인덱스를 categorical 로 보고 `first` → 사실상 **세그멘테이션 마스크**.
- `count_cat` 은 카테고리마다 채널을 나누므로 `return_single_channel=True` 나 labels 반환과
  **함께 쓸 수 없다**(에러).

`agg_func` 로 직접 지정할 수 있는 값은 `sum`·`count`·`count_cat`·`first`.

## 격자 전용 고속 경로: `rasterize_bins()`

[[Visium HD]] 처럼 **격자로 배열된 bin** 을 픽셀 하나씩에 대응시킨다. docstring 이 명시한다 —
*"e.g. Visium HD data, **but not Visium data**"*. [[Visium]] 의 spot 격자는 대상이 아니다.

일반 `rasterize()` 와 다른 점: 공간 조인 없이 **(row, col) 정수 인덱스를 픽셀 좌표로 직접 사용**한다.
그래서 훨씬 빠르다. 대신 bin 격자가 실제 좌표계에서 살짝 회전돼 있으므로, **무작위 20개 bin
(최소 6개 필요)으로 `estimate_transform("affine")` 을 돌려 격자 → 실좌표 affine 을 추정**하고
결과 이미지의 좌표변환으로 심는다.

전제 조건 (전부 어기면 에러):

- table 이 **단일 region** 만 주석할 것
- `table.obs[region_key]` 가 **category dtype** 일 것
- table `obs` 에 행·열 정수 인덱스 컬럼이 있을 것
- sparse `X` 는 **`csc_matrix`** 일 것 (`table.X = table.X.tocsc()`)

`return_region_as_labels=True` 면 Labels 를 만든다. 이때 `instance_key` 를 0 을 피하고 연속이 되도록
relabel 해 `relabeled_<key>` 컬럼에 넣으므로, 이어서
`rasterize_bins_link_table_to_labels()` 로 table 의 주석 대상을 새 Labels 로 옮겨야 한다.

`value_key=None` 이면 모든 var 를 채널로 만들며, dask `map_blocks` 로 **lazy** 하게 구성된다.

> `spatialdata-plot` 으로 결과를 그릴 때는 `.render_shapes(scale='full')` 이 필요하다 —
> 안 그러면 자동 래스터화가 여기서 한 래스터화와 충돌한다.

## 왜 변환하는가

- **기능 잠금 해제**: 어떤 연산은 한쪽 표현만 받는다 (예: `aggregate` 의 `by`=Labels 경로는
  Image 값만 받는다).
- **속도**: 큰 폴리곤 집합보다 래스터가 빠른 연산이 있고, 반대도 있다.
- **시각화**: 수십만 개 폴리곤을 그리느니 래스터가 낫다.
- **표현 통일**: 여러 기술을 섞을 때 한쪽 표현으로 모으면 다루기 쉽다.

## 링크

- 대상: [[SpatialData Shapes element]], [[SpatialData elements]]
- 자매 연산: [[Spatial aggregation]]
- 좌표: [[Coordinate systems and transformations]] · 프레임워크: [[SpatialData]]
- 적용 사례: [[Visium HD]], [[Xenium]]
- 출처: [[SpatialData source - Shapes conversion and aggregation ops]]
- 영역 MOC: [[Bioinformatics]]

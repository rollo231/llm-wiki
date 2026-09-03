---
type: concept
title: Spatial queries in SpatialData
area: [bioinformatics]
aliases:
  - bounding_box_query
  - polygon_query
  - 공간 질의
  - SpatialData 공간 질의
  - BoundingBoxRequest
tags: [spatial-omics, query, dask, geopandas, xarray, performance]
created: 2026-07-27
updated: 2026-09-03
sources: ["[[SpatialData source - Spatial and relational queries]]"]
---

# Spatial queries in SpatialData

[[SpatialData]] 의 **공간 질의** — 영역을 주고 그 안의 데이터만 잘라낸다. 공개 API 는 두 개이고,
`SpatialData` 객체의 메서드로도 쓸 수 있다(`sdata.query.bounding_box(...)`, `sdata.query.polygon(...)`).

| 함수 | 질의 형태 |
|---|---|
| `bounding_box_query()` | 축정렬 bounding box (다중 box 지원) |
| `polygon_query()` | (multi)polygon |

둘 다 `SpatialData` 전체 또는 개별 element 에 쓸 수 있고, `singledispatch` 로 **element 종류마다 완전히
다른 구현**을 탄다. 이 갈래가 이 페이지의 핵심이다.

## 핵심: "청크 프루닝을 하는가"의 답이 종류마다 다르다

| element | 구현 | 실제로 I/O 가 주는가 |
|---|---|---|
| **Images·Labels** (`DataArray`/`DataTree`) | bbox 를 intrinsic 좌표로 역변환 → `slice` 생성 → `image.sel(selection)` | ✅ **예.** dask 기반 lazy 슬라이싱이라 교차 청크만 읽는다 |
| **Points** (`DaskDataFrame`) | **`points.compute()` 로 전량 materialize** 후 boolean mask | ❌ **아니오.** 전부 메모리에 올린다 |
| **Shapes** (`GeoDataFrame`) | `sindex.query(predicate="intersects")` — R-tree 공간 인덱스 | ⚠️ 인메모리 인덱스. Shapes 는 lazy loading 미구현이라 어차피 전량 메모리 |

> 📏 **오브젝트 스토리지에서 이 차이의 크기 (실측 2026-08-08 · 단일 노드 ·
> `docs/experiments/object-storage-bench/`)** — 4 MiB 객체에서 64 KiB range GET 은 full GET 대비
> **27.4배** 빠르다 (37.0 → 1012.3 op/s; MinIO 27.36 · RustFS 27.41 로 사실상 동일).
> ⭐ **읽는 바이트는 1/64 인데 처리량은 27배다** — 요청당 고정비가 남기 때문이다. 래스터의 청크
> 프루닝이 버는 것이 이 배수이고, 청크를 잘게 쪼갤수록 수익이 그 고정비 쪽으로 깎인다.

**즉 "공간 predicate pushdown"이라 부를 수 있는 건 래스터뿐이다.** docstring 도 인정한다:

> If the object has `points` element, depending on the number of points, it MAY suffer from
> performance issues. Please consider filtering the object before calling this function by calling
> the `subset()` method of `SpatialData`.

이건 [[Spatial aggregation|`aggregate()`]] 가 points 를 전부 메모리에 올리는 문제
([issue #210](https://github.com/scverse/spatialdata/issues/210))와 같은 패턴이다. 일반화하면:
**points 는 어느 경로로 접근하든 전량 메모리에 올라간다** — `aggregate()`, `bounding_box_query()`,
[[Relational queries in SpatialData|`get_values()`]] 셋 다 `.compute()` 를 부른다.

### v0.8.0 의 points 최적화는 I/O 최적화가 아니다

v0.8.0 에 "Speedup for bounding_box_query"(PR #1104)가 들어갔다. 실체는 **변환 종류별 fast path** 다.

- `is_identity_transform` — 항등 변환이면 좌표 투영을 통째로 건너뛴다.
- `is_scaling_transform` — 선형부가 대각(순수 스케일)이면, 전체 점을 affine 투영하는 대신
  **bbox 두 점만 역변환**해 intrinsic 공간에서 마스킹한다. 음수 스케일은 구간이 뒤집히므로
  `min`/`max` 를 다시 정렬한다.
- 그 외 일반 affine — 모든 점 좌표를 행렬곱으로 투영한 뒤 마스킹.

**`.compute()` 는 세 경로 모두에 그대로 있다.** 줄어든 것은 산술 비용이지 읽는 바이트가 아니다.

## `return_request_only` — 읽지 않고 "무엇을 읽을지"만 얻기

래스터 전용 인자다. `True` 면 실제 슬라이싱을 하지 않고 **`{axis: slice(...)}` 딕셔너리만 반환**한다.
질의가 건드릴 범위를 데이터를 읽지 않고 계산할 수 있다는 뜻이라, 비용 추정·질의 계획에 쓸 수 있다.
(`DataArray`·`DataTree` 에만 유효.)

## 회전이 있으면 래스터와 Shapes 의 의미가 달라진다

bbox 는 항상 element 의 **intrinsic 좌표계로 역변환**된 뒤 적용된다. 그런데 그 다음이 다르다.

- **래스터**: 역변환된 코너들의 **축정렬 min/max** 를 취해 `slice` 를 만든다 → 회전 변환에서는
  회전된 사각형의 외접 박스가 되어 **과선택(over-select)** 한다.
- **Shapes**: 역변환된 코너로 **실제 회전된 `Polygon`** 을 만들어 교차 판정한다 → 정확하다.

같은 인자로 같은 좌표계에 질의해도 element 종류에 따라 포함 범위가 달라질 수 있다.

## 지원되지 않는 변환 조합

`_get_case_of_bounding_box_query()` 가 (데이터 차원, 변환 rank, 출력 차원) 조합을 5가지 case 로 분류하고,
**가역 변환인 case 1(2D→2D)·case 5(3D→3D)만 구현되어 있다.** case 2·3·4 는 `ValueError` 로 거부된다 —
요컨대 **3D 데이터를 2D 로 투영하는 변환을 통한 질의는 불가능**하다. 설계 논의는
[PR #151 의 코멘트](https://github.com/scverse/spatialdata/pull/151#issuecomment-1444609101)에 있다.

축 개수가 안 맞으면 `_adjust_bounding_box_to_real_axes()` 가 조정한다: 2D 데이터에 3D bbox 를 주면
남는 축을 버리고, 3D 데이터에 2D bbox 를 주면 그 축을 `±(float32 최대값 − 1)` 로 채워 "전 범위"로
만든다.

## 함정

- **`polygon_query()` 를 이미지·라벨에 쓰면 폴리곤이 무시된다.** 구현이 폴리곤의 `.bounds` 를 뽑아
  `bounding_box_query()` 로 그대로 위임한다. **폴리곤 마스킹은 일어나지 않는다** — 외접 박스가
  돌아온다. Shapes·Points 는 정상적으로 폴리곤 교차를 쓴다.
- **좌표계 이름을 틀리면 조용히 빈 결과.** `_dict_query_dispatcher()` 는 target 좌표계에 매핑되지 않은
  element 를 **에러 없이 건너뛴다**. 오타 하나로 빈 `SpatialData` 를 받고도 아무 경고가 없다.
- **결과가 빈 element 는 아예 사라진다.** 질의 결과가 비면 `None` 이 되고 반환된 `SpatialData` 에서
  누락된다 — 키가 있는지 먼저 확인해야 한다.
- **경계 처리가 종류별로 불일치한다.** Points 마스크는 엄격 부등호 `(col > min) & (col < max)` 라
  **경계 위의 점이 빠지고**, Shapes 는 `predicate="intersects"` 라 **살짝 걸치기만 해도 포함**된다
  (완전 포함이 아니다).
- **`clip=True`(polygon_query)는 circle 을 폴리곤으로 변환한 뒤 자른다.** docstring 이 radius 에
  의존하는 다운스트림 연산과 성능에 영향을 준다고 경고한다. 기본값은 `False` — 즉 걸친 shape 은
  잘리지 않고 통째로 반환된다. `clip` 은 이미지·라벨·points 에서는 **무시**된다.
- **`filter_table=True`(기본값)가 v0.8.0 에서 테이블 행 순서를 바꾼다.** 다중 region 을 주석하는
  테이블에 한해서다 — [[Relational queries in SpatialData]] 의 리그레션 항목 참고. 공간 질의도
  이 경로를 타므로 그대로 영향을 받는다.

## 링크

- 관계 질의: [[Relational queries in SpatialData]]
- 프레임워크: [[SpatialData]] · 데이터 모델: [[SpatialData elements]]
- 좌표: [[Coordinate systems and transformations]] · Shapes: [[SpatialData Shapes element]]
- 관련 연산: [[Spatial aggregation]], [[Rasterization and vectorization]]
- 응용: [[SpatialData as a data engineering substrate]]
- 출처: [[SpatialData source - Spatial and relational queries]]
- 영역 MOC: [[Bioinformatics]]

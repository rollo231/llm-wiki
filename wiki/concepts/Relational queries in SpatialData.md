---
type: concept
title: Relational queries in SpatialData
area: [bioinformatics]
aliases:
  - join_spatialelement_table
  - get_values
  - match_table_to_element
  - filter_by_table_query
  - 관계 질의
  - SpatialData 조인
tags: [spatial-omics, query, join, anndata, relational, annsel]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[SpatialData source - Spatial and relational queries]]"]
---

# Relational queries in SpatialData

[[SpatialData elements]] 는 element 간 링크를 저장하지 않는다. `Tables` 만 예외적으로
`region`/`region_key`/`instance_key` 세 키로 Regions 를 가리키는데, 설계 문서는 이 관계가
**강제되지 않는다**고만 말한다. **관계 질의는 이 soft FK 를 실행 가능한 조인으로 만든 레이어다.**

조인 키는 양쪽이 다르다:

- **element 쪽** — 인덱스 (Shapes·Points 는 `.index`, Labels 는 픽셀의 고유 정수값)
- **table 쪽** — `region_key` 컬럼으로 어느 element 인지 고르고, `instance_key` 컬럼으로 어느 행인지

## SQL 식 조인 5종

`join_spatialelement_table(sdata, spatial_element_names, table_name, how=..., match_rows=...)`.
element 와 table 을 하나의 표로 합치지 **않는다** — 각각 필터된 상태로 튜플 `(element_dict, table)` 을
돌려준다. 원본은 수정하지 않는다.

| `how` | element 결과 | table 결과 |
|---|---|---|
| `left` (기본) | 그대로 | 매칭되는 행만 |
| `left_exclusive` | table 에 **없는** 인덱스만 | `None` |
| `inner` | 교집합 | 교집합 |
| `right` | table 에 있는 것만 | 그대로 |
| `right_exclusive` | `None` 처리 | 매칭 element 가 **없는** 행만 |

**Labels 는 `left` 와 `right_exclusive` 만 지원**된다(docstring 명시). `left_exclusive` 는 Labels 를
경고와 함께 건너뛴다. Labels 에서 배경 라벨 `0` 은 항상 결과에서 빠진다.

### `match_rows` — 필터링과 별개의 "행 순서 맞추기"

`'no'`(기본)·`'left'`·`'right'`. 필터가 아니라 **순서 정렬**을 제어한다. 조합이 안 맞으면
(예: `how='right'` 에 `match_rows='left'`) 경고만 내고 무시한다. 자주 쓰는 조합에 편의 함수가 있다.

| 편의 함수 | 실제 호출 |
|---|---|
| `match_table_to_element()` | `how='left'`, `match_rows='left'` — 테이블을 element 순서에 맞춤 |
| `match_element_to_table()` | `how='right'`, `match_rows='right'` — element 를 테이블 순서에 맞춤 |
| `match_sdata_to_table()` | `SpatialData` 전체를 테이블에 맞춰 필터 (기본 `how='right'`) |

## `filter_by_table_query()` — `WHERE` 절에 가장 가까운 것

`annsel` 라이브러리(`table.an.filter(...)`)의 Predicate 로 테이블의 `obs`·`var`·`X`·`obs_names`·
`var_names` 에 조건을 걸고, **그 결과를 공간 element 로 전파**한다(내부적으로 `match_sdata_to_table`).

```python
sdata.filter_by_table_query(table_name="table", obs_expr=...)   # 메서드로도 제공
```

선언적 술어로 테이블을 거르면 대응하는 shape·point·label 이 함께 걸러진다는 뜻이라, 이 프레임워크에서
관계형 필터에 가장 근접한 물건이다. 대신 `annsel` 이라는 추가 의존성을 끌어온다.

## `get_values()` — 값이 어디 있든 찾아온다

`value_key` 하나를 주면 네 곳 중 어디에 있든 찾아 `DataFrame` 으로 돌려준다.

| origin | 어디 |
|---|---|
| `df` | Shapes·Points 의 자체 컬럼 |
| `obs` | table 의 `obs` 컬럼 |
| `var` | table 의 `var_names` → 즉 `X`(또는 지정 `layer`)의 발현값 |
| `obsm` | table 의 `obsm` 키 |

계약이 엄격하다 — **여러 곳에서 발견되면 에러**(모호성을 통과시키지 않는다), **아무 데서도 못 찾아도
에러**. 한 번의 호출에서 **origin 을 섞을 수 없고**, categorical 과 non-categorical 도 섞을 수 없다.
반환 `DataFrame` 의 인덱스는 해당 element 에 대한 table 의 `instance_key` 다.

성능 주의 두 가지: `df` origin 이 `DaskDataFrame` 이면 `.compute()` 한다. `var` origin 은 sparse
행렬을 `.todense()` 로 펼치므로 **유전자를 많이 지정하면 메모리가 터진다**.

## 보조 함수

- `get_element_annotators(sdata, element_name)` → 그 element 를 주석하는 **테이블 이름 집합**.
  포맷이 저장하지 않는 링크를 런타임에 역방향으로 찾는 방법이다.
- `get_element_instances(element)` → element 의 인덱스. **Labels 는 `da.unique()` 로 전체 배열을
  스캔**한다 — 소스 주석이 "can be slow" 라고 적어둔 지점이다.

## 함정

### v0.8.0 리그레션 — 테이블 행 순서가 조용히 바뀐다 (issue #1162, 미해결)

**다중 region 을 주석하는 테이블을 필터하면 `obs` 행이 region 별로 재정렬된다.** interleaved 였던
`a,b,a,b,…` 가 `a,a,…,b,b,…` 로 뭉친다. 원인은 PR #1131(v0.8.0 의 관계 질의 리팩터)이
`_filter_table_by_elements` 를 순서 보존 boolean mask 에서 `join_spatialelement_table(how="left")` 로
바꾼 것 — left join 이 내부에서 `obs.groupby(region_key)` 를 한다.

**[[Spatial queries in SpatialData|공간 질의도 이 경로를 탄다]]**: `bounding_box_query`·`polygon_query`
의 `filter_table` 기본값이 `True` 이기 때문이다. 테이블 행과 지오메트리의 위치 대응을 가정하는
코드에서는 조용한 데이터 오류가 된다.
([issue #1162](https://github.com/scverse/spatialdata/issues/1162))

### `filter_label_pixels` 의 기본값이 요청을 무시한다

`right`·`inner` 조인에서 Labels 를 다룰 때 쓰는 3-상태 인자다.

| 값 | 동작 |
|---|---|
| `True` | 테이블에 없는 instance id 의 **픽셀을 0 으로** 만든다 |
| `None` (**기본**) | **필터하지 않고 경고만** 낸다 |
| `False` | 필터하지 않고 조용히 넘어간다 |

즉 **기본값으로 inner join 을 하면 라벨 픽셀은 하나도 걸러지지 않는다.** 경고를 억제하는
파이프라인에서는 필터된 줄 알고 전체 마스크를 쓰게 된다.

켜더라도 비싸다: `get_element_instances()` 로 전체 라벨 배열을 스캔해 instance 목록을 뽑고,
`xr.apply_ufunc(..., dask="parallelized", allow_rechunk=True)` 로 지운다. **3D 라벨은
`NotImplementedError`.**

### `left_exclusive` 인덱스 버그 (issue #824, 미해결)

`left_exclusive` 만 다른 조인들과 달리 **instance_key 값을 위치 인덱스로 사용**한다.

```python
mask = np.full(len(element), True, dtype=bool)
mask[table_instance_key_column.values] = False   # 값을 위치로 취급
```

`instance_id` 가 `0..n-1` 인 [[spatialdata-io]] 관례에서는 우연히 맞지만, [[Xenium]] 처럼 임의의
cell id 를 쓰면 엉뚱한 행을 지우거나 `IndexError` 가 난다.
([issue #824](https://github.com/scverse/spatialdata/issues/824))

### 그 밖에

- **주석하지 않는 element 를 넘기면 경고 후 건너뛴다** — 에러가 아니다.
- **Images 와 Tables 는 조인 대상이 될 수 없다** (`ValueError`). Tables 가 Tables 를 주석할 수 없다는
  [[SpatialData elements]] 의 규칙과 일관된다.
- 참조 정합성을 검사하는 공식 수단은 **아직 없다** —
  [issue #218](https://github.com/scverse/spatialdata/issues/218) 이 `validate_data_relationships()`
  를 제안한 게 2023-04-05 이고 여전히 미해결이다. 검증이 필요하면 직접 써야 한다
  ([[SpatialData as a data engineering substrate]] §5 에 그 검사 목록을 옮겨 뒀다).

## 링크

- 공간 질의: [[Spatial queries in SpatialData]]
- 데이터 모델: [[SpatialData elements]] (Table 의 세 키) · [[SpatialData Shapes element]]
- 관련 연산: [[Spatial aggregation]]
- 프레임워크: [[SpatialData]] · 리더 관례: [[spatialdata-io]]
- 응용: [[SpatialData as a data engineering substrate]]
- 출처: [[SpatialData source - Spatial and relational queries]]
- 영역 MOC: [[Bioinformatics]]

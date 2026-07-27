---
type: source
title: SpatialData source - Spatial and relational queries
area: [bioinformatics]
aliases:
  - spatial_query.py
  - relational_query.py
  - SpatialData query 소스
  - SpatialData 질의 소스
tags: [spatial-omics, query, join, dask, geopandas, anndata, source-code]
created: 2026-07-27
updated: 2026-07-27
sources:
  - "raw/bioinformatics/spatialdata-docs/src-query_spatial--v0.8.0.py"
  - "raw/bioinformatics/spatialdata-docs/src-query_relational--v0.8.0.py"
  - "https://github.com/scverse/spatialdata/tree/v0.8.0/src/spatialdata/_core/query"
---

# SpatialData source - Spatial and relational queries

**출처:** [[SpatialData]] `v0.8.0` 패키지 소스 `src/spatialdata/_core/query/` 2개 파일.
저장소 <https://github.com/scverse/spatialdata> · **버전 핀 `v0.8.0`** (2026-07-02 릴리스,
**접근일 2026-07-27 기준 최신 태그**) · 로컬 스냅샷
`raw/bioinformatics/spatialdata-docs/src-query_{spatial,relational}--v0.8.0.py`.

| 파일 | 줄 수 | 공개 API |
|---|---|---|
| `spatial_query.py` | 975 | `bounding_box_query`, `polygon_query` |
| `relational_query.py` | 1,156 | `join_spatialelement_table`, `match_table_to_element`, `match_element_to_table`, `match_sdata_to_table`, `filter_by_table_query`, `get_values`, `get_element_annotators`, `get_element_instances` |

API 문서(`docs/api/*.md`)는 autodoc 스텁이라 내용이 없다 — 소스가 SoT다. 이 인제스트로 [[Bioinformatics]]
MOC의 "공간·관계 질의는 이름만 파악됨" 열린 질문이 닫힌다.

## 요점

- **`bounding_box_query()`는 element 종류마다 완전히 다른 구현으로 갈린다.** 그리고 그중
  **raster만 실제로 I/O를 줄인다.** 자세히는 [[Spatial queries in SpatialData]].
- **`polygon_query()`를 이미지·라벨에 쓰면 폴리곤이 무시되고 bounding box가 적용된다.**
- **관계 질의는 SQL식 조인 5종을 제공한다** — [[SpatialData elements]]가 "강제되지 않는다"고만
  적었던 `region`/`region_key`/`instance_key` soft FK 위에 실행 가능한 조인 레이어가 얹혀 있다.
  자세히는 [[Relational queries in SpatialData]].
- **`filter_by_table_query()`** 가 `annsel` 의존성으로 obs/var/X 에 predicate 필터를 걸고 그 결과를
  공간 element 로 전파한다 — 이 프레임워크에서 `WHERE` 절에 가장 가까운 물건.
- **v0.8.0 에서 관계 질의가 리팩터되었고(PR #1131), 그 리팩터가 리그레션을 낳았다** (아래 참고).

## 신선도·품질 주의

이 버전에서 확인된 문제 3건. 전부 **미해결(open)** 이다.

### 1. v0.8.0 리그레션 — 테이블 행 순서가 조용히 바뀐다 (issue #1162)

**가장 중요한 발견.** PR #1131(v0.8.0 의 "Refactor relational queries")이 `_filter_table_by_elements`
를 순서 보존 boolean mask 에서 `join_spatialelement_table(how="left")` 로 바꿨다. left join 은 내부에서
`obs.groupby(region_key)` 를 하므로, **여러 region 을 주석하는 테이블을 필터하면 obs 행이 region 별로
재정렬된다.** 원래 순서가 interleaved(`a,b,a,b,…`)였다면 `a,a,…,b,b,…` 로 뭉친다.

소스에서 경로가 그대로 확인된다: `_filter_table_by_elements`(`relational_query.py:123-159`) →
`_left_join_spatialelement_table` → `obs.groupby(by=region_column_name, observed=False)`
(`relational_query.py:446`).

**공간 질의가 이걸 상속한다.** `bounding_box_query`·`polygon_query` 의 `filter_table` 기본값이 `True`
이고, 그 경로가 `_get_filtered_or_unfiltered_tables` → `_filter_table_by_elements` 다. 즉
**기본 설정으로 공간 질의를 하면 다중 region 테이블의 행 순서가 바뀐다.** 테이블 행과 element
지오메트리의 위치 대응을 가정하는 코드에서는 조용한 데이터 오류가 된다.

[issue #1162](https://github.com/scverse/spatialdata/issues/1162) (2026-07-10 등록 — v0.8.0 릴리스
8일 뒤). `spatialdata-plot` 테스트의 순서 단언을 깨뜨려 발견됐다.

### 2. `left_exclusive` 조인의 인덱스 버그 (issue #824)

`_left_exclusive_join_spatialelement_table`(`relational_query.py:414-415`)만 다른 조인들과 다르게
**instance_key 값을 위치 인덱스로 사용**한다.

```python
mask = np.full(len(element), True, dtype=bool)
mask[table_instance_key_column.values] = False   # 값을 위치로 취급
```

같은 파일의 다른 조인은 전부 `np.isin(table_instance_key_column.values, element_indices)` 를 쓴다.
`instance_id` 가 `0..n-1` 인 [[spatialdata-io]] 관례에서는 우연히 맞지만, [[Xenium]] 처럼 임의의
cell id 를 쓰면 엉뚱한 행을 마스킹하거나 `IndexError` 가 난다.

[issue #824](https://github.com/scverse/spatialdata/issues/824) (2025-01-13 등록, 미해결). 위키에서
코드 대조로 먼저 의심한 뒤 업스트림에서 확인한 건이다.

### 3. Python 3.13 핫픽스가 남긴 느슨한 검사 (issue #852)

`_call_join`(`relational_query.py:705-708`)에 주석 달린 우회가 있다. `JoinTypes.__members__` 가
Python 3.13 에서 비어서, 원래의 `how in JoinTypes.__dict__["_member_names_"]` 대신
`how in JoinTypes.__dict__` 를 쓴다. 후자는 Enum 의 멤버가 아닌 속성 이름도 통과시키므로 검사가
느슨해졌다. [issue #852](https://github.com/scverse/spatialdata/issues/852).

## 관련 업스트림 이슈 (이 소스를 읽으며 확인)

- [#218](https://github.com/scverse/spatialdata/issues/218) — *Method to validate the relationship
  between elements* (2023-04-05, **미해결**). `validate_data_relationships()` 제안. element 간
  참조 정합성 검사가 **프레임워크에 없다는 사실이 3년 넘게 업스트림에서 인정된 상태**임을 보여준다.
  제안된 검사 목록이 구체적이라 그대로 파이프라인 검증에 옮길 수 있다 —
  [[SpatialData as a data engineering substrate]] §5 에 반영했다.
- [#1130](https://github.com/scverse/spatialdata/issues/1130) — points·shapes 인덱스의 유일성이
  명확히 규정되지 않았다.
- [#210](https://github.com/scverse/spatialdata/issues/210) — `aggregate()` 가 points 를 전부
  메모리에 올린다. 이번 인제스트로 **같은 패턴이 질의 경로에도 있음**이 확인됐다.

## 모순

기존 페이지와 충돌하는 사실은 없었다. 다만 **[[SpatialData as a data engineering substrate]] 의
서술 하나를 정정**해야 했다: 그 노트는 "청크 프루닝 = 공간 predicate pushdown"을 포맷 전반의
성질처럼 적었는데, 소스 확인 결과 **raster 에만 해당**하고 points 는 정반대(전량 materialize)다.
해당 노트 §1·§2·§5·§8 을 이 인제스트에 맞춰 갱신했다.

## 링크

- 개념: [[Spatial queries in SpatialData]], [[Relational queries in SpatialData]]
- 프레임워크: [[SpatialData]] · 데이터 모델: [[SpatialData elements]]
- 좌표: [[Coordinate systems and transformations]]
- 관련 연산: [[Spatial aggregation]], [[Rasterization and vectorization]]
- 응용: [[SpatialData as a data engineering substrate]]
- 영역 MOC: [[Bioinformatics]]

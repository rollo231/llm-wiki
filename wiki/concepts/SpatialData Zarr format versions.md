---
type: concept
title: SpatialData Zarr format versions
area: [bioinformatics]
aliases: [SpatialData format, ShapesFormat, RasterFormat, spatialdata_format_version, 포맷 버전]
tags: [spatial-omics, zarr, ome-ngff, data-format, versioning]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[SpatialData source - ShapesModel and shapes IO]]"]
---

# SpatialData Zarr format versions

[[SpatialData]] 의 온디스크 포맷은 **하나의 버전이 아니다**. element 종류마다 독립적으로 버전이
매겨지고, 그 위에 컨테이너(`SpatialData` 객체 자체) 버전이 하나 더 있다. 전부
`ome_zarr.format.Format` 의 서브클래스로 구현된다 — 즉 [[OME-NGFF]] 버전을 상속받고 그 위에
SpatialData 고유 버전을 얹는 이중 구조다.

목적은 **하위 호환**이다. major 변경이 생겨도 옛 store 를 읽을 수 있도록, 버전별 클래스를 남겨 둔다.

## 버전 표 (v0.8.0 기준)

| element 종류 | SpatialData 버전 | 상속한 NGFF 포맷 | NGFF 버전 문자열 | 현행 |
|---|---|---|---|---|
| **raster** (images·labels) | 0.1 | `FormatV04` | `0.4` | |
| | 0.2 | `FormatV04` | `0.4-dev-spatialdata` | |
| | 0.3 | `FormatV05` | `0.5-dev-spatialdata` | ✅ |
| **shapes** | 0.1 | `FormatV04` | | ragged array 저장 |
| | 0.2 | `FormatV04` | | GeoParquet 도입 |
| | 0.3 | `FormatV05` | | ✅ |
| **points** | 0.1 | `FormatV04` | | |
| | 0.2 | `FormatV05` | | ✅ |
| **tables** | 0.1 | `FormatV04` | | |
| | 0.2 | `FormatV05` | | ✅ |
| **container** (`SpatialData`) | 0.1 | `FormatV04` | | |
| | 0.2 | `FormatV05` | | ✅ |

`FormatV04` → Zarr v2, `FormatV05` → Zarr v3 계열이다. 그래서 **각 element 종류의 최신 버전은
일제히 Zarr v3 로 넘어간 세대**이고, 컨테이너 v0.2 가 그 세대를 묶는다.

`-dev-spatialdata` 접미사는 의도적이다: NGFF 사양에 아직 병합되지 않은 PR 위에 만들어진
확장이라는 신호다 (raster 의 경우
[PR #849](https://github.com/scverse/spatialdata/pull/849)). 같은 이유로 라이브러리는
`ome_zarr.format.format_implementations` 를 **몽키패치**해 자기 포맷 클래스를 끼워 넣는다.

## 컨테이너 버전이 element 버전을 제약한다

아무 조합이나 되는 게 아니다.

| 컨테이너 | 허용되는 element 포맷 |
|---|---|
| **V01** | raster 0.1·0.2 · shapes 0.1·0.2 · points 0.1 · tables 0.1 |
| **V02** | raster 0.3 · shapes 0.3 · points 0.2 · tables 0.2 |

즉 **세대를 섞을 수 없다**. 컨테이너 V01 을 지정하고 element 포맷을 안 주면 각각
raster 0.2 / shapes 0.2 / points 0.1 / tables 0.1 로 기본값이 채워진다. 위반하면 쓰기 시점에
허용 목록을 나열한 `ValueError` 가 난다.

## 버전이 디스크 어디에 적히나

element 그룹의 메타데이터 안, `spatialdata_attrs` 키 아래:

```json
{ "spatialdata_attrs": { "version": "0.3" } }
```

(`ATTRS_KEY = "spatialdata_attrs"`.) 읽을 때 `_parse_version()` 이 이 값을 뽑아
`ShapesFormats["0.3"]` 처럼 포맷 클래스를 되찾고, 그에 맞는 읽기 경로를 고른다. 모르는 버전이면
*"Please update the spatialdata library"* 로 거부한다.

컨테이너 쪽은 추가로 `spatialdata_software_version` (패키지 `__version__`)을 남긴다 — 포맷 버전과
**별개**다. 포맷은 그대로여도 라이브러리 버전은 계속 오른다.

## 실무적 함의

- **store 를 읽는 쪽에서 "SpatialData 포맷 버전"을 하나로 물으면 답이 없다.** element 종류별로
  확인해야 한다.
- 옛 store 는 읽히지만, 새로 쓰면 현행 포맷으로 나간다 — round-trip 이 포맷을 조용히 올린다.
  구버전 라이브러리와 파일을 주고받는다면 `formats=` 인자로 명시적으로 낮춰 써야 한다.
- shapes 0.1 → 0.2 가 특히 큰 단절이다: zarr 배열 여러 개 → `shapes.parquet` 한 개.
  자세히는 [[SpatialData Shapes element]].

## 문서에서 빠진 부분

v0.8.0 의 `docs/api/data_formats.html` 는 `RasterFormatV02`·`RasterFormatV03`·`ShapesFormatV03`·
`PointsFormatV02`·`TablesFormatV02` 와 컨테이너 포맷 전체를 나열하지 않는다. 하필 **현행 포맷들이
빠져 있어서**, 문서만 보면 shapes 최신이 V02 라고 오해하게 된다. 이 페이지는 소스 기준이다.

## 링크

- 프레임워크: [[SpatialData]] · 사양: [[OME-NGFF]]
- element: [[SpatialData elements]], [[SpatialData Shapes element]]
- 좌표변환 저장: [[Coordinate systems and transformations]]
- 출처: [[SpatialData source - ShapesModel and shapes IO]]
- 영역 MOC: [[Bioinformatics]]

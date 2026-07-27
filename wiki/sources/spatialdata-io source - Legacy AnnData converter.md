---
type: source
title: spatialdata-io source - Legacy AnnData converter
area: [bioinformatics]
aliases:
  - from_legacy_anndata
  - to_legacy_anndata
  - legacy_anndata.py
  - 레거시 AnnData 컨버터
tags: [spatial-omics, anndata, scanpy, squidpy, legacy, source-code, converter]
created: 2026-07-27
updated: 2026-07-27
sources:
  - "raw/bioinformatics/spatialdata-io/src-converter_legacy_anndata--v0.7.1.py"
  - "https://github.com/scverse/spatialdata-io/blob/v0.7.1/src/spatialdata_io/converters/legacy_anndata.py"
---

# spatialdata-io source - Legacy AnnData converter

**출처:** [[spatialdata-io]] `v0.7.1` 소스 `src/spatialdata_io/converters/legacy_anndata.py` (366줄).
저장소 <https://github.com/scverse/spatialdata-io> · **버전 핀 `v0.7.1`** (2026-07-02 릴리스) ·
**접근일 2026-07-27** · 로컬 스냅샷
`raw/bioinformatics/spatialdata-io/src-converter_legacy_anndata--v0.7.1.py`.

`spatialdata_io.experimental` 로 공개되는 두 함수 — `from_legacy_anndata()`, `to_legacy_anndata()`.
"레거시(legacy) spatial AnnData" 는 Scanpy 와 **구버전 Squidpy** 가 쓰던 h5ad 관례를 말한다.

이 파일을 읽은 이유: **[[SpatialData]] 가 왜 필요한지**를 가장 구체적으로 보여주는 자료이기 때문이다.
컨버터의 코드가 곧 레거시 관례의 명세이고, 그 변환이 무엇을 잃는지가 곧 새 프레임워크의 존재 이유다.
정리 → [[Legacy AnnData spatial convention]].

## 요점

- **컨버터가 읽고 쓰는 키가 레거시 관례의 전부다** — `obsm["spatial"]` 하나와
  `uns["spatial"][dataset_id]` 아래의 이미지·스케일팩터. 그 외에 공간 정보가 들어갈 자리가 없다.
- **`obsm["spatial"]` 은 언제나 점(중심좌표)일 뿐이다.** 복원 시
  `ShapesModel.parse(xy, geometry=0, radius=radius)` 로 **circle** 이 된다 (`geometry=0` = Point).
  반지름조차 거기 없어서 `uns[...]["scalefactors"]["spot_diameter_fullres"]` 에서 가져오고,
  **없으면 기본값 10 을 쓰며 경고**한다.
- **역방향 변환이 손실적이다.** `to_legacy_anndata()` 는 주석 그대로
  *"convert polygons, multipolygons and labels to circles"* — `to_circles()` 로 전부 뭉갠다.
  docstring 도 *"Labels will be approximated to circles by using the centroids of each label and an
  average approximated radius"* 라고 명시한다.
- **레거시에는 "표가 어느 기하를 가리키는가" 라는 개념이 없다.** `from_legacy_anndata()` 는 그래서
  관계를 **발명한다** — region 이름을 `"locations"` 로 짓고 `region_key='region'`·
  `instance_key='instance_id'` 컬럼을 새로 만들어 붙인다.
- 라이브러리 스스로 권하지 않는다: *"Using this format for any new package is not recommended."*

## 핵심 발췌

레거시 → SpatialData 복원부. 읽는 키가 이게 전부다.

```python
SPATIAL = "spatial"
SCALEFACTORS = "scalefactors"
TISSUE_HIRES_SCALEF = "tissue_hires_scalef"
TISSUE_LOWRES_SCALEF = "tissue_lowres_scalef"
SPOT_DIAMETER_FULLRES = "spot_diameter_fullres"
IMAGES, HIRES, LOWRES = "images", "hires", "lowres"

# SpatialData 쪽에서 새로 만들어 붙이는 것 (레거시에 없던 개념)
REGION       = "locations"
REGION_KEY   = "region"
INSTANCE_KEY = "instance_id"
SPOT_DIAMETER_FULLRES_DEFAULT = 10
```

```python
if SPATIAL in adata.obsm:
    xy = adata.obsm[SPATIAL]
    radius = spot_diameter_fullres / 2
    shapes[REGION] = ShapesModel.parse(xy, geometry=0, radius=radius, ...)
    #                                      ^^^^^^^^^^ Point → circle. 폴리곤은 불가능.
```

SpatialData → 레거시. 기하가 뭉개지는 지점:

```python
# convert polygons, multipolygons and labels to circles
shapes = to_circles(element)
...
adata.obsm["spatial"] = get_centroids(sdata_post_rasterize[region_name],
                                      coordinate_system=coordinate_system).compute().values
```

## 그 밖에 확인된 제약 (`to_legacy_anndata` docstring)

- 표는 **Shapes 또는 Labels 하나만** 주석할 수 있다. 여러 Shapes 를 가리키면 `ValueError` — 미리
  하나로 합쳐야 한다. Points 는 아예 불가.
- 좌표계에 속하지 않는 표 행과, 표에 주석되지 않는 shape 행은 **버려진다**.
- `include_images=True` 는 권장되지 않는다. 이미지를 2000×2000(hires)·600×600(lowres)로 렌더링해
  넣는데, 원점이 (0,0)으로 리셋되고 다운스케일 오차가 크다
  ([issue #165](https://github.com/scverse/spatialdata/issues/165), 미해결). Squidpy 의
  `ImageContainer` 는 쓰지 않는다.
- 이미지들의 위치가 서로 많이 떨어져 있으면 공통 bounding box 로 렌더링되면서 **빈 공간이 대부분**이
  된다.

## 모순

없음 — 기존 페이지와 충돌하지 않는다. 오히려 [[SpatialData elements]] 에 이미 기록된 설계 문서 문장
(*"`Tables` 는 좌표계를 가질 수 없다. 표에 공간 좌표를 넣어둘 수는 있지만 라이브러리가 처리하지
않는다"*)이 **무엇을 겨눈 말인지** 확인됐다: 정확히 이 `obsm["spatial"]` 관례다.

## 링크

- 정리: [[Legacy AnnData spatial convention]]
- 라이브러리: [[spatialdata-io]] · 프레임워크: [[SpatialData]]
- 데이터 모델: [[SpatialData elements]], [[SpatialData Shapes element]]
- 좌표: [[Coordinate systems and transformations]]
- 영역 MOC: [[Bioinformatics]]

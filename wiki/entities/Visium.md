---
type: entity
title: Visium
area: [bioinformatics]
aliases: [10x Visium, Visium Spatial Gene Expression, 비지움]
tags: [spatial-transcriptomics, spatial-omics, 10x-genomics, array-based]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[spatialdata-io docs - README and readers]]"]
---

# Visium

10x Genomics의 **spot 기반**(array-based) 공간 전사체 플랫폼. 조직 슬라이드 위의 규칙적인
spot 격자에서 mRNA를 포집하므로, 측정 단위가 세포가 아니라 **spot**이다.

[[SpatialData]]에서는 spot을 **원(circle) Shapes**로 표현한다 — [[SpatialData elements]]에서
"배열 기반 기술 대부분을 Shapes로 표현할 수 있다"고 한 그 사례다. 후속 세대는 [[Visium HD]].

## SpatialData로 읽기

[[spatialdata-io]]의 `visium()`. 출처: 리더 소스 v0.7.1.

**읽는 파일** — Space Ranger 출력

| 파일 | 역할 |
|---|---|
| `(<id>_)filtered_feature_bc_matrix.h5` | counts + 메타데이터 (대안: `raw_feature_bc_matrix.h5`) |
| `spatial/tissue_positions_list.csv` (SpaceRanger 1) 또는 `spatial/tissue_positions.csv` (2) | spot 위치 |
| `spatial/scalefactors_json.json` | spot 지름, hires/lowres 스케일 계수 |
| `spatial/tissue_hires_image.png` · `tissue_lowres_image.png` | 축소 이미지 |
| (선택) `fullres_image_file` | Space Ranger 입력으로 쓴 원본 현미경 이미지 |

**만드는 element**

- **Shapes** 1개 — spot 원. 반지름 = `spot_diameter_fullres / 2`, 인덱스 = `spot_id`.
- **Table** 1개 — `AnnData`. `region` = `dataset_id`, `region_key` = `"region"`,
  `instance_key` = `"spot_id"`(0..N-1). 좌표는 `obsm["spatial"]`에도 남긴다(legacy squidpy 호환).
- **Images** — `<id>_full_image`(있을 때, 4단 피라미드) · `<id>_hires_image` · `<id>_lowres_image`.

**좌표계 3개**

`<dataset_id>` · `<dataset_id>_downscaled_hires` · `<dataset_id>_downscaled_lowres`.

spot 원은 세 좌표계 모두에 매핑된다(원본엔 Identity, 나머지엔 해당 scale). 축소 이미지는 반대로
**자기 좌표계엔 Identity, 원본 좌표계엔 scale의 역변환**을 갖는다. 결과적으로 어느 좌표계에서
봐도 spot과 이미지가 겹친다. [[Coordinate systems and transformations]]의 extrinsic 좌표계
활용 예시.

## 실무 함정

- **`dataset_id` 추론 실패**: counts 파일명에서 `<library_id>_` 접두사를 떼어 추론한다. 파일을
  리네임했거나 `.mtx` 형식이면 추론이 깨지므로 `dataset_id`를 직접 넘겨야 한다. `dataset_id`와
  추론된 `library_id`가 다르면 경고를 내고 `dataset_id`를 쓴다.
- **SpaceRanger 버전 차이**: 위치 파일명이 다르고, SpaceRanger < 2.0인데 헤더가 있는 변종도
  존재해 리더가 첫 행을 보고 분기한다.
- **`.btf` 이미지**: `dask_image`가 인식하지 못해 `imageio`로 우회하고, 축 순서를 shape로 추론한다
  (채널 축은 크기가 가장 작은 축으로 판정). OME 메타데이터가 없어 생기는 한계라고 주석에 명시.

## 링크

- 다음 세대: [[Visium HD]]
- 리더: [[spatialdata-io]]
- 데이터 모델: [[SpatialData elements]], [[Coordinate systems and transformations]]
- 출처: [[spatialdata-io docs - README and readers]]

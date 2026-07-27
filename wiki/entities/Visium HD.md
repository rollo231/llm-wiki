---
type: entity
title: Visium HD
area: [bioinformatics]
aliases: [10x Visium HD, VisiumHD, visium_hd, 비지움 HD]
tags: [spatial-transcriptomics, spatial-omics, 10x-genomics, array-based, binning]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[spatialdata-io docs - README and readers]]"]
---

# Visium HD

10x Genomics의 고해상도 후속 플랫폼. [[Visium]]의 spot 격자 대신 **2µm 정사각형 bin** 격자를
쓰고, 분석 편의를 위해 여러 bin 크기(2 / 8 / 16µm …)로 집계한 결과를 함께 제공한다. 최근
버전은 **세포·핵 세그멘테이션 결과**까지 출력한다.

[[spatialdata-io]]의 리더 4개 중 가장 복잡하다 — bin 크기가 여러 개이고, 세그멘테이션 출력이
선택적이며, CytAssist 이미지 정렬이 투영 변환을 요구한다.

## SpatialData로 읽기

`visium_hd()`. 출처: 리더 소스 v0.7.1.

**bin 크기마다 별도 element 쌍**

각 `square_XXXum` 디렉토리에서 shapes 1개 + table 1개를 만든다. `bin_size`로 일부만 고를 수
있고, 기본은 존재하는 전부.

- **Shapes**: 기본값 `bins_as_squares=True` — 원을 만든 뒤 `buffer(radius, cap_style=3)`으로
  **정사각형화**한다. bin은 실제로 사각형이므로 올바른 시각화를 위해 이쪽이 기본이다.
- **Table**: `region` = `<dataset_id>_square_XXXum`, `instance_key` = bin 인덱스.
- `annotate_table_by_labels=True`면 bin을 `rasterize_bins()`로 래스터화해 **Labels**도 만들고
  table을 그쪽에 연결한다. 이 경로는 bin 격자의 미세한 회전을 affine으로 추정해 보정한다 —
  전제 조건과 동작은 [[Rasterization and vectorization]] 참고. ([[Visium]]의 spot 격자는
  이 고속 경로의 대상이 아니다.)

**세그멘테이션 출력** (`segmented_outputs/`가 있을 때)

- 세포: cell GeoJSON + `filtered_feature_cell_matrix.h5` → 별도 Shapes + Table.
- 핵: `load_nucleus_segmentations=True`일 때만. **2µm bin 카운트를 `barcode_mappings.parquet`로
  집계**해 "세그멘트된 핵 아래의 bin만" 각 세포 카운트에 기여하도록 만든다.
- ⚠️ **`load_segmentations_only` 기본값이 향후 `True`로 바뀐다.** 지금 미지정이면
  `FutureWarning`이 뜬다 — `True`(세그멘테이션만) / `False`(binned만, 기존 동작) 중 하나를
  명시하는 게 안전하다.

**Images** — `_full_image`(피라미드) · `_hires_image` · `_lowres_image`, 그리고
`load_all_images=True`일 때 `_cytassist_image`. 좌표계 구성은 [[Visium]]과 같은 3중 구조.

## CytAssist 이미지: 투영 변환 우회

기록해 둘 가치가 있는 실전 사례다. CytAssist 이미지를 현미경 좌표에 맞추려면 **projective
(투영) 변환**이 필요한데, [[Coordinate systems and transformations]]에서 정리한 대로
[[SpatialData]]는 affine까지만 지원한다.

리더의 해법: 투영 행렬을 **affine 성분 + projective shift로 분해**하고,

- projective shift는 skimage `warp`로 **픽셀을 실제로 구워버린다**(이미지 데이터를 변형),
- 남은 affine만 SpatialData 좌표변환으로 심는다.

즉 프레임워크가 표현할 수 없는 변환은 데이터에 미리 적용해 표현 가능한 범위로 끌어내린다.
CytAssist 이미지가 작고 단일 스케일이라 메모리에서 계산할 수 있어 성립하는 전략이다.
(투영 행렬이 이미 affine이면 분해 없이 그대로 심는다.)

## 실무 함정

- **파일 포맷 버전**: `"1.0"`만 검증하고 그 외는 경고만 낸다 — 새 포맷은 조용히 어긋날 수 있다.
- **Visium HD 3.0.0에는 `segmented_outputs/` 폴더가 없다.** 리더가 `scalefactors` 파일을
  하위 디렉토리 전체에서 다시 찾아 대응한다.
- **full-resolution 이미지 자동 탐색**: 여러 개 찾으면 첫 번째를 쓰고 경고, 못 찾으면 경고만
  내고 넘어간다 → `fullres_image_file`을 명시하는 편이 안전.
- `gex_only` 기본값이 `False`다 ([[Xenium]] 리더는 `True`) — 유전자 발현 외 feature type이
  섞여 들어올 수 있다.

## 링크

- 이전 세대: [[Visium]]
- 리더: [[spatialdata-io]]
- 데이터 모델: [[SpatialData elements]], [[Coordinate systems and transformations]]
- 연산: [[Rasterization and vectorization]], [[Spatial aggregation]]
- 출처: [[spatialdata-io docs - README and readers]],
  [[SpatialData source - Shapes conversion and aggregation ops]]

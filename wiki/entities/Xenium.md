---
type: entity
title: Xenium
area: [bioinformatics]
aliases: [10x Xenium, XOA, Xenium Onboard Analysis, Xenium Explorer, 제니움]
tags: [spatial-transcriptomics, spatial-omics, 10x-genomics, in-situ, single-molecule]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[spatialdata-io docs - README and readers]]"]
---

# Xenium

10x Genomics의 **in situ** 공간 전사체 플랫폼. [[Visium]] 계열의 격자 포집과 달리 개별 전사체
분자의 위치를 직접 이미징하므로, 측정 단위가 **단분자(transcript)**이고 세포는 세그멘테이션으로
얻는다. 출력 분석 소프트웨어는 **XOA**(Xenium Onboard Analysis), 뷰어는 **Xenium Explorer**.

[[spatialdata-io]]의 리더 중 만드는 element 종류가 가장 많다 — [[SpatialData elements]] 5종이
전부 등장한다.

## SpatialData로 읽기

`xenium()`. 출처: 리더 소스 v0.7.1.

**만드는 element**

| element | 이름 | 내용 |
|---|---|---|
| Labels | `cell_labels`, `nucleus_labels` | 래스터 세그멘테이션 마스크 (`cells.zarr.zip` 안) |
| Shapes | `cell_boundaries`, `nucleus_boundaries` | 경계 폴리곤 (parquet) |
| Shapes | `cell_circles` | 선택 — 중심 + 면적에서 계산한 반지름(√(area/π)) |
| Points | `transcripts` | 단분자 좌표 xyz + `feature_name`(gene) + `cell_id` |
| Table | `table` | `AnnData` — cell feature matrix + 세포 메타데이터 |
| Images | `morphology_focus`, `morphology_mip` | 형태 이미지. mip은 XOA < 2.0.0 에만 |
| Images | `he_image`, `if_image` | 정렬된 H&E · IF 이미지 (있을 때 자동 탐색) |

**분석에는 폴리곤이 아니라 래스터를 쓸 것** — 리더 docstring이 명시한다. 폴리곤 버전은 시각화용으로
단순화되어 있다. 기본값도 이를 반영해 `cells_as_circles=False`이고, table은 `cell_labels`를
annotate하도록 매핑된다.

**좌표**: micron 단위 데이터에 `1/pixel_size` scale을 걸어 픽셀 좌표계로 보낸다 — 모두
`"global"` 좌표계 하나에 모인다([[Coordinate systems and transformations]]의 기본 좌표계).

## XOA 버전별 포맷 차이

`cells.zarr.zip`의 구조가 XOA 버전마다 다르다. 리더는 `polygon_sets`·`seg_mask_value`의 존재
여부로 감지하며(둘은 상호 배타), **다핵세포 표현 가능 여부가 갈리므로 분석 결과에 영향을 준다.**

| XOA | `cell_id` 인코딩 | 라벨↔세포 매핑 | 다핵세포 / 핵 없는 세포 |
|---|---|---|---|
| **< 1.3.0** | 평범한 정수 배열 | 없음 (parquet에서 직접 읽음) | 표현 불가 |
| **1.3.0 – 1.x** | `(N,2) uint32` prefix/suffix → `aaaaficg-1` 같은 문자열 | `seg_mask_value` (세포만) | **세포:핵 1:1을 암묵 가정** |
| **2.0.0+** | 동일 | `polygon_sets/{0,1}/cell_index` | 지원 — 한 세포가 폴리곤 여럿을 가질 수 있고, 핵 없는 세포는 항목 자체가 없음 |

- 마스크 인덱스 0 = 핵, 1 = 세포. 래스터 라벨 값은 폴리곤 위치 + 1 (배경 0).
- `cell_summary`는 전 버전에 존재하되 v2.0.0+에서 `nucleus_count` 열이 추가된다.
- ⚠️ **v2.0.0 초기 빌드**: parquet에 `label_id` 열이 없어 다핵세포의 핵들이 하나의 퇴화 폴리곤으로
  병합된다. 리더는 **핵 경계를 아예 스킵**하고 경고와 함께 `spatialdata.to_polygons()`로 래스터에서
  유도하라고 안내한다.
- `xeniumranger`로 재세그멘테이션하면 `specs`에 `xenium_ranger` 항목이 생기고, 버전 분기는
  원래 `analysis_sw_version` 대신 그 값을 따른다.

## 유틸리티 함수

- **`xenium_aligned_image(image_path, alignment_file)`** — Xenium 좌표에 정렬된 추가 이미지(H&E·IF)를
  읽는다. 정렬 CSV가 있으면 Affine, 없으면 이미 정렬된 것으로 보고 Identity. H&E로 판정되면 채널명을
  `r`/`g`/`b`(`a`)로 붙인다. 축 순서 추론이 실패하는 경우 `dims`를 직접 넘긴다.
- **`xenium_explorer_selection(path)`** — Xenium Explorer의 Freehand/Rectangular 선택을 내보낸 CSV를
  shapely `Polygon`으로 바꾼다. 픽셀 좌표계(= Xenium의 `"global"`) 폴리곤 질의에 바로 쓸 수 있다.
  `pixel_size` 기본값 **0.2125 µm**. 여러 개 선택했으면 리스트로 반환.

## 실무 함정

- **버전 간 동작 변경 (spatialdata-io v0.6.0 이전)**: `cells_as_circles`가 기본 `True`였고, table이
  원/폴리곤 중 어디에 붙는지가 그 값에 따라 달랐으며, 원 반지름을 **핵** 면적으로 계산했다. 지금은
  **세포** 면적 기준. 과거 스크립트를 재실행하면 결과가 달라진다.
- **Protein 데이터**: HDF5에 고정소수점 스케일이 적용되어 있어 리더가 `protein_scaling_factor`로
  되돌린다.
- **성능**: `cells_as_circles=True`로 하면 시각화가 빨라지지만 정확도를 잃는다.
- `n_jobs`는 폐기됨(shapes 읽기가 빨라져 병렬화 불필요).
- 리더는 `cell_id` 일관성을 zarr·parquet·h5 사이에서 **샘플링 비교**로 교차 검증하고, 어긋나면
  "지원되지 않는 새 버전일 수 있다"는 경고를 낸다 — 이 경고가 뜨면 결과를 신뢰하기 전에 확인해야 한다.

## 링크

- 리더: [[spatialdata-io]]
- 같은 회사 플랫폼: [[Visium]], [[Visium HD]]
- 데이터 모델: [[SpatialData elements]], [[Coordinate systems and transformations]]
- 출처: [[spatialdata-io docs - README and readers]]

---
type: entity
title: MERSCOPE
area: [bioinformatics]
aliases: [Vizgen MERSCOPE, MERFISH, merscope, VPT, 머스코프]
tags: [spatial-transcriptomics, spatial-omics, vizgen, in-situ, single-molecule]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[spatialdata-io docs - README and readers]]"]
---

# MERSCOPE

Vizgen의 **in situ** 공간 전사체 플랫폼으로, MERFISH(multiplexed error-robust FISH) 화학을
사용한다. [[Xenium]]과 같은 단분자 계열 — 전사체 위치를 직접 검출하고 세포는 세그멘테이션으로
얻는다. 후처리 도구는 **VPT**(Vizgen post-processing tool).

## SpatialData로 읽기

[[spatialdata-io]]의 `merscope()`. 출처: 리더 소스 v0.7.1.

**읽는 파일**

| 파일 | 역할 |
|---|---|
| `detected_transcripts.csv` | 전사체 좌표 (global x/y/z) + gene |
| `cell_by_gene.csv` | counts |
| `cell_metadata.csv` | 세포별 메타데이터 |
| `cell_boundaries.parquet` | 세포 경계 폴리곤 |
| `images/mosaic_<stain>_z<N>.tif` | stain × z-layer별 모자이크 이미지 |
| `images/micron_to_mosaic_pixel_transform.csv` | **micron → 픽셀 변환 행렬** |

**만드는 element**

- **Points** `<id>_transcripts` — 좌표 x/y/z, `feature_key`는 gene(categorical로 변환).
- **Shapes** `<id>_polygons` — 세포 경계. 모두 `MultiPolygon`으로 통일한다.
- **Table** `table` — `region_key`/`instance_key`를 VPT 규약 열로 채우고, `region`은
  `<id>_polygons`를 가리킨다. `obs`에 `region`·`slide`·`dataset_id`를 함께 심는다.
- **Images** `<id>_z<N>` — z-layer별 이미지. **채널 좌표가 stain 이름**이 된다(`c_coords=stainings`).
  기본 청크 `(1, 4096, 4096)`, 4단 피라미드.

`dataset_id`는 `<slide_name>_<region_name>`으로 조합되며, 미지정 시 경로에서 유추한다(region은
디렉토리명, slide는 부모 디렉토리명).

**좌표**: `micron_to_mosaic_pixel_transform.csv`에서 읽은 **Affine을 `"global"` 좌표계에 적용**한다.
[[Visium]]처럼 좌표계를 여러 개 만들지 않고 하나로 모으는 방식.

## 알아둘 동작

- **z-layer 기본값은 중간층 하나(`z_layers=3`)**다. 전체 z를 원하면 리스트로 넘기고,
  `None`이면 이미지를 아예 읽지 않는다.
- **백엔드 2종**: `rioxarray`(RAM 절약) vs `dask_image`. 명시하지 않으면 `rioxarray`가 설치돼
  있을 때만 그것을 쓴다 — 즉 **같은 코드가 환경에 따라 다른 경로를 탄다**.
- **blank probe는 발현 행렬에서 분리된다.** 열 이름에 `blank`가 들어간 것은 `adata.X`에서 빼고
  `obsm["blank"]`에 따로 담는다. MERFISH의 대조 프로브를 품질 관리용으로 남기되 분석 행렬은
  오염시키지 않는 처리.
- **경계 중복·불량 제거**: `z_index == 0`인 것만 남겨 z별 중복 폴리곤을 제거하고, 유효하지 않은
  geometry는 버린다.
- **VPT 출력 지원**: `vpt_outputs`에 폴더를 주면 `cellpose_micron_space.parquet` 또는
  `watershed_micron_space.parquet` 중 존재하는 쪽을 자동으로 고른다. dict로 파일별 경로를 직접
  지정할 수도 있다.
- 각 구성요소는 `transcripts` · `cells_boundaries` · `cells_table` · `mosaic_images` 플래그로
  개별 on/off 할 수 있고, 파일이 없으면 경고만 내고 해당 element를 건너뛴다.

## 링크

- 리더: [[spatialdata-io]]
- 같은 단분자 계열: [[Xenium]]
- 데이터 모델: [[SpatialData elements]], [[Coordinate systems and transformations]]
- 출처: [[spatialdata-io docs - README and readers]]

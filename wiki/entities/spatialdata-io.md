---
type: entity
title: spatialdata-io
area: [bioinformatics]
aliases: [spatialdata_io, SpatialData IO, spatialdata-io readers]
tags: [spatial-omics, spatial-transcriptomics, scverse, python, data-loading]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[spatialdata-io docs - README and readers]]", "https://spatialdata.scverse.org/projects/io/en/stable/"]
---

# spatialdata-io

[[SpatialData]] 에코시스템의 **리더 라이브러리**. 상용 공간 오믹스 장비의 출력 디렉토리를
`SpatialData` 객체로 변환하는 함수 모음이다. 설계 문서에서 P0으로 지정된 위성 프로젝트이며,
"[[SpatialData]] 본체는 포맷 컨버터가 아니다"는 non-goal을 떠받치는 자리 — 변환 로직을 여기로
격리한다.

버전: **v0.7.1** (2026-07-02). `pip install spatialdata-io` 또는 conda-forge.

## 리더의 공통 형태

리더 4개를 읽어 확인한 공통 골격. 어느 리더를 보든 이 순서다.

1. 출력 디렉토리에서 규약된 파일명을 찾는다 (없으면 경고 후 스킵하거나 예외).
2. 각 파일을 `Image2DModel` · `Labels2DModel` · `ShapesModel` · `PointsModel` · `TableModel`의
   `.parse()`에 넘겨 [[SpatialData elements]]로 만든다 — 이때 좌표변환을 함께 심는다.
3. `SpatialData(images=…, labels=…, points=…, shapes=…, tables=…)`로 조립한다.
4. `_set_reader_metadata(sdata, "<reader>")`로 어느 리더가 만들었는지 기록한다.

즉 리더는 **"장비 출력 → element dict" 변환기**이고, 도메인 지식은 대부분 *어떤 파일이 어떤
element가 되는지*와 *좌표를 어떻게 맞추는지*에 들어 있다.

### element 이름 규약이 갈린다

- **`dataset_id` 접두사**: [[Visium]], [[Visium HD]], [[MERSCOPE]] — `<dataset_id>_full_image` 식.
- **고정 이름**: [[Xenium]] — `cell_labels`, `transcripts`, `morphology_focus` 식.

여러 샘플을 하나의 `SpatialData`에 합칠 때 Xenium은 **이름 충돌 위험**이 있다. 직접 이름을
바꿔줘야 한다.

## 지원 기술 (v0.7.1)

| 기술 | 리더 | 위키 페이지 |
|---|---|---|
| 10x Genomics Visium | `visium` | [[Visium]] |
| 10x Genomics Visium HD | `visium_hd` | [[Visium HD]] |
| 10x Genomics Xenium | `xenium` | [[Xenium]] |
| Vizgen MERSCOPE (MERFISH) | `merscope` | [[MERSCOPE]] |
| Akoya PhenoCycler (구 CODEX) | `codex` | — |
| NanoString CosMx | `cosmx` | — |
| Curio Seeker | `curio` | — |
| DBiT-seq | `dbit` | — |
| Spatial Genomics GenePS (seqFISH) | `seqfish` | — |
| STOmics Stereo-seq | `stereoseq` | — |
| MACSima | `macsima` | — |
| MCMICRO (파이프라인 출력) | `mcmicro` | — |
| Steinbock (파이프라인 출력) | `steinbock` | — |

포맷 무관 리더도 있다: `generic`, `image`, `geojson`.

## 리더 외: 레거시 AnnData 컨버터

`spatialdata_io.experimental` 에 리더가 아닌 것도 있다.

- `from_legacy_anndata(adata)` / `to_legacy_anndata(sdata, ...)` — Scanpy·구버전 Squidpy 가 쓰던
  `obsm["spatial"]` + `uns["spatial"]` 관례와의 양방향 다리. **왕복이 손실적**이다(폴리곤이 circle 로
  뭉개진다). 이 컨버터가 [[SpatialData]] 가 왜 필요한지를 가장 구체적으로 보여주는 자료라
  따로 정리했다 → [[Legacy AnnData spatial convention]].
- `iss` — In Situ Sequencing 리더(실험 단계).

**문서/코드 불일치**: 소스 트리에는 `iss.py`(In Situ Sequencing)·`macsima.py`가 있으나
`docs/api.md`의 리더 목록에는 둘 다 없다. 반면 README는 MACSima를 지원 목록에 넣는다. 문서가
코드에서 생성되는데도 목록이 어긋난 상태다 — 버전이 올라가면 재확인할 지점.

## 3rd-party 리더

`spatialdata-io`에 없지만 다른 라이브러리로 `SpatialData`로 읽을 수 있는 것들.

- **METASPACE**(MALDI 등) — [metaspace-converter](https://github.com/metaspace2020/metaspace-converter)
- **PhenoCycler · MACSima · Hyperion**(Imaging Mass Cytometry) — [SOPA](https://github.com/gustaveroussy/sopa)

## 실무 주의

- **파싱 후 Zarr로 쓰고 다시 읽어야 한다.** 리더가 반환한 객체를 그대로 쓰면 SpatialData Zarr
  포맷의 성능 이점이 없다. "시각화가 느리다"는 대표 증상.

  ```python
  from spatialdata_io import xenium
  from spatialdata import read_zarr

  sdata = xenium("raw_data")
  sdata.write("data.zarr")
  sdata = read_zarr("data.zarr")
  ```

  (README 원문 예제는 `data.zarr`로 쓰고 `sdata.zarr`를 읽는 오타가 있다. 위 코드가 맞다.)
- **정확성 보장이 없다.** 커뮤니티 관리 라이브러리이며 각 장비사의 공식 승인을 받지 않았다고
  명시한다. 장비 포맷이 바뀌면 리더가 뒤처질 수 있으니, 데이터 표현이 이상하면 버그로 신고하라는
  입장. 실무에서는 **리더가 만든 element를 한 번 눈으로 확인하는 습관**이 필요하다는 뜻.
- **알려진 한계**: Stereo-seq은 7.x만 지원(8.x 미지원).

## 링크

- 프레임워크: [[SpatialData]]
- 데이터 모델: [[SpatialData elements]], [[Coordinate systems and transformations]]
- 기술: [[Visium]], [[Visium HD]], [[Xenium]], [[MERSCOPE]]
- 레거시 관례: [[Legacy AnnData spatial convention]]
- 출처: [[spatialdata-io docs - README and readers]],
  [[spatialdata-io source - Legacy AnnData converter]]
- 영역 MOC: [[Bioinformatics]]

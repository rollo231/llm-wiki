---
type: source
title: spatialdata-io docs - README and readers
area: [bioinformatics]
aliases: [spatialdata-io README, spatialdata-io reader sources, spatialdata-io v0.7.1]
tags: [spatial-omics, spatial-transcriptomics, scverse, data-loading, documentation]
created: 2026-07-27
updated: 2026-07-27
sources: ["raw/bioinformatics/spatialdata-io/README--v0.7.1.md", "raw/bioinformatics/spatialdata-io/reader-visium--v0.7.1.py", "raw/bioinformatics/spatialdata-io/reader-visium_hd--v0.7.1.py", "raw/bioinformatics/spatialdata-io/reader-xenium--v0.7.1.py", "raw/bioinformatics/spatialdata-io/reader-merscope--v0.7.1.py", "https://spatialdata.scverse.org/projects/io/en/stable/"]
---

# spatialdata-io docs - README and readers

**출처:** [[spatialdata-io]] 프로젝트 문서 및 리더 소스. scverse 프로젝트(NumFOCUS 재정 후원).
문서 사이트: <https://spatialdata.scverse.org/projects/io/en/stable/> ·
repo: `scverse/spatialdata-io` · **버전 핀 `v0.7.1`**(2026-07-02 릴리스) ·
**접근일 2026-07-27** · 로컬 스냅샷: `raw/bioinformatics/spatialdata-io/`.
인용 논문은 [[SpatialData docs - Design doc]]과 동일(Marconato et al., *Nat Methods* 2024).

## 이 소스의 특이점: 문서가 코드에서 생성된다

인제스트 방식에 영향을 준 사실이라 먼저 적는다. `spatialdata-io`의 `docs/`는 실질적으로 비어
있다 — `index.md`는 134바이트 toctree 스텁이고 `api.md`는 951바이트 autodoc 지시문으로 **리더
이름만** 나열한다. 렌더된 사이트에 보이는 설명은 전부 빌드 시점에 **Python docstring에서** 나온다.

따라서 이 소스의 실체는 **`README.md` + 리더 모듈 소스**다. 이번에는 4개를 읽었다:
`visium.py`, `visium_hd.py`, `xenium.py`, `merscope.py` (총 2,654줄).

## 요점

- **역할**: 상용 장비 출력 → `SpatialData` 객체 변환. [[SpatialData]] 본체의 "포맷 컨버터가
  아니다"는 non-goal을 떠받치는 격리 지점.
- **리더의 공통 골격**: 규약된 파일명 탐색 → `*Model.parse()`로 element 생성(좌표변환 동시 주입)
  → `SpatialData(...)` 조립 → `_set_reader_metadata()`로 출처 기록. 상세는 [[spatialdata-io]].
- **지원 기술 13종** — 10x [[Visium]] · [[Visium HD]] · [[Xenium]], Vizgen [[MERSCOPE]], Akoya
  PhenoCycler(구 CODEX), NanoString CosMx, Curio Seeker, DBiT-seq, Spatial Genomics GenePS(seqFISH),
  STOmics Stereo-seq, MACSima, 그리고 파이프라인 출력 MCMICRO·Steinbock.
- **element 이름 규약이 갈린다**: [[Xenium]]은 고정 이름, 나머지는 `dataset_id` 접두사 →
  여러 샘플 병합 시 Xenium은 충돌 위험.
- **Table 3키가 실물로 확인된다**: [[SpatialData elements]]에서 정리한
  `region`/`region_key`/`instance_key` 규칙이 리더별로 어떻게 채워지는지 확인 가능. 예:
  Visium은 `instance_key="spot_id"`, MERSCOPE는 VPT 규약 열, Xenium은 `cell_labels`.
- **[[Visium HD]]의 CytAssist 투영 변환 우회**가 눈에 띈다. [[SpatialData]]가 affine까지만
  지원하므로, 투영 행렬을 affine + projective shift로 분해해 shift는 skimage `warp`로 픽셀에
  구워버리고 affine만 좌표변환으로 남긴다 — [[Coordinate systems and transformations]]의
  "비선형 미지원" 한계에 대한 실전 대응 사례.
- **정확성 보장 없음**을 README가 명시한다: 커뮤니티 관리, 장비사 공식 승인 없음, 포맷이 바뀌면
  리더가 뒤처질 수 있음. 리더가 만든 element를 눈으로 확인하는 습관이 필요하다는 뜻.

## 핵심 발췌

> This library is community maintained and is not officially endorsed by the aforementioned spatial
> technology companies. As such, we cannot offer any warranty of the correctness of the
> representation.

> **Problem: I cannot visualize the data, everything is slow.** Solution: after parsing the data with
> `spatialdata-io` readers, you need to write it to Zarr and read it again. Otherwise the performance
> advantage given by the SpatialData Zarr format will not available.

> `cells_labels`: Whether to read cell labels (raster). The polygonal version of the cell labels are
> simplified for visualization purposes, and using the raster version is recommended for analysis.
> — `xenium()` docstring

## 문서 결함 / 불일치

발견한 것을 그대로 남긴다.

1. **`api.md`에 `iss`·`macsima`가 없다.** 소스 트리에는 `iss.py`·`macsima.py`가 존재하고 README는
   MACSima를 지원 목록에 넣는다. 문서가 코드에서 생성되는데도 목록이 어긋난 상태.
2. **README 예제 코드의 오타** — `sdata.write("data.zarr")`로 쓰고 `read_zarr("sdata.zarr")`를
   읽는다. 위키에는 고쳐 적었다([[spatialdata-io]]).
3. **README의 "Python 3.8 or newer"는 낡았을 가능성이 높다.** 리더 코드가
   `dict | None` 스타일 유니온과 `zip(..., strict=)`를 쓰므로 실제 요구 버전은 훨씬 높다. 정확한
   값은 `pyproject.toml`을 봐야 한다(이번 스냅샷에 포함하지 않음).
4. **PhenoCycler·MACSima가 자체 리더와 3rd-party(SOPA) 목록에 중복 등재**되어 있다. 어느 쪽을
   써야 하는지는 문서가 말해주지 않는다.

## 신선도 주의

- 스냅샷은 **v0.7.1**. [[Visium HD]]의 `load_segmentations_only`는 **기본값이 향후 `True`로
  바뀔 예정**(현재 `FutureWarning`)이므로, 다음 버전에서 동작이 달라진다.
- [[Xenium]] 리더는 **spatialdata-io v0.6.0 이전과 동작이 다르다**(`cells_as_circles` 기본값,
  원 반지름 계산 기준). 과거 스크립트 재실행 시 결과가 달라질 수 있다.
- README의 알려진 한계: Stereo-seq 7.x만 지원(8.x 미지원).

## 모순

기존 페이지와의 모순 없음. 오히려 [[SpatialData docs - Design doc]]에서 정리한 내용이 실물로
확인되는 쪽이다 — Table 3키 규칙, "element 간 명시적 링크 없이 좌표계로 묶는다"는 원칙(모든
리더가 좌표계를 명시적으로 심는다), 그리고 비선형 변환 미지원의 실제 영향.

## 링크

- 리더 라이브러리: [[spatialdata-io]]
- 기술: [[Visium]], [[Visium HD]], [[Xenium]], [[MERSCOPE]]
- 프레임워크: [[SpatialData]], [[SpatialData elements]], [[Coordinate systems and transformations]]
- 영역 MOC: [[Bioinformatics]]

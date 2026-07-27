---
type: source
title: SpatialData docs - Design doc
area: [bioinformatics]
aliases: [SpatialData design document, SpatialData 설계 문서, spatialdata design_doc]
tags: [spatial-omics, data-format, scverse, documentation]
created: 2026-07-27
updated: 2026-07-27
sources: ["raw/bioinformatics/spatialdata-docs/design_doc--v0.8.0.md", "raw/bioinformatics/spatialdata-docs/index--v0.8.0.md", "https://spatialdata.scverse.org/en/stable/design_doc.html"]
---

# SpatialData docs - Design doc

**출처:** *Design document for `SpatialData`* — [[SpatialData]] 공식 문서의 설계 문서 섹션.
scverse 프로젝트(NumFOCUS 재정 후원). 문서 사이트:
<https://spatialdata.scverse.org/en/stable/design_doc.html> ·
원문 소스: `scverse/spatialdata` repo `docs/design_doc.md` · **버전 핀 `v0.8.0`**
(2026-07-02 릴리스) · **접근일 2026-07-27** · 로컬 스냅샷:
`raw/bioinformatics/spatialdata-docs/design_doc--v0.8.0.md`.
관련 논문: Marconato, L. et al. *SpatialData: an open and universal data framework for spatial
omics.* **Nature Methods** (2024 Mar). doi:[10.1038/s41592-024-02212-x](https://doi.org/10.1038/s41592-024-02212-x)
(프리프린트: bioRxiv 2023.05.05.539647).

문서 스스로를 "프로젝트가 진화하면 갱신되는 **living document**"로 규정한다. 사양·설계 근거·
로드맵을 한 문서에 담고 있어, 이 프레임워크가 *무엇을 하기로 했고 무엇을 하지 않기로 했는지*를
가장 직접적으로 보여준다.

## 요점

- **분석 라이브러리가 아니다 — 인프라다.** non-goal에 명시: 분석 라이브러리도 아니고 포맷
  컨버터도 아니다. 분석 라이브러리에 IO와 공간 질의 기반을 제공하는 것이 역할이고, 포맷
  변환은 [[OME-NGFF]]를 교환 포맷으로 삼아 회피한다. (다만 `spatialdata-io`가 흔한 변환을
  담는 자리로 열려 있다.)
- **데이터 모델 → [[SpatialData elements]]**: Images·Labels·Shapes·Points·Tables 5종의
  조합으로 데이터셋을 모델링한다. 핵심 결정은 *전용 클래스를 만들지 않는 것* — 표준 과학
  파이썬 클래스(xarray·geopandas·dask·AnnData) + 규약화된 메타데이터.
- **element 간 명시적 링크가 없다.** "이 Labels는 저 Image에 대응"을 저장하지 않고,
  좌표계로 의미적 그룹핑을 하라고 권한다.
- **좌표 정렬 → [[Coordinate systems and transformations]]**: intrinsic(스키마에서 추론) vs
  extrinsic(이름 필수). 모든 element는 최소 하나의 extrinsic 좌표계에 매핑돼야 하고,
  미지정 시 `"global"`에 Identity로 매핑된다. 변환 클래스가 IO용·연산용 두 세트로 나뉜
  이유도 여기서 설명된다.
- **저장 = Zarr + Parquet.** lazy loading·청크·multiscale. Zarr 계층 구조는 아직 미지원이라
  현재는 flat store일 수 있다.
- **에코시스템은 위성 프로젝트로 분리.** 시각화(napari-spatialdata), raw IO(spatialdata-io),
  정적 플로팅(spatialdata-plot)은 P0~P1로 구현됨. **Squidpy를 SpatialData 입력용으로 리팩터
  하고 이미지 분석 기능을 Squidpy에서 deprecate**하는 계획은 P2로 미완.
- **명시된 한계**: 비선형 변환 미지원(P2), Shapes의 lazy loading 미구현(P1), 시간축 미지원(P2),
  Points 표현은 "아직 논의 중이며 바뀔 수 있음"으로 표기.

## 핵심 발췌

> _SpatialData_ is not an analysis library. Instead the aim is to provide an infrastructure to
> analysis libraries for IO and spatial queries.

> SpatialData elements are not special classes, but are instead standard scientific Python
> classes (e.g., `xarray.DataArray`, `AnnData`) with specified metadata.

> There is no explicit link between elements (e.g. we don't save information equivalent to
> "this Labels element refers to this Image element"), and one is encouranged to use coordinate
> systems to semantically group elements together, based on spatial overlap.

> each element MUST be mapped at least to an extrinsic coordinate system. When no mapping is
> specified, we define a mapping to the "global" coordinate system via an "Identity"
> transformation.

## 신선도 주의

이 스냅샷은 **v0.8.0** 문서다. 두 가지가 stale 신호를 낸다.

1. **Roadmap 2025 항목이 전부 미완 체크박스**다 — transformation 코드를
   `ome-zarr-models-py`로 이전, 그것을 의존성으로 쓰도록 리팩터, 모듈식 `read()` 공개 API,
   **Zarr v3(sharding) 지원**, dask 제약 제거. 접근일(2026-07-27) 기준으로 이미 지난
   시간표이므로, 이 중 일부는 완료되었을 수 있다. 최신 상태는 changelog로 확인할 것.
2. **NGFF 좌표변환 사양이 문서 시점에 제안 단계**였다. 문서 안에 `# TODO update reference
   once proposal accepted`가 그대로 남아 있고, SpatialData 온디스크 표현과 제안된 NGFF 표현
   사이에 작은 차이가 있다고 인정한다.

랜딩 페이지(`index.md`)에서 함께 확인한 실무 함정: **dask ≥ 2025.2.0에서 `Points` 조작 시
에러** — `disable_dask_tune_optimization()` 컨텍스트 매니저로 우회
([issue #1064](https://github.com/scverse/spatialdata/issues/1064), 업스트림 수정 대기).

## 모순

없음 — 인제스트 시점에 bioinformatics 영역이 비어 있어 대조할 기존 페이지가 없었다.

## 링크

- 프레임워크: [[SpatialData]]
- 개념: [[SpatialData elements]], [[Coordinate systems and transformations]]
- 사양: [[OME-NGFF]]
- 영역 MOC: [[Bioinformatics]]

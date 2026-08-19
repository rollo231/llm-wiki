---
type: entity
title: SpatialData
area: [bioinformatics]
aliases: [spatialdata, SpatialData framework, SpatialData object, 스페이셜데이터]
tags: [spatial-transcriptomics, spatial-omics, scverse, python, data-format]
created: 2026-07-27
updated: 2026-08-19
sources: ["[[SpatialData docs - Design doc]]", "https://spatialdata.scverse.org/en/stable/"]
---

# SpatialData

공간 오믹스(spatial omics) 데이터를 위한 **저장 포맷 + 스키마 + 인메모리 표현**을 묶은
오픈 프레임워크. [scverse](https://scverse.org) 프로젝트의 일부이며 NumFOCUS가 재정 후원한다.
단·다중 모달 데이터셋을 모두 다루고, Python 외에 R·JavaScript 구현체도 존재한다.

핵심 성격은 **인프라**다 — 분석 라이브러리가 아니다. 자세한 설계 근거는
[[SpatialData docs - Design doc]] 참고.

> ⚠️ **"인프라"의 범위 주의.** 설계 문서가 말하는 인프라는 *"분석 라이브러리가 아니다"* 라는
> 뜻이고, **데이터 플랫폼의 층을 채운다는 뜻이 아니다.** DE 아키텍처 층위로 보면 테이블 포맷·
> 카탈로그·질의 엔진·오케스트레이션 중 어느 것도 채우지 않는다 —
> [[Adopting SpatialData - schema not storage]] §2.

## 이름이 가리키는 세 가지

문서가 명시적으로 구분하는 지점이라 옮겨 적을 가치가 있다.

1. *SpatialData* **라이브러리** — 핵심 Python 패키지(`spatialdata`).
2. *SpatialData* **프레임워크** — 라이브러리 + 위성 프로젝트 전체.
3. `SpatialData` **객체** — 인메모리 파이썬 객체. [[SpatialData elements]]의 모음을 담는다.

## 기술적 기반

- **온디스크**: Zarr(래스터·메타데이터) + Parquet(points·shapes). 가능한 한
  [[OME-NGFF]] 사양을 따르고, 그것이 규정하지 않는 부분만 자체 정의한다. 포맷은 element
  종류별로 따로 버전이 매겨진다 — [[SpatialData Zarr format versions]].
- **인메모리**: `xarray.DataArray`·`xarray.DataTree`(images·labels), `geopandas`(shapes),
  `dask.dataframe`(points), `AnnData`(tables). 전용 클래스 계층을 만들지 않는다.
- **성능**: dask 기반 lazy loading, 청크 저장, multiscale(피라미드) 표현.
- 좌표 정렬은 [[Coordinate systems and transformations]]가 담당한다.

## 에코시스템 (위성 프로젝트)

| 프로젝트 | 역할 | 우선순위 |
|---|---|---|
| [[spatialdata-io]] | 상용 공간 오믹스 장비의 raw 데이터 리더 (13종 지원) | P0 (구현됨) |
| `napari-spatialdata` | napari 플러그인 — 인터랙티브 탐색·주석 | P0 (구현됨) |
| `spatialdata-plot` | 정적 플로팅 | P1 (구현됨) |
| Squidpy | SpatialData 객체를 입력으로 받도록 리팩터 예정 | P2 (미완) |
| (image analysis) | skimage 등 래핑 — 완성 시 Squidpy의 해당 기능은 deprecate 예정 | P2 (미완) |

다른 언어 구현: `SpatialData` (R), `SpatialData.js` (JS/TS).

## 문서 섹션 트래커

`https://spatialdata.scverse.org/en/stable/` 기준. 인제스트 진행 상황.

- [x] Index (랜딩) — 이 페이지에 흡수
- [x] Design document → [[SpatialData docs - Design doc]]
- [ ] Installation
- [ ] User Guide
- [~] API — 일부. **소스에서** 읽은 하위 섹션:
      `models`·`data_formats` (→ [[SpatialData source - ShapesModel and shapes IO]]),
      `operations` 중 Shapes 관련 4개
      (→ [[SpatialData source - Shapes conversion and aggregation ops]]),
      `query` 전체 (→ [[SpatialData source - Spatial and relational queries]]).
      미이관: `SpatialData`·`io`·`transformations`·`datasets`·`dataloader`·`models_utils`·
      `transformations_utils`·`testing`, `operations` 의 `transform`·`map`.
      주의: `docs/api*.md` 는 autodoc 스텁이라 문서만 읽어선 내용이 없다 — 소스를 읽어야 한다.
- [ ] Tutorials
- [ ] Datasets (8개 기술의 예시 데이터셋)
- [ ] Glossary
- [ ] Contributing
- [x] Changelog — **스텁**. `docs/changelog.md` 는 GitHub Releases 로 안내하는 4줄짜리다.
      릴리스 노트는 API(`/repos/scverse/spatialdata/releases`)로 읽어야 한다.
- [ ] References

## 릴리스 현황

**v0.8.0 (2026-07-02)이 최신 태그다** (확인일 2026-07-27). 설계 문서의 **2025 로드맵 4개 항목**
(`ome-zarr-models-py` 이전, 모듈식 `read()` 공개 API, **Zarr v3 sharding**, dask 제약 제거)은
v0.7.2~v0.8.0 릴리스 노트에 **전혀 등장하지 않는다** — 여전히 미완으로 보인다.

v0.8.0 의 주요 변경 중 위키에 반영된 것:

- 지원 Python 을 **3.12/3.13/3.14** 로 이동 (PR #1151).
- `bounding_box_query` speedup (PR #1104) — 실체는 identity/scaling 변환 fast path이며
  **I/O 최적화가 아니다**: [[Spatial queries in SpatialData]].
- 관계 질의 리팩터 (PR #1131) — **리그레션 유발**(issue #1162):
  [[Relational queries in SpatialData]].
- dataloader 성능 개선 (PR #687) — 아직 미이관.

## 알려진 함정

- **dask ≥ 2025.2.0**: `Points`를 직접 조작하면 에러가 날 수 있다
  ([issue #1064](https://github.com/scverse/spatialdata/issues/1064)). 파티션이 2개 이상일 때
  `disable_dask_tune_optimization()` 컨텍스트 매니저로 dask 그래프 최적화를 끄는 우회책을
  라이브러리가 제공한다. 업스트림 수정 대기 중.
- 문서 자체가 "활발한 개발 중이며 버전 간 API가 바뀔 수 있다"고 경고한다 — 재현성을 위해
  작업한 버전을 기록해 둘 것.

## 링크

- **채택 판단**: [[Adopting SpatialData - schema not storage]] — ⭐ 리더·모델은 사고 store는 분석가용 산출물로. **인프라가 아니라 도메인 스키마다.**
- 개념: [[SpatialData elements]], [[Coordinate systems and transformations]],
  [[SpatialData Shapes element]], [[SpatialData Zarr format versions]]
- 질의: [[Spatial queries in SpatialData]], [[Relational queries in SpatialData]]
- 연산: [[Rasterization and vectorization]], [[Spatial aggregation]]
- 사양: [[OME-NGFF]]
- 리더: [[spatialdata-io]] → [[Visium]], [[Visium HD]], [[Xenium]], [[MERSCOPE]]
- 출처: [[SpatialData docs - Design doc]], [[SpatialData source - ShapesModel and shapes IO]]
- 영역 MOC: [[Bioinformatics]]

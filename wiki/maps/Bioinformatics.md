---
type: moc
title: Bioinformatics
area: [bioinformatics]
aliases: [생물정보학, 바이오인포매틱스, Bioinformatics MOC]
tags: [bioinformatics, spatial-omics, spatial-transcriptomics]
created: 2026-07-27
updated: 2026-08-19
sources: []
---

# Bioinformatics

**bioinformatics** 영역의 Map of Content. 현재는 **공간 오믹스(spatial omics) 데이터 인프라**를
중심으로 쌓이고 있다 — 데이터를 어떻게 저장하고, 표현하고, 정렬하는가.

> 처음 읽는다면: [[Legacy AnnData spatial convention]] → [[SpatialData elements]] 순서를 권한다.
> 전자가 *왜 이 프레임워크가 필요했는가*, 후자가 *그래서 무엇으로 대체했는가*를 다룬다.
> 용어가 헷갈릴 때(mask? annotation? ROI?)는 [[Spatial omics vocabulary]].

## 프레임워크·사양

- [[SpatialData]] — 공간 오믹스용 저장 포맷·스키마·인메모리 표현을 묶은 scverse 프레임워크.
- [[OME-NGFF]] — SpatialData가 교환 포맷으로 채택한 OME의 차세대 이미징 사양(OME-Zarr).

## 개념

- [[Spatial omics vocabulary]] — mask·annotation·ROI·boundaries 가 각각 무엇을 가리키는지.
  SpatialData 용어 ↔ 현장 용어 ↔ QuPath·napari·GeoJSON 대응.
- [[Legacy AnnData spatial convention]] — SpatialData 이전 h5ad 관례와 그 한계. **왜 필요했는가.**
- [[SpatialData elements]] — 데이터 모델의 빌딩 블록 5종(Images·Labels·Shapes·Points·Tables).
- [[Coordinate systems and transformations]] — intrinsic/extrinsic 좌표계와 정렬 방식.
- [[SpatialData Shapes element]] — Shapes 상세: circles vs polygons, `ShapesModel` 계약, 온디스크 레이아웃.
- [[SpatialData Zarr format versions]] — element 종류별 포맷 버전 체계와 조합 제약.

## 연산

- [[Rasterization and vectorization]] — Labels ↔ Shapes 변환, `rasterize()`·`rasterize_bins()`.
- [[Spatial aggregation]] — `aggregate()`: 영역별로 값을 모아 table 을 만든다.
- [[Spatial join execution]] — 그 연산의 정체(격자·인덱스·refine)를 엔진 중립으로 본 개념 페이지.
  → 인접 영역 MOC: [[Data Engineering]]

## 질의

- [[Spatial queries in SpatialData]] — `bounding_box_query()`·`polygon_query()`. 프루닝이
  실제로 I/O 를 줄이는 건 **래스터뿐**이다.
- [[Relational queries in SpatialData]] — SQL 식 조인 5종·`get_values()`·`filter_by_table_query()`.
  soft FK 위에 얹힌 실행 레이어.

## 데이터 적재

- [[spatialdata-io]] — 장비 출력을 SpatialData로 읽는 리더 라이브러리(13종 지원).

### 기술 플랫폼

| 플랫폼 | 계열 | 측정 단위 |
|---|---|---|
| [[Visium]] | 10x · array-based | spot |
| [[Visium HD]] | 10x · array-based | 2µm bin (+ 세포·핵 세그멘테이션) |
| [[Xenium]] | 10x · in situ | 단분자 transcript |
| [[MERSCOPE]] | Vizgen · in situ (MERFISH) | 단분자 transcript |

## 종합 노트

- ⭐ [[SpatialData and Sedona interop]] — **[[SpatialData]]와 [[Apache Sedona]]/[[SedonaDB]]가 만나는
  지점 전체.** `points.parquet`·`shapes.parquet`은 이미 엔진이 읽을 수 있고, 좌표변환 이음새는
  [[Xenium]]·[[MERSCOPE]] 리더에서 상쇄된다(소스 확인). issue #210 우회의 실제 경로.
- [[SpatialData as a data engineering substrate]] — 포맷을 데이터 엔지니어링 관점으로 읽고
  (레이크하우스 파일 포맷 층에 이점, 테이블 포맷 층에 없음), 그 위의 ETL·카탈로그를 설계한다.
  → 인접 영역 MOC: [[Data Engineering]]
- [[Spatial omics platform roadmap]] — 위 노트의 자매편. **플랫폼을 [[Xenium]]·[[Visium]]·
  [[MERSCOPE]] 3종으로 고정**하면 "3개 플랫폼"이 아니라 **2개 워크로드**가 되고, 버전 매트릭스가
  유한해져 **CI 픽스처로 고정 가능**해진다. 실제 스택(K8s·Airflow·MinIO·Postgres) 위에서
  정석 패턴을 **되돌릴 수 있는가** 축으로 정렬한 로드맵.

## 출처

- [[SpatialData docs - Design doc]] — SpatialData 공식 설계 문서(v0.8.0): 목표·비목표·사양·로드맵.
- [[spatialdata-io docs - README and readers]] — spatialdata-io v0.7.1의 README + 리더 소스 4종.
- [[spatialdata-io source - Legacy AnnData converter]] — v0.7.1 `converters/legacy_anndata.py`:
  레거시 h5ad 관례의 명세이자 손실적 왕복의 근거.
- [[SpatialData source - ShapesModel and shapes IO]] — v0.8.0 소스 3종(`models.py`·`io_shapes.py`·`format.py`).
- [[SpatialData source - Shapes conversion and aggregation ops]] — v0.8.0 `_core/operations/` 4종.

## 열린 질문

이 영역이 자라면서 파볼 지점.

- ~~v0.8.0 문서의 **2025 로드맵**이 어디까지 진행됐는가~~ → **확인됨(2026-07-27): 여전히 미완.**
  v0.8.0 이 최신 태그이고 로드맵 4개 항목이 릴리스 노트에 등장하지 않는다. [[SpatialData]] 참고.
  남은 질문은 **Zarr v3 sharding 이 실제로 언제 오는가** — 대용량 store 의 객체 수 문제가 여기 걸려
  있다 ([[SpatialData as a data engineering substrate]] §6).
- **Squidpy**가 SpatialData 객체를 받도록 리팩터되었는가 (문서 시점 P2·미완).
- 비선형 정합이 필요한 작업은 지금 무엇으로 하는가 — SpatialData는 비선형 변환 미지원(P2).
  [[Visium HD]]의 "픽셀에 미리 굽는" 우회가 유일한 해법인가.
- **아직 안 읽은 리더 11개** — 특히 Stereo-seq·CosMx·PhenoCycler. `iss`·`macsima`는 코드에는
  있는데 API 문서 목록에 없다(다음 버전에서 재확인).
- 플랫폼 자체의 생물학·해상도 특성은 아직 비어 있다 — 리더 contract만 정리된 상태다.
  플랫폼 비교(해상도 vs 처리량 vs 비용)를 다룬 소스가 들어오면 `notes/`에 비교 페이지를 만들 만하다.
- ~~**공간·관계 질의**는 아직 이름만 파악됐다~~ → **인제스트 완료**:
  [[Spatial queries in SpatialData]], [[Relational queries in SpatialData]].
- **points 가 전량 메모리에 올라가는 문제가 일반적 패턴으로 확인됐다** — `aggregate()`
  ([issue #210](https://github.com/scverse/spatialdata/issues/210))뿐 아니라 `bounding_box_query()`·
  `get_values()` 도 `.compute()` 한다.
  → ✅ **닫혔다 (2026-08-19)**: 타일로 자르는 게 아니라 **엔진을 바꾼다** — [[SedonaDB]]가 같은
  `points.parquet`을 읽고, 결과가 `aggregate()`와 **완전히 일치한다**(실행 검증).
  **기준선도 실측됐다** — 셀 3,600 × 유전자 100 기준 `aggregate()` 는 20M≈9GB/19.7s,
  **50M≈10.6GB/94s 로 시간이 초선형으로 꺾인다**; 같은 구간 SedonaDB 는 1.97s/1.4GB.
  ⚠️ **store 를 쓰는 것도 같은 벽**(50M build peak 9.6GB). → [[SpatialData and Sedona interop]] §7
- ~~**리더 13종 전부가 points 와 shapes 에 같은 transform 을 넣는가**~~ → ✅ **15종 전수 조사 완료.**
  points+shapes 를 함께 만드는 것은 4개(xenium·merscope·stereoseq·seqfish)뿐이고 **seqfish 가 반례다**
  — transcripts 는 `Identity`, 세포 경계 폴리곤은 `Scale`. ⭐ 조인 전 assert 가 필수라는 결론.
  → [[SpatialData and Sedona interop]] §2
- **(신규 2026-08-19) `cosmx` 는 세그멘테이션이 Labels 다** — `aggregate()` 가 지원하지 않는 조합
  (Labels × Points)이라 먼저 벡터화해야 하고, **FOV 마다 affine 이 달라** FOV 를 넘나드는 조인은
  intrinsic 공간에서 불가능하다. 이 플랫폼의 전처리 경로가 나머지와 다르다.
- ~~**`sedonadb-zarr` 가 [[OME-NGFF]] multiscale 레이아웃을 읽는가**~~ → ✅ **읽는다 (2026-08-19).**
  ⭐ 원인이 명확하다 — **OME-NGFF 가 아니라 순수 Zarr 로 읽는다.** 그래서 비표준 버전 문자열도
  CRS 없음도 무해하고, 동시에 **좌표변환을 무시한다**(envelope 이 배열 인덱스 공간·y 부호 반전).
  multiscale 은 `arrays=["s0"]` 로 레벨 하나씩. 카탈로그 함의는 **기대의 절반** —
  물리 속성은 공짜, **공간 속성(extent)은 여전히 사용자 몫**.
  → [[SpatialData and Sedona interop]] §6
- **(신규 2026-08-19) 래스터 envelope 를 벡터와 맞추는 실제 코드** — y 부호 반전 + OME scale 적용.
  무엇을 해야 하는지는 확정됐고 작성만 남았다. 그리고 **Zarr v2 구버전 store 는 미확인**이다
  ([[SpatialData Zarr format versions]]).
- **v0.8.0 리그레션 #1162**(다중 region 테이블의 `obs` 재정렬)가 언제 고쳐지는가. `filter_table=True`
  가 기본값이라 공간 질의 사용자 전부가 영향권이다.
- `_core/query/_utils.py` 미이관 — 래스터 슬라이싱의 세부(`_create_slices_and_translation`,
  `_process_query_result`)가 거기 있다. 회전 변환에서의 과선택 동작을 정확히 보려면 필요.
- circle 이 모든 연산에서 폴리곤으로 buffer 된다. `buffer_resolution` 기본값 16 이 [[Visium]] spot
  집계 정확도에 실제로 얼마나 영향을 주는지 정량적으로 본 자료가 있는가.
- 옛 store 를 읽어 다시 쓰면 **포맷 버전이 조용히 올라간다**. `formats=` 로 고정하는 게
  실제로 어떻게 동작하는지 — 그리고 [[Xenium]] 의 NaN radius 처럼 옛 데이터가 새 검증에 걸리는
  경우가 또 있는지 확인 필요. [[SpatialData Zarr format versions]] 참고.
- 문서/코드 drift 가 두 곳에서 반복됐다(리더 목록, `data_formats` 포맷 목록). API 문서를
  신뢰 기준으로 쓰지 말 것 — 소스가 SoT.

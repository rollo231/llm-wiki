---
type: concept
title: Legacy AnnData spatial convention
area: [bioinformatics]
aliases:
  - legacy AnnData
  - obsm spatial
  - "obsm['spatial']"
  - 레거시 AnnData
  - AnnData 공간 관례
  - 왜 SpatialData 가 필요한가
tags: [spatial-omics, anndata, scanpy, squidpy, h5ad, legacy, data-model, rationale]
created: 2026-07-27
updated: 2026-07-27
sources:
  - "[[spatialdata-io source - Legacy AnnData converter]]"
  - "[[SpatialData docs - Design doc]]"
---

# Legacy AnnData spatial convention

[[SpatialData]] 이전, 공간 전사체 데이터를 **h5ad 하나에 담던 시절의 관례**. Scanpy 와 구버전
Squidpy 가 기대하던 형태다. 이 페이지는 그 관례의 명세와 한계를 정리하고, **그 한계 하나하나가
SpatialData 의 어느 설계 결정에 대응하는지** 짚는다 — 즉 "SpatialData 가 왜 필요한가" 에 대한
구체적 답이다.

관례가 추측이 아니라 **명세로 확인 가능한 이유**: `spatialdata-io` 에 `from_legacy_anndata()` /
`to_legacy_anndata()` 컨버터가 있고, 그 코드가 읽고 쓰는 키의 목록이 곧 레거시 어휘의 전부다
([[spatialdata-io source - Legacy AnnData converter]]).

## 관례의 전부

```python
adata.obsm["spatial"]                                     # (n_obs, 2) — 중심좌표 배열
adata.uns["spatial"][dataset_id]["images"]["hires"]       # 이미지 배열 (y, x, c)
                                          ["lowres"]
adata.uns["spatial"][dataset_id]["scalefactors"]["tissue_hires_scalef"]
                                                ["tissue_lowres_scalef"]
                                                ["spot_diameter_fullres"]
```

이게 끝이다. 공간 정보가 들어갈 자리가 이 두 곳뿐이고, 나머지는 전부 일반 AnnData 필드다.

| 필드 | 담는 것 | 성격 |
|---|---|---|
| `obsm["spatial"]` | 관측 하나당 **점 하나** (x, y) | `obs` 에 정렬된 `(n_obs × 2)` 배열 |
| `uns["spatial"][id]["images"]` | 다운스케일된 이미지 두 장 | 비정형 dict — 검증도 청킹도 없다 |
| `uns[...]["scalefactors"]` | 이미지↔좌표 배율, spot 지름 | 사실상 좌표변환을 숫자 세 개로 눌러 담은 것 |

## 폴리곤은 여기 들어갈 수 없다 — 구조적으로

`obsm` 은 정의상 **`(n_obs × k)` 직사각 배열**이고 `obs` 행에 정렬된다. 폴리곤은 세포마다 꼭짓점
개수가 다른 **ragged** 데이터라 이 shape 계약에 애초에 맞지 않는다.

그래서 복원 코드가 `obsm["spatial"]` 을 해석하는 방식이 이렇다:

```python
xy = adata.obsm[SPATIAL]
shapes["locations"] = ShapesModel.parse(xy, geometry=0, radius=radius, ...)
#                                           ^^^^^^^^^^ geometry=0 = Point → circle
```

**언제나 circle 이다** ([[SpatialData Shapes element]]). 게다가 반지름이 `obsm` 에 없어서
`uns[...]["scalefactors"]["spot_diameter_fullres"] / 2` 에서 가져오고, 그마저 없으면 **기본값 10 을
쓰며 경고**한다.

### 그럼 폴리곤은 어디 있었나 — h5ad 바깥

세포 경계는 **h5ad 옆에 놓인 별도 파일**로 존재했다. 리더 소스가 그대로 보여준다 —
[[MERSCOPE]] 리더는 boundaries 파일을 h5ad 와 무관하게 따로 찾아 `geopandas.read_parquet()` 로 읽는다.
[[Xenium]] 도 `cell_boundaries` 가 별도 파일이다. `ShapesModel.parse()` 가 GeoJSON **파일 경로**를
입력으로 받는 경로가 있는 것도 같은 전제다 — GeoJSON 은 원래 표 바깥에 있는 것이다.

즉 당시 표준 구성은 **`h5ad` + 사이드카 파일 몇 개**였고, 둘을 잇는 것은 파일명 관례와 사람의
기억이었다. 매니페스트도, 타입도, 검증도 없었다.

## 왕복이 손실적이다

`to_legacy_anndata()` 가 SpatialData → 레거시로 갈 때 하는 일:

```python
# convert polygons, multipolygons and labels to circles
shapes = to_circles(element)
...
adata.obsm["spatial"] = get_centroids(...).compute().values
```

**폴리곤·멀티폴리곤·라벨을 전부 circle 로 뭉갠다.** docstring 이 인정한다 — *"Labels will be
approximated to circles by using the centroids of each label and an average approximated radius."*

레거시 포맷이 폴리곤을 담을 수 없으니, 담으려면 근사하는 것 외에 방법이 없다. 이 **비대칭**
(SpatialData → 레거시는 손실, 레거시 → SpatialData 는 정보를 발명해야 함)이 두 모델의 표현력 차이를
가장 선명하게 보여준다.

## 한계 → SpatialData 의 답

| 레거시의 한계 | SpatialData 의 설계 결정 |
|---|---|
| 기하가 **점 하나**뿐 (폴리곤 불가) | [[SpatialData Shapes element\|Shapes]] 를 독립 element 로 — circle 과 polygon 둘 다, GeoParquet 저장 |
| 이미지가 `uns` 안의 생 배열 (검증·청킹·multiscale 없음) | Images·Labels 를 [[OME-NGFF]] 준수 Zarr 로 — 청크·피라미드·lazy loading |
| 좌표변환이 스케일 숫자 세 개 | [[Coordinate systems and transformations]] — 이름 붙은 좌표계와 합성 가능한 변환 |
| 표 하나에 기하 하나 | `region`/`region_key`/`instance_key` 로 **한 표가 여러 Regions** 를 가리킨다 ([[SpatialData elements]]) |
| 단분자 좌표를 담을 자리가 없음 | Points 를 독립 element 로 (Parquet + dask) |
| 다중 모달·다중 샘플 조합 불가 | element 들의 **임의 조합**이 데이터 모델의 출발점 |
| 폴리곤은 사이드카 파일, 링크는 파일명 관례 | 하나의 Zarr store 가 전부를 담고, 좌표계가 의미적 그룹핑을 한다 |
| 버전 개념 없음 | element 종류별 [[SpatialData Zarr format versions\|포맷 버전]] + 하위 호환 리더 |

설계 문서에 이미 기록된 문장이 이 역사를 정확히 겨눈다 ([[SpatialData elements]]):

> `Tables` 는 좌표계를 가질 수 **없다**. 표에 공간 좌표를 넣어둘 수는 있지만 라이브러리가 처리하지
> 않는다 — 프레임워크가 인식하려면 element 로 만들어 좌표계에 두어야 한다.

추상적 원칙이 아니라 **`obsm["spatial"]` 관례를 명시적으로 폐기하는 선언**이다. "표 안에 좌표를
숨겨두는" 방식을 인정하지 않고, 기하를 독립 element 로 승격시켜 좌표계에 매핑하라는 것.

## 레거시에 없던 개념을 복원 시 발명한다

`from_legacy_anndata()` 가 관계를 **만들어 붙이는** 대목이 이 차이를 잘 보여준다.

```python
REGION       = "locations"      # region 이름을 지어낸다
REGION_KEY   = "region"
INSTANCE_KEY = "instance_id"
```

레거시 h5ad 에는 *"이 표가 어느 기하를 가리키는가"* 라는 개념 자체가 없었다 — 표와 좌표가 같은
객체 안에 있으니 링크가 필요 없었고, **그래서 표 하나에 기하 하나를 넘어설 수 없었다.** 관계를
명시하는 순간(= `region`/`instance_key` 도입) 다대일과 다중 모달이 가능해진다.

## 지금도 남아 있는 흔적

레거시가 완전히 사라진 게 아니다. [[spatialdata-io]] 리더 4개가 **여전히 `obsm["spatial"]` 을
채운다** — [[Visium]]·[[Visium HD]]·[[MERSCOPE]]·[[Xenium]] 모두. 하위 호환을 위한 중심좌표 사본이고,
정본은 Shapes element 쪽이다.

`to_legacy_anndata()` 의 용도도 그대로다 — Scanpy 나 구버전 Squidpy 처럼 AnnData 를 기대하는 패키지에
넘길 때. 다만 docstring 이 못 박는다:

> Using this format for any new package is not recommended.

## 링크

- 출처: [[spatialdata-io source - Legacy AnnData converter]], [[SpatialData docs - Design doc]]
- 프레임워크: [[SpatialData]] · 리더: [[spatialdata-io]]
- 데이터 모델: [[SpatialData elements]], [[SpatialData Shapes element]]
- 좌표: [[Coordinate systems and transformations]] · 사양: [[OME-NGFF]]
- 저장: [[SpatialData Zarr format versions]]
- 플랫폼: [[Visium]], [[Visium HD]], [[Xenium]], [[MERSCOPE]]
- 영역 MOC: [[Bioinformatics]]

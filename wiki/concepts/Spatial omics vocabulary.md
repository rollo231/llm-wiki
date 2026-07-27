---
type: concept
title: Spatial omics vocabulary
area: [bioinformatics]
aliases:
  - mask
  - 마스크
  - annotation
  - 어노테이션
  - ROI
  - region of interest
  - segmentation mask
  - boundaries
  - 세포 경계
  - 공간 오믹스 용어
  - 용어 정리
tags: [spatial-omics, terminology, glossary, data-model, qupath, napari, geojson]
created: 2026-07-27
updated: 2026-07-27
sources:
  - "[[SpatialData docs - Design doc]]"
  - "[[SpatialData source - ShapesModel and shapes IO]]"
  - "[[SpatialData source - Shapes conversion and aggregation ops]]"
---

# Spatial omics vocabulary

같은 대상을 [[SpatialData]] 사양·논문·도구 UI·현장 대화가 각기 다른 이름으로 부른다. 이 페이지는
그 다리다 — **어떤 단어가 무엇을 가리키는지, 그리고 어디서 어긋나는지.**

> **근거 구분.** SpatialData 내부 용어는 설계 문서와 소스에서 인용했다(줄 번호 표기). 현장 관행
> (QuPath·napari·Cellpose 등)은 **위키에 인제스트된 출처가 없는 일반 지식**이므로 별도 표시했다 —
> 연구실·도구마다 흔들리는 부분이다.

## 한 장 요약

| SpatialData 용어 | 무엇 | 현장에서 흔히 부르는 말 |
|---|---|---|
| **Regions** | 공간의 영역을 지정하는 것 (상위 개념) | ROI, 영역 |
| **Labels** | 영역의 **래스터** 표현 (정수 픽셀 배열) | **mask**, segmentation mask, label image |
| **Shapes** | 영역의 **벡터** 표현 (circle·polygon) | ROI, boundaries, outlines, contours, polygons, (사람이 그린 것) annotation |
| **Points** | 단분자 좌표 | transcripts, molecules, point cloud |
| **Tables** | 영역에 붙는 **값** | **annotation**, metadata, obs, 발현 행렬 |
| **Images** | 픽셀 강도 | image, channel, morphology |

핵심은 **한 칸이 아니라 두 축**이다. 아래 둘을 분리하면 대부분의 혼동이 사라진다.

## 축 1 — 기하냐 값이냐: "annotation"의 진짜 의미

SpatialData 용어법에서 **annotation 은 언제나 *값* 이고 *기하* 가 아니다.** 설계 문서의 어법이
일관되다:

```
104: Elements ... can be annotated by one or multiple Table elements
115: _Tables_ of annotations
130: Any Element MAY be annotated by Tables; also Shapes and Points MAY contain
     annotations within themselves as additional dataframe columns
245: #### Table (table of annotations for regions)
286: A table MUST not have a coordinate system since it annotates Region Elements
```

문법이 방향을 못 박는다 — **Tables 가 annotate 하고, Shapes 는 annotated 된다.** 코드도 같다:
`PointsModel.parse(annotation=pd.DataFrame)` 의 `annotation` 은 점마다 붙는 **속성 표**다.

그래서 **"Shapes = 어노테이션" 은 틀렸다.** Shapes 의 상위어는 **ROI** 이고, 설계 문서가 직접 그렇게
쓴다:

> Shapes can be used to represent a variety of **regions of interest**, such as clinical
> annotations and user-defined regions of interest. *(220행)*

**"clinical annotations" 는 ROI 의 한 종류로 나열된다** — 상위어가 ROI, 어노테이션은 그 아래 항목.

### 결정적 반례

[[Visium]] spot, [[Visium HD]] bin, [[Xenium]] `cell_circles` 가 **전부 Shapes** 다. 이건 장비의
물리적 격자이지 누가 주석한 게 아니다. 그래서 `Shapes ⊃ annotation` 이지 `Shapes = annotation` 이
아니다.

## 축 2 — 래스터냐 벡터냐: "mask"의 진짜 의미

**mask 는 Labels 전용어다.** 설계 문서:

```
113: Pixel masks (such as segmentation masks), aka _Labels_, 2D, or 3D
206: ##### Labels (pixel mask)
208: Labels are a pixel mask representation of regions.
```

`models.py` 에는 "mask" 라는 단어가 **한 번도 안 나온다** — `ShapesModel` 은 이 어휘를 쓰지 않는다.
`vectorize.py` 의 내부 함수 이름이 방향성을 그대로 드러낸다: **`_vectorize_mask(mask)`** — 입력이
mask, 출력이 shapes.

Labels 와 Shapes 는 **같은 것의 두 표현**이라 서로 변환된다 ([[Rasterization and vectorization]]):

```
mask (Labels) ──to_polygons() / to_circles()──▶ Shapes
Shapes ──rasterize(return_regions_as_labels=True)──▶ mask (Labels)
```

## 축 3 — 누가 만들었나

같은 폴리곤이라도 출처에 따라 부르는 말이 갈린다. **이게 현장 용어의 실제 구분 축이다.**

| 출처 | 부르는 말 |
|---|---|
| 사람이 손으로 그림 | **annotation**, ROI |
| 알고리즘 세그멘테이션 | boundaries, outlines, contours, (래스터면) **mask** |
| 장비의 물리 격자 | spot, bin — annotation 이라 하지 않는다 |

*(이 표는 현장 관행이며 인제스트된 출처 없음.)* QuPath 가 이 구분을 UI 로 못박아 둔 대표 사례다 —
**Annotations**(사람이 그린 영역) vs **Detections**(알고리즘이 찾은 객체).

설계 문서가 나열하는 Region 의 예시도 이 스펙트럼을 그대로 담는다: 조직, 조직 구조, **임상 주석**,
다세포 커뮤니티, 세포, 세포내 구조, **장비의 물리 구조(Visium "spot")**, 알고리즘이 만든 합성 영역
([[SpatialData elements]]).

## 다의어 주의 — 코드에서 같은 단어가 두 뜻

| 단어 | 뜻 A | 뜻 B |
|---|---|---|
| **mask** | 세그멘테이션 마스크 = Labels (`_vectorize_mask`) | **boolean 배열**로 행 고르기 (`_bounding_box_mask_points`, `_get_masked_element`) |
| **annotation** | element 에 붙는 값 = Tables·컬럼 | Python `from __future__ import annotations` (무관) |
| **feature** | GeoJSON/GIS 의 `Feature` = 기하+속성 | 유전자·단백질 등 **측정 변수**(`var`, `feature_key`) |

특히 `feature` 가 위험하다 — 공간 오믹스에서 `feature_key` 는 **gene id** 를 가리키지 GIS 의
Feature 가 아니다.

## 외부 어휘 대응

*(이 절은 일반 지식이며 인제스트된 출처 없음.)*

| 도구/사양 | 벡터 영역 | 래스터 영역 | 값 |
|---|---|---|---|
| **SpatialData** | Shapes | Labels | Tables |
| **napari** | Shapes layer | Labels layer | (layer properties) |
| **QuPath** | Annotations / Detections | — | measurements |
| **GeoJSON / GIS** | `Feature.geometry` | — | `Feature.properties` |
| **Cellpose** | outlines | `masks` (반환 변수명이 문자 그대로 `masks`) | — |
| **scanpy/AnnData** | (없음 — 표현 불가) | (없음) | `obs`, `var`, `X` |

**GeoJSON 대응이 특히 깔끔하다.** `Feature = geometry + properties` 라는 분리가 SpatialData Shapes
(= `geometry` 컬럼 + 주석 컬럼)와 정확히 같다. 그래서 GeoParquet 이 저장 포맷으로 자연스럽게
맞아떨어진다 ([[SpatialData Shapes element]]). 이 어휘에서도 "annotation" 에 해당하는 건
`properties` 쪽이지 `geometry` 가 아니다.

맨 아랫줄이 [[Legacy AnnData spatial convention]] 이 왜 한계였는지를 요약한다 — 벡터 영역을 담을
어휘 자체가 없었다.

## 흔한 오해 정리

- ❌ "Shapes = 어노테이션" → Shapes 는 **ROI**. 어노테이션은 거기 붙는 **값**(Tables).
- ❌ "Shapes = 마스크" → 마스크는 **Labels**(래스터). Shapes 는 벡터 쪽.
- ❌ "세포 마스크를 Shapes 로 저장했다" → 표현이 섞였다. 폴리곤이면 boundaries, 라벨 이미지면 mask.
- ⚠️ "세그멘테이션 결과" 는 표현 방식을 말해주지 않는다 — 폴리곤일 수도 라벨 이미지일 수도 있다.
  [[Xenium]] 처럼 **둘 다 내놓는** 데이터에서는 어느 쪽인지 확인해야 한다.
- ⚠️ circle 은 원 도형이 아니라 **중심점 + 반지름**이다 ([[SpatialData Shapes element]]).

## 링크

- 데이터 모델: [[SpatialData elements]], [[SpatialData Shapes element]]
- 변환: [[Rasterization and vectorization]] · 집계: [[Spatial aggregation]]
- 역사: [[Legacy AnnData spatial convention]]
- 프레임워크: [[SpatialData]] · 사양: [[OME-NGFF]]
- 플랫폼: [[Visium]], [[Visium HD]], [[Xenium]], [[MERSCOPE]]
- 출처: [[SpatialData docs - Design doc]], [[SpatialData source - ShapesModel and shapes IO]],
  [[SpatialData source - Shapes conversion and aggregation ops]]
- 영역 MOC: [[Bioinformatics]]

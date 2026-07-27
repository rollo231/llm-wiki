---
type: concept
title: SpatialData elements
area: [bioinformatics]
aliases: [Elements, SpatialData Element, 엘리먼트, 스페이셜데이터 엘리먼트]
tags: [spatial-omics, data-model, anndata, xarray, geopandas, dask]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[SpatialData docs - Design doc]]"]
---

# SpatialData elements

**Element**는 [[SpatialData]] 데이터 모델의 빌딩 블록이다. 공간 데이터셋을 하나의 거대한
객체로 모델링하지 않고, 타입이 다른 element들의 **조합**으로 본다. 그래서 임의의 조합이
가능하고, 각 element를 독립적으로 추가·수정할 수 있다.

## 핵심 설계 결정: 새 클래스를 만들지 않는다

Element는 SpatialData 전용 클래스가 **아니다**. 표준 과학 파이썬 클래스에 **규약화된
메타데이터**를 얹은 것이다. 메타데이터가 좌표계·좌표변환 등 element를 표시하고 통합하는 데
필요한 정보를 담는다. 디스크에서 읽어 초기화하거나, `numpy` 배열 같은 인메모리 객체에서
parser 함수를 통해 만든다.

## 다섯 가지 타입

| Element | 무엇 | 인메모리 표현 | 축 |
|---|---|---|---|
| **Images** | 픽셀 기반 이미지 | `xarray.DataArray` / `xarray.DataTree`(multiscale) | 2D `cyx`, 3D `czyx` |
| **Labels** | 픽셀 마스크(세그멘테이션 등). 정수값 하나가 한 영역 | Images와 동일 | 2D `yx`, 3D `zyx` |
| **Shapes** | (multi)polygon·circle 형태의 ROI | `geopandas.GeoDataFrame` | 2D |
| **Points** | 단분자 좌표·점군 (transcript 위치 등) | `dask.dataframe.DataFrame` (온디스크 Parquet) | `x,y` 또는 `x,y,z` |
| **Tables** | 영역에 대한 주석 | `AnnData` | (없음) |

`Labels`와 `Shapes`는 둘 다 **Regions**의 구현이다 — 공간의 특정 영역을 지정해 관측을
선택·집계하는 데 쓰인다. (mask·annotation·ROI 등 현장 용어와의 대응은
[[Spatial omics vocabulary]].) 영역의 예: 조직, 조직 구조, 임상 주석, 다세포 커뮤니티, 세포,
세포내 구조, 장비의 물리 구조(Visium "spot" 등), 알고리즘이 만든 합성 영역.

**Shapes의 실용적 중요성**: 배열 기반 공간 오믹스 기술 대부분 — 10x Visium, BGI Stereo-seq,
DBiT-seq — 을 Shapes로 표현할 수 있다. 필수 컬럼·검증 규칙·온디스크 레이아웃은
[[SpatialData Shapes element]] 참고.

## Element 간에 명시적 링크가 없다

반직관적이지만 중요한 지점이다. *"이 Labels는 저 Image에 대응한다"* 같은 정보를
**저장하지 않는다**. 대신 [[Coordinate systems and transformations]]를 써서, 공간적으로
겹치는 element들을 같은 좌표계에 두는 방식으로 **의미적으로 묶으라**고 권한다.

## 가정 (대부분 [[OME-NGFF]]에서 상속)

- `Images`·`Labels`·`Points`·`Shapes`는 좌표계·좌표변환을 하나 이상 **가져야 한다**.
- `Tables`는 좌표계를 가질 수 **없다**. 표에 공간 좌표를 넣어둘 수는 있지만 라이브러리가
  처리하지 않는다 — 프레임워크가 인식하려면 element로 만들어 좌표계에 두어야 한다.
  이 문장은 추상적 원칙이 아니라 **`obsm["spatial"]` 관례를 명시적으로 폐기하는 선언**이다:
  [[Legacy AnnData spatial convention]].
- 모든 `Element`는 `Tables`로 주석될 수 있다. `Shapes`·`Points`는 자기 안에 컬럼으로
  주석을 담을 수도 있다(점별 형광 강도, gene id 등).
- `Tables`는 다른 `Tables`로 주석될 수 **없다**.

## Table의 세 키

`Tables`가 어떤 영역을 가리키는지는 세 필드로 표현한다.

- `region` — 이 표가 가리키는 Regions(하나 또는 목록)
- `region_key` — `obs`의 어느 컬럼이 "어느 Regions 컨테이너에 속하는가"를 말하는지
- `instance_key` — `obs`의 어느 컬럼이 "어느 인스턴스인가"를 말하는지 (예: `cell_id`)

**셋 중 하나라도 정의하면 셋 다 정의해야 한다.** 아예 정의하지 않은 표도 허용되지만, 그
표는 어떤 공간 element에도 매핑되지 않는다. 표 한 개가 여러 Regions 집합을 가리킬 수 있으나,
각 행은 자기 Regions element 안의 영역 하나에만 매핑된다.

`spatialdata-io`의 관례(권장이지만 강제는 아님): `region_key`는 `'region'`,
`instance_key`는 `'instance_id'`.

## 이름 규칙

Element 이름은 저장 안정성과 호환성을 위해 제약을 받는다.

- 빈 문자열 불가
- 영숫자와 `-`, `.`, `_` 만 허용 (공백·슬래시 등 불가. 다른 문자 체계의 문자는 허용)
- `.` 또는 `..` 단독 불가 (경로로 해석됨)
- `__`로 시작 불가
- **대소문자만 다른 이름 불가** (대소문자 구분 없는 파일시스템에서 충돌 방지)

표에서는 이 규칙이 `obs`·`var`의 컬럼명과 `obsm`·`obsp`·`varm`·`varp`·`uns`·`layers`의
키에 적용된다. 추가로 `_index`는 예약어이므로 컬럼명으로 쓸 수 없다.

## 링크

- 프레임워크: [[SpatialData]]
- 좌표: [[Coordinate systems and transformations]]
- 타입별 상세: [[SpatialData Shapes element]]
- 이 모델이 무엇을 대체했나: [[Legacy AnnData spatial convention]]
- 질의: [[Spatial queries in SpatialData]], [[Relational queries in SpatialData]]
- 저장 포맷: [[SpatialData Zarr format versions]]
- 사양: [[OME-NGFF]]
- 출처: [[SpatialData docs - Design doc]]

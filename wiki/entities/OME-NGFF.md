---
type: entity
title: OME-NGFF
area: [bioinformatics]
aliases: [NGFF, OME-Zarr, Next-Generation File Format, ome-ngff]
tags: [spatial-omics, imaging, data-format, standard, zarr]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[SpatialData docs - Design doc]]", "https://ngff.openmicroscopy.org/latest/"]
---

# OME-NGFF

OME(Open Microscopy Environment)의 **Next-Generation File Format** 사양. 대용량 생물
이미징 데이터를 클라우드 친화적으로 저장하기 위한 표준으로, Zarr 컨테이너에 이미지·라벨과
그 메타데이터를 담는 규칙을 정의한다. 흔히 **OME-Zarr**로도 불린다.

[[SpatialData]]는 이 사양을 **교환 포맷으로 채택**한다 — 자체 포맷을 새로 만드는 대신
NGFF를 따르고, NGFF가 규정하지 않는 부분만 확장한다. "포맷 컨버터를 만들지 않는다"는
SpatialData의 non-goal이 성립하는 근거가 바로 이것이다.

## NGFF가 규정하는 것 / 규정하지 않는 것

- **규정한다**: 래스터 타입 — [image layout](https://ngff.openmicroscopy.org/latest/#image-layout)
  (이미지·라벨), multiscale(피라미드) 표현, 축(axes)과 좌표계·좌표변환 메타데이터.
- **규정하지 않는다**: Points·Shapes 같은 비래스터 element, 표 형태의 주석.
  → 이 공백을 [[SpatialData elements]]와 [[Coordinate systems and transformations]]가 메운다.

## SpatialData가 상속하는 제약

NGFF를 따르기 때문에 SpatialData의 가정 상당수가 여기서 온다.

- 이미지/라벨은 intrinsic 좌표계를 **정확히 하나** 가진다.
- 좌표계는 이름이 있어야 하고, 모든 축을 명시해야 한다.
- 축 이름 제약: NGFF v0.4에서는 축 이름에 제약이 있고, v0.5부터 완화된다
  (그래서 시간축 지원이 v0.5 이후 과제로 남아 있다).

좌표변환 사양은 문서 작성 시점(v0.8.0)에 여전히 **제안 단계**였고
([ome/ngff PR #138](https://github.com/ome/ngff/pull/138)), SpatialData의 온디스크 표현과
제안된 NGFF 표현 사이에 작은 차이가 남아 있다고 명시된다. 사양이 확정되면 100% 준수를
목표로 한다.

## 링크

- 프레임워크: [[SpatialData]]
- 개념: [[SpatialData elements]], [[Coordinate systems and transformations]]
- 출처: [[SpatialData docs - Design doc]]

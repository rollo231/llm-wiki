---
type: concept
title: Coordinate systems and transformations
area: [bioinformatics]
aliases: [Coordinate systems, Coordinate transformations, 좌표계, 좌표변환, intrinsic coordinate system, extrinsic coordinate system]
tags: [spatial-omics, data-model, registration, ngff]
created: 2026-07-27
updated: 2026-07-27
sources: ["[[SpatialData docs - Design doc]]"]
---

# Coordinate systems and transformations

여러 데이터셋·모달리티를 같은 공간에 정렬하는 장치. [[SpatialData]]에서는
[[SpatialData elements]] 사이에 명시적 링크가 없으므로, **좌표계가 element를 의미적으로
묶는 유일한 수단**이라는 점에서 특히 중요하다.

**좌표계**는 이름을 가진 축(axis)의 집합이고, 각 축은 이름·타입·(선택적) 단위를 가진다.
**좌표변환**은 element를 한 좌표계에서 다른 좌표계로 옮기는 연산의 집합이다. 개념은
[[OME-NGFF]] 제안에서 왔다.

## intrinsic vs extrinsic

- **intrinsic**(암묵적) — element의 데이터 구조에 묶여 그것을 서술한다. 이미지의 intrinsic
  좌표계는 곧 그 배열의 축 집합이다. NGFF 관점에서 intrinsic 좌표계가 없는 이미지는 축
  정보가 없는 이미지다.
- **extrinsic**(명시적) — 특정 element에 매여 있지 않은 좌표계. 여러 데이터셋이 **공유하는
  공통 좌표계**를 정의할 때 쓴다.

용도로 보면: intrinsic은 "이 배열의 픽셀 공간", extrinsic은 "여러 데이터가 만나는 물리
공간"이다. 이미지의 좌표변환은 픽셀 공간 ↔ 물리 공간, 그리고 서로 다른 물리 공간 사이를
매핑한다.

## NGFF의 규칙 vs SpatialData의 완화

NGFF는 이미지·라벨만 규정하므로, SpatialData는 개념을 Points·Shapes까지 확장하는 대신
NGFF의 verbose한 제약 일부를 완화한다.

| | NGFF | SpatialData |
|---|---|---|
| 대상 | 이미지·라벨만 | 모든 element |
| intrinsic | 이미지/라벨마다 정확히 하나, 명시 필요 | **명시 불필요** — element 스키마에서 추론 |
| extrinsic | 이름 필수, 모든 축 명시 필수 | 이름 필수, **축 명시는 선택** |
| 변환 정의 범위 | 임의의 두 좌표계 사이 (intrinsic↔intrinsic 포함) | intrinsic ↔ extrinsic 사이만 (향후 완화 예정) |

SpatialData의 추가 규칙:

- 모든 element는 **최소 하나의 extrinsic 좌표계에 매핑되어야 한다.**
- 매핑을 지정하지 않으면 `"global"` 좌표계로 **Identity** 변환이 자동으로 정의된다.
- `Tables`는 좌표계를 가질 수 없다 — 이미 좌표계를 가진 Region을 주석하는 존재이므로.

프레임워크는 여전히 유효한 NGFF를 읽고 쓴다. SpatialData 좌표계로 변환이 불가능한 경우에는
예외를 발생시킨다.

## 변환 클래스가 두 세트인 이유

이 프레임워크에는 좌표변환 클래스 계층이 **둘** 있다. 헷갈리기 쉬운 지점이라 이유를 남긴다.

- **`NgffBaseTransformation` 계열** — 입출력(IO) 전용. `NgffIdentity`, `NgffMapAxis`,
  `NgffTranslation`, `NgffScale`, `NgffAffine`, `NgffRotation`, `NgffSequence`,
  `NgffByDimension`. (미지원: `NgffMapIndex`, `NgffDisplacements`, `NgffCoordinates`,
  `NgffInverseOf`, `NgffBijection`.)
- **`BaseTransformation` 계열** — 실제 연산용. `Identity`, `MapAxis`, `Translation`,
  `Scale`, `Affine`, `Sequence`.

**차이의 핵심**: `Ngff*`는 각 변환이 입력·출력 좌표계를 완전히 명시하도록 요구한다. 따라서
변환은 입력 좌표계와 호환돼야 하고, 두 변환을 연결하려면 앞의 출력 좌표계와 뒤의 입력
좌표계가 일치해야 한다. 반면 `BaseTransformation`은 **self-defined** — 좌표계 정보가 필요
없고, 거의 모든 변환을 거의 모든 element에 적용하고 서로 연결할 수 있다. 결과가 유일하게
정해지지 않으면 예외를 던진다.

이를 가능하게 하는 규칙은 **축 pass-through**다: element에는 있지만 변환에는 없는 축은
그대로 통과시키고, 변환에는 있지만 element에는 없는 축은 무시한다.

- 적용 가능: `Scale([2, 3, 4], axes=('x','y','z'))`를 `cyx` 이미지에 적용 → `c`는 통과,
  `z` 스케일은 무시.
- 적용 불가: `Affine xy -> xyz`를 `xyz` 데이터에 적용 → `z`가 변환의 출력이기도 해서
  통과시킬 수 없다.

두 계열 사이의 변환은 v0.8.0 문서 시점에 100% 지원되지 않으며, NGFF 사양이 승인되면
마무리할 예정이다.

## 지원되는 변환

Identity, scale, translation, rotation, affine, 그리고 이들의 sequence. 축 permute 유틸리티
제공. **비선형 변환(coordinates·displacements)은 미지원**이며 우선순위 P2로 남아 있다 —
비선형 정합이 필요한 작업에는 지금의 SpatialData만으로는 부족하다는 뜻이다.

### 표현 못 하는 변환을 만나면: 데이터에 미리 굽는다

[[Visium HD]] 리더의 CytAssist 이미지 정렬이 실전 사례다. 이 정렬은 **projective(투영) 변환**을
요구하는데 affine까지만 표현할 수 있으므로, 리더는 투영 행렬을 **affine 성분 + projective
shift로 분해**한 뒤

- projective shift는 skimage `warp`로 **픽셀을 실제로 변형**해 흡수하고,
- 남은 affine만 좌표변환으로 심는다.

즉 프레임워크가 표현할 수 없는 부분은 데이터에 미리 적용해 표현 가능한 범위로 끌어내린다.
대가는 원본 픽셀의 손실(재샘플링)이며, 대상 이미지가 작아 메모리에서 계산할 수 있어 성립한다.

## 링크

- 프레임워크: [[SpatialData]]
- 데이터 모델: [[SpatialData elements]]
- 사양: [[OME-NGFF]]
- 실전 사례: [[Visium]](좌표계 3중 구조), [[Visium HD]](투영 변환 우회), [[Xenium]]·[[MERSCOPE]](micron→pixel)
- 출처: [[SpatialData docs - Design doc]], [[spatialdata-io docs - README and readers]]

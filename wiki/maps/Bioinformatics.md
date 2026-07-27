---
type: moc
title: Bioinformatics
area: [bioinformatics]
aliases: [생물정보학, 바이오인포매틱스, Bioinformatics MOC]
tags: [bioinformatics, spatial-omics, spatial-transcriptomics]
created: 2026-07-27
updated: 2026-07-27
sources: []
---

# Bioinformatics

**bioinformatics** 영역의 Map of Content. 현재는 **공간 오믹스(spatial omics) 데이터 인프라**를
중심으로 쌓이고 있다 — 데이터를 어떻게 저장하고, 표현하고, 정렬하는가.

## 프레임워크·사양

- [[SpatialData]] — 공간 오믹스용 저장 포맷·스키마·인메모리 표현을 묶은 scverse 프레임워크.
- [[OME-NGFF]] — SpatialData가 교환 포맷으로 채택한 OME의 차세대 이미징 사양(OME-Zarr).

## 개념

- [[SpatialData elements]] — 데이터 모델의 빌딩 블록 5종(Images·Labels·Shapes·Points·Tables).
- [[Coordinate systems and transformations]] — intrinsic/extrinsic 좌표계와 정렬 방식.

## 출처

- [[SpatialData docs - Design doc]] — SpatialData 공식 설계 문서(v0.8.0): 목표·비목표·사양·로드맵.

## 열린 질문

이 영역이 자라면서 파볼 지점.

- v0.8.0 문서의 **2025 로드맵**(`ome-zarr-models-py` 이전, Zarr v3 sharding, dask 제약 제거)이
  실제로 어디까지 진행됐는가 — changelog로 확인 필요.
- **Squidpy**가 SpatialData 객체를 받도록 리팩터되었는가 (문서 시점 P2·미완).
- 비선형 정합이 필요한 작업은 지금 무엇으로 하는가 — SpatialData는 비선형 변환 미지원(P2).
- 실제 기술별 적재 경로: `spatialdata-io`가 Visium·Xenium·Stereo-seq 등을 어떻게 읽는가.

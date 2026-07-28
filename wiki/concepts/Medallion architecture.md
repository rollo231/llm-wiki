---
type: concept
title: Medallion architecture
area: [data-engineering]
aliases:
  - Medallion
  - Bronze silver gold
  - 메달리온 아키텍처
  - 브론즈 실버 골드
tags: [data-engineering, medallion, data-modeling, pipeline, lakehouse]
created: 2026-07-28
updated: 2026-07-28
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers"]
---

# Medallion architecture

같은 데이터가 파이프라인 안에서 **여러 정제 단계로 동시에 존재**할 때, 그 단계를 세 층으로 나누는
관례. 층마다 별도 저장소를 두는 것도 가능하지만(raw는 레이크, processed는 웨어하우스), 실제로는
**같은 저장소를 재사용해 생애 단계만 나누는** 경우가 흔하다.

| 층 | 무엇 | 누가 본다 |
|---|---|---|
| **Bronze** | 소스에서 온 그대로의 raw 데이터 | 파이프라인을 디버깅하는 엔지니어 |
| **Silver** | 정제·정합화 — 타입 교정, 중복 제거, 여러 소스를 한 테이블로 조인 | 중간 소비자 |
| **Gold** | 집계·모델링 — 대시보드나 리포트 같은 특정 용도에 맞춘 모양 | 분석가 |

## 왜 생기는가

[[ETL and ELT|ELT]]에서 raw를 먼저 쏟아붓고 나중에 변환하기 때문이다. raw와 processed가 **둘 다**
저장돼야 하고, 그 사이 단계까지 포함하면 세 층이 자연스럽게 나온다.

## 정제도만 말한다 — 모양은 말하지 않는다

메달리온은 **얼마나 정제됐는가**의 축이다. 그 데이터가 *어떤 모양의 테이블* 인지에 대해서는 아무
말도 하지 않는다. 모양은 별개 축이고 [[Dimensional modeling]]이 담당한다 — fact/dimension으로
나눌 것인지, star schema를 쓸 것인지, 아니면 그냥 넓은 비정규화 테이블 하나로 갈 것인지.

두 축은 교차한다: **data mart**(팀·주제별 슬라이스)는 보통 **gold** 층에 산다.

## 링크

- 직교하는 축: [[Dimensional modeling]] — 정제도가 아니라 모양
- 왜 층이 필요한가: [[ETL and ELT]]
- 어디에 얹히나: [[Analytical data storage tiers]]
- 적용: [[SpatialData as a data engineering substrate]] — 공간 오믹스 파이프라인을 bronze(장비 원본)
  / silver(검증 통과한 불변 store) / gold(Iceberg 위의 obs·QC 테이블)로 나눈 설계
- 출처: [[Data landscape guide for developers]]

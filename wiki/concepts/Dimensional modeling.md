---
type: concept
title: Dimensional modeling
area: [data-engineering]
aliases:
  - Fact table
  - Dimension table
  - Star schema
  - Snowflake schema
  - Grain
  - Data mart
  - One big table
  - OBT
  - 차원 모델링
  - 팩트 테이블
  - 스타 스키마
tags: [data-engineering, data-modeling, kimball, data-warehouse, star-schema]
created: 2026-07-28
updated: 2026-07-28
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers"]
---

# Dimensional modeling

웨어하우스의 테이블을 조직하는 방식. **Ralph Kimball**이 *The Data Warehouse Toolkit* 에서
대중화했다. 분석가가 "fact table", "grain" 같은 말을 쓸 때 나오는 어휘가 전부 여기서 온다.

[[Medallion architecture]]가 *얼마나 정제됐는가* 를 말한다면, 차원 모델링은 *어떤 모양인가* 를
말한다 — 두 축은 직교한다.

## 두 종류의 테이블

- **Fact table** — **이벤트나 측정값**을 담는다. 주문 1건, 결제 1건, 페이지뷰 1건이 한 행.
  길고 좁다(long and narrow). 대부분 숫자와 dimension 테이블을 가리키는 외래 키로 이뤄지고,
  계속 자란다.
- **Dimension table** — 그 fact가 **어떤 맥락에서 일어났는지**를 담는다. 고객 1명, 상품 1개,
  달력 날짜 1일이 한 행. 넓고(wide), 덜 바뀐다.

## 스키마 모양

- **Star schema** — fact table을 가운데 두고 dimension들을 둘러 그리면 별 모양이 된다.
- **Snowflake schema** — 더 정규화한 변형. **Snowflake 웨어하우스와는 아무 관계가 없다.**

## 두 용어 더

- **Grain(그레인)** — 한 행이 무엇을 나타내는가. 주문 1건인가? 주문 라인 1건인가? 고객별·일자별
  주문인가? 테이블 설계에서 가장 먼저 못박아야 하는 것.
- **Data mart** — 한 팀이나 한 주제에 맞춰 모델링한 웨어하우스의 슬라이스. 마케팅 마트, 재무 마트.
  보통 [[Medallion architecture|gold]] 층에 산다.

## 반론 — one big table

모든 팀이 이걸 엄격히 따르지는 않는다. **현대 웨어하우스가 빠르고 스토리지가 상대적으로 싸서**,
특정 용도를 위해 그냥 넓은 비정규화 테이블 하나를 만드는 팀도 많다 — 이걸 **"one big table"(OBT)**
접근이라 부르기도 한다.

## 링크

- 직교하는 축: [[Medallion architecture]] — 모양이 아니라 정제도
- 사는 곳: [[Analytical data storage tiers]]
- 정의의 단일 출처: [[Data catalog and semantic layer]] — "어느 orders 테이블을 써야 하나",
  "revenue에 환불이 포함되나" 같은 질문은 모델링만으로 안 풀리고 semantic layer가 필요하다
- 출처: [[Data landscape guide for developers]]

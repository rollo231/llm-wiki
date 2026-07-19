---
type: concept
title: Traditional data engineering
area: [data-engineering]
aliases: [기존 DE, 전통적 데이터 엔지니어링, DW·BI 데이터 엔지니어링]
tags: [data-engineering, data-warehouse, business-intelligence]
created: 2026-07-19
updated: 2026-07-19
sources: [raw/data-engineering/ch01-1-de-vs-ai-de-ot.pdf]
---

# Traditional data engineering

정형 데이터를 수집·정제해 데이터 웨어하우스(DW)에 적재하고, BI로 의사결정을 돕는 형태의 데이터
엔지니어링. [[AI data engineering]]과 대비되는 "기존" 방식. 처음 등장: [[AI DE Course - Ch1-1 OT]].

## 핵심 역할

- **정형 데이터 파이프라인**: 엑셀·ERP 등 정형 데이터 수집 → 정제 → DW 적재.
- **BI·대시보드**: 수집 데이터로 차트/그래프, 경영진용 대시보드 제공.
- **품질·정합성**: 오류 수정·중복 제거, 거버넌스로 데이터 신뢰성 유지.

## 파이프라인

수집(정형 데이터) → 클렌징(ETL/ELT) → 저장(DW) → 분석/시각화(BI 대시보드).

## 한 줄

정형 데이터를 정리해 경영진 의사결정을 돕는 **인사이트 제공자**.

## 링크

- 대비: [[AI data engineering]]
- 출처: [[AI DE Course - Ch1-1 OT]]

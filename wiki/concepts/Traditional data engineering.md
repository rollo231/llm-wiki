---
type: concept
title: Traditional data engineering
area: [data-engineering]
aliases: [기존 DE, 전통적 데이터 엔지니어링, DW·BI 데이터 엔지니어링]
tags: [data-engineering, data-warehouse, business-intelligence]
created: 2026-07-19
updated: 2026-07-28
sources: ["raw/data-engineering/ch01-1-de-vs-ai-de-ot.pdf", "https://sinja.io/blog/data-landscape-guide-for-developers"]
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

## 다른 축의 분류

[[Data landscape guide for developers]]는 같은 지형을 **다른 축**으로 나눈다. 시간축(기존 DE →
AI DE)이 아니라 **공존하는 4직군**이다: **analytical**(data analyst·BI analyst — SQL·스프레드시트·
Tableau) / **scientific**(data scientist — Python·노트북) / **engineering**(data engineer —
파이프라인·Spark·웨어하우스) / **machine learning**(모델 학습·배포).

이 페이지의 "기존 DE"는 그 분류에서 **engineering type과 analytical type에 걸쳐 있다.**
파이프라인을 짓는 쪽과 BI로 인사이트를 내는 쪽이 여기서는 한 직무의 두 국면이지만, 저 글에서는
도구도 일과도 다른 별개 직군이다. 저 글의 data engineer는 BI 대시보드를 만들지 않는다 —
분석가가 효율적으로 쿼리할 수 있게 만드는 데까지가 일이다.

어느 쪽이 현업의 실제 모습인지는 아직 근거가 없다(둘 다 1차 자료 없는 개괄이다).
→ [[Data Engineering]] MOC의 열린 질문.

## 링크

- 대비: [[AI data engineering]]
- 다른 축: [[Data landscape guide for developers]]
- 출처: [[AI DE Course - Ch1-1 OT]]

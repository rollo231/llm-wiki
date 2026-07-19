---
type: source
title: AI DE Course - Ch1-1 OT
area: [data-engineering]
aliases: [CH01-1 OT, 기존 DE vs AI DE, DE vs AI DE OT]
tags: [data-engineering, course, fast-campus]
created: 2026-07-19
updated: 2026-07-19
sources: [raw/data-engineering/ch01-1-de-vs-ai-de-ot.pdf]
---

# AI DE Course - Ch1-1 OT

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · 챕터 **CH01-1 [OT]**
"기존 DE vs AI DE: 데이터 적재에서 모델 지원으로의 변화". 원본(로컬):
`raw/data-engineering/ch01-1-de-vs-ai-de-ot.pdf`. 강의 홈: [[AI Data Engineering (Fast Campus course)]].

오리엔테이션 챕터. 데이터 엔지니어링의 목적이 "정형 데이터를 적재해 의사결정을 돕는 것"에서
"AI 모델의 학습·추론을 지원하는 것"으로 어떻게 이동하는지를 개괄한다.

## 요점

- **기존 DE → [[Traditional data engineering]]**: DW·BI 중심. 수집(정형) → 클렌징(ETL/ELT) →
  저장(DW) → 분석/시각화(BI). 품질·정합성·거버넌스로 신뢰성 확보. 목적은 경영진 의사결정 인사이트.
- **AI DE → [[AI data engineering]]**: 모델 학습(고품질 데이터·버전관리·GPU 스케줄링·실험관리),
  추론(서빙·레이턴시·오토스케일링·모니터링), 비정형 데이터(이미지·오디오·비디오·텍스트 → 텐서).
- **왜 지금**: 데이터의 ~80%가 비정형이고, 실시간 수요가 커짐(YouTube·Coupang 등).
- **한 줄 대비**: DE = 정형 데이터로 의사결정 돕는 "인사이트 제공자" / AI DE = 비정형까지 다루며
  AI 모델을 돕는 "시스템 건축가".

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Traditional data engineering]], [[AI data engineering]]

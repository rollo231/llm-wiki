---
type: moc
title: Data Engineering
area: [data-engineering]
aliases: [데이터 엔지니어링, DE, Data Engineering MOC]
tags: [data-engineering, data-pipeline, storage, orchestration]
created: 2026-07-27
updated: 2026-07-27
sources: []
---

# Data Engineering

**data-engineering** 영역의 Map of Content. 현재 두 갈래로 쌓이고 있다 — 직무·방식의 변화(기존 DW·BI
중심 → AI·비정형 지원)와, 실제 저장 포맷을 파이프라인 관점에서 읽는 작업.

## 기본 개념

- [[Traditional data engineering]] — 정형 데이터를 DW에 적재하고 BI로 의사결정을 돕는 기존 방식.
- [[AI data engineering]] — 비정형 데이터와 모델 라이프사이클(학습·추론)을 지원하는 확장된 방식.

## 저장 포맷을 파이프라인 관점으로

- [[SpatialData as a data engineering substrate]] — 공간 오믹스 포맷([[SpatialData]])을
  레이크하우스 층위로 분해하고, 그 위의 ETL·카탈로그를 설계한다. 이 영역과
  [[Bioinformatics]] 영역이 겹치는 지점.

## 출처

- [[AI DE Course - Ch1-1 OT]] — Fast Campus DE 강의 OT: 기존 DE vs AI DE.

### 진행 중인 코스

- [[AI Data Engineering (Fast Campus course)]] — 챕터 트래커.

## 열린 질문

이 영역이 자라면서 파볼 지점.

- **직무 구분의 실제 경계** — 강의는 기존 DE와 AI DE를 대비시키지만, 현업에서 두 역할이 실제로
  분리되어 있는지, 아니면 같은 사람이 둘 다 하는지는 아직 근거가 없다.
- **테이블 포맷(Iceberg·Delta·Hudi) 자체를 다룬 소스가 없다.**
  [[SpatialData as a data engineering substrate]]가 Iceberg를 카탈로그·gold 층으로 전제하고 쓰는데,
  정작 Iceberg 쪽 지식은 위키에 들어온 적이 없다 — 그 노트의 가장 약한 발판.
- **오케스트레이터 비교**(Airflow vs Argo vs Prefect·Dagster) — 위 노트가 Airflow를 고르지만
  근거가 "이미 쓰고 있어서"에 가깝다. 선택 기준을 다룬 소스가 필요하다.
- **비정형 데이터의 "텐서 변환·저장" 실무** — [[AI data engineering]]이 핵심 역할로 꼽지만
  구체적 방법론(포맷·청킹·로더)은 비어 있다. 공간 오믹스 쪽에서 쌓은 Zarr 지식이 여기로
  일반화되는지 확인해볼 지점.

## 링크

- 인접 영역 MOC: [[Bioinformatics]]

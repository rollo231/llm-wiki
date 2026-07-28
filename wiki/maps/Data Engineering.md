---
type: moc
title: Data Engineering
area: [data-engineering]
aliases: [데이터 엔지니어링, DE, Data Engineering MOC]
tags: [data-engineering, data-pipeline, storage, orchestration]
created: 2026-07-27
updated: 2026-07-28
sources: []
---

# Data Engineering

**data-engineering** 영역의 Map of Content. 세 갈래로 쌓이고 있다 — 파이프라인 전체를 훑는
랜드스케이프 어휘, 직무·방식의 변화(기존 DW·BI 중심 → AI·비정형 지원), 그리고 실제 저장 포맷을
파이프라인 관점에서 읽는 작업.

## 여기서 시작

[[Data landscape guide for developers]] — 데이터 팀 어휘 전체를 한 번에 훑는 지도. 아래 개념
페이지 대부분이 여기서 나왔다. 툴 이름이 처음 보이는 게 어느 단계에 속하는지 모르겠으면 여기부터.

## 파이프라인을 따라가며

1. **어디서 오고 어떻게 흐르나** — [[ETL and ELT]]
   추출·변환·적재, ELT가 순서를 바꾸는 이유, 인제스천 툴과 CDC, 반대 방향의 reverse ETL.
2. **어떤 바이트로** — [[Columnar and in-memory data formats]]
   Parquet은 스캔 최적화, Arrow는 처리 최적화. CSV·ORC·Avro의 자리.
3. **어디에 담나** — [[Analytical data storage tiers]]
   웨어하우스 / 레이크 / 레이크하우스를 구조 강제·쿼리 엔진 결합·비용 세 축으로.
4. **레이크를 레이크하우스로 만드는 층** — [[Table formats]]
   Iceberg·Delta·Hudi. ACID·스키마 진화·time travel이 왜 여기 붙는가.
5. **언제 처리하나** — [[Batch and stream processing]]
   배치 vs 스트림, Kafka가 메시지 큐와 다른 점, 그리고 **오케스트레이터는 배치 전용**이라는 경계.
6. **어떤 단계로 착지하나** — [[Medallion architecture]] (정제도: bronze/silver/gold)
   × [[Dimensional modeling]] (모양: fact·dimension·star·grain). **두 축은 직교한다.**
7. **무엇이 어디에 있고 무엇을 뜻하나** — [[Data catalog and semantic layer]]
   metastore(기계용) ≠ data catalog(사람용) ≠ semantic layer(정의용). + lineage와 거버넌스.

## 직무·방식

- [[Traditional data engineering]] — 정형 데이터를 DW에 적재하고 BI로 의사결정을 돕는 기존 방식.
- [[AI data engineering]] — 비정형 데이터와 모델 라이프사이클(학습·추론)을 지원하는 확장된 방식.

두 페이지는 **시간축**(기존 → AI) 분류이고, [[Data landscape guide for developers]]는 **공존축**
(analytical / scientific / engineering / ML) 분류다. 같은 지형을 다른 축으로 자른 것 — 각 페이지의
"다른 축의 분류" 절 참고.

## 저장 포맷을 파이프라인 관점으로

- [[SpatialData as a data engineering substrate]] — 공간 오믹스 포맷([[SpatialData]])을
  레이크하우스 층위로 분해하고, 그 위의 ETL·카탈로그를 설계한다. 이 영역과
  [[Bioinformatics]] 영역이 겹치는 지점.

## 출처

- [[Data landscape guide for developers]] — OlegWock, sinja.io (2026-07-14). 개발자를 위한 데이터
  랜드스케이프 가이드.
- [[AI DE Course - Ch1-1 OT]] — Fast Campus DE 강의 OT: 기존 DE vs AI DE.

### 진행 중인 코스

- [[AI Data Engineering (Fast Campus course)]] — 챕터 트래커.

## 열린 질문

이 영역이 자라면서 파볼 지점.

- **Iceberg 1차 문서가 필요하다.** [[Table formats]]가 개념 층위는 세웠지만 세 포맷의 **선택
  기준**과 스냅샷·매니페스트의 **온디스크 구조**는 여전히 없다.
  [[SpatialData as a data engineering substrate]] §4를 검증하려면 이게 있어야 한다. **현재 1순위.**
- **오케스트레이터 비교**(Airflow vs Dagster vs Prefect·Argo) — 경계는 좁혀졌다
  ([[Batch and stream processing]]: 오케스트레이터는 배치 전용, 스트리밍은 스트림 프로세서 몫).
  하지만 **배치 안에서 무엇을 고를지**의 기준은 여전히 없다 — 어느 소스도 넷을 비교하지 않았다.
- **직무 구분의 실제 경계** — 시간축(강의)과 공존축(랜드스케이프 가이드) 중 어느 쪽이 현업의
  실제 모습인지 아직 근거가 없다. 둘 다 1차 자료 없는 개괄이다. 채용 공고나 팀 구성 사례 같은
  1차 자료가 있으면 갈린다.
- **비정형 데이터의 "텐서 변환·저장" 실무** — [[AI data engineering]]이 핵심 역할로 꼽지만
  구체적 방법론(포맷·청킹·로더)은 비어 있다. 랜드스케이프 가이드도 ML은 의도적으로 비워뒀다
  (저자가 자기 지식이 제한적이라고 명시). 공간 오믹스 쪽에서 쌓은 Zarr 지식이 여기로 일반화되는지
  확인해볼 지점.
- **데이터 품질·관측성의 실제 도입** — Great Expectations·dbt tests(수동 정의) vs Monte Carlo·
  Bigeye(자동 이상 탐지)의 갈림. 랜드스케이프 가이드가 존재만 알리고 넘어갔다.
- **semantic layer는 실제로 쓰이는가** — 개념은 선명하지만(정의의 단일 출처) 채택률과 실패 사례에
  대한 근거가 없다. LLM 에이전트가 웨어하우스를 질의하는 맥락에서 다시 뜨는 주제라 확인 가치가 있다.

## 링크

- 인접 영역 MOC: [[Bioinformatics]]

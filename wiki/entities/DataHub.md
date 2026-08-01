---
type: entity
title: DataHub
area: [data-engineering]
aliases: [데이터허브, 데이터 허브]
tags: [data-engineering, metadata, catalog, lineage, graph, datahub]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part3 Ch2 Graph fundamentals]]", "[[AI DE Course - Part3 Ch2 Graph in practice]]"]
---

# DataHub

**메타데이터 그래프의 대표 구현.** 데이터 자산과 그 관계를 그래프로 관리해 탐색·리니지·영향도 분석을
제공하는 도구.

강의는 [[Knowledge graph]] 챕터에서 **"데이터 엔지니어 관점에서 가장 직관적인 그래프 활용처는
메타데이터 관리"** 라고 말하면서 대표 예로 DataHub를 든다.

## 무엇을 그래프로 두나

| 노드 | 엣지 |
|---|---|
| `Dataset` `Column` `ETL Job` `DataFlow` `Dashboard` `Chart` `Metric` `Owner` `Team` `Tag` | `upstream` `downstream` `owns` `documents` `uses` `transforms` |

이렇게 두면 단순 메타데이터 저장을 넘어 **영향도 분석과 탐색**이 가능해진다:

- 이 컬럼이 바뀌면 어떤 대시보드가 깨지는가
- 이 데이터셋은 어떤 잡이 만들었는가
- 이 리포트는 어떤 테이블과 어떤 팀에 연결되는가
- 이 모델 feature는 어떤 원천 데이터에서 왔는가

## 왜 그래프여야 하나

> **"정답이 한 개 문서 안에 있지 않다. 여러 자산 사이 관계를 따라가야만 답할 수 있다."**

메타데이터 그래프는 다섯 가지를 동시에 가능하게 한다 — 탐색형 질의 · 연관 자산 추천 · 영향도 분석 ·
변경 안전성 판단 · 지식 축적.

## ⚠️ 강의가 다루는 깊이

**로고와 이름 수준의 언급이다.** 아키텍처(GMS·메타데이터 모델·ingestion framework), 경쟁 도구
(Amundsen · OpenMetadata · Atlas), 도입 경험은 나오지 않는다.
→ [[Data catalog and semantic layer]]의 "카탈로그 제품 선택" 공백과 같은 성격의 미해결 지점.

## 링크

- [[Knowledge graph]] — 메타데이터 그래프와 리니지
- [[Data catalog and semantic layer]] — metastore / catalog / semantic layer 3분법과 lineage
- [[Knowledge graph pipeline]] — 메타데이터 그래프를 실제로 채우는 파이프라인
- [[Graph database]] — 저장 계층
- 강의: [[AI Data Engineering (Fast Campus course)]]

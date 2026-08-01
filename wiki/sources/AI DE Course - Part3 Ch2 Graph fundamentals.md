---
type: source
title: AI DE Course - Part3 Ch2 Graph fundamentals
area: [data-engineering]
aliases: [Part3 Ch2-1, Graph에 대해 이해하기1]
tags: [data-engineering, course, fast-campus, graph, knowledge-graph, metadata, lineage]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/Part 3_Ch 2.pdf (p1–20)"]
---

# AI DE Course - Part3 Ch2 Graph fundamentals

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch2 "Graph에 대한 이해"의 소단원 **1**
"Graph에 대해 이해하기1". 원본(로컬): `raw/data-engineering/Part 3_Ch 2.pdf` **p1–20** (74p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> **주의:** Ch2의 소단원 4개는 **제목이 전부 "Graph에 대해 이해하기 1/2/3/4"로 같다.** 내용은 각각
> 기초 / PG vs RDF / 실무 활용 / AI+Graph로 뚜렷이 다르다. 제목만 보고 합치면 안 된다.

## 구성

`01 Graph란? · 02 Graph의 종류 · 03 지식그래프 · 04 실서비스에서의 Graph · 05 데이터엔지니어에게 Graph`

## 왜 Graph — 관계를 1급 데이터로

> **"데이터는 개체 자체보다 개체 사이 연결이 더 중요한 경우가 있다."**
> **"무엇이 있는가 → 무엇과 어떻게 연결되는가."**
> **속성 중심 데이터 이해에서 관계 중심 데이터 이해로.**
> **"관계를 1급 데이터로 보는 사고의 필요성."**

## 구성 요소와 읽는 단위

Node / Edge(Relationship) / Property / Label. 그리고 Path / Hop / Pattern.

> **"모든 실체가 node가 될 수 있다"** — 사람, 상품, 카테고리, 검색어, **테이블, 컬럼, DAG, 대시보드,
> ML Feature, 모델 버전.**
> 이 예시 목록이 이미 DE 도메인 쪽으로 기울어 있고, 05절의 복선이다.

Path 예시가 좋다: `Dashboard → Chart → Dataset → ETL Job → Source Table`.
Pattern 예시: "이 지표를 깨뜨릴 수 있는 upstream asset 조합".

→ 상세는 [[Graph data model]]

## 그래프의 종류

Directed/Undirected · Weighted · Homogeneous/Heterogeneous.

> **"데이터 파이프라인 lineage, dependency, ownership 같은 실무에서의 관계는 대부분 방향성이 중요하다."**
> **"현실의 서비스 데이터는 대부분 heterogeneous graph다."**

## 지식그래프

> **"단순 키워드 저장이 아니라 이것이 무엇이며 다른 것과 어떤 관계를 갖는가를 명시적으로 표현."**

`서울 - 수도이다 - 대한민국` (subject-predicate-object). Google 공식 도움말이 Knowledge Graph를
*people, places, things*에 대한 *billions of facts*를 담은 데이터베이스로 설명한다고 인용.

**Google Search의 knowledge panel** 사례:

> **"검색 결과 화면의 박스 자체가 아니라, 그 박스를 가능하게 하는 데이터 모델이다.
> 검색어를 단순 문자열로만 처리하지 않고 사람·장소·사물·조직 같은 entity와 그 관계를 기준으로
> 이해한다는 점."**

이미 대규모 검색 시스템에서 **factual information organization**과 **entity-centric retrieval**의
기반으로 쓰이는 실전 기술이라는 프레이밍.

→ [[Knowledge graph]]

## ⭐ 데이터 엔지니어에게 — 메타데이터 그래프와 Lineage

**이 소단원에서 DE에게 가장 직접적인 대목.**

> **"데이터 엔지니어링 환경은 생각보다 그래프에 매우 적합한 도메인이다."**

노드: `Dataset` `Column` `ETL Job` `DataFlow` `Dashboard` `Chart` `Metric` `Owner` `Team` `Tag`
엣지: `upstream` `downstream` `owns` `documents` `uses` `transforms`

→ **단순 메타데이터 저장을 넘어 영향도 분석과 탐색이 가능해진다:**

- 이 컬럼이 바뀌면 어떤 대시보드가 깨지는가
- 이 데이터셋은 어떤 잡이 만들었는가
- 이 리포트는 어떤 테이블과 어떤 팀에 연결되는가
- 이 모델 feature는 어떤 원천 데이터에서 왔는가

대표 예로 **[[DataHub]]** 를 로고와 함께 든다. (설명은 없다)

> **[[Data catalog and semantic layer]]가 말하던 lineage에 "그래프"라는 구현 형태가 처음 붙는다.**

## 언제 Graph를 고려할까

| Graph가 강한 문제 | 굳이 쓰지 않아도 되는 문제 |
|---|---|
| 다단계 연결 탐색이 자주 필요 | 단순 집계와 리포팅 중심 |
| 몇 hop 떨어진 이웃을 분석 | 행 단위 CRUD 위주 |
| upstream/downstream 영향도 추적 | 관계보다 속성 필터가 핵심 |
| 추천 후보를 연결 기반으로 확장 | 한두 번의 정형 join이면 충분한 경우 |
| entity 간 패턴을 찾아야 함 | |
| 메타데이터와 비즈니스 맥락을 함께 연결해야 함 | |

**설계 전 5문항:** 핵심 객체는? / 관계가 방향성을 가지나? / 관계 자체에 속성이 붙나? /
업무 질문이 2-hop, 3-hop, n-hop 탐색으로 바뀌나? / 스키마보다 연결 구조의 해석이 더 중요한가?

> 이 "안 써도 되는 경우"를 먼저 말하는 태도가 좋다. Part 2 Ch5의 "Feature Store가 불필요한 경우"와
> 같은 결이다.

## 기존 페이지와의 대조

- **새 concept:** [[Graph data model]] · [[Knowledge graph]] / **새 entity:** [[DataHub]]
- **보강** — [[Data catalog and semantic layer]]의 lineage 서술에 구현 형태가 붙는다.
- **[[NoSQL]]과의 연결** — Ch1에서 4타입 중 하나로 한 줄이던 Graph가 여기서 본격화된다.

## 자료 품질

- 인용 이미지 출처 대부분 표기 없음(그래프 레벨 다이어그램, hop 다이어그램, homo/hetero 그림,
  Author-Paper-Venue heterogeneous graph 그림). **Ch1보다 표기가 나쁘다.**
- DataHub는 **로고와 이름만** — 아키텍처·경쟁 도구·도입 경험 없음.
- 출처 없는 수치 없음.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Graph data model]] · [[Knowledge graph]] · [[Data catalog and semantic layer]] ·
  [[NoSQL]] · [[Graph database]]
- 도구: [[DataHub]]
- 앞: [[AI DE Course - Part3 Ch1 Semantics]]
- 다음: [[AI DE Course - Part3 Ch2 Property graph vs RDF]]

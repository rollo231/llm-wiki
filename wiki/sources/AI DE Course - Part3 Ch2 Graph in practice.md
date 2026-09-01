---
type: source
title: AI DE Course - Part3 Ch2 Graph in practice
area: [data-engineering]
aliases: [Part3 Ch2-3, Graph에 대해 이해하기3, 실무에서의 Graph]
tags: [data-engineering, course, fast-campus, graph, metadata, lineage, recommendation, search]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part3/02. Ch2. Graph에 대한 이해.pdf (p36–51)"]
---

# AI DE Course - Part3 Ch2 Graph in practice

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch2의 소단원 **3**
"Graph에 대해 이해하기3". 원본(로컬): `raw/data-engineering/ai-de-course/part3/02. Ch2. Graph에 대한 이해.pdf` **p36–51** (16p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

## 구성

`01 Graph는 언제 써야 하는가 · 02 실무에서의 Graph, 메타데이터 · 03 리니지 · 04 추천 · 05 검색`

네 가지 use case를 도는데, **02·03(메타데이터·리니지)이 DE에게 가장 가깝고 강의도 그렇게 배치한다.**

## ⭐ "JOIN이 많아지면 Graph를 쓴다"는 기준이 아니다

> **"단순 JOIN 횟수가 아니라 문제의 의미가 다단계 연결 탐색일 때."**

| RDB가 잘하는 질문 | Graph가 더 자연스러운 질문 |
|---|---|
| 어제 주문 건수는 몇 건인가 | 이 지표가 깨졌을 때 어떤 잡과 어떤 소스까지 영향이 전파되는가 |
| 카테고리별 매출 합계는 얼마인가 | 이 상품을 본 사용자와 유사 행동을 보인 다른 사용자들은 무엇을 구매했는가 |
| 상위 10개 상품은 무엇인가 | 같은 전화번호, 기기, 주소를 공유한 계정 묶음은 무엇인가 |

**그래프가 잘 맞는 문제의 공통점 4가지:** 엔터티보다 관계가 더 중요 · 질문이 1-hop에서 끝나지 않음 ·
재귀적 탐색 또는 패턴 탐색이 필요 · **스키마가 고정되어 있더라도 연결 구조가 계속 진화**.

마지막 항목이 좋다 — 새 이벤트 타입, 새 관계, 새 자산 유형이 계속 추가되는 환경.

## 메타데이터 관리와 데이터 카탈로그

| 실무에서 필요한 질문 | 그래프로 관리해야 하는 이유 |
|---|---|
| 이 테이블은 어디서 생성되는가 | 계보 추적 가능 |
| 어떤 대시보드가 이 데이터를 사용하는가 | 영향도 분석 가능 |
| 누가 책임지고 있는가 | 책임자와 문서 연결 가능 |
| 변경 시 어디까지 영향이 가는가 | 검색과 탐색 품질 향상 |

다이어그램: `Documentation --documented by--> Dataset --owned by--> Owner`,
`Dataset → Table --produces--> ETL Job --feeds--> Dashboard --calculates--> Metric`,
`Tag --tagged with--> Dashboard <--linked to-- Glossary`

> ⭐ **"단순 검색보다 컨텍스트. '이 대시보드는 어떤 데이터셋 쓰나요?', '이 컬럼은 어느 파이프라인에서
> 만들어졌나요?' — 정답이 한 개 문서 안에 있지 않다. 여러 자산 사이 관계를 따라가야만 답할 수 있다."**

메타데이터 그래프가 동시에 가능하게 하는 다섯 가지: 탐색형 질의 · 연관 자산 추천 · 영향도 분석 ·
**변경 안전성 판단** · 지식 축적.

## Lineage — 문서에서 도구로

> ⭐ **"lineage는 그래프로 모델링할 때 비로소 '정적 문서'가 아니라 탐색 가능한 운영 도구가 된다."**

lineage는 본질적으로 **경로 정보** — `source → transformation → model → dashboard`.
"이 테이블 수정하니까 대시보드 에러나요"가 lineage 질문이다.

컬럼 레벨 lineage UI 스크린샷 한 장(`PET_DETAILS.species` → 4개 다운스트림 자산으로 뻗는 화면).
**출처 표기 없음** — 어느 제품 화면인지 밝히지 않는다.

## 추천

사용자–상품 직접 관계만이 아니라 `사용자–상품–카테고리`, `사용자–상품–다른 사용자–다른 상품` 같은
다단계 연결을 자연스럽게 탐색. 추천은 결국 **현재 행동과 과거 행동을 연결하고, 다른 사용자와의
유사성을 연결하고, 상품 속성 및 지식 정보를 연결하는 문제.**

**cold-start** — 사용자 로그가 적거나 신규 아이템이라 상호작용 기록이 부족한 상황.
**그래프 접근은 행동 이력 부족을 주변 관계 신호로 보완하는 데 유리.**

## 검색

전통적 검색은 문서/상품 설명 텍스트에서 질의어와 일치하는 문자열을 찾는다.
그래프가 결합되면: 질의어가 어떤 엔터티를 의미하는지 파악 → 연관 엔터티와의 관계 탐색 →
사용자 의도와 맥락 보강 → **더 적절한 결과와 설명 제시.**

Knowledge Graph의 역할: 엔터티와 사실 관계 구조화 · 의미 기반 검색 지원 · 지식 패널 생성 ·
질문 응답 정확도 향상 · **동의어와 표기 변형을 넘어 같은 대상을 연결.**

Steve Jobs 지식그래프 시각화(semrush.com 출처 표기 있음)와 Google "apple" 검색 결과 스크린샷.

## 기존 페이지와의 대조

- **[[Knowledge graph]]에 통합** — 이 소단원이 그 concept의 실무 절 대부분을 이룬다.
- **보강** — [[Data catalog and semantic layer]]의 lineage·거버넌스에 "그래프로 모델링하면 도구가
  된다"는 관점이 붙는다.
- **[[Unstructured data ingestion]]과의 대비** — Part 1은 검색을 "임베딩 → Vector DB → ANN →
  reranking"으로만 설명했다. 여기서 **entity 기반 검색이라는 다른 축**이 등장한다.
  둘은 경쟁이 아니라 결합 대상이고, 그 결합이 [[GraphRAG]]다.

## 자료 품질

- **인용 이미지 4장 중 3장이 출처 미표기** (메타데이터 그래프 다이어그램, 컬럼 lineage UI 스크린샷,
  추천 그래프 다이어그램). Steve Jobs 그래프만 semrush 출처 있음.
- lineage UI 스크린샷은 어느 제품인지 밝히지 않아 **재확인이 불가능**하다.
- 출처 없는 수치 없음.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Knowledge graph]] · [[Graph data model]] · [[Data catalog and semantic layer]] ·
  [[Graph database]] · [[GraphRAG]]
- 도구: [[DataHub]]
- 앞: [[AI DE Course - Part3 Ch2 Property graph vs RDF]]
- 다음: [[AI DE Course - Part3 Ch2 Graph and AI]]

---
type: source
title: AI DE Course - Part3 Ch1 Semantics
area: [data-engineering]
aliases: [Part3 Ch1-4, "Semantic이란?", 시멘틱이란]
tags: [data-engineering, course, fast-campus, semantics, metadata, context]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part3/01. Ch1. 스키마 중심 모델과 시멘틱.pdf (p49–59)"]
---

# AI DE Course - Part3 Ch1 Semantics

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch1의 소단원 **4** "Semantic이란?".
원본(로컬): `raw/data-engineering/ai-de-course/part3/01. Ch1. 스키마 중심 모델과 시멘틱.pdf` **p49–59** (11p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

## 이 소단원의 자리

**Part 3 전체의 개념적 중심.** Ch1의 앞 세 소단원이 "스키마 중심 설계가 어디서 무너지나"를 쌓았다면,
여기가 그 답이다. 이후 Ch2(그래프) · Ch3(온톨로지) · Ch4(GraphRAG)는 전부 **이 계층을 어떻게
구현하는가**에 대한 것이다.

구성: `01 Semantic이란? · 02 Semantic을 구성하는 핵심 요소 · 03 Semantic의 중요성 ·
04 Semantic의 실무적용 · 05 Semantic 요약`

## 정의

> **"스키마가 형식을 정의한다면, 시멘틱은 의미를 정의한다."**
> **"시멘틱은 데이터 해석의 계약(contract)이다."**

스키마는 컬럼/타입/제약으로 저장 구조를 보장하지만, **이 값이 어떤 기준으로 계산됐는지 · 어떤 조건을
포함/제외하는지 · 어떤 기간/타임존/시점을 기준으로 하는지**는 알지 못한다.

스키마만으로 설명하기 어려운 것들 — `user_id`와 `member_id`가 같은 개념인가 / `created_at`이 생성
시각인가 가입 시각인가 주문 시각인가 / `status`가 업무 상태인가 결제 상태인가 배송 상태인가 /
두 테이블의 연결이 식별 관계인가 이벤트 관계인가 집계 관계인가.

## 네 요소 — Entity · Attribute · Relationship · Context

앞 세 개는 예상 가능하다. **Context가 별도 요소로 올라온 게 이 슬라이드의 기여다.**

> **"같은 데이터도 맥락이 달라지면 의미가 달라진다. 같은 용어라도 조직과 시스템에 따라 의미가 다를
> 수 있다."**
>
> `active_user` — 최근 7일 로그인? 최근 30일 유효 행동? 유료 사용자만?
> `Revenue` — 총 결제 금액? 취소 제외 순매출? 세전/세후?

Context의 예로 드는 것: 시간 · 채널 · 지역 · **정책 버전 · 실험군 · 모델 버전**.
뒤 세 개가 AI 시스템 특유의 컨텍스트다.

> ⭐ **이건 [[Feature store]]의 Feature 재정의와 정확히 같은 이야기다.**
> Part 2 Ch5가 `total_order_count` ❌ → `total_order_count_last_30_days_as_of_t` ⭕라고 했던 것 —
> **Feature 이름에 window와 기준 시점을 박는 것이 곧 Context를 이름에 명시하는 것이다.**
> 강의는 두 파트를 잇지 않는다. **위키가 붙인 연결.**

## AI가 시멘틱을 더 요구한다

전통적 BI는 정해진 집계와 리포트 중심. AI/LLM 기반 시스템은 더 복잡한 질문을 다룬다 — 이 사용자와
비슷한 성향의 고객은 누구인가 / 이 문서와 관련된 정책·제품·팀은 무엇인가 / 이 장애와 과거 유사한
이슈는 무엇인가 / **이 피처가 어떤 모델·데이터셋·서비스와 연결되는가.**

AI가 자주 요구하는 것: 의미 기반 검색 · 개체 간 연결 탐색 · 이질적 소스 통합 · 문맥 기반 해석 ·
동일 개념 정규화.

## 두 가지 사고

| 스키마 중심 | 시멘틱 중심 |
|---|---|
| 어떤 테이블에 저장할 것인가 | 이 데이터는 어떤 개체를 표현하는가 |
| 어떤 컬럼 타입을 가질 것인가 | 어떤 속성과 관계를 가지는가 |
| 어떤 키로 조인할 것인가 | 다른 시스템의 어떤 개념과 연결되는가 |
| | 어떤 문맥에서 해석해야 하는가 |

**"스키마 중심은 저장 최적화에 강하고, Semantic 중심은 연결·탐색·재사용·해석에 강하다.
AI 시대 데이터 엔지니어는 두 관점을 함께 다뤄야 한다."**

## ⭐ 실무 스펙트럼 — Part 3의 목차이기도 하다

| 강도 | 형태 |
|---|---|
| 가장 약한 형태 | 공통 용어 정의 · 지표 사전 · **데이터 카탈로그** · 컬럼 설명 |
| 더 구조화된 형태 | 공통 엔터티 모델 · 표준 식별자 체계 · 도메인 간 관계 정의 |
| 더 발전한 형태 | **온톨로지 · 지식 그래프 · semantic layer · context-aware retrieval** |

> **이 표가 Part 3 나머지 챕터의 목차다.** Ch2~Ch3이 "더 발전한 형태"를, Ch4가 context-aware
> retrieval을 다룬다.
> 그리고 **[[Data catalog and semantic layer]]가 이미 왼쪽~가운데 구간을 담고 있다** — 두 페이지는
> 같은 스펙트럼의 다른 구간이라 서로 링크로 이어야 한다.

## 요약 슬라이드

> **"RDBMS는 구조를 잘 다룬다. NoSQL은 유연성과 확장을 잘 다룬다.
> 하지만 둘 다 데이터의 의미를 자동으로 설명하지는 못한다.
> Semantic은 개념·관계·문맥을 해석 가능하게 만드는 계층이다.
> AI 시대의 데이터 엔지니어는 파이프라인만 만드는 역할에 머물기 어렵다 —
> 데이터가 어떤 의미를 가지는지, 시스템 간 개념을 어떻게 연결할지, 문맥을 어떻게 보존할지."**

## 기존 페이지와의 대조

- **새 concept:** [[Data semantics]]
- **보강** — [[Data catalog and semantic layer]]. Part 1은 semantic layer를 "정의용 층"으로 한 줄
  다뤘는데, 여기서 **왜 필요한지의 논증**(같은 KPI 3개, SQL이 비즈니스 로직이 됨)과 **네 구성
  요소**가 붙는다.
- **연결** — [[Feature store]](Context = window + 기준 시점) · [[Context engineering]](Part 2).
- **미해결 질문에 진전** — MOC의 *"semantic layer는 실제로 쓰이는가"* 는 여전히 채택률·실패 사례가
  없다. 다만 강의가 **이번엔 "semantic"이라는 용어를 정면으로 쓴다** — Part 1에서 용어를 피하고
  카탈로그+LLM으로 흡수하던 것과 태도가 다르다. **같은 코스 안에서 온도가 바뀌었다.**

## 자료 품질

- **11페이지로 짧지만 밀도가 높다.** Part 3에서 낭비가 가장 적은 소단원.
- 중복 슬라이드 없음. 출처 없는 수치 없음.
- 다만 **구체적 도구가 하나도 안 나온다** — dbt semantic layer, Cube, Looker LookML, AtScale 등이
  언급되지 않는다. "실무 적용" 절이 스펙트럼 나열로 끝난다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Data semantics]] · [[Data catalog and semantic layer]] · [[Ontology]] ·
  [[Knowledge graph]] · [[Feature store]] · [[Context engineering]]
- 앞: [[AI DE Course - Part3 Ch1 RDBMS limits and NoSQL]]
- 다음: [[AI DE Course - Part3 Ch2 Graph fundamentals]]

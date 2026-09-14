---
type: source
title: AI DE 강의 2-10 Feature Store 기본 개념
aliases: [AI DE 2-10]
tags: [AI-DE-강의, MLOps, 피처 스토어]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/data-engineering/ai-de-course/part2/05. Ch5. Feature Store 및 운영.pdf"
---

# AI DE 강의 2-10 Feature Store 기본 개념

[[AI 데이터 엔지니어링 강의]] Part 2의 마지막 덱(Ch5). 파일 제목은 "Feature Store 및 운영"이지만 안에는 소단원 1
"Feature Store의 기본 개념과 필요성" 하나만 있다. 피처를 **계산 규칙 + 시점 + 스키마**로 다시 정의하고, 피처 스토어가
무엇을 해결하는지와 **언제 필요 없는지**를 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 2 「AI 학습/추론 중심 데이터 파이프라인 설계」 |
| 덱 제목 | Ch5. Feature Store 및 운영 — 1. Feature Store의 기본 개념과 필요성 |
| 원본 파일 | `part2/05. Ch5. Feature Store 및 운영.pdf` p1–15 (15p, 덱 전체) |
| 강사 | Habi (슬라이드 표기) |
| 작성 시기 | PDF 생성일 2026-03-24 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch5`, 소단원 번호 `1`은 표지 슬라이드 |

## 요약

### 01. 필요성 — 성능이 나빠지는 이유는 데이터

- 모델보다 **데이터가 더 자주 어긋난다.** 모델 성능 저하의 주요 원인은 모델 코드가 아니라 Feature다.
- 학습과 서빙 환경이 달라지면서 문제가 생기고, Feature 정의가 사람·팀·파이프라인마다 달라진다.
- "Feature Store는 **성능 향상 도구가 아니라 ML 시스템의 안정성을 위한 인프라**."

### 02. Feature란? — 재정의

- Feature는 단순한 컬럼이 아니고, 원천 데이터도 아니다. **특정 시점 기준으로 계산된 의미 있는 값**이며 비즈니스 로직과
  시간 개념을 포함한다.
- 예: `total_order_count` → `total_order_count_last_30_days_as_of_t`
- **"Feature는 계산 규칙 + 시점 + 스키마의 묶음."**

### 03. Feature 관리가 어려워지는 이유

Feature가 늘어날수록:

- 같은 Feature를 팀마다 다시 구현한다.
- 학습용 SQL과 서빙용 코드가 분리된다.
- Feature 변경 이력을 추적할 수 없다 → **어떤 모델이 어떤 Feature를 쓰는지 모른다.**

결과: Training–Serving Skew, 재현 불가능한 실험, 장애 원인 파악에 오랜 시간이 걸리거나 불가능.

### 04. 기존 방식의 한계 — Feature Store 없는 구조

| | Offline (학습) | Online (서빙) |
|---|---|---|
| 생성 | Raw Data → Spark / SQL로 Feature 생성 | API 서버에서 직접 재계산(real-time processing) |
| 저장·조회 | Feature 파일을 CSV / Parquet로 저장 | Redis / DB에서 ad-hoc 조회 |

### 05. 등장 배경 — 무엇을 해결하려 했나

1. Feature 정의의 단일화
2. 학습/서빙 Feature 일관성 보장
3. Feature 재사용성 증가
4. Feature 운영 자동화

"Feature를 **데이터가 아니라 운영 대상 자산**으로 관리하기 위한 시스템."

### 06. 기본 개념

- **정의** — 모델에 입력되는 가공된 데이터(Feature)를 저장·관리하는 중앙 저장소("모델 개발을 위한 중간 Feature 저장소").
  필요성: 여러 팀이 같은 로직으로 만든 Feature 재사용(중복 개발 방지), 학습(Offline)과 추론(Online)에 동일한 데이터
  공급 보장. 핵심 이점: 모델 배포 속도 단축, 데이터 정합성 유지.

| | Offline Feature Store | Online Feature Store |
|---|---|---|
| 주요 목적 | 학습 데이터 생성, **과거 시점 Feature 재현**, 대규모 배치 처리 | 실시간 추론 시 Feature 제공, 낮은 latency·높은 가용성 |
| 특징 | 데이터 레이크 기반(Parquet·Hive·BigQuery 등), **시간 기준 조회 가능**, 대량 조인·집계 최적화 | Redis·DynamoDB·Cassandra 등, Key 기반 조회, 최신 상태 유지 |
| 제약 | — | **모든 Feature를 Online에 둘 수는 없다** |

- **효과**

| 조직 관점 | 시스템 관점 |
|---|---|
| Feature 중복 개발 감소 | 재현 가능한 학습 |
| 팀 간 협업 개선 | 안정적인 서빙 |
| 장애 원인 추적 가능 | 모델 교체 비용 감소 |

### 07. Feature Store는 만능이 아니다

"Feature Store는 항상 필요한 기본 인프라가 아니다."

| 생각해 볼 조건 | 불필요한 경우 |
|---|---|
| Feature가 실시간·서빙에 반드시 필요한가? | 클라이언트가 Feature 값을 이미 알고 있을 때 |
| 계산 비용이 높아 중복 실행을 피해야 하는가? | 데이터 웨어하우스에 이미 있고 사용 가능할 때 |
| 여러 모델·팀 간에 Feature를 공유해야 하는가? | 시간 의존성이 없는 Feature일 때 |
| | Batch serving만 필요할 때 |
| | 계산 비용이 낮은 Feature일 때 |

## 핵심

- **"계산 규칙 + 시점 + 스키마"는 시점 정합성의 요구 그 자체다.** `as_of_t`를 이름에 넣는 순간, 학습 데이터를 만들 때
  각 행에 "t 시점에 알 수 있었던 값"을 붙여야 한다는 규칙이 생긴다. Feast 공식 문서는 이것을 시점 조인으로 구현한다 —
  "the `entity_df` must include an `event_timestamp` column. This timestamp acts as the **upper bound (inclusive)** for
  which feature values are allowed to be retrieved for each entity row. Feast performs a point-in-time join (also called
  a "last known good value" temporal join)" · "This ensures point-in-time correctness, which is critical to prevent
  data leakage during model training." 조회는 엔티티 시점부터 TTL만큼 **과거로** 거슬러 올라간다
  ("Feast will scan backward in time from the entity dataframe timestamp up to a maximum of the TTL time specified.").
  [https://docs.feast.dev/getting-started/concepts/feature-retrieval ·
  https://docs.feast.dev/getting-started/concepts/point-in-time-joins , 2026-09-14 확인]
  → Part 1이 남긴 [[피처 스토어]]의 빈칸(시점 정합성)이 **반쯤** 채워졌다 — 강의가 시간 차원을 이름 붙였지만(오프라인
  스토어의 "과거 시점 재현·시간 기준 조회") 조인이 어떻게 미래 값을 막는지는 보여 주지 않는다. *(위키의 관찰)*
  → [[데이터 누수]]
- **"만능이 아니다" 슬라이드가 가장 실무적이다.** 특히 "Batch serving만 필요하면 불필요" — 예측을 미리 계산해 두는
  배치 서빙에서는 학습과 추론이 같은 배치 코드로 돌 수 있어 온라인 스토어가 풀려는 문제 자체가 작다. 피처 스토어 도입
  여부가 [[모델 서빙]] 방식 선택에 딸려 있다는 뜻이다. *(위키의 관찰)*
- **"Feature Store 없는 구조" 그림은 스큐의 구조도다** — 오프라인은 Spark/SQL, 온라인은 API 서버 재계산. 같은 피처를 두
  언어·두 팀이 두 번 구현하는 모양이 [[학습-서빙 스큐]]가 경고하는 원인과 일치한다. 강의도 03절에서 결과로 skew를 든다.
- "어떤 모델이 어떤 Feature를 쓰는지 모른다"는 피처 단위의 **계보 부재**다 → [[데이터 거버넌스와 카탈로그]]

## 주의·결함

- ❗ **덱 제목은 "Feature Store 및 운영"인데 "운영"이 없다.** 소단원 1(기본 개념과 필요성)만 있고, 도구(Feast 등) 실습,
  오프라인·온라인 동기화, 피처 모니터링은 나오지 않는다. Part 2는 이 덱으로 끝난다.
- **p9는 Ch1 p22와 문구가 같다** — 정의·필요성·핵심 이점을 그대로 반복한다
  → [[AI DE 강의 2-01 데이터 파이프라인의 진화와 데이터 엔지니어]]
- **p11과 p12가 같은 슬라이드다**(Online Feature Store). p3–5는 출처 설명 없이 같은 webflow CDN 이미지 하나를 재사용한다.
- ✅ **p14–15의 기준은 Lak Lakshmanan, "Do You Really Need a Feature Store?", *Towards Data Science*, 2022-02-02와
  일치한다.** 슬라이드에는 URL만 있다. 원문: "Here are some concrete situations where you don't need a feature store. If
  your feature is 1. Known by the client. 2. In a data warehouse. 3. Not time dependent. 4. Needed by only batch serving.
  5. Computationally inexpensive. Keep it simple." · "tldr: Use a feature store if you need to inject features
  server-side, especially if the method of computing these features will keep improving. Otherwise, it is overkill."
  필자는 당시 Google Cloud 소속이었다("we'd love it if you used Vertex AI Feature Store").
  [https://medium.com/data-science/do-you-really-need-a-feature-store-e59e3cc666d3 , 2026-09-14 확인]
- 슬라이드 머리글이 템플릿 잔재다 — "2. AI 시대를 위한 파이프라인과 데이터엔지니어의 진화방향".

## 관련

- 개념: [[피처 스토어]] · [[학습-서빙 스큐]] · [[데이터 누수]] · [[모델 서빙]] · [[데이터 거버넌스와 카탈로그]] · [[MLOps]]
- 이전 강의: [[AI DE 강의 2-09 서빙의 CPU·GPU 가속]]
- 다음 강의: Part 3 (미인제스트)

---
type: source
title: AI DE Course - Part2 Ch3 ML data pipeline
area: [data-engineering]
aliases: [Part2 Ch3-1, ML 데이터 파이프라인의 특징과 구조]
tags: [data-engineering, course, fast-campus, mlops, labeling, data-validation, lineage]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part2/03. Ch3. ML 데이터·서빙 파이프라인.pdf"]
---

# AI DE Course - Part2 Ch3 ML data pipeline

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 2 Ch3** "ML 데이터/서빙
파이프라인"의 소단원 **1** "ML 데이터 파이프라인의 특징과 구조". 강사 **Habi**. 원본(로컬):
`raw/data-engineering/ai-de-course/part2/03. Ch3. ML 데이터·서빙 파이프라인.pdf` **p1–17**. 강의 홈:
[[AI Data Engineering (Fast Campus course)]].

같은 PDF의 나머지: [[AI DE Course - Part2 Ch3 Serving pipeline]](p18–36) ·
[[AI DE Course - Part2 Ch3 Training-serving skew patterns]](p37–51).

**"ML 파이프라인이 일반 데이터 파이프라인과 무엇이 다른가"에 답하는 소단원.**
→ [[ML data pipeline]]

## 논지 — 소비자가 사람이 아니다

> **"BI는 사람이 해석하는 결과를 만들고, ML은 모델이 직접 소비하는 입력을 만든다."**

여기서 세 가지가 따라 나온다:

- **데이터가 곧 성능이며, 성능이 곧 제품 품질**이다
- 운영 이후의 변화(분포·정책·사용자)가 파이프라인에 영향을 준다
- 따라서 **ML 파이프라인은 "모델을 위한 데이터"가 아니라 "운영되는 시스템"을 만든다**

**"모델은 교체 가능하고, 데이터 시스템은 누적 자산이다."**
모델은 버전이 빠르게 바뀌고 분포는 시간이 지나며 변하지만, 파이프라인은 장기 운영 대상이다.
**"실패 원인의 상당 부분은 데이터/파이프라인에서 발생한다."**

## 범위 — "수집부터 학습 전까지"가 아니다

강의의 정의는 **데이터 시스템 전체**다:

1. 데이터 시스템 설계, 데이터 소스 정의, 수집/적재
2. 정제/표준화, **라벨(정답) 생성 또는 수집**, **데이터 검증(Validation)**
3. **학습용 데이터셋 구성(샘플링/분할)**
4. 메타데이터/리니지 관리

2~4가 일반 파이프라인에는 없는 단계다. 하나씩.

## Task Type이 시스템 디자인을 결정한다

문제 정의 → Task Type → 시스템 디자인 순서. 강의가 인용한 분류 트리:

```
Task type ─┬─ Regression
           └─ Classification ─┬─ Binary
                              ├─ Multiclass ─┬─ Low cardinality
                              │              └─ High cardinality
                              └─ Multilabel
```

> 왜 DE가 이걸 알아야 하나 — **multiclass의 cardinality가 높으면 라벨 저장 구조·클래스 불균형
> 샘플링·평가 데이터 구성이 전부 달라지기 때문**이다. Task Type은 모델러의 선택이지만 그 여파는
> 데이터 시스템으로 온다.

## 데이터 소스 — 멀티소스·멀티레이트

- OLTP(정형), 이벤트 로그(반정형), 문서/텍스트(비정형)
- 배치/스트리밍/하이브리드 형태로 유입
- **소스별 신뢰도와 결측/지연 특성이 다르다**
- **"파이프라인 설계는 소스 특성부터 시작해야 한다"**

강의는 여기에 **Lambda / Kappa 아키텍처** 그림을 붙인다 — Part 1
[[Latency and throughput]]에서 이미 다룬 내용.

## 라벨은 파이프라인의 일부다

**"라벨링은 ML 데이터 파이프라인에서 가장 비싸고 취약한 지점"** — 이 소단원의 가장 뾰족한 주장.

- **라벨은 자연 발생하지 않는다**
- **라벨 정의가 바뀌면 모델 목표가 바뀔 수 있다**
- **라벨 생성 지연이 전체 학습 주기를 늘린다**
- **라벨 품질이 모델 상한선을 결정한다** → 라벨링 파이프라인이 필요하다

> 세 번째 항목이 DE에게 직접적이다 — 라벨이 T+7에 생기면 재학습 주기는 아무리 자동화해도 7일보다
> 짧아질 수 없다. **[[Data drift and training-serving skew]]의 "MTTR < 4시간" 같은 KPI가 라벨 지연
> 앞에서 무의미해질 수 있다는 뜻**인데, 강의는 이 연결을 짓지 않는다.

바운딩 박스 어노테이션 툴 스크린샷(보행자·차량 라벨링)으로 "이건 사람이 하는 일"임을 보여준다.

## 데이터 검증은 선택이 아니라 필수

ML 파이프라인에 **검증 단계가 내장**돼야 한다:

- 스키마/타입/범위/결측 검증
- **분포 요약 통계 모니터링** (평균/분산/분위수 등)
- 이상치/급격한 분포 변화 감지
- **"들어오는 데이터가 정상인지를 자동으로 판단해야 함"**

> Part 1 [[Data SLA and observability]]의 3대 지표(신선도·완전성·정확성)와 같은 자리인데,
> **여기서는 "재학습 트리거의 입력"이라는 목적이 붙는다.** 분포 요약 통계를 저장해두는 것이
> 곧 drift 감지의 기준선이 된다.

## 데이터 분할 — 전략 자체가 성능을 왜곡한다

Train / Validation / Test (강의 그림 기준 약 70 / 15 / 15%).

- **시간 기반 분할이 필요한 경우가 많다**
- **사용자/그룹 단위 누수(leakage)를 피해야 한다**
- **테스트는 미래의 입력 분포를 가정해야 한다**
- **분할 전략 자체가 성능을 과대평가/과소평가할 수 있다** — 층화 추출(Stratified Sampling)

> **"랜덤 분할"이 기본값이 아니라는 것**이 요지다. 시계열 데이터를 랜덤으로 자르면 미래를 보고
> 과거를 맞히는 셈이 되고, 같은 사용자의 행동이 train과 test에 걸치면 누수다.

## 메타데이터와 리니지

"왜 이 데이터가 어떻게 생성됐는지 추적이 필요" — 데이터의 출처, 변환 단계(누가/언제/무엇을),
사용된 데이터셋(어떤 버전), **장애/품질 이슈의 원인 추적을 가능하게 한다**.

컬럼 레벨 리니지 그래프 예시를 인용한다 (PostgreSQL `raw_product_data` → Snowflake `stg_product`
→ dbt `product` → `fact_sales` → Tableau 대시보드).

> Part 1 [[Data catalog and semantic layer]]의 lineage와 같은 물건인데, **여기서는 "어떤 모델이
> 어떤 데이터 버전으로 학습됐나"라는 재현성 질문에 답하는 용도**로 쓰인다 →
> [[Data and model versioning]].

## 데이터 엔지니어의 책임 — 이 소단원의 결론

**"데이터 엔지니어는 ML 데이터 생산 체계를 설계한다"**

- 멀티소스 수집 구조 설계
- **라벨 생성/수집 파이프라인 설계**
- **데이터 검증(quality gates) 내장**
- 데이터 버저닝/리니지 기반 운영 가능성 확보

## 기존 페이지와의 대조

- **신규** — 라벨링 파이프라인, 데이터 분할 전략은 위키에 전혀 없던 주제다 → [[ML data pipeline]].
- **재사용** — 데이터 검증·리니지는 [[Data SLA and observability]]·
  [[Data catalog and semantic layer]]와 같은 도구인데 **목적이 다르다**(사람의 신뢰 vs 재학습 트리거).
- **일치** — Lambda/Kappa, 멀티소스 유입 구도는 Part 1과 같다.

## 언급되지만 설명되지 않는 것

강의 슬라이드에 **Airflow · Kafka · Dagster(다람쥐 로고)** 아이콘이 나란히 붙지만 본문에서 셋을
비교하지 않는다. [[Data Engineering]] MOC의 열린 질문 "오케스트레이터 비교"는 **여전히 미해결**이다 —
Part 2도 이름만 대고 지나간다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[ML data pipeline]] (상세) · [[MLOps]] · [[Data SLA and observability]] ·
  [[Data and model versioning]] · [[Latency and throughput]]
- 앞: [[AI DE Course - Part2 Ch2 LLMOps]]
- 다음: [[AI DE Course - Part2 Ch3 Serving pipeline]]

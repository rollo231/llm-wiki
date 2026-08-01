---
type: concept
title: ML data pipeline
area: [data-engineering]
aliases:
  - ML 데이터 파이프라인
  - Labeling pipeline
  - 라벨링 파이프라인
  - Data validation
  - Train test split
  - 데이터 분할
tags: [data-engineering, mlops, labeling, data-validation, data-split, lineage]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part2 Ch3 ML data pipeline]]"]
---

# ML data pipeline

**모델이 직접 소비하는 입력을 만드는 파이프라인.** BI 파이프라인과의 차이는 한 줄이다:

> **BI는 사람이 해석하는 결과를 만들고, ML은 모델이 직접 소비하는 입력을 만든다.**

소비자가 사람이 아니라는 사실에서 나머지가 따라 나온다 — 사람은 이상한 숫자를 보면 의심하지만
**모델은 의심하지 않는다.** 그래서 검증이 파이프라인 안으로 들어와야 한다.

**"모델은 교체 가능하고, 데이터 시스템은 누적 자산이다."**
모델 버전은 빠르게 바뀌지만 파이프라인은 장기 운영 대상이고,
**실패 원인의 상당 부분이 데이터/파이프라인에서 발생한다.**

## 범위 — 일반 파이프라인에 없는 4단계

수집·정제·적재는 [[ETL and ELT]]와 같다. ML 파이프라인이 **추가로** 갖는 것:

1. **라벨(정답) 생성 또는 수집**
2. **데이터 검증(Validation)**
3. **학습용 데이터셋 구성 (샘플링·분할)**
4. **메타데이터/리니지 관리**

## Task Type이 시스템 디자인을 결정한다

```
Task type ─┬─ Regression
           └─ Classification ─┬─ Binary
                              ├─ Multiclass ─┬─ Low cardinality
                              │              └─ High cardinality
                              └─ Multilabel
```

Task Type은 모델러의 선택이지만 여파는 데이터 시스템으로 온다 — **multiclass의 cardinality가 높으면
라벨 저장 구조·클래스 불균형 샘플링·평가 데이터 구성이 전부 달라진다.**

## 라벨은 파이프라인의 일부다

> **"라벨링은 ML 데이터 파이프라인에서 가장 비싸고 취약한 지점."**

- **라벨은 자연 발생하지 않는다**
- **라벨 정의가 바뀌면 모델 목표가 바뀐다**
- **라벨 생성 지연이 전체 학습 주기를 늘린다**
- **라벨 품질이 모델 상한선을 결정한다**

> ⚠️ **세 번째 항목이 운영 KPI를 무력화할 수 있다.**
> [[Data drift and training-serving skew]]는 재학습 목표로 *MTTR < 4시간*을 든다. 하지만 라벨이
> T+7에 생기는 도메인이라면 **재학습 파이프라인을 아무리 자동화해도 회복 주기는 7일보다 짧아질 수
> 없다.** 사기 탐지처럼 "정답"이 며칠 뒤 chargeback으로 확정되는 경우가 그렇다.
> **강의는 이 연결을 짓지 않는다** — 두 챕터가 서로 다른 파트에 있어서다.

## 데이터 검증은 필수 단계

- 스키마/타입/범위/결측 검증
- **분포 요약 통계 모니터링** (평균/분산/분위수)
- 이상치/급격한 분포 변화 감지
- **"들어오는 데이터가 정상인지를 자동으로 판단해야 한다"**

[[Data SLA and observability]]의 3대 지표와 같은 도구인데 **목적이 다르다** — 거기서는 *사람의
신뢰*를 위한 것이고, 여기서는 **재학습 트리거의 입력**이다. 학습 시점의 분포 요약을 저장해두는 것이
곧 drift 감지의 기준선이 된다.

## 데이터 분할 — 전략 자체가 성능을 왜곡한다

Train / Validation / Test (관례적으로 약 70 / 15 / 15%).

- **시간 기반 분할이 필요한 경우가 많다**
- **사용자/그룹 단위 누수(leakage)를 피해야 한다**
- **테스트는 미래의 입력 분포를 가정해야 한다**
- **분할 전략 자체가 성능을 과대평가/과소평가할 수 있다** — 층화 추출(Stratified Sampling)

> **"랜덤 분할이 기본값이 아니다"**가 요지다. 시계열을 랜덤으로 자르면 미래를 보고 과거를 맞히는
> 셈이고, 같은 사용자의 행동이 train과 test에 걸치면 누수다.
>
> 이 페이지에서 **DE가 가장 직접적으로 개입하는 지점**이기도 하다 — 분할은 SQL/Spark 잡으로
> 구현되고, 누수는 조인 키를 잘못 잡아서 생긴다.

## 메타데이터와 리니지

데이터의 출처 / 변환 단계(누가·언제·무엇을) / 사용된 데이터셋 버전 →
**장애·품질 이슈의 원인 추적을 가능하게 한다.**

[[Data catalog and semantic layer]]의 lineage와 같은 물건이지만, 여기서 답해야 할 질문은
**"이 모델은 어떤 데이터 버전으로 학습됐나"** 라는 재현성 질문이다 →
[[Data and model versioning]].

## 데이터 엔지니어의 책임

- 멀티소스 수집 구조 설계 (OLTP 정형 / 이벤트 로그 반정형 / 문서·텍스트 비정형,
  **소스별 신뢰도와 결측·지연 특성이 다르다**)
- **라벨 생성/수집 파이프라인 설계**
- **데이터 검증(quality gates) 내장**
- 데이터 버저닝/리니지 기반 운영 가능성 확보

## 열린 질문

- **라벨링 파이프라인의 실제 구성** — 툴(Label Studio 등), 어노테이터 관리, 라벨 품질 측정
  (inter-annotator agreement), 능동 학습(active learning)이 전혀 나오지 않는다.
- **검증 도구** — Great Expectations·dbt tests 등 구체적 도구는 여기서도 언급되지 않는다.
  ([[Data Engineering]] MOC의 기존 열린 질문과 같은 공백.)
- **라벨 지연과 재학습 주기의 관계** — 위 경고 참고. 근거 자료가 필요하다.

## 링크

- 상위: [[MLOps]] (라이프사이클 2단계)
- 이어지는 단계: [[Batch and online serving]] · [[Feature store]]
- 정합성 문제: [[Data drift and training-serving skew]]
- 검증·리니지의 원래 자리: [[Data SLA and observability]] · [[Data catalog and semantic layer]]
- 출처: [[AI DE Course - Part2 Ch3 ML data pipeline]]

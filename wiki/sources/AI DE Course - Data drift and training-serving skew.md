---
type: source
title: AI DE Course - Data drift and training-serving skew
area: [data-engineering]
aliases: [AI 모델의 적, Data Drift와 Training-Serving Skew 강의]
tags: [data-engineering, course, fast-campus, data-drift, mlops, feature-store, psi]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/1. AI 모델의 적- Data Drift(데이터 변화)와 Training-Serving Skew 1.pdf", "raw/data-engineering/2. AI 모델의 적- Data Drift(데이터 변화)와 Training-Serving Skew 2.pdf", "raw/data-engineering/3. AI 모델의 적- Data Drift(데이터 변화)와 Training-Serving Skew 3.pdf"]
---

# AI DE Course - Data drift and training-serving skew

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 후반부**
"AI 모델의 적: Data Drift(데이터 변화)와 Training-Serving Skew (1)(2)(3)". 원본(로컬):
`raw/data-engineering/1.~3. AI 모델의 적- Data Drift(데이터 변화)와 Training-Serving Skew 1~3.pdf`
(6p + 8p + 6p = 20p). 강의 홈: [[AI Data Engineering (Fast Campus course)]].

> **챕터 번호 주의:** 이 세 파일은 파일명이 `1.` `2.` `3.` 으로만 되어 있고 CH 번호가 파일명에도
> 본문에도 없다. **CH04 다음이라는 순서는 확실하지만 챕터 번호(CH05?)는 추론이다** —
> 근거는 같은 번호 계열의 `10.` 파일 제목이 "Part 1 정리"라는 것.
> → [[AI Data Engineering (Fast Campus course)]]의 '자료 이름 규칙 주의' 절.

**개념 정리는 [[Data drift and training-serving skew]]와 [[Feature store]]로 옮겼다.**
여기는 이 덱의 구성과 사례를 남긴다.

## 3부 구성 — 문제를 두 겹으로 쌓는다

이 덱의 설계가 좋다. **먼저 우리 코드의 문제를 풀고, 그 다음 세상의 변화를 다룬다.**

- **(1) Training-Serving Skew** — 파이프라인 불일치. 해법: [[Feature store]]
- **(2) Data Drift & Concept Drift** — *"파이프라인이 아무리 완벽해도 입력되는 데이터 자체가
  변한다면?"* → **"이제 코드 에러도 없고 파이프라인은 논리적으로 완벽합니다. 하지만, 세상은 변한다."**
- **(3) 방어** — 데이터 SLA + 통계적 모니터링 + Self-Healing MLOps

## (1) Skew — 33배 뻥튀기 사례

강의의 핵심 예시. "최근 30일 평균 결제액" 피처에서 구매 100만 → 취소 -100만 → 구매 2만:

| | 로직 | 계산 | 결과 |
|---|---|---|---|
| 학습 | 구매 - 취소 = 순매출 | (100만 - 100만 + 2만) / **1건** | **20,000원** → 소액 구매 고객(정상) |
| 서빙 | **취소 미반영** | (100만 + 100만 + 2만) / **3건** | **673,333원** → VIP 고객(오판) |

서빙 개발자가 '취소 예외처리' 로직을 누락한 것만으로 평균이 33배가 됐다.
비즈니스 영향(강의 제시): CTR 예상 5.5% → **1.2%**, CVR **0.3%** (고가 상품 추천 실패).

> **"시스템 에러 로그는 0건입니다."** 그래서 강의는 skew를 **'침묵의 살인자'** 로 부른다.
> 같은 성질의 문제를 다음 챕터가 **'침묵의 실패'** 로 부른다
> → [[AI DE Course - Data SLA and pipeline monitoring]]

### 왜 필연적인가 — 두 환경의 구조적 차이

| | 학습 (연구실) | 서빙 (운영) |
|---|---|---|
| WHO | 데이터 사이언티스트 | 백엔드·플랫폼 엔지니어 |
| DATA | 과거 데이터(Batch), 대용량 이력, 정적 분석 | 실시간 데이터(Streaming), 건별, 이벤트 스트림 |
| TOOLS | Python · Pandas · Spark | Java · Go · C++ |
| LOGIC | 복잡한 집계, 고지연 허용 | 단순화, 초저지연(ms) |

> **핵심 원인: 언어와 환경이 달라 로직을 이중으로 구현(Python vs Java)하면서 발생하는 미세한 처리
> 방식의 차이.**

해법 아키텍처와 도구(Feast·Tecton·Hopsworks·Vertex AI Feature Store)는 [[Feature store]] 참조.
실무 체크리스트 3종: **피처 계약 명문화** / **동일 코드·라이브러리 재사용** /
**오프라인-온라인 통계 모니터링**.

## (2) Drift — 두 개의 사례가 이 챕터를 만든다

**모델에도 유통기한이 있다.** *"모델은 '과거의 데이터'를 학습한 '과거의 거울'일 뿐이다."*
**성능 하락은 버그가 아니라 시간의 함수다.**

| | Data Drift (Covariate Shift) | Concept Drift |
|---|---|---|
| 변하는 것 | 입력 분포 `P(X)` | **정답의 기준** `P(Y\|X)` |
| 사례 | **코로나19 마스크 대란** — 2019년엔 대량 구매가 희귀 패턴이라 '사기/매점매석' 판정. 2020년엔 생존 필수 행동인데도 여전히 사기로 차단 → 정상 거래 오탐지 | **스팸 메일의 진화** — 과거 "당첨! 100% 무료 증정"은 키워드로 쉽게 분류. 지금은 "CJ대한통운 배송 안내입니다"처럼 일상 단어를 쓰면서 악성 링크로 연결 |
| 한 줄 | **"세상은 변했는데 AI는 과거의 기준을 고수한다"** | **"입력은 비슷해 보이지만 결과값의 기준이 완전히 뒤바뀌었다"** |

**발생 유형 3종:** Sudden(락다운) · Gradual(인플레이션·트렌드) · Recurrent(블랙프라이데이·계절).

### 원인 — 외부만이 아니다

| 환경적(외부) | 비즈니스적(내부) |
|---|---|
| 팬데믹·사회적 이슈 | 마케팅 캠페인 (신규 사용자층 급증) |
| 경기 변동·인플레이션 (가격 민감도) | 제품 UI/UX 개편 (구매 버튼 위치 변경 → 클릭 로그 패턴 변화) |
| 규제·정책 변화 | 가격 정책·서비스 변경 (구독료 인상 등) |
| 계절성 | **데이터 파이프라인 변경** (로깅 로직 수정, 단위 cm→m) |

> ⚠️ **마지막 항목이 데이터 엔지니어에게 가장 중요하다** — 우리의 엔지니어링 작업 자체가 drift의
> 원인이 된다. drift가 외부에서만 온다고 생각하면 이걸 놓친다.

## (3) 방어 3종

### 데이터 SLA 4대 축

> *"AI 서비스에서 서버가 24시간 정상 작동해도, 모델이 엉뚱한 예측을 한다면 그 서비스는
> '장애 상태'입니다. 인프라 중심에서 '데이터 상태' 중심으로 운영 지표를 전환해야 합니다."*

**신선도**(파이프라인 지연, 피처/라벨 도착 시간) · **분포 안정성**(학습 vs 서빙 분포 차이) ·
**품질/완전성**(결측치·이상치·스키마) · **피처 일관성**(학습/서빙 전처리 로직 및 값 동일성).

→ 뒤의 두 축이 이 페이지의 문제다. 앞의 두 축은
[[AI DE Course - Data SLA and pipeline monitoring]]이 3대 지표로 자세히 다룬다.

### 통계적 감지 지표

**PSI (Population Stability Index)** · **KL Divergence** · **KS Test** · **Chi-square**.
기준 분포(학습)와 실시간 분포(서빙)를 비교한다.

### Self-Healing MLOps

**트리거 3종** — drift 임계치 초과(`PSI > 0.2`) / 성능 저하(Accuracy·F1 하락) / 스케줄·이벤트.

**5단계 파이프라인** — 데이터 수집(최신 피처·라벨, 품질·스키마 검증, 데이터셋 버전 관리) →
모델 학습(전처리 실행, HP 튜닝, **재현 가능한 환경**) → 모델 평가(Champion vs Challenger,
오프라인 지표, **공정성·바이어스 체크**) → 배포(카나리/블루-그린, 섀도우 모드, **자동 롤백 가드레일**)
→ 관측성(실시간 추론 모니터링, 피드백 루프, 로그·트레이스).

**안전장치 2종** — **쿨다운 기간**(무분별한 재학습 방지) · **Human-in-the-loop**(고위험 모델 배포 시
전문가 승인 의무화).

## 역할 이동 — 이 코스의 프레이밍

> **BONUS INSIGHT: 데이터 엔지니어의 역할이 단순 '배관공'에서 '데이터 품질 및 거버넌스 지휘자'로
> 진화한다.** 미래상은 **The Guardian** — 데이터의 '수질(quality)'과 '신선도(freshness)'를 보증하는
> 거버넌스 설계자.

핵심 책임 3축: 신선도·품질 관리(SLO 정의, **Data Contract 수립**, 실시간 품질 검증) /
[[Feature store]] 거버넌스(재사용성·표준화, **lineage 추적**, ground truth 피드백) /
재학습 오케스트레이션(drift 기반 트리거 설계, 모델 버전·메타데이터 관리, **FinOps**).

문화는 **Data as a Product** — 데이터를 부산물이 아니라 내부 고객(데이터 사이언티스트·모델)이 쓰는
'제품'처럼 관리하며 신뢰도를 최우선으로. 태그: `#Documentation #Discoverability #Trust`.

**KPI 예시:** MTTD(drift 감지 시간) **< 10분** · MTTR(복구·재학습) **< 4시간** ·
데이터 다운타임 **99.9% uptime**.

## 검증 필요

- **`PSI > 0.2`** — 임계값을 제시하지만 출처나 도출 근거는 없다.
- **CTR 5.5% → 1.2%** 같은 수치 — 예시로 제시되며 실제 사례 출처는 없다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Data drift and training-serving skew]] (상세), [[Feature store]],
  [[Data SLA and observability]], [[Data and model versioning]], [[AI data engineering]]
- 앞 챕터: [[AI DE Course - Ch4-5,6 Stream processing engines]]
- 이어지는 챕터: [[AI DE Course - Data SLA and pipeline monitoring]]

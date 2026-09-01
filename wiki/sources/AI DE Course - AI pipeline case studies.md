---
type: source
title: AI DE Course - AI pipeline case studies
area: [data-engineering]
aliases: [AI 데이터 파이프라인 구축 사례, Case Study 강의, Part 1 정리]
tags: [data-engineering, course, fast-campus, case-study, mlops, feature-store, data-mesh]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part1/25. [Case Study] 성공적인 AI 데이터 파이프라인 구축 사례 분석 및 Part 1 정리.pdf"]
---

# AI DE Course - AI pipeline case studies

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 마지막**
"[Case Study] 성공적인 AI 데이터 파이프라인 구축 사례 분석 및 Part 1 정리". 원본(로컬):
`raw/data-engineering/ai-de-course/part1/25. [Case Study] 성공적인 AI 데이터 파이프라인 구축 사례 분석 및 Part 1 정리.pdf`
(8p). 강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⚠️ **제목과 내용 불일치:** 파일 제목에 "및 Part 1 정리"가 붙어 있지만 **덱 안에 Part 1 정리 절은
> 없다.** 8페이지 전부가 케이스 스터디이고 마지막 장이 "AI 데이터 품질 관리의 5대 기둥"으로 끝난다.
> 굳이 정리에 해당하는 것을 찾자면 그 마지막 장이다.
> (이 파일 제목이 `1.`~`10.` 파일들을 Part 1에 배치한 근거이기도 하다.)

## 산업화 배경

- **AI 팩토리** — 우수한 모델 개발을 넘어 지속 운영·확장할 인프라가 중요해졌다. 글로벌 선도 기업은
  수조 개 이벤트를 실시간 처리하고 수백만 사용자에게 즉각 예측을 제공하는 **산업화된 아키텍처**를
  지향한다.
- **E2E 자동화** — 수집·정제·피처 생성·학습·배포·모니터링 전 과정을 자동화·표준화해
  **데이터 과학자가 비즈니스 로직에만 집중**하도록 복잡성을 추상화한다.
- **병목: 데이터 준비 70%+** — 현대 대규모 AI 시스템은 데이터 준비에 전체 작업 시간의 **70% 이상**을
  소모한다. 이를 해결하기 위해 **[[Feature store]]** 를 도입해 피처 추출 로직을 재사용한다.
- **리스크: Training-Serving Skew** — 파이프라인이 견고하지 못하면 모델은 학습 시와 다른 데이터를
  서빙 시에 받는다 → [[Data drift and training-serving skew]]

## 6개 사례

### Uber — Michelangelo (중앙 집중식 ML 플랫폼)

- **Palette (피처 저장소)** — 피처 생성·분산 파이프라인 자동 생성.
  **오프라인/온라인 환경에서 동일한 데이터 추출 로직 보장** → [[Feature store]]의 정의 그대로다
- **스키마 검증** — 타입 불일치·**분포 이동**·카디널리티 변화를 실시간 감지해 모델 오염 방지
- **섀도우 배포** — 신규 모델을 실제 운영 트래픽으로 사전 검증.
  엔드포인트 섀도우(팀별 트래픽 분할 비율) + 디플로이먼트 섀도우(**자동 드리프트 감지**)
- **경량화된 스코어링** — 온라인 서빙 지연 최소화
- 성과(강의 제시): 모델 개발 시간 **70%** 단축 · 앱 설치율 **+2%** · 배포 시간 수주로 단축 ·
  성능 회귀 감지를 며칠 → 몇 시간으로

### Netflix — Keystone + 데이터 메시

- **선언적 화해 프로토콜(declarative reconciliation)** — 인프라의 **희망 상태**를 AWS RDS에 저장하고,
  시스템이 실제 상태를 지속 감시하며 불일치 시 자동 복구. (Kubernetes의 reconcile 루프와 같은 발상)
- **자가 치유** — 노드 실패·네트워크 불안정에서도 데이터 유실 최소화
- **Kafka + Flink** — 메시지 버스로 [[Apache Kafka]], 스트림 처리 엔진으로 Flink.
  → [[Stream processing semantics]]의 조합 그대로
- **중앙 집중식 ETL → 데이터 메시** — 병목·변경 취약에서 **도메인 소유권·자율성**으로
- 데이터 메시 구성 4종: **CDC 소스 커넥터**(변경 이벤트 실시간 발행) · GraphQL 보강(Studio Edge) ·
  **스키마 진화 관리(호환성 위반 시 자동 중단)** · **Iceberg 싱크**(분석용 테이블 저장)
- 규모: 일일 **1.3PB** 처리 · **5,000억+** 이벤트 · 주당 약 **2PB** 생성(텍스트~고해상도 영상)

> **이 사례가 Part 1의 여러 챕터를 한 그림으로 잇는다** — [[Change data capture]] + [[Apache Kafka]] +
> Flink + [[Table formats|Iceberg]] + 스키마 레지스트리. "호환성 위반 시 자동 중단"은
> [[Data SLA and observability]]의 **서킷 브레이커**와 같은 발상이다.

### Tesla — Data Engine (비전 중심 자율주행)

- **섀도우 모드 수집** — 신규 알고리즘이 백그라운드에서 실행되며 **실제 운전자의 조작과 자신의 예측을
  비교**. 차량 내 SSD 캐시로 실시간 카메라 피드 처리, 엣지 케이스 선별
- **4단계 데이터 플라이휠** — `수집(섀도우 모드) → 처리(Flink/Kafka) → 학습(Dojo/GPU) →
  배포(OTA 업데이트)` 가 닫힌 고리를 돈다
- **오토 레이블링** — 수백만 클립 자동 처리, 4D 공간 이해 모델
- 규모: 수백만 대 차량 데이터 · 주간 **2PB**

> **엣지 케이스만 골라 올리는 것이 이 사례의 핵심이다** — 전량 수집이 불가능한 규모에서
> "무엇을 수집하지 않을지"가 설계다.

### Meta — FBLearner Flow (대규모 실험 자동화)

- **`@workflow` 데코레이터** — 파이썬 코드로 쓰면 복잡한 병렬화 로직을 시스템에 맡긴다
- **DAG 컴파일** — 데이터 의존성을 분석해 그래프 생성, **퓨처(Future) 객체 반환**
- **연산자 실행** — 의존성 없는 연산자들이 자동 병렬 실행
- 규모: 월간 수백만 AI 실험 · 개발 시간 70% 단축 · 가용성 99.9%

> DAG·의존성·병렬 실행은 [[Batch and stream processing]]의 오케스트레이션 그대로다. 다만
> Airflow처럼 별도 시스템이 아니라 **ML 프레임워크에 내장된** 형태.

**부수 내용(강의 슬라이드 기준):** "50개 이상의 전문 AI 에이전트가 4,100개 파일을 분석해 59개
컨텍스트 파일 생성 → 신입 엔지니어/AI 코딩 에이전트의 실수 획기적 감소". 사례의 나머지와 맥락이
다소 붕 떠 있다.

### Google — TFX (TensorFlow Extended)

- **StatisticsGen / SchemaGen** — 데이터의 통계적 특성을 자동 분석하고 **스키마를 추론**
- **ExampleValidator** — **학습 데이터와 서빙 로그 간의 skew를 감지**
- **Beam 기반** — Cloud Dataflow 같은 서버리스 환경에서 대규모 확장
- 성과: 배포 시간 수개월 → 수주 · 앱 설치율 +2%

> **skew를 "예방"(Feature Store) 하는 대신 "감지"하는 접근이다** — 두 전략의 대비가 선명하다.

### Airbnb — Bighead

- **Zipline** — 온라인·오프라인 피처 추출 로직의 완벽한 일치(consistency)
- **Deepthought** — 실시간 추론 환경, 다양한 모델 포맷 지원
- **ML Automator** — 학습 자동화·실험 결과 관리
- 성과: 개발 시간 70% 단축 · 배포 주기 수일

## 마지막 장 — AI 데이터 품질 관리의 5대 기둥

| | 묻는 것 | 지표 예시 | 장치 |
|---|---|---|---|
| **정확성** (Accuracy) | 실제 세계의 사실과 일치하는가? | KS 통계값 0.05, 정확도 99.5% | 실시간 검증 |
| **완전성** (Completeness) | 핵심 정보가 누락되지 않았는가? | 누락률 0.1%, 완전성 99.9% | 자동 누락 감지 |
| **일관성** (Consistency) | 소스·시간대별로 형식이 통일되어 있는가? | 일관성 98.5%, 스키마 매칭 100% | 자동 스키마 검증 |
| **신선도** (Freshness) | 실시간 의사결정을 지원할 만큼 최신인가? | 지연 <1s, 신선도 99.8% | 실시간 업데이트 |
| **공정성** (Fairness) | 특정 집단에 대한 편향이 없는가? | 편향도 0.02, 공정성 99.5% | **자동 편향 감지** |

> **[[Data SLA and observability]]의 3대 지표(신선도·완전성·정확성)에 일관성과 공정성이 더해진
> 확장판이다.** 특히 **공정성(fairness)이 데이터 품질 지표로 들어온 것**이 이 목록의 특징이다 —
> Part 1의 다른 챕터에서는 "공정성/바이어스 체크"가 재학습 파이프라인의 한 단계로만 나왔다.

## 사례들이 공통으로 말하는 것

Part 1의 개념들이 실제로 어떻게 조합되는지를 보여준다.

1. **여섯 곳 모두 피처 일관성을 별도 시스템으로 해결했다** — Palette · Zipline · ExampleValidator.
   [[Feature store]]가 이론이 아니라 필요에서 나왔다는 근거.
2. **Kafka + Flink + 테이블 포맷이 반복 등장한다** (Netflix·Tesla) — Part 1 CH04의 구성 그대로.
3. **배포 안전장치가 공통이다** — 섀도우 배포(Uber·Tesla), 자동 롤백, 호환성 위반 시 자동 중단(Netflix).
4. **70% / 2% 같은 수치가 여러 사례에서 반복된다** — Uber·Meta·Airbnb 모두 "개발 시간 70% 단축",
   Uber·Google 모두 "앱 설치율 +2%". **동일 수치가 서로 다른 회사 사례에 붙어 있고 출처 표기가
   없어서 인용에 주의가 필요하다.**

## 검증 필요

- 모든 성과 수치(70% · 2% · 1.3PB · 5,000억 등)에 **출처 표기가 없다.**
- 위 4번처럼 **같은 수치가 여러 회사에 중복 사용된다.** 원문 문헌(Uber/Netflix/Meta 엔지니어링
  블로그, TFX 논문)을 확인해야 인용 가능하다. → 향후 1차 자료 인제스트 후보.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Feature store]], [[Data drift and training-serving skew]],
  [[Data SLA and observability]], [[Apache Kafka]], [[Stream processing semantics]],
  [[Change data capture]], [[Table formats]]
- 앞 챕터: [[AI DE Course - Data governance and catalog]]

---
type: concept
title: Data SLA and observability
area: [data-engineering]
aliases:
  - Data SLA
  - Data observability
  - Silent failure
  - Circuit breaker
  - Data contract
  - 데이터 SLA
  - 데이터 관측성
  - 침묵의 실패
  - 서킷 브레이커
tags: [data-engineering, sla, observability, data-quality, monitoring, governance]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Data SLA and pipeline monitoring]]", "[[AI DE Course - Data drift and training-serving skew]]"]
---

# Data SLA and observability

**서버 가동률(uptime)은 데이터가 건강하다는 것을 증명하지 못한다.** 이 페이지는 그 간극과, 그것을
메우는 지표·감시·차단 장치다. [[Data Engineering]] MOC가 열린 질문으로 남겨둔
"데이터 품질·관측성의 실제 도입"에 처음 들어온 근거다.

## 침묵의 실패 (Silent Failure)

기존 IT SLA는 **99.9% uptime**을 약속한다. 그런데 데이터 파이프라인에서는 이런 상태가 가능하다:

| 시스템의 주장 | 실제 데이터 |
|---|---|
| Exit Code: 0 (정상 종료) | Row Count: **0건** (예상 100만건) |
| 에러 로그 없음 | 결제 금액: Null / 음수 |
| 스케줄러 상태: Green | 데이터 가치: 쓰레기 |

**시스템 로그에 에러 한 줄 남기지 않는 가장 무서운 적이고, 기존 IT 모니터링으로는 절대 잡을 수 없다.**
[[Data drift and training-serving skew]]의 skew도 정확히 같은 성질이다 — 에러 0건인데 모델만 망가진다.

### 나비효과 — 왜 이게 재앙이 되나

```
VIP 구매 데이터 수집 실패 → 잘못된 데이터로 재학습 → 엉뚱한 상품 노출
  → 실망한 VIP 이탈 → 매출·ROI 폭락
```

각 단계가 조용하다. 강의의 결론: **AI 성능은 알고리즘의 우수성보다 입력 데이터의 신뢰성에 전적으로
의존하고, 데이터 SLA가 이 재앙을 막는 최전선의 방어벽이다.**

## 데이터 SLA — 신뢰의 계약

시스템이 켜져 있음의 보장이 아니라, **데이터 생산자(엔지니어)와 소비자(AI 모델·분석가) 간에
시간·완전성·정확성을 보장하는 상호 합의된 계약**이다.

강의가 드는 명세 예시:

| 항목 | 약속 |
|---|---|
| **Timeliness** | 매일 아침 08:00까지 적재 완료 |
| **Completeness** | 누락 없음 (source 대비 100%) |
| **Accuracy** | 결제금액 Null / 음수 0건 |

**위반 시: 즉시 알람 & 롤백.** 운영 프로세스는 `실시간 모니터링 → 위반 감지·알림 →
모델 학습 중단/에스컬레이션`.

## 3대 지표 — 품질의 삼각편대

### 신선도 (Freshness & Latency) — "제시간에 도착했는가?"

```
Latency = Now() - Event_Timestamp
```

- **평균값보다 p95·p99 같은 꼬리(tail) 지연을 중점 관리한다** → [[Latency and throughput]]
- 처리 방식별로 기준이 다르다: 배치는 "매일 08:00까지 적재, 08:10 도착 시 위반",
  스트리밍은 "p95 latency 3초 이내".
- 임계값에 **호출 조건**을 박는다 (예: 08:30 초과 시 엔지니어 호출).

### 완전성 (Completeness) — "100% 다 들어왔는가?"

```
assert Source.count() == Target.count()
```

- **Volume Check** — 소스와 타겟의 row count 대사(reconciliation).
- **Uniqueness Check** — PK 중복 검사로 중복 적재 방지.
- **조용한 증발(Silent Loss)** — 네트워크 오류나 메모리 부족으로 100만 건이 90만 건이 되는데 로그가
  없다.
- 위험은 양이 아니라 **편향**이다: 특정 시간대나 사용자군(예: 20대) 데이터가 통째로 누락되면
  AI는 편향된 지식을 진실로 학습한다.
- 금융·결제는 **Zero Tolerance** (단 1건 오차도 불가). 탐지 시 **backfill 자동 트리거**,
  MTTR 30분 이내.

### 정확성·유효성 (Accuracy & Validity) — "값이 상식적인가?"

검증 규칙 4종: 스키마 체크(컬럼 수) · 타입 체크 · 도메인 룰(`email contains '@'`) ·
범위 체크(`0 < age < 120`). 목표 pass rate 99.9% 이상.

대표 오류: 비상식적 값(나이 -5살, 200살) → 잘못된 분포 학습 / 필수 값 Null → 처리 중단.

오류 발견 시 대응은 **격리(quarantine)** 다: `실패 레코드 격리(main DB 오염 방지) → 담당자 알림 →
자동 정정 또는 재처리`.

### AI 관점의 확장 — 4대 축과 5대 기둥

같은 코스가 두 곳에서 축을 다르게 센다. 모순이 아니라 **관점 차이**다.

- **데이터 SLA 4대 축** (drift 챕터, AI 운영 관점): 신선도 · **분포 안정성** ·
  품질/완전성 · **피처 일관성**. 뒤의 둘이 [[Data drift and training-serving skew]]의 문제다.
- **품질 5대 기둥** (케이스 스터디 챕터): 정확성 · 완전성 · 일관성 · 신선도 · **공정성(fairness)**.
  편향 탐지가 품질 지표로 들어온 것이 특징.

## 데이터 관측성 (Data Observability)

수동 확인의 한계를 넘는 자동 감시. 수백~수천 개 파이프라인과 TB급 데이터를 사람이 매일 아침
확인하는 것은 불가능하다.

| 수동 확인 | 데이터 관측성 |
|---|---|
| 물리적 검증 불가 | **자동 수집·분석** — 볼륨·신선도·스키마 변경·값 분포를 24시간 감시 |
| 골든타임 상실 (뒤늦게 인지) | **ML 기반 이상 탐지** — 과거 정상 패턴을 학습해 미세한 징후를 선제 포착 |
| 휴먼 에러 위험 | **선제적 방어** — 문제가 하류로 전파되기 전에 차단 |

## 경고 피로 (Alert Fatigue) 방지

**모든 오류가 응급상황은 아니다.** 무의미한 알람이 쌓이면 엔지니어가 알람을 무시하기 시작한다.

- **비즈니스 임팩트 필터링** — 실제 타격을 주는 핵심 SLA 위반만 알람.
- **동적 임계치(Dynamic Threshold)** — 단순 고정값 대신 시간대별 트래픽·계절성을 반영.
- **채널 차별화** — 경미한 이슈는 대시보드 로그로, 심각한 장애만 on-call 전화로.

## RCA 프로세스

`감지 → 격리 → 완화 → 원인 규명 → 복구` 순서로 매뉴얼에 따라 대응한다.

- **투명한 커뮤니케이션** — 소비 팀에게 "현재 인지 중이며 복구 예정"을 즉시 알리는 것이 신뢰 유지의
  첫걸음.
- **CAPA** — 단순 수정을 넘어 구조적 취약점을 찾아 재발 방지 대책을 수립한다.
- 원인 역추적의 재료가 **lineage**다 → [[Data catalog and semantic layer]]

## 서킷 브레이커 — 방어적 엔지니어링

**철학: "멈춤이 최선의 품질."** 오염된 데이터가 AI 모델을 망치게 두느니 차라리 파이프라인을 멈추고
안전 모드(fail-safe)로 전환한다 — 예: 어제의 데이터를 대신 사용.

- **설치 위치** — 데이터가 변형·이동하는 주요 단계(stage) 사이마다.
- **동작** — 사전 정의된 규칙 위반 시 스위치를 내려 하류 전파를 막는다.
  예: `Null 비율 1% → 50% 급증`.

> **망가진 데이터를 넣어서 모델을 망칠 바에는, 차라리 멈추는 것이 낫다.**

## 한 줄

> **SLA는 종이 위의 약속이 아니다. 시스템으로 지켜질 때 비로소 진짜 약속이 된다.**

## 링크

- 같은 성질의 문제: [[Data drift and training-serving skew]] — 에러 0건인데 망가지는 두 번째 사례
- 꼬리 지연: [[Latency and throughput]] — p95·p99를 왜 보나
- 원인 역추적: [[Data catalog and semantic layer]] — lineage
- 이 계약을 지켜야 할 대상: [[Feature store]], [[Unstructured data ingestion]]
- 출처: [[AI DE Course - Data SLA and pipeline monitoring]],
  [[AI DE Course - Data drift and training-serving skew]]

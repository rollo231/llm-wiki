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
  - SLI
  - SLO
  - Error Budget
  - 알람 피로
  - Alert fatigue
  - Golden Signals
tags: [data-engineering, sla, slo, sli, error-budget, observability, data-quality, monitoring, governance, alerting]
created: 2026-08-01
updated: 2026-08-19
sources: ["[[AI DE Course - Data SLA and pipeline monitoring]]", "[[AI DE Course - Data drift and training-serving skew]]", "[[AI DE Course - Part4 Ch5 AI system metrics and SLA]]", "[[AI DE Course - Part4 Ch5 Monitoring dashboards and alerts]]", "[[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]"]
---

# Data SLA and observability

**서버 가동률(uptime)은 데이터가 건강하다는 것을 증명하지 못한다.** 이 페이지는 그 간극과, 그것을
메우는 지표·감시·차단 장치다. [[Data Engineering]] MOC가 열린 질문으로 남겨둔
"데이터 품질·관측성의 실제 도입"에 처음 들어온 근거다.

> **Part 1이 "데이터 SLA"였다면 Part 4 Ch5는 이를 AI 시스템 전체로 넓힌다** — SLI/SLO/SLA 4단계
> 정의, **비용 SLO**, 대시보드 5종, 알람 4조건 패턴. 아래 **§ AI 시스템 운영** 절이 그 확장이다.

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

⭐ **구현 자리는 [[Data orchestration]]의 DAG다** — 품질 검사를 태스크로 넣고, 그 태스크 실패가
하류 태스크를 막게 한다. 즉 **오케스트레이터의 성공 조건에 데이터 조건을 넣는 것**이 서킷 브레이커다.
⚠️ 반대로 그렇게 하지 않으면 [[Apache Airflow]]는 0건 적재를 성공으로 보고 초록불을 켠다 — 위
§침묵의 실패가 가장 잘 일어나는 자리.

---

# AI 시스템 운영 — Part 4 Ch5의 확장

## ⭐ SLI / SLO / SLA / Error Budget

| 구분 | 핵심 질문 | 정의 | 추천 API 예시 |
|---|---|---|---|
| **SLI** (Indicator) | **"무엇을 측정하는가?"** | 서비스 상태를 나타내는 **실제 측정값** | P99 응답 속도 · HTTP 500 비율 · **피처 최신화 지연** |
| **SLO** (Objective) | **"어느 정도가 정상인가?"** | SLI 기반의 **내부 목표치** | P99 200ms 이하 · 정상 응답률 99.9% · **피처 최신화 5분 이내** |
| **SLA** (Agreement) | **"목표 실패 시 어떻게 책임지는가?"** | 고객과 맺는 **비즈니스 계약.** 미달 시 위약금/보상 | **"가동률 99.9% 미달 시 이용료의 10% 환불"** |
| **Error Budget** | — | SLO 기준 **허용되는 실패 여유분** | 99.9% SLO → 30일 동안 0.1% 실패 허용 |

**SLA가 SLO와 다른 이유는 법적 구속력과 보상이다.** 위 § 데이터 SLA 절의 "신뢰의 계약"이 조직 내부
합의였다면, SLA는 외부 계약이다.

### AI 시스템 SLA/SLO의 5개 층위

| 층위 | 내용 |
|---|---|
| **서비스 SLA** | 요청 성공률, 응답 지연, 가용성 |
| **데이터 SLA** | freshness, completeness, **schema 안정성** ← 위 3대 지표가 여기 |
| **모델 품질 SLO** | 정확도, drift, score distribution, **segment별 성능** |
| **인프라 SLO** | GPU availability, **GPU memory headroom**, queue length, node readiness |
| ⭐ **비용 SLO** | **cost per inference, idle GPU cost, batch job 비용 한도** |

> ⭐ **"비용 SLO"가 새 층위다.** 성능 목표와 나란히 비용 목표를 SLO로 관리한다 —
> [[GPU resource allocation]]의 "80GB A100을 4GB만 쓰는 좀비 노드"가 비용 SLO 위반이다.

## AI 시스템의 실패는 정확도 저하가 아니다

> **대표 실패 6가지 — 모두 "에러 로그 0건"이다:**
> 모델은 정확하지만 **응답이 너무 느림** · 모델은 정상인데 **feature 값이 오래됨** ·
> **GPU는 켜져 있지만 사용률이 낮고 비용만 발생** · 배치 추론은 성공했지만 **결과 테이블이 약속
> 시간 이후 생성** · API는 살아있지만 **특정 모델 버전에서 에러율 급증** ·
> 품질은 좋아 보이지만 **특정 사용자군에서 성능 저하**

**위 § 침묵의 실패의 AI 버전이다.** 그리고 **비용 낭비가 실패 유형에 들어간 것**이 새롭다.

### 좋은 지표 / 나쁜 지표

| 좋은 지표 | 나쁜 지표 |
|---|---|
| 사용자 경험과 연결됨 | 높으면 좋을 것 같은데 **무엇을 해야 할지 모르는** 지표 |
| **운영자가 행동할 수 있음** | **평균만 보고 tail latency를 놓치는** 지표 |
| 측정 방법이 명확함 | **GPU 사용률만 보고 사용자 지연을 설명하지 못하는** 지표 |
| 시간 범위가 정의됨 | **정확도만 보고 데이터 freshness 문제를 숨기는** 지표 |
| ⭐ **소유자가 있음** | ⭐ **`200 OK`** |

> ⭐ **`200 OK`가 나쁜 지표라는 한 단어가 이 페이지 전체의 압축이다.**
> "소유자가 있음"도 중요하다 — 오너 없는 지표는 알람이 울려도 아무도 대응하지 않는다.

## 관측 데이터 4종 — Events가 추가된다

| 종류 | 역할 | 운영 흐름에서의 질문 |
|---|---|---|
| **Metrics** | 상태를 수치로 | **문제가 발생했는지** |
| **Logs** | 개별 사건의 상세 | **어떤 요청에서** 문제가 생겼는지 |
| **Traces** | 요청 흐름의 단계별 시간 | **어느 단계에서** 시간이 걸렸는지 |
| ⭐ **Events** | 시스템 변화 기록 (배포, 모델 교체, autoscaling, node 생성) | ⭐ **문제 직전에 무엇이 바뀌었는지** |

> **표준 3축에 "무엇이 바뀌었나"를 더한 게 좋다.** 실무 장애의 상당수가 변경 직후에 발생하므로
> **변경 이력을 같은 타임라인에 놓는 것**이 원인 특정을 크게 앞당긴다.
> [[Data and model versioning]]의 "무엇이 달라졌는지 특정할 수 있어야 디버깅이 된다"가 관측
> 계층에서 반복된다.

### ⭐ label 설계 — 평균은 문제를 숨긴다

필요 label: `service`, `endpoint`, `model_name`, **`model_version`**, **`feature_version`**,
**`dataset_version`**, `pipeline_name`, `batch_id`, **`user_segment`**, `gpu_type`, `gpu_node`.

**왜 필요한가 — 모두 "전체는 정상, 부분은 장애" 형태다:**

- 전체 평균 latency는 정상, **하지만 `model_version=v3`만 느림**
- 전체 오류율은 정상, **하지만 신규 사용자 segment에서 오류 증가**
- 전체 GPU 사용률은 정상, **하지만 L4 node pool에서만 pending pod 증가**
- 전체 batch job은 성공, **하지만 특정 `pipeline_name`의 freshness 지연**

> ⭐ **tail은 시간축의 꼬리이고, label은 엔티티축의 꼬리다.** 위 § 3대 지표가 p95/p99를 보라고
> 했다면, 여기는 **차원별로 쪼개서 보라**고 한다.

## 대시보드 5종 — 장애 대응 절차의 UI

**설계 순서:** ① 사용자 영향 확인 → ② 영향 범위 확인 → ③ 원인 후보 좁히기 → ④ 첫 대응 결정 →
⑤ 사후 분석 근거 확보.

| # | 대시보드 | 답해야 할 질문 |
|---|---|---|
| **1** | **Overview** | 지금 장애인가? SLO가 깨지고 있는가? **어느 drill-down으로 들어가야 하는가?** ⭐ **원인 분석용 세부 그래프는 최소화** |
| **2** | **Online Inference** | ⭐ **지연이 feature lookup / queueing / inference 중 어디서 발생하는가?** 트래픽 때문인가, 모델 배포 때문인가? |
| **3** | **Data Pipeline** | 데이터가 최신인가? row count·null ratio·schema가 평소와 다른가? ⭐ **"성공 여부만 보지 말 것 — 성공했더라도 데이터 양과 품질이 정상인지"** |
| **4** | **Model Quality** | 점수 분포가 변했는가? ⭐ **label이 늦게 도착하면 품질 지표도 늦게 갱신되므로 `prediction_time`과 `label_event_time`을 분리해서 봐야 한다** |
| **5** | **GPU / Capacity** | 부족해서 밀리는가, 남는데 안 쓰는가? (해석표는 아래) |

**2번의 latency 3구간 분해가 [[Inference optimization]]의 Total Latency 분해와 같다.**
**4번의 두 시각 분리는 [[Stream processing semantics]]의 event time 문제가 모델 모니터링에서
반복되는 형태다.**

### ⭐ GPU 3축 해석표

| GPU 사용률 | Queue | Latency | 해석 |
|---|---|---|---|
| 높음 | 낮음 | 정상 | **잘 활용 중** |
| 높음 | 높음 | 높음 | **capacity 병목** |
| **낮음** | **높음** | **높음** | ⭐ **GPU 앞단 병목** (feature lookup, CPU 전처리, network) |
| 낮음 | 낮음 | 정상 | **과잉 프로비저닝** |
| 높음 | 낮음 | 높음 | **memory, batch size, model 병목** |

> ⭐ **3행이 [[Inference optimization]]의 "GPU는 마지막 수단"의 진단 도구다** — GPU 사용률이 낮은데
> 느리면 GPU를 늘려도 소용없다. → [[GPU resource allocation]]

## ⭐ 알람 설계

> ⭐ **"대시보드: 분석 가능한 맥락 제공. 알람: 행동 가능한 조건만 선택."**
> **"알람은 증상에서 시작하고, 원인은 대시보드로 좁힌다."**

| **증상 지표** — 사용자·downstream이 겪는 문제 | **원인 지표** — 증상을 만들 수 있는 내부 상태 |
|---|---|
| p99 latency 증가 · error rate 증가 | GPU memory 부족 · pod restart 증가 |
| **batch deadline miss** | **Spark shuffle spill** |
| **feature freshness SLO 위반** | **feature pipeline lag** |
| **prediction table 미생성** | **Triton queue time 증가** |
| model quality 하락 | provisioning 실패 · schema validation failure |

**운영 원칙 4단계:** ① **증상 지표로 incident 시작** → ② **원인 지표로 drill-down** →
③ logs·traces로 세부 확인 → ④ **events로 최근 변경 확인.**
**관측 4축과 정확히 대응한다.**

### 좋은 알람의 7요소

| 답해야 할 질문 | 알람 필드 예시 |
|---|---|
| 어떤 SLO가 위험한가 | `[SEV2] recommender-api p99 latency SLO risk` |
| 어떤 서비스·모델 버전인가 | `service=recommender-api`, `model_version=v42` |
| 얼마나 오래 지속됐는가 | `p99_latency=1.8s`, `threshold=1.0s`, **`duration=12m`** |
| 사용자 영향은 | `request_rate=normal` |
| ⭐ **첫 번째로 볼 대시보드는** | `dashboard=Online Inference Dashboard` |
| ⭐ **누가 대응해야 하는가** | `owner=mlops-platform` |
| ⭐ **첫 대응은 무엇인가** | `first_action=check queueing delay and recent model rollout` |

**나쁜 알람:** `GPU high` · `CPU high` · `Latency high` · `Pipeline failed` —
**모두 "명사 + high/failed" 형태로 상태만 알리고 행동을 지시하지 않는다.**

### 심각도 — AI 특화 예시

| 등급 | 범위 | 예시 |
|---|---|---|
| **P1** | 핵심 서비스 전체, SLA 위반. **즉시 호출** | 서비스 DB·API 장애 |
| **P2** | 일부 모델·세그먼트·지역 | **새 추천 모델 V3의 CTR이 기존 대비 20% 하락** |
| **P3** | 장기 추세 악화, 비용 증가. **업무 시간 내** | **Feature Store의 Null 비율이 0.1% → 2%** |

### ⭐⭐ 알람 4조건 패턴 — 경고 피로의 처방

위 § 경고 피로가 원칙이었다면, 이것이 구체적 구현이다.

**원인 6가지:** 일시적 spike에도 알람 · **원인 지표를 모두 page로 연결** ·
같은 장애가 여러 알람으로 중복 · **담당자 없는 알람** · **대응 방법 없는 알람** ·
**SLO와 무관한 threshold**

```
나쁜 예:  GPU utilization > 90%

좋은 예:  p99 latency SLO 위험
          AND request queue length 증가
          AND 10분 이상 지속
          AND request rate가 최소 기준 이상
```

| 조건 | 막는 것 |
|---|---|
| **SLO 기반 증상 지표** | 원인 지표(GPU%)로 알람하는 것 |
| **AND 다른 지표 동반** | 단일 지표 오탐 |
| **AND 지속 시간** | 일시적 spike |
| ⭐ **AND 최소 트래픽** | **트래픽이 거의 없을 때의 통계적 노이즈** (새벽에 3건 중 1건이 느리면 p99는 폭발하지만 장애가 아니다) |

**추가 개선:** 서비스·모델 버전 단위 grouping · **배포 시간대와 maintenance window 반영** ·
**page / ticket / info 구분** · **알람마다 runbook 연결** · ⭐ **장애 이후 알람 품질 리뷰**
(포스트모템에서 코드만 고치고 알람은 그대로 두는 것이 흔하다).

## 워크로드별 SLO 예시 — 숫자가 있다

| 워크로드 | SLO 예시 |
|---|---|
| **온라인 추론** | 정상 응답률 99.9% · **p95 300ms 이하** · p99 1s 이하 · feature lookup 실패율 0.1% 이하 · **LLM 첫 토큰 지연 p95 1s 이하** |
| **Batch inference** | ⭐ **매일 07:00 KST 이전 prediction table 생성** · 99.5% 이상 scoring 완료 · 실패 partition 0.5% 이하 |
| **Feature Store** | online lookup p99 50ms 이하 · **freshness 5분 이하** · ⭐ **offline-online mismatch 0.1% 이하** |
| **학습·모니터링** | 학습 데이터셋 매일 09:00 이전 · ⭐ **데이터 검증 실패 시 학습 job 시작 금지** · serving log 10분 이내 반영 · ⭐ **prediction-label join은 label 도착 후 1시간 이내** |

> ⭐ **"매일 07:00 KST 이전" 같은 deadline형 SLO**가 중요하다. 가용성 %로는 표현할 수 없고,
> 배치 파이프라인의 진짜 SLO는 대부분 이 형태다.
>
> ⭐⭐ **`offline-online skew`를 SLI로 세운 것**이 최대의 수확이다 —
> [[Feature store]]가 열어놓기만 했던 "두 스토어 간 일치"가 **측정 대상으로 승격**된다.
> ⚠️ 다만 **어떻게 재는가는 여전히 없다** (샘플링 주기·기준 시점 정렬·허용 오차).
>
> **"데이터 검증 실패 시 학습 job 시작 금지"** 는 위 § 서킷 브레이커가 학습 파이프라인에 적용된
> 형태다.

## ⚠️ 여전히 빈 곳

- **도구가 하나도 안 나온다** — Prometheus·Grafana·OpenTelemetry·Datadog,
  Great Expectations·dbt tests·Monte Carlo·Bigeye가 **이 코스 전체에서 한 번도 언급되지 않는다.**
- **Error Budget policy가 없다** — 정의만 하고 "소진되면 기능 배포를 멈춘다" 같은 운용 규칙이 없다.
- **SLO burn rate 알람이 없다** — multi-window multi-burn-rate 대신 "10분 이상 지속" 같은
  duration 조건에 머문다. **Error Budget을 정의했으면서 burn rate로 잇지 않는다.**
- **제시된 숫자의 근거가 없다** — "p95 300ms", "freshness 5분", "mismatch 0.1%"를 어떻게
  도출하는지(사용자 영향 기반 역산, 과거 분포의 분위수)가 없어 다른 도메인에 옮기기 어렵다.
- **offline-online skew 측정 방법** (위 참조).

## 한 줄

> **SLA는 종이 위의 약속이 아니다. 시스템으로 지켜질 때 비로소 진짜 약속이 된다.**

## 링크

- 같은 성질의 문제: [[Data drift and training-serving skew]] — 에러 0건인데 망가지는 두 번째 사례
- 꼬리 지연: [[Latency and throughput]] — p95·p99를 왜 보나
- 원인 역추적: [[Data catalog and semantic layer]] — lineage
- 이 계약을 지켜야 할 대상: [[Feature store]] · [[Unstructured data ingestion]] · [[ML data pipeline]]
- 인프라 계층의 SLO: [[Replication and consensus]] — RTO/RPO
- GPU 진단: [[GPU resource allocation]] · [[Inference optimization]]
- 변경 이력: [[Data and model versioning]]
- 출처: [[AI DE Course - Data SLA and pipeline monitoring]] ·
  [[AI DE Course - Data drift and training-serving skew]] ·
  [[AI DE Course - Part4 Ch5 AI system metrics and SLA]] ·
  [[AI DE Course - Part4 Ch5 Monitoring dashboards and alerts]] ·
  [[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]

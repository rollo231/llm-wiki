---
type: source
title: AI DE Course - Part4 Ch5 Monitoring dashboards and alerts
area: [data-engineering]
aliases: [Part4 Ch5-2, 실시간 모니터링 대시보드 및 알람 구성, 알람 피로]
tags: [data-engineering, course, fast-campus, observability, monitoring, alerting, dashboard, golden-signals]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/Part 4_Ch 5.pdf (p22–47)"]
---

# AI DE Course - Part4 Ch5 Monitoring dashboards and alerts

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 4** Ch5의 소단원 **2**
"실시간 모니터링 대시보드 및 알람 구성". 원본(로컬):
`raw/data-engineering/Part 4_Ch 5.pdf` **p22–47** (75p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐ **"모니터링의 목적은 지표 수집이 아니라 운영 판단 구조."** 관측(Observe) → 판단(Orient) →
> 대응(Act)이라는 OODA식 프레이밍으로 시작해서, **대시보드 5종**과 **좋은 알람의 7요소**까지
> 내려간다. **[[Data SLA and observability]]의 "경고 피로"가 여기서 원인과 처방까지 갖춘다.**

## 구성

`01 모니터링의 목적 재정의 · 02 AI 시스템 관측 데이터 설계 · 03 대시보드 설계 · 04 알람 설계`

## 모니터링의 목적 재정의

| 단계 | 내용 |
|---|---|
| **관측 (Observe)** | 시스템의 현재 상태를 **골든 시그널**(Latency, Traffic, Error, Saturation)을 통해 즉시 파악 |
| **판단 (Orient)** | 수집된 데이터가 **SLA 범위를 벗어났는지, 단순 스파이크인지 구조적 결함인지** 분석 |
| **대응 (Act)** | 자동화된 복구(Scale-out, Rollback) 혹은 운영자 개입 |

**대시보드 설계 순서 5단계:**

1. 사용자 영향 확인
2. 영향 범위 확인
3. 원인 후보 좁히기
4. 첫 대응 결정
5. **사후 분석을 위한 근거 확보**

> ⭐ **이 순서가 대시보드 5종의 배치 순서와 정확히 대응한다** — Overview(1,2) → Online Inference(3) →
> Data Pipeline·Model Quality·GPU(3) → 알람(4). **대시보드를 "지표 모음"이 아니라 "장애 대응 절차의
> UI"로 설계**하라는 것이 이 소단원의 논지다.

### ⭐ AI 시스템의 특수성

| 일반 웹 서비스에서 주로 보는 지표 | AI 서비스에서 주로 보는 지표 |
|---|---|
| 요청 수 | **모델 버전** |
| 응답 지연 | **피처 버전** |
| 에러율 | **데이터 신선도** |
| 서버 자원 | **입력 분포 변화** |
| 배포 상태 | **예측 점수 분포** |
| | **정답 label 도착 지연** |
| | **GPU 사용률과 GPU 대기열** |
| | **batch inference 완료 시각** |
| | **재학습 후보 데이터 생성 상태** |

> **왼쪽 5개는 그대로 필요하고, 오른쪽 9개가 추가된다.** AI 시스템 관측은 대체가 아니라 **확장**
> 이라는 게 정확하다.

### 대시보드와 알람의 역할 분담

| 대시보드 | 알람 |
|---|---|
| 현재 상태를 **넓게** 보여줌 | 운영자가 **즉시 행동해야 하는 상황**을 전달 |
| 문제의 영향 범위 파악 | SLO 위반 가능성을 알려줌 |
| 지표 간 관계 분석 | 사용자 영향 발생을 감지 |
| 원인 후보를 좁힘 | 장애 대응 프로세스를 시작 |
| 배포 전후 변화 비교 | |

> ⭐ **"대시보드: 분석 가능한 맥락 제공. 알람: 행동 가능한 조건만 선택."**
>
> 이 한 줄이 알람 설계 전체의 기준이다 — **대시보드에 있어야 할 것을 알람으로 만들면 알람 피로가
> 생긴다.**

## 관측 데이터 4종

| 종류 | 역할 | 예시 | 운영 흐름에서의 질문 |
|---|---|---|---|
| **Metrics** | 상태를 수치로 측정 | latency, error rate, GPU utilization | **문제가 발생했는지** |
| **Logs** | 개별 사건의 상세 기록 | `request_id`, `model_version`, `error_message` | **어떤 요청에서** 문제가 생겼는지 |
| **Traces** | 요청 흐름의 단계별 시간 | `feature lookup → inference → postprocess` | **어느 단계에서** 시간이 걸렸는지 |
| **Events** | 시스템 변화 기록 | 배포, 모델 교체, autoscaling, GPU node 생성 | **문제 직전에 무엇이 바뀌었는지** |

> ⭐ **Events를 4번째 축으로 세우는 게 좋다.** 표준 observability 3축(metrics/logs/traces)에
> **"무엇이 바뀌었나"** 를 추가한다. 실무 장애의 상당수가 배포·설정 변경 직후에 발생하므로
> **변경 이력을 같은 타임라인에 놓는 것**이 원인 특정을 크게 앞당긴다.
>
> **[[Data and model versioning]]의 "무엇이 달라졌는지 특정할 수 있어야 디버깅이 된다"** 가
> 관측 계층에서 반복된다.

### ⭐ label 설계 — 평균은 문제를 숨긴다

> **"AI 시스템 지표에는 반드시 구분 기준이 필요하다."**

필요한 label: `service`, `endpoint`, `model_name`, **`model_version`**, **`feature_version`**,
**`dataset_version`**, `pipeline_name`, `batch_id`, **`user_segment`**, `gpu_type`, `gpu_node`

**왜 필요한가 — 네 가지 실제 상황:**

- 전체 평균 latency는 정상, **하지만 `model_version=v3`만 느림**
- 전체 오류율은 정상, **하지만 신규 사용자 segment에서 오류 증가**
- 전체 GPU 사용률은 정상, **하지만 L4 node pool에서만 pending pod 증가**
- 전체 batch job은 성공, **하지만 특정 `pipeline_name`의 freshness 지연**

> ⭐ **네 예시가 모두 "전체는 정상, 부분은 장애" 형태다.** Ch5-1의 나쁜 지표
> *"평균만 보고 tail latency를 놓치는"* 이 여기서 **차원(dimension) 문제**로 확장된다 —
> tail은 시간축의 꼬리이고, label은 **엔티티축의 꼬리**다.
>
> **이 목록이 Ch5-3 트러블슈팅 사례의 전제이기도 하다** — 사례 1에서 `model_version=v42`만 느린
> 것을 발견할 수 있는 이유가 이 label 설계다.

### AI 시스템 지표의 5개 계층

| 계층 | 질문 | 지표 |
|---|---|---|
| **1. 서비스** | 사용자가 영향을 받는가 | 요청 수, latency, error rate, timeout |
| **2. 데이터** | 모델 입력이 정상인가 | freshness, row count, schema error, missing feature ratio |
| **3. 모델** | 예측 품질이 변하고 있는가 | score distribution, drift, model_version별 품질 |
| **4. 인프라** | 자원이 병목인가 | pod restart, queue length, GPU utilization/memory |
| **5. 비용** | 과도하게 낭비하고 있는가 | GPU idle cost, cost per inference, batch run cost |

**Ch5-1의 SLA 5층위와 정확히 같은 분류다** — 서비스/데이터/모델/인프라/비용. **일관성이 좋다.**

## ⭐ 대시보드 5종

### 1. Overview Dashboard — 1분 안에 장애 여부 판단

**목표 질문:** 지금 장애인가? / 어느 서비스가 영향을 받는가? / SLO가 깨지고 있는가? /
**어느 drill-down 화면으로 들어가야 하는가?**

**화면 구성:** 정상/주의/장애 상태를 즉시 구분 · **원인 분석용 세부 그래프는 최소화** ·
서비스별 drill-down 링크 제공 · **최근 배포·스케일링 이벤트를 같은 화면에 표시**

> ⭐ **"원인 분석용 세부 그래프는 최소화"** 가 핵심 규율이다. Overview에 모든 그래프를 밀어 넣는
> 것이 가장 흔한 실패인데, **Overview의 목적은 "어디로 들어갈지"를 정하는 것**이라고 못 박는다.

### 2. Online Inference Dashboard — 사용자가 느린지 확인

**질문:** 사용자가 느린 응답을 받고 있는가? / 어느 endpoint 또는 model_version에서 느린가? /
⭐ **지연은 feature lookup, queueing, inference 중 어디서 발생하는가?** /
트래픽 증가 때문인가, 모델 배포 때문인가?

**지표:** request rate · success/error rate · **p50/p95/p99 latency** · **queueing delay** ·
**feature lookup latency** · **model inference latency** · post-processing latency ·
timeout count · **model_version별 latency와 error rate** · 최근 배포 이벤트

> ⭐ **latency를 feature lookup / queueing / inference / post-processing 4단계로 분해**하는 게
> 핵심이다. [[Inference optimization]](Part 2)의 **"Total Latency 분해"** 가 대시보드 설계로
> 내려온 형태이고, Ch5-3 사례 1의 원인 A/B/C가 정확히 이 세 구간이다.

### 3. Data Pipeline Dashboard — 모델 입력이 정상인지

**질문:** 데이터가 최신인가? / feature table이 제시간에 갱신됐는가? /
batch inference 결과가 downstream 약속 시간 전에 생성됐는가? / **row count, null ratio, schema가
평소와 다른가?** / label join이 지연되고 있는가?

> ⭐ **"이 화면에서 가장 중요한 비교: 성공 여부만 보지 말 것. 성공했더라도 데이터 양과 품질이
> 정상인지 확인."**
>
> **Part 1의 "침묵의 실패"가 대시보드 요구사항으로 번역된 문장이다.**

### 4. Model Quality Dashboard — 모델이 여전히 잘 작동하는지

**질문:** 모델 점수 분포가 변했는가? / 특정 사용자군에서 성능이 나빠졌는가? /
새 model_version이 이전 버전보다 나쁜가? / prediction과 label의 관계가 깨지고 있는가? /
drift가 발생했는가?

> ⭐ **"모델 품질 지표는 즉시 계산되지 않을 수 있다. label이 늦게 도착하면 품질 지표도 늦게 갱신된다.
> 따라서 `prediction_time`과 `label_event_time`을 분리해서 봐야 한다."**
>
> **이것이 Ch3의 event time vs processing time이 모델 모니터링에서 반복되는 형태다.**
> 강의가 두 챕터를 잇지 않지만 같은 구조의 문제다 — **두 개의 시각을 구분하지 않으면 지표가
> 틀어진다.**
>
> **"모델 품질 대시보드는 배포 직후의 정적 평가가 아니라, 운영 데이터에서 계속 변하는 품질을 보는
> 화면"** — [[Data drift and training-serving skew]]의 운영 측 대응이다.

### 5. GPU / Capacity Dashboard — 병목과 낭비를 동시에

**질문:** GPU가 부족해서 요청이 밀리는가? / **GPU는 많은데 사용되지 않고 있는가?** /
어느 model 또는 pipeline이 GPU를 점유하는가? / GPU memory 부족이 발생하는가? /
**MIG slice가 제대로 활용되는가?** / GPU node provisioning이 실패하고 있는가?

> ⭐⭐ **해석 규칙 4종 — 이 소단원 최고의 산출물:**
>
> | GPU utilization | 동반 지표 | 해석 |
> |---|---|---|
> | **낮음** | queue length 낮음 | **낭비 가능성** |
> | **높음** | queue length 높음 | **capacity 부족 가능성** |
> | **낮음** | latency 높음 | ⭐ **feature lookup, CPU preprocessing, network 병목 가능성** |
> | **높음 (memory)** | OOM | batch size, model size, **KV cache** 문제 가능성 |
>
> **세 번째 행이 Part 2 "GPU는 마지막 수단"의 진단 도구다.** GPU 사용률이 낮은데 느리면
> **GPU를 늘려도 소용없다** — 앞단이 문제다. Ch4-1,2의 PCIe 병목과 Ch4-4의 "입력 파이프라인이
> 병목"이 여기서 관측 규칙이 된다.
>
> **네 번째 행에 KV cache가 등장하는 게 흥미롭다** — 이 코스에서 KV cache라는 단어가 나오는
> 거의 유일한 지점인데, **설명 없이 이름만 나온다.**

## ⭐ 알람 설계

### 증상 알람과 원인 알람

> ⭐ **"알람은 증상에서 시작하고, 원인은 대시보드로 좁힌다."**

| 증상 알람 (사용자 영향·SLO 위반과 직접 연결) | 원인 알람 (장애를 만들 수 있는 내부 상태) |
|---|---|
| p99 latency SLO 초과 | GPU memory 95% 이상 |
| error rate 급증 | GPU pod pending 증가 |
| **batch inference deadline miss** | feature pipeline 실패 |
| **feature freshness SLO 위반** | model server pod restart |
| **prediction table 미생성** | schema validation failure |
| | **Karpenter provisioning 실패** |

### 좋은 알람의 7요소 + 실제 예시

| 알람이 답해야 할 질문 | 예시 알람의 필드 |
|---|---|
| 어떤 SLO가 위험한가 | `[SEV2] recommender-api p99 latency SLO risk` |
| 어떤 서비스 또는 모델 버전인가 | `service=recommender-api`, `model_version=v42` |
| 얼마나 오래 지속됐는가 | `p99_latency=1.8s`, `threshold=1.0s`, **`duration=12m`** |
| 사용자 영향은 무엇인가 | `request_rate=normal` |
| **첫 번째로 볼 대시보드는 무엇인가** | `dashboard=Online Inference Dashboard` |
| **누가 대응해야 하는가** | `owner=mlops-platform` |
| **첫 대응은 무엇인가** | `first_action=check queueing delay and recent model rollout` |

**나쁜 알람:** `GPU high` · `CPU high` · `Latency high` · `Pipeline failed`

> ⭐⭐ **좋은 알람 예시가 이 소단원에서 가장 실용적이다.** 알람에 **dashboard·owner·first_action**을
> 포함시키라는 것 — 알람을 받은 사람이 **다음에 무엇을 할지 알 수 있어야** 한다는 원칙이다.
>
> **나쁜 알람 4개가 모두 "명사 + high/failed" 형태**인 것도 정확한 관찰이다. 상태만 알려주고
> 행동을 지시하지 않는다.

### 심각도와 라우팅 — "얼마나 빨리 사람이 행동해야 하는가"

| 등급 | 범위 | 예시 |
|---|---|---|
| **P1 (SEV1)** | 핵심 서비스 전체 영향, SLA 위반 또는 대규모 사용자 영향. **즉시 호출** | 서비스 DB 장애, 서비스 API 장애 |
| **P2 (SEV2)** | 일부 모델·세그먼트·지역 영향. 빠른 대응 필요 | **새로 배포된 추천 모델 V3의 CTR이 기존 모델 대비 20% 하락** |
| **P3 (SEV3)** | 장기 추세 악화, capacity 부족, 비용 증가. **업무 시간 내 처리** | **Feature Store에 적재되는 최신 유저 로그의 Null 비율이 평소 0.1%에서 2%로 상승** |

> ⭐ **P2·P3 예시가 AI 특화라는 게 중요하다.** 일반적인 심각도 분류는 "장애 범위"로 나누는데,
> 여기는 **모델 품질 저하(CTR 20% 하락)와 데이터 품질 저하(Null 2%)** 를 각각 등급에 배치한다.
> **Ch5-1의 "실패 유형 6가지"가 여기서 대응 우선순위로 번역된다.**

### ⭐ 알람 피로

**원인 6가지:** 일시적 spike에도 알람 · **원인 지표를 모두 page로 연결** ·
같은 장애가 여러 알람으로 중복 발생 · **담당자 없는 알람** · **대응 방법 없는 알람** ·
**SLO와 무관한 threshold**

**개선 방식 7가지:** 지속 시간 조건 추가 · **최소 트래픽 조건 추가** ·
서비스 또는 모델 버전 단위 grouping · **배포 시간대와 maintenance window 반영** ·
**page / ticket / info 구분** · **알람마다 runbook 연결** · **장애 이후 알람 품질 리뷰**

**나쁜 예 → 좋은 예:**

```
나쁜 예:  GPU utilization > 90%

좋은 예:  p99 latency SLO 위험
          AND request queue length 증가
          AND 10분 이상 지속
          AND request rate가 최소 기준 이상
```

> ⭐⭐ **이 before/after가 이 소단원의 결론이다.** 좋은 예의 4개 조건이 각각 다른 실패 모드를 막는다:
>
> | 조건 | 막는 것 |
> |---|---|
> | **SLO 기반 증상 지표** | 원인 지표(GPU%)로 알람하는 것 |
> | **AND queue length 증가** | 단일 지표 오탐 |
> | **AND 10분 이상 지속** | 일시적 spike |
> | **AND request rate 최소 기준 이상** | ⭐ **트래픽이 거의 없을 때의 통계적 노이즈** |
>
> **네 번째 조건이 특히 실무적이다** — 새벽에 요청 3건 중 1건이 느리면 p99는 폭발하지만 장애가
> 아니다. **[[Data SLA and observability]]의 "경고 피로"에 이 4조건 패턴을 반영해야 한다.**
>
> **"장애 이후 알람 품질 리뷰"** 도 좋다 — 포스트모템에서 코드만 고치고 알람은 그대로 두는 것이
> 흔한데, **알람 자체를 리뷰 대상으로** 삼는다.

## 기존 페이지와의 대조

- **[[Data SLA and observability]] 대폭 보강** — Part 1의 "경고 피로"가 **원인 6 + 개선 7 +
  4조건 패턴**으로 구체화된다. Metrics/Logs/Traces/**Events** 4축, label 설계, 대시보드 5종도 새롭다.
- **[[Inference optimization]]** — latency 4단계 분해가 대시보드 요구사항으로.
- **[[Data drift and training-serving skew]]** — Model Quality Dashboard,
  `prediction_time` vs `label_event_time` 분리.
- **[[Data and model versioning]]** — Events 축, `model_version`/`feature_version`/`dataset_version`
  label.
- **[[GPU resource allocation]]** — GPU 해석 규칙 4종.
- **[[Feature store]]** — feature freshness SLO 위반이 증상 알람.

## 자료 품질

**Part 4 Ch5에서 가장 실용적인 소단원.**

- ✅ **GPU 해석 규칙 4종** — 사용률 단독으로는 아무것도 못 판단한다는 걸 표로 정리
- ✅ **좋은 알람 예시가 실제 필드 형태**로 (`owner`, `dashboard`, `first_action`)
- ✅ **알람 4조건 패턴**의 before/after
- ✅ **label 설계**의 "전체는 정상, 부분은 장애" 4예시
- ✅ Metrics/Logs/Traces에 **Events**를 추가한 4축
- ✅ 5개 계층이 Ch5-1의 SLA 5층위와 일관
- ⚠️ **도구가 하나도 안 나온다** — Prometheus·Grafana·OpenTelemetry·Datadog이 한 번도 언급되지 않는다.
  **[[Data Engineering]] MOC에 남긴 "제품 선택의 갈림은 그대로다"(Great Expectations·Monte Carlo
  부재)가 관측 도구에서도 반복된다.** `Karpenter`만 알람 예시에 이름이 나온다.
- ⚠️ **KV cache가 설명 없이 이름만 등장**
- ⚠️ **SLO burn rate 알람이 없다** — SRE 표준인 multi-window multi-burn-rate 방식이 언급되지 않고,
  "10분 이상 지속" 같은 duration 조건에 머문다. Ch5-1에서 Error Budget을 정의했으면서
  **burn rate로 알람하는 방법**으로 잇지 않는다
- ⚠️ 대시보드 스크린샷 슬라이드(p33·p35·p39·p41)가 **이미지 전용**이라 실제 화면 구성이 텍스트에 없음
- ⚠️ 중복 슬라이드: p36/p37 완전 동일

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Data SLA and observability]] · [[Inference optimization]] ·
  [[Data drift and training-serving skew]] · [[Data and model versioning]] ·
  [[GPU resource allocation]] · [[Feature store]] · [[Stream processing semantics]]
- 앞: [[AI DE Course - Part4 Ch5 AI system metrics and SLA]]
- 다음: [[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]
- Part 1의 대응 페이지: [[AI DE Course - Data SLA and pipeline monitoring]]

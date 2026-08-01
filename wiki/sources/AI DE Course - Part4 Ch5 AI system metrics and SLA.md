---
type: source
title: AI DE Course - Part4 Ch5 AI system metrics and SLA
area: [data-engineering]
aliases: [Part4 Ch5-1, AI 시스템의 핵심 지표 설정과 SLA 정의, SLI SLO SLA Error Budget]
tags: [data-engineering, course, fast-campus, sla, slo, sli, error-budget, observability, mlops]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/Part 4_Ch 5.pdf (p1–21)"]
---

# AI DE Course - Part4 Ch5 AI system metrics and SLA

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 4** Ch5 "시스템 운영 및 최적화"의 소단원 **1**
"AI 시스템의 핵심 지표 설정과 SLA 정의". 원본(로컬):
`raw/data-engineering/Part 4_Ch 5.pdf` **p1–21** (75p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐ **Part 1 CH06의 [[AI DE Course - Data SLA and pipeline monitoring]]이 "데이터 SLA"였다면,
> 여기는 AI 시스템 전체로 넓힌 버전이다.** SLI/SLO/SLA/Error Budget 4단계를 정식으로 정의하고,
> **워크로드 4종별 SLI/SLO 예시**를 구체적 숫자까지 제시한다. 이 코스에서 **운영 목표를 숫자로
> 쓰는 법**을 가장 자세히 다루는 소단원이다.

## 구성

`01 AI 시스템 운영 지표 필요성 · 02 SLA / SLO / SLI / Error Budget · 03 AI 시스템의 핵심 지표 분류 ·
04 워크로드별 SLA/SLO 설계`

> ⚠️ 목차 슬라이드(p2)에 **`05 GPU 데이터 파이프라인 설계 판단 기준`** 이 남아 있다.
> **Ch4-5의 목차 복붙 잔재**이고 본문에 없다. (Ch3-2의 "05 합의의 대가"와 같은 종류의 실수 —
> **Part 4에만 이런 잔재가 세 건이다.**)

## ⭐ 시스템의 실패는 정확도 저하가 아니다

> **"모델 정확도 저하로 시스템의 실패가 발생하는가?"** — 대표 실패 유형 6가지:
>
> - **모델은 정확하지만 응답이 너무 느림**
> - **모델은 정상인데 feature 값이 오래됨**
> - **GPU는 켜져 있지만 사용률이 낮고 비용만 발생**
> - **배치 추론은 성공했지만 결과 테이블이 약속 시간 이후 생성됨**
> - 서빙 API는 살아있지만 **특정 모델 버전에서 에러율 급증**
> - 모델 품질은 좋아 보이지만 **특정 사용자군에서 성능 저하**

> ⭐ **Part 1의 "침묵의 실패"([[Data SLA and observability]])가 AI 시스템 버전으로 확장된 목록이다.**
> 여섯 개 모두 **"에러 로그가 0건"** 이라는 공통점이 있다. 그리고 **비용 낭비를 실패 유형에 포함**
> 시키는 게 새롭다 — 성능만이 아니라 **돈도 SLO의 대상**이라는 관점이 뒤에서 "비용 SLO"로 이어진다.

### AI 시스템은 여러 경로가 동시에 움직인다

| 경로 | 흐름 | 목표 |
|---|---|---|
| **온라인 추론** | `request → feature lookup → model inference → response → serving log` | 빠른 응답, 낮은 에러율, **안정적인 tail latency** |
| **배치 추론** | `feature table → batch inference → prediction table → downstream 소비` | **정해진 시간 안에** 결과 테이블 생성 |
| **학습 데이터** | `raw log → feature engineering → label join → training dataset` | 정확한 데이터셋 생성, **재현성**, 완료 시각 준수 |
| **모니터링** | `serving log → prediction-label join → drift / quality metric → retraining trigger` | 모델 버전별 품질 변화와 데이터 분포 변화 감지 |

> ⭐ **네 경로가 각각 다른 SLO를 갖는다는 게 이 소단원의 구조적 통찰이다.** "우리 서비스 SLO는
> 99.9%"라는 단일 숫자로는 배치 추론의 deadline이나 feature freshness를 표현할 수 없다.

### 좋은 운영 지표 / 나쁜 운영 지표

> **"운영 지표는 관찰용 숫자가 아니라 행동 기준."**

목적: 현재 상태 파악 · 사용자 영향 판단 · 장애 조기 감지 · 증설/축소 판단 · **모델 롤백 판단** ·
**재학습 필요성 판단** · **비용 낭비 탐지**

| 좋은 지표 | 나쁜 지표 |
|---|---|
| 사용자 경험과 연결됨 | 높으면 좋은 것 같은데 **무엇을 해야 할지 모르는** 지표 |
| **운영자가 행동할 수 있음** | **평균만 보고 tail latency를 놓치는** 지표 |
| 측정 방법이 명확함 | **GPU 사용률만 보고 사용자 지연을 설명하지 못하는** 지표 |
| **시간 범위가 정의됨** | **정확도만 보고 데이터 freshness 문제를 숨기는** 지표 |
| **소유자가 있음** | **`200 OK`** |
| 알람 기준으로 바꿀 수 있음 | |

> ⭐ **나쁜 지표 목록의 마지막 항목 `200 OK` 가 이 소단원의 압축이다.**
> Part 1의 *"uptime은 데이터 건강을 증명하지 않는다"* 와 정확히 같은 말인데, 한 단어로 줄였다.
>
> **"소유자가 있음"을 좋은 지표의 조건으로 넣은 것도 좋다** — 지표에 오너가 없으면 알람이 울려도
> 아무도 대응하지 않는다. Ch5-2의 "담당자 없는 알람"이 알람 피로의 원인으로 다시 나온다.

## ⭐ SLI / SLO / SLA / Error Budget

| 구분 | 핵심 질문 | 정의 | 비유 (건강 검진) | 추천 API 예시 |
|---|---|---|---|---|
| **SLI** (Service Level **Indicator**) | **"무엇을 측정하는가?"** | 서비스 상태를 나타내는 **실제 측정값** | 체온계의 눈금, 혈압 수치 | P99 응답 속도(ms) · HTTP 500 에러 비율(%) · **피처 최신화 지연 시간** |
| **SLO** (Service Level **Objective**) | **"어느 정도가 정상인가?"** | SLI를 기반으로 설정한 **내부 목표치** | 36.5~37.5도 유지, 혈압 120/80 미만 | P99 200ms 이하 · 한 달간 정상 응답률 99.9% · **피처 최신화 지연 5분 이내** |
| **SLA** (Service Level **Agreement**) | **"목표 실패 시 어떻게 책임지는가?"** | 고객과 맺는 **비즈니스 계약**. 미달 시 위약금/보상 포함 | 건강보험 계약 | **"API 가동률 99.9% 미달 시, 이번 달 서비스 이용료의 10%를 환불"** |
| **Error Budget** | — | SLO를 기준으로 **허용되는 실패 여유분** | — | 99.9% SLO라면 30일 동안 **0.1% 실패 허용** |

> ⭐ **"핵심 질문" 열이 이 표를 유용하게 만든다.** SLI/SLO/SLA는 혼동되기 쉬운데,
> **측정 → 목표 → 계약(+책임)** 이라는 층위가 질문 형태로 명확해진다.
>
> **SLA 예시에 "10% 환불"이라는 구체적 위약금이 들어간 게 좋다** — SLA가 SLO와 다른 이유는
> **법적 구속력과 보상**이다. Part 1의 SLA 논의는 이 구분이 흐릿했다.

### ⭐ AI 시스템 SLA/SLO의 5개 층위

| 층위 | 내용 |
|---|---|
| **서비스 SLA** | 요청 성공률, 응답 지연, 가용성 |
| **데이터 SLA** | 데이터 freshness, completeness, **schema 안정성** |
| **모델 품질 SLO** | 정확도, drift, score distribution, **segment별 성능** |
| **인프라 SLO** | GPU availability, **GPU memory headroom**, queue length, node readiness |
| **비용 SLO** | **cost per inference, idle GPU cost, batch job 비용 한도** |

> ⭐⭐ **"비용 SLO"라는 개념이 이 코스에서 처음 나온다.** 성능 목표와 나란히 **비용 목표를 SLO로
> 관리**한다는 발상인데, GPU 시대에는 타당하다 — Ch4-3의 "80GB A100을 4GB만 쓰는 좀비 노드"가
> 비용 SLO 위반이다. **[[Data SLA and observability]]에 이 층위를 추가해야 한다.**

## 핵심 지표 분류 5종

### 서비스 지표 — 사용자가 직접 체감

| 온라인 AI 서비스 | LLM 서비스 |
|---|---|
| **availability** — 정상 응답 비율 | **time to first token** — 첫 토큰까지의 시간 |
| **latency** — 요청부터 응답까지 | **time per output token** — 토큰 생성 속도 |
| **error rate** — 5xx, timeout, model unavailable, **feature lookup failure** 비율 | **tokens per second** — 전체 생성 처리량 |
| **throughput** — 초당 처리 요청 수 | **prompt length / output length** — 입출력 길이에 따른 latency 변화 |

> ⭐ **LLM 서빙 지표가 이 코스에서 처음 제대로 나온다.** TTFT / TPOT / TPS는 LLM 서빙의 표준
> 지표이고, **[[Data Engineering]] MOC의 "Part 2가 남긴 질문 — LLM 서빙 계보가 통째로 빠졌다"**
> 에 대한 **부분적 답**이다.
>
> ⚠️ **다만 지표 이름만 나오고 그 뒤의 메커니즘은 여전히 없다** — vLLM·continuous batching·
> KV 캐시·PagedAttention이 Part 4에서도 등장하지 않는다. **"무엇을 재는가"는 생겼지만 "무엇이 그
> 값을 결정하는가"는 여전히 공백이다.**

### 데이터 지표 — 모델 입력의 신뢰성

**freshness**(최신 데이터가 얼마나 빨리 반영되는가) · **completeness**(예상한 데이터가 빠짐없이
들어왔는가) · **validity**(값이 정의된 범위와 schema를 만족하는가) ·
**schema stability**(컬럼 이름·타입·의미가 깨지지 않았는가)

> **Part 1의 3대 지표(신선도·완전성·정확성)에 schema stability가 추가됐다.**

### 모델 품질 지표

accuracy / precision / recall / F1 · AUC / NDCG / MAP · conversion rate · click-through rate ·
**prediction-label agreement** · **score distribution** · **calibration** · **segment별 성능** ·
drift metric

### GPU / 인프라 지표

| GPU | 서빙 인프라 |
|---|---|
| GPU utilization · GPU memory utilization / used | pod restart count · replica count |
| GPU temperature · GPU power usage | **request queue length** · **batch queue length** |
| **GPU throttling** · GPU error / ECC error | **model load time** · container OOM |
| GPU allocation count · **MIG slice 사용률** | node readiness · autoscaling event |

> **`model load time`과 `request queue length`가 목록에 있는 게 좋다** — Ch5-3의 트러블슈팅에서
> 실제로 이 둘이 원인 지표로 쓰인다.

### 비용 지표

cost per 1,000 inference · **cost per 1M tokens** · cost per batch inference run ·
**GPU idle cost** · GPU hour per model · training cost per experiment · feature pipeline cost ·
**storage cost per dataset version**

## ⭐ 워크로드별 SLA/SLO 설계 — 숫자가 있다

### 온라인 추론

목표: 사용자가 요청한 순간 빠르고 안정적으로 응답.

| 대표 SLI | SLO 예시 |
|---|---|
| 정상 응답 비율 · p95/p99 latency · timeout 비율 · model unavailable 비율 · **feature lookup 실패율** · **queueing delay** · tokens per second · time to first token | 최근 30일 기준 **정상 응답률 99.9% 이상** · **p95 latency 300ms 이하** · **p99 latency 1s 이하** · **feature lookup 실패율 0.1% 이하** · **LLM 첫 토큰 지연 p95 1s 이하** |

### Batch Inference와 데이터 파이프라인

목표: 정해진 시간 안에 대량 예측 결과를 생성하고 downstream이 사용할 수 있게 함.

| 대표 SLI | SLO 예시 |
|---|---|
| job success rate · **deadline miss count** · prediction table freshness · processed row count · **failed partition count** · retry count · output completeness · cost per run | **매일 07:00 KST 이전 prediction table 생성** · 전체 대상 user의 **99.5% 이상 scoring 완료** · **실패 partition 0.5% 이하** · 재시도 후 job success rate 99% 이상 · **batch inference 비용 월 예산 이하** |

> ⭐ **"매일 07:00 KST 이전"** 같은 **deadline형 SLO**가 나오는 게 중요하다. 가용성 %로는 표현할 수
> 없는 종류의 약속이고, 배치 파이프라인의 진짜 SLO는 대부분 이 형태다.

### Feature Store와 데이터 신선도

목표: 학습과 추론에서 **일관된** feature 제공, 온라인 추론 시 최신 feature를 빠르게 조회.

| 대표 SLI | SLO 예시 |
|---|---|
| online feature lookup latency · feature availability · feature freshness · missing feature ratio · ⭐ **offline-online skew** · schema violation count · feature pipeline success rate | **online feature lookup p99 50ms 이하** · **주요 feature freshness 5분 이하** · missing feature ratio 0.1% 이하 · ⭐ **offline-online feature mismatch 0.1% 이하** · feature pipeline success rate 99% 이상 |

> ⭐⭐ **`offline-online skew`를 SLI로, `mismatch 0.1% 이하`를 SLO로 세운 것이 이 소단원 최대의
> 수확이다.**
>
> **[[Data Engineering]] MOC에 "❌ Feature Store가 skew를 정말 없애나 — Part 2가 답하지 못했다"고
> 남긴 질문에 Part 4가 부분적으로 답한다.** Part 2 Ch5는 "offline/online 두 스토어를 두면 두 스토어
> 간 일치가 새로운 보장 대상이 된다"는 문제를 열어놓기만 했는데, **여기서 그것을 측정 대상(SLI)으로
> 승격시킨다.**
>
> ⚠️ **다만 "어떻게 재는가"는 여전히 없다.** 같은 엔티티에 대해 offline 값과 online 값을 샘플링해
> 비교하는 것으로 보이지만, 샘플링 주기·기준 시점 정렬·비교 허용 오차가 전혀 언급되지 않는다.
> **"재야 한다"까지는 왔고 "이렇게 잰다"는 아직이다.**

### 학습 파이프라인과 모델 모니터링

| 학습 파이프라인 SLI | 모델 모니터링 SLI |
|---|---|
| training dataset generation success rate · dataset completeness · **data validation failure count** · training job success rate · experiment runtime · model registry registration success | **serving log ingestion delay** · ⭐ **prediction-label join delay** · drift metric freshness · model quality metric freshness · alert evaluation delay · segment별 metric completeness |

**SLO 예시:**
- 학습 데이터셋은 **매일 09:00 이전 생성**
- ⭐ **데이터 검증 실패 시 학습 job 시작 금지**
- serving log는 **10분 이내** 모니터링 테이블 반영
- ⭐ **prediction-label join은 label 도착 후 1시간 이내 반영**
- drift metric은 매일 1회 이상 갱신

> ⭐ **"prediction-label join delay"가 SLI로 등장하는 것이 [[ML data pipeline]]의 라벨 지연 문제에
> 대한 답이다.**
>
> **MOC에 "라벨 지연이 재학습 주기의 상한이다 — 강의는 두 사실을 다른 파트에서 각각 말하고 잇지
> 않는다"고 남겼는데, 여기서 처음으로 라벨 도착을 명시적 SLI로 다룬다.** 다만 여전히
> **"label 도착 후 1시간"** 이지 **"label이 언제 도착하는가"** 는 아니다. 라벨 자체의 지연은
> SLO 대상 밖으로 남아 있다.
>
> **"데이터 검증 실패 시 학습 job 시작 금지"** 는 [[Data SLA and observability]]의 **서킷 브레이커**
> 가 학습 파이프라인에 적용된 형태다.

## 기존 페이지와의 대조

- **[[Data SLA and observability]] 대폭 보강** — SLI/SLO/SLA/Error Budget 4단계 정의,
  **5개 층위(특히 비용 SLO)**, 워크로드별 SLO 예시가 모두 새롭다. Part 1의 "데이터 SLA"가
  AI 시스템 전체로 확장된다.
- **[[Feature store]] 보강** — **offline-online skew를 SLI로 측정**한다는 발상.
- **[[ML data pipeline]]** — prediction-label join delay.
- **[[LLMOps]]** — LLM 서빙 지표(TTFT/TPOT/TPS).
- **[[Data drift and training-serving skew]]** — drift metric freshness, segment별 성능.

## 자료 품질

- ✅ **SLI/SLO/SLA/Error Budget 4단계를 "핵심 질문"과 함께 정의** — 이 코스에서 가장 명료한 표 중 하나
- ✅ **워크로드 4종별로 구체적 숫자** (p95 300ms, 07:00 KST, freshness 5분, p99 50ms)
- ✅ **`200 OK`를 나쁜 지표로** 꼽는 압축
- ✅ **비용 SLO**라는 층위 신설
- ✅ **offline-online skew를 SLI로** 승격
- ✅ LLM 서빙 지표 4종이 처음 등장
- ⚠️ 목차의 `05 GPU 데이터 파이프라인 설계 판단 기준` — Ch4-5 복붙 잔재
- ⚠️ **제시된 숫자들의 근거가 없다.** "p95 300ms", "freshness 5분", "mismatch 0.1%"가 **어디서 온
  값인지, 어떻게 도출하는지**가 없다. SRE 문헌의 표준 관행(사용자 영향 기반 역산, 과거 분포의
  분위수)이 언급되지 않아 **다른 도메인에 옮기기 어렵다.**
- ⚠️ **Error Budget을 정의만 하고 쓰지 않는다.** "소진되면 기능 배포를 멈춘다" 같은
  **error budget policy**가 SRE 실무의 핵심인데 한 줄도 없다.
- ⚠️ **offline-online skew의 측정 방법이 없다** (위 참조)

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Data SLA and observability]] · [[Feature store]] · [[ML data pipeline]] ·
  [[Data drift and training-serving skew]] · [[MLOps]] · [[LLMOps]] · [[GPU resource allocation]]
- 앞: [[AI DE Course - Part4 Ch4 GPU in data engineering and RAPIDS]]
- 다음: [[AI DE Course - Part4 Ch5 Monitoring dashboards and alerts]]
- Part 1의 대응 페이지: [[AI DE Course - Data SLA and pipeline monitoring]]

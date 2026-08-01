---
type: source
title: AI DE Course - Part2 Ch4 Serving architecture
area: [data-engineering]
aliases: [Part2 Ch4-1, Batch vs Online 서빙 아키텍처 비교]
tags: [data-engineering, course, fast-campus, mlops, serving, airflow, kubeflow, flyte, slo]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/Part2_Ch 4.pdf"]
---

# AI DE Course - Part2 Ch4 Serving architecture

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 2 Ch4** "서빙 아키텍처 및
플랫폼"의 소단원 **1** "Batch vs Online 서빙 아키텍처 비교". 강사 **Habi**. 원본(로컬):
`raw/data-engineering/Part2_Ch 4.pdf` **p1–16**. 강의 홈:
[[AI Data Engineering (Fast Campus course)]].

같은 PDF의 나머지: [[AI DE Course - Part2 Ch4 Serving platforms]](p17–60) ·
[[AI DE Course - Part2 Ch4 CPU and GPU inference]](p61–77).

Ch3이 세운 Batch/Online 개념을 **아키텍처 구성요소 수준**으로 내린다 → [[Batch and online serving]].

## 논지 — "서빙 방식은 모델 문제가 아니라 시스템 선택"

> 동일한 모델이라도 Batch로 서빙하면 전혀 다른 시스템, Online으로 서빙하면 전혀 다른 시스템.
> **서빙 방식 선택은 인프라·데이터 파이프라인·운영 비용을 동시에 결정한다.**

**모델은 그대로인데 시스템이 통째로 달라진다**는 프레이밍이 이 소단원의 전부다. 서빙 방식은
ML 팀의 취향이 아니라 아키텍처 결정이다.

## Batch 서빙 아키텍처

흐름: **주기적 스케줄 실행(hourly/daily) → 대량 데이터 로드 → Feature 계산 → 모델 추론 →
결과를 테이블/스토리지에 저장** ⇒ 예측 결과는 사전에 계산됨.

세부 구조: `Data Lake/Warehouse → Batch Feature Pipeline (Spark, SQL) → Distributed Inference
(Spark UDF, Ray, Batch job) → 결과 저장 테이블 or Cache`.

주기 표기가 재밌다 — **`1W / 1D / 1H / 10m`** 로 `Data Set → Model → DB/Cache` 를 도는 그림.
**10분 주기 배치까지 내려오면 "배치"와 "스트리밍"의 경계는 실무적으로 흐릿해진다** (Part 1
[[Latency and throughput]]의 마이크로배치 논의와 같은 자리).

### 배치 서빙 도구 3종 — 이 코스의 첫 오케스트레이터 비교

**[[Data Engineering]] MOC가 계속 비어 있다고 적어둔 "오케스트레이터 비교"에 처음으로 실질이 생긴다.**
다만 축이 일반 ETL이 아니라 **ML 배치 추론**이다.

| | **Airflow** | **Kubeflow Pipeline** | **Flyte** |
|---|---|---|---|
| 위치 | SQL/Spark/Python 기반 배치 예측에 최적 | 학습–배포–Batch 추론까지 **ML 라이프사이클 중심**, K8s 기반 | **Airflow와 Kubeflow의 중간 지점** |
| 아키텍처 관점 | **DAG = 예측 파이프라인**, Task 단위로 Feature 생성·모델 로딩·Batch Inference·결과 적재 | **Pipeline = ML 워크플로우**, Component 단위로 Feature 생성·학습·추론, 모델 아티팩트 관리 | **Task/Workflow가 강하게 타입화**, 데이터·모델 아티팩트 관리가 기본 설계에 포함 |
| 장점 | 데이터 엔지니어 친화적 · **기존 ETL 파이프라인과 자연스럽게 통합** · 재시도·백필·스케줄링 강력 | 모델 버전·실험 추적과 자연스럽게 연결 · **GPU/분산 환경 제어 용이** · 학습–서빙 일관성 확보 | **재현성·버전 관리·캐싱이 기본 제공** · 대규모 Batch 추론에 안정적 · ML/데이터 워크플로우 모두 적합 |
| 한계 | **ML 개념(모델 버전, 실험 추적)에 대한 네이티브 지원 부족** · GPU·분산 추론 제어는 별도 설계 필요 | **인프라 복잡도 높음** · 순수 Batch 서빙만 놓고 보면 과한 선택 | **러닝 커브** · 생태계는 Airflow보다 작음 |

> **선택 축이 명확하다: "ML 개념을 얼마나 네이티브로 아는가" vs "인프라 복잡도".**
> Airflow는 ETL에서 넘어오기 쉽지만 모델을 모르고, Kubeflow는 모델을 알지만 무겁고, Flyte가
> 그 사이. Dagster·Prefect는 여기서도 언급되지 않는다.

## Online 서빙 아키텍처

> **"온라인 서빙은 단일 모델 서버가 아니라 여러 역할을 가진 컴포넌트들의 협업 구조"**

| 구성 요소 | 역할 | 예 |
|---|---|---|
| **Client** | 웹/앱/내부 서비스, 예측 요청 생성 | — |
| **Load Balancer** | 요청 분산, 헬스 체크 기반 트래픽 제어 | — |
| **Prediction Service (Replica)** | 요청 수신·Feature 조회·모델 추론·응답 생성 | — |
| **Online Feature Store / Cache** | 실시간 조회 가능한 Feature 제공 | Redis, DynamoDB, Feast Online Store |
| **Model Artifact Storage** | 모델 파일 저장 | S3, GCS, Model Registry |
| **Logging / Metrics Pipeline** | 요청·응답·Feature·예측 결과 수집 | Kafka, Pub/Sub, Prometheus |

**요청 흐름:**

```
Client → Load Balancer → Prediction Service
  → Feature Key 추출 → Online Feature Store 조회
  → Feature 결합 및 전처리 → 모델 추론 (CPU/GPU) → 후처리 및 응답 반환
  (+ 결과 필터링, Fallback Logic, 서킷 브레이커)
```

> **마지막 줄의 서킷 브레이커가 Part 1 [[Data SLA and observability]]에서 온 개념이다.**
> 거기서는 *나쁜 데이터가 하류로 퍼지는 걸 끊는* 장치였는데, 여기서는 *느린 의존성이 응답을 잡아먹는
> 걸 끊는* 장치다. 같은 이름의 다른 용도.

### 운영 시 주의 요소 — "Online 서빙은 운영 시스템"

| | |
|---|---|
| **Latency SLO** | **p95 / p99 기준 설정** |
| **Timeout & Fallback** | Feature 조회 실패 시 기본값 |
| **Partial Failure 대응** | **일부 Feature Store 장애 허용** |
| **Observability** | 요청 단위 로그, **Feature 분포 모니터링**, 예측 결과 드리프트 감지 |

도구: TorchServe·BentoML·Ray·Triton + **Prometheus·Grafana·Datadog**.

> ⚠️ **"Feature 조회 실패 시 기본값"과 "일부 Feature Store 장애 허용"은 앞 소단원이 경고한 skew
> 패턴 3(결측 처리 차이)을 정면으로 만든다.** 가용성을 위해 기본값을 넣는 순간 입력 분포가 학습
> 때와 달라진다. **강의는 두 소단원에서 이 상충을 각각 말하지만 한자리에서 붙이지는 않는다** —
> 실무의 답은 skew 소단원 쪽이다: `is_missing` 플래그로 **"채웠다는 사실 자체를 피처로 넘긴다."**
> → [[AI DE Course - Part2 Ch3 Training-serving skew patterns]]

**p95/p99**는 Part 1 [[Latency and throughput]]이 말한 "평균보다 꼬리"의 서빙판이다.

## 기존 페이지와의 대조

- **신규** — Online 서빙의 6개 컴포넌트 구성, 배치 오케스트레이터 3종 비교 → [[Batch and online serving]].
- **부분 해소** — [[Data Engineering]] MOC의 열린 질문 "오케스트레이터 비교"에 **ML 배치 축의
  비교표**가 생겼다. 다만 **일반 ETL 축의 Airflow vs Dagster vs Prefect는 여전히 공백**이다.
- **연결** — 서킷 브레이커·p99가 [[Data SLA and observability]]·[[Latency and throughput]]에서
  서빙 문맥으로 재사용된다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Batch and online serving]] (상세) · [[Feature store]] · [[Data SLA and observability]] ·
  [[Latency and throughput]] · [[Model serving platforms]]
- 앞: [[AI DE Course - Part2 Ch3 Training-serving skew patterns]]
- 다음: [[AI DE Course - Part2 Ch4 Serving platforms]]

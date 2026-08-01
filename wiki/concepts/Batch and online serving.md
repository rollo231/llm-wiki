---
type: concept
title: Batch and online serving
area: [data-engineering]
aliases:
  - Batch serving
  - Online serving
  - 배치 서빙
  - 온라인 서빙
  - Batch prediction
  - Online prediction
  - 서빙 파이프라인
tags: [data-engineering, mlops, serving, inference, latency, airflow, kubeflow, flyte]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part2 Ch3 Serving pipeline]]", "[[AI DE Course - Part2 Ch4 Serving architecture]]"]
---

# Batch and online serving

**추론 요청을 처리하는 실행 경로를 어떻게 놓을 것인가.** 서빙 파이프라인은 외부 요청을 받아 →
Feature를 조회하거나 계산하고 → 모델 추론을 수행하고 → 결과를 응답한다.

> **"서빙 방식은 모델 문제가 아니라 시스템 선택이다.
> 동일한 모델이라도 Batch로 서빙하면 전혀 다른 시스템, Online으로 서빙하면 전혀 다른 시스템."**
> 이 선택이 **인프라·데이터 파이프라인·운영 비용을 동시에 결정한다.**

⚠️ **[[Batch and stream processing]]과 축이 다르다.** 저쪽은 *데이터를 언제 처리하나*이고
여기는 *예측을 언제 만드나*다. 스트리밍으로 피처를 만들면서 배치로 예측할 수도 있다.

## 두 방식

| 구분 | **Batch 서빙 (비동기)** | **Online 서빙 (동기)** |
|---|---|---|
| 예측 시점 | 주기적 (예: 4시간마다, `1W/1D/1H/10m`) | **요청 즉시** |
| 결과 | **사전에 계산되어 저장됨** | 실시간 생성, 수 ms ~ 수십 ms |
| 모델 호출 | **사용자 요청과 분리됨** | **사용자 요청 경로에 직접 포함됨** |
| 최적화 목표 | **높은 처리량(Throughput)** | **낮은 지연(Low Latency)** |
| 설계 목표 | 비용 효율성, **재현 가능성** | 높은 가용성, 예측 일관성 |
| 사례 | 추천 점수 사전 계산, 고객 세그먼트, 리스크·신용 점수, 마케팅 타겟 리스트 | 실시간 사기 탐지, 광고 입찰, 개인화 추천, 실시간 이상 탐지 |
| 장점 | 대규모 처리 유리 · 인프라 비용 최적화(Spot·예약) · **실패 시 재시도·백필 용이** | 최신 상태 즉시 반영 |
| 제약 | **결과가 최신이 아닐 수 있음** · 사용자 행동 변화에 즉각 대응 불가 | **모델 실패 = 서비스 실패** · **Feature 조회가 latency의 대부분** · 트래픽 스파이크 대응 |

[[Latency and throughput]]의 시소가 서빙에서 그대로 재현된다.

> **`10m` 주기 배치까지 내려오면 "배치"와 "온라인"의 경계는 실무적으로 흐릿해진다** — 마이크로배치가
> 스트리밍과 배치 사이에 있는 것과 같은 구조.

## Batch 서빙 아키텍처

```
Data Lake / Warehouse
  → Batch Feature Pipeline (Spark, SQL)
  → Distributed Inference (Spark UDF, Ray, Batch job)
  → 결과 저장 테이블 or Cache
```

주기적 스케줄 실행 → 대량 로드 → Feature 계산 → 모델 추론 → 저장.

### 오케스트레이터 3종 — ML 배치 축

| | **Airflow** | **Kubeflow Pipeline** | **Flyte** |
|---|---|---|---|
| 단위 | **DAG = 예측 파이프라인**, Task 단위 | **Pipeline = ML 워크플로우**, Component 단위 | **Task/Workflow가 강하게 타입화** |
| 강점 | DE 친화적 · **기존 ETL과 자연스럽게 통합** · 재시도·백필·스케줄링 | 모델 버전·실험 추적 연결 · **GPU/분산 제어 용이** · 학습–서빙 일관성 | **재현성·버전 관리·캐싱이 기본 제공** · 대규모 배치 추론에 안정적 |
| 약점 | **ML 개념(모델 버전·실험 추적) 네이티브 지원 부족** · GPU·분산 추론은 별도 설계 | **인프라 복잡도 높음** · 순수 배치 서빙만 놓고 보면 과함 | **러닝 커브** · 생태계가 Airflow보다 작음 |

> 선택 축은 **"ML 개념을 얼마나 네이티브로 아는가" vs "인프라 복잡도"** 하나다.
> Airflow는 ETL에서 넘어오기 쉽지만 모델을 모르고, Kubeflow는 모델을 알지만 무겁고, Flyte가 사이.

## Online 서빙 아키텍처

> **"온라인 서빙은 단일 모델 서버가 아니라 여러 역할을 가진 컴포넌트들의 협업 구조."**

| 구성 요소 | 역할 | 예 |
|---|---|---|
| Client | 예측 요청 생성 | 웹/앱/내부 서비스 |
| Load Balancer | 요청 분산, 헬스 체크 | — |
| **Prediction Service (Replica)** | 요청 수신·Feature 조회·추론·응답 | → [[Model serving platforms]] |
| **Online Feature Store / Cache** | 실시간 조회 가능한 Feature | Redis, DynamoDB, Feast Online Store |
| Model Artifact Storage | 모델 파일 저장 | S3, GCS, Model Registry |
| Logging / Metrics Pipeline | 요청·응답·Feature·예측 수집 | Kafka, Pub/Sub, Prometheus |

```
Client → Load Balancer → Prediction Service
  → Feature Key 추출 → Online Feature Store 조회
  → Feature 결합·전처리 → 모델 추론 (CPU/GPU) → 후처리·응답
  (+ 결과 필터링, Fallback Logic, 서킷 브레이커)
```

## Feature 조회가 병목이다

**"서빙 성능은 Feature 접근 방식에 크게 의존한다."** 네 가지 접근: 실시간 계산 / 사전 계산 /
캐시 기반 / 외부 스토어 조회.

서빙 경로에서의 조회 비용: 네트워크 호출 · 스토리지 응답 지연 · **캐시 미스** · **일부 Feature 누락**.

**캐싱 전략 — "서빙 경로에서는 계산을 최소화":** 변경 주기가 긴 Feature는 사전 계산 · 요청 단위 계산
최소화 · 동일 요청 반복 시 캐시 · **캐시 실패를 고려한 fallback 필요**.

> ⚠️ **fallback이 조용한 skew의 진입로다.** 조회 실패를 0으로 채우면 학습 때와 다른 입력이 된다.
> 답은 **`is_missing` 플래그** — 채웠다는 사실 자체를 피처로 넘긴다.
> → [[Data drift and training-serving skew]]

[[Feature store]]의 online store가 "초저지연 조회 계층"이자 **동시에 서빙 latency의 최대 항목**
이라는 두 얼굴을 갖는다.

## 운영 — "Online 서빙은 운영 시스템"

| | |
|---|---|
| **Latency SLO** | **p95 / p99 기준 설정** (평균이 아니라 꼬리) |
| **Timeout & Fallback** | Feature 조회 실패 시 기본값 |
| **Partial Failure 대응** | 일부 Feature Store 장애 허용 |
| **Observability** | 요청 단위 로그, Feature 분포 모니터링, 예측 결과 드리프트 감지 |

**Latency Budget은 ML 팀이 혼자 정하지 않는다 — 백엔드팀과 협상 대상이다.**
모델 추론 시간은 전체 예산의 일부일 뿐이다 → [[Inference optimization]].

부하 측정 도구로 Locust, 관측에 Prometheus·Grafana·Datadog.

## 모델 버전 관리

**"서빙 환경에서는 항상 여러 모델이 공존한다"** — 현재 운영 모델, 신규 배포 모델, 롤백 대상 모델.
필요한 제어: **트래픽 분할 · 단계적 배포 · 즉시 롤백 가능 구조.** 도구는 MLflow(Model Registry).

[[Data and model versioning]]이 *재현*을 위한 버전 관리라면, 여기는 **롤백**을 위한 버전 관리다.

## 열린 질문

- **배치와 온라인을 함께 쓰는 하이브리드** — 실무에서 흔한 "사전 계산 + 실시간 보정" 패턴이
  강의에 나오지 않는다. Lambda 아키텍처의 서빙판이 있을 텐데 다루지 않는다.
- **트래픽 분할·카나리의 구현** — "필요하다"까지만 나오고 방법이 없다.
- **Dagster·Prefect** — ML 배치 오케스트레이터 비교에도 등장하지 않는다.
  ([[Data Engineering]] MOC의 열린 질문은 **일반 ETL 축에서 여전히 미해결**.)

## 링크

- 상위: [[MLOps]] (라이프사이클 4단계)
- 실행 계층: [[Model serving platforms]] · [[Inference optimization]]
- 피처 공급: [[Feature store]] · [[ML data pipeline]]
- 축이 다른 형제: [[Batch and stream processing]] (처리 시점) · [[Latency and throughput]]
- 운영: [[Data SLA and observability]] · [[Data and model versioning]]
- 출처: [[AI DE Course - Part2 Ch3 Serving pipeline]] ·
  [[AI DE Course - Part2 Ch4 Serving architecture]]

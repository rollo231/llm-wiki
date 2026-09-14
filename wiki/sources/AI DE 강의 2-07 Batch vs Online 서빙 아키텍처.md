---
type: source
title: AI DE 강의 2-07 Batch vs Online 서빙 아키텍처
aliases: [AI DE 2-07]
tags: [AI-DE-강의, 서빙, MLOps, 아키텍처]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/data-engineering/ai-de-course/part2/04. Ch4. 서빙 아키텍처 및 플랫폼.pdf"
---

# AI DE 강의 2-07 Batch vs Online 서빙 아키텍처

[[AI 데이터 엔지니어링 강의]] Part 2의 Ch4 첫 소단원. 배치 서빙과 온라인 서빙을 **구성 요소 수준**에서 비교한다 —
배치 쪽은 오케스트레이션 도구(Airflow·Kubeflow Pipelines·Flyte)와 예측 파이프라인 구조, 온라인 쪽은 요청 경로의
컴포넌트와 운영 요소. 같은 덱의 뒤 소단원은 [[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]과
[[AI DE 강의 2-09 서빙의 CPU·GPU 가속]]이다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 2 「AI 학습/추론 중심 데이터 파이프라인 설계」 |
| 덱 제목 | Ch4. 서빙 아키텍처 및 플랫폼 — 1. Batch vs Online 서빙 아키텍처 비교 |
| 원본 파일 | `part2/04. Ch4. 서빙 아키텍처 및 플랫폼.pdf` p1–16 (16p, 덱 전체 77p) |
| 강사 | Habi (슬라이드 표기) |
| 작성 시기 | PDF 생성일 2026-03-24 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch4`, 소단원 번호 `1`은 표지 슬라이드 |

## 요약

### 서빙 방식은 모델 문제가 아니라 시스템 선택

같은 모델이라도 배치로 서빙하면 전혀 다른 시스템이고, 온라인으로 서빙하면 또 전혀 다른 시스템이다. **서빙 방식
선택은 인프라·데이터 파이프라인·운영 비용을 동시에 결정한다.** → [[모델 서빙]]

### 배치 서빙의 흐름

```
주기적 스케줄 실행(hourly / daily) → 대량 데이터 로드 → Feature 계산 → 모델 추론 → 결과를 테이블·스토리지에 저장
```

**예측 결과는 사전에 계산된다.** → [[배치 처리]]

### 배치 서빙 도구

| | Airflow | Kubeflow Pipelines | Flyte |
|---|---|---|---|
| 위치 | SQL·Spark·Python 기반 배치 예측에 최적 | 학습–배포–배치 추론까지 ML 라이프사이클 중심, Kubernetes 기반 ML 플랫폼 | Airflow와 Kubeflow의 중간 지점, typed workflow 기반 |
| 아키텍처 관점 | DAG = 예측 파이프라인. Task 단위로 Feature 생성, 모델 로딩, 배치 추론, 결과 적재 | Pipeline = ML 워크플로. Component 단위로 Feature 생성, 학습, 배치 추론, 모델 아티팩트 관리 | Task·Workflow가 강하게 타입화됨. 데이터·모델 아티팩트 관리가 기본 설계에 포함 |
| 장점 | 데이터 엔지니어 친화적, 기존 ETL 파이프라인과 자연스럽게 통합, 재시도·백필·스케줄링 강력 | 모델 버전·실험 추적과 자연스럽게 연결, GPU·분산 환경 제어 용이, 학습–서빙 일관성 확보 | 재현성·버전 관리·캐싱 기본 제공, 대규모 배치 추론에 안정적, ML·데이터 워크플로 모두 적합 |
| 한계 | ML 개념(모델 버전, 실험 추적) 네이티브 지원 부족, GPU·분산 추론 제어는 별도 설계 필요 | 인프라 복잡도 높음, 순수 배치 서빙만 보면 과한 선택일 수 있음 | 러닝 커브, 생태계가 Airflow보다 작음 |

표의 내용은 전부 강의의 주장이다.

### 배치 서빙 세부 구조 — 예측 파이프라인

```
오프라인 데이터 → Feature 변환 → 대량 추론 → 결과 저장
```

| 단계 | 구성 예 |
|---|---|
| 원천 | Data Lake / Warehouse |
| Feature | Batch Feature Pipeline (Spark, SQL) |
| 추론 | Distributed Inference (Spark UDF, Ray, Batch job) |
| 결과 | 결과 저장 테이블 또는 Cache |

p12 도식: `Data Set —(preparation)→ Model —(Inference)→ DB/Cache`, 실행 주기 `1W/1D/1H/10m`.

### 온라인 서빙 세부 구조 — 컴포넌트의 협업

온라인 서빙은 단일 모델 서버가 아니라 여러 역할을 가진 컴포넌트의 협업이다.

| 컴포넌트 | 역할 | 예 |
|---|---|---|
| Client | 예측 요청 생성 | 웹·앱·내부 서비스 |
| Load Balancer | 요청 분산, 헬스체크 기반 트래픽 제어 | — |
| Prediction Service (Replica) | 요청 수신, Feature 조회, 모델 추론, 응답 생성 | — |
| Online Feature Store / Cache | 실시간 조회 가능한 Feature 제공 | Redis, DynamoDB, Feast Online Store |
| Model Artifact Storage | 모델 파일 저장 | S3, GCS, Model Registry |
| Logging / Metrics Pipeline | 요청·응답·Feature·예측 결과 수집 | Kafka, Pub/Sub, Prometheus |

**요청 흐름**

```
Client → Load Balancer → Prediction Service
  → Feature Key 추출 → Online Feature Store 조회
  → Feature 결합·전처리 → 모델 추론(CPU / GPU) → 후처리·응답 반환
```

추가로 결과 필터링, Fallback 로직, 서킷 브레이커를 설정한다. → [[피처 스토어]]

### 운영 시 주의할 요소 — 온라인 서빙은 운영 시스템

| 요소 | 내용 |
|---|---|
| Latency SLO | p95 / p99 기준 설정 |
| Timeout & Fallback | Feature 조회 실패 시 기본값 |
| Partial Failure 대응 | 일부 Feature Store 장애 허용 |
| Observability | 요청 단위 로그, Feature 분포 모니터링, 예측 결과 드리프트 감지 |

p16은 도구 로고 슬라이드다 — PyTorch(TorchServe), BentoML, FastAPI, NVIDIA Triton Inference Server, Prometheus,
Grafana, Datadog. → [[TorchServe]] · [[BentoML]] · [[FastAPI]] · [[Triton Inference Server]]

## 핵심

- **[[AI DE 강의 2-05 서빙 파이프라인 설계]]와 크게 겹친다.** 둘 다 배치 vs 온라인을 다루지만, 2-05는 **요구사항**
  (지연 예산·처리량·재현성·사용 사례)이고 이 강의는 **구성 요소**(도구·컴포넌트·요청 경로)다. 두 페이지를 짝으로
  읽는다. *(위키의 관찰)*
- **"Feature 조회 실패 시 기본값"은 스큐의 씨앗이다** — 바로 앞 [[AI DE 강의 2-06 Training-Serving Skew 예방]]의 결측
  처리 형태가 경고하는 지점인데 강의는 둘을 잇지 않는다. *(위키의 관찰)* → [[학습-서빙 스큐]]
- **서킷 브레이커의 자리가 바뀌었다.** Part 1의 [[데이터 관측성]]에서 서킷 브레이커는 품질이 나쁜 데이터가 하류로
  흐르지 않게 **파이프라인을 끊는** 장치였다. 여기서는 **요청 경로**에서 장애 난 의존성(피처 스토어 등)을 끊고
  fallback으로 응답하는 장치다. 같은 이름, 다른 층. *(위키의 관찰)*
- 온라인 서빙의 운영 요소가 [[지연 시간과 처리량]]의 한쪽 끝을 구체화한다 — 평균이 아니라 p95/p99 꼬리 지연을
  SLO로 삼는다.

## 주의·결함

- **목차 슬라이드(p2) 머리글이 템플릿 잔재다** — Ch4인데 Ch1 소단원 제목 "1. 데이터 파이프라인의 과거와 현재,
  데이터 엔지니어의 역할"이 붙어 있다. 나머지 슬라이드 머리글도 "2. AI 시대를 위한 파이프라인과 데이터엔지니어의
  진화방향"이다.
- **목차와 본문 구성이 비대칭이다** — 목차는 `02 Batch 서빙 아키텍쳐 / 03 Batch … 세부구조 / 04 Online … 세부구조`로
  배치에는 개요와 세부가 있지만 온라인은 세부 구조만 있다.
- **Airflow·Kubeflow Pipelines·Flyte 비교는 출처 없는 정성 평가다.** 벤치마크나 공식 문서 인용이 없다.
- ⚠️ **Flyte는 강의 작성 시점 전후로 세대가 갈렸다.** 슬라이드(2026-03)는 Flyte를 하나의 제품으로 설명하지만, Flyte 2 —
  순수 Python으로 새로 만든 재구축 — 가 2025-09-18 발표, 2026-03-04 로컬 오픈소스 공개, 2026-08-04 GA됐다(GA 날짜는
  Union.ai 보도자료 — 회사 발표). 강의가 드는 typed task·캐싱은 **Flyte 1 기준으로 맞다** ✅. [GitHub flyteorg/flyte
  README — "Flyte 2 is now generally available!" · "Looking for Flyte 1? Go to the master branch, where Flyte 1 is now
  maintained." https://github.com/flyteorg/flyte ; Flyte v1 캐싱 문서 — "a cache entry is created for each distinct
  combination of name, signature, cache version, and input set." https://www.union.ai/docs/v1/flyte/user-guide/ ,
  2026-09-14 확인]
- ✅ Kubeflow Pipelines 설명(Kubernetes 기반, 캐싱)은 공식 개요와 맞다. [Kubeflow 문서 — "a platform for building and
  deploying portable and scalable machine learning (ML) workflows using containers on Kubernetes-based systems",
  "caching to eliminating redundant executions" https://www.kubeflow.org/docs/components/pipelines/overview/ ,
  2026-09-14 확인]
- 온라인 서빙의 모델 배포 전략(카나리·트래픽 분할)과 오토스케일링은 이 소단원에서 다루지 않는다 — 트래픽 분할·
  단계적 배포는 [[AI DE 강의 2-05 서빙 파이프라인 설계]]의 모델 버전 관리 절에 짧게 있다.

## 관련

- 개념: [[모델 서빙]] · [[배치 처리]] · [[피처 스토어]] · [[학습-서빙 스큐]] · [[데이터 관측성]] ·
  [[지연 시간과 처리량]] · [[MLOps]]
- 도구: [[FastAPI]] · [[TorchServe]] · [[BentoML]] · [[Triton Inference Server]]
- 이전 강의: [[AI DE 강의 2-06 Training-Serving Skew 예방]]
- 다음 강의: [[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]

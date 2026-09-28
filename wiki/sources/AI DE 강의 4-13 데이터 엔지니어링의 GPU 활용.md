---
type: source
title: AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용
aliases: [AI DE 4-13]
tags: [AI-DE-강의, GPU, MLOps, ETL]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf"
---

# AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용

[[AI 데이터 엔지니어링 강의]] Part 4 Ch4의 소단원 4다. GPU를 학습 전용 자원이 아니라 MLOps 데이터 흐름 전체(전처리, 피처, 배치 추론, 임베딩, 서빙 로그, 모니터링)의 처리 자원으로 보고, 어디에 쓰고 어디에 쓰지 말지, 데이터 엔지니어와 MLE가 무엇을 합의해야 하는지를 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch4. GPU 워크로드 전략: 4. 데이터 엔지니어링에 GPU 활용하기 |
| 원본 파일 | `part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` p302–326 (25p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch1~4`, 챕터 `Ch4`와 소단원 번호 `4`는 표지 슬라이드 |

## 요약

### 01. 데이터 엔지니어링에서 GPU 활용 범위 (p304–309)

- GPU는 학습뿐 아니라 전처리, 피처 변환, 배치 추론, 이미지·영상·음성 입력 처리, 대규모 DataFrame 처리에 쓰인다. 데이터 엔지니어 쪽 위치는 GPU 가속 ETL, GPU 피처 엔지니어링, 학습 입력 파이프라인, 대량 배치 추론, 임베딩 생성, 서빙 로그 처리, 모니터링·드리프트 분석이다(p304).
- 데이터 엔지니어가 맡는 MLOps 데이터 흐름: 원천 수집, 학습 데이터셋 생성, 피처 계산과 저장, 배치 추론 입력 생성, 임베딩 파이프라인, 추론 로그 적재, 품질 모니터링 데이터, 재학습 트리거 데이터(p305).
- MLE와의 경계(p306): MLE는 모델 구조·학습 코드·평가 지표·서빙 요구를, 데이터 엔지니어는 입력 품질·피처 정합성·파이프라인 확장성·저장·재처리·모니터링을 맡고, 모델 버전·데이터 버전·추론 결과·운영 메트릭 연결은 공통 영역이다. 예로 MLflow Model Registry(lineage, versioning, aliasing, metadata tagging)와 Feast(offline store가 학습 데이터를, online store가 실시간 추론용 최신 피처를 제공)를 든다.
- GPU를 쓸지 판단하는 세 질문(p307–309): 대량 병렬 연산인가, 데이터 이동 비용보다 계산 이득이 큰가, MLOps 운영 흐름(피처 저장소·모델 버전·추론 로그·재학습)과 이어지는가.

### 02. GPU 가속 ETL, Feature Engineering (p310–313)

- cuDF: GPU DataFrame. pandas·Polars·Spark 계열 워크플로우 가속, filter·join·group by·aggregation 같은 열 연산에 적합(p310–311).
- Spark RAPIDS: 기존 Spark SQL·DataFrame을 플러그인으로 가속, 미지원 연산은 CPU로 fallback. RDD 중심의 오래된 코드는 효과가 제한된다(p312).
- Dask-cuDF(multi-GPU·multi-node)와 NVTabular(추천 시스템용 TB급 피처 전처리)(p313).

### 03. 학습·추론 입력 파이프라인 가속 (p314–317)

- 학습이 느린 이유가 모델 연산이 아니라 데이터 공급(로딩, 디코딩, resize, augmentation, tokenization, batch 구성)일 수 있다. GPU가 기다리면 utilization이 떨어진다(p314).
- 데이터 엔지니어의 역할: 학습 데이터 포맷, 파일 크기와 shard, batch 구성, streaming read와 prefetch, CPU/GPU 전처리 분리, 재현 가능한 dataset version(p315).
- 배치 추론과 임베딩 생성: 대량 문서 임베딩, 이미지 피처 추출, offline scoring, 벡터 DB 적재 전 임베딩 파이프라인. 설계 요소는 batch size, GPU 메모리, 모델 로딩 비용, 재시도와 checkpoint, 결과 포맷, 모델 버전과 데이터 버전 연결(p316–317).

### 04. 모델 서빙과 MLOps 운영 데이터 흐름 (p318–321)

- Triton: 여러 프레임워크 모델, 실시간·배치·ensemble·streaming 추론, 모델 저장소. 데이터 엔지니어 쪽 연결은 입력 포맷 표준화, 서빙 로그 적재, request/response schema, 모델 버전별 결과 비교, throughput·latency 모니터링(p318).
- KServe: InferenceService 리소스, Knative 기반 모드의 요청량 autoscaling, GPU resource limit. 추론 결과는 모니터링·분석·재학습 데이터로 다시 들어오고, 서빙 GPU는 배치 ETL GPU와 분리해야 한다(p319).
- MLOps 데이터 흐름의 세 축은 Feature Store(Feast), Model Registry(MLflow), Pipeline Orchestrator(Kubeflow Pipelines)다(p320). 데이터 엔지니어의 연결 책임은 네 질문으로 준다. 어떤 데이터로 어떤 모델이, 어떤 피처 버전이 어떤 모델 버전에, 어떤 모델 버전이 어떤 추론 로그를, 어떤 모니터링 결과가 어떤 재학습을(p321).

### 05. GPU 데이터 파이프라인 설계 판단 기준 (p322–326)

- 잘 맞는 후보: 큰 DataFrame 연산, 대량 join·group by·aggregation, 배치 추론, 임베딩 생성, 이미지·영상·음성 전처리, 추천 피처 엔지니어링, 반복 벡터·행렬 연산. 공통 조건은 충분한 크기, 높은 병렬성, 규칙적인 연산, GPU 메모리에 맞는 batch, 이동 비용보다 큰 계산 이득(p322–323).
- 오히려 나빠질 수 있는 경우: 작은 데이터, 짧고 잦은 작업, 큰 이동 비용, 잦은 CPU fallback, RDD 중심 Spark, 분기와 불규칙 접근이 많은 로직, GPU 메모리보다 커서 spill과 재처리가 많은 데이터, MLOps 추적 없는 단발성 가속(p324).
- DE와 MLE가 합의할 인터페이스(p325–326): 데이터(입력 schema, feature·label definition, partition, batch size, 데이터 버전), 모델(model version, input/output schema, inference batch format, latency·throughput, fallback), 운영(추론 로그 schema, 모니터링 지표, drift 기준, 재학습 트리거, 재시도 기준, 비용 budget).

## 핵심

- GPU를 쓸지 말지를 세 질문(p307–309)과 "오히려 나빠지는 경우"(p324)로 판단하게 하는 것이 이 소단원에서 가장 옮겨 쓰기 좋다. 조건들의 하드웨어 이유는 [[GPU 아키텍처]]에, 도구는 [[RAPIDS]]에 있다.
- DE–MLE 인터페이스 세 묶음(p325–326)은 사실상 두 팀 사이의 [[데이터 계약]] 목록이다. 코스의 다른 곳에서 흩어져 나온 요소(피처 정의는 [[피처 스토어]], 모델·데이터 버전은 [[데이터와 모델 버전 관리]], drift 기준은 [[데이터 드리프트]], 비용 budget은 [[AI DE 강의 4-15 AI 시스템 지표와 SLA]])를 한 장에 모은다. 데이터 계약으로 읽는 것은 위키의 해석이다.
- 데이터 엔지니어의 연결 책임 네 질문(p321)은 [[MLOps]]의 계보 추적을 데이터 쪽에서 쓴 것이다.

## 주의·결함

- ⚠️ NVTabular(p313)는 2023-08(v23.08.00) 이후 릴리스가 없다. 저장소는 보관되지 않았지만 정체 상태다([[RAPIDS]]). [GitHub REST API로 확인, 2026-09-28]
- ⚠️ cuDF가 "Polars" 워크플로우를 가속한다(p310)는 것은 Polars GPU 엔진(cudf-polars) 이야기이고, 이것은 2024-09부터 Open Beta다. [https://docs.pola.rs/user-guide/gpu-support/ , 2026-09-28 확인]
- ⚠️ KServe의 "Knative 기반 모드"(p319)는 이름이 바뀌었다. 현재 문서는 배포 모드를 `Standard`(옛 RawDeployment)와 `Knative`(옛 Serverless)로 부르고, LLM용 `LLMInferenceService` CRD가 새로 생겼다. KServe는 2025-09-29 CNCF Incubating 프로젝트가 됐다. [https://kserve.github.io/website/docs/admin-guide/kubernetes-deployment · https://www.cncf.io/projects/kserve/ ("KServe was accepted to CNCF on September 29, 2025 at the Incubating maturity level.") · https://github.com/kserve/kserve/blob/master/pkg/constants/constants.go (`LegacyRawDeployment … deprecated: use Standard`) , 2026-09-28 확인]
- ✅ MLflow Model Registry의 alias(p306, p320)는 현행 방식이다. 스테이지는 2.9.0부터 deprecated다. [https://mlflow.org/docs/latest/ml/model-registry/workflow/ , 2026-09-28 확인]
- 수치가 없다. "대량", "충분히 큼", "이동 비용보다 큰 이득"의 기준(몇 GB부터인지, 어떤 연산에서 몇 배인지)을 주지 않는다. 수치는 다음 소단원의 사례에만 나오고 출처가 없다([[AI DE 강의 4-14 RAPIDS 가속 ETL]]).
- 이 소단원의 cuDF·Spark RAPIDS·Dask-cuDF 소개(p310–313)가 다음 소단원(p342–348)에서 거의 그대로 다시 나온다.

## 관련

- 개념: [[GPU 아키텍처]] · [[MLOps]] · [[피처 스토어]] · [[모델 서빙]] · [[데이터 계약]] · [[데이터와 모델 버전 관리]]
- 엔티티: [[RAPIDS]] · [[Triton Inference Server]] · [[Apache Spark]]
- 이전 강의: [[AI DE 강의 4-12 GPU 할당 아키텍처]]
- 다음 강의: [[AI DE 강의 4-14 RAPIDS 가속 ETL]]

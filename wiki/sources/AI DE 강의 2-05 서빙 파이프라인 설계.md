---
type: source
title: AI DE 강의 2-05 서빙 파이프라인 설계
aliases: [AI DE 2-05]
tags: [AI-DE-강의, 서빙, MLOps]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/data-engineering/ai-de-course/part2/03. Ch3. ML 데이터·서빙 파이프라인.pdf"
---

# AI DE 강의 2-05 서빙 파이프라인 설계

[[AI 데이터 엔지니어링 강의]] Part 2의 Ch3 두 번째 소단원. 추론 요청 하나를 처리하는 **실행 경로**로서의 서빙
파이프라인과 그 **요구사항**을 다룬다 — 배치 서빙 vs 온라인 서빙, 서빙 경로의 피처 접근과 캐싱, CPU/GPU 선택,
모델 버전 관리. 같은 주제를 **구성 요소** 쪽에서 다시 보는 강의가 [[AI DE 강의 2-07 Batch vs Online 서빙 아키텍처]]다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 2 「AI 학습/추론 중심 데이터 파이프라인 설계」 |
| 덱 제목 | Ch3. ML 데이터/서빙 파이프라인 — 2. 서빙 파이프라인 설계 및 요구사항 |
| 원본 파일 | `part2/03. Ch3. ML 데이터·서빙 파이프라인.pdf` p17–36 (20p, 덱 전체 51p) |
| 강사 | Habi (슬라이드 표기) |
| 작성 시기 | PDF 생성일 2026-03-05 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch3`, 소단원 번호 `2`는 표지 슬라이드 |

## 요약

### 01. 서빙 파이프라인이란

서빙 파이프라인은 **추론 요청을 처리하는 실행 경로**다.

```
외부 요청(입력) → 실시간 Feature 조회·계산 → 모델 추론 → 결과를 응답으로 반환
```

이 과정이 **사용자 요청마다 반복 실행**된다. p20 그림은 전체 MLOps 고리를 한 장에 그린 스케치다 — Data Ingestion →
(Offline) Data Analysis → Data Preparation → Model Training ↔ Model Evaluation and Validation → Trained Model →
Model Registry → Model Serving → Prediction Service → Model Performance Monitoring → Trigger → 다시 Data Ingestion.
서빙은 이 고리의 오른쪽 끝이다. → [[MLOps]]

### 02. 입력과 출력

서빙은 **데이터 형태가 고정되지 않은 상태**에서 동작한다.

| 입력 | 출력 |
|---|---|
| 실시간 이벤트, API 요청, 사용자 컨텍스트 | 예측값, 점수, 랭킹, 분류 결과 |

입력 데이터는 **불완전하거나 지연될 수 있고**, 서빙 파이프라인은 이를 전제로 설계해야 한다.

### 03. 기본 요구사항

서빙은 연구 환경과 다른 제약을 가진다.

- **지연 시간 제한(Latency Budget)**이 있다 — 백엔드 팀과 소통이 필요하다.
- **실패율이 곧 서비스 장애**로 이어진다.
- 트래픽 변동에 따라 **자동 확장**이 필요하다.
- **요청 단위로** 안정적으로 동작해야 한다.

### 04. Batch Serving과 Online Serving

**Batch Serving** — 일정 주기로 데이터를 모아 대량으로 예측하고, 결과를 테이블·파일·캐시로 저장해 시스템이 쓴다.

```
원천 데이터 적재(Data Lake / Warehouse) → Feature 변환·집계 → 모델 추론(Spark, Batch Job) → 예측 결과 저장(DB, DW, Object Storage)
```

| 항목 | 내용 |
|---|---|
| 사용 사례 | 추천 점수 사전 계산, 고객 세그먼트 분류, 리스크 스코어·신용 점수, 마케팅 타겟 리스트 |
| 핵심 특징 | 실시간 추론 불필요, 예측은 사전에 계산·저장, 모델 호출이 사용자 요청과 분리 |
| 설계 목표 | 높은 처리량(Throughput), 비용 효율성, 재현 가능성(Reproducibility) |
| 장점 | 대규모 데이터 처리에 유리, 인프라 비용 최적화(Spot·예약 리소스), 실패 시 재시도·백필이 쉬움 |
| 제약 | 예측 결과가 최신이 아닐 수 있음, 데이터 지연 감수, 사용자 행동 변화에 즉각 대응 불가 |

**Online Serving** — 요청이 들어오는 순간 실시간으로 추론하고 결과를 즉시 응답으로 돌려준다.

```
클라이언트 요청 수신(API) → 실시간 Feature 조회 → 모델 추론 → 응답 반환(수 ms ~ 수십 ms)
```

| 항목 | 내용 |
|---|---|
| 사용 사례 | 실시간 사기 탐지, 광고 입찰, 개인화 추천, 실시간 이상 탐지 |
| 핵심 특징 | 사용자 요청 경로에 모델이 직접 포함됨, 지연 시간이 시스템 품질을 결정, 모델 실패 = 서비스 실패 가능성 |
| 설계 목표 | 낮은 지연 시간, 높은 가용성, 예측 일관성(Consistency) |
| 핵심 제약 | **Feature 조회 시간이 전체 latency의 대부분**, 모델 크기·복잡도가 응답 시간에 직접 영향, 트래픽 스파이크 대응 |

**비교(p30)**

| 구분 | 배치 예측 (비동기) | 온라인 예측 (동기) |
|---|---|---|
| 예측 빈도 | 주기적으로 수행 (예: 4시간마다) | 요청이 들어오는 즉시 수행 |
| 적합한 사용 사례 | 즉각적인 결과가 필요 없는 누적 데이터 처리 (예: 추천 시스템, 리포트 생성) | 데이터 샘플이 생성되자마자 예측이 필요한 경우 (예: 이상 거래 탐지, 실시간 사기 탐지) |
| 최적화 목표 | 높은 처리량 (High Throughput) | 낮은 지연 시간 (Low Latency) |

### 05. 서빙 파이프라인에서 Feature의 역할

서빙 성능은 **Feature 접근 방식**에 크게 의존한다. 접근 방식은 네 가지 — 실시간 계산 Feature, 사전 계산된 Feature,
캐시 기반 Feature, 외부 스토어 조회 Feature(p31–32, Databricks 피처 스토어 그림).

서빙 경로에서 Feature 조회는 비용이 크다:

- 네트워크 호출 비용
- 스토리지 응답 지연
- 캐시 미스 발생 가능성
- 일부 Feature 누락 가능성

→ [[피처 스토어]]

### 06. 캐싱 전략

서빙 경로에서는 **계산을 최소화**한다.

- 변경 주기가 긴 Feature는 사전 계산
- 요청 단위 계산은 최소
- 동일 요청 반복 시 캐시 활용
- **캐시 실패를 고려한 fallback**이 필요

### 07. 서빙 플랫폼 선택

특성에 맞는 서빙 플랫폼과 CPU/GPU를 고른다.

| CPU | GPU |
|---|---|
| 낮은 비용, 빠른 스케일 | 높은 처리량, 초기 로딩 비용 |

배치 추론 여부에 따라 효율이 달라지고, 자원 선택은 **트래픽 패턴**으로 결정한다. → [[AI DE 강의 2-09 서빙의 CPU·GPU 가속]]

### 08. 모델 버전 관리

서빙 환경에서는 **항상 여러 모델이 공존**한다 — 현재 운영 모델, 신규 배포 모델, 롤백 대상 모델. 필요한 제어는
트래픽 분할, 단계적 배포, 즉시 롤백 가능한 구조다. → [[데이터와 모델 버전 관리]]

## 핵심

- **서빙 방식은 모델이 아니라 요구사항에서 정해진다.** [[AI DE 강의 2-02 MLOps와 ML 생애주기]]의 Project Scoping 단계가
  "온라인 추론인지 배치 예측인지"를 먼저 정하고, 그 선택이 [[AI DE 강의 2-07 Batch vs Online 서빙 아키텍처]]에서 전혀
  다른 두 시스템이 된다. 이 강의는 **요구사항**, 2-07은 **구성 요소**다 — 두 페이지를 짝으로 읽는다. *(위키의 관찰)*
  → [[모델 서빙]]
- **지연 예산은 남의 SLO 안에 있다.** 온라인 서빙은 백엔드 요청 경로의 한 구간이라, 모델에 쓸 수 있는 시간은 백엔드가
  사용자에게 약속한 응답 시간에서 나머지를 뺀 몫이다. 요구사항 슬라이드에 "백엔드 팀과 소통"이 들어간 이유다.
  *(위키의 관찰)*
- **배치 vs 온라인은 [[지연 시간과 처리량]]의 시소가 다시 나온 것이다.** 비교표의 마지막 줄이 그대로 "높은 처리량 vs 낮은
  지연 시간"이다. Part 1의 [[AI DE 강의 1-10 배치 vs 스트리밍]]이 데이터 처리에서 한 이야기를 추론에서 반복한다.
- **온라인 서빙에서 어려운 것은 모델이 아니라 피처 접근이다.** 이 강의는 "Feature 조회 시간이 latency의 대부분"이라고
  하고(수치·출처는 없다 — 주의·결함), 그 비용을 줄이는 수단으로 사전 계산·캐시·fallback을 든다. 캐시·fallback 값이 학습 때
  본 값과 다르면 스큐가 된다. *(위키의 연결)* → [[학습-서빙 스큐]] · [[피처 스토어]]
- **배치 서빙의 장점 목록은 [[배치 처리]]의 장점과 같다** — 재시도·백필·재현성·Spot 인스턴스. 배치 서빙은 "출력이 예측값인
  배치 파이프라인"이다. *(위키의 관찰)*

## 주의·결함

- ⚠️ **p30 비교표는 Chip Huyen의 표를 출처 없이 옮긴 것이다.** 행 구성(빈도·적합한 사용 사례·최적화 목표)과 예시(4시간마다,
  추천 시스템, 사기 탐지)가 거의 그대로이고, 원본의 마지막 행 **Examples**(Netflix recommendations | Google Assistant speech
  recognition)만 빠졌다. 원 표는 Huyen의 Stanford CS 329S 강의 노트에서 Table 6-1이고, 책 [[Designing Machine Learning Systems]]에서는
  Ch. 7 "Model Deployment and Prediction Service"에 속한다(책의 표 번호는 확인하지 못함). [CS 329S Lecture 8 note —
  "Batch prediction (asynchronous) | Online prediction (synchronous) | Frequency: Periodical, such as every 4 hours | As soon
  as requests come | Useful for: Processing accumulated data when you don't need immediate results (such as recommendation
  systems) | When predictions are needed as soon as data sample is generated (such as fraud detection) | Optimized for: High
  throughput | Low latency | Examples: Netflix recommendations | Google Assistant speech recognition"
  https://docs.google.com/document/d/1hNuW6bqWYZjlwpit_8W1cu7kllb-jTfy3Liof1GJWug , 2026-09-14 확인] [Chip Huyen, "Real-time
  machine learning: challenges and solutions" (2022-01-02) — "all predictions are precomputed in batch, generated at a certain
  interval, e.g. every 4 hours or every day. Typical use cases for batch prediction are collaborative filtering, content-based
  recommendations." https://huyenchip.com/2022/01/02/real-time-machine-learning-challenges-and-solutions.html , 2026-09-14 확인]
- **"Feature 조회 시간이 전체 latency의 대부분"** — 수치나 출처가 없다. 방향은 그럴듯하지만 서비스마다 다르다.
- **중복 슬라이드** — p35와 p36이 완전히 같고, p31과 p32는 같은 Databricks 그림을 두 번 쓴다.
- **슬라이드 머리글이 템플릿 잔재다** — Ch3 전체 머리글이 Ch1 소단원 제목 "2. AI 시대를 위한 파이프라인과 데이터엔지니어의
  진화방향"이다. 오탈자 "높은 처리량Throughput)"(p25).
- **배치와 온라인의 이분법만 제시한다.** 온라인 예측이라도 피처를 배치로 미리 계산해 두는지, 스트리밍으로 갱신하는지에 따라
  시스템이 크게 달라지는데 그 중간 지대는 다루지 않는다. 캐싱 절의 "사전 계산 Feature"가 그 흔적일 뿐이다. *(위키의 관찰)*
- 모델 버전 관리 절은 트래픽 분할·단계적 배포·롤백을 **이름만** 든다 — 카나리·A/B·섀도우의 차이와 승격 기준은 없다.

## 관련

- 개념: [[모델 서빙]] · [[피처 스토어]] · [[학습-서빙 스큐]] · [[지연 시간과 처리량]] · [[배치 처리]] ·
  [[데이터와 모델 버전 관리]] · [[MLOps]]
- 도서: [[Designing Machine Learning Systems]]
- 이전 강의: [[AI DE 강의 2-04 ML 데이터 파이프라인]]
- 다음 강의: [[AI DE 강의 2-06 Training-Serving Skew 예방]]

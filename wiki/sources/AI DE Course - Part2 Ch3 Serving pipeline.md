---
type: source
title: AI DE Course - Part2 Ch3 Serving pipeline
area: [data-engineering]
aliases: [Part2 Ch3-2, 서빙 파이프라인 설계 및 요구사항]
tags: [data-engineering, course, fast-campus, mlops, serving, inference, caching, model-registry]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part2/03. Ch3. ML 데이터·서빙 파이프라인.pdf"]
---

# AI DE Course - Part2 Ch3 Serving pipeline

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 2 Ch3** "ML 데이터/서빙
파이프라인"의 소단원 **2** "서빙 파이프라인 설계 및 요구사항". 강사 **Habi**. 원본(로컬):
`raw/data-engineering/ai-de-course/part2/03. Ch3. ML 데이터·서빙 파이프라인.pdf` **p18–36**. 강의 홈:
[[AI Data Engineering (Fast Campus course)]].

**Batch/Online 서빙의 개념을 세우는 자리.** 아키텍처 상세는 Ch4가 이어받는다 →
[[AI DE Course - Part2 Ch4 Serving architecture]]. 개념은 [[Batch and online serving]]으로 옮겼다.

## 정의 — 서빙 파이프라인은 "추론 요청을 처리하는 실행 경로"

외부 요청을 입력으로 받음 → 실시간 Feature를 조회하거나 계산 → 모델 추론 수행 → 결과를 응답으로
반환. **이 과정은 사용자 요청마다 반복 실행된다.**

**입출력의 성질:** "서빙은 데이터 형태가 고정되지 않은 상태에서 동작한다."

- 입력: 실시간 이벤트, API 요청, 사용자 컨텍스트
- 출력: 예측 값, 점수, 랭킹, 분류 결과
- **입력 데이터는 불완전하거나 지연될 수 있다**
- **서빙 파이프라인은 이를 전제로 설계해야 한다**

> 마지막 두 줄이 다음 소단원(skew)의 복선이다. *불완전·지연을 전제로 설계한다*는 말은 곧
> **학습 때와 다른 값이 들어온다는 걸 인정한다**는 뜻이다 →
> [[AI DE Course - Part2 Ch3 Training-serving skew patterns]].

## 요구사항 — "연구 환경과 다른 제약"

- **지연 시간 제한(Latency Budget)이 존재** — 그리고 이건 ML팀 혼자 정하는 게 아니다:
  **"백엔드팀과 소통 필요"**
- **실패율이 곧 서비스 장애로 연결됨**
- 트래픽 변동에 따라 자동 확장 필요
- 요청 단위로 안정적으로 동작해야 함

부하 테스트 도구 **Locust** 대시보드 스크린샷(RPS·응답시간 p50/p95·동시 사용자)을 붙여
"측정하고 시작한다"는 태도를 보인다.

> **Latency Budget을 백엔드와 협상한다**는 지점이 이 소단원에서 가장 실무적이다. 모델의 추론
> 시간은 전체 예산의 일부일 뿐이고, 예산 자체는 제품 팀이 쥐고 있다.
> Ch4가 이 예산을 항목별로 분해한다 → [[AI DE Course - Part2 Ch4 CPU and GPU inference]].

## Batch Serving vs Online Serving

강의는 Chip Huyen 책의 Batch prediction / Online prediction 그림을 인용한다.

### Batch Serving

일정 주기로 데이터를 모아 **대량으로 예측을 수행**하고, 결과를 테이블·파일·캐시로 저장해 시스템이
꺼내 쓴다. 흐름: `원천 적재(Lake/DW) → Feature 변환·집계 → 모델 추론(Spark, Batch Job) →
예측 결과 저장(DB·DW·Object Storage)`.

| | 내용 |
|---|---|
| 사용 사례 | 추천 점수 사전 계산, 고객 세그먼트 분류, 리스크·신용 점수, 마케팅 타겟 리스트 |
| 특징 | 실시간 추론 불필요 · 예측 결과가 **사전에** 계산되어 저장 · **모델 호출이 사용자 요청과 분리됨** |
| 설계 목표 | 높은 처리량(Throughput) · 비용 효율성 · **재현 가능성(Reproducibility)** |
| 장점 | 대규모 처리 유리 · 인프라 비용 최적화(Spot·예약 리소스) · **실패 시 재시도·백필이 용이** |
| 제약 | 예측 결과가 최신이 아닐 수 있음 · 데이터 지연 감수 · **사용자 행동 변화에 즉각 대응 불가** |

### Online Serving

요청이 들어오는 순간 실시간 추론 → 즉시 응답. 흐름: `클라이언트 요청 수신(API) → 실시간 Feature
조회 → 모델 추론 → 응답 반환 (수 ms ~ 수십 ms)`.

| | 내용 |
|---|---|
| 사용 사례 | 실시간 사기 탐지, 광고 입찰, 개인화 추천, 실시간 이상 탐지 |
| 특징 | **사용자 요청 경로에 모델이 직접 포함됨** · 지연 시간이 시스템 품질을 결정 · **모델 실패 = 서비스 실패 가능성** |
| 설계 목표 | 낮은 지연(Low Latency) · 높은 가용성 · 예측 일관성(Consistency) |
| 핵심 제약 | **Feature 조회 시간이 전체 latency의 대부분을 차지** · 모델 크기·복잡도가 응답 시간에 직접 영향 · 트래픽 스파이크 대응 |

### 정리표

| 구분 | 배치 예측 (비동기) | 온라인 예측 (동기) |
|---|---|---|
| 예측 빈도 | 주기적 (예: 4시간마다) | 요청 즉시 |
| 적합한 사례 | 즉각적 결과가 불필요한 누적 데이터 처리(추천, 리포트) | 데이터 샘플이 생성되자마자 예측이 필요한 경우(이상 거래·실시간 사기 탐지) |
| 최적화 목표 | **높은 처리량(High Throughput)** | **낮은 지연(Low Latency)** |

> Part 1 [[Latency and throughput]]의 "시소의 법칙"이 서빙에서 그대로 재현된다. **다만 축이
> 다르다** — Part 1은 *데이터 처리*의 배치/스트림이었고 여기는 *예측 생성 시점*의 배치/온라인이다.
> 스트리밍 처리를 쓰면서 배치 서빙을 할 수도 있다. → [[Batch and online serving]]

## Feature 조회가 서빙의 병목이다

**"서빙 성능은 Feature 접근 방식에 크게 의존"** — 네 가지 접근이 있다: 실시간 계산 Feature /
사전 계산된 Feature / 캐시 기반 Feature / 외부 스토어 조회 Feature.

서빙 경로에서 Feature 조회는 비용이 크다: **네트워크 호출 비용 · 스토리지 응답 지연 ·
캐시 미스 가능성 · 일부 Feature 누락 가능성.**

### 캐싱 전략 — "서빙 경로에서는 계산을 최소화"

- 변경 주기가 긴 Feature는 **사전 계산**
- 요청 단위 계산은 최소
- 동일 요청 반복 시 캐시 활용
- **캐시 실패를 고려한 fallback 필요**

그림: `Client → API → Cache (miss) → Feature Store → put(user_id, features, TTL)`.

> **"캐시 미스 시 fallback"이 조용한 skew의 진입로**다 — 조회 실패를 0으로 채우면 학습 때와 다른
> 입력이 된다. 다음 소단원이 이걸 정면으로 다룬다.

## 서빙 플랫폼과 자원

플랫폼 4종(TorchServe·BentoML·Ray·Triton) 로고를 걸고 원칙만 제시한다:

- CPU: 낮은 비용, 빠른 스케일 / GPU: 높은 처리량, **초기 로딩 비용**
- **배치 추론 여부에 따라 효율이 달라짐**
- **자원 선택은 트래픽 패턴에 따라 결정**

상세는 Ch4 → [[Model serving platforms]] · [[AI DE Course - Part2 Ch4 Serving platforms]].

## 모델 버전 관리

**"서빙 환경에서는 항상 여러 모델이 공존한다"** — 현재 운영 모델, 신규 배포 모델, 롤백 대상 모델.
필요한 제어: **트래픽 분할 · 단계적 배포 · 즉시 롤백 가능 구조.**

도구로 **MLflow**를 든다 (MLflow 3.0 Tracking UI 스크린샷 — Models 탭에 `torch-iris-0`~`-100`
버전별 accuracy·activation·Dataset·Source run이 나열된 화면).

> Part 1 [[Data and model versioning]]이 "재현성 3요소"를 말했다면, 여기는 **운영 중 공존**이
> 주제다. 버전 관리의 목적이 재현에서 **롤백**으로 옮겨간다.

## 기존 페이지와의 대조

- **신규** — Batch/Online 서빙의 구분, Feature 조회 비용, 서빙 캐싱 전략 → [[Batch and online serving]].
- **연결** — [[Feature store]]의 online store가 여기서 "서빙 latency의 대부분"이라는 위치를 얻는다.
  Part 1은 online store를 "초저지연 조회 계층"이라 적었는데, **Part 2는 그게 병목이라고 말한다.**
  같은 사실의 다른 얼굴 — 보강이지 모순은 아니다.
- **일치** — MLflow가 모델 레지스트리라는 구도는 Part 1 [[AI DE Course - Ch1-4 Tech stack and tooling]]과 동일.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Batch and online serving]] (상세) · [[Feature store]] · [[Latency and throughput]] ·
  [[Data and model versioning]] · [[Model serving platforms]]
- 앞: [[AI DE Course - Part2 Ch3 ML data pipeline]]
- 다음: [[AI DE Course - Part2 Ch3 Training-serving skew patterns]]

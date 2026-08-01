---
type: concept
title: Data and model versioning
area: [data-engineering]
aliases:
  - Data versioning
  - Model versioning
  - Reproducibility
  - 데이터 버전 관리
  - 재현성
tags: [data-engineering, versioning, reproducibility, mlops, mindset]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Ch1-2,3 Latency and Versioning]]"]
---

# Data and model versioning

강의가 [[AI data engineering]]의 **두 가지 핵심 마인드셋** 중 하나로 꼽는 것
(다른 하나는 [[Latency and throughput|Latency]]).

전제는 단순하다: **코드는 git으로 관리하는데, 데이터와 모델도 버전 관리 대상이다.**
"모델 성능이 지난주보다 떨어졌다"는 보고가 왔을 때 **무엇이 달라졌는지 특정할 수 없다면** 디버깅이
불가능하기 때문이다 — 코드는 같은데 데이터가 바뀌었을 수 있다.

## 재현성의 3요소

강의가 제시하는 최소 조건. 셋 중 하나라도 빠지면 같은 실험이 같은 결과를 내지 않는다.

| 요소 | 방법 |
|---|---|
| **데이터 스냅샷** | 학습을 시작하는 그 순간의 데이터를 사진 찍듯 스냅샷으로 저장 |
| **환경 고정** | Docker 컨테이너, Conda 가상환경 |
| **랜덤 시드** | seed 고정 |

## 왜 git만으로는 안 되나

git은 텍스트 diff에 최적화되어 있고, 수십 GB~TB급 바이너리(Parquet·이미지·모델 가중치)를 담을
설계가 아니다. 그래서 데이터 쪽은 **"파일을 복사하지 않고 시점을 가리키는"** 방식으로 푼다 —
그게 [[Table formats]]의 **time travel**이다.

- **Delta Lake의 트랜잭션 로그** — 로그를 특정 시점까지만 읽으면 그 시점의 유효 파일 목록이 나온다.
  데이터를 복제하지 않고 스냅샷을 얻는다 → [[AI DE Course - Ch2-7 Delta Lake and ACID]]
- **ELT가 raw를 보존하는 이유**와도 맞물린다 — 원본이 남아 있으면 언제든 재계산할 수 있다
  → [[ETL and ELT]]

즉 **"데이터 스냅샷"은 별도 도구가 아니라 저장 계층의 기능으로 얻는 것이 현대적 방식이다.**

## 운영으로 이어지는 지점

재현성은 학술적 미덕이 아니라 [[Data drift and training-serving skew|drift]] 대응의 전제다.
재학습 파이프라인이 자동으로 돌 때 각 단계가 요구하는 것:

- **데이터셋 버전 관리** — 어떤 스냅샷으로 학습했는지
- **모델 버전·메타데이터 관리** — Champion vs Challenger 비교, 자동 롤백의 기준점
- **재현 가능한 학습 환경** — 롤백했을 때 정말 이전 성능이 재현되는가

## 이 페이지의 한계

**출처 덱이 매우 얇다.** CH01-2,3은 16페이지 중 대부분이 제목 카드이고 versioning 관련 실질 내용은
"git → 데이터·모델도 대상" + 재현성 3요소, 이 정도다. 도구(DVC·MLflow·Weights & Biases 등)나
실제 워크플로우는 나오지 않는다.

→ **Part 2 Ch2(MLOps와 LLMOps)** 가 Machine Learning Life Cycle을 다루므로 그때 채운다.
([[AI Data Engineering (Fast Campus course)]])

## 링크

- 짝을 이루는 마인드셋: [[Latency and throughput]]
- 스냅샷을 실제로 구현하는 층: [[Table formats]] — time travel
- raw 보존: [[ETL and ELT]]
- 왜 필요한가: [[Data drift and training-serving skew]] — 재학습 파이프라인의 전제
- 출처: [[AI DE Course - Ch1-2,3 Latency and Versioning]]

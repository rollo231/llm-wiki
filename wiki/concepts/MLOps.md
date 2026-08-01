---
type: concept
title: MLOps
area: [data-engineering]
aliases:
  - ML Ops
  - 엠엘옵스
  - Machine learning lifecycle
  - ML 라이프사이클
  - 머신러닝 생애주기
tags: [data-engineering, mlops, devops, lifecycle, model-serving]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part2 Ch2 MLOps and the ML lifecycle]]"]
---

# MLOps

**ML 시스템을 운영 가능한 형태로 만드는 체계.** 모델 개발과 서비스 운영을 잇고, 데이터·모델·인프라·
배포를 하나의 흐름으로 관리한다.

존재 이유는 한 문장이다 — **"모델은 만들어졌지만, 서비스는 자동으로 되지 않는다."**
모델 학습은 시작일 뿐이고, 재학습·배포·모니터링이 반복적으로 발생하며,
**모델 품질은 시간이 지나며 자연스럽게 하락**한다. 사람 손으로 관리할 수 없는 양이 된다.

## DevOps와 무엇이 다른가

| DevOps | MLOps |
|---|---|
| 코드만 관리 | **데이터 버전 + 모델 버전**이 함께 중요 |
| 결과물 = 빌드된 애플리케이션 | **모델 자체가 결과물** |
| 성능 기준이 고정 | **성능 기준이 고정되지 않음** |
| 배포하면 그대로 동작 | **시간이 지나면 자연스럽게 품질이 떨어짐** |

차이는 "관리 대상이 하나 늘었다"가 아니다. **결과물이 확률적이고 기준선이 움직인다**는 성질 자체가
다르다. 그래서 [[Data and model versioning]]의 재현성 3요소(스냅샷·환경·시드)가 필수가 되고,
CI/CD만으로는 부족해 **CT(Continuous Training)** 가 붙는다.

## Machine Learning Life Cycle — 6단계

Chip Huyen, *Designing Machine Learning Systems* Fig 2-2. **원형으로 순환하고, 인접하지 않은
단계끼리도 이어진다** — 일방향 파이프라인이 아니다.

```
1. Project scoping ──────────→ 2. Data engineering
        ↑                              ↓
6. Business analysis          3. ML model development
        ↑                              ↓
5. Monitoring & continual ←──── 4. Deployment
   learning
   (모든 단계가 점선으로 상호 연결)
```

| 단계 | 한 문장 | 여기서 결정되는 것 |
|---|---|---|
| **1. Project Scoping** | 문제 정의가 전체 시스템을 결정한다 | **성공 지표를 accuracy가 아닌 business metric으로.** 온라인 추론인가 배치 예측인가, 실시간이 필요한가, 데이터에 접근 가능한가 |
| **2. Data Engineering** | 모델 성능의 대부분은 데이터에서 결정된다 | 수집·정제·Feature 생성, 학습 데이터셋 구성, [[Feature store]] 설계, **학습/추론 정합성** → [[ML data pipeline]] |
| **3. ML Model Development** | 모델 개발은 반복 실험의 연속 | 아키텍처·하이퍼파라미터, 모델 아티팩트 저장, 실험 메타데이터 |
| **4. Deployment** | 모델이 실제 서비스가 되는 지점 | **Batch vs Online 서빙**, GPU 사용 여부, 트래픽 처리, **롤백 전략** → [[Batch and online serving]] |
| **5. Monitoring & Continual Learning** | 모델은 시간이 지나면 망가진다 | Drift 감지 → 재학습 트리거 → 자동 검증 → [[Data drift and training-serving skew]] |
| **6. Business Analysis** | 모델 성능보다 중요한 것은 비즈니스 효과 | **예측 정확도와 실제 매출은 다를 수 있다.** KPI 영향 분석 → 1번 재조정 |

**1번과 6번이 짝을 이루는 것이 이 그림의 설계다.** scoping에서 성공을 business metric으로 정의했기
때문에 6번에서 그 지표로 되돌아가 scoping을 고칠 수 있다. accuracy로 정의했다면 루프가 닫히지 않는다.

**루프의 실행 형태**가 [[Data drift and training-serving skew]]의 "Self-Healing MLOps 5단계"
(수집 → 학습 → 평가 → 배포 → 관측성)다. 즉 그 5단계는 여기 **5번 단계의 내부**에 해당한다.

## 데이터 엔지니어가 책임지는 영역

- 데이터 파이프라인 설계 → [[ML data pipeline]]
- [[Feature store]] 운영
- 학습/추론 데이터 일관성 → [[Data drift and training-serving skew]]
- **GPU 사용 흐름 설계** → [[Inference optimization]]
- 자동 재학습 파이프라인 구축

> 다섯 중 넷은 데이터의 문제지만 **다섯 번째는 연산 자원의 문제**다. AI 시대의 DE가 데이터의
> 이동뿐 아니라 **연산의 배치**까지 설계 대상으로 삼는다는 신호. → [[AI data engineering]]

## 확장 — AI Engineering과 LLMOps

강의는 관리 대상이 **모델 → 제품 → 생성 시스템**으로 이동한다고 본다.

| | 중심 | 핵심 자산 | 핵심 문제 |
|---|---|---|---|
| **MLOps** | 모델 | 학습 데이터셋, 피처, 모델 아티팩트 | 재학습, 드리프트, 서빙 안정화 |
| **AI Engineering** | 제품 | 모델 + 파이프라인 + 서빙 + 관측/평가 + 비용 | 제품화(UX), 운영 안정성, 비용, 안전 |
| **LLMOps** | 생성 시스템 | **프롬프트**, 컨텍스트 파이프라인, 지식베이스 | 품질 평가/통제, 토큰 비용, 안전, 지식 최신성 |

상세는 [[LLMOps]].

## 열린 질문

- **MLOps 성숙도 모델** — 강의는 "체계가 필요하다"까지만 말하고, 어느 수준부터 무엇을 도입할지의
  단계 구분을 주지 않는다. (Google의 MLOps level 0/1/2 같은 프레임이 있는 것으로 알려져 있으나
  이 위키에 근거 자료가 없다.)
- **CT(Continuous Training)의 실제 운영 비용** — 자동 재학습이 얼마나 자주 돌아야 하는지,
  쿨다운을 어떻게 잡는지의 근거가 없다.

## 링크

- 라이프사이클 각 단계: [[ML data pipeline]] · [[Batch and online serving]] ·
  [[Data drift and training-serving skew]] · [[Feature store]] · [[Data and model versioning]]
- LLM 시대의 확장: [[LLMOps]] · [[Context engineering]]
- 직무 맥락: [[AI data engineering]]
- 출처: [[AI DE Course - Part2 Ch2 MLOps and the ML lifecycle]]

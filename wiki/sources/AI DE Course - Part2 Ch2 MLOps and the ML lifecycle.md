---
type: source
title: AI DE Course - Part2 Ch2 MLOps and the ML lifecycle
area: [data-engineering]
aliases: [Part2 Ch2-1,2, MLOps의 핵심 개념과 생애주기]
tags: [data-engineering, course, fast-campus, mlops, devops, lifecycle]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part2/02. Ch2. MLOps와 LLMOps.pdf"]
---

# AI DE Course - Part2 Ch2 MLOps and the ML lifecycle

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 2 Ch2** "MLOps와 LLMOps"의
소단원 **1·2** "MLOps의 핵심 개념과 생애주기 (1)(2)". 강사 **Habi**. 원본(로컬):
`raw/data-engineering/ai-de-course/part2/02. Ch2. MLOps와 LLMOps.pdf` **p1–18**. 강의 홈:
[[AI Data Engineering (Fast Campus course)]].

같은 PDF의 p19–33(LLMOps)은 [[AI DE Course - Part2 Ch2 LLMOps]]로 분리했다.

**이 두 소단원이 위키에 MLOps라는 개념 페이지를 처음 세우게 한다.** Part 1은 MLOps를 "drift 대응"
맥락으로만 언급했지 정의하지 않았다. → [[MLOps]]

## 논지 — "모델은 만들어졌지만, 서비스는 자동으로 되지 않는다"

MLOps 필요성의 논증이 다섯 줄이다. 마지막 줄이 결론이다.

1. 모델 학습은 시작일 뿐이다
2. 실제 서비스까지는 많은 수작업이 존재
3. 재학습·배포·모니터링이 **반복적으로** 발생
4. **모델 품질은 시간이 지나며 자연스럽게 하락**
5. → 이 과정을 사람 손으로 관리하는 것은 불가능

4번은 Part 1의 [[Data drift and training-serving skew]]("모델에도 유통기한이 있다")와 같은
문장이다. **Part 1은 이 사실에서 "재학습 트리거"를 뽑았고, Part 2는 같은 사실에서 "체계(MLOps)"를
뽑는다.**

**MLOps의 정의(강의):** ML 시스템을 **운영 가능한 형태로 만드는 체계**. 모델 개발과 서비스 운영을
연결하는 프레임워크 — 데이터·모델·인프라·배포를 하나의 흐름으로 관리하고, 반복 가능한 학습
파이프라인과 안정적 추론 서비스, 성능 저하 감지를 통한 자동 재학습을 갖춘다.

## DevOps와 무엇이 다른가

| DevOps | MLOps |
|---|---|
| 코드만 관리 | **데이터 버전 + 모델 버전**이 함께 중요 |
| 결과물 = 빌드된 애플리케이션 | **모델 자체가 결과물** |
| 성능 기준이 고정 | **성능 기준이 고정되지 않음** |
| 배포하면 그대로 동작 | **시간이 지나면 자연스럽게 품질이 떨어짐** |

> 강의 표현: **"더 복잡한 MLOps."** 축이 하나(코드) 늘어난 게 아니라, *결과물이 확률적이고
> 기준선이 움직인다*는 성질 자체가 다르다.

이 표가 [[Data and model versioning]]의 "재현성 3요소"와 맞물린다 — DevOps가 코드 커밋 하나로
재현되는 데 반해 MLOps는 데이터 스냅샷·환경·시드를 함께 묶어야 한다.

## Machine Learning Life Cycle — 6단계

강의는 **Chip Huyen, *Designing Machine Learning Systems* 의 Figure 2-2**를 그대로 인용한다
(출처가 슬라이드에 표기된 몇 안 되는 자료다). 6단계가 **원형으로 순환**하고, 인접하지 않은 단계끼리도
점선으로 이어져 **어느 단계에서든 앞으로 되돌아간다**는 것이 그림의 요지다.

```
1. Project scoping → 2. Data engineering → 3. ML model development
        ↑                                            ↓
6. Business analysis ← 5. Monitoring & continual ← 4. Deployment
                          learning
   (모든 단계가 점선으로 상호 연결 — 일방향 파이프라인이 아니다)
```

| 단계 | 핵심 문장 | 결정하는 것 |
|---|---|---|
| **1. Project Scoping** | "문제 정의가 전체 시스템을 결정한다" | 비즈니스 문제 명확화, **성공 지표를 accuracy가 아닌 business metric으로**, 온라인 추론인지 배치 예측인지, 실시간 요구 여부, 데이터 접근 가능성 |
| **2. Data Engineering** | "모델 성능의 대부분은 데이터에서 결정" | Raw 수집·정제·Feature 생성, 학습 데이터셋 구성, [[Feature store]] 설계, **학습/추론 데이터 정합성 유지** |
| **3. ML Model Development** | "모델 개발은 반복 실험의 연속" | 아키텍처 시도, 하이퍼파라미터 튜닝, 학습 결과 비교, **모델 아티팩트 저장**, 실험 메타데이터 |
| **4. Deployment** | "모델이 실제 서비스가 되는 지점" | **Batch Serving vs Online Serving**, GPU 사용 여부, 트래픽 처리, **모델 롤백 전략**, 배포 자동화 |
| **5. Monitoring & Continual Learning** | "모델은 시간이 지나면 망가진다" | Data Drift, Model Drift, 이상값 증가 → **Drift 감지·재학습 트리거·자동 검증** |
| **6. Business Analysis** | "모델 성능보다 중요한 것은 비즈니스 효과" | **예측 정확도와 실제 매출은 다를 수 있음**, KPI 영향 분석, 사용자 행동 변화 → 결과에 따라 1번 재조정 |

> **1번과 6번이 짝을 이루는 게 이 그림의 설계다.** scoping에서 "accuracy 말고 business metric"으로
> 성공을 정의했기 때문에, 6번에서 그 지표로 되돌아가 scoping을 고칠 수 있다. accuracy로 정의했다면
> 루프가 닫히지 않는다.

**4번의 "Batch Serving vs Online Serving"이 Ch3·Ch4 전체의 씨앗**이다 →
[[Batch and online serving]].

## 데이터 엔지니어 관점에서의 MLOps

강의가 6단계 중 DE의 지분을 따로 뽑는다.

- 데이터 파이프라인 설계
- [[Feature store]] 운영
- 학습/추론 데이터 일관성
- **GPU 사용 흐름 설계**
- 자동 재학습 파이프라인 구축

> 5개 중 4개가 Part 1에서 이미 다뤄졌고, **새로운 건 "GPU 사용 흐름 설계"** 하나다. Part 2가
> DE의 책임 범위에 **연산 자원 배치**를 새로 넣는다는 신호다 →
> [[AI DE Course - Part2 Ch4 CPU and GPU inference]].

## 기존 페이지와의 대조

- **보강** — [[Data drift and training-serving skew]]의 "Self-Healing MLOps 5단계"가 여기 6단계
  라이프사이클의 **5번 단계 내부**에 해당한다는 게 이제 보인다. Part 1은 재학습 루프만 확대해
  보여줬고, Part 2가 그 루프가 놓인 전체 그림을 준다.
- **신규** — DevOps vs MLOps 대조, 6단계 라이프사이클은 위키에 없던 골격이다 → [[MLOps]].
- **일치** — "모델 품질은 시간이 지나면 하락한다"는 Part 1과 같은 전제.

## 인용 자료

- Chip Huyen, *Designing Machine Learning Systems* (O'Reilly), Figure 2-2 — ML 시스템 개발 사이클.
  **이 코스에서 원저자·도서명이 표기된 드문 인용이다.** 1차 자료 인제스트 후보.
- Databricks "MLOps Cycle" 인포그래픽 (Data Prep → EDA → Develop → (Re-)Train → Review →
  Deploy → Inference → Monitor 무한대 기호).

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[MLOps]] (상세) · [[Data and model versioning]] · [[Feature store]] ·
  [[Data drift and training-serving skew]] · [[Batch and online serving]]
- 앞 챕터: [[AI DE Course - Part2 Ch1 Pipeline evolution and the DE role]]
- 다음: [[AI DE Course - Part2 Ch2 LLMOps]]

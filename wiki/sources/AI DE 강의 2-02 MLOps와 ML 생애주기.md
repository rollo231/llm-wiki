---
type: source
title: AI DE 강의 2-02 MLOps와 ML 생애주기
aliases: [AI DE 2-02]
tags: [AI-DE-강의, MLOps, 운영]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/data-engineering/ai-de-course/part2/02. Ch2. MLOps와 LLMOps.pdf"
---

# AI DE 강의 2-02 MLOps와 ML 생애주기

[[AI 데이터 엔지니어링 강의]] Part 2의 두 번째 강의. Ch2 덱의 소단원 1·2("MLOps의 핵심 개념과 생애주기 1·2")를 한
페이지로 묶었다. (1) MLOps의 필요성과 정의, DevOps와의 차이, (2) ML 라이프사이클 6단계와 데이터 엔지니어의 책임.
같은 덱의 소단원 3은 [[AI DE 강의 2-03 LLMOps]]에 있다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 2 「AI 학습/추론 중심 데이터 파이프라인 설계」 |
| 덱 제목 | Ch2. MLOps와 LLMOps — 1. MLOps의 핵심 개념과 생애주기 1 · 2. MLOps의 핵심 개념과 생애주기 2 |
| 원본 파일 | `part2/02. Ch2. MLOps와 LLMOps.pdf` (33p 중 p1–17, 17p) — 소단원 1: p1–7, 소단원 2: p8–17 |
| 강사 | Habi (슬라이드 표기, Ch1 p2) |
| 작성 시기 | PDF 생성일 2026-03-05 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명의 `Ch2`, 소단원 번호(1·2)는 표지 슬라이드 |
| 인용 도서 | 라이프사이클 그림과 단계 슬라이드에 "Designing Machine Learning Systems" 표기 → [[Designing Machine Learning Systems]] |

## 요약

### (1) MLOps의 핵심 개념과 생애주기 1

- **필요성(p3)** — "모델은 만들어졌지만, 서비스는 자동으로 되지 않는다." 학습은 시작일 뿐이고, 실서비스까지 수작업이
  많으며, 재학습·배포·모니터링이 반복되고, 모델 품질은 시간이 지나며 자연스럽게 떨어진다. 사람 손으로는 관리 불가.
- **정의(p4)** — ML 시스템을 운영 가능한 형태로 만드는 체계. 모델 개발과 서비스 운영을 잇는 프레임워크로 데이터·모델·
  인프라·배포를 하나의 흐름으로 관리한다. 반복 가능한 학습 파이프라인, 안정적인 추론 서비스, 성능 저하 감지를 통한
  자동 재학습.
- **DevOps와 MLOps의 차이(p5)** — "더 복잡한 MLOps"
  - 코드만 관리하지 않는다 — 데이터 버전·모델 버전이 중요하고, 모델 자체가 결과물이다.
  - 성능 기준이 고정되지 않는다 — 시간이 지나면 자연스럽게 품질이 떨어진다.
- **ML 라이프사이클(p6–7)** — 데이터 수집부터 배포·유지보수까지 이어지는 반복 프로세스, "데이터에서 가치로 이어지는
  선순환". 데이터는 계속 변한다(Garbage In, Garbage Out), 성능을 지속 확인하는 피드백 루프, 단순 모델 개발이 아닌
  프로덕션 시스템. 그림은 DMLS Figure 2-2 — "The process of developing an ML system looks more like a cycle with a lot
  of back and forth between steps."

### (2) MLOps의 핵심 개념과 생애주기 2 — 6단계

그림(p10): 1 → 2 → 3 → 4 → 5 → 6 → 1 로 도는 실선 순환에, 2·3·5·6 사이를 오가는 **점선 양방향 화살표**가 겹쳐 있다.

| 단계 | 슬라이드 제목 | 내용 |
|---|---|---|
| 1. Project Scoping | 문제 정의가 전체 시스템을 결정한다 | 비즈니스 문제 명확화, 성공 지표 정의(accuracy가 아닌 business metric), 온라인 추론 vs 배치 예측 결정, 실시간 요구 여부, 데이터 접근 가능성 |
| 2. Data Engineering | 모델 성능의 대부분은 데이터에서 결정 | Raw 수집·정제·Feature 생성, 학습 데이터셋 구성, Feature Store 설계, 학습/추론 데이터 정합성. DE 핵심 역할: 안정적인 파이프라인, 재현 가능한 데이터 버전 관리 |
| 3. ML Model Development | 모델 개발은 반복 실험의 연속 | 여러 아키텍처 시도, 하이퍼파라미터 튜닝, 결과 비교, 모델 아티팩트 저장, 실험 메타데이터 관리 |
| 4. Deployment | 모델이 실제 서비스가 되는 지점 | Batch Serving vs Online Serving, GPU 사용 여부, 트래픽 처리 방식, 모델 롤백 전략, 배포 자동화 필수 |
| 5. Monitoring & Continual Learning | 모델은 시간이 지나면 망가진다 | 입력 분포 변화(Data Drift), 예측 성능 저하(Model Drift)·이상값 증가, 실시간 품질 모니터링. 운영 핵심: Drift 감지, 재학습 트리거, 자동 검증 |
| 6. Business Analysis | 모델 성능보다 중요한 것은 비즈니스 효과 | 예측 정확도와 실제 매출은 다를 수 있음, 모델 개선이 KPI에 미치는 영향, 사용자 행동 변화 확인, 결과에 따라 Project Scoping 재조정 |

- **데이터 엔지니어 관점의 MLOps(p17)** — DE가 책임지는 영역: 데이터 파이프라인 설계, Feature Store 운영, 학습/추론
  데이터 일관성, GPU 사용 흐름 설계, 자동 재학습 파이프라인 구축.

## 핵심

- **라이프사이클은 파이프라인이 아니라 순환이다.** 성공 지표를 accuracy가 아닌 비즈니스 지표로 잡는 1단계와, 그 지표로
  돌아가 문제 정의를 고치는 6단계가 고리를 닫는다. 그림의 점선 화살표가 말하는 것은 "단계를 끝내고 넘어가는" 흐름이
  아니라 **어느 단계에서든 앞 단계로 되돌아간다**는 것이다. → [[MLOps]]
- **DE의 몫은 2단계에 그치지 않는다** — p17의 DE 책임 목록(Feature Store 운영·학습/추론 데이터 일관성·자동 재학습)은
  2~5단계를 가로지른다. *(위키의 관찰)* → [[MLOps]]
- **1단계에서 서빙 방식이 정해진다** — "온라인 추론인지 배치 예측인지"를 문제 정의 단계에서 결정하라는 것은, 서빙 방식이
  모델이 아니라 요구사항의 문제라는 뜻이다. 같은 주장이 [[AI DE 강의 2-07 Batch vs Online 서빙 아키텍처]]의 "서빙 방식은
  모델 문제가 아니라 시스템 선택"으로 이어진다. → [[모델 서빙]]
- **"Model Drift"라는 용어** — p15는 입력 분포 변화를 Data Drift, **예측 성능 저하를 Model Drift**라고 부른다. Part 1
  [[AI DE 강의 1-13 Skew와 Drift]]는 원인 쪽으로 Data Drift(P(X) 변화)와 Concept Drift(P(Y|X) 변화)를 나눴고 "model
  drift"라는 말은 쓰지 않았다. 두 분류는 축이 다르다 — Part 1은 **무엇이 바뀌었나**, 이 슬라이드는 **무엇으로
  관측되나**(입력 vs 성능). → [[데이터 드리프트]]
- Part 1의 Self-Healing 파이프라인 5단계는 이 6단계 중 2~5단계를 자동화한 고리이고, Part 1에 없던 것은 양 끝(1·6단계)이다.
  *(위키의 관찰)* → [[MLOps]]

## 주의·결함

- **p15 소제목 "모델이 실제 서비스가 되는 지점"은 p14(Deployment)의 소제목을 복사한 것**이다. p15의 실제 주제는
  "모델은 시간이 지나면 망가진다".
- **Ch2 전체 슬라이드 머리글이 "2. AI 시대를 위한 파이프라인과 데이터엔지니어의 진화방향"이다** — Ch1 소단원 2의 제목이
  템플릿에 남은 것.
- **라이프사이클 그림의 출처 표기가 책 제목뿐이다** — 저자·출판사·그림 번호는 슬라이드 문구로 밝히지 않았다(그림 캡션
  이미지에 "Figure 2-2"가 보일 뿐). 책은 Chip Huyen, O'Reilly 2022. 여섯 단계 이름은 저자의 Stanford CS 329S 강의 노트와
  일치한다 — "Step 1. Project scoping … Step 2. Data engineering … Step 3. ML model development … Step 4. Deployment …
  Step 5. Monitoring and continual learning … Step 6. Business analysis" [CS 329S Lecture 1 노트,
  https://docs.google.com/document/d/1C3dlLmFdYHJmACVkz99lSTUPF4XQbWb_Ah7mPE12Igo , 2026-09-14 확인]. 단계 슬라이드(p11–17)에도 같은 책 제목이 워터마크처럼 붙어 있어 어디까지가 책의
  내용이고 어디부터가 강사의 정리인지 구분되지 않는다. → [[Designing Machine Learning Systems]]
- p6의 "데이터는 계속 변화하고 있다, Garbage In Garbage Out"은 서로 다른 두 문제(분포 변화, 입력 품질)를 한 줄에
  묶었다.
- 각 단계가 bullet 목록이라 **단계 사이의 인계물(무엇이 넘어가나)**은 없다 — 예: 3단계가 4단계에 넘기는 아티팩트·
  메타데이터, 5단계가 2단계에 되돌리는 트리거의 형태.

## 관련

- 개념: [[MLOps]] · [[모델 서빙]] · [[피처 스토어]] · [[데이터 드리프트]] · [[학습-서빙 스큐]] · [[데이터와 모델 버전 관리]]
- 도서: [[Designing Machine Learning Systems]]
- 이전 강의: [[AI DE 강의 2-01 데이터 파이프라인의 진화와 데이터 엔지니어]]
- 다음 강의: [[AI DE 강의 2-03 LLMOps]]

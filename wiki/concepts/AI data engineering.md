---
type: concept
title: AI data engineering
area: [data-engineering]
aliases: [AI DE, AI를 위한 데이터 엔지니어링, 모델 지원 데이터 엔지니어링]
tags: [data-engineering, machine-learning, unstructured-data]
created: 2026-07-19
updated: 2026-07-28
sources: ["raw/data-engineering/ch01-1-de-vs-ai-de-ot.pdf", "https://sinja.io/blog/data-landscape-guide-for-developers"]
---

# AI data engineering

AI 모델의 **학습과 추론을 지원**하는 데이터 엔지니어링. 정형 데이터·DW·BI 중심의
[[Traditional data engineering]]에서 확장된 형태로, 비정형 데이터와 모델 라이프사이클을 다룬다.
처음 등장: [[AI DE Course - Ch1-1 OT]].

## 핵심 역할

- **모델 학습 지원**: 고품질 학습 데이터 준비·버전 관리, 학습 파이프라인 자동화·실험 관리,
  GPU 리소스 할당·학습 스케줄링 최적화.
- **추론 지원**: 모델 서빙 환경 구축·응답 속도(latency) 최적화, 비용 효율 인프라·오토스케일링,
  성능 모니터링·결과 로깅.
- **비정형 데이터**: 이미지·오디오·비디오·텍스트를 딥러닝이 이해하는 텐서(tensor)로 변환,
  대용량 비정형 데이터의 효율적 저장·검색.

## 왜 지금

- 데이터의 ~80%가 비정형(예: Instagram·YouTube).
- 실시간 수요 증가(예: YouTube·Coupang).

## 한 줄

비정형 데이터까지 다루며 AI 모델이 잘 학습·추론하도록 돕는 **시스템 건축가**.

## 다른 축의 분류

[[Data landscape guide for developers]]는 데이터 직군을 **동시에 존재하는 네 유형**으로 본다
(analytical / scientific / engineering / **machine learning**). 이 페이지의 "AI DE"에 대응하는 것은
**machine learning type**인데, 프레이밍이 정면으로 갈린다:

- **이 페이지(강의) — 시간축.** AI DE는 [[Traditional data engineering]]이 **확장·진화한 형태**다.
  같은 직무가 변한다.
- **저 글 — 공존축.** ML type은 "앞의 유형들과 겹쳐 보이지만 **도구셋이 아주 달라서**" 갈라지는
  **별개 직군**이다. 네 직군이 한 회사에 동시에 있다.

충돌하는 것은 결론이 아니라 **축**이다. 어느 쪽이 현업의 실제 모습인지는 아직 근거가 없다 —
둘 다 1차 자료 없는 개괄이다. → [[Data Engineering]] MOC의 열린 질문.

**무게 차이 주의:** 저 글의 저자는 ML에 대한 자기 지식이 제한적이라고 밝히고 본문에서 ML을 다루지
않는다("we won't be covering ML-related topics in this article"). ML 쪽 서술의 근거는 강의 쪽이
더 두껍다.

## 링크

- 대비: [[Traditional data engineering]]
- 다른 축: [[Data landscape guide for developers]]
- 출처: [[AI DE Course - Ch1-1 OT]]

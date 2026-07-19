---
type: concept
title: AI data engineering
area: [data-engineering]
aliases: [AI DE, AI를 위한 데이터 엔지니어링, 모델 지원 데이터 엔지니어링]
tags: [data-engineering, machine-learning, unstructured-data]
created: 2026-07-19
updated: 2026-07-19
sources: [raw/data-engineering/ch01-1-de-vs-ai-de-ot.pdf]
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

## 링크

- 대비: [[Traditional data engineering]]
- 출처: [[AI DE Course - Ch1-1 OT]]

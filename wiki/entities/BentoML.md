---
type: entity
title: BentoML
aliases: [Bento, Yatai]
tags: [서빙, 도구, 모델 서버]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "[[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]"
  - "[[AI DE 강의 2-07 Batch vs Online 서빙 아키텍처]]"
---

# BentoML

모델 패키징과 서빙을 묶은 **Python ML 서빙 프레임워크.** 강의는 "FastAPI + ML 기능을 결합한 구조"로 소개한다.

## 구조 (강의의 설명 — BentoML 1.1 이전 구조)

| 구성 | 역할 |
|---|---|
| API Server | 비동기 요청 수신, Pydantic 검증, 비즈니스 로직 (CPU·I/O bound) |
| Runner | 모델을 로드해 추론하는 독립 프로세스, 모델별 전·후처리 (GPU·CPU bound) |
| Adaptive Batching | Runner가 개별 요청을 런타임에 모아 배치 연산 |
| Bento | 모델·코드·의존성·설정을 묶은 배포 단위, `bentofile.yaml` → `bento build` → Docker 이미지 |
| Yatai | Bento를 Kubernetes에 배포·관리 |

API 서버와 Runner를 **따로 확장**하는 것이 핵심 이점이다.

## 강의의 평가

- **장점** — 패키징·버전 관리 내장, 여러 프레임워크 지원, 비교적 낮은 진입 장벽.
- **제약** — 대규모 트래픽의 성능 튜닝은 추가 설계 필요, 추상화가 늘수록 내부 이해 필요.

## 현재 상태

- **Runner는 레거시다** — BentoML 1.2(2024-02-19)부터 서비스를 클래스로 정의하는 Services API가 기본이다(하위 호환 유지).
  [https://docs.bentoml.com/en/latest/build-with-bentoml/services.html — "Runners are a legacy concept in BentoML 1.1",
  2026-09-14 확인]
- `bentofile.yaml`은 지원되지만 v1.3.20부터 Python SDK 방식이 권장된다. [https://docs.bentoml.com/en/latest/reference/bentoml/bento-build-options.html
  — "we recommend using the new Python SDK", 2026-09-14 확인]
- **Yatai는 보관 처리됐다**(2026-06-11) — 마지막 릴리스 v1.1.13(2023-10-09)로 1.2 이상을 지원한 적이 없다.
  [https://github.com/bentoml/Yatai — "⚠️ Yatai for BentoML 1.2 is currently under construction.", 2026-09-14 확인]
- BentoML 자체는 활발하다(v1.4.39, 2026-05-07). Adaptive Batching은 현행 기능이다.

세부 검증: [[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]

## 관련

- [[모델 서빙]] · [[추론 최적화]] · [[데이터와 모델 버전 관리]] · [[FastAPI]] · [[TorchServe]] · [[Triton Inference Server]]

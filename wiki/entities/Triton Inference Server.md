---
type: entity
title: Triton Inference Server
aliases: [Triton, NVIDIA Triton, NVIDIA Triton Inference Server, Dynamo-Triton, NVIDIA Dynamo-Triton]
tags: [서빙, 도구, 추론 엔진, GPU]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "[[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]"
  - "[[AI DE 강의 2-07 Batch vs Online 서빙 아키텍처]]"
---

# Triton Inference Server

NVIDIA의 오픈소스 **모델 서버(추론 서빙 소프트웨어).** 여러 프레임워크 모델을 한 서버에서 GPU 효율 위주로 스케줄링하고,
실제 연산은 TensorRT·ONNX Runtime·PyTorch 같은 **백엔드**에 맡긴다. → [[모델 서빙]]의 "서빙 플랫폼의 층"
NVIDIA 제품 페이지는 이제 "NVIDIA Dynamo-Triton"이라는 이름을 쓴다.

## 구조 (강의의 설명)

| 구성 | 역할 |
|---|---|
| HTTP/gRPC 엔드포인트 | 추론 요청 전달만 — 검증·라우팅·인증을 하지 않는다 |
| Model Repository | 숫자 버전 디렉터리, 동적 로드·언로드 |
| Per-Model Scheduler Queues | 모델별 대기열, Dynamic Batching · Sequence Batching |
| Framework Backends | TensorRT · TensorFlow · PyTorch · ONNX · Custom, 같은 GPU에서 동시 실행 |
| Metrics | Liveness/Readiness, 지연·처리량을 Prometheus 등으로 |

그 밖에 Shared Memory(대용량 입력 복사 비용 절감), Model Ensemble(전처리~여러 모델을 서버 내부 DAG로).

## 강의의 평가

- **장점** — 매우 높은 성능, 동적 배치·멀티 모델·GPU 최적화, 다양한 프레임워크.
- **제약** — 진입 장벽 높음, 운영 복잡도 높음, "비즈니스 로직 직접 구현 불가".
- 비교표: 추상화 매우 높음 · 성능 매우 우수 · GPU 최적화 · 운영 난이도 높음 · 확장성 매우 우수.

## 현재 상태

- ❌ **비즈니스 로직은 구현할 수 있다** — Python 백엔드, BLS(Business Logic Scripting), 앙상블 모델.
  [https://github.com/triton-inference-server/python_backend — "The goal of Python backend is to let you serve models written
  in Python by Triton Inference Server without having to write any C++ code.", 2026-09-14 확인]
- ⚠️ 런타임 모델 로드·언로드는 모델 제어 모드 EXPLICIT·POLL에서만 된다(기본 NONE).
  [https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_management.md , 2026-09-14 확인]
- 이름: [https://developer.nvidia.com/dynamo-triton — "NVIDIA Dynamo-Triton, formerly NVIDIA Triton Inference Server",
  2026-09-14 확인]. 개명 날짜는 1차 자료로 확인하지 못했다. GitHub·문서는 여전히 Triton Inference Server라는 이름을 쓰고,
  프로젝트는 활발하다(v2.72.0, 2026-08-31).

세부 검증: [[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]

## 관련

- [[모델 서빙]] · [[추론 최적화]](동적 배칭) · [[ONNX]](백엔드 중 하나) · [[지연 시간과 처리량]] · [[TorchServe]] · [[BentoML]] · [[FastAPI]]

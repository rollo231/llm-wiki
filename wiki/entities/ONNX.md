---
type: entity
title: ONNX
aliases: [Open Neural Network Exchange, ONNX Runtime, ORT]
tags: [서빙, 도구, 포맷]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "[[AI DE 강의 2-09 서빙의 CPU·GPU 가속]]"
---

# ONNX

**ONNX(Open Neural Network Exchange)** 는 딥러닝 모델을 프레임워크와 무관한 연산 그래프로 저장하는 표준 포맷이고,
**ONNX Runtime(ORT)** 은 그 그래프를 추론 전용으로 실행하는 엔진이다. 강의는 둘을 함께 "GPU 이전에 해야 할 CPU
최적화"의 런타임 수준 수단으로 소개한다([[AI DE 강의 2-09 서빙의 CPU·GPU 가속]]).

## ONNX — 포맷

- PyTorch·TensorFlow·Scikit-learn은 실행 엔진과 연산 방식이 제각각이다. ONNX는 **모델 구조 + 연산 그래프를 표준화한 중간
  표현**이다.
- 쓰임새(강의의 예): TensorFlow 모델을 배포해 둔 뒤 PyTorch 모델 배포 요청이 오거나, 여러 프레임워크 모델이 섞여 있을 때
  ONNX로 변환해 **서빙 쪽을 하나로** 맞춘다.
- 모델을 프레임워크 코드가 아니라 **데이터 자산(그래프 파일)** 으로 다룬다는 점에서 [[Triton Inference Server]]의 모델
  저장소 발상과 같은 방향이다. *(위키의 연결)*

## ONNX Runtime — 엔진

강의의 설명: 오직 추론만을 위한 C++ 기반 엔진으로 Python 오버헤드를 줄이고, 하드웨어에 맞게 그래프를 최적화해 실행한다.

| 기능 | 내용 | 확인된 사실 (2026-09-14) |
|---|---|---|
| 그래프 최적화 | 연속된 연산을 미리 분석해 합치고 불필요한 것은 제거 | 수준이 나뉜다 — **Basic**(의미 보존 재작성: Identity·Dropout 제거 등), **Extended**(복잡한 노드 결합), **Layout** 최적화 |
| 추론 전용 그래프 | Dropout·Grad 같은 학습용 연산 제거 | Dropout Elimination은 Basic 수준 ✅ |
| CPU 실행 | 강의: "AVX/AVX2/AVX-512 자동 활용, Intel MKL, OpenMP 기반 병렬 처리" | 기본 CPU 백엔드는 **MLAS**(AVX2·AVX-512·VNNI 경로)와 **자체 스레드 풀**. CPU 패키지는 v1.7.0(2021-03)부터 OpenMP 없이 빌드. oneDNN·OpenVINO는 별도 execution provider ⚠️ |
| 하드웨어 선택 | CPU Execution Provider | CPU 외에 GPU·가속기용 **execution provider**를 갈아 끼우는 구조 |

출처: [Graph optimizations https://onnxruntime.ai/docs/performance/model-optimizations/graph-optimizations.html ·
v1.7.0 릴리스 노트 "all ONNX Runtime CPU packages are now built without OpenMP"
https://github.com/microsoft/onnxruntime/releases/tag/v1.7.0 · Execution Providers
https://onnxruntime.ai/docs/execution-providers/ , 2026-09-14 확인]

## 양자화와 ORT

- 강의는 "ONNX Runtime INT8"을 CPU에서도 큰 효과가 있는 양자화의 예로 든다. → [[추론 최적화]]
- ORT 문서 기준으로 **FP16은 GPU 쪽** 최적화다("the CPU version of ONNX Runtime doesn't support float16 ops").
  **INT8의 CPU 이득은 모델과 하드웨어에 달려 있다** — VNNI가 있는 x86-64에서 유리하고, 오래된 장치에서는 오히려 느려질 수
  있다. [https://onnxruntime.ai/docs/performance/model-optimizations/float16.html ·
  https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html , 2026-09-14 확인]

## 서빙 스택에서의 위치

[[Triton Inference Server]]는 ONNX를 지원 프레임워크 백엔드 중 하나로 둔다([[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]).
즉 ONNX는 모델 서버와 경쟁하는 것이 아니라 **모델 서버 아래의 실행 계층**이다. *(위키의 정리)* → [[모델 서빙]]

## 빈칸

- 변환이 항상 되는 것은 아니다 — 지원되지 않는 연산자, 동적 shape, 변환 후 수치 차이 검증은 강의에 없다.
- 변환된 ONNX 파일도 학습된 모델과 **다른 아티팩트**이므로 버전·평가 대상이 된다. → [[데이터와 모델 버전 관리]] *(위키의 관찰)*

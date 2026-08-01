---
type: entity
title: ONNX
area: [data-engineering]
aliases:
  - Open Neural Network Exchange
  - ONNX Runtime
  - 오닉스
  - Operator fusion
tags: [data-engineering, mlops, inference, onnx, interoperability, cpu, optimization]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part2 Ch4 CPU and GPU inference]]"]
---

# ONNX

**Open Neural Network Exchange** — 딥러닝 모델을 **프레임워크 독립적인 그래프 표현**으로 저장하는
표준.

PyTorch·TensorFlow·Scikit-learn은 각자 다른 실행 엔진과 연산 방식을 갖는다.
ONNX는 **모델 구조 + 연산 그래프를 표준화한 중간 표현(통합 모델 포맷)**이다.

```
Caffe2 ┐                        ┌ ONNX Runtime
PyTorch│                        │ Caffe2
TensorFlow ├→ export to onnx →  ONNX  → load from onnx ─┼ PyTorch
Keras  │                        │ TensorFlow / Keras
MXNet  │                        │ MXNet
CNTK   ┘                        └ CNTK
```

**강의가 드는 상황:**

- TensorFlow로 개발·배포를 마쳤는데, 이후 PyTorch로 개발 요청이 들어온다
- TensorFlow·Keras·PyTorch 등을 **ONNX로 변환한 뒤 배포**한다

> 즉 ONNX가 파는 것은 **학습 프레임워크와 서빙 스택의 분리**다. 팀이 무엇으로 학습하든 서빙은
> 한 가지 방식으로 돌아간다. [[NVIDIA Triton Inference Server]]가 ONNX를 백엔드로 지원하는 이유이기도 하다.

## ONNX Runtime — 오직 추론만을 위한 엔진

고성능 추론 실행 엔진. ONNX 모델을 입력받아 **하드웨어에 맞게 최적화된 방식으로 실행**한다.
**C++ 기반 정적 실행, Python 오버헤드 최소화.**

**PyTorch/TensorFlow 기본 실행보다 빠른 경우가 다수** — 이유는 세 가지.

### 1. Graph-level Optimization — 연속된 연산을 하나로 묶음

> **"PyTorch는 실행할 때 연산을 하나씩 처리하는 반면"**, ONNX Runtime은 연산들을 **미리 분석**해
> 합칠 수 있는 건 합치고 불필요한 건 제거한다.

예시 (강의 인용 그림): `Conv → BatchNormalization → Clip` 반복 구조가
**`Conv(+bias) → Clip`** 으로 fusion 된다. BatchNorm의 scale/B/mean/var가 Conv의 가중치에
접혀 들어간다.

**이것이 operator fusion이다** — 연산 횟수가 줄 뿐 아니라 **중간 텐서를 메모리에 쓰고 다시 읽는
왕복이 사라진다.** 실제 이득의 상당 부분은 후자에서 온다.

### 2. 불필요한 연산 제거

**학습용 연산(Dropout, Grad 등) 제거 → 추론 전용 그래프 생성.**

> 학습 그래프를 그대로 서빙하면 쓰지도 않는 Dropout·gradient 경로를 **매 요청마다** 지나간다.

### 3. CPU 친화적 실행

- **AVX / AVX2 / AVX-512 자동 활용** (CPU의 SIMD 벡터 명령어)
- **Intel MKL, OpenMP 기반 병렬 처리**
- 연산 결합(Operator Fusion), 벡터화(SIMD), 멀티스레딩

## 서빙에서의 위치

**[[Inference optimization]]의 "GPU 이전에 해야 할 CPU 최적화" 중 런타임 층**을 담당한다.
모델 수준 최적화(Quantization·Pruning·Distillation)와 조합된다 —
특히 **ONNX Runtime INT8 양자화**가 강의가 드는 대표 예시다.

```
모델 수준: Quantization · Pruning · Distillation
런타임 수준: ONNX Runtime  ← 여기
그래도 부족하면: GPU
```

## 열린 질문

- **변환 실패 문제** — 커스텀 연산자·동적 shape 등 ONNX로 안 넘어가는 경우가 실무에서 흔한데
  강의가 다루지 않는다.
- **변환 후 수치 일치 검증** — 프레임워크와 ONNX Runtime의 출력이 미세하게 다를 수 있고, 이는
  [[Data drift and training-serving skew]]의 skew가 되는 경로다. 강의는 언급하지 않는다.
- **ONNX vs TensorRT** — 둘 다 [[NVIDIA Triton Inference Server]]의 백엔드로 나오지만 선택
  기준이 없다.
- **얼마나 빠른가** — "빠른 경우가 다수"까지만. 벤치마크 수치가 없다.

## 링크

- 상위: [[Inference optimization]]
- 백엔드로 쓰는 곳: [[NVIDIA Triton Inference Server]] · [[Model serving platforms]]
- 출처: [[AI DE Course - Part2 Ch4 CPU and GPU inference]]

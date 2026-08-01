---
type: source
title: AI DE Course - Part2 Ch4 CPU and GPU inference
area: [data-engineering]
aliases: [Part2 Ch4-4, 서빙 환경에서의 CPU GPU 가속 활용 방안]
tags: [data-engineering, course, fast-campus, gpu, inference, quantization, onnx, cost]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/Part2_Ch 4.pdf"]
---

# AI DE Course - Part2 Ch4 CPU and GPU inference

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 2 Ch4** "서빙 아키텍처 및
플랫폼"의 소단원 **4** "서빙 환경에서의 CPU/GPU 가속 활용 방안". 강사 **Habi**. 원본(로컬):
`raw/data-engineering/Part2_Ch 4.pdf` **p61–77**. 강의 홈:
[[AI Data Engineering (Fast Campus course)]].

**"GPU를 쓰지 마라"에 가까운 17페이지.** Part 2에서 가장 반직관적이고, 비용 감각이 가장 뚜렷한
소단원이다. → [[Inference optimization]]

## 논지 — "GPU는 해결책의 마지막 단계에 가깝다"

> **흔한 오해: CPU = 느림, GPU = 빠름.**
> **실제 현실: CPU 추론이 더 빠른 경우도 많다. GPU는 비용이 비싸고 운영 난이도가 높고,
> 작은 요청에는 오히려 불리한 면이 있다.**

### ⭐ Total Latency의 분해

```
Total Latency = 네트워크 + 직렬화 + 전/후처리 + 모델 추론 + 스케줄링
```

**"모델 추론이 병목이 아닌 경우가 매우 많다"** — 작은 모델 / 낮은 QPS / I/O 중심 서비스.
**→ 이 경우 GPU는 효과가 미미함.**

> **이 다섯 항목 분해가 이 소단원 전체의 근거다.** GPU는 다섯 항목 중 **하나**만 줄인다. 나머지
> 넷이 지배적이면 GPU를 붙여도 총 지연은 거의 그대로인데 비용만 몇 배가 된다.
> Part 1 [[Latency and throughput]]이 배치/스트림 문맥에서 말한 "물리적 오버헤드"의 서빙판이다.

## 언제 CPU로 충분한가

- 모델 크기가 작음 (수 MB ~ 수십 MB)
- **단건 요청 latency가 중요**
- QPS가 낮거나 중간 수준
- 모델이 **트리 계열 / 선형 모델 / 작은 NN**

**대표 예시:** 추천 후보 생성 · 이상치 탐지 · 피처 기반 분류 · 룰 + ML 혼합 서비스.

## 언제 GPU가 필요한가

- 모델이 크다 (CNN, Transformer, LLM)
- 연산이 행렬 중심이다
- **QPS가 충분히 높다**
- **배치 처리가 가능하다**

> **GPU의 본질: "빠른 단일 추론기가 아니라 병렬 연산을 전제로 한 처리 장치."**
> **⇒ 배치 없이는 GPU 이점이 거의 사라진다.**

**이 한 줄이 Ch4 전체를 관통한다.** 앞 소단원에서 TorchServe의 Request Batching, BentoML의
Adaptive Batching, Triton의 Dynamic Batching이 왜 하나같이 배치 기능을 자랑했는지가 여기서
설명된다 — **배치는 편의 기능이 아니라 GPU를 쓰기 위한 전제 조건**이다.
→ [[AI DE Course - Part2 Ch4 Serving platforms]]

## GPU 이전에 반드시 해야 할 CPU 최적화

### 모델 수준 최적화 3종

| | 하는 일 | 얻는 것 |
|---|---|---|
| **Quantization** | FP32 → **INT8 / FP16** 변환 | 연산량 감소 + **캐시 효율 증가**. **CPU에서도 큰 효과.** 예: ONNX Runtime INT8, OpenVINO |
| **Pruning** | 영향이 적은 weight 제거 | 모델 크기 감소, **메모리 접근 감소**. **실시간 서빙에서 특히 효과적** |
| **Knowledge Distillation** | 큰 모델(Teacher) → 작은 모델(Student)로 지식 이전 | **"서빙용 모델"을 따로 만드는 전략.** 정확도 손실 대비 latency 이득이 큼 |

> Quantization의 이득을 **"연산량 감소 + 캐시 효율"** 두 갈래로 나눈 게 정확하다. INT8이 FP32보다
> 4배 작으니 같은 캐시에 4배 더 들어간다 — CPU에서 효과가 큰 진짜 이유다.
>
> **Knowledge Distillation의 프레이밍이 특히 실용적이다** — "모델을 줄인다"가 아니라
> **"서빙용 모델을 따로 만든다"**. 학습용과 서빙용이 다른 모델일 수 있다는 것.

### 런타임 최적화 — ONNX Runtime

ONNX Runtime(CPU Execution Provider)은 **PyTorch/TensorFlow 기본 실행보다 빠른 경우 다수**.
Graph optimization, operator fusion 적용.

## ONNX와 ONNX Runtime

**ONNX (Open Neural Network Exchange)** — 딥러닝 모델을 **프레임워크 독립적인 그래프 표현**으로
저장하는 표준. PyTorch·TensorFlow·Scikit-learn은 각자 다른 실행 엔진과 연산 방식을 갖는데,
ONNX는 **모델 구조 + 연산 그래프를 표준화한 중간 표현(통합 모델 포맷)**이다.

강의가 드는 두 상황:
- TensorFlow로 개발·배포 완료 → 이후 PyTorch로 개발 요청이 들어옴
- TensorFlow·Keras·PyTorch 등을 **ONNX로 변환 후 배포**

**ONNX Runtime** — 고성능 추론 실행 엔진, **오직 추론만을 위한 엔진**. ONNX 모델을 입력받아
하드웨어에 맞게 최적화된 방식으로 실행. **C++ 기반 정적 실행, Python 오버헤드 최소화.**

CPU 기준 3가지 최적화:

1. **Graph-level Optimization** — 연속된 연산을 하나로 묶음.
   **"PyTorch는 실행할 때 연산을 하나씩 처리하는 반면"**, ONNX Runtime은 미리 분석해 합칠 수 있는
   건 합치고 불필요한 건 제거. (그림: Conv+BatchNorm+Clip 반복 → Conv+Clip 로 fusion)
2. **불필요한 연산 제거** — 학습용 연산(Dropout, Grad 등) 제거 → **추론 전용 그래프 생성**
3. **CPU 친화적 실행** — **AVX / AVX2 / AVX-512 자동 활용**, Intel MKL·OpenMP 기반 병렬 처리

> **"학습용 연산을 제거한 추론 전용 그래프"**가 핵심이다. 학습 그래프를 그대로 서빙하면 쓰지도
> 않는 Dropout·gradient 경로를 매 요청마다 지나간다. → [[ONNX]]

## ⭐ CPU에서 GPU로 — 전환 판단 체크리스트

> 1. **CPU 최적화는 이미 완료되었는가?**
> 2. **추론 연산이 전체 latency의 대부분인가?**
> 3. **배치 처리가 가능한가?**
> 4. **GPU 비용 대비 효과가 명확한가?**

**GPU로 전환을 고려할 상황:**

- 모델 자체가 큰 경우 — Transformer 계열, LLM, 대형 CV 모델
- **단일 추론 latency가 SLA를 못 맞추는 경우** — CPU 최적화 이후에도 부족
- **QPS가 높아 수평 확장 비용이 과도한 경우** — CPU 서버 여러 대 > GPU 한 대
- 대량 행렬 연산이 지배적인 경우

> 세 번째가 비용 논증이다 — **"CPU 서버 여러 대 > GPU 한 대"**. GPU를 성능이 아니라 **단가**로
> 정당화한다.

## GPU를 쓰면 따라오는 것 — 3가지 변화

| 1. 아키텍처 변화 | 2. 운영 복잡도 증가 | 3. 비용 구조 변화 |
|---|---|---|
| CUDA 의존성 | 메모리 관리 | 인스턴스 단가 급증 |
| 드라이버 관리 | **OOM 이슈** | **idle GPU 비용 문제** |
| GPU 스케줄링 필요 | GPU utilization 모니터링 | **autoscaling 전략 필요** |
| Kubernetes GPU 리소스 관리 | 멀티 모델 로딩 전략 | |

> **"idle GPU 비용"**이 Ch1에서 예고한 *"항상 켜두기 어려운 자원"*의 실체다. CPU 서버는 유휴여도
> 싸지만 GPU는 유휴 시간이 곧 손실이다. → autoscaling과 **멀티 모델 로딩**(한 GPU에 여러 모델을
> 태워 가동률을 올리는 것)이 필수가 된다. Triton의 Concurrent Model Execution이 정확히 이 문제의
> 답이다 → [[NVIDIA Triton Inference Server]].

## 기존 페이지와의 대조

- **신규** — 추론 최적화(quantization·pruning·distillation·런타임), CPU/GPU 전환 판단은 위키에
  없던 주제다 → [[Inference optimization]] · [[ONNX]].
- **연장** — Total Latency 분해는 [[Latency and throughput]]의 서빙 문맥 확장. 그 페이지에 반영.
- **연결** — "배치 없이는 GPU 이점이 없다"가 [[AI DE Course - Part2 Ch4 Serving platforms]]의
  세 플랫폼이 모두 배치 기능을 강조한 이유를 설명한다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Inference optimization]] (상세) · [[Latency and throughput]] ·
  [[Batch and online serving]] · [[Model serving platforms]]
- 도구: [[ONNX]] · [[NVIDIA Triton Inference Server]]
- 앞: [[AI DE Course - Part2 Ch4 Serving platforms]]
- 다음 챕터: [[AI DE Course - Part2 Ch5 Feature store in practice]]

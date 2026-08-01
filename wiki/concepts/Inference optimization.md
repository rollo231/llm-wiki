---
type: concept
title: Inference optimization
area: [data-engineering]
aliases:
  - 추론 최적화
  - Quantization
  - 양자화
  - Pruning
  - Knowledge distillation
  - 지식 증류
  - GPU serving
  - CPU inference
tags: [data-engineering, mlops, inference, gpu, quantization, onnx, cost, latency]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part2 Ch4 CPU and GPU inference]]"]
---

# Inference optimization

**"GPU는 해결책의 마지막 단계에 가깝다."**

> **흔한 오해: CPU = 느림, GPU = 빠름.**
> **현실: CPU 추론이 더 빠른 경우도 많다. GPU는 비싸고 운영 난이도가 높고, 작은 요청에는 오히려
> 불리하다.**

## ⭐ 출발점 — Total Latency의 분해

```
Total Latency = 네트워크 + 직렬화 + 전/후처리 + 모델 추론 + 스케줄링
```

**GPU는 이 다섯 항목 중 하나만 줄인다.** 나머지 넷이 지배적이면 GPU를 붙여도 총 지연은 거의
그대로인데 비용만 몇 배가 된다.

**모델 추론이 병목이 아닌 경우가 매우 많다** — 작은 모델 / 낮은 QPS / I/O 중심 서비스.
→ **이 경우 GPU는 효과가 미미하다.**

이 분해가 [[Latency and throughput]]이 배치/스트림 문맥에서 말한 "물리적 오버헤드"의 서빙판이고,
[[Batch and online serving]]의 "Feature 조회가 latency의 대부분"이라는 관찰과 맞물린다 —
**전/후처리와 조회가 진짜 범인인 경우가 많다.**

## 언제 CPU면 충분한가

- 모델 크기가 작다 (수 MB ~ 수십 MB)
- **단건 요청 latency가 중요**
- QPS가 낮거나 중간
- 모델이 **트리 계열 / 선형 모델 / 작은 NN**

예: 추천 후보 생성 · 이상치 탐지 · 피처 기반 분류 · 룰 + ML 혼합 서비스.

## 언제 GPU가 필요한가

- 모델이 크다 (CNN, Transformer, LLM)
- 연산이 행렬 중심
- **QPS가 충분히 높다**
- **배치 처리가 가능하다**

> **GPU의 본질: 빠른 단일 추론기가 아니라 병렬 연산을 전제한 처리 장치.**
> **⇒ 배치 없이는 GPU 이점이 거의 사라진다.**

이 한 줄이 [[Model serving platforms]]의 세 플랫폼(TorchServe·BentoML·Triton)이 하나같이
배치 기능을 자랑한 이유다 — **배치는 편의 기능이 아니라 GPU를 쓰기 위한 전제 조건.**

## GPU 이전에 해야 할 CPU 최적화

### 모델 수준 3종

| | 하는 일 | 얻는 것 |
|---|---|---|
| **Quantization** | FP32 → **INT8 / FP16** | 연산량 감소 **+ 캐시 효율 증가**. CPU에서도 효과 큼. ONNX Runtime INT8, OpenVINO |
| **Pruning** | 영향이 적은 weight 제거 | 모델 크기 감소, **메모리 접근 감소**. 실시간 서빙에서 특히 효과적 |
| **Knowledge Distillation** | 큰 모델(Teacher) → 작은 모델(Student)로 지식 이전 | **"서빙용 모델"을 따로 만드는 전략.** 정확도 손실 대비 latency 이득이 큼 |

> Quantization의 이득이 **연산량 + 캐시 효율** 두 갈래인 게 핵심이다. INT8은 FP32의 1/4 크기라
> 같은 캐시에 4배 들어간다 — CPU에서 효과가 큰 진짜 이유.
>
> Knowledge Distillation의 프레이밍이 특히 유용하다: **"모델을 줄인다"가 아니라 "서빙용 모델을
> 따로 만든다".** 학습용과 서빙용이 다른 모델일 수 있다는 것 →
> [[Data and model versioning]]에 관리 대상이 하나 늘어난다.

### 런타임 최적화

**[[ONNX]] Runtime (CPU Execution Provider)** — PyTorch/TensorFlow 기본 실행보다 빠른 경우가
다수. Graph optimization, operator fusion, 학습용 연산(Dropout·Grad) 제거로 **추론 전용 그래프**
생성, AVX/AVX2/AVX-512 자동 활용.

## ⭐ CPU → GPU 전환 체크리스트

> 1. **CPU 최적화는 이미 완료되었는가?**
> 2. **추론 연산이 전체 latency의 대부분인가?**
> 3. **배치 처리가 가능한가?**
> 4. **GPU 비용 대비 효과가 명확한가?**

**전환을 고려할 상황:**

- 모델 자체가 큰 경우 — Transformer 계열, LLM, 대형 CV 모델
- **단일 추론 latency가 SLA를 못 맞추는 경우** (CPU 최적화 이후에도)
- **QPS가 높아 수평 확장 비용이 과도한 경우 — CPU 서버 여러 대 > GPU 한 대**
- 대량 행렬 연산이 지배적인 경우

> 세 번째가 **성능이 아니라 단가로 GPU를 정당화**하는 논증이다.

## GPU를 쓰면 따라오는 것

| 1. 아키텍처 변화 | 2. 운영 복잡도 | 3. 비용 구조 |
|---|---|---|
| CUDA 의존성 | 메모리 관리 | 인스턴스 단가 급증 |
| 드라이버 관리 | **OOM 이슈** | **idle GPU 비용** |
| GPU 스케줄링 | GPU utilization 모니터링 | **autoscaling 전략 필요** |
| Kubernetes GPU 리소스 관리 | **멀티 모델 로딩 전략** | |

> **"idle GPU 비용"이 GPU를 다른 자원과 구분 짓는다.** CPU 서버는 유휴여도 싸지만 GPU는 유휴
> 시간이 곧 손실이다. 그래서 **가동률을 올리는 것**이 성능이 아니라 비용의 문제가 되고,
> **멀티 모델 로딩**(한 GPU에 여러 모델)이 필수 전략이 된다 —
> [[NVIDIA Triton Inference Server]]의 Concurrent Model Execution이 정확히 이 답이다.

## 열린 질문

- **Quantization의 정확도 손실 크기** — "정확도 손실 대비 이득이 크다"까지만. INT8에서 어느 정도
  떨어지는지, 어떤 모델류에서 안전한지의 근거가 없다.
- **QAT vs PTQ** — 양자화 방식 구분이 없다.
- **GPU 공유 기술** — MIG가 TorchServe의 한계 서술에 한 번 등장할 뿐, 시분할·MPS·MIG의 비교가 없다.
- **LLM 추론 최적화** — KV 캐시, PagedAttention, continuous batching 등 LLM 특유의 최적화가
  전혀 다뤄지지 않는다. [[LLMOps]]를 다루면서 추론은 전통 ML 기준이다.
- **비용 손익분기** — "CPU 서버 여러 대 > GPU 한 대"의 실제 계산 예시가 없다.

## 링크

- 서빙 방식: [[Batch and online serving]] · [[Model serving platforms]]
- 런타임: [[ONNX]]
- 지연의 일반론: [[Latency and throughput]]
- 상위: [[MLOps]]
- 출처: [[AI DE Course - Part2 Ch4 CPU and GPU inference]]

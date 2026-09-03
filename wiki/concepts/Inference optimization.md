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
  - PCIe bottleneck
tags: [data-engineering, mlops, inference, gpu, quantization, onnx, cost, latency, roofline]
created: 2026-08-01
updated: 2026-09-03
sources: ["[[AI DE Course - Part2 Ch4 CPU and GPU inference]]", "[[AI DE Course - Part4 Ch4 GPU architecture and CUDA]]", "[[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]"]
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

---

# Part 4가 채운 것 — 왜 그런가의 하드웨어 근거

Part 2가 **판단 규칙**("GPU는 마지막 수단")이었다면 Part 4 Ch4·Ch5는 **그 근거와 진단 도구**다.
상세는 [[GPU architecture]] · [[GPU resource allocation]].

## ⭐ 왜 GPU가 어떤 워크로드에서 느린가 — 실리콘 면적

| | 목표 | 면적 배분 |
|---|---|---|
| **CPU** | 단일 스레드 속도 극대화 | **Control Logic & Deep Cache** — 분기 예측, 비순차 실행, 큰 L1/L2/L3 |
| **GPU** | 단위 시간당 전체 작업량 극대화 | **Massive ALUs & SIMT** — **컨트롤 로직을 버림** |

> ⭐ **컨트롤 로직을 버렸기 때문에 분기가 많은 로직에서는 오히려 느리다.**
> "row마다 다른 조건문(if-else)을 타는 쿼리"가 GPU의 적이다(warp divergence).

## ⭐ Total Latency 분해에 항목이 하나 더 있었다 — PCIe

| 경로 | 대역폭 |
|---|---|
| **PCIe Gen4** (Host → Device) | **약 64 GB/s** (x16 양방향 합산) |
| **GPU 내부 HBM** | **2~3 TB/s** |

> ⭐ **"계산은 0.1초 만에 끝났는데 데이터 전송에 10초가 소요되는" 40~50배의 절벽.**
>
> 위 § Total Latency 분해의 "네트워크 + 직렬화"에 해당하는데, **GPU를 붙이는 순간 이 항목이
> 새로 생긴다.** GPU가 줄이는 것은 "모델 추론" 하나인데, **동시에 전송이라는 항목을 추가한다.**
> H100이 **PCIe Gen5 채택**을 주요 개선으로 내세우는 이유이고,
> [[NVIDIA RAPIDS]]가 **"데이터를 GPU 위에 오래 유지"** 를 목표로 하는 이유다.

## Roofline — 병목이 연산인가 메모리인가

> **산술 집약도(Arithmetic Intensity) = 연산량 / 메모리 이동량**

| X축 | Y축 | 읽는 법 |
|---|---|---|
| 산술 집약도 | 실제 처리 성능 | **사면(기울어진 선)에 부딪히면 메모리 병목, 지붕(평평한 선)에 부딪히면 연산 병목** |

**실무 함의 — ETL은 메모리 집약이다:**

> ⭐ **"Join이나 Sort 같은 ETL은 코어 연산보다 메모리 이동이 극도로 많다. T4는 HBM이 아닌 GDDR을
> 써서 데이터 통로가 좁아 Memory-bound에 부딪혀 심각한 병목이 발생한다."**
>
> **ETL용 GPU는 FLOPs가 아니라 대역폭으로 골라야 한다.** "저렴한 추론용 GPU를 ETL에도 쓰면
> 되지 않나"에 대한 정확한 반박.

**[[ONNX]]의 operator fusion이 왜 효과적인지도 Roofline으로 설명된다** — 분모(메모리 이동)를
줄여 X축 오른쪽으로 미는 조작. 메커니즘은 **HBM 왕복 횟수 감소**다 → [[CUDA]]

## ⭐⭐ 진단 도구 — GPU 3축 해석표

Part 2의 체크리스트가 **도입 전** 판단이었다면, 이것은 **도입 후** 진단이다.

| GPU 사용률 | Queue | Latency | 해석 |
|---|---|---|---|
| 높음 | 낮음 | 정상 | **잘 활용 중** |
| 높음 | 높음 | 높음 | **GPU capacity 병목** — 증설이 답 |
| **낮음** | **높음** | **높음** | ⭐ **GPU 앞단 병목** — feature lookup, CPU 전처리, network |
| 낮음 | 낮음 | 정상 | **과잉 프로비저닝** |
| 높음 | 낮음 | 높음 | **memory, batch size, model 병목** — 증설해도 안 나아짐 |

> ⭐ **3행이 "GPU는 마지막 수단"의 실물이다.** GPU 사용률이 낮은데 느리면 **GPU를 늘려도
> 소용없다.** 1행과 5행의 차이(둘 다 사용률 높음 + 큐 낮음)도 중요하다 — latency 하나로
> 정반대 상황이 갈린다.

### 온라인 추론 지연의 세 원인 — 사례

| 원인 | 메커니즘 |
|---|---|
| **A. Feature Lookup 지연** | 모델 고도화로 피처 양·복잡도 증가 → **고속 캐시가 아닌 무거운 DB 쿼리로 전환.** ⭐ **데이터량 많은 '헤비 유저'의 조회가 길어져 P99만 폭증** (평균은 정상) |
| **B. Queueing Delay** | ⭐ **Dynamic Batching의 역설** — 배치가 찰 때까지 기다리거나 timeout이 너무 길면 **트래픽이 적은 시간대에 큐에서 시간을 허비** |
| **C. Model Inference** | VRAM 한계, **메모리 단편화**로 연산 효율 급감 |

> ⭐ **B가 특히 값지다.** Dynamic Batching은 [[NVIDIA Triton Inference Server]]의 대표 기능이고
> 위에서 "배치는 GPU를 쓰기 위한 전제 조건"이라고 했는데, **처리량 최적화가 지연을 만드는**
> 역설이 있다. [[Latency and throughput]]의 시소의 법칙이 서빙 설정에서 반복된다.
>
> **A는 [[Caching strategies]] 실패의 실물이다** — 캐시 레이어가 있었는데 피처가 커지면서
> DB로 넘어갔다.

## 열린 질문 — 갱신

- **Quantization의 정확도 손실 크기** — 여전히 근거 없음. **Part 4도 답하지 않았다.**
- **QAT vs PTQ** — 여전히 없음.
- ✅ **GPU 공유 기술** — **Part 4가 답했다.**
  **Time-slicing / MPS / MIG 비교표**(분할 방식·context switching·격리 수준·지원 장비)가
  [[GPU resource allocation]]에 있다. MPS의 격리는 **"최악(하나 죽으면 다 같이)"**.
- ⚠️ **LLM 추론 최적화 — 부분만.** Part 4 Ch5가 **지표**는 준다
  (**TTFT · time per output token · tokens per second · prompt/output length별 latency**).
  하지만 **KV 캐시가 대시보드 항목에 이름만 한 번 나오고**, PagedAttention·continuous batching·
  vLLM·TGI는 **Part 4에서도 등장하지 않는다.** **"무엇을 재는가"는 생겼고 "무엇이 그 값을
  결정하는가"는 여전히 공백이다.** → [[LLMOps]]
- **비용 손익분기** — 여전히 없음. Part 4의 RAPIDS 사례가 "TCO 70~80% 절감"을 주장하지만
  **단가 × 시간 계산이 없다** → [[NVIDIA RAPIDS]]
- **신규** — **gang scheduling** (분산 학습에서 N개 GPU 동시 확보). Kueue·Volcano가 강의 전체에
  없다 → [[GPU resource allocation]]

## 링크

- 서빙 방식: [[Batch and online serving]] · [[Model serving platforms]]
- 하드웨어: [[GPU architecture]] · [[CUDA]] · [[GPU resource allocation]]
- 런타임: [[ONNX]] · [[NVIDIA Triton Inference Server]]
- GPU ETL: [[NVIDIA RAPIDS]]
- 지연의 일반론: [[Latency and throughput]]
- 관측: [[Data SLA and observability]]
- 캐싱: [[Caching strategies]]
- 상위: [[MLOps]]
- 출처: [[AI DE Course - Part2 Ch4 CPU and GPU inference]] ·
  [[AI DE Course - Part4 Ch4 GPU architecture and CUDA]] ·
  [[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]

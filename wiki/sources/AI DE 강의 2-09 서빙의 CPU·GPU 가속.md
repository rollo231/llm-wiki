---
type: source
title: AI DE 강의 2-09 서빙의 CPU·GPU 가속
aliases: [AI DE 2-09]
tags: [AI-DE-강의, 서빙, 성능, GPU]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/data-engineering/ai-de-course/part2/04. Ch4. 서빙 아키텍처 및 플랫폼.pdf"
---

# AI DE 강의 2-09 서빙의 CPU·GPU 가속

[[AI 데이터 엔지니어링 강의]] Part 2의 Ch4 마지막 소단원. "추론이 느리면 GPU"라는 통념을 뒤집어, **병목부터 찾고 →
모델을 줄이고 → 런타임을 바꾸고 → 그래도 안 되면 GPU**라는 순서를 제시한다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 2 「AI 학습/추론 중심 데이터 파이프라인 설계」 |
| 덱 제목 | Ch4. 서빙 아키텍처 및 플랫폼 — 4. 서빙 환경에서의 CPU/GPU 가속 활용 방안 |
| 원본 파일 | `part2/04. Ch4. 서빙 아키텍처 및 플랫폼.pdf` p60–77 (18p, 덱 전체 77p) |
| 강사 | Habi (슬라이드 표기) |
| 작성 시기 | PDF 생성일 2026-03-24 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch4`, 소단원 번호 `4`는 표지 슬라이드 |

## 요약

### 01. GPU를 서빙에 무조건 사용해야 할까?

- 추론 속도 문제의 원인은 다양하고, **GPU는 해결책의 마지막 단계에 가깝다.**
- 흔한 오해 "CPU = 느림, GPU = 빠름". 실제로는 CPU 추론이 더 빠른 경우도 많다. GPU는 비싸고 운영이 어렵고, **작은
  요청에는 오히려 불리하다.**
- **병목의 실제 원인** — `Total Latency = 네트워크 + 직렬화 + 전/후처리 + 모델 추론 + 스케줄링`. 작은 모델·낮은 QPS·I/O
  중심 서비스에서는 모델 추론이 병목이 아니므로 GPU 효과가 미미하다.

### 02. CPU로 서빙이 충분한 경우

- 모델 크기가 작다(수 MB ~ 수십 MB), 단건 요청 latency가 중요하다, QPS가 낮거나 중간, 트리 계열·선형 모델·작은 NN.
- 예: 추천 후보 생성, 이상치 탐지, 피처 기반 분류, 룰 + ML 혼합 서비스.

### 03. GPU가 필요한 경우

- 모델이 크다(CNN·Transformer·LLM), 연산이 행렬 중심, QPS가 충분히 높다, **배치 처리가 가능하다.**
- **GPU의 본질** — 빠른 단일 추론기가 아니라 병렬 연산을 전제로 한 처리 장치. **배치 없이는 GPU 이점이 거의 사라진다.**

### 04. GPU 이전에 반드시 해야 할 CPU 최적화

| 수준 | 기법 | 강의의 설명 |
|---|---|---|
| 모델 | Quantization | FP32 → INT8 / FP16. 연산량 감소 + 캐시 효율 증가, "CPU에서도 큰 효과"(예: ONNX Runtime INT8, OpenVINO) |
| 모델 | Pruning | 영향이 적은 weight 제거. 모델 크기·메모리 접근 감소, 실시간 서빙에서 특히 효과적 |
| 모델 | Knowledge Distillation | 큰 모델 → 작은 모델로 지식 이전. **"서빙용 모델"을 따로 만드는 전략**, 정확도 손실 대비 latency 이득이 크다 |
| 런타임 | ONNX Runtime (CPU Execution Provider) | PyTorch·TensorFlow 기본 실행보다 빠른 경우 다수. Graph optimization, operator fusion |

### 05. ONNX, ONNX Runtime

- **ONNX** — 딥러닝 모델을 프레임워크 독립적인 그래프 표현으로 저장하는 표준. PyTorch·TensorFlow·Scikit-learn은 실행
  엔진이 제각각이지만 ONNX는 모델 구조 + 연산 그래프를 표준화한 중간 표현이다. 예: TensorFlow로 배포한 뒤 PyTorch 모델
  요청이 오거나 여러 프레임워크가 섞여 있으면 ONNX로 변환해 배포한다.
- **ONNX Runtime** — 오직 추론만을 위한 고성능 실행 엔진. C++ 기반 정적 실행으로 Python 오버헤드를 줄이고, CPU에서는
  그래프 최적화·불필요 연산 제거·연산 결합·SIMD 벡터화·멀티스레딩을 쓴다.
  1. Graph-level optimization — PyTorch가 연산을 하나씩 처리하는 반면, 미리 분석해 합칠 것은 합치고 불필요한 것은 제거.
  2. 학습용 연산(Dropout, Grad 등) 제거 → 추론 전용 그래프.
  3. CPU 친화적 실행 — "AVX / AVX2 / AVX-512 자동 활용, Intel MKL, OpenMP 기반 병렬 처리".

→ [[ONNX]]

### 06. CPU에서 GPU로

**전환 판단 체크리스트** — CPU 최적화는 이미 완료되었는가? 추론 연산이 전체 latency의 대부분인가? 배치 처리가 가능한가?
GPU 비용 대비 효과가 명확한가?

**GPU로 전환을 고려할 때** — 모델 자체가 큰 경우(Transformer 계열·LLM·대형 CV), CPU 최적화 이후에도 단일 추론 latency가
SLA를 못 맞추는 경우, QPS가 높아 수평 확장 비용이 과도한 경우("CPU 서버 여러 대 > GPU 한 대"), 대량 행렬 연산이 지배적인
경우.

**GPU를 쓰면 바뀌는 것**

| 아키텍처 | 운영 복잡도 | 비용 구조 |
|---|---|---|
| CUDA 의존성 | 메모리 관리 | 인스턴스 단가 급증 |
| 드라이버 관리 | OOM 이슈 | idle GPU 비용 |
| GPU 스케줄링 | GPU utilization 모니터링 | autoscaling 전략 필요 |
| Kubernetes GPU 리소스 관리 | 멀티 모델 로딩 전략 | |

## 핵심

- **순서가 이 강의의 전부다** — 병목 측정 → 모델 수준 → 런타임 수준 → GPU. 이 순서는 Part 2 서빙 절반에서 가장 옮겨 쓰기
  좋은 생각이다. "GPU는 해결책의 마지막 단계"는 비용이 가장 크고 되돌리기 어려운 수단을 맨 뒤에 둔다는 뜻이다.
  *(위키의 관찰)* → [[추론 최적화]]
- **"배치 없이는 GPU 이점이 사라진다"는 [[지연 시간과 처리량]]의 시소가 하드웨어에서 반복되는 것이다.** 모아서 한꺼번에
  처리하면 처리량이 오르지만 모이기를 기다리는 지연이 생긴다 — 동적 배칭([[Triton Inference Server]])·adaptive
  batching([[BentoML]])이 그 절충을 서버가 대신 해 주는 장치다. *(위키의 연결)*
- **지식 증류는 "서빙용 모델을 따로 만든다"는 뜻이다** — 서빙되는 아티팩트가 학습된 모델과 달라진다. 무엇을 배포했는지,
  그 모델로 다시 평가했는지를 따로 추적해야 한다. → [[데이터와 모델 버전 관리]] *(위키의 연결)*
- **양자화도 서빙 모델을 바꾼다** — 그러므로 오프라인 평가를 양자화된 아티팩트로 다시 해야 한다. 강의는 "정확도 손실 대비
  latency 이득이 크다"고만 하고 손실을 어떻게 재는지는 말하지 않는다. *(위키의 관찰)*
- p76의 "CPU 서버 여러 대 > GPU 한 대"는 **비용** 비교의 약식 표기다 — 같은 QPS를 CPU 수평 확장으로 감당하는 비용이 GPU
  한 대보다 커질 때 전환한다는 뜻으로 읽는다. *(위키의 해석)*

## 주의·결함

- ⚠️ **ONNX Runtime의 "Intel MKL, OpenMP 기반 병렬 처리"는 기본 패키지에 맞지 않는다.** CPU 패키지는 v1.7.0(2021-03-03)부터
  OpenMP 없이 빌드되고, ORT는 자체 스레드 풀을 쓴다. 기본 CPU 백엔드는 MLAS이며 MKL 계열(oneDNN)·OpenVINO는 **별도
  execution provider**다. "AVX/AVX2/AVX-512 자동 활용"은 MLAS의 명령어 경로로 대체로 맞다.
  [ONNX Runtime v1.7.0 릴리스 노트 — "Starting from this release, all ONNX Runtime CPU packages are now built without
  OpenMP." https://github.com/microsoft/onnxruntime/releases/tag/v1.7.0 ; Threading 문서 — `intra_op_num_threads = 0` →
  "Number of physical CPU Cores" https://onnxruntime.ai/docs/performance/tune-performance/threading.html ; Execution
  Providers 목록 https://onnxruntime.ai/docs/execution-providers/ , 2026-09-14 확인]
- ✅ **학습용 연산 제거·연산 결합** — Dropout·Identity 제거는 Basic 수준 그래프 최적화에, 노드 결합(fusion)은 Extended
  수준에 해당한다. [Graph optimizations 문서 — Basic은 "semantics-preserving graph rewrites which remove redundant nodes
  and redundant computation", 목록에 Identity Elimination·Dropout Elimination; Extended는 "complex node fusions"
  https://onnxruntime.ai/docs/performance/model-optimizations/graph-optimizations.html , 2026-09-14 확인]
- ⚠️ **"FP32 → INT8 / FP16 … CPU에서도 큰 효과"는 과장이다.** ORT에서 FP16은 GPU 쪽 최적화이고, INT8의 CPU 이득은
  하드웨어에 달려 있다(VNNI가 있으면 유리, 오래된 CPU에서는 오히려 느려질 수 있다).
  [Float16 문서 — "the CPU version of ONNX Runtime doesn't support float16 ops"
  https://onnxruntime.ai/docs/performance/model-optimizations/float16.html ; Quantization 문서 — "The performance
  improvement depends on your model and hardware." · "it is not rare to get worse performance on old devices."
  https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html , 2026-09-14 확인]
- **수치가 하나도 없다** — CPU가 GPU보다 빠른 경우, 양자화·ONNX Runtime의 속도 향상 모두 벤치마크 없이 방향만 말한다.
- 슬라이드 이미지 출처가 블로그(DigitalOcean, Towards Data Science, Medium)다 — 1차 자료가 없다.

## 관련

- 개념: [[추론 최적화]] · [[모델 서빙]] · [[지연 시간과 처리량]] · [[데이터와 모델 버전 관리]]
- 도구: [[ONNX]] · [[Triton Inference Server]] · [[BentoML]] · [[TorchServe]]
- 이전 강의: [[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]
- 다음 강의: [[AI DE 강의 2-10 Feature Store 기본 개념]]

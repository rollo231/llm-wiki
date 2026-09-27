---
type: source
title: AI DE 강의 2-09 서빙의 CPU·GPU 가속
aliases: [AI DE 2-09]
tags: [AI-DE-강의, 서빙, 성능, GPU]
created: 2026-09-14
updated: 2026-09-27
sources:
  - "raw/data-engineering/ai-de-course/part2/04. Ch4. 서빙 아키텍처 및 플랫폼.pdf"
---

# AI DE 강의 2-09 서빙의 CPU·GPU 가속

[[AI 데이터 엔지니어링 강의]] Part 2의 Ch4 마지막 소단원. "추론이 느리면 GPU를 쓴다"는 통념에 반대하고, 병목을 먼저 찾은 뒤 모델을 줄이고, 런타임을 바꾸고, 그래도 안 되면 GPU로 가는 순서를 제시한다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 2 「AI 학습/추론 중심 데이터 파이프라인 설계」 |
| 덱 제목 | Ch4. 서빙 아키텍처 및 플랫폼: 4. 서빙 환경에서의 CPU/GPU 가속 활용 방안 |
| 원본 파일 | `part2/04. Ch4. 서빙 아키텍처 및 플랫폼.pdf` p60–77 (18p, 덱 전체 77p) |
| 강사 | Habi (슬라이드 표기) |
| 작성 시기 | PDF 생성일 2026-03-24 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch4`, 소단원 번호 `4`는 표지 슬라이드 |

## 요약

### 01. GPU를 서빙에 무조건 사용해야 할까?

- 추론이 느린 원인은 여러 가지이고, 강의는 GPU를 해결책의 마지막 단계에 가깝다고 본다.
- 흔한 오해는 "CPU = 느림, GPU = 빠름"이다. 실제로는 CPU 추론이 더 빠른 경우가 많다. GPU는 비싸고 운영이 어렵고, 작은 요청에는 오히려 불리하다.
- 병목의 실제 원인은 `Total Latency = 네트워크 + 직렬화 + 전/후처리 + 모델 추론 + 스케줄링`으로 나눠 본다. 작은 모델, 낮은 QPS, I/O 중심 서비스에서는 모델 추론이 병목이 아니어서 GPU를 써도 효과가 거의 없다.

### 02. CPU로 서빙이 충분한 경우

- 모델 크기가 작을 때(수 MB ~ 수십 MB), 단건 요청의 latency가 중요할 때, QPS가 낮거나 중간일 때, 트리 계열·선형 모델·작은 NN일 때.
- 예: 추천 후보 생성, 이상치 탐지, 피처 기반 분류, 룰 + ML 혼합 서비스.

### 03. GPU가 필요한 경우

- 모델이 크고(CNN·Transformer·LLM), 연산이 행렬 중심이고, QPS가 충분히 높고, 배치 처리가 가능할 때.
- 강의는 GPU를 빠른 단일 추론기로 보지 않고, 병렬 연산을 전제로 한 처리 장치로 설명한다. 배치 없이는 GPU의 이점이 거의 사라진다.

### 04. GPU 이전에 반드시 해야 할 CPU 최적화

| 수준 | 기법 | 강의의 설명 |
|---|---|---|
| 모델 | Quantization | FP32 → INT8 / FP16. 연산량 감소 + 캐시 효율 증가, "CPU에서도 큰 효과"(예: ONNX Runtime INT8, OpenVINO) |
| 모델 | Pruning | 영향이 적은 weight 제거. 모델 크기·메모리 접근 감소, 실시간 서빙에서 특히 효과적 |
| 모델 | Knowledge Distillation | 큰 모델 → 작은 모델로 지식 이전. "서빙용 모델"을 따로 만드는 전략, 정확도 손실 대비 latency 이득이 크다 |
| 런타임 | ONNX Runtime (CPU Execution Provider) | PyTorch·TensorFlow 기본 실행보다 빠른 경우 다수. Graph optimization, operator fusion |

### 05. ONNX, ONNX Runtime

- ONNX: 딥러닝 모델을 프레임워크와 무관한 그래프 표현으로 저장하는 표준이다. PyTorch·TensorFlow·Scikit-learn은 실행 엔진이 제각각이지만, ONNX는 모델 구조와 연산 그래프를 표준화한 중간 표현이다. 예를 들어 TensorFlow로 배포한 곳에 PyTorch 모델 요청이 오거나 여러 프레임워크가 섞여 있으면 ONNX로 변환해 배포한다.
- ONNX Runtime: 추론만을 위한 고성능 실행 엔진이다. C++ 기반 정적 실행으로 Python 오버헤드를 줄이고, CPU에서는 그래프 최적화, 불필요한 연산 제거, 연산 결합, SIMD 벡터화, 멀티스레딩을 쓴다.
  1. Graph-level optimization: PyTorch는 연산을 하나씩 처리하지만, ONNX Runtime은 그래프를 미리 분석해 합칠 것은 합치고 불필요한 것은 없앤다.
  2. 학습용 연산(Dropout, Grad 등)을 없애 추론 전용 그래프로 만든다.
  3. CPU 친화적 실행: "AVX / AVX2 / AVX-512 자동 활용, Intel MKL, OpenMP 기반 병렬 처리".

도구 페이지는 [[ONNX]]다.

### 06. CPU에서 GPU로

전환 판단 체크리스트는 네 가지다. CPU 최적화를 이미 마쳤는가, 추론 연산이 전체 latency의 대부분인가, 배치 처리가 가능한가, GPU 비용 대비 효과가 분명한가.

GPU 전환을 고려할 경우: 모델 자체가 클 때(Transformer 계열·LLM·대형 CV), CPU 최적화 뒤에도 단일 추론 latency가 SLA를 못 맞출 때, QPS가 높아 수평 확장 비용이 지나칠 때("CPU 서버 여러 대 > GPU 한 대"), 대량 행렬 연산이 대부분일 때.

GPU를 쓰면 바뀌는 것:

| 아키텍처 | 운영 복잡도 | 비용 구조 |
|---|---|---|
| CUDA 의존성 | 메모리 관리 | 인스턴스 단가 급증 |
| 드라이버 관리 | OOM 이슈 | idle GPU 비용 |
| GPU 스케줄링 | GPU utilization 모니터링 | autoscaling 전략 필요 |
| Kubernetes GPU 리소스 관리 | 멀티 모델 로딩 전략 | |

## 핵심

- 이 강의에서 가장 쓸모 있는 것은 순서다. 병목 측정, 모델 수준, 런타임 수준, GPU 순으로 간다. Part 2 서빙 부분에서 다른 곳에 옮겨 쓰기 가장 좋은 생각이다. "GPU는 해결책의 마지막 단계"는 비용이 가장 크고 되돌리기 어려운 수단을 맨 뒤에 둔다는 뜻으로 읽었다. 이는 위키의 관찰이다([[추론 최적화]]).
- "배치 없이는 GPU 이점이 사라진다"는 [[지연 시간과 처리량]]의 맞교환이 하드웨어 수준에서 다시 나타난 것이다. 이 연결은 위키가 한 것이다([[추론 최적화]]).
- 지식 증류("서빙용 모델")와 양자화를 하면 서빙하는 아티팩트가 학습한 모델과 달라진다. 경량화한 아티팩트로 다시 평가하고 버전을 따로 추적해야 하는데, 강의는 "정확도 손실 대비 latency 이득이 크다"고만 한다. 이 지적은 위키의 관찰이다([[추론 최적화]] · [[데이터와 모델 버전 관리]]).
- p76의 "CPU 서버 여러 대 > GPU 한 대"는 비용 비교를 줄여 쓴 것으로 읽었다. 같은 QPS를 CPU 수평 확장으로 감당하는 비용이 GPU 한 대보다 커질 때 전환한다는 뜻이다. 이 읽기는 위키의 해석이다.

## 주의·결함

- ⚠️ ONNX Runtime의 "Intel MKL, OpenMP 기반 병렬 처리"는 기본 패키지와 맞지 않는다. CPU 패키지는 v1.7.0(2021-03-03)부터 OpenMP 없이 빌드되고, ORT는 자체 스레드 풀을 쓴다. 기본 CPU 백엔드는 MLAS이고, MKL 계열(oneDNN)과 OpenVINO는 별도의 execution provider다. "AVX/AVX2/AVX-512 자동 활용"은 MLAS의 명령어 경로를 가리키는 말로는 대체로 맞다. [ONNX Runtime v1.7.0 릴리스 노트 — "Starting from this release, all ONNX Runtime CPU packages are now built without OpenMP." https://github.com/microsoft/onnxruntime/releases/tag/v1.7.0 ; Threading 문서 — `intra_op_num_threads = 0` → "Number of physical CPU Cores" https://onnxruntime.ai/docs/performance/tune-performance/threading.html ; Execution Providers 목록 https://onnxruntime.ai/docs/execution-providers/ , 2026-09-14 확인]
- ✅ 학습용 연산 제거와 연산 결합은 맞다. Dropout·Identity 제거는 Basic 수준 그래프 최적화에, 노드 결합(fusion)은 Extended 수준에 들어간다. [Graph optimizations 문서 — Basic은 "semantics-preserving graph rewrites which remove redundant nodes and redundant computation", 목록에 Identity Elimination·Dropout Elimination; Extended는 "complex node fusions" https://onnxruntime.ai/docs/performance/model-optimizations/graph-optimizations.html , 2026-09-14 확인]
- ⚠️ "FP32 → INT8 / FP16 … CPU에서도 큰 효과"는 과장이다. ORT에서 FP16은 GPU 쪽 최적화이고, CPU에서 INT8이 얼마나 빨라지는지는 하드웨어에 달렸다. VNNI가 있으면 유리하고, 오래된 CPU에서는 오히려 느려질 수 있다. [Float16 문서 — "the CPU version of ONNX Runtime doesn't support float16 ops" https://onnxruntime.ai/docs/performance/model-optimizations/float16.html ; Quantization 문서 — "The performance improvement depends on your model and hardware." · "it is not rare to get worse performance on old devices." https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html , 2026-09-14 확인]
- ⚠️ Pruning이 "실시간 서빙에서 특히 효과적"이라는 것도 과장이다. weight를 0으로 만드는 비구조적 가지치기만으로는 dense 커널에서 크기도 지연도 줄지 않는다. 속도가 빨라지는 것은 구조적 가지치기나 하드웨어가 지원하는 2:4 희소성(NVIDIA Ampere 이상)을 쓸 때다. [PyTorch 튜토리얼 「semi-structured (2:4) sparsity」 — "Zeroing out parameters doesn't affect the latency / memory overhead of our model out of the box." https://docs.pytorch.org/tutorials/advanced/semi_structured_sparse.html · Mishra et al., arXiv:2104.08378 — "Sparse Tensor Cores, which exploit a 2:4 (50%) sparsity pattern that leads to twice the math throughput of dense matrix units." https://arxiv.org/abs/2104.08378 , 2026-09-14 확인]
- 수치가 하나도 없다. CPU가 GPU보다 빠른 경우도, 양자화나 ONNX Runtime의 속도 향상도 벤치마크 없이 방향만 말한다.
- 슬라이드 이미지의 출처가 블로그(DigitalOcean, Towards Data Science, Medium)이고, 1차 자료는 없다.

## 관련

- 개념: [[추론 최적화]] · [[모델 서빙]] · [[지연 시간과 처리량]] · [[데이터와 모델 버전 관리]]
- 도구: [[ONNX]] · [[Triton Inference Server]] · [[BentoML]] · [[TorchServe]]
- 이전 강의: [[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]
- 다음 강의: [[AI DE 강의 2-10 Feature Store 기본 개념]]

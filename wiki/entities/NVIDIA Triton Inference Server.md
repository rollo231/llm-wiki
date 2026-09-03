---
type: entity
title: NVIDIA Triton Inference Server
area: [data-engineering]
aliases:
  - Triton
  - Triton Inference Server
  - 트리톤
  - Model Ensemble
  - Concurrent Model Execution
tags: [data-engineering, mlops, serving, triton, nvidia, gpu, kubernetes, tensorrt]
created: 2026-08-01
updated: 2026-09-03
sources: ["[[AI DE Course - Part2 Ch4 Serving platforms]]"]
---

# NVIDIA Triton Inference Server

**고성능 추론에 특화된 Inference Engine / 추론 런타임.** 4종 서빙 플랫폼 중 **추상화가 가장 높고
성능·확장성이 가장 좋으며 진입 장벽도 가장 높다.** → [[Model serving platforms]]

| 장점 | 제약 |
|---|---|
| 매우 높은 성능 | **진입 장벽 높음** |
| 동적 배치, 멀티모델, GPU 최적화 | **비즈니스 로직 직접 구현 불가** |
| 다양한 프레임워크 지원 (ONNX, TensorRT 등) | 운영 복잡도 높음 |

## 구조

```
Client Application
  → Python/C++ Client Library
    → HTTP / gRPC ─────────────────┐          ┌─ Model Repository (Persistent Volume)
                                   ↓          ↓
    ┌──────────── NVIDIA Triton Inference Server ────────────┐
    │  Inference Request → Per-Model Scheduler Queues        │  ← Model Management
    │  Inference Response ← Framework Backends               │
    │      (TensorRT · TensorFlow · ONNX · PyTorch · Custom) │
    │  Status/Health Metrics Export → HTTP (Prometheus 등)    │
    └────────────────────────────────────────────────────────┘
              GPU  GPU  GPU  GPU        CPU
```

### HTTP / gRPC Endpoint — 일부러 비워둔 층

외부 요청의 단일 진입점. HTTP와 gRPC 동시 지원, K8s의 Service/Ingress와 자연스럽게 연동.

> **"여기서는 비즈니스 로직을 처리하지 않는다!"**
> [[FastAPI]] 같은 프레임워크와 달리 validation·routing·auth 중심이 아니라 **목적은 오직
> Inference Request 전달.** 설계 의도는 **네트워크 계층을 단순화하여 내부 스케줄링과 GPU 활용에
> 집중**하는 것.

**FastAPI와 Triton은 같은 자리를 정반대 철학으로 채운다** — 로직을 다 넣을 것인가, 아무것도 넣지
않을 것인가. 그래서 실무에서는 **FastAPI(또는 BentoML API Server) 뒤에 Triton을 두는 조합**이
자연스러운데, 강의는 이 조합을 명시하지 않는다.

### Model Repository / Model Management

- 모델을 **동적으로 로드 / 언로드**, 버전 관리 (1, 2, 3 …)
- **컨테이너 재시작 없이 모델 교체 가능**
- **모델은 서버 코드에 포함되지 않고 데이터 자산처럼 취급**
- **Kubernetes + PVC와 궁합이 매우 좋음**

> **이 네 줄이 [[TorchServe]]의 한계("Frontend가 Stateful → K8s Native하지 않음")와 정확히
> 대칭**이다. 모델을 코드에서 분리해 볼륨에 두면, 서버는 stateless가 되고 수평 확장이 열린다.

### Per-Model Scheduler Queues — 핵심 기술

**각 모델이 자신만의 독립적인 대기열을 가진다.**

> **"요청 단위로 즉시 실행하지 않음. Scheduler가 개입, GPU 효율을 최우선으로 고려."**

- **Dynamic Batching** — 여러 클라이언트로부터 들어온 개별 요청을 지능적으로 모아 **하나의 배치로 구성**
- **Sequence Batching** — 상태 정보가 필요한 모델(RNN 등)을 위해 **요청의 순서를 보장하며** 배치 구성

> 처리 흐름: 요청 수신 → 큐에 적재 → **배치 가능 여부 판단** → 실행 → 응답 반환.
> "즉시 실행하지 않는다"가 latency를 조금 희생해 throughput을 크게 얻는 거래이고,
> [[Latency and throughput]]의 시소가 스케줄러 수준에서 구현된 형태다.

### Framework Backends

- **멀티 프레임워크** — TensorRT·TensorFlow·PyTorch·[[ONNX]] + 사용자 정의 **Custom Backend**
- **Concurrent Model Execution** — **동일한 GPU 내에서 서로 다른 프레임워크의 모델들을 동시에
  실행**하여 자원 점유율 최적화

### 하드웨어 추상화

- **GPU/CPU 가속** — 특정 모델은 GPU 0번, 다른 모델은 CPU에 할당하는 식의 **정교한 자원 배분**
- **Status/Health Metrics Export** — Liveness/Readiness와 추론 통계(Latency, Throughput)를
  HTTP로 외부 모니터링(Prometheus 등)에 전송

## 왜 Triton인가 — 세 가지 논거

**1. 극한의 성능**

- **C++ 기반 코어 설계로 파이썬 인터프리터의 오버헤드 완벽 제거**
- **Dynamic Batching**으로 GPU 처리량 극대화
- **Shared Memory** — 대용량 데이터(영상/이미지) 전송 시 **메모리 복사 비용 최소화**

**2. 통합 운영의 효율성 (Model Consolidation)**

- **Multi-Framework** — 파편화된 모델들을 단일 서버에서 통합 관리
- **Model Ensemble** — 전처리부터 여러 모델 추론까지 전 과정을 **서버 내부 DAG(Directed Acyclic
  Graph)로 구성하여 네트워크 지연(Latency) 제거**

> **Model Ensemble이 숨은 킬러 기능이다.** 전처리 서비스와 모델 서비스를 따로 두면 그 사이 네트워크
> 홉이 [[Inference optimization]]의 `Total Latency` 분해에서 **네트워크 + 직렬화** 항목으로
> 잡힌다. 서버 안 DAG로 넣으면 그 항목이 사라진다 — **GPU를 빠르게 하는 게 아니라 GPU 바깥을
> 없애는 최적화.**

**3. 인프라 비용 절감 (Cost Efficiency)**

- **Concurrent Execution**으로 동일 GPU 내 다중 모델 인스턴스 실행 → 자원 점유율 최적화
- **하드웨어 가속기(GPU/CPU)의 가동률을 100%에 가깝게 유지하여 운영 비용(TCO) 절감**

> 이것이 [[Inference optimization]]이 말한 **"idle GPU 비용"** 문제의 답이다. GPU는 유휴 시간이
> 곧 손실이므로 **가동률 올리기가 성능이 아니라 비용의 문제**가 된다.

## 열린 질문

- **비즈니스 로직을 어디에 두나** — "직접 구현 불가"라고만 하고, 앞단에 무엇을 세울지의 권고가 없다.
  (FastAPI/BentoML과의 조합이 자연스러워 보이지만 강의가 말하지 않는다.)
- **TensorRT 변환의 비용과 제약** — 최고 성능 경로인데 변환 실패·연산자 미지원 같은 실무 이슈가 없다.
- **Dynamic Batching의 지연 예산** — max queue delay를 어떻게 잡는지, p99에 미치는 영향이 없다.
- **LLM 서빙** — vLLM 등 LLM 전용 스택과의 관계가 다뤄지지 않는다.

## 링크

- 비교: [[Model serving platforms]]
- 대칭: [[TorchServe]] (K8s 궁합) · [[FastAPI]] (로직의 위치)
- 인접: [[BentoML]] · [[ONNX]]
- 자원·비용: [[Inference optimization]] · [[Latency and throughput]]
- 출처: [[AI DE Course - Part2 Ch4 Serving platforms]]

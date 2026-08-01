---
type: entity
title: CUDA
area: [programming, data-engineering]
aliases: [쿠다, Compute Unified Device Architecture, CUDA kernel, SIMT, warp]
tags: [programming, gpu, cuda, nvidia, simt, parallel-computing, pytorch]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch4 GPU architecture and CUDA]]"]
---

# CUDA

**엔비디아의 병렬 컴퓨팅 플랫폼이자 프로그래밍 모델.**

> **"GPU 안에는 수천 개의 코어(ALU)가 존재하지만, 작성하는 Python이나 C++ 코드는 기본적으로 CPU가
> 읽고 처리하도록 만들어진 직렬 언어다. CUDA는 이 간극을 메우는 지휘 체계이자 통역사 역할을 한다."**

하드웨어 쪽은 [[GPU architecture]], 여기는 **프로그래밍 모델**을 다룬다.

## ⭐ The Core Mapping — 논리 구조 ↔ 물리 구조 1:1

> **"CUDA의 목표: 소프트웨어상의 논리적 구조를 GPU의 물리적 하드웨어 구조에 정확히 1:1로
> 대응시키는 것."**

| 소프트웨어 | 하드웨어 | 설명 |
|---|---|---|
| **스레드 (Thread)** | **GPU 코어** | 가장 작은 실행 단위 하나가 코어 하나에 할당 |
| **블록 (Thread Block)** | **SM** (Streaming Multiprocessor) | 여러 스레드를 묶은 논리적 단위가 SM에 통째로 할당. **같은 블록의 스레드는 Shared Memory 공유** |
| **그리드 (Grid)** | **GPU 디바이스 전체** | 여러 블록을 묶은 단위. 특정 연산을 던질 때 생성되는 전체 작업 덩어리 |

**스케줄러는 개별 스레드가 아니라 Warp(보통 32개 스레드) 단위로 명령을 내린다.**

## 커널과 SIMT

| | 뜻 |
|---|---|
| **커널 (Kernel)** | CPU(Host)에서 호출하지만 실제 코드는 GPU(Device)의 수많은 스레드에서 **동시에 병렬 실행되는 함수** |
| **SIMT** (Single Instruction, Multiple Threads) | 수백 개 스레드가 **완전히 동일한 명령**을 받되 각자 **서로 다른 데이터**로 계산. 예: *"각자의 위치에 있는 숫자에 2를 곱해라"* |

> ⭐ **SIMT가 GPU의 강점이자 약점이다.** 같은 명령이면 수천 개가 동시에 돌지만,
> **분기(if-else)가 생기면 경로별로 직렬화되어 코어가 논다** (warp divergence).
> → [[GPU architecture]]의 "row 단위 조건문이 GPU ETL의 적"

## ⭐ PyTorch 한 줄로 따라가기

```python
A = torch.randn(100000).cuda()
B = torch.randn(100000).cuda()
C = A + B          # 이 한 줄이 실행될 때 GPU에서는?
```

| 단계 | 일어나는 일 |
|---|---|
| **CPU라면** | 코어 하나가 A[0]+B[0], A[1]+B[1]… **10만 번의 덧셈을 순서대로** |
| **커널 배포** | `.cuda()`가 붙어 있어 이 덧셈이 **CUDA 커널로 변환.** 10만 개의 스레드에 "자기 번호표(ID)에 맞는 데이터 1개씩 더하라"고 명령 |
| **Thread → Core** | '스레드 #505번'은 코어 하나에 배정 → **"HBM에서 A[505]와 B[505]를 가져와 더한 뒤 C[505]에 Write"** 만 수행. 10만 개 코어가 동시에 1번씩 |
| **Block → SM** | CUDA는 스레드를 **1,024개씩** 묶어 한 블록으로. 같은 SM의 1,024개 스레드는 **Shared Memory(L1)를 공유** → 평균을 구하거나 데이터를 교환할 때 **HBM까지 안 가고** 캐시에서 |
| **Grid → GPU 전체** | 블록 약 100개가 모이면 10만 개(그리드). **A100 안의 108개 SM에 전달**되면서 동시 연산 시작 |

> **"블록 100개 → A100의 SM 108개"** 같은 실제 숫자로 착지하는 게 좋다.
> (A100의 SM 수는 실제로 108개)

## ⭐ Operator Fusion — 커널을 합치는 이유

```python
C = A + B
D = C * 2
```

| | 동작 | 결과 |
|---|---|---|
| **비최적화** | ① 덧셈 커널 → HBM에서 A,B Read → 연산 → **C를 HBM에 Write** ② 곱셈 커널 새로 호출 → **HBM에서 C 다시 Read** → 연산 → D Write | ⚠️ **실제 연산 시간보다 Global Memory 왕복 I/O가 더 커지는 Memory-Bound** |
| **최적화** | HBM에서 A,B를 **한 번만** Read, 코어 내부 **레지스터에 결과를 둔 채** 덧셈·곱셈 연속 수행. `(A+B)*2` 형태의 **단일 커널** 생성 | Global Memory 접근 **절반** → **Arithmetic Intensity 비약적 상승** |

> **[[ONNX]] 런타임의 operator fusion이 왜 효과가 있는지가 이것이다.**
> Part 2([[AI DE Course - Part2 Ch4 CPU and GPU inference]])는 "operator fusion으로 빨라진다"까지
> 였고, 여기서 **VRAM I/O 왕복 횟수 감소**라는 메커니즘이 나온다.
>
> **Roofline으로 번역하면**: fusion은 분자(연산량)를 그대로 두고 분모(메모리 이동량)를 줄여
> **X축 오른쪽으로 미는** 조작 — 메모리 사면에서 연산 지붕 쪽으로. → [[GPU architecture]]

## DE가 CUDA를 직접 쓰는가

**대개 쓰지 않는다.** 데이터 엔지니어는 [[NVIDIA RAPIDS]](cuDF, Spark RAPIDS)나 PyTorch를 통해
간접적으로 CUDA를 쓴다.

**그럼에도 알아야 하는 이유:**

| 알아야 할 것 | 왜 |
|---|---|
| **SIMT와 분기** | Python UDF·row 단위 조건문이 GPU ETL에서 왜 느린지 |
| **Shared Memory / HBM 계층** | 왜 데이터를 "GPU 위에 오래 유지"해야 하는지 |
| **Operator fusion** | 왜 중간 결과를 저장하지 않는 파이프라인이 빠른지 |
| **Block/Grid** | batch size와 chunking 설계가 왜 성능을 좌우하는지 |

## 생태계 구성 요소

컨테이너·Kubernetes 환경에서 GPU를 쓰려면 CUDA 런타임 외에 여러 층이 필요하다:

- **NVIDIA Container Toolkit** — 컨테이너에 GPU 노출
- **K8s device plugin** — `nvidia.com/gpu` 확장 리소스 광고
- **gpu-feature-discovery (GFD)** — 노드 label 자동 부착
- **GPU Operator** — 위 전부 + driver + MIG 관리를 묶어서

→ [[GPU resource allocation]]

## ⚠️ 이 위키에 아직 없는 것

- **CUDA 스트림과 비동기 실행** — H2D 전송과 계산을 겹치는 기법 (PCIe 병목 완화의 핵심)
- **메모리 종류** — pinned memory, unified memory의 실제 동작
- **cuDNN / cuBLAS** — 라이브러리 계층
- **warp divergence의 정확한 비용** — 강의는 "코어의 절반이 안 돈다"로 뭉뚱그리는데, 실제로는
  분기 경로 수만큼 직렬화되므로 절반보다 나쁠 수 있다
- **ROCm / SYCL 같은 대안** — GPU = NVIDIA를 전제한다

## 관련 페이지

- [[GPU architecture]] — 하드웨어 구조와 Roofline
- [[GPU resource allocation]] — 컨테이너·K8s에서의 GPU
- [[NVIDIA RAPIDS]] — DE가 실제로 쓰는 계층
- [[ONNX]] — operator fusion
- [[Inference optimization]] · [[NVIDIA Triton Inference Server]]

## 출처

- [[AI DE Course - Part4 Ch4 GPU architecture and CUDA]]

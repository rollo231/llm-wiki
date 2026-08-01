---
type: concept
title: GPU architecture
area: [data-engineering, programming]
aliases: [GPU 아키텍처, SIMT, SM, Streaming Multiprocessor, Roofline, Arithmetic Intensity, HBM, NVLink, coalescing]
tags: [data-engineering, gpu, cuda, simt, roofline, hbm, pcie, memory-bandwidth, operator-fusion]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch4 GPU architecture and CUDA]]"]
---

# GPU architecture

**왜 어떤 워크로드에서 GPU가 빠르고 어떤 워크로드에서는 오히려 느린가.**

> ⭐ **"데이터 엔지니어도 'GPU가 빠르다' 수준이 아니라 '왜 어떤 워크로드에서 빠른가'를 알아야
> 자원 배치와 파이프라인 설계가 가능하다."**

[[Inference optimization]]의 **"GPU는 마지막 수단"** 이라는 판단 규칙의 하드웨어적 근거다.

## ⭐ 설계 철학 — 실리콘 면적을 어디에 썼나

| | 목표 | 실리콘 면적 배분 |
|---|---|---|
| **CPU** (Latency Optimized) | **단일 스레드의 실행 속도를 극한으로** | **Control Logic & Deep Cache** — 분기 예측기, 비순차 실행(OoO), 거대한 L1/L2/L3 |
| **GPU** (Throughput Optimized) | 개별 스레드는 느려도 **단위 시간당 전체 작업량 극대화** | **Massive ALUs & SIMT** — 단순 연산 유닛으로 채우고 **컨트롤 로직을 버림** |

> ⭐ **GPU가 빠른 이유는 마법이 아니라 트랜지스터를 어디에 썼는가의 선택이다.**
> 컨트롤 로직을 버렸기 때문에 **분기가 많은 로직에서는 오히려 느리다.**
>
> **[[Latency and throughput]]의 "시소의 법칙"이 실리콘 수준에서 반복되는 형태다.**

**CPU와 GPU는 대체가 아니라 역할 분담이다** — CPU는 프로그램 흐름·입력 처리·스케줄링, GPU는
대규모 병렬 커널 실행. **host memory와 device memory는 분리되어 있다**
(Unified Memory가 있어도 역할 차이 자체는 남는다).

## 하드웨어 구조

### SM (Streaming Multiprocessor)

> **"GPU는 단순히 '코어가 많은 칩'이 아니라 'SM의 집합체'."**

- 스케줄러는 개별 코어가 아니라 **Warp(보통 32개 스레드 묶음)** 단위로 명령을 내린다
- 같은 SM의 스레드들은 **레지스터와 Shared Memory**(사용자가 제어 가능한 L1 캐시)를 공유한다
- **"이 공간을 활용해 글로벌 메모리(HBM) 접근을 최소화하는 것이 GPU 프로그래밍의 핵심"**

### 메모리 — 대역폭이 전부다

| | 뜻 |
|---|---|
| **HBM** (High Bandwidth Memory) | **계산 칩 바로 옆에 붙여 통로를 수천 개로 뚫어놓은 메모리.** SM으로 데이터를 가져오는 대역폭을 넓힘. **LLM 서빙의 핵심** |
| **NVLink** | 다수의 GPU를 고속으로 묶는 상호연결. PCIe보다 수 배~수십 배. **거대 모델이 한 GPU의 HBM에 안 들어갈 때 8대를 하나처럼** |

## ⭐⭐ DE에게 직접 닿는 두 가지

### 1. Coalescing — 왜 컬럼너 포맷이 GPU와 맞나

> ⭐ **"데이터가 메모리상에 흩어져 있으면(Random Access) GPU는 이를 가져오느라 시간을 낭비한다.
> 컬럼 기반(Columnar) 포맷인 Parquet, Arrow가 GPU와 어울리는 이유가 바로 연속된 메모리 접근이
> 가능하기 때문이다."**

**이것이 [[Columnar and in-memory data formats]]와 GPU 시대를 잇는 고리다.**
Parquet/Arrow를 "스캔 최적화 / 처리 최적화"로 알고 있었다면, 여기에 **"메모리 접근 병합"** 이라는
하드웨어 이유가 추가된다. [[NVIDIA RAPIDS]]의 cuDF가 Arrow 기반인 것도 이 때문이다.

> ⭐ **그리고 피해야 할 것: "행(Row)마다 다른 조건문(if-else)을 타는 쿼리."**
> 분기가 발생하면 GPU 코어가 놀게 된다(warp divergence). **row 단위 복잡 로직과 Python UDF가
> GPU ETL에 안 맞는 이유다.**

### 2. PCIe 병목 — 40~50배의 절벽

| 경로 | 대역폭 |
|---|---|
| **PCIe Gen4** (Host → Device) | **약 64 GB/s** (x16 양방향 합산) |
| **GPU 내부 HBM** | **2~3 TB/s** |

> ⭐ **"데이터를 변환하려고 GPU로 보냈다가 다시 CPU로 가져온다면, 정작 계산은 0.1초 만에 끝났는데
> 데이터 전송에 10초가 소요되는 문제."**

**이 절벽이 GPU 데이터 엔지니어링 전체의 근거다:**

- [[NVIDIA RAPIDS]]가 **"데이터를 가능한 한 GPU 위에 오래 유지"** 를 목표로 하는 이유
- Zero-copy로 PyTorch에 메모리 포인터만 넘기는 이유
- [[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]의
  **"GPU 사용률 낮음 + latency 높음 = 앞단 병목"** 이 성립하는 이유
- H100이 **PCIe Gen5 채택**을 주요 개선으로 내세우는 이유

## Operator Fusion

```python
C = A + B
D = C * 2
```

| | 동작 | 결과 |
|---|---|---|
| **비최적화** | 덧셈 커널 → HBM에서 A,B 읽고 **C를 HBM에 Write** → 곱셈 커널이 **C를 다시 Read** → D Write | **연산 시간보다 메모리 왕복 I/O가 더 커지는 Memory-Bound** |
| **최적화** | A,B를 **한 번만** 읽고 **레지스터에 결과를 둔 채** 덧셈·곱셈 연속 수행. `(A+B)*2` 단일 커널 | Global Memory 접근 **절반** → Arithmetic Intensity 상승 |

> **[[ONNX]]의 operator fusion이 왜 효과가 있는지의 메커니즘이 이것이다** — HBM 왕복 횟수 감소.

## Roofline Model — 병목이 연산인가 메모리인가

### Arithmetic Intensity

> **산술 집약도 = 연산량 / 메모리 이동량.** 1 Byte를 가져왔을 때 수행하는 연산(FLOPs) 횟수.

| | 결과 |
|---|---|
| **낮으면** | 가져오자마자 단순 처리만 → **코어는 놀고 메모리만 바쁨** |
| **높으면** | 한 번 가져온 데이터로 복잡한 계산 → **코어 100% 가동** |

### 차트 읽기

| 축 | 뜻 |
|---|---|
| **X축** | 산술 집약도 |
| **Y축** | 실제 처리 성능 |

> **사면(기울어진 선)에 부딪히면 메모리 병목, 지붕(평평한 선)에 부딪히면 연산 병목.**

**Operator Fusion은 분모(메모리 이동)를 줄여 X축 오른쪽으로 미는 조작이다** — 사면에서 지붕 쪽으로
옮긴다.

## ⭐ 실무 판단 — ETL은 메모리 집약이다

> ⭐⭐ **"Join이나 Sort 같은 ETL 작업은 코어 연산보다 메모리 이동이 극도로 많은 작업이다.
> T4는 고성능 HBM이 아닌 일반 GDDR 메모리를 사용하여 데이터 통로가 좁기 때문에, 이런 작업 시
> 메모리 대역폭 한계(Memory-bound)에 부딪혀 심각한 병목이 발생한다."**

**"저렴한 GPU를 ETL에 쓰면 되지 않나"에 대한 정확한 반박이다.** Roofline으로 번역하면:
**ETL은 산술 집약도가 낮아 사면에 부딪히고, 그 사면의 높이가 곧 메모리 대역폭이다.**
따라서 **ETL용 GPU는 FLOPs가 아니라 대역폭으로 골라야 한다.**

### GPU 스펙 — 대역폭 중심으로

| GPU | 아키텍처 | 메모리 / 대역폭 | DE 관점 추천 워크로드 | AWS / GCP |
|---|---|---|---|---|
| **T4** | Turing | 16GB **GDDR6** / ~320 GB/s | 마이크로 배치, 경량 추론 API. ⚠️ **대량 ETL 부적합** | g4dn / N1+T4 |
| **L4** | Ada Lovelace | 24GB GDDR6 / 300 GB/s | 중규모 전처리, 차세대 범용 | g6 / G2 |
| **A10G** | Ampere | 24GB GDDR6 / 600 GB/s | AWS 주력 범용 처리 | g5 / — |
| **A100** | Ampere | 40·80GB **HBM2e** / ~2 TB/s | **대용량 병렬 ETL(RAPIDS), 분산 학습.** MIG 최대 7 | p4d·p4de / A2 |
| **H100** | Hopper | 80GB **HBM3** / ~3.3 TB/s | 초거대 클러스터, LLM. **PCIe Gen5**, Transformer Engine | p5 / A3 |

**이 스펙들은 실제와 일치한다** (검증됨). 다만 **강의 시점 기준이라 Blackwell(B200) 세대가 빠져
있다** — 강의 자체도 MIG 지원 목록에는 B200을 넣으면서 이 표에는 넣지 않는 불일치가 있다.

## CUDA 프로그래밍 모델

논리 구조와 물리 구조가 1:1로 대응한다. 상세는 [[CUDA]].

| 소프트웨어 | 하드웨어 |
|---|---|
| **Thread** | GPU 코어 |
| **Block** | **SM** |
| **Grid** | GPU 디바이스 전체 |

**SIMT** (Single Instruction, Multiple Threads) — 수백 개 스레드가 **동일한 명령**을 받되
**서로 다른 데이터**를 계산한다.

## 관련 페이지

- [[CUDA]] — 프로그래밍 모델 상세
- [[GPU resource allocation]] — 이 하드웨어를 어떻게 나눠 쓸 것인가 (MIG·MPS·time-slicing)
- [[NVIDIA RAPIDS]] — GPU 위에서 데이터를 처리하는 도구군
- [[Inference optimization]] — **"GPU는 마지막 수단"** 의 판단 규칙
- ⭐ [[Columnar and in-memory data formats]] — **coalescing 때문에 Parquet·Arrow가 GPU와 맞는다**
- [[ONNX]] — operator fusion
- [[Latency and throughput]] — 시소의 법칙의 실리콘 버전
- [[Distributed processing]] — 노드 간 분산과 같은 트레이드오프가 GPU 안에서도 반복된다

## 출처

- [[AI DE Course - Part4 Ch4 GPU architecture and CUDA]]

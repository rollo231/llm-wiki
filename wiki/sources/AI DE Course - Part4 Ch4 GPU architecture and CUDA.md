---
type: source
title: AI DE Course - Part4 Ch4 GPU architecture and CUDA
area: [data-engineering, programming]
aliases: [Part4 Ch4-1,2, GPU 아키텍처란 CPU와의 차이, Roofline Model]
tags: [data-engineering, course, fast-campus, gpu, cuda, simt, roofline, hbm, nvlink, operator-fusion]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf (p241–277)"]
---

# AI DE Course - Part4 Ch4 GPU architecture and CUDA

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 4** Ch4 "GPU 워크로드 전략"의 소단원
**1 "GPU 아키텍처란? CPU와의 차이1"** + **2 "…차이2"**. 제목이 같은 연속 소단원이라 한 페이지로
묶었다. 원본(로컬): `raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` **p241–277** (356p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐ **Part 2의 [[AI DE Course - Part2 Ch4 CPU and GPU inference]]가 "GPU는 마지막 수단"이라는 판단
> 규칙이었다면, 여기는 "왜 그런가"의 하드웨어적 근거다.** 실리콘 면적 배분 → SIMT → 메모리 대역폭 →
> PCIe 병목 → Roofline으로 이어지는 논리가 깔끔하다.

## 구성

소단원 1: `01 GPU 구조를 알아야 하는 이유 · 02 CPU와 GPU · 03 CUDA · 04 예시로 CUDA 이해하기`
소단원 2: `01 GPU 성능의 핵심 원리 · 02 Roofline Model · 03 모던 GPU 아키텍처`

## ⭐ 왜 DE가 GPU 구조를 알아야 하나

> **"데이터 엔지니어도 'GPU가 빠르다' 수준이 아니라 '왜 어떤 워크로드에서 빠른가'를 알아야 자원
> 배치와 파이프라인 설계가 가능."**

강의가 든 촌극이 정확하다:

> *"저희 추천 서비스 해야 하는데 GPU가 필요해요, A100 주세요"*
> → *"(A100이 뭐지?) 네 드릴게요"*
> → **"모델 크기가 어떻게 되시나요?"**

**CPU와 GPU는 대체가 아니라 역할 분담이다:**

- **CPU**: 전체 프로그램 흐름, 입력 처리, 스케줄링, 운영체제와의 상호작용
- **GPU**: 대규모 병렬 계산 커널 실행
- **host memory와 device memory가 분리**되어 있으며 협업 구조
- **"Unified Memory 같은 기능이 있어도 아키텍처 역할 차이 자체가 사라지는 것은 아니다"**

## ⭐ 설계 철학 — Latency vs Throughput

| | 목표 | 실리콘 면적 배분 |
|---|---|---|
| **CPU** (Latency Optimized) | **단일 스레드의 실행 속도(응답 지연)를 극한으로 줄이는 것** | **Control Logic & Deep Cache Hierarchy** — 분기 예측기, 비순차적 실행(Out-of-Order) 로직, 거대한 L1/L2/L3 캐시 |
| **GPU** (Throughput Optimized) | 개별 스레드는 다소 느리더라도 **단위 시간당 전체 작업량을 극대화** | **Massive ALUs & SIMT** — 단순한 연산 유닛으로 채우고 **컨트롤 로직을 버림** |

> ⭐ **"실리콘 면적 할당 차이"** 라는 프레이밍이 이 소단원의 핵심이다. GPU가 빠른 이유는 마법이
> 아니라 **트랜지스터를 어디에 썼는가의 선택**이고, 그래서 **분기가 많은 로직에서는 오히려 느리다.**
>
> **이것이 Part 1 [[Latency and throughput]]의 "시소의 법칙"이 실리콘 수준에서 반복되는 것이다.**

### SM (Streaming Multiprocessor)

> **"GPU는 단순히 '코어가 많은 칩'이 아니라 'SM의 집합체'."**

- **동작 방식**: GPU 내부 스케줄러는 개별 코어가 아니라 **Warp(보통 32개의 스레드 묶음)** 단위로
  명령을 내림
- **자원 공유**: 같은 SM에 할당된 스레드들은 **레지스터와 Shared Memory**(사용자가 직접 제어 가능한
  L1 캐시 역할)를 공유
- **"이 공간을 활용해 글로벌 메모리(DRAM/HBM) 접근을 최소화하고 커널 성능을 최적화하는 것이
  GPU 프로그래밍(CUDA)의 핵심"**

### 메모리 계층 비교

CPU 쪽은 캐시를 학교 비유로 설명한다 — L1 = 교수님 책상 위(가장 빠르고 가장 작음), L2 = 개인
책장, L3 = 학과 공용 자료실, DRAM = **"거대한 중앙 도서관"**.

GPU 쪽에서 그림에 없는 두 요소를 따로 짚는 게 좋다:

| | 뜻 |
|---|---|
| **HBM** (High Bandwidth Memory) | **계산 칩 바로 옆에 찰싹 붙여서 통로를 수천 개로 뚫어놓은 메모리.** 메모리 병목을 해결하기 위해 SM으로 데이터를 가져오는 대역폭을 매우 넓힘. **LLM 서빙에 주로 활용** |
| **NVLink** | 다수의 GPU를 고속으로 묶는 상호연결. PCIe보다 수 배~수십 배 빠름. **"LLM 모델들은 거대해서 한 대의 GPU 메모리(HBM)에 들어갈 수 없다"** — 8대의 GPU가 하나의 거대한 GPU처럼 작동 |

## CUDA

> **"GPU 안에는 수천 개의 코어(ALU)가 존재하지만, 작성하는 Python·C++ 코드는 기본적으로 CPU가 읽고
> 처리하도록 만들어진 직렬 언어. CUDA는 이 간극을 메우는 지휘 체계이자 통역사."**

### The Core Mapping — 논리 구조 ↔ 물리 구조 1:1

| 소프트웨어 | 하드웨어 |
|---|---|
| **스레드 (Thread)** | **GPU 코어** — 가장 작은 실행 단위 하나가 코어 하나에 할당 |
| **블록 (Thread Block)** | **SM** — 여러 스레드를 묶은 논리적 단위가 SM에 통째로 할당 |
| **그리드 (Grid)** | **GPU 디바이스 전체** — 여러 블록을 묶은 단위. GPU에 특정 연산을 던질 때 생성되는 전체 작업 덩어리 |

### 커널과 SIMT

| | 뜻 |
|---|---|
| **커널 (Kernel)** | CPU(Host)에서 호출하지만 실제 코드는 GPU(Device)의 수많은 스레드에서 **동시에 병렬로 실행되는 함수** |
| **SIMT** (Single Instruction, Multiple Threads) | 수백 개의 스레드가 **완전히 동일한 명령**을 받지만 각자 **서로 다른 데이터**를 들고 계산. 예: *"각자의 위치에 있는 숫자에 2를 곱해라"* |

### ⭐ PyTorch 한 줄로 따라가기

```python
A = torch.randn(100000).cuda()
B = torch.randn(100000).cuda()
C = A + B          # 이 한 줄이 실행될 때 GPU에서는?
```

| 단계 | 일어나는 일 |
|---|---|
| **CPU라면** | 코어 하나가 A[0]+B[0], A[1]+B[1]… **10만 번의 덧셈을 순서대로** |
| **CUDA 커널 배포** | `.cuda()`가 붙어 있어 이 덧셈이 **CUDA 커널로 변환**. 10만 개의 작업자(Thread)에 대해 각자 자기 번호표(ID)에 맞는 데이터 1개씩만 더하라는 명령 |
| **Thread → Core** | '스레드 #505번'은 코어 하나에 배정 → **"HBM에서 A[505]와 B[505]를 가져와 더한 뒤 C[505]에 Write"** 만 수행. 10만 명의 코어가 동시에 1번씩 |
| **Block → SM** | CUDA는 스레드를 **1,024개씩** 묶어 한 블록으로. 같은 SM의 1,024개 스레드는 **L1 캐시(Shared Memory)를 공유** → 평균을 구하거나 데이터를 교환할 때 **HBM까지 안 가고** 캐시에서 주고받음 |
| **Grid → GPU 전체** | 블록 약 100개가 모이면 10만 개(그리드). **이 블록 100개가 A100 안의 108개 SM에 전달**되면서 동시에 연산 시작 |

> ⭐ **"A100의 108개 SM"** 같은 구체적 숫자가 나오는 게 좋다. 추상적 설명이 실제 칩 스펙에 착지한다.
> (A100의 SM 수는 실제로 108개 — 검증됨)

### ⭐ Operator Fusion

```python
C = A + B
D = C * 2
```

| | 동작 | 결과 |
|---|---|---|
| **비최적화** | ① 덧셈 커널 호출 → HBM에서 A,B 읽기 → 연산 → **C를 HBM에 Write** ② 곱셈 커널 새로 호출 → **HBM에서 C 다시 Read** → 연산 → D Write | **실제 연산 시간보다 Global Memory 왕복 I/O가 더 커지는 Memory-Bound 발생** |
| **최적화** | HBM에서 A,B를 **한 번만** 읽고, 코어 내부 **레지스터에 결과를 둔 상태로** 덧셈과 곱셈을 연속 수행. `(A+B)*2` 형태의 **단일 커널** 생성 | Global Memory 접근이 **절반으로** → **Arithmetic Intensity 비약적 상승** |

> **[[ONNX]]의 operator fusion(Part 2 Ch4)이 여기서 왜 효과가 있는지 설명된다.**
> Part 2는 "operator fusion으로 빨라진다"까지였고, 여기는 **VRAM I/O 왕복 횟수가 줄기 때문**이라는
> 메커니즘을 준다. 두 파트가 잇지 않지만 같은 이야기다.

---

## ⭐ GPU 성능의 핵심 원리 — DE에게 직접 닿는 부분

### 데이터는 모아서(Batch), 정렬해서(Coalescing)

> ⭐ **"데이터 엔지니어링 관점에서 가장 피해야 할 것은 '행(Row)마다 다른 조건문(if-else)'을 타는
> 쿼리. 분기가 발생하면 GPU 코어의 절반은 가동되지 않는다."** (warp divergence)

> ⭐⭐ **"메모리 접근 병합(Coalescing): 데이터가 메모리상에 흩어져 있으면(Random Access) GPU는 이를
> 가져오느라 시간을 낭비한다. 컬럼 기반(Columnar) 포맷인 Parquet, Arrow가 GPU와 어울리는 이유가
> 바로 연속된 메모리 접근이 가능하기 때문이다."**
>
> **이 문장이 Part 1과 Part 4를 잇는 최고의 연결이다.** [[Columnar and in-memory data formats]]에서
> Parquet/Arrow를 "스캔 최적화 / 처리 최적화"로 배웠는데, **GPU 시대에 컬럼너가 왜 다시 중요한지**를
> coalescing이라는 하드웨어 이유로 설명한다. Ch4-5의 RAPIDS가 Arrow 기반인 것도 이 때문이다.

### ⭐ 데이터 파이프라인의 최대 병목 — PCIe

> **"CPU가 쓰는 메모리(Host RAM)와 GPU가 쓰는 메모리(Device VRAM)는 완전히 분리됨."**

| 경로 | 대역폭 |
|---|---|
| **PCIe Gen4** (Host → Device) | **약 64 GB/s** |
| **GPU 내부 HBM** | **2~3 TB/s** |

> ⭐ **"데이터를 변환하려고 GPU로 보냈다가 다시 CPU로 가져온다면, 정작 계산은 0.1초 만에 끝났는데
> 데이터 전송에 10초가 소요되는 문제."**

**약 40~50배 차이가 이 챕터 전체의 근거다** — Ch4-5의 RAPIDS가 "GPU 위에 데이터를 오래 유지"를
목표로 하는 이유, Ch4-3의 MIG/NVLink 논의, Ch5의 "GPU 사용률 낮음 + latency 높음 = 앞단 병목"이
모두 여기서 나온다.

> **수치 검증:** PCIe Gen4 x16은 방향당 ~32 GB/s, 양방향 합산 ~64 GB/s다. 강의의 64 GB/s는
> **양방향 합산 기준**으로 읽어야 맞다. HBM 2~3 TB/s는 A100(~2 TB/s)·H100(~3.35 TB/s)과 일치한다.

## Roofline Model

### Arithmetic Intensity 먼저

> **산술 집약도 = 연산량 / 메모리 이동량.** 메모리에서 1 Byte를 가져왔을 때 GPU 코어가 수행하는
> 연산(FLOPs)의 횟수.

| | 결과 |
|---|---|
| **낮으면** | 데이터를 가져오자마자 단순 처리만 수행 → **코어는 놀고 메모리만 바빠짐** |
| **높으면** | 한 번 가져온 데이터로 복잡한 계산 수행 → **코어가 100% 가동** |

### 병목 진단

> **Roofline 모델은 파이프라인의 병목이 '연산 능력(Compute)'에 막혔는지 '메모리 전송
> 속도(Memory)'에 막혔는지 보여주는 차트.**

| 축 | 뜻 |
|---|---|
| **X축** | 산술 집약도 (1 Byte를 가져와서 몇 번 연산하는가?) |
| **Y축** | 실제 처리 성능 |

> **사면(기울어진 선)에 부딪히면 메모리 병목, 지붕(평평한 선)에 부딪히면 연산 병목.**

> ⭐ **Operator Fusion이 왜 효과적인지가 Roofline으로 설명된다** — fusion은 분자(연산량)를 그대로
> 두고 분모(메모리 이동량)를 줄여 **X축 오른쪽으로 밀어내는** 조작이다. 강의가 이 연결을 명시하지는
> 않지만 두 절이 나란히 배치된 이유가 그것으로 보인다.

## 모던 GPU 아키텍처 — 스펙 비교

> **"GPU 종류에 따라 인프라 비용이 수십 배 차이."**

| GPU | 아키텍처 | 스펙 | 특징 |
|---|---|---|---|
| **T4** | Turing | 16GB **GDDR6** / ~320 GB/s / 70W | 비용 효율 극대화된 **추론 전용**. ⚠️ **"Join·Sort 같은 ETL 작업은 메모리 이동이 극도로 많은 작업. T4는 HBM이 아닌 GDDR을 써서 데이터 통로가 좁아 Memory-bound에 부딪혀 심각한 병목 발생"** |
| **L4** | Ada Lovelace | 24GB GDDR6 / 300 GB/s | T4의 한계(메모리 부족, 구형)를 극복한 차세대 가성비. 비디오/이미지 처리, 중소규모 서빙 |
| **A10G** | Ampere | 24GB GDDR6 / 600 GB/s | AWS에서 범용 AI 서빙·중규모 처리에 가장 널리 쓰이는 미드레인지 |
| **A100** | Ampere | 40/80GB **HBM2e** / ~2 TB/s | **대용량 데이터 파이프라인(RAPIDS) 및 분산 학습의 표준 워크호스.** **MIG로 최대 7개 인스턴스 격리** |
| **H100** | Hopper | 80GB **HBM3** / ~3.3 TB/s | A100 대비 대역폭 비약적 상승. **PCIe Gen5로 Host-to-Device 병목 대폭 완화.** **Transformer Engine** 탑재 |

| 구분 | 추천 워크로드 (DE 관점) | AWS | GCP |
|---|---|---|---|
| T4 | 마이크로 배치, 경량 추론 API | g4dn | N1 + T4 |
| L4 | 중규모 데이터 전처리, 차세대 범용 | g6 | G2 |
| A10G | AWS 주력 범용 처리 장비 | g5 | — |
| A100 | **대용량 병렬 ETL (RAPIDS), 분산 학습** | p4d / p4de | A2 |
| H100 | 초거대 스케일 클러스터, LLM 처리 | p5 | A3 |

> ⭐⭐ **T4 항목이 이 표의 백미다.** "저렴한 GPU를 ETL에 쓰면 되지 않나"에 대한 정확한 반박 —
> **ETL은 연산 집약이 아니라 메모리 집약이므로 GDDR 기반 저가 GPU에서는 오히려 병목**이다.
> Roofline과 연결하면: **ETL은 산술 집약도가 낮아 사면(메모리 한계선)에 부딪히고, 그 사면의 높이가
> 곧 대역폭이다.** 논리가 일관된다.
>
> **이 스펙들은 검증했다 — 실제와 맞는다** (T4 320GB/s, L4 300GB/s, A10G 600GB/s,
> A100 80GB HBM2e ~2TB/s, H100 SXM HBM3 ~3.35TB/s, MIG 최대 7개). **Part 1의 출처 없는 "80%"와
> 대비되는 품질이다.**

## 기존 페이지와의 대조

- **새 concept:** [[GPU architecture]]
- **새 entity:** [[CUDA]]
- **[[Inference optimization]](Part 2 Ch4) 보강** — "GPU는 마지막 수단"의 근거가 여기 있다.
  Roofline과 PCIe 병목을 추가해야 한다.
- ⭐ **[[Columnar and in-memory data formats]](Part 1) 보강** — **coalescing 때문에 Parquet/Arrow가
  GPU와 맞는다**는 연결이 새롭다. 이 위키에서 Part 1과 Part 4를 잇는 가장 강한 고리.
- **[[ONNX]]** — operator fusion의 메커니즘(HBM 왕복 감소).
- **[[Latency and throughput]]** — 시소의 법칙이 실리콘 면적 배분으로 반복된다.

## 자료 품질

**Part 4에서 GPU 스펙 정확도가 가장 좋은 소단원.**

- ✅ **GPU 스펙 5종이 모두 실제와 일치** (대역폭·메모리·MIG 개수·클라우드 인스턴스 매핑)
- ✅ A100의 SM 108개 같은 구체적 숫자
- ✅ **PyTorch 한 줄 → 커널 → 스레드/블록/그리드**로 내려가는 설명이 단계적
- ✅ **Coalescing → Columnar 포맷** 연결이 DE 관점에서 정확
- ✅ Operator Fusion 전/후 비교가 명확
- ⚠️ **PCIe Gen4 "고작 64GB/s"** — 양방향 합산 기준이라는 단서가 없다. 단방향 기준(~32GB/s)과
  혼동할 수 있다
- ⚠️ **Roofline 차트 슬라이드(p269·p270)가 이미지 전용**이라 축과 꺾이는 지점 설명이 텍스트에 없다
- ⚠️ **warp divergence를 "코어의 절반이 안 돈다"로 뭉뚱그린다** — 실제로는 분기 경로 수만큼 직렬화
  되므로 절반보다 나쁠 수 있다
- ⚠️ **B200/Blackwell 세대가 없다.** 2026년 시점에 H100이 최신으로 제시되는 것은 시의성이 떨어진다
  (Ch4-3의 MIG 지원 목록에는 B200이 나오는데 이 표에는 없다 — **파트 내부 불일치**)

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[GPU architecture]] · [[Inference optimization]] · [[Latency and throughput]] ·
  [[Columnar and in-memory data formats]] · [[GPU resource allocation]]
- 도구: [[CUDA]] · [[ONNX]] · [[NVIDIA RAPIDS]]
- 앞: [[AI DE Course - Part4 Ch3 Lambda Kappa and modern architecture]]
- 다음: [[AI DE Course - Part4 Ch4 GPU allocation architecture]]

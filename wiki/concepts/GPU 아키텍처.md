---
type: concept
title: GPU 아키텍처
aliases: [GPU, GPU architecture, CUDA, SIMT, SM, Streaming Multiprocessor, Warp, 워프, Roofline, Roofline model, 루프라인 모델, 산술 집약도, Arithmetic intensity, 연산 융합, Operator fusion, Kernel fusion, HBM, NVLink]
tags: [GPU, 하드웨어, 성능]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 4-11 GPU 아키텍처와 CUDA]]"
  - "[[AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용]]"
  - "[[AI DE 강의 4-14 RAPIDS 가속 ETL]]"
---

# GPU 아키텍처

GPU는 같은 전력·비용 범위에서 CPU보다 훨씬 높은 연산 처리량과 메모리 대역폭을 내도록 설계된 가속기다. [[AI DE 강의 4-11 GPU 아키텍처와 CUDA]]는 데이터 엔지니어가 "GPU가 빠르다"가 아니라 어떤 워크로드에서 왜 빠른지 알아야 자원 배치와 파이프라인 설계를 할 수 있다고 한다(p243). 이 페이지는 강의의 설명과 1차 자료로 고친 부분을 함께 모은다. GPU를 여러 작업에 나눠 주는 문제는 [[GPU 할당과 스케줄링]]에 있다.

## CPU와 GPU: 지연 시간 대 처리량

강의는 두 칩의 설계 철학을 [[지연 시간과 처리량]]의 대비로 설명한다(p245).

| | CPU | GPU |
|---|---|---|
| 목표 | 단일 스레드의 응답 지연을 줄인다 | 단위 시간당 전체 처리량을 늘린다 |
| 실리콘을 쓰는 곳 | 분기 예측기, 비순차 실행 로직, 큰 L1/L2/L3 캐시 | 단순한 연산 유닛(ALU)을 많이, 제어 로직은 적게 |
| 실행 방식 | 복잡한 조건문과 순차 논리에 강하다 | 같은 명령을 여러 스레드가 서로 다른 데이터에 실행한다(SIMT) |
| 역할 | 프로그램 흐름, 입력 처리, 스케줄링, OS와의 상호작용 | 대규모 병렬 계산 커널 실행 |

CPU와 GPU는 대체 관계가 아니라 협업 관계이고, 기본적으로 host memory와 device memory가 분리돼 있다. Unified Memory가 있어도 역할 차이는 사라지지 않는다(p244).

## SM, 워프, 메모리 계층

GPU는 코어가 많은 칩이라기보다 SM(Streaming Multiprocessor)의 집합이다(p246). 스케줄러는 개별 코어가 아니라 32개 스레드 묶음인 워프(warp) 단위로 명령을 낸다. 같은 블록의 스레드는 SM의 shared memory를 함께 쓰고, 레지스터는 SM의 레지스터 파일에서 스레드마다 따로 받는다. CUDA 문서는 "Within a thread block, threads are organized into groups of 32 threads called warps", "The shared memory is accessible by all threads within a thread block or cluster"라고 적는다. 강의는 shared memory를 SM의 스레드들이 공유한다고 쓰는데, 보이는 범위는 SM 전체가 아니라 블록(또는 클러스터)이다. [https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html , 2026-09-28 확인]

메모리는 레지스터 → shared memory·L1 → L2 → DRAM(HBM 또는 GDDR) 순서로 멀고 크고 느려진다. 강의는 CPU 캐시를 교수님 책상·개인 책장·학과 자료실에, DRAM을 중앙 도서관에 비유한다(p248–249). HBM은 칩 바로 옆에 붙여 통로를 수천 개로 넓힌 DRAM이고, NVLink는 여러 GPU를 PCIe보다 빠르게 잇는 연결이다(p252). H100 SXM 기준으로 NVLink 900 GB/s 대 PCIe Gen5 128 GB/s(둘 다 양방향 합계)라 약 7배다. [https://www.nvidia.com/en-us/data-center/h100/ , 2026-09-28 확인]

## 스레드 계층과 하드웨어 대응 (정정)

CUDA의 소프트웨어 계층은 스레드 → 블록 → 그리드다. 커널은 CPU(host)가 호출하지만 GPU(device)의 많은 스레드에서 병렬로 실행되는 함수다(p255).

강의는 이 계층을 하드웨어에 "정확히 1:1로 대응"시킨다고 설명한다(p254). 스레드 → 코어, 블록 → SM, 그리드 → GPU 전체다. 예시에서는 `C = A + B`(원소 10만 개)를 스레드 10만 개로 쪼개고 "10만 명의 코어가 동시에 1번씩만 덧셈"한다고 한다(p258). 1차 자료와 대조하면 셋 가운데 둘이 틀리다.

| 강의의 설명 | 실제 | 판정 |
|---|---|---|
| 스레드 1개 = CUDA 코어 1개, 10만 스레드가 동시에 한 번씩 덧셈(p254·258) | 워프가 SM 스케줄러에 올라 번갈아 실행된다(SIMT). A100은 SM 108개, FP32 코어 6,912개, SM당 상주 스레드 최대 2,048개다. 10만 스레드는 한꺼번에 상주할 수는 있지만 동시에 도는 FP32 연산은 최대 6,912개다 | ❌ |
| 블록 → SM(p254·259) | 블록 하나는 SM 하나에서 돈다. SM 하나에는 자원이 허락하면 여러 블록이 동시에 올라간다 | ✅ (단서) |
| "CUDA는 스레드들을 1,024개씩 묶어서 한 블록으로" 만든다(p259) | 1,024는 기본값이 아니라 블록당 상한이다. 블록 크기는 커널을 띄우는 쪽이 정한다 | ❌ |
| 같은 SM의 1,024 스레드가 shared memory를 공유하므로 "10만 개 전체의 평균"을 HBM까지 가지 않고 구할 수 있다(p259) | shared memory는 블록 안에서만 보인다. 전체 평균은 블록별 부분합을 전역 메모리에 쓰고 두 번째 커널이나 atomic으로 합쳐야 한다 | ❌ |

근거: NVIDIA Ampere 아키텍처 블로그("108 SMs", "6912 FP32 CUDA Cores per GPU", "Max Threads / SM 2048"), CUDA Programming Guide("a thread block may contain up to 1024 threads", "If resources allow, more than one thread block can be scheduled on an SM simultaneously"). [https://developer.nvidia.com/blog/nvidia-ampere-architecture-in-depth/ · https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/intro-to-cuda-cpp.html , 2026-09-28 확인]

PyTorch가 이 덧셈을 실제로 어떻게 띄우는지도 강의와 다르다. 강의에는 수치가 없어 검증 과정에서 PyTorch 소스(`main`, 2026-09)를 확인했다. `thread_constants.h`의 `num_threads()`는 `C10_WARP_SIZE * 4`(= 128)이고 `thread_work_size()`는 8(CUDA 기준, ROCm은 4)이다. 벡터화 경로에서는 float32를 128비트 로드로 4개씩 읽는다. 그래서 float32 덧셈의 블록 하나는 128 스레드 × 8 = 1,024개 원소를 맡고, 10만 원소는 블록 98개쯤이 된다. 블록 수는 강의의 "약 100개"(p260)와 비슷하지만 스레드 수는 1/8이다. 옛 버전은 thread_work_size가 4였으므로 이 수치는 버전을 붙여 읽는다. [https://github.com/pytorch/pytorch/blob/main/aten/src/ATen/native/cuda/CUDALoops.cuh , 2026-09-28 확인]

## 연산 융합 (정정)

강의의 예시(p261–262)는 `C = A + B; D = C * 2`다. 융합하지 않으면 덧셈 커널과 곱셈 커널이 따로 뜨고, 중간 결과 C가 전역 메모리(HBM)를 왕복한다. 융합하면 `(A + B) * 2`를 한 커널에서 레지스터에 둔 채 계산하고 D만 쓴다.

강의는 이것으로 전역 메모리 접근이 "절반"으로 줄어든다고 한다. 텐서 크기 단위로 세면 융합 전은 A 읽기, B 읽기, C 쓰기, C 읽기, D 쓰기로 5회이고, 융합 후는 A 읽기, B 읽기, D 쓰기로 3회다. 줄어드는 폭은 40%이고, 절반이 되는 것은 커널 실행 횟수(2 → 1)다.

강의는 누가 융합하는지를 말하지 않는다. PyTorch eager 모드는 연산마다 커널을 따로 띄우고, 이런 융합은 `torch.compile`(TorchInductor가 Triton 커널을 생성) 같은 컴파일러가 한다. PyTorch 튜닝 가이드는 "PyTorch eager-mode initiates a separate kernel for each operation"이라고 적는다. [https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html , 2026-09-28 확인] 여기서 Triton은 OpenAI의 커널 언어이고 NVIDIA의 [[Triton Inference Server]]와는 다른 것이다. 서빙 쪽 최적화 순서는 [[추론 최적화]]에 있다.

## 메모리 병목: 병합 접근, 분기, PCIe

[[AI DE 강의 4-11 GPU 아키텍처와 CUDA]] 소단원 2는 GPU 성능 원리를 데이터 엔지니어링 쪽으로 옮긴다(p265–266).

- 분기: 워프 안의 스레드가 행마다 다른 if-else를 타면 일부 스레드가 쉰다. 행마다 조건이 갈리는 로직은 GPU에 맞지 않는다.
- 병합 접근(coalescing): 워프의 스레드들이 연속된 주소를 읽어야 메모리 트랜잭션이 적다. 강의는 Parquet·Arrow 같은 열 기반 포맷이 GPU와 어울리는 이유를 여기서 찾는다([[행 기반과 열 기반 저장]]).
- PCIe 병목: host RAM과 device VRAM은 분리돼 있어서, 데이터를 GPU로 보냈다가 CPU로 되가져오는 변환은 계산보다 전송이 오래 걸린다. 강의는 "PCIe Gen4 64GB/s" 대 "HBM 2~3TB/s"를 비교한다. 다만 64 GB/s는 PCIe 4.0 x16의 양방향 합계이고 한 방향은 약 32 GB/s다. HBM 수치와 나란히 놓으면 PCIe가 실제보다 두 배 좋아 보인다. [https://www.nvidia.com/en-us/data-center/a100/ ("PCIe Gen4: 64 GB/s"), 2026-09-28 확인]

## Roofline 모델과 산술 집약도

산술 집약도(arithmetic intensity)는 메모리에서 1바이트를 가져올 때마다 하는 연산(FLOPs) 수다. Roofline 차트는 x축에 산술 집약도, y축에 달성 성능을 두고, 기울어진 선(메모리 대역폭 한계)에 걸리면 메모리 병목, 평평한 지붕(연산 한계)에 걸리면 연산 병목으로 읽는다(p267–268). 조인·정렬·필터 같은 ETL 연산은 산술 집약도가 낮아 대부분 메모리 병목 쪽에 있다. 그래서 강의는 GDDR 메모리를 쓰는 T4가 조인·정렬 ETL에서 대역폭 한계에 부딪힌다고 한다(p272). ETL과 메모리 병목의 연결은 강의의 서술이고, "대부분"이라는 일반화는 위키가 강의의 예시에서 끌어낸 것이다.

## GPU 사양 (정정·보충)

강의의 사양 표(p272–277)를 1차 자료로 고친 것이다.

| GPU | 아키텍처 | 메모리 | 대역폭 | 강의의 추천 워크로드 | AWS | GCP |
|---|---|---|---|---|---|---|
| T4 | Turing | 16GB GDDR6 | 320+ GB/s, 70W | 마이크로 배치, 경량 추론 API | g4dn | N1 + T4 |
| L4 | Ada Lovelace | 24GB GDDR6 | 300 GB/s, 72W | 중규모 전처리, 비디오·이미지, 중소 모델 서빙 | g6 | G2 |
| A10G | Ampere | 24GB GDDR6 | 600 GB/s | AWS의 범용 미드레인지 | g5 | (L4로 대체) |
| A100 40GB | Ampere | 40GB HBM2 | 1,555 GB/s | 대용량 병렬 ETL(RAPIDS), 분산 학습 | p4d | A2 Standard |
| A100 80GB | Ampere | 80GB HBM2e | 1,935(PCIe)·2,039(SXM) GB/s | 같음 | p4de | A2 Ultra |
| H100 SXM | Hopper | 80GB HBM3 | 3.35 TB/s | 초거대 클러스터, LLM | p5 | A3 |
| H100 PCIe | Hopper | 80GB HBM2e | 2 TB/s | — | — | — |

- ❌ 강의는 A100을 "40GB 또는 80GB HBM2e, 약 2TB/s"로 적는다(p275). 40GB판은 HBM2 1,555 GB/s다.
- ⚠️ H100의 "80GB HBM3, 약 3.3TB/s"(p276)는 SXM판 수치다. PCIe판은 HBM2e 2 TB/s이고 NVL판은 94GB 3.9 TB/s다. 현재 A100·H100 제품 페이지에는 A100 40GB와 H100 PCIe 사양이 빠져 있어서, 40GB판(HBM2, 1,555GB/s)은 A100 데이터시트(nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf)로, H100 PCIe판(HBM2e, 2,000 GB/s)은 H100 PCIe Product Brief(PB-11133-001)로 확인했다. [https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf · https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf , 2026-09-28 확인]
- A10G는 AWS 전용 변형이라 NVIDIA 공식 데이터시트가 없다. 수치는 NVIDIA 블로그와 AWS 발표에 기댄다.
- 출처: NVIDIA 제품 페이지(T4 · L4 · A100 · H100), NVIDIA 블로그 「AWS Brings NVIDIA A10G Tensor Core GPUs to the Cloud with New EC2 G5 Instances」, Google Cloud GPU 문서. [https://www.nvidia.com/en-us/data-center/tesla-t4/ · https://www.nvidia.com/en-us/data-center/l4/ · https://www.nvidia.com/en-us/data-center/a100/ · https://www.nvidia.com/en-us/data-center/h100/ · https://developer.nvidia.com/blog/aws-brings-nvidia-a10g-tensor-core-gpus-to-the-cloud-with-new-ec2-g5-instances/ · https://docs.cloud.google.com/compute/docs/gpus , 2026-09-28 확인]

⚠️ 강의의 표는 H100에서 멈춘다. 슬라이드 작성 시점(2026-05)에 AWS에는 이미 H200(P5e 2024-09-09, P5en 2024-12-02), B200(P6-B200 2025-05-15), GB200(P6e-GB200 2025-07), B300(P6-B300 2025-11), GB300(P6e-GB300 2025-12)이 나와 있었다. GCP도 A3 Ultra(H200), A4(B200), A4X(GB200)를 제공한다. GCP의 GA 날짜는 검증에서 확인하지 못했다. [https://aws.amazon.com/about-aws/whats-new/2025/11/amazon-ec2-p6-b300-instances-nvidia-blackwell-ultra-gpus-available/ · https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-ec2-p6e-gb300-ultraservers-nvidia-gb300-nvl72-generally-available , 2026-09-28 확인] 같은 강의의 MIG 슬라이드(p286)는 H200·B200을 언급하므로 사양 표만 뒤처진 것이다.

## GPU 사용률은 무엇을 재는가

위키가 덧붙이는 단서다. nvidia-smi와 NVML의 "GPU utilization"은 SM이 얼마나 바쁜지가 아니라 표본 구간 가운데 커널이 하나라도 돌던 시간의 비율이다. NVML 문서는 "Percent of time over the past sample period during which one or more kernels was executing on the GPU"라고 정의한다. 그래서 작은 커널 하나가 계속 돌기만 해도 100%가 나올 수 있다. SM이 실제로 얼마나 차 있는지는 DCGM의 `DCGM_FI_PROF_SM_ACTIVE`("The fraction of time at least one warp was active on a multiprocessor, averaged over all multiprocessors")와 SM occupancy로 본다. [https://docs.nvidia.com/deploy/nvml-api/api/structnvmlUtilization__t.html · https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/feature-overview.html , 2026-09-28 확인] 강의의 사용률 × 대기열 × 지연 해석 표([[AI DE 강의 4-17 병목 파악과 트러블슈팅]])를 읽을 때 이 정의를 함께 둔다.

## 데이터 엔지니어링에서

GPU가 잘 맞는 일과 오히려 나빠지는 일의 판단 기준은 [[AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용]](p307–309, p322–324)에, GPU ETL 도구는 [[RAPIDS]]에 있다. 공통 조건은 데이터가 충분히 크고, 병렬성이 높고, 연산 패턴이 규칙적이고, 이동 비용보다 계산 이득이 큰 경우다. 이 페이지의 아키텍처 설명(분기, 병합 접근, PCIe, 산술 집약도)이 그 조건의 이유다. 두 설명을 잇는 것은 위키의 정리다.

## 관련

- [[GPU 할당과 스케줄링]] · [[RAPIDS]] · [[추론 최적화]] · [[모델 서빙]] · [[지연 시간과 처리량]] · [[행 기반과 열 기반 저장]]
- 자료: [[AI DE 강의 4-11 GPU 아키텍처와 CUDA]] · [[AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용]] · [[AI DE 강의 4-14 RAPIDS 가속 ETL]] · [[AI DE 강의 2-09 서빙의 CPU·GPU 가속]]

## 빈칸

- 텐서 코어와 정밀도(FP16·BF16·FP8·INT8)는 H100의 "Transformer Engine" 한 줄(p276) 말고는 다루지 않는다.
- GPU 사이 통신(NCCL, 텐서·파이프라인 병렬)은 NVLink 설명(p252)에서 멈춘다.
- LLM 추론의 KV cache가 GPU 메모리를 어떻게 먹는지는 운영 덱의 GPU 대시보드 한 줄(「GPU memory 높음 + OOM: batch size, model size, KV cache」, [[AI DE 강의 4-16 모니터링 대시보드와 알람]])에만 나온다.

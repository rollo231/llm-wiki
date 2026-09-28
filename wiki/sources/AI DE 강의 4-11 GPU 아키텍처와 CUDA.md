---
type: source
title: AI DE 강의 4-11 GPU 아키텍처와 CUDA
aliases: [AI DE 4-11]
tags: [AI-DE-강의, GPU, 하드웨어]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf"
---

# AI DE 강의 4-11 GPU 아키텍처와 CUDA

[[AI 데이터 엔지니어링 강의]] Part 4 Ch4 「GPU 워크로드 전략」의 소단원 1·2다. 제목이 「GPU 아키텍쳐란? CPU와의 차이1」「…2」로 이어져 한 페이지로 묶었다. 소단원 1은 CPU와 GPU의 설계 차이와 CUDA의 실행 모델을, 소단원 2는 GPU 성능의 원리(병합 접근, PCIe, Roofline)와 GPU 제품 비교를 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch4. GPU 워크로드 전략: 1. GPU 아키텍쳐란? CPU와의 차이1 · 2. GPU 아키텍쳐란? CPU와의 차이2 |
| 원본 파일 | `part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` p241–277 (37p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch1~4`, 챕터 `Ch4`와 소단원 번호 `1`·`2`는 표지 슬라이드 |

## 요약

### 소단원 1. CPU와의 차이 1 (p241–262)

#### 01. GPU 구조를 알아야 하는 이유 (p243–244)

- GPU는 같은 전력·비용 범위에서 CPU보다 높은 처리량과 메모리 대역폭을 목표로 한 가속기다. AI 시스템의 행렬·벡터 연산과 잘 맞는다.
- 데이터 엔지니어도 GPU가 왜 어떤 워크로드에서 빠른지를 알아야 자원 배치와 파이프라인 설계를 할 수 있다. 슬라이드는 "A100 주세요"라는 요청에 "(A100이 뭐지?) 네 드릴게요" 대신 "모델 크기가 어떻게 되시나요?"라고 되물어야 한다는 대화로 보여 준다(p243).
- CPU는 흐름·입력·스케줄링·OS를, GPU는 병렬 커널을 맡는 협업 구조다. host memory와 device memory는 분리돼 있다(p244).

#### 02. CPU와 GPU (p245–252)

- 설계 철학: CPU는 latency optimized(분기 예측, 비순차 실행, 큰 캐시), GPU는 throughput optimized(많은 ALU, SIMT)다(p245).
- GPU는 SM의 집합이고, 스케줄러는 워프(보통 32 스레드) 단위로 명령을 낸다. 같은 SM의 스레드는 레지스터와 shared memory를 공유하고, 이것으로 전역 메모리 접근을 줄이는 것이 CUDA 프로그래밍의 핵심이다(p246).
- CPU 구성 요소(코어, 제어 장치, L1·L2·L3, DRAM)를 교수님 책상·개인 책장·학과 자료실·중앙 도서관에 비유한다(p247–249). GPU 그림에서는 수천 개 코어의 그리드, 단순한 제어 구조, 작은 L1·shared memory, 공유 L2, DRAM을 짚는다(p250–251).
- 그림에 없는 요소로 HBM(칩 옆에 붙여 대역폭을 넓힌 DRAM, LLM 서빙에 주로 쓰임)과 NVLink(여러 GPU를 PCIe보다 "수 배에서 수십 배" 빠르게 잇는 연결)를 든다(p252).

#### 03. CUDA (p253–255)

- CUDA는 직렬 코드와 수천 개 코어 사이의 간극을 메우는 NVIDIA의 병렬 플랫폼이자 프로그래밍 모델이다(p253).
- 논리 구조를 하드웨어에 "정확히 1:1로 대응"시키는 세 단계로 설명한다. 스레드 → 코어, 블록 → SM, 그리드 → GPU 전체다(p254).
- 커널은 host가 호출하고 device의 수많은 스레드가 병렬로 실행하는 함수이고, SIMT는 수백 개 스레드가 같은 명령을 서로 다른 데이터에 실행하는 방식이다(p255).

#### 04. 예시로 CUDA 이해하기 (p256–262)

- `A = torch.randn(100000).cuda(); B = ...; C = A + B`에서 CPU는 10만 번의 덧셈을 차례로 하지만, GPU에서는 덧셈이 커널로 바뀌어 스레드마다 자기 번호의 원소 하나를 더한다고 한다(p256–258).
- 스레드 1,024개를 한 블록으로 묶고, 블록 약 100개가 A100의 SM 108개에 나뉘어 동시에 시작한다고 한다(p259–260).
- operator fusion(p261–262): `C = A + B; D = C * 2`를 커널 두 개로 돌리면 C가 전역 메모리를 왕복해 memory-bound가 되고, `(A + B) * 2` 한 커널로 합치면 전역 메모리 접근이 절반으로 줄어 산술 집약도가 오른다고 한다.

### 소단원 2. CPU와의 차이 2 (p263–277)

#### 01. GPU 성능의 핵심 원리 (p265–266)

- 데이터는 모아서(batch), 정렬해서(coalescing). 행마다 다른 if-else를 타는 쿼리는 코어의 절반을 놀게 하고, 흩어진 메모리 접근은 시간을 낭비한다. 열 기반 포맷(Parquet, Arrow)이 GPU와 어울리는 이유다(p265).
- PCIe I/O 병목: "PCIe Gen4의 속도는 고작 64GB/s", HBM은 "2~3TB/s"라서 GPU로 보냈다가 CPU로 되가져오면 계산은 0.1초, 전송은 10초가 될 수 있다(p266).

#### 02. Roofline Model (p267–270)

- 산술 집약도 = 연산량 / 메모리 이동량. 낮으면 코어가 놀고 메모리만 바쁘다(p267).
- Roofline 차트는 병목이 연산인지 메모리 전송인지 보여 준다. 기울어진 선에 닿으면 메모리 병목, 평평한 지붕에 닿으면 연산 병목이다(p268–270).

#### 03. 모던 GPU 아키텍처 (p271–277)

- GPU 종류에 따라 인프라 비용이 수십 배 차이 난다(p271).
- T4(16GB GDDR6, 320 GB/s, 70W, 추론 전용, 조인·정렬 ETL에서 대역폭 한계), L4(24GB, 300 GB/s, 차세대 가성비), A10G(24GB, 600 GB/s, AWS 범용), A100(40·80GB, MIG 최대 7개, RAPIDS와 분산 학습의 표준), H100(80GB HBM3, 3.3 TB/s, PCIe Gen5, Transformer Engine)을 클라우드 인스턴스와 짝지어 비교한다(p272–277).

## 핵심

- CPU와 GPU를 지연 시간 대 처리량의 설계 선택으로 설명하는 틀(p245)은 [[지연 시간과 처리량]]을 하드웨어 층위로 내린 것이다. 전문은 [[GPU 아키텍처]]에 있다.
- 이 소단원에서 데이터 엔지니어에게 가장 쓸모 있는 것은 소단원 2의 세 원리(분기 회피, 병합 접근, PCIe 왕복 회피, p265–266)다. [[AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용]]의 "GPU가 오히려 나빠지는 경우"와 [[AI DE 강의 4-14 RAPIDS 가속 ETL]]의 판단 질문이 모두 여기서 나온다. 이 연결은 위키의 관찰이다.
- 소단원 1의 CUDA 설명은 틀린 곳이 많아 [[GPU 아키텍처]]의 정정 표를 함께 읽어야 한다(아래).

## 주의·결함

- ❌ 스레드 → 코어 1:1 대응(p254)과 "10만 명의 코어가 동시에 1번씩만 덧셈"(p258)은 틀렸다. 워프가 SM에 올라 번갈아 실행되고, A100의 FP32 코어는 6,912개다. SM당 상주 스레드는 최대 2,048개다. [https://developer.nvidia.com/blog/nvidia-ampere-architecture-in-depth/ , 2026-09-28 확인]
- ❌ "CUDA는 스레드들을 1,024개씩 묶어서 한 블록으로 만듬"(p259). 1,024는 블록당 상한이고 기본값이 아니다. PyTorch의 elementwise 커널은 실제로 블록당 128 스레드, 스레드당 8원소(`main`, 2026-09 기준)로 띄운다. [https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/intro-to-cuda-cpp.html · https://github.com/pytorch/pytorch/blob/main/aten/src/ATen/native/cuda/CUDALoops.cuh , 2026-09-28 확인]
- ❌ shared memory로 "10만 개 전체의 평균"을 HBM까지 가지 않고 구한다는 설명(p259). shared memory는 블록 안에서만 보이므로 전체 집계는 전역 메모리를 거친다. 같은 쪽의 "같은 SM에 배정된 1,024개의 스레드들"도 범위를 SM으로 잘못 잡는다.
- ❌ operator fusion으로 전역 메모리 접근이 "절반"(p262). 세어 보면 5회 → 3회(40% 감소)이고, 절반이 되는 것은 커널 수다. 누가 융합하는지(PyTorch eager는 하지 않고 `torch.compile` 같은 컴파일러가 한다)도 말하지 않는다. [https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html , 2026-09-28 확인]
- ⚠️ "PCIe Gen4 고작 64GB/s"(p266)는 양방향 합계다. 한 방향은 약 32 GB/s이고, 옆에 놓은 HBM 수치는 한 방향이라 비교가 PCIe에 두 배 유리하다.
- ❌ A100을 "40GB 또는 80GB HBM2e"(p275)로 적는다. 40GB판은 HBM2 1,555 GB/s다. ⚠️ H100의 "80GB HBM3, 3.3 TB/s"(p276)는 SXM판이고 PCIe판은 HBM2e 2 TB/s다. [A100 데이터시트 https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf · H100 PCIe Product Brief https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf · https://www.nvidia.com/en-us/data-center/h100/ , 2026-09-28 확인]
- ⚠️ 사양 표가 H100에서 멈춘다(p277). 작성 시점에 AWS에는 H200(P5e 2024-09), B200(P6-B200 2025-05), B300(P6-B300 2025-11)이 이미 있었다. 같은 덱의 MIG 슬라이드(4-12 p286)는 H200·B200을 언급한다. 세부는 [[GPU 아키텍처]]의 사양 절.
- ✅ 워프 32, 블록이 SM 하나에서 돈다는 것, NVLink가 PCIe보다 수 배 빠르다는 것(H100 900 GB/s 대 PCIe Gen5 128 GB/s, 약 7배), T4·L4·A10G 수치와 클라우드 매핑은 맞다.
- 수사가 과하다. NVLink가 데이터를 "빛의 속도로" 교환하고 8대의 GPU가 "한 몸처럼" 움직인다(p252)고 한다. [[AI DE 강의 4-12 GPU 할당 아키텍처]]도 같은 노드 안의 PCIe·NVLink 교환을 "빛의 속도"라고 부른다(p301).
- 중복 슬라이드: p269 = p270(Roofline 그림).
- p250의 "CPU는 4개뿐이었지만"은 슬라이드 그림(CPU 코어 4개)을 가리키는 말이라 그림 없이는 읽히지 않는다.

## 관련

- 개념: [[GPU 아키텍처]] · [[지연 시간과 처리량]] · [[행 기반과 열 기반 저장]] · [[추론 최적화]]
- 엔티티: [[RAPIDS]]
- 이전 강의: [[AI DE 강의 4-10 람다·카파와 현대 아키텍처]]
- 다음 강의: [[AI DE 강의 4-12 GPU 할당 아키텍처]]

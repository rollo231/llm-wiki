---
type: source
title: AI DE Course - Part4 Ch4 GPU allocation architecture
area: [data-engineering, programming]
aliases: [Part4 Ch4-3, GPU 할당을 위한 아키텍처 설계, MIG, MPS, time-slicing]
tags: [data-engineering, course, fast-campus, gpu, mig, mps, time-slicing, kubernetes, spot, device-plugin]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf (p278–301)"]
---

# AI DE Course - Part4 Ch4 GPU allocation architecture

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 4** Ch4의 소단원 **3**
"GPU 할당을 위한 아키텍처 설계". 원본(로컬): `raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` **p278–301**
(356p 중). 강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐ **"GPU 할당은 쿠버네티스 설정 한 줄 문제가 아니다."** 하드웨어 격리 → 스케줄링 → 프로비저닝 →
> 비용 통제를 **한 구조로** 설계하라는 4계층 프레임이 이 소단원의 뼈대다.
> **MIG vs MPS vs Time-Slicing 비교표에서 MPS의 격리 수준을 "최악"이라고 명시하는 정직함**이 눈에 띈다.

## 구성

`01 GPU 할당 설계 · 02 하드웨어 레벨 분할 · 03 Kubernetes 레벨 오케스트레이션 ·
04 클라우드 인프라 준비 계층 · 05 아키텍처 시나리오`

## 왜 할당 전략인가

> ⭐ **"좋은 GPU 1장보다 그 GPU를 어떻게 나눠 쓰고 언제 반납할지가 운영 비용을 좌우한다.
> GPU 운영의 핵심은 단순 성능이 아니라 할당 전략. 목표는 이용률 상승과 장애 격리의 동시 달성."**

### 대표 실패 2종

| 실패 | 내용 |
|---|---|
| **Under-utilization** | **80GB A100 인스턴스를 점유하고 실제로는 4GB만 사용.** 과도한 상위 SKU 선택, **24시간 켜진 '좀비 노드'** — 주기성 작업만 짧게 수행하면서 계속 켜둠 |
| **Noisy Neighbor** | 격리 설계 없이 여러 작업을 혼재시킬 때. **한 작업의 OOM 또는 비정상 점유가 다른 작업의 QoS를 파괴.** *"조금만 같이 태우면 되겠지"* 라는 낙관이 장애 도메인 확대로 이어짐 |

**두 실패가 정확히 반대 방향이라는 게 요점이다** — 격리를 강화하면 이용률이 떨어지고, 이용률을
높이면 격리가 약해진다. 아래 4계층이 이 트레이드오프를 다루는 도구다.

## ⭐ GPU 할당 설계의 네 계층

| 계층 | 결정 사항 |
|---|---|
| **하드웨어** | full GPU · MIG · shared GPU |
| **Kubernetes** | device plugin · 스케줄링 · node 격리 |
| **클라우드** | quota · instance family · capacity type · image/driver |
| **비용** | Spot · 자동 축소 · 노드 수명 · 예산 통제 |

> **"하드웨어 격리 → 스케줄링 → 프로비저닝 → 비용 통제를 한 구조로 설계."**

## 하드웨어 레벨 분할

> ⭐ **"GPU 할당은 전용 vs 공유의 이분법이 아니라 전용 / 소프트웨어 공유 / 하드웨어 분할의
> 스펙트럼."**

| 방식 | 특징 |
|---|---|
| **전용 GPU** | 한 작업이 GPU 전체 독점. 가장 단순, **가장 비쌈**(Under Utilization 가능), 가장 예측 가능 |
| **Shared GPU** | 여러 작업이 공유. 이용률 상승 가능, **간섭과 fault domain 관리가 핵심** |
| **Time-Slicing** | CPU 멀티태스킹과 유사 — GPU 코어가 ms 단위로 `A → B → C` 스위칭 무한 반복. **소프트웨어(드라이버/스케줄러) 선에서 구현**, 거의 모든 GPU에서 사용 가능. ⚠️ **한 작업이 코어를 꽉 잡고 안 놓으면 다른 작업들이 줄줄이 대기 (격리 실패)** |
| **MIG** | **물리 GPU를 하드웨어 수준으로 분할.** compute와 memory를 분리된 인스턴스로 제공. **연산 코어(SM), L2 캐시, 메모리 대역폭 자체를 물리적으로 막음** |

### MIG 심층

- 하나의 물리 GPU를 여러 **GPU 인스턴스**로 분할, compute와 memory를 독립적으로 배정
- Kubernetes와 컨테이너 환경에서도 **개별 할당 대상처럼 사용 가능**
- 공식 문서 기준 대표 지원군: **A100/A30, H100/H200, B200, 일부 RTX PRO Blackwell**
- 컨테이너·K8s 환경에서는 **NVIDIA Container Toolkit, K8s device plugin, gpu-feature-discovery**
  같은 구성 요소가 함께 필요 (**gpu-operator**)

### ⭐⭐ Time-Slicing vs MPS vs MIG 비교표

| 구분 | Time Slicing | MPS (Multi-Process Service) | MIG |
|---|---|---|---|
| **분할 방식** | 시간 분할 (Temporal) | **공간 분할** (동시 실행, Spatial) | **공간 분할** (물리적, Spatial) |
| **Context Switching** | 발생함 (느림) | 발생 안 함 (대리인이 묶어서 처리) | 발생 안 함 |
| **격리 수준 (보안/장애)** | 낮음 (OOM 간섭 있음) | ⚠️ **최악 (하나 죽으면 다 같이 죽음)** | **완벽함 (물리적 격리)** |
| **사용 시기 (실무)** | 가벼운 테스트 환경, 단순 서빙 | 단일 팀의 신뢰할 수 있는 병렬 배치 작업 (예: HPC) | **K8s 멀티 테넌트 프로덕션 환경** |
| **지원 장비** | 대부분의 GPU | 대부분의 GPU (V100 등에서도 가능) | **A100, H100 전용** |

**MPS 상세:**

- MPS를 켜면 GPU와 애플리케이션들 사이에 **'MPS 서버(대리인/프록시)'** 가 생성
- 애플리케이션이 각자 GPU에 명령하는 대신 MPS 서버에게 명령하고 **MPS가 스케줄링**
- CUDA MPS control daemon이 관여
- device plugin 기준 memory/compute fraction 제어 가능
- ⚠️ **Kubernetes device plugin에서는 experimental이고 MIG와 동시 지원 불가**
- ⚠️ **장애 격리(Fault Isolation) 불가**

> ⭐ **"MPS의 격리 수준: 최악 (하나 죽으면 다 같이 죽음)"** —
> 이런 표현을 벤더 자료에서는 볼 수 없다. **MPS는 성능(context switching 제거)을 위해 격리를 완전히
> 포기한 방식**이라는 점을 정확히 짚는다. **"단일 팀의 신뢰할 수 있는 병렬 작업"** 이라는 사용
> 조건도 정확하다 — 서로를 신뢰하는 프로세스끼리만 써야 한다.
>
> **비교표의 축(분할 방식 / context switching / 격리 / 사용 시기 / 지원 장비)이 잘 골라졌다.**
> 특히 **temporal vs spatial** 구분이 핵심 — MPS와 MIG는 둘 다 공간 분할이지만
> **소프트웨어 공간 분할 vs 하드웨어 공간 분할**로 격리가 갈린다.

## Kubernetes 레벨

### GPU는 K8s의 기본 리소스가 아니다

> **"Kubernetes는 GPU를 기본 리소스로 직접 알지 못한다. vendor device plugin이 kubelet에 하드웨어
> 자원을 광고해야 schedulable resource가 된다."**

- NVIDIA 공식 device plugin은 보통 **DaemonSet**으로 배포
- 이후 `nvidia.com/gpu` 같은 **확장 리소스**로 파드 스케줄 가능

**GPU 요청 규칙:**

- GPU는 보통 **`limits`** 로 요청
- `requests`를 같이 쓰면 값은 같아야 함
- **`requests`만 단독으로 쓰는 방식은 허용되지 않음**

### 배포 방식 두 가지

| | 내용 |
|---|---|
| **단순 방식** | NVIDIA device plugin + 필요 구성요소를 직접 설치 |
| **운영형 방식** | **GPU Operator**로 driver / toolkit / device plugin / GFD / MIG 관리까지 묶어서 운영 |

### MIG on K8s

- **GPU Operator의 MIG Manager**가 노드 label 변화를 보고 **MIG geometry 재구성**
  (예: `nvidia.com/mig.config=all-1g.10gb`)
- ⚠️ **Reconfiguration 과정**: Shut down — **GPU pods 중지**, 필요 시 reboot, MIG 적용 후 재시작
- **MIG strategy**에 따라 `nvidia.com/gpu`로 보이게 할지, `nvidia.com/mig-...` 리소스로 노출할지
  달라짐 (예: `nvidia.com/mig-3g.40gb: 1`)

> ⭐ **"Reconfiguration 시 GPU pods를 중지한다"는 게 실무에서 중요하다.** MIG geometry 변경은
> 무중단이 아니다 — **profile을 바꾸려면 그 노드의 모든 GPU 워크로드를 내려야 한다.** 이것이 아래의
> "파편화" 문제가 심각한 이유이기도 하다.

### GPU 격리 권장 원칙

- GPU 노드는 **일반 CPU 노드와 분리**
- GPU NodePool 또는 별도 node group 사용
- **taint로 기본 격리**, GPU workload만 **toleration** 부여
- **label / nodeSelector / affinity**로 GPU 종류와 목적 구분

목적: 일반 워크로드가 비싼 GPU 노드를 실수로 점유하는 것 방지 · 팀별/용도별 전용 pool 설계 ·
**MIG 노드와 full-GPU 노드를 따로 운영**.

## 클라우드 인프라 준비 계층

> **"반드시 먼저 준비할 것"** — 세 가지 한계로 나눈 게 좋다.

| 한계 | 준비 사항 |
|---|---|
| **행정적** | Region별 GPU quota 확인 · **On-Demand와 Spot quota 각각** 확인 |
| **소프트웨어적** | GPU AMI / driver / container runtime 준비 · **bootstrap 후 device plugin이 정상 구동되는지 검증** |
| **물리적** | 최소 baseline capacity 또는 **fallback 전략** 정의 |

> **"행정적 한계"라는 표현이 정확하다.** GPU 인프라에서 가장 흔한 블로커가 기술이 아니라
> **quota 승인 대기**다. 이것을 별도 계층으로 세우는 자료가 드물다.

### 구매 전략 — On-Demand baseline과 Spot burst 분리

| On-Demand baseline | Spot burst |
|---|---|
| 중요한 서빙 | 배치 ETL |
| **stateful 장기 작업** | 재시도 가능한 전처리 |
| interruption에 취약한 파이프라인 | **checkpoint 가능한 학습/추론 batch** |
| 반드시 살아있어야 하는 최소 capacity | 급증 시 보조 capacity |

## ⭐ 아키텍처 시나리오 — scale-out vs scale-up

**상황:** A/B/C 모델을 동시 서빙, 각 모델 크기와 메모리 요구가 다름.

| | **방향 1: T4/L4 scale-out** | **방향 2: A100/H100 MIG scale-up** |
|---|---|---|
| **구성** | 노드 여러 대 | 대형 GPU 한 대 |
| | 모델별 분리 단순 | 하드웨어 격리된 MIG slice에 모델별 배치 |
| | **장애 도메인 분산** | 높은 메모리 대역폭과 node-local 집중 |
| | 네트워크 홉·동기화·운영 수 증가 가능 | **실패 시 단일 물리 노드 fault domain이 커짐** |
| | | MIG profile 설계와 K8s exposure 필요 |

### 방향 1 — 장점과 비판

**장점 (장애 격리와 단순함):** 가장 직관적이고 안전. **"1번 노드의 쿨러가 고장 나 서버가 죽어도
A모델만 죽을 뿐 B, C모델은 정상 서비스"** — 장애 도메인이 완벽히 분산.

⚠️ **비판적 시각 (네트워크 병목과 오버헤드):**

> **"A모델이 텍스트를 추출하고 그 결과를 B모델이 받아 요약하는 '앙상블(파이프라인)' 구조라면,
> 거대한 텐서 데이터를 1번 노드에서 2번 노드로 네트워크(LAN)를 통해 넘겨야 한다.
> GPU 연산은 0.01초 만에 끝났는데 네트워크 전송에 0.1초가 걸리는 상황."**

또한 관리해야 할 K8s 노드 개수가 많아져 인프라 운영 복잡도 상승.

### 방향 2 — 장점과 비판

**장점 (초고속 대역폭과 집중화):** 물리적으로 같은 노드이므로 모델 간 통신 시 네트워크를 탈 필요 없이
**PCIe 버스나 NVLink를 통해 데이터 교환**(Locality). A100의 HBM 대역폭으로 T4보다 훨씬 빠른 추론.

⚠️ **비판적 시각 (치명적인 SPOF):**

> **"A100 물리 서버의 메인보드에 문제가 생기거나 K8s 노드가 네트워크 단절(NotReady)에 빠지면
> A, B, C모델 전체가 동시에 셧다운. 고가용성 확보가 필요하고, 결국 A100 노드를 최소 2대
> 프로비저닝하면 인프라 비용이 천문학적으로 상승."**

> ⭐ **각 방향에 "비판적 시각"을 붙이는 구성이 이 소단원의 미덕이다.** 한쪽을 권하지 않고
> **앙상블 구조인가(→ scale-up), 독립 모델인가(→ scale-out)** 라는 판단 기준을 남긴다.
>
> **이것이 [[AI DE Course - Part4 Ch1 Distributed processing basics]]의 "단일 서버로 충분한가"
> 논지가 GPU에서 반복되는 형태다** — 장애 도메인 분산 vs locality의 트레이드오프.
> **Ch1-4의 "고가용성의 대가"** 도 여기서 "최소 2대 = 비용 2배"로 반복된다.

## ⚠️ Ch5-4와 상당히 겹친다

**[[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]의 소단원 4가 이 소단원과 주제가
거의 같다** — GPU 할당 방식(Full/MIG/time-slicing/MPS), K8s NodePool, Spot/On-Demand가 양쪽에
나온다. Ch5 쪽은 **워크로드 분류와 우선순위**(서빙/배치/학습/실험/ETL별 정책)를 추가하고 Karpenter류
동적 프로비저닝을 다루는 것이 차이다. **강의가 두 챕터를 교차 참조하지 않는다.**

## 기존 페이지와의 대조

- **새 concept:** [[GPU resource allocation]]
- **[[NVIDIA Triton Inference Server]]** — Part 2에서 "K8s 궁합 최상"이라고 했던 것의 인프라 측
  근거가 여기 있다.
- **[[Inference optimization]]** — "GPU는 마지막 수단"의 비용 논거(under-utilization, 좀비 노드).
- **[[Batch and online serving]]** — 서빙/배치 GPU pool 분리가 그 페이지의 "배치 vs 온라인"과 같은 축.
- ⚠️ **[[AI DE Course - Part4 Ch4 GPU architecture and CUDA]]와 불일치** — MIG 지원 장비가 이
  소단원에서는 **A100/A30/H100/H200/B200/RTX PRO Blackwell**인데, 비교표에서는 **"A100, H100 전용"**
  이다. 그리고 앞 소단원의 GPU 스펙 표에는 B200이 없다.

## 자료 품질

- ✅ **4계층 프레임**(하드웨어·K8s·클라우드·비용)이 명료
- ✅ **MIG/MPS/Time-Slicing 비교표** — 특히 MPS 격리를 "최악"으로 명시하는 정직함
- ✅ K8s 세부가 실제와 일치: device plugin as DaemonSet, `nvidia.com/gpu` 확장 리소스,
  **`limits`로만 요청 가능** 규칙, `nvidia.com/mig-3g.40gb` 리소스 이름, MIG 재구성 시 pod 중지
- ✅ **"행정적 한계(quota)"를 별도 계층으로** 세운 것
- ✅ 시나리오에 **각 방향의 비판적 시각**을 붙임
- ⚠️ **MIG 지원 장비 서술이 같은 챕터 안에서 불일치** (위 참조)
- ⚠️ **MIG profile 파편화 문제가 Ch5-4에만 있고 여기엔 없다** — 여기서 다뤄야 할 내용
- ⚠️ 중복/이미지 전용 슬라이드: p288·p290·p292
- ⚠️ **"0.01초 vs 0.1초", "비용이 천문학적으로 상승"** 은 예시용 수치이지 측정값이 아니다
- ⚠️ **Kueue·Volcano 같은 배치 스케줄러, gang scheduling, DRA(Dynamic Resource Allocation)가
  전혀 없다** — 학습 워크로드의 K8s 스케줄링에서 핵심인데 빠져 있다

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[GPU resource allocation]] · [[GPU architecture]] · [[Inference optimization]] ·
  [[Batch and online serving]] · [[Distributed processing]]
- 도구: [[CUDA]] · [[NVIDIA Triton Inference Server]] · [[NVIDIA RAPIDS]]
- 앞: [[AI DE Course - Part4 Ch4 GPU architecture and CUDA]]
- 다음: [[AI DE Course - Part4 Ch4 GPU in data engineering and RAPIDS]]
- 겹치는 챕터: [[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]

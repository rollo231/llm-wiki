---
type: concept
title: GPU resource allocation
area: [data-engineering, programming]
aliases: [GPU 할당, GPU 스케줄링, MIG, MPS, time-slicing, Multi-Instance GPU, GPU NodePool]
tags: [data-engineering, gpu, mig, mps, kubernetes, scheduling, spot, cost-optimization, karpenter]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch4 GPU allocation architecture]]", "[[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]"]
---

# GPU resource allocation

**비싼 GPU를 어떻게 나눠 쓰고 언제 반납할 것인가.**

> ⭐ **"좋은 GPU 1장보다 그 GPU를 어떻게 나눠 쓰고 언제 반납할지가 운영 비용을 좌우한다.
> GPU 운영의 핵심은 단순 성능이 아니라 할당 전략이고, 목표는 이용률 상승과 장애 격리의 동시
> 달성이다."**

## ⭐ 세 가지 실패 — 서로 반대 방향

| 실패 | 내용 |
|---|---|
| **1. 과소활용 (Under-utilization)** | **80GB A100을 점유하고 실제로는 4GB만 사용.** 과도한 상위 SKU 선택, 주기성 작업만 짧게 수행하며 **24시간 켜진 '좀비 노드'** |
| **2. 간섭 (Noisy Neighbor)** | 격리 없이 여러 작업 혼재. **한 작업의 OOM이나 memory pressure가 다른 작업의 QoS를 파괴.** 서빙 latency가 batch job 때문에 흔들림 |
| **3. 파편화 (Fragmentation)** | ⭐ **MIG slice 또는 GPU node가 애매하게 남음.** 작은 workload는 많은데 필요한 profile이 없고, 큰 workload를 올릴 연속 자원이 부족 |

> **1번과 2번이 정확히 반대 방향이다** — 격리를 강화하면 이용률이 떨어지고, 이용률을 높이면 격리가
> 약해진다. **아래 모든 도구가 이 트레이드오프 위의 점들이다.**
>
> **3번이 가장 다루기 어렵다.** MIG geometry 재구성은 **무중단이 아니다**(아래 참조) —
> 파편화됐는데 쉽게 고칠 수 없다.

## ⭐ 네 계층으로 설계한다

> **"GPU 할당은 쿠버네티스 설정 한 줄 문제가 아니다.
> 하드웨어 격리 → 스케줄링 → 프로비저닝 → 비용 통제를 한 구조로 설계해야 한다."**

| 계층 | 결정 사항 |
|---|---|
| **하드웨어** | full GPU · MIG · shared GPU |
| **Kubernetes** | device plugin · 스케줄링 · node 격리 |
| **클라우드** | quota · instance family · capacity type · image/driver |
| **비용** | Spot · 자동 축소 · 노드 수명 · 예산 통제 |

## 1. 하드웨어 — 전용/공유의 이분법이 아니라 스펙트럼

> ⭐ **"전용 / 소프트웨어 공유 / 하드웨어 분할의 스펙트럼."**

### ⭐⭐ Time-Slicing vs MPS vs MIG

| 구분 | **Time Slicing** | **MPS** (Multi-Process Service) | **MIG** |
|---|---|---|---|
| **분할 방식** | 시간 분할 (Temporal) | **공간 분할** (동시 실행, Spatial) | **공간 분할** (물리적, Spatial) |
| **Context Switching** | 발생함 (느림) | 발생 안 함 (대리인이 묶어 처리) | 발생 안 함 |
| **격리 (보안/장애)** | 낮음 (OOM 간섭 있음) | ⚠️ **최악 (하나 죽으면 다 같이 죽음)** | **완벽 (물리적 격리)** |
| **사용 시기** | 가벼운 테스트, 단순 서빙 | **단일 팀의 신뢰할 수 있는 병렬 배치 작업** (HPC) | **K8s 멀티 테넌트 프로덕션** |
| **지원 장비** | 대부분의 GPU | 대부분의 GPU (V100 등 포함) | A100/A30, H100/H200, B200 등 |

> ⭐ **MPS의 격리를 "최악"이라고 명시하는 것이 정확하다.** MPS는 성능(context switching 제거)을
> 위해 **격리를 완전히 포기한** 방식이다. **서로를 신뢰하는 프로세스끼리만** 써야 한다.
>
> **MPS와 MIG는 둘 다 공간 분할인데 격리가 정반대인 이유:**
> 소프트웨어 공간 분할(MPS) vs **하드웨어 공간 분할**(MIG). MIG는 **연산 코어(SM)·L2 캐시·
> 메모리 대역폭 자체를 물리적으로 막는다.**

**Time-Slicing의 함정:** 소프트웨어 선에서 구현되어 거의 모든 GPU에서 쓸 수 있지만,
**한 작업이 코어를 꽉 잡고 안 놓으면 다른 작업들이 줄줄이 대기한다.** 게다가 A→B 전환 때마다
GPU 내부를 정리하는 **Context Switching 오버헤드**가 붙는다.

**MPS 상세:** GPU와 애플리케이션 사이에 **MPS 서버(프록시)** 가 생성되고, 앱은 GPU가 아니라 MPS
서버에 명령한다. K8s device plugin에서는 **experimental이고 MIG와 동시 지원 불가**.

## 2. Kubernetes

### GPU는 K8s의 기본 리소스가 아니다

> **"Kubernetes는 GPU를 기본 리소스로 직접 알지 못한다. vendor device plugin이 kubelet에 하드웨어
> 자원을 광고해야 schedulable resource가 된다."**

- NVIDIA device plugin은 보통 **DaemonSet**으로 배포 → `nvidia.com/gpu` 확장 리소스
- **GPU는 `limits`로 요청한다.** `requests`를 같이 쓰면 값이 같아야 하고,
  **`requests` 단독은 허용되지 않는다**

| 배포 방식 | 내용 |
|---|---|
| **단순** | NVIDIA device plugin + 필요 구성요소 직접 설치 |
| **운영형** | **GPU Operator** — driver / toolkit / device plugin / GFD / MIG 관리를 묶어서 |

### ⚠️ MIG on K8s — 재구성은 무중단이 아니다

- **GPU Operator의 MIG Manager**가 노드 label 변화를 보고 geometry 재구성
  (`nvidia.com/mig.config=all-1g.10gb`)
- ⚠️ **재구성 절차: Shut down → GPU pods 중지 → 필요 시 reboot → MIG 적용 → 재시작**
- MIG strategy에 따라 `nvidia.com/gpu`로 보일지 `nvidia.com/mig-3g.40gb` 리소스로 노출될지 결정

> ⭐ **이것이 파편화가 심각한 이유다.** profile을 바꾸려면 그 노드의 모든 GPU 워크로드를 내려야
> 하므로, **"나중에 조정하지"가 통하지 않는다.** MIG profile 설계는 앞에서 정해야 한다.

### 격리 원칙

GPU 노드를 일반 CPU 노드와 분리 · GPU NodePool 또는 별도 node group ·
**taint로 기본 격리, GPU workload만 toleration** · label/nodeSelector/affinity로 GPU 종류·목적 구분.

**필요한 K8s 정책 6종:** node label · **taint/toleration** · nodeSelector/affinity ·
**priorityClass** · **namespace quota** · resource request/limit.

## 3. 워크로드 분류와 정책 — 핵심 표

| Workload | 핵심 목표 | **실패 허용** | 적합한 정책 |
|---|---|---|---|
| **온라인 추론** | 낮은 latency, 높은 가용성 | **낮음** | **On-Demand**, 높은 우선순위, 안정적 할당 |
| **배치 추론** | deadline 내 완료 | 중간 | **Spot 가능**, 재시도 가능, queue 기반 |
| **학습** | 긴 시간 안정적 실행 | 낮음~중간 | **checkpoint, 전용 GPU, 중단 대응** |
| **GPU ETL** | 특정 시간대 처리량 | 중간 | **Spot burst, 시간대별 scale-out** |
| **실험/개발** | 비용 절감 | **높음** | 낮은 우선순위, **preempt 가능** |

> ⭐ **"실패 허용" 열이 이 표를 유용하게 만든다.** Spot을 쓸 수 있는지는 예산이 아니라
> **중단을 감당할 수 있는가**가 결정한다.

### 서빙과 배치를 같은 pool에 섞으면

| 잘못된 구성 | 발생 문제 |
|---|---|
| 온라인 추론 Pod + 배치 Job + ETL Job + 실험 Pod을 **같은 NodePool**에 | **배치 job이 GPU를 선점해 서빙 replica pending** · **Spot 중단이 serving까지 영향** · 실험이 GPU memory 과점유 · **서빙 latency가 ETL 시간대에 흔들림** |

**권장 pool 5종:**

```
gpu-serving-ondemand      gpu-training
 - 온라인 추론               - 장시간 학습
 - 높은 priority            - checkpoint 전제
 - 최소 capacity 유지        - 큰 GPU 우선

gpu-batch-spot            gpu-mig-serving
 - batch inference         - 작은 모델 다중 서빙
 - GPU ETL                 - MIG profile 기반 할당
 - 재시도 가능 workload

gpu-experiment
 - 개발·실험 / 낮은 priority / quota 제한
```

## 4. 클라우드와 비용

### ⭐ 동적 프로비저닝이 해결하지 못하는 것 6가지

Karpenter류의 역할: pending pod 요구사항 확인 → instance type 선택 → GPU node 생성 →
**작업 완료 후 빈 node 제거.**

> ⭐⭐ **"하지만 해결하지 못하는 것":**
>
> | 항목 | 성격 |
> |---|---|
> | **cloud quota 부족** | 행정 |
> | **region capacity 부족** | **물리** |
> | driver/runtime 구성 오류 | 소프트웨어 |
> | 너무 좁은 instance type 조건 | 설정 |
> | **Spot interruption** | 계약 |
> | ⭐ **model load warm-up 지연** | 시간 |
>
> **"오토스케일러를 붙였으니 GPU 부족은 해결됐다"는 착각을 깬다.**
> **region capacity**는 자동화로 못 푸는 물리적 한계이고, **model load warm-up**은 노드가 떠도
> 서비스가 바로 되지 않는다는 뜻이다 — **스케일아웃 지연 = 노드 프로비저닝 + 이미지 pull +
> 모델 로딩.**

**미리 준비할 것 세 가지 한계:**

| 한계 | 준비 |
|---|---|
| **행정적** | Region별 GPU quota, **On-Demand와 Spot quota 각각** |
| **소프트웨어적** | GPU AMI/driver/container runtime, **bootstrap 후 device plugin 정상 구동 검증** |
| **물리적** | 최소 baseline capacity 또는 **fallback 전략** |

### Spot vs On-Demand — 판단 기준은 checkpoint 가능성

| On-Demand | Spot |
|---|---|
| 온라인 추론 baseline | GPU ETL |
| 중요 모델 서빙 | batch inference |
| **checkpoint가 어려운 장시간 job** | 재시도 가능한 전처리 |
| **SLO 위반 비용이 큰 workload** | 실험 job |
| | **checkpoint 가능한 학습 job** |

> ⭐ **학습 job이 양쪽에 걸쳐 있는 게 요점이다 — checkpoint를 붙이면 Spot으로 내려갈 수 있다.**
> **엔지니어링으로 비용 등급을 바꿀 수 있다.**

## ⭐ scale-out vs scale-up 시나리오

**상황:** A/B/C 모델 동시 서빙, 각 모델 크기와 메모리 요구가 다름.

| | **T4/L4 scale-out** | **A100/H100 MIG scale-up** |
|---|---|---|
| **구성** | 노드 여러 대, 모델별 분리 | 대형 GPU 한 대, MIG slice에 모델별 배치 |
| **장점** | ⭐ **장애 도메인 분산** — 1번 노드가 죽어도 A모델만 죽음 | ⭐ **Locality** — 모델 간 통신이 PCIe/NVLink로. 높은 HBM 대역폭 |
| **비판** | ⚠️ **앙상블 구조라면 거대한 텐서를 노드 간 네트워크로 넘겨야 함.** GPU 연산 0.01초, 네트워크 0.1초. K8s 노드 수 증가로 운영 복잡도 상승 | ⚠️ **치명적 SPOF** — 물리 서버 장애 시 A·B·C 전체 셧다운. HA 위해 최소 2대 → **비용 2배** |

> ⭐ **판단 기준: 앙상블/파이프라인 구조인가(→ scale-up), 독립 모델인가(→ scale-out).**
>
> **[[Distributed processing]]의 "단일 서버로 충분한가"가 GPU에서 반복되는 형태이고,
> [[Replication and consensus]]의 "고가용성의 대가"가 "최소 2대 = 비용 2배"로 반복된다.**

## 진단 — 사용률만으로는 아무것도 모른다

| GPU 사용률 | Queue | Latency | 해석 |
|---|---|---|---|
| 높음 | 낮음 | 정상 | **잘 활용 중** |
| 높음 | 높음 | 높음 | **capacity 병목** |
| **낮음** | **높음** | **높음** | ⭐ **GPU 앞단 병목** (feature lookup, CPU 전처리, network) |
| 낮음 | 낮음 | 정상 | **과잉 프로비저닝** |
| 높음 | 낮음 | 높음 | **memory, batch size, model 병목** |

> ⭐⭐ **3행이 [[Inference optimization]]의 "GPU는 마지막 수단"의 진단 도구다.**
> GPU 사용률이 낮은데 느리면 **GPU를 늘려도 소용없다.** [[GPU architecture]]의 PCIe 병목,
> [[Caching strategies]]의 feature lookup 지연이 여기로 수렴한다.

## ⚠️ 이 위키에 아직 없는 것

- **gang scheduling** — 분산 학습에서 "N개 GPU를 동시에 확보하거나 아예 시작하지 않기".
  **Kueue·Volcano가 강의에 한 번도 안 나온다.**
- **priorityClass의 preemption 동작** — 이름만 나오고 동작 설명이 없다.
- **DRA (Dynamic Resource Allocation)** — K8s의 차세대 디바이스 할당 API.
- **MIG profile 설계 실무** — 어떤 조합(1g.10gb × 7 vs 3g.40gb × 2)을 언제 고르는가.

## 관련 페이지

- [[GPU architecture]] — 나눠 쓸 하드웨어의 구조
- [[Inference optimization]] — **"GPU는 마지막 수단"**
- [[NVIDIA RAPIDS]] — GPU ETL 워크로드
- [[Batch and online serving]] — 서빙/배치 pool 분리의 근거
- [[NVIDIA Triton Inference Server]] — MIG·K8s 궁합
- [[Data SLA and observability]] — GPU 지표와 비용 SLO
- [[Distributed processing]] — 같은 트레이드오프의 노드 버전

## 출처

- [[AI DE Course - Part4 Ch4 GPU allocation architecture]]
- [[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]]

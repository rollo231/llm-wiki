---
type: concept
title: GPU 할당과 스케줄링
aliases: [GPU scheduling, GPU 스케줄링, GPU 할당, GPU 공유, MIG, Multi-Instance GPU, MPS, Multi-Process Service, Time-slicing, 타임 슬라이싱, GPU Operator, NVIDIA GPU Operator, Karpenter, Spot 인스턴스]
tags: [GPU, 인프라, Kubernetes, 비용]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 4-12 GPU 할당 아키텍처]]"
  - "[[AI DE 강의 4-18 GPU 스케줄링과 할당 최적화]]"
---

# GPU 할당과 스케줄링

비싼 GPU를 어떤 작업에 얼마만큼, 얼마 동안 줄지 정하는 설계다. [[AI DE 강의 4-12 GPU 할당 아키텍처]](Ch4-3)와 [[AI DE 강의 4-18 GPU 스케줄링과 할당 최적화]](Ch5-4)가 같은 주제를 두 번 다루는데 서로를 참조하지 않는다. 이 페이지가 두 소단원의 내용을 한곳에 모으고, 어느 쪽에서 나온 서술인지 쪽 번호로 밝힌다(Ch4-3은 덱 `01`, Ch5-4는 덱 `02`의 쪽이다). GPU 칩 자체의 구조는 [[GPU 아키텍처]]에 있다.

## 목표: 이용률과 격리

강의는 GPU 운영의 핵심을 단순 성능이 아니라 할당 전략으로 본다. 목표는 이용률을 올리면서 장애를 격리하는 것이다(Ch4-3 p280). Ch5-4는 이것을 "빈 GPU에 Pod를 올리는 것"이 아니라 워크로드마다 다른 목표를 지키는 문제로 다시 쓴다(p62–63). 서빙은 지연을, 배치는 마감을, 학습은 장시간 안정 점유를 지켜야 하고, 실험은 비용을 낮추되 실패를 감수하며, ETL은 특정 시간대에만 대량 GPU가 필요하다.

## 세 가지 실패

두 소단원의 실패 목록을 합치면 셋이다.

| 실패 | 모습 | 출처 |
|---|---|---|
| 과소 활용(under-utilization) | 80GB A100을 점유하고 4GB만 쓴다. 과한 상위 SKU, 24시간 켜 둔 "좀비 노드" | Ch4-3 p281, Ch5-4 p64 |
| 간섭(noisy neighbor) | 격리 없이 섞으면 한 작업의 OOM·과점유가 다른 작업의 QoS를 깬다. 서빙 지연이 배치 때문에 흔들린다 | Ch4-3 p281, Ch5-4 p64 |
| 파편화 | MIG slice나 GPU 노드가 애매하게 남는다. 작은 워크로드는 많은데 맞는 profile이 없고, 큰 워크로드를 올릴 연속 자원이 없다 | Ch5-4 p64 |

## 네 계층

Ch4-3은 할당을 쿠버네티스 설정 한 줄이 아니라 네 계층의 설계로 본다(p282). 하드웨어 격리 → 스케줄링 → 프로비저닝 → 비용 통제 순서다.

| 계층 | 결정할 것 |
|---|---|
| 하드웨어 | full GPU, MIG, 공유(time-slicing·MPS) |
| Kubernetes | device plugin, 스케줄링, 노드 격리 |
| 클라우드 | quota, 인스턴스 패밀리, capacity type(On-Demand·Spot), 이미지·드라이버 |
| 비용 | Spot, 자동 축소, 노드 수명, 예산 통제 |

## GPU를 나누는 네 방식

강의는 전용과 공유의 이분법이 아니라 전용 / 소프트웨어 공유 / 하드웨어 분할의 스펙트럼으로 설명한다(Ch4-3 p285). 아래 표는 강의의 비교표(Ch4-3 p293)를 뼈대로, 1차 자료로 고친 칸을 표시한 것이다.

| | Full GPU | Time-slicing | MPS | MIG |
|---|---|---|---|---|
| 분할 방식 | 없음(독점) | 시간 분할. 짧은 간격으로 작업을 번갈아 실행 | 공간 분할. MPS 서버(프록시)가 여러 프로세스의 커널을 함께 실행 | 공간 분할. SM·L2·메모리 대역폭을 하드웨어로 나눈 인스턴스 |
| 컨텍스트 전환 | 없음 | 있음(느림) | 없음 | 없음 |
| 메모리·장애 격리 | 완전 | 없음. 같은 fault domain | 약함. 한 클라이언트의 치명적 오류가 같은 GPU의 모든 클라이언트에 전달된다 | 강함. 다른 인스턴스의 OOM이 번지지 않는다 |
| 강의가 권하는 곳 | 대형 학습, 대형 LLM 추론 | 가벼운 테스트, 단순 서빙 | 한 팀의 신뢰할 수 있는 병렬 배치(HPC) | K8s 멀티 테넌트 프로덕션, 작은 모델 여러 개 |
| 지원 장비 | 전부 | 대부분 | 대부분(강의: "V100 등에서도 가능") | Ampere 이후 데이터센터 GPU 일부(아래) |

- ❌ 강의 표(Ch4-3 p293)는 MIG를 "A100, H100 전용"이라 적는데, 같은 소단원 p286이 맞다. NVIDIA MIG 사용자 가이드의 지원 목록은 A100, A30, H100, H20, H200, GH200의 H100, B200, GB200, RTX PRO 6000·5000·4500 Blackwell, Thor iGPU다. 인스턴스 최대 개수는 A30이 4개, RTX PRO 6000이 4개, RTX PRO 5000·4500과 Thor iGPU가 2개이고 나머지 데이터센터 GPU는 7개다. [https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html ("MIG is supported on GPUs starting with the NVIDIA Ampere generation"), 2026-09-28 확인]
- ✅ MPS의 장애 전파는 강의 표의 "하나 죽으면 다 같이 죽음"보다 범위가 정해져 있다. CUDA MPS 문서는 "A fatal GPU fault … will be reported to all the clients running on the subset of GPUs in which the fatal fault is contained", "Clients running on other GPUs remain unaffected"라고 적는다. 같은 GPU를 쓰는 클라이언트는 함께 영향을 받고, 다른 GPU의 클라이언트는 무사하다. [https://docs.nvidia.com/deploy/mps/when-to-use-mps.html , 2026-09-28 확인]
- ✅ MPS는 NVIDIA k8s-device-plugin에서 v0.15.0(2024-04-17)부터 실험 기능이고, MIG를 켠 장치에서는 쓸 수 없다(Ch4-3 p289). README: "As of v0.15.0 … MPS support is considered experimental", "Sharing with MPS is currently not supported on devices with MIG enabled". [https://github.com/NVIDIA/k8s-device-plugin , 2026-09-28 확인]
- ✅ time-slicing은 격리를 하지 않는다. 같은 README가 "nothing special is done to isolate workloads … each workload has access to the GPU memory and runs in the same fault-domain"이라 적는다.

Ch5-4는 선택 기준을 질문 다섯 개로 준다(p69). SLA가 중요한가, 메모리 요구량이 얼마인가, 간섭을 허용할 수 있는가, GPU 전체가 필요한가, 작은 워크로드를 많이 태울 것인가. MIG에는 profile 파편화와 재구성 비용이 따른다(p68).

## Kubernetes에서

- Kubernetes는 GPU를 기본 리소스로 알지 못한다. vendor device plugin(NVIDIA는 보통 DaemonSet)이 kubelet에 자원을 광고해야 `nvidia.com/gpu` 같은 확장 리소스로 스케줄된다(Ch4-3 p294).
- ✅ GPU는 limits로 요청한다. requests를 함께 쓰면 값이 같아야 하고, requests만 쓸 수는 없다. 문서: "You can specify GPU in both limits and requests but these two values must be equal. You cannot specify GPU requests without specifying limits." [https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/ , 2026-09-28 확인]
- 배포 방식은 device plugin과 구성 요소를 직접 설치하는 방식과, GPU Operator로 드라이버·container toolkit·device plugin·GFD(gpu-feature-discovery)·MIG 관리를 묶는 방식이 있다(Ch4-3 p295).
- ✅ GPU Operator의 MIG Manager는 노드 라벨(`nvidia.com/mig.config=all-1g.10gb`)이 바뀌면 MIG 구성을 다시 짠다. 재구성 중에는 GPU 파드를 종료하고, 필요하면 노드를 재부팅한다. MIG 전략이 single이면 `nvidia.com/gpu`로, mixed이면 `nvidia.com/mig-3g.40gb` 같은 이름으로 노출된다(Ch4-3 p295). 문서: "terminates all the GPU pods", "the node might need to be rebooted". [https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-operator-mig.html , 2026-09-28 확인]
- 격리 원칙: GPU 노드를 CPU 노드와 분리하고, taint로 막은 뒤 GPU 워크로드에만 toleration을 준다. label·nodeSelector·affinity로 GPU 종류와 목적을 구분한다(Ch4-3 p296). Ch5-4는 여기에 priorityClass, namespace quota, resource request/limit을 더한다(p71).

## 목적별 노드 풀

Ch5-4는 서빙·배치·실험을 한 GPU 풀에 섞으면 배치가 GPU를 선점해 서빙 replica가 pending되고, Spot 중단이 서빙까지 번지고, ETL 시간대에 서빙 지연이 흔들린다고 한다(p66). 권장 구성은 풀을 목적별로 나누는 것이다(p67, p70).

| 풀 | 워크로드 | 정책 |
|---|---|---|
| gpu-serving-ondemand | 온라인 추론 | On-Demand, 높은 priority, 최소 capacity 유지 |
| gpu-batch-spot | 배치 추론, GPU ETL | Spot 중심, queue 기반, checkpoint·retry 전제 |
| gpu-training | 장시간 학습 | checkpoint 전제, 큰 GPU 우선 |
| gpu-mig-serving | 작은 모델 여러 개 | MIG profile 기반 할당 |
| gpu-experiment | 개발·실험 | 낮은 priority, quota 제한, preempt 가능 |

워크로드별 목표와 실패 허용도는 Ch5-4 p65의 표에 있다. 온라인 추론은 실패 허용이 낮고, 배치 추론과 GPU ETL은 중간, 실험은 높다.

## 구매 방식과 동적 프로비저닝

- On-Demand baseline과 Spot burst를 나눈다(Ch4-3 p298, Ch5-4 p75). On-Demand에는 온라인 추론 baseline, 중요 모델 서빙, checkpoint가 어려운 장시간 작업, SLO 위반 비용이 큰 워크로드를 둔다. Spot에는 GPU ETL, 배치 추론, 재시도 가능한 전처리, 실험, checkpoint 가능한 학습을 둔다.
- 먼저 준비할 것(Ch4-3 p297): 리전별 GPU quota(On-Demand와 Spot 각각), GPU AMI·드라이버·container runtime, 부트스트랩 뒤 device plugin 정상 구동 검증, 최소 baseline capacity나 fallback 전략.
- Karpenter 류의 동적 프로비저닝은 pending pod의 요구를 보고 맞는 인스턴스 타입을 골라 GPU 노드를 만들고, 작업이 끝나면 빈 노드를 없앤다(Ch5-4 p72). 해결하지 못하는 것은 cloud quota 부족, 리전 capacity 부족, 드라이버·런타임 오류, 너무 좁은 인스턴스 조건, Spot 중단, 모델 로드 warm-up 지연이다(p73). ✅ Karpenter는 AWS에서 시작했고 Azure provider가 공식이며, 그 밖에 커뮤니티 provider와 Cluster API 구현이 있다. [https://github.com/kubernetes-sigs/karpenter · https://karpenter.sh/docs/ , 2026-09-28 확인]

## 시나리오: 작은 GPU 여러 대 대 큰 GPU 하나를 MIG로

Ch4-3 p299–301은 크기가 다른 모델 A·B·C를 동시에 서빙할 때의 두 방향을 비교한다.

| | T4/L4 scale-out | A100/H100 MIG scale-up |
|---|---|---|
| 구조 | 모델마다 노드 | 큰 GPU 한 대를 MIG slice로 나눠 모델별 배치 |
| 장점 | 단순하고 장애 도메인이 분산된다. 1번 노드가 죽어도 B·C는 산다 | 같은 노드 안에서 PCIe·NVLink로 교환해 네트워크 홉이 없다. HBM 대역폭이 크다 |
| 약점 | A의 출력을 B가 받는 파이프라인이면 텐서가 LAN을 탄다. K8s 노드 수가 늘어 운영이 복잡하다 | 물리 노드 하나가 SPOF다. 고가용성을 위해 최소 2대를 두면 비용이 크게 오른다 |

강의는 어느 쪽이 정답인지 말하지 않고 장단점만 나열한다. 모델 사이에 데이터가 오가는지와 가용성 요구가 판단 축이라는 것은 표에서 읽히는 정리다.

## 관련

- [[GPU 아키텍처]] · [[RAPIDS]] · [[모델 서빙]] · [[추론 최적화]] · [[서비스 수준 목표]] · [[AI 시스템 모니터링]] · [[분산 시스템]]
- 자료: [[AI DE 강의 4-12 GPU 할당 아키텍처]] · [[AI DE 강의 4-18 GPU 스케줄링과 할당 최적화]] · [[AI DE 강의 4-17 병목 파악과 트러블슈팅]](GPU 병목 오해)

## 빈칸

- MIG profile을 어떤 기준으로 고르고, 파편화가 생겼을 때 언제 재구성할지 수치나 절차가 없다.
- 공정 분배(여러 팀의 queue, gang scheduling, Kueue·Volcano 같은 배치 스케줄러)는 "여러 팀을 공정하게 나눌 것인가"(Ch5-4 p63) 질문으로만 나온다.
- Spot 중단 알림을 받아 checkpoint를 저장하고 재개하는 흐름은 원칙으로만 나온다.
- 두 소단원 모두 비용 수치(시간당 가격, 이용률 개선폭)가 없다.

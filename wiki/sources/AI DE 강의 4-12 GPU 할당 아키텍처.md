---
type: source
title: AI DE 강의 4-12 GPU 할당 아키텍처
aliases: [AI DE 4-12]
tags: [AI-DE-강의, GPU, 인프라, Kubernetes]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf"
---

# AI DE 강의 4-12 GPU 할당 아키텍처

[[AI 데이터 엔지니어링 강의]] Part 4 Ch4의 소단원 3이다. 비싼 GPU를 어떻게 나눠 쓰고 언제 반납할지를 하드웨어 분할(full·time-slicing·MPS·MIG), Kubernetes 오케스트레이션, 클라우드 준비, 아키텍처 시나리오 순으로 다룬다. 같은 주제를 운영 덱의 [[AI DE 강의 4-18 GPU 스케줄링과 할당 최적화]]가 다시 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch4. GPU 워크로드 전략: 3. GPU 할당을 위한 아키텍쳐 설계 |
| 원본 파일 | `part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` p278–301 (24p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch1~4`, 챕터 `Ch4`와 소단원 번호 `3`은 표지 슬라이드 |

## 요약

### 01. GPU 할당 설계 (p280–282)

- 좋은 GPU 1장보다 그 GPU를 어떻게 나눠 쓰고 언제 반납할지가 운영 비용을 좌우한다. 목표는 이용률 상승과 장애 격리의 동시 달성이다(p280).
- 대표 실패 두 가지: under-utilization(80GB A100에 4GB만 쓰는 작업, 24시간 켜진 좀비 노드)과 noisy neighbor(격리 없이 섞어 한 작업의 OOM이 다른 작업의 QoS를 깸)(p281).
- 할당은 하드웨어 · Kubernetes · 클라우드 · 비용의 네 계층을 한 구조로 설계하는 일이다(p282).

### 02. 하드웨어 레벨 분할 (p283–293)

- 전용 GPU는 가장 단순하고 비싸고 예측 가능하다. Shared GPU는 이용률이 오르지만 간섭과 fault domain 관리가 핵심이다(p283).
- time-slicing은 ms 단위로 작업을 번갈아 실행하고 거의 모든 GPU에서 되지만, 한 작업이 코어를 잡고 놓지 않으면 나머지가 대기한다(p284, p287).
- MIG는 SM·L2·메모리 대역폭을 하드웨어로 나눈 인스턴스를 준다. 지원군은 A100/A30, H100/H200, B200, 일부 RTX PRO Blackwell이고, K8s에서는 Container Toolkit, device plugin, gpu-feature-discovery(GPU Operator)가 함께 필요하다(p285–286).
- MPS는 MPS 서버(프록시)가 여러 프로세스의 명령을 받아 함께 스케줄한다. device plugin에서는 실험 기능이고 MIG와 동시에 쓸 수 없으며, 장애 격리가 안 된다(p289).
- 비교표(p293): 분할 방식, 컨텍스트 전환, 격리 수준, 실무 사용 시기, 지원 장비를 time-slicing · MPS · MIG로 나란히 놓는다.

### 03. Kubernetes 레벨 오케스트레이션 (p294–296)

- Kubernetes는 GPU를 모른다. device plugin(DaemonSet)이 `nvidia.com/gpu`를 광고한다. GPU는 limits로 요청하고, requests를 쓰면 같은 값이어야 한다(p294).
- 단순 방식(device plugin 직접 설치)과 운영형 방식(GPU Operator). MIG Manager가 `nvidia.com/mig.config` 라벨을 보고 재구성하고, 이때 GPU 파드를 멈추고 필요하면 재부팅한다. MIG strategy에 따라 리소스 이름이 달라진다(p295).
- GPU 노드를 분리하고 taint·toleration, label·nodeSelector·affinity로 격리한다(p296).

### 04. 클라우드 인프라 준비 계층 (p297–298)

- 행정적 한계(리전별 quota, On-Demand·Spot 각각), 소프트웨어 한계(AMI·드라이버·런타임, device plugin 구동 검증), 물리적 한계(baseline capacity와 fallback)(p297).
- On-Demand baseline(중요 서빙, stateful 장기 작업)과 Spot burst(배치 ETL, 재시도 가능한 전처리, checkpoint 가능한 작업)를 나눈다(p298).

### 05. 아키텍처 시나리오 (p299–301)

- 모델 A·B·C 동시 서빙에서 T4/L4 여러 대로 scale-out하는 방향과 A100/H100 한 대를 MIG로 나누는 방향을 장점·비판적 시각으로 비교한다. 앞쪽은 장애 도메인 분산 대신 모델 사이 텐서가 LAN을 타고, 뒤쪽은 노드 안 교환이 빠른 대신 물리 노드 하나가 SPOF다(p299–301).

## 핵심

- 할당을 이용률과 격리의 동시 달성으로 정의하고 네 계층(하드웨어 · K8s · 클라우드 · 비용)으로 나누는 틀(p280–282)이 이 소단원의 뼈대다. 전문은 [[GPU 할당과 스케줄링]]에 모았다.
- 공유 방식을 전용 대 공유가 아니라 "전용 / 소프트웨어 공유 / 하드웨어 분할의 스펙트럼"(p285)으로 보는 것이 옮겨 쓰기 좋다.
- p299–301의 시나리오는 각 방향에 "비판적 시각"을 붙여 정답 없이 판단 축(모델 사이 데이터 이동, 가용성)을 드러낸다. Part 4의 "도입 판단부터" 기조([[AI DE 강의 4-01 분산 처리의 등장과 도입 판단]])와 같은 방식이다. 이 연결은 위키의 관찰이다.

## 주의·결함

- ❌ 비교표(p293)는 MIG 지원 장비를 "A100, H100 전용"이라 적는데, 같은 소단원 p286이 맞다. 공식 가이드의 목록은 A100, A30, H100, H20, H200, GH200의 H100, B200, GB200, RTX PRO 6000·5000·4500 Blackwell, Thor iGPU다. [https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html , 2026-09-28 확인]
- ✅ MPS에 대한 p289 서술(device plugin에서 실험 기능, MIG와 동시 지원 불가)은 README와 맞다. 지원은 v0.15.0(2024-04-17)부터다. 장애 격리는 "불가"보다 범위가 정해져 있다. 치명적 오류는 같은 GPU를 쓰는 클라이언트에 전달되고 다른 GPU의 클라이언트는 영향이 없다. [https://github.com/NVIDIA/k8s-device-plugin · https://docs.nvidia.com/deploy/mps/when-to-use-mps.html , 2026-09-28 확인]
- ✅ p294의 limits 규칙과 p295의 MIG Manager 서술(라벨, 파드 종료, 재부팅 가능성, single/mixed 전략)은 공식 문서와 맞다.
- 오탈자: p284 "Time Sliciing", p295 "파일 리소스 요청란"(파드로 보인다).
- p288, p290, p292는 그림만 있는 슬라이드다(time-slicing의 시간축 그림, Pascal과 Volta의 MPS 비교 그림, MIG 인스턴스 그림). 그림에 설명 글이 없다.
- 이 소단원의 On-Demand/Spot 구분(p298)과 격리 원칙(p296)이 [[AI DE 강의 4-18 GPU 스케줄링과 할당 최적화]](덱 `02` p66–75)에서 거의 그대로 반복되는데, 두 소단원은 서로를 참조하지 않는다.
- 비용 수치가 없다. "GPU 종류에 따라 인프라 비용이 수십 배 차이"(4-11 p271)라고 하면서 시나리오의 비용 비교에는 숫자가 없다.

## 관련

- 개념: [[GPU 할당과 스케줄링]] · [[GPU 아키텍처]] · [[분산 시스템]]
- 같은 주제: [[AI DE 강의 4-18 GPU 스케줄링과 할당 최적화]]
- 이전 강의: [[AI DE 강의 4-11 GPU 아키텍처와 CUDA]]
- 다음 강의: [[AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용]]

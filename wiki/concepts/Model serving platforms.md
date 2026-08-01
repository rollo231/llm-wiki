---
type: concept
title: Model serving platforms
area: [data-engineering]
aliases:
  - 서빙 플랫폼
  - Model server
  - 모델 서버
  - Dynamic batching
  - 동적 배치
tags: [data-engineering, mlops, serving, fastapi, torchserve, bentoml, triton, gpu]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part2 Ch4 Serving platforms]]"]
---

# Model serving platforms

**모델을 안정적이고 빠른 API 서비스로 전환하는 계층.** 배포·운영 자동화, 안정성·고성능 보장,
오토스케일이 하는 일이다.

> **"선택은 개발 편의성 문제가 아니라 운영 비용과 안정성을 위한 것."**
> 잘못 고르면: 배포 복잡도 증가 · **최대 성능 도달 실패** · 장애 대응 어려움 · 팀 생산성 저하.

## ⭐ 비교 — 하나의 축이 나머지를 결정한다

| 항목 | [[FastAPI]] | [[TorchServe]] | [[BentoML]] | [[NVIDIA Triton Inference Server\|Triton]] |
|---|---|---|---|---|
| **추상화 수준** | 낮음 | 중 | 중~높음 | **매우 높음** |
| **성능 최적화** | 직접 | 제한적 | 기본 제공 | **매우 우수** |
| **GPU 활용** | 직접 | 가능 | 가능 | **최적화** |
| **운영 난이도** | **낮음** | 중 | 중 | 높음 |
| **확장성** | 직접 설계 | 제한적 | 비교적 좋음 | **매우 우수** |

**추상화 수준이 성능·GPU·확장성을 거의 그대로 결정한다.** 그런데 **"운영 난이도"만은 추상화와
같은 방향으로 움직인다** — 추상화가 높다고 운영이 쉬워지지 않는다. 이 표의 반직관적인 부분이고,
선택을 실제로 가르는 지점이다.

## 네 가지 설계 철학

| | 무엇을 준다 | 무엇을 포기한다 |
|---|---|---|
| **[[FastAPI]]** | 자유도, 백엔드 팀과의 협업, 복잡한 비즈니스 로직 | 모델 관리·버전 관리·배포 자동화·성능 튜닝을 **전부 직접** |
| **[[TorchServe]]** | PyTorch 통합, 기본 버전 관리, GPU 서빙, **Java frontend로 장애 격리** | PyTorch 종속, 커스텀 확장 제한, **Frontend가 Stateful → K8s Native 아님** |
| **[[BentoML]]** | **API Server와 Runner 분리 → 독립 스케일링**, 패키징·버전 관리 내장, 멀티 프레임워크 | 대규모 트래픽 튜닝은 추가 설계, 추상화 내부 이해 필요 |
| **[[NVIDIA Triton Inference Server\|Triton]]** | C++ 코어, **Per-Model Scheduler + Dynamic Batching**, Concurrent Model Execution, Model Ensemble | **비즈니스 로직 직접 구현 불가**, 진입 장벽·운영 복잡도 |

## 반복되는 두 가지 설계 패턴

네 플랫폼을 나란히 놓으면 같은 문제에 대한 같은 답이 반복된다.

### 1. 배치(batching) — GPU를 쓰기 위한 전제

- TorchServe: **Optional Request Batching**
- BentoML: **Adaptive Batching** (Runner가 런타임에 자동으로 모음)
- Triton: **Dynamic Batching** + **Sequence Batching**(순서 보장이 필요한 RNN 등)

셋 다 자랑하는 이유는 하나다 — **GPU는 빠른 단일 추론기가 아니라 병렬 연산 장치이고,
배치 없이는 GPU 이점이 거의 사라진다** → [[Inference optimization]].

### 2. I/O 계층과 연산 계층의 분리

| 플랫폼 | I/O 계층 | 연산 계층 | 분리한 이유 |
|---|---|---|---|
| TorchServe | Frontend (Java) | Backend Worker (Python) | **장애 격리** — 추론이 죽어도 프론트는 산다. 네트워크는 Java, 연산은 Python |
| BentoML | API Server (Async/IO Bound) | Runner (CPU/GPU Bound) | **독립 스케일링** — CPU 일과 GPU 일을 따로 늘린다 |
| Triton | HTTP/gRPC Endpoint (로직 없음) | Per-Model Scheduler → Backends | **네트워크 계층을 단순화**해 GPU 활용에 집중 |

**같은 관찰에서 나온 세 가지 답이다: 전처리(CPU)와 추론(GPU)의 부하 특성이 다르다.**
전처리는 널널한데 GPU만 병목일 때 서버 전체를 복제하면 자원 낭비다.

## Kubernetes 궁합 — 갈리는 지점

- **TorchServe**: Frontend가 Stateful, Horizontal 스케일링이 어려움 ⇒ **K8s Native하지 않음**.
  Frontend 장애 시 모든 추론이 즉시 중단(single choke point).
- **Triton**: Model Repository가 **모델을 서버 코드가 아닌 데이터 자산으로 취급**,
  컨테이너 재시작 없이 동적 로드/언로드 ⇒ **K8s + PVC와 궁합이 매우 좋음**.
- **BentoML**: Bento(표준 배포 단위) + **Yatai**(K8s 배포·관리 플랫폼)로 명시적으로 대응.

> **강의가 명시적으로 잇지는 않지만 TorchServe와 Triton이 정확히 대칭이다.**
> 그리고 강의가 TorchServe의 "커뮤니티/활성도 감소 추세"를 언급한 이유이기도 하다.

## 고르는 순서 (이 위키의 정리)

강의는 명시적 결정 트리를 주지 않는다. 위 표에서 도출하면:

1. **모델이 하나이고 비즈니스 로직이 무거운가** → [[FastAPI]] (또는 BentoML의 API Server)
2. **여러 프레임워크 모델을 운영하고 CPU/GPU를 따로 스케일해야 하는가** → [[BentoML]]
3. **GPU 가동률과 처리량이 비용을 좌우하는가** → [[NVIDIA Triton Inference Server]]
4. **PyTorch 단일 스택이고 K8s를 안 쓰는가** → [[TorchServe]] (다만 활성도 하락 유의)

⚠️ **이 순서는 강의 본문이 아니라 비교표에서의 추론이다.**

## 열린 질문

- **Ray Serve** — 슬라이드 로고에는 반복해서 등장하지만 **본문에서 한 번도 설명되지 않는다.**
  BentoML·Triton과 어떻게 다른지 공백.
- **vLLM / TGI 같은 LLM 전용 서빙** — PagedAttention·continuous batching 등 LLM 서빙의 별도
  계보가 전혀 다뤄지지 않는다. [[LLMOps]]를 다루면서 서빙은 전통 ML 기준이다.
- **KServe** — K8s 표준 서빙 레이어가 언급되지 않는다. TorchServe의 "K8s Native 아님"을
  지적하면서 그 해법 계열을 말하지 않는 건 공백이다.
- **실제 벤치마크 없음** — "매우 우수", "제한적" 같은 정성 평가만 있고 수치 비교가 없다.

## 링크

- 서빙 방식 결정: [[Batch and online serving]]
- 자원·최적화: [[Inference optimization]] · [[ONNX]]
- 개별 도구: [[FastAPI]] · [[TorchServe]] · [[BentoML]] · [[NVIDIA Triton Inference Server]]
- 상위: [[MLOps]]
- 출처: [[AI DE Course - Part2 Ch4 Serving platforms]]

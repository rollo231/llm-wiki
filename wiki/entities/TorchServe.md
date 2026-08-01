---
type: entity
title: TorchServe
area: [data-engineering]
aliases:
  - Torchserve
  - 토치서브
  - Model Handler
  - mar
tags: [data-engineering, mlops, serving, pytorch, torchserve, gpu]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part2 Ch4 Serving platforms]]"]
---

# TorchServe

**PyTorch 공식 서빙 프레임워크.** 모델 서버 역할에 집중하며 중간–대규모 서빙을 노린다.
→ [[Model serving platforms]]

| 장점 | 제약 |
|---|---|
| PyTorch 모델과 자연스러운 통합 | **PyTorch 종속** |
| 기본적인 모델 버전 관리 제공 | 커스텀 로직 확장이 상대적으로 제한적 |
| GPU 서빙 지원 | **커뮤니티/활성도 감소 추세** |

## 구조 — Frontend(Java) / Backend(Python)

```
[Management API 8081] ┐
                      ├→ Frontend (Java)  ──소켓──→ Backend (Python)
[Inference API 8080]  ┘   · Process orchestration      · Worker Process ×N
                          · Optional request batching     └ Model Handler → Trained model
                          · Logging & Metrics                        ↕
                                                            Model Store (.mar)
```

### Frontend (Java) — '통제'

| 구성 | 역할 |
|---|---|
| **Management API (8081)** | 모델 등록(Register)·삭제, **워커 개수 조절** |
| **Inference API (8080)** | 실제 사용자 예측 요청 |
| **Optional Request Batching** | 개별 요청을 모아 모델에 전달하는 **동적 배치** — GPU 효율 극대화 |
| Logging & Metrics | 서버 로그·성능 지표 수집 → 모니터링 시스템 |
| Process Orchestration | 백엔드 워커 상태 확인, 설정에 따른 워커 스케일링 |

### Backend (Python) — '실행'

- **Worker Process** — 각 모델 워커가 **독립된 Python 프로세스**로 구동.
  **GIL(Global Interpreter Lock)의 영향을 최소화**하고 모델 단위 병렬 처리를 얻는다.
  CPU/GPU를 물리적으로 점유하며 프론트엔드와 소켓 통신.
- **Model Handler** — 입력 데이터가 모델을 거쳐 출력되기까지 전 과정을 제어하는 Python 클래스.
  **"TorchServe라는 규격화된 틀 안에서 엔지니어가 비즈니스 로직을 주입하는 유일한 통로."**

  | 단계 | 하는 일 |
  |---|---|
  | **Initialize** | 모델 가중치 로드 + GPU 메모리 적재. **서버 시작 시 1회** |
  | **Pre-process** | Base64 이미지·Raw Text 등 비정형을 **Tensor로 변환**. 정규화·리사이징·토큰화 — **데이터 품질을 결정하는 단계** |
  | **Inference** | 원시 예측값(Raw Logits) 산출. 단일 요청뿐 아니라 **Batch 데이터에 대한 연산 효율 최적화 필요** |
  | **Post-process** | 확률값·텐서를 사람이 읽을 형식(JSON·Label)으로 정제, 비즈니스 요구에 맞춰 필터링·포맷팅 |

- **Model Store** — `.mar`(Model Archive) 형태. **모델 파일 + Handler + 설정 정보**를 함께 담아
  **배포 단위 관리를 담당**한다.

> **`.mar`이 "추론 코드도 아티팩트"라는 관점을 강제한다.** 모델 가중치만 배포하면 전처리 규칙이
> 코드베이스에 남아 학습과 어긋난다 —
> [[Data drift and training-serving skew]]의 skew 패턴 그대로다. 핸들러를 모델과 함께 패키징하는
> 것은 그 방어책이기도 하다.

## 왜 두 언어로 나눴나

강의의 설명 두 가지:

- **안정성** — 모델 추론 중 에러로 백엔드 프로세스가 죽어도 **Java 프론트엔드는 살아있어**
  시스템 전체 장애로 번지지 않는다.
- **언어의 조화** — 네트워크 처리와 동시성에 강한 Java가 입구를, 딥러닝 생태계가 풍부한 Python이
  연산을 맡는다.

## 한계 — 강의가 솔직한 부분

- **Frontend의 병목** — QPS 증가 시 **Frontend CPU 사용률이 먼저 포화**
- **Frontend 장애 = 모든 추론 즉시 중단** (Single choke point)
- **Frontend는 Stateful, Horizontal 스케일링이 어려운 구조 ⇒ Kubernetes Native하지 않음**
- GPU를 **Worker 단위로 할당** — GPU 공유·MIG·동적 배치 관리 지원이 제한적

> **"Kubernetes Native하지 않다"가 결정적이다.** 장애 격리를 위해 도입한 Frontend/Backend 분리가,
> 프론트엔드를 상태 있는 단일 관문으로 만들어 **수평 확장을 막는다.** 같은 결정이 장점이자 한계다.
>
> [[NVIDIA Triton Inference Server]]가 정확히 반대편에 선다 — 모델을 데이터 자산으로 취급하고
> K8s + PVC와 궁합이 좋다.

## 열린 질문

- **"커뮤니티/활성도 감소 추세"의 근거** — 강의가 주장만 하고 자료를 대지 않는다. 프로젝트의 현재
  유지보수 상태를 1차 자료로 확인할 필요가 있다.
- **Frontend를 여러 대 두면?** — Stateful이라 안 된다는 서술은 있지만 무엇이 상태인지(모델 등록
  정보? 워커 핸들?)는 설명하지 않는다.

## 링크

- 비교: [[Model serving platforms]]
- 대칭: [[NVIDIA Triton Inference Server]] (K8s 궁합) · [[BentoML]] (독립 스케일링)
- 서빙 아키텍처: [[Batch and online serving]] · [[Inference optimization]]
- 출처: [[AI DE Course - Part2 Ch4 Serving platforms]]

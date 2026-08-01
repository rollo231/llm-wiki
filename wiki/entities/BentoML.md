---
type: entity
title: BentoML
area: [data-engineering]
aliases:
  - Bento
  - Yatai
  - Runner
  - Adaptive batching
tags: [data-engineering, mlops, serving, bentoml, kubernetes, packaging, gpu]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part2 Ch4 Serving platforms]]"]
---

# BentoML

**모델 서빙 중심 ML 서빙 프레임워크.** 강의의 요약은 "FastAPI + ML 기능을 결합한 구조".
→ [[Model serving platforms]]

| 장점 | 제약 |
|---|---|
| **모델 패키징·버전 관리 내장** | 대규모 트래픽에서의 성능 튜닝은 추가 설계 필요 |
| 다양한 프레임워크 지원 (PyTorch, TF, sklearn) | **추상화가 늘어날수록 내부 동작 이해 필요** |
| 비교적 낮은 진입 장벽 | |

## 구조 — API Server와 Runner의 분리

```
BentoML Service
├─ API Server  (Async / I/O Bound)          ← CPU 위주로 확장
│   ├─ HTTP/gRPC Endpoint
│   ├─ Data Validation (Pydantic)
│   └─ Business Logic
└─ Runners     (GPU / CPU Bound)            ← GPU 노드에 집중 배치
    ├─ Runner: Model A (PyTorch)  — Inference + Pre/Post-processing
    └─ Runner B (TensorFlow)      — Inference
        ⇒ Independent Scaling / Adaptive Batching
```

### API Server — The Entry Point

- **비동기 통신(Async / I/O Bound)** — 수많은 사용자 요청을 동시에 수신·관리
- **데이터 검증(Pydantic)** — **유효하지 않은 요청이 무거운 모델 연산(Runner)까지 도달하지 않도록
  입구에서 차단**
- **비즈니스 로직** — 단순 추론 외에 데이터 가공, DB 조회, 결과 필터링

> 이 층이 하는 일은 [[FastAPI]]와 거의 같다. BentoML의 차별점은 이 위가 아니라 **아래**에 있다.

### Runners — The Compute Engine

- **모델 전용 프로세스 (CPU/GPU Bound)** — 실제 모델 가중치를 로드하고 연산을 수행하는 독립 단위
- **프레임워크 독립성** — 한 서비스 안에서 **PyTorch(모델 A)와 TensorFlow(모델 B)를 동시에 운영**
- **격리된 전/후처리** — 모델별 특화된 핸들러 로직이 러너 내부에서 독립 실행

## 두 가지 핵심 기능

### Independent Scaling

- **자원 최적화** — 요청을 받는 API 서버는 CPU 위주로 확장하고, 연산이 무거운 Runner는 GPU 노드에
  집중 배치
- **병목 해결** — 특정 모델(Runner B)의 부하가 **다른 모델이나 API 서버의 응답 속도에 영향을 주지
  않음**

> **동기: "전처리 로직(CPU)은 널널한데 모델 연산(GPU)만 병목이 생길 때, 서버 전체를 복제하면
> 불필요한 자원 낭비가 발생한다."**
> API Server(CPU)와 Runner(GPU)를 각각 **필요한 만큼만** 늘릴 수 있어 비용을 절감한다.

### Adaptive Batching

여러 API 서버에서 들어온 다수의 개별 요청을 **Runner가 런타임에서 자동으로 모아 배치 연산으로 전환.**
**"복잡한 멀티프로세싱 로직을 직접 짤 필요 없이, 설정만으로 GPU 처리량을 최대 사용."**

배경: **사용자의 요청이 하나씩 들어올 때마다 GPU가 작동하면 연산 효율이 극도로 떨어진다** —
[[Inference optimization]]의 "배치 없이는 GPU 이점이 사라진다"와 같은 이야기.

## 패키징과 배포 — Bento와 Yatai

| | 무엇 |
|---|---|
| **Bento** (도시락) | 모델·코드·환경 설정을 하나로 묶은 **표준화된 배포 단위**. 모델 파일 + Runner 정의 + API 정의 + 의존성 정보 + 환경 설정. Docker 컨테이너화 자동 지원 |
| **Yatai** (포장마차) | 생성된 Bento를 **쿠버네티스로 배포하고 관리하는 오케스트레이션 플랫폼** |

**해결하려는 문제:** "모델 가중치, 전처리 코드, Python 라이브러리 버전이 엉켜 서버 배포 시 에러가
발생하는 경우."
⇒ **`bentofile.yaml` 하나로 패키징**, `bento build` 명령 한 번으로 Docker 이미지 자동 생성 →
**로컬/스테이징/운영 어디서나 환경 일관성(Environment Consistency) 보장.**

> [[Data and model versioning]]이 말한 "재현성 3요소" 중 **환경**을 도구로 강제하는 형태다.
> [[TorchServe]]의 `.mar`이 모델+핸들러를 묶었다면, Bento는 **환경까지** 묶는다.

## 열린 질문

- **Runner 간 통신 비용** — API Server와 Runner를 프로세스/노드로 분리하면 그 사이 직렬화와
  네트워크 홉이 생긴다. [[NVIDIA Triton Inference Server]]가 Shared Memory와 Model Ensemble로
  줄이려는 바로 그 비용인데, BentoML 쪽 설명이 없다.
- **Yatai의 현재 상태** — 프로젝트 활성도·대체재(BentoCloud 등) 확인 필요.
- **"대규모 트래픽에서 추가 튜닝 필요"의 구체** — 어느 지점에서 무엇이 막히는지가 없다.

## 링크

- 비교: [[Model serving platforms]]
- 인접: [[FastAPI]] (API Server 층) · [[TorchServe]] · [[NVIDIA Triton Inference Server]]
- 배치와 GPU: [[Inference optimization]]
- 서빙 아키텍처: [[Batch and online serving]]
- 출처: [[AI DE Course - Part2 Ch4 Serving platforms]]

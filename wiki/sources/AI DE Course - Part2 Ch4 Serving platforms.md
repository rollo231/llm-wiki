---
type: source
title: AI DE Course - Part2 Ch4 Serving platforms
area: [data-engineering, programming]
aliases: [Part2 Ch4-2,3, 서빙 플랫폼 선택 기준 및 기술 스택]
tags: [data-engineering, course, fast-campus, serving, fastapi, torchserve, bentoml, triton]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part2/04. Ch4. 서빙 아키텍처 및 플랫폼.pdf"]
---

# AI DE Course - Part2 Ch4 Serving platforms

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 2 Ch4** "서빙 아키텍처 및
플랫폼"의 소단원 **2·3** "서빙 플랫폼 선택 기준 및 기술 스택 (1)(2)". 강사 **Habi**. 원본(로컬):
`raw/data-engineering/ai-de-course/part2/04. Ch4. 서빙 아키텍처 및 플랫폼.pdf` **p17–60**. 강의 홈:
[[AI Data Engineering (Fast Campus course)]].

**Part 2에서 가장 긴 단일 주제(44p)이고, 4종 플랫폼의 내부 구조를 하나씩 뜯는다.**
개념 축은 [[Model serving platforms]], 개별 도구는 각 entity 페이지로 분리했다.

## 전제 — "선택은 개발 편의성 문제가 아니라 운영 비용과 안정성을 위한 것"

서빙 플랫폼이 하는 일: 모델을 안정적이고 빠른 API 서비스로 전환 / 배포·운영 자동화 /
안정성·고성능 보장, 오토스케일.

**잘못된 선택으로 이어지는 문제:** 배포 복잡도 증가 · **최대 성능 도달 실패** ·
장애 대응 어려움 · 팀 생산성 저하.

## 1. FastAPI — 최소한의 서빙 구조

일반적인 Python 웹 프레임워크. **서빙 로직을 직접 구현**한다.

| 장점 | 제약 |
|---|---|
| 높은 자유도 | **모델 관리·버전 관리·배포 자동화를 직접 구현해야 함** |
| 기존 백엔드 팀과 협업 용이 | **성능 튜닝은 전적으로 개발자 책임** |
| 복잡한 비즈니스 로직 구현에 유리 | |

### 아키텍처 — 왜 빠른가

강의가 tiangolo(FastAPI 저자)의 "Performance with FastAPI" 도식을 인용해 층을 뜯는다.

```
FastAPI
├─ Starlette (web toolkit / micro-framework)   ← 웹 기능: 라우팅·세션·쿠키·웹소켓
│   └─ Uvicorn (implements ASGI spec)
│       └─ Uvloop (high-performance asyncio)
│           └─ Cython (compiled Python / C-extensions)
└─ Pydantic (data validation, serialization, documentation)
    └─ Cython
```

- **Starlette (Backbone)** — FastAPI는 Starlette을 **직접 상속받은 클래스**라 Starlette의 모든
  기능을 그대로 쓸 수 있다.
- **Uvicorn & ASGI** — 파이썬 표준 비동기 인터페이스. **수천 개의 동시 접속을 효율적으로 관리.**
- **uvloop** — 파이썬 기본 이벤트 루프(asyncio)를 C로 작성된 고성능 루프로 대체.
  **"네트워크 입출력 속도를 Node.js나 Go 수준으로 끌어올림."**
- **Cython** — 파이썬 코드를 C로 변환·컴파일. uvloop과 Pydantic은 **C로 컴파일된 바이너리 상태로
  실행**되어 "인터프리터 방식의 파이썬 한계를 하드웨어 레벨에서 해결".
- **Pydantic** — 데이터 검증·직렬화. **내부 로직이 Rust와 Cython으로 최적화.**

**WSGI vs ASGI**

| WSGI | ASGI |
|---|---|
| 동기적, 한 번에 하나의 요청만 처리 | **비동기적, 동시에 여러 요청 처리** |
| 파이썬 웹 앱–웹 서버 간 표준 인터페이스 | WSGI의 비동기 버전, 웹소켓 등 비동기 프로토콜 지원 |

> **이 절이 위키의 첫 `programming` 영역 실질 내용이다.** → [[FastAPI]]

## 2. TorchServe — PyTorch 중심 모델 서버

PyTorch 공식 서빙 프레임워크. 모델 서버 역할에 집중, 중간–대규모 서빙.

| 장점 | 제약 |
|---|---|
| PyTorch 모델과 자연스러운 통합 | **PyTorch 종속** |
| 기본적인 모델 버전 관리 제공 | 커스텀 로직 확장이 상대적으로 제한적 |
| GPU 서빙 지원 | **커뮤니티/활성도 감소 추세** |

### 아키텍처 — Frontend(Java) / Backend(Python) 분리

- **Frontend (Java 기반)** — 요청 접수, 스케줄링, 모델 관리 등 시스템 전반의 **'통제'**
  - **Management API (8081)** — 모델 등록/삭제, 워커 개수 조절
  - **Inference API (8080)** — 실제 예측 요청
  - **Optional Request Batching** — 개별 요청을 모아 전달하는 **동적 배치**, GPU 효율 극대화
  - Logging & Metrics, Process Orchestration(워커 상태 확인·스케일링)
- **Backend (Python 기반)** — 실제 추론이 일어나는 **'실행'** 계층
  - **Worker Process** — 각 모델 워커가 **독립된 Python 프로세스**로 구동되어 **GIL 영향을 최소화**,
    모델 단위 병렬 처리. CPU/GPU를 물리적으로 점유하고 프론트엔드와 **소켓 통신**.
  - **Model Handler** — 입력→출력 전 과정을 제어하는 Python 클래스.
    **"엔지니어가 비즈니스 로직을 주입하는 유일한 통로"**. 4단계: Initialize(가중치 로드·GPU 적재,
    서버 시작 시 1회) → Pre-process(Base64 이미지·Raw Text → Tensor, 정규화·리사이징·토큰화) →
    Inference(Raw Logits 산출) → Post-process(JSON·Label로 정제).
- **Model Store** — `.mar`(Model Archive) 형태. 모델 파일 + Handler + 설정 정보를 함께 담는다
  → **배포 단위 관리를 담당**.

> **왜 굳이 두 언어로 나눴나 (강의의 설명):**
> **안정성** — 모델 추론 중 에러로 백엔드 프로세스가 죽어도 Java 프론트엔드는 살아있어 시스템 전체
> 장애로 번지지 않는다. **언어의 조화** — 네트워크·동시성에 강한 Java가 입구를, 딥러닝 생태계가
> 풍부한 Python이 연산을 맡는다.

### 한계 — 이 강의의 솔직한 부분

- **Frontend의 병목 가능성** — QPS 증가 시 **Frontend CPU 사용률이 먼저 포화**
- **Frontend 장애 시 모든 추론 요청이 즉시 중단** (Single choke point)
- **Frontend는 Stateful, Horizontal 스케일링이 어려운 구조 ⇒ Kubernetes Native하지 않음**
- GPU를 **Worker 단위로 할당** — GPU 공유·MIG·동적 배치 관리 지원이 제한적

> **"Kubernetes Native하지 않다"**가 결정적 지적이다. 뒤의 Triton이 정확히 이 반대편에 선다.
> → [[TorchServe]]

## 3. BentoML — "FastAPI + ML 기능"

모델 서빙 중심 ML 서빙 프레임워크.

| 장점 | 제약 |
|---|---|
| **모델 패키징·버전 관리 내장** | 대규모 트래픽에서의 성능 튜닝은 추가 설계 필요 |
| 다양한 프레임워크 지원 (PyTorch, TF, sklearn) | **추상화가 늘어날수록 내부 동작 이해 필요** |
| 비교적 낮은 진입 장벽 | |

### 아키텍처 — API Server와 Runner의 분리

```
BentoML Service
├─ API Server  (Async / I/O Bound)      ← CPU 위주로 확장
│   ├─ HTTP/gRPC Endpoint
│   ├─ Data Validation (Pydantic)
│   └─ Business Logic
└─ Runners     (GPU / CPU Bound)        ← GPU 노드에 집중 배치
    ├─ Runner: Model A (PyTorch) — Inference + Pre/Post-processing
    └─ Runner B (TensorFlow) — Inference
        ⇒ Independent Scaling / Adaptive Batching
```

- **API Server (The Entry Point)** — 비동기 통신으로 다수 요청 수신·관리. **Pydantic 검증으로
  유효하지 않은 요청이 무거운 Runner까지 도달하지 않도록 입구에서 차단.** 데이터 가공·DB 조회·결과
  필터링 같은 비즈니스 로직 수행.
- **Runners (The Compute Engine)** — 모델 전용 프로세스. **프레임워크 독립성** — 한 서비스 안에서
  PyTorch(모델 A)와 TensorFlow(모델 B)를 동시에 운영 가능. 모델별 전/후처리가 러너 내부에서 격리 실행.
- **Independent Scaling** — 요청받는 API 서버는 CPU 위주로, 연산이 무거운 Runner는 GPU 노드에.
  **특정 모델의 부하가 다른 모델이나 API 서버 응답 속도에 영향을 주지 않음.**
- **Adaptive Batching** — 여러 API 서버에서 들어온 다수의 개별 요청을 **Runner가 런타임에서 자동으로
  모아 배치 연산으로 전환.**
- **Bento(도시락)** — 모델·코드·환경 설정을 하나로 묶은 표준 배포 단위. `bentofile.yaml` 하나로
  패키징, `bento build` 한 번으로 Docker 이미지 자동 생성 → **로컬/스테이징/운영 어디서나 환경
  일관성 보장.**
- **Yatai(포장마차)** — 생성된 Bento를 쿠버네티스로 배포·관리하는 오케스트레이션 플랫폼.

> **BentoML의 논지는 "CPU 일과 GPU 일을 따로 스케일하라"** 하나로 요약된다. 전처리 로직(CPU)은
> 널널한데 모델 연산(GPU)만 병목일 때 서버 전체를 복제하면 자원 낭비다. → [[BentoML]]

## 4. NVIDIA Triton Inference Server — 고성능 추론 엔진

| 장점 | 제약 |
|---|---|
| 매우 높은 성능 | **진입 장벽 높음** |
| 동적 배치, 멀티모델, GPU 최적화 | **비즈니스 로직 직접 구현 불가** |
| 다양한 프레임워크 지원 (ONNX, TensorRT 등) | 운영 복잡도 높음 |

### 구조

`Client Application → Python/C++ Client Library → HTTP/gRPC → [Inference Request →
Per-Model Scheduler Queues → Framework Backends → Inference Response] ← Model Repository`,
하단에 `Status/Health Metrics Export → HTTP`, 최하단에 GPU×4 + CPU.

- **HTTP/gRPC Endpoint** — 외부 요청의 단일 진입점. **"여기서는 비즈니스 로직을 처리하지 않는다!"**
  FastAPI와 달리 validation·routing·auth 중심이 아니라 **목적은 오직 Inference Request 전달**.
  설계 의도는 **네트워크 계층을 단순화하여 내부 스케줄링과 GPU 활용에 집중**하는 것.
- **Model Repository / Model Management** — 동적 로드/언로드, 버전 관리(1, 2, 3…).
  **컨테이너 재시작 없이 모델 교체 가능. 모델은 서버 코드에 포함되지 않고 데이터 자산처럼 취급.**
  **Kubernetes + PVC와 궁합이 매우 좋음.**
- **Per-Model Scheduler Queues** — **Triton의 핵심 기술.** 각 모델이 자신만의 독립 대기열을 가짐.
  **요청 단위로 즉시 실행하지 않고 Scheduler가 개입, GPU 효율을 최우선으로 고려.**
  - **Dynamic Batching** — 여러 클라이언트의 개별 요청을 지능적으로 모아 하나의 배치로 구성
  - **Sequence Batching** — 상태 정보가 필요한 모델(RNN 등)을 위해 **요청 순서를 보장하며** 배치 구성
- **Framework Backends** — TensorRT·TensorFlow·PyTorch·ONNX + **사용자 정의 Custom Backend**.
  **Concurrent Model Execution** — 동일 GPU 내에서 서로 다른 프레임워크의 모델을 동시 실행.
- **하드웨어 추상화** — 특정 모델은 GPU 0번, 다른 모델은 CPU에 할당하는 식의 정교한 자원 배분.
  Status/Health(Liveness/Readiness)와 추론 통계(Latency·Throughput)를 HTTP로 Prometheus에 전송.

**왜 Triton인가 (강의 정리)**

- **극한의 성능** — C++ 기반 코어로 **파이썬 인터프리터 오버헤드 완벽 제거** · Dynamic Batching ·
  **Shared Memory**(대용량 영상/이미지 전송 시 메모리 복사 비용 최소화)
- **통합 운영** — 파편화된 멀티프레임워크 모델을 단일 서버에서 관리 · **Model Ensemble**: 전처리부터
  여러 모델 추론까지 전 과정을 **서버 내부 DAG로 구성하여 네트워크 지연 제거**
- **비용 절감** — Concurrent Execution으로 **가속기 가동률을 100%에 가깝게 유지 → TCO 절감**

> **Model Ensemble이 Triton의 숨은 킬러 기능이다** — 전처리 서비스와 모델 서비스를 따로 두면
> 그 사이 네트워크 홉이 latency로 잡히는데, 서버 안 DAG로 넣으면 사라진다. → [[NVIDIA Triton Inference Server]]

## ⭐ 4종 비교표

| 항목 | FastAPI | TorchServe | BentoML | Triton |
|---|---|---|---|---|
| **추상화 수준** | 낮음 | 중 | 중~높음 | **매우 높음** |
| **성능 최적화** | 직접 | 제한적 | 기본 제공 | **매우 우수** |
| **GPU 활용** | 직접 | 가능 | 가능 | **최적화** |
| **운영 난이도** | **낮음** | 중 | 중 | 높음 |
| **확장성** | 직접 설계 | 제한적 | 비교적 좋음 | **매우 우수** |

> **하나의 축(추상화 수준)이 나머지를 거의 결정한다.** 추상화가 올라갈수록 성능·확장성은 좋아지고
> 자유도·운영 편의는 떨어진다. **다만 "운영 난이도"만은 추상화와 같은 방향으로 움직인다** —
> 추상화가 높다고 운영이 쉬워지지 않는다는 것이 이 표의 반직관적인 부분이다.
> → [[Model serving platforms]]

## 기존 페이지와의 대조

- **신규** — 위키에 서빙 플랫폼 관련 내용이 전혀 없었다. 개념 1 + entity 4가 새로 생긴다.
- **`programming` 영역 개시** — FastAPI 내부 구조(Starlette·Uvicorn·uvloop·Cython·Pydantic,
  WSGI vs ASGI)가 이 위키의 첫 프로그래밍 영역 실질 콘텐츠다.
- **연결** — TorchServe의 "Frontend가 Stateful이라 K8s Native하지 않다"와 Triton의 "Model
  Repository는 K8s+PVC와 궁합이 좋다"가 **정확히 대칭**이다. 강의가 명시적으로 잇지는 않는다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Model serving platforms]] (비교 축) · [[Batch and online serving]]
- 도구: [[FastAPI]] · [[TorchServe]] · [[BentoML]] · [[NVIDIA Triton Inference Server]] · [[ONNX]]
- 앞: [[AI DE Course - Part2 Ch4 Serving architecture]]
- 다음: [[AI DE Course - Part2 Ch4 CPU and GPU inference]]

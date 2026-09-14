---
type: source
title: AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton
aliases: [AI DE 2-08]
tags: [AI-DE-강의, 서빙, MLOps, 도구]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/data-engineering/ai-de-course/part2/04. Ch4. 서빙 아키텍처 및 플랫폼.pdf"
---

# AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton

[[AI 데이터 엔지니어링 강의]] Part 2 Ch4의 두 번째·세 번째 소단원. 제목이 같은 "서빙 플랫폼 선택 기준 및 기술 스택
1·2"를 한 페이지로 묶었다. (1) 서빙 플랫폼의 의미, [[FastAPI]], [[TorchServe]], (2) [[BentoML]],
[[Triton Inference Server]], 네 플랫폼 비교.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 2 「AI 학습/추론 중심 데이터 파이프라인 설계」 |
| 덱 제목 | Ch4. 서빙 아키텍처 및 플랫폼 — 2. 서빙 플랫폼 선택 기준 및 기술 스택 1 · 3. 서빙 플랫폼 선택 기준 및 기술 스택 2 |
| 원본 파일 | `part2/04. Ch4. 서빙 아키텍처 및 플랫폼.pdf` p17–37 (21p) · p38–59 (22p), 덱 전체 77p |
| 강사 | Habi (슬라이드 표기) |
| 작성 시기 | PDF 생성일 2026-03-24 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명 Ch4, 소단원 2·3 (표지 슬라이드) |

## 요약

### (1) 서빙 플랫폼이란

- 서빙 플랫폼은 **모델을 안정적이고 빠른 API 서비스로 바꾸는 것**을 돕는다 — 배포·운영 자동화, 안정성과 고성능, 오토스케일.
- **선택은 개발 편의가 아니라 운영 비용과 안정성의 문제다.** 잘못 고르면 배포 복잡도 증가, 최대 성능 도달 실패, 장애 대응
  어려움, 팀 생산성 저하가 온다.
- 종류로 네 로고를 보여 준다(p20): PyTorch(TorchServe), BentoML, FastAPI, NVIDIA Triton Inference Server.

### FastAPI — 최소한의 서빙 구조, 소규모 서빙

일반 Python 웹 프레임워크에 서빙 로직을 직접 구현한다.

| 장점 | 제약 |
|---|---|
| 높은 자유도 | 모델 관리·버전 관리·배포 자동화를 직접 구현 |
| 기존 백엔드 팀과 협업 용이 | 성능 튜닝은 전적으로 개발자 책임 |
| 복잡한 비즈니스 로직 구현에 유리 | |

아키텍처(p22 도식 "Performance with FastAPI", @tiangolo):

- **Starlette** — 가벼운 ASGI 툴킷. 라우팅·세션·쿠키·웹소켓 담당. FastAPI는 Starlette을 직접 상속한 클래스다.
- **실행·네트워크 계층** — Uvicorn이 ASGI를 구현해 수천 개 동시 접속을 관리. **uvloop**이 asyncio 기본 이벤트 루프를 C로
  쓴 고성능 루프로 대체해 "네트워크 입출력을 Node.js나 Go 수준으로". **Cython**으로 uvloop·Pydantic의 주요 로직이 C로
  컴파일된 바이너리로 실행되어 "인터프리터 방식 파이썬의 한계를 하드웨어 레벨에서 해결".
- **WSGI vs ASGI** — WSGI는 동기라 "한 번에 하나의 요청만" 처리, ASGI는 비동기라 동시에 여러 요청과 웹소켓을 처리.
- **Pydantic** — 데이터 검증·직렬화. "성능을 위해 내부 로직이 Rust와 Cython으로 최적화".

### TorchServe — PyTorch 중심 서빙 서버, 중간~대규모

| 장점 | 제약 |
|---|---|
| PyTorch 모델과 자연스러운 통합 | PyTorch 종속 |
| 기본적인 모델 버전 관리 제공 | 커스텀 로직 확장이 상대적으로 제한적 |
| GPU 서빙 지원 | 커뮤니티/활성도 감소 추세 |

아키텍처(p28 공식 도식):

- **Frontend(Java)** — 요청 접수·스케줄링·모델 관리 등 통제. Management API(8081: 모델 등록·삭제·워커 수 조절), Inference
  API(8080), 선택적 요청 배칭(동적 배치로 GPU 효율 극대화), 로깅·메트릭, 워커 프로세스 상태 확인과 스케일링.
- **Backend(Python)** — 실제 추론이 일어나는 워커 프로세스의 집합. 워커마다 독립 Python 프로세스라 GIL 영향을 줄이고,
  CPU/GPU를 점유하며 프론트엔드와 소켓으로 통신.
- **Model Handler** — 입력부터 출력까지를 제어하는 Python 클래스. 규격화된 틀 안에 비즈니스 로직을 넣는 유일한 통로.
  Initialize(가중치 로드·GPU 적재, 1회) → Pre-process(Base64 이미지·원문을 텐서로, 정규화·리사이징·토큰화) → Inference
  (원시 logits, 배치 연산 효율) → Post-process(JSON·라벨로 정제, 필터링·포매팅).
- **Model Store** — `.mar`(Model Archive) = 모델 파일 + 핸들러 + 설정. 배포 단위를 관리한다.
- **왜 나눴나** — 추론 중 백엔드 프로세스가 죽어도 Java 프론트엔드는 살아 있어 전체 장애로 번지지 않는다. 네트워크·동시성은
  Java가, 딥러닝 연산은 Python이.
- **한계(p37 요약)** — QPS가 늘면 프론트엔드 CPU가 먼저 포화, 프론트엔드 장애 시 전체 추론 중단(single choke point),
  "Frontend는 Stateful이라 수평 확장이 어렵고 Kubernetes Native 하지 않음", 워커 단위 GPU 할당이라 GPU 공유·MIG·동적 배치
  관리 지원이 제한적 → 대규모 서빙에는 제한.

### BentoML — ML 서빙 프레임워크 ("FastAPI + ML 기능")

| 장점 | 제약 |
|---|---|
| 모델 패키징·버전 관리 내장 | 대규모 트래픽에서의 성능 튜닝은 추가 설계 필요 |
| 다양한 프레임워크 지원(PyTorch·TF·sklearn) | 추상화가 늘수록 내부 동작 이해 필요 |
| 비교적 낮은 진입 장벽 | |

아키텍처(p41 도식):

- **API Server** — 비동기(I/O bound)로 요청 수신, Pydantic 검증으로 잘못된 요청이 무거운 Runner까지 가지 않게 차단, 데이터
  가공·DB 조회·결과 필터링 같은 비즈니스 로직.
- **Runners** — 모델 가중치를 로드해 연산하는 독립 프로세스(CPU/GPU bound). 한 서비스에서 PyTorch 모델 A와 TensorFlow
  모델 B를 함께 운영, 모델별 전·후처리를 러너 안에서.
- **Independent Scaling** — API 서버는 CPU 위주로, Runner는 GPU 노드에 집중 배치. 특정 러너의 부하가 다른 모델·API 서버에
  번지지 않는다.
- **Adaptive Batching** — 여러 API 서버에서 온 개별 요청을 Runner가 런타임에 모아 배치 연산으로.
- **Bento & Yatai** — Bento(도시락)는 모델·Runner 정의·API 정의·의존성·환경 설정을 묶은 배포 단위(Docker 이미지 자동 생성),
  Yatai(포장마차)는 Bento를 Kubernetes에 배포·관리하는 플랫폼.
- **왜 쓰나(p47)** — 가중치·전처리 코드·라이브러리 버전이 엉켜 배포가 깨지는 문제를 `bentofile.yaml` 하나와 `bento build`
  한 번으로 막고(로컬·스테이징·운영의 환경 일관성), 요청마다 GPU를 돌리는 비효율을 설정만으로 배칭하고, CPU 전처리와 GPU
  연산을 따로 늘려 비용을 줄인다.

### Triton Inference Server — 고성능 추론 엔진

| 장점 | 제약 |
|---|---|
| 매우 높은 성능 | 진입 장벽 높음 |
| 동적 배치, 멀티 모델, GPU 최적화 | 비즈니스 로직 직접 구현 불가 |
| 다양한 프레임워크 지원(ONNX·TensorRT 등) | 운영 복잡도 높음 |

아키텍처(p49 공식 도식):

- **Client** — 웹 서비스·배치 잡·마이크로서비스, Python/C++ 클라이언트 라이브러리(HTTP/gRPC). 입력 텐서를 직렬화하고 결과를
  복원.
- **HTTP/gRPC Endpoint** — 단일 진입점. FastAPI와 달리 검증·라우팅·인증이 아니라 **추론 요청 전달만** 한다 — 네트워크 계층을
  단순화해 스케줄링과 GPU 활용에 집중.
- **Model Repository / Management** — 모델을 동적으로 로드·언로드, 버전(1, 2, 3…) 관리, 컨테이너 재시작 없이 교체. 모델은
  서버 코드가 아니라 데이터 자산처럼 다룬다. Kubernetes + PVC와 궁합.
- **요청 처리** — 즉시 실행하지 않고 큐에 적재 → 배치 가능 여부 판단 → 실행. 스케줄러가 GPU 효율을 우선한다.
- **Per-Model Scheduler Queues** — 모델마다 독립 대기열. Dynamic Batching(개별 요청을 모아 배치), Sequence Batching(RNN처럼
  상태가 필요한 모델을 위해 순서 보장).
- **Framework Backends** — TensorRT·TensorFlow·PyTorch·ONNX·Custom. 같은 GPU에서 서로 다른 프레임워크 모델을 동시 실행.
- **Compute Resources** — 모델별로 GPU 0번·CPU 등 자원 배분, Liveness/Readiness와 Latency·Throughput을 Prometheus 등으로 내보냄.
- **왜 Triton인가** — C++ 코어로 "파이썬 인터프리터의 오버헤드 완벽 제거", Dynamic Batching, Shared Memory(영상·이미지 전송
  복사 비용 최소화), 멀티 프레임워크 통합, Model Ensemble(전처리~여러 모델을 서버 내부 DAG로 구성해 네트워크 지연 제거), 같은
  GPU에 다중 인스턴스로 "가동률을 100%에 가깝게 유지"해 TCO 절감.

### (2) 서빙 플랫폼 비교 (p59)

| 항목 | FastAPI | TorchServe | BentoML | Triton |
|---|---|---|---|---|
| 추상화 수준 | 낮음 | 중 | 중~높음 | 매우 높음 |
| 성능 최적화 | 직접 | 제한적 | 기본 제공 | 매우 우수 |
| GPU 활용 | 직접 | 가능 | 가능 | 최적화 |
| 운영 난이도 | 낮음 | 중 | 중 | 높음 |
| 확장성 | 직접 설계 | 제한적 | 비교적 좋음 | 매우 우수 |

## 핵심

- **네 플랫폼은 같은 종류가 아니다** — 웹 프레임워크(FastAPI)와 모델 서버(TorchServe·BentoML·Triton)는 층이 달라 겹쳐 쓸 수
  있는데, p59 비교표는 한 축에 나란히 놓는다. *(위키의 관찰)* → [[모델 서빙]]의 "서빙 플랫폼의 층"
  ⚠️ 위키 정정 (2026-09-14 린트): 처음에는 Triton을 "추론 런타임(엔진)"으로 분류했다 — Triton은 ONNX Runtime·TensorRT를
  백엔드로 돌리는 모델 서버다.
- **세 모델 서버가 같은 설계를 한다** — 요청 접수(I/O)와 추론(연산)을 분리한다: Java 프론트엔드 / Python 워커(p28),
  API Server / Runner(p41), HTTP·gRPC 엔드포인트 / 모델별 스케줄러·백엔드(p49). *(위키의 종합)* → [[모델 서빙]]
- **셋 다 요청을 잠깐 모아 GPU에 한 번에 넣는다** — TorchServe의 선택적 요청 배칭, BentoML의 Adaptive Batching, Triton의
  Dynamic Batching. 약간의 대기로 처리량을 사는 [[지연 시간과 처리량]]의 선택이다. → [[추론 최적화]]
- **이 강의의 플랫폼 절반은 가장 빨리 낡는다.** 2026-09 기준 네 플랫폼 중 TorchServe는 저장소가 보관(archived) 처리됐고,
  BentoML은 강의가 설명하는 구조(Runner·Yatai)가 레거시다. 강의는 "무엇을 살까"가 아니라 **"요청 접수와 연산을 어떻게
  나누나"라는 아키텍처 패턴**으로 읽는 것이 오래 간다. *(위키의 관찰)*
- 배포 단위(`.mar`, Bento, Triton의 버전 디렉터리)는 모두 **모델 + 추론 코드 + 설정**을 한 묶음으로 버전 관리하는 장치다.
  → [[데이터와 모델 버전 관리]]

## 주의·결함

(2026-09-14 공식 문서·GitHub 저장소와 대조)

**TorchServe**

- ⚠️ **"커뮤니티/활성도 감소 추세"는 낡은 과소 서술이다** — 2025-02-28에 Limited Maintenance 공지가 붙었고, 2025-08-07에 저장소가
  보관(읽기 전용) 처리됐다. 마지막 릴리스는 v0.12.0(2024-09-30). 슬라이드(2026-03)는 이미 1년 전에 유지보수가 끝난 도구를
  현역 선택지로 제시한다. [https://github.com/pytorch/serve — "⚠️ Notice: Limited Maintenance — This project is no longer
  actively maintained. While existing releases remain available, there are no planned updates, bug fixes, new features, or
  security patches.", 2026-09-14 확인]
- ✅ 포트는 맞다 — Inference 8080, Management 8081(메트릭 8082도 있다). [https://docs.pytorch.org/serve/rest_api.html —
  "By default, TorchServe listens on port 8080 for the Inference API and 8081 for the Management API.", 2026-09-14 확인]
- ⚠️ **"Frontend는 Stateful, Kubernetes Native 하지 않음"** — 공식 근거를 찾지 못한 강사의 평가다. 공식 저장소에는 Helm 차트
  배포와 오토스케일링 문서가 있다. [https://github.com/pytorch/serve/blob/master/kubernetes/README.md — "This page
  demonstrates a Torchserve deployment in Kubernetes using Helm Charts", 2026-09-14 확인]

**BentoML**

- ⚠️ **"API Server + Runners"는 BentoML 1.2(2024-02) 이전 구조다** — 1.2부터 서비스를 클래스로 정의하는 Services API로
  바뀌었고 Runner는 레거시 개념이 됐다(하위 호환은 유지). [https://docs.bentoml.com/en/latest/build-with-bentoml/services.html
  — "Runners are a legacy concept in BentoML 1.1", 2026-09-14 확인]
- ⚠️ `bentofile.yaml`은 여전히 지원되지만 v1.3.20부터 Python SDK로 런타임 명세를 정의하는 방식이 권장된다.
  [https://docs.bentoml.com/en/latest/reference/bentoml/bento-build-options.html — "While BentoML maintains compatibility
  with these configuration files, we recommend using the new Python SDK", 2026-09-14 확인]
- ⚠️ **Yatai는 슬라이드 제작 시점에 이미 낡았다** — 마지막 릴리스 v1.1.13(2023-10-09)로 1.2 이상을 지원한 적이 없고, 2024-02부터
  "under construction" 공지 상태였으며 2026-06-11 저장소가 보관 처리됐다. [https://github.com/bentoml/Yatai — "⚠️ Yatai for
  BentoML 1.2 is currently under construction.", 2026-09-14 확인]
- ✅ "Adaptive Batching"은 현행 용어다. [https://docs.bentoml.com/en/latest/get-started/adaptive-batching.html — "a dynamic
  request dispatching mechanism that intelligently groups multiple requests", 2026-09-14 확인]
- p41 BentoML 도식은 오탈자("Endpont", "Valiation", "Ayanc", "TensorFow")로 보아 **AI로 생성한 그림**으로 보인다. *(위키의 관찰)*

**Triton Inference Server**

- ❌ **"비즈니스 로직 직접 구현 불가"는 틀렸다** — Python 백엔드로 C++ 없이 모델을 쓸 수 있고, BLS(Business Logic Scripting)는
  반복·조건문·데이터 의존 제어 흐름을 모델 실행과 섞으려고 있는 기능이며, 앙상블 모델로 파이프라인을 구성한다.
  [https://github.com/triton-inference-server/python_backend — "The goal of Python backend is to let you serve models written
  in Python by Triton Inference Server without having to write any C++ code.", 2026-09-14 확인]
- ⚠️ **"C++ 코어로 파이썬 오버헤드 완벽 제거"는 과장이다** — 코어는 C++이지만 Python 백엔드 모델은 스텁 프로세스로 파이썬
  인터프리터를 그대로 돌린다. [https://github.com/triton-inference-server/python_backend — "Python backend uses a *stub*
  process to connect your `model.py` file to the Triton C++ core", 2026-09-14 확인]
- ⚠️ **"가동률 100%에 가깝게"는 문서에 없는 표현이다** — 공식 문서는 "GPU 활용도를 높이는 기능"이라고만 한다.
  [https://github.com/triton-inference-server/server/blob/main/docs/user_guide/faq.md — "several features designed to increase
  GPU utilization", 2026-09-14 확인]
- ⚠️ **"컨테이너 재시작 없이 모델 교체"는 조건부다** — 런타임 로드·언로드는 모델 제어 모드가 EXPLICIT이나 POLL일 때만 되고
  기본값은 NONE이다. 슬라이드는 무조건 되는 것처럼 쓴다. [https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_management.md
  , 2026-09-14 확인]
- ✅ 동적 배칭·시퀀스 배칭, 모델별 스케줄러, 숫자 버전 디렉터리의 모델 저장소, 같은 GPU의 다중 인스턴스 동시 실행은 문서와
  맞다. [https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_execution.md — "allows multiple
  models and/or multiple instances of the same model to execute in parallel on the same system", 2026-09-14 확인]
- 이름: 제품 페이지는 이제 **"NVIDIA Dynamo-Triton, formerly NVIDIA Triton Inference Server"**라고 쓴다. 개명 날짜는 1차 자료로
  확인하지 못했고, GitHub·문서는 여전히 Triton Inference Server라는 이름을 쓰며 프로젝트는 활발하다(v2.72.0, 2026-08-31).
  [https://developer.nvidia.com/dynamo-triton, 2026-09-14 확인]

**FastAPI 절**

- ✅ FastAPI는 Starlette을 직접 상속한다. [https://github.com/fastapi/fastapi/blob/master/fastapi/applications.py —
  `class FastAPI(Starlette):`, 2026-09-14 확인]
- ❌ **"Pydantic은 Cython으로 컴파일" / "Rust와 Cython으로 최적화"는 두 세대를 섞었다** — p22 도식(@tiangolo)은 Pydantic v1
  시절 그림이다. Cython 컴파일은 v1의 선택 사항이었고, v2의 코어(pydantic-core)는 Rust다. 현행 FastAPI는 Pydantic 2.9 이상을
  요구한다. [https://github.com/pydantic/pydantic-core — "Core validation logic for pydantic written in rust", 2026-09-14 확인]
- ⚠️ **uvloop은 FastAPI의 기본 구성 요소가 아니다** — FastAPI 의존성에는 uvicorn도 uvloop도 없고, `uvicorn[standard]`로 설치할
  때 딸려 온다. [https://github.com/encode/uvicorn/blob/master/docs/installation.md — "When `uvloop` is installed, Uvicorn will
  use it by default", 2026-09-14 확인]
- ⚠️ **"네트워크 입출력을 Node.js나 Go 수준으로"** — uvloop README가 주장하는 것은 asyncio 대비 2~4배뿐이다. Go·Node.js 비교는
  1차 자료로 확인하지 못했다. [https://github.com/MagicStack/uvloop — "uvloop makes asyncio 2-4x faster.", 2026-09-14 확인]
- ⚠️ "인터프리터 방식 파이썬의 한계를 하드웨어 레벨에서 해결"은 과장이다 — C 확장은 일부 핫패스를 네이티브 코드로 돌릴 뿐,
  핸들러의 파이썬 코드는 그대로 인터프리터에서 돈다. *(위키의 관찰)*
- ⚠️ **"WSGI는 한 번에 하나의 요청만 처리"는 과장이다** — 동기 제약은 워커 스레드·프로세스 단위이고, WSGI 서버는 멀티스레드·
  멀티프로세스로 동시 요청을 처리한다. ASGI가 푼 실제 한계는 긴 연결(long-poll·WebSocket)이다.
  [https://peps.python.org/pep-3333/ — `wsgi.multithread`: "…may be simultaneously invoked by another thread in the same
  process…"; https://asgi.readthedocs.io/en/latest/introduction.html — "WSGI applications are a single, synchronous callable
  that takes a request and returns a response; this doesn't allow for long-lived connections, like you get with long-poll
  HTTP or WebSocket connections.", 2026-09-14 확인]

**양식**

- Ch4 슬라이드 머리글이 모두 Ch1의 "2. AI 시대를 위한 파이프라인과 데이터엔지니어의 진화방향"이다(템플릿 잔재).
- p43과 p44는 같은 슬라이드(Runners)가 두 번 들어 있다. p22·p28·p41·p49는 텍스트 없이 도식만 있다.
- 비교표(p59)의 등급은 기준·측정 없는 정성 평가다.

## 관련

- 개념: [[모델 서빙]] · [[추론 최적화]] · [[지연 시간과 처리량]] · [[데이터와 모델 버전 관리]] · [[MLOps]]
- 도구: [[FastAPI]] · [[TorchServe]] · [[BentoML]] · [[Triton Inference Server]] · [[ONNX]]
- 서빙 요구사항: [[AI DE 강의 2-05 서빙 파이프라인 설계]]
- 이전 강의: [[AI DE 강의 2-07 Batch vs Online 서빙 아키텍처]]
- 다음 강의: [[AI DE 강의 2-09 서빙의 CPU·GPU 가속]]

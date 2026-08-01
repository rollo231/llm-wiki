---
type: entity
title: FastAPI
area: [programming, data-engineering]
aliases:
  - Starlette
  - Uvicorn
  - uvloop
  - Pydantic
  - ASGI
  - WSGI
tags: [programming, python, web-framework, fastapi, asgi, serving, api]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part2 Ch4 Serving platforms]]"]
---

# FastAPI

Python 웹 프레임워크. ML 서빙 맥락에서는 **가장 추상화가 낮은 선택지** — 서빙 로직을 직접
구현한다. → [[Model serving platforms]]

| 장점 | 제약 |
|---|---|
| 높은 자유도 | **모델 관리·버전 관리·배포 자동화를 직접 구현해야 함** |
| 기존 백엔드 팀과 협업 용이 | **성능 튜닝은 전적으로 개발자 책임** |
| 복잡한 비즈니스 로직 구현에 유리 | |

## 구조 — 왜 빠른가

FastAPI는 **자체 구현이 거의 없고 남의 것을 조립한 층**이다.

```
FastAPI
├─ Starlette (web toolkit / micro-framework)   ← 라우팅·세션·쿠키·웹소켓
│   └─ Uvicorn (implements ASGI spec)
│       └─ uvloop (high-performance asyncio)
│           └─ Cython (compiled Python / C-extensions)
└─ Pydantic (data validation, serialization, documentation)
    └─ Cython
```

| 층 | 역할 |
|---|---|
| **Starlette** | 웹 관련 핵심 기능. **FastAPI는 Starlette을 직접 상속받은 클래스**라 Starlette의 모든 기능을 그대로 쓸 수 있다 |
| **Uvicorn / ASGI** | 파이썬 표준 비동기 인터페이스. **수천 개의 동시 접속을 효율적으로 관리** |
| **uvloop** | 파이썬 기본 이벤트 루프(asyncio)를 C로 작성된 고성능 루프로 대체. **네트워크 I/O 속도를 Node.js·Go 수준으로** |
| **Cython** | 파이썬 코드를 C로 변환·컴파일. **uvloop과 Pydantic은 C 바이너리로 실행** — 인터프리터의 한계를 하드웨어 레벨에서 해결 |
| **Pydantic** | 데이터 검증·직렬화. **내부 로직이 Rust와 Cython으로 최적화** |

> **"빠르다"의 정체는 두 가지다: 비동기(동시 접속 처리량)와 C 컴파일(단위 연산 속도).**
> 프레임워크 설계가 아니라 **아래 층들의 성질**이다.

## WSGI vs ASGI

| WSGI | ASGI |
|---|---|
| **동기적, 한 번에 하나의 요청만 처리** | **비동기적, 동시에 여러 요청 처리** |
| 파이썬 웹 앱–웹 서버 간 표준 인터페이스 | WSGI의 비동기 버전 |
| 성능 제한 가능성 | 웹소켓 등 비동기 프로토콜 지원 |

ML 서빙에서 이게 중요한 이유: **추론 요청은 대부분 I/O 대기**(Feature 조회, 모델 서버 호출)이므로
동기 처리하면 워커가 놀면서 막힌다 → [[Batch and online serving]].

## 서빙에서의 위치

- **BentoML의 API Server 층이 사실상 FastAPI가 하는 일**과 같다(비동기 수신 + Pydantic 검증 +
  비즈니스 로직). BentoML은 여기에 Runner 분리와 패키징을 얹은 것 → [[BentoML]].
- **[[NVIDIA Triton Inference Server\|Triton]]은 정반대**다 — HTTP/gRPC 엔드포인트에서
  **비즈니스 로직을 처리하지 않는다.** validation·routing·auth 중심이 아니라 오직 추론 요청 전달.

> 즉 FastAPI와 Triton은 같은 자리(HTTP 입구)를 정반대 철학으로 채운다: **로직을 다 넣을 것인가,
> 아무것도 넣지 않을 것인가.**

## 열린 질문

- **동기 코드가 섞였을 때의 함정** — FastAPI에서 `def`(동기)와 `async def`의 실행 경로가 다르고,
  블로킹 호출이 이벤트 루프를 막는 문제가 흔한데 강의는 다루지 않는다.
- **워커 구성** — Gunicorn + Uvicorn worker 같은 배포 형태, 워커 수 산정 기준이 없다.
- **이 위키의 첫 `programming` 페이지다.** Python·웹 프레임워크 계열이 자라면 이 페이지가
  분기점이 된다.

## 링크

- 비교: [[Model serving platforms]]
- 대비되는 설계: [[NVIDIA Triton Inference Server]] · [[BentoML]]
- 서빙 아키텍처: [[Batch and online serving]]
- 출처: [[AI DE Course - Part2 Ch4 Serving platforms]]

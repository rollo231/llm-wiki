---
type: entity
title: FastAPI
aliases: []
tags: [서빙, 도구, 웹 프레임워크]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "[[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]"
  - "[[AI DE 강의 2-07 Batch vs Online 서빙 아키텍처]]"
---

# FastAPI

Starlette 위에 Pydantic 검증을 얹은 **Python 비동기 웹 프레임워크.** 모델 서빙 전용 도구가 아니라, 서빙 로직을 직접
구현하는 가장 얇은 선택지로 강의에 나온다.

## 구조 (강의의 설명)

| 층 | 역할 |
|---|---|
| Starlette | ASGI 툴킷 — 라우팅·세션·쿠키·웹소켓. FastAPI는 이를 직접 상속한다 |
| Uvicorn · uvloop | ASGI 서버와 고성능 이벤트 루프 |
| Pydantic | 요청·응답 데이터 검증과 직렬화 |

## 강의의 평가

- **장점** — 높은 자유도, 기존 백엔드 팀과 협업 용이, 복잡한 비즈니스 로직에 유리.
- **제약** — 모델 관리·버전 관리·배포 자동화를 직접 구현, 성능 튜닝은 전적으로 개발자 책임.
- 비교표: 추상화 낮음 · 성능 최적화 직접 · GPU 활용 직접 · 운영 난이도 낮음 · 확장성 직접 설계.

## 현재 상태

- FastAPI는 Starlette을 직접 상속한다. [https://github.com/fastapi/fastapi/blob/master/fastapi/applications.py —
  `class FastAPI(Starlette):`, 2026-09-14 확인]
- 현행 FastAPI는 **Pydantic v2**(코어가 Rust)를 요구한다. 강의의 "Cython으로 컴파일된 Pydantic"은 v1 시절 설명이다.
  [https://github.com/pydantic/pydantic-core — "Core validation logic for pydantic written in rust", 2026-09-14 확인]
- uvloop은 FastAPI 기본 의존성이 아니라 `uvicorn[standard]`로 설치할 때 쓰인다. [https://github.com/encode/uvicorn/blob/master/docs/installation.md
  — "When `uvloop` is installed, Uvicorn will use it by default", 2026-09-14 확인]

세부 검증: [[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]

## 관련

- [[모델 서빙]] · [[BentoML]](강의는 "FastAPI + ML 기능"으로 소개) · [[Triton Inference Server]](앞단 비즈니스 로직 계층으로 겹쳐 쓸 수 있다)

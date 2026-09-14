---
type: entity
title: TorchServe
aliases: [pytorch/serve]
tags: [서빙, 도구, 모델 서버]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "[[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]"
  - "[[AI DE 강의 2-07 Batch vs Online 서빙 아키텍처]]"
---

# TorchServe

PyTorch 프로젝트의 **공식 모델 서빙 서버.** ⚠️ **2025-08-07 저장소가 보관(archived) 처리되어 더 이상 유지보수되지 않는다.**

## 구조 (강의의 설명)

| 구성 | 역할 |
|---|---|
| Frontend (Java) | Inference API(8080) · Management API(8081), 선택적 요청 배칭, 로깅·메트릭, 워커 관리 |
| Backend (Python) | 모델마다 독립 워커 프로세스, 소켓으로 프론트엔드와 통신 |
| Model Handler | initialize → preprocess → inference → postprocess |
| Model Store | `.mar` 아카이브(모델 + 핸들러 + 설정) |

프론트엔드와 백엔드를 나눈 이유: 추론 워커가 죽어도 요청 접수 계층은 산다.

## 강의의 평가

- **장점** — PyTorch와 자연스러운 통합, 기본적인 모델 버전 관리, GPU 서빙.
- **제약** — PyTorch 종속, 커스텀 로직 확장 제한, 커뮤니티 활성도 감소 추세. 프론트엔드가 병목·단일 장애 지점이 되고 GPU 공유·
  MIG 지원이 제한적이라 대규모 서빙에 제한.

## 현재 상태

- 2025-02-28 Limited Maintenance 공지, **2025-08-07 저장소 보관**, 마지막 릴리스 v0.12.0(2024-09-30). 강의(2026-03)는 이를
  "활성도 감소"로만 적는다. [https://github.com/pytorch/serve — "⚠️ Notice: Limited Maintenance — This project is no longer
  actively maintained. While existing releases remain available, there are no planned updates, bug fixes, new features, or
  security patches.", 2026-09-14 확인]
- 포트(8080/8081, 메트릭 8082)와 Java 프론트엔드·Python 백엔드 구조는 공식 문서와 맞다.
  [https://docs.pytorch.org/serve/rest_api.html — "By default, TorchServe listens on port 8080 for the Inference API and 8081
  for the Management API.", 2026-09-14 확인]

세부 검증: [[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]]

## 관련

- [[모델 서빙]] · [[추론 최적화]] · [[데이터와 모델 버전 관리]] · 같은 설계의 다른 서버: [[BentoML]] · [[Triton Inference Server]]

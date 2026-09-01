---
type: source
title: AI DE Course - Ch1-2,3 Latency and Versioning
area: [data-engineering]
aliases: [CH01-2 3 Latency와 Versioning, AI DE 핵심 마인드셋]
tags: [data-engineering, course, fast-campus, latency, versioning]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part1/02. CH01-2, 3. AI DE의 핵심 마인드셋 Latency와 Versioning.pdf"]
---

# AI DE Course - Ch1-2,3 Latency and Versioning

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 CH01-2,3**
"AI DE의 핵심 마인드셋: Latency와 Versioning". 원본(로컬):
`raw/data-engineering/ai-de-course/part1/02. CH01-2, 3. AI DE의 핵심 마인드셋 Latency와 Versioning.pdf` (16p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⚠️ **분량 주의 — 16페이지 중 실질 내용은 4장 정도다.** 나머지는 "Latency", "Versioning",
> "데이터 늪", "핵심 열쇠" 같은 **제목 카드**다. 아래 요점이 이 덱에 담긴 내용의 거의 전부다.

## 요점

- **여는 질문**: "데이터만 열심히, 아주 많이 쌓아 두면 만사형통일까?" → 아니다. 관리되지 않으면
  **데이터 늪(swamp)** 이 된다. (같은 개념이 [[Analytical data storage tiers]]와
  [[AI DE Course - Data governance and catalog]]에서 구조적으로 다시 다뤄진다.)

- **배치 처리 4분할** — 정의(일정 기간 모아서 일괄 처리) / 장점(대량 처리 효율, 리소스 비용 최적화) /
  한계(실시간성 낮아 즉각 피드백 불가) / 사례(야간 정산, 일일 리포트, 비동기 백업).
  → 훨씬 자세한 논의는 [[AI DE Course - Ch4-1,2 Batch vs Streaming]].

- **두 정의**:
  - **Real Time** — 데이터를 얻자마자 즉시 처리.
  - **Latency** — 요청을 보낸 시점부터 응답을 받는 데 걸리는 시간.

- **버전 관리의 확장**: git으로 코드를 관리하듯 **데이터와 모델도 버전 관리 대상**이다.

- **재현성을 위한 3요소** — 이 덱의 가장 실용적인 산출물:
  1. **데이터 스냅샷** — 학습을 시작하는 순간의 데이터를 사진 찍듯 저장
  2. **환경 고정** — Docker 컨테이너, Conda 가상환경
  3. **랜덤 시드** 고정

## 이 덱이 다루지 않는 것

Latency의 트레이드오프 메커니즘(왜 throughput과 반비례하나), 버전 관리 도구(DVC·MLflow 등),
실제 워크플로우 — 전부 없다. 앞의 것은 CH04에서, 뒤의 것은 Part 2 Ch2(MLOps)에서 채워질 예정.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Latency and throughput]], [[Data and model versioning]]
- 이어지는 챕터: [[AI DE Course - Ch1-4 Tech stack and tooling]]

---
type: concept
title: AI data engineering
area: [data-engineering]
aliases: [AI DE, AI를 위한 데이터 엔지니어링, 모델 지원 데이터 엔지니어링]
tags: [data-engineering, machine-learning, unstructured-data]
created: 2026-07-19
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part1/01. CH01-1. [OT] 기존 DE vs AI DE.pdf", "https://sinja.io/blog/data-landscape-guide-for-developers", "[[AI DE Course - Data drift and training-serving skew]]"]
---

# AI data engineering

AI 모델의 **학습과 추론을 지원**하는 데이터 엔지니어링. 정형 데이터·DW·BI 중심의
[[Traditional data engineering]]에서 확장된 형태로, 비정형 데이터와 모델 라이프사이클을 다룬다.
처음 등장: [[AI DE Course - Ch1-1 OT]].

## 핵심 역할

- **모델 학습 지원**: 고품질 학습 데이터 준비·버전 관리, 학습 파이프라인 자동화·실험 관리,
  GPU 리소스 할당·학습 스케줄링 최적화.
- **추론 지원**: 모델 서빙 환경 구축·응답 속도(latency) 최적화, 비용 효율 인프라·오토스케일링,
  성능 모니터링·결과 로깅.
- **비정형 데이터**: 이미지·오디오·비디오·텍스트를 딥러닝이 이해하는 텐서(tensor)로 변환,
  대용량 비정형 데이터의 효율적 저장·검색.

## 왜 지금

- 데이터의 ~80%가 비정형(예: Instagram·YouTube).
- 실시간 수요 증가(예: YouTube·Coupang).

## 한 줄

비정형 데이터까지 다루며 AI 모델이 잘 학습·추론하도록 돕는 **시스템 건축가**.

## 두 가지 핵심 마인드셋

강의가 AI DE의 사고 전환으로 꼽는 둘 — [[Latency and throughput|Latency]]와
[[Data and model versioning|Versioning]]. 앞의 것은 "언제까지 도착해야 가치가 있나",
뒤의 것은 "무엇이 달라졌는지 특정할 수 있나"를 묻는다.

## 역할의 이동 — 배관공에서 지휘자로

**이 코스가 Part 1 전체에서 반복하는 프레이밍이다.** 데이터를 옮기는 일에서
**데이터 품질·거버넌스의 지휘자**로 이동한다. 미래상은 **The Guardian** — 데이터의 수질(quality)과
신선도(freshness)를 보증하는 거버넌스 설계자.

핵심 책임 3축:

- **신선도·품질 관리** — SLO 정의, **Data Contract 수립**, 실시간 품질 검증
  → [[Data SLA and observability]]
- **[[Feature store]] 거버넌스** — 피처 재사용성·표준화, lineage 추적, ground truth 피드백
- **재학습 오케스트레이션** — drift 기반 트리거 설계, 모델 버전·메타데이터 관리, FinOps
  → [[Data drift and training-serving skew]]

문화는 **Data as a Product** — 데이터를 부산물이 아니라 내부 고객(데이터 사이언티스트·모델)이 쓰는
'제품'으로 관리한다. KPI 예시: MTTD(drift 감지) < 10분 · MTTR(복구·재학습) < 4시간 ·
데이터 다운타임 99.9% uptime.

## 범위의 확장 — 데이터의 이동에서 연산의 배치로

Part 2가 DE의 책임 목록에 **새 항목 하나**를 넣는다. [[MLOps]] 관점에서 DE가 책임지는 영역은
데이터 파이프라인 설계 · [[Feature store]] 운영 · 학습/추론 데이터 일관성 · 자동 재학습 —
여기까지는 Part 1과 같은데, 다섯 번째가 새롭다:

> **"GPU 사용 흐름 설계"** · **"데이터 엔지니어는 계산이 발생하는 흐름까지 설계 대상이 된다."**

즉 **Part 1이 데이터의 이동을 다뤘다면 Part 2는 연산의 배치를 다룬다.** 어떤 추론을 배치로 돌리고
어떤 것을 온라인으로 둘지([[Batch and online serving]]), CPU로 충분한지 GPU가 필요한지
([[Inference optimization]]), 어떤 서빙 플랫폼을 쓸지([[Model serving platforms]])가 DE의
결정 범위로 들어온다.

**LLM 시대에는 관리 대상이 한 번 더 옮겨간다** — 피처에서 **컨텍스트**로.
지식 소스 수집·정제, chunking·embedding 파이프라인, Vector DB 운영, retrieval 품질 모니터링,
권한 기반 필터링이 DE의 일이 된다 → [[LLMOps]] · [[Context engineering]].

> 이 서술은 **[[Traditional data engineering]]의 "품질·정합성·거버넌스로 신뢰성 확보"와 겹친다.**
> 강의 기준으로 달라진 것은 관심사가 아니라 **소비자**다 — 신뢰성을 보증할 대상이 경영진 리포트에서
> **AI 모델**로 바뀌었고, 그래서 지표가 uptime에서 분포 안정성·피처 일관성으로 확장된다.

## 다른 축의 분류

[[Data landscape guide for developers]]는 데이터 직군을 **동시에 존재하는 네 유형**으로 본다
(analytical / scientific / engineering / **machine learning**). 이 페이지의 "AI DE"에 대응하는 것은
**machine learning type**인데, 프레이밍이 정면으로 갈린다:

- **이 페이지(강의) — 시간축.** AI DE는 [[Traditional data engineering]]이 **확장·진화한 형태**다.
  같은 직무가 변한다.
- **저 글 — 공존축.** ML type은 "앞의 유형들과 겹쳐 보이지만 **도구셋이 아주 달라서**" 갈라지는
  **별개 직군**이다. 네 직군이 한 회사에 동시에 있다.

충돌하는 것은 결론이 아니라 **축**이다. 어느 쪽이 현업의 실제 모습인지는 아직 근거가 없다 —
둘 다 1차 자료 없는 개괄이다. → [[Data Engineering]] MOC의 열린 질문.

**무게 차이 주의:** 저 글의 저자는 ML에 대한 자기 지식이 제한적이라고 밝히고 본문에서 ML을 다루지
않는다("we won't be covering ML-related topics in this article"). ML 쪽 서술의 근거는 강의 쪽이
더 두껍다.

## 링크

- 대비: [[Traditional data engineering]]
- "비정형을 텐서로"의 실제 방법: [[Unstructured data ingestion]]
- 모델을 지키는 일: [[Data drift and training-serving skew]], [[Feature store]],
  [[Data SLA and observability]]
- 운영 체계: [[MLOps]] · [[LLMOps]]
- 연산 쪽: [[Batch and online serving]] · [[Inference optimization]] · [[Model serving platforms]]
- 마인드셋: [[Latency and throughput]], [[Data and model versioning]]
- 다른 축: [[Data landscape guide for developers]]
- 코스 전체: [[AI Data Engineering (Fast Campus course)]]
- 출처: [[AI DE Course - Ch1-1 OT]], [[AI DE Course - Data drift and training-serving skew]],
  [[AI DE Course - Part2 Ch1 Pipeline evolution and the DE role]]

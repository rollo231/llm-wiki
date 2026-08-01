---
type: concept
title: Feature store
area: [data-engineering]
aliases:
  - Feature Store
  - 피처 스토어
  - Feast
  - Tecton
  - Offline store
  - Online store
tags: [data-engineering, mlops, feature-store, feast, serving]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Data drift and training-serving skew]]", "[[AI DE Course - AI pipeline case studies]]"]
---

# Feature store

피처(모델 입력값) 변환 로직을 **중앙에 한 번 정의**하고, 학습과 서빙이 그 결과를 각자 읽어가게
만드는 저장소. 존재 이유는 하나다 —
**[[Data drift and training-serving skew|training-serving skew]] 제거.**

## 구조 — 하나의 로직, 두 개의 스토어

```
Batch Source (DW·Lake)  ┐
                        ├→ Feature Transformation ─┬→ Offline Store → 학습
Stream Source (Kafka)   ┘   (Unified Logic)        └→ Online Store  → 서빙
                             + Feature Registry & Metadata
```

| | Offline Store | Online Store |
|---|---|---|
| 담는 것 | 대용량 **이력** 데이터 | **실시간 최신값** |
| 저장소 | S3 · BigQuery · Snowflake | Redis · DynamoDB · Cassandra |
| 쓰는 쪽 | 모델 학습 (`get_historical_features()`) | 모델 서빙 (`get_online_features()`) |
| 접근 | Python SDK (Pandas) | REST/gRPC API |

핵심은 **두 스토어가 같은 변환 로직에서 나온다**는 것 — 원칙은 **Write Once, Compute Anywhere**.
[[Data drift and training-serving skew]]의 "33배 뻥튀기" 사례처럼 학습(Python)과 서빙(Java)에서
로직을 이중 구현하다 생기는 미세한 차이를 구조적으로 막는다.

**Feature Registry**가 함께 붙는다 — 어떤 피처가 있고 누가 쓰고 어떻게 정의되는지의 메타데이터.
[[Data catalog and semantic layer]]의 semantic layer가 지표에 대해 하는 일을 피처에 대해 하는 셈이다.

## 부수 효과 — 재사용

skew 제거가 1차 목적이지만, 실무에서 더 눈에 띄는 이득은 **피처 추출 로직의 재사용**이다.
현대 AI 시스템이 데이터 준비 단계에서 전체 작업 시간의 **70% 이상**을 소모하는데
([[AI DE Course - AI pipeline case studies]]), 그 중복을 줄이는 자리가 여기다.

## 구현 도구

- **오픈소스·전용** — Feast · Hopsworks
- **상용** — Tecton
- **클라우드 매니지드** — Vertex AI Feature Store
- **사내 자체 구축** — 아래 케이스 스터디

## 빅테크의 자체 구현

이 개념이 논문이 아니라 **현장에서 필요해서 만들어졌다**는 근거.

| 회사 | 이름 | 특징 |
|---|---|---|
| **Uber** | Palette (Michelangelo의 일부) | 피처 생성·분산 파이프라인 자동 생성. **오프라인/온라인 환경에서 동일한 추출 로직 보장** |
| **Airbnb** | Zipline (Bighead의 일부) | 온라인·오프라인 피처 추출 로직의 완벽한 일치(consistency) |
| **Google** | TFX의 ExampleValidator | 피처 스토어는 아니지만 **학습 데이터와 서빙 로그 간 skew를 감지**하는 방향 |

셋 다 같은 문장을 다르게 쓴 것이다: **"학습과 서빙이 같은 로직을 쓰게 하라."**

## 서빙 방식과의 관계

[[Latency and throughput]]의 밀리초 사례들이 전부 여기를 지난다 — FDS는 "최근 위치" 피처를
Redis에서 200ms 안에, 실시간 추천은 clickstream 피처를 Flink + Redis로 100ms 안에 뽑는다.
**online store는 곧 초저지연 조회 계층이다.**

## 열린 질문

- **만능이 아니다.** offline·online 두 스토어를 두는 순간 **두 스토어 간 일치**가 새로운 보장
  대상이 된다. 강의 Part 1은 이 지점을 "Write Once, Compute Anywhere"로 넘어간다.
  → **Part 2 Ch5가 "Feature Store은 만능이 아니다"를 다룰 예정이므로 그때 채운다.**
  ([[AI Data Engineering (Fast Campus course)]])
- **Feast vs Tecton vs Hopsworks의 선택 기준** — 강의는 이름만 나열한다.

## 링크

- 존재 이유: [[Data drift and training-serving skew]]
- 품질 계약: [[Data SLA and observability]] — 4대 축 중 '피처 일관성'
- 조회 지연: [[Latency and throughput]]
- 메타데이터 층: [[Data catalog and semantic layer]]
- 사례: [[AI DE Course - AI pipeline case studies]]
- 출처: [[AI DE Course - Data drift and training-serving skew]],
  [[AI DE Course - AI pipeline case studies]]

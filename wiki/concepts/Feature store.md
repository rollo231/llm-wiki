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
sources: ["[[AI DE Course - Data drift and training-serving skew]]", "[[AI DE Course - AI pipeline case studies]]", "[[AI DE Course - Part2 Ch5 Feature store in practice]]"]
---

# Feature store

피처(모델 입력값) 변환 로직을 **중앙에 한 번 정의**하고, 학습과 서빙이 그 결과를 각자 읽어가게
만드는 저장소. 목적은 **[[Data drift and training-serving skew|training-serving skew]] 제거**다.

> ⚠️ **다만 "유일한 해법"은 아니다.** Part 2는 이것을
> **공용 변환 로직 → Feature Contract → (필요시) Feature Store** 3단계 중 **가장 무거운 마지막
> 수단**으로 놓는다. 아래 "필요하지 않은 경우" 참고.

## Feature란 무엇인가 — 재정의

> **"Feature는 단순한 컬럼이 아니며, 원천 데이터도 아니다.
> 특정 시점 기준으로 계산된 의미 있는 값이다 — 비즈니스 로직 + 시간 개념 포함."**
>
> **"Feature는 계산 규칙 + 시점 + 스키마의 묶음이다."**

| ❌ | ⭕ |
|---|---|
| `total_order_count` | `total_order_count_last_30_days_as_of_t` |

**이름에 window와 기준 시점이 들어가야 한다**는 주장이고, 이건
[[Data drift and training-serving skew]]의 skew 패턴 1·2(시간 기준·집계 범위)에 대한 **명명 규칙
차원의 방어**다. 이름이 모호하면 학습과 서빙이 다르게 해석한다.

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
| 주요 목적 | **학습 데이터 생성** | **실시간 추론 시 Feature 제공** |
| 핵심 요구 | **과거 시점 Feature 재현**(point-in-time), 대량 조인·집계 최적화 | 낮은 latency, 높은 가용성, Key 기반 조회 |
| 저장소 | S3 · BigQuery · Snowflake · Parquet · Hive | Redis · DynamoDB · Cassandra |
| 쓰는 쪽 | 모델 학습 (`get_historical_features()`) | 모델 서빙 (`get_online_features()`) |
| 접근 | Python SDK (Pandas) | REST/gRPC API |
| 제약 | — | **모든 Feature를 Online에 둘 수는 없다** |

**offline store의 존재 이유는 "과거 시점 재현"이다** — 단순 저장이 아니라, *그때 그 시점에 알 수
있었던 값*을 되살리는 것. 미래 정보가 새어 들어가면 학습이 오염된다
([[ML data pipeline]]의 누수 문제와 같은 뿌리).

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

## 서빙 방식과의 관계 — 두 얼굴

[[Latency and throughput]]의 밀리초 사례들이 전부 여기를 지난다 — FDS는 "최근 위치" 피처를
Redis에서 200ms 안에, 실시간 추천은 clickstream 피처를 Flink + Redis로 100ms 안에 뽑는다.
**online store는 곧 초저지연 조회 계층이다.**

**동시에 online store는 서빙 latency의 최대 항목이기도 하다.** Part 2의 서술:
*"Feature 조회 시간이 전체 latency의 대부분을 차지한다"* — 네트워크 호출, 스토리지 응답 지연,
캐시 미스, 일부 Feature 누락. 같은 사실의 다른 얼굴이다 → [[Batch and online serving]].

## ⭐ 필요하지 않은 경우 — "만능이 아니다"

Part 2 Ch5가 이 절을 명시적으로 둔다. **Feature Store가 파는 것은 결국 두 가지 —
"시점 정합성"과 "온라인 저지연 조회"** 이고, 둘 다 필요 없으면 DW 테이블로 충분하다.

**도입을 생각해볼 조건:**

- Feature가 **실시간/서빙에 반드시 필요한가?**
- Feature 계산 **비용이 높아 중복 실행을 피해야 하는가?**
- **여러 모델 / 팀 간에 Feature를 공유해야 하는가?**

**불필요한 경우:**

- **클라이언트가 Feature 값을 이미 알고 있는 경우**
- 데이터 웨어하우스에 이미 존재하고 사용 가능할 때
- **시간 의존성이 없는 Feature일 때** ← 시점 정합성이 필요 없다
- **Batch serving만 필요한 경우** ← 온라인 조회가 필요 없다
- 계산 비용이 낮은 Feature일 때

> 출처: 강의가 인용한 Medium 글
> `https://medium.com/data-science/do-you-really-need-a-feature-store-e59e3cc666d3`

## 왜 관리가 어려워지나 (도입의 근거)

- **동일한 Feature를 팀마다 다시 구현**
- **학습용 SQL과 서빙용 코드가 분리**
- **Feature 변경 이력 추적 불가** → 어떤 모델이 어떤 Feature를 쓰는지 모름

결과: skew · 재현 불가능한 실험 · **장애 시 원인 파악에 오랜 시간이 소요되거나 불가.**

> **"모델 성능 저하의 주요 원인은 모델 코드가 아니라 Feature다."**
> **"Feature Store는 성능 향상 도구가 아니라 ML 시스템의 안정성을 위한 인프라다."**

## 열린 질문

- ⚠️ **두 스토어 간 정합성 — 여전히 미해결.** offline·online 두 스토어를 두는 순간 **두 스토어 간
  일치**가 새로운 보장 대상이 된다. **Part 2 Ch5를 기대했으나 답하지 않았다** — Ch5의 "만능이
  아니다"는 *"안 써도 되는 경우"*이지 *"썼을 때 남는 문제"*가 아니다. 백필 방법, online store가
  뒤처졌을 때의 감지 방법은 Part 2 전체에서 나오지 않는다.
  → **부분적 우회책은 있다:** [[Data drift and training-serving skew]] 패턴 2의 대응 —
  **"long-term(배치) + short-term(실시간)으로 피처를 아예 분리"**. 정합성을 맞추는 대신 맞출
  필요가 없게 만든다.
- **Feast vs Tecton vs Hopsworks의 선택 기준** — 두 파트 모두 이름만 나열한다. **진전 없음.**
- **Feature Contract의 실제 형태** — Part 2가 "공용 변환 로직 → Feature Contract → Feature Store"
  3단계를 제시하지만, 중간 단계인 Feature Contract를 무엇으로 어떻게 쓰는지는 설명하지 않는다.

## 링크

- 존재 이유: [[Data drift and training-serving skew]]
- 서빙에서의 위치: [[Batch and online serving]]
- 데이터 생산: [[ML data pipeline]]
- 품질 계약: [[Data SLA and observability]] — 4대 축 중 '피처 일관성'
- 조회 지연: [[Latency and throughput]]
- 메타데이터 층: [[Data catalog and semantic layer]]
- LLM 시대의 대응물: [[Context engineering]] (피처 대 컨텍스트)
- 상위: [[MLOps]]
- 사례: [[AI DE Course - AI pipeline case studies]]
- 출처: [[AI DE Course - Data drift and training-serving skew]] ·
  [[AI DE Course - AI pipeline case studies]] ·
  [[AI DE Course - Part2 Ch5 Feature store in practice]]

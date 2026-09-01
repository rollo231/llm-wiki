---
type: source
title: AI DE Course - Part2 Ch5 Feature store in practice
area: [data-engineering]
aliases: [Part2 Ch5, Feature Store 및 운영, Feature Store의 기본 개념과 필요성]
tags: [data-engineering, course, fast-campus, feature-store, mlops, training-serving-skew]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part2/05. Ch5. Feature Store 및 운영.pdf"]
---

# AI DE Course - Part2 Ch5 Feature store in practice

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 2 Ch5** "Feature Store 및 운영"의
소단원 **1** "Feature Store의 기본 개념과 필요성". 강사 **Habi**. 원본(로컬):
`raw/data-engineering/ai-de-course/part2/05. Ch5. Feature Store 및 운영.pdf` (15p, Part 2의 마지막이자 가장 짧은 챕터).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> **⚠️ 이 챕터는 Part 1이 명시적으로 기대하고 있던 자리다.** [[Feature store]]와
> [[Data Engineering]] MOC에 *"Part 2 Ch5가 '만능이 아니다'를 다룰 예정이므로 그때 채운다"*
> 라고 적어뒀다. **결론부터: 절반만 답한다.** 아래 "열린 질문은 닫히지 않았다" 절 참고.

## Feature의 재정의 — 이 챕터의 가장 좋은 부분

> **"Feature는 단순한 컬럼이 아니며, 원천 데이터도 아니다.
> 특정 시점 기준으로 계산된 의미 있는 값이다 — 비즈니스 로직 + 시간 개념 포함."**

강의의 예시 하나가 이걸 다 설명한다:

| ❌ | ⭕ |
|---|---|
| `total_order_count` | `total_order_count_last_30_days_as_of_t` |

> **"Feature는 계산 규칙 + 시점 + 스키마의 묶음이다."**

**이름에 window와 기준 시점이 들어가야 한다**는 주장이고, 이건 앞 소단원의 skew 패턴 1·2(시간 기준,
집계 범위)에 대한 **명명 규칙 차원의 방어**다. 이름이 모호하면 학습과 서빙이 다르게 해석한다.
→ [[AI DE Course - Part2 Ch3 Training-serving skew patterns]]

## 왜 Feature 관리가 어려워지나

- **동일한 Feature를 팀마다 다시 구현**
- **학습용 SQL과 서빙용 코드가 분리**
- **Feature 변경 이력 추적 불가** → 어떤 모델이 어떤 Feature를 쓰는지 모름

**결과:** Training–Serving Skew · 재현 불가능한 실험 · **장애 발생 시 원인 파악에 오랜 시간이
소요되거나 불가**.

> 첫 문장의 진단이 정확하다: **"모델 성능 저하의 주요 원인은 모델 코드가 아니라 Feature."**
> 그리고 **"Feature 정의가 사람·팀·파이프라인마다 달라진다."**
> ⇒ **"Feature Store는 성능 향상 도구가 아니라 ML 시스템의 안정성을 위한 인프라."**

## Feature Store 없이 운영하면

```
        Offline (학습)                    │        Online (서빙)
  Raw Data → Spark/SQL → Feature Files    │   API Server → 직접 재계산
           → CSV / Parquet 저장            │             → Redis / DB에서 ad-hoc 조회
```

**왼쪽은 Spark/SQL로 만들고, 오른쪽은 API 서버에서 다시 만든다.** 이 그림 자체가 skew의 발생
지점이다 — [[Data drift and training-serving skew]]의 "33배 뻥튀기" 사례가 정확히 이 구조에서 났다.

## 등장 배경 — 무엇을 해결하려 했나

1. **Feature 정의의 단일화**
2. **학습/서빙 Feature 일관성 보장**
3. **Feature 재사용성 증가**
4. **Feature 운영 자동화**

> **"Feature를 데이터가 아니라 운영 대상 자산으로 관리하기 위한 시스템."**

## Offline / Online 두 스토어

| | **Offline Feature Store** | **Online Feature Store** |
|---|---|---|
| 주요 목적 | **학습 데이터 생성** | **실시간 추론 시 Feature 제공** |
| 핵심 요구 | **과거 시점 Feature 재현**, 대규모 배치 처리 | 낮은 latency, 높은 가용성 |
| 저장소 | 데이터 레이크 기반 (Parquet, Hive, BigQuery) | Redis, DynamoDB, Cassandra |
| 특징 | **시간 기준 조회 가능**, 대량 조인/집계 최적화 | Key 기반 조회, 최신 상태 유지 |
| 제약 | — | **모든 Feature를 Online에 둘 수는 없다** |

Part 1 [[Feature store]]의 표와 거의 같지만 **두 줄이 새롭다**:

- offline의 **"과거 시점 Feature 재현"** — point-in-time 조회가 offline store의 존재 이유라는 것
- online의 **"모든 Feature를 Online에 둘 수는 없다"** — 용량·비용 제약이 명시된다

### 효과

| 조직 관점 | 시스템 관점 |
|---|---|
| Feature 중복 개발 감소 | 재현 가능한 학습 |
| 팀 간 협업 개선 | 안정적인 서빙 |
| **장애 원인 추적 가능** | **모델 교체 비용 감소** |

## ⭐ "Feature Store는 만능이 아니다"

**Part 1이 기대했던 절.** 강의는 Medium 글
(`medium.com/data-science/do-you-really-need-a-feature-store-e59e3cc666d3`)을 출처로 걸고
두 목록을 준다.

**Feature Store를 생각해볼 조건:**

- Feature가 **실시간/서빙에 반드시 필요한가?**
- Feature를 계산하는 **비용이 높아 중복 실행을 피해야 하는가?**
- **여러 모델 / 팀 간에 Feature를 공유해야 하는가?**

**Feature Store가 불필요한 경우:**

- **클라이언트가 Feature 값을 이미 알고 있는 경우**
- 데이터 웨어하우스에 이미 존재하고 사용 가능할 때
- **시간 의존성이 없는 Feature일 때**
- **Batch serving만 필요한 경우**
- 계산 비용이 낮은 Feature일 때

> **세 번째와 네 번째가 핵심이다.** Feature Store가 파는 것은 결국 **"시점 정합성"**과
> **"온라인 저지연 조회"** 두 가지인데, 시간 의존성이 없으면 전자가 필요 없고 배치 서빙만 하면
> 후자가 필요 없다. 둘 다 아니면 그냥 DW 테이블로 충분하다.
>
> 이것이 Ch3의 3단계 강제 수단 — **공용 변환 로직 → Feature Contract → (필요시) Feature Store** —
> 과 일관된다. **Feature Store는 마지막 수단이다.**

## ⚠️ 열린 질문은 닫히지 않았다

Part 1을 인제스트하며 [[Feature store]]와 [[Data Engineering]] MOC에 남긴 질문은 이것이었다:

> **"Feature Store가 skew를 정말 없애나? offline·online 두 스토어를 두는 순간 두 스토어 간 일치가
> 새로운 보장 대상이 된다."**

**Ch5는 이 질문에 답하지 않는다.** Ch5의 "만능이 아니다"는 **"안 써도 되는 경우"**에 대한 것이지,
**"썼을 때 남는 문제"**에 대한 것이 아니다. 두 스토어의 정합성을 어떻게 보장하는지 —
백필은 어떻게 하는지, online store가 뒤처지면 어떻게 감지하는지 — 는 **Part 2 전체에서 한 번도
나오지 않는다.**

다만 **간접적인 힌트는 있다.** Ch3의 skew 패턴 2(Full vs Partial Window)가 사실상 이 문제의 한
얼굴이다 — *"serving은 최신 구간만 실시간, 나머지는 배치값/캐시로 섞이기 쉽다"*. 그리고 그 대응인
**"long-term(배치) + short-term(실시간) 분리"** 가 두 스토어 정합성 문제에 대한 부분적 답이다:
**정합성을 맞추려 애쓰는 대신 애초에 다른 피처로 쪼갠다.**

→ **열린 질문은 유지하되, 이 힌트를 붙여 갱신한다.**

## 기존 페이지와의 대조

- **보강** — Feature의 재정의(계산 규칙 + 시점 + 스키마), 명명 규칙, offline의 point-in-time 재현,
  "불필요한 경우" 5종이 [[Feature store]]에 추가된다.
- **강조점 확인** — Ch3의 "(필요시) Feature Store"와 Ch5의 "항상 필요한 기본 인프라가 아니다"가
  같은 방향이다. **Part 1의 서술("존재 이유는 하나다 — skew 제거")보다 신중한 온도**이고, 이쪽이
  더 정확해 보인다.
- **미해결** — 두 스토어 간 정합성 문제. 위 참고.

## 인용 자료

- "Do you really need a feature store?" — Medium / Data Science.
  `https://medium.com/data-science/do-you-really-need-a-feature-store-e59e3cc666d3`
  **강의가 URL까지 표기한 드문 인용.** 1차 자료 인제스트 후보.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Feature store]] (상세) · [[Data drift and training-serving skew]] ·
  [[ML data pipeline]] · [[Batch and online serving]]
- 앞: [[AI DE Course - Part2 Ch4 CPU and GPU inference]] — **Part 2의 마지막 챕터**
- 다음 파트: [[AI Data Engineering (Fast Campus course)]] Part 3 (시맨틱 & 컨텍스트 기반 데이터 설계)

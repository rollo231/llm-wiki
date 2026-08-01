---
type: source
title: AI DE Course - Part2 Ch3 Training-serving skew patterns
area: [data-engineering]
aliases: [Part2 Ch3-3, Training-Serving Skew의 이해와 예방, skew 4패턴]
tags: [data-engineering, course, fast-campus, mlops, training-serving-skew, feature-store, event-time]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/Part2_Ch 3.pdf"]
---

# AI DE Course - Part2 Ch3 Training-serving skew patterns

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 2 Ch3** "ML 데이터/서빙
파이프라인"의 소단원 **3** "Training-Serving Skew의 이해와 예방". 강사 **Habi**. 원본(로컬):
`raw/data-engineering/Part2_Ch 3.pdf` **p37–51**. 강의 홈:
[[AI Data Engineering (Fast Campus course)]].

> **⭐ Part 2에서 가장 값진 15페이지다.** Part 1([[AI DE Course - Data drift and training-serving skew]])은
> skew를 **일화 하나**("33배 뻥튀기")로 설명하고 "Feature Store를 쓰라"로 끝냈다. 이 소단원은 같은
> 현상을 **재현 가능한 4가지 패턴**으로 분해하고, 각각의 대응을 준다. 진단 틀이 생긴다.
> → [[Data drift and training-serving skew]]에 반영.

## 정의와 심각성

모델 학습 시 사용한 데이터 분포 또는 **처리 방식**과 실제 서빙 시 입력 데이터가 서로 다른 상태.
**"모델 자체는 정상이어도 입력 데이터의 차이만으로 성능이 급격히 저하될 수 있음."**

발생 상황: **오프라인 평가 지표는 높음 / 프로덕션 성능은 지속적으로 저하.**
영향: 잘못된 의사결정 자동화 · 비즈니스 KPI 악화 · 모델 재학습 → 배포 반복으로 운영 비용 증가.

> 마지막 항목이 새롭다 — skew를 drift로 오진하면 **재학습을 반복하며 비용만 태운다.** 원인이
> 코드 불일치인데 데이터를 새로 먹이니 고쳐질 리가 없다. Part 1이 "둘은 다른 문제"라고 한 이유가
> 여기서 비용으로 구체화된다.

## 왜 반복해서 생기나 — 구조적 필연

원인 목록: Feature 생성 로직 불일치 · 데이터 분포 변화(Data Drift) · 라벨 생성 방식 차이 ·
데이터 누락 또는 지연 · 서빙 환경의 제약.

**학습 파이프라인 vs 서빙 파이프라인**

| 학습 | 서빙 |
|---|---|
| 과거 데이터 기반 | 현재 또는 실시간 데이터 |
| **전체 데이터 접근 가능** | **부분 데이터, 누락 가능성 존재** |
| 처리 지연 허용 | 지연 시간 제약 |
| **정확성 중심 설계** | **안정성과 일관성 중심 설계** |

> **⇒ "학습, 서빙 같은 Feature를 만들기 어려운 구조"**

### 왜 환경 차이가 값 차이로 이어지나

**"Feature는 단순 값이 아니라 데이터 소스 + 집계 기준 + 시간 해석 + 전처리 규칙의 결과다."**
생성 환경이 달라지면 **이 조합을 완전히 동일하게 구현할 수 없다.**

```
환경 차이 → 구현 차이 → Feature 값 차이 → Skew
```

**"Training과 Serving은 다른 코드, 다른 팀, 다른 실행 환경"**
(training: 과거/완전/배치, serving: 현재/부분/지연·누락 가능)
→ Feature 로직이 자연스럽게 분리된다.
**"문제는 이 분리를 설계로 통제하지 않는 것."**

> **이 문장이 Part 1과의 결정적 차이다.** Part 1은 원인을 *"언어와 환경이 달라 이중 구현하는 것"*
> 이라고 했다 — 사람의 실수처럼 들린다. Part 2는 **분리 자체는 필연이고, 통제하지 않은 것이
> 문제**라고 말한다. 없앨 수 없으니 관리하라는 것.

## ⭐ Skew의 4가지 패턴

**"운영에서 가장 자주 깨지는 4가지 규칙."** 이 목록이 이 소단원의 핵심 산출물이다.

### 1. 시간 기준 차이 — Event Time vs Processing Time

"최근 10분" ⇒ 어떤 시간을 기준으로 하는지에 따라 값이 다름.

- **Event time**: 실제 행동이 발생한 시각
- **Processing time**: 시스템이 이벤트를 받은/처리한 시각
- **training은 배치로 event time 기반 집계가 쉬움**
- **serving은 실시간으로 processing time 기반이 되기 쉬움**
- 지연/누락 이벤트 때문에 **포함되는 이벤트 집합이 달라짐**

> Part 1 [[Stream processing semantics]]가 세운 event time / watermark 개념이 **여기서 skew의
> 원인으로 재등장**한다. 스트리밍의 정확성 문제가 곧 ML의 정합성 문제였다는 연결.

### 2. 집계 범위 차이 — Full Window vs Partial Window

"서빙은 종종 기간 전체가 아니라 부분 집계로 동작."

- **Full window**: 정확한 기간 전체 집계 (예: 7일치 완전)
- **Partial window**: 지연/캐시/배치 갱신 주기로 기간 **일부만** 반영
- training은 전체 데이터를 가지고 full window를 만들기 쉽고,
- **serving은 최신 구간만 실시간, 나머지는 배치값/캐시로 섞이기 쉬움**

### 3. 결측 처리 차이 — Null→0 vs Drop vs 조회 실패

**"결측 처리는 단순한 전처리가 아니라 의미 정의다."**

- training: 결측을 0/평균으로 채우거나, 결측 row를 drop
- serving: **실시간 조회 실패/지연도 결측으로 나타남**
- ⚠️ **진짜 "값 없음"과 "조회 실패"를 같은 값(0)으로 처리하면 위험**
- 결측 처리 규칙이 달라지면 입력 분포가 달라짐

> **이게 4패턴 중 가장 실무적으로 흔하고 가장 눈에 안 띈다.** 앞 소단원의 "캐시 미스 시 fallback"이
> 바로 이 함정으로 들어가는 문이다 → [[AI DE Course - Part2 Ch3 Serving pipeline]].

### 4. 스케일링 차이 — Global vs Local Normalization

"정규화/스케일링 파라미터가 다르면 같은 값도 다른 입력이 됨."

- **Global scaling**: 학습 전체 분포에서 계산한 mean/std/min/max
- **Local scaling**: 최근 window/사용자 단위로 즉석에서 다시 계산
- training은 global stats를 쓰기 쉽고, **serving은 local로 바뀌기 쉬움**
- 또는 **training은 라이브러리, serving은 직접 구현**하면서 공식이 달라짐

## 해결의 출발점 — "Skew는 모델 성능 문제가 아니라 Feature 생성 규칙 문제"

> **원칙: "Training은 Serving을 따라가야 한다."** (서빙에서 가능한 규칙을 학습에도 동일 적용)

**이 한 줄이 이 소단원의 결론이고, Part 1에 없던 방향이다.** Part 1의 "Write Once, Compute
Anywhere"는 *어디서 쓰든 같게*라는 대칭적 구호였다. 여기는 **비대칭**을 말한다 — 제약이 큰 쪽(서빙)이
기준이고, 학습이 거기 맞춰 내려와야 한다. 학습에서만 가능한 정교한 집계는 애초에 쓰지 말라는 뜻.

### 4패턴에 대한 현실적 대응

| 패턴 | 대응 |
|---|---|
| **시간 기준** | **Time semantics 고정** — event vs processing 중 하나를 선택하고 동일 적용. 지연 이벤트를 허용할지(워터마크) 정책화 |
| **집계 범위** | **Window를 데이터 가용성에 맞게 설계** — 실시간에서 full window가 불가능하면 **feature를 재정의**. long-term(배치) + short-term(실시간) 분리 |
| **결측 처리** | **Missing을 의미로 분리** — "값 없음"과 "조회 실패"를 같은 0으로 처리하지 않음. `is_missing` 플래그 / fallback 정책 |
| **스케일링** | **Scaling 파라미터를 아티팩트로 고정** — global stats(mean/std/min/max)를 **모델과 함께 버전으로 배포**. training/serving 동일 로직 사용 |

> **"실시간에서 full window가 불가능하면 feature를 재정의한다"** — 서빙이 못 하는 피처는
> **만들지 않는다**는 뜻이다. 위의 비대칭 원칙이 실행으로 옮겨진 형태.
>
> **스케일링 파라미터를 모델 아티팩트에 동봉**하는 것도 구체적이다 → [[Data and model versioning]]의
> "재현성 3요소"에 실질을 더한다.

### 강제 수단 3단계

> **"이 규칙을 시스템으로 강제하는 대표 수단: 공용 변환 로직 / Feature Contract / (필요시) Feature Store"**

⚠️ **주목: [[Feature store]]가 "(필요시)"로 마지막에 온다.** Part 1은 Feature Store를 skew의
**해법 그 자체**로 서술했다("존재 이유는 하나다 — skew 제거"). Part 2는 그것을 **세 수단 중 가장
무거운 마지막 것**으로 놓는다. 모순은 아니지만 **강조점이 뚜렷이 다르고, Ch5가 이 온도를 확인해준다**
("Feature Store는 항상 필요한 기본 인프라가 아니다") →
[[AI DE Course - Part2 Ch5 Feature store in practice]].

## 기존 페이지와의 대조

- **대폭 보강** — [[Data drift and training-serving skew]]가 사례 1건으로 설명하던 skew에
  **4패턴 진단 틀 + 패턴별 대응 + "Training이 Serving을 따라간다" 원칙**이 추가된다.
- **강조점 이동(주의)** — Feature Store의 위상이 *해법*에서 *최후 수단*으로 내려온다. 위 참고.
- **연결** — [[Stream processing semantics]](event time·워터마크)가 ML 정합성 문제의 원인으로
  재등장. Part 1에서 따로 놀던 두 페이지가 이어진다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Data drift and training-serving skew]] (상세) · [[Feature store]] ·
  [[Stream processing semantics]] · [[ML data pipeline]] · [[Data and model versioning]]
- 앞: [[AI DE Course - Part2 Ch3 Serving pipeline]]
- 다음 챕터: [[AI DE Course - Part2 Ch4 Serving architecture]]

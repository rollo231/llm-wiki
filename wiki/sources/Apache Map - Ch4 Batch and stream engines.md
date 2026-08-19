---
type: source
title: Apache Map - Ch4 Batch and stream engines
area: [data-engineering]
aliases: [Apache 지도 Ch4, Apache 지도 배치와 스트림을 돌리는 엔진, Apache Map Ch4]
tags: [data-engineering, apache, spark, flink, beam, streaming, book]
created: 2026-08-19
updated: 2026-08-19
sources: [raw/data-engineering/apache/apache-book-full-spread.pdf]
---

# Apache Map - Ch4 Batch and stream engines

『Apache로 읽는 데이터 기술의 지도』(이현수, 2026) **Ch4. 배치와 스트림을 돌리는 엔진** — 개념 6개,
PDF pp.27–33. 트래커: [[Apache data technology map (book)]].

공백 2/6이었고 [[Apache Spark]]·[[Apache Flink]]·[[Batch and stream processing]]·
[[Stream processing semantics]]가 이미 이 영역을 덮고 있었다. **그런데 이 장에서 이 책 전체를 통틀어
가장 실용적인 문장 하나가 나온다.**

## ⭐⭐⭐ 논지 (개념 6) — 엔진보다 먼저 시간을 자른다

> **"엔진 이름을 고르기 전에, 먼저 '시간을 어떻게 자를지'를 정하는 편이 낫다. 이 선택이 Spark·Flink
> 논쟁보다 먼저 와야 한다. 시간 모델을 정해야 엔진 비교가 의미를 갖는다."**

| | 시간 모델 | 성질 | 쓰는 곳 |
|---|---|---|---|
| 1️⃣ | **배치** | 단순하고 **비용 예측이 쉽지만 결과가 늦다** | 늦게 조회되어도 되는 대용량 정리·리포트 |
| 2️⃣ | **마이크로배치** | 덩어리를 짧게 쪼갠 준실시간 | 수분~수십 초 지연 허용 |
| 3️⃣ | **이벤트 스트림** | 이벤트마다 상태 갱신, **이벤트 타임** 기준 윈도우 | 초 단위 갱신 + 상태·늦은 데이터 |

⚠️ **"처리 시각(프로세싱 타임)만 보면 결과가 어긋난다"** — 늦은 데이터를 고려해야 하면 이벤트 타임까지
설계한다. → [[Stream processing semantics]]

### ⭐⭐⭐ 그리고 논쟁을 끝내는 한 숫자

> **"지연 허용 범위를 숫자로 정해 두면 기술 논쟁이 훨씬 짧아진다.
> SLA를 '평균'이 아니라 '최대 허용 지연'으로 정해 두면 배치와 스트림의 경계가 명확해진다."**

⭐ **이 책 전체에서 가장 값이 나가는 문장일 수 있다.** [[Wiki gap analysis - DE readiness]]가 이 위키의
반복 결함을 ***"'재야 한다'는 있고 '이렇게 잰다'가 없다"*** 로 진단했는데, 이건 **"이렇게 잰다"** 다.

[[Latency and throughput]]·[[Data SLA and observability]]는 이미 *평균이 아니라 p95/p99* 를 말한다.
차이는 **그 숫자를 무엇에 쓰는가**다 — 거기서는 *약속(SLO)* 이고, 여기서는 **엔진 선택의 경계선**이다.
허용 지연이 24시간이면 1️⃣, 30초면 2️⃣, 1초면 3️⃣이고 **그 뒤에야 Spark냐 Flink냐가 의미를 갖는다.**
[[Batch and stream processing]]에 절을 신설했다.

⭐ *"'진짜 실시간'이 필요한 구간만 스트림으로 두고 나머지는 배치로."*
[[Apache Map - Ch1 How to read this book]]이 두 스택을 **함께** 쓰라고 한 이유다.

## Spark · Flink · Spark vs Flink — 위키가 이미 아는 것

개념 1·2·3은 [[Apache Spark]](In-Memory + DAG)·[[Apache Flink]](상태, RocksDB backend, 체크포인트)·
[[Stream processing semantics]](윈도우·워터마크·exactly-once)가 이미 **더 자세히** 갖고 있다.
확인된 것만 적는다.

- **Spark** — *"하나의 엔진에서 배치·SQL·스트리밍·ML을 동일한 프로그래밍 모델 안에서"* + Parquet·Iceberg
  연동. ⭐ *"분석용 대용량 처리의 기본 엔진을 고른다면 Spark를 가장 먼저 보는 기본값으로."*
- **Flink** — *"핵심은 상태(state)"*. **"'이 사용자의 최근 5분 주문 합계', '이미 처리한 키인가'처럼
  시간을 가로지르는 정보를 엔진이 관리한다"** 는 설명은 [[Stream processing semantics]]의 상태 절과
  일치한다.
- **Spark vs Flink** — 🔹 Spark: 대용량 배치 ETL·SQL 중심 레이크하우스 / 🔸 Flink: 저지연 스트림·복잡한
  상태·CDC 기반. ⭐ *"한쪽이 다른 쪽을 완전히 대체하지 않고 실시간 경로와 배치 경로를 나누어 맡는다.
  **같은 허브를 쓰면서 소비 방식을 나누는 것이 핵심.**"* → [[Lambda and Kappa architecture]]
  ⚠️ 그리고 정직하게 인정한다 — *"Spark Structured Streaming과 Flink 배치 API가 발전하면서 두 엔진의
  경계는 흐려졌다."*
- ⭐ 실무 진입 순서까지 준다: *"Spark에 익숙한 팀이라면 Spark를 주 엔진으로 두고 **실시간 처리가 필요한
  일부 경로에만 Flink를 붙일 수 있다.**"*

## 위키에 새로 들어온 둘 — Beam과 StreamPark

### Apache Beam (🔹 Tier 1)

**파이프라인을 표현하는 공통 프로그래밍 모델.** 한 번 작성한 로직을 Spark·Flink·Dataflow 같은 여러
**runner**에서 돌린다. 배치와 스트림을 하나의 모델로 표현하고 **윈도우·워터마크·트리거를 표준화**한다.
푸는 문제: **"엔진이 바뀔 때마다 코드를 다시 짜는 비용."**

⚠️⚠️ **그리고 그 대가를 정직하게 적는다** — *"추상화 단계가 하나 더 생기는 셈이라, **디버깅과 성능 튜닝
경로도 엔진 직접 사용보다 길어질 수 있다.** 실행 환경을 바꿀 계획이 없으면 엔진 API를 직접 쓰는 편이 더
단순하다."*

⭐ 판단 문항 하나 — **"엔진을 바꿔도 같은 코드를 쓸 수 있는가"가 그 추상화 비용을 감수할 만큼 중요한가.**
이건 [[LangChain]]에 대해 이 위키가 이미 적은 것(*추상을 얻고 제어를 내준다*)과 정확히 같은 형태의
트레이드오프다.

### Apache StreamPark (🔸 Tier 2)

*"Flink나 Spark로 스트림 앱을 **만드는 것**과, 그것을 여러 팀이 반복해서 **배포·감시·롤백하는 것**은
다른 문제다."* 엔진을 대체하지 않고 **앱의 생명주기를 표준화**한다.

⭐ 도입 신호가 관찰 가능하다 — **"'누가 어떤 잡을, 어떤 설정으로, 어디에 올렸는지'를 추적하기
어려워질 때"**, 그리고 **배포 실수가 반복될 때.**
⭐ **성능 도구가 아니라 일관성 도구다** — *"계산 성능 튜닝보다 **배포 실수와 설정 불일치**를 줄이는
도구로 이해하면 도입 판단이 쉬워진다."* → [[Data and model versioning]] · [[Data orchestration]]

⚠️ *"작은 팀에서 잡 두세 개만 운영한다면 엔진 기본 도구만으로도 충분할 수 있다."*

## 👍 강점 · ⚠️ 약점

**강점**: 논지(개념 6)가 이 책에서 가장 실행 가능하다. 출처 없는 수치 **0건**(9장 연속).
Beam의 추상화 비용을 감추지 않는다.

**약점**: ⚠️ Spark·Flink 자체는 위키가 이미 더 깊다 — Spark의 Catalyst·Tungsten·shuffle,
Flink의 체크포인트 배리어·state backend가 없다. 이 장의 값은 **엔진 설명이 아니라 엔진 앞의 결정**이다.

## 위키에 들어온 것

**새 페이지: source 1장뿐.** 기존 1곳 대폭 갱신:
[[Batch and stream processing]] — **§엔진보다 먼저 정할 것: 시간을 어떻게 자를지**(3모델 +
**최대 허용 지연** 측정 규칙) · **§엔진 위·옆의 두 계층**(Beam · StreamPark) · 별칭 추가.

**승격 판단**: **Beam ⏸** — Tier 1이지만 지식의 단위가 *"이식성 vs 추상화 비용"* 이라는 트레이드오프
하나라, [[Batch and stream processing]]에 별칭으로 흡수했다(Doris·NiFi와 같은 판단).
**StreamPark ⏸** — 같은 이유.

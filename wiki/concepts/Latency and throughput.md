---
type: concept
title: Latency and throughput
area: [data-engineering]
aliases:
  - Latency
  - Throughput
  - 지연 시간
  - 처리량
  - 레이턴시
  - Lambda architecture
  - Kappa architecture
tags: [data-engineering, latency, throughput, performance, architecture, batch, streaming]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Ch4-1,2 Batch vs Streaming]]", "[[AI DE Course - Ch1-2,3 Latency and Versioning]]"]
---

# Latency and throughput

배치와 스트리밍을 가르는 것은 "시간 차이"가 아니라 **이 두 지표의 트레이드오프**다.
[[Batch and stream processing]]이 *무엇을 고르나*라면, 이 페이지는 *왜 둘을 동시에 가질 수 없나*다.

- **Latency** — 요청을 보낸 시점부터 응답을 받을 때까지의 총 소요 시간 (RTT, turnaround time).
  비유: 맛집 대기 시간.
- **Throughput** — 단위 시간당 처리할 수 있는 작업의 총량 (TPS·QPS·RPM·MB/s).
  비유: 주방의 1시간당 소화력.

**평균(P50)보다 꼬리(P99) 관리가 더 중요할 수 있다** — 느린 1%가 VIP일 수 있고, SLA는 보통 꼬리에
걸린다 → [[Data SLA and observability]]

## 시소의 법칙 — 왜 반비례하나

| | Latency 최적화 | Throughput 최적화 |
|---|---|---|
| 자원 | **독점** — 요청 하나에 집중 | **공유** — 모아서 한꺼번에 |
| 대가 | 잦은 문맥 전환·준비 비용 | 데이터가 모일 때까지의 대기 시간 |
| 비유 | 쉐프 1명이 손님 1명 전담 (오마카세) | 대형 솥에 50인분 (급식소) |

원인은 추상적 선택이 아니라 **물리적 오버헤드**다. 강의는 세 층위에서 설명한다.

### 1. CPU — 문맥 전환과 캐시 지역성

작업을 바꿀 때마다 레지스터 상태를 저장·복원하는 준비 시간이 든다. 이건 연산이 아니라 **순수
오버헤드**다. 게다가 연속 처리하면 L1/L2 캐시 적중률이 높은데, 잦은 전환은 캐시를 차갑게 만든다
(캐시 미스 한 번에 CPU 사이클 수백 개).

```
Throughput = (Actual Work Time) / (Total Time)
```

강의 제시 수치: 배치 효율 95% / 캐시 적중 92%, 스트리밍 효율 60% / 캐시 적중 58%.

### 2. 네트워크 — 패킷 헤더 비율

모든 패킷에 헤더가 붙는다. 작은 데이터를 자주 보내면 **실제 데이터보다 주소표가 더 많아진다**
(스트리밍 헤더 오버헤드 ~40% vs 배치 <1%).

### 3. 디스크 — 순차 쓰기 vs 랜덤 쓰기

디스크 헤드가 움직이는 **seek time**이 가장 비싼 비용 중 하나다. 배치는 순차 쓰기로 이를 최소화한다.

> ⚠️ **이 셋째 항목은 강의 내부에서 모순이 있다.** CH04-1,2는 "스트리밍 = 랜덤 I/O"로 일반화하는데,
> 바로 다음 챕터의 [[Apache Kafka]]는 **순차 쓰기(sequential I/O)** 로 디스크를 써서 "느린 하드
> 디스크에서도 메모리급 속도"를 낸다고 설명한다. 즉 스트리밍이 곧 랜덤 I/O인 것이 아니라,
> **건별로 목적지에 직접 쓰면** 랜덤 I/O가 되는 것이다. append-only 로그로 받으면 스트리밍도
> 순차 쓰기다. → [[AI DE Course - Ch4-1,2 Batch vs Streaming]]

## 중간지대 — 마이크로 배치

아주 짧은 시간(0.5초~수 초) 모아서 작은 덩어리로 처리한다. 결과: **1~5초 지연 + 배치에 준하는
효율**. Spark Structured Streaming의 `Trigger.ProcessingTime("1 second")`가 그것이다.
준실시간성 · 시스템 안정성 · exactly-once를 함께 얻는다.

> **완벽한 실시간이 필요 없다면 마이크로 배치가 비용 대비 최고 효율이다.**

## 둘 다 필요할 때 — Lambda / Kappa

**Lambda Architecture** — 정확성과 신속성을 둘 다 요구할 때의 하이브리드.

- **Batch Layer** — immutable master dataset을 관리하며 전체를 주기적으로 재처리해 완벽한 정확성 확보.
- **Speed Layer** — 배치가 끝나기 전까지의 최근 데이터(gap)를 처리. 정확도는 다소 낮다.
- **Serving Layer** — batch view + real-time view를 병합해 제공.
- ⚠️ **단점: 배치·스트리밍 두 개의 코드베이스를 유지보수해야 한다.**
- 대안이 **Kappa Architecture** (stream only).

## 선택 기준

강의가 제시하는 3축 결정 매트릭스:

| 질문 | Streaming | Batch |
|---|---|---|
| 데이터 가치 소멸 시간? | 초 단위 | 일 단위 |
| 정확성 요구? | 허용 오차 있음 | **1원도 오차 불가** (금융 정산·감사) |
| 비용·운영 역량? | 고비용·전문 인력·24x7 | 저비용·일반 인력 |

> **Golden Rule:** 실시간성이 필수인 구간(경보·추천)에만 스트리밍을 도입하고, 나머지는 안정적인
> 배치를 기본으로. **Start Simple, Scale Later.**

## 밀리초가 돈이 되는 사례

강의가 드는 세 가지 — 세 경우 모두 "배치로 하면 이미 늦다"가 논지다.

| 사례 | 허용 지연 | 배치로 하면 |
|---|---|---|
| 자율주행 | < 100ms (E2E < 50ms 목표) | 이미 사고 발생 |
| 이상 거래 탐지 (FDS) | < 500ms (결제 대기 한계) | 카드 한도 소진 후 발견 |
| 실시간 추천 | < 200ms (clickstream) | 지난달 관심사를 추천 (낮은 CVR) |

FDS·추천 모두 파이프라인에 **Redis + [[Feature store]]** 가 들어간다 — 최근 행동 패턴을 밀리초에
조회하는 자리다.

## 모델 서빙에서의 latency 분해

같은 개념이 추론 서비스로 오면 **항목별 분해**가 된다.

```
Total Latency = 네트워크 + 직렬화 + 전/후처리 + 모델 추론 + 스케줄링
```

> **"모델 추론이 병목이 아닌 경우가 매우 많다"** — 작은 모델 / 낮은 QPS / I/O 중심 서비스.
> GPU는 다섯 항목 중 **하나**만 줄이므로, 나머지 넷이 지배적이면 비용만 몇 배가 되고 총 지연은
> 거의 그대로다. → [[Inference optimization]]

실제로 [[Batch and online serving]]에서는 **Feature 조회(네트워크 + 스토리지 응답)가 전체
latency의 대부분**을 차지한다고 본다. 위 "밀리초가 돈이 되는 사례"의 Redis 조회가 정확히 그 항목이다.

**서빙에서는 예산이 협상 대상이다** — Latency Budget은 ML 팀 혼자 정하는 것이 아니라 백엔드팀과
합의한다. 그리고 목표는 평균이 아니라 **p95 / p99 SLO**로 잡는다(이 페이지 앞의 "꼬리 관리").

## 링크

- 선택의 축: [[Batch and stream processing]] — 배치/스트림/마이크로배치와 도구 지도
- 스트리밍의 정확성 메커니즘: [[Stream processing semantics]] — 윈도우·워터마크·exactly-once
- 실어 보내는 층: [[Apache Kafka]]
- 서빙에서의 지연: [[Batch and online serving]] · [[Inference optimization]] ·
  [[Model serving platforms]]
- 지표로 약속하기: [[Data SLA and observability]] — p95·p99를 SLA에 박는 방식
- 출처: [[AI DE Course - Ch4-1,2 Batch vs Streaming]], [[AI DE Course - Ch1-2,3 Latency and Versioning]],
  [[AI DE Course - Part2 Ch4 CPU and GPU inference]]

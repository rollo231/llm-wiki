---
type: concept
title: Data orchestration
area: [data-engineering]
aliases:
  - 데이터 오케스트레이션
  - 오케스트레이션
  - orchestration
  - workflow scheduler
  - 워크플로 스케줄러
  - Apache DolphinScheduler
  - DolphinScheduler
tags: [data-engineering, orchestration, scheduling, airflow, dag, batch]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch7 Ingestion and orchestration]]"]
---

# Data orchestration

**"무엇을 하나"와 "언제·어떤 순서로·실패하면 어떻게 하나"는 다른 문제다.** 후자를 맡는 층.

> "오케스트레이터는 NiFi나 Spark를 대신하지 않는다. **데이터를 옮기고 가공하는 일은 다른 전용 도구가
> 맡고**, Airflow나 DolphinScheduler는 그 작업들의 **순서·일정·재시도를 지휘한다.**"

## 이 층이 앉는 자리 — 역할 3분할

파이프라인 입구의 도구 이름을 한꺼번에 외우면 구분이 흐려진다. **역할 세 가지로만 나눈다.**

| | 역할 | 하는 일 | 대표 |
|---|---|---|---|
| 1️⃣ | **수집** | 파일·API처럼 잡다한 소스에서 받아 보낸다 | NiFi → [[Data integration tools]] |
| 2️⃣ | **CDC** | 운영 DB에서 **바뀐 내용만** 이벤트로 뽑는다 | Flink CDC → [[Change data capture]] |
| 3️⃣ | **오케스트레이션** | 배치 작업의 순서·일정·회복 | [[Apache Airflow]] · DolphinScheduler |

SeaTunnel·Hop·Camel은 그 사이에서 데이터를 옮기거나 변환하는 **실행 도구**다.
⭐ **겉보기엔 비슷한 파이프라인 도구처럼 보여도 맡는 일이 다르다.**

한 그림으로 그리면: 파일·API는 수집 계층으로 들어오고, DB 변경은 CDC를 거쳐 Kafka나 레이크 테이블에
반영된다. 매일·매시간 돌아가는 변환·품질 검사·집계는 오케스트레이터가 Spark·SQL·Hop 작업을 순서대로
호출한다. **실시간 경로는 스케줄 없이 스트림이 계속 돌고, 배치 경로만 DAG가 배치 단위로 맞춘다.**
→ [[Batch and stream processing]]의 *오케스트레이터는 배치 전용*

## ⭐⭐ 고르는 축은 도구가 아니라 팀의 운영 방식이다

Airflow vs DolphinScheduler는 **성능 비교가 아니다.**

> "'어느 쪽이 더 강력한가'보다 **'우리 팀이 파이프라인을 어떻게 변경·배포하는가'** 가 더 맞는 기준이다."

| | 운영 철학 | 맞는 팀 |
|---|---|---|
| 🔹 **[[Apache Airflow]]** | Python으로 DAG를 **코드화**해 리뷰·테스트·패키징 | 엔지니어가 **Git으로 파이프라인을 관리**하고 로컬 테스트·CI가 중요 |
| 🔸 **DolphinScheduler** | **시각적 설계** + 분산 스케줄 운영 콘솔. 마스터·워커 구조, 쉘·SQL·Spark·Flink 태스크를 UI에서 연결 | 운영자·분석 엔지니어가 **UI에서 조립**, 대량 스케줄 실행 화면이 중심 |

생태계·클라우드 관리형 옵션·커뮤니티 자료량은 **대체로 Airflow 쪽이 훨씬 넓다.**
DolphinScheduler는 중국·아시아권 채택 사례가 많다.

### 도구 이름보다 먼저 정할 네 가지

> "어느 쪽을 고르든, **먼저 정해야 할 것은 도구 이름이 아니라 운영 방식이다.**"

1. **누가 파이프라인을 만들고 배포하는가**
2. **실패하면 누구에게 알리는가**
3. **권한은 어디에 두는가**
4. **비밀정보(secret)는 어디에 두는가**

⭐ 이 네 문항이 곧 도구 선택이다 — 1번이 "엔지니어 + Git"이면 Airflow, "운영자 + UI"면
DolphinScheduler로 사실상 정해진다. 2~4번은 두 도구 모두 답을 주지 않으므로 **직접 설계해야 하는
부분**이고, 그래서 이 질문들을 먼저 하는 것이 순서다.

⚠️ **이미 하나를 표준으로 쓰고 있다면 특별한 이유 없이 둘을 병행하지 않는다.** 이중 오케스트레이션은
"어느 DAG가 이 테이블을 만들었나"를 추적 불가능하게 만든다 → [[Data catalog and semantic layer]]의 리니지

## 오케스트레이션이 SLA를 지키는 방식과 그 한계

재시도·알림·센서·백필은 [[Data SLA and observability]]를 지키는 장치다. 하지만 ⚠️ **DAG 성공은 데이터
건강을 증명하지 않는다** — 그 페이지의 *침묵의 실패* 가 정확히 여기서 일어난다. 태스크가 0건을 적재하고
성공으로 끝나면 오케스트레이터는 초록불을 켠다.

그래서 품질 검사가 **DAG 안의 태스크로** 들어가야 한다 — 오케스트레이터의 성공 조건에 데이터 조건을
넣는 것이 [[Data SLA and observability]]의 서킷 브레이커를 구현하는 방법이다.

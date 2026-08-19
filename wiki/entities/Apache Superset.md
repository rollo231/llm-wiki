---
type: entity
title: Apache Superset
area: [data-engineering]
aliases: [Superset, BI, 셀프서비스 분석, self-service analytics, SQL Lab, Apache Zeppelin, Zeppelin, 대시보드]
tags: [data-engineering, apache, bi, visualization, dashboard, superset]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch10 Governance and BI]]"]
---

# Apache Superset

**SQL을 기반으로 차트와 대시보드를 만들고 공유하는 BI·셀프서비스 분석 플랫폼.**
[[Apache Map - Ch1 How to read this book]]의 레이크하우스 기본 스택에서 **"화면"** 칸이다.

풀려는 문제: **데이터가 레이크와 웨어하우스에 있어도 현업이 SQL 클라이언트로만 접근하면 병목이 생긴다.**

- 데이터셋·차트·대시보드를 조합하고, 필터와 **SQL Lab**으로 탐색한다.
- **셀프서비스** — 권한이 있는 범위에서 분석가가 직접 화면을 만든다. *"매번 엔지니어에게 리포트를
  요청하는 부담을 줄인다."*
- **다중 소스** — Druid·Pinot·웨어하우스·PostgreSQL 등 서로 다른 소스를 **하나의 BI 화면**에서 연결한다.
  → [[Consumption layer]]

⚠️ **저장이나 계산을 대신하지 않는다.** 이미 준비된 데이터를 사람이 읽기 쉽게 보여 주는 역할이고,
[[SQL execution layer]] 3단계의 **3️⃣ 접속·소비** 칸에 앉는다.

## ⚠️ BI가 거버넌스를 대신하지 않는다

> **"잘못된 집계 정의, 중복 대시보드, 과도한 권한은 BI 안에서도 반복된다.
> 카탈로그·권한·품질이 받쳐 줄 때 셀프서비스가 안전해진다."**

⭐ 이것이 [[Data catalog and semantic layer]]의 **semantic layer**가 필요한 이유다 — 지표 정의가
BI 대시보드마다 흩어지면 셀프서비스는 *"같은 이름 다른 숫자"* 를 대량 생산한다. 그 페이지의
*카탈로그의 실패 모드는 '없음'이 아니라 '틀림'* 이 BI 층에서 재현되는 형태이기도 하다.

## Superset vs Zeppelin — 대시보드와 노트북

**Apache Zeppelin**은 노트북 기반으로 SQL·코드·시각화를 한 문서에 이어 가는 **탐색적 분석 환경**이다.
인터프리터로 엔진을 바꿔 가며 Spark 등과 대화형으로 결합한다.

| | 역할 |
|---|---|
| **Superset** | **공유·운영 대시보드.** 고정된 리포트의 기준 |
| **Zeppelin** | **실험용 노트북.** 대시보드로 고정하기 전, 가설 검증과 중간 과정 기록 |

⚠️ 최근에는 Zeppelin이 Jupyter·관리형 노트북과 역할을 나누는 경우가 많다.
⚠️ **"노트북만으로 전사 소비를 맡기면 버전 관리와 권한이 흐트러지기 쉽다."**

⭐ 그래서 흔한 배치는 **운영 리포트의 기준은 BI에, 깊은 탐색은 노트북으로 분리**하는 것이다.
[[Consumption layer]]의 *역할을 억지로 합치지 않는다* 가 사람 쪽 끝단에서도 같은 형태로 나타난다.

## 위키 안에서의 위치

- [[Consumption layer]] — 사람에게 도달하는 마지막 칸.
- [[SQL execution layer]] — 3단계의 3️⃣. 앞단은 Kyuubi 같은 게이트웨이·JDBC.
- [[Data catalog and semantic layer]] — BI를 안전하게 만드는 받침.
- [[Dimensional modeling]] — 대시보드가 조회하는 fact·dimension의 모양.

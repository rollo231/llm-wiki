---
type: entity
title: Apache Calcite
area: [data-engineering]
aliases: [Calcite, SQL parser, SQL optimizer, 쿼리 옵티마이저, cost-based optimization, CBO]
tags: [data-engineering, apache, sql, query-engine, optimizer]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch8 SQL on the lake]]"]
---

# Apache Calcite

**SQL 문장을 파싱·검증하고 더 효율적인 실행 계획으로 바꾸는 프레임워크.** 웨어하우스도 엔진도
아니고, **여러 쿼리 엔진 안에 들어가는 라이브러리**다.

> **"여러 SQL 엔진이 서로 비슷한 문법을 쓰는 이유."**

- 하는 일 세 가지: SQL **파싱**, 타입·오류 **검증**, 비용 기반·규칙 기반 **최적화**.
- 채택: Hive · Drill · Flink SQL 계열 등 많은 도구가 Calcite의 코드나 아이디어를 활용해 왔다.
- **설치 목록에 오르지 않는다.** 설치되는 것은 완제품 엔진이고, Calcite는 그 아래 또는 옆에 있다.

## 왜 알아야 하나

[[SQL execution layer]]의 3단계 중 **2️⃣ SQL 실행 안에 숨어 있는 부품**이다. Doris·Impala와
나란히 놓고 "어떤 걸 설치할까"로 비교하면 범주 오류다.

⭐ 대신 이걸 알면 **엔진 비교가 덜 막연해진다** — `문장 → 계획 → 실행`의 중간 단계가 보이기 때문이다.
엔진마다 다른 것은 대개 3단계(실행)이고, 1~2단계는 상당 부분 공유한다. "엔진 A가 B보다 빠르다"는
말이 실제로는 스캔·조인 구현의 차이를 가리킨다는 것도 여기서 나온다.

데이터 엔지니어가 Calcite를 직접 설정하는 경우는 많지 않다. **읽는 목적은 구조 이해 하나다.**

## 위키 안에서의 위치

- [[SQL execution layer]] — 이 부품이 어디에 끼는지.
- [[Table formats]] — Hive가 Calcite를 쓴다. Hive의 SQL 계층과 메타스토어는 별개의 것이다.
- [[Apache Flink]] — Flink SQL 계열이 Calcite 기반이다. Flink를 SQL로 쓰는 경로의 밑바탕.
- [[Apache DataFusion]] — **같은 자리의 현대적 대안.** Calcite는 JVM 생태계의 공통 뼈대이고,
  DataFusion은 Rust·Arrow 생태계에서 파서·플래너·실행기를 함께 제공한다.

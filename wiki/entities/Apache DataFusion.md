---
type: entity
title: Apache DataFusion
area: [data-engineering]
aliases: [DataFusion, embedded SQL engine, 임베디드 SQL 엔진]
tags: [data-engineering, apache, sql, query-engine, arrow, rust]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch8 SQL on the lake]]"]
---

# Apache DataFusion

**Arrow 컬럼 배치 위에서 동작하는 Rust 기반 SQL·분석 엔진.** 단독 제품으로 세우는 것이 아니라,
**애플리케이션·도구·다른 쿼리 엔진 안에 작은 SQL 엔진으로 심는다.**

> **"SQL 실행 계층도 제품에 내장될 수 있다."**

- **Arrow 네이티브** — [[Columnar and in-memory data formats]]의 Arrow가 메모리에서 컬럼 배치를
  다루면, DataFusion은 **그 위에서 SQL과 분석을 수행한다.**
- **앱 내장** — 거대 웨어하우스를 따로 운영하지 않고, 파이프라인 도구·노트북·커스텀 서비스가 SQL과
  실행 계획을 재사용한다.
- **확장** — 커스텀 함수·플래너·소스로 특화 가능. 커뮤니티와 벤더가 이를 바탕으로 목적에 맞는 특화
  엔진을 만든다.

⚠️ **범용 웨어하우스가 아니다.** 완제품 클러스터가 아니라 **엔진을 구성하는 부품**이다. Doris·Impala를
대체하지 않는다.

## 왜 알아야 하나

⭐ **Arrow 생태계가 저장·전송·실행까지 이어지는 지점**이 여기다.

| Arrow 생태계 | 담당 |
|---|---|
| Parquet | 디스크 위의 컬럼 저장 |
| **Arrow** | 메모리 위의 컬럼 표현 |
| Arrow Flight SQL | 컬럼 배치를 그대로 옮기는 전송 프로토콜 |
| **DataFusion** | 그 위에서 SQL을 실행 |

[[Columnar and in-memory data formats]]가 이미 "Arrow는 처리 최적화"라고 말하는데, **그 '처리'를
실제로 하는 물건의 이름**이 DataFusion이다. 직접 설치하지 않아도 Arrow 생태계를 이해할 때 자주
마주친다.

## 위키 안에서의 위치

- [[SQL execution layer]] — 엔진 유형 중 **임베디드 엔진** 칸.
- [[Columnar and in-memory data formats]] — Arrow·Parquet과의 층위.
- [[Apache Calcite]] — 같은 "SQL 뼈대" 자리의 JVM 쪽 선배. Calcite는 파서·옵티마이저만 주고,
  DataFusion은 실행기까지 함께 준다.
- [[NVIDIA RAPIDS]] — cuDF도 Arrow 기반이다. Arrow가 CPU·GPU·언어 경계를 넘는 공통 표현이 된 이유가
  이 계열 전체에서 반복된다.

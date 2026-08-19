---
type: concept
title: SQL execution layer
area: [data-engineering]
aliases:
  - SQL 실행 계층
  - Query engine
  - Query engine layer
  - 쿼리 엔진
  - 쿼리 엔진 계층
  - MPP
  - Apache Doris
  - Doris
  - Apache Impala
  - Impala
  - Apache Kyuubi
  - Kyuubi
  - Apache Drill
  - Drill
  - Apache Phoenix
  - Phoenix
  - Apache ShardingSphere
  - ShardingSphere
  - Spark SQL
  - Trino
  - Presto
  - schema-on-read
  - 스키마리스
  - 샤딩
  - sharding
tags: [data-engineering, lakehouse, query-engine, sql, mpp, olap]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch8 SQL on the lake]]"]
---

# SQL execution layer

**저장만으로는 아무도 데이터를 볼 수 없다.** 저장된 테이블을 실제 SQL로 읽어 사람에게 전달하는 층.
[[Analytical data storage tiers]]가 스토리지와 쿼리 엔진의 결합을 풀었다면, **그 분리의 대가로 새로
생긴 선택 문제**가 이 층이다.

> **"레이크하우스는 저장과 실행이 짝을 이룰 때 완성된다."**
> 저장이 아무리 잘 되어 있어도 질의 엔진이 없으면 조회할 수 없고, 엔진이 아무리 빨라도 믿을 수 있는
> 테이블이 없으면 결과를 신뢰할 수 없다.

## ⭐ 3단계로 나눠 보면 이름이 정리된다

데이터가 **사람에게 도달하는 순서**대로 세 단계다.

| | 단계 | 하는 일 | 대표 |
|---|---|---|---|
| 1️⃣ | **테이블 규칙** | "무엇이 진짜 최신 데이터인지"를 정한다 | [[Table formats]] (Iceberg 등) |
| 2️⃣ | **SQL 실행** | 스캔·조인·집계를 수행한다 | Impala · Spark SQL · Doris · [[Apache DataFusion]] |
| 3️⃣ | **접속·소비** | 결과를 사람이 쓰는 화면과 연결한다 | Kyuubi · JDBC · Superset |

> **"테이블의 물리적인 데이터는 테이블 포맷이, 계산은 엔진이, 접속은 게이트웨이가 맡는다.
> 제품이 바뀌어도 이 역할 구분은 그대로 둔다."**

[[Apache Calcite]]처럼 SQL 문장을 실행 계획으로 바꿔 주는 부품은 **2️⃣ 안에 숨어 있다** — 설치
목록에 오르지 않는다.

## 엔진을 가르는 축 — "데이터가 어디에 사는가"

"가장 빠른 엔진"으로 고르는 문제가 아니다. **엔진이 데이터를 소유하는지 아닌지**가 첫 갈림길이다.

| 유형 | 데이터 위치 | 대표 | 언제 |
|---|---|---|---|
| **웨어하우스 제품** | 엔진이 자체 저장·테이블 모델을 갖는다 | Doris | 고정 리포트 + 동시 접속 많은 대시보드 |
| **레이크 질의 엔진** | 레이크 파일을 **복사하지 않고** 그대로 | Impala · Trino | 레이크를 SQL로 바로 조회 |
| **처리 엔진의 SQL 계층** | 레이크 파일 | Spark SQL | ETL과 SQL이 한몸일 때 |
| **임베디드 엔진** | 호스트 앱의 메모리 | [[Apache DataFusion]] | 제품·도구 안에 SQL을 심을 때 |
| **게이트웨이**(엔진 아님) | — | Kyuubi | 표준 JDBC/ODBC로 분산 엔진을 여는 앞단 |
| **공통 부품**(엔진 아님) | — | [[Apache Calcite]] | 파싱·검증·최적화 |

⭐ 판단 순서는 제품 벤치마크가 아니라 **주 부하가 무엇인지**다 — 대시보드인가, 레이크에서 그때그때
하는 탐색인가, ETL과 SQL의 통합인가. 그리고 그보다 먼저 **"레이크를 바로 조회할지, 별도 웨어하우스로
옮길지"** 를 정하면 나머지는 따라온다.

## SQL이라는 한 단어가 가리는 세 개의 경계

**같은 "SQL"이라고 해서 같은 문제를 푸는 도구가 아니다.** 이 층에서 헷갈림이 생기는 지점은 셋이다.

1. **분석용 SQL ≠ 운영용 SQL.** ShardingSphere는 샤딩·읽기 분리·분산 트랜잭션을 하는 **운영 DB
   미들웨어**이지 웨어하우스 엔진이 아니다. 앱에는 DB가 하나처럼 보이고 뒤에서 여러 물리 DB로
   라우팅한다. ⚠️ **운영 DB 확장 문제를 분석 도구로 해결하려 들면 더 큰 문제를 만든다.**
   → [[Analytical data storage tiers]]의 OLTP/OLAP 구분, [[Schema-centric data modeling]]
2. **schema-on-write ≠ schema-on-read.** Drill은 테이블을 미리 정의하지 않고 **읽을 때 구조를
   파악한다**(스키마리스). 현대 레이크하우스가 Iceberg·Parquet으로 스키마를 강화하는 방향과 반대지만,
   탐색·프로토타이핑·이질적 소스 질의에서는 유효하다. 판단 기준: **반정형 탐색 요구가 큰가** —
   크면 전용 도구, 작으면 주 엔진의 JSON 함수.
3. **SQL은 레이크 전용 언어가 아니다.** Phoenix는 HBase 위에 SQL·JDBC와 이차 인덱스를 올린다.
   특화 저장소 위에도 SQL 계층이 얹힌다. → [[NoSQL]]

## 도구를 바꾸기 쉬워도 설계는 남는다

엔진을 둘 두는 조직도 있지만 **어떤 테이블의 기준 데이터가 어디에 있는지**는 명확해야 한다.

⭐ **[[Table formats]]의 오픈 테이블이 있으면 도구 교체는 쉬워지지만, 의미 계층·권한·SLA는 여전히
설계 대상이다.** 즉 이 층은 [[Data catalog and semantic layer]]와 [[Data SLA and observability]]를
면제해 주지 않는다 — 오히려 엔진이 여러 개가 되는 순간 그 셋이 처음으로 진짜 문제가 된다.

3단계의 1️⃣ "테이블 규칙"도 마찬가지다. 오픈 테이블 포맷만으로 "무엇을 믿을지"가 정해지지 않는다 —
어느 스냅샷이 현재인지 가리키는 것은 **카탈로그**다. → [[Object storage layout]],
[[Apache Map - Ch1 How to read this book]]

## ⚠️ 이 층의 실제 기본값은 Apache 밖에 많다

Apache 프로젝트만 보면 이 층의 지형이 왜곡된다. 실무에서 이 자리를 가장 많이 채우는 것은
**Trino/Presto**, 그리고 Snowflake·BigQuery·Databricks SQL 같은 SaaS 웨어하우스다. Impala는
"온프레미스·Hadoop 활용이 큰 조직에서는 여전히 유효한" 쪽이고, 신규 클라우드 레이크하우스의 기본값이
아니다.

**그래서 역할로 외우고 제품명은 갈아 끼운다** — *"엔진 이름은 바뀌어도 그 역할은 남는다."*

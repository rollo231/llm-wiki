---
type: source
title: Apache Map - Ch8 SQL on the lake
area: [data-engineering]
aliases: [Apache 지도 Ch8, Apache 지도 레이크 위에서 SQL, Apache Map Ch8]
tags: [data-engineering, apache, sql, query-engine, lakehouse, book]
created: 2026-08-19
updated: 2026-08-19
sources: [raw/data-engineering/apache/apache-book-full-spread.pdf]
---

# Apache Map - Ch8 SQL on the lake

『Apache로 읽는 데이터 기술의 지도』(이현수, 2026) **Ch8. 레이크 위에서 SQL을 실행하기** — 개념
10개, PDF pp.63–73. 트래커: [[Apache data technology map (book)]].

**이 위키의 가장 큰 공백이었던 장이다.** 저장(포맷·테이블)과 소비(BI)는 두꺼운데 그 사이가 비어
있었다. 이 장이 채우는 것은 개별 제품이 아니라 **계층 하나**다 → [[SQL execution layer]].

## ⭐ 이 장의 실질은 마지막 개념 하나다

개념 1~8은 도구 카탈로그이고, **개념 10이 논지**다.

> "앞 장까지는 데이터를 파일과 테이블로 어떻게 저장하는지를 다뤘습니다. **하지만 저장만으로는 아무도
> 데이터를 볼 수 없습니다.** (…) 저장이 아무리 잘 되어 있어도 질의 엔진이 없으면 조회할 수 없고,
> 엔진이 아무리 빨라도 믿을 수 있는 테이블이 없으면 결과를 신뢰할 수 없습니다. 그래서 **레이크하우스는
> 저장과 실행이 짝을 이룰 때 완성됩니다.**"

그리고 이름 10개를 **데이터가 사람에게 도달하는 순서**로 3단계로 접는다.

1. **테이블 규칙** — Iceberg 등으로 "무엇을 믿을지" 정함
2. **SQL 실행** — 엔진이 스캔·조인·집계를 수행
3. **접속·소비** — JDBC·게이트웨이·BI로 사람에게 연결

> **"테이블의 물리적인 데이터는 테이블 포맷이, 계산은 엔진이, 접속은 게이트웨이가 맡는다.
> 제품이 바뀌어도 이 역할 구분은 그대로 둔다."**

Calcite는 2️⃣ **안에 숨어 있고**, Phoenix·ShardingSphere는 레이크가 아니라 HBase·운영 DB 쪽에서
같은 "SQL 접근" 문제를 다룬다 — 저자가 직접 이렇게 정리한다. 개념 10이 개념 1~8의 **분류표**인 셈이다.

## 개념 10개

전부 🔸 **Tier 2다. Tier 1이 하나도 없는 유일한 실무 장이다** — 그 이유는 아래 §비판.

| # | 개념 | 한 줄 | 3단계 |
|---|---|---|---|
| 1 | **Doris** | 실시간 적재 + 리포팅·대화형 분석용 **MPP 웨어하우스**. 자체 저장·테이블 모델을 갖는다 | 2️⃣ |
| 2 | **Impala** | 레이크 파일을 **복사하지 않고** 바로 읽는 고성능 MPP SQL 엔진. Hive보다 낮은 지연이 목표였다 | 2️⃣ |
| 3 | **DataFusion** | Arrow 배치 위의 Rust SQL 엔진. 제품 **안에 심는** 미니 엔진 → [[Apache DataFusion]] | 2️⃣ |
| 4 | **Calcite** | SQL 파서·검증·옵티마이저 **프레임워크**. Hive·Drill·Flink SQL이 쓴다 → [[Apache Calcite]] | 2️⃣ 내부 |
| 5 | **Kyuubi** | Spark·Flink를 JDBC/ODBC로 열어 주는 멀티테넌트 SQL **게이트웨이**. 세션·권한·엔진 수명주기 관리 | 3️⃣ |
| 6 | **Drill** | 스키마를 미리 정의하지 않는 **schema-on-read** SQL. JSON·중첩·이질적 소스 탐색 | 2️⃣ |
| 7 | **Phoenix** | HBase 위에 SQL·JDBC와 이차 인덱스를 올린다 | (레이크 밖) |
| 8 | **ShardingSphere** | 샤딩·읽기 분리·분산 트랜잭션 **운영 DB 미들웨어**. 웨어하우스 엔진이 아니다 | (레이크 밖) |
| 9 | Doris vs Impala vs Spark SQL | 비교 절 — 아래 | — |
| 10 | SQL 실행 계층이 하는 일 | **이 장의 논지** — 위 | — |

## 비교 절 (개념 9) — 세 축

> "**'가장 빠른 엔진' 하나로 고르기보다**, 주 부하가 대시보드인지, 레이크에서 그때그때 탐색하는
> 질의인지, ETL과 SQL 통합인지부터 정하는 편이 낫습니다."

| | 정체 | 이럴 때 |
|---|---|---|
| 🔹 **Doris** | 리포팅형 MPP **웨어하우스 제품** | 고정 리포트 + 동시 접속 많은 대시보드가 핵심 |
| 🔸 **Impala** | 레이크 대상 **질의 엔진** | 이미 Hadoop/레이크 위 대화형 SQL을 Impala로 운영 중 → 유지·최적화가 우선 |
| ▪️ **Spark SQL** | 처리 엔진과 결합된 **SQL 계층** | 파이프라인과 분석이 Spark 중심 (+ Kyuubi 같은 게이트웨이) |

⭐ 그리고 **엔진을 둘 두더라도 "어떤 테이블의 기준 데이터가 어디에 있는지"는 명확해야 한다**는
경고가 붙는다.

> "Iceberg 같은 오픈 테이블이 있으면 도구를 변경하는 것은 쉬워지지만, **의미 계층·권한·SLA는 여전히
> 설계 대상입니다.**"

이 한 줄이 [[Data catalog and semantic layer]]와 [[Data SLA and observability]]를 이 층에 붙여 준다.
**엔진이 하나일 때는 안 보이던 문제가, 엔진이 둘이 되는 순간 처음으로 진짜 문제가 된다.**

## SQL이라는 단어가 가리는 경계 셋

저자가 개념 6·7·8을 **넣은 이유를 스스로 밝히는데**, 세 개 다 "SQL"이라는 한 단어의 오해를 깨는
용도다. 카탈로그로 읽으면 잡동사니처럼 보이고, 이 의도로 읽으면 일관된다.

1. **Drill** — *"'SQL은 오직 깔끔한 테이블에만 쓴다'는 생각을 바로잡는 역할."*
   현대 레이크하우스가 Iceberg·Parquet으로 스키마를 강화하는 흐름과 **방향이 다르다**고 명시하면서도
   탐색·프로토타이핑에서는 유효하다고 남긴다. 판단은 요구 크기 — 크면 전용 도구, 작으면 주 엔진의
   JSON 함수.
2. **Phoenix** — *"SQL이 레이크 전용 언어가 아니라는 사실."* 특화 저장소 위에도 SQL 계층이 얹힌다.
3. **ShardingSphere** — *"SQL에도 분석용과 운영용이 있다는 경계를 분명히 하기 위해서."*
   ⚠️ **"운영 DB 확장 병목을 분석 도구로 해결하려다 더 큰 문제를 마주칠 수 있다."**

세 번째가 이 위키에 특히 정확히 꽂힌다 — [[Spatial omics platform roadmap]]에서 카탈로그 저장소를
Iceberg → Postgres로 정정한 근거가 바로 *"행 수천 개짜리 상태 테이블은 OLAP이 아니다"* 였다.
**같은 오류의 반대 방향**이 여기 적혀 있다.

## ⚠️ 비판 — Tier 1이 0개인 이유는 이 계층의 기본값이 Apache 밖에 있기 때문이다

이 장은 실무 10개 장 중 **유일하게 Tier 1이 없다**. 저자가 이 계층을 얕게 봤기 때문이 아니다 —
책 스스로 그 이유를 두 번 흘린다.

- 개념 2(Impala): *"클라우드 시대에는 **Trino**·Spark SQL·웨어하우스 SaaS가 같은 역할을 많이 맡지만,
  온프레미스·Hadoop 활용이 큰 조직에서는 여전히 유효한 엔진입니다."*
- 개념 9: *"**Trino 등 비Apache 엔진**도 같은 역할을 하므로 함께 비교하면 됩니다."*

⭐ **즉 이 책의 Tier는 "Apache 안에서의 상대 순위"이고, 시장 기본값과 같지 않다.** SQL 실행 계층의
실제 기본값(Trino/Presto · Snowflake · BigQuery · Databricks SQL)이 Apache 재단 밖에 있어서 Tier 1로
올릴 후보가 애초에 없었던 것이다. **Ch8의 Tier 1 = 0은 이 책의 렌즈가 만든 왜곡의 증거이지, 계층의
중요도가 낮다는 뜻이 아니다.**

읽는 방법: **이 장은 역할 분류표로만 쓰고, 제품 선택은 여기서 하지 않는다.** 저자 본인의 표현이
그렇다 — *"엔진 이름은 바뀌어도 그 역할은 남습니다."*

## 👍 반대로 이 장의 강점

⭐ **출처 없는 수치가 사실상 없다.** 이 장 전체에서 숫자는 Doris의 *"질의 응답은 1초 미만에서 수 초
안을 목표로"* 하나뿐이고, 그것도 "목표로 합니다"라고 헤지되어 있다.

[[AI Data Engineering (Fast Campus course)]]가 `80% 비정형` · `70% 시간 단축` · `하둡보다 100배` 같은
출처 없는 배지를 남발했던 것과 대비된다. **깊이는 얕지만 거짓은 없다** — 이 책의 신뢰 프로필은 코스와
반대다.

대신 값을 치른 곳이 있다. **개념 1~8이 서로를 "이건 저것과 다르다"로만 설명한다.** Doris를 읽으면
"Impala와 다르다", Impala를 읽으면 "Doris·Pinot과 다르다", DataFusion을 읽으면 "Doris·Impala를
대체하지 않는다"… **차이는 8번 말하는데 각각이 내부적으로 어떻게 동작하는지는 한 번도 말하지 않는다.**
[[Apache Spark]]의 In-Memory + DAG 같은 설명이 이 장에는 없다.

## 위키에 들어온 것

| | 페이지 |
|---|---|
| 새 개념 | [[SQL execution layer]] — 3단계 분해 + 엔진 유형 6종 + 경계 셋 |
| 새 엔티티 | [[Apache Calcite]] · [[Apache DataFusion]] |
| 흡수 | Doris · Impala · Kyuubi · Drill · Phoenix · ShardingSphere · Trino → [[SQL execution layer]]의 별칭과 표 |

**엔티티로 승격한 기준**: 다른 페이지에서 반복해 참조될 부품인가. Calcite는 Hive·Drill·Flink SQL의
공통 의존이고, DataFusion은 Arrow 생태계(Parquet→Arrow→Flight SQL→DataFusion)의 마지막 칸이다.
나머지 6개는 개념당 500자라 전용 페이지를 만들면 껍데기가 된다 — Doris는 **Ch9(Druid·Pinot·Kylin)를
읽은 뒤** 비교가 가능해질 때 승격을 재검토한다.

## 다음

- **Ch9(빠르게 읽고 바로 보여 주기)** — Druid·Pinot·Kylin·Cassandra·HBase·Lucene·Solr. 이 장의
  마지막 문장이 그대로 예고한다: *"다음 파트는 같은 '데이터를 읽고 싶다'는 요구를, 더 특화된 저장소와
  서비스로 나누는 주제로 이어집니다."* Phoenix ↔ HBase, Doris ↔ Pinot/Druid가 거기서 만난다.
- **Ch6(오픈 테이블 포맷)** — 3단계의 1️⃣. [[Table formats]]가 Delta 로그 구조만 아는 상태를 메운다.

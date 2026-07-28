---
type: concept
title: Analytical data storage tiers
area: [data-engineering]
aliases:
  - Data warehouse
  - Data lake
  - Data lakehouse
  - 데이터 웨어하우스
  - 데이터 레이크
  - 데이터 레이크하우스
  - DW
  - data swamp
tags: [data-engineering, storage, data-warehouse, data-lake, lakehouse, olap]
created: 2026-07-28
updated: 2026-07-28
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers"]
---

# Analytical data storage tiers

분석용 데이터를 담는 세 가지 저장 계층 — **데이터 웨어하우스 · 데이터 레이크 · 데이터 레이크하우스**.
소스에서 매번 데이터를 끌어오는 건 비효율적이고 원본 시스템에 부담을 주므로, 처리 전에 중앙 저장소로
한 번 적재해두는 것이 공통 전제다. 셋을 가르는 축은 세 개다.

| | 구조 강제 | 쿼리 엔진 | 저장 비용 | 담을 수 있는 것 |
|---|---|---|---|---|
| **웨어하우스** | 강제 (정형) | **강결합** — 자체 엔진을 함께 제공 | 최고 | 정형·정제 데이터 |
| **레이크** | 없음 | 분리 — 직접 붙인다 | 최저 (오브젝트 스토리지) | 정형·반정형·비정형·바이너리 |
| **레이크하우스** | 부분 (스키마 정의 필요) | 분리 | 중간 | 정형·반정형 (비정형은 부적합) |

**쿼리 엔진 결합 축이 실무에서 가장 자주 놓치는 지점이다.** MySQL·Mongo만 다뤄봤다면 "저장소가
쿼리 엔진을 내장한다"가 당연해 보이지만, 레이크·레이크하우스에서는 저장과 컴퓨트가 분리된다.
그래서 **레이크하우스와 웨어하우스는 비용을 1:1로 비교할 수 없다** — 워크로드에 따라
레이크하우스 + 별도 컴퓨트가 웨어하우스보다 크게 쌀 수 있다.

## 데이터 웨어하우스

PostgreSQL·MySQL 같은 DB와 비슷하지만 **분석 워크로드에 최적화**된 것.

- **OLTP vs OLAP** — MySQL은 OLTP로 **행** 단위 작업에 최적화되어 있다(id로 유저 레코드 하나 가져오기).
  웨어하우스는 OLAP으로 **열** 단위에 최적화된다. `orders` 테이블에 "작년 지역별 총매출"을 물으면
  웨어하우스가 훨씬 빠른 이유. *단, 작은 프로젝트라면 전통 DB로도 놀랄 만큼 멀리 갈 수 있다.*
- **저장과 쿼리 방식을 함께 관리한다** — 자체 쿼리 엔진을 제공하고 거기에 강하게 묶여 있다.
- 정형·정제 데이터에 최적화된 만큼 **전통적으로는 처리된 데이터의 최종 저장소**였다. 다만
  [[ETL and ELT]]의 ELT가 흔해지면서 **raw 데이터의 착지 지점**으로도 쓰이고, 변환을 웨어하우스
  안에서 바로 한다.
- 구조화된 데이터 + 최적화된 엔진 덕에 쿼리가 빠르다 → BI·리포팅 도구의 사용자 경험과 잘 맞는다.
- 셋 중 **가장 비싸다** — 성능과 편의를 함께 사는 값.

상용: **Snowflake**, **BigQuery**(Google), **Redshift**(Amazon).
오픈소스·셀프호스팅: **ClickHouse**, **Apache Doris**, **StarRocks**.

## 데이터 레이크

웨어하우스의 반대편. CSV·Parquet·JSON 등을 **거의 또는 전혀 처리하지 않고 그냥 쏟아붓는 곳**.
쉽게 말해 **"큰 클라우드 폴더 + α"**. 구조에 제약이 없어 정형(Parquet)·반정형(CSV)·비정형(이메일)·
바이너리(이미지)를 모두 담는다.

만드는 법: 싼 스토리지(**S3**, **Google Cloud Storage**, **Azure Blob Storage**)에서 시작 → 네이밍·
파티셔닝 규약을 세우고 → Parquet 몇 개 올리고 → 접근 정책을 걸고 → **메타데이터 카탈로그 + 쿼리
엔진**을 붙인다. 관리하지 않으면 **data swamp(데이터 늪)** 가 된다.

그 "+α"가 핵심이다. 레이크를 *쓸 수 있게* 만드는 두 부품:

- **메타데이터 카탈로그(metastore)** — 어떤 데이터가 있는지 기술한다: 테이블명, 스키마, 그것이
  어떤 파일에 매핑되는지. **Hive Metastore**, **AWS Glue Data Catalog**, **Unity Catalog**.
  → 사람이 읽는 data catalog와는 다른 물건이다: [[Data catalog and semantic layer]]
- **쿼리 엔진** — SQL을 받아 레이크의 데이터에 실행한다. 카탈로그의 도움을 받아 관련 파일만 골라
  읽는다. **Apache Spark**, **Trino**, **Amazon Athena**.

이 둘이 있어야 "스크립트에서 CSV 파일을 손으로 찾아 내려받고 파싱해 메모리에 올리는" 대신
**질의**할 수 있다.

매니지드: **Azure Data Lake**, **Snowflake**(웨어하우스 회사지만 레이크도 한다).

## 데이터 레이크하우스

레이크 + 웨어하우스. 레이크 **위에** 블록 몇 개를 얹어 웨어하우스에 가깝게 만든 것이고,
그중 가장 중요한 블록이 **테이블 포맷**이다 → [[Table formats]].

테이블 포맷이 얹어주는 것:

- **ACID** — 여러 애플리케이션이 같은 데이터를 동시에 다뤄도 깨지지 않는다.
- **스키마 강제** — 레이크보다 엄격하다. 반정형도 담을 수 있지만 구조를 정의해야 하고 레이크하우스가
  그걸 강제한다. **완전 비정형은 레이크하우스의 대상이 아니다** — 밑이 레이크라 저장은 되지만
  테이블 포맷의 혜택을 하나도 못 받는다.
- **스키마 진화·버저닝**, **파티셔닝·인덱스 최적화**, 일부는 **time travel**.

싼 스토리지 위의 레이크 위에서 도니 웨어하우스보다는 여전히 싸다.
매니지드: **Google's Lakehouse for Apache Iceberg**(구 BigLake), **Databricks**(Delta Lake),
**IBM watsonx.data**(Iceberg).

## 링크

- 상세: [[Table formats]] — 레이크하우스를 레이크와 가르는 층
- 카탈로그 3분할: [[Data catalog and semantic layer]] — metastore ≠ data catalog ≠ semantic layer
- 담기는 바이트: [[Columnar and in-memory data formats]]
- 채워 넣는 방식: [[ETL and ELT]], [[Medallion architecture]]
- 테이블 모양: [[Dimensional modeling]]
- 적용: [[SpatialData as a data engineering substrate]] — 공간 오믹스 포맷을 이 계층에 대응시킨 노트
- 출처: [[Data landscape guide for developers]]

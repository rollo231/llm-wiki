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
  - OLTP
  - OLAP
  - 데이터 사일로
tags: [data-engineering, storage, data-warehouse, data-lake, lakehouse, olap]
created: 2026-07-28
updated: 2026-08-19
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers", "[[AI DE Course - Ch2-1,2,3 Storage evolution]]"]
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

⭐ **그리고 분리한 대가로 "엔진을 고른다"는 문제가 새로 생긴다** — 그 층이 [[SQL execution layer]]다.
웨어하우스는 이 문제를 제품이 대신 정해 줬고, 레이크하우스는 사용자에게 넘긴다.

## 왜 중앙 저장소인가 — 사일로

"소스에서 매번 끌어오는 건 비효율적"이라는 이유 말고, 조직 쪽 이유도 있다.
부서별로 데이터를 중복 저장하면([[AI DE Course - Ch2-1,2,3 Storage evolution]]):

- **데이터 정합성 훼손** — 버전 불일치로 전사 데이터의 신뢰도 하락
- **협업 저하·의사결정 지연** — 전사 관점의 인사이트를 얻지 못한다
- **비용 상승** — 각기 다른 시스템·라이선스에 중복 투자

## 데이터 웨어하우스

PostgreSQL·MySQL 같은 DB와 비슷하지만 **분석 워크로드에 최적화**된 것.

- **OLTP vs OLAP** — MySQL은 OLTP로 **행** 단위 작업에 최적화되어 있다(id로 유저 레코드 하나 가져오기).
  웨어하우스는 OLAP으로 **열** 단위에 최적화된다. `orders` 테이블에 "작년 지역별 총매출"을 물으면
  웨어하우스가 훨씬 빠른 이유. *단, 작은 프로젝트라면 전통 DB로도 놀랄 만큼 멀리 갈 수 있다.*

  | | OLTP (Row Oriented) | OLAP (Columnar) |
  |---|---|---|
  | 잘하는 것 | 단건 CRUD — 한 사용자의 전체 정보를 **한 번의 디스크 접근**으로 (헤드 이동 최소화) | 필요한 컬럼만 스캔 → **I/O 부하 1/10~1/100** |
  | 못하는 것 | '평균 나이' 계산 시 불필요한 이름·주소까지 읽어야 함 | 단건 갱신 |
  | 압축 효율 | 낮음 **1:3** (엔트로피 높음 — 타입 혼재) | 높음 **1:10+** (엔트로피 낮음 — 같은 타입 연속) |
  | 예 | 은행 계정계, 배달 주문 DB | 분석·리포팅·AI 학습 |

  한 줄 판별: **"백만 건 중 한 건" → Row / "백만 건 매출 합계" → Columnar.**
  압축률 차이의 근거는 엔트로피다 → [[Columnar and in-memory data formats]]

- ⭐ **그 사이를 한 저장소로 노리는 것도 있다** — **Apache Kudu**는 행 단위 수정을 지원하면서
  컬럼형 스캔을 유지한다(HDFS는 스캔 강·갱신 약, OLTP는 갱신 강·초대형 스캔 부담). ⚠️ 오픈 테이블
  포맷과 **계층이 다른 자체 저장 엔진**이므로 Iceberg와 같은 계열로 묶으면 안 된다 →
  [[Table formats]] §이건 테이블 포맷이 아니다
- **OLTP와 OLAP은 고르는 문제가 아니다** — 실무는 둘을 함께 쓰고, **[[Change data capture|CDC]]로
  잇는다**: front-end는 OLTP로 고객 요청을 처리하고 변경분을 OLAP에 동기화한다.
  스키마 전략도 갈린다 — OLTP는 정규화로 무결성, OLAP은 star schema·비정규화로 조인 최소화
  ([[Dimensional modeling]]).
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

**레이크를 성립시키는 4요소**([[AI DE Course - Ch2-1,2,3 Storage evolution]]):
**확장성**(오브젝트 스토리지 기반, PB급까지 성능 저하 없는 수평 확장) ·
**접근성**(메타데이터 카탈로그 + schema-on-read) · **보안**(중앙 IAM, 전송/저장 암호화) ·
**비용 관리**(lifecycle 정책으로 콜드 데이터를 저렴한 계층으로 이동).

**늪이 되는 이유는 두 층위다:**

- **기술적** — ACID·스키마 강제가 없어 깨진 데이터가 섞이고 최신 버전을 모른다
  → [[Table formats]]가 푼다
- **조직적** — 찾을 수 없고, 정의가 모호하고, 신뢰할 수 없다
  → [[Data catalog and semantic layer]]가 푼다

## 저장소 설계 5단계

강의가 제시하는 실무 절차. 위의 세 계층 중 무엇을 고를지가 아니라 **어떻게 조합할지**의 순서다.

1. **워크로드 진단** — I/O 패턴, Read/Write 비율(CRUD vs 조회), 지연 요구(실시간 vs 배치)
2. **저장 방식 결정** — 트랜잭션이면 Row(RDBMS), 분석이면 Columnar(DW/Lake)
3. **하이브리드 설계** — OLTP로 요청 처리 + **CDC로 OLAP 동기화**
4. **스키마 전략** — OLTP 정규화 / OLAP star schema·비정규화
5. **최적화** — 압축 코덱(Snappy·Zstd), 파티셔닝(날짜/지역별)

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
- 채워 넣는 방식: [[ETL and ELT]], [[Change data capture]], [[Medallion architecture]]
- 테이블 모양: [[Dimensional modeling]]
- **비정형은 어디로 가나:** [[Unstructured data ingestion]] — 완전 비정형은 레이크하우스의 대상이
  아닌데, 실무는 **S3 원본 + NoSQL 메타데이터 이원화 + Vector DB**로 그 경계를 우회한다
- 적용: [[SpatialData as a data engineering substrate]] — 공간 오믹스 포맷을 이 계층에 대응시킨 노트
- **강의가 다루지 않는 축:** 이 페이지의 **쿼리 엔진 결합**(웨어하우스는 자체 엔진과 강결합, 레이크는
  분리)과 그로 인한 **비용 비교 불가** 논의는 강의에 없다. 랜드스케이프 가이드 쪽 근거만 있다.
- 출처: [[Data landscape guide for developers]], [[AI DE Course - Ch2-1,2,3 Storage evolution]]

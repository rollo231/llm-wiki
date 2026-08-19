---
type: entity
title: Apache data technology map (book)
area: [data-engineering]
aliases: [Apache로 읽는 데이터 기술의 지도, Apache 데이터 기술 지도, hyunsooIT Apache 책, Apache map book]
tags: [data-engineering, book, apache, chapter-tracker]
created: 2026-08-19
updated: 2026-08-19
sources: [raw/data-engineering/apache/apache-book-full-spread.pdf]
---

# Apache data technology map (book)

『**Apache로 읽는 데이터 기술의 지도** — 데이터 플랫폼을 구성하는 Apache 오픈소스 기술의 역할과
선택 기준』(hyunsooIT 데이터 시리즈). 이현수(hyunsooIT) 저, 2026.
**11개 장 / 개념 90개 / PDF 104페이지.**

이 페이지가 **장 트래커**다. 인제스트 단위는 **장 1개 = source 페이지 1개**(총 11개), 아래
[장별 진행](#장별-진행)의 체크 상태가 진행도다.

**진행: 1/11 — Ch1 ✅.**

## 이 자료의 성격 — 깊이가 아니라 넓이

[[AI Data Engineering (Fast Campus course)]]와 역할이 다르다. 강의는 한 개념에 여러 슬라이드를
써서 원리까지 파고들었고, 이 책은 **개념 1개당 정확히 1페이지**(본문 약 500자)다. 90개를 다 읽어도
어느 하나를 구현할 수는 없다.

대신 이 자료가 주는 것은 두 가지다.

- **넓이** — Apache 데이터 프로젝트 90개의 위치. 이 중 42개는 위키에 관련 페이지조차 없었다.
- **선택 기준** — 저자가 매긴 **Tier 1/2 라벨**과 `A vs B, 언제 무엇을 고를까` 형태의 **비교 절
  11개**(Kafka vs Pulsar · Spark vs Flink · Parquet vs ORC vs Avro · Iceberg vs Hudi vs Paimon ·
  NiFi vs Hop vs SeaTunnel · Airflow vs DolphinScheduler · Doris vs Impala vs Spark SQL ·
  Druid vs Pinot · 메시지 큐 vs 이벤트 로그 · 검색 vs OLAP vs NoSQL · 배치 vs 마이크로배치 vs
  이벤트 타임). 이 비교 절이 이 책의 실질이다.

읽는 방향도 그래서 반대다 — 강의는 처음부터 끝까지 따라가는 자료였고, **이 책은 이름을 만났을 때
펼치는 사전**이다. 저자 자신이 그렇게 쓰라고 말한다("Tier 2는 필요한 순간에 사전처럼 펼쳐 보면
됩니다", 개념 2).

## 저자

이현수(Hyunsoo Lee, Ryan Lee). 데이터 엔지니어 출신의 데이터·AI 교육 전문가.

- Databricks · Senior Technical Instructor (2026~)
- Codeit · Data Engineering Lead Instructor (2024~2026)
- 천재교육 · Data Engineer (2022~2024) — 밀크T, AI 디지털 교과서(AIDT) 데이터 플랫폼·파이프라인

교육자 이력이 자료 형태에 그대로 드러난다 — 개념당 1페이지 고정, 장마다 목차 디바이더, 매 페이지
하단에 그 장의 순서 재표시. **일관성은 높고 밀도는 낮다.**

## Tier 체계 (저자 정의)

| | 뜻 | 개수 |
|---|---|---|
| 🔹 **Tier 1** | "특별한 이유가 없으면 여기서 고른다" — 표준급. 우선순위 | **22** |
| 🔸 **Tier 2** | 성숙했지만 기본값은 아닌, 목적이 뚜렷할 때 검토하는 전문 기술 | **68** |

⚠️ **Apache 공식 등급이 아니다.** 저자가 채택률·운영 사례를 기준으로 매긴 실무용 분류이고, 책 안에서
그렇게 명시한다. 저자 소속(Databricks)을 감안하면 레이크하우스 계열에 유리한 편향을 의심할 만하다 —
다만 Delta Lake는 Apache 프로젝트가 아니므로 이 책에 아예 없고, [[Table formats]]의 Delta 자리가
여기서는 Iceberg·Hudi·Paimon으로 채워진다.

**Tier 1 22개**: ZooKeeper · YARN · Kafka(2개념) · Pulsar · Spark · Flink · Beam ·
Parquet · ORC · Avro · Arrow · Iceberg · Hudi · Hive · NiFi · Airflow · Cassandra · HBase ·
Lucene · Solr · Superset.

## 레퍼런스 아키텍처 — 책 전체의 축

책은 90개를 **역할 5단계 + 가로지르는 2계층**으로 배열한다. 장 번호가 곧 이 순서다.

| 역할 | 대표 | 장 |
|---|---|---|
| ① 소스 | 서비스 DB · 앱 로그 · 센서 | (책 밖) |
| ② 수집 | NiFi · Kafka Connect · Flink CDC | Ch7 |
| ③ 처리 | Spark · Flink | Ch4 |
| ④ 저장 | Parquet · Iceberg · Hudi | Ch5 · Ch6 |
| ⑤ 소비 | Doris · Pinot · Superset | Ch8 · Ch9 |
| ⟂ 오케스트레이션 | Airflow | Ch7 |
| ⟂ 기반 계층 | ZooKeeper · YARN | Ch2 |

이벤트 허브(Ch3)는 ②와 ③ 사이에 걸치고, 거버넌스(Ch10)와 특화 라이브러리(Ch11)는 전 단계를
가로지른다. → 자세한 내용은 [[Apache Map - Ch1 How to read this book]].

## 페이지 번호 주의

**표의 `PDF p`는 PDF 페이지 번호다.** 원본에 인쇄된 페이지 번호가 없다(A4 가로 슬라이드형,
파일명이 `full-spread`). 규칙은 단순하고 예외가 없다.

- **개념 1개 = PDF 1페이지.**
- 각 장 앞에 목차 디바이더 1페이지.
- 앞부속 3페이지(표지 · 저자 소개 · 목차).
- 검산: 90(개념) + 11(디바이더) + 3(앞부속) = **104** = `pdfinfo` 페이지 수. ✅

## 장별 진행

| 장 | 제목 | 개념 | Tier 1 | PDF p | source 페이지 | 상태 |
|---|---|---|---|---|---|---|
| Ch1 | 이 책을 읽는 법 | 5 | 0 | 4–9 | [[Apache Map - Ch1 How to read this book]] | ✅ |
| Ch2 | 분산 시스템을 떠받치는 기반 | 7 | 2 | 10–17 | `Apache Map - Ch2 Distributed foundations` | ⬜ |
| Ch3 | 이벤트 스트리밍의 중심 | 8 | 3 | 18–26 | `Apache Map - Ch3 Event streaming` | ⬜ |
| Ch4 | 배치와 스트림을 돌리는 엔진 | 6 | 3 | 27–33 | `Apache Map - Ch4 Batch and stream engines` | ⬜ |
| Ch5 | 데이터를 담는 포맷과 교환 계층 | 8 | 4 | 34–42 | `Apache Map - Ch5 Formats and exchange layer` | ⬜ |
| Ch6 | 파일을 테이블처럼 다루기 | 8 | 3 | 43–51 | `Apache Map - Ch6 Open table formats` | ⬜ |
| Ch7 | 데이터를 모으고 일정을 맞추기 | 10 | 2 | 52–62 | `Apache Map - Ch7 Ingestion and orchestration` | ⬜ |
| Ch8 | 레이크 위에서 SQL을 실행하기 | 10 | 0 | 63–73 | `Apache Map - Ch8 SQL on the lake` | ⬜ |
| Ch9 | 빠르게 읽고 바로 보여 주기 | 11 | 4 | 74–85 | `Apache Map - Ch9 Serving OLAP search and NoSQL` | ⬜ |
| Ch10 | 믿고 쓰게 만드는 계층 | 8 | 1 | 86–94 | `Apache Map - Ch10 Governance and BI` | ⬜ |
| Ch11 | 특화 분석과 공통 라이브러리 | 9 | 0 | 95–104 | `Apache Map - Ch11 Specialized analytics and libraries` | ⬜ |

백틱 표기는 **아직 만들지 않은** source 페이지의 예정 파일명이다(만들 때 위키링크로 바꾼다).

## 개념 90개 목차

`기존 위키` 열은 그 개념이 이미 위키의 어느 페이지에 흡수돼 있는지다. **빈 칸이 곧 공백**이며,
90개 중 **42개**가 빈 칸이다.

### Ch1. 이 책을 읽는 법 — 개념 5개 (Tier 1 0개) · PDF pp.4–9

| # | Tier | 개념 | 한 줄 | PDF p | 기존 위키 |
|---|---|---|---|---|---|
| 1 | 🔸 2 | Apache 오픈소스가 데이터 플랫폼의 표준이 된 이유 |  | 5 |  |
| 2 | 🔸 2 | Tier 1과 Tier 2, 어떻게 읽고 고를까 |  | 6 |  |
| 3 | 🔸 2 | Apache 레퍼런스 아키텍처 |  | 7 |  |
| 4 | 🔸 2 | 레이크하우스 기본 스택 | Spark · Parquet · Iceberg · Airflow · Superset | 8 |  |
| 5 | 🔸 2 | 실시간 스택 | Kafka · Flink · Pinot/Druid | 9 |  |

### Ch2. 분산 시스템을 떠받치는 기반 — 개념 7개 (Tier 1 2개) · PDF pp.10–17

| # | Tier | 개념 | 한 줄 | PDF p | 기존 위키 |
|---|---|---|---|---|---|
| 1 | 🔹 1 | Apache ZooKeeper | 분산 합의와 코디네이션의 기초 | 11 |  |
| 2 | 🔹 1 | Apache Hadoop YARN | 클러스터 리소스를 나누는 스케줄러 | 12 |  |
| 3 | 🔸 2 | Apache HDFS | 전통적인 분산 파일시스템 | 13 | [[Apache Hadoop]] |
| 4 | 🔸 2 | Apache Ozone | 클라우드형 분산 오브젝트 스토리지 | 14 | [[Object storage layout]] |
| 5 | 🔸 2 | Apache YuniKorn | Kubernetes 시대의 리소스 스케줄러 | 15 |  |
| 6 | 🔸 2 | Apache BookKeeper | 분산 로그·원장 저장 계층 | 16 |  |
| 7 | 🔸 2 | Apache Ratis | 합의·복제를 라이브러리로 쓰는 방법 | 17 | [[Replication and consensus]] |

### Ch3. 이벤트 스트리밍의 중심 — 개념 8개 (Tier 1 3개) · PDF pp.18–26

| # | Tier | 개념 | 한 줄 | PDF p | 기존 위키 |
|---|---|---|---|---|---|
| 1 | 🔹 1 | Apache Kafka, 여러 시스템을 잇는 중앙 이벤트 허브 |  | 19 | [[Apache Kafka]] |
| 2 | 🔹 1 | Apache Kafka의 핵심 부품 | 토픽·파티션·오프셋·컨슈머 그룹 | 20 | [[Apache Kafka]] |
| 3 | 🔸 2 | Apache Kafka Connect | 외부 시스템과 Kafka를 잇는 다리 | 21 | [[Apache Kafka]] |
| 4 | 🔹 1 | Apache Pulsar | 멀티테넌트 메시징 플랫폼 | 22 | [[Message broker]] |
| 5 | 🔸 2 | Kafka vs Pulsar, 언제 무엇을 고를까 |  | 23 | [[Message broker]] |
| 6 | 🔸 2 | Apache RocketMQ | 트랜잭션·순서·지연 메시지 | 24 | [[Message broker]] |
| 7 | 🔸 2 | Apache ActiveMQ와 Apache Qpid | 전통 메시지 브로커의 역할 | 25 | [[Message broker]] |
| 8 | 🔸 2 | 메시지 큐와 이벤트 로그는 무엇이 다른가 |  | 26 | [[Message broker]] |

### Ch4. 배치와 스트림을 돌리는 엔진 — 개념 6개 (Tier 1 3개) · PDF pp.27–33

| # | Tier | 개념 | 한 줄 | PDF p | 기존 위키 |
|---|---|---|---|---|---|
| 1 | 🔹 1 | Apache Spark | 배치·SQL·스트리밍을 한곳에 | 28 | [[Apache Spark]] |
| 2 | 🔹 1 | Apache Flink | 상태 기반 실시간 처리의 강자 | 29 | [[Apache Flink]] |
| 3 | 🔸 2 | Spark vs Flink, 경쟁이 아니라 역할 분담 |  | 30 | [[Stream processing semantics]] |
| 4 | 🔹 1 | Apache Beam | 실행 환경을 바꿔 쓸 수 있는 파이프라인 모델 | 31 |  |
| 5 | 🔸 2 | Apache StreamPark | Flink·Spark 앱 운영 플랫폼 | 32 |  |
| 6 | 🔸 2 | 배치·마이크로배치·이벤트 타임, 처리 방식 고르는 기준 |  | 33 | [[Batch and stream processing]] |

### Ch5. 데이터를 담는 포맷과 교환 계층 — 개념 8개 (Tier 1 4개) · PDF pp.34–42

| # | Tier | 개념 | 한 줄 | PDF p | 기존 위키 |
|---|---|---|---|---|---|
| 1 | 🔹 1 | Apache Parquet | 분석용 컬럼형 파일의 사실상 표준 | 35 | [[Columnar and in-memory data formats]] |
| 2 | 🔹 1 | Apache ORC | Hive·Hadoop 중심의 컬럼형 포맷 | 36 | [[Columnar and in-memory data formats]] |
| 3 | 🔹 1 | Apache Avro | 스키마와 함께 움직이는 행 지향 포맷 | 37 | [[Columnar and in-memory data formats]] |
| 4 | 🔸 2 | Parquet vs ORC vs Avro, 어디에 무엇을 쓸까 |  | 38 | [[Columnar and in-memory data formats]] |
| 5 | 🔹 1 | Apache Arrow | 메모리 위에서 언어를 넘는 컬럼 교환 | 39 | [[Columnar and in-memory data formats]] |
| 6 | 🔸 2 | Apache Arrow Flight SQL | 고속 SQL 데이터 이동 프로토콜 | 40 |  |
| 7 | 🔸 2 | Apache OpenDAL | 여러 스토리지를 하나의 API로 | 41 | [[Object storage layout]] |
| 8 | 🔸 2 | Apache CarbonData | 인덱싱이 강한 분석용 컬럼 포맷 | 42 |  |

### Ch6. 파일을 테이블처럼 다루기 — 개념 8개 (Tier 1 3개) · PDF pp.43–51

| # | Tier | 개념 | 한 줄 | PDF p | 기존 위키 |
|---|---|---|---|---|---|
| 1 | 🔸 2 | 오픈 테이블 포맷이란? | 파일을 테이블처럼 다루는 방법 | 44 | [[Table formats]] |
| 2 | 🔹 1 | Apache Iceberg | 여러 엔진이 공유하는 오픈 테이블 포맷 | 45 | [[Table formats]] |
| 3 | 🔹 1 | Apache Hudi | upsert·CDC·증분 읽기에 강한 레이크 테이블 | 46 | [[Table formats]] |
| 4 | 🔸 2 | Apache Paimon | 스트림과 배치를 잇는 레이크 테이블 | 47 |  |
| 5 | 🔸 2 | Iceberg vs Hudi vs Paimon 선택 가이드 |  | 48 | [[Table formats]] |
| 6 | 🔹 1 | Apache Hive | 메타스토어와 SQL 계층의 출발점 | 49 | [[Table formats]] |
| 7 | 🔸 2 | Apache Kudu | 업데이트와 분석을 함께 다루는 저장소 | 50 |  |
| 8 | 🔸 2 | 오픈 테이블 포맷이 레이크하우스를 바꾼 이유 |  | 51 | [[Analytical data storage tiers]] |

### Ch7. 데이터를 모으고 일정을 맞추기 — 개념 10개 (Tier 1 2개) · PDF pp.52–62

| # | Tier | 개념 | 한 줄 | PDF p | 기존 위키 |
|---|---|---|---|---|---|
| 1 | 🔹 1 | Apache NiFi | 눈으로 짜는 수집·라우팅 플랫폼 | 53 |  |
| 2 | 🔸 2 | Apache SeaTunnel | 배치·스트리밍·CDC 통합 | 54 |  |
| 3 | 🔸 2 | Apache Flink CDC | DB 변화를 이벤트로 만들기 | 55 | [[Change data capture]] |
| 4 | 🔸 2 | Apache Camel | 시스템과 프로토콜을 잇는 통합 프레임워크 | 56 |  |
| 5 | 🔸 2 | Apache Hop | 시각적 ETL·파이프라인 플랫폼 | 57 |  |
| 6 | 🔸 2 | NiFi vs Hop vs SeaTunnel, 통합 도구 고르기 |  | 58 |  |
| 7 | 🔹 1 | Apache Airflow | DAG로 파이프라인을 오케스트레이션하기 | 59 | [[Batch and stream processing]] |
| 8 | 🔸 2 | Apache DolphinScheduler | 시각적·분산 워크플로 스케줄러 | 60 |  |
| 9 | 🔸 2 | Airflow vs DolphinScheduler, 운영 관점 비교 |  | 61 |  |
| 10 | 🔸 2 | 수집·CDC·오케스트레이션을 한 그림으로 보기 |  | 62 | [[ETL and ELT]] |

### Ch8. 레이크 위에서 SQL을 실행하기 — 개념 10개 (Tier 1 0개) · PDF pp.63–73

| # | Tier | 개념 | 한 줄 | PDF p | 기존 위키 |
|---|---|---|---|---|---|
| 1 | 🔸 2 | Apache Doris | 실시간 리포팅에 강한 MPP 웨어하우스 | 64 |  |
| 2 | 🔸 2 | Apache Impala | 레이크 대상 고성능 SQL 엔진 | 65 |  |
| 3 | 🔸 2 | Apache DataFusion | Arrow 위에 올리는, 임베디드 SQL 엔진 | 66 | [[Columnar and in-memory data formats]] |
| 4 | 🔸 2 | Apache Calcite | SQL 파서·옵티마이저의 공통 뼈대 | 67 |  |
| 5 | 🔸 2 | Apache Kyuubi | Spark·Flink를 JDBC로 열어 주는 게이트웨이 | 68 |  |
| 6 | 🔸 2 | Apache Drill | 반정형 데이터용 스키마리스 SQL | 69 |  |
| 7 | 🔸 2 | Apache Phoenix | HBase를 SQL로 다루기 | 70 |  |
| 8 | 🔸 2 | Apache ShardingSphere | 샤딩과 DB 게이트웨이 미들웨어 | 71 | [[NoSQL]] |
| 9 | 🔸 2 | Doris vs Impala vs Spark SQL, 쿼리 엔진 선택 |  | 72 |  |
| 10 | 🔸 2 | 레이크하우스에서 SQL 실행 계층이 하는 일 |  | 73 | [[Analytical data storage tiers]] |

### Ch9. 빠르게 읽고 바로 보여 주기 — 개념 11개 (Tier 1 4개) · PDF pp.74–85

| # | Tier | 개념 | 한 줄 | PDF p | 기존 위키 |
|---|---|---|---|---|---|
| 1 | 🔸 2 | Apache Druid | 실시간 이벤트 분석 OLAP | 75 |  |
| 2 | 🔸 2 | Apache Pinot | 초저지연 사용자 대면 OLAP | 76 |  |
| 3 | 🔸 2 | Druid vs Pinot, 대시보드냐 서비스냐 |  | 77 |  |
| 4 | 🔸 2 | Apache Kylin | 미리 집계해 빠르게 조회하는 OLAP 엔진 | 78 | [[Dimensional modeling]] |
| 5 | 🔸 2 | Apache IoTDB | 산업·센서 시계열 데이터베이스 | 79 |  |
| 6 | 🔹 1 | Apache Cassandra | 멀티리전 wide-column NoSQL | 80 | [[NoSQL]] |
| 7 | 🔹 1 | Apache HBase | Hadoop 위의 wide-column 저장소 | 81 | [[NoSQL]] |
| 8 | 🔸 2 | Apache Ignite | 분산 인메모리 컴퓨팅·캐시 | 82 | [[Caching strategies]] |
| 9 | 🔹 1 | Apache Lucene | 검색을 만드는 역색인 라이브러리 | 83 | [[Hybrid search and reranking]] |
| 10 | 🔹 1 | Apache Solr | Lucene 기반 분산 검색 서버 | 84 | [[Hybrid search and reranking]] |
| 11 | 🔸 2 | 검색·OLAP·NoSQL, 소비 계층을 나누는 기준 |  | 85 | [[NoSQL]] |

### Ch10. 믿고 쓰게 만드는 계층 — 개념 8개 (Tier 1 1개) · PDF pp.86–94

| # | Tier | 개념 | 한 줄 | PDF p | 기존 위키 |
|---|---|---|---|---|---|
| 1 | 🔸 2 | Apache Atlas | 카탈로그·분류·계보 | 87 | [[Data catalog and semantic layer]] |
| 2 | 🔸 2 | Apache Ranger | 권한·정책·감사 | 88 | [[Data catalog and semantic layer]] |
| 3 | 🔸 2 | Apache Griffin | 데이터 품질을 재는 프레임워크 | 89 | [[Data SLA and observability]] |
| 4 | 🔸 2 | Apache Gravitino | 통합 메타데이터·카탈로그 | 90 | [[Data catalog and semantic layer]] |
| 5 | 🔸 2 | Apache Polaris | Iceberg 중심 레이크 카탈로그 | 91 | [[Table formats]] |
| 6 | 🔸 2 | Atlas·Ranger·Griffin으로 보는 거버넌스 삼각형 |  | 92 | [[Data catalog and semantic layer]] |
| 7 | 🔹 1 | Apache Superset | SQL 기반 BI·셀프서비스 분석 | 93 |  |
| 8 | 🔸 2 | Apache Zeppelin | 노트북으로 탐색하는 분석 환경 | 94 |  |

### Ch11. 특화 분석과 공통 라이브러리 — 개념 9개 (Tier 1 0개) · PDF pp.95–104

| # | Tier | 개념 | 한 줄 | PDF p | 기존 위키 |
|---|---|---|---|---|---|
| 1 | 🔸 2 | Apache TinkerPop | Gremlin 그래프 컴퓨팅 표준 | 96 | [[Graph database]] |
| 2 | 🔸 2 | Apache HugeGraph | 분산 그래프 데이터베이스 | 97 | [[Graph database]] |
| 3 | 🔸 2 | Apache Sedona | 대용량 지리공간 처리 | 98 |  |
| 4 | 🔸 2 | Apache Mahout | 분산 머신러닝·행렬 연산 | 99 |  |
| 5 | 🔸 2 | Apache MADlib | SQL 안에서 돌리는 ML | 100 |  |
| 6 | 🔸 2 | Apache SINGA | 분산 딥러닝 프레임워크 | 101 |  |
| 7 | 🔸 2 | Apache OpenNLP | 기초 NLP 라이브러리 | 102 |  |
| 8 | 🔸 2 | Apache DataSketches | 근사 집계 알고리즘 | 103 |  |
| 9 | 🔸 2 | Apache Commons Math | 수치·통계 공통 라이브러리 | 104 |  |

## 위키 공백 — 무엇이 새로 들어오나

개념 90개 중 **42개**는 위키에 관련 페이지가 아예 없다. 프로젝트 이름으로 세면, 이 책이 다루는
Apache 프로젝트 약 70개 가운데 전용 엔티티 페이지가 있는 것은 [[Apache Kafka]]·[[Apache Spark]]·
[[Apache Flink]]·[[Apache Hadoop]] **넷뿐**이다.

장별 빈 칸: Ch1 5/5 · Ch2 4/7 · Ch3 0/8 · Ch4 2/6 · Ch5 2/8 · Ch6 2/8 · **Ch7 7/10** ·
**Ch8 7/10** · Ch9 4/11 · Ch10 2/8 · **Ch11 7/9**. (Ch1은 책 자체의 프레임이라 성격이 다르고,
Ch3이 0인 것은 [[Apache Kafka]]와 [[Message broker]]가 이미 그 장을 덮기 때문이다.)

빈 칸이 몰린 곳이 이 위키의 실제 공백이다.

| 장 | 빈 칸이 몰린 이유 |
|---|---|
| **Ch8** SQL 실행 계층 | **7/10** — 위키에 **쿼리 엔진 계층이라는 개념 자체가 없다.** 저장(포맷·테이블)과 소비(BI)는 있는데 그 사이가 비었다 |
| **Ch7** 수집·오케스트레이션 | **7/10** (도구 7종 중 5종) — [[ETL and ELT]]·[[Change data capture]]는 원리만 있고 **구현체가 없다.** Airflow를 실제로 운영하면서 위키에 Airflow 페이지가 없다 |
| **Ch11** 특화 라이브러리 | **7/9** — TinkerPop·HugeGraph만 [[Graph database]]에 걸린다 |
| **Ch2** 기반 계층 | **4/7** (ZooKeeper·YARN·YuniKorn·BookKeeper) — [[Replication and consensus]]가 Raft를 원리로 다루는데 **그 원리의 구현체 이름을 모른다** |

이는 [[Wiki gap analysis - DE readiness]]의 진단("1차 자료·운영 도구·자기 측정치 세 축이 얇다")
중 **운영 도구** 축과 정확히 겹친다. 단 이 책 자체는 여전히 2차 자료이고 개념당 1페이지라, 공백의
**이름은 채워 주지만 깊이는 채워 주지 못한다.**

## 실제 스택에 걸리는 항목

[[Spatial omics platform roadmap]]의 스택(K8s · Airflow · MinIO · Postgres)과 직접 맞물리는 것들.
이 순서로 읽으면 이 책이 사전으로 쓰인다.

| 개념 | 왜 | PDF p |
|---|---|---|
| Apache Polaris | **Iceberg 중심 레이크 카탈로그.** 로드맵에서 카탈로그를 Postgres로 정정한 결정과 정면으로 맞물린다 | 91 |
| Apache Airflow / DolphinScheduler 비교 | 이미 Airflow를 운영 중 — 대안을 본 적이 없다 | 59–61 |
| Apache YuniKorn | **K8s 리소스 스케줄러.** GPU·대용량 잡을 K8s에서 돌릴 때의 선택지 | 15 |
| Apache Ozone · OpenDAL | MinIO 자리의 대안과 스토리지 추상 계층. [[Object storage layout]]의 후속 | 14 · 41 |
| Apache Sedona | **대용량 지리공간 처리.** 공간 오믹스의 좌표·폴리곤 연산과 같은 축 — [[SpatialData as a data engineering substrate]]에서 Shapes 집계를 분산 처리해야 할 때 | 98 |
| Apache Griffin | 데이터 품질 측정 프레임워크. [[Data SLA and observability]]의 구현체 | 89 |
| Apache Iceberg | Tier 1인데 위키는 아직 **Delta 로그 구조만** 안다 ([[Table formats]] 참조) | 45 |

## 인용

> 이현수(hyunsooIT). 『Apache로 읽는 데이터 기술의 지도 — 데이터 플랫폼을 구성하는 Apache
> 오픈소스 기술의 역할과 선택 기준』. hyunsooIT 데이터 시리즈, 2026. 11개 장 · 개념 90개 ·
> PDF 104p (A4 가로 슬라이드형). © 2026 이현수(hyunsooIT), 무단 전재·복제·재배포 금지.
> 저자 채널: LinkedIn · YouTube · Threads (책 안에서는 링크가 텍스트로만 표기되어 URL 미확인).

로컬 파일: `raw/data-engineering/apache/apache-book-full-spread.pdf` (121MB, 2026-08-19 반입).
`raw/`는 gitignore 대상이므로 각 source 페이지는 자체적으로 완결된 인용을 갖는다.

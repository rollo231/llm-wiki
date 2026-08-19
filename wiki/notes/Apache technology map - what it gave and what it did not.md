---
type: note
title: Apache technology map - what it gave and what it did not
area: [data-engineering]
aliases: [Apache 지도 총평, Apache 책 총평, Apache map verdict]
tags: [data-engineering, apache, book, review, meta]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache data technology map (book)]]"]
---

# Apache technology map - what it gave and what it did not

『Apache로 읽는 데이터 기술의 지도』(이현수, 2026) **완주 총평** — 11장 / 개념 90개 / PDF 104p,
2026-08-19 하루에 인제스트. 트래커: [[Apache data technology map (book)]].

이 노트는 **소스 요약이 아니라 이 위키에 무엇이 남았는지에 대한 회계**다.

## 한 줄

> ⭐⭐ **이 책은 깊이를 팔아 판단 축을 샀다.** 개념당 1페이지(≈500자)라 어느 하나도 구현할 수 없지만,
> **"무엇을 먼저 정할지"에 대해서는 이 위키의 어떤 소스보다 일관되다.**

## 회계 — 무엇이 남았나

**새 페이지 28장** — source 11 · **entity 11**(트래커 포함) · concept 5 · note 1(이 페이지).
**기존 위키 페이지 24곳 갱신** (+ `index.md` · `log.md`).

### 새로 생긴 계층 개념 5개

| | 무엇을 채웠나 |
|---|---|
| [[SQL execution layer]] | **저장과 소비 사이가 비어 있었다.** 3단계(테이블 규칙/실행/접속) + 엔진 유형 6종 |
| [[Consumption layer]] | **조회 형태가 축이다** — 검색/실시간집계/사전집계/키조회/시계열/인메모리 + 오차 다이얼 |
| [[Data orchestration]] | 오케스트레이션 개념 자체가 없었다. **축은 팀의 운영 방식** |
| [[Data integration tools]] | [[ETL and ELT]]에 원리만 있고 구현체가 없었다 |
| [[Cluster resource scheduling]] | **"누가 얼마나 쓸지"** — [[Data orchestration]]과 다른 층 |

### 새 엔티티 11개 (트래커 포함)

[[Apache data technology map (book)]](장 트래커) ·
**[[Apache Airflow]]**(실제 운영 중인데 페이지가 없었다) · [[Apache ZooKeeper]](Ratis 흡수) ·
[[Apache Calcite]] · [[Apache DataFusion]] · [[Apache Lucene]](Solr·OpenNLP 흡수) ·
[[Apache Cassandra]] · [[Apache HBase]] · [[Apache Polaris]](Gravitino 흡수) ·
[[Apache Superset]](Zeppelin 흡수) · **[[Apache Sedona]]**.

⭐ **흡수 원칙**: 지식의 단위가 *비교* 이거나 *한 축의 두 형태* 면 떼지 않는다 — Doris·NiFi·Beam·
Druid/Pinot·Hive Metastore가 그렇게 흡수됐고, Ratis·Solr·Gravitino·Zeppelin은 짝과 함께 한 페이지에 있다.

### 닫힌 열린 질문 셋

| 어디에 있던 질문 | 결과 |
|---|---|
| [[Columnar and in-memory data formats]] — *"ORC와 Parquet의 실제 비교가 없다"* | ✅ **완전 해소.** 축은 성능이 아니라 **생태계** |
| [[Table formats]] — *"세 포맷의 선택 기준이 비어 있다"* | ✅ **해소.** 3축(엔진 공유 / 잦은 변경 / 스트림-배치) |
| [[Table formats]] — *"Iceberg의 스냅샷·매니페스트 구조"* | ⚠️ **절반.** 이름·역할은 확인, **계층 구조는 여전히 1차 문서 필요** |
| [[GPU resource allocation]] — *"gang scheduling(Kueue·Volcano)"* | ⚠️ **인접 항목만** — YuniKorn. 동일 여부 미확인 |

### 종결된 판단 넷

- ❌ **Ozone 해당 없음** — MinIO가 이미 S3 호환. 책이 스스로 제외한다.
- ❌ **OpenDAL 해당 없음** — 저장소가 하나인 동안은 추상 계층의 값이 없다. **늘릴 때 재검토.**
- ✅ **Polaris는 로드맵을 확인해 준다** — [[Spatial omics platform roadmap]] §2.2의 Postgres 정정을
  뒤집지 않는다. *Iceberg 테이블이면 Polaris, 불투명 산출물이면 직접 만든다.*
- ❌ **Hive Metastore 엔티티 불필요** — Polaris가 계보를 확정했고 그 계보는
  [[Data catalog and semantic layer]] 3분류 표 안에 들어간다.

## ⭐⭐⭐ 이 책이 실제로 가르친 것 — 판단 축 네 개

개별 제품 지식이 아니라 **결정 순서**가 이 책의 산출물이다.

### 1. 성능 비교를 거부한다 (비교 절 7개 전부)

| 장 | 든 축 |
|---|---|
| Ch3 | *"기능 체크리스트보다 **운영 조직의 형태**를 먼저"* (Kafka vs Pulsar) |
| Ch4 | *"엔진 이름보다 먼저 **시간을 어떻게 자를지**"* |
| Ch5 | *"'무엇이 제일 좋은가'보다 **'지금 데이터가 어디를 지나는가'**"* |
| Ch6 | *"벤치마크 숫자보다 **팀의 기술 역량·이미 쓰는 엔진·변경 패턴**"* |
| Ch7 | *"도구 이름이 아니라 **운영 방식** — 누가 만들고 배포하나"* |
| Ch8 | *"'가장 빠른 엔진'보다 **주 부하가 무엇인지**"* |
| Ch9 | *"제품 이름을 비교하기 전에 **가장 자주 발생하는 조회**"* |

### 2. ⭐⭐ 먼저 합의할 숫자가 둘 있다

| 다이얼 | 어디서 | 효과 |
|---|---|---|
| **최대 허용 지연** | Ch4 | 배치 / 마이크로배치 / 스트림의 경계가 정해진다 |
| **허용 오차** | Ch11 | 근사 집계(스케치)를 쓸지가 정해진다 |

⭐ 둘 다 **"평균이 아니라"** 형태다. [[Wiki gap analysis - DE readiness]]가 이 위키의 반복 결함을
***"'재야 한다'는 있고 '이렇게 잰다'가 없다"*** 로 진단했는데, **이 두 항목이 정면 반례다.**

### 3. 처방은 항상 "문장으로 적어 고정하라" (5회)

Ch5(*교환은 Avro, 분석 저장은 Parquet, 기존 Hive는 ORC*) · Ch7(*수집은 NiFi, 동기화는 SeaTunnel,
일정은 Airflow*) · Ch9(*'상품명 검색'처럼 기능을 문장으로*) · Ch10(*목록은 ○○, 권한은 ○○, 품질은 ○○*) ·
Ch3(*소비 후 삭제인가 남겨 두고 재생인가*).

⭐ 그리고 Ch10이 한 걸음 더 간다 — **"제품 설치 순서보다 우리 팀에서 비어 있는 축이 어디인지 확인하라."**
**선택을 "제품 비교"가 아니라 "역할 문장 작성 + 자기 진단"으로 바꾼다.**

### 4. 결합을 풀면 그 자리에 선택 문제가 생긴다

| | 무엇을 떼어냈나 | 새로 생긴 문제 |
|---|---|---|
| **YARN** (Ch2) | 저장 ↔ 처리 엔진 | 엔진 선택 + 자원 배분 → [[Cluster resource scheduling]] |
| **테이블 포맷** (Ch6) | 저장 ↔ 쿼리 엔진 | 엔진 선택 → [[SQL execution layer]] |
| **Pulsar** (Ch3) | 브로커 ↔ 저장(BookKeeper) | 운영 컴포넌트 하나 추가 |
| **KRaft** (Ch2) | ↔ 반대 방향(외부 합의 → 내장) | 합의 장애가 제품 장애와 한 몸 |

⭐ **표준/이식 계층 5종**(TinkerPop·[[Apache Calcite]]·Beam·Arrow·OpenDAL)도 같은 형태다 —
*"엔진을 바꿔도 같은 것을 쓸 수 있는가"* 를 팔고, 대가로 **추상화 한 층**을 받는다.

## ⚠️ 이 책이 주지 않은 것

### 1. 구조 — 11장 연속

**내부 동작이 없다.** 확인된 것만: Iceberg 매니페스트 계층 · Kafka 로그 컴팩션·ISR·`acks` ·
Parquet row group·dictionary encoding · ZooKeeper ZAB·znode·watch · Ratis 로그 복제 ·
Airflow Executor·Scheduler·메타DB · Polaris 커밋 프로토콜 · Druid 세그먼트 · Pinot 색인 종류 ·
Cassandra quorum · Lucene 스코어링 공식 · Sedona 공간 인덱스 종류.

⭐⭐ **그리고 세 번은 위키가 소스보다 자세했다** — Ch6(Iceberg 스케치) · Ch3(Kafka) · Ch5(Parquet).
**2차 소스로 채울 수 있는 깊이의 한계가 이 지점이다.**

### 2. 운영 비용

*"~의 가치"* 는 말하고 *"~의 비용"* 은 말하지 않는다. Airflow의 스케줄러 지연·`catchup` 폭주 ·
테이블 포맷의 스냅샷 만료·고아 파일 정리·컴팩션 스케줄 · ZooKeeper 앙상블 운영 · 팬아웃 후의 사본
정합성. **Ch7이 "오케스트레이션의 가치"까지만 말하는 것이 대표적이다.**

### 3. 조직·규제

Ch7만 *"누가 만들고 배포하나"* 를 묻는다. Ch10의 거버넌스 삼각형에는 **담당자·정책 승인자가 없고
PII·규제 이름이 하나도 없다**(GDPR 등). "민감 태그"라는 추상만 있다.

### 4. ⚠️ Apache 렌즈 — 세 번 확인

| 장 | 재단 밖이라 빠진 것 |
|---|---|
| Ch6 | **Delta Lake** — 저자 소속이 Databricks인데도 명단에 없다 |
| Ch8 | **Trino/Presto** · Snowflake · BigQuery · Databricks SQL |
| Ch9 | **Elasticsearch · OpenSearch** |

⭐ **편향이 아니라 렌즈다.** 그래서 이 책의 "대표 3종"은 시장의 3종이 아니다.
👍 단 **Ch10은 스스로 보정한다** — Griffin 옆에 Great Expectations·dbt tests를 표에 넣는다.

### 5. ⚠️ Tier는 채택 연차의 함수다

**Ch9가 증거**: Tier 1 4개(Cassandra·HBase·Lucene·Solr)가 전부 성숙기·레거시 쪽이고 **가장 활발한
Druid·Pinot는 Tier 2**다. **Ch8은 Tier 1이 0개**인데 이유는 그 계층의 기본값이 재단 밖에 있어서다.

> **보정 규칙: Tier는 "오래 쓰인 정도"로 읽고 "지금 고를 것"으로 읽지 않는다.**

### 6. 벡터 검색

2026년 자료인데 Ch9의 검색 항목이 **역색인 렉시컬뿐**이다. 이 위키는 [[Vector database]]·
[[Hybrid search and reranking]]을 이미 갖고 있어 **빠진 줄이 어디인지 정확히 보인다.**

## 👍 신뢰 프로필 — 코스와 반대다

⭐⭐ **출처 없는 수치 0건. 11장 전부.** 유일한 수치는 Doris의 *"1초 미만~수 초를 목표로"*, Pinot의
*"밀리초~1초 미만"* 이고 둘 다 헤지되어 있다.

[[AI Data Engineering (Fast Campus course)]]와 정반대다 — 그 코스는 `80% 비정형`·`하둡보다 100배`·
`TCO 70~80% 절감` 같은 배지를 남발하면서 깊이는 있었다.

> **깊이는 얕지만 거짓은 없다.** 두 소스를 함께 쓰는 방법도 여기서 나온다 —
> **판단 축은 이 책에서, 원리는 코스에서, 구조는 1차 문서에서.**

그리고 8~10개 장에서 **모든 항목에 "~는 만능이 아니다" / "~을 대체하지 않는다" 줄이 붙는다.**
**무엇이 아닌지를 먼저 말하는 형식**이 90개 항목 전체에 일관된다.

## 다음에 무엇을 읽어야 하나

이 인제스트가 확인한 것은 **[[Wiki gap analysis - DE readiness]]의 1순위가 바뀌지 않았다**는 것이다.

1. ⭐ **Iceberg 스펙(1차 문서)** — 유일하게 절반만 해소된 항목. 알아야 할 것 셋은
   [[Table formats]] §Iceberg 문서가 필요한 이유에 그대로 남아 있다(매니페스트 입도 · 통계 항목 ·
   **스냅샷 만료와 고아 파일 정리**). **그때 [[Apache Polaris]]와 함께 Iceberg 엔티티를 승격한다.**
2. **Airflow 공식 문서** — 이 책은 *"무엇을 고를까"* 에 답하고 *"지금 겪는 문제"* 에는 답하지 않는다.
   실제 운영 중이므로 Executor·Scheduler 구조와 운영 난점이 필요하다.
3. **Trino 또는 DuckDB** — [[SQL execution layer]]의 실제 기본값이 재단 밖에 있다는 것이 확인됐다.
4. **Sedona 실측** — [[Apache Sedona]]의 4단계 경로가 미검증이다. [[Spatial aggregation]]의 issue #210
   제약이 실제 데이터에서 어느 규모부터 터지는지가 선행 질문이다.
5. **gang scheduling(Kueue·Volcano) vs YuniKorn** — [[Cluster resource scheduling]]에 남긴 미확인 항목.

⭐ 그리고 이 책 자체의 사용법은 저자가 두 번 말했다 —
Ch1 *"Tier 2는 필요한 순간에 **사전처럼** 펼쳐 보면 됩니다"*, Ch11 *"**모든 영역을 다 쓸 필요는
없습니다.** 해결하려는 문제에 필요한 기술만 고르면 됩니다."*
**이 위키에서 그 사전 역할은 [[Apache data technology map (book)]]의 개념 90개 목차 표가 한다.**

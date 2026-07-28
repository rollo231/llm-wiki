---
type: source
title: Data landscape guide for developers
area: [data-engineering]
aliases:
  - Guide to data tools landscape for developers
  - sinja.io data landscape guide
  - OlegWock data guide
  - 데이터 랜드스케이프 가이드
tags: [data-engineering, overview, tooling, glossary]
created: 2026-07-28
updated: 2026-07-28
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers", "raw/data-engineering/data-landscape-guide/guide--2026-07-14.md"]
---

# Data landscape guide for developers

**출처:** *Guide to data tools landscape for developers* — OlegWock, 개인 블로그
[sinja.io](https://sinja.io/blog/data-landscape-guide-for-developers), 2026-07-14 발행 (2026-07-28
접속). 저자는 소프트웨어 엔지니어로 Deepnote(클라우드 노트북)를 거쳐 현재 Metabase(BI)에서 일한다 —
**데이터 배경 없이 데이터 회사에 들어간 개발자**의 시점에서 쓴 글이라고 스스로 밝힌다. 로컬 스냅샷:
`raw/data-engineering/data-landscape-guide/` (gitignored).

데이터 팀에 던져진 개발자를 위한 **랜드스케이프 지도**. 툴 사용법이 아니라 *"이 단어가 파이프라인
어디에 앉는가"* 를 그린다. 저자가 명시적으로 범위를 좁힌다 — Metabase에서 대시보드 만드는 법,
통계 기초, Spark 클러스터 운영은 다루지 않고, 같은 부류 툴끼리의 심층 비교도 하지 않는다.
데이터 생애주기(어디서 오고 → 어떻게 처리되고 → 어디에 저장되고 → 어떻게 소비되는가)를 따라가며
각 툴이 어느 단계에 속하는지를 배치하는 것이 전부다.

**성격 주의:** 개인 블로그의 개괄 글이지 레퍼런스가 아니다. 툴 ~70개를 언급하지만 대부분 한 문장씩
스치고, 벤치마크·수치·1차 출처는 없다. 이 위키에서의 값어치는 **어휘와 배치**에 있다 — 개별 툴에
대한 주장의 근거로 인용하기에는 약하다.

## 요점

### 1. 저장 계층 — [[Analytical data storage tiers]]

웨어하우스 / 레이크 / 레이크하우스를 세 축으로 갈랐다: **구조를 강제하는가**, **쿼리 엔진과
결합되는가**, **얼마인가**. 특히 두 번째 축이 이 글의 기여다 — 웨어하우스는 저장과 쿼리 엔진을
함께 관리하며 강결합인데(MySQL·Mongo만 다뤄본 사람에게는 낯선 지점이라고 저자가 짚는다),
레이크와 레이크하우스는 그렇지 않다. 그래서 **레이크하우스와 웨어하우스는 비용을 1:1로 비교할
수 없다** — 레이크하우스 + 별도 컴퓨트가 워크로드에 따라 훨씬 싸질 수 있다.

레이크는 "그냥 큰 클라우드 폴더 + α"이고, 그 α가 **메타데이터 카탈로그 + 쿼리 엔진**이다.
관리 안 하면 **data swamp**가 된다.

### 2. 테이블 포맷 — [[Table formats]]

레이크하우스를 레이크와 가르는 핵심 블록. **쿼리 엔진과 raw 파일 사이에 앉아 저장을 관리하는 층**
으로 정의하고, ACID·스키마 진화/버저닝·인덱스/파티셔닝 최적화·time travel을 전부 이 층의 기능으로
귀속시킨다. Iceberg / Delta Lake / Hudi.

→ 이 위키에서 [[Data Engineering]] MOC가 "가장 약한 발판"이라고 적어둔 자리를 메운다.

### 3. "카탈로그"는 세 가지 다른 물건이다 — [[Data catalog and semantic layer]]

이 글에서 가장 실용적인 구분:

- **metastore(메타데이터 카탈로그)** — *기계용*. 쿼리 엔진이 파일을 찾도록 테이블명·스키마·파일
  매핑을 담는다.
- **data catalog** — *사람용*. 문서에 가깝다. 출처·소유자·접근 정책 같은 비즈니스 맥락.
- **semantic layer** — *정의용*. "revenue에 환불이 포함되는가", "EMEA는 어느 마켓들인가"를
  한 곳에 못박고 BI·AI 에이전트가 그걸 읽어 쿼리를 만든다.

Unity Catalog가 세 역할을 다 걸쳐서 이름이 헷갈리는 것이지, 개념은 별개다.

### 4. 오케스트레이터는 배치 전용이라는 주장 — [[Batch and stream processing]]

> "orchestrators are a batch processing thing. They run a pipeline from start to finish and then
> stop until the next trigger, which doesn't really map onto stream processing where the pipeline
> is meant to run continuously and never 'finish'."

시작→끝→정지 모델이 끝나지 않는 파이프라인에 안 맞으므로, 스트리밍 셋업에서는 오케스트레이터가
아니라 스트림 프로세서(Flink 등)가 그 역할을 한다. **경계를 긋는 주장이지 툴 선택 기준은 아니다** —
Airflow·Dagster·Prefect·Luigi를 나열만 하고 비교는 없다.

Kafka에 대해서도 유용한 선긋기가 하나 있다. **이벤트 스트리밍 플랫폼 ≠ 메시지 큐**: consumer가
ack해도 이벤트가 사라지지 않고 로그에 남아 retention까지 몇 번이고 다시 읽힌다. 그리고 Kafka
자체는 아무 처리도 하지 않는다.

### 5. Parquet은 스캔, Arrow는 처리 — [[Columnar and in-memory data formats]]

둘 다 분석 워크로드용 컬럼너지만 최적화 대상이 다르다. **Parquet = 파일 포맷**, 압축·전송·
**스캔**(디스크→메모리) 최적화. **Arrow = 인메모리 포맷**, 자리를 더 먹는 대신 zero-copy 전송과
CPU/GPU 캐시 효율, 즉 **처리** 최적화. Arrow는 소스에서 받는 포맷이 아니라 **이미 로드된 데이터를
툴 사이에서 주고받는** 포맷이다(pandas → Rust DataFusion). Avro도 나오는데, 바이너리지만
**행 지향**이라 레코드 전달과 스트리밍 쪽이다.

### 6. 착지 지점 — [[Medallion architecture]] / [[Dimensional modeling]]

두 개념이 **직교한다**는 배치가 좋다: 메달리온(bronze/silver/gold)은 *얼마나 정제됐는가*를 말하고
모양에 대해서는 아무 말도 하지 않는다. 모양은 차원 모델링(fact/dimension·star·grain·data mart)이
담당한다. 다만 저자는 곧바로 반론을 단다 — 현대 웨어하우스가 빠르고 스토리지가 싸서 그냥 넓은
비정규화 테이블("one big table")을 쓰는 팀도 많다.

### 7. 그 밖에 (별도 페이지 없이 여기 요약)

- **인제스천 툴** — Fivetran / Airbyte / dlt. 커넥터로 소스·목적지를 잇고 auth·페이지네이션·
  에러 처리 같은 반복 글루 코드를 없앤다. 다만 **이 방식은 ELT 쪽으로 민다** — 추출된 데이터가
  처리되기 전에 일단 어딘가 착지해야 하므로. DB 소스에는 **CDC**(replication log를 읽어 insert·
  update·delete를 잡아냄)가 쓰이고, 독립 블록으로는 Debezium.
- **SQL 변환** — dbt / SQLMesh. 변환을 `select` 문으로 기술하면 툴이 컴파일해 **쿼리 엔진에게**
  실행시킨다 — dbt·SQLMesh는 데이터를 직접 만지지 않는다. `ref()`로 테이블명 하드코딩 대신 모델을
  참조하면 의존성 그래프를 만들어 순서를 잡아준다.
- **로컬 데이터프레임** — pandas(eager, RAM 제한) vs Polars `LazyFrame`·DataFusion(lazy). lazy는
  연산이 즉시 실행되지 않고 **논리 계획**으로 쌓였다가 `.collect()` 때 최적화 후 실행된다.
  **DuckDB**는 데이터프레임 라이브러리가 아니라 in-process OLAP DB("분석용 SQLite")인데 같은
  자리를 차지한다 — 인프라 없이 로컬에서 CSV·Parquet·pandas DataFrame을 SQL로 조회.
- **분산 처리** — Hadoop(레거시) → **Spark**(사실상 표준). Dask는 pandas/numpy API에 붙어 클러스터로
  확장, Ray는 더 범용(ML 학습에 인기), Flink는 배치도 되지만 특기는 스트리밍.
- **관측성** — 두 갈래다. **파이프라인 모니터링**(돌았나·실패했나·얼마 걸렸나)은 평범한 웹앱 스택
  (Prometheus·Grafana·ELK)이면 되고 오케스트레이터가 일부 커버한다. **데이터 품질 모니터링**은
  별개 — 최신인가·볼륨 이상은 없나·스키마가 조용히 바뀌지 않았나. 수동 정의(Great Expectations,
  dbt tests) vs 자동 학습 후 이상 탐지(Monte Carlo, Bigeye, Metaplane).
- **앱에 서빙** — 웨어하우스 gold 테이블은 내부 대시보드엔 충분하지만, 다수 사용자에게 밀리초로
  응답해야 하면 **실시간 OLAP DB**(Druid·Pinot·ClickHouse)로 옮긴다.
- **reverse ETL** — 웨어하우스 → 운영 도구(HubSpot·Zendesk). 이걸로 실현하는 유스케이스가
  **operational analytics**: 경영진 보고서가 아니라 영업·CS가 *일상 업무 중에* 쓰는 데이터.
  툴: Hightouch, RudderStack, Airbyte Data activation, Fivetran Activations.
- **data lineage** — 카탈로그가 "무엇이 있나"면 lineage는 "어떻게 변환됐나". 오케스트레이터 DAG·
  SQL 파싱·워커가 뱉는 이벤트에서 자동 수집. table-level vs column-level. 용도는 다운스트림 영향
  평가·근본 원인 분석·컴플라이언스(PII 추적). **OpenLineage**가 신흥 표준.
- **소비 형태** — 대시보드/BI(self-service가 핵심 셀링 포인트), operational analytics, ad-hoc·
  탐색적 분석(노트북 — Jupyter·Colab·Deepnote·marimo), ML(feature store 등 자체 생태계),
  embedded analytics(Sisense·Luzmo; 앱이 authn/authz, 툴이 쿼리·렌더), **data as a product**
  (Bloomberg Terminal형 — 데이터 자체를 판다).
- **데이터 거버넌스** — 저자 스스로 "기술과 가장 관련이 적은 섹션"이라 부른다. 누가 접근하나·
  누가 접근했나·소유자는 누구인가·잊힐 권리·물리적 저장 위치·보관 기간. 웨어하우스 RBAC,
  카탈로그의 소유자 정보, lineage의 PII 추적이 거들지만 **본질은 사람과 프로세스**이고 법무·
  컴플라이언스·보안 팀에 가깝다.

### 4직군 분류 — 기존 위키와 축이 다르다

이 글은 데이터 직군을 **공존하는 네 유형**으로 나눈다:

| 유형 | 대표 직함 | 도구 | 예시 업무 |
|---|---|---|---|
| **analytical** | data analyst, BI analyst | SQL, 스프레드시트, Tableau | 지역별 이탈률 계산 → 대시보드 → 마케팅에 제안 |
| **scientific** | data scientist | Python(pandas·scikit-learn), 노트북 | 이탈 상관 요인 탐색 → 예측 모델 → A/B 테스트 설계 |
| **engineering** | data engineer | Python, Spark, DB·웨어하우스, 클라우드 | 다중 소스 인제스천 유지·스키마 표준화·쿼리 최적화·품질 체크 |
| **machine learning** | (ML scientist / ML engineer 통칭) | 별도 스택 | 추천 모델 학습 → API 뒤에 배포 → 모니터링·재학습 |

저자는 경계가 특히 소규모 팀에서 흐릿하다고 단서를 달고, ML 유형에 대해서는 **자기 지식이 제한적**
이라고 밝힌다(그래서 본문에서 ML을 다루지 않는다).

**[[AI DE Course - Ch1-1 OT]]와 충돌하는 것은 결론이 아니라 축이다.** 강의는 *시간축* 으로 본다 —
[[Traditional data engineering]]이 [[AI data engineering]]으로 **진화한다**. 이 글은 *공존축* 으로
본다 — engineering type과 ML type이 **도구셋이 달라서 갈라지는 별개 직군**이다. 같은 현상을 놓고
"하나의 직무가 변한다" vs "네 직무가 동시에 있다"로 프레이밍이 갈린다. 어느 쪽이 현업의 실제
모습인지는 [[Data Engineering]] MOC의 열린 질문으로 남아 있고, 이 소스도 답을 주지는 않는다
(둘 다 1차 근거 없는 개괄이다).

## 시의성 주의

2026-07-14 발행이라 지금은 매우 신선하지만, 랜드스케이프 글은 조용히 낡는다. 이 판본이 기록한
움직이는 사실들:

- **SparkR이 최근 deprecated** 되었다고 서술.
- **Census가 Fivetran에 인수**되어 **Fivetran Activations**로 개명.
- **BigLake → "Google's Lakehouse for Apache Iceberg"** 로 개명.
- **Looker Studio**가 최근 Google에 의해 다시 **Data Studio**로 개명되었다고 각주에 서술
  (LookML을 쓰지 않는 별개 제품이라는 점도 함께).
- Polars에 대해 "채택률이 pandas에 한참 못 미친다"고 평가 — 시간에 민감한 판단.

## 링크

- 개념: [[Analytical data storage tiers]], [[Table formats]], [[ETL and ELT]],
  [[Medallion architecture]], [[Dimensional modeling]],
  [[Columnar and in-memory data formats]], [[Batch and stream processing]],
  [[Data catalog and semantic layer]]
- 직군 축 대조: [[Traditional data engineering]], [[AI data engineering]],
  [[AI DE Course - Ch1-1 OT]]
- 적용: [[SpatialData as a data engineering substrate]] — 이 노트가 전제로 깔고 쓰던
  메달리온·Iceberg·카탈로그 어휘의 근거가 이제 위키 안에 생겼다.
- MOC: [[Data Engineering]]

---
type: concept
title: Columnar and in-memory data formats
area: [data-engineering]
aliases:
  - Apache Parquet
  - Parquet
  - Apache Arrow
  - Arrow
  - Apache Avro
  - Apache ORC
  - Columnar format
  - 컬럼너 포맷
  - 컬럼 지향 포맷
  - 인메모리 포맷
  - Predicate pushdown
  - Schema evolution
  - Schema Registry
  - 스키마 진화
  - ORC
  - Apache Arrow Flight SQL
  - Arrow Flight SQL
  - Apache OpenDAL
  - OpenDAL
  - Apache CarbonData
  - CarbonData
tags: [data-engineering, data-format, parquet, arrow, avro, columnar, storage]
created: 2026-07-28
updated: 2026-08-19
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers", "[[AI DE Course - Ch2-4,5,6 Parquet and Avro]]"]
---

# Columnar and in-memory data formats

데이터가 담기는 바이트 수준의 포맷. **파일 포맷**(디스크·전송)과 **메모리 포맷**(처리) 두 갈래이고,
둘을 가르는 축이 이 페이지의 핵심이다.

## 파일 포맷

| 포맷 | 방향 | 쓰임 |
|---|---|---|
| **CSV** (·Excel) | 행 | 소량 전송. 아무 오피스 소프트웨어로나 열린다 — 비기술 사용자와 주고받는 포맷. 영업팀이 분기 딜 분석해달라며 보내는 그것. |
| **Apache Parquet** | **열** | 기술 사용자의 기본값. 압축률이 좋고 대용량 저장·전송에 적합. 대부분의 데이터 툴이 읽고 쓴다 — **데이터 툴링의 링구아 프랑카**. |
| **Apache ORC** | 열 | **Hive·Hadoop 생태계에서 자란** 컬럼형. 아래 §ORC vs Parquet |
| **Apache Avro** | **행** | 바이너리지만 행 지향. **레코드를 주고받는 용도**, 특히 스트림 처리에서. |

> 컬럼너란 데이터가 행 단위가 아니라 **열 단위로 배치**된다는 뜻이고, 그래서 압축이 잘 되고
> 필요한 열만 읽을 수 있다.

## 왜 열이 압축되나 — 엔트로피

행 지향은 한 행에 숫자·문자·날짜가 섞여 있어 **엔트로피가 높고** 압축률이 낮다(대략 1:3).
열 지향은 같은 타입이 연속되어 **엔트로피가 낮고** 압축률이 높다(1:10 이상). 강의 기준
CSV 100GB → Parquet 10GB 이하.

Parquet이 쓰는 인코딩 두 가지:

- **RLE (Run-Length Encoding)** — `Male, Male, Male…(100,000번)` → `"Male" × 100,000`
- **Dictionary Encoding** — 고유 값을 숫자로 매핑

## Predicate Pushdown — Parquet이 스캔을 건너뛰는 법

**Parquet 파일은 각 데이터 블록마다 통계(최소값·최대값·Null 개수)를 요약한 Header/Footer 메타데이터를
내장한다.** 처리 엔진은 실제 데이터를 읽기 전에 메타데이터를 먼저 확인하고, 조건에 맞지 않는 블록은
**디스크 레벨에서 통째로 건너뛴다.**

> `SELECT * WHERE age < 30` 을 실행할 때 메타데이터상 `Min Age: 30` 인 블록은 열어볼 필요조차 없다.

이것이 컬럼 프루닝(필요한 열만 읽기)과 **다른 축**이라는 점이 중요하다 — 프루닝은 *열*을 줄이고,
푸시다운은 *행 블록*을 줄인다. 둘이 곱해져서 I/O가 줄어든다.

AI 학습에서 이게 중요한 이유: 학습 워크로드는 **대용량 반복 읽기 + 특정 피처만 추출**이라는 '편식'
패턴이고, 행 기반이면 필요한 10%를 얻기 위해 100%를 읽어 **GPU가 데이터를 기다리며 idle**에 빠진다.

## Avro — 왜 스트리밍용인가

랜드스케이프 가이드는 "레코드를 주고받는 용도, 특히 스트림 처리에서"라고만 했다. 이유는 둘이다.

**1. Parquet의 구조적 한계**

- **쓰기 지연** — 컬럼 단위로 분해·압축하는 과정에 높은 CPU 연산이 든다. 폭포수처럼 쏟아지는
  데이터를 실시간으로 받아내기엔 느리다.
- **Small Files 문제** — 실시간으로 쓰면 작은 파일이 무수히 생기고, 수천 개의 작은 파일은
  **추후 읽기 성능을 급격히 저하시킨다** → 이걸 푸는 것이 [[Table formats]]의 compaction이다.

**2. Avro의 구조 — self-describing**

```
Log_20260304.avro
├─ File Header (Metadata)   "schema": { ...JSON... }, codec: snappy
└─ Data Block (Binary)      Row 1: 010110…  Row 2: 110010…
```

데이터와 스키마가 한 파일에 공존해서 **헤더만 읽으면 구조를 파악할 수 있다.** 스키마는 사람이 읽는
JSON(`.avsc`)으로 정의하고, 데이터는 행 단위 append(쓰기 지연 최소화) + 이진 직렬화(JSON 대비 1/10).

### 스키마 진화 — Avro의 진짜 무기

| 모드 | 의미 | 유리한 경우 |
|---|---|---|
| **BACKWARD** | 새 스키마로 이전 데이터를 읽을 수 있음 | 필드 **삭제** 시 |
| **FORWARD** | 이전 스키마로 새 데이터를 읽을 수 있음 | 필드 **추가** 시 |
| **FULL** | 양방향 호환. 이상적이나 조건이 까다롭다 (default 필수) | — |

- **안전한 변경** — 필드 추가(**default 값 필수**), default가 있던 필드 삭제,
  타입 확대(int→long, float→double)
- **위험한 변경** — 필드 이름 변경(alias 없이), default 없는 필드 추가,
  타입 축소(long→int, 데이터 손실)
- **운영 장치는 Schema Registry** — 버전을 저장소에서 관리하고 Kafka에는 `Avro Binary + Schema ID`만
  흘린다. 컨슈머가 ID로 스키마를 조회한다. → [[Change data capture]]에서 스키마 변경으로 파이프라인이
  죽는 것을 막는 장치가 바로 이것

## ✅ ORC vs Parquet — 이 페이지의 오래된 공백

**둘 다 컬럼형이고 같은 문제를 푼다. 갈리는 것은 성능이 아니라 생태계다.**

| | 출발점 | 잘 맞는 곳 |
|---|---|---|
| **Parquet** | 여러 엔진이 공유하는 **범용 표준** | 다중 엔진 레이크·레이크하우스. Spark·Hive·DuckDB·Trino가 기본 지원 |
| **ORC** | *"Hive 테이블을 더 빠르고 작게"* | 온프레미스 Hadoop, **Hive Metastore 기반 웨어하우스**. 인덱싱·통계·압축을 파일 안에 적극적으로 넣는다 |

⭐ ORC의 전형적 환경은 **파티션된 Hive 테이블의 실제 파일이 ORC로 쌓여 있는 것**이고, 질의 엔진이
파일 통계를 보고 불필요한 **행 그룹을 건너뛴다**(위 §Predicate Pushdown과 같은 메커니즘).

⚠️ **신규 프로젝트는 Parquet 쪽이다** — 클라우드 레이크하우스와 다중 엔진 환경이 늘면서.
*"이미 ORC로 운영 중인 Hive 웨어하우스가 크다면 ORC를 유지하거나, 신규 경로부터 Parquet으로 옮긴다."*

### ⭐ 세 포맷을 한 문장으로 고정한다

> **"교환은 Avro, 분석 저장은 Parquet, 기존 Hive는 ORC."**

*"'무엇이 제일 좋은가'보다 **'지금 데이터가 어디를 지나는가'**를 먼저 묻는 편이 선택에 도움이 된다.
세 포맷을 한 파이프라인에 동시에 활용할 수도 있다. 다만 **단계마다 왜 그 포맷을 쓰는지가 분명해야
한다.**"* → 아래 §갈아타는 문제

## 파일 포맷 위·아래의 세 계층

포맷 이야기에 자주 섞여 들어오지만 **계층이 다른** 것 셋이다.

| | 무엇을 정하나 | 계층 |
|---|---|---|
| **Arrow Flight SQL** | **질의는 SQL로 받고 결과는 Arrow 배치로 보낸다** | 파일·메모리 위의 **수송 프로토콜** |
| **Apache OpenDAL** | *"파일을 어떻게 저장할까"가 아니라 **"파일을 어디에서 읽고 쓸까"*** | 포맷·테이블 **아래**의 접근 계층 |
| **Apache CarbonData** | 인덱싱·세부 메타데이터를 **파일 안에** 더 넣는다 | 같은 파일 포맷 계층의 **특화 포맷** |

- **Arrow Flight SQL** — 전통적인 행 단위 프로토콜이 대량 결과에서 병목이 되는 문제를 푼다.
  **JDBC/ODBC의 대안**이고, **서버가 이미 Arrow로 연산 중이면 결과를 다른 포맷으로 바꾸지 않고 그대로
  흘려보낸다.** [[Apache DataFusion]]·일부 웨어하우스가 이 경로를 지원한다.
  → [[SQL execution layer]] 3단계의 3️⃣ 접속·소비
- **OpenDAL** — 로컬 디스크·HDFS·S3 호환·Azure·GCS를 **하나의 API로**. 읽기·쓰기·목록 조회를 늘 같은
  인터페이스로 호출하고 **설정만 바꿔 실제 저장소를 지정한다.** 클라우드를 옮기거나 여러 클라우드를
  함께 쓸 때 파이프라인 코드를 크게 고치지 않는다. → [[Object storage layout]]
- **CarbonData** — 대용량 팩트 테이블에 **다양한 필터가 걸리고 응답 시간이 중요할 때.**
  ⚠️ *"신규 레이크하우스의 기본값으로 고르는 팀은 Parquet·Iceberg 조합보다 적다"* — 생태계가 넓은
  Parquet이 유리한 경우가 많다. ⭐ 요점은 **컬럼형에도 범용 표준과 특화 포맷이 나뉜다**는 것.

## 고르는 문제가 아니라 갈아타는 문제 — Compaction 패턴

| | **Avro** (행) | **Parquet** (열) |
|---|---|---|
| 강점 | 압도적 쓰기 속도(append), 스키마 진화 | 극한의 압축률·조회 성능, predicate pushdown |
| Best For | Kafka · Landing Zone · Streaming | Data Lake Analytics · [[Feature store]] · AI Training |

> **유입 시점엔 작은 Avro 파일들로 빠르게 저장하고, 새벽 배치에 큰 Parquet 파일 하나로 묶어 변환한다.**

```
Ingestion (Real-time)   →   Processing (Batch)      →   AI Training
Kafka + Avro                ETL & Compaction            Parquet
· Schema Registry 검증       · 작은 파일 병합              · 컬럼 기반 고속 조회
· 초고속 순차 쓰기            · 정제·조인                  · Predicate Pushdown
· 원본(Raw) 보존             · 파티셔닝(날짜/시간)          · GPU 메모리 최적화
```

이 흐름은 [[Medallion architecture]]의 bronze→silver→gold와 나란히 놓고 볼 만하다 —
**정제도의 축과 포맷의 축이 같은 방향으로 움직인다.**

## 메모리 포맷 — Apache Arrow

가장 널리 쓰이는 인메모리 포맷이자 **사실상의 표준**.

**Parquet과 Arrow의 대비가 이 페이지에서 가장 실용적인 지점이다.** 둘 다 분석 워크로드용 컬럼너인데
최적화 대상이 다르다:

- **Parquet = 스캔 최적화.** 압축과 파일 크기(저장·전송)에 맞춰져 있고, 관련 항목을 메모리로
  **올리는** 일을 잘한다.
- **Arrow = 처리 최적화.** 자리를 더 먹는 대신 zero-copy 전송이 되고, CPU/GPU 명령과 캐시를
  효율적으로 쓰도록 배치되어 있어 **계산 자체**를 잘한다.

그래서 Arrow는 **소스에서 받는 포맷이 아니다.** 이미 로드된 데이터를 툴 사이에서 옮길 때 쓴다 —
Python의 pandas에서 Rust의 DataFusion으로 넘기는 식. pandas는 Arrow를 선택적 백엔드로 쓸 수 있고,
**Polars**·**DataFusion**은 처음부터 Arrow 위에 지어졌다.

## ⭐ GPU 시대에 컬럼너가 다시 중요해지는 이유 — Coalescing

위에서 Arrow의 이점을 "CPU/GPU 명령과 캐시를 효율적으로"라고 적었는데, **GPU 쪽에는 하드웨어
수준의 구체적 이유가 있다** (Part 4 Ch4).

> ⭐ **"메모리 접근 병합(Coalescing): 데이터가 메모리상에 흩어져 있으면(Random Access) GPU는 이를
> 가져오느라 시간을 낭비한다. 컬럼 기반(Columnar) 포맷인 Parquet, Arrow가 GPU와 어울리는 이유가
> 바로 연속된 메모리 접근이 가능하기 때문이다."**

GPU는 수천 개 코어가 **같은 명령으로 서로 다른 데이터**를 처리한다(SIMT). 인접한 스레드가 인접한
주소를 읽으면 메모리 트랜잭션 하나로 묶이지만, 흩어져 있으면 트랜잭션이 그만큼 늘어난다.
**컬럼 하나가 메모리에 연속 배치되는 것이 곧 coalescing 조건이다.**

**그래서:**

- [[NVIDIA RAPIDS]]의 **cuDF가 Arrow 기반**이다 — 직렬화 없이 GPU↔CPU 전송
- Spark RAPIDS의 가속 가능 영역이 **"Parquet / ORC 기반 처리"** 로 명시된다
- 반대로 **row 단위 복잡 로직과 Python UDF는 GPU에서 느리다** (warp divergence)

⚠️ **다만 GPU ETL에서는 small file problem이 더 치명적이다** — 위 § Compaction 패턴 참조.
RAPIDS 판단 질문 중 하나가 **"작은 파일이 너무 많지는 않은가? 수 GB 단위의 큰 입력 파일이 유리"**
다. → [[GPU architecture]]

## 링크

- 혼동 주의: **파일 포맷 ≠ 테이블 포맷.** Parquet은 파일 하나의 레이아웃이고, Iceberg 같은
  테이블 포맷은 *여러 Parquet 파일을 하나의 테이블로 묶는 규약*이다 → [[Table formats]]
- 어디에 놓이나: [[Analytical data storage tiers]]
- Avro가 왜 스트리밍인가: [[Batch and stream processing]], [[Apache Kafka]]
- Schema Registry가 실제로 막는 사고: [[Change data capture]]
- small files 문제를 푸는 층: [[Table formats]] — compaction·Z-Ordering
- 인접: [[SpatialData as a data engineering substrate]] — 공간 오믹스에서 Zarr(청크 배열)와
  GeoParquet이 같은 자리를 차지한다. 래스터는 Parquet의 표 모델에 안 맞아 Zarr가 쓰인다는 것이
  그 노트의 출발점.
- ✅ **해소(2026-08-19):** ORC와 Parquet의 비교 → 위 §ORC vs Parquet.
  갈리는 축은 성능이 아니라 **생태계**(범용 다중 엔진 vs Hive·Hadoop 최적화)였다.
  → [[Apache Map - Ch5 Formats and exchange layer]]
- 출처: [[Data landscape guide for developers]], [[AI DE Course - Ch2-4,5,6 Parquet and Avro]]

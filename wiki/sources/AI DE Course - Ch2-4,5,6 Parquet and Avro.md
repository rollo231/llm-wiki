---
type: source
title: AI DE Course - Ch2-4,5,6 Parquet and Avro
area: [data-engineering]
aliases: [CH02-4 5 6 Parquet Avro, AI를 위한 데이터 구조, Columnar Storage의 원리]
tags: [data-engineering, course, fast-campus, parquet, avro, columnar, schema-evolution]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part1/06. CH02-4. AI를 위한 데이터 구조- Parquet, Avro 및 Columnar Storage의 원리1.pdf", "raw/data-engineering/ai-de-course/part1/07. CH02-5. AI를 위한 데이터 구조- Parquet, Avro 및 Columnar Storage의 원리 2.pdf", "raw/data-engineering/ai-de-course/part1/08. CH02-6. AI를 위한 데이터 구조- Parquet, Avro 및 Columnar Storage의 원리 3.pdf"]
---

# AI DE Course - Ch2-4,5,6 Parquet and Avro

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 CH02-4 / CH02-5 / CH02-6**
"AI를 위한 데이터 구조: Parquet, Avro 및 Columnar Storage의 원리 (1)(2)(3)".
덱 안의 제목은 "AI 시대, 데이터 저장 방식이 바뀌어야 하는 이유". 원본(로컬):
`raw/data-engineering/ai-de-course/part1/` 의 `06.` (7p) + `07.` (7p) + `08.` (8p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

**Part 1에서 가장 밀도 높은 덱 중 하나다.** [[Columnar and in-memory data formats]]가 랜드스케이프
가이드에서 "Parquet은 열, Avro는 행"까지만 얻었던 자리를 **왜 그런지**로 채운다.

## (1) AI 워크로드가 왜 다른가

AI 학습이 일반 데이터 처리와 다른 세 가지 소비 패턴:

| 패턴 | 내용 |
|---|---|
| **대용량 읽기** (Heavy Read) | 쓰기보다 수십 TB~PB를 메모리로 **반복** 불러오는 읽기가 압도적 |
| **선택적 열 접근** (Feature Extraction) | 수백 개 속성 중 학습에 필요한 특정 피처(열)만 추출하는 **'편식' 성향** |
| **목적 적합 I/O** (High Throughput) | 랜덤 접근보다 **순차 대량 읽기**에 최적화. **GPU가 쉬지 않도록** 대역폭 극대화 |

**행 기반의 한계 — "사과만 먹고 싶은데 과일 바구니를 통째로 사야 한다."**
`SELECT Age FROM Users`에서 필요한 데이터는 10%인데 100%를 읽는다. 디스크는 헛심을 쓰고
**GPU는 데이터가 도착할 때까지 idle 상태**에 빠진다.

**열 기반의 세 가지 이득:**

- **컬럼 단위 저장** — 불필요한 열은 아예 읽지 않아 I/O 낭비가 0에 가깝다
- **고효율 압축** — 숫자는 숫자끼리, 문자는 문자끼리 모여 패턴이 유사
- **벡터화 실행** — 한 건씩 처리하는 대신 컬럼 통째로 CPU 캐시에 올려 배열 연산

## (2) Parquet의 내부 — 마법의 정체

### 압축·인코딩

- 하둡 생태계에서 시작된 오픈소스 컬럼너 포맷.
- **CSV 100GB → Parquet 10GB 이하** (강의 제시: 압축률 10배).
- 원리는 두 인코딩:
  - **RLE (Run-Length Encoding)** — `Male, Male, Male…(100,000번)` → `"Male" × 100,000`
  - **Dictionary Encoding** — 고유 값을 숫자로 매핑

### Predicate Pushdown — 이 덱의 핵심 기여

**Parquet 파일은 각 데이터 블록마다 통계 정보(최소값·최대값·Null 개수)를 요약한 Header/Footer
메타데이터를 내장한다.**

처리 엔진은 실제 데이터를 읽기 전에 메타데이터를 먼저 확인하고, 조건에 맞지 않는 블록은
**디스크 레벨에서 통째로 건너뛴다.**

> 예: `SELECT * WHERE age < 30` 을 실행할 때, 메타데이터상 `Min Age: 30` 인 블록은 열어볼 필요조차
> 없다. 메모리로 올리는 낭비가 사라진다.

효과: 물리적 I/O를 획기적으로 줄여 대용량 조회 속도를 수십 배 향상.

### ML/DL 생태계와의 시너지

- **Spark** — Parquet의 파티셔닝 구조를 인식해 작업 노드에 데이터를 효율 분배
- **Pandas** — 필요한 컬럼만 읽는 **Column Pruning**으로 DataFrame 메모리 최소화
- **Arrow** — Parquet 호환 인메모리 포맷. 직렬화/역직렬화 오버헤드 없는 **zero-copy** 전송
- **벡터화 연산** — 컬럼 단위 배치 처리로 CPU throughput 향상

## (3) Avro — Parquet이 못하는 것

### Parquet의 구조적 한계

- **쓰기 지연** — 컬럼 단위로 분해·압축하는 과정에 높은 CPU 연산.
  "폭포수처럼 쏟아지는 데이터를 실시간으로 받아내기엔 처리 속도가 따라가지 못한다."
- **Small Files 문제** — 실시간 저장 시 작은 파일이 무수히 생성되고, 수천 개의 작은 파일은
  **추후 읽기 성능을 급격히 저하시킨다.**

실시간 처리가 요구하는 세 조건: 고속 순차 쓰기(append only) · 유연한 스키마 대응 ·
효율적 이진 직렬화. → **답이 Apache Avro.**

### Avro 파일 구조

**데이터와 스키마가 한 파일에 공존하는 self-describing 구조.**

```
Log_20260304.avro
├─ File Header (Metadata)   "schema": { ...JSON... }, codec: snappy
└─ Data Block (Binary)      Row 1: 010110…  Row 2: 110010…  Row 3: …
```

- **헤더만 읽으면 데이터 구조를 파악할 수 있다.**
- 스키마는 사람이 읽을 수 있는 **JSON**(`.avsc`)으로 정의.
- **행 기반 쓰기** — 발생 즉시 레코드 단위 append로 쓰기 지연 최소화.
- **이진 직렬화** — JSON 대비 1/10 크기.

### 스키마 진화 — Avro의 진짜 무기

호환성 규칙 3종:

| 모드 | 의미 | 유리한 경우 |
|---|---|---|
| **BACKWARD** | 새 스키마로 이전 데이터를 읽을 수 있음 | 필드 **삭제** 시 |
| **FORWARD** | 이전 스키마로 새 데이터를 읽을 수 있음 | 필드 **추가** 시 |
| **FULL** | 양방향 모두 호환. 가장 이상적이나 조건이 까다롭다 (default 필수) | — |

**Safe Changes** — 필드 추가(단, **default 값 필수**) · 필드 삭제(default가 있던 필드) ·
타입 확대(int→long, float→double)
**Risky Changes** — 필드 이름 변경(alias 없이) · default 없는 필드 추가 ·
타입 축소(long→int, 데이터 손실)

**운영 전략은 Schema Registry** — Ver 1, Ver 2… 를 저장소에 두고, Kafka에는
`Avro Binary + Schema ID`만 흘리고 컨슈머가 ID로 스키마를 조회한다.
→ [[Change data capture]]에서 같은 장치가 스키마 변경 대응에 쓰인다.

## Avro vs Parquet 선택 기준

| | **Apache Avro** (행) | **Apache Parquet** (열) |
|---|---|---|
| 강점 | 압도적인 쓰기 속도 (append) | 극한의 압축률 & 조회 성능 |
| 두 번째 강점 | 강력한 스키마 진화 | Predicate Pushdown |
| Best For | **Kafka · Landing Zone · Streaming** | **Data Lake Analytics · Feature Store · AI Training** |
| 고르는 질문 | 실시간 이벤트 로그, 모든 필드를 다 기록해야 하나? | 대규모 과거 데이터 분석, 특정 컬럼만 집계하나? |

### Compaction 패턴 — 실무 결론

> **유입 시점엔 작은 Avro 파일들로 빠르게 저장하고, 새벽 배치에 큰 Parquet 파일 하나로 묶어
> 변환하라.**

```
Data Ingestion          Data Processing              AI Training
(Real-time Stream)      (Batch / Micro-batch)        (Model Serving)
Kafka + Avro       →    ETL & Compaction        →    Feature Store
                        Avro → Parquet
· Schema Registry 검증   · 작은 파일 병합(Compaction)   · 컬럼 기반 고속 조회
· 초고속 순차 쓰기         · 데이터 정제 및 조인            · Predicate Pushdown
· 원본(Raw) 보존         · 파티셔닝 (날짜/시간별)         · GPU 메모리 최적화
```

**두 포맷을 고르는 문제가 아니라 파이프라인의 단계별로 갈아타는 문제다** — 이 덱의 가장 실용적인
결론이고, [[Medallion architecture]]의 bronze→silver→gold와 나란히 놓고 볼 만하다.

운영 대시보드 지표 예시: Ingestion Latency < 500ms · Compression Ratio 1:12 (Parquet Snappy) ·
Schema Drift Auto-Heal (Registry Active) · Data Quality 99.9%.

## 기존 페이지와의 대조

- **일치** — Parquet=열/스캔 최적화, Avro=행/스트리밍, Arrow=zero-copy 처리 최적화.
  [[Columnar and in-memory data formats]]와 충돌 없다.
- **보강(큼)** — Parquet 내부(RLE·Dictionary·footer 통계·predicate pushdown), Avro의
  self-describing 구조와 스키마 진화 3모드, **Avro→Parquet compaction 패턴**, small files 문제.
  랜드스케이프 가이드는 "Avro는 레코드를 주고받는 용도, 특히 스트림 처리에서"라고만 썼는데
  **그 이유(쓰기 지연 + 스키마 진화)** 가 여기서 채워졌다.
- **여전히 없는 것** — ORC와의 비교. 랜드스케이프 가이드도 "Parquet과 같은 문제를 푸는 다른 포맷"
  이라고만 했다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Columnar and in-memory data formats]], [[Change data capture]] (Schema Registry),
  [[Apache Kafka]], [[Medallion architecture]], [[Feature store]]
- 이어지는 챕터: [[AI DE Course - Ch2-7 Delta Lake and ACID]] — small files 문제를 테이블 포맷이
  compaction으로 푸는 이야기

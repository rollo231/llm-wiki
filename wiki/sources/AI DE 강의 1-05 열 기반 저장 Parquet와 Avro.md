---
type: source
title: AI DE 강의 1-05 열 기반 저장 Parquet와 Avro
aliases: [AI DE 1-05]
tags: [AI-DE-강의, 저장, 포맷]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/data-engineering/ai-de-course/part1/06. CH02-4. AI를 위한 데이터 구조- Parquet, Avro 및 Columnar Storage의 원리1.pdf"
  - "raw/data-engineering/ai-de-course/part1/07. CH02-5. AI를 위한 데이터 구조- Parquet, Avro 및 Columnar Storage의 원리 2.pdf"
  - "raw/data-engineering/ai-de-course/part1/08. CH02-6. AI를 위한 데이터 구조- Parquet, Avro 및 Columnar Storage의 원리 3.pdf"
---

# AI DE 강의 1-05 열 기반 저장 Parquet와 Avro

[[AI 데이터 엔지니어링 강의]] Part 1의 저장 파트 두 번째 강의. 연속 덱 세 개((1)~(3))를 한 페이지로 묶었다.
열 기반 저장의 원리 → Parquet → Avro 순서로 간다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 1 |
| 덱 제목 | AI 시대, 데이터 저장 방식이 바뀌어야 하는 이유 (1)·(2)·(3) (파일명: AI를 위한 데이터 구조- Parquet, Avro 및 Columnar Storage의 원리 1~3) |
| 원본 파일 | `part1/06. CH02-4. …원리1.pdf` (7p) · `part1/07. CH02-5. …원리 2.pdf` (7p) · `part1/08. CH02-6. …원리 3.pdf` (8p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-03-17 |
| URL | 없음 (유료 강의 자료) |

## 요약

### (1) 왜 열 기반인가 — 덱 06

- **AI 학습 워크로드의 세 가지 특성** — 대량 읽기(TB~PB를 반복해서 메모리로), 선택적 열 접근(수백 속성 중
  필요한 피처만), 순차적 고처리량(GPU가 쉬지 않도록 대역폭 극대화).
- **행 기반의 한계** — "사과만 먹고 싶은데 과일 바구니를 통째로 사야 한다." 필요한 데이터가 10%여도 100%를
  읽어 디스크는 헛일하고 GPU는 대기한다.
- **열 기반의 원리** — 같은 열끼리 물리적으로 모아 저장(불필요한 열은 읽지 않음), 같은 타입이 연속돼 압축률
  상승, 컬럼을 통째로 CPU 캐시에 올리는 벡터화 실행.

### (2) Apache Parquet — 덱 07

- **정의** — 하둡 생태계에서 출발한 오픈소스 열 기반 저장 포맷.
- **압축·인코딩** — RLE(`Male, Male, …` × 100,000 → `"Male" × 100,000`), 딕셔너리 인코딩(고유 값을 숫자로
  매핑). 결과로 저장 비용과 메모리 로딩 시간이 줄어든다.
- **Predicate Pushdown** — 블록마다 최솟값·최댓값·Null 개수 같은 통계가 메타데이터로 들어 있다. 엔진은 실제
  데이터를 읽기 전에 메타데이터를 보고, 조건에 맞지 않는 블록을 통째로 건너뛴다(`WHERE age < 30`이면 최소
  연령 30인 블록은 열지 않는다).
- **ML 생태계와의 결합** — Spark(Parquet 파티셔닝을 인식해 병렬 분배), Pandas(column pruning으로 메모리
  최소화), Arrow(인메모리 포맷으로 직렬화 오버헤드 없는 전송).
- **실천 과제** — 원천 CSV를 Parquet로 표준화하고, 파이프라인을 pruning·pushdown을 고려해 설계한다.

### (3) Apache Avro와 스키마 진화 — 덱 08

- **Parquet의 구조적 한계** — 컬럼으로 분해·압축하느라 **쓰기 지연**이 크고, 실시간으로 저장하면 **작은 파일**이
  무수히 생겨 읽기 성능이 떨어진다.
- **실시간 쓰기의 조건** — 행 기반 순차 추가(append-only), 유연한 스키마, 텍스트(JSON)보다 작은 바이너리
  직렬화 → Avro.
- **Avro 파일 구조** — 헤더에 JSON 스키마와 코덱(snappy)이 들어 있고 데이터 블록은 바이너리 행이다. 데이터와
  스키마가 한 파일에 공존하는 **self-describing** 구조라 헤더만 읽으면 구조를 안다.
- **스키마 진화** — V1(`user_id`, `action`) → V2(`+ dwell_time: long, default 0`) → V3. 호환성 규칙:

| 규칙 | 덱의 정의 |
|---|---|
| BACKWARD | 새 스키마로 이전 데이터를 읽을 수 있음 (필드 삭제 시 유리) |
| FORWARD | 이전 스키마로 새 데이터를 읽을 수 있음 (필드 추가 시 유리) |
| FULL | 양방향 모두 호환. 가장 이상적이나 default 값이 필수 |

  안전한 변경은 default가 있는 필드 추가, default가 있던 필드 삭제, 타입 확대(int → long, float → double).
  위험한 변경은 alias 없는 이름 변경, default 없는 필드 추가, 타입 축소(long → int).
- **스키마 레지스트리** — 프로듀서는 스키마를 등록하고 ID를 받아, Kafka에는 **Avro 바이너리 + 스키마 ID**만
  보낸다. 컨슈머는 ID로 스키마를 조회한다.
- **Avro vs Parquet 선택** — 실시간 이벤트 로그처럼 모든 필드를 기록하면 Avro(Kafka·랜딩 존·스트리밍), 대규모
  과거 데이터에서 특정 컬럼만 집계하면 Parquet(레이크 분석·피처 스토어·학습).
- **Compaction 패턴** — 유입 시점엔 작은 Avro 파일로 빠르게 쓰고, 새벽 배치에서 큰 Parquet 파일로 묶어 변환한다.
- **전체 흐름** — 수집(Kafka + Avro, 레지스트리 검증, 원본 보존) → 처리(ETL·compaction, 정제·조인, 날짜별
  파티셔닝) → 서빙(피처 스토어의 Parquet, pushdown, GPU 메모리 최적화).

## 핵심

- **두 포맷은 경쟁이 아니라 파이프라인의 앞뒤다.** Avro는 쓰기 최적화(행·append·스키마 진화), Parquet는 읽기
  최적화(열·pushdown·압축)이고, **compaction이 둘의 경계**다. → [[행 기반과 열 기반 저장]] · [[지연 시간과 처리량]]
- Parquet 속도의 원천은 결국 **"안 읽기"**다 — 열을 안 읽고(pruning), 블록을 안 읽고(pushdown), 읽는 양을
  줄인다(인코딩·압축).
- 스키마 진화의 호환성 정의는 **이 덱이 맞고, 같은 코스의 [[AI DE 강의 1-08 CDC]]가 반대로 틀렸다.**
  → [[스키마 진화]]

## 주의·결함

- ⚠️ **Parquet 메타데이터 위치** — 덱 07 요약(p7)은 "**헤더**의 메타데이터를 먼저 확인"한다고 쓰고, p5는
  "Header/Footer 메타데이터"라고 뭉뚱그린다. Parquet는 파일 메타데이터(row group·컬럼 통계)를 데이터 뒤인
  **footer**에 쓰고, 헤더는 4바이트 매직 넘버 `PAR1`뿐이다. 덱의 "블록"은 row group에 해당한다.
  [Apache Parquet 문서 "File Format" — "File metadata is written after the data to allow for single pass
  writing." https://parquet.apache.org/docs/file-format/ , 2026-09-14 확인]
- **Arrow의 "Zero-Copy Reads, 직렬화·역직렬화 오버헤드 없이"** — Parquet를 Arrow로 읽을 때도 압축 해제와
  디코딩은 필요하다. zero-copy는 Arrow 메모리 포맷끼리 데이터를 주고받을 때의 성질이다.
- 출처 없는 수치: "CSV 100GB → Parquet 10GB(10배)", "Avro는 JSON 대비 1/10 크기", "조회 속도 수십 배 이상",
  "GPU/CPU 가동률 100%", 운영 대시보드의 `< 500ms`·`1 : 12`·`99.9%`(장식).
- 덱 06은 다음 강의에서 "Parquet, ORC, Avro를 비교"한다고 예고하지만 ORC는 이후 나오지 않는다.
- 덱 08 마무리 슬라이드(p8)는 학습 목표 슬라이드(p2)를 글자 그대로 복사했다("…파악하게 될 것입니다").
- **덱 교체 흔적** *(추론)* — 세 덱의 슬라이드 제목("AI 시대, 데이터 저장 방식이 바뀌어야 하는 이유")이
  파일명과 다르고, 양식과 PDF 생성일(2026-03-17)도 앞뒤 덱(2026-02-19)과 다르다. 나중에 교체·추가된 덱으로 보인다.

## 관련

- 개념·도구: [[Apache Parquet]] · [[Apache Avro]] · [[행 기반과 열 기반 저장]] · [[스키마 진화]]
- 이전 강의: [[AI DE 강의 1-04 저장소의 진화 DW에서 Lakehouse까지]]
- 다음 강의: [[AI DE 강의 1-06 Delta Lake와 ACID]]

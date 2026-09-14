---
type: entity
title: Apache Avro
aliases: [Avro, 아브로]
tags: [도구, 저장, 포맷, 직렬화]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "[[AI DE 강의 1-04 저장소의 진화 DW에서 Lakehouse까지]]"
  - "[[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]]"
  - "[[AI DE 강의 1-08 CDC]]"
---

# Apache Avro

**행 기반 바이너리 직렬화 포맷.** 데이터가 도착하는 즉시 레코드 단위로 뒤에 붙여 쓰기에 맞고, 스키마 진화를 설계의
중심에 둔다. Part 1에서는 [[Apache Parquet]]의 짝(쓰기 최적화 쪽)으로 나온다.

## 구조

- **Self-describing 파일** — 헤더에 JSON으로 쓴 스키마와 코덱(예: snappy)이 들어 있고, 데이터 블록은 바이너리 행이다.
  헤더만 읽으면 구조를 안다.
- **스키마 정의(`.avsc`)** — 사람이 읽을 수 있는 JSON.

```json
{
  "type": "record",
  "name": "UserActivity",
  "fields": [
    {"name": "user_id", "type": "string"},
    {"name": "action", "type": "string"},
    {"name": "dwell_time", "type": "long", "default": 0}
  ]
}
```

`dwell_time`의 `default`가 스키마 진화의 열쇠다 — 이 필드가 없던 옛 데이터를 새 스키마로 읽을 때 채울 값이 있다.
([[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]])

## 왜 실시간 유입에 쓰나

[[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]]가 드는 실시간 쓰기의 세 조건:

1. **순차 추가(append-only)** — 행 기반이라 들어오는 즉시 끝에 붙인다.
2. **유연한 스키마** — 컬럼이 추가·변경돼도 파이프라인이 멈추지 않는다. → [[스키마 진화]]
3. **효율적 직렬화** — JSON 같은 텍스트보다 작은 바이너리.

## Avro vs Parquet

| | Avro | Parquet |
|---|---|---|
| 방향 | 행 기반, 쓰기 최적화 | 열 기반, 읽기·압축 최적화 |
| 강점 | 빠른 추가, 스키마 진화 | pruning, pushdown, 압축률 |
| 맞는 곳 | Kafka 메시지, 랜딩 존, 스트리밍, CDC 이벤트 | 레이크 분석, 피처 스토어, 학습 |
| 선택 질문 | 실시간 이벤트를 모든 필드 그대로 기록하나? | 과거 데이터에서 특정 컬럼만 집계하나? |

둘은 경쟁이 아니라 파이프라인의 앞뒤다 — **작은 Avro 파일로 빠르게 받고, 새벽 배치에서 큰 Parquet 파일로 합친다**
(compaction 패턴).

## 스트림에서의 스키마

Kafka 메시지마다 스키마를 싣지 않고 **스키마 레지스트리**를 쓴다: 프로듀서가 스키마를 등록해 ID를 받고, 메시지에는
Avro 바이너리 + 스키마 ID만 넣는다. CDC 도구도 DB 로그를 JSON이나 Avro 이벤트로 번역한다([[AI DE 강의 1-08 CDC]]).

## 주의

- ⚠️ **[[AI DE 강의 1-04 저장소의 진화 DW에서 Lakehouse까지]]는 Avro를 열 기반으로 분류한다**("Disk Storage Layout
  (Parquet/Avro)", "Parquet/Avro 도입 검증 — 컬럼 프루닝 테스트"). Avro는 행 기반이며, 같은 코스의 덱 08이 이를 명시한다.
- 강의의 "JSON 대비 1/10 크기"는 출처가 없다.

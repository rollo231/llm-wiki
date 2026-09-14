---
type: entity
title: Apache Parquet
aliases: [Parquet, 파케이, 파켓, Predicate Pushdown, Column Pruning]
tags: [도구, 저장, 포맷]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "[[AI DE 강의 1-04 저장소의 진화 DW에서 Lakehouse까지]]"
  - "[[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]]"
  - "[[AI DE 강의 1-06 Delta Lake와 ACID]]"
---

# Apache Parquet

하둡 생태계에서 출발한 오픈소스 **열 기반 저장 파일 포맷.** 분석과 AI 학습처럼 "많이 읽고 일부 컬럼만 쓰는" 워크로드의
사실상 표준이다. → [[행 기반과 열 기반 저장]]

## 빠른 이유 — 안 읽기

| 기법 | 무엇을 안 읽나 | 원리 |
|---|---|---|
| Column pruning | 필요 없는 **열** | 같은 열끼리 물리적으로 모여 있어 필요한 열만 읽는다 |
| Predicate pushdown | 조건에 맞지 않는 **블록(row group)** | row group마다 컬럼별 최솟값·최댓값·Null 개수 통계가 있다. `WHERE age < 30`이면 최솟값이 30인 row group은 열지 않는다 |
| 인코딩·압축 | 읽을 **바이트 양** 자체 | 같은 타입이 연속되므로 RLE(반복 요약)·딕셔너리 인코딩(고유 값을 번호로)이 잘 먹힌다. 코덱은 Snappy·Zstd 등 |

## 파일 구조

```
PAR1 (4바이트 매직 넘버)
row group 1 ─ column chunk A, column chunk B, …
row group 2 ─ …
File Metadata (스키마, row group·컬럼 청크 위치와 통계)
메타데이터 길이 (4바이트)
PAR1
```

**메타데이터는 데이터 뒤, 파일 끝(footer)에 있다.** 데이터를 한 번에 쭉 쓰고 마지막에 요약을 붙이기 위해서다. 읽는 쪽은
파일 끝부터 읽어 메타데이터를 보고, 필요한 row group·column chunk만 찾아간다.
[Apache Parquet "File Format" — "File metadata is written after the data to allow for single pass writing."
https://parquet.apache.org/docs/file-format/ , 2026-09-14 확인]

⚠️ [[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]]의 요약 슬라이드는 "**헤더**의 메타데이터를 먼저 확인"한다고 쓴다.

## 생태계

- **Spark** — Parquet의 파티셔닝 구조를 인식해 작업 노드에 데이터를 분배한다.
- **Pandas** — 필요한 컬럼만 읽어 DataFrame 메모리를 줄인다.
- **Arrow** — 인메모리 열 기반 포맷. Parquet를 Arrow로 읽을 때도 압축 해제·디코딩은 필요하고, zero-copy는 Arrow 형식끼리
  주고받을 때의 성질이다.

## 약점과 짝

| 약점 | 이유 | 짝 |
|---|---|---|
| 쓰기 지연 | 컬럼으로 분해하고 압축하느라 CPU를 쓴다 | 유입은 [[Apache Avro]]로 빠르게 받는다 |
| 작은 파일 문제 | 실시간으로 조금씩 쓰면 작은 파일이 쌓여 메타데이터 부하와 읽기 저하 | 배치로 큰 파일로 합친다(compaction) |
| 행 수정·트랜잭션 없음 | 파일 포맷일 뿐이라 한 줄 수정에 파일 재작성, 동시 쓰기 격리 없음 | [[Delta Lake]]가 Parquet 파일 위에 트랜잭션 로그를 얹는다 |

## Part 1에서의 쓰임

원천 CSV를 Parquet로 표준화 → 레이크 분석, 피처 스토어, AI 학습용 서빙 레이어
([[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]]). Delta Lake의 데이터 파일
([[AI DE 강의 1-06 Delta Lake와 ACID]]).

## 주의

- 강의의 "CSV 100GB → Parquet 10GB(10배)"는 출처 없는 수치다. 압축률은 컬럼 수와 값 분포에 따라 크게 달라진다.

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
tags: [data-engineering, data-format, parquet, arrow, avro, columnar, storage]
created: 2026-07-28
updated: 2026-07-28
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers"]
---

# Columnar and in-memory data formats

데이터가 담기는 바이트 수준의 포맷. **파일 포맷**(디스크·전송)과 **메모리 포맷**(처리) 두 갈래이고,
둘을 가르는 축이 이 페이지의 핵심이다.

## 파일 포맷

| 포맷 | 방향 | 쓰임 |
|---|---|---|
| **CSV** (·Excel) | 행 | 소량 전송. 아무 오피스 소프트웨어로나 열린다 — 비기술 사용자와 주고받는 포맷. 영업팀이 분기 딜 분석해달라며 보내는 그것. |
| **Apache Parquet** | **열** | 기술 사용자의 기본값. 압축률이 좋고 대용량 저장·전송에 적합. 대부분의 데이터 툴이 읽고 쓴다 — **데이터 툴링의 링구아 프랑카**. |
| **Apache ORC** | 열 | Parquet과 같은 문제를 푸는 다른 포맷. |
| **Apache Avro** | **행** | 바이너리지만 행 지향. **레코드를 주고받는 용도**, 특히 스트림 처리에서. |

> 컬럼너란 데이터가 행 단위가 아니라 **열 단위로 배치**된다는 뜻이고, 그래서 압축이 잘 되고
> 필요한 열만 읽을 수 있다.

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

## 링크

- 혼동 주의: **파일 포맷 ≠ 테이블 포맷.** Parquet은 파일 하나의 레이아웃이고, Iceberg 같은
  테이블 포맷은 *여러 Parquet 파일을 하나의 테이블로 묶는 규약*이다 → [[Table formats]]
- 어디에 놓이나: [[Analytical data storage tiers]]
- Avro가 왜 스트리밍인가: [[Batch and stream processing]]
- 인접: [[SpatialData as a data engineering substrate]] — 공간 오믹스에서 Zarr(청크 배열)와
  GeoParquet이 같은 자리를 차지한다. 래스터는 Parquet의 표 모델에 안 맞아 Zarr가 쓰인다는 것이
  그 노트의 출발점.
- 출처: [[Data landscape guide for developers]]

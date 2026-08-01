---
type: entity
title: NVIDIA RAPIDS
area: [data-engineering, programming]
aliases: [RAPIDS, cuDF, cudf.pandas, Dask-cuDF, Spark RAPIDS, RMM, NVTabular, cuSpatial]
tags: [data-engineering, gpu, rapids, cudf, spark, arrow, etl, feature-engineering]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part4 Ch4 GPU in data engineering and RAPIDS]]"]
---

# NVIDIA RAPIDS

**GPU 위에서 DataFrame·ETL·feature engineering을 수행하는 라이브러리 모음.**
데이터 엔지니어가 CUDA를 직접 쓰지 않고 GPU를 활용하는 계층이다.

## 왜 필요한가 — GPU Starvation

> **"데이터는 커지는데 모델 학습 준비 시간에 오랜 시간이 소요된다."**

| 문제 | 내용 |
|---|---|
| **CPU의 한계** | 데이터 로딩·전처리(Pandas)·피처 엔지니어링이 CPU에서 처리되며 극심한 지연 |
| **PCIe 병목** | 전처리된 데이터를 CPU 메모리 → GPU 메모리로 넘기는 과정(복사·직렬화)에서 병목. ⭐ **GPU는 빠르지만 데이터를 기다리느라 놀고 있는 상태 (Starvation)** |

> **"MLOps 관점에서는 ETL 병목이 모델 실험 속도, 재학습 주기, 배치 추론 처리량까지 직접 영향을
> 준다."**

**핵심 전략: 데이터를 가능한 한 GPU 위에 오래 유지한다.** PCIe(~64 GB/s)와 HBM(2~3 TB/s)의
40~50배 차이가 이 전략의 근거다. → [[GPU architecture]]

## 생태계

| 기술 | 처리 주체 | 데이터 규모 | 적용 대상 | **코드 수정** |
|---|---|---|---|---|
| **cuDF** | 단일 GPU | 단일 GPU VRAM 이내 | 고속 Tabular ETL | **API 변경 필요** (`pandas` → `cudf`) |
| **cudf.pandas** | 단일 GPU / CPU | 단일 GPU VRAM 이내 | 기존 pandas 유저의 손쉬운 가속 | ⭐ **없음** (매직 커맨드만) |
| **Dask-cuDF** | 다중 GPU / 노드 | **단일 GPU VRAM 초과** | 단일 GPU 한계 극복, 분산 처리 | API 변경 필요 |
| **Spark RAPIDS** | 다중 GPU / 노드 | 클러스터 기반 빅데이터 | 기존 Spark 워크로드 고속화 | ⭐ **없음** (플러그인 설정만) |
| **RMM** | GPU 메모리 관리 | — | 위 기술들의 **메모리 병목·파편화 방지** | — (내부적으로 자동) |

**추가 구성 요소:** **NVTabular**(추천 시스템용 feature engineering, terabyte-scale recommender
dataset) · **cuSpatial**(공간 연산).

### cuDF — Arrow 기반

- Pandas와 유사한 API로 GPU에서 DataFrame 조작
- ⭐ **Apache Arrow 기반** 컬럼형 in-memory 표현
- **직렬화/역직렬화 오버헤드 없이** GPU↔CPU 간, 다른 도구 간 데이터 전송이 매우 빠름

> ⭐ **cuDF가 Arrow를 쓰는 이유가 [[GPU architecture]]의 coalescing이다** —
> *"컬럼 기반 포맷(Parquet, Arrow)이 GPU와 어울리는 이유는 연속된 메모리 접근이 가능하기 때문."*
> [[Columnar and in-memory data formats]]에서 배운 Arrow가 여기서 하드웨어 이유로 정당화된다.

### cudf.pandas — 스마트 폴백

한 줄 추가 또는 실행 옵션 변경만으로 가속:

```
# Jupyter
%load_ext cudf.pandas

# 스크립트
python -m cudf.pandas script.py
```

**동작:** GPU 지원 연산이면 cuDF로 처리, **미지원 연산이나 사용자 정의 함수면 자동으로
pandas(CPU)로 전환(Fallback).**

### Dask-cuDF — 단일 GPU 메모리 한계 극복

- 거대한 DataFrame을 **cuDF 파티션으로 쪼갬**
- 단일 서버의 여러 GPU(Multi-GPU) 또는 네트워크로 연결된 서버(Multi-Node)에 분산
- `dask.distributed` 클러스터가 스케줄링
- **OOM 해결** — TB 단위 데이터셋도 처리

### Spark RAPIDS — Catalyst를 가로챈다

- **플러그인 아키텍처** — Spark 코드 수정 불필요. `spark-submit` 시 `.jar` 포함 + 설정만
- ⭐ **Catalyst Optimizer 개입** — Spark의 **물리적 실행 계획(Physical Plan) 단계를 가로채서**
  CPU에서 실행되던 Sort/Join/Aggregate를 GPU 연산으로 대체
- **최적화된 셔플링** — **UCX / RDMA**로 노드 간 셔플의 네트워크 병목 감소

→ [[Apache Spark]]

### RMM — 메모리 풀 할당자

| 문제 | 해결 |
|---|---|
| 기본 할당자 `cudaMalloc`은 **시스템 콜이 발생**해 느리고 **동기화 오버헤드**가 큼 | 프로그램 시작 시 GPU 메모리 **Pool을 미리 선점.** 라이브러리가 요구하면 시스템 콜 없이 풀 안에서 빠르게 빌려주고 반납 |

> **"DataFrame 처리처럼 수많은 중간 배열(Array)이 생성되고 버려지는 작업에 이 오버헤드가
> 치명적이다."** — 왜 별도 할당자가 필요한지를 워크로드 특성과 묶어 설명하는 게 좋다.

## ⭐ GPU ETL이 맞는가 — 판단 5문항

| 잘 맞음 | 애매함 |
|---|---|
| 대량 필터링·조인·group by 집계 | 데이터 크기가 작음 |
| **컬럼 단위 변환** | **Python UDF가 많음** |
| **Parquet / ORC 기반 분석형 처리** | **분기와 문자열 처리 중심**, row 단위 복잡 로직 |
| 대용량 feature table 생성 | **입출력 파일이 지나치게 작고 많음** |
| batch inference 입력 전처리 | CPU fallback이 많은 Spark job |
| 반복적 벡터·수치 연산 | GPU 왕복 비용 > 계산 이득 |

1. 이 ETL은 **컬럼 단위 대량 연산**인가? (filter/projection/join/group by/aggregation 중심)
2. **GPU 메모리에 맞는 batch/partition 설계가 가능한가?** (처리 단위가 너무 크면 OOM)
3. **CPU fallback이 적은가?**
4. **작은 파일이 너무 많지는 않은가?** (수 GB 단위 큰 입력이 유리)
5. ⭐ **결과가 MLOps 흐름과 연결되는가?** (feature store, batch inference, monitoring, retraining)

> ⭐ **5번이 이 도구를 판단하는 이 강의의 독자적 각도다.** 실패 사례 목록에도
> **"MLOps 추적 없이 단발성 가속만 수행"** 이 들어간다 — **빨라지는 것만으로는 부족하고
> 운영 흐름에 들어가야 가치가 있다.**
>
> **4번은 [[Columnar and in-memory data formats]]의 small file problem이 GPU에서 더 치명적이라는
> 뜻이다.**

## 분산 GPU ETL — shuffle이 다시 병목

**분산 ETL의 핵심 병목:** join · aggregation · repartition · sort · shuffle write/read ·
network transfer.

**GPU shuffle의 목표:** 데이터를 가능한 한 GPU 위에 오래 유지 · CPU와 host memory 경유 비용 감소 ·
GPU 간 데이터 이동 최적화.

> ⭐ **"GPU ETL은 연산만 빠르게 해서는 부족하다. 분산 ETL에서는 shuffle과 network 경로까지
> GPU 친화적으로 설계해야 한다."**
>
> **[[Apache Hadoop]] MapReduce의 shuffle 병목이 GPU 시대에 되돌아온 형태다 — 분산 처리의 병목은
> 20년째 shuffle이다.**

## ⚠️ 활용 사례의 수치는 인용하기 어렵다

강의가 든 세 사례:

| 사례 | 주장된 효과 |
|---|---|
| **추천 시스템 피처 엔지니어링** (NVTabular, Zero-copy로 PyTorch에 포인터 전달) | ⚠️ **"전처리 시간이 8시간에서 15분으로", GPU 활용률 80~90%** |
| **대규모 Geospatial Joins** (cuSpatial) | ⚠️ **"50대의 CPU 노드가 풀던 문제를 A100 1장이 수 분에", TCO 70~80% 절감** |
| **실시간 로그 파싱** (cuDF String 연산, 정규식) | ⚠️ **"15분 마이크로배치 → 수 초 이내 탐지"** |

> ⚠️⚠️ **사례 1에 내부 모순이 있다.** AS-IS 슬라이드는 **"전처리에 4시간"**, TO-BE 슬라이드는
> **"8시간에서 15분으로 단축"** 이라고 한다. **연속된 두 슬라이드에서 4시간 vs 8시간이 어긋난다.**
>
> ⚠️ **세 사례 모두 출처가 없다.** 회사명·벤치마크 조건·데이터 규모 정의가 없고, NVIDIA 마케팅
> 자료에서 흔히 보는 형태의 수치인데 **강의가 이를 벤더 주장이라고 밝히지 않는다.**
> (Part 3가 Neo4j·Microsoft 수치에 "자사 비교"라고 명시했던 것보다 후퇴했다.)
>
> **다만 사례들이 가리키는 워크로드 성격은 타당하다** — geospatial join과 대량 정규식은 실제로
> 병렬성이 높고 산술 집약도가 있어 GPU에 잘 맞는다. **방향은 맞고 수치는 못 쓴다.**
>
> ⚠️ **비용 비교가 없다.** "A100 1장이 CPU 50대를 대체"라면 A100 시간당 단가 × 시간 vs CPU 노드
> 단가 × 시간을 비교해야 TCO 주장이 성립하는데 그 계산이 없다.

## MLOps 파이프라인에서의 위치

**Feature Engineering 단계:** 원본 로그 정제 → 사용자/item/session feature → ⭐ **label join
(기준 시점 기반 조인)** → negative sampling → offline feature table.

**Batch Inference 단계:** scoring 대상 추출 → 입력 feature 조립(key join, snapshot 선택) →
모델 입력 변환(**null 처리, type 변환, 컬럼 순서 정렬**) → **GPU memory 기준 chunking** →
결과 재결합(**model_version 추가**) → 결과 집계.

> ⭐ **"label join — 기준 시점 기반 조인"이 [[Data drift and training-serving skew]]의
> skew 패턴 1(시간 기준 불일치)과 같은 지점이다.** point-in-time correctness라는 용어는 안 쓰지만
> 그 이야기다.
>
> **"null 처리, type 변환, 컬럼 순서 정렬"이 skew 패턴 3(결측 처리)의 실제 작업 위치다.**

## ⚠️ 이 위키에 아직 없는 것

- **cuML · cuGraph** — RAPIDS의 주요 구성요소인데 생태계 표에 없다
- **실제 벤치마크** — 독립적인 성능 측정
- **Polars / DuckDB와의 비교** — CPU 쪽 고성능 대안이 언급되지 않는다.
  "작은 데이터는 CPU가 더 빠를 수 있다"고 하면서 그 CPU 쪽 선택지를 말하지 않는다
- **GPU 메모리 관리 실무** — spill 정책, OOM 발생 시 대응

## 관련 페이지

- [[GPU architecture]] — coalescing, PCIe 병목, Roofline
- [[CUDA]] — 아래 계층
- [[Apache Spark]] — Spark RAPIDS
- [[GPU resource allocation]] — GPU ETL 워크로드의 스케줄링
- [[Columnar and in-memory data formats]] — Arrow·Parquet
- [[Feature store]] · [[ML data pipeline]] · [[MLOps]]
- [[Data drift and training-serving skew]] — label join의 기준 시점

## 출처

- [[AI DE Course - Part4 Ch4 GPU in data engineering and RAPIDS]]

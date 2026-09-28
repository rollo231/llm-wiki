---
type: entity
title: RAPIDS
aliases: [NVIDIA RAPIDS, cuDF, cudf.pandas, Dask-cuDF, RAPIDS Accelerator for Apache Spark, Spark RAPIDS, RMM, cuSpatial, NVTabular]
tags: [GPU, 도구, ETL, 데이터프레임]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용]]"
  - "[[AI DE 강의 4-14 RAPIDS 가속 ETL]]"
---

# RAPIDS

NVIDIA의 GPU 데이터 과학 라이브러리 묶음이다. 데이터프레임 처리(cuDF), 분산 처리(Dask-cuDF), Spark 가속(RAPIDS Accelerator for Apache Spark), GPU 메모리 관리(RMM) 등으로 이뤄진다. [[AI DE 강의 4-14 RAPIDS 가속 ETL]]은 이것을 "데이터를 기다리느라 GPU가 노는 상태(starvation)"를 줄이는 도구로 소개한다(p329). GPU가 왜 이런 연산에 맞는지는 [[GPU 아키텍처]]에 있다.

## 구성 요소

강의의 비교표(p348)에 현재 상태를 더한 것이다.

| 구성 요소 | 처리 주체 | 데이터 규모 | 코드 수정 | 상태 (2026-09) |
|---|---|---|---|---|
| cuDF | 단일 GPU | VRAM 이내 | `import cudf`로 API 변경 | 현역. Arrow 호환 열 형식 |
| cudf.pandas | 단일 GPU + CPU 폴백 | VRAM 이내 | 없음. `%load_ext cudf.pandas` 또는 `python -m cudf.pandas script.py` | 현역 |
| cudf-polars (Polars GPU 엔진) | 단일 GPU | VRAM 이내 | Polars에서 엔진 지정 | Open Beta(2024-09~) |
| Dask-cuDF | 다중 GPU·다중 노드 | VRAM 초과 | dask 적용 | 현역 |
| RAPIDS Accelerator for Apache Spark | Spark 클러스터의 GPU | 클러스터 규모 | 없음. 플러그인 jar와 설정 | 현역 |
| RMM | GPU 메모리 풀 | — | 보통 라이브러리가 내부에서 쓴다 | 현역 |
| NVTabular | 추천 피처 전처리 | TB급 | NVTabular API | ⚠️ 정체. 마지막 릴리스 v23.08.00(2023-08-29) |
| cuSpatial · cuProj | 공간 연산 | — | — | ❌ 중단. 25.06부터 배포 중단, 저장소 2025-07-28 보관 |

- cudf.pandas는 지원 연산이면 GPU로, 미지원 연산이나 사용자 정의 함수면 자동으로 pandas(CPU)로 돌아간다(p343). [https://docs.nvidia.com/cudf/latest/cudf_pandas/usage/ , 2026-09-28 확인]
- ⚠️ 강의는 cuDF가 "pandas, Polars, Spark 계열 워크플로우 가속"에 쓰인다고 한다(4-13 p310). Polars GPU 엔진은 아직 Open Beta다. Polars 문서: "This functionality is available in Open Beta". [https://docs.pola.rs/user-guide/gpu-support/ , 2026-09-28 확인]
- ⚠️ NVTabular(NVIDIA Merlin의 일부)은 보관되지 않았지만 2023년 이후 릴리스가 없다. Merlin 쪽 저장소도 마지막 릴리스가 Merlin v24.06.00, core v23.08, models·Transformers4Rec v23.12다. 강의는 추천 피처 엔지니어링 사례(p337)와 생태계(4-13 p313)에서 현역 도구처럼 소개한다. [GitHub REST API로 NVIDIA-Merlin 저장소의 archived 플래그와 최신 릴리스 조회, 2026-09-28 확인]
- ❌ 강의는 공간 조인 사례(p339)에 cuSpatial을 쓰지만, RAPIDS는 25.06부터 cuSpatial 패키지를 내지 않고 개발을 멈췄다. 공지: "RAPIDS will stop publishing cuSpatial packages in RAPIDS Release v25.06 … Development … will be paused". [https://docs.nvidia.com/datascience/notices/rsn0045/index.html , 2026-09-28 확인] 슬라이드 작성(2026-05)보다 약 1년 앞선 일이다.

## cuDF와 Arrow (단서)

강의는 cuDF가 Apache Arrow 기반이라 "직렬화/역직렬화 오버헤드 없이 GPU-CPU 간, 다른 도구 간의 데이터 전송이 매우 빠름"이라고 한다(p342). Arrow 호환 형식 덕분에 줄어드는 것은 형식 변환이다. host와 device 사이의 PCIe 복사는 그대로 남고, 같은 강의 앞부분(4-11 p266)이 이것을 데이터 파이프라인의 최대 병목으로 든다. ❌ 전송이 빠르다는 말은 과장이다. 도구 사이에 복사 없이 넘기는 것은 같은 장치 메모리 안에서의 이야기다(DLPack, `__cuda_array_interface__`). 강의의 사례 1이 말하는 "메모리 포인터만 PyTorch로 넘겨(Zero-copy)"(p337)도 이 경우다. 이 연결은 위키의 정리다.

## RAPIDS Accelerator for Apache Spark

- `spark-submit`에 플러그인 jar를 넣고 `spark.plugins=com.nvidia.spark.SQLPlugin`을 켜면, Catalyst의 물리 실행 계획에서 지원 연산(Sort·Join·Aggregate 등)을 GPU 연산으로 바꾼다. 미지원 연산은 CPU 경로로 돌아간다(p346, 4-13 p312).
- 가속이 큰 곳은 Spark SQL·DataFrame, scan·filter·projection, join·aggregation·sort 일부, Parquet·ORC다. 제한되는 곳은 RDD 직접 조작, 미지원 SQL 연산, 일부 UDF, 복잡한 행 단위 처리, CPU 폴백이 많은 계획이다(p349–350).
- ⚠️ 셔플: 강의는 UCX·RDMA로 셔플 병목을 줄인다고만 한다(p346). 현재 RAPIDS 셔플 매니저의 기본값은 MULTITHREADED 모드이고, UCX는 RDMA 환경에서 고르는 선택지다(외부 셔플 서비스와 동적 할당을 꺼야 한다). 문서: "Multi-threaded mode (default)". [https://docs.nvidia.com/spark-rapids/user-guide/latest/additional-functionality/rapids-shuffle.html , 2026-09-28 확인]
- [[Apache Spark]]의 기존 SQL·DataFrame 파이프라인을 그대로 두고 GPU 구간부터 켤 수 있다는 점이 강의가 드는 가장 큰 장점이다(4-13 p312).

## RMM (단서)

RMM은 GPU 메모리 풀 할당자다. 시작할 때 풀을 잡아 두고 라이브러리가 요구할 때마다 시스템 콜 없이 빌려주고 돌려받는다(p347). README는 "device memory pool sub-allocator to reduce the cost of dynamic device memory allocation"이라 적는다. [https://github.com/rapidsai/rmm , 2026-09-28 확인] ✅ 강의는 "기본 할당자(cudaMalloc)"가 동기화 오버헤드가 크다고 한다. NVIDIA 블로그도 CUDA 11.2의 `cudaMallocAsync`·`cudaFreeAsync`를 소개하며 기존 할당·해제를 "device-synchronizing global operations"라 부르므로 강의의 서술이 맞다. 인제스트 때 이 칸에 「동기화하는 쪽은 주로 cudaFree」라고 적었던 것은 검증 보고를 옮긴 것이었고, 같은 출처로 확인되지 않아 고쳤다. 강의가 말하지 않은 대안은 스트림 순서를 따르는 `cudaMallocAsync`(CUDA 11.2부터)다. [https://developer.nvidia.com/blog/using-cuda-stream-ordered-memory-allocator-part-1/ , 2026-09-28 확인]

## 언제 쓰나

강의의 판단 질문 다섯 개(p334–335)는 이렇다. 열 단위 대량 연산(filter·projection·join·group by·aggregation)인가, GPU 메모리에 맞는 batch·partition을 짤 수 있는가, CPU 폴백이 적은가, 작은 파일이 너무 많지 않은가(수 GB 단위 입력이 유리), 결과가 피처 스토어·배치 추론·모니터링·재학습 데이터로 이어지는가. 애매한 작업은 작은 데이터, Python UDF가 많은 작업, 분기·문자열 중심 로직, 행 단위 복잡 로직, 작은 파일이 많은 입력이다(p333).

## 관련

- [[GPU 아키텍처]] · [[GPU 할당과 스케줄링]] · [[Apache Spark]] · [[행 기반과 열 기반 저장]] · [[Apache Parquet]] · [[피처 스토어]] · [[MLOps]]
- 자료: [[AI DE 강의 4-14 RAPIDS 가속 ETL]] · [[AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용]]

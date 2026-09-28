---
type: source
title: AI DE 강의 4-14 RAPIDS 가속 ETL
aliases: [AI DE 4-14]
tags: [AI-DE-강의, GPU, ETL, 도구]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf"
---

# AI DE 강의 4-14 RAPIDS 가속 ETL

[[AI 데이터 엔지니어링 강의]] Part 4 Ch4의 마지막 소단원(5)이자 덱 `01`의 끝이다. RAPIDS를 쓰는 이유, 잘 맞는 작업과 애매한 작업, 사례 세 가지, 생태계(cuDF, cudf.pandas, Dask-cuDF, Spark RAPIDS, RMM), 분산 GPU ETL의 셔플, MLOps 안에서의 피처 엔지니어링과 배치 추론 흐름을 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch4. GPU 워크로드 전략: 5. RAPIDS를 활용한 가속 ETL 처리 |
| 원본 파일 | `part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` p327–356 (30p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch1~4`, 챕터 `Ch4`와 소단원 번호 `5`는 표지 슬라이드 |

## 요약

### 01. RAPIDS (p329–335)

- 데이터 로딩·전처리(pandas)·피처 엔지니어링이 CPU에서 느리고, 끝난 데이터를 GPU 메모리로 옮기는 PCIe 구간이 병목이라 비싼 GPU가 기다리며 논다(starvation)(p329). MLOps 관점에서 ETL 병목은 실험 속도, 재학습 주기, 배치 추론 처리량에 직접 영향을 준다(p330).
- GPU ETL이 잘 맞는 작업(대량 필터·조인·group by, 열 단위 변환, Parquet·ORC 분석형 처리, 대용량 feature table)과 애매한 작업(작은 데이터, Python UDF, 분기·문자열 중심, 행 단위 복잡 로직, 작고 많은 파일, CPU fallback이 많은 Spark job)(p332–333).
- 판단 질문 다섯 개: 열 단위 대량 연산인가, GPU 메모리에 맞는 batch·partition이 되는가, CPU fallback이 적은가, 작은 파일이 너무 많지 않은가, 결과가 MLOps 흐름과 이어지는가(p334–335).

### 02. RAPIDS 활용 사례 (p336–341)

| 사례 | AS-IS | TO-BE | 강의가 주장하는 효과 |
|---|---|---|---|
| 1. 추천 피처 엔지니어링 (p336–337) | 100GB 로그를 CPU Spark로 전처리해 Parquet로 저장, PyTorch가 다시 읽어 학습. 전처리 "4시간" 동안 학습 GPU 사용률 0% | RAPIDS·NVTabular로 GPU에서 바로 읽고 전처리, 중간 저장 없이 메모리 포인터만 PyTorch로 넘김(zero-copy) | 전처리 "8시간에서 15분", GPU 활용률 80~90% 이상 |
| 2. 공간 조인 (p338–339) | 수백만 라이더·차량 위치와 수만 개 행정동 폴리곤을 수십~수백 대 CPU Spark로 | cuSpatial로 GPU에서 | CPU 노드 50대의 일을 A100 1장이 수 분에, TCO 최대 70~80% 절감 |
| 3. 실시간 로그 파싱 (p340–341) | 초당 수십만 건 웹 로그에 정규식, Logstash나 Spark Streaming이 못 따라가 Kafka에 적체되고 15분 마이크로 배치로 타협 | cuDF 문자열 연산으로 병렬 정규식 | backpressure 해소, "수 초 이내" 탐지의 "진정한 실시간(Sub-second)" |

### 03. RAPIDS 생태계 (p342–348)

- cuDF(Arrow 기반 GPU DataFrame, `import cudf`), cudf.pandas(매직 커맨드·`python -m cudf.pandas`, 자동 CPU fallback), Dask-cuDF(파티션을 여러 GPU·노드에 나눠 VRAM 한계 극복), Spark RAPIDS(플러그인 jar와 설정, Catalyst 물리 계획 교체, UCX·RDMA 셔플), RMM(GPU 메모리 풀 할당자)을 설명하고 비교표로 정리한다(p342–348).

### 04. 분산 GPU ETL (p349–352)

- Spark RAPIDS에서 가속되는 영역(SQL·DataFrame, scan·filter·projection, join·aggregation·sort 일부, Parquet·ORC, GPU shuffle)과 제한 영역(RDD, 미지원 SQL, 일부 UDF, 행 기반 처리, fallback이 많은 plan)(p349–350).
- 분산 ETL의 병목은 join·aggregation·repartition·sort의 shuffle과 네트워크다. GPU shuffle은 데이터를 GPU 위에 오래 두고 host memory 경유를 줄인다. 연산만 빠르게 해서는 부족하고 셔플 경로까지 GPU 친화적으로 설계해야 한다(p351–352).

### 05. MLOps에서의 RAPIDS (p353–356)

- 피처 엔지니어링 단계 표(p354): 원본 로그 정제 → 사용자·item·session feature → 기준 시점 기반 label join → negative sampling(anti-join) → 스냅샷으로 offline feature table.
- 배치 추론 단계 표(p356): scoring 대상 추출 → 입력 feature 조립(key join, snapshot) → 모델 입력 변환(null·type·컬럼 순서) → GPU 메모리 기준 batch 구성 → 결과 재결합(key, model_version) → 결과 집계(score 분포, rank, top-k).

## 핵심

- 판단 질문 다섯 개(p334–335)와 "애매한 작업" 목록(p333)이 이 소단원의 쓸모 있는 부분이다. 구성 요소와 현재 상태는 [[RAPIDS]]에, 이유가 되는 하드웨어 원리는 [[GPU 아키텍처]]에 있다.
- p352의 "연산만 빠르게 해서는 부족"은 [[AI DE 강의 4-01 분산 처리의 등장과 도입 판단]]의 네트워크·셔플 지표(p29)와 같은 문제를 GPU 쪽에서 다시 말한 것이다. 이 연결은 위키의 관찰이다.
- p354의 "기준 시점 기반 조인"은 [[데이터 누수]]와 [[피처 스토어]]의 point-in-time join이다. 강의는 이름만 쓰고 이유를 설명하지 않는다.

## 주의·결함

- ❌ 사례 1의 수치가 한 장 사이에 바뀐다. AS-IS는 전처리 "4시간"(p336)인데 TO-BE의 효과는 "8시간에서 15분"(p337)이다.
- 사례 세 개의 수치(8시간 → 15분, 활용률 80~90%, CPU 50대 → A100 1장, TCO 70~80%)에 출처가 없다. 어느 회사의 어떤 데이터인지, 벤치마크인지 가상 사례인지 밝히지 않는다.
- 사례 3 안에서 "수 초 이내에 위협을 탐지"와 "진정한 실시간(Sub-second)"(p341)이 어긋난다. "CPU는 한 번에 하나의 문자열 패턴만 검사"(p340)도 멀티코어·SIMD를 무시한 단순화다(위키의 판단).
- ❌ 사례 2의 cuSpatial은 RAPIDS 25.06부터 배포가 중단됐고 저장소는 2025-07-28 보관됐다. 슬라이드 작성(2026-05) 전의 일이다. [https://docs.nvidia.com/datascience/notices/rsn0045/index.html , 2026-09-28 확인]
- ⚠️ 사례 1의 NVTabular는 2023-08 이후 릴리스가 없다([[RAPIDS]]).
- ❌ cuDF가 Arrow 기반이라 "GPU-CPU 간 … 데이터 전송이 매우 빠름"(p342)은 과장이다. Arrow는 형식 변환을 줄일 뿐 PCIe 복사는 남는다. 같은 강의가 이 복사를 최대 병목으로 든다(4-11 p266, 이 소단원 p329).
- ⚠️ Spark RAPIDS 셔플을 UCX·RDMA로만 설명한다(p346). 현재 기본은 MULTITHREADED 모드이고 UCX는 RDMA 환경의 선택지다. [https://docs.nvidia.com/spark-rapids/user-guide/latest/additional-functionality/rapids-shuffle.html , 2026-09-28 확인]
- ✅ "기본 할당자(cudaMalloc)는 … 동기화 오버헤드 큼"(p347)은 맞다. NVIDIA 블로그가 기존 할당·해제를 "device-synchronizing global operations"라 부르고, 그 대안으로 CUDA 11.2의 `cudaMallocAsync`를 소개한다. 강의는 이 대안을 말하지 않는다. [https://developer.nvidia.com/blog/using-cuda-stream-ordered-memory-allocator-part-1/ , 2026-09-28 확인]
- ✅ cudf.pandas의 사용법(p343)과 자동 fallback, Spark RAPIDS의 플러그인 설정과 CPU fallback은 공식 문서와 맞다.
- 중복: p343 = p344. 생태계 설명이 앞 소단원([[AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용]] p310–313)과 겹친다.
- 덱 `01`은 이 소단원으로 끝나고, Ch1~4 전체를 정리하는 슬라이드가 없다.

## 관련

- 개념: [[GPU 아키텍처]] · [[피처 스토어]] · [[데이터 누수]] · [[MLOps]] · [[모델 서빙]] · [[행 기반과 열 기반 저장]]
- 엔티티: [[RAPIDS]] · [[Apache Spark]] · [[Apache Parquet]]
- 이전 강의: [[AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용]]
- 다음 강의: [[AI DE 강의 4-15 AI 시스템 지표와 SLA]]

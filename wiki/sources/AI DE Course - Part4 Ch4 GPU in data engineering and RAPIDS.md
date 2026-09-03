---
type: source
title: AI DE Course - Part4 Ch4 GPU in data engineering and RAPIDS
area: [data-engineering, programming]
aliases: ["Part4 Ch4-4,5", 데이터 엔지니어링에 GPU 활용하기, RAPIDS를 활용한 가속 ETL]
tags: [data-engineering, course, fast-campus, gpu, rapids, cudf, spark-rapids, nvtabular, mlops, batch-inference]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf (p302–356)"]
---

# AI DE Course - Part4 Ch4 GPU in data engineering and RAPIDS

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 4** Ch4의 소단원
**4 "데이터 엔지니어링에 GPU 활용하기"** + **5 "RAPIDS를 활용한 가속 ETL 처리"**.
원본(로컬): `raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` **p302–356** (356p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> **소단원 4가 "어디에 쓰나"(범위와 판단 기준), 소단원 5가 "무엇으로 하나"(RAPIDS 생태계와 사례)다.**
> 판단 기준이 상당 부분 중복되어 한 페이지로 묶었다.
>
> ⭐ **이 소단원의 진짜 논지는 GPU 가속이 아니라 [[Feature store]]·[[MLOps]] 연결이다** —
> **"MLOps 추적 없이 단발성 가속만 수행"** 을 실패 사례로 꼽는다.

## 구성

소단원 4: `01 데이터 엔지니어링에서 GPU 활용 범위 · 02 GPU 가속 ETL, Feature Engineering ·
03 학습 추론 입력 파이프라인 가속 · 04 모델 서빙과 MLOps 운영 데이터 흐름 ·
05 GPU 데이터 파이프라인 설계 판단 기준`
소단원 5: `01 RAPIDS · 02 RAPIDS 활용 사례 · 03 RAPIDS 생태계 · 04 분산 GPU ETL ·
05 MLOps에서의 RAPIDS`

## DE의 GPU 활용 위치

> **"현대 데이터 엔지니어링은 MLOps 데이터 흐름까지 확장. 모델 학습·추론·피처 생성·임베딩 생성·
> 모니터링·재학습 데이터 생성이 하나의 파이프라인으로 연결."**

| 활용 위치 |
|---|
| GPU 가속 ETL |
| GPU 기반 feature engineering |
| 학습 입력 파이프라인 가속 |
| 대량 batch inference |
| **embedding generation** |
| 모델 서빙 로그 처리 |
| 모니터링·드리프트 분석용 데이터 파이프라인 |

**데이터 엔지니어가 맡는 MLOps 데이터 흐름 8단계:** 원천 데이터 수집 → 학습 데이터셋 생성 →
피처 계산과 저장 → 배치 추론 입력 생성 → 임베딩 생성 파이프라인 운영 → 추론 로그 적재 →
모델 품질 모니터링 데이터 생성 → **재학습 트리거용 데이터 구성**.

### ⭐ MLE와의 협업 경계

| 역할 | 책임 |
|---|---|
| **MLE** | 모델 구조, 학습 코드, 평가 지표, 서빙 요구 정의 |
| **데이터 엔지니어** | **입력 데이터 품질, 피처 정합성, 파이프라인 확장성, 저장·재처리·모니터링 설계** |
| **MLOps 공통 영역** | 모델 버전, 데이터 버전, 추론 결과, 운영 메트릭 연결 |

> **"MLOps는 모델 코드만이 아니라 데이터 계층과 모델 계층의 연결 문제."**

도구로 **MLflow Model Registry**(lineage·versioning·aliasing·metadata tagging)와
**Feast**(offline store는 학습 데이터·피처값 생성, online store는 실시간 추론용 최신 피처 제공)를
든다.

> **[[Feature store]]의 offline/online 이원 구조가 여기서 다시 나온다.** Part 2 Ch5에서 개념으로
> 배운 것이 여기서 **DE의 구현 책임**으로 되돌아온다.

### GPU 활용을 판단하는 세 가지 질문

1. **데이터 처리가 대량 병렬 연산인가?** — 큰 DataFrame 변환, join/group by/filtering,
   벡터·행렬 연산, 이미지·영상·음성 전처리, 대량 batch inference
2. **데이터 이동 비용보다 GPU 계산 이득이 큰가?** — GPU로 올리고 내리는 비용, **작은 데이터는 CPU가
   더 단순하고 빠를 수 있음**, GPU 메모리 용량과 batch size
3. ⭐ **MLOps 운영 흐름과 연결되는가?** — 피처 저장소·모델 버전·추론 로그·모니터링/재학습 흐름과 연결

> ⭐ **3번이 다른 GPU 가속 자료와 이 소단원을 구별한다.** "빨라지나"가 아니라 **"운영 흐름에
> 들어가나"** 를 판단 기준으로 세운다. 소단원 5의 실패 목록에도 **"MLOps 추적 없이 단발성 가속만
> 수행"** 이 들어간다.

## GPU 가속 도구 3종 (소단원 4)

| 도구 | 역할 | DE 관점의 의미 |
|---|---|---|
| **cuDF** | GPU에서 동작하는 DataFrame 처리. pandas·Polars·Spark 계열 워크플로우 가속. **필터링·join·group by·aggregation 같은 대량 컬럼 연산에 적합** | 모델 학습 전 feature table 생성, 대용량 로그 전처리, batch inference 입력 가공, 통계·집계 피처 생성 |
| **Spark RAPIDS** | Spark SQL/DataFrame 연산을 GPU에서 실행. **plugin 방식으로 기존 앱 수정 없이 적용.** 미지원 연산은 CPU 경로로 **fallback** | 이미 Spark 기반 Lakehouse/Batch ETL이 있는 조직에 자연스러움. **CPU Spark 클러스터를 전부 버리지 않고 가속 구간부터 적용 가능.** ⚠️ **RDD 직접 조작 중심의 오래된 코드는 가속 효과 제한** |
| **Dask-cuDF / NVTabular** | Dask-cuDF는 Dask DataFrame 백엔드로 cuDF 사용 → **multi-GPU / multi-node**. NVTabular는 **추천 시스템용 feature engineering에 특화**, terabyte-scale recommender dataset 대상 | pandas/cuDF 감각을 분산 GPU 처리로 확장 |

## ⭐ 학습이 느린 진짜 이유 — 입력 파이프라인

> ⭐ **"GPU는 빠르게 계산할 준비가 되어 있다. 하지만 데이터 로딩, 디코딩, resize, crop,
> augmentation, tokenization, batch 구성에서 병목이 발생할 수 있다.
> 모델 학습 병목이 모델 연산이 아니라 데이터 공급일 수 있다."**

**데이터 엔지니어의 역할 6가지:** 학습 데이터 포맷 설계 · **파일 크기와 shard 설계** ·
batch 구성 전략 · **streaming read와 prefetch** · CPU/GPU 전처리 분리 ·
재현 가능한 dataset version 관리.

> **이 목록이 DE가 ML 학습에 기여하는 가장 구체적인 지점이다.** "모델은 MLE가, 데이터는 DE가"라는
> 경계가 **shard 크기와 prefetch**라는 실물로 내려온다.

### Batch inference와 embedding generation

용도: 대량 문서 embedding 생성 · 이미지 feature extraction · 사용자 로그 기반 예측값 생성 ·
재학습 후보 데이터 생성 · offline scoring · **vector database 적재 전 embedding pipeline**.

핵심 설계 요소: batch size · GPU memory 한계 · **모델 로딩 비용** · 재시도와 checkpoint ·
결과 저장 포맷 · **모델 버전과 데이터 버전 연결**.

> **"vector database 적재 전 embedding pipeline"이 [[Unstructured data ingestion]](Part 1)과
> [[Retrieval-augmented generation]](Part 3)을 잇는다.** RAG 인덱싱이 곧 대량 batch inference라는
> 관점인데, **강의가 이 연결을 명시하지 않는다.**

### 서빙 도구

| 도구 | DE 관점의 연결 |
|---|---|
| **Triton** | 여러 프레임워크 모델 서빙, 실시간·batch·ensemble·streaming query. **추론 입력 데이터 포맷 표준화, 서빙 로그 적재, request/response schema 관리, 모델 버전별 결과 비교** |
| **KServe** | K8s 기반 inference serving. `InferenceService` 리소스, **Knative 기반 모드에서 요청량 기반 autoscaling**. ⭐ **"GPU 서빙 자원은 batch ETL GPU 자원과 분리 설계 필요 — latency SLA와 batch throughput 요구를 구분해야 함"** |

> ⭐ **"추론 서비스도 데이터 파이프라인의 일부. 추론 결과는 모니터링·분석·재학습 데이터로 다시
> 유입된다."** — [[MLOps]]의 순환 구조가 DE 언어로 표현된다.
>
> **KServe가 Part 2에서 "로고로만 등장하고 설명이 없다"고 남긴 공백이 여기서 조금 채워진다.**
> InferenceService·Knative autoscaling까지는 나오지만 여전히 얕다.

### DE와 MLE가 합의해야 할 인터페이스 3종

| 인터페이스 | 항목 |
|---|---|
| **데이터** | 입력 schema · feature definition · label definition · partition 기준 · batch size 기준 · **데이터 버전** |
| **모델** | model version · input/output schema · inference batch format · latency/throughput 요구 · **fallback 정책** |
| **운영** | 추론 로그 schema · 모니터링 지표 · **drift 계산 기준** · **재학습 트리거 조건** · 장애 재시도 기준 · **비용 budget** |

> ⭐ **이 3표가 소단원 4의 최고 산출물이다.** [[ML data pipeline]](Part 2)이 "라벨은 파이프라인의
> 일부"였다면, 여기는 **DE와 MLE 사이의 계약서 목록**을 준다. Part 3의
> [[AI DE Course - Part3 Ch3 SHACL and graph data contracts]]가 그래프용 데이터 계약이었던 것과
> 같은 계열의 사고인데, **강의가 "데이터 계약"이라는 말을 여기서 쓰지 않는다.**

---

## RAPIDS (소단원 5)

### 왜 필요한가 — GPU Starvation

> **"데이터는 커지는데 모델 학습 준비 시간에 오랜 시간이 소요."**

| 문제 | 내용 |
|---|---|
| **CPU의 한계** | 데이터 로딩, 전처리(Pandas), 피처 엔지니어링 단계가 CPU에서 처리되며 극심한 지연 |
| **PCIe 병목** | 전처리가 끝난 데이터를 CPU 메모리 → GPU 메모리로 넘기는 과정(복사·직렬화/역직렬화)에서 심각한 병목. **GPU는 빠르지만 데이터를 기다리느라 놀고 있는 상태(Starvation)** |

> **"MLOps 관점에서는 ETL 병목이 모델 실험 속도, 재학습 주기, 배치 추론 처리량까지 직접 영향."**

### GPU ETL이 잘 맞는 / 애매한 작업

| 잘 맞음 | 애매함 |
|---|---|
| 대량 필터링 · 대량 조인 · group by 집계 | 데이터 크기가 작음 |
| **컬럼 단위 변환** | **Python UDF가 많음** |
| **Parquet / ORC 기반 분석형 처리** | **분기와 문자열 처리 중심** · row 단위 복잡 로직 |
| 대용량 feature table 생성 | **입출력 파일이 지나치게 작고 많음** |
| batch inference 입력 데이터 전처리 | CPU fallback이 많은 Spark job |
| 반복적인 벡터·수치 연산 | GPU로 올리고 내리는 비용이 계산 이득보다 큼 |

**판단 질문 5가지:**

1. 이 ETL은 **컬럼 단위 대량 연산**인가? (filter, projection, join, group by, aggregation 중심이면 후보)
2. **GPU 메모리에 맞는 batch/partition 설계가 가능한가?** (큰 데이터라도 처리 단위가 너무 크면 OOM)
3. **CPU fallback이 적은가?** (Spark RAPIDS에서 미지원 연산이 많으면 GPU 효과 감소)
4. **작은 파일이 너무 많지는 않은가?** (수 GB 단위의 큰 입력 파일이 유리)
5. ⭐ **결과가 MLOps 흐름과 연결되는가?** (feature store, batch inference, model monitoring,
   retraining dataset과 연결되면 가치 증가)

> **4번이 [[Columnar and in-memory data formats]](Part 1)의 compaction 논의와 이어진다** —
> small file problem이 GPU ETL에서 더 치명적이라는 뜻이다.

### RAPIDS 생태계

| 기술 | 처리 주체 | 데이터 규모 | 적용 대상 | 코드 수정 |
|---|---|---|---|---|
| **cuDF** | 단일 GPU | 단일 GPU VRAM 이내 | 고속 Tabular ETL | **API 변경 필요** (`pandas` → `cudf`) |
| **cudf.pandas** | 단일 GPU / CPU | 단일 GPU VRAM 이내 | 기존 pandas 유저의 손쉬운 가속 | **없음** (매직 커맨드만) |
| **Dask-cuDF** | 다중 GPU / 노드 | **단일 GPU VRAM 초과** | 단일 GPU 한계 극복, 분산 처리 | API 변경 필요 |
| **Spark RAPIDS** | 다중 GPU / 노드 | 클러스터 기반 빅데이터 | 기존 Spark 워크로드 고속화 | **없음** (플러그인 설정만) |
| **RMM** | GPU 메모리 관리 | — | 위 기술들의 **메모리 병목 및 파편화 방지** | — (보통 내부적으로 자동 구동) |

**세부:**

- **cuDF** — **Apache Arrow 기반** 컬럼형 in-memory 표현. **직렬화/역직렬화 오버헤드 없이**
  GPU↔CPU 간, 다른 도구 간 데이터 전송이 매우 빠름
- **cudf.pandas** — **스마트 폴백**: GPU 지원 연산이면 cuDF로, 미지원 연산이나 UDF면 자동으로
  pandas로 전환. `%load_ext cudf.pandas` 또는 `python -m cudf.pandas script.py`
- **Dask-cuDF** — 거대한 DataFrame을 cuDF 파티션으로 쪼개 multi-GPU / multi-node에 분산.
  **OOM 해결** — TB 단위 데이터셋도 처리
- **Spark RAPIDS** — **Catalyst Optimizer 개입**: Spark의 **물리적 실행 계획 단계를 가로채서**
  CPU에서 실행되던 Sort/Join/Aggregate를 GPU 연산으로 대체. 셔플에서 **UCX나 RDMA**로 네트워크
  병목 감소
- **RMM** — GPU 전용 **메모리 풀 할당자**. `cudaMalloc`은 시스템 콜이 발생해 느리고 동기화
  오버헤드가 큼. **DataFrame 처리처럼 수많은 중간 배열이 생성·폐기되는 작업에 치명적** → 프로그램
  시작 시 풀을 미리 선점

> ⭐ **cuDF가 Arrow 기반이라는 점이 Ch4-1,2의 coalescing과 직결된다.** *"컬럼 기반 포맷이 GPU와
> 어울리는 이유는 연속된 메모리 접근"* → cuDF가 Arrow를 쓰는 이유가 그것이다. **강의가 두 소단원에
> 나눠 말하고 잇지 않지만, 이 위키에서는 [[GPU architecture]]와 [[NVIDIA RAPIDS]]가 이 고리로
> 연결된다.**
>
> **RMM 항목이 특히 좋다** — 왜 별도 할당자가 필요한지(cudaMalloc의 시스템 콜 + 동기화)를
> DataFrame 워크로드 특성(중간 배열 대량 생성)과 묶어 설명한다.

### 분산 GPU ETL — 가속되는 것과 안 되는 것

| 가속 가능성이 큰 영역 | 가속 제한 영역 |
|---|---|
| Spark SQL · DataFrame API | **RDD 직접 조작** |
| 컬럼형 연산 · scan, filter, projection | 미지원 SQL 연산 |
| join, aggregation, sort 일부 | 일부 UDF |
| **Parquet / ORC 기반 처리** | 복잡한 row 기반 처리 |
| **GPU shuffle 사용 시 대규모 데이터 이동 최적화** | **CPU fallback이 많은 plan** |

**GPU shuffle의 목표:** 데이터를 가능한 한 GPU 위에 오래 유지 · CPU와 host memory 경유 비용 감소 ·
GPU 간 데이터 이동 최적화.

> ⭐ **"GPU ETL은 연산만 빠르게 해서는 부족. 분산 ETL에서는 shuffle과 network 경로까지 GPU
> 친화적으로 설계해야 한다."**
>
> **이것이 Ch1-1 MapReduce의 shuffle 논의가 GPU 시대에 되돌아온 형태다.** 분산 처리의 병목은
> 20년째 shuffle이다.

### MLOps에서의 RAPIDS — 파이프라인 표 2종

**Feature Engineering 단계표:**

| 단계 | 입력 | 변환 | 출력 |
|---|---|---|---|
| 원본 로그 정제 | raw event log | 필터링, 중복 제거, 타입 변환 | clean event log |
| 사용자 feature | clean event log | `user_id` 기준 집계 | user feature table |
| item feature | click/order/impression log | `item_id` 기준 통계 계산 | item feature table |
| session feature | timestamped event log | `session_id` 기준 행동 요약 | session feature table |
| **label join** | feature table + label table | **기준 시점 기반 조인** | training table |
| negative sampling | user-item 후보 | anti-join, sampling | negative sample table |
| offline feature table | 여러 feature table | join, snapshot 생성 | 학습용 feature table |

> ⭐ **"label join — 기준 시점 기반 조인"** 이 [[Data drift and training-serving skew]]의
> **skew 패턴 1(시간 기준 불일치)** 과 정확히 같은 지점이다. point-in-time correctness라는 용어는
> 안 쓰지만 그 이야기다. **Part 2 Ch3의 skew 논의와 잇지 않는 것이 아쉽다.**

**Batch Inference 단계표:**

| 단계 | 입력 | 변환 | 출력 |
|---|---|---|---|
| scoring 대상 추출 | 사용자·상품·문서 원본 테이블 | 필터링, 후보군 선별 | inference target table |
| 입력 feature 조립 | user/item/session feature table | **key 기준 join, snapshot 선택** | model input table |
| 모델 입력 변환 | model input table | **null 처리, type 변환, 컬럼 순서 정렬** | inference batch |
| batch 구성 | inference batch | **GPU memory 기준 chunking** | batch files / batch dataframe |
| 결과 재결합 | model output + 원본 key | key join, **model_version 추가** | prediction table |
| 결과 집계 | prediction table | 모델별 score 분포, rank, top-k | monitoring / serving table |

> **"null 처리, type 변환, 컬럼 순서 정렬"이 명시된 게 좋다** — skew 패턴 3(결측 처리)의 실제
> 작업 위치가 여기다.

## ⚠️ 실무 활용 사례 3건 — 수치를 그대로 쓸 수 없다

| 사례 | AS-IS | TO-BE | 주장된 효과 |
|---|---|---|---|
| **1. 추천 시스템 피처 엔지니어링** | 100GB 유저 로그를 CPU Spark로 전처리 → Parquet 저장 → PyTorch로 재로딩. **전처리에 4시간**, 그동안 학습 GPU 사용률 0% (**GPU Starvation**) | RAPIDS/NVTabular로 GPU에서 바로 읽어 전처리, 중간 저장 없이 **메모리 포인터만 PyTorch로 넘김(Zero-copy)** | ⚠️ **"전처리 시간이 8시간에서 15분으로 단축"**, GPU 활용률 80~90% |
| **2. 대규모 공간/위치 데이터 (Geospatial Joins)** | 수백만 라이더·차량 위치 × 수만 개 행정동 폴리곤 교차 계산. 기하학적 연산은 CPU 최악 → 수십~수백 대 Spark 클러스터 | RAPIDS/**cuSpatial**로 좌표와 다각형을 GPU 메모리에 올려 병렬 계산 | ⚠️ **"50대의 CPU 노드가 풀던 문제를 A100 1장이 수 분에", 유지보수 포인트 50 → 1, TCO 70~80% 절감** |
| **3. 실시간 텍스트/로그 파싱 (보안/옵저버빌리티)** | 초당 수십만 건 웹 로그에 복잡한 정규표현식. CPU는 한 번에 하나의 패턴만 → Kafka 큐에 적체 → **'15분 단위 마이크로배치'로 타협** | **cuDF String 연산**으로 수천 스레드가 수만 줄을 동시에 스캔·정규식 매칭 | ⚠️ Backpressure 소멸, **"15분 뒤 인지"에서 "수 초 이내 탐지"로** |

> ⚠️⚠️ **사례 1에 내부 모순이 있다.** AS-IS 슬라이드(p336)는 **"전처리에 4시간이 소요될 수 있음"**,
> TO-BE 슬라이드(p337)는 **"전처리 시간이 8시간에서 15분으로 단축"** 이라고 한다. **연속된 두
> 슬라이드에서 4시간 vs 8시간이 어긋난다.** 어느 쪽도 출처가 없다.
>
> ⚠️ **세 사례 모두 출처가 없다.** 회사명·벤치마크 조건·데이터 규모의 정확한 정의가 없다.
> 사례 2의 "TCO 70~80% 절감"과 "50대 → 1대"는 NVIDIA 마케팅 자료에서 흔히 보는 형태의 주장이고,
> **강의가 이를 자사/벤더 주장이라고 밝히지 않는다** — Part 3가 Neo4j·Microsoft 수치에 대해
> "자사 비교"라고 명시했던 것보다 **후퇴했다.**
>
> **다만 사례들이 가리키는 워크로드 성격은 타당하다** — geospatial join과 대량 정규식은 실제로
> 임베러싱리 패럴렐하고 산술 집약도가 높아 GPU에 잘 맞는다. **방향은 맞고 수치는 못 쓴다.**

## 기존 페이지와의 대조

- **새 entity:** [[NVIDIA RAPIDS]]
- **[[Feature store]] 보강** — offline feature table 생성 파이프라인의 실제 단계표가 여기 있다.
- **[[ML data pipeline]](Part 2)** — label join, negative sampling, dataset version이 구체화된다.
- **[[Inference optimization]]** — batch inference의 chunking·모델 로딩 비용.
- **[[Columnar and in-memory data formats]]** — cuDF가 Arrow 기반이라는 점, small file problem.
- **[[Data drift and training-serving skew]]** — label join의 "기준 시점"이 skew 패턴 1.
- ⚠️ **[[Model serving platforms]]** — KServe가 처음으로 조금 설명된다(여전히 얕음).

## 자료 품질

- ✅ **"MLOps 흐름과 연결되는가"를 GPU 도입 판단 기준으로** 세운 것 — 이 소단원의 독자적 기여
- ✅ **DE/MLE 인터페이스 3표**와 **파이프라인 단계표 2종**이 실무에서 바로 쓸 수 있는 형태
- ✅ RAPIDS 생태계 비교표의 축(처리 주체 / 데이터 규모 / 적용 대상 / **코드 수정 필요성**)이 실용적
- ✅ **RMM의 존재 이유**(cudaMalloc의 시스템 콜·동기화 오버헤드)를 정확히 설명
- ✅ Spark RAPIDS가 **Catalyst physical plan을 가로챈다**는 메커니즘 설명이 정확
- ⚠️⚠️ **사례 1의 4시간 vs 8시간 내부 모순**
- ⚠️ **세 사례 모두 출처 없음**, 벤더 마케팅 수치 형태인데 그렇다고 밝히지 않음
- ⚠️ **cuML·cuGraph가 생태계 표에 없다** — RAPIDS의 주요 구성요소인데 cuSpatial만 사례에서 언급
- ⚠️ **비용 비교가 없다** — "A100 1장이 CPU 50대를 대체"라면 A100 시간당 단가 × 시간 vs CPU 노드
  단가 × 시간을 비교해야 TCO 주장이 성립하는데 그 계산이 없다
- ⚠️ 중복 슬라이드: p343/p344 완전 동일

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[GPU architecture]] · [[GPU resource allocation]] · [[Feature store]] ·
  [[ML data pipeline]] · [[MLOps]] · [[Inference optimization]] ·
  [[Columnar and in-memory data formats]] · [[Data drift and training-serving skew]]
- 도구: [[NVIDIA RAPIDS]] · [[Apache Spark]] · [[CUDA]] ·
  [[NVIDIA Triton Inference Server]] · [[Model serving platforms]]
- 앞: [[AI DE Course - Part4 Ch4 GPU allocation architecture]]
- 다음: [[AI DE Course - Part4 Ch5 AI system metrics and SLA]]

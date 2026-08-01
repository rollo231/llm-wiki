---
type: moc
title: Data Engineering
area: [data-engineering]
aliases: [데이터 엔지니어링, DE, Data Engineering MOC]
tags: [data-engineering, data-pipeline, storage, orchestration]
created: 2026-07-27
updated: 2026-08-01
sources: []
---

# Data Engineering

**data-engineering** 영역의 Map of Content. 네 갈래로 쌓이고 있다 — 파이프라인 전체를 훑는
랜드스케이프 어휘, 직무·방식의 변화(기존 DW·BI 중심 → AI·비정형 지원), **AI 모델을 지키는 운영
(품질·drift·SLA)**, 그리고 실제 저장 포맷을 파이프라인 관점에서 읽는 작업.

## 여기서 시작

[[Data landscape guide for developers]] — 데이터 팀 어휘 전체를 한 번에 훑는 지도. 아래 개념
페이지 대부분이 여기서 나왔다. 툴 이름이 처음 보이는 게 어느 단계에 속하는지 모르겠으면 여기부터.

## 파이프라인을 따라가며

1. **어디서 오고 어떻게 흐르나** — [[ETL and ELT]]
   추출·변환·적재, ELT가 순서를 바꾸는 이유(스토리지 99% 하락 + MPP), 규제 때문에 여전히 ETL을
   써야 하는 경우, 반대 방향의 reverse ETL.
   - **로그로 추출하기** — [[Change data capture]] — polling 대신 트랜잭션 로그를 읽어 소스 부하를
     피한다. Debezium·순서 보장·멱등성.
   - **비정형은 다른 파이프라인** — [[Unstructured data ingestion]] — 수집→저장→OCR·임베딩→RAG.
2. **어떤 바이트로** — [[Columnar and in-memory data formats]]
   Parquet은 스캔 최적화(predicate pushdown), Arrow는 처리 최적화, Avro는 쓰기·스키마 진화.
   **고르는 게 아니라 단계별로 갈아탄다**(Avro로 받고 Parquet으로 묶기).
3. **어디에 담나** — [[Analytical data storage tiers]]
   웨어하우스 / 레이크 / 레이크하우스를 구조 강제·쿼리 엔진 결합·비용 세 축으로. + OLTP/OLAP.
4. **레이크를 레이크하우스로 만드는 층** — [[Table formats]]
   Iceberg·Delta·Hudi. ACID·스키마 진화·time travel이 왜 여기 붙는가.
   **Delta의 트랜잭션 로그 구조는 이제 안다 — Iceberg는 아직 모른다.**
5. **언제 처리하나** — [[Batch and stream processing]]
   배치 vs 스트림, Kafka가 메시지 큐와 다른 점, 그리고 **오케스트레이터는 배치 전용**이라는 경계.
   - **왜 둘 다 못 갖나** — [[Latency and throughput]] — 시소의 법칙, 마이크로배치, Lambda/Kappa.
   - **실어 오는 층** — [[Apache Kafka]] — 토픽·파티션·오프셋, 순서 보장의 범위, 로그 컴팩션.
   - **처리의 의미론** — [[Stream processing semantics]] — 윈도우·워터마크·상태·exactly-once.
6. **어떤 단계로 착지하나** — [[Medallion architecture]] (정제도: bronze/silver/gold)
   × [[Dimensional modeling]] (모양: fact·dimension·star·grain). **두 축은 직교한다.**
7. **무엇이 어디에 있고 무엇을 뜻하나** — [[Data catalog and semantic layer]]
   metastore(기계용) ≠ data catalog(사람용) ≠ semantic layer(정의용). + lineage와 거버넌스.
   카탈로그의 실패 모드는 '없음'이 아니라 '틀림'이다 → 자동화·CI/CD 강제.
8. **약속을 지키는가** — [[Data SLA and observability]]
   uptime은 데이터가 건강함을 증명하지 못한다. **침묵의 실패**, 신선도·완전성·정확성,
   관측성·경고 피로·서킷 브레이커.

## AI 모델을 지키는 쪽

파이프라인이 정상인데 모델만 망가지는 문제들. **에러 로그가 0건이라는 공통점이 있다.**

- [[Data drift and training-serving skew]] — 우리 코드가 학습/서빙에서 다르게 도는 문제(skew)와
  세상이 변하는 문제(drift). 둘은 다르고 해법도 다르다.
- [[Feature store]] — skew를 구조적으로 막는 장치. offline/online 두 스토어, 하나의 로직.
- [[Data and model versioning]] — 재현성 3요소. "무엇이 달라졌는지" 특정할 수 있어야 디버깅이 된다.

## 직무·방식

- [[Traditional data engineering]] — 정형 데이터를 DW에 적재하고 BI로 의사결정을 돕는 기존 방식.
- [[AI data engineering]] — 비정형 데이터와 모델 라이프사이클(학습·추론)을 지원하는 확장된 방식.

두 페이지는 **시간축**(기존 → AI) 분류이고, [[Data landscape guide for developers]]는 **공존축**
(analytical / scientific / engineering / ML) 분류다. 같은 지형을 다른 축으로 자른 것 — 각 페이지의
"다른 축의 분류" 절 참고.

## 저장 포맷을 파이프라인 관점으로

- [[SpatialData as a data engineering substrate]] — 공간 오믹스 포맷([[SpatialData]])을
  레이크하우스 층위로 분해하고, 그 위의 ETL·카탈로그를 설계한다. 이 영역과
  [[Bioinformatics]] 영역이 겹치는 지점.

## 출처

- [[Data landscape guide for developers]] — OlegWock, sinja.io (2026-07-14). 개발자를 위한 데이터
  랜드스케이프 가이드.

### 진행 중인 코스

**[[AI Data Engineering (Fast Campus course)]]** — 챕터 트래커(5개 파트 / 41개 덱 / ~1,155p).
**Part 1 완료(16/16), Part 2~5 대기.**

Part 1 source 페이지 — 파이프라인 순서대로:

| | 챕터 | 페이지 |
|---|---|---|
| CH01 | OT · 마인드셋 · 스택 | [[AI DE Course - Ch1-1 OT]] · [[AI DE Course - Ch1-2,3 Latency and Versioning]] · [[AI DE Course - Ch1-4 Tech stack and tooling]] |
| CH02 | 저장 | [[AI DE Course - Ch2-1,2,3 Storage evolution]] · [[AI DE Course - Ch2-4,5,6 Parquet and Avro]] · [[AI DE Course - Ch2-7 Delta Lake and ACID]] |
| CH03 | 수집 | [[AI DE Course - Ch3-1,2 Batch and ETL]] · [[AI DE Course - Ch3-3,4 CDC]] · [[AI DE Course - Ch3-5,6 Unstructured data ingestion]] |
| CH04 | 처리 | [[AI DE Course - Ch4-1,2 Batch vs Streaming]] · [[AI DE Course - Ch4-3,4 EDA and Kafka]] · [[AI DE Course - Ch4-5,6 Stream processing engines]] |
| CH05~08 | 운영 | [[AI DE Course - Data drift and training-serving skew]] · [[AI DE Course - Data SLA and pipeline monitoring]] · [[AI DE Course - Data governance and catalog]] · [[AI DE Course - AI pipeline case studies]] |

> ⚠️ **이 코스의 수치는 인용 주의.** "데이터의 80%가 비정형", "배치가 워크로드의 80%",
> "탐색에 80% 시간", "데이터 준비 70%+", "개발 시간 70% 단축", "PSI > 0.2" — **어디에도 출처가
> 없고 일부는 서로 다른 회사 사례에 같은 수치가 붙어 있다.**
> → [[AI DE Course - AI pipeline case studies]]의 '검증 필요' 절.

## 열린 질문

이 영역이 자라면서 파볼 지점. **✅는 Part 1 인제스트로 해소된 것, ⚠️는 부분 해소.**

- ⚠️ **Iceberg 1차 문서가 필요하다.** **여전히 1순위.** Part 1로 **Delta의 트랜잭션 로그 구조는
  채워졌다**(`_delta_log/000000.json`, Add/Remove, optimistic concurrency, 체크포인트) →
  [[Table formats]]. 하지만 **Iceberg의 스냅샷·매니페스트 구조와 세 포맷의 선택 기준은 그대로 비어
  있다** — 강의는 Delta만 다루고 Iceberg·Hudi를 언급조차 하지 않는다.
  [[SpatialData as a data engineering substrate]] §4는 Iceberg를 전제하므로 **검증에 필요한 쪽이
  아직 없다.**
- **오케스트레이터 비교**(Airflow vs Dagster vs Prefect·Argo) — **진전 없음.** 강의도 Airflow만
  이름을 대고 비교하지 않는다. 배치 안에서 무엇을 고를지의 기준은 여전히 근거가 없다.
- ⚠️ **직무 구분의 실제 경계** — 시간축(강의)과 공존축(랜드스케이프 가이드) 중 어느 쪽이 현업인지.
  강의가 [[AI DE Course - Ch1-4 Tech stack and tooling]]에서 "현업 채용 공고 분석"을 제시하지만
  **출처 표기가 없어 1차 자료로 못 쓴다.** 실제 JD나 팀 구성 사례가 필요하다.
- ✅ **비정형 데이터의 "텐서 변환·저장" 실무** — [[Unstructured data ingestion]]으로 채워졌다:
  4단계 골격, S3+NoSQL 이원화, OCR, 임베딩 모델 선정, Vector DB·ANN·reranking.
  → 남은 갈래: **공간 오믹스의 Zarr 지식이 여기로 일반화되는가** (청크 배열 vs 벡터 인덱스는
  다른 물건으로 보인다).
- ⚠️ **데이터 품질·관측성의 실제 도입** — **프로세스는 채워졌다**([[Data SLA and observability]]:
  SLA 명세·3대 지표·관측성·경고 피로·RCA·서킷 브레이커). 하지만 **제품 선택의 갈림은 그대로다** —
  강의에 Great Expectations·dbt tests·Monte Carlo·Bigeye가 **한 번도 나오지 않는다.**
  "ML 기반 이상 탐지"를 지향점으로 말하면서 도구를 지목하지 않는다.
- ⚠️ **semantic layer는 실제로 쓰이는가** — 채택률·실패 사례 근거는 여전히 없다. 다만 새 관점이
  생겼다: 강의는 semantic layer라는 **용어를 쓰지 않고**, 같은 문제("이 컬럼의 '가격'은 세금
  포함인가?")를 **카탈로그 + LLM 자동 태깅 + Text-to-SQL**이 흡수하는 그림을 제시한다.
  → **두 접근(정의를 명시적으로 못박기 vs LLM이 추론하기)이 경쟁 관계인지 확인할 가치가 있다.**

### Part 1이 새로 남긴 질문

- **Feature Store가 skew를 정말 없애나** — offline·online 두 스토어를 두는 순간 **두 스토어 간
  일치**가 새로운 보장 대상이 된다. 강의 Part 1은 "Write Once, Compute Anywhere"로 넘어간다.
  → **Part 2 Ch5 "Feature Store은 만능이 아니다"** 가 답할 예정. [[Feature store]]
- **케이스 스터디의 1차 자료** — Uber Michelangelo·Netflix Keystone·Meta FBLearner·Google TFX·
  Airbnb Bighead. 강의의 수치는 출처가 없고 회사 간 중복된다. **엔지니어링 블로그·논문 인제스트
  후보.** [[AI DE Course - AI pipeline case studies]]
- **ORC vs Parquet** — 두 소스 모두 "같은 문제를 푸는 다른 포맷"에서 멈춘다.
  [[Columnar and in-memory data formats]]
- **`PSI > 0.2` 임계값의 근거** — 강의가 재학습 트리거 기준으로 제시하지만 도출 방식이 없다.
  [[Data drift and training-serving skew]]
- **스트리밍은 정말 랜덤 I/O인가** — 강의 내부 모순. CH04-1,2는 그렇게 일반화하는데 CH04-3,4의
  Kafka는 순차 쓰기다. → [[Latency and throughput]]에 정리해뒀지만 벤치마크 근거는 없다.

## 링크

- 인접 영역 MOC: [[Bioinformatics]]

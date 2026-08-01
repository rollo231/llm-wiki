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

**data-engineering** 영역의 Map of Content. 여섯 갈래로 쌓이고 있다 — 파이프라인 전체를 훑는
랜드스케이프 어휘, 직무·방식의 변화(기존 DW·BI 중심 → AI·비정형 지원), **AI 모델을 지키는 운영
(품질·drift·SLA)**, **모델을 학습시키고 서빙하는 쪽(MLOps·서빙·추론 자원)**,
**데이터의 의미를 설계하는 쪽(시멘틱·그래프·온톨로지·GraphRAG)**, 그리고 실제 저장 포맷을 파이프라인
관점에서 읽는 작업.

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
  **skew 4패턴**(시간 기준·집계 범위·결측 처리·스케일링)이 진단의 출발점.
- [[Feature store]] — skew를 막는 장치. offline/online 두 스토어, 하나의 로직.
  단, **"공용 변환 로직 → Feature Contract → (필요시) Feature Store"** 중 마지막 수단이다.
- [[Data and model versioning]] — 재현성 3요소. "무엇이 달라졌는지" 특정할 수 있어야 디버깅이 된다.

## 모델을 학습시키고 서빙하는 쪽

**Part 2가 새로 연 갈래.** 데이터의 *이동*이 아니라 **연산의 배치**를 설계한다.

- **운영 체계** — [[MLOps]] (DevOps와 무엇이 다른가, ML 라이프사이클 6단계) →
  [[LLMOps]] (프롬프트·컨텍스트·가드레일·토큰 비용) + [[Context engineering]]
- **학습 데이터를 만드는 쪽** — [[ML data pipeline]] — 라벨링·검증·분할·리니지.
  **라벨은 파이프라인의 일부이고 가장 비싼 지점이다.**
- **추론을 내보내는 쪽** — [[Batch and online serving]] — 같은 모델도 배치냐 온라인이냐에 따라
  전혀 다른 시스템이 된다.
  - [[Model serving platforms]] — [[FastAPI]] · [[TorchServe]] · [[BentoML]] ·
    [[NVIDIA Triton Inference Server]]. 축은 **추상화 수준** 하나.
  - [[Inference optimization]] — **GPU는 마지막 수단.** Total Latency 분해 → CPU 최적화
    (quantization·pruning·distillation·[[ONNX]]) → 그래도 부족하면 GPU.

## 데이터의 의미를 설계하는 쪽

**Part 3가 새로 연 갈래.** 앞의 갈래들이 데이터를 *옮기고*(파이프라인) *배치하는*(서빙) 문제라면,
여기는 **데이터가 무엇을 뜻하는지**를 설계한다.

> **논지 한 줄: 스키마는 형식을 잡지만 의미는 별도 계층이 필요하다 → 그 계층이 시멘틱 →
> 그 구현이 그래프·온톨로지 → 그 활용이 GraphRAG.**

1. **출발점 — 저장 기술로는 안 되는 것**
   - [[Schema-centric data modeling]] — 관계형이 강했던 이유(제약이 버그를 저장 단계에서 방어,
     **정규화는 중복 제거가 아니라 업데이트 안정성**)와 무너지는 지점.
     **"규모가 커지면 스키마 합의가 병목이 된다"** — 기술 문제가 아니라 조직 합의의 비용.
   - [[NoSQL]] — 4타입과 등장 배경. 그리고 절반은 **"NoSQL이면 확장성이 자동 해결될까? 아니다"** —
     파티션 키가 시스템을 결정하고, **운영 포인트는 줄지 않고 분산된다.**
2. **의미 계층** — [[Data semantics]]
   Entity · Attribute · Relationship · **Context**. **"같은 회사에서 매출 숫자가 3개 이상 나오는
   이유: 지표가 계약이 아니라 쿼리가 된다."** [[Data catalog and semantic layer]]와 **같은 스펙트럼의
   다른 구간**이다(용어사전·카탈로그 ↔ 온톨로지·지식그래프).
3. **표현 수단** — [[Graph data model]] (node·edge·property·label, path·hop·pattern,
   **Property Graph vs RDF** 판단 6문항) → [[Graph database]] (index-free adjacency,
   **"Graph DB가 빠르다"의 정확한 의미**, 제품 4종) → [[Neo4j]] · [[Amazon Neptune]] ·
   [[ArangoDB]] · [[JanusGraph]]
4. **무엇을 담나** — [[Knowledge graph]]
   DE에게 가장 직관적인 활용처는 **메타데이터 그래프와 리니지**([[DataHub]]).
   **"lineage는 그래프로 모델링할 때 비로소 정적 문서가 아니라 탐색 가능한 운영 도구가 된다."**
5. **스키마·규칙 계층** — [[Ontology]]
   클래스·인스턴스·속성·관계·제약, RDFS/OWL, **SHACL = 그래프용 데이터 계약.**
   ⭐ **"테이블 = 클래스, 컬럼 = 속성, FK = 관계로 그대로 옮기는 것이 가장 흔한 실수."**
   그리고 절제: **"OWL은 필요한 경우가 제한적이다 — 단순 메타데이터 수집·lineage 시각화·태그 검색
   정도면 과설계."**
6. **그래서 어떻게 만드나** — [[Knowledge graph pipeline]]
   10단계(수집→정규화→식별자→엔터티 분해→매핑→RDF 생성→검증→추론→저장→**증분 갱신**).
   **"그래프는 파일 변환이 아니라 데이터 엔지니어링 파이프라인의 문제"** —
   결국 [[ETL and ELT]] 하나를 더 운영하는 일이다.
7. **활용** — [[Retrieval-augmented generation]] (한계 4종:
   **검색 단위 불일치 · retrieval-generation mismatch · Lost in the Middle · 고정 top-k**) →
   [[GraphRAG]] (MS 논문형 local/global, **현실의 4패턴**, 변형 3종, 제품화) ·
   [[Microsoft GraphRAG]]

> ⭐ **이 갈래가 [[Context engineering]](Part 2)로 되돌아온다.**
> *"Graph + AI의 성패는 모델 성능보다, AI가 읽는 운영 컨텍스트를 얼마나 정확하고 최신으로
> 구조화했는가에 달려 있다. 그 컨텍스트를 가장 잘 만들 수 있는 역할이 데이터 엔지니어다."*
> Part 2가 "Feature가 있던 자리를 컨텍스트가 대체한다"였다면, Part 3는 **"그 컨텍스트를 무엇으로
> 만드나 — 그래프로"** 라고 답한다. 강사가 다르고 서로 인용하지도 않는데 논지가 이어진다.

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
**Part 1 완료(16/16) · Part 2 완료(10/10) · Part 3 완료(15/15) · Part 4~5 대기(~471p).**

Part 1 source 페이지 — 파이프라인 순서대로:

| | 챕터 | 페이지 |
|---|---|---|
| CH01 | OT · 마인드셋 · 스택 | [[AI DE Course - Ch1-1 OT]] · [[AI DE Course - Ch1-2,3 Latency and Versioning]] · [[AI DE Course - Ch1-4 Tech stack and tooling]] |
| CH02 | 저장 | [[AI DE Course - Ch2-1,2,3 Storage evolution]] · [[AI DE Course - Ch2-4,5,6 Parquet and Avro]] · [[AI DE Course - Ch2-7 Delta Lake and ACID]] |
| CH03 | 수집 | [[AI DE Course - Ch3-1,2 Batch and ETL]] · [[AI DE Course - Ch3-3,4 CDC]] · [[AI DE Course - Ch3-5,6 Unstructured data ingestion]] |
| CH04 | 처리 | [[AI DE Course - Ch4-1,2 Batch vs Streaming]] · [[AI DE Course - Ch4-3,4 EDA and Kafka]] · [[AI DE Course - Ch4-5,6 Stream processing engines]] |
| CH05~08 | 운영 | [[AI DE Course - Data drift and training-serving skew]] · [[AI DE Course - Data SLA and pipeline monitoring]] · [[AI DE Course - Data governance and catalog]] · [[AI DE Course - AI pipeline case studies]] |

Part 2 source 페이지 — **학습·추론 시스템 설계**(강사 Habi):

| | 챕터 | 페이지 |
|---|---|---|
| Ch1 | 진화·역할 | [[AI DE Course - Part2 Ch1 Pipeline evolution and the DE role]] |
| Ch2 | 운영 체계 | [[AI DE Course - Part2 Ch2 MLOps and the ML lifecycle]] · [[AI DE Course - Part2 Ch2 LLMOps]] |
| Ch3 | 데이터·서빙·**skew** | [[AI DE Course - Part2 Ch3 ML data pipeline]] · [[AI DE Course - Part2 Ch3 Serving pipeline]] · [[AI DE Course - Part2 Ch3 Training-serving skew patterns]] ⭐ |
| Ch4 | 서빙 아키텍처·플랫폼·자원 | [[AI DE Course - Part2 Ch4 Serving architecture]] · [[AI DE Course - Part2 Ch4 Serving platforms]] · [[AI DE Course - Part2 Ch4 CPU and GPU inference]] |
| Ch5 | Feature Store 운영 | [[AI DE Course - Part2 Ch5 Feature store in practice]] |

Part 3 source 페이지 — **의미 모델링**:

| | 챕터 | 페이지 |
|---|---|---|
| Ch1 | 스키마 → NoSQL → **시멘틱** | [[AI DE Course - Part3 Ch1 Schema design and RDBMS]] · [[AI DE Course - Part3 Ch1 RDBMS limits and NoSQL]] · [[AI DE Course - Part3 Ch1 Semantics]] ⭐ |
| Ch2 | 그래프 | [[AI DE Course - Part3 Ch2 Graph fundamentals]] · [[AI DE Course - Part3 Ch2 Property graph vs RDF]] · [[AI DE Course - Part3 Ch2 Graph in practice]] · [[AI DE Course - Part3 Ch2 Graph and AI]] |
| Ch3 | 온톨로지·파이프라인·**SHACL** | [[AI DE Course - Part3 Ch3 Ontology basics]] · [[AI DE Course - Part3 Ch3 Ontology design principles]] ⭐ · [[AI DE Course - Part3 Ch3 Knowledge graph pipeline]] · [[AI DE Course - Part3 Ch3 SHACL and graph data contracts]] |
| Ch4 | **RAG → GraphRAG** | [[AI DE Course - Part3 Ch4 RAG and its limits]] ⭐ · [[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]] · [[AI DE Course - Part3 Ch4 GraphRAG variants and products]] |
| Ch5 | 그래프 DB | [[AI DE Course - Part3 Ch5 Graph databases]] |

> ⚠️ **이 코스의 수치는 인용 주의.** "데이터의 80%가 비정형", "배치가 워크로드의 80%",
> "탐색에 80% 시간", "데이터 준비 70%+", "개발 시간 70% 단축", "PSI > 0.2",
> Part 2의 **"온프레미스 시대 인프라 관리에 70% 이상"** — **어디에도 출처가 없고 일부는 서로 다른
> 회사 사례에 같은 수치가 붙어 있다.**
> → [[AI DE Course - AI pipeline case studies]]의 '검증 필요' 절.

## 열린 질문

이 영역이 자라면서 파볼 지점. **✅는 Part 1 인제스트로 해소된 것, ⚠️는 부분 해소.**

- ⚠️ **Iceberg 1차 문서가 필요하다.** **여전히 1순위.** Part 1로 **Delta의 트랜잭션 로그 구조는
  채워졌다**(`_delta_log/000000.json`, Add/Remove, optimistic concurrency, 체크포인트) →
  [[Table formats]]. 하지만 **Iceberg의 스냅샷·매니페스트 구조와 세 포맷의 선택 기준은 그대로 비어
  있다** — 강의는 Delta만 다루고 Iceberg·Hudi를 언급조차 하지 않는다.
  [[SpatialData as a data engineering substrate]] §4는 Iceberg를 전제하므로 **검증에 필요한 쪽이
  아직 없다.**
- ⚠️ **오케스트레이터 비교**(Airflow vs Dagster vs Prefect·Argo) — **부분 해소.**
  Part 2가 **ML 배치 추론 축**에서 처음으로 비교표를 준다: Airflow(DE 친화·ETL 통합, ML 개념
  네이티브 지원 부족) vs Kubeflow Pipeline(모델 버전·GPU 제어, 인프라 복잡) vs Flyte(중간, 재현성·
  캐싱 기본). → [[Batch and online serving]].
  **하지만 일반 ETL 축의 Airflow vs Dagster vs Prefect는 그대로 공백이다** — Dagster는 Part 2
  슬라이드에 로고로만 등장하고 본문에서 설명되지 않는다.
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
- ⚠️ **semantic layer는 실제로 쓰이는가** — **Part 3로 그림이 크게 바뀌었지만 핵심 질문은 남았다.**
  Part 1에서는 강의가 semantic layer라는 **용어를 피하고** 같은 문제를 카탈로그 + LLM 자동 태깅 +
  Text-to-SQL로 흡수했는데, **Part 3는 "시멘틱"을 정면으로 한 챕터 다룬다**
  ([[Data semantics]]) — 같은 코스 안에서 온도가 바뀌었다. 논증도 훨씬 낫다("같은 KPI가 3개가 되는
  이유", Entity·Attribute·Relationship·Context 4요소, 용어사전→온톨로지 스펙트럼).
  **그래도 비어 있는 것:** ① 채택률·실패 사례 근거 ② **도구가 하나도 안 나온다** — dbt semantic
  layer, Cube, Looker LookML, AtScale이 Part 3 전체에서 한 번도 언급되지 않는다.
  → **두 접근(정의를 명시적으로 못박기 vs LLM이 추론하기)의 경쟁 여부는 여전히 열려 있다.**

### Part 1이 새로 남긴 질문

- ❌ **Feature Store가 skew를 정말 없애나 — Part 2가 답하지 못했다.** offline·online 두 스토어를
  두는 순간 **두 스토어 간 일치**가 새로운 보장 대상이 된다. **Part 2 Ch5를 기대했으나**, Ch5의
  "만능이 아니다"는 *"안 써도 되는 경우"*(클라이언트가 값을 앎 / DW에 이미 있음 / 시간 의존성 없음 /
  batch만 필요)이지 *"썼을 때 남는 문제"*가 아니다. 백필·지연 감지는 Part 2 전체에서 안 나온다.
  → **부분적 우회책만 확보:** skew 패턴 2의 대응 "long-term(배치) + short-term(실시간) 분리" —
  정합성을 맞추는 대신 맞출 필요가 없게 만든다. [[Feature store]]
- **케이스 스터디의 1차 자료** — Uber Michelangelo·Netflix Keystone·Meta FBLearner·Google TFX·
  Airbnb Bighead. 강의의 수치는 출처가 없고 회사 간 중복된다. **엔지니어링 블로그·논문 인제스트
  후보.** [[AI DE Course - AI pipeline case studies]]
- **ORC vs Parquet** — 두 소스 모두 "같은 문제를 푸는 다른 포맷"에서 멈춘다.
  [[Columnar and in-memory data formats]]
- **`PSI > 0.2` 임계값의 근거** — 강의가 재학습 트리거 기준으로 제시하지만 도출 방식이 없다.
  [[Data drift and training-serving skew]]
- **스트리밍은 정말 랜덤 I/O인가** — 강의 내부 모순. CH04-1,2는 그렇게 일반화하는데 CH04-3,4의
  Kafka는 순차 쓰기다. → [[Latency and throughput]]에 정리해뒀지만 벤치마크 근거는 없다.

### Part 2가 새로 남긴 질문

- **LLM 서빙 계보가 통째로 빠졌다.** [[LLMOps]]를 한 챕터 다루면서 서빙은 전통 ML 기준이다 —
  vLLM·TGI, PagedAttention, continuous batching, KV 캐시가 **한 번도 나오지 않는다.**
  Ray Serve와 KServe도 로고로만 등장하고 설명이 없다. → [[Model serving platforms]] ·
  [[Inference optimization]]
- **retrieval 품질을 무엇으로 재나** — "품질 게이트", "드리프트 모니터링"을 말하지만 지표
  (recall@k·MRR·nDCG)나 임계값 설정법이 없다. Part 5가 일부 답할 가능성. [[LLMOps]]
- **라벨 지연이 재학습 주기의 상한이다** — 라벨이 T+7에 생기면 MTTR < 4시간 같은 KPI는 무의미해진다.
  **강의는 두 사실을 다른 파트에서 각각 말하고 잇지 않는다.** [[ML data pipeline]]
- **가용성과 정합성의 상충** — Ch4는 "Feature 조회 실패 시 기본값·일부 Store 장애 허용"을 권하고,
  Ch3은 그것이 skew를 만든다고 경고한다. 답은 `is_missing` 플래그지만 강의가 한자리에서 붙이지 않는다.
  [[Batch and online serving]]
- **1차 자료 후보 3건** — Chip Huyen *Designing Machine Learning Systems*(라이프사이클 원출처),
  "Do you really need a feature store?"(Medium), tiangolo의 FastAPI 성능 도식.
  **이 코스에서 출처가 표기된 드문 자료들이다.**

### Part 3가 새로 남긴 질문

- ✅ **retrieval 품질을 무엇으로 재나 — Part 3도 답하지 않았다.** Part 2에서 남긴 질문인데, RAG를
  49페이지 다루면서 recall@k·MRR·nDCG 같은 지표가 **여전히 한 번도 안 나온다.** 오히려 악화됐다 —
  LazyGraphRAG가 "global/local 질의 품질을 유지하거나 능가한다"고 인용하면서 **무엇으로 쟀는지
  밝히지 않는다.** → [[Retrieval-augmented generation]] · [[GraphRAG]].
  **Part 5(RAG의 진화: Hybrid Search와 Reranking, 9p)가 마지막 기회다.**
- ⭐ **지식그래프의 증분 갱신을 실제로 어떻게 하나** — [[Knowledge graph pipeline]] 10단계 중 마지막
  (전체 재생성 vs 증분 / **삭제 반영** / 중복 병합 / 버전 충돌 / provenance)이 **슬라이드 한 장에
  질문 6개만 던지고 끝난다.** 실무에서 가장 오래 붙잡을 지점이 가장 얇다.
  [[Change data capture]]와 연결되어야 할 자리인데 강의가 잇지 않는다. **Part 3 최대의 공백.**
- **그래프에서 잘못된 엣지의 오염 범위** — 강의는 *"초기 오염은 크게 확산될 여지가 있다"*고만 말한다.
  관계형에서 잘못된 행 하나는 행 하나로 끝나지만 그래프에서는 탐색 경로 전체가 오염된다는 것이
  위키의 해석인데, **정량적 근거나 사례가 없다.** [[Knowledge graph pipeline]]
- **온톨로지 도구가 통째로 빠졌다** — Protégé, TopBraid, RDFLib, Apache Jena, GraphDB(Ontotext),
  Stardog가 **한 번도 안 나온다.** SHACL 검증을 무엇으로 실행하는지도 없다.
  Ch5 제목이 "실습"인데 실습이 없는 것과 같은 성격. [[Ontology]]
- **GraphRAG의 비용을 실제로 재본 자료** — 인덱싱 비용이 세 변형이 나온 이유인데, 강의의 유일한
  수치가 Microsoft 자사 비교의 "0.1%"다. **독립 벤치마크가 필요하다.** [[GraphRAG]]
- **P3(엔터프라이즈 그라운딩)가 [[Knowledge graph pipeline]]과 같은 물건인가** — Ch3에서 만든
  메타데이터 그래프가 그대로 Ch4 P3의 grounding 소스가 되는 것으로 보이는데 **강의가 두 챕터를
  잇지 않는다.** 위키가 붙인 연결이므로 검증이 필요하다.
- **1차 자료 후보 4건 추가** — *RAG for Knowledge-Intensive NLP Tasks*(원논문),
  *RAG for LLMs: A Survey*(arXiv 2312.10997), *Lost in the Middle*,
  MS *From Local to Global*. **Part 3는 이 코스에서 출처가 가장 좋은 파트다.**

## 링크

- 인접 영역 MOC: [[Bioinformatics]]

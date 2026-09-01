---
type: source
title: AI DE Course - Part2 Ch1 Pipeline evolution and the DE role
area: [data-engineering]
aliases: [Part2 Ch1, 데이터 파이프라인의 진화과정과 데이터 엔지니어]
tags: [data-engineering, course, fast-campus, mlops, career, cloud]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part2/01. Ch1. 데이터 파이프라인의 진화과정과 데이터 엔지니어.pdf"]
---

# AI DE Course - Part2 Ch1 Pipeline evolution and the DE role

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 2 "AI 학습/추론 중심 데이터
파이프라인 설계" Ch1** "데이터 파이프라인의 진화과정과 데이터 엔지니어". 강사 **Habi**(데이터
엔지니어 / MLOps 엔지니어 / 데이터 사이언티스트). 원본(로컬):
`raw/data-engineering/ai-de-course/part2/01. Ch1. 데이터 파이프라인의 진화과정과 데이터 엔지니어.pdf` (30p). 강의 홈: [[AI Data Engineering (Fast Campus course)]].

**Part 2의 도입부이자 이 파트에서 가장 얇은 챕터다.** 내용의 절반 이상이 Part 1 CH02·CH03과
겹치고, 나머지는 뒤 챕터의 예고편이다. **이 페이지의 가치는 새 정보가 아니라 Part 2가 무엇을 하려는지
선언하는 데 있다.**

> **강의 목적(강사 서술):** "AI 시대의 비즈니스 요구사항에 맞춰 파이프라인을 **설계할 수 있는
> 엔지니어적 시야**를 갖는 것" — 아키텍처를 이해하고, 인프라를 설계하고, 그에 쓰이는 오픈소스를 훑는다.

## 논지 — 과거 / 현재 / 앞으로

| | 과거 | 현재 (온프레미스 → 클라우드) | 앞으로 |
|---|---|---|---|
| 문제 | 서비스 DB에서 집계 쿼리 → 병목·장애 | 인프라 관리가 일의 대부분 | 소비자가 사람이 아니라 **모델**이다 |
| 답 | OLTP와 OLAP의 분리, DW 등장 | Serverless·Managed·Auto-scaling·IaC | Feature/Vector/GPU 파이프라인 |
| DE의 정체 | 적재 담당 | 서버 관리자 → **데이터 아키텍트** | 학습·추론까지 책임지는 범위 확장 |

### 과거 — ETL이 그랬던 이유, ELT로 바뀐 이유

Part 1 [[AI DE Course - Ch3-1,2 Batch and ETL]]과 같은 이야기이고 결론도 같다.
[[ETL and ELT]]에 이미 정리돼 있다. 한 줄 요약: **저장공간과 컴퓨팅이 비쌌기 때문에 DW에 넣기 전
"작고 예쁘게 깎아서" 넣어야 했고**, 클라우드 DW(BigQuery·Snowflake)의 연산력과 스토리지 가격
하락이 그 전제를 무너뜨렸다.

### 현재 — 온프레미스 시대의 DE는 무슨 일을 했나

이 절이 Ch1에서 **유일하게 Part 1에 없던 내용**이다. 온프레미스 스택은
Hadoop(HDFS)·Spark·Hive·Sqoop·초기 Airflow였고, 데이터 엔지니어의 실제 일은:

- 서버 랙(Rack) 설치 및 네트워크 설정 모니터링
- Hadoop 클러스터 최적화 (Memory·CPU 자원 할당)
- 장애 발생 시 물리 서버 재부팅 및 복구

> **강의 주장: "인프라 관리에 70% 이상의 시간 소요. 비즈니스 로직 개발 속도가 더딤."**
> ⚠️ 또 출처 없는 70%다 — 이 코스의 상습 패턴. [[AI DE Course - AI pipeline case studies]] 참고.

클라우드 네이티브로 넘어오며 **Serverless & Managed**(인프라 부담을 클라우드사에 위임) ·
**Auto-scaling** · **IaC**(Terraform)가 자리를 대신한다. 강의의 정리:
**"엔지니어는 이제 서버 관리자가 아니라 데이터 아키텍트의 역할."**

### 앞으로 — BI 파이프라인 vs AI/ML 파이프라인

| 구분 | BI (Business Intelligence) | AI / Machine Learning |
|---|---|---|
| 최종 목적 | 리포트·대시보드·의사결정 지원 | 예측 모델·추천 시스템·생성형 AI 서비스 |
| 주요 데이터 | 구조화된 수치·로그 (Table) | 비정형 (Text·Image·Vector) |
| 데이터 신선도 | **T+1 (Daily Batch)로 충분** | **실시간 혹은 근실시간** |
| 성공 기준 | 수치의 정확성, 시각화의 명확성 | 모델 성능(Accuracy), 추론(Inference) 속도 |
| 주요 사용자 | 경영진·기획자·데이터 분석가 | 데이터 사이언티스트·ML 엔지니어·**AI 모델** |

> **표에서 가장 중요한 칸은 마지막 줄 오른쪽이다 — 소비자 목록에 "AI 모델"이 들어간다.**
> 사람이 읽고 해석하는 결과가 아니라 **모델이 그대로 삼키는 입력**을 만든다는 것. Part 2 전체가
> 이 한 칸의 파생이다. Ch3이 이걸 다시 문장으로 쓴다: *"BI는 사람이 해석하는 결과를 만들고,
> ML은 모델이 직접 소비하는 입력을 만든다."*

### 시대 구분 3단

강의는 인용 그림 3장으로 시대를 자른다 (출처는 슬라이드에 URL로 표기됨).

1. **2015~2018 ML 이전** — Source → Extract → Staging(Transform) → DW → Analyze. 단선형.
2. **2018~2022 ML 이후** — "Data Pipeline Patterns": 온프레미스·엣지·SaaS·클라우드 4종 producer가
   Replication / Streaming Ingestion / API / Data Integration 네 경로로 들어와 Lake·DW·MDM으로
   갈라지고, consumer 쪽에 **Machine Learning이 BI와 나란히** 선다.
3. **2022~ AI·LLM** — LLMOps 그림: Proprietary/Public Data → Data Processing Pipelines →
   Embeddings(Vector Stores), Pre-trained LLM → Fine-tuning → LLM API → 앱, 그리고 하단에
   Model Versioning · Caching · Monitoring, 우측에 RLHF.

## 예고편 4종 (뒤 챕터에서 본론)

| 주제 | Ch1에서의 서술 | 본론 |
|---|---|---|
| **Feature Store** | 모델 입력값의 중앙 저장소. 재사용(중복 개발 방지) + offline/online 동일 공급 | Ch5 → [[AI DE Course - Part2 Ch5 Feature store in practice]] |
| **Vector DB / RAG** | 텍스트를 벡터로 → 유사 검색 → LLM 전달. 엔지니어는 임베딩 파이프라인·저장구조·검색 성능을 설계 | Ch2 → [[AI DE Course - Part2 Ch2 LLMOps]] |
| **GPU** | 빠르지만 비싸고 **항상 켜두기 어려운** 자원. 언제·어디서·왜 쓸지가 설계 대상 | Ch4 → [[AI DE Course - Part2 Ch4 CPU and GPU inference]] |
| **Monitoring / Drift** | drift 감지 → 파이프라인 재실행 트리거 | Part 1에서 이미 → [[Data drift and training-serving skew]] |

GPU 절의 한 줄이 Part 2의 태도를 보여준다: **"데이터 엔지니어는 계산이 발생하는 흐름까지 설계
대상이 된다."** Part 1이 데이터의 이동을 다뤘다면 Part 2는 **연산의 배치**를 다룬다.

## 곁가지 — 채용 공고와 AI 활용

- **최근 JD 스크린샷.** 선호 자격요건에 Spring Boot 등 **Kotlin/Java 백엔드 개발 경험**,
  **Kubernetes 운영**, **MLOps 환경 구축 / AI 서비스 파이프라인 설계·운영**. 우대사항에
  kafka·flink, MongoDB·Redis·ElasticSearch, 대규모 트래픽 백엔드, k8s 기반 추천 시스템 플랫폼,
  MLFlow·KubeFlow.
  → **Part 1 CH01-4의 "JD 분석"과 달리 이번엔 실물 캡처다.** 다만 회사명이 가려져 있어 여전히
  1차 자료로 인용하긴 어렵다. [[Data Engineering]] MOC의 열린 질문("직무 구분의 실제 경계")에
  **부분적 근거**가 되지만 충분치는 않다.
- **밈 한 장** — 텅 빈 관중석 "Data Engineer" vs 꽉 찬 관중석 "AI Engineers".
- **AI 활용을 통한 자동화** — 로그 자동 분석·장애 원인 요약, 에러 로그 패턴 추출, 인프라 상태 요약과
  이상 징후 탐지, 운영 티켓 자동 분류. 강사의 선 긋기:
  **"AI는 생각을 대신하는 도구가 아니라 노동을 줄이는 도구."**

## 기존 페이지와의 대조

- **중복(큼)** — OLTP/OLAP 분리, ETL→ELT 전환, 클라우드 DW의 등장은
  [[AI DE Course - Ch2-1,2,3 Storage evolution]]·[[AI DE Course - Ch3-1,2 Batch and ETL]]과
  같은 내용이다. 새 개념 페이지를 만들 거리가 없다.
- **보강** — 온프레미스 시대 DE의 실제 업무 목록과 클라우드 전환의 성격(Serverless·IaC)은
  [[Traditional data engineering]]·[[AI data engineering]]에 없던 구체다.
- **확장** — "BI vs AI/ML 파이프라인" 표의 *주요 사용자에 AI 모델이 포함된다*는 관점이
  [[AI data engineering]]의 논지를 한 칸 더 밀어준다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[AI data engineering]] · [[Traditional data engineering]] · [[ETL and ELT]] ·
  [[Analytical data storage tiers]]
- 다음 챕터: [[AI DE Course - Part2 Ch2 MLOps and the ML lifecycle]]

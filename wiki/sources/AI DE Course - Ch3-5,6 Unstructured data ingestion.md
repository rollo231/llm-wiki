---
type: source
title: AI DE Course - Ch3-5,6 Unstructured data ingestion
area: [data-engineering]
aliases: [CH03-5 6 비정형 데이터, 비정형 데이터 수집과 전처리 프로세스]
tags: [data-engineering, course, fast-campus, unstructured-data, ocr, embedding, rag, vector-db]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part1/12. CH03-5, 6. 비정형 데이터(PDF_이미지) 수집과 전처리 프로세스의 이해 1, 2.pdf"]
---

# AI DE Course - Ch3-5,6 Unstructured data ingestion

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 CH03-5,6**
"비정형 데이터(PDF·이미지) 수집과 전처리 프로세스의 이해 (1)(2)". 원본(로컬):
`raw/data-engineering/ai-de-course/part1/12. CH03-5, 6. 비정형 데이터(PDF_이미지) 수집과 전처리 프로세스의 이해 1, 2.pdf`
(24p). 강의 홈: [[AI Data Engineering (Fast Campus course)]].

**[[Data Engineering]] MOC의 열린 질문 "비정형 데이터의 텐서 변환·저장 실무"에 처음 들어온 근거다.**
개념 정리는 [[Unstructured data ingestion]]에 옮겼다.

## 이 덱의 논지 — 왜 비정형인가

**양이 많아서가 아니다.** 강의의 프레이밍:

- **정형 데이터 = 결과(Result)** — "매출이 10% 하락했다", "평점이 1.5점이다" 같은 *현상*만.
- **비정형 데이터 = 원인(Reason)** — "왜 하락했는가", "어떤 점이 불편했는가"의 답.

사례: 주문 테이블에는 `#1024 / Summer Dress / 1.0★` 만 있어 원인 불명. 리뷰 텍스트
*"배송은 빨랐는데 피부가 따가워요. 옷감이 너무 거칠어서…"* 와 반품 사진을 함께 보면
**원단 재질 불량**으로 특정된다.

## 4단계 골격 (강의의 핵심 산출물)

```
수집(Ingestion) → 저장(Storage) → 처리(Processing) → 활용(Serving)
빗물 수집          댐 저장         정수 처리          수도 공급
```

> **"구구단처럼 외우세요. 어떤 프로젝트를 만나도 이 4단계 기본 골격은 변하지 않습니다."**

| 단계 | 도구 (강의 제시) |
|---|---|
| 수집 | Web Crawler(Scrapy·Selenium·Playwright) · API Gateway(REST/GraphQL) · Kafka·Kinesis·Flink |
| 저장 | S3 (Data Lake) · MongoDB (NoSQL) · Cold Storage |
| 처리 | OCR (Tesseract·Google Cloud Vision·AWS Textract) · Embedding Model · Vector DB |
| 활용 | RAG Chatbot · BI Dashboard · Client App |

## 이 덱 고유의 실무 서술

### 비정형 파이프라인은 "지능형 컨베이어 벨트"

정형이 규격화된 수도관이라면, 비정형은 크기·모양이 제각각인 물건을 자동 분류·포장하는 벨트다.
요구되는 성질 넷:

- **유연한 데이터 처리** — 1GB 영상부터 텍스트 한 줄, **깨진 파일**까지 막힘없이 흐른다
- **견고한 예외 처리** — 오염·포맷 불일치에도 전체가 멈추지 않는다.
  **문제 데이터를 격리하고 재처리하는 fail-safe가 핵심**
- **무한한 확장성** — 물량에 따라 scale-out
- (수집 시) **안정성** — 상대 서버에 부하를 주지 않는 '착한 수집' + 재시도

### 이원화 저장 전략

> **"무거운 몸체(데이터)는 S3에, 가벼운 영혼(정보)은 DB에."**

원본 파일은 S3에, 검색용 속성(경로·생성일·수집 출처·태그)은 NoSQL(MongoDB·Elasticsearch)에.
**저장 비용을 낮추면서 검색 성능을 유지하는 비정형 아키텍처의 핵심.**

추가 장치: `yyyy/mm/dd/category` 날짜 기반 파티셔닝 · Glacier로 자동 아카이빙(lifecycle).

### 처리 4종

- **OCR** — 인쇄체뿐 아니라 **구겨진 영수증, 흘려 쓴 손글씨, 복잡한 표**까지. 출력 예시로
  영수증 → `{"invoice_id": …, "total_amount": 15000, "items": [...]}` 구조화 JSON을 든다
- **정제** — 정규표현식으로 특수문자·노이즈 제거, 불용어 삭제, 맞춤법 검사
- **PII 비식별화** — 주민번호·전화번호·이메일 자동 탐지 후 마스킹
- **대용량 분산 처리** — Spark·Dask, 실패 시 자동 retry

### 임베딩과 Vector DB 4종

- **임베딩 모델** — OpenAI·Titan·BERT·E5. **데이터 특성과 언어(한국어)에 최적화된 모델 선정이
  필수적**이라고 명시한다
- **Vector DB** — Milvus·Pinecone·Weaviate. 수억 개 벡터 저장·관리
- **ANN 인덱스** — HNSW·IVF로 0.1초 이내 응답
- **Reranking** — Cross-Encoder로 1차 검색 결과를 재채점
  (→ Part 5의 "RAG의 진화: Hybrid Search와 Reranking"에서 다시 나올 주제)

의미 유사도 설명: 글자가 같은지가 아니라 뜻이 가까운 것이 벡터 공간에서 가깝다
(`King - Man + Woman = Queen`).

### RAG를 왜 하는가 — LLM의 3한계

- **최신 정보 부재** — 학습 cut-off 이후를 모른다
- **내부 데이터 접근 불가** — 사내 규정·비공개 매뉴얼은 학습되지 않았다
- **환각(hallucination)**

> **"RAG는 AI에게 암기 테스트가 아닌 오픈북 테스트(Open-book Test)를 보게 하는 것이다."**

효과는 정확도만이 아니라 **신뢰성** — "사규 문서 12페이지에 따르면…"처럼 근거를 제시할 수 있다.

### 데이터 엔지니어의 미션 4종

자동화 파이프라인 · 모니터링 & 확장성 · 데이터 품질 관리(검증 로직 + retry) ·
**워크플로우 지휘(Airflow로 순서·의존성 관리)**.

→ 오케스트레이터가 배치 전용이라는 [[Batch and stream processing]]의 경계와 일치한다.
이 파이프라인은 배치 성격이 강하다.

### 마무리 4점

1. **변환의 목적** — PDF·이미지를 텍스트·벡터로 바꾸는 것은 RAG와 멀티모달의 핵심 연료
2. **Garbage In, Garbage Out** — 전처리 없이는 아무리 똑똑한 모델도 환각을 일으킨다
3. **지능의 상한선 결정** — **데이터 가공 능력이 곧 회사가 도입할 AI 서비스의 품질 한계**
4. **필연적 공생** — 모델은 도구일 뿐, 그 도구를 쓰는 힘은 양질의 데이터에서 나온다

## 기존 페이지와의 대조

- **[[AI data engineering]] 보강** — "이미지·오디오·비디오·텍스트를 텐서로 변환"이라고만 적혀 있던
  자리에 실제 4단계와 도구가 들어왔다.
- **[[Analytical data storage tiers]]와의 관계** — 그 페이지는 "완전 비정형은 레이크하우스의 대상이
  아니다"라고 정리했는데, 이 덱이 **그 경계를 실무에서 어떻게 우회하는지**(S3 원본 + NoSQL 메타데이터
  이원화 + Vector DB)를 보여준다. 모순이 아니라 보완이다.
- **일치** — "데이터의 80% 이상이 비정형"은 [[AI DE Course - Ch1-1 OT]]와 같은 수치.
  (근거 없음은 동일 → [[AI DE Course - Ch3-1,2 Batch and ETL]]의 '검증 필요' 참조)

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Unstructured data ingestion]] (상세), [[AI data engineering]],
  [[Analytical data storage tiers]], [[Batch and stream processing]],
  [[Data SLA and observability]]
- 앞 챕터: [[AI DE Course - Ch3-3,4 CDC]]

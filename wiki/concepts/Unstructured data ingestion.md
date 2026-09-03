---
type: concept
title: Unstructured data ingestion
area: [data-engineering]
aliases:
  - Unstructured data
  - 비정형 데이터
  - 비정형 데이터 수집
  - OCR
  - Vector database
tags: [data-engineering, unstructured-data, ocr, embedding, vector-db, rag, preprocessing]
created: 2026-08-01
updated: 2026-09-03
sources: ["[[AI DE Course - Ch3-5,6 Unstructured data ingestion]]"]
---

# Unstructured data ingestion

PDF·이미지·영상·로그·SNS 글처럼 **스키마가 없는 날것의 데이터**를 AI가 소비할 수 있는 형태로 만드는
파이프라인. [[AI data engineering]]이 "비정형을 텐서로"라고만 적어둔 자리의 실제 방법론이다.

## 정형과 무엇이 다른가

| | 정형 | 비정형 |
|---|---|---|
| 스키마 | 행·열이 명확히 정의 | 없음 |
| 저장소 | RDBMS | NoSQL, 오브젝트 스토리지(S3), 데이터 레이크 |
| 조회·처리 | SQL | AI 모델, OCR, NLP |
| 예 | 고객 테이블, 재고, 매출 장부 | PDF, 이미지, 동영상, 로그, SNS 게시글 |

전 세계 데이터의 **80% 이상이 비정형**이라는 것이 이 챕터의 전제다
(같은 수치가 [[AI DE Course - Ch1-1 OT]]에도 나온다).

**왜 중요한가는 양이 아니라 정보의 종류다:**

- **정형 데이터 = 결과(Result)** — "평점이 1.0점이다"라는 *현상*만 보여준다.
- **비정형 데이터 = 원인(Reason)** — "옷감이 거칠어서 피부가 따가웠다"는 *이유*를 준다.

강의의 사례: 주문 테이블만 보면 낮은 평점의 원인을 알 수 없지만, 리뷰 텍스트와 반품 사진을 함께
보면 "원단 재질 불량"으로 원인이 특정된다.

## 4단계 골격

```
1. 수집(Ingestion) → 2. 저장(Storage) → 3. 처리(Processing) → 4. 활용(Serving)
   크롤러·API·          S3(원본) +        OCR → 정제 →         RAG 챗봇·검색·
   스트리밍             NoSQL(메타데이터)   임베딩 → Vector DB    BI·API
```

강의는 이걸 "빗물 수집 → 댐 저장 → 정수 처리 → 수도 공급"에 비유하고, **어떤 프로젝트를 만나도
이 4단계 골격은 변하지 않는다**고 못박는다.

### 1. 수집

| 경로 | 도구 | 비유 |
|---|---|---|
| **웹 크롤러** | Scrapy · Selenium · Playwright · BeautifulSoup | 야생의 채집 |
| **공식 API** | REST · GraphQL · OAuth | 마트 쇼핑 |
| **실시간 스트리밍** | Kafka · Kinesis · Flink | 수도관 연결 |

- 크롤러는 **동적 페이지**(JS 렌더링)까지 시뮬레이션해 캡처해야 한다.
- 원칙은 **"착한 수집"** — 상대 서버에 부하를 주지 않고, rate limit을 준수하고, 실패 시 재시도한다.
- 안정성 장치는 **멱등성(중복 수집 방지)** 과 **retry**. [[Change data capture]]와 같은 요구사항이다.

### 2. 저장 — 이원화 전략

**"무거운 몸체(데이터)는 S3에, 가벼운 영혼(정보)은 DB에."**

- **오브젝트 스토리지** (S3·GCS·Azure Blob) — 원본 파일을 형태·크기 제약 없이 그대로 적재.
- **메타데이터는 NoSQL로 분리** (MongoDB·Elasticsearch) — 파일 경로, 생성일, 수집 출처, 태그.
  검색은 여기서 하고 실물은 S3에서 가져온다. **저장 비용을 낮추면서 검색 성능을 유지하는 핵심.**
- **파티셔닝** — `yyyy/mm/dd/category` 형태의 날짜 기반 구조로 스캔 범위를 줄인다.
- **수명 주기 관리** — 접근이 드문 오래된 데이터는 Glacier 같은 아카이브 계층으로 자동 이동.

### 3. 처리 — 변환의 두 단계

```
Raw (픽셀·바이트)  →  Text (읽을 수 있는 문자)  →  Vector (의미를 담은 숫자 배열)
                     OCR / STT                  Embedding
```

- **텍스트 추출 (OCR)** — 인쇄체뿐 아니라 구겨진 영수증·손글씨·복잡한 표까지 딥러닝으로 읽는다.
  Tesseract(오픈소스) · Google Cloud Vision · AWS Textract.
- **정제(Pre-processing)** — 정규표현식으로 특수문자·노이즈 제거, 불용어 삭제, 맞춤법 검사.
- **PII 비식별화** — 주민번호·전화번호·이메일을 자동 탐지해 마스킹. 법적 리스크 제거.
  ([[ETL and ELT]]에서 "언제 ETL을 쓰나"의 이유와 같은 축이다.)
- **대용량 분산 처리** — 단일 서버로 불가능하면 Spark·Dask, 실패 시 자동 retry.

### 4. 임베딩과 Vector DB

- **임베딩 모델** — 텍스트를 고차원 벡터로. **데이터 특성과 언어(한국어)에 최적화된 모델 선정이
  필수적이다.** 글자가 같은지가 아니라 **뜻이 비슷한 것이 벡터 공간에서 가깝게** 놓인다
  (`King - Man + Woman = Queen`). → [[Text embeddings]] · [[Tokenization]]
- **Vector DB** — 벡터 간 거리 계산을 수행. Milvus · Pinecone · Weaviate. → [[Vector database]]
- **ANN 인덱스** — HNSW · IVF로 근사 이웃 검색. 정확도와 속도의 균형을 맞춰 0.1초 내 응답.
- **재순위화(Reranking)** — 1차 검색 결과를 Cross-Encoder로 다시 정밀 채점해 정확도를 끌어올린다.
  → [[Hybrid search and reranking]]

> **Part 5가 이 네 줄을 각각 한 페이지로 펼쳤다.** 특히 임베딩만으로는 식별자(버전·제품 코드)를
> 놓친다는 점과, 그래서 **BM25를 함께 돌려야 한다**는 것이 여기에는 없다.

## 왜 지금 — RAG와 멀티모달

LLM의 세 한계가 이 파이프라인의 수요를 만든다:

- **최신 정보 부재** — 학습 cut-off 이후를 모른다.
- **내부 데이터 접근 불가** — 사내 규정·비공개 매뉴얼은 학습되지 않았다.
- **환각(hallucination)** — 모르는 걸 그럴듯하게 지어낸다.

**RAG는 AI에게 암기 테스트가 아닌 오픈북 테스트를 보게 하는 것이다.** 외부/내부 문서를 먼저
검색해 참고서로 쓰고, "사규 문서 12페이지에 따르면…"처럼 근거를 제시한다.

> **Garbage In, Garbage Out** — 전처리 없이는 아무리 똑똑한 모델도 환각을 일으킨다. 강의의 결론은
> **데이터 가공 능력이 곧 도입할 AI 서비스의 품질 상한선**이라는 것.

## 링크

- 상위: [[AI data engineering]] — "비정형을 텐서로"의 구체적 방법
- 수집 경로: [[ETL and ELT]] · [[Batch and stream processing]] · [[Change data capture]]
- 담기는 곳: [[Analytical data storage tiers]] — 완전 비정형은 레이크의 영역이고 레이크하우스가
  아니다. 이 파이프라인이 그 경계를 실제로 어떻게 우회하는지(S3 + NoSQL 이원화) 보여준다
- 오케스트레이션: [[Batch and stream processing]] — Airflow로 4단계 의존성 관리
- 품질 보증: [[Data SLA and observability]]
- ⚠️ **RAG는 여기서 종착점으로 한 줄 다뤄지지만 그게 전부가 아니다** — 구조(Retriever/Generator),
  **한계 4종**(검색 단위 불일치 · retrieval-generation mismatch · Lost in the Middle · 고정 top-k),
  진화는 [[Retrieval-augmented generation]]. 그 한계에 대한 그래프 기반 대응이 [[GraphRAG]].
  **이 페이지의 RAG 서술은 Part 3 기준으로 얕다.**
- 출처: [[AI DE Course - Ch3-5,6 Unstructured data ingestion]]

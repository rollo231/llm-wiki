---
type: source
title: AI DE 강의 1-09 비정형 데이터 수집과 전처리
aliases: [AI DE 1-09]
tags: [AI-DE-강의, 수집, 비정형]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/data-engineering/ai-de-course/part1/12. CH03-5, 6. 비정형 데이터(PDF_이미지) 수집과 전처리 프로세스의 이해 1, 2.pdf"
---

# AI DE 강의 1-09 비정형 데이터 수집과 전처리

[[AI 데이터 엔지니어링 강의]] Part 1의 수집 파트 마지막 강의. PDF·이미지 같은 비정형 데이터를 수집해 AI가 쓸
수 있는 텍스트·벡터로 바꾸는 파이프라인 전체를 그린다. **Part 1에서 RAG·벡터 DB가 나오는 유일한 강의**다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 1 |
| 덱 제목 | 비정형 데이터 수집과 전처리 프로세스 (파일명: 비정형 데이터(PDF_이미지) 수집과 전처리 프로세스의 이해 1, 2) |
| 원본 파일 | `part1/12. CH03-5, 6. 비정형 데이터(PDF_이미지) 수집과 전처리 프로세스의 이해 1, 2.pdf` (24p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-02-19 |
| URL | 없음 (유료 강의 자료) |

## 요약

### 왜 비정형인가 (p2–5)

- **정형 vs 비정형** — 고정 스키마·RDBMS·SQL(고객 정보, 재고) vs 스키마 없음·NoSQL·오브젝트 스토리지·
  AI 모델·OCR·NLP(PDF, 이미지, 동영상, 로그, SNS 게시글).
- **정형 = 결과, 비정형 = 원인** — 쇼핑몰 원피스 평점 1.0이라는 결과(DB)는 "배송은 빨랐는데 피부가 따가워요,
  옷감이 거칠고 마감도 엉망" 리뷰와 사진(비정형)을 봐야 원인(원단 재질 불량)이 나온다.
- **변환의 마법** — 원시 파일(PDF·JPG·MP4) → 텍스트 추출(OCR·STT) → 벡터화(임베딩) → AI Ready.
  "재료 손질이 엉망이면 최고급 셰프(AI)도 맛없는 요리를 만든다."

### 4단계 파이프라인 (p6–10, p15–20)

비유: 빗물 수집 → 댐 저장 → 정수 처리 → 수도 공급.

| 단계 | 하는 일 | 도구(덱) |
|---|---|---|
| 수집 | 웹 크롤러(동적 페이지까지, "착한 수집"·재시도), 공식 API(인증 키·호출량 제한), 실시간 스트리밍(초당 수만 건 로그·센서) | Scrapy·Selenium·Playwright·BeautifulSoup / REST·GraphQL·OAuth / Kafka·Kinesis·Flink |
| 저장 | **원본은 오브젝트 스토리지에, 속성 정보는 NoSQL에(이원화)**. `yyyy/mm/dd/category` 파티셔닝, 수명주기로 아카이브 이동 | S3·GCS·Azure Blob / MongoDB·Elasticsearch / Glacier |
| 처리 | OCR로 텍스트 추출, 정규표현식·불용어로 정제, PII 자동 탐지·마스킹, 대용량은 분산 처리와 재시도, 임베딩과 벡터 저장 | Tesseract·AWS Textract·Google Cloud Vision / Spark·Dask / 벡터 DB |
| 활용 | RAG 챗봇, BI 대시보드(감성 분석·토픽 트렌드), RESTful API, Redis 캐싱·rate limiting | Tableau·Power BI |

수집 전략: 긴급성에 맞춰 배치(Cron·Airflow)와 실시간을 고르고, 중복 수집 방지(멱등성)·재시도·로깅으로 안정성을
확보한다. 파이프라인은 "스마트 공장 컨베이어 벨트"처럼 크기와 모양이 제각각인 입력에도 멈추지 않아야 한다 —
문제 데이터는 **격리하고 재처리**(fail-safe), 물량에 따라 scale-out.

### AI 쪽 부품 (p11–14, p19)

- **패러다임 변화** — 정형 데이터 중심(KPI) → 빅데이터 태동기(Hadoop·DW) → 비정형 혁명(RAG·멀티모달).
- **RAG** — LLM의 한계(학습 시점 이후 정보 부재, 사내 문서 접근 불가, 환각)를 사내 문서를 먼저 검색해 근거로
  답하는 방식으로 보완한다. "AI에게 암기 테스트가 아니라 오픈북 테스트를 보게 하는 것."
- **OCR** — 인쇄체뿐 아니라 구겨진 영수증·손글씨·표까지 읽어 JSON(`invoice_id`, `date`, `total_amount`,
  `items`)으로 만든다.
- **임베딩** — "사과"를 수백 개의 숫자 좌표로. 뜻이 비슷한 단어가 벡터 공간에서 가깝다(King − Man + Woman =
  Queen).
- **임베딩 & 벡터 DB** — 데이터 특성·언어(한국어)에 맞는 임베딩 모델 선정, 벡터 DB(Milvus·Pinecone·Weaviate)에
  수억 개 벡터 저장, 근사 최근접 검색 인덱스(HNSW·IVF), 1차 결과를 Cross-Encoder로 다시 채점하는 리랭킹.

### 마무리 (p21–23)

DE의 미션은 자동화·모니터링과 확장성·품질 관리(검증과 재처리)·오케스트레이션(Airflow). 4단계 골격은
"구구단처럼 외우라". 전처리 없이는 똑똑한 모델도 환각을 일으키고, **데이터 가공 능력이 곧 회사 AI 서비스의
품질 상한**이다.

## 핵심

- **저장 이원화** — 원본은 오브젝트 스토리지, 속성 정보는 NoSQL. 같은 원리가 레이크하우스·카탈로그에도 있다.
  *(위키의 연결)* → [[비정형 데이터 파이프라인]]
- 처리 단계는 정형 ETL의 Transform이 확장된 것이다 — 정제·PII 마스킹은 그대로, 여기에 OCR과 임베딩이 붙는다.
  → [[ETL과 ELT]]
- Part 1에서 **임베딩·벡터 DB·RAG가 나오는 강의는 이것뿐**이다. 다만 한 장씩 소개 수준이다.

## 주의·결함

- ⚠️ **"OpenAI Titan"** — 임베딩 모델 목록이 "OpenAI Titan, BERT, E5"로 붙어 있다. **Titan은 Amazon의 임베딩
  모델**(Amazon Titan Text Embeddings)이다. 쉼표 누락("OpenAI, Titan")일 수도 있지만 슬라이드상으로는 한
  이름처럼 읽힌다. [AWS Bedrock 문서 "Amazon Titan Embeddings models include Amazon Titan Text Embeddings V2 and
  Titan Text Embeddings G1 model." https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html ,
  2026-09-14 확인]
- ⚠️ **"전 세계 데이터의 80% 이상은 비정형 데이터"** — 출처가 없다. 이 수치의 이른 출처로 흔히 거론되는 것은
  Merrill Lynch 1998년 보고서의 "some estimates run as high as 80%"인데 근거가 불분명하다(Wikipedia
  "Unstructured data" 문서 경유, 원문 미확인). 흔히 함께 인용되는 IDC·Seagate 「Data Age 2025」(2018) 백서에는
  "unstructured"라는 단어가 나오지 않는다.
- **같은 덱에서 단계 수가 다르다** — p6 파이프라인 개요는 3단계(수집·저장·처리), p15·p22는 4단계(+활용).
- **청킹(chunking)이 없다** — RAG 전처리에서 문서를 어떤 단위로 잘라 임베딩할지가 핵심인데, 텍스트 추출에서 곧바로
  임베딩으로 넘어간다.
- 예시 수치: "HNSW·IVF로 0.1초 이내 응답 보장"(인덱스 파라미터·규모·재현율 목표에 따라 달라진다), 불량 검출
  "98%", 감정 분석 "92% Confidence".

## 관련

- 개념: [[비정형 데이터 파이프라인]] · [[ETL과 ELT]]
- 이전 강의: [[AI DE 강의 1-08 CDC]]
- 다음 강의: [[AI DE 강의 1-10 배치 vs 스트리밍]]

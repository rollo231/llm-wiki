---
type: entity
title: Apache Lucene
area: [data-engineering]
aliases: [Lucene, Apache Solr, Solr, 역색인, inverted index, 전문 검색, full-text search, Elasticsearch, OpenSearch, Apache OpenNLP, OpenNLP]
tags: [data-engineering, apache, search, inverted-index, lucene, solr]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch9 Serving OLAP search and NoSQL]]"]
---

# Apache Lucene

**전문 검색을 만드는 역색인(inverted index) 라이브러리.** 독립된 검색 서버가 아니라 **여러 검색 제품의
기반이 되는 기술**이다.

> **`LIKE '%키워드%'` 만으로는 데이터가 늘어날수록 느려지고, 검색어와 더 관련 있는 결과를 먼저 보여
> 주기도 어렵다.**

## 하는 일 — 세 단계

1. **토큰화** — 문장을 검색에 사용할 작은 단위로 나눈다. 언어·형태소에 맞춘 처리.
2. **역색인** — 각 단어가 **어느 문서에 들어 있는지**를 미리 정리해 둔다. (문서→단어의 역방향)
3. **스코어링** — 검색어가 들어오면 일치 정도를 **점수로 계산해 결과 순서를 정한다.**

⭐ 3번이 이 라이브러리의 핵심 가치다. 키 조회([[Apache Cassandra]])나 숫자 집계(Druid·Pinot)와 달리
**"관련도 순으로 줄을 세우는" 일**이 Lucene의 자리다. → [[Consumption layer]]의 조회 형태 표

## Lucene 위의 서버들

Lucene 자체는 **클러스터 제품이 아니라 라이브러리**다. 실제 서비스는 그 위에 분산 처리·네트워크
API·운영 기능을 더한 서버를 쓴다.

| | 정체 |
|---|---|
| **Apache Solr** | 🔹 Apache 생태계의 대표 분산 검색 서버. 색인 후 키워드 검색·조건 필터·정렬·하이라이트를 **HTTP API**로 제공. **샤드·복제**로 검색량 확장. 카테고리별 결과 수를 보여 주는 **패싯**은 상품 탐색 화면에 유용 |
| Elasticsearch · OpenSearch | 같은 자리의 비-Apache 제품. 책이 Lucene 항목에서 이름만 언급한다 |

- **애플리케이션 안에 검색을 직접 넣어야 할 때** → Lucene
- **여러 사용자가 함께 쓰는 분산 검색 서비스** → Solr 같은 서버 제품

⚠️ Solr는 **OLAP 집계나 멀티리전 키-값 저장의 주력 엔진이 아니다.** 거래 처리용 DB나 분석 웨어하우스를
대신하지 않는다. *"숫자 집계는 OLAP 엔진이, 텍스트 검색과 결과 순위는 Solr가 담당하도록 역할을
나눈다."*

## 색인 앞단의 언어 분석 — OpenNLP

> *"Lucene이 검색 색인이라면, **Apache OpenNLP는 그 앞단의 언어 분석**을 담당한다."*

OpenNLP는 **토큰화 · 문장 분할 · 품사 태깅 · 개체명 인식**을 제공하는 기초 NLP 라이브러리다.
LLM 이전부터 쓰인 텍스트 전처리 도구이고, **경량·온프레미스·Java 생태계**에서 여전히 실용적이다.

⚠️ **"최신 생성형 LLM이나 대규모 임베딩 스택을 대체하는 제품은 아니다."** 현대에는 spaCy·Hugging
Face·클라우드 NLP API가 더 자주 쓰인다. → [[Text embeddings]] · [[Unstructured data ingestion]]

⭐ 선택 기준은 단순하다 — **텍스트 검색만 필요하면 Lucene/Solr로 충분하고, 개체 추출·규칙적 전처리·
경량 파이프라인이 필요하면 OpenNLP**다.

## 위키 안에서의 위치

⭐ **[[Hybrid search and reranking]]의 절반이 여기서 나온다.** 그 페이지의 논지 —
**"의미는 남고 식별자는 사라진다"** — 에서 *식별자를 잡아 주는 쪽*이 Lucene 계열의 역색인·BM25이고,
*의미를 잡는 쪽*이 [[Vector database]]의 ANN이다. **대체가 아니라 두 절반이다.**

- [[Consumption layer]] — 조회 형태 중 **문장 검색** 칸.
- [[Hybrid search and reranking]] — BM25 스코어링과 RRF 결합. **Lucene은 BM25가 사는 곳이다.**
- [[Text embeddings]] · [[Vector database]] — 같은 "검색"이라는 단어의 다른 절반.
- [[Apache Calcite]] — 같은 형태의 부품. **설치 목록에 오르지 않는 라이브러리가 제품 여러 개의
  공통 기반이 되는 패턴**이 SQL 계층과 검색 계층에서 반복된다.

---
type: source
title: AI DE 강의 3-04 그래프의 기본 개념
aliases: [AI DE 3-04]
tags: [AI-DE-강의, 그래프, 지식 그래프]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part3/02. Ch2. Graph에 대한 이해.pdf"
---

# AI DE 강의 3-04 그래프의 기본 개념

[[AI 데이터 엔지니어링 강의]] Part 3 Ch2의 첫 소단원. 데이터를 "무엇이 있는가"에서 "무엇과 어떻게 연결되는가"로 다시 보는 관점을 세우고, 그래프의 구성 요소(Node·Edge·Property·Label), 읽는 단위(Path·Hop·Pattern), 종류, 지식 그래프, 데이터 엔지니어가 그래프를 고려할 때의 질문을 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 3 「시멘틱 & 컨텍스트 기반 데이터 설계」 |
| 덱 제목 | Ch2. Graph에 대한 이해: 1. Graph에 대해 이해하기 1 |
| 원본 파일 | `part3/02. Ch2. Graph에 대한 이해.pdf` p1–20 (20p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-04-21 |
| URL | 없음 (유료 강의 자료) |
| 분할 | Ch2의 소단원 넷은 제목이 모두 「Graph에 대해 이해하기 1~4」다. 같은 제목이면 묶는 것이 분할 규칙이지만, 74쪽에 주제가 넷이라 주제별로 나눴다(사용자 결정). 페이지 이름의 주제는 위키가 붙인 것이다 |

## 요약

### 01. Graph란?

- 개체 자체보다 개체 사이의 연결이 더 중요한 경우가 있다. 사용자와 상품, 대시보드와 지표의 관계가 예다.
- 강의의 정의: 그래프는 복잡한 연결 구조를 객체 간 관계 네트워크로 표현하는 데이터 모델이다. 관계를 1급 데이터로 보고, 속성 중심의 이해에서 관계 중심의 이해로 옮긴다.

구성 요소(p4–7):

| 요소 | 뜻 | 강의의 예 |
|---|---|---|
| Node | 개체를 표현하는 기본 단위 | 사람, 상품, 검색어, 테이블, 컬럼, DAG, 대시보드, ML Feature, 모델 버전 |
| Edge (Relationship) | 두 개체 사이의 연결 | PURCHASED, VIEWED, BELONGS_TO, DEPENDS_ON, GENERATED_BY, OWNED_BY |
| Property | 노드와 관계에 붙는 key-value 속성 | 상품 가격, 생성 시각, 관계 신뢰도, 클릭 횟수, 유사도 점수 |
| Label / Type | 노드나 관계의 종류 | User, Product, Dataset, Dashboard / CLICKED, PRODUCED, DOWNSTREAM_OF |

읽는 단위(p8–9):

- Path: 노드와 관계가 이어진 경로. 예: Dashboard → Chart → Dataset → ETL Job → Source Table.
- Hop: 한 노드에서 다음 노드로 가는 한 단계. 1-hop은 직접 연결, 2-hop은 한 단계 더 건넌 연결이다.
- Pattern: 찾고 싶은 연결 구조 자체. 예: "특정 사용자가 본 상품과 같은 카테고리의 인기 상품", "이 지표를 깨뜨릴 수 있는 upstream asset 조합".

### 02. Graph의 종류

| 구분 | 종류 | 강의의 예 |
|---|---|---|
| 방향 | Directed | DAG, 참조·생성·호출. lineage·dependency·ownership 같은 실무 관계는 대부분 방향이 중요하다 |
| 방향 | Undirected | 공동구매, 공동저자, 네트워크 연결 |
| 가중치 | Weighted | 클릭 횟수, 공동구매 빈도, similarity score, confidence score |
| 타입 수 | Homogeneous | 사용자 노드와 친구 관계만 있는 소셜 그래프 |
| 타입 수 | Heterogeneous | User·Product·Query·Brand·Seller·Review와 VIEW·CLICK·BUY·BELONGS_TO 등. 현실의 서비스 데이터는 대부분 이쪽이다 |

### 03. 지식 그래프

- Knowledge Graph는 heterogeneous graph다. 사람·장소·조직·제품·개념 같은 entity와 그 사이의 사실 관계를 구조화한다.
- 슬라이드는 Google 공식 도움말의 설명(people, places, things에 대한 billions of facts)을 인용한다.
- 예시 트리플: subject 서울, predicate 수도이다, object 대한민국.

### 04. 실서비스에서의 Graph

- Google Search의 knowledge panel. 강의는 화면의 박스가 아니라 그 박스를 가능하게 하는 데이터 모델이 핵심이라고 한다. 검색어를 문자열이 아니라 entity와 관계로 이해한다.

### 05. 데이터 엔지니어에게 Graph

- Dataset·Column·ETL Job·Dashboard·Metric·Owner·Team·Tag를 노드로, upstream·downstream·owns·uses·transforms를 edge로 두면 메타데이터 저장을 넘어 영향도 분석이 된다. 대표 예로 DataHub를 든다.
- 그래프가 강한 문제: 다단계 연결 탐색, n-hop 이웃 분석, upstream/downstream 영향도 추적, 연결 기반 추천 후보 확장, 메타데이터와 비즈니스 맥락 연결.
- 그래프를 굳이 쓰지 않아도 되는 문제: 단순 집계·리포팅, 행 단위 CRUD, 관계보다 속성 필터가 핵심, 한두 번의 정형 join이면 충분한 경우.
- 판단 질문 다섯(p20): 핵심 객체는 무엇인가, 관계에 방향이 있는가, 관계 자체에 속성이 붙는가, 업무 질문이 n-hop 탐색으로 바뀌는가, 스키마보다 연결 구조의 해석이 더 중요한가.

## 핵심

- 구성 요소와 종류의 정리는 [[그래프 데이터 모델]]에, 지식 그래프의 정의와 쓰임은 [[지식 그래프]]에 모았다.
- 강의의 예시 노드가 거의 다 데이터 플랫폼 자산이다(테이블, DAG, 대시보드, 피처, 모델 버전). Part 3가 그래프를 소셜·추천보다 메타데이터와 계보의 도구로 먼저 본다는 뜻이다. 이 관점은 [[데이터 거버넌스와 카탈로그]]의 계보 절로 이어진다. 이 해석은 위키의 것이다.
- ✅ Google 도움말의 문구는 실제로 "our database of billions of facts about people, places, and things"다. [https://support.google.com/knowledgepanel/answer/9787176 , 2026-09-28 확인]
- ✅ DataHub 문서도 스스로를 그래프로 설명한다: "An entity is the primary node in the metadata graph." 계보는 엔티티 사이의 관계(엣지)로 모델링된다. [https://docs.datahub.com/docs/metadata-modeling/metadata-model , 2026-09-28 확인]
- "그래프를 굳이 쓰지 않아도 되는 문제" 목록은 [[관계형 데이터베이스]]가 여전히 기본값이라는 뜻이다. 같은 판단이 [[AI DE 강의 3-06 그래프의 실무 활용]]의 "JOIN 횟수가 아니라 질문의 의미"와 [[AI DE 강의 3-14 그래프 DB의 특징]]의 RDB·그래프 DB 선택 기준에서 다시 나온다.

## 주의·결함

- p16과 p17은 거의 같은 슬라이드다. p17에 "entity-centric retrieval의 기반" 한 문단이 더 붙어 있을 뿐이다.
- 예시 트리플 "서울 / 수도이다 / 대한민국"은 술어의 방향이 문장과 어긋나 읽기 어렵다. RDF 관례로는 `서울 capitalOf 대한민국`이나 `대한민국 capital 서울`처럼 술어가 방향을 드러낸다. 이 지적은 위키의 것이다.
- 지식 그래프를 소개하지만 트리플을 어떤 모델로 저장하는지(Property Graph인지 RDF인지)는 다음 소단원([[AI DE 강의 3-05 Property Graph와 RDF]])으로 미룬다.

## 관련

- 개념: [[그래프 데이터 모델]] · [[지식 그래프]] · [[데이터 거버넌스와 카탈로그]] · [[그래프 데이터베이스]] · [[관계형 데이터베이스]]
- 이전 강의: [[AI DE 강의 3-03 시맨틱]]
- 다음 강의: [[AI DE 강의 3-05 Property Graph와 RDF]]

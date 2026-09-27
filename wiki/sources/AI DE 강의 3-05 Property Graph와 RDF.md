---
type: source
title: AI DE 강의 3-05 Property Graph와 RDF
aliases: [AI DE 3-05]
tags: [AI-DE-강의, 그래프, RDF]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part3/02. Ch2. Graph에 대한 이해.pdf"
---

# AI DE 강의 3-05 Property Graph와 RDF

[[AI 데이터 엔지니어링 강의]] Part 3 Ch2의 두 번째 소단원. 그래프를 표현하는 두 모델, 노드·관계·속성 중심의 Property Graph와 주어·술어·목적어 트리플 중심의 RDF를 기본 단위, 스키마, 질의 언어, 유리한 경우로 비교하고 고르는 질문을 준다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 3 「시멘틱 & 컨텍스트 기반 데이터 설계」 |
| 덱 제목 | Ch2. Graph에 대한 이해: 2. Graph에 대해 이해하기 2 |
| 원본 파일 | `part3/02. Ch2. Graph에 대한 이해.pdf` p21–35 (15p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-04-21 |
| URL | 없음 (유료 강의 자료) |
| 분할 | 소단원 제목은 「Graph에 대해 이해하기 2」다. 주제로 나누고 이름을 붙인 것은 위키다(사용자 결정, [[AI DE 강의 3-04 그래프의 기본 개념]]의 인용 표 참고) |

## 요약

### 01. Graph 모델의 설계 방향

- 그래프를 노드-관계-속성 중심으로 표현할지, 주어-술어-목적어의 사실(triple) 중심으로 표현할지를 먼저 정한다.
- 이 선택이 모델링 단위, 스키마 표현, 질의 방식, 추론 가능성, 도구 생태계, 성능 특성까지 전부 정한다.

### 02. Property Graph

- 개체를 node로, 연결을 relationship으로 표현하고, node와 relationship 모두에 property를 직접 붙인다.
- 기본 요소: Node(`User`, `Dataset`), Label(`:User`), Relationship(`BOUGHT`, `DEPENDS_ON`), Property(`created_at`, `confidence_score`). p26은 dataversity의 그림 한 장이다.
- 질의의 핵심은 pattern matching이다. `(노드A)-[관계]->(노드B)` 꼴의 패턴 묘사, 경로 탐색(특정 hop만큼 떨어진 노드), 속성 필터링을 조합한다. 예: "A와 친구인 사람 중 서울에 사는 사람의 친구 목록", "내가 구매한 상품과 비슷한 항목을 구매한 사용자의 또 다른 추천 상품".

### 03. RDF (Resource Description Framework)

- 모든 정보를 subject, predicate, object 세 부분의 triple로 표현한다.
- 강의는 RDF가 단순한 트리플 저장이 아닌 이유로 넷을 든다: URI로 자원을 식별해 연결하고(Semantic Connectivity), 트리플이 모여 하나의 그래프가 되고(Graph Model), RDFS·OWL과 결합해 추론과 상호운용성을 주고(Reasoning & Interoperability), W3C 표준이다(Standardized Representation).

### 04. Property Graph와 RDF의 차이

| | Property Graph | RDF |
|---|---|---|
| 기본 단위 | node · relationship · property | triple |
| 사고 방식(p30) | 사람 노드, 영화 노드, ACTED_IN 관계에 role 속성 | "사람A가 영화B에 출연했다", "사람A의 이름은 …"을 각각 트리플로 |
| 스키마 | schema-less 또는 schema-flexible, 속성을 동적으로 추가 | RDFS·OWL로 클래스·관계·제약을 정의, SHACL로 구조 검증 |
| 메타데이터 | 노드·엣지의 key-value 속성 안에 | 데이터를 기술하는 RDF 트리플로 |
| 질의 언어 | Cypher 계열, 패턴을 시각적으로 기술 | SPARQL, triple pattern 조합 |

유리한 경우(p33–34):

- Property Graph: 관계 탐색과 경로 질의가 핵심(추천, fraud, lineage, impact analysis), 엔티티 구조가 비교적 분명, 관계에 속성이 많이 붙음, 개발자·분석가가 빠르게 모델링해야 함.
- RDF: 데이터가 매우 heterogeneous, 출처마다 구조와 용어가 다름, 데이터와 메타데이터를 같은 형식으로 다루고 싶음, 자동 추론이 필요, ontology와 표준 vocabulary로 의미를 공유. 예: 의료 지식, 학술 지식, 공공데이터 통합.

### 05. 판단 질문

1. 핵심이 경로 탐색인가? 그렇다면 Property Graph 쪽이다.
2. 출처가 다양하고 의미 표준화가 핵심인가? 그렇다면 RDF 쪽이다.
3. 데이터와 스키마를 같은 형식으로 다루고 싶은가? 그렇다면 RDF 쪽이다.
4. 관계에 속성을 많이 붙이고 실용적으로 탐색하는가? 그렇다면 Property Graph 쪽이다.
5. 추론·ontology·semantic interoperability가 필요한가? 그렇다면 RDF/RDFS/OWL 쪽이다.
6. 운영팀과 개발팀이 빠르게 모델링해야 하는가? 그렇다면 Property Graph 쪽이다(학습 곡선이 보통 더 완만).

## 핵심

- 두 모델의 비교표와 판단 질문, 질의 언어와 표준 현황은 [[그래프 데이터 모델]]에 모았다.
- 판단 질문 여섯을 줄이면 축이 둘이다. 경로를 따라가는 탐색(Property Graph)과 여러 출처의 의미를 맞추는 통합(RDF)이다. 앞쪽은 [[그래프 데이터베이스]]와 lineage로, 뒤쪽은 [[온톨로지]]와 [[SHACL]]로 이어진다. 이 요약은 위키의 것이다.
- ⚠️ p31은 RDF 쪽 스키마를 "RDFS·OWL로 클래스, 관계, 제약조건을 엄격하게 정의"한다고 쓴다. RDFS의 domain·range는 위반을 막는 제약이 아니라 타입을 추론하는 규칙이고, 구조 검증은 같은 슬라이드가 뒤에 적은 SHACL의 몫이다. 자세한 것은 [[온톨로지]]에 있다.
- 슬라이드는 Property Graph 질의 언어로 Cypher만 든다. Gremlin·GQL은 Ch5([[AI DE 강의 3-14 그래프 DB의 특징]])에 가서야 나온다. GQL은 2024년 4월 ISO/IEC 39075:2024로 발행된 Property Graph 표준 질의 언어다. [http://peter.eisentraut.org/blog/2024/04/17/gql-2024-is-out , 2026-09-28 확인. ISO 페이지는 열리지 않았다]

## 주의·결함

- p23의 목록은 문장이 끊겨 있다("모델링 단위 / 스키마 표현 방식 / … / 성능 특성까지 전부 연결"). 무엇이 무엇에 연결되는지 말하지 않는다.
- p26은 텍스트 없는 이미지 한 장(dataversity.net)이다.
- "Property Graph는 schema-less"는 단서가 필요하다. 대부분의 제품이 제약(유일성·존재)과 인덱스를 제공하고, 강의도 Ch5에서 Neo4j의 constraints를 든다([[Neo4j]]). 이 지적은 위키의 것이다.
- 관계에 속성을 붙이는 문제에서 RDF 쪽 대응(reification, RDF 1.2의 triple term)은 다루지 않는다. RDF 1.2는 2026-09 기준 아직 Candidate Recommendation 단계다([[그래프 데이터 모델]]).

## 관련

- 개념: [[그래프 데이터 모델]] · [[온톨로지]] · [[지식 그래프]] · [[그래프 데이터베이스]]
- 엔티티: [[SHACL]] · [[Neo4j]] · [[Amazon Neptune]]
- 이전 강의: [[AI DE 강의 3-04 그래프의 기본 개념]]
- 다음 강의: [[AI DE 강의 3-06 그래프의 실무 활용]]

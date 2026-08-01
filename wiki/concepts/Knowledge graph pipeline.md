---
type: concept
title: Knowledge graph pipeline
area: [data-engineering]
aliases: [지식그래프 파이프라인, 시맨틱 ETL, Semantic ETL, R2RML, Direct Mapping, 그래프 생성 파이프라인]
tags: [data-engineering, knowledge-graph, ontology, etl, rdf, shacl, pipeline]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part3 Ch3 Knowledge graph pipeline]]"]
---

# Knowledge graph pipeline

**원천 데이터에서 [[Knowledge graph|지식 그래프]]를 만들어 운영하기까지의 파이프라인.**

> ⭐ **"온톨로지를 잘 정의했다고 그래프가 자동으로 생성되는 것은 아니다.
> 그래프는 단순 파일 변환이 아니라 데이터 엔지니어링 파이프라인의 문제다."**

Part 3에서 **DE 실무에 가장 직접적인 대목**이다. [[Ontology]]가 모델이라면 이 페이지는 산출물이다.

## ⚠️ 강의 내부 불일치

개요 슬라이드는 흐름을 **`수집 → 정규화 → 의미매핑 → 그래프 생성 → 검증 → 제공`** 6단계로 그리고
1~7단계로 번호를 매기는데, **바로 다음 상세 슬라이드는 1~10단계**다. 단계 수가 맞지 않는다.
아래는 **상세 쪽(10단계)** 을 정본으로 삼는다 — 내용이 더 구체적이고 개요의 7단계를 포함한다.

## 10단계

### 1. 원천 데이터 수집

> **"그래프 생성은 단일 소스 적재가 아니라 다중 소스 통합이다."**

그래프의 원천 소스는 보통 하나가 아니다.

- 이커머스(MSA 구조) — 회원DB, 주문DB, 상품 마스터, 브랜드 마스터, 카테고리 테이블, 이벤트 로그,
  운영문서…
- 데이터 플랫폼 — 메타스토어, Airflow(오케스트레이션), BI, 데이터 카탈로그, 품질 검사, 권한/조직 정보

먼저 할 일: **어떤 소스들이 있고 어떤 키로 연결 가능한지를 파악해두기.**

### 2. 정규화·품질 정리

RDF로 변환하기 전에 원천 데이터부터 바로잡는다. 중복 고객, 중복 상품 코드, 브랜드명 표기 차이
(`iphone` vs `Iphone`), 날짜 타입 불일치(`datetime` vs `timestamp`), NULL 처리 방식, 코드값,
문자열 공백/대소문자…

> **"잘못된 정규화 상태에서 그래프를 만들면 이후에 Relation이 오염된다. 초기 오염은 크게 확산될
> 여지가 있다."**

관계형에서는 잘못된 행 하나가 행 하나로 끝나지만, 그래프에서는 **잘못 연결된 엣지가 탐색 경로 전체를
오염시킨다.** 이게 그래프에서 앞단 품질이 더 중요한 이유다.

### 3. 식별자 설계

> ⭐ **"좋은 그래프는 좋은 edge보다 좋은 node identity에서 시작한다."**

A 레코드와 B 레코드가 같은 대상인지를 정하는 단계.

| 도메인 | 식별 기준 |
|---|---|
| 이커머스 | Customer는 `customer_id`, Order는 `order_id`, Product는 `product_id`, Brand는 `brand_code` |
| 데이터 플랫폼 | Dataset은 `platform + database + schema + table` 조합 · Job은 `orchestrator(Airflow) + dag/task` 조합 · Dashboard는 `tool + workspace + dashboard_id` 조합 |

가능하면 **안정적인 비즈니스 key 또는 composite key**를 사용한다.

### 4. 엔터티와 관계 분해

테이블을 개체와 연결로 다시 본다. `orders`, `order_items`, `products`, `brands`, `customers`를
그대로 옮기지 않는다.

- 엔터티 후보: Customer, Order, Product, Brand
- 관계 후보: `Customer placesOrder Order`, `Order containsProduct Product`,
  `Product belongsToBrand Brand`

> **테이블 하나가 클래스가 아닌 경우도 존재한다.** 조인 테이블은 단순 연결이거나 독립 개체가 될 수
> 있다 — `order_items`는 단순 many-to-many bridge처럼 보이지만 **수량·할인액·옵션·상태가 붙으면
> 관계가 아니라 별도 개체로 승격 가능**하다.
> → [[Ontology]]의 "관계에 정보가 많이 붙으면 독립 개체다"와 같은 판단.

### 5. 온톨로지 매핑 (시맨틱 매핑)

소스 컬럼을 의미 모델에 연결한다.

```
customers.customer_id  → ex:Customer 의 식별자
orders.order_id        → ex:Order 의 식별자
orders.customer_id     → ex:placesOrder 관계의 연결 근거
products.brand_code    → ex:belongsToBrand 관계의 생성 근거
```

> **Mapping spec을 별도로 관리한다.** 코드 안에 하드코딩하면 유지보수가 어렵고, 온톨로지가 바뀔 때
> 전체 파이프라인에 영향을 준다.

### 6. RDF 생성

행 데이터를 subject–predicate–object 트리플로 변환.

| 방식 | 특징 |
|---|---|
| **Direct Mapping** | DB 구조를 거의 그대로 RDF 그래프로 반영. 빠르게 시작할 수 있지만 **target vocabulary를 자유롭게 변경하지 못한다** |
| **R2RML** | 원하는 온톨로지와 vocabulary 기준으로 **커스텀 매핑**. 실무에서 많이 사용 |

> **"그래프 생성은 자동 변환보다는 어떤 vocabulary를 표현할 것인가의 문제다."**
> Direct Mapping을 쓰는 순간 4단계(엔터티 분해)와 5단계(매핑)의 판단이 무의미해진다 — 스키마를
> 그대로 옮기는 것이니까.

### 7. 검증과 품질관리

대표적 오류: Order인데 Customer 타입이 붙어 있음 · Product인데 Brand 연결이 없음 · 가격이 숫자가
아니라 문자 · 같은 개체가 중복으로 두 번 생성됨.

**SHACL로 shape 검증** — 어떤 클래스가 어떤 속성을 가져야 하는지, 최소 몇 개인지, 값 타입이 맞는지,
관계를 어떤 형태로.

> **"단순 파이프라인보다 검증이 더 중요하다."** → [[Ontology]]의 SHACL 절.

### 8. 추론과 보강

그래프를 지식 레이어로 올리는 단계. 검증 이후 선택적으로 붙인다.

- `VIPCustomer`가 `Customer`의 하위 클래스면 → VIPCustomer 인스턴스를 **Customer로도 해석**
- Dataset A가 Dataset B의 upstream이고 Dataset B가 Dashboard C의 upstream이면
  → **간접 영향 범위를 계산하는 보강**

원천 데이터만 반영한 graph와 의미 규칙까지 보강한 graph는 활용 범위가 다르다.
**다만 운영 안정상 필요 범위까지만 제한하는 경우도 존재한다.**

### 9. 저장·질의·서비스 연결

**"그래프를 만든 이후 저장하고 쿼리가 가능해야 의미가 있다."**

Triple store 적재 → SPARQL endpoint → 검색시스템 / 추천시스템 / 지식 탐색 UI /
**AI context layer** / [[GraphRAG|Graph RAG]].

실제 질의: "이 고객이 주문한 상품의 브랜드는 뭐야?", "이 대시보드는 어떤 데이터셋에 연결되어 있지?",
"이 개체와 연결된 상위 개념은 뭐지?"

> **"결국 쿼리 가능한 구조를 만들어야 의미가 있다."**

### 10. ⭐ 증분 갱신과 운영

**그래프는 지속 운영이 필요하다.** Refresh 전략에 대한 운영 기준이 필요하다:

- 매일 새로 전체 재생성? / 변경분만 증분 반영?
- **삭제는 어떻게 반영?**
- 중복 병합을 어떻게 계산?
- 버전 충돌 방지?
- **Lineage와 Provenance를 어떻게 남기지?**

실제 운영: 새 Job run이 생길 때마다 lineage event 반영 · 새 대시보드 퍼블리시 시 오너십과 사용관계
업데이트 · 데이터셋 스키마 변경 시 graph validation 재실행.

> **"그래프가 살아있도록 운영한다."**
> 이 단계가 [[Change data capture]]·배치 스케줄링과 만나는 지점이고, **강의가 가장 짧게 다루지만
> 실무에서 가장 오래 붙잡는 곳**으로 보인다.

## DE 관점의 현실적 구현 순서

1. 원천 데이터 수집
2. 정규화 레이어 구축
3. 식별자 정책 수립
4. 매핑 레이어 구현
5. RDF 생성 및 적재
6. SHACL 검증
7. SPARQL/검색/API 제공
8. 스케줄링/증분 갱신

> **"새로운 데이터 제품용 [[ETL and ELT|ELT/ETL]] 파이프라인을 하나 더 운영하는 것."**
> 특별한 무언가가 아니라 **기존 DE 역량이 그대로 적용되는 일**이라는 프레이밍이 이 챕터의 가장 좋은
> 메시지다.

## 관련 페이지

- [[Ontology]] — 매핑 대상이 되는 의미 모델, SHACL 검증
- [[Knowledge graph]] — 산출물
- [[ETL and ELT]] — 이 파이프라인의 상위 유형
- [[Change data capture]] — 증분 갱신의 구현 수단
- [[Data catalog and semantic layer]] — lineage·provenance
- [[GraphRAG]] — 산출물의 소비처
- [[Graph database]] — 적재 대상

## 출처

- [[AI DE Course - Part3 Ch3 Knowledge graph pipeline]]

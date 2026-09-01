---
type: source
title: AI DE Course - Part3 Ch3 Knowledge graph pipeline
area: [data-engineering]
aliases: [Part3 Ch3-3, 데이터 수집부터 그래프 생성까지의 파이프라인]
tags: [data-engineering, course, fast-campus, knowledge-graph, pipeline, rdf, r2rml, etl]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part3/03. Ch3. 온톨로지 및 지식 그래프.pdf (p30–45)"]
---

# AI DE Course - Part3 Ch3 Knowledge graph pipeline

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch3의 소단원 **3**
"데이터 수집부터 그래프 생성까지의 파이프라인".
원본(로컬): `raw/data-engineering/ai-de-course/part3/03. Ch3. 온톨로지 및 지식 그래프.pdf` **p30–45** (16p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> **Part 3에서 DE 실무에 가장 직접적인 소단원.** 앞의 Ch1~Ch3-2가 "무엇을 어떻게 모델링하나"였다면,
> 여기는 **"그래서 그걸 어떻게 만들고 운영하나"** 다.

## 전제

> ⭐ **"온톨로지를 잘 정의했다고 해서 그래프가 자동으로 생성되는 것은 아니다.
> 그래프는 단순 파일 변환이 아니라 데이터 엔지니어링 파이프라인의 문제다."**

## ⚠️ 강의 내부 불일치 — 단계 수가 맞지 않는다

개요 슬라이드(p33–34)는 흐름을 **`수집 → 정규화 → 의미매핑 → 그래프 생성 → 검증 → 제공`** 으로 그리고
**1~7단계**로 번호를 매긴다. 그런데 **바로 다음 상세 슬라이드(p35–44)는 1~10단계**다.

두 목록의 대응:

| 개요(7) | 상세(10) |
|---|---|
| 1 원천 데이터 수집 | 1 원천 데이터 수집 |
| 2 정규화·품질 정리 | 2 정규화 품질 정리 |
| 3 식별자와 엔터티 기준 설정 | 3 식별자 설계 / 4 엔터티와 관계 분해 |
| 4 온톨로지 & 매핑 | 5 온톨로지와 매핑 |
| 5 트리플/그래프 생성 | 6 RDF 생성 |
| 6 검증과 보강 | 7 검증과 품질관리 / 8 추론과 보강 |
| 7 저장과 서비스 | 9 저장·질의·서비스 연결 / 10 증분 갱신과 운영 |

**상세 쪽이 개요를 세분화한 것**이라 모순은 아니지만, 같은 챕터 안에서 단계 수를 두 번 다르게 제시한
건 편집 실수다. **위키는 상세(10단계)를 정본으로 삼는다.**

## 10단계 요약

전체 내용은 → [[Knowledge graph pipeline]]. 여기서는 **이 소단원에서만 나오는 관찰**을 남긴다.

### 1. 수집 — "단일 소스 적재가 아니라 다중 소스 통합"

이커머스(MSA 구조): 회원DB, 주문DB, 상품 마스터, 브랜드 마스터, 카테고리 테이블, 이벤트 로그, 운영문서.
데이터 플랫폼: 메타스토어, **Airflow**, BI, 데이터 카탈로그, 품질 검사, 권한/조직 정보.

### 2. 정규화 — 그래프에서 앞단 품질이 더 중요한 이유

> **"잘못된 정규화 상태에서 그래프를 만들면 이후에 Relation이 오염된다. 초기 오염은 크게 확산될
> 여지가 있다."**

관계형에서는 잘못된 행 하나가 행 하나로 끝나지만, **그래프에서는 잘못 연결된 엣지가 탐색 경로 전체를
오염시킨다.** 강의는 "확산"이라고만 말하고 이 메커니즘을 설명하지 않는다 — **위키가 붙인 해석.**

정리 대상: 중복 고객, 중복 상품 코드, 브랜드명 표기 차이(`iphone`:`Iphone`), 날짜 타입 불일치
(`datetime`-`timestamp`), NULL 처리 방식, 코드값, 문자열 공백/대소문자.

### 3. 식별자 설계

> ⭐ **"좋은 그래프는 좋은 edge보다 좋은 node identity부터 시작한다."**

데이터 플랫폼 쪽 식별자 예시가 실용적이다:
`Dataset = platform + database + schema + table` / `Job = orchestrator(Airflow) + dag/task` /
`Dashboard = tool + workspace + dashboard_id`.

**가능하면 안정적인 비즈니스 key 또는 composite key 사용.**

### 4. 엔터티와 관계 분해

**"테이블 하나가 클래스가 아닌 경우도 존재한다."** `order_items`는 단순 many-to-many bridge처럼
보이지만 **수량·할인액·옵션·상태가 붙으면 관계가 아니라 별도 개체로 승격 가능**하다.
→ Ch3-2의 "관계에 정보가 많이 붙으면 독립 개체다"의 적용.

### 5. 온톨로지 매핑

```
customers.customer_id → ex:Customer 의 식별자
orders.customer_id    → ex:placesOrder 관계의 연결 근거
products.brand_code   → ex:belongsToBrand 관계의 생성 근거
```

> **"Mapping spec을 별도로 관리한다. 코드 안에 하드코딩 방식은 유지보수가 어렵고, 온톨로지가 바뀔 때
> 전체 파이프라인에 영향을 줄 수 있다."**

### 6. RDF 생성 — Direct Mapping vs R2RML

| | 특징 |
|---|---|
| **Direct Mapping** | DB 구조를 거의 그대로 RDF로 반영. 빠르게 시작 가능하지만 **target vocabulary를 자유롭게 변경하지 못함** |
| **R2RML** | 원하는 온톨로지와 vocabulary 기준으로 커스텀 매핑. **실무에서 많이 사용** |

> **"그래프 생성은 자동 변환보다는 어떤 vocabulary를 표현할 것인가의 문제."**
>
> 이게 Ch3-2의 "스키마 복사가 아니다"와 이어진다 — **Direct Mapping을 쓰는 순간 4·5단계의 판단이
> 무의미해진다.** 강의는 이 연결을 명시하지 않지만 두 슬라이드가 같은 말을 하고 있다.

### 7~8. 검증과 추론

대표 오류: Order인데 Customer 타입이 붙음 · Product인데 Brand 연결이 없음 · 가격이 문자 · 같은 개체
중복 생성. **SHACL로 shape 검증.** → [[AI DE Course - Part3 Ch3 SHACL and graph data contracts]]

추론·보강은 선택적이다 — `VIPCustomer ⊂ Customer`면 VIP 인스턴스를 Customer로도 해석,
A→B→C upstream이면 간접 영향 범위 계산. **"운영 안정상 필요 범위까지만 제한하는 경우도 존재한다."**

### 10. ⭐ 증분 갱신과 운영

**"그래프는 지속 운영이 필요하다."** Refresh 전략 기준: 매일 전체 재생성? / 변경분만 증분? /
**삭제는 어떻게 반영?** / 중복 병합 계산? / 버전 충돌 방지? / **Lineage와 Provenance를 어떻게 남기지?**

실제 운영: 새 Job run마다 lineage event 반영 · 새 대시보드 퍼블리시 시 오너십·사용관계 업데이트 ·
데이터셋 스키마 변경 시 graph validation 재실행.

> **"그래프가 살아있도록 운영한다."**
>
> **이 단계가 한 슬라이드로 끝난다.** 질문만 6개 던지고 답은 없다. 실무에서 가장 오래 붙잡을 지점이
> 가장 얇게 다뤄졌다 — **Part 3의 가장 큰 공백.**

## DE 관점의 구현 순서

수집 → 정규화 레이어 → 식별자 정책 → 매핑 레이어 → RDF 생성·적재 → SHACL 검증 → SPARQL/검색/API →
스케줄링/증분 갱신.

> **"새로운 데이터 제품용 ELT/ETL 파이프라인을 하나 더 운영하는 것."**
>
> **이 프레이밍이 이 챕터의 가장 좋은 메시지다.** 온톨로지·RDF·SPARQL이라는 낯선 어휘를 걷어내면
> **기존 DE 역량이 그대로 적용되는 일**이라고 말한다. [[ETL and ELT]]의 한 사례로 읽으면 된다.

## 기존 페이지와의 대조

- **새 concept:** [[Knowledge graph pipeline]]
- **[[ETL and ELT]]의 하위 사례**로 읽힌다 — 강의 자신이 그렇게 말한다.
- **[[Change data capture]]와의 연결** — 10단계 증분 갱신은 CDC 문제인데 강의가 잇지 않는다.
  **위키가 붙인 연결.**
- **[[Data catalog and semantic layer]]** — lineage·provenance를 남기는 문제가 여기서도 나온다.

## 자료 품질

- 중복 슬라이드 없음.
- **단계 수 불일치**(위 참고)가 유일한 결함이지만 명백한 편집 실수다.
- 이미지는 파이프라인 아이콘 1장뿐(반복 사용). 인용 출처 문제 없음.
- 출처 없는 수치 없음.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Knowledge graph pipeline]] · [[Ontology]] · [[Knowledge graph]] · [[ETL and ELT]] ·
  [[Change data capture]] · [[Data catalog and semantic layer]]
- 앞: [[AI DE Course - Part3 Ch3 Ontology design principles]]
- 다음: [[AI DE Course - Part3 Ch3 SHACL and graph data contracts]]

---
type: source
title: AI DE Course - Part3 Ch3 Ontology design principles
area: [data-engineering]
aliases: [Part3 Ch3-2, 클래스 속성 관계 정의의 실무 원칙, 온톨로지 설계 원칙]
tags: [data-engineering, course, fast-campus, ontology, data-modeling, granularity]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part3/03. Ch3. 온톨로지 및 지식 그래프.pdf (p16–29)"]
---

# AI DE Course - Part3 Ch3 Ontology design principles

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch3의 소단원 **2**
"클래스, 속성, 관계 정의의 실무 원칙". 원본(로컬): `raw/data-engineering/ai-de-course/part3/03. Ch3. 온톨로지 및 지식 그래프.pdf`
**p16–29** (14p). 강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐ **Part 3에서 가장 실무적인 소단원이고, 최고의 문장이 여기 있다.**

## 구성

`01 온톨로지를 안 무너지게 설계하기 · 02 세부 개념들-클래스 · 03 속성 · 04 관계 ·
05 domain과 range · 06 주의점 · 07 정리`

## 문제 정의

> **"온톨로지 설계가 어려운 이유는 문법이 어려워서가 아니다.
> 무엇을 클래스, 무엇을 속성, 무엇을 관계로 둘지 경계가 애매하기 때문이다."**
>
> 어디까지를 클래스라고 볼 것인가 / 무엇을 속성으로 둘 것인가 / 어떤 연결을 관계로 승격할 것인가.
> **"이 판단이 흔들리면 뒤의 지식 그래프, 시맨틱 ETL, 검증 규칙까지 함께 흔들린다."**

## 모델은 질의와 활용 시나리오에서 출발

실제 사용 질문에서 시작한다 — "이 상품은 어떤 브랜드에 속하는가", "이 Dataset은 어떤 Job이
만들었는가", "이 Dashboard는 어떤 테이블을 사용하는가".

| 질문에서의 등장 방식 | 후보 |
|---|---|
| 반복적으로 **독립 개체**로 등장 | 클래스 후보 |
| 개체의 **설명값**으로만 등장 | 속성 후보 |
| 두 개체를 잇는 **의미 있는 연결**로 반복 | 관계 후보 |

> **쉽게: 클래스는 명사형 개체, 관계는 동사형 연결, 속성은 설명 값.**

## 클래스

기준: **"이것은 ~의 한 종류인가"** 라고 말할 수 있으면 클래스 후보.
(PremiumCustomer는 Customer의 한 종류 / FactTable은 Dataset의 한 종류)

**주의: 클래스는 개별 행을 직접 표현하지 않는다.** `Customer`는 클래스, `customer_1001`은 인스턴스.
`DatasetType`은 클래스, `dataset_sales_daily`는 인스턴스.
→ 반복해서 재사용되는 개념 이름이면 클래스, 운영 중 실제 식별자와 함께 관리되는 대상이면 인스턴스.

### Granularity

> **"Granularity는 지식 그래프가 실제 세상을 얼마나 상세하고 밀도 있게 표현하는지를 나타내는 지표."**

- 이커머스에서 `Product`만 관리하면 충분한가, **SKU**까지 구분해야 하는가?
  → **사이즈·색상·옵션별 재고를 다루면 SKU 수준까지 내려가야 한다.**
- 데이터 플랫폼에서 `Job`만 보면 충분한가, **Run**까지 봐야 하는가?
  → **장애 분석·재처리·실행 이력 추적이 중요하면 Run까지 분리해야 한다.**

> 두 예시 모두 **"어떤 질문에 답해야 하나"가 granularity를 결정한다**는 같은 논리다.
> [[Dimensional modeling]]의 grain 개념과 같은 종류의 판단인데, 강의는 잇지 않는다.

### 새 클래스로? 속성값으로?

> **"모델링에서 가장 흔한 고민."**

상품 상태(판매중/품절/예약판매)를 단순 문자열 속성으로 둘 수도 있다. 데이터셋 중요도를
high/medium/low 문자열로 둘 수도 있다. **그런데 중요도별 승인 절차, 품질 기준, 모니터링 정책이
달라진다면 단순 값보다 더 명시적인 개념 체계가 필요할 수 있다.**

> **판단 기준: 다른 규칙과 관계를 바꾸면 클래스 후보, 단순 설명만 하면 속성값 후보.**

## 속성

두 종류로 나누는 편이 안전하다:

| | 연결 대상 | 예 |
|---|---|---|
| **Data Property** | 대상과 **값** | `hasEmail`, `hasPrice`, `createdAt` |
| **Object Property** | 대상과 **다른 대상** | `placesOrder`, `belongsToBrand`, `usesDataset` |

쉽게 구분: 문자열·숫자·날짜면 보통 Data Property, **독립 식별자가 있는 다른 대상이면 Object Property.**

## 관계

> **"관계는 선 하나가 아님. 왜 연결되었는가까지 담는 의미 계약."**

좋은 관계 이름의 조건: 방향이 분명 · 업무 의미가 분명 · **이름만 봐도 주어와 목적어가 떠오름.**

| 좋은 예 | 나쁜 예 |
|---|---|
| `produces` `usesDataset` `belongsToBrand` `ownedBy` | `relatedTo` `linkedTo` `hasInfo` |

### ⭐ 관계에 정보가 많이 붙으면 그건 독립 개체다

- 고객과 상품 사이에는 단순 "구매했다"만 있는 게 아니라 **구매 시각·수량·결제수단·할인·주문상태**가
  함께 붙는다 → `Customer -buys-> Product`보다 **`Order`라는 별도 개체**를 두는 편이 자연스럽다.
- `Job -produces-> Dataset`만으로 부족할 수 있다. 실행 시각·run id·소스 환경·품질 결과까지 중요하면
  **`Run`이나 `LineageEvent` 같은 중간 개체**가 필요하다.

> **"관계에 설명해야 할 정보가 많아질수록 그 관계는 독립 개체일 가능성이 크다."**
>
> 이게 좋은 이유: **판단 기준이 주관적 취향이 아니라 "붙는 정보의 양"이라는 관찰 가능한 신호**다.
> 그리고 두 번째 예(Run·LineageEvent)는 그대로 [[Knowledge graph]] 메타데이터 그래프 설계에 쓰인다.

## domain과 range

`domain` = 이 관계를 쓰는 시작 쪽 대상, `range` = 이 관계가 가리키는 도착 쪽 대상.
`produces` → domain = `Job`, range = `Dataset`.

## ⭐⭐ 주의점 — Part 3 최고의 문장

> **"가장 흔한 실수: 테이블 = 클래스, 컬럼 = 속성, FK = 관계로 그대로 옮기는 것."**
>
> - `orders` 테이블이 있다고 `Order`가 반드시 단순 클래스인 것은 아니다
> - `brand_name` 컬럼이 있다고 `Brand`를 문자열로만 둬야 하는 것도 아니다
> - `owner_email` 컬럼이 있다고 `Owner`를 값으로만 봐야 하는 것도 아니다
>
> **"운영 DB 스키마는 저장과 처리 효율을 위한 구조이고, 온톨로지는 의미 해석과 재사용을 위한 구조다.
> 목적이 다르다."**
>
> 물어야 할 것: **이건 독립적으로 식별되는 대상인가 단순 값인가 · 이 연결은 구현 디테일인가 의미 있는
> 관계인가.**
>
> **"온톨로지 설계는 스키마 복사가 아니라 의미 구조를 다시 세우는 작업이다."**

이 절이 Ch1의 [[Schema-centric data modeling]]과 정면으로 연결된다 — Ch1이 "스키마는 형식만 잡는다"
였다면, 여기는 **"그러니 그 형식을 그대로 의미로 옮기지 마라"** 다.

## 체크리스트

| **클래스 체크** | **속성 체크** |
|---|---|
| 이 개념은 독립적으로 재사용되는가 | 이건 값인가, 다른 대상을 가리키는가 |
| 하위 클래스로 나눌 이유가 분명한가 | 문자열로 두면 나중에 확장에 막히지 않는가 |
| 실제 한 건과 개념 유형이 섞이지 않았는가 | 값 타입은 명확한가 |

| **관계 체크** | **운영 체크** |
|---|---|
| 방향이 분명한가 | 사람이 읽을 label과 설명이 있는가 |
| 이름만 보고 의미가 드러나는가 | **활용 질문에 실제로 답할 수 있는가** |
| 관계에 시간·상태·출처 같은 정보가 많이 붙지 않는가 | 모델을 바꿔도 유지보수 가능한가 |

## 기존 페이지와의 대조

- **[[Ontology]]에 통합** — 이 소단원 전체가 그 concept의 "설계의 실무 원칙" 절이다.
- **[[Schema-centric data modeling]]과 대칭** — "스키마 복사가 아니다"가 두 페이지를 잇는다.
- **[[Dimensional modeling]]의 grain과 유사** — granularity 판단이 같은 종류인데 강의는 잇지 않는다.
  **위키가 붙인 연결.**

## 자료 품질

- 중복 슬라이드 없음. **14페이지 전부가 내용이 있다** — Part 3에서 밀도가 가장 높다.
- 카메라 온톨로지 다이어그램(Viewer/Range/Camera/SLR/Digital/LargeFormat) 이미지가 6장 반복 사용되고
  **출처 표기 없음.** 슬라이드 내용과의 대응도 느슨하다.
- 출처 없는 수치 없음.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Ontology]] · [[Schema-centric data modeling]] · [[Knowledge graph]] ·
  [[Dimensional modeling]] · [[Data semantics]]
- 앞: [[AI DE Course - Part3 Ch3 Ontology basics]]
- 다음: [[AI DE Course - Part3 Ch3 Knowledge graph pipeline]]

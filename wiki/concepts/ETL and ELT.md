---
type: concept
title: ETL and ELT
area: [data-engineering]
aliases:
  - ETL
  - ELT
  - Extract Transform Load
  - Reverse ETL
  - CDC
  - Change data capture
  - 데이터 수집
  - 인제스천
tags: [data-engineering, etl, elt, ingestion, cdc, reverse-etl]
created: 2026-07-28
updated: 2026-07-28
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers"]
---

# ETL and ELT

데이터 생애주기를 요약하는 세 글자. **Extract**(소스에서 원본 추출) → **Transform**(정제·조인 등
변환) → **Load**(최종 목적지에 적재). 흔한 패턴일 뿐 고정된 법칙은 아니어서 **순서가 바뀌거나
반복되거나 겹칠 수 있다.**

## ELT — 순서를 바꾼 변형

가장 널리 쓰이는 변형. 추출한 데이터를 **변환 없이 웨어하우스(또는 레이크/레이크하우스)에 먼저
적재**하고, 변환을 그 안에서 수행해 결과를 다른 테이블 집합에 쓴다.

- **비용이 는다** — 스토리지와 컴퓨트를 둘 다 더 쓴다.
- **대신 원본이 남는다** — 나중에 다르게 처리해야 할 일이 생겼을 때 다시 추출하지 않아도 된다.
  이게 ELT를 고르는 실질적 이유다.
- raw와 processed를 **둘 다** 저장해야 하므로 같은 저장소 안에서 정제 단계를 나누는 관례가
  따라온다 → [[Medallion architecture]]

## 데이터는 어디서 오는가

- 자사 애플리케이션 DB(PostgreSQL·Mongo) — 예: 온라인 쇼핑몰의 주문 이력.
- 서드파티 서비스 API — 예: 결제 실패 분석을 위한 Stripe.
- 사용자·기기에서 직접 — 브라우저에서 보내는 애널리틱스 이벤트, IoT 디바이스 이벤트.

## 인제스천 툴

Stripe 데이터를 BigQuery에 넣는 Python 스크립트는 이미 세상에 수천 개 있다. 맞춤 로직이 필요한 게
아니라면 **데이터 인제스천 툴**로 소스·목적지 커넥터를 설정하는 편이 낫다 — auth·페이지네이션·
에러 처리 같은 반복 글루 코드를 툴이 맡는다.

**Fivetran** · **Airbyte** · **dlt**.

> ⚠️ **이 방식은 ELT 쪽으로 민다.** 추출된 데이터는 처리되기 전에 일단 어딘가 착지해야 하기 때문.
> 인제스천 툴 도입은 곧 아키텍처 선택이기도 하다.

**CDC(change data capture)** — DB에서 데이터를 끌어올 때 자주 나오는 말. 테이블을 반복 조회해
새 데이터를 찾는 대신 **DB의 replication log를 읽어** insert·update·delete를 발생하는 대로 잡아낸다.
인제스천 툴들이 DB 소스에 내부적으로 CDC를 쓰고, 독립 부품이 필요하면 **Debezium**.

## Reverse ETL — 반대 방향

보통 데이터는 운영 소스 → 웨어하우스로 흐르지만 반대도 가능하다. 처리된 데이터를 **운영 도구로
되돌려 적재**하는 것이 reverse ETL이다. 예: Stripe에서 데이터를 끌어와 고객 생애가치(LTV)를 계산한
뒤 HubSpot에 올려 영업팀이 고가치 고객을 바로 보게 하는 것.

- 이걸로 실현하는 유스케이스가 **operational analytics** — 경영진 보고서가 아니라 영업·CS·CX가
  *일상 업무 중에 쓰는 앱 안에서* 데이터를 만나게 하는 것. Zendesk에 고객의 최근 주문·티켓·플랜을
  동기화하는 식.
- reverse ETL이 유일한 전달 수단은 아니다. 웨어하우스에서 데이터를 끌어오는 사내 Customer 360 앱을
  직접 만들어도 그것 역시 operational analytics다.
- 툴은 웨어하우스를 가리키고 어느 테이블·컬럼이 어디로 동기화될지 지정하면 실패·재시도·레이트
  리밋·알림·증분 동기화를 맡아준다. **Hightouch**, **RudderStack**, **Airbyte Data activation**,
  **Fivetran Activations**(인수 전 이름은 Census).

## 링크

- 착지 지점: [[Analytical data storage tiers]], [[Medallion architecture]]
- 변환 방식: [[Batch and stream processing]] — 배치냐 스트림이냐, 그리고 오케스트레이션
- 변환 도구: SQL 변환(dbt·SQLMesh)과 데이터프레임은 [[Data landscape guide for developers]]에 요약
- 출처: [[Data landscape guide for developers]]

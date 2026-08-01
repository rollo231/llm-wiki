---
type: concept
title: ETL and ELT
area: [data-engineering]
aliases:
  - ETL
  - ELT
  - Extract Transform Load
  - Reverse ETL
  - Golden record
  - MPP
  - 데이터 수집
  - 인제스천
tags: [data-engineering, etl, elt, ingestion, cdc, reverse-etl]
created: 2026-07-28
updated: 2026-08-01
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers", "[[AI DE Course - Ch3-1,2 Batch and ETL]]"]
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

## 왜 원래 ETL이었고, 무엇이 바뀌어 ELT가 됐나

**ETL은 설계 철학이 아니라 생존 전략이었다.** 20년 전 엔터프라이즈 스토리지는 "금보다 비싼 자원"
이었고(Teradata·Oracle 장비 증설이 "강남 아파트 한 채 값"), 1TB 증설이 예산 결재 사항이었다.
**비싼 저장소에 넣기 전에 정제·요약하는 것이 유일한 선택지였다.**

그 전제를 두 변화가 무너뜨렸다:

1. **스토리지 비용 99% 하락** — 클라우드 오브젝트 스토리지(S3·GCS·Azure Blob)로 1GB 저장 비용이
   커피 한 잔 값도 안 되는 수준으로. 그러자 질문이 뒤집혔다 —
   *"저장소가 이렇게 싼데, 굳이 비싼 인력을 써가며 데이터를 줄여서 넣을 필요가 있을까?"*
2. **MPP (Massively Parallel Processing)** — 저장소가 싸도 계산이 느리면 소용없다. 과거 단일
   서버(SMP)에서 현재 수백~수천 노드 병렬로. ETL 서버 한 대가 10시간 걸린 변환을 수백 대가 10분에.
   **Snowflake · BigQuery · Redshift**가 이 엔진을 탑재한 주자들이다.

### 별도 ETL 서버가 병목이었다

- **SPOF** — 소스와 저장소 사이의 ETL 서버가 멈추면 적재 불가.
- **확장성 부족** — 데이터는 10배인데 서버는 그대로. Black Friday에 CPU 100%를 치며 데이터가
  유실되거나 분석이 지연된다.

ELT의 Transform은 **In-DB Processing**이다 — 데이터를 밖으로 꺼내지 않고 DW 내부 엔진으로 처리한다.
SQL 중심(`CREATE TABLE AS SELECT`·`MERGE`), 네트워크 egress/ingress 생략, 쿼리 옵티마이저가 실행
계획을 자동 최적화. 그래서 **dbt**(SQL 기반 모델링)가 이 자리에 앉는다.

## 언제 무엇을 — 결정 기준

ELT가 현대적 기본값이지만 **ETL이 여전히 필수인 영역이 있다.**

| | ETL을 써야 할 때 | ELT를 써야 할 때 |
|---|---|---|
| 결정 요인 | **규제** | **민첩성** |
| 상황 | 금융·의료. **민감 정보(PII)가 원본 그대로 클라우드에 올라가는 것이 법적으로 금지되거나 매우 위험** | 스타트업·이커머스·게임. 엄격한 정제보다 빠른 수집과 가설 검증이 중요 |
| 근거 | GDPR·HIPAA·신용정보법. **적재 전(before load)** 에 마스킹 또는 복호화 불가능한 단방향 암호화. 최소 권한의 원칙 | 새 소스 연결 즉시 쿼리 가능. **schema-on-read** — 저장할 때가 아니라 읽을 때 구조 정의 |
| 철학 | *"냄비(DW)에 들어가기 전에 모든 손질을 마친다"* — 위생 중심 | *"Load First, Think Later"* — 이사하듯 일단 옮기고 나중에 정리 |

**Extract 단계의 제1원칙은 어느 쪽이든 같다: "소스 시스템에 절대 부하를 주지 말라."**
운영 중인 서비스의 심장을 건드리지 않고 혈액을 채취하는 일이다. 대량 조회로 쇼핑몰 DB가 느려져
고객이 결제를 못 하면 치명적이다. 완화 수단은 스로틀링, 새벽 시간 추출, 그리고
**[[Change data capture|CDC]]**.

**Load의 목표는 Golden Record** — 조직 내 누구도 의심하지 않는 단 하나의 진실(single source of truth).
반대로 지켜야 할 것이 **GIGO**(Garbage In, Garbage Out): 오염된 데이터의 유입을 원천 차단.

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
→ 상세: [[Change data capture]]

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

- 추출의 한 방식: [[Change data capture]] — 로그 기반으로 소스 부하를 피하는 법
- 착지 지점: [[Analytical data storage tiers]], [[Medallion architecture]]
- 변환 방식: [[Batch and stream processing]] — 배치냐 스트림이냐, 그리고 오케스트레이션
- 왜 배치가 대체 불가인가: [[Latency and throughput]] — 준비 비용(setup cost)과 규모의 경제
- 원본 보존이 주는 것: [[Data and model versioning]] — "지난달 지표 다시 뽑아주세요"에 답하는 능력
- 변환 도구: SQL 변환(dbt·SQLMesh)과 데이터프레임은 [[Data landscape guide for developers]]에 요약
- 출처: [[Data landscape guide for developers]], [[AI DE Course - Ch3-1,2 Batch and ETL]]

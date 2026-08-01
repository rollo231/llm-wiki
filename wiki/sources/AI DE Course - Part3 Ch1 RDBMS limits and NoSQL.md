---
type: source
title: AI DE Course - Part3 Ch1 RDBMS limits and NoSQL
area: [data-engineering]
aliases: [Part3 Ch1-2,3, RDBMS의 한계와 NoSQL의 등장]
tags: [data-engineering, course, fast-campus, nosql, cap, sharding, scalability]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/Part 3_Ch 1.pdf (p20–48)"]
---

# AI DE Course - Part3 Ch1 RDBMS limits and NoSQL

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 3** Ch1 "스키마 중심 모델과 시멘틱"의 소단원
**2·3** "RDBMS의 한계와 NoSQL의 등장 1 / 2".
원본(로컬): `raw/data-engineering/Part 3_Ch 1.pdf` **p20–48**.
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> **분할 주의:** 원본은 소단원 2와 3으로 나뉘어 있지만 **제목이 같은 연속 덱**이라 한 장으로 합쳤다
> (Part 1의 `(1)(2)(3)` 병합 규칙과 동일). 소단원 3의 후반부(02~04)는 시멘틱으로 넘어가는 다리라
> [[AI DE Course - Part3 Ch1 Semantics]]와 함께 읽어야 한다.

## 구성

- **소단원 2** (p20–34): `01 RDBMS가 강한 부분 · 02 RDBMS의 한계 · 03 NoSQL의 등장`
- **소단원 3** (p35–48): `01 NoSQL이면 확장성이 자동 해결될까? · 02 저장 기술 선택과 의미는 다른 문제
  · 03 스키마 중심의 한계 · 04 시멘틱`

## RDBMS의 한계 3종

| | 내용 |
|---|---|
| **1. 스케일(Scale-up)** | QPS 증가 → DB CPU 90% 고정 → p95/p99 급등 → 인덱스/조인 최적화로 버티다 한계점. 원인은 **단일 노드(또는 단일 primary) 중심 설계** + 강한 일관성·트랜잭션 비용. read replica로 읽기를 늘려도 **쓰기가 병목이면 효과 제한적** |
| **2. 스키마 변경과 개발 속도** | 컬럼 추가/타입 변경/제약 변경 → 테이블 락 또는 장시간 백필, 마이그레이션 도구·롤백 설계 필요. **하나의 스키마를 여러 서비스/팀이 공유하면 변경은 기술 문제가 아니라 조직 합의의 비용이 된다** — 이 컬럼은 누가 소유하나? 어떤 서비스가 영향받나? 배포 순서와 호환성은? |
| **3. 분산에서 강한 일관성 비용** | 노드가 1개면 트랜잭션이 내부에서 끝나지만 여러 개면 네트워크를 건넌다 — 동기 복제, 분산 락, 2PC 같은 조정(coordination). **네트워크는 느리고 부분 장애가 필연적** |

## NoSQL의 등장 — 기술이 아니라 서비스가 먼저 바뀌었다

**Facebook/Instagram** — 사용자 폭발, 피드/좋아요/댓글/팔로우 이벤트가 초당 대량 생성.
**쓰기 이벤트가 OLTP보다 훨씬 자주 발생.**
**LinkedIn** — 사람-사람-회사-직무 관계가 복잡, **관계 탐색(Who knows who)이 핵심 기능.**

> **"새로운 서비스는 정확한 트랜잭션보다 대규모 이벤트 처리, 낮은 지연, 높은 가용성이 먼저 필요해졌다."**

이 프레이밍이 좋다 — NoSQL을 기술 트렌드가 아니라 **요구사항의 변화**로 설명한다.

4타입(Key-Value / Document / Wide-column / Graph)의 워크로드 매칭표와 대표 도구는
→ [[NoSQL]]

## ⭐ 이 소단원의 핵심 — "NoSQL이면 확장성이 자동 해결될까?"

> **"NoSQL = 분산 DB = 자동 스케일이라는 단순화. 실제로는 샤딩/파티셔닝 설계가 성공/실패를 좌우한다."**

세 가지 운영 현실:

1. **파티션 키가 시스템을 결정한다** — 한 번 정해지면 바꾸기 어렵다. 실패 패턴은 특정 키에 트래픽
   집중(핫 파티션)과 시간 기반 키로 쓰기 집중. **노드를 추가해도 병목이 해소되지 않는다.**
2. **일관성 완화는 애플리케이션 복잡도로 전가된다** — 재시도 설계, 중복 처리(멱등성), 순서 꼬임 처리,
   보정 배치. trade-off를 설명하는 대표 개념이 **CAP**.
3. **백업/복구/관측이 더 어렵다** — ⭐ **"운영 포인트가 줄어드는 것이 아니라 분산된다."**
   여러 노드를 같은 시점 기준으로 맞추기 어렵고, 리밸런싱 중 성능 저하가 생기고, 장애는 전체 다운보다
   **partial failure**로 나타나 원인 파악이 더 어렵다. 관측 포인트가 늘어난다 —
   QPS/latency, partition hotness/skew, replication lag, timeout/leader change.

> **이 절이 Part 3에서 가장 정직한 대목이다.** Part 1의 "Kafka는 기능을 빼서 이겼다"와 같은 결의
> 냉정함이고, 강의가 새 기술을 팔지 않는다는 신호다.
> [[Apache Kafka]]의 파티션 설계와 **같은 종류의 문제**이고,
> [[Data SLA and observability]]의 "침묵의 실패"가 분산에서 갖는 구체적 형태다.

## 그리고 저장 기술로는 답이 안 되는 것

RDBMS/NoSQL은 저장·확장·성능 문제를 다룬다. 하지만 답하지 못하는 질문:

- 활성 사용자 정의는?
- 매출은 환불/쿠폰/포인트 처리 포함?
- 전환의 윈도우는 7일/30일?

> **"이 데이터가 무엇을 의미하는가는 스키마만으로 부족하다."**

### 스키마 중심의 한계 두 가지

1. ⭐ **같은 KPI가 여러 개가 된다** — 한 회사에서 매출 숫자가 3개 이상 나오는 이유: 정의가 SQL에
   흩어지고, 팀마다 제외 조건이 다르고, **지표가 계약이 아니라 쿼리가 된다.**
   결과는 숫자 맞추기 회의와 분석 신뢰도 하락.
2. **SQL이 비즈니스 로직이 된다** — 지표 정의가 코드로만 존재 → 재사용 불가, 변경 영향 추적 어려움.
   KPI 변경 → 대시보드 전면 수정, 실험/리포트 결과 불일치.

**시멘틱 계층 = 비즈니스 의미를 데이터 위로 올리는 레이어.**
→ [[Data semantics]] · [[AI DE Course - Part3 Ch1 Semantics]]

## 기존 페이지와의 대조

- **새 concept:** [[NoSQL]] — 위키에 없던 큰 공백이었다. Part 1·2는 NoSQL을 "S3+NoSQL 이원화"
  ([[Unstructured data ingestion]])와 온라인 스토어(Redis/DynamoDB, [[Feature store]])로만 스쳤다.
- **보강** — [[Data catalog and semantic layer]]가 다루던 "이 컬럼의 '가격'은 세금 포함인가?" 문제에
  **"같은 KPI가 3개"** 라는 더 날카로운 버전이 붙는다.
- **연결** — [[Apache Kafka]] 파티션 설계, [[Data SLA and observability]] 부분 실패.
- **미언급** — 그래프 DB가 4타입 중 하나로 소개되지만 여기서는 한 줄이고, Ch2·Ch5에서 본격적으로
  다뤄진다.

## 자료 품질

- 소단원 2와 3이 **제목이 같은데 내용은 다르다** — 3은 절반이 NoSQL 비판, 절반이 시멘틱 도입부다.
  제목이 내용을 정확히 반영하지 않는다.
- p23의 마지막 줄이 이미지에 가려 잘림("쓰기(write)가 병목이면 효과 제한…").
- 핫 파티션 다이어그램에 출처 URL 표기 있음(substack).
- **출처 없는 수치 없음.**

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[NoSQL]] · [[Schema-centric data modeling]] · [[Data semantics]] · [[Apache Kafka]] ·
  [[Data SLA and observability]] · [[Graph database]]
- 앞: [[AI DE Course - Part3 Ch1 Schema design and RDBMS]]
- 다음: [[AI DE Course - Part3 Ch1 Semantics]]

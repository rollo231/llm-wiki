---
type: source
title: AI DE Course - Part3 Ch1 Schema design and RDBMS
area: [data-engineering]
aliases: [Part3 Ch1-1, 전통적 스키마 설계와 RDBMS]
tags: [data-engineering, course, fast-campus, rdbms, schema, acid, normalization]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part3/01. Ch1. 스키마 중심 모델과 시멘틱.pdf (p2–19)"]
---

# AI DE Course - Part3 Ch1 Schema design and RDBMS

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 3 "시맨틱 & 컨텍스트 기반 데이터
설계"** Ch1 "스키마 중심 모델과 시멘틱"의 소단원 **1** "전통적 스키마 설계와 RDBMS".
원본(로컬): `raw/data-engineering/ai-de-course/part3/01. Ch1. 스키마 중심 모델과 시멘틱.pdf` **p2–19** (59p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

## 이 소단원의 자리

**Part 3 전체의 출발점이자 유일하게 "복습"에 가까운 대목.** RDBMS 101(관계·키·제약·트랜잭션·ACID·
정규화·조인)을 훑고 마지막 두 장에서 **약점**을 제시한다. Part 3의 논증은 그 약점에서 시작한다.

구성: `01 RDBMS란? · 02 스키마란? · 03 트랜잭션의 중요성 · 04 ACID · 05 정규화의 목적 · 06 Join ·
07 스키마 중심 설계의 약점`

## 좋은 정의 세 개

> **"관계형이 의미하는 것은 표가 아니라 관계다."**
> PK는 엔터티를 유일하게 식별, FK는 테이블 간 관계를 **강제**. 관계를 강제하면 데이터 중복 감소 ·
> 참조 무결성 확보 · 조인 기반의 일관된 조회가 따라온다.

> **"스키마는 데이터 형식의 선언이 아니라 규칙이다."**
> 스키마가 하는 일 = 무엇이 들어올 수 있는지 제한 + 어떻게 연결되는지 명시.
> **"제약은 버그를 저장 단계에서 방어할 수 있다 — 애플리케이션 버그를 DB가 1차 방어."**

> ⭐ **"정규화는 중복 제거가 아니라 업데이트 안정성이다."**
> 중복이 많을수록 업데이트 이상(anomaly)이 증가. 고객 이름 변경 시 주문 행을 모두 수정해야 하나?
> **결과는 쓰기(write) 무결성 강화.**

세 번째가 이 소단원에서 가장 좋다. 정규화를 "저장 공간 절약"으로 배운 사람에게 방향을 고쳐준다.

## ACID — 주문/결제 예시로

트랜잭션 = 여러 DB 작업을 하나의 논리적 단위로. `BEGIN → 작업 → COMMIT | ROLLBACK`.
주문 생성 · 결제 기록 · 재고 차감 **셋은 항상 함께 성공해야 한다.**

| | 깨지면 |
|---|---|
| Atomicity | 주문은 성공했는데 결제 기록이 실패 / 재고는 차감됐는데 주문은 실패 |
| Consistency | 재고가 0인데 -1이 됨 / 존재하지 않는 고객 ID로 주문 생성 |
| Isolation | 1개 남은 상품을 동시에 2명이 결제 |
| Durability | 결제 완료 응답을 줬는데 서버가 죽어 기록이 사라짐 |

실무에서 트랜잭션이 보장하는 것: 중간 상태 노출 방지 · 실패 시 원복 · 동시성 상황에서도 예측 가능.
**결론: RDBMS는 OLTP(업무 트랜잭션)에 최적.**

> 이 ACID 설명은 [[Table formats]](Part 1 CH02-7)의 Delta Lake ACID와 **같은 내용, 다른 문맥**이다.
> Part 1은 "레이크가 잃었던 것을 되찾는" 이야기였고, 여기는 "RDBMS가 원래 갖고 있던 것"이다.
> 모순은 없다.

## Join — 표현력이자 병목

조인은 **분산된 데이터를 질의 시점에 '의미 있는 정보'로 변환**하는 관계형 모델의 핵심이다. 동시에
조인할 테이블이 N개면 조인 가짓수가 기하급수적으로 증가하고, 네스티드 루프/해시 조인 선택에 따라
성능 편차가 크며, **규모가 커지면 조인은 표현력에서 병목이 된다.**

## 약점 — Part 3가 여기서 출발한다

### 1. 변경

스키마 변경 = 마이그레이션. 다운타임/락/백필 이슈. **여러 서비스가 같은 테이블을 공유하면 변경
난이도 폭증.**

> ⭐ **"규모가 커지면 '스키마 합의'가 병목이 된다."**

### 2. 비정형/다양성

이벤트 로그(키/값이 자주 바뀜) · 문서/텍스트(컬럼 표현이 비효율) · 그래프(조인 폭발) ·
임베딩/벡터(RDBMS 질의 모델과 다름).

> ⭐ **"스키마는 형식을 잡지만, '의미'는 별도 계층이 필요하다."**
> **이 한 문장이 Part 3 전체의 테제다.** 여기서 [[Data semantics]]로 간다.

## 기존 페이지와의 대조

- **새 concept:** [[Schema-centric data modeling]] — 이 소단원 + 다음 소단원의 앞부분을 담는다.
- **보강** — [[Analytical data storage tiers]]의 OLTP 쪽이 처음으로 구체화된다(그동안 OLAP 중심).
- **중복** — ACID는 [[Table formats]]와 겹친다. 새 정보는 없고 문맥만 다르다.
- **반대 방향** — 정규화(쓰기 최적화)와 [[Dimensional modeling]](읽기 최적화)이 같은 데이터에 대해
  반대로 옳다는 점은 강의가 명시하지 않는다. **위키가 붙인 연결.**

## 자료 품질

- 슬라이드 p5·p6이 **완전히 동일**(온톨로지 챕터도 마찬가지). Part 3 전반에 복붙 중복이 잦다.
- 인용 이미지 2건에 출처 URL 표기 있음(velog DB-Normalization, SQL JOINS 다이어그램).
  **Part 1보다 출처 표기 습관이 낫다.**
- 출처 없는 수치는 이 소단원에 **없다.**

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Schema-centric data modeling]] · [[Analytical data storage tiers]] · [[Table formats]] ·
  [[Dimensional modeling]]
- 다음: [[AI DE Course - Part3 Ch1 RDBMS limits and NoSQL]]

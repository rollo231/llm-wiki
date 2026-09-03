---
type: source
title: AI DE Course - Ch2-1,2,3 Storage evolution
area: [data-engineering]
aliases: [CH02 저장소의 진화, DW에서 Data Lake Lakehouse까지]
tags: [data-engineering, course, fast-campus, storage, olap, oltp, lakehouse]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part1/04. CH02-1. 저장소의 진화 Data Warehouse에서 Data Lake, Lakehouse까지 1.pdf", "raw/data-engineering/ai-de-course/part1/05. CH02-2, 3. 저장소의 진화 Data Warehouse에서 Data Lake, Lakehouse까지 2, 3.pdf"]
---

# AI DE Course - Ch2-1,2,3 Storage evolution

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 CH02-1 / CH02-2,3**
"저장소의 진화: Data Warehouse에서 Data Lake, Lakehouse까지". 원본(로컬):
`raw/data-engineering/ai-de-course/part1/` 의 `04.` (6p) + `05.` (15p). 강의 홈:
[[AI Data Engineering (Fast Campus course)]].

## 요점

### 출발점 — 사일로 현상

저장소 진화의 동기를 **부서 간 단절**에서 찾는다. 부서별로 데이터를 중복 저장하면:

- **데이터 정합성 훼손** — 버전 불일치로 전사 데이터의 신뢰도 하락
- **협업 저하·의사결정 지연** — 전사 관점의 인사이트를 못 얻는다
- **비용 상승** — 각기 다른 시스템·라이선스에 중복 투자

→ 중앙 저장소가 필요한 이유. [[Analytical data storage tiers]]가 "매번 소스에서 끌어오는 건
비효율적"이라고 쓴 것과 같은 결론에 다른 경로로 도달한다.

### 데이터 레이크의 4요소

| 요소 | 내용 |
|---|---|
| **확장성** | S3·Blob 등 오브젝트 스토리지 기반, 페타바이트급까지 성능 저하 없는 수평 확장 |
| **접근성** | **메타데이터 카탈로그**로 검색, **스키마 온 리드**로 다양한 분석 도구 즉시 연결 |
| **보안** | 중앙 집중식 권한 관리(IAM), 전송/저장 시 암호화 |
| **비용 관리** | 수명주기 정책(Lifecycle)으로 콜드 데이터를 저렴한 계층으로 이동 |

### OLTP vs OLAP — 이 챕터의 중심

| | OLTP | OLAP |
|---|---|---|
| 목적 | 실시간 트랜잭션 처리 | 대량 데이터 분석 |
| 접근 | 레코드 단위 빠른 접근 | 필요한 **열만** 스캔 |
| 저장 | **Row Oriented** — 행 단위 연속 저장 | **Columnar** — 열 단위 분할 저장 (Parquet/Avro) |
| 잘하는 것 | 단건 CRUD — 한 사용자의 전체 정보를 **한 번의 디스크 접근**으로 (헤드 이동 최소화) | 분석 쿼리 — 필요한 컬럼만 뽑아 스캔, **I/O 부하 1/10~1/100** |
| 못하는 것 | '평균 나이' 계산 시 불필요한 이름·주소까지 읽어야 함 (I/O 병목) | — |
| 압축 효율 | 낮음 **1:3** (entropy high — 타입 혼재) | 높음 **1:10+** (entropy low — 같은 타입 연속, RLE 가능) |

- 예시: 은행 계정계/배달 주문 DB = OLTP. 분석 = OLAP.
- 한 줄 요약: **"백만 건 중 한 건" → Row / "백만 건 매출 합계" → Columnar.**
- **압축 효율의 근거를 엔트로피로 설명하는 것이 이 덱의 기여다** — 같은 데이터 타입끼리 모여 있으면
  패턴이 균일해 RLE 같은 고효율 압축이 걸린다.

### 데이터 레이크 → 레이크하우스

```
Data Source → Data Lake → Lakehouse → AI & BI
(IoT·로그·RDBMS·  (원시 상태 저장,   (레이크의 유연성 +  (ML 학습·실시간
 이미지/영상)      S3·HDFS, 저비용)   DW의 관리/성능,     대시보드·고급 분석)
                                 ACID 지원)
```

### 저장소 설계 5단계

강의가 제시하는 실무 절차:

1. **워크로드 진단** — I/O 패턴 분석, Read/Write 비율(CRUD vs 조회), 지연 시간 요구(실시간 vs 배치)
2. **저장 방식 결정** — 트랜잭션이면 Row(RDBMS), 분석이면 Columnar(DW/Lake)
3. **하이브리드 설계** — Front-end는 OLTP로 고객 요청 처리, **CDC로 OLAP에 동기화**
4. **스키마 전략** — OLTP는 정규화로 무결성 보장, OLAP은 Star Schema/비정규화로 조인 최소화
5. **최적화** — 압축(Snappy/Zstd 코덱), 파티셔닝(날짜/지역별)

> 3번이 이 코스의 축을 보여준다 — **OLTP와 OLAP을 고르는 문제가 아니라 둘을 [[Change data capture|CDC]]로
> 잇는 문제**로 본다.

### 마무리 액션 5종

내 워크로드 정밀 진단(CRUD vs 분석) → Parquet/Avro 도입 검증(컬럼 프루닝 테스트) →
**CDC → Lakehouse 파이프라인**(실시간 동기화 PoC) → 데이터 거버넌스 체계화(Catalog & DQ 규칙) →
비용/성능 최적화 튜닝(파티셔닝 & 압축)

## 기존 페이지와의 대조

- **일치** — OLTP/OLAP의 행/열 구분, 레이크하우스가 "레이크 + DW"라는 정의,
  레이크가 관리되지 않으면 늪이 된다는 경고. [[Analytical data storage tiers]]와 충돌 없다.
- **보강** — 압축률 수치(1:3 vs 1:10+)와 그 **엔트로피 근거**, 데이터 레이크 4요소,
  저장소 설계 5단계.
- **덜 다루는 것** — 이 덱에는 **쿼리 엔진 결합 축**(웨어하우스는 자체 엔진과 강결합, 레이크는 분리)
  이 없다. [[Analytical data storage tiers]]가 "실무에서 가장 자주 놓치는 지점"이라고 꼽은 축인데
  강의는 언급하지 않는다. 비용 비교 불가 논의도 없다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Analytical data storage tiers]], [[Columnar and in-memory data formats]],
  [[Table formats]], [[Dimensional modeling]] (Star Schema), [[Change data capture]]
- 이어지는 챕터: [[AI DE Course - Ch2-4,5,6 Parquet and Avro]],
  [[AI DE Course - Ch2-7 Delta Lake and ACID]]

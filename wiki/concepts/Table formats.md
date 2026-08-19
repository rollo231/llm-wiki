---
type: concept
title: Table formats
area: [data-engineering]
aliases:
  - Table format
  - Apache Iceberg
  - Iceberg
  - Delta Lake
  - Apache Hudi
  - 테이블 포맷
  - 오픈 테이블 포맷
  - ACID
  - Time travel
  - Transaction log
  - Z-Ordering
  - Compaction
  - 트랜잭션 로그
  - Apache Hive
  - Hive
  - Hive metastore
  - Hive partitioning
  - hidden partitioning
  - partition evolution
tags: [data-engineering, lakehouse, iceberg, delta-lake, hudi, hive, acid, storage, partitioning]
created: 2026-07-28
updated: 2026-08-19
sources: ["https://sinja.io/blog/data-landscape-guide-for-developers", "[[AI DE Course - Ch2-7 Delta Lake and ACID]]"]
---

# Table formats

**쿼리 엔진과 raw 파일 사이에 앉아 데이터가 어떻게 저장되는지를 관리하는 층.**
[[Analytical data storage tiers|데이터 레이크]] 위에 이 층을 얹으면 레이크하우스가 된다 —
그래서 테이블 포맷은 레이크하우스를 정의하는 블록이다. 이 층이 있으면 저장소가 "파일 더미"에서
"관습적인 데이터베이스"에 한 걸음 가까워진다.

대표 3종: **Apache Iceberg** · **Delta Lake** · **Apache Hudi**.

⭐ **이 층은 "무엇을 믿을지"만 정한다.** 그 테이블을 실제로 스캔·조인·집계해 사람에게 보내는 것은
[[SQL execution layer]]이고, 둘이 짝을 이룰 때 레이크하우스가 완성된다. **오픈 테이블이 있으면
엔진 교체는 쉬워지지만, 의미 계층·권한·SLA는 여전히 설계 대상으로 남는다.**

## 이 층이 얹어주는 것

- **ACID** — 가장 두드러진 기능. 여러 애플리케이션이 같은 데이터를 동시에 다뤄도 깨지지 않는다.
  동시 쓰기 관리, 쓰기 도중 에러 처리를 테이블 포맷이 책임진다.
- **스키마 강제** — 레이크보다 엄격하다. 반정형(JSON 등)도 담을 수 있지만 **어떤 필드를 가져야
  하는지 정의해야 하고**, 레이크하우스가 그걸 강제한다.
- **스키마 진화(schema evolution)와 버저닝** — 스키마가 시간에 따라 바뀔 수 있고, 그 변경 이력을
  추적한다.
- **파티셔닝·인덱스 최적화** — 데이터와 스키마를 통제하니 인덱스를 만들고 파티셔닝을 조정해
  쿼리를 빠르게 할 수 있다.
- **time travel** (일부 구현) — 특정 시점의 스냅샷에 쿼리를 실행한다.

## 이 층이 없으면 무엇이 깨지나

레이크가 '늪'이 되는 5가지 결함. **공통 원인은 하나다: 레이크는 데이터베이스가 아니라 파일
시스템이다.**

| 결함 | 내용 | 테이블 포맷의 답 |
|---|---|---|
| 수정·삭제의 비효율 | 한 줄을 고치려도 **1GB 파일 전체를 다시 써야** 한다 | 트랜잭션 로그의 Add/Remove |
| 동시성 | 쓰는 도중 읽으면 깨진 데이터. **격리(isolation)가 없다** | ACID의 I |
| 작은 파일 문제 | 스트리밍이 만든 수만 개 파일이 메타데이터 부하를 일으켜 쿼리 속도 저하 | **Compaction** |
| 신뢰할 수 없는 품질 | **스키마 강제가 없다.** 형식이 다른 쓰레기가 섞여 들고 최신 버전을 모른다 | 스키마 enforcement |
| 백업·복구의 고통 | 실수로 삭제하면 되돌릴 방법이 없다 | **Time travel** |

### ACID — 은행 예시로

| | 의미 | 은행 예시 |
|---|---|---|
| **A** 원자성 | 모두 성공하거나 실행되지 않은 상태로 복구 (All or Nothing) | 내 통장에서 돈은 나갔는데 친구 통장에 입금이 안 됐다면 거래 전체 취소 |
| **C** 일관성 | 전후로 정의된 규칙(스키마·제약)을 만족 | '잔액은 0원 이상' 유지, 없는 계좌로는 송금 불가 |
| **I** 고립성 | 동시 실행되어도 서로의 중간 단계를 볼 수 없다 | 송금 완료 전 0.1초 사이에 조회하면 송금 전 잔액만 보인다 |
| **D** 내구성 | 커밋된 결과는 장애가 나도 영구 보존 | "송금 완료" 직후 전원이 꺼져도 재부팅 후 내역은 살아 있다 |

## Hive — 이 층이 있기 전, 그리고 경로가 구속이었던 시절

> ⚠️ **이 절은 위키에 1차 소스가 없다.** 강의도 랜드스케이프 가이드도 Hive를 다루지 않는다.
> 일반 지식으로 정리한 것이니 Iceberg·Hive 1차 문서로 검증해야 한다.

테이블 포맷을 이해하는 가장 빠른 길은 **무엇을 고치려고 나왔는지**를 보는 것이고, 그 대상이
Hive다.

**Hive의 모델은 디렉토리 레이아웃이 곧 데이터 모델이다.** 테이블 = prefix, 파티션 =
`key=value` 하위 디렉토리. 쿼리 프루닝은 술어를 **경로 세그먼트에 매칭**해서 일어나고,
메타스토어는 파티션 → 위치 매핑을 들고 있다.

이게 "디렉토리 규칙을 정해준다"는 느낌의 출처다. 문제는 그 규약이 **구속**이라는 것:

| Hive의 문제 | 내용 |
|---|---|
| 레이아웃이 구속 | 파티션 스킴을 바꾸면 **데이터 재작성** |
| 리스팅이 곧 스캔 계획 | 오브젝트 스토리지에서 느리고, 목록과 실제가 어긋날 수 있다 |
| 메타스토어 병목 | 파티션 1개 = 메타스토어 행 1개. 수십만 파티션이면 planning이 죽는다 |
| **원자적 커밋 없음** | **디렉토리에 파일을 쓰는 것이 커밋이다.** 쓰다 죽으면 반쯤 보인다 |
| 물리 레이아웃 노출 | 사용자가 `WHERE dt='...'` 를 파티션 규약대로 써야 한다. 안 쓰면 full scan |

**Iceberg의 한 수는 이걸 전부 뒤집는 한 가지에서 나온다 — 테이블의 내용을 디렉토리 리스팅이
아니라 매니페스트가 정의한다.** 스냅샷 → 매니페스트 리스트 → 매니페스트 → 데이터 파일 경로 +
파일별 컬럼 통계(min/max). 결과적으로 **파일이 어디 있든 상관없어지고**, 파티션 값이 경로에
나타날 필요도 없다(*hidden partitioning*). 파티션 스킴을 바꿔도 옛 데이터는 옛 spec을 유지한다
(*partition evolution*).

> **Hive는 경로에 의미를 실었고, Iceberg는 경로를 의미에서 해방시켰다.**
> Delta의 `_delta_log/`(아래)도 같은 방향의 답이다 — 진실이 디렉토리가 아니라 로그에 있다.

⭐ **이 아이디어는 테이블 밖으로 이식된다.** 관리 대상이 쿼리 엔진이 못 읽는 불투명 blob이면
Iceberg를 *쓸* 수는 없지만, **같은 구조를 손으로 만들 수 있다** — 경로를 불투명하게 두고
별도 카탈로그가 *어느 객체가 유효한가*와 *열기 전에 걸러낼 통계*를 들고 있게 한다.
→ [[Object storage layout]] · [[Spatial omics platform roadmap]] §2.2

## Delta Lake의 온디스크 구조

**세 포맷 중 Delta에 대해서만** 실제 구조를 알고 있다
(출처: [[AI DE Course - Ch2-7 Delta Lake and ACID]]).

| | 내용 |
|---|---|
| **로그 위치** | 테이블 루트 하위 **`_delta_log/`** 폴더 |
| **로그 형식** | 순차 증가하는 **`000000.json`** 파일 |
| **로그 내용** | 메타데이터 변경, 파일 **추가(Add)**, 파일 **논리적 삭제(Remove)** |
| **상태 해석** | 로그를 **순서대로 읽어** 현재 유효한 파일 목록을 구성 |
| **동시성 제어** | **Optimistic Concurrency** — 충돌 감지 시 재시도 |
| **실제 데이터** | **Parquet 파일**로 클라우드 스토리지에 저장 |

> **"파일 논리적 삭제" + "로그를 순서대로 읽어 유효 파일 목록 구성"이 time travel의 정체다.**
> 파일을 실제로 지우지 않으므로, 로그를 특정 지점까지만 읽으면 그 시점의 파일 목록이 나온다.
> **데이터를 복제하지 않고 스냅샷을 얻는다** → [[Data and model versioning]]

**Delta의 5가지 기둥:** 트랜잭션 로그(진실의 원천) · **스냅샷 & 체크포인트**(로그를 요약해 현재
상태를 정의 — 빠른 읽기와 time travel의 기준점) · 스키마 관리(enforcement + evolution) ·
데이터 최적화(**Compaction**으로 작은 파일 해결, **Z-Ordering**으로 쿼리 속도) · 오픈 스토리지.

> 로그가 수만 개 쌓이면 매번 전부 읽을 수 없으니 주기적으로 요약본(**체크포인트**)을 만든다.
> [[Stream processing semantics]]의 checkpointing과 이름은 같지만 목적이 다르다 —
> 여기선 읽기 성능, 거기선 장애 복구.

## 왜 이게 아키텍처를 바꾸는가

웨어하우스는 저장과 쿼리 엔진을 함께 관리하며 **강결합**이다. 테이블 포맷은 그렇지 않다 —
**쿼리 엔진을 특정 벤더에 묶지 않는다.** 결과적으로:

- 같은 데이터에 Spark·Trino·DuckDB 등 다른 엔진을 붙일 수 있다.
- **레이크하우스와 웨어하우스의 비용을 1:1로 비교할 수 없다.** 레이크하우스는 저장만 값을
  매기고 컴퓨트는 별도이기 때문. 워크로드에 따라 (레이크하우스 + 컴퓨트)가 웨어하우스보다
  크게 쌀 수 있다.

## 매니지드 제품

- **Google's Lakehouse for Apache Iceberg** (구 BigLake)
- **Databricks** — Delta Lake 기반
- **IBM watsonx.data** — Iceberg 기반

## 이 페이지가 아직 답하지 못하는 것

두 소스를 합쳐도 **여전히 Delta 한 종류만 안다.**

- ❌ **Iceberg vs Delta vs Hudi의 선택 기준** — 어느 것이 어떤 워크로드에 맞는지.
  랜드스케이프 가이드는 이름만 나열하고, 강의는 **Delta만 다루며 다른 둘을 언급조차 하지 않는다.**
- ✅ **time travel 지원 여부** — **Delta는 지원한다**(강의가 챕터 제목으로 쓴다).
  Iceberg·Hudi는 여전히 미확인. 랜드스케이프 가이드의 "some lakehouses also support time travel"이
  아직 유효한 상태.
- ⚠️ **온디스크 구조** — **Delta의 트랜잭션 로그는 위에 정리됐다.**
  하지만 **Iceberg의 스냅샷·매니페스트 구조는 여전히 없다.** 위 Hive 절에서 개요를 적었지만
  1차 소스가 아니다.

### 🔄 Iceberg 문서가 필요한 이유가 바뀌었다 (2026-08-02)

원래는 *"[[SpatialData as a data engineering substrate]] §4가 Iceberg를 카탈로그로 전제하므로
그 설계를 검증하려면 필요하다"* 였다. **그 근거는 사라졌다** — §4는 Postgres로 정정됐다
(행 수천 개짜리 상태 테이블은 OLAP이 아니다. [[Spatial omics platform roadmap]] §2.2).

**더 나은 이유로 남는다: 도입할 도구가 아니라 손으로 만드는 것의 레퍼런스 설계이기 때문에.**
구체적으로 알아야 하는 것 셋:

1. **매니페스트를 어떤 단위로 쪼개는가** — 카탈로그 자식 테이블의 입도 참고
2. **파일별 통계를 어디까지 들고 있는가** — min/max 말고 무엇을 컬럼화할 가치가 있는가
3. **스냅샷 만료·고아 파일 정리** — 불변 산출물을 쌓는 설계에는 GC가 반드시 따라온다

## 링크

- 상위: [[Analytical data storage tiers]] — 레이크 위에 이 층을 얹은 것이 레이크하우스
- 혼동 주의: **테이블 포맷 ≠ 파일 포맷.** Parquet은 파일 하나의 레이아웃이고, 테이블 포맷은
  *여러 Parquet 파일을 하나의 테이블로 묶는 규약*이다 → [[Columnar and in-memory data formats]]
- 혼동 주의: **테이블 포맷 ≠ 카탈로그** → [[Data catalog and semantic layer]]
- **테이블이 아닌 것에는 이 층이 오지 않는다** → [[Object storage layout]] —
  경로를 의미에서 해방시킨다는 Iceberg의 아이디어를 불투명 blob에 손으로 적용하는 쪽
- small files 문제의 출처: [[Columnar and in-memory data formats]] — Avro로 빠르게 받고 Parquet으로
  묶는 compaction 패턴이 이 층의 compaction과 같은 문제를 다룬다
- 재현성으로 이어지는 곳: [[Data and model versioning]]
- 적용: [[SpatialData as a data engineering substrate]]
- 출처: [[Data landscape guide for developers]], [[AI DE Course - Ch2-7 Delta Lake and ACID]]

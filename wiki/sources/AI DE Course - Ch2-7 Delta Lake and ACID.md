---
type: source
title: AI DE Course - Ch2-7 Delta Lake and ACID
area: [data-engineering]
aliases: [CH02-7 Delta Lake, 데이터의 시간 여행, Delta Lake와 ACID 트랜잭션]
tags: [data-engineering, course, fast-campus, delta-lake, acid, time-travel, table-format]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part1/09. CH02-7. 데이터의 시간 여행 Delta Lake와 ACID 트랜잭션의 개념.pdf"]
---

# AI DE Course - Ch2-7 Delta Lake and ACID

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 CH02-7**
"데이터의 시간 여행: Delta Lake와 ACID 트랜잭션의 개념". 원본(로컬):
`raw/data-engineering/ai-de-course/part1/09. CH02-7. 데이터의 시간 여행 Delta Lake와 ACID 트랜잭션의 개념.pdf` (11p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

**[[Data Engineering]] MOC의 1순위 열린 질문("스냅샷·트랜잭션 로그의 온디스크 구조")에 처음 들어온
근거다.** 다만 Delta에 대해서만이고 Iceberg는 여전히 비어 있다.

## 요점

### 데이터 레이크가 왜 '늪'이 되는가 — 5가지 결함

[[Analytical data storage tiers]]가 "관리하지 않으면 늪이 된다"고만 쓴 자리를 구조적 원인으로 채운다.
**공통 원인은 하나다: 레이크는 데이터베이스가 아니라 파일 시스템이다.**

| 결함 | 내용 |
|---|---|
| **수정·삭제의 비효율** | 단 한 줄을 고치려도 **1GB 파일 전체를 다시 써야** 한다 |
| **동시성** | 쓰는 도중에 읽으면 깨진 데이터를 읽거나 에러. **격리(isolation)가 없다** |
| **작은 파일 문제** | 스트리밍이 만든 수만 개 자잘한 파일이 메타데이터 부하를 일으켜 쿼리 속도 저하 |
| **신뢰할 수 없는 품질** | **스키마 강제 기능이 없다.** 형식이 다른 쓰레기가 섞여 들고 어느 버전이 최신인지 모른다 |
| **백업·복구의 고통** | 실수로 운영 데이터를 삭제하면 되돌릴 방법이 없다 |

### Delta Lake의 정의

**Storage Layer + Transaction Log.** 기존 스토리지 위에 얹는 **신뢰성 계층(reliability layer)** 이다.

| Data Lake | Delta Lake |
|---|---|
| 단순 파일 시스템, DB 기능 부재 (No ACID) | 기존 스토리지 위의 보호막 |
| 작은 변경에도 파일 전체 재작성 | **ACID 트랜잭션** — All or Nothing |
| 읽기/쓰기 충돌 시 깨진 데이터 노출 | **Time Travel & 스냅샷** — 과거 시점 복구·감사 |
| 스키마 검증 없음 → 품질 저하 | **스키마 관리** — enforcement로 오염 방지, 성능 자동 최적화 |

### ACID — 은행 예시로

| | 의미 | 은행 예시 |
|---|---|---|
| **A** 원자성 | 모두 성공하거나, 실패 시 실행되지 않은 상태로 복구 (All or Nothing) | 내 통장에서 돈은 나갔는데 친구 통장에 입금이 안 됐다면 거래 전체를 취소 |
| **C** 일관성 | 트랜잭션 전후로 미리 정의된 규칙(스키마·제약)을 만족 | '잔액은 0원 이상' 규칙 유지, 없는 계좌번호로는 송금 불가 |
| **I** 고립성 | 동시 실행되어도 서로의 중간 단계를 볼 수 없다 | 송금 완료 전(0.1초 사이)에 다른 사람이 조회하면 송금 전 잔액만 보인다 |
| **D** 내구성 | 커밋된 결과는 장애가 나도 영구 보존 | "송금 완료" 직후 서버 전원이 꺼져도 재부팅 후 내역은 살아 있다 |

### 트랜잭션 로그 — 온디스크 구조 (이 덱의 핵심 기여)

| | 내용 |
|---|---|
| **로그 위치** | 테이블 루트 경로 하위 **`_delta_log/`** 폴더 |
| **로그 형식** | 순차적으로 증가하는 **`000000.json`** 파일 생성 |
| **로그 내용** | 메타데이터 변경, 파일 **추가(Add)**, 파일 **논리적 삭제(Remove)** |
| **상태 해석** | 로그를 **순서대로 읽어** 현재 유효한 파일 목록을 구성 |
| **동시성 제어** | **Optimistic Concurrency** — 충돌 감지 시 재시도 |

> **"파일 논리적 삭제"와 "로그를 순서대로 읽어 유효 파일 목록 구성"이 time travel의 정체다.**
> 파일을 실제로 지우지 않으므로, 로그를 특정 지점까지만 읽으면 그 시점의 파일 목록이 나온다.
> 데이터를 복제하지 않고 스냅샷을 얻는 방식 → [[Data and model versioning]]

### Delta Lake의 5가지 핵심 기둥

1. **트랜잭션 로그** — 모든 변경을 순차 기록하는 **진실의 원천**. ACID·원자성 보장.
2. **스냅샷 & 체크포인트** — 로그를 **요약**해 현재 상태를 정의. 빠른 읽기와 **Time Travel의 기준점**.
3. **스키마 관리** — Enforcement(오염 방지) + Evolution(유연한 구조 변경).
4. **데이터 최적화** — **Compaction**으로 작은 파일 문제 해결, **Z-Ordering**으로 쿼리 속도 향상.
5. **오픈 스토리지** — 벤더 종속 없는 개방형 포맷. **실제 데이터는 Parquet 파일**로 클라우드에 저장.

> 2번의 **체크포인트**가 중요하다 — 로그가 수만 개 쌓이면 매번 전부 읽을 수 없으니 주기적으로
> 요약본을 만든다. [[Stream processing semantics]]의 checkpointing과 이름은 같지만 목적이 다르다
> (여기선 읽기 성능, 거기선 장애 복구).

## 기존 페이지와의 대조

- **[[Table formats]]의 열린 질문 일부 해소:**
  - ✅ **"어느 것이 time travel을 지원하는가"** — **Delta는 지원한다**(강의가 챕터 제목으로 쓴다).
  - ✅ **트랜잭션 로그의 온디스크 구조** — `_delta_log/000000.json`, Add/Remove, 순차 재생,
    optimistic concurrency, 체크포인트 요약. **Delta에 한해** 답이 나왔다.
  - ❌ **Iceberg vs Delta vs Hudi 선택 기준** — 여전히 없다. 이 덱은 Delta만 다루고 다른 둘을
    언급조차 하지 않는다. **Iceberg 1차 문서 필요성은 그대로 남는다.**
- **보강** — 레이크가 늪이 되는 5가지 구조적 원인, 5대 기둥(특히 Compaction·Z-Ordering),
  "Parquet 파일로 저장한다"는 명시.
- **연결** — CH02-4,5,6이 남긴 **small files 문제**를 여기서 compaction으로 푼다. 두 덱을 이어 읽으면
  "왜 테이블 포맷이 필요한가"가 완성된다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Table formats]], [[Analytical data storage tiers]],
  [[Columnar and in-memory data formats]], [[Data and model versioning]]
- 앞 챕터: [[AI DE Course - Ch2-4,5,6 Parquet and Avro]] — small files 문제의 출처

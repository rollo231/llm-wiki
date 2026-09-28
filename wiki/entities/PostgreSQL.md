---
type: entity
title: PostgreSQL
aliases: [Postgres, PG]
tags: [데이터베이스, RDBMS]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[DB 면접 5 NoSQL과 RDBMS 비교]]"
  - "[[AI DE 강의 4-03 고가용성·복제·합의]]"
---

# PostgreSQL

오픈소스 [[관계형 데이터베이스]]다. [[인프런 DB 면접 강의]]는 대부분의 답을 [[MySQL]] InnoDB 기준으로 하고, PostgreSQL은 [[DB 면접 5 NoSQL과 RDBMS 비교]]의 Q1-4 "MySQL과 PostgreSQL은 어떤 차이가 있나요?"(p82–84)와 p59의 그림(인덱스가 힙을 가리키는 구조)에서 비교 대상으로 나온다. 같은 질문이 PostgreSQL에서는 다른 답을 갖는 곳이 많아서, 이 페이지가 그 차이를 모은다.

## MySQL과의 네 가지 차이 (p84)

자료의 Gold 답은 네 가지를 든다. 판정은 PostgreSQL 공식 문서와 대조한 결과다(2026-09-28).

| # | 자료의 서술 | 판정 | 근거 |
|---|---|---|---|
| 1 | 기본 격리 수준이 MySQL은 REPEATABLE READ, PostgreSQL은 READ COMMITTED | 맞음 | "Read Committed is the default isolation level in PostgreSQL" |
| 2 | InnoDB는 PK가 클러스터링 인덱스이고 리프에 데이터가 있지만, PostgreSQL은 리프에 위치 식별자만 둔다 | 맞음 | 행은 힙 테이블에 있고, 인덱스 항목은 행의 물리 위치(`ctid`)를 가리킨다. "All indexes in PostgreSQL are secondary indexes" |
| 3 | MySQL은 DB → 테이블, PostgreSQL은 DB → 스키마 → 테이블이라 권한 묶기가 쉽다 | 맞음 | "A database contains one or more named schemas, which in turn contain tables." MySQL에서는 스키마와 데이터베이스가 같은 말이다 |
| 4 | MVCC를 MySQL은 언두 로그로, PostgreSQL은 "원본에 마킹 후 새 레코드를 추가하는 MGA 방식"으로 구현한다 | 단서 필요 | 동작 설명은 맞다. "MGA"(Multi-Generational Architecture)는 PostgreSQL 문서의 용어가 아니다. Firebird 문서가 자기 구조를 부르는 이름이다(출처는 [[MVCC]]) |

[격리 수준: https://www.postgresql.org/docs/current/transaction-iso.html · 인덱스: https://www.postgresql.org/docs/current/indexes-index-only-scans.html · 스키마: https://www.postgresql.org/docs/current/ddl-schemas.html · 시스템 컬럼: https://www.postgresql.org/docs/current/ddl-system-columns.html , 2026-09-28 확인] 4번에서 "MGA"가 PostgreSQL 문서에 없다는 것은 postgresql.org의 사이트 검색으로 PostgreSQL 18 문서(`/docs/18/`)를 찾아 0건이었다는 확인이다(2026-09-28).

4번의 실제 동작은 이렇다. UPDATE는 옛 튜플을 그 자리에서 고치지 않는다. 옛 튜플의 `xmax`에 지운 트랜잭션 ID를 적고("The identity (transaction ID) of the deleting transaction"), 새 튜플을 따로 쓴다. 옛 튜플은 VACUUM이 나중에 회수한다("an UPDATE or DELETE of a row does not immediately remove the old version of the row"). [https://www.postgresql.org/docs/current/routine-vacuuming.html , 2026-09-28 확인] 옛 버전을 언두 로그로 빼 두는 InnoDB와 반대로, PostgreSQL은 옛 버전을 테이블 안에 남긴다. 그래서 PostgreSQL에서는 VACUUM이 운영의 몫이 된다. 비교의 일반론은 [[MVCC]]에 있다.

2번에서 이어지는 결과도 있다. PostgreSQL에는 InnoDB식 클러스터링 인덱스가 없으므로, PK로 찾든 다른 컬럼으로 찾든 인덱스 → 힙의 두 단계다. 예외는 index-only scan이다. 필요한 컬럼이 모두 인덱스에 있고 visibility map이 그 페이지를 all-visible로 표시하면 힙을 건너뛴다. [https://www.postgresql.org/docs/current/indexes-index-only-scans.html , 2026-09-28 확인] 자료 [[DB 면접 4 인덱스]] p52의 "리프 노드의 레코드 주소로 데이터 파일을 읽는다"는 InnoDB에는 틀리고 PostgreSQL에는 맞는 설명이다([[데이터베이스 인덱스]]).

## 격리 수준이 InnoDB와 다르게 동작하는 곳

- SERIALIZABLE을 락이 아니라 SSI(Serializable Snapshot Isolation)로 구현한다. 문서는 직렬 실행을 "emulates"한다고 쓰고, 기법 이름을 "Serializable Snapshot Isolation"이라고 밝힌다. 자료 p10의 "모든 읽기와 쓰기에 Lock을 걸어 순차 실행"은 PostgreSQL에 맞지 않는다.
- REPEATABLE READ에서 다른 트랜잭션이 바꾼 행을 고치려 하면 오류로 중단한다("ERROR: could not serialize access due to concurrent update"). 그래서 PostgreSQL RR에서는 Lost Update가 조용히 생기지 않고, 애플리케이션이 재시도해야 한다. 자료 p38의 "격리 수준으로는 Lost Update를 해결하지 못한다"의 반례다.
- 표준이 REPEATABLE READ에서 허용하는 Phantom Read가 PostgreSQL에서는 생기지 않는다(표 13.1의 "Allowed, but not in PG").
- 스냅숏은 BEGIN이 아니라 트랜잭션의 첫 문장 시점에 잡힌다("as of the start of the first non-transaction-control statement in the transaction").

[https://www.postgresql.org/docs/current/transaction-iso.html , 2026-09-28 확인] 격리 수준 전반은 [[트랜잭션 격리 수준]]에 있다.

## 위키의 다른 자료에서

- [[AI DE 강의 4-03 고가용성·복제·합의]]는 PostgreSQL을 고가용성과 복제의 예로 쓴다. primary-standby, WAL shipping과 streaming replication, 기본 비동기 복제와 `synchronous_commit` 단계다([[복제]] · [[합의 알고리즘]]).
- [[변경 데이터 캡처]]와 [[Debezium]]은 PostgreSQL WAL의 logical decoding과 replication slot을 다룬다.
- HikariCP의 풀 크기 공식 `((core_count * 2) + effective_spindle_count)`는 PostgreSQL 프로젝트가 제시한 것이다([[커넥션 풀]]).

## 관련

- [[MySQL]] · [[관계형 데이터베이스]] · [[MVCC]] · [[트랜잭션 격리 수준]] · [[데이터베이스 인덱스]] · [[DB 면접 5 NoSQL과 RDBMS 비교]] · [[복제]]

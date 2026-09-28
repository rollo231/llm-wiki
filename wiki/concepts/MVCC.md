---
type: concept
title: MVCC
aliases: [Multi-Version Concurrency Control, 다중 버전 동시성 제어, 언두 로그, Undo log, 일관된 읽기, Consistent read, 스냅숏 읽기]
tags: [데이터베이스, 트랜잭션, 동시성, MySQL, PostgreSQL]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/interviews/database/수업 자료.pdf"
  - "[[DB 면접 2 트랜잭션]]"
---

# MVCC

한 행의 여러 버전을 함께 두고, 읽는 트랜잭션마다 "자기 시점에 맞는 버전"을 골라 보여 주는 동시성 제어 방식이다. 읽기가 락을 잡지 않으므로 읽기와 쓰기가 서로를 막지 않는다. PostgreSQL 문서는 MVCC의 주된 이점을 "읽기는 쓰기를 막지 않고 쓰기는 읽기를 막지 않는다"로 요약한다. [PostgreSQL 문서 13.1 Introduction, https://www.postgresql.org/docs/current/mvcc-intro.html , 2026-09-28 확인] [[트랜잭션 격리 수준]] 가운데 READ COMMITTED와 REPEATABLE READ가 이 방식으로 구현되고, PostgreSQL의 SERIALIZABLE(SSI)도 스냅숏 위에 검사를 더한 것이다. 이 페이지는 [[DB 면접 2 트랜잭션]]의 Q2-2·Q2-3을 바탕으로, InnoDB와 PostgreSQL 매뉴얼을 보탠 것이다.

## 스냅숏은 언제 잡히나

- InnoDB REPEATABLE READ는 트랜잭션 시작(`BEGIN`)이 아니라 첫 일관된 읽기에서 스냅숏을 잡는다. 매뉴얼은 "같은 트랜잭션 안의 모든 일관된 읽기는 그 트랜잭션의 첫 번째 읽기가 만든 스냅숏을 읽는다"고 쓴다. 시작 시점으로 당기려면 `START TRANSACTION WITH CONSISTENT SNAPSHOT`을 쓴다. [MySQL 8.4 매뉴얼 17.7.2.3 Consistent Nonlocking Reads, https://dev.mysql.com/doc/refman/8.4/en/innodb-consistent-read.html , 2026-09-28 확인]
- InnoDB READ COMMITTED는 같은 트랜잭션 안에서도 일관된 읽기마다 새 스냅숏을 잡는다. [MySQL 8.4 매뉴얼 17.7.2.1, https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html , 2026-09-28 확인]
- 위키가 MySQL 9.2.0(Innovation 릴리스)을 로컬에 띄워 확인했다. `BEGIN` 뒤 첫 읽기 전에 다른 세션이 커밋한 값은 보였고, `START TRANSACTION WITH CONSISTENT SNAPSHOT` 뒤에 커밋된 값은 보이지 않았다. (2026-09-28)
- PostgreSQL REPEATABLE READ도 `BEGIN`이 아니라 트랜잭션 제어문이 아닌 첫 문장이 시작될 때의 스냅숏을 본다. [PostgreSQL 문서 13.2.2, https://www.postgresql.org/docs/current/transaction-iso.html , 2026-09-28 확인]

## 어떤 버전이 보이나

스냅숏을 잡은 쿼리는 "그 시점 이전에 커밋한 트랜잭션의 변경은 보고, 그 뒤에 커밋했거나 아직 커밋하지 않은 트랜잭션의 변경은 보지 않는다". [MySQL 8.4 매뉴얼 17.7.2.3, 2026-09-28 확인] 기준은 상대 트랜잭션이 언제 시작했느냐가 아니라 스냅숏 시점에 커밋되어 있었느냐다. 나보다 먼저 시작했어도 스냅숏 시점에 아직 진행 중이던 트랜잭션의 변경은, 그 트랜잭션이 나중에 커밋해도 계속 보이지 않는다. 같은 로컬 MySQL 9.2.0에서 먼저 시작해 UPDATE만 해 둔 트랜잭션을 내 첫 읽기 뒤에 커밋시켰더니, 내 트랜잭션은 끝까지 옛 값을 읽었다. (2026-09-28) 매뉴얼은 이 스냅숏을 read view라고 부른다(17.7.2.4 Locking Reads). read view가 스냅숏 시점에 활성이던 트랜잭션 목록을 들고 이것으로 버전을 가른다는 내부 구조는 널리 알려진 설명이지만, 위키는 이번에 1차 자료로 확인하지 않았다.

한 가지 예외가 있다. 스냅숏은 SELECT에 적용되고 UPDATE·DELETE에는 꼭 적용되지 않는다. 다른 트랜잭션이 방금 커밋한 행을 내 UPDATE가 고칠 수 있고, 고친 뒤에는 그 행이 내게도 보인다. [MySQL 8.4 매뉴얼 17.7.2.3, 2026-09-28 확인] 이 예외 때문에 InnoDB REPEATABLE READ에서 Lost Update가 생긴다([[트랜잭션 격리 수준]]).

## 옛 버전은 어디에 두나

| | InnoDB (MySQL) | PostgreSQL |
|---|---|---|
| 최신 버전의 자리 | 클러스터링 인덱스의 행 자체 | 힙에 새 튜플을 추가 |
| 옛 버전의 자리 | 언두 로그(rollback segment) | 힙의 옛 튜플이 그대로 남음 |
| 버전 판별 | 행마다 숨은 필드 `DB_TRX_ID`(마지막으로 넣거나 고친 트랜잭션)와 `DB_ROLL_PTR`(언두 레코드를 가리키는 포인터) | 튜플의 `xmin`·`xmax`(만든·지운 트랜잭션 ID) |
| 회수 | purge 스레드가 언두 로그와 delete-mark된 레코드를 지운다 | VACUUM이 죽은 튜플을 회수한다 |

- InnoDB는 행마다 `DB_TRX_ID`(6바이트)와 `DB_ROLL_PTR`(7바이트)을 덧붙인다. 읽는 트랜잭션이 시작된 뒤 바뀐 레코드라면 언두 로그에서 올바른 버전을 되살린다. [MySQL 8.4 매뉴얼 17.3 InnoDB Multi-Versioning, https://dev.mysql.com/doc/refman/8.4/en/innodb-multi-versioning.html , 2026-09-28 확인]
- 언두 로그는 insert용과 update용으로 나뉜다. insert 언두는 커밋하면 버릴 수 있지만, update 언두는 그 옛 버전이 필요할 수 있는 스냅숏을 가진 트랜잭션이 하나도 남지 않은 뒤에야 버릴 수 있다. [같은 절, 2026-09-28 확인] 그래서 오래 열린 트랜잭션 하나가 언두 로그 회수를 붙잡는다. 매뉴얼도 일관된 읽기만 하는 트랜잭션까지 주기적으로 커밋하라고 권하고, 그러지 않으면 rollback segment가 너무 커져 언두 테이블스페이스를 채울 수 있다고 쓴다. [같은 절, 2026-09-28 확인]
- InnoDB에서 DELETE한 행은 곧바로 물리적으로 지워지지 않는다. 매뉴얼은 삽입과 삭제가 비슷한 속도로 계속되면 purge가 뒤처져 "죽은" 행 때문에 테이블이 계속 커질 수 있다고 경고한다. [같은 절, 2026-09-28 확인]
- PostgreSQL에서도 UPDATE와 DELETE는 옛 버전을 곧바로 지우지 않는다. 회수는 VACUUM의 몫이다. [PostgreSQL 문서 24.1.2 Recovering Disk Space, https://www.postgresql.org/docs/current/routine-vacuuming.html , 2026-09-28 확인]
- 자료(p84)는 PostgreSQL의 방식을 "MGA"라고 부른다. MGA(multi-generational architecture)는 Firebird 문서가 자기 구조를 부르는 이름이고(「Because Firebird uses multi-generational architecture, every time a row is updated or deleted, Firebird keeps a copy of the previous version in the database.」), PostgreSQL 문서의 용어는 아니다. [Firebird gfix 문서, https://firebirdsql.org/file/documentation/html/en/firebirddocs/gfix/firebird-gfix.html , 2026-09-28 확인] 자세한 비교는 [[PostgreSQL]]에 있다.

## MVCC가 막지 않는 것

- 쓰기끼리의 충돌. 같은 행을 두 트랜잭션이 고치면 여전히 행 락으로 줄을 선다([[데이터베이스 락]]).
- 잠금 읽기. `SELECT ... FOR UPDATE`는 스냅숏이 아니라 최신 데이터를 읽는다. 매뉴얼은 일관된 읽기가 read view에 있는 레코드에 걸린 락을 무시한다고 쓴다. [MySQL 8.4 매뉴얼 17.7.2.4 Locking Reads, https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html , 2026-09-28 확인] 그래서 배타 락이 걸린 행도 일반 SELECT로는 읽힌다.

## 면접에서

- 자료의 Gold 답(p19)의 뼈대(여러 버전, 언두 영역, Lock 없는 읽기, 스냅숏)는 그대로 써도 된다. 스냅숏 시점을 "트랜잭션 시작"이 아니라 "첫 읽기"라고 정확히 말하면 꼬리 질문(START TRANSACTION WITH CONSISTENT SNAPSHOT)에 대비된다.
- "보이는 버전의 기준"을 물으면 시작 순서가 아니라 커밋 여부라고 답한다.
- 이어질 만한 질문은 "긴 트랜잭션이 왜 나쁜가"다. 락과 커넥션 점유(자료 p7) 말고도 언두 로그·VACUUM 회수를 붙잡는다는 답을 보탤 수 있다. 이 질문은 위키가 예상한 것이다.

## 자료의 서술과 정정

| 쪽 | 자료 서술 | 판정 | 근거 |
|---|---|---|---|
| p10·p19 | REPEATABLE READ는 트랜잭션이 생성·시작된 시점의 스냅숏을 읽는다 | 단서 필요 | InnoDB·PostgreSQL 모두 첫 읽기(첫 문장) 시점 |
| p16 | 내 트랜잭션보다 나중에 시작된 트랜잭션이 커밋한 변경은 무시 | 틀림 | 기준은 스냅숏 시점의 커밋 여부, 먼저 시작했지만 진행 중이던 트랜잭션의 변경도 숨김 |
| p16 | Dirty Read는 언두 영역의 커밋 전 원본을 읽어 해결 | 맞음 (InnoDB) | PostgreSQL은 힙의 옛 튜플을 읽는다 |
| p19 | MVCC는 Lock 없이 읽기를 해서 동시성을 높인다 | 맞음 | 잠금 읽기와 쓰기끼리는 여전히 락 |

## 관련

- [[트랜잭션 격리 수준]] · [[데이터베이스 락]] · [[관계형 데이터베이스]]
- [[MySQL]] · [[PostgreSQL]]
- [[Delta Lake]] (트랜잭션 로그와 Time Travel도 여러 버전을 남기는 방식이다. 이 연결은 위키가 했다)
- 자료: [[DB 면접 2 트랜잭션]]

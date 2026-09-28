---
type: entity
title: MySQL
aliases: [InnoDB, MySQL InnoDB]
tags: [데이터베이스, RDBMS]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[DB 면접 2 트랜잭션]]"
  - "[[DB 면접 3 Lock과 동시성 제어]]"
  - "[[DB 면접 4 인덱스]]"
  - "[[DB 면접 5 NoSQL과 RDBMS 비교]]"
  - "[[DB 면접 7 운영]]"
---

# MySQL

오픈소스 [[관계형 데이터베이스]]다. 기본 스토리지 엔진은 InnoDB이고, 트랜잭션·행 락·MVCC·클러스터링 인덱스는 전부 InnoDB의 성질이다. [[인프런 DB 면접 강의]]의 답은 대부분 MySQL InnoDB를 전제한다. 자료가 MySQL·InnoDB를 이름으로 밝히는 쪽은 p13·p16·p19·p20–22·p56·p82–84·p122·p127–128·p134이고, 격리 수준의 정의(p10)·Section 3의 락·인덱스 구조(p45–55)처럼 엔진 이름 없이 일반론으로 읽히는 답도 InnoDB 이야기인 경우가 많다. 이 관찰은 위키가 한 것이다.

위키의 MySQL 서술은 8.4 매뉴얼을 기준으로 한다. 8.4는 LTS 릴리스이고 9.x는 Innovation 릴리스다. 매뉴얼의 「MySQL Release Models」에 따르면 LTS는 필요한 수정만 담고 기능 추가·제거는 첫 LTS 릴리스(8.4.0)에서만 하며, Innovation 릴리스는 새 기능과 동작 변경을 담고 다음 Innovation 릴리스가 나올 때까지만 지원된다. [https://dev.mysql.com/doc/refman/8.4/en/mysql-releases.html , 2026-09-28 확인. 요약 도구를 거쳐 읽었고 원문 문장은 대조하지 않았다]

## 이 자료와 만나는 InnoDB의 성질

각 주제의 전문은 개념 페이지에 있고, 여기에는 InnoDB에 특유한 점만 모은다.

| 주제 | InnoDB의 동작 | 전문 |
|---|---|---|
| 기본 격리 수준 | REPEATABLE READ ("The default isolation level for InnoDB is REPEATABLE READ") | [[트랜잭션 격리 수준]] |
| MVCC | 언두 로그에 옛 버전을 두고, consistent read는 첫 읽기 시점의 스냅숏을 본다 | [[MVCC]] |
| SERIALIZABLE | autocommit이 꺼져 있으면 plain SELECT를 `FOR SHARE`로 바꿔 락을 건다 | [[트랜잭션 격리 수준]] |
| 행 락 | 레코드 락, 갭 락, 넥스트 키 락. unique 인덱스로 존재하는 한 행을 찾으면 레코드 락만 건다 | [[데이터베이스 락]] |
| 인덱스 구조 | PK가 클러스터링 인덱스이고 리프가 곧 행이다. 세컨더리 인덱스 리프에는 인덱스 컬럼과 PK가 있다 | [[데이터베이스 인덱스]] |
| 해시 인덱스 | 사용자가 HASH 인덱스를 만들 수 없다. `USING HASH`라고 적어도 B-tree로 만든다. 어댑티브 해시 인덱스는 내부 기능이고, 8.4부터 기본으로 꺼져 있다(`innodb_adaptive_hash_index`, 8.4 이전에는 기본으로 켜져 있었다) | [[데이터베이스 인덱스]] |
| 데드락 | wait-for graph로 감지하고 작은 트랜잭션(삽입·갱신·삭제한 행 수 기준)을 롤백한다. 행 락 대기 한도는 `innodb_lock_wait_timeout`(기본 50초)이고, `lock_wait_timeout`은 메타데이터 락용이다 | [[데드락 재현과 해법]] |
| 복제 | 소스가 binlog에 쓰고, 레플리카의 receiver 스레드가 relay log로 복사하고, applier 스레드가 재실행한다. 기본은 비동기다 | [[복제]] |
| 운영 도구 | 슬로우 쿼리 로그(`long_query_time`), `EXPLAIN`·`EXPLAIN ANALYZE`(8.0.18+), `SHOW PROCESSLIST` | [[실행 계획]] |

어댑티브 해시 인덱스의 기본값은 8.4 매뉴얼의 InnoDB 시스템 변수 페이지에서 원문으로 확인했다("This variable is disabled by default", "Before MySQL 8.4, this option was enabled by default"). [https://dev.mysql.com/doc/refman/8.4/en/innodb-parameters.html , 2026-09-28 확인] 기본 격리 수준 행의 인용문은 격리 수준 페이지(https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html)를 요약 도구를 거쳐 읽은 것이고, 원문 문장은 대조하지 못했다. 나머지 행의 근거는 각 개념 페이지에 있다.

## 용어 변경: Master/Slave에서 Source/Replica로

자료는 복제 역할을 Master/Slave로 부른다(p119·p122). MySQL은 8.0.22부터 `START REPLICA`가 `START SLAVE`를 대체하고("From MySQL 8.0.22, use START REPLICA in place of START SLAVE"), 8.0 매뉴얼은 복제 스레드를 "I/O (receiver) thread"처럼 옛 이름과 새 이름(receiver·applier)을 함께 적는다. 8.0.27부터 applier가 기본 4개인 멀티스레드다("Beginning with MySQL 8.0.27, the default value is 4, which means that replicas are multithreaded by default"). [https://dev.mysql.com/doc/refman/8.0/en/start-replica.html · https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html , 2026-09-28 확인]

[[Redis]]도 같은 이유로 5.0부터 master-replica 용어를 쓴다.

## PostgreSQL과의 비교

자료 p84의 네 가지 차이(기본 격리 수준, 인덱스 구조, 스키마 계층, MVCC 구현)와 판정은 [[PostgreSQL]]에 있다.

## 관련

- [[PostgreSQL]] · [[관계형 데이터베이스]] · [[트랜잭션 격리 수준]] · [[MVCC]] · [[데이터베이스 락]] · [[데이터베이스 인덱스]] · [[복제]] · [[실행 계획]] · [[커넥션 풀]] · [[HikariCP]]
- 위키 안의 다른 언급: [[변경 데이터 캡처]](binlog 기반 CDC), [[Debezium]]

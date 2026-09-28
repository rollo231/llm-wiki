---
type: entity
title: HikariCP
aliases: [Hikari]
tags: [Java, 데이터베이스, 커넥션]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[DB 면접 6 커넥션과 커넥션 풀]]"
---

# HikariCP

Java의 JDBC [[커넥션 풀]] 라이브러리다. Spring Boot가 기본으로 고르는 풀이다. Spring Boot 문서는 "We prefer HikariCP for its performance and concurrency. If HikariCP is available, we always choose it"라고 쓰고, 없을 때 Tomcat 풀, Commons DBCP2, Oracle UCP 순으로 넘어간다. `spring-boot-starter-jdbc`나 `spring-boot-starter-data-jpa`를 쓰면 HikariCP가 함께 들어온다. [https://docs.spring.io/spring-boot/reference/data/sql.html , 2026-09-28 확인]

[[DB 면접 6 커넥션과 커넥션 풀]]은 모니터링 질문(p106)에서 HikariCP를 기준으로 답한다.

## 주요 설정

README에서 직접 확인한 기본값이다. [https://github.com/brettwooldridge/HikariCP , 2026-09-28 확인]

| 설정 | 기본값 | 뜻 |
|---|---|---|
| `maximumPoolSize` | 10 | 풀이 가질 수 있는 커넥션 최대 수(쉬는 것과 쓰는 것을 합쳐). 다 차면 `getConnection()`이 `connectionTimeout`만큼 막힌다 |
| `minimumIdle` | `maximumPoolSize`와 같음 | 유지할 최소 유휴 커넥션 수 |
| `connectionTimeout` | 30000 (30초) | 풀에서 커넥션을 기다리는 최대 시간. 최소 250ms. 넘기면 `SQLException` |
| `idleTimeout` | 600000 (10분) | 유휴 커넥션을 닫기까지의 시간. `minimumIdle`이 `maximumPoolSize`보다 작을 때만 쓴다 |
| `maxLifetime` | 1800000 (30분) | 커넥션 하나의 최대 수명 |
| `leakDetectionThreshold` | 0 (꺼짐) | 커넥션이 풀 밖에 이만큼 머물면 누수 가능성을 로그로 남긴다. 켜려면 2000ms 이상 |

기본 크기 10은 [[스레드 풀]]이 인용한 소스 상수 `DEFAULT_POOL_SIZE = 10`과 같은 값이다.

`connectionTimeout`이라는 이름은 드라이버의 연결 타임아웃과 헷갈리기 쉽다. README의 문장은 "the maximum number of milliseconds that a client (that's you) will wait for a connection from the pool"이다. 드라이버 설정과의 구분은 [[커넥션 풀]]에 있다.

## 풀 크기에 대한 입장

HikariCP 위키의 「About Pool Sizing」은 풀을 작게 두라고 한다. 요지는 "You want a small pool, saturated with threads waiting for connections"이고, 출발점으로 PostgreSQL 프로젝트의 공식 `connections = ((core_count * 2) + effective_spindle_count)`를 소개한다. [https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing , 2026-09-28 확인] 근거와 SSD에 대한 반론은 [[커넥션 풀]]에서 다룬다.

## 메트릭

Micrometer를 붙이면 `hikaricp.` 접두사로 메트릭을 낸다. 소스 `MicrometerMetricsTracker.java`에 정의된 이름은 `hikaricp.connections`(전체), `.active`, `.idle`, `.pending`, `.max`, `.min`, `.acquire`(획득 대기 시간), `.usage`(사용 시간), `.creation`(생성 시간), `.timeout`(타임아웃 횟수)이다. [https://github.com/brettwooldridge/HikariCP , 2026-09-28 확인]

## 관련

- [[커넥션 풀]] · [[스레드 풀]] · [[DB 면접 6 커넥션과 커넥션 풀]] · [[MySQL]] · [[PostgreSQL]]

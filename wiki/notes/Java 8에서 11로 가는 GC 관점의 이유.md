---
type: note
title: Java 8에서 11로 가는 GC 관점의 이유
aliases: [Java 8 → 11, JDK 8 → 11 마이그레이션, Java 8 vs Java 11 GC]
tags: [Java, JVM, GC, 마이그레이션, 면접]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "[[Java 면접 3 GC]]"
---

# Java 8에서 11로 가는 GC 관점의 이유

「Java 8은 Parallel GC가 기본이라 큰 램에 톰캣을 여러 개 띄워 멈춤을 피했고, Java 11의 G1은 큰 램을 잘라서 치우니 전환해야 한다」는 주장이 논리적인지 따진 질의에서 나왔다. 결론은 방향은 맞지만 빈 곳이 셋 있다는 것이다.

## 맞는 부분

- Java 8의 기본은 Parallel이고, Parallel은 전부 STW다. Full GC 멈춤은 힙 크기에 비례해 길어진다([[가비지 컬렉터]]의 기본 GC 변천).
- G1은 Region 단위로 일부만 치운다. `-XX:MaxGCPauseMillis`(기본 200ms)에 맞춰 한 번에 수거할 Region 수를 고르므로 큰 힙에서도 한 번의 멈춤을 제한할 수 있다. 「큰 램을 잘라서 처리한다」가 이 뜻이면 맞다.

## 빈 곳 1 — G1은 Java 8에도 있다

G1은 JDK 9에서 기본값이 되었을 뿐, Java 8에서도 `-XX:+UseG1GC`로 쓸 수 있었다. Java 8 튜닝 가이드에 G1 장이 따로 있고, 목표를 "heap sizes of around 6 GB or larger, and a stable and predictable pause time below 0.5 seconds"로 적는다. [Oracle, 「Java Platform, Standard Edition HotSpot Virtual Machine Garbage Collection Tuning Guide」 Java 8, Garbage-First Garbage Collector, https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/g1_gc.html , 2026-09-27 확인]

그러니 「G1을 쓰려면 11로 가야 한다」는 틀렸다. 정확히는 Java 8의 G1이 덜 성숙했다. 대표가 Full GC다. JDK 10 전까지 G1의 Full GC는 단일 스레드 mark-sweep-compact여서, Java 8 G1에서 Full GC가 나면 병렬 Full GC를 가진 Parallel보다 오래 멈출 수 있었다. JEP 307이 이를 병렬화했다: "The current implementation of the full GC for G1 uses a single threaded mark-sweep-compact algorithm." [JEP 307 「Parallel Full GC for G1」(JDK 10), https://openjdk.org/jeps/307 , 2026-09-27 확인]

그래서 「Java 11이면 큰 힙에 G1을 안심하고 쓸 수 있다」고 말하는 편이 정확하다.

## 빈 곳 2 — 인스턴스를 여러 개 띄우는 건 GC 때문만이 아니다

작은 JVM 여러 개는 힙이 작아 GC 멈춤이 짧다. 하지만 여러 인스턴스를 두는 이유에는 장애 격리(하나가 죽어도 나머지가 요청을 받는다), 무중단 배포(하나씩 돌려 교체), 스레드·커넥션 한도 분산([[스레드 풀]])도 있다. G1으로 바꿔도 인스턴스 분리는 남고, 「GC 때문에 억지로 쪼개던 부분」만 줄어든다. 이 문단은 위키의 판단이며 1차 자료로 확인하지 않았다.

## 빈 곳 3 — G1도 멈춘다

- 200ms는 목표일 뿐 보장하지 않는다. Young GC와 Mixed GC 자체가 STW다([[가비지 컬렉션]]의 Stop-The-World 절).
- 수거보다 할당이 빠르면 Full GC로 떨어진다. Humongous 객체가 많으면 더 그렇다([[가비지 컬렉터]]의 Humongous 절).
- 아주 큰 힙에서 멈춤을 ms 단위로 줄이려면 ZGC를 쓴다. JDK 11에서는 실험 기능이었고 JDK 15에서 정식이 됐다(JEP 333 → 377).

## GC 말고도 있는 8 → 11의 이유

| 이유 | 내용 | 근거 |
|---|---|---|
| G1 성숙 | JDK 9 기본화(JEP 248), JDK 10 병렬 Full GC(JEP 307) | [[가비지 컬렉터]] · JEP 307 |
| 메모리 절약 | Compact Strings: Latin-1 문자열을 1바이트로 저장해 문자열이 많은 힙이 준다 | JEP 254 (JDK 9), https://openjdk.org/jeps/254 |
| 컨테이너 인식 | JVM이 cgroup의 CPU·메모리 제한을 읽는다 | JDK-8146115 (JDK 10). 8u191로 백포트돼 Java 8 최신 업데이트로도 된다 |
| LTS | 11은 8 다음 LTS | — |

[JDK-8146115 「Improve docker container detection and resource configuration usage」, 수정 버전 10, 백포트 8u191 · 8u192 · 8u201 · 8u202, https://bugs.openjdk.org/browse/JDK-8146115 , 2026-09-27 확인]

컨테이너에서는 반대 함정도 있다. JDK 9~26은 CPU 2개 미만 또는 메모리 1792MB 미만이면 G1 대신 Serial을 고른다([[가비지 컬렉터]]의 컨테이너 함정). 11로 올려도 작은 파드에서는 G1이 켜지지 않을 수 있다.

## 2026년에는 질문 자체가 낡았다

Spring Boot 3.0부터 Java 17이 최소 버전이다: "Spring Boot 3.0 requires Java 17 as a minimum version." 현재 정식 버전 4.1.1(2026-08-20)도 최소 Java 17이고, Java 26까지 호환된다(4.2는 마일스톤 단계). 그래서 지금 마이그레이션 질문은 「8 → 17 또는 21·25」가 현실적이다. 그 사이에 ZGC 정식(15), Generational ZGC(21), 가상 스레드(21, [[스레드 풀]])가 들어온다. [Spring Boot 3.0 Release Notes, https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Release-Notes ; Spring Boot 4.1.1 System Requirements, https://docs.spring.io/spring-boot/system-requirements.html , 2026-09-27 확인]

## 면접에서

「Java 8의 기본인 Parallel GC는 Full GC 멈춤이 힙 크기에 비례해 큰 힙을 쓰기 부담스러웠습니다. G1은 Java 8에도 있었지만 Full GC가 단일 스레드였고, JDK 9에서 기본이 되고 JDK 10에서 Full GC가 병렬화되면서 11에서는 큰 힙에 G1을 안심하고 쓸 수 있게 됐습니다. G1은 Region 단위로 목표 멈춤 시간에 맞춰 일부만 치웁니다. 다만 인스턴스를 여러 개 두는 건 장애 격리와 무중단 배포 때문이기도 해서 GC만으로 없어지지는 않고, 지금은 Spring Boot 3가 17을 요구하니 17 이상으로 가는 게 현실적입니다.」

## 관련

- [[가비지 컬렉터]] · [[가비지 컬렉션]] · [[지연 시간과 처리량]] · [[스레드 풀]] · [[JVM]]
- 자료: [[Java 면접 3 GC]]

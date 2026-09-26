---
type: entity
title: JVM
aliases: [Java Virtual Machine, 자바 가상 머신, HotSpot]
tags: [Java, 런타임, 면접]
created: 2026-09-26
updated: 2026-09-26
sources:
  - "[[Java 면접 2 JVM과 실행 원리]]"
  - "[[Java 면접 3 GC]]"
---

# JVM

Java Virtual Machine. 바이트코드(.class)를 실행하는 가상 머신이다. 명세는 JVMS(Java Virtual Machine Specification)이고, 가장 널리
쓰이는 구현은 OpenJDK의 **HotSpot**이다. 이 위키의 JVM 서술은 HotSpot 기준이다.

## 장단점

- **플랫폼 독립** — 같은 바이트코드가 OS·CPU가 달라도 돈다. JVM이 OS와 프로그램 사이에서 중재한다.
- **자동 메모리 관리** — [[가비지 컬렉션]]이 해제를 맡아 해제 누락·이중 해제 같은 휴먼 에러를 없앤다. 대가는 STW pause다.
- **느린 시작, 빠른 피크** — 처음에는 인터프리터로 돌아 느리고, [[JIT 컴파일]]이 hot 코드를 기계어로 바꾸면서 빨라진다.
  런타임 프로파일로 최적화하므로 피크 성능이 AOT 컴파일 언어에 근접하거나 넘기도 한다. 대가는 워밍업과 메모리 사용량이다.

## 실행 과정 (JVMS 순서)

1. **빌드 시점** — `javac`가 .java를 바이트코드(.class)로 컴파일한다. **JVM 밖에서 끝나는 일이다.**
2. **JVM 기동** — `java` 명령으로 JVM 프로세스가 뜨고 힙 등 메모리를 예약한다.
3. **클래스 로딩 → 링킹(검증·준비·해석) → 초기화** — 클래스는 처음 필요할 때 로드된다(지연 로딩).
4. **실행** — 실행 엔진이 인터프리터로 시작하고, hot 코드는 [[JIT 컴파일]]로 기계어가 된다.
5. **GC는 "마지막 단계"가 아니라 실행 내내 돈다.**

[Oracle, 「The Java Virtual Machine Specification」 Java SE 25 §5 Loading, Linking, and Initializing,
https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-5.html , 2026-09-26 확인]

⚠️ [[Java 면접 2 JVM과 실행 원리]] Q2의 5단계는 "JVM 메모리 할당 → javac 컴파일" 순서로 적어 성립하지 않는다(javac는 JVM 실행
전에 끝난다). GC를 다섯째 단계로 둔 것도 오해를 부른다.

## 구성 요소

| 구성 | 역할 | 자세히 |
|---|---|---|
| 클래스 로더 | .class를 찾아 로드·링크·초기화 | 위 실행 과정 |
| 런타임 데이터 영역 | 힙(객체·static 필드), 스레드별 스택, 메타스페이스(클래스 메타데이터, JDK 8부터), 코드 캐시 | [[가비지 컬렉션]] |
| 실행 엔진 | 인터프리터 + JIT(C1·C2) | [[JIT 컴파일]] |
| GC | 힙 회수 | [[가비지 컬렉션]] · [[가비지 컬렉터]] |

## DE와의 관계

DE 스택의 상당수가 JVM 위에서 돈다 — [[Apache Spark]](Scala), [[Apache Kafka]](Scala·Java), [[Apache Flink]](Java). 그래서
JVM 지식은 면접용만이 아니라 운영 지식이다. *(위키의 연결)*

- **GC pause** — Spark executor의 긴 Full GC는 heartbeat 타임아웃과 태스크 재시도로, Flink에서는 체크포인트 지연으로 번진다.
  → [[가비지 컬렉터]]
- **힙 크기 설계** — Kafka 브로커는 데이터를 OS 페이지 캐시에 맡기므로 힙을 작게 두는 것이 관례다. 힙을 키우면 GC만 비싸진다.
- **워밍업** — 스트리밍 잡을 재시작한 직후 처리량이 낮은 것도 JIT가 차가운 탓이 크다. → [[JIT 컴파일]]

## 관련

- 개념: [[JIT 컴파일]] · [[가비지 컬렉션]] · [[가비지 컬렉터]] · [[동시성 문제]]
- 자료: [[Java 면접 2 JVM과 실행 원리]] · [[Java 면접 3 GC]] · [[인프런 Java 면접 강의]]

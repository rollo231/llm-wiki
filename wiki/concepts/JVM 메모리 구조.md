---
type: concept
title: JVM 메모리 구조
aliases: [런타임 데이터 영역, Runtime data areas, 메서드 영역, 메소드 영역, Method area, Metaspace, 메타스페이스, 런타임 상수 풀, JVM 스택, PC 레지스터, PermGen]
tags: [Java, JVM, 메모리, 면접]
created: 2026-09-26
updated: 2026-09-27
sources:
  - "[[Java 면접 2 빈출 질문]]"
  - "[[Java 면접 3 GC]]"
---

# JVM 메모리 구조

[[JVM]]이 프로그램을 실행하는 동안 쓰는 메모리 영역이다. 이 영역은 두 층으로 봐야 한다. 하나는 **JVMS가 정한 논리 모델**(런타임
데이터 영역)이고, 다른 하나는 **HotSpot이 그 모델을 실제로 구현한 모습**이다. 면접 답은 대개 논리 모델에서 멈추고, 꼬리 질문은
구현 쪽에서 나온다.

## JVMS의 런타임 데이터 영역 (§2.5)

| 영역 | 범위 | 담는 것 |
|---|---|---|
| **PC 레지스터** | 스레드마다 | 현재 실행 중인 JVM **명령어의 주소**. native 메서드를 실행하는 중에는 값이 정의되지 않는다 |
| **JVM 스택** | 스레드마다 | 메서드 호출마다 프레임 하나를 push하고, 끝나면 pop한다. 프레임에는 지역 변수 배열, 피연산자 스택, **현재 클래스의 런타임 상수 풀 참조**가 있다(§2.6) |
| **네이티브 메서드 스택** | 스레드마다 | native 코드용 스택. **선택 사항**이라 두지 않는 구현도 있다 |
| **힙** | 공유 | 모든 **인스턴스와 배열**. GC가 회수한다 |
| **메서드 영역** | 공유 | 클래스별 구조: 런타임 상수 풀, 필드·메서드 데이터, 메서드·생성자 코드. 명세는 이 영역을 "logically part of the heap"이라 부르면서도 위치와 관리 방식은 구현에 맡긴다 |
| **런타임 상수 풀** | 클래스마다 (메서드 영역에서 할당) | `.class`의 `constant_pool`을 런타임에 표현한 것. 상수와 심볼릭 참조가 들어 있고, [[클래스 로딩]]의 해석 단계가 이 참조를 실제 참조로 바꾼다 |

JVMS는 6개 절로 나눈다. 흔히 "5가지"로 세는 것은 런타임 상수 풀을 메서드 영역 안에 넣었기 때문이다.

[Oracle, 「The Java Virtual Machine Specification」 Java SE 25 §2.5 Run-Time Data Areas · §2.6 Frames,
https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-2.html#jvms-2.5 , 2026-09-26 확인]

## HotSpot에서는

| 논리 영역 | HotSpot의 실제 위치 | 언제부터 |
|---|---|---|
| 메서드 영역의 클래스 메타데이터 | **Metaspace** — 네이티브 메모리. `-XX:MaxMetaspaceSize`로 상한을 둔다 | JDK 8. PermGen을 없앴다(JEP 122) |
| static 필드 | 힙의 `java.lang.Class` 미러 객체 안 | JDK 7 (JDK-7017732) |
| intern된 문자열 | 힙 | JDK 7 (JDK-6962931) |
| JIT가 만든 기계어 | **코드 캐시** — JVMS에 없는 HotSpot 구현 영역. `-XX:ReservedCodeCacheSize` | → [[JIT 컴파일]] |
| JVM 스택 + 네이티브 메서드 스택 | 하나로 합쳐져 있다. Java 스레드 하나에 OS 스레드 스택 하나를 쓰고, Java 프레임과 native 프레임이 같은 스택에 쌓인다. 크기는 `-Xss` | — |

그래서 "메서드 영역은 어디 있나"라는 질문에 "Metaspace"라고만 답하면 반만 맞는다. 메서드 영역이라는 논리 영역은 HotSpot 안에서
Metaspace · 힙 · 코드 캐시로 **흩어져 있다.** *(위키의 종합)* 단서: JVMS §2.5.4가 메서드 영역에 두라고 적은 것은 클래스별 구조(상수 풀,
필드·메서드 데이터, 코드)다. static 필드 값, intern 문자열, JIT 기계어까지 「메서드 영역의 일부」로 보는 것은 PermGen 시절 배치에서
나온 해석이고, 명세는 이것들의 자리를 정하지 않는다.

[OpenJDK JEP 122 「Remove the Permanent Generation」, https://openjdk.org/jeps/122 — 본문은 "native memory"라고만 쓰고, Metaspace라는
이름은 구현(JDK-6964458)과 옵션에서 쓴다 ; JDK-7017732, https://bugs.openjdk.org/browse/JDK-7017732 ; JDK-6962931,
https://bugs.openjdk.org/browse/JDK-6962931 ; Oracle, 「The Java HotSpot Performance Engine Architecture」(JDK 1.x 시절 백서) — "Both Java programming
language methods and native methods share the same stack", https://www.oracle.com/java/technologies/whitepaper.html — 현재 구현은
HotSpot 소스 `src/hotspot/os/linux/os_linux.cpp`의 Java 스레드 스택 배치 그림과 `src/hotspot/share/runtime/stackOverflow.hpp`의
native·VM 코드용 shadow zone으로 확인, https://github.com/openjdk/jdk ; Oracle,
`java` 명령 매뉴얼 JDK 25, https://docs.oracle.com/en/java/javase/25/docs/specs/man/java.html , 2026-09-26 확인]

## 가상 스레드의 스택

위 표의 「OS 스레드 스택 하나」는 **플랫폼 스레드** 이야기다. JDK 21의 가상 스레드(→ [[스레드 풀]])는 스택을 **힙에** 둔다.

- "The stacks of virtual threads are stored in Java's garbage-collected heap as *stack chunk* objects." 스택은 실행하면서 늘고
  줄며, 깊이는 플랫폼 스레드의 스택 크기 설정(`-Xss`)까지 허용한다.
- 가상 스레드는 실행할 때 캐리어(플랫폼) 스레드에 올라가고(mount), 블로킹하면 내려온다(unmount). 스레드 덤프와 예외의 스택
  트레이스에는 캐리어의 프레임이 섞이지 않는다.
- **GC Root가 아니다.** "Unlike platform thread stacks, virtual thread stacks are not GC roots." 그래서 G1처럼 힙을 동시에 훑는
  컬렉터는 가상 스레드 스택 속 참조를 STW 중에 따라가지 않는다. 가상 스레드를 수백만 개 만들어도 루트 스캔 멈춤이 그만큼
  늘지 않는 이유다. → [[가비지 컬렉션]] GC Root

[OpenJDK JEP 444 「Virtual Threads」(JDK 21, Delivered), https://openjdk.org/jeps/444 , 2026-09-27 확인] mount 때 프레임이 힙과 캐리어 스택 사이에서 어떻게 옮겨지는지는 JEP에 적혀 있지 않아 쓰지 않았다.

## 영역별로 나는 오류

| 오류 | 영역 | 흔한 원인 |
|---|---|---|
| `StackOverflowError` | 스레드 스택 | 끝나지 않는 재귀. `-Xss`는 스레드당 크기라, 스레드가 늘면 예약되는 가상 주소 공간도 는다(실제 commit은 쓴 만큼) |
| `OutOfMemoryError: Java heap space` | 힙 | 누수 또는 힙이 너무 작음 → [[가비지 컬렉션]]의 OOM 대응 |
| `OutOfMemoryError: Metaspace` | Metaspace | `MaxMetaspaceSize` 초과. 클래스를 끝없이 생성하거나 재배포 때 클래스 로더가 누수되는 경우가 흔하다고 알려져 있다(Oracle 가이드에는 없는 업계 통념) |

*(위키의 정리 — 오류 메시지는 JDK 표준이다. [Oracle, 「Troubleshooting Guide」 JDK 25 Memory Leaks,
https://docs.oracle.com/en/java/javase/25/troubleshoot/troubleshooting-memory-leaks.html , 2026-09-26 확인])*

## 면접에서

- 구조도를 **스레드별 / 공유**로 먼저 나누면 동시성 질문으로 자연스럽게 넘어간다. 공유 영역(힙 · 메서드 영역)에 있는 것만 여러
  스레드가 동시에 건드릴 수 있고, 지역 변수는 각 스레드의 스택에 있어 안전하다. → [[동시성 문제]] *(위키의 연결)*
- "PC 레지스터 = 몇 번째 줄"이 아니라 "명령어 주소"라고 말한다. 줄 번호는 디버그 정보(`LineNumberTable`)에 따로 있다.
- 힙의 내부(Young · Old)는 이 페이지가 아니라 [[가비지 컬렉션]]에 있다.

## 관련

- [[클래스 로딩]] — 메서드 영역을 채우는 과정
- [[가비지 컬렉션]] — 힙과 GC Root(static 필드가 JDK 7부터 힙에 있다는 정정)
- [[JIT 컴파일]] — 코드 캐시
- [[JVM]] · 자료: [[Java 면접 2 빈출 질문]]

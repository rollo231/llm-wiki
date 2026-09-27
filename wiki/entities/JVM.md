---
type: entity
title: JVM
aliases: [Java Virtual Machine, 자바 가상 머신, HotSpot]
tags: [Java, 런타임, 면접]
created: 2026-09-26
updated: 2026-09-27
sources:
  - "[[Java 면접 2 JVM과 실행 원리]]"
  - "[[Java 면접 3 GC]]"
  - "[[Java 면접 2 빈출 질문]]"
  - "[[Java 면접 기타 빈출 질문 1 자바 기본]]"
---

# JVM

Java Virtual Machine. 바이트코드(.class)를 실행하는 가상 머신이다. JVMS는 이것을 "abstract computing machine"이라 부른다. 실제 기계처럼 명령어 집합이 있고 런타임에 여러 메모리 영역을 다루며, Java 언어는 모르고 `class` 파일 형식만 안다(JVMS §1.2). 명세는 JVMS(Java Virtual Machine Specification)이고, 가장 널리 쓰이는 구현은 OpenJDK의 HotSpot이다. 이 위키의 JVM 서술은 HotSpot 기준이다.

## 장단점

- 플랫폼 독립: 같은 바이트코드가 OS·CPU가 달라도 돈다. JVM이 OS와 프로그램 사이에서 중재한다.
- 자동 메모리 관리: [[가비지 컬렉션]]이 해제를 맡아 해제 누락·이중 해제 같은 휴먼 에러를 없앤다. 대가는 STW pause다.
- 느린 시작, 빠른 피크: 처음에는 인터프리터로 돌아 느리고, [[JIT 컴파일]]이 hot 코드를 기계어로 바꾸면서 빨라진다. 런타임 프로파일로 최적화하므로 피크 성능이 AOT 컴파일 언어에 근접할 수 있다(워크로드에 크게 좌우된다). 이 평가는 위키의 것이다. 대가는 워밍업과 메모리 사용량이다.

## 실행 과정 (JVMS 순서)

1. 빌드 시점: `javac`가 .java를 바이트코드(.class)로 컴파일한다. JVM 밖에서 끝나는 일이다.
2. JVM 기동: `java` 명령으로 JVM 프로세스가 뜨고 힙 등 메모리를 예약한다.
3. 클래스 로딩 → 링킹(검증·준비·해석) → 초기화: HotSpot은 클래스를 처음 필요할 때 로드한다. 명세가 엄격하게 정하는 것은 초기화 시점뿐이다([[클래스 로딩]]).
4. 실행: 실행 엔진이 인터프리터로 시작하고, hot 코드는 [[JIT 컴파일]]로 기계어가 된다.
5. GC는 "마지막 단계"에 오는 것이 아니고, 실행 내내 돈다.

[Oracle, 「The Java Virtual Machine Specification」 Java SE 25 §5 Loading, Linking, and Initializing, https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-5.html , 2026-09-26 확인]

⚠️ [[Java 면접 2 빈출 질문]] Q1은 JVM을 "가상의 운영 체제"라 부른다. JVM이 흉내 내는 것은 OS보다 기계 쪽이다.

⚠️ [[Java 면접 2 JVM과 실행 원리]] Q2의 5단계는 "JVM 메모리 할당 → javac 컴파일" 순서로 적어 성립하지 않는다(javac는 JVM 실행 전에 끝난다). GC를 다섯째 단계로 둔 것도 오해를 부른다.

## 구성 요소

아래 세 갈래(클래스 로더 · 런타임 데이터 영역 · 실행 엔진)는 교과서에서 흔히 쓰는 틀이고 JVMS의 분류가 아니다. JVMS에는 "실행 엔진"이라는 용어가 없고, 인터프리터로 실행할지 기계어로 번역할지는 구현자 재량이다(JVMS 2장 서문).

| 구성 | 역할 | 자세히 |
|---|---|---|
| 클래스 로더 | .class의 바이트를 찾아 로드한다. 링크·초기화는 JVM이 한다 | [[클래스 로딩]] |
| 런타임 데이터 영역 | JVMS: PC 레지스터·JVM 스택·네이티브 메서드 스택(스레드별), 힙·메서드 영역·런타임 상수 풀(공유). HotSpot: 메타스페이스(JDK 8부터), static 필드는 힙(JDK 7부터), 코드 캐시 | [[JVM 메모리 구조]] |
| 실행 엔진 | 인터프리터 + JIT(C1·C2) | [[JIT 컴파일]] |
| GC | 힙 회수 | [[가비지 컬렉션]] · [[가비지 컬렉터]] |

## JDK와 JRE

JRE(Java Runtime Environment)는 JVM과 표준 클래스 라이브러리를 묶은 실행 환경이고, JDK(Java Development Kit)는 여기에 `javac` 같은 개발 도구를 더한 것이다. 개념으로는 지금도 이 구분이 맞다. 다만 「실행만 할 거면 JRE를 따로 설치한다」는 낡았다. JDK 9에서 런타임이 모듈로 나뉘었고(JEP 220), `jlink`(JEP 282)로 앱에 필요한 모듈만 담은 런타임을 만들 수 있게 됐다. Oracle JDK 11 Migration Guide는 "Oracle no longer offers JRE and Server JRE downloads", "JDK 11 does not have the JRE image"라고 쓴다. Eclipse Temurin처럼 JRE 빌드를 계속 내는 배포판도 있다. [OpenJDK JEP 220 · JEP 282 (Release 9), https://openjdk.org/jeps/220 ; Oracle, JDK 11 Migration Guide, https://docs.oracle.com/en/java/javase/11/migrate/index.html , 2026-09-27 확인]

⚠️ [[Java 면접 기타 빈출 질문 1 자바 기본]] Q3은 「JDK는 개발자용, JRE는 실행용」으로 끝나 이 변화가 빠졌다. 컨테이너 이미지에 JDK 전체 대신 `jlink`로 줄인 런타임을 넣는 것이 요즘 쓰임이다(위키의 보충).

## DE와의 관계

DE 스택의 상당수가 JVM 위에서 돈다: [[Apache Spark]](Scala), [[Apache Kafka]](Scala·Java), [[Apache Flink]](Java). 그래서 JVM 지식은 면접용이면서 운영 지식이기도 하다. 이 연결은 위키가 붙였다.

- GC pause: 긴 GC 멈춤이 Spark·Flink 잡으로 번지는 경로는 [[가비지 컬렉터]]의 「DE가 신경 쓰는 이유」에 있다.
- 힙 크기 설계: Kafka 브로커는 데이터를 OS 페이지 캐시에 맡기므로 힙을 작게 두는 것이 관례다. 힙을 키우면 GC만 비싸진다.
- 워밍업: 스트리밍 잡을 재시작한 직후 처리량이 낮은 것도 JIT가 아직 데워지지 않은 탓이 크다([[JIT 컴파일]]).

## 관련

- 개념: [[클래스 로딩]](초기화 락 포함) · [[JVM 메모리 구조]] · [[JIT 컴파일]] · [[가비지 컬렉션]] · [[가비지 컬렉터]] · [[동시성 문제]] · [[동시성 컬렉션]] · [[JDK 개선 제안]](JEP 읽는 법)
- 자료: [[Java 면접 2 JVM과 실행 원리]] · [[Java 면접 2 빈출 질문]] · [[Java 면접 3 GC]] · [[Java 면접 3 빈출 질문]] · [[Java 면접 4 동시성 이슈]] · [[Java 면접 4 빈출 질문]] · [[Java 면접 기타 빈출 질문 1 자바 기본]] · [[인프런 Java 면접 강의]]

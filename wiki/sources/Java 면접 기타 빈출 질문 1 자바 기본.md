---
type: source
title: Java 면접 기타 빈출 질문 1 자바 기본
aliases: [자바 기본 빈출 질문, 채널톡 자바 기본 빈출 질문]
tags: [면접, Java, equals, hashCode, JDK]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "raw/interviews/java/기타_채널톡_면접관이_뽑은_빈출_질문.pdf"
---

# Java 면접 기타 빈출 질문 1 자바 기본

[[인프런 Java 면접 강의]]의 부록 PDF 「[기타] 채널톡 면접관이 뽑은 빈출 질문」 가운데 첫 소절 「자바 기본」이다. 다른 부록들은 제목이 슬라이드 Section 제목과 같지만 이 PDF는 제목이 「기타」이고 대응하는 Section이 없다. 형식은 [[Java 면접 5 빈출 질문]] 등 앞의 부록과 같다(질문마다 빈도 별점 ⭐1~3과 짧은 답 하나, 등급 루브릭 없음). PDF는 스스로 네 소절로 나뉘어 있어 위키도 네 페이지로 나눴다(사용자 결정 2026-09-27). 나머지는 [[Java 면접 기타 빈출 질문 2 문자열 예외 제네릭]] · [[Java 면접 기타 빈출 질문 3 어노테이션과 리플렉션]] · [[Java 면접 기타 빈출 질문 4 JCF]]다.

자료에는 질문 번호가 없다. 위키가 PDF 전체에 걸쳐 Q1~Q44로 매겼고(자바 기본 Q1~13, 문자열·예외·제네릭 Q14~23, 어노테이션·리플렉션 Q24~27, JCF Q28~44), 네 페이지가 같은 번호를 쓴다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 「[기타] 채널톡 면접관이 뽑은 빈출 질문」의 「자바 기본」 소절. 인프런 Java 면접 대비 강의의 부록 PDF다. 인프런은 워터마크로 확인했다 |
| 원본 파일 | `raw/interviews/java/기타_채널톡_면접관이_뽑은_빈출_질문.pdf` p1–2 (전체 4p, A3) |
| 형식 | 웹 페이지를 인쇄한 PDF(생성기 HeadlessChrome). 앞의 부록과 같은 「답변」 토글 모양이다. 코드 블록은 없다 |
| 강사 | 자료에 표기 없음. 「채널톡 면접관」은 제목에 적힌 표현이다 |
| 작성 시기 | PDF 생성일 2026-03-07. 다른 부록과 같은 날이다 |
| URL | 없음 (유료 강의 자료) |

## 요약

| # | 질문 | 빈도 | 답의 요지 | 자세히 |
|---|---|---|---|---|
| Q1 | 사용해 본 Java 버전과 그 이유 | ⭐⭐ | 주로 Java 8. 람다·스트림·새 날짜/시간 API로 코드가 간결해졌다 (p1) | 이 페이지 「Java 버전」 · [[람다와 스트림]] |
| Q2 | Java 8 · 11 · 17 | ⭐⭐ | 8은 람다·스트림·날짜 API, 11은 `isBlank()`·`lines()`·HttpClient·람다 매개변수의 `var`, 17은 record와 sealed class | 이 페이지 「Java 버전」 |
| Q3 | JDK와 JRE | ⭐ | JDK는 개발 도구(컴파일러·라이브러리·실행 환경), JRE는 JVM + 클래스 라이브러리. JDK는 개발자용, JRE는 실행용 | [[JVM]] |
| Q4 | 동일성과 동등성 | ⭐⭐ | 메모리 주소가 같으면 동일, 내용이 같으면 동등 | [[equals와 hashCode]] |
| Q5 | `equals()`와 `==` | ⭐⭐ | `==`는 동일성, `equals`는 동등성. 재정의하지 않은 `equals`는 `==`와 같다 | [[equals와 hashCode]] |
| Q6 | HashCode, `equals()`와 `hashCode()`의 차이 | ⭐⭐⭐ | 해시 코드는 객체를 식별하는 정수. `equals`는 내용을, `hashCode`는 같은 객체인지를 확인한다 | [[equals와 hashCode]] |
| Q7 | 왜 `hashCode()`도 재정의하나 | ⭐⭐ | 해시 컬렉션은 해시 코드를 먼저 비교하고 내용을 비교한다. 재정의하지 않으면 `Object.hashCode()`가 고유 주소를 돌려줘 다른 객체로 본다 | [[equals와 hashCode]] · [[HashMap]] |
| Q8 | `toString()` | ⭐ | 기본은 클래스 이름과 해시 코드. 로깅하기 좋게 오버라이드한다 | [[equals와 hashCode]] |
| Q9 | main은 왜 static인가 | ⭐⭐⭐ | 진입점이라 객체 생성 없이 호출되어야 한다 | 이 페이지 「main과 static」 |
| Q10 | 상수와 리터럴 | ⭐ | 상수는 `final`로 선언한 변하지 않는 값, 리터럴은 소스 코드의 고정 값. `final int MAX = 10;` | 이 페이지 「주의·결함」 |
| Q11 | 기본형과 참조형 | ⭐⭐ | 기본형은 값을 저장하고 효율을 위해 스택에, 참조형은 객체를 힙에 두고 스택에 참조를 둔다 | [[JVM 메모리 구조]] |
| Q12 | Call by Value인가 Call by Reference인가 | ⭐⭐⭐ | Call by Value. 참조의 복사본이 전달된다. 메서드 안에서 참조를 바꿔도 원본은 그대로지만, 참조로 객체 상태는 바꿀 수 있다 (p1–2) | 이 페이지 「값 전달」 |
| Q13 | 직렬화 | ⭐ | 객체 상태를 바이트 스트림으로. `Serializable` 구현, `ObjectOutputStream`/`ObjectInputStream`, `transient` 필드는 제외. 보안에 주의 (p2) | 이 페이지 「직렬화」 |

## 핵심

- 별점 셋짜리는 Q6 · Q9 · Q12다. Q6은 틀렸고 Q9는 JDK 25에서 낡았다. Q12만 그대로 써도 된다.
- Q4~Q8은 한 흐름(동일성 → `==`·`equals` → `hashCode` → 재정의 이유 → `toString`)이다. 그런데 Q4는 동일성을 「주소」로 설명하고, Q6의 「같은 객체인지 확인」과 Q7의 「고유한 주소 값」은 `hashCode`를 주소처럼 설명한다. 같은 오해가 JCF 소절의 Set 중복 제거 답(Q38)에도 다시 나온다([[Java 면접 기타 빈출 질문 4 JCF]]). 정정은 [[equals와 hashCode]] 한 곳에 모았다.
- Q7이 재정의 이유를 해시 컬렉션의 비교 순서(해시 → 내용)로 설명하는 줄기 자체는 맞다. `HashMap.putVal`의 판정 조건이 그렇다([[HashMap]]).
- Q1 · Q2는 Java 8 · 11 · 17에서 멈춘다. 자료 작성 시점(2026-03)에도 이미 JDK 21 · 25가 LTS였다.

## Java 버전

자료의 Q2 서술은 기능별로 맞다. 도입 버전을 확인한 결과다(2026-09-27, JEP 페이지).

| 기능 | 자료 | 정식 도입 | 근거 |
|---|---|---|---|
| `String.isBlank()` · `lines()` | 11 | 11 | Javadoc `@since 11` |
| HttpClient (HTTP/1.1 · HTTP/2 · WebSocket) | 11 | 11 | JEP 321 |
| 람다 매개변수의 `var` | 11 | 11 | JEP 323 |
| record | 17 | 16 (14·15는 preview) | JEP 395 |
| sealed class | 17 | 17 | JEP 409 |

record를 「Kotlin data class와 유사」하다고 한 것은 비유다. `Record` Javadoc은 record를 "a shallowly immutable, transparent carrier"라고 부른다. 얕은 불변일 뿐이다([[불변 객체]]).

지금 기준으로 다시 적으면 이렇다(2026-09-27 확인). JDK 25가 2025-09-16에 나온 LTS이고, JDK 26(2026-03-17)을 거쳐 최신 릴리스는 JDK 27(2026-09-15 GA, LTS 아님)이다. 다음 LTS는 JDK 29(2027-09 예정)로 알려져 있는데, 이 일정은 2차 자료(InfoQ)로만 확인했다. [OpenJDK, https://openjdk.org/projects/jdk/ ; inside.java 「JDK 27 Is Now Available」, 2026-09-15]

Q1은 경험을 묻는 질문이라 판정하지 않았다. 다만 「Java 8을 썼다」에 멈추면 요즘 면접에서는 「왜 올리지 않았나」가 이어지기 쉽다. GC 쪽에서 본 8 → 11 · 17의 이유는 [[Java 8에서 11로 가는 GC 관점의 이유]]에 있다. 이 연결은 위키가 붙였다.

## main과 static

자료의 답(Q9)은 전통적인 `public static void main(String[])`에만 맞다. JDK 25에서 정식이 된 JEP 512(Compact Source Files and Instance Main Methods)부터는 인스턴스 main도 진입점이 된다. 런처는 `String[]` 매개변수가 있는 main을 먼저 고르고, 없으면 매개변수 없는 `main()`을 고른다. 고른 메서드가 static이면 바로 부르고, 인스턴스 메서드면 매개변수 없는 non-private 생성자로 객체를 만든 뒤 부른다. JEP 원문은 "The launcher invokes that constructor and then invokes the chosen main method of the resulting object"라고 쓴다. [OpenJDK JEP 512, Release 25, https://openjdk.org/jeps/512 , 2026-09-27 확인]

그래서 지금 답한다면 「JVM이 객체를 만들지 않고 부르려면 static이어야 했다. JDK 25부터는 런처가 기본 생성자로 객체를 만들어 인스턴스 main도 부를 수 있다」가 된다. static 일반의 단점은 [[객체지향 프로그래밍]]의 static 절에 있다.

## 값 전달

Q12는 맞다. JLS §8.4.1은 "the values of the actual argument expressions initialize newly created parameter variables"라고 정의한다. 참조 타입이면 참조 값이 복사된다. 그래서 메서드 안에서 매개변수에 다른 객체를 대입해도 호출한 쪽 변수는 그대로고, 매개변수로 객체의 필드를 바꾸면 호출한 쪽에서도 보인다. 자료의 「참조값을 변경해도 원본 객체에는 영향을 미치지 않는다」는 「매개변수에 다른 참조를 대입해도 호출한 쪽 변수는 바뀌지 않는다」로 읽어야 뜻이 분명하다. [JLS SE 25 §8.4.1, https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html , 2026-09-27 확인]

## 직렬화

Q13의 메커니즘 서술(`Serializable`, `ObjectOutputStream`/`ObjectInputStream`, `transient`)은 맞다. 빠진 것과 과장된 것이 있다.

- 기본 직렬화 필드는 "non-transient and non-static fields"다. `static` 필드도 저장되지 않는다. [Java Object Serialization Specification §1.5, JDK 25, https://docs.oracle.com/en/java/javase/25/docs/specs/serialization/serial-arch.html]
- 「안전하게 전송하고 저장하는 데 필수적」은 거꾸로다. 신뢰할 수 없는 데이터를 역직렬화하는 것은 원격 코드 실행 취약점의 잘 알려진 원천이다. JDK는 역직렬화 필터(JEP 290, JDK 9, 8u121로 백포트)와 문맥별 필터(JEP 415, JDK 17)를 더했다. 『Effective Java』 3판 Item 85의 제목은 「Prefer alternatives to Java serialization」이다(2차 자료).

## 주의·결함

외부 검증 결과다(2026-09-27). 대조한 1차 자료: JLS SE 25 §3.10 · §4.12.4 · §8.4.1 · §8.10.3 · §15.21.3, JVMS SE 25 §2.5.3 · §2.6.1, JDK 8 · 11 · 25 `Object` Javadoc, OpenJDK HotSpot `globals.hpp` · `synchronizer.cpp`, `Record` Javadoc, JEP 220 · 282 · 290 · 321 · 323 · 395 · 409 · 415 · 512, Oracle JDK 11 Migration Guide, Java Object Serialization Specification. 『Effective Java』와 InfoQ는 2차 자료로 표시했다.

| 질문 | 자료의 서술 | 판정 | 정정이 있는 곳 |
|---|---|---|---|
| Q1 | 주로 Java 8을 썼다 | 판정하지 않음(경험). 최신 LTS는 JDK 25 | 이 페이지 「Java 버전」 |
| Q2 | 11 · 17의 새 기능 | 맞음. record는 17이 아니라 16에 정식 도입 | 이 페이지 「Java 버전」 |
| Q3 | JRE는 실행용으로 따로 있다 | 낡음. Oracle은 JDK 11부터 JRE를 따로 내지 않고, `jlink`로 앱 전용 런타임을 만든다 | [[JVM]] |
| Q4 | 메모리 주소가 같으면 동일 | 단서 필요. JLS는 「같은 객체를 가리킨다」로 정의한다. GC가 객체를 옮기므로 주소는 비유다 | [[equals와 hashCode]] |
| Q5 | `equals` 「연산자」 | 단서 필요. `equals`는 메서드다. 기본 `equals`가 `==`와 같다는 것은 맞다 | [[equals와 hashCode]] |
| Q6 | `hashCode()`는 같은 객체인지 확인한다 | 틀림. 해시 테이블용 값이고, 다른 객체도 같은 값을 가질 수 있다 | [[equals와 hashCode]] |
| Q7 | `Object.hashCode()`는 고유한 주소 값 | 틀림. HotSpot 기본은 스레드별 xor-shift 난수이고 고유하지도 않다. 재정의 이유의 줄기는 맞다 | [[equals와 hashCode]] |
| Q8 | 기본 `toString()` = 클래스 이름 + 해시 코드 | 맞음. 정확히는 `getClass().getName() + '@' + Integer.toHexString(hashCode())` | [[equals와 hashCode]] |
| Q9 | main은 객체 없이 불려야 해서 static | 낡음. JDK 25(JEP 512)부터 인스턴스 main이 정식 | 이 페이지 「main과 static」 |
| Q10 | 상수 = `final`로 선언한 값 | 단서 필요. JLS의 상수 변수는 기본형이나 String이고 상수식으로 초기화된 `final` 변수다(§4.12.4). `final List` 변수는 상수가 아니다. 리터럴 정의(§3.10)는 맞다 | 이 페이지 |
| Q11 | 기본형은 스택에 저장 | 단서 필요. 스택에 있는 것은 지역 변수뿐이고, 기본형 필드와 배열 원소는 힙에 있다 | [[JVM 메모리 구조]] |
| Q12 | Call by Value | 맞음 | 이 페이지 「값 전달」 |
| Q13 | 직렬화는 필수적, `transient`는 제외 | 단서 필요. `static`도 제외, 역직렬화는 보안 취약점의 원천 | 이 페이지 「직렬화」 |

집계: 틀림 2 · 낡음 2 · 단서 필요 5 · 맞음 3 · 판정하지 않음 1.

## 관련

- [[equals와 hashCode]]: Q4~Q8의 정정
- [[JVM]] · [[JVM 메모리 구조]]: Q3 · Q11
- [[객체지향 프로그래밍]]: static의 단점
- [[람다와 스트림]]: Java 8의 대표 기능
- [[JDK 개선 제안]]: 위 표의 JEP 읽는 법
- 같은 PDF: [[Java 면접 기타 빈출 질문 2 문자열 예외 제네릭]] · [[Java 면접 기타 빈출 질문 3 어노테이션과 리플렉션]] · [[Java 면접 기타 빈출 질문 4 JCF]]
- 트래커: [[인프런 Java 면접 강의]]

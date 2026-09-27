---
type: source
title: Java 면접 기타 빈출 질문 2 문자열 예외 제네릭
aliases: [문자열 예외 제네릭 빈출 질문, 채널톡 예외 빈출 질문]
tags: [면접, Java, 문자열, 예외, 제네릭]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "raw/interviews/java/기타_채널톡_면접관이_뽑은_빈출_질문.pdf"
---

# Java 면접 기타 빈출 질문 2 문자열 예외 제네릭

[[인프런 Java 면접 강의]]의 「[기타]」 부록 PDF 가운데 「문자열, 예외, 제네릭」 소절이다. 이 부록은 대응하는 슬라이드 Section이 없고, 자료가 스스로 네 소절로 나눈다. 소절마다 source 페이지 하나로 나눴다(사용자 결정 2026-09-27). 자료에는 질문 번호가 없어서 위키가 PDF 전체에 Q1–Q44를 매겼고, 이 소절은 Q14–Q23이다. 앞의 부록들([[Java 면접 5 빈출 질문]] 등)과 형식이 같다. 질문마다 빈도 별점(⭐1~3)과 짧은 답 하나가 붙고 등급 루브릭은 없다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 「[기타] 채널톡 면접관이 뽑은 빈출 질문」의 소절 「문자열, 예외, 제네릭」. 인프런 Java 면접 대비 강의의 부록 PDF다. 인프런은 워터마크로 확인했다 |
| 원본 파일 | `raw/interviews/java/기타_채널톡_면접관이_뽑은_빈출_질문.pdf` p2 (전체 4p, A3) |
| 형식 | 웹 페이지를 인쇄한 PDF(생성기 HeadlessChrome). 코드 블록은 없다 |
| 강사 | 자료에 표기 없음. 「채널톡 면접관」은 제목에 적힌 표현이다 |
| 작성 시기 | PDF 생성일 2026-03-07. 다른 부록과 같은 날이다 |
| URL | 없음 (유료 강의 자료) |

같은 PDF의 다른 소절은 [[Java 면접 기타 빈출 질문 1 자바 기본]] (Q1–Q13), [[Java 면접 기타 빈출 질문 3 어노테이션과 리플렉션]] (Q24–Q27), [[Java 면접 기타 빈출 질문 4 JCF]] (Q28–Q44)다.

## 요약

| # | 질문 | 빈도 | 답의 요지 | 자세히 |
|---|---|---|---|---|
| Q14 | String 리터럴과 `new String("")`의 차이 | ⭐ | 리터럴은 String Constant Pool에 저장되어 재사용되고, `new String`은 매번 새 인스턴스를 만든다 | 이 페이지 「문자열」 |
| Q15 | String · StringBuilder · StringBuffer의 차이 | ⭐ | String은 불변, 나머지 둘은 가변. StringBuffer는 메서드가 synchronized라 스레드 안전하다 | 이 페이지 「문자열」 |
| Q16 | Exception과 Error의 차이 | ⭐⭐ | Exception은 개발자 로직의 실수라 처리해야 하고, Error는 수습 불가한 시스템 문제라 개발자가 예측해 방지해야 한다 | [[Java 예외 처리]] |
| Q17 | Exception 클래스의 예시 | ⭐ | Checked Exception과 Runtime(Unchecked) Exception으로 나뉜다. 예시는 들지 않는다 | [[Java 예외 처리]] |
| Q18 | Checked와 Unchecked Exception의 차이 | ⭐⭐ | Checked는 RuntimeException을 상속하지 않아 컴파일 단계에서 처리해야 하고, Unchecked는 상속한다. 복구 가능하면 Checked(이미지를 못 찾으면 기본 이미지) | [[Java 예외 처리]] |
| Q19 | throw와 throws의 차이 | ⭐ | throw는 메서드 안에서 예외를 발생시키고, throws는 선언부에서 던질 수 있음을 선언한다 | [[Java 예외 처리]] |
| Q20 | finally의 역할 | ⭐ | 항상 실행되며 주로 connection 같은 자원 해제에 쓴다 | [[Java 예외 처리]] |
| Q21 | Throwable과 Exception의 차이 | ⭐ | Throwable은 Error와 Exception의 슈퍼 클래스, Exception은 에러를 뺀 예외의 슈퍼 클래스 | [[Java 예외 처리]] |
| Q22 | 제네릭이란, 왜 쓰나 | ⭐⭐⭐ | 데이터 타입을 일반화해 재사용성을 높이고 「타입 안정성」을 보장한다 | 이 페이지 「제네릭」 |
| Q23 | 제네릭을 쓴 경험 | ⭐ | 타입만 다른 `Pair` 클래스의 중복 제거, raw `ArrayList` 대신 `ArrayList<String>`으로 `ClassCastException` 방지 | 이 페이지 「제네릭」 |

## 핵심

- 이 소절에서 별점 셋은 Q22(제네릭) 하나뿐이다. 예외 질문은 여섯 개(Q16–Q21)로 가장 많지만 모두 ⭐~⭐⭐다.
- 예외 질문 여섯 개는 한 흐름으로 읽힌다. 계층(Q21) → 두 갈래(Q16) → checked/unchecked(Q18) → 문법(Q19 · Q20) 순이다. 정리와 정정은 [[Java 예외 처리]] 한 곳에 모았다.
- Q18의 「복구할 수 있으면 checked, 아니면 unchecked」는 『Effective Java』 3판 Item 70 「Use checked exceptions for recoverable conditions and runtime exceptions for programming errors」와 같은 지침이다. 자료는 출처를 밝히지 않았고, 대조는 위키가 2차 자료로 했다.
- Q15의 StringBuffer 동기화는 [[동시성 컬렉션]]의 Vector · Hashtable과 같은 방식(메서드마다 락)이다. 이 연결은 위키가 했다. String이 왜 불변이어도 스레드 안전한지는 [[불변 객체]]에 있다.

## 문자열

Q14 · Q15는 맞다. 자료에 없는 보강만 적는다.

- 리터럴은 인턴된다. JLS §3.10.5는 같은 내용의 문자열 리터럴이 "always refers to the same instance of class String"이라 하고, 그 이유를 리터럴(과 상수식의 값)이 `String.intern`처럼 "interned"되기 때문이라고 쓴다. `new`로 시작하는 인스턴스 생성식은 언제나 새 객체를 할당한다(JLS §15.9.4, "space is allocated for the new class instance").
- `new String("java")`에서도 인자 `"java"`는 리터럴이라 풀에 들어간다. 새로 생기는 것은 풀 밖의 String 객체 하나다. `intern()`을 부르면 풀의 인스턴스를 돌려받는다.
- 풀의 위치: HotSpot은 JDK 7부터 인턴 문자열을 PermGen이 아니라 힙에 둔다(JDK-6962931, [[JVM 메모리 구조]]).

아래는 로컬 JDK 25.0.2에서 적힌 그대로 컴파일해 실행한 결과다.

```java
public class Str {
    public static void main(String[] args) {
        String a = "java";
        String b = "java";
        String c = new String("java");
        System.out.println(a == b);
        System.out.println(a == c);
        System.out.println(a.equals(c));
        System.out.println(a == c.intern());
    }
}
```

```
true
false
true
true
```

`==`와 `equals`의 차이는 [[equals와 hashCode]]에 있다.

StringBuilder와 StringBuffer는 같은 API를 가진다. StringBuffer javadoc은 "thread-safe … the methods are synchronized where necessary"라 쓰고, StringBuilder javadoc은 "no guarantee of synchronization"이라며 단일 스레드에서는 StringBuilder를 권한다. 락이 메서드 단위라서, 여러 호출을 묶은 복합 연산(확인 후 추가 등)은 StringBuffer여도 호출자가 따로 동기화해야 한다. 이 지적은 위키의 것이다([[동기화 기법]]).

## 제네릭

Q22의 「타입 안정성」은 type safety의 번역이라 「타입 안전성」이 맞는 말이다. 자료는 제네릭이 어떻게 동작하는지는 말하지 않는다. 꼬리 질문으로 자주 이어지는 것은 타입 소거다.

- 타입 소거(type erasure): 컴파일러가 타입 검사를 마친 뒤 매개변수화된 타입을 소거된 타입으로 바꾼다. JLS §4.6은 이것을 "a mapping from types (possibly including parameterized types and type variables) to types (that are never parameterized types or type variables)"로 정의한다. `List<String>`의 소거는 `List`다.
- 그래서 런타임에는 타입 인자가 없다. `List<String>`과 `List<Integer>`는 같은 `Class` 객체를 쓴다. 아래는 로컬 JDK 25.0.2에서 적힌 그대로 실행한 결과다.

```java
import java.util.ArrayList;
import java.util.List;

public class Erasure {
    public static void main(String[] args) {
        List<String> s = new ArrayList<>();
        List<Integer> i = new ArrayList<>();
        System.out.println(s.getClass() == i.getClass());
    }
}
```

```
true
```

- 타입 안전성의 실체는 컴파일 타임 검사다. Q23의 경험담(raw `ArrayList` 대신 `ArrayList<String>`)이 이것을 잘 보여 준다. 꺼낼 때마다 하던 형변환과 거기서 나던 `ClassCastException`을 컴파일 오류로 앞당긴다. 소거 때문에 `new T()`, `instanceof List<String>` 같은 것은 허용되지 않는다는 점까지 말하면 답이 깊어진다(위키의 보충).

## 주의·결함

외부 검증 결과다(2026-09-27). 대조한 1차 자료: JLS SE 25 §3.10.5 · §4.6 · §11.1.1 · §11.2 · §14.20.2 · §14.20.3 · §15.9.4, JDK 25 javadoc(`Error` · `Exception` · `Throwable` · `Runtime` · `AutoCloseable` · `StringBuffer` · `StringBuilder`). 『Effective Java』 3판은 2차 자료로 표시했다.

| 질문 | 자료의 서술 | 판정 | 정정이 있는 곳 |
|---|---|---|---|
| Q14 | 리터럴은 풀에서 재사용, `new String`은 매번 새 인스턴스 | 맞음. 풀은 JDK 7부터 힙 | 이 페이지 「문자열」 |
| Q15 | StringBuilder는 스레드 안전하지 않고 StringBuffer는 synchronized | 맞음 | 이 페이지 「문자열」 |
| Q16 | Exception은 개발자 로직의 실수, Error는 개발자가 예측해 방지 | 틀림. Error javadoc은 "a reasonable application should not try to catch"라 한다. checked 예외는 외부 조건에서도 난다 | [[Java 예외 처리]] |
| Q17 | 예시 질문에 분류만 답함 | 틀림. 질문에 답하지 않았다 | [[Java 예외 처리]] |
| Q18 | Checked = RuntimeException을 상속하지 않은 클래스 | 단서 필요. Exception 계열 안에서는 맞지만, JLS §11.1.1의 unchecked에는 Error도 들어간다 | [[Java 예외 처리]] |
| Q19 | throw는 발생, throws는 선언 | 맞음 | [[Java 예외 처리]] |
| Q20 | finally는 항상 실행, 자원 해제용 | 단서 필요. `System.exit` · `halt` · JVM 중단 때는 돌지 않는다. 자원 해제는 try-with-resources(Java 7)가 권장된다 | [[Java 예외 처리]] |
| Q21 | Throwable은 Error와 Exception의 슈퍼 클래스 | 맞음 | [[Java 예외 처리]] |
| Q22 | 재사용성과 「타입 안정성」 | 단서 필요. 용어는 타입 안전성. 타입 소거(JLS §4.6)가 빠졌다 | 이 페이지 「제네릭」 |
| Q23 | `Pair` 중복 제거, `ArrayList<String>`으로 `ClassCastException` 방지 | 맞음. 경험 답이다 | 이 페이지 「제네릭」 |

Q18의 판정은 1차 검증 보고(「틀림(불완전)」)와 다르다. `Exception` javadoc이 "The class Exception and any subclasses that are not also subclasses of RuntimeException are checked exceptions"라고 자료와 같은 범위로 정의하므로, 질문을 Exception 계열에 한정해 읽으면 틀린 것은 아니라고 위키가 판단했다.

문서 결함: Q16의 「종료되어할」은 「종료되어야 할」의 오타다.

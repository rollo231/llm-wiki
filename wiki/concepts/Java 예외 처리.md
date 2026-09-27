---
type: concept
title: Java 예외 처리
aliases: [예외 처리, Exception handling, Checked exception, Unchecked exception, 체크 예외, 언체크 예외, try-with-resources, Throwable]
tags: [Java, 예외, 면접]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "[[Java 면접 기타 빈출 질문 2 문자열 예외 제네릭]]"
---

# Java 예외 처리

Java에서 예외는 `Throwable`이나 그 하위 클래스의 인스턴스로 표현된다. 면접에서는 Exception과 Error의 차이, checked와 unchecked의 차이, throw와 throws, finally의 역할을 차례로 묻는다([[Java 면접 기타 빈출 질문 2 문자열 예외 제네릭]] Q16–Q21). 이 질문들은 결국 하나의 계층도와 컴파일러가 무엇을 검사하느냐로 답할 수 있다.

## 계층

JLS §11.1.1의 정의다.

```
Throwable
├─ Error                      unchecked
│   └─ OutOfMemoryError, StackOverflowError, ...
└─ Exception                  checked
    ├─ IOException, SQLException, ...        checked
    └─ RuntimeException       unchecked
        └─ NullPointerException, IllegalArgumentException, ...
```

- `Throwable`과 그 하위 클래스 전부를 JLS는 "exception classes"라 부른다. `Exception`과 `Error`는 `Throwable`의 직접 하위 클래스다.
- `Exception`은 "the superclass of all the exceptions from which ordinary programs may wish to recover"다.
- `RuntimeException`은 `Exception`의 직접 하위 클래스로, 식을 평가하는 중에 여러 이유로 날 수 있지만 "from which recovery may still be possible"한 예외의 상위 클래스다.
- `Error`에 대해서는 javadoc이 "serious problems that a reasonable application should not try to catch. Most such errors are abnormal conditions."라고 쓴다.

## checked와 unchecked

JLS §11.1.1은 이렇게 나눈다.

> "The unchecked exception classes are the run-time exception classes and the error classes. The checked exception classes are all exception classes other than the unchecked exception classes. That is, the checked exception classes are Throwable and all its subclasses other than RuntimeException and its subclasses and Error and its subclasses." — JLS SE 25 §11.1.1

그래서 `RuntimeException`을 상속하지 않는다고 checked인 것은 아니다. `Error` 계열은 `RuntimeException`과 무관하지만 unchecked다. `Exception` 계열 안에서만 보면 「`RuntimeException`의 하위가 아니면 checked」가 맞고, `Exception` javadoc도 그 범위에서 그렇게 쓴다("The class Exception and any subclasses that are not also subclasses of RuntimeException are checked exceptions").

차이는 컴파일러가 무엇을 검사하느냐다. JLS §11.2는 "a program contains handlers for checked exceptions which can result from execution of a method or constructor"를 요구한다. checked 예외가 날 수 있는 곳은 `catch`로 잡거나, 메서드 선언의 `throws`에 적어 호출자에게 넘겨야 한다. 둘 다 안 하면 컴파일 오류다. unchecked 예외는 이 검사를 받지 않는다. 잡아도 되고 안 잡아도 된다.

| | checked | unchecked |
|---|---|---|
| 범위 | `Throwable` 중 아래 둘을 뺀 전부 | `RuntimeException` · `Error`와 그 하위 |
| 컴파일러 | 잡거나 `throws`로 선언해야 한다(§11.2) | 검사하지 않는다 |
| 예 | `IOException` · `SQLException` · `InterruptedException` | `NullPointerException` · `IllegalArgumentException` · `ArrayIndexOutOfBoundsException` · `OutOfMemoryError` |
| 흔한 원인 | 파일·네트워크·DB처럼 프로그램 밖의 조건 | 프로그래밍 오류(null, 잘못된 인자), 또는 JVM 자원 고갈 |

언제 무엇을 쓰느냐는 명세가 아니라 설계 지침의 문제다. 『Effective Java』 3판 Item 70의 제목이 「Use checked exceptions for recoverable conditions and runtime exceptions for programming errors」이고(2차 자료), 자료 Q18의 「복구할 수 있으면 checked」도 같은 지침이다.

## throw와 throws

- `throw`는 문장이다. `throw new IllegalArgumentException("...")`처럼 예외 객체를 실제로 던진다.
- `throws`는 메서드·생성자 선언의 절이다. `void read() throws IOException`처럼 이 메서드가 호출자에게 넘길 수 있는 예외를 선언한다. checked 예외에서는 이 선언이 §11.2 검사를 통과하는 한 방법이다. `Error` javadoc은 `Error` 하위 클래스는 `throws`에 적을 필요가 없다고 명시한다.

## finally가 돌지 않을 때

JLS §14.20.2는 try 블록이 정상으로 끝나든 예외 등으로 갑자기(abruptly) 끝나든 finally 블록을 실행한다고 정의한다. 그래서 흔히 「항상 실행된다」고 말하지만 예외가 있다.

- `System.exit` · `Runtime.exit`: 호출이 돌아오지 않으므로 try 블록이 끝나지 않고, finally에 도달하지 않는다. 종료 순서(shutdown hook)는 돈다.
- `Runtime.halt`: javadoc은 "Termination of the Java Virtual Machine is unconditional and immediate"라 하고, shutdown hook도 돌지 않는다.
- JVM이 강제로 죽을 때(kill -9, 크래시, 컨테이너 OOMKilled). 무한 루프나 데드락으로 try 블록이 끝나지 않을 때도 마찬가지다.

finally 안에서 `return`하거나 예외를 던지면, try 블록에서 난 예외가 사라진다. §14.20.2의 규칙상 finally가 갑자기 끝나면 try 문 전체가 그 이유로 끝나기 때문이다. 이 함정은 위키가 규칙에서 끌어낸 것이다.

## try-with-resources

자원 해제에는 finally보다 try-with-resources(Java 7, JLS §14.20.3)가 권장된다. JLS는 이렇게 정의한다: 자원 변수를 try 블록 전에 초기화하고, try 블록이 끝나면 "closed automatically, in the reverse order from which they were initialized". 자원은 `AutoCloseable`을 구현해야 하고, `AutoCloseable` javadoc은 이 구조가 "ensures prompt release"한다고 쓴다.

finally로 직접 닫을 때 생기는 문제는 본문과 `close()`가 둘 다 예외를 던지는 경우다. 손으로 쓰면 `close()`의 예외가 본문 예외를 덮는다. try-with-resources는 본문 예외를 던지고, `close()`의 예외는 거기에 억제된(suppressed) 예외로 붙인다. `Throwable.getSuppressed()` javadoc: "Returns an array containing all of the exceptions that were suppressed, typically by the try-with-resources statement, in order to deliver this exception."

아래는 로컬 JDK 25.0.2에서 적힌 그대로 컴파일해 실행한 결과다.

```java
public class Twr {
    static class Res implements AutoCloseable {
        public void close() { throw new IllegalStateException("close 실패"); }
    }

    public static void main(String[] args) {
        try (Res r = new Res()) {
            throw new IllegalArgumentException("본문 실패");
        } catch (Exception e) {
            System.out.println(e.getMessage());
            System.out.println(e.getSuppressed()[0].getMessage());
        }
    }
}
```

```
본문 실패
close 실패
```

## 면접에서

1. 계층부터 그린다. `Throwable` 아래 `Error`와 `Exception`, `Exception` 아래 `RuntimeException`. Q21은 이것으로 끝난다.
2. Exception과 Error(Q16): Error는 애플리케이션이 잡으려 하지 않아야 할 심각한 문제(OOM, StackOverflow)이고, Exception은 프로그램이 복구를 시도할 수 있는 조건이다. 「Exception은 개발자의 실수」라고 하면 `IOException`처럼 외부 조건에서 나는 checked 예외를 설명하지 못한다.
3. checked와 unchecked(Q18): 기준은 컴파일러의 검사(§11.2)이고, unchecked는 `RuntimeException`과 `Error` 둘이라고 말한다. 예시(Q17)는 양쪽에서 두 개씩 든다.
4. finally(Q20): 항상 돈다고 한 뒤 `System.exit` · `halt`는 예외라고 덧붙이고, 자원 해제는 try-with-resources와 억제된 예외로 넘어간다.

## 자료의 서술과 정정

| 자료 | 판정 | 정정 |
|---|---|---|
| Exception은 개발자가 구현한 로직의 실수라 처리해야 한다 (Q16) | 틀림 | checked 예외는 외부 조건에서도 나고, 처리 의무는 checked에만 있다(§11.2) |
| Error는 개발자가 예측하여 방지해야 한다 (Q16) | 틀림 | javadoc: "a reasonable application should not try to catch". OOM · StackOverflow는 코드로 예측해 막는 대상이 아니다 |
| 예시 질문에 분류만 답함 (Q17) | 틀림 | 질문에 답하지 않았다. `IOException` · `SQLException` / `NullPointerException` · `IllegalArgumentException` |
| Checked = RuntimeException을 상속하지 않은 클래스 (Q18) | 단서 필요 | Exception 계열 안에서만 맞다. unchecked에는 Error도 들어간다(§11.1.1) |
| throw는 발생, throws는 선언 (Q19) | 맞음 | — |
| finally는 항상 실행, 자원 해제용 (Q20) | 단서 필요 | exit · halt · JVM 중단 때는 돌지 않는다. 자원 해제는 try-with-resources |
| Throwable은 Error와 Exception의 슈퍼 클래스 (Q21) | 맞음 | — |

근거 (2026-09-27 확인): JLS SE 25 §11.1.1 · §11.2 · §14.20.2 · §14.20.3, JDK 25 javadoc `Throwable` · `Exception` · `Error` · `Runtime` · `AutoCloseable`. Joshua Bloch, 『Effective Java』 3판 Item 70 (2차 자료).

## 관련

- [[JVM 메모리 구조]]: 영역별로 나는 `OutOfMemoryError` · `StackOverflowError`
- [[가비지 컬렉션]]: OOM 메시지별 대응
- [[동기화 기법]]: `synchronized`는 예외가 나도 모니터를 푼다(바이트코드의 두 번째 `monitorexit`)
- 자료: [[Java 면접 기타 빈출 질문 2 문자열 예외 제네릭]]

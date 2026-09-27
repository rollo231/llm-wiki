---
type: concept
title: equals와 hashCode
aliases: [동일성과 동등성, equals, hashCode, Object.equals, Object.hashCode, Identity and equality]
tags: [Java, 면접, 컬렉션]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "[[Java 면접 기타 빈출 질문 1 자바 기본]]"
  - "[[Java 면접 기타 빈출 질문 4 JCF]]"
---

# equals와 hashCode

Java에서 두 객체가 「같다」는 말은 두 가지다. 동일성(identity)은 두 참조가 같은 객체를 가리키는 것이고 `==`로 본다. 동등성(equality)은 두 객체가 논리적으로 같은 값을 나타내는 것이고 `equals`로 본다. `hashCode`는 동등성을 해시 테이블에서 빠르게 쓰기 위한 보조 값이다. 면접에서는 셋의 차이와 「왜 둘을 함께 재정의하나」를 묻는다([[Java 면접 기타 빈출 질문 1 자바 기본]] Q4~Q8).

## 동일성: `==`

JLS §15.21.3은 참조의 `==`를 이렇게 정의한다: 결과가 true인 것은 두 피연산자가 모두 null이거나 "both refer to the same object or array"일 때다. 명세는 메모리 주소를 말하지 않는다. HotSpot의 GC는 객체를 옮기므로(복사·컴팩션, [[가비지 컬렉션]]) 「주소가 같다」는 설명은 비유로만 쓸 수 있다. [JLS SE 25 §15.21.3, https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html , 2026-09-27 확인]

## 동등성: `equals`

`equals`는 연산자가 아니라 `Object`의 메서드다. 재정의하지 않으면 `==`와 같다. `Object` Javadoc: true를 돌려주는 것은 "if and only if x and y refer to the same object (x == y has the value true)"다. 그래서 값을 나타내는 클래스는 `equals(Object)`를 재정의해야 동등성 비교가 된다.

재정의한 `equals`는 동치 관계여야 한다(반사·대칭·추이·일관성, null과 비교하면 false). 이 규칙은 `Object.equals` Javadoc에 있다.

재정의할 때 가장 흔한 실수는 매개변수를 자기 타입으로 쓰는 것이다. `equals(Point)`는 `equals(Object)`를 오버라이드하지 않고 오버로딩을 하나 더할 뿐이라, `HashSet`이 부르는 `equals(Object)`는 여전히 `==`다. 코드와 실행 결과는 [[오버로딩과 오버라이딩]]의 「`equals`를 오버로딩해 버리는 실수」에 있다. `@Override`를 붙이면 컴파일러가 잡는다.

## hashCode의 계약

`Object.hashCode` Javadoc의 일반 계약은 세 줄이다.

1. 한 번의 실행 안에서 `equals` 비교에 쓰는 정보가 바뀌지 않으면 같은 객체의 `hashCode`는 매번 같은 정수다. 실행이 바뀌면 달라도 된다.
2. `equals`로 같은 두 객체는 같은 `hashCode`를 가져야 한다.
3. `equals`로 다른 두 객체가 다른 `hashCode`를 가질 필요는 없다. 다르면 해시 테이블 성능이 좋아질 뿐이다: "It is not required that if two objects are unequal according to the equals method, then calling the hashCode method on each of the two objects must produce distinct integer results."

그래서 `hashCode`는 식별자가 아니다. 같은 해시 코드는 「같은 객체일 수도 있다」는 후보 표시일 뿐이고, 판정은 `equals`가 한다. 방향은 한쪽이다: 동등하면 해시가 같아야 하지만, 해시가 같다고 동등하지는 않다(해시 충돌).

## 왜 둘을 함께 재정의하나

해시 컬렉션은 해시로 버킷을 찾고, 그 버킷 안에서만 `equals`로 비교한다. `HashSet.add`는 내부의 `HashMap.put`을 부르고, `HashMap.putVal`의 판정 조건은 `p.hash == hash && ((k = p.key) == key || (key != null && key.equals(k)))`다([[HashMap]]). `equals`만 재정의하고 `hashCode`를 그대로 두면 계약 2가 깨진다. 동등한 두 객체가 대개 다른 해시를 가져 다른 버킷으로 가고, `equals`는 불리지도 않는다.

```java
import java.util.*;

public class Main {
    static class Money {
        final int amount;
        Money(int amount) { this.amount = amount; }
        @Override public boolean equals(Object o) {
            return o instanceof Money m && m.amount == amount;
        }
        // hashCode()를 재정의하지 않았다
    }

    record Won(int amount) {}

    public static void main(String[] args) {
        Money a = new Money(1000), b = new Money(1000);
        System.out.println(a == b);           // false
        System.out.println(a.equals(b));      // true
        Set<Money> set = new HashSet<>(List.of(a));
        System.out.println(set.contains(b));  // 대개 false

        Set<Won> wons = new HashSet<>(List.of(new Won(1000)));
        System.out.println(wons.contains(new Won(1000)));  // true
        System.out.println(new Won(1000));                 // Won[amount=1000]
    }
}
```

OpenJDK 25.0.2에서 세 번 실행한 출력은 모두 `false true false true Won[amount=1000]`이었다. 주석의 「대개」는 두 객체의 기본 해시 코드가 우연히 같은 버킷에 떨어지면 `equals`가 불려 true가 나올 수 있다는 뜻이다. 우연에 기대는 동작이라 버그다.

record는 이 문제가 없다. JLS §8.10.3은 record가 `equals`를 명시하지 않으면 "public final boolean equals(Object) that returns true if and only if the argument is an instance of R, and the current instance is equal to the argument instance at every record component"를 암묵적으로 선언하고, `hashCode`와 `toString`도 컴포넌트로 만든다고 정한다. 위 예의 `Won`이 그 경우다. [JLS SE 25 §8.10.3, https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html , 2026-09-27 확인]

재정의한 객체를 해시 컬렉션에 넣은 뒤 `equals`에 쓰는 필드를 바꾸면 계약 1이 깨져 그 객체를 다시 못 찾는다. 맵 키로 [[불변 객체]]가 좋은 이유다.

## 기본 hashCode는 주소가 아니다

재정의하지 않은 `Object.hashCode()`를 「객체의 주소」로 설명하는 경우가 많다. JDK 8 Javadoc에 그런 문장이 있었기 때문이다. 문구는 이렇게 바뀌었다.

| 버전 | Javadoc 문구 |
|---|---|
| JDK 8 | "This is typically implemented by converting the internal address of the object into an integer, but this implementation technique is not required" |
| JDK 9–11 | "The hashCode may or may not be implemented as some function of an object's memory address at some point in time." |
| JDK 12 이후 | 괄호 문장이 사라지고 "As far as is reasonably practical, the hashCode method defined by class Object returns distinct integers for distinct objects."만 남았다 |

JDK 12 경계는 OpenJDK `jdk11u`와 `jdk12u` 저장소의 `Object.java`에서 "memory address" 문구가 있는지로 확인했다.

HotSpot 구현은 더 분명하다. 알고리즘은 실험용 플래그 `hashCode`로 고르는데, 기본값이 JDK 8부터 5다(JDK 7은 0). `ObjectSynchronizer::get_next_hash`에서 5는 "Marsaglia's xor-shift scheme with thread-specific state", 곧 스레드별 상태를 쓰는 난수다. 0도 전역 Park-Miller 난수다. 주소를 쓰는 것은 모드 1과 4뿐이다. 만든 값은 객체 헤더(mark word)의 해시 비트 수로 잘리므로(`markWord::hash_mask`) 서로 다른 객체가 같은 값을 가질 수 있다. 한 번 만든 값은 객체에 기록되어 GC가 객체를 옮겨도 바뀌지 않는다(계약 1). [OpenJDK `src/hotspot/share/runtime/globals.hpp` · `synchronizer.cpp`, master ; jdk8u · jdk7u `globals.hpp`, https://github.com/openjdk , 2026-09-27 확인]

재정의 여부와 상관없이 이 기본 값을 얻으려면 `System.identityHashCode(Object)`를 쓴다.

## toString

기본 `toString()`은 `getClass().getName() + '@' + Integer.toHexString(hashCode())`다(`Object` Javadoc). `hashCode()`를 부르므로 `hashCode`를 재정의하면 기본 `toString`의 `@` 뒤도 바뀐다. `@` 뒤의 16진수는 주소가 아니라 해시 코드다. 로깅용으로 필드를 보여 주게 오버라이드하는 것이 보통이고, record는 이것도 자동으로 만든다.

## 면접에서

1. 동일성은 `==`로 같은 객체를 가리키는지, 동등성은 `equals`로 같은 값을 나타내는지 본다. 「주소」 대신 「같은 객체」라고 말한다.
2. `hashCode`는 식별자가 아니라 해시 테이블용 값이다. 계약은 「equals가 같으면 hashCode도 같아야 한다, 반대는 아니다」.
3. 함께 재정의하는 이유: 해시 컬렉션이 해시로 버킷을 먼저 고르므로, `hashCode`를 안 맞추면 동등한 객체를 다른 버킷에서 찾는다.
4. 꼬리 질문에 대비한다. 「기본 hashCode는 주소인가요?」에는 HotSpot 기본은 스레드별 난수이고 고유하지 않다고, 「equals를 잘못 재정의하는 흔한 실수는?」에는 `equals(Point)` 오버로딩과 `@Override`를 답한다. 요즘 코드라면 값 클래스는 record로 쓰면 둘 다 자동으로 생긴다고 덧붙인다.

## 자료의 서술과 정정

| 자료 | 판정 | 정정 |
|---|---|---|
| 메모리 주소가 같으면 동일 (Q4) | 단서 필요 | JLS는 「같은 객체를 가리킨다」로 정의. GC가 객체를 옮기므로 주소는 비유 |
| `equals` 「연산자」, 기본 `equals`는 `==`와 같다 (Q5) | 단서 필요 | `equals`는 메서드. 뒷부분은 맞다 |
| 해시 코드는 객체를 식별하는 정수, `hashCode()`는 같은 객체인지 확인 (Q6) | 틀림 | 해시 테이블용 값. 다른 객체도 같은 값을 가질 수 있어 식별도 확인도 못 한다 |
| `Object.hashCode()`는 객체의 고유한 주소 값 (Q7) | 틀림 | HotSpot 기본(JDK 8+)은 스레드별 xor-shift 난수, 해시 비트로 잘려 고유하지 않음. 주소 문구는 JDK 12 Javadoc부터 없다 |
| 해시 컬렉션은 해시를 먼저, 내용을 나중에 비교 (Q7) | 맞음 | `HashMap.putVal`의 조건과 같다. 다만 비교 대상은 같은 버킷의 노드뿐이다 |
| 기본 `toString()` = 클래스 이름 + 해시 코드 (Q8) | 맞음 | `getClass().getName() + '@' + Integer.toHexString(hashCode())` |
| `hashCode()`는 객체의 주소로 같은 객체인지 확인, `equals`가 true면 동일한 객체 (JCF Q38) | 틀림 | 위와 같은 오해. `equals`가 true면 「동등한」 객체다([[Java 면접 기타 빈출 질문 4 JCF]]) |

근거 (2026-09-27 확인): JLS SE 25 §8.10.3 · §15.21.3, JDK 8 · 11 · 25 `java.lang.Object` Javadoc, OpenJDK `jdk11u` · `jdk12u` `Object.java`, HotSpot `globals.hpp` · `synchronizer.cpp`(master, jdk8u, jdk7u), OpenJDK master `HashMap.java` · `HashSet.java`. 실행 결과는 로컬 OpenJDK 25.0.2.

## 관련

- [[HashMap]]: 해시 → 버킷 인덱스, 체이닝과 트리화
- [[Java 컬렉션 프레임워크]]: `HashSet` · `HashMap`을 비롯한 해시 컬렉션
- [[오버로딩과 오버라이딩]]: `equals(Point)` 실수와 `@Override`
- [[불변 객체]]: 맵 키로 안전한 이유, record
- 자료: [[Java 면접 기타 빈출 질문 1 자바 기본]] · [[Java 면접 기타 빈출 질문 4 JCF]] · [[인프런 Java 면접 강의]]

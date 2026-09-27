---
type: concept
title: SOLID 원칙
aliases: [SOLID, SRP, OCP, LSP, ISP, DIP, 단일 책임 원칙, 개방-폐쇄 원칙, 리스코프 치환 원칙, 인터페이스 분리 원칙, 의존관계 역전 원칙, 관심사 분리]
tags: [Java, 객체지향, 설계, 면접]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "[[Java 면접 5 빈출 질문]]"
---

# SOLID 원칙

객체지향 설계 원칙 다섯 가지의 머리글자를 모은 이름이다. 단일 책임(SRP), 개방-폐쇄(OCP), 리스코프 치환(LSP), 인터페이스 분리(ISP), 의존관계 역전(DIP)이다. 다섯 원칙은 모두 변경이 생겼을 때 고칠 곳을 줄이려는 장치이고, [[결합도와 응집도]]를 원칙 단위로 풀어 쓴 것에 가깝다. 이 요약은 위키의 것이다.

자료([[Java 면접 5 빈출 질문]] Q12, p2)는 다섯 원칙을 한 답에 설명하고, 관심사 분리를 묻는 꼬리 질문 셋(Q17–Q19, p3)에서 SRP를 다시 다룬다. 자료는 어느 정의에도 출처를 적지 않는다. 아래 원문과 판정은 외부 검증(2026-09-27)으로 위키가 붙였다.

## 한눈에

| 약어 | 이름 | 원문 | 자료의 서술 | 판정 |
|---|---|---|---|---|
| SRP | 단일 책임 원칙 | "A module should be responsible to one, and only one, actor." (Martin 2017) | 하나의 모듈은 오직 하나의 액터에 대해서만 책임져야 한다 | 단서 필요 (출처 없음) |
| OCP | 개방-폐쇄 원칙 | "open for extension but closed for modification" (Meyer 1988, Martin 2000) | 확장할 수 있으면서 사용하는 코드는 수정하지 않는다, 변하는 부분을 추상화 | 맞음 |
| LSP | 리스코프 치환 원칙 | "the behavior of P is unchanged when o1 is substituted for o2" (Liskov 1987) | 정확성을 깨뜨리지 않으면서 하위 타입 인스턴스로 바꿀 수 있어야 | 맞음 (요지로서) |
| ISP | 인터페이스 분리 원칙 | "Clients should not be forced to depend upon interfaces that they do not use." (Martin 1996) | 사용하지 않는 메소드에 의존 관계를 맺으면 안 된다 | 맞음 |
| DIP | 의존관계 역전 원칙 | A. 상위 모듈은 하위 모듈에 의존하지 않고 둘 다 추상에 의존한다 B. 추상은 세부에 의존하지 않는다 (Martin 1996) | 추상은 구체에 의존하지 않는다, 인터페이스에 의존하라 | 단서 필요 (A항 누락) |

## SRP: 단일 책임 원칙

자료(Q12)는 "한 클래스는 하나의 책임만"이라는 흔한 정의를 들고, "책임이라는 기준은 사람마다 정하기 나름"이라며 액터 정의로 넘어간다. 액터는 "시스템이 동일한 방식으로 변하길 바라는 사용자의 집단"이다. 메서드가 여럿이어도 그 객체를 쓰는 액터가 하나면 SRP를 지킨 것이라는 설명도 붙인다.

이 정의는 Robert C. Martin의 『Clean Architecture』(2017) 7장 p.65 문장의 번역이다: "A module should be responsible to one, and only one, actor." 자료는 이 출처를 밝히지 않는다. 더 오래된 표현은 『Agile Software Development, Principles, Patterns, and Practices』 8장 p.95의 "A class should have only one reason to change"이고, 이 책의 판권 연도는 보통 2003으로 인용된다. 두 책은 2차 자료로 확인했다. Martin은 2014-05-08 블로그 글에서 "Each software module should have one and only one reason to change"라고 다시 쓰고 "This principle is about people."이라고 덧붙인다(원문 확인). 「변경의 이유」가 곧 「그 변경을 요구하는 사람」이라는 연결이 액터 정의의 뿌리다.

### 관심사 = 액터 (Q17–Q19)

자료는 "하나의 클래스에는 하나의 관심사"라는 말을 액터로 풀고, 사례 셋을 든다.

- Q17 `OrderProcessor`: 판매팀·고객 서비스·물류 담당이 모두 "주문 처리 흐름 최적화"라는 같은 이유로 고친다면 관심사는 하나다. 사람 수가 아니라 변경의 이유가 기준이다.
- Q18 `UserAuthenticator`: 보안팀(암호화 알고리즘), 사용자 경험팀(인증 절차 간소화), 데이터 관리팀(저장 방식)이 각자 다른 이유로 고친다면 관심사가 셋이다. 자료가 드는 문제는 한 액터의 요구가 다른 액터에게 번지는 부작용, 복잡해지는 테스트, 세 갈래의 변경 지점이다.
- Q19 `OrderService`: 주문 생성과 결제 세부 로직이 한 클래스에 있고, PG사마다 `if~else`로 분기했다. 결제 인터페이스를 분리하고 `OrderService`는 그 인터페이스에만 의존하게 바꿨다. 대안으로 `OrderService`·`PaymentService`를 묶는 `OrderFacade`를 든다.

Q19의 해법은 SRP만의 일이 아니다. PG사 분기를 인터페이스 뒤로 옮긴 것은 전략 패턴이고, 새 PG사를 붙일 때 `OrderService`를 고치지 않게 되는 것은 OCP, `OrderService`가 구현 대신 추상에 의존하게 된 것은 DIP다. 면접에서는 세 원칙을 함께 짚어야 사례가 원칙과 맞물린다. 이 관찰은 위키의 것이다. Facade는 관심사를 나눈 뒤 흐름을 한 곳에서 조율하는 방법이라 분기 문제는 그대로 남는다는 점도 위키가 덧붙인다.

## OCP: 개방-폐쇄 원칙

자료의 설명(기존 코드는 그대로 두고 확장, 변하는 부분을 추상화)은 맞다. 원칙의 기원은 Bertrand Meyer의 『Object-Oriented Software Construction』(1988)이다. Meyer의 해법은 상속이었다: 클래스는 컴파일되어 라이브러리에 들어가 닫혀 있고, 새 클래스가 그것을 부모로 삼을 수 있어 열려 있다(2차 자료). Martin은 이를 추상과 다형성 쪽으로 옮겼다. 2000년 논문 「Design Principles and Design Patterns」: "A module should be open for extension but closed for modification. … It originated from the work of Bertrand Meyer." "abstraction is the key to the OCP."(원문 확인)

다형성으로 OCP를 얻는 구조는 [[다형성]]에 있다. 자료의 슬라이드 쪽도 OCP 언급을 Silver와 Gold를 가르는 기준으로 쓴다.

## LSP: 리스코프 치환 원칙

자료는 "상위 타입의 객체는 프로그램의 정확성을 깨뜨리지 않으면서 하위 타입의 인스턴스로 바꿀 수 있어야"라고 쓴다. 요지는 맞다. Barbara Liskov의 OOPSLA '87 기조연설 「Data Abstraction and Hierarchy」(SIGPLAN Notices 23(5), 1988)의 문장은 이렇다: "If for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2, then S is a subtype of T."(원문 확인) 원문의 기준은 "정확성"이 아니라 "behavior unchanged"이고, 자료의 "정확성"은 흔한 풀이다.

Liskov & Wing, 「A Behavioral Notion of Subtyping」(ACM TOPLAS 16(6), 1994)은 이를 증명 가능한 성질로 다시 쓴다: "Let φ(x) be a property provable about objects x of type T. Then φ(y) should be true for objects y of type S where S is a subtype of T." 원문 PDF에서 위치는 확인했으나 텍스트가 깨져 온전한 문장은 2차 자료로 확인했다.

LSP는 is-a가 언제 성립하는지의 기준이다([[상속과 조합]]). 오버라이딩에서 반환 타입을 공변으로만 바꾸고 접근을 좁히거나 checked 예외를 넓히지 못하게 하는 규칙은 LSP 가운데 컴파일러가 강제할 수 있는 부분이다([[오버로딩과 오버라이딩]]). 이 해석은 위키의 것이다. 행동의 약속(사전·사후 조건, 불변식)은 컴파일러가 보지 못하므로 설계자가 지켜야 한다.

## ISP: 인터페이스 분리 원칙

자료의 설명은 맞다. Martin의 1996년 C++ Report 칼럼 「The Interface Segregation Principle」: "CLIENTS SHOULD NOT BE FORCED TO DEPEND UPON INTERFACES THAT THEY DO NOT USE."(원문 확인) 2000년 논문은 "Many client specific interfaces are better than one general purpose interface"라고 쓴다(원문 확인). 자료는 "사용하지 않는 메소드"라고 옮겼고 원문은 "interfaces"다. 뜻은 같다.

Java에서는 인터페이스를 여러 개 구현할 수 있으므로, 큰 인터페이스 하나보다 역할별 작은 인터페이스 여럿으로 나누기 쉽다([[인터페이스와 추상 클래스]]).

## DIP: 의존관계 역전 원칙

Martin의 1996년 5월 C++ Report 칼럼 「The Dependency Inversion Principle」의 원문은 두 항이다(원문 확인).

- A. "HIGH LEVEL MODULES SHOULD NOT DEPEND UPON LOW LEVEL MODULES. BOTH SHOULD DEPEND UPON ABSTRACTIONS."
- B. "ABSTRACTIONS SHOULD NOT DEPEND UPON DETAILS. DETAILS SHOULD DEPEND UPON ABSTRACTIONS."

자료는 B항과 2000년 논문의 "Depend upon Abstractions. Do not depend upon concretions."만 옮겼다. 원칙 이름의 근거인 A항이 빠졌다. 같은 1996년 글에 따르면 전통적인 절차적 설계에서는 "high level modules depend upon low level modules"이고, 이 방향을 뒤집는 것이 "inversion"이다. 자료의 "변화하기 쉬운 것에 의존해서는 안 된다"는 2000년 논문의 안정성(non-volatility) 논의와 통한다.

```java
// 역전 전: 상위 정책이 하위 세부에 직접 의존한다
class OrderService { private final CardPgClient pg = new CardPgClient(); }

// 역전 후: 추상은 상위 쪽이 소유하고, 세부가 그것을 구현한다
interface PaymentGateway { void pay(Order order); }      // OrderService 쪽 패키지
class OrderService { private final PaymentGateway pg; OrderService(PaymentGateway pg) { this.pg = pg; } }
class CardPgClient implements PaymentGateway { ... }       // 하위 모듈이 상위의 추상을 향한다
```

화살표의 방향이 바뀐다. 전에는 `OrderService → CardPgClient`였고, 후에는 `CardPgClient → PaymentGateway ← OrderService`다. 인터페이스를 만드는 것만으로는 부족하고, 그 인터페이스를 누가 소유하느냐(상위 정책 쪽)가 역전의 요점이다. 이 설명과 예시는 위키가 붙였다. Q19의 결제 인터페이스 분리가 바로 이 모양이다.

## 이름의 역사

- Martin의 2000년 논문 「Design Principles and Design Patterns」에는 클래스 설계 원칙으로 OCP·LSP·DIP·ISP만 있고(나머지는 REP·CCP 같은 패키지 원칙이다) SRP도 "SOLID"라는 단어도 없다(원문 확인).
- SRP는 이 논문에 없고, 위 SRP 절의 『Agile Software Development, Principles, Patterns, and Practices』(보통 2003년으로 인용)에 나온다(2차 자료).
- 머리글자 "SOLID"는 Michael Feathers가 2004년 무렵 만들었다고 알려져 있다. 1차 증거는 확인하지 못했고 2차 자료(Wikipedia SOLID 문서)로만 확인했다.

## 면접에서

- 원칙마다 정의 한 문장과 "무엇을 막으려는가"를 붙인다. SRP는 한 액터의 변경이 다른 액터에게 번지는 것, OCP는 새 기능마다 기존 코드를 고치는 것, LSP는 하위 타입이 상위 타입의 약속을 깨는 것, ISP는 쓰지 않는 기능의 변경에 끌려가는 것, DIP는 상위 정책이 하위 세부에 묶이는 것이다. 이 정리는 위키의 것이다.
- SRP는 "메서드 하나당 책임 하나"가 아니라 액터로 설명하고, 출처(『Clean Architecture』 7장)를 말할 수 있으면 좋다.
- DIP는 "인터페이스에 의존하라"에서 멈추지 말고 A항과 역전의 방향(추상을 상위 쪽이 소유)을 말한다.
- 사례 질문(Q19)에는 SRP·OCP·DIP가 한꺼번에 들어 있다는 것을 짚는다.

## 근거

- Robert C. Martin, 「The Dependency Inversion Principle」, C++ Report, 1996-05. https://www.cs.utexas.edu/~downing/papers/DIP-1996.pdf (원문 확인)
- Robert C. Martin, 「The Interface Segregation Principle」, C++ Report, 1996. https://d3s.mff.cuni.cz/f/teaching/nprg043/extras/martin96-interface_segregation_principle.pdf (원문 확인)
- Robert C. Martin, 「Design Principles and Design Patterns」, Object Mentor, 2000 (objectmentor.com 배포본, 원문 확인)
- Robert C. Martin, 「The Single Responsibility Principle」, 2014-05-08, https://blog.cleancoder.com (원문 확인)
- Robert C. Martin, 『Clean Architecture』, 2017, 7장 p.65 · 『Agile Software Development, Principles, Patterns, and Practices』, 8장 p.95 (2차 자료)
- Barbara Liskov, 「Data Abstraction and Hierarchy」, OOPSLA '87 keynote, SIGPLAN Notices 23(5), 1988. https://www.cs.tufts.edu/~nr/cs257/archive/barbara-liskov/data-abstraction-and-hierarchy.pdf (원문 확인)
- Barbara Liskov & Jeannette Wing, 「A Behavioral Notion of Subtyping」, ACM TOPLAS 16(6), 1994. https://www.cs.columbia.edu/~wing/publications/LiskovWing94.pdf (위치 확인, 문장은 2차)
- Bertrand Meyer, 『Object-Oriented Software Construction』, 1988 (2차 자료) · Wikipedia 「SOLID」 「Open–closed principle」 (2차 자료)
- 모두 2026-09-27 확인.

## 관련

- [[결합도와 응집도]] · [[객체지향 프로그래밍]] · [[캡슐화]]
- [[다형성]]: OCP를 다형성으로 얻는 구조
- [[상속과 조합]] · [[상속을 쓰는 이유]] · [[오버로딩과 오버라이딩]]: LSP와 오버라이딩 규칙
- [[인터페이스와 추상 클래스]]: ISP와 여러 인터페이스 구현
- 자료: [[Java 면접 5 빈출 질문]] · [[인프런 Java 면접 강의]]

---
type: source
title: Java 면접 기타 빈출 질문 3 어노테이션과 리플렉션
aliases: [어노테이션 빈출 질문, 리플렉션 빈출 질문]
tags: [면접, Java, 어노테이션, 리플렉션]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "raw/interviews/java/기타_채널톡_면접관이_뽑은_빈출_질문.pdf"
---

# Java 면접 기타 빈출 질문 3 어노테이션과 리플렉션

[[인프런 Java 면접 강의]]의 「[기타]」 부록 PDF 가운데 「어노테이션, 리플렉션」 소절이다. 위키가 매긴 PDF 전체 번호로 Q24–Q27이다(자료에는 번호가 없다). 네 질문이 「어노테이션이란 → 왜 쓰나 → 리플렉션이란 → 구현해 봤나」로 이어지는 꼬리 질문 사슬이고, 앞의 셋이 모두 ⭐⭐⭐다. 네 소절 가운데 가장 짧지만 별점 밀도는 가장 높다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 「[기타] 채널톡 면접관이 뽑은 빈출 질문」의 소절 「어노테이션, 리플렉션」. 인프런 Java 면접 대비 강의의 부록 PDF다. 인프런은 워터마크로 확인했다 |
| 원본 파일 | `raw/interviews/java/기타_채널톡_면접관이_뽑은_빈출_질문.pdf` p2–3 (전체 4p, A3). Q25는 질문이 p2 끝, 답이 p3 첫머리에 있다 |
| 형식 | 웹 페이지를 인쇄한 PDF(생성기 HeadlessChrome). 코드 블록은 없다 |
| 강사 | 자료에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-03-07 |
| URL | 없음 (유료 강의 자료) |

같은 PDF의 다른 소절은 [[Java 면접 기타 빈출 질문 1 자바 기본]] · [[Java 면접 기타 빈출 질문 2 문자열 예외 제네릭]] · [[Java 면접 기타 빈출 질문 4 JCF]]다.

## 요약

| # | 질문 | 빈도 | 답의 요지 |
|---|---|---|---|
| Q24 | 어노테이션이란 | ⭐⭐⭐ | 인터페이스를 기반으로 한 문법. 주석처럼 코드에 달아 클래스에 특별한 의미를 주거나 기능을 주입한다 |
| Q25 | 어노테이션을 왜 쓰나 | ⭐⭐⭐ | 리플렉션으로 런타임에 어노테이션을 조회하고, 그 메타데이터로 특별한 로직을 짤 수 있다 |
| Q26 | 리플렉션이란 | ⭐⭐⭐ | 힙에 로드된 클래스 타입의 객체로 인스턴스를 만들고, 필드와 메서드를 접근 제어자와 상관없이 쓰게 해 주는 자바 API |
| Q27 | 리플렉션으로 어노테이션 메타데이터를 읽는 로직을 구현해 봤나 | ⭐⭐ | Bot의 Name을 검증하려고 커스텀 어노테이션을 만들고, 붙은 필드를 리플렉션으로 가져와 길이 등을 검사했다 |

이 소절의 주제는 자기 개념 페이지가 없어서 정정을 이 페이지에 모두 적는다.

## 어노테이션은 스스로 아무것도 하지 않는다

Q24의 앞 절반은 맞다. JLS §9.6은 어노테이션 인터페이스 선언을 "an annotation interface, a specialized kind of interface"라 하고, `interface` 앞에 `@`를 붙여 일반 인터페이스와 구별한다고 쓴다. `Class` javadoc도 "an annotation interface is a kind of interface"라 한다.

틀린 것은 「기능을 주입한다」다. JLS §9.7은 어노테이션을 이렇게 정의한다.

> "An annotation is a marker which associates information with a program element, but has no effect at run time." — JLS SE 25 §9.7

어노테이션은 정보를 붙일 뿐이고, 그 정보를 읽어 무언가를 하는 코드가 따로 있어야 한다. 읽는 쪽은 셋이다. 이 분류는 위키가 정리한 것이다.

| 읽는 쪽 | 언제 | 예 | 필요한 보존 정책 |
|---|---|---|---|
| 컴파일러 자신 | 컴파일 | `@Override`(재정의가 아니면 오류), `@FunctionalInterface`, `@SuppressWarnings` | `SOURCE`로 충분 |
| 어노테이션 프로세서 | 컴파일 | 코드 생성·검사. Lombok · MapStruct(2차 예) | `SOURCE` 이상 |
| 리플렉션 코드 | 런타임 | 프레임워크의 설정·검증·매핑, Q27의 검증기 | `RUNTIME`만 |

「주석처럼」도 비유로만 맞다. 주석은 컴파일러가 버리지만 어노테이션은 보존 정책에 따라 클래스 파일과 런타임까지 남는다.

## 런타임에 보이는 것은 RUNTIME 어노테이션뿐이다

Q25는 쓰는 이유를 리플렉션 하나로만 답한다. 두 가지가 빠졌다.

첫째, 보존 정책(`@Retention`)이다. `RetentionPolicy` javadoc의 세 값은 이렇다.

| 값 | javadoc |
|---|---|
| `SOURCE` | "Annotations are to be discarded by the compiler." |
| `CLASS` | "recorded in the class file by the compiler but need not be retained by the VM at run time." `@Retention`을 적지 않으면 이 값이다 |
| `RUNTIME` | "recorded in the class file by the compiler and retained by the VM at run time, so they may be read reflectively." |

그래서 Q27처럼 리플렉션으로 읽을 커스텀 어노테이션은 `@Retention(RetentionPolicy.RUNTIME)`을 붙여야 한다. 빠뜨리면 `getAnnotation`이 `null`을 돌려준다. 면접에서 구현 경험을 말할 때 이것을 함께 말하면 실제로 해 본 사람의 답이 된다(위키의 보충).

둘째, 컴파일 타임 처리다. Java 6(JSR 269, 「Pluggable Annotation Processing API」)부터 `javax.annotation.processing`의 어노테이션 프로세서가 컴파일 중에 어노테이션을 읽는다. `Processor` javadoc에 따르면 처리는 라운드 단위로 돌고, 한 라운드에서 생성한 소스가 다음 라운드의 입력이 된다. 런타임 비용 없이 코드를 만들어 내는 방식이라 리플렉션 기반과 대비된다.

## 리플렉션과 접근 제어

Q26에는 단서가 둘 붙는다.

- 「힙에 로드된 클래스 타입의 객체」: `java.lang.Class` 인스턴스는 힙에 있는 평범한 객체다. 다만 클래스의 메타데이터 자체는 HotSpot에서 Metaspace에 있고, `Class` 객체는 그것을 가리키는 거울(mirror)이다. HotSpot 소스 `klass.hpp`의 `Klass`에 `_java_mirror` 필드가 있다(OpenJDK master, 2026-09-27 확인). 영역 구분은 [[JVM 메모리 구조]]에 있다.
- 「접근 제어자와 상관없이」: 틀린 말에 가깝다. private 멤버를 쓰려면 `setAccessible(true)`로 접근 검사를 꺼야 하고, 이것도 모듈 경계에서 막힌다. `AccessibleObject.setAccessible` javadoc은 호출자 C가 선언 클래스 D의 멤버에 접근을 켤 수 있는 경우를 C와 D가 같은 모듈이거나, D의 패키지를 C의 모듈에 export(public 멤버) 또는 open한 경우 등으로 한정하고, 안 되면 `InaccessibleObjectException`을 던진다. 모듈이 없는 코드(unnamed module)끼리는 여전히 다 열린다.
- JDK 내부 API는 강하게 캡슐화되었다. JEP 396(JDK 16, 「Strongly Encapsulate JDK Internals by Default」)이 기본값을 막았고, JEP 403(JDK 17, 「Strongly Encapsulate JDK Internals」)이 우회용 `--illegal-access` 옵션을 없앴다. 필요하면 `--add-opens`로 패키지를 명시적으로 열어야 한다. JEP 읽는 법은 [[JDK 개선 제안]]에 있다.

Q27은 경험 답이라 판정하지 않았다. 애플리케이션 자기 모듈(또는 unnamed module) 안의 클래스 필드를 읽는 것이라 위 제약에 걸리지 않는다. 같은 일을 하는 표준으로 Jakarta Bean Validation이 있지만 이 페이지에서는 대조하지 않았다.

## 주의·결함

외부 검증 결과다(2026-09-27). 대조한 1차 자료: JLS SE 25 §9.6 · §9.7, JDK 25 javadoc(`Retention` · `RetentionPolicy` · `AccessibleObject` · `Class` · `javax.annotation.processing.Processor`), JSR 269, JEP 396 · 403, OpenJDK master `src/hotspot/share/oops/klass.hpp`.

| 질문 | 자료의 서술 | 판정 | 정정 |
|---|---|---|---|
| Q24 | 인터페이스 기반 문법, 의미를 부여하거나 기능을 주입 | 틀림(일부). 인터페이스 기반은 맞다(§9.6). 어노테이션은 "has no effect at run time"(§9.7)이라 기능은 읽는 코드가 만든다 | 이 페이지 「어노테이션은 스스로 아무것도 하지 않는다」 |
| Q25 | 리플렉션으로 런타임에 조회 | 단서 필요. `RUNTIME` 보존일 때만 보인다. 컴파일러·어노테이션 프로세서(JSR 269)라는 더 큰 쓰임이 빠졌다 | 이 페이지 「런타임에 보이는 것은 RUNTIME 어노테이션뿐이다」 |
| Q26 | 힙의 클래스 객체로 인스턴스 생성, 접근 제어자와 상관없이 사용 | 단서 필요. 메타데이터는 Metaspace, `Class`는 힙의 거울. private 접근은 `setAccessible` + 모듈 open이 필요(JEP 396 · 403) | 이 페이지 「리플렉션과 접근 제어」 |
| Q27 | 커스텀 어노테이션 + 리플렉션으로 필드 검증 | 판정하지 않음(경험 답). `RUNTIME` 보존을 말하면 좋다 | 이 페이지 「런타임에 보이는 것은 RUNTIME 어노테이션뿐이다」 |

문서 결함: Q26은 질문에서 「어노테이션은 리플렉션으로 동작한다고 말씀해 주셨는데」라고 Q25의 답을 받는다. 그런데 Q25가 말한 것은 「리플렉션으로 조회할 수 있다」였고, 어노테이션이 리플렉션으로 동작한다는 일반화는 위 표의 컴파일 타임 쓰임과 어긋난다.

---
type: concept
title: JDK 개선 제안
aliases: [JEP, JDK Enhancement Proposal, JDK Enhancement-Proposal, JBS, JDK 이슈]
tags: [Java, JDK, OpenJDK, 출처]
created: 2026-09-27
updated: 2026-09-27
sources: []
---

# JDK 개선 제안

**JEP(JDK Enhancement Proposal)**는 OpenJDK에 큰 변경을 들일 때 쓰는 제안서이자 설계 문서다. 패치노트가 아니다. 「무엇이
바뀌었나」보다 **「왜, 어떻게 바꾸기로 했나」**를 적는다. 그래서 위키는 「왜 G1이 기본이 됐나」, 「왜 ZGC가 세대별이 됐나」 같은
주장의 근거로 JEP를 인용한다(→ [[가비지 컬렉터]]).

## 언제 JEP를 쓰나

JEP 1이 이 절차를 정의한다. 다음 가운데 하나라도 해당하면 JEP를 쓴다.

- 엔지니어링에 **2주 이상** 드는 일
- JDK나 그 개발 절차·인프라에 **큰 변화**를 주는 일
- 개발자 등의 수요가 큰 일

본문은 대개 Summary · Goals / Non-Goals · Motivation · Description · Alternatives · Risks로 이뤄진다. 이유를 인용할 때는 **Motivation**을
본다. 예: JEP 439의 "ZGC currently stores all objects together, regardless of age, so it must collect all objects every time it runs."

결과가 코드가 아닌 JEP도 있다. research JEP의 결과는 "not working code in the JDK but rather a documented deeper understanding of the
problem being addressed and its solution space"다.

[JEP 1 「JDK Enhancement-Proposal & Roadmap Process」, https://openjdk.org/jeps/1 ; JEP 439, https://openjdk.org/jeps/439 ; 2026-09-27 확인]

## 읽는 법 — 어느 버전에 들어갔나

JEP 페이지 머리의 **Status**와 **Release**를 본다. 「Closed / Delivered」에 Release 21이면 JDK 21에 들어갔다(예: JEP 444 가상 스레드).
같은 기능이 여러 JEP를 거치는 일이 흔하다. 실험 → 정식 → 기본값 → 옛 모드 제거가 각각 다른 JEP다(예: ZGC의 JEP 333 → 377 → 439 →
474 → 490). *(위키의 관찰)*

## JEP · 릴리스 노트 · JDK 이슈 · JSR

| | 무엇 | 단위 | 위키에서 쓰는 곳 |
|---|---|---|---|
| **JEP** | 큰 기능·변경의 제안과 설계 | 기능 하나 | 도입 이유, 도입 버전 |
| **릴리스 노트** | 한 릴리스에서 바뀐 것의 목록 | 버전 하나 | 올리면 무엇이 달라지나 |
| **JDK 이슈**(JBS, `JDK-숫자`) | 버그 수정·작은 변경 하나. 백포트 이력이 붙는다 | 수정 하나 | 정확한 수정 버전·백포트 |
| **JSR**(JCP) | Java SE **명세**(언어·표준 API)의 변경 | 명세 하나 | — |

- 모든 변경에 JEP가 있지는 않다. 컨테이너 인식은 JEP 없이 **JDK-8146115**로 JDK 10에 들어갔고, 이슈의 백포트 기록으로 8u191에도
  들어간 것을 확인할 수 있다(→ [[Java 8에서 11로 가는 GC 관점의 이유]]). static 필드가 힙으로 옮겨 간 JDK 7 변경도 이슈(JDK-7017732)로만
  남아 있다(→ [[JVM 메모리 구조]]).
- JEP 1: "This process does not in any way supplant the Java Community Process." 표준 인터페이스를 바꾸는 JEP는 JCP에서 따로 JSR 절차를
  밟는다. 줄이면 **JEP는 OpenJDK 구현을, JSR은 Java 명세를** 바꾼다. GC는 명세가 아니라 구현이라 GC 변경은 JEP로 온다.
  *(줄인 문장은 위키의 정리)*

## 관련

- [[가비지 컬렉터]] · [[가비지 컬렉션]] · [[JVM 메모리 구조]] · [[스레드 풀]] · [[JVM]]

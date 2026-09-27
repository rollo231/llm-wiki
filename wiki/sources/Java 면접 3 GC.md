---
type: source
title: Java 면접 3 GC
aliases: [Java 면접 3]
tags: [면접, Java, JVM, GC]
created: 2026-09-26
updated: 2026-09-27
sources:
  - "raw/interviews/java/수업 자료.pdf"
---

# Java 면접 3 GC

[[인프런 Java 면접 강의]]의 Section 3이다. 주 질문 2개와 꼬리 질문 7개가 있다. 전반부(Q1 계열)는 GC 원리(알고리즘·Heap 세대·Root·STW)이고, 후반부(Q2 계열)는 GC 구현체(Serial~G1)와 운영(모니터링·OOM)이다. 이전 섹션은 [[Java 면접 2 JVM과 실행 원리]], 다음 섹션은 [[Java 면접 4 동시성 이슈]]다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 인프런(Inflearn) Java 면접 대비 강의 자료 PDF. 강의명은 자료에 없고, 인프런은 워터마크로 확인 |
| 섹션 제목 | Section 3 — GC (Garbage Collection) |
| 원본 파일 | `raw/interviews/java/수업 자료.pdf` p23–50 (전체 117p) |
| 강사 | 자료에 표기 없음 |
| 작성 시기 | PDF 수정일 2026-03-03 |
| URL | 없음 (유료 강의 자료) |

## 요약

| 질문 | 쪽 | Gold 답의 요지 | Gold와의 차이("이유") |
|---|---|---|---|
| **Q1.** GC 알고리즘, Java는 무엇을 쓰나 | p24–26 | Reference Counting과 Mark and Sweep이 있고, Java는 Mark and Sweep을 쓴다. RC는 순환 참조 때문에 누수가 난다. M&S는 Root에서 그래프 순회로 도달 가능한 객체를 마킹하고 나머지를 해제하는데, 특정 시점에 수행하므로 STW가 생긴다 | Silver는 동작과 선택 근거가 부족하다 |
| **Q1-1.** Heap 구조와 GC 실행 시점 (Java 8 기준) | p27–29 | Heap = Young(Eden·Survivor 0·1) + Old. Eden이 차면 Minor GC가 M&S로 살아 있는 객체를 Survivor로 옮긴다. 여러 번 살아남으면 Old로 승격된다. Old가 차면 Major GC | Bronze는 Young/Old 구조가 없다. Silver는 M&S와 객체 이동이 없다 |
| **Q1-2.** Root Space란 | p30–32 | M&S가 그래프 순회를 시작하는 출발점. Stack의 로컬 변수, 메서드 영역의 static 변수처럼 Heap 객체를 가리키는 변수들 | Silver는 위치·예시만 있고 "순회 시작점"이라는 원리가 없다 |
| **Q1-3.** 왜 Young과 Old로 나누나 | p33–35 | 통계적으로 대부분의 객체는 금방 죽는다. 그래서 수명 짧은 객체가 모인 Young만 집중 수거하면 전체 Heap을 매번 훑는 것보다 효율적이다 | Bronze는 "효율적"만 말한다. Silver는 영역 집중 수거라는 원리가 없다 |
| **Q1-4.** Stop-The-World란, 왜 생기나 | p36–38 | GC 동안 애플리케이션의 모든 스레드가 멈추는 것. 이유는 둘: 실행 중엔 참조가 계속 바뀌어 판별이 어렵고, Compaction 때 객체 주소가 바뀐다 | Silver는 현상만 말하고 원인이 없다 |
| **Q2.** JVM의 Garbage Collector 종류 | p39–41 | Serial(단일 스레드, STW 김, Compaction 있음), Parallel(Serial의 멀티 스레드판), CMS(대부분 동시 수행, CPU·메모리 많이 씀, Compaction 기본 없음), G1(Region 단위, 동시 수행 + Compaction) | Silver는 이름과 개념만 나열한다("G1은 최신 GC") |
| **Q2-1.** Java 8·11 기본 GC와 바뀐 이유 | p42–44 | Java 8은 Parallel, Java 11은 G1. G1은 Region을 독립적으로 골라 수집해 큰 Heap에 유리하다. 짧고 예측 가능한 STW가 중요한 금융·실시간 처리에 맞는다(`-XX:MaxGCPauseMillis`) | Bronze는 "더 좋아서". Silver는 큰 Heap·예측 가능한 STW라는 맥락이 없다 |
| **Q2-2.** G1의 Heap 구조와 동작 | p45–47 | 고정 크기 Region에 Young/Old 역할이 동적으로 붙고, 물리적으로 연속일 필요가 없다. 큰 객체는 Humongous. Young-only를 반복하다 Old 비율이 임계치를 넘으면 Concurrent Marking, 이어 Mixed GC로 garbage 많은 Old Region부터 수거("Garbage First"). Marking은 동시지만 Young·Mixed GC는 STW | Bronze는 Region의 의미가 없다. Silver는 비연속성·사이클·Mixed GC가 빠졌다 |
| **Q2-3.** GC 모니터링의 필요성, OOM 대처 | p48–50 | Minor GC는 수 ms~수십 ms, Major GC는 수백 ms~수 초라 타임아웃·장애가 날 수 있다. 그래서 GC 로그·VisualVM·Prometheus+Grafana로 빈도·시간·Heap 사용률을 본다. OOM 대처 4단계: 힙 덤프 자동 생성 옵션 → MAT·VisualVM으로 분석(Leak Suspects) → 근본 원인 수정 → 임시로 `-Xmx` 증설 | Bronze는 "Heap을 늘리면 된다". Silver는 예방·덤프 옵션·체계적 단계가 없다 |

## 핵심

- **Q2-1과 Q2-2는 [[지연 시간과 처리량]]의 맞교환을 GC에 적용한 것이다.** Parallel은 처리량, G1은 예측 가능한 지연을 고른다. 자료는 이 축을 이름 붙이지 않는다. *(위키의 연결)* → [[가비지 컬렉터]]
- **OOM 대처 순서(덤프 → 분석 → 근본 원인 → 마지막에 힙 증설)는 그대로 쓸 만하다.** "Heap을 늘린다"를 Bronze로 둔 판정이 이 섹션에서 가장 실무적이다. → [[가비지 컬렉션]]
- **Q1-3의 근거는 약한 세대 가설(weak generational hypothesis)이다.** 자료는 이름을 붙이지 않는다. → [[가비지 컬렉션]]

## 주의·결함

- ⚠️ **"Java는 Mark and Sweep을 쓴다"(Q1)와 "Minor GC도 Mark and Sweep"(Q1-1)은 틀렸다.** Young 영역은 복사(copying) 방식이고 sweep 단계가 없다. Old·Full GC는 mark-compact다. → [[가비지 컬렉션]]
- ⚠️ **"Major GC"는 JVM 공식 용어가 아니다.** 로그에서는 Full GC와 G1의 Mixed GC를 구분한다. → [[가비지 컬렉션]]
- ⚠️ **GC Root 목록(Q1-2)이 불완전하다.** JNI 참조, 살아 있는 스레드, 잡힌 모니터 등도 루트다. static 필드는 JDK 7부터 힙에 있다(⚠️ 위키 정정: 처음엔 JDK 8로 적었다). → [[가비지 컬렉션]]
- ⚠️ **STW가 본질적으로 필요하다는 서술(Q1-4)은 전통적 GC에만 맞다.** ZGC·Shenandoah는 compaction까지 동시에 한다. → [[가비지 컬렉션]]
- ⚠️ **GC 목록(Q2)이 G1에서 멈춘다.** CMS는 JDK 14에서 제거됐고, ZGC·Shenandoah가 빠졌다. → [[가비지 컬렉터]]
- ⚠️ **G1이 기본이 된 것은 JDK 9이고, 그것도 server-class 머신에서만이다(Q2-1).** 작은 컨테이너에서는 Serial이 골라진다. JDK 27부터는 모든 환경에서 G1이다. → [[가비지 컬렉터]]
- ✅ G1 사이클(Q2-2)과 힙 덤프 플래그 철자(Q2-3)는 1차 자료와 맞다. 다만 p50 원문은 `-XX:+ HeapDumpOnOutOfMemoryError`처럼 `+` 뒤에 공백이 있다(오타). GC 소요 시간 수치는 힙 크기·GC 종류에 따라 크게 다른 경험치다.
- Q1-1의 "Survivor 0/1 Generation"은 세대가 아니라 Young 세대 안의 공간(space)이다.

## 관련

- 개념: [[가비지 컬렉션]] · [[가비지 컬렉터]] · [[지연 시간과 처리량]] · [[JVM 메모리 구조]](Q1-2의 "메서드 영역의 static 변수"가 실제로 어디 있나)
- 엔티티: [[JVM]] · [[인프런 Java 면접 강의]]
- 같은 섹션의 부록: [[Java 면접 3 빈출 질문]] (GC 정의·장단점·OOM 종류·PermGen·static)
- 이전 섹션: [[Java 면접 2 JVM과 실행 원리]]
- 다음 섹션: [[Java 면접 4 동시성 이슈]]

---
type: source
title: Java 면접 4 빈출 질문
aliases: [동시성 빈출 질문, 채널톡 동시성 빈출 질문]
tags: [면접, Java, 동시성, 스레드, 컬렉션]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "raw/interviews/java/동시성_이슈_채널톡_면접관이_뽑은_빈출_질문.pdf"
---

# Java 면접 4 빈출 질문

[[인프런 Java 면접 강의]] Section 4(동시성 이슈)의 부록 PDF다. 부록이라는 것은 제목의 "[동시성 이슈]"가 Section 4 제목과 같아서 한 추론이다. [[Java 면접 2 빈출 질문]] · [[Java 면접 3 빈출 질문]]과 형식이 같다. 질문은 9개이고, 질문마다 빈도 별점(⭐1~3)과 짧은 답 하나가 붙는다. 등급 루브릭은 없다. 슬라이드 쪽 [[Java 면접 4 동시성 이슈]]는 가시성·원자성과 volatile·synchronized·CAS를 다루고, 이 자료는 그 밖의 주제인 불변 객체, 싱글톤 초기화, 스레드 안전의 정의, 동시성 컬렉션을 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 「[동시성 이슈] 채널톡 면접관이 뽑은 빈출 질문」. 인프런 Java 면접 대비 강의의 부록 PDF다. 인프런은 워터마크로 확인했다 |
| 원본 파일 | `raw/interviews/java/동시성_이슈_채널톡_면접관이_뽑은_빈출_질문.pdf` p1–2 (전체 2p, A3) |
| 형식 | 웹 페이지를 인쇄한 PDF(생성기 HeadlessChrome). 앞의 두 부록과 같은 「답변」 토글 모양이다. Q4에 코드 블록 하나가 있다 |
| 강사 | 자료에 표기 없음. 「채널톡 면접관」은 제목에 적힌 표현이다 |
| 작성 시기 | PDF 생성일 2026-03-07. Section 3 부록과 같은 날이다 |
| URL | 없음 (유료 강의 자료) |

## 요약

| # | 질문 | 빈도 | 답의 요지 | 자세히 |
|---|---|---|---|---|
| 1 | 가변 객체와 불변 객체의 차이 | ⭐⭐ | 가변 객체는 생성 뒤 상태가 바뀌어 멀티스레드에서 동기화가 필요하다(ArrayList · HashMap · StringBuilder). 불변 객체는 바뀌지 않아 멀티스레드에서 안전하다(String) | [[불변 객체]] |
| 2 | 불변 객체는 언제 쓰나 | ⭐ | 캐싱, 멀티스레드에서 동기화를 쉽게 하려고 | [[불변 객체]] |
| 3 | 가시성만 해결하면 되지 않나 | ⭐ | 가시성은 공유 메모리를 읽을 때의 보장이다. 여러 스레드가 쓰면 여전히 문제가 난다 | [[동시성 문제]] |
| 4 | synchronized를 써 본 경험 | ⭐⭐ | 싱글톤 생성에 썼다가, 하나 외에 전부 lock에 걸려 비효율이라 LazyHolder로 바꿨다. JVM의 클래스 초기화가 보장하는 원자성에 초기화를 맡긴다(p1 코드) | [[동기화 기법]] · [[클래스 로딩]] |
| 5 | Thread-safe의 의미 | ⭐⭐⭐ | 여러 스레드가 함수·변수·객체에 동시에 접근해도 실행에 문제가 없다 | [[동시성 문제]] |
| 6 | Vector · Hashtable · `Collections.synchronizedXxx`의 문제 | ⭐ | 잠금 객체 하나를 공유해서, 한 스레드가 잡으면 나머지는 모든 메서드에서 Blocking되고, 성능이 떨어진다 | [[동시성 컬렉션]] |
| 7 | Synchronized 컬렉션 vs Concurrent 컬렉션 | ⭐ | 전자는 읽기·쓰기 모두 인스턴스를 잠근다. Concurrent 컬렉션은 읽기에 잠금이 없고 쓰기만 잠금이나 CAS를 쓴다 | [[동시성 컬렉션]] |
| 8 | SynchronizedList vs CopyOnWriteArrayList | ⭐ | 후자는 쓸 때 잠그고 원본 배열을 복사한 임시 배열에 쓴 뒤 원본을 갱신한다. 그래서 읽기는 잠금이 없다 (p2) | [[동시성 컬렉션]] |
| 9 | ConcurrentHashMap을 HashMap과 비교 | ⭐⭐ | SynchronizedMap은 인스턴스를 잠근다. ConcurrentHashMap은 버킷마다 따로 잠그고, 빈 버킷에 넣을 때는 락 대신 CAS를 쓴다 (p2) | [[동시성 컬렉션]] |

Q4의 코드는 `private static class Holder { public static final Singleton instance = new Singleton(); }`와 `getInstance() { return Holder.instance; }`다. 흔히 initialization-on-demand holder라고 부르는 관용구이고, 자료는 "LazyHolder"라는 이름만 쓴다.

## 핵심

- 별점이 가장 높은 Q5(Thread-safe)의 답이 가장 막연하다. "문제가 없다"만으로는 정의가 되지 않는다. 스레드 안전은 어떤 인터리빙에서도, 호출하는 쪽이 따로 동기화하지 않아도, 명세대로 동작한다는 뜻이다. 이 세 조건을 말해야 Q6(동기화 컬렉션도 복합 연산은 안전하지 않다)로 이어진다([[동시성 문제]]).
- Q3의 답은 조건을 잘못 짚었다. 문제를 일으키는 것은 쓰는 스레드의 수보다, 읽고-고치고-쓰기나 확인 후 행동 같은 복합 연산이다. 쓰는 스레드가 하나면 `volatile`로 충분하고, 여러 스레드가 `count++`를 하면 `volatile`로도 깨진다([[원자성 문제가 나는 시나리오]]).
- Q4는 synchronized 경험을 물었지만, 답의 중심은 클래스 초기화에 있다. holder 관용구가 안전한 이유는 JLS §12.4.2의 클래스별 초기화 락이 상호 배제와 happens-before를 함께 주기 때문이다. 초기화가 지연되는 이유는 §12.4.1(static 필드를 처음 쓸 때 초기화)이다. [[클래스 로딩]]에 적은 "명세가 보장하는 것은 초기화 시점"이 여기에 쓰인다는 연결은 위키가 했다.
- Q6~Q9는 이어서 읽힌다. 락 하나에서 시작해 락을 쪼개고(버킷 락), 읽기에서 락을 없앤다(스냅샷·volatile 읽기). 자료는 이 흐름을 "Concurrent는 읽기에 락이 없다"는 한 문장으로 뭉뚱그리다가 틀렸다(Q7, [[동시성 컬렉션]]).

## 주의·결함

외부 검증 결과다(2026-09-27). 대조한 1차 자료: JLS SE 21 §12.4 · §17.4.5 · §17.5 · §17.7(인용한 문구는 SE 25에도 그대로 있다), OpenJDK `openjdk/jdk` master와 jdk8u · jdk7u의 `ConcurrentHashMap.java` · `CopyOnWriteArrayList.java` · `Collections.java` · `String.java`, `java.util.concurrent` package-summary, JDK-8134853. Goetz 『Java Concurrency in Practice』 · Bloch 『Effective Java』는 2차 자료로 표시했다.

| 질문 | 자료의 서술 | 판정 | 정정이 있는 곳 |
|---|---|---|---|
| Q1 | 불변 객체는 멀티스레드에서 안전하다 | 단서 필요. 필드가 모두 `final`이고 생성자에서 `this`가 새지 않아야 JLS §17.5가 동기화 없는 가시성을 보장한다. 그렇지 않으면 안전한 공개가 따로 필요하다 | [[불변 객체]] |
| Q1 | String은 내부 상태가 바뀌지 않는다 | 단서 필요. `hash` 필드는 final이 아니고 처음 계산할 때 쓰인다(소스 주석 "benign data race"). 바뀌지 않는 것은 관찰 가능한 상태다 | [[불변 객체]] |
| Q2 | 쓰임 = 캐싱 · 동기화 단순화 | 단서 필요. 맵 키·집합 원소(해시가 안 바뀜), 방어적 복사가 필요 없는 공유, 실패 원자성이 빠졌다 | [[불변 객체]] |
| Q3 | 여러 스레드가 쓰면 문제 | 단서 필요. 진짜 조건은 복합 연산이다. 가시성 · 원자성 · 순서를 나눠 말해야 한다 | [[동시성 문제]] |
| Q4 | synchronized 싱글톤은 "동시에 생성자에 접근할 때" 하나 외 전부 lock | 틀림. `synchronized getInstance()`는 생성이 끝난 뒤에도 호출할 때마다 모니터를 잡는다. 경합이 없으면 요즘 HotSpot에서 싸다는 단서는 붙는다 | [[동기화 기법]] |
| Q4 | LazyHolder = 클래스 초기화의 "원자적 특성" | 단서 필요. 정확히는 초기화 락 LC의 상호 배제 + happens-before(JLS §12.4.2). 생성자가 예외를 던지면 이후 접근은 `NoClassDefFoundError`다. 리플렉션·직렬화에는 enum 싱글톤이 대안이다(Effective Java Item 3, 2차) | [[동기화 기법]] · [[클래스 로딩]] |
| Q5 | Thread-safe = 동시에 접근해도 문제없음 | 단서 필요. 인터리빙과 무관하게, 호출자의 추가 동기화 없이, 올바르게 동작한다(JCIP §2.1, 2차) | [[동시성 문제]] |
| Q6 | 락 하나를 공유해 모두 Blocking | 맞음(구현) · 누락. `Collections.SynchronizedCollection`의 `mutex = this`. 더 큰 문제인 복합 연산의 비원자성과 순회 중 수동 동기화(javadoc "It is imperative that the user manually synchronize"), fail-fast 이터레이터가 빠졌다 | [[동시성 컬렉션]] |
| Q7 | Concurrent 컬렉션은 읽기에 잠금이 없다 | 틀림. 일반화할 수 없다. `ArrayBlockingQueue`는 락 하나로 `peek`·`size`까지 잠그고, `LinkedBlockingQueue.take`는 `takeLock`을 잡는다. 반대로 `ConcurrentLinkedQueue`·`ConcurrentSkipListMap`은 쓰기에도 락이 없다. package-summary가 약속하는 것은 "not governed by a single exclusion lock"과 weakly consistent 이터레이터다 | [[동시성 컬렉션]] |
| Q8 | 복사본에 쓴 뒤 "원본 배열을 갱신" | 단서 필요. 원본은 건드리지 않는다. `setArray`로 volatile 배열 참조를 새 배열로 바꾼다. 락은 JDK 8의 `ReentrantLock`에서 JDK 9부터 `synchronized (lock)`으로 바뀌었다(JDK-8134853). 쓰기마다 O(n) 복사라 읽기가 압도적으로 많을 때만 맞는다 | [[동시성 컬렉션]] |
| Q9 | 버킷별 잠금, 빈 버킷은 CAS | 단서 필요. 설명은 JDK 8 이후 구현으로 맞다(`casTabAt`, 첫 노드에 `synchronized (f)`). 그러나 질문(HashMap 비교)과 답(SynchronizedMap 비교)이 어긋난다. HashMap과의 차이인 null 금지, 락 없는 `get`, JDK 7의 Segment 락이 빠졌다 | [[동시성 컬렉션]] |

오타: "CopyOnArrayList"(바른 이름 `CopyOnWriteArrayList`), "SynchronziedXxx", "HashTable"(바른 이름 `Hashtable`). "SynchronizedList · SynchronizedMap"은 `Collections.synchronizedList/Map`이 돌려주는 내부 클래스 이름이지 공개 API가 아니다.

## 관련

- 개념: [[불변 객체]] · [[동시성 컬렉션]] · [[동시성 문제]] · [[동기화 기법]] · [[클래스 로딩]]
- 노트: [[원자성 문제가 나는 시나리오]] · [[가시성 문제는 지금도 생기나]]
- 엔티티: [[인프런 Java 면접 강의]]
- 같은 섹션의 슬라이드: [[Java 면접 4 동시성 이슈]] · 앞 섹션의 부록: [[Java 면접 3 빈출 질문]]

---
type: source
title: Java 면접 기타 빈출 질문 4 JCF
aliases: [JCF 빈출 질문, 채널톡 JCF 빈출 질문, 컬렉션 빈출 질문]
tags: [면접, Java, 컬렉션, 자료구조]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "raw/interviews/java/기타_채널톡_면접관이_뽑은_빈출_질문.pdf"
---

# Java 면접 기타 빈출 질문 4 JCF

[[인프런 Java 면접 강의]]의 부록 PDF 「[기타] 채널톡 면접관이 뽑은 빈출 질문」 가운데 마지막 소절 「JCF」다. 이 PDF는 대응하는 슬라이드 Section이 없고, 자료가 스스로 네 소절(자바 기본 · 문자열, 예외, 제네릭 · 어노테이션, 리플렉션 · JCF)로 나눈다. 위키는 소절마다 source 페이지를 하나씩 두었다(사용자 결정 2026-09-27). 앞의 세 소절은 [[Java 면접 기타 빈출 질문 1 자바 기본]] · [[Java 면접 기타 빈출 질문 2 문자열 예외 제네릭]] · [[Java 면접 기타 빈출 질문 3 어노테이션과 리플렉션]]이다. 질문은 17개이고, 형식은 다른 부록과 같다(빈도 별점 ⭐1~3과 짧은 답 하나, 등급 루브릭 없음).

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 「[기타] 채널톡 면접관이 뽑은 빈출 질문」의 「JCF」 소절. 인프런 Java 면접 대비 강의의 부록 PDF다. 인프런은 워터마크로 확인했다 |
| 원본 파일 | `raw/interviews/java/기타_채널톡_면접관이_뽑은_빈출_질문.pdf` p3–4 (전체 4p, A3) |
| 형식 | 웹 페이지를 인쇄한 PDF(생성기 HeadlessChrome). 코드 블록은 없다 |
| 강사 | 자료에 표기 없음. 「채널톡 면접관」은 제목에 적힌 표현이다 |
| 작성 시기 | PDF 생성일 2026-03-07. 다른 부록과 같은 날이다 |
| URL | 없음 (유료 강의 자료) |

## 요약

자료에는 질문 번호가 없다. 위키는 PDF 전체에 1~44로 번호를 매겼고, 이 소절은 Q28~Q44다.

| # | 질문 | 빈도 | 답의 요지 | 자세히 |
|---|---|---|---|---|
| 28 | JCF란 | ⭐ | 다수의 데이터를 쉽고 효과적으로 처리하는 표준화된 방법을 제공하는 클래스의 집합 (p3) | [[Java 컬렉션 프레임워크]] |
| 29 | JCF의 계층 구조 | ⭐ | Collection과 Map으로 나뉘고, Collection은 List · Queue · Set으로 나뉜다 | [[Java 컬렉션 프레임워크]] |
| 30 | List와 구현체 | ⭐ | 순서가 있고 중복을 허용한다. ArrayList · LinkedList · Vector | [[Java 컬렉션 프레임워크]] |
| 31 | ArrayList | ⭐⭐⭐ | 크기가 가변적인 선형 리스트, 인덱스로 요소를 관리한다 | [[Java 컬렉션 프레임워크]] |
| 32 | ArrayList는 어떻게 늘어나나 | ⭐⭐⭐ | capacity를 넘으면 자동으로 용량을 늘린다 | [[Java 컬렉션 프레임워크]] |
| 33 | LinkedList | ⭐⭐⭐ | 노드가 데이터와 포인터를 갖고 앞뒤로 연결된다. 추가·삭제 때 앞뒤 링크만 바뀐다 | [[Java 컬렉션 프레임워크]] |
| 34 | ArrayList와 LinkedList 선택 | ⭐⭐⭐ | ArrayList는 접근이 빠르고 삽입·삭제가 느리다. 양 끝 삽입·삭제가 잦은 Queue는 LinkedList | [[Java 컬렉션 프레임워크]] |
| 35 | ArrayList와 Vector | ⭐ | Vector는 모든 메서드가 synchronized라 느리고, CopyOnWriteArrayList 같은 대안이 있어 거의 안 쓴다 | [[동시성 컬렉션]] |
| 36 | Stack과 Queue | ⭐⭐⭐ | Stack은 LIFO이고 Vector를 상속한 레거시, Queue는 FIFO이고 주로 LinkedList로 구현한다 | [[Java 컬렉션 프레임워크]] |
| 37 | Set과 구현 클래스 | ⭐ | 중복을 저장하지 않고 저장 순서를 유지하지 않는다. HashSet · LinkedHashSet · TreeSet | [[Java 컬렉션 프레임워크]] |
| 38 | Set의 중복 제거 | ⭐⭐⭐ | hashCode()로 해시 코드를 얻어 비교하고, 같으면 equals()로 비교한다 | [[HashMap]] · [[equals와 hashCode]] |
| 39 | Map과 구현 클래스 | ⭐ | 키는 중복 불가, 값은 중복 가능. 키로 상수 시간에 찾는다. HashTable · HashMap · TreeMap (p3–4) | [[Java 컬렉션 프레임워크]] |
| 40 | HashMap의 동작 | ⭐⭐⭐ | 해시 함수로 키를 인덱스로 바꿔 그 자리에 저장한다. 이 인덱스를 해시 값이라 부른다 (p4) | [[HashMap]] |
| 41 | HashMap의 최악 시간 복잡도 | ⭐⭐⭐ | 해시 충돌은 체이닝으로 푼다. 한 버킷에 모두 충돌하면 O(N) | [[HashMap]] |
| 42 | Map이 Collection을 상속하지 않은 이유 | ⭐ | Map의 「요소」가 모호하다. `remove`가 키-값 쌍이 아니라 키를 받는다 | [[Java 컬렉션 프레임워크]] |
| 43 | Iterable과 Iterator | ⭐ | Iterable은 Collection의 상위 인터페이스로 `iterator()`를 가진다. Iterator는 `hasNext` · `next` · `remove` | [[Java 컬렉션 프레임워크]] |
| 44 | Collection과 Collections | ⭐ | Collection은 최상위 인터페이스, Collections는 정적 메서드를 모은 유틸리티 클래스 | [[Java 컬렉션 프레임워크]] |

## 핵심

- 별점 셋짜리 여덟 질문(Q31~Q34 · Q36 · Q38 · Q40 · Q41) 가운데 Q38 · Q40은 틀렸고 Q41은 JDK 8 이전 이야기다. Q32 · Q34 · Q36에는 단서가 필요하다. 가장 자주 나온다는 HashMap 질문 세 개(Q38 · Q40 · Q41)가 모두 흔들린다.
- Q38의 「hashCode()는 객체의 주소를 가져와서 같은 객체인지 확인한다」는 [[Java 면접 기타 빈출 질문 1 자바 기본]]의 hashCode 답과 같은 오류다. hashCode는 주소도 식별자도 아니다([[equals와 hashCode]]).
- Q34 · Q36은 「양 끝 삽입·삭제에는 LinkedList」라고 한다. 지금의 Javadoc은 큐와 스택 모두 `ArrayDeque`를 권한다([[Java 컬렉션 프레임워크]]).
- Q35의 Vector 대안인 `CopyOnWriteArrayList`는 읽기가 압도적으로 많을 때만 효율적이다. 이 부분은 [[동시성 컬렉션]]에 이미 정리되어 있다.
- Q42는 결론은 맞지만 논거가 설계 FAQ와 다르다. FAQ는 `remove`의 인자 모양이 아니라 「키가 무엇에 매핑되는지 물을 수 없는 빈약한 추상화」를 이유로 든다.

## 주의·결함

외부 검증 결과다(2026-09-27). 대조한 1차 자료: OpenJDK `openjdk/jdk` master의 `java/util` 소스(`HashMap.java` · `HashSet.java` · `ArrayList.java` · `LinkedList.java` · `ArrayDeque.java` · `Stack.java` · `Vector.java` · `Collection.java` · `List.java` · `Queue.java`, `java/lang/Iterable.java`), JDK 25 Javadoc, JEP 180 · JEP 431, 「Java Collections API Design FAQ」(JDK 25판). Joshua Bloch의 트윗은 2차 자료로 표시했다.

| 질문 | 자료의 서술 | 판정 | 정정이 있는 곳 |
|---|---|---|---|
| Q28 | JCF = 표준화된 방법을 제공하는 클래스의 집합 | 맞음. 외부 검증 대상에 넣지 않았고 위키의 판단이다 | [[Java 컬렉션 프레임워크]] |
| Q29 | Collection은 List · Queue · Set으로 나뉜다 | 단서 필요. 위에 Iterable, 아래에 Deque · Sorted/Navigable, JDK 21의 Sequenced 인터페이스가 빠졌다 | [[Java 컬렉션 프레임워크]] |
| Q30 | List가 ArrayList 등에 「상속」 | 단서 필요. 인터페이스이므로 구현(implements)이다 | [[Java 컬렉션 프레임워크]] |
| Q31 | 가변 크기, 인덱스로 관리 | 맞음 | [[Java 컬렉션 프레임워크]] |
| Q32 | capacity를 넘으면 자동으로 늘린다 | 단서 필요. 약 1.5배와 지연 할당은 구현이고, 명세는 「상각 상수 시간」뿐이다 | [[Java 컬렉션 프레임워크]] |
| Q33 | 노드가 앞뒤로 연결, 링크만 바뀐다 | 맞음. 이중 연결 리스트이고 Deque도 구현한다 | [[Java 컬렉션 프레임워크]] |
| Q34 | LinkedList는 삽입·삭제가 빠르다, Queue는 LinkedList | 단서 필요. 위치 지정 삽입은 순회 O(n), 큐에는 ArrayDeque | [[Java 컬렉션 프레임워크]] |
| Q35 | CopyOnWriteArrayList가 더 효율적인 대안 | 단서 필요. 순회가 변경보다 훨씬 많을 때만이다 | [[동시성 컬렉션]] |
| Q36 | Queue는 FIFO, 주로 LinkedList | 단서 필요. Queue는 FIFO를 강제하지 않는다(PriorityQueue). Stack · Queue 모두 ArrayDeque 권장 | [[Java 컬렉션 프레임워크]] |
| Q37 | Set은 저장 순서를 유지하지 않는다 | 틀림. HashSet만 그렇다. 같은 답에 든 LinkedHashSet은 삽입 순서, TreeSet은 정렬 순서다 | [[Java 컬렉션 프레임워크]] |
| Q38 | hashCode()는 주소를 가져와 같은 객체인지 확인한다 | 틀림. 같은 버킷의 노드와 섞은 해시를 비교한 뒤 `==` 또는 `equals`. equals가 참이면 동등하지 같은 객체가 아니다 | [[HashMap]] · [[equals와 hashCode]] |
| Q39 | Map은 상수 시간 탐색, 구현 HashTable | 단서 필요. 상수 시간은 해시 기반만(TreeMap은 log n), 클래스 이름은 `Hashtable` | [[Java 컬렉션 프레임워크]] |
| Q40 | 이 인덱스를 해시 값이라 부른다 | 틀림. 해시 값과 버킷 인덱스(`(n - 1) & hash`)는 다른 값이다 | [[HashMap]] |
| Q41 | 한 버킷에 모두 충돌하면 O(N) | 낡음. JDK 8(JEP 180)부터 트리화로 O(log n). 단, 해시가 같고 Comparable도 아닌 키는 여전히 O(n) | [[HashMap]] |
| Q42 | 요소가 모호하고 `remove` 인자가 다르다 | 단서 필요. 결론은 설계 FAQ와 같고 논거가 다르다. 「Collections.remove」는 `Collection.remove`의 오타 | [[Java 컬렉션 프레임워크]] |
| Q43 | Iterator의 `remove` 등 | 단서 필요. Iterable은 `java.lang`에 있고 for-each의 대상이 된다. `Iterator.remove`는 기본 구현이 예외를 던지는 default 메서드다 | [[Java 컬렉션 프레임워크]] |
| Q44 | Collection과 Collections | 맞음 | [[Java 컬렉션 프레임워크]] |

합계 17문항: 맞음 4(Q28은 위키 판단) · 단서 필요 9 · 틀림 3 · 낡음 1.

문서 결함: Q42의 「Collections.remove(Object o)」는 인터페이스 `Collection`을 유틸리티 클래스 `Collections`로 잘못 적었다. 바로 뒤 Q44가 둘의 차이를 묻는 질문이라 더 눈에 띈다. Q39의 「HashTable」도 클래스 이름(`Hashtable`)과 다르다.

## 관련

- 트래커: [[인프런 Java 면접 강의]]
- 같은 PDF의 다른 소절: [[Java 면접 기타 빈출 질문 1 자바 기본]] · [[Java 면접 기타 빈출 질문 2 문자열 예외 제네릭]] · [[Java 면접 기타 빈출 질문 3 어노테이션과 리플렉션]]
- 개념: [[Java 컬렉션 프레임워크]] · [[HashMap]] · [[equals와 hashCode]] · [[동시성 컬렉션]]

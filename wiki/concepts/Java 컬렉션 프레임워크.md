---
type: concept
title: Java 컬렉션 프레임워크
aliases: [JCF, Java Collections Framework, 컬렉션 프레임워크, Collection, Collections, Iterable, Iterator, ArrayList, LinkedList, ArrayDeque, SequencedCollection]
tags: [Java, 컬렉션, 자료구조, 면접]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "[[Java 면접 기타 빈출 질문 4 JCF]]"
---

# Java 컬렉션 프레임워크

`java.util`의 컬렉션 인터페이스와 구현체, 알고리즘을 묶어 부르는 이름이다. 약어 JCF(Java Collections Framework)는 면접 자료가 쓰는 표현이다. 면접에서는 계층 구조, 구현체를 무엇으로 고르는지, 레거시 클래스를 왜 안 쓰는지를 묻는다([[Java 면접 기타 빈출 질문 4 JCF]] Q28~Q44). 해시 기반 구현의 내부는 [[HashMap]], 스레드 안전한 컬렉션은 [[동시성 컬렉션]]에 따로 있다.

## 계층

자료(Q29)는 「Collection과 Map으로 나뉘고, Collection은 List · Queue · Set으로 나뉜다」고 한다. 큰 틀은 맞지만 위아래가 빠졌다. JDK 25 기준의 주요 인터페이스는 이렇다.

| 인터페이스 | 상위 인터페이스 (JDK 25) | 대표 구현 |
|---|---|---|
| `Collection` | `Iterable` | — |
| `SequencedCollection` (JDK 21) | `Collection` | — |
| `List` | `SequencedCollection` | `ArrayList` · `LinkedList` |
| `Queue` | `Collection` | `PriorityQueue` |
| `Deque` | `Queue` · `SequencedCollection` | `ArrayDeque` · `LinkedList` |
| `Set` | `Collection` | `HashSet` |
| `SequencedSet` (JDK 21) | `SequencedCollection` · `Set` | `LinkedHashSet` |
| `SortedSet` → `NavigableSet` | `Set` · `SequencedSet` | `TreeSet` |
| `Map` | 없음 (Collection과 별개) | `HashMap` |
| `SequencedMap` (JDK 21) | `Map` | `LinkedHashMap` |
| `SortedMap` → `NavigableMap` | `SequencedMap` | `TreeMap` |

상위 인터페이스는 로컬 JDK 25의 `javap` 출력으로 확인했다.

- `Collection<E> extends Iterable<E>`다. Javadoc은 Collection을 "The root interface in the *collection hierarchy*"라 부르지만, 그 위에 `java.lang.Iterable`이 있다. Iterable을 구현하면 향상된 for 문(for-each)의 대상이 된다(JLS §14.14.2).
- JDK 21의 JEP 431 「Sequenced Collections」가 "collections with a defined encounter order"를 나타내는 인터페이스를 넣었다. `List`와 `Deque`는 `SequencedCollection`을, `SortedSet`은 `SequencedSet`을 상속한다. 그래서 `getFirst()` · `getLast()` · `reversed()`를 List와 Deque, LinkedHashSet, LinkedHashMap이 같은 이름으로 갖는다.
- List는 인터페이스이므로 ArrayList 등이 List를 「상속」한다는 자료(Q30)의 표현은 부정확하다. `ArrayList extends AbstractList implements List`처럼 구현(implements)한다.

[OpenJDK master `Collection.java` · `List.java` · `Deque.java` · `SortedSet.java`, JEP 431 https://openjdk.org/jeps/431 , 2026-09-27 확인]

### Map이 Collection이 아닌 이유

설계 FAQ의 답은 이렇다. "This was by design. We feel that mappings are not collections and collections are not mappings. … If a Map is a Collection, what are the elements? The only reasonable answer is "Key-value pairs", but this provides a very limited (and not particularly useful) Map abstraction. You can't ask what value a given key maps to, nor can you delete the entry for a given key without knowing what value it maps to." FAQ는 이어서 Map을 `keySet` · `entrySet` · `values` 세 가지 Collection 뷰로 볼 수 있다고 덧붙인다.

자료(Q42)는 결론이 같지만, 논거로 `remove`의 인자 모양(키-값 쌍 대신 키)을 든다. FAQ의 요점은 인자 모양이 아니라 키로 값을 묻거나 지울 수 없는 추상화가 쓸모없다는 데 있다. [Oracle, 「Java Collections API Design FAQ」 JDK 25판, https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/doc-files/coll-designfaq.html , 2026-09-27 확인]

## 구현체 고르기

| 쓰임 | 기본 선택 | 대안과 이유 |
|---|---|---|
| 목록 | `ArrayList` | 인덱스 접근 O(1), 끝에 추가는 상각 O(1). 중간 삽입·삭제는 뒤 원소를 미는 O(n) |
| 스택 | `ArrayDeque` | `Stack`은 Vector를 상속한 레거시다. Javadoc이 Deque를 쓰라고 한다 |
| 큐 | `ArrayDeque` | `LinkedList`도 Deque지만 Javadoc은 ArrayDeque가 더 빠를 것이라 한다. 우선순위가 필요하면 `PriorityQueue` |
| 집합 | `HashSet` | 순서가 필요하면 `LinkedHashSet`(삽입 순서), 정렬이 필요하면 `TreeSet` |
| 맵 | `HashMap` | 순서가 필요하면 `LinkedHashMap`(삽입 순서), 정렬·범위 검색이 필요하면 `TreeMap`(연산 log n) |
| 여러 스레드 | [[동시성 컬렉션]] | `ConcurrentHashMap`, 읽기 위주의 작은 목록은 `CopyOnWriteArrayList` |

### ArrayList

배열 하나(`elementData`)에 원소를 담는다. 자리가 모자라면 더 큰 배열을 만들어 복사한다.

- 지금 구현은 `grow()`에서 `ArraysSupport.newLength(oldCapacity, minCapacity - oldCapacity, oldCapacity >> 1)`로 새 크기를 정한다. 기존 크기의 절반만큼 늘리므로 약 1.5배다. 복사는 `Arrays.copyOf`다.
- 기본 생성자는 빈 배열 상수(`DEFAULTCAPACITY_EMPTY_ELEMENTDATA`)로 시작하고, 첫 `add` 때 `DEFAULT_CAPACITY = 10`짜리 배열을 만든다. 할당을 첫 추가까지 미룬다.
- 1.5배는 명세가 아니다. Javadoc: "The details of the growth policy are not specified beyond the fact that adding an element has constant amortized time cost." 면접에서 1.5배를 말한다면 구현 세부라고 덧붙이는 것이 정확하다.
- 크기를 미리 알면 `new ArrayList<>(n)`이나 `ensureCapacity(n)`로 복사를 줄인다.

[OpenJDK master `ArrayList.java`, JDK 25 Javadoc, 2026-09-27 확인]

### LinkedList

"Doubly-linked list implementation of the `List` and `Deque` interfaces."(Javadoc) 노드는 `item` · `next` · `prev`를 갖는다. 자료(Q33)의 설명은 맞다.

「LinkedList는 삽입·삭제가 빠르다」(자료 Q34)는 노드를 이미 쥐고 있을 때만 성립한다. `add(index, e)`나 `remove(index)`는 먼저 `node(index)`로 그 위치까지 순회해야 하므로 O(n)이다. Javadoc: "Operations that index into the list will traverse the list from the beginning or the end, whichever is closer to the specified index." 노드마다 객체 하나와 참조 두 개를 더 쓰고 메모리에 흩어져 있어 캐시에도 불리하다. 이 성능 설명은 위키가 보충했다. ArrayList Javadoc도 "The constant factor is low compared to that for the `LinkedList` implementation"이라고 적는다.

양 끝 삽입·삭제에는 `ArrayDeque`가 낫다. ArrayDeque Javadoc: "This class is likely to be faster than `Stack` when used as a stack, and faster than `LinkedList` when used as a queue." LinkedList를 쓴 Joshua Bloch 자신이 "Does anyone actually use LinkedList? I wrote it, and I never use it."이라고 쓴 트윗이 있다(2015-04, 2차 자료, https://x.com/joshbloch/status/583813919019573248).

### Queue와 Stack

- Queue는 FIFO를 강제하지 않는다. Javadoc: "Queues typically, but do not necessarily, order elements in a FIFO (first-in-first-out) manner. Among the exceptions are priority queues…" 자료(Q36)의 「Queue는 FIFO」는 일반적인 경우다.
- `Stack extends Vector`다. Javadoc: "A more complete and consistent set of LIFO stack operations is provided by the `Deque` interface and its implementations, which should be used in preference to this class. For example: `Deque<Integer> stack = new ArrayDeque<Integer>();`"

### Set과 Map의 순서

자료(Q37)는 Set이 「요소의 저장 순서를 유지하지 않는다」고 하면서 같은 답에 LinkedHashSet과 TreeSet을 든다. 순서를 보장하지 않는 것은 HashSet뿐이다. HashSet Javadoc: "It makes no guarantees as to the iteration order of the set". LinkedHashSet은 삽입 순서를, TreeSet은 정렬 순서를 따른다. Map도 같다. HashMap은 순서가 없고, LinkedHashMap은 삽입 순서(또는 접근 순서), TreeMap은 키 정렬 순서다.

Map이 「키로 상수 시간에 찾는다」(자료 Q39)는 HashMap, 그것도 해시가 고르게 퍼질 때만이다. TreeMap Javadoc은 "guaranteed log(n) time cost for the containsKey, get, put and remove operations"라고 적는다. 자료가 쓴 「HashTable」은 클래스 이름이 `Hashtable`이다.

## 레거시 클래스

`Vector` · `Stack` · `Hashtable`은 JDK 1.0부터 있던 클래스로, 1.2에서 컬렉션 프레임워크에 끼워 넣어졌다. 셋 다 메서드마다 `synchronized`가 붙어 있다. Vector Javadoc: "If a thread-safe implementation is not needed, it is recommended to use `ArrayList` in place of `Vector`." 락 하나로 감싸는 방식의 한계와 대안(`Collections.synchronizedList` · `CopyOnWriteArrayList` · `ConcurrentHashMap`)은 [[동시성 컬렉션]]에 있다.

## Iterator

- `Iterable`은 `iterator()` 하나를 추상 메서드로 갖고, JDK 8부터 `forEach`를 default 메서드로 갖는다.
- `Iterator`의 추상 메서드는 `hasNext()`와 `next()`다. `remove()`는 JDK 8부터 default 메서드이고, `@implSpec`은 "The default implementation throws an instance of UnsupportedOperationException and performs no other action."이다. 자료(Q43)처럼 세 메서드를 나란히 두면 `remove`가 늘 쓸 수 있는 것처럼 들린다. `List.of`가 돌려주는 불변 리스트의 이터레이터에서 `remove`를 부르면 `UnsupportedOperationException`이 난다([[불변 객체]]).
- for-each 도중 컬렉션을 직접 고치면 ArrayList · HashMap 같은 일반 컬렉션의 fail-fast 이터레이터가 `ConcurrentModificationException`을 던진다. 순회하며 지우려면 `Iterator.remove()`나 `Collection.removeIf`를 쓴다.

## Collection과 Collections

`Collection`은 인터페이스, `Collections`는 정적 메서드만 모은 유틸리티 클래스다. Javadoc: "This class consists exclusively of static methods that operate on or return collections." 정렬(`sort`), 이진 검색(`binarySearch`), 래퍼(`synchronizedList` · `unmodifiableList`) 등이 있다. 자료(Q44)의 설명은 맞다. 자료 Q42가 「Collections.remove(Object o)」라고 쓴 것은 `Collection.remove`의 오타다.

## 면접에서

1. 계층(Q29)을 물으면 Iterable → Collection → List · Set · Queue(Deque)와 별개의 Map을 그리고, JDK 21의 Sequenced 인터페이스를 덧붙이면 최신 지식을 보여 줄 수 있다.
2. ArrayList의 성장(Q32)은 「약 1.5배로 늘려 복사한다, 다만 명세는 상각 O(1)만 약속한다」로 답한다.
3. ArrayList와 LinkedList(Q34)는 「LinkedList는 삽입이 빠르다」로 끝내지 않는다. 위치를 찾는 순회가 O(n)이고, 큐·스택에는 ArrayDeque를 쓴다고 말한다.
4. Map이 Collection이 아닌 이유(Q42)는 설계 FAQ의 논거(요소가 키-값 쌍이면 키로 값을 묻지 못하는 빈약한 추상화)로 답한다.

## 자료의 서술과 정정

판정 전체는 [[Java 면접 기타 빈출 질문 4 JCF]]에 있다. 이 페이지가 정정을 맡은 것만 모았다.

| 자료 | 판정 | 정정 |
|---|---|---|
| Collection은 List · Queue · Set으로 (Q29) | 단서 필요 | Iterable, Deque, Sorted/Navigable, Sequenced(JDK 21) |
| List를 「상속」 (Q30) | 단서 필요 | 구현(implements) |
| capacity를 넘으면 늘린다 (Q32) | 단서 필요 | 약 1.5배 · 지연 할당은 구현, 명세는 상각 상수 시간 |
| LinkedList는 삽입·삭제가 빠르다, Queue는 LinkedList (Q34 · Q36) | 단서 필요 | 위치 지정은 O(n) 순회, 큐·스택은 ArrayDeque, Queue는 FIFO를 강제하지 않는다 |
| Set은 저장 순서를 유지하지 않는다 (Q37) | 틀림 | HashSet만. LinkedHashSet은 삽입 순서, TreeSet은 정렬 |
| Map은 상수 시간, HashTable (Q39) | 단서 필요 | TreeMap은 log n, 이름은 `Hashtable` |
| Map은 요소가 모호하고 remove 인자가 다르다 (Q42) | 단서 필요 | 결론은 FAQ와 같고 논거가 다르다 |
| Iterator의 remove (Q43) | 단서 필요 | default 메서드, 기본 구현은 `UnsupportedOperationException` |

근거 (2026-09-27 확인): OpenJDK `openjdk/jdk` master의 `java/util/{Collection,List,Queue,Deque,SortedSet,ArrayList,LinkedList,ArrayDeque,Stack,Vector,HashSet,TreeMap,Iterator,Collections}.java`와 `java/lang/Iterable.java`, JDK 25 Javadoc, JEP 431, 「Java Collections API Design FAQ」 JDK 25판.

## 관련

- [[HashMap]]: 해시 기반 Map · Set의 내부, 충돌과 트리화
- [[equals와 hashCode]]: 해시 컬렉션이 기대는 계약
- [[동시성 컬렉션]]: Vector · Hashtable · synchronized 래퍼와 `java.util.concurrent`
- [[불변 객체]]: `List.of` 같은 불변 컬렉션
- [[JDK 개선 제안]]: JEP 431을 읽는 법
- 자료: [[Java 면접 기타 빈출 질문 4 JCF]]

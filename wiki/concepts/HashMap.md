---
type: concept
title: HashMap
aliases: [해시맵, Java HashMap, 해시 충돌, Hash collision, 트리화, Treeify]
tags: [Java, 컬렉션, 자료구조, 해시, 면접]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "[[Java 면접 기타 빈출 질문 4 JCF]]"
---

# HashMap

`java.util.HashMap`은 해시 테이블로 구현한 Map이다. 키의 `hashCode()`로 버킷을 고르고, 같은 버킷 안에서는 `equals()`로 키를 찾는다. `HashSet`도 속은 HashMap이다. 면접에서는 동작 원리, 해시 충돌, 최악 시간 복잡도를 묻는다([[Java 면접 기타 빈출 질문 4 JCF]] Q38 · Q40 · Q41). 이 페이지는 JDK 8 이후 구현(JDK 25 소스)을 기준으로 한다. 컬렉션 전체에서의 자리는 [[Java 컬렉션 프레임워크]]에 있다.

## 해시 값과 버킷 인덱스

자료(Q40)는 「해시 함수로 키를 인덱스로 바꾸고, 이 인덱스를 해시 값이라 부른다」고 한다. HashMap 안에서 둘은 다른 값이다.

1. 키의 `hashCode()`를 부른다. 32비트 `int`다.
2. `hash()`가 상위 16비트를 하위 16비트에 XOR로 섞는다: `(h = key.hashCode()) ^ (h >>> 16)`. null 키의 해시는 0이다. 테이블이 작으면 인덱스에 하위 비트만 쓰이므로, 상위 비트도 인덱스에 영향을 주게 하려는 것이다(소스 주석: "to incorporate impact of the highest bits that would otherwise never be used in index calculations because of table bounds").
3. 버킷 인덱스는 `(n - 1) & hash`다. 테이블 크기 `n`이 늘 2의 거듭제곱이라 나머지 연산 대신 비트 AND를 쓴다.

노드는 이 섞은 해시(`hash` 필드)를 저장해 두고, 비교와 리사이즈에 다시 쓴다.

## 넣기와 찾기

`putVal`의 비교 조건은 이렇다.

```java
p.hash == hash && ((k = p.key) == key || (key != null && key.equals(k)))
```

같은 버킷의 노드만 본다. 저장된 해시가 같고, 참조가 같거나 `equals`가 참이면 같은 키로 보고 값을 바꾼다. 아니면 버킷 끝에 새 노드를 붙인다. 해시를 먼저 비교하는 것은 비싼 `equals` 호출을 줄이기 위해서다.

그래서 `equals`를 재정의하고 `hashCode`를 재정의하지 않으면, 동등한 두 키가 대개 다른 버킷으로 가서 `equals`가 불리지도 않는다. 이 계약은 [[equals와 hashCode]]에 있다.

`HashSet.add(e)`는 `map.put(e, PRESENT) == null`이다(`PRESENT`는 더미 값). 자료(Q38)가 설명하는 Set의 중복 제거가 곧 위 조건이다. 자료는 「hashCode()는 객체의 주소를 가져와서 같은 객체인지 확인한다」고 하는데, 비교하는 것은 주소가 아니라 섞은 해시이고, 그 대상도 저장된 모든 해시가 아니라 같은 버킷의 노드뿐이다. `equals`가 참이라는 것은 같은 객체가 아니라 동등한 객체라는 뜻이다.

## 해시 충돌

다른 키가 같은 버킷에 모이는 것이 해시 충돌이다. `hashCode`가 같으면 당연히 충돌하고, 달라도 `(n - 1) & hash`가 같으면 충돌한다. 아래 코드는 `"Aa"`와 `"BB"`의 `hashCode`가 같아 같은 버킷에 들어가도 둘 다 제대로 저장된다는 것을 보인다.

```java
import java.util.HashMap;
import java.util.Map;

public class Collide {
    static int spread(Object key) {
        int h = key.hashCode();
        return h ^ (h >>> 16);
    }

    public static void main(String[] args) {
        System.out.println("Aa".hashCode() + " " + "BB".hashCode());
        System.out.println(((16 - 1) & spread("Aa")) + " " + ((16 - 1) & spread("BB")));

        Map<String, Integer> map = new HashMap<>();
        map.put("Aa", 1);
        map.put("BB", 2);
        System.out.println(map.get("Aa") + " " + map.get("BB") + " " + map.size());
    }
}
```

JDK 25.0.2에서 적힌 그대로 컴파일해 실행한 결과다.

```
2112 2112
0 0
1 2 2
```

`spread`는 HashMap의 `hash()`를 흉내 낸 것이고, 16은 기본 테이블 크기다. 해시가 같으니 버킷도 같고(0번), 같은 버킷 안에서 `equals`로 구분되므로 두 값 모두 찾는다.

HashMap은 충돌을 체이닝으로 푼다. 버킷마다 노드의 연결 리스트를 두고 뒤에 붙인다(개방 주소법이 아니다).

## 트리화와 최악 시간 복잡도

자료(Q41)는 「한 버킷에 모두 충돌하면 O(N)」이라고 한다. JDK 7까지는 맞았다. JDK 8의 JEP 180 「Handle Frequent HashMap Collisions with Balanced Trees」가 바꿨다: "once the number of items in a hash bucket grows beyond a certain threshold, that bucket will switch from using a linked list of entries to a balanced tree. In the case of high hash collisions, this will improve worst-case performance from O(n) to O(log n)."

| 상수 | 값 | 뜻 |
|---|---|---|
| `TREEIFY_THRESHOLD` | 8 | 노드가 이만큼 있는 버킷에 하나를 더 넣을 때(9번째) 트리로 바꾼다. 소스 주석: "Bins are converted to trees when adding an element to a bin with at least this many nodes." |
| `MIN_TREEIFY_CAPACITY` | 64 | 테이블이 이보다 작으면 트리로 바꾸지 않고 리사이즈만 한다 |
| `UNTREEIFY_THRESHOLD` | 6 | 리사이즈로 나뉜 트리 버킷이 이만큼 이하가 되면 연결 리스트로 되돌린다 |

트리는 레드블랙 트리(`TreeNode`)이고, 노드를 해시 값 순으로 놓는다. 해시가 같으면 키가 같은 클래스의 `Comparable`일 때 `compareTo`로 가른다.

**해시가 같고 `Comparable`도 아닌 키는 트리화 뒤에도 최악이 O(n)이다.** 조회할 때 방향을 정할 수 없으면 `TreeNode.find`가 양쪽 서브트리를 다 뒤진다. 삽입 때 쓰는 `tieBreakOrder`는 "a consistent insertion rule"일 뿐 조회에는 쓰이지 않는다. 소스 주석도 이 경우를 인정한다: "worst-case O(log n) operations when keys either have distinct hashes or are orderable … (If neither of these apply, we may waste about a factor of two in time and space compared to taking no precautions. …)" 그러니 정확한 답은 「JDK 8부터 충돌이 몰린 버킷은 트리로 바꿔 O(log n)이 된다. 다만 키가 Comparable이어야 하고, 아니면 여전히 O(n)이다」이다. JEP 180도 적용 대상을 "any key type that implements Comparable"로 적는다.

JEP 180이 밝힌 동기는 그 전의 「alternative string-hashing」(String 키에만 듣고 모든 String에 `hash32` 필드를 더한 방식)을 모든 Comparable 키에 듣는 방식으로 바꾸고 걷어 내는 것이다. 같은 변경이 `LinkedHashMap`에도 들어갔고, `Hashtable`은 순회 순서에 기대는 레거시 코드 때문에 제외했다. 충돌을 일부러 일으키는 서비스 거부 공격(같은 해시의 키를 대량으로 보내 체이닝 리스트를 길게 만드는 것)이 이런 대비의 배경으로 흔히 거론되지만, JEP 180 본문은 공격을 언급하지 않는다. 이 연결은 위키가 보충한 것이고 1차 자료로 확인하지 않았다.

## 리사이즈

- 기본 테이블 크기는 16(`DEFAULT_INITIAL_CAPACITY = 1 << 4`), 기본 load factor는 0.75다. 테이블은 첫 `put` 때 만든다.
- 원소 수가 `threshold`(= 크기 × load factor, 기본 12)를 넘으면(`++size > threshold`) 테이블을 2배로 늘린다(`newCap = oldCap << 1`).
- 크기가 2배가 되면 인덱스에 쓰이는 비트가 하나 는다. 그래서 각 노드는 원래 자리 `j`에 남거나 `j + oldCap`으로 옮겨 가고, 어느 쪽인지는 `(e.hash & oldCap) == 0`으로 정한다. 해시를 다시 계산하지 않는다.
- 크기를 미리 알면 `HashMap.newHashMap(n)`(JDK 19+)처럼 load factor를 감안한 크기로 만들어 리사이즈를 피한다. 이 팁은 위키가 보충했다.

[OpenJDK master · JDK 25 `HashMap.java` · `HashSet.java`, JEP 180 https://openjdk.org/jeps/180 , 2026-09-27 확인]

## 스레드 안전

HashMap은 동기화하지 않는다(Javadoc: "unsynchronized and permits nulls"). 여러 스레드가 고치면 데이터를 잃거나 구조가 깨질 수 있다. 대안인 `ConcurrentHashMap`의 버킷 단위 잠금·CAS와 HashMap과의 비교표는 [[동시성 컬렉션]]에 있다. `Hashtable`은 메서드마다 `synchronized`인 레거시 클래스다.

## 면접에서

1. 동작(Q40)은 「hashCode → 상위 비트를 섞은 해시 → `(n - 1) & hash`로 버킷 인덱스 → 같은 버킷 안에서 해시 비교 후 equals」 순서로 말한다. 해시 값과 인덱스를 구분한다.
2. 최악 시간 복잡도(Q41)는 「JDK 7까지 O(n), JDK 8부터 노드가 8개인 버킷에 하나를 더 넣을 때 테이블이 64 이상이면 레드블랙 트리로 바꿔 O(log n)」까지 답하고, Comparable이 아닌 같은 해시 키의 예외를 덧붙이면 꼬리 질문에 막히지 않는다.
3. Set의 중복 제거(Q38)는 HashSet이 HashMap의 키 집합이라는 데서 시작한다. hashCode를 「주소」로 설명하지 않는다.
4. 「왜 크기가 2의 거듭제곱인가」가 꼬리로 올 수 있다. 나머지 대신 비트 AND로 인덱스를 구하고, 리사이즈 때 노드가 두 자리 중 하나로만 가게 하기 위해서다.

## 자료의 서술과 정정

| 자료 | 판정 | 정정 |
|---|---|---|
| hashCode()는 주소를 가져와 같은 객체인지 확인, 같은 해시면 equals (Q38) | 틀림 | 같은 버킷 노드와 섞은 해시를 비교한 뒤 `==` 또는 `equals`. hashCode는 주소가 아니다([[equals와 hashCode]]) |
| 키를 인덱스로 바꾸고 이 인덱스를 해시 값이라 부른다 (Q40) | 틀림 | 해시 값은 `hashCode() ^ (h >>> 16)`, 인덱스는 `(n - 1) & hash` |
| 체이닝으로 해결, 한 버킷에 모두 충돌하면 O(N) (Q41) | 낡음 | JDK 8 트리화로 O(log n). Comparable이 아닌 같은 해시 키는 여전히 O(n) |

## 관련

- [[Java 컬렉션 프레임워크]]: HashSet · LinkedHashMap · TreeMap과의 선택
- [[equals와 hashCode]]: HashMap이 기대는 계약
- [[동시성 컬렉션]]: ConcurrentHashMap과 비교
- [[JDK 개선 제안]]: JEP 180을 읽는 법
- 자료: [[Java 면접 기타 빈출 질문 4 JCF]]

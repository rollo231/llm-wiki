---
type: concept
title: JIT 컴파일
aliases: [JIT, JIT 컴파일러, Just-In-Time compilation, 코드 캐시, Code cache, JVM 워밍업, C1, C2, 계층형 컴파일, Tiered compilation, 역최적화, Deoptimization, Graal]
tags: [Java, JVM, 성능, 면접]
created: 2026-09-26
updated: 2026-09-26
sources:
  - "[[Java 면접 2 JVM과 실행 원리]]"
---

# JIT 컴파일

[[JVM]]은 바이트코드를 처음에는 **인터프리터**로 한 줄씩 실행한다. 그러다 자주 실행되는 코드("hot" 코드)를 **런타임에
기계어로 컴파일**해 **코드 캐시**에 넣고, 이후로는 그 기계어를 실행한다. 이것이 Just-In-Time 컴파일이다.

DE 어휘로 옮기면 **런타임 프로파일에 따른 지연 materialization**에 가깝다. 모든 쿼리 결과를 미리 만들어 두지 않고, 자주
조회되는 것만 캐시에 굳힌다. 캐시가 차가울 때 느린 것도 같다. *(위키의 연결)*

## 계층형 컴파일 (C1 · C2)

HotSpot은 두 JIT 컴파일러를 단계적으로 쓴다(tiered compilation). **C1**(client compiler)은 컴파일이 빠르고 최적화가 가볍다.
**C2**(server compiler)는 컴파일이 느리지만 프로파일을 근거로 공격적으로 최적화한다. 계층형 컴파일은 Java SE 7에서 들어왔고
**JDK 8(hs25)부터 기본**이다. 그전에는 `-client`(C1)와 `-server`(C2) 가운데 하나를 골라 썼다.

실행 단계(level)는 다섯 개다.

| 단계 | 누가 | 무엇 |
|---|---|---|
| tier 0 | 인터프리터 | 실행하면서 호출 수·루프 반복 수를 센다(프로파일은 MDO에 쌓인다) |
| tier 1 | C1 | 최적화는 하되 프로파일은 수집하지 않는다. **사소한(trivial) 메서드**의 종착점 |
| tier 2 | C1 | 호출·back-edge 카운터만 붙인다. **C2 큐가 밀렸을 때** 거치는 단계 |
| tier 3 | C1 | 프로파일을 모두 수집하는 코드를 붙인다 |
| tier 4 | C2 | C1이 모은 프로파일로 공격적으로 최적화한다(인라이닝, 탈가상화 등) |

- **보통 경로는 0 → 3 → 4다.** 프로파일 수집 코드가 붙은 tier 3은 tier 2보다 약 30% 느리다. 그래서 필요한 만큼만 머문다.
- **tier 2는 C2가 바쁠 때 쓴다.** C2 큐가 길 때 tier 3으로 가면 C2 차례가 올 때까지 느린 코드에 묶인다. 그래서 먼저 tier 2로
  가고, C2 부하가 줄면 tier 3으로 다시 컴파일해 프로파일을 모은다.
- **tier 1은 첫 C1 컴파일 뒤에 정해진다.** 블록 수·루프 수를 보고 C2로 가도 C1과 같은 코드가 나올 사소한 메서드라고 판단하면,
  tier 4 대신 tier 1로 컴파일하고 끝낸다.

[HotSpot `compilationPolicy.hpp` 주석 ; Oracle, *Java HotSpot VM Performance Enhancements*,
https://docs.oracle.com/javase/8/docs/technotes/guides/vm/performance-enhancements-7.html ; JDK-8008938, https://bugs.openjdk.org/browse/JDK-8008938 ;
2026-09-26 확인]

**무엇을 "자주"로 보나.** 호출 수 i와 루프 back-edge 수 b를 **함께** 본다. JDK 25 기본값은 다음과 같다.

- tier 3 진입: `i > 200`, 또는 `i > 100` 이면서 `i + b > 2000`
- tier 4 진입: `i > 5000`, 또는 `i > 600` 이면서 `i + b > 15000`
- 루프 도중에 컴파일된 코드로 갈아타는 OSR은 back-edge 임계치(tier 3 60000, tier 4 40000)로 따로 판정한다.
- 임계치는 컴파일 큐 길이에 따라 동적으로 조정된다.

[HotSpot `compilationPolicy.hpp` 주석, https://github.com/openjdk/jdk/blob/master/src/hotspot/share/compiler/compilationPolicy.hpp ;
JDK 25 `-XX:+PrintFlagsFinal`, 2026-09-26 확인]

## 역최적화 (deoptimization)

C2가 빠른 이유는 **추측**이다. 호출 지점의 타입 프로파일이 한쪽으로 쏠려 있으면, 가장 흔했던 타입(한두 개)을 가정하는 검사를
넣고 그 타입의 메서드를 인라인한다. 사실상 단형(monomorphic)인 호출은 통째로 인라인된다. 클래스 계층 분석(CHA)으로 "이 클래스는
하위 클래스가 없다"거나 "이 메서드는 재정의가 없다"고 가정할 때도 있다. 이런 가정은 검사할 수 있는 **의존성**으로 등록해 둔다.

가정이 깨지면 역최적화한다. 최적화된 스택 프레임을 최적화 안 된 프레임으로 바꾸고, 잘못된 추측이 들어간 코드를 버린다.

- **예상 못 한 타입이 들어오면** 그 호출 지점이나 캐스트에서 역최적화한다. 경우에 따라서는 역최적화하지 않고 느린 vtable/itable
  호출로 처리한다.
- **새 클래스가 로드되어 CHA 가정이 깨지면** 영향을 받는 메서드를 실행 중인 모든 스레드를 safepoint로 멈추고 역최적화한다.

그래서 C2의 최적화는 공격적이면서도 의미상으로 안전하다. 대신 역최적화가 잦으면 컴파일과 버리기가 반복되어 성능이 떨어진다.

[OpenJDK Wiki, *HotSpot PerformanceTechniques*, https://wiki.openjdk.org/display/HotSpot/PerformanceTechniques , 2026-09-26 확인]

## Graal JIT

Graal은 **Java로 작성한 JIT 컴파일러**다. JDK 9의 JVMCI(JVM 컴파일러 인터페이스)로 HotSpot에 붙는다. JDK 10에서 실험 기능으로
들어왔고(JEP 317, Linux/x64 한정, `-XX:+UnlockExperimentalVMOptions -XX:+UseJVMCICompiler`), JDK 17에서 OpenJDK에서 제거됐다
(JEP 410). 지금은 GraalVM 배포판에서 쓴다. JDK 9의 실험적 AOT 컴파일러(`jaotc`, 역시 JEP 410에서 제거)도 Graal을 바탕으로 했다.

[JEP 317, https://openjdk.org/jeps/317 ; JEP 410, https://openjdk.org/jeps/410 ; 2026-09-26 확인]

## 코드 캐시가 꽉 차면

- JVM은 "CodeCache is full. Compiler has been disabled." 경고를 내고 JIT를 멈춘다. 새로 hot해진 코드는 인터프리터로 돈다.
  이미 컴파일된 코드는 계속 실행된다.
- `UseCodeCacheFlushing`이 기본으로 켜져 있어 JVM이 차가운 코드를 치워 공간을 회수하려 한다. 회수되면 컴파일이 재개될 수 있다.
  JDK 20에서 별도 sweeper가 제거되어 지금은 GC가 이 정리를 맡는다(JDK-8290025).
- JDK 9부터 코드 캐시는 세그먼트(비메서드·프로파일된·프로파일 안 된 코드)로 나뉜다(JEP 197).
- `ReservedCodeCacheSize` 기본값은 tiered일 때 240MB다.

[JEP 197 Segmented Code Cache, https://openjdk.org/jeps/197 ; JDK-8290025, https://bugs.openjdk.org/browse/JDK-8290025 ;
JDK 25 플래그, 2026-09-26 확인]

## 콜드 스타트와 워밍업

배포 직후 인스턴스가 느린 이유는 여러 겹이다.

1. 코드 캐시가 비어 모든 코드가 인터프리터로 돈다.
2. 클래스 로딩·링킹·검증 비용이 든다([[클래스 로딩]]). Spring 같은 프레임워크는 컨텍스트 초기화 비용도 크다.
3. JIT 컴파일 스레드가 요청 처리와 CPU를 나눠 쓴다.

해법은 두 갈래다.

| 방법 | 무엇 | 도입 |
|---|---|---|
| **워밍업** | 트래픽을 받기 전에 주요 경로를 미리 호출해 JIT를 돌린다. readiness probe를 워밍업 뒤에 통과시킨다 | 애플리케이션이 직접 |
| CDS / AppCDS | 클래스 메타데이터를 아카이브해 로딩을 줄인다 | CDS는 JDK 5부터. 앱 클래스까지 넓힌 AppCDS 공개는 JDK 10 (JEP 310) |
| AOT Class Loading & Linking | 이전 실행에서 로딩·링킹된 클래스를 캐시로 재사용 | JDK 24 (JEP 483) |
| AOT Method Profiling | 이전 실행의 메서드 프로파일을 캐시에 넣어 JIT가 바로 최적화 | JDK 25 (JEP 515) |
| CRaC | 워밍업이 끝난 프로세스를 체크포인트로 떠 두고 복원 | OpenJDK 프로젝트, 일부 배포판 지원 |
| GraalVM Native Image | 빌드 시점에 전부 기계어로 AOT 컴파일. 시작은 빠르지만 피크 성능·동적 기능에 제약 | GraalVM |

[JEP 483, https://openjdk.org/jeps/483 ; JEP 515, https://openjdk.org/jeps/515 ; 2026-09-26 확인]

**배포 전략과 이어진다.** 롤링 배포나 오토스케일로 뜬 새 인스턴스가 차가운 채 트래픽을 받으면 p99 지연이 튄다. 워밍업은
[[지연 시간과 처리량]]의 꼬리 지연 문제다. *(위키의 연결)*

## 면접에서

자료의 Gold 답([[Java 면접 2 JVM과 실행 원리]] Q2-2~Q2-4)보다 나은 뼈대:

- **판단 기준** — "호출 횟수와 루프 반복 횟수를 합쳐 셉니다. C1이 약 2,000, C2가 약 15,000 근처에서 컴파일하고, C2는 C1이 모은
  프로파일을 보고 최적화합니다. 루프 안에서는 OSR로 도중에 갈아탑니다."
- **코드 캐시** — "새 코드는 인터프리터로 돌지만, 기본 설정이면 JVM이 캐시를 비워 공간을 회수하려 합니다. 운영에서는
  경고 로그를 보고 `ReservedCodeCacheSize`를 조정합니다."
- **콜드 스타트** — "JIT만이 아니라 클래스 로딩·프레임워크 초기화도 원인입니다. 워밍업 후 readiness를 열고, 필요하면 CDS나
  JDK 24+ AOT 캐시로 시작 비용을 줄입니다."

## 자료의 서술과 정정

| 자료 | 판정 | 정정 |
|---|---|---|
| JIT는 "메서드 호출 횟수"로 판단 (p16) | 단서 필요 | 숫자(2,000·15,000)는 맞지만 back-edge도 함께 센다. OSR은 따로 판정 |
| 코드 캐시가 꽉 차면 인터프리터로 (p19) | 단서 필요 | flushing으로 회수·재개 가능. JDK 9 세그먼트 구조 |
| 초기 요청이 느린 이유 = 빈 코드 캐시, 해법 = 워밍업 (p22) | 단서 필요 | 클래스 로딩·초기화 비용이 빠졌고, CDS·AOT 캐시·CRaC·Native Image 같은 해법이 없다 |

## 관련

- [[JVM]] · [[가비지 컬렉션]] · [[지연 시간과 처리량]]
- 자료: [[Java 면접 2 JVM과 실행 원리]]

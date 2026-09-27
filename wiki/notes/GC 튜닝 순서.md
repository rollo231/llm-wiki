---
type: note
title: GC 튜닝 순서
aliases: [GC tuning, GC 튜닝, G1 튜닝, JVM 튜닝 순서]
tags: [Java, JVM, GC, 성능, 운영, 면접]
created: 2026-09-27
updated: 2026-09-27
sources:
  - "[[Java 면접 3 GC]]"
---

# GC 튜닝 순서

「GC 튜닝은 어떤 순서로 하나」 질의에서 나온 절차 종합. 뼈대는 Oracle GC 튜닝 가이드(JDK 25)의 권장이고, 위키의 여러 페이지를
한 흐름으로 묶었다. 원칙은 **기본값에서 시작해, 큰 손잡이부터, 하나씩**이다.

```
0 목표·기준선 → 1 코드 → 2 기본값 + 힙 크기 → 3 컬렉터 선택 → 4 목표 하나 → 5 증상별 튜닝 → 6 재측정
```

## 0. 목표를 정하고 기준선을 잰다

우선할 것 하나를 고른다: **지연**(p99, 최대 멈춤), **처리량**(앱이 일한 시간 비율), **메모리**(힙·컨테이너 크기). 셋은 부딪친다.
"The pressure to achieve a throughput goal (which may require a larger heap) competes with the goals for a maximum pause-time and a
minimum footprint (which both may require a small heap)." [Oracle GC Tuning Guide JDK 25, Ergonomics,
https://docs.oracle.com/en/java/javase/25/gctuning/ergonomics.html , 2026-09-27 확인] → [[지연 시간과 처리량]]

바꾸기 전에 GC 로그(`-Xlog:gc*`)로 기준선을 남긴다. 무엇을 보는지는 [[가비지 컬렉션]] 모니터링 절.

## 1. 코드 문제를 먼저 치운다

튜닝은 누수를 고치지 못한다. GC 후 바닥선이 계속 오르면 코드 문제다. 할당량 자체를 줄이는 것이 어떤 옵션보다 효과가 크다.
→ [[객체 수명과 메모리 상한]] (바닥선의 네 모양, 안티패턴). *(이 단계를 맨 앞에 둔 것은 위키의 판단 — Oracle 가이드는 옵션의 순서만 다룬다)*

## 2. 기본값으로 돌리고 힙 크기만 조정한다

"Unless your application has rather strict pause-time requirements, first run your application and allow the VM to select a
collector. If necessary, adjust the heap size to improve performance."

- 첫 손잡이는 `-Xmx`(필요하면 `-Xms`).
- **다른 컬렉터에서 G1로 옮길 때는 GC 옵션을 모두 지운다**: "start by removing all options that affect garbage collection, and only
  set the pause-time goal and overall heap size by using `-Xmx` and optionally `-Xms`."

[Oracle GC Tuning Guide JDK 25, Available Collectors — Selecting a Collector,
https://docs.oracle.com/en/java/javase/25/gctuning/available-collectors.html ; G1 Tuning — Moving to G1 from Other Collectors,
https://docs.oracle.com/en/java/javase/25/gctuning/garbage-first-garbage-collector-tuning.html , 2026-09-27 확인]

## 3. 그래도 모자라면 목표에 맞는 컬렉터를 고른다

| 상황 | 컬렉터 |
|---|---|
| 데이터가 작다(약 100MB까지), 또는 CPU 하나에 멈춤 요구 없음 | Serial |
| 최고 성능이 최우선이고 멈춤 요구가 없거나 1초 이상 멈춤도 괜찮다 | VM에 맡기거나 Parallel |
| 처리량보다 응답 시간이 중요하고 멈춤을 짧게 해야 한다 | G1 |
| 응답 시간이 최우선이다 | ZGC |

가이드도 이것은 **출발점**일 뿐이라고 한다. 성능은 힙 크기, 살아 있는 데이터 양, CPU 수와 속도에 달려 있다. 맞지 않으면 먼저 힙과
세대 크기를 조정하고, 그래도 안 되면 다른 컬렉터를 시도한다. [Available Collectors — Selecting a Collector] 컬렉터별 특징은
[[가비지 컬렉터]].

## 4. 컬렉터에게 목표 하나만 준다 (G1)

- 일반 권장: "use G1 with its default settings, eventually giving it a different pause-time goal and setting a maximum Java heap size
  by using `-Xmx` if desired." 처리량을 원하면 멈춤 목표를 느슨하게 하거나 힙을 키우고, 지연을 원하면 멈춤 목표를 조인다.
- ⚠️ **Young 크기를 고정하지 않는다.** "Avoid limiting the young generation size to particular values by using options like `-Xmn`,
  `-XX:NewRatio` and others because the young generation size is the main means for G1 to allow it to meet the pause-time."
  "Setting the young generation size to a single value overrides and practically disables pause-time control."
  `NewRatio=2`(Old:Young = 2:1, JDK 25 기본값) 같은 고정 비율 감각은 Serial·Parallel의 것이다.

[G1 Tuning — General Recommendations for G1, 같은 URL, 2026-09-27 확인]

## 5. 로그로 확인된 증상만 튜닝한다 (G1)

| 증상 | 로그에서 보는 것 | 가이드가 드는 손잡이 |
|---|---|---|
| **Full GC** | `Pause Full (G1 Compaction Pause)`. 대개 앞에 Allocation 이유의 evacuation failure가 있다 | 동시 마킹이 제때 끝나게 한다: Old 할당 줄이기, 힙 키우기, `-XX:ConcGCThreads` 늘리기, 마킹을 일찍 시작(`-XX:G1ReservePercent` 올리기, 또는 `-XX:-G1UseAdaptiveIHOP` + `-XX:InitiatingHeapOccupancyPercent`) |
| Full GC의 원인이 `System.gc()` | GC 원인 | 코드를 못 고치면 `-XX:+ExplicitGCInvokesConcurrent` 또는 `-XX:+DisableExplicitGC` |
| **Humongous가 많다** | `gc+heap=info`의 `Humongous regions: X->Y`가 Old Region 수에 비해 크다 | `-XX:G1HeapRegionSize`를 키우거나 힙을 키운다. 극단적이면 Humongous 할당 자체를 줄인다 (→ [[가비지 컬렉터]] Humongous) |
| **멈춤 중 Sys 시간이 크다** | `gc+cpu=info`의 `User= Sys= Real=` | `-Xms` = `-Xmx` + `-XX:+AlwaysPreTouch`, Linux THP 끄기, 로그 디스크 분리나 `-Xlog:async` |
| Real이 User+Sys보다 훨씬 크다 | 같은 줄 | 머신 과부하로 VM이 CPU를 못 받았다 |
| **Reference 처리가 길다** | Reference Processing 단계 | `-XX:ReferencesPerThread`, `-XX:ParallelRefProcEnabled` |
| **Young GC가 길다** | Evacuate Collection Set, 특히 Object Copy | `-XX:G1NewSizePercent`를 낮춘다. 생존 객체가 갑자기 늘어 튄다면 `-XX:G1MaxNewSizePercent`를 낮춘다 |
| **Mixed GC가 길다** | `gc+ergo+cset=debug`의 예측 시간(young · old) | `-XX:G1MixedGCCountTarget`을 올려 여러 번에 나눈다, `-XX:G1MixedGCLiveThresholdPercent`로 비싼 Region을 후보에서 뺀다 |

Young GC 시간은 대략 Young 크기, 더 정확히는 **복사해야 할 산 객체 수**에 비례한다는 것이 가이드의 설명이다([[가비지 컬렉션]]의
「Minor GC 비용은 산 객체 수에 비례」와 같다).

[G1 Tuning — Observing Full Garbage Collections · Humongous Object Fragmentation · Tuning for Latency, 같은 URL, 2026-09-27 확인]

## 6. 하나씩 바꾸고 다시 잰다

옵션을 한꺼번에 바꾸면 무엇이 효과였는지 알 수 없다. 0단계 기준선과 비교하고, 효과 없는 옵션은 되돌린다. *(운영 통념)*

## 면접에서

「먼저 지연·처리량·메모리 중 목표를 정하고 GC 로그로 기준선을 잽니다. 누수나 과다 할당은 튜닝이 아니라 코드로 고칩니다. 그다음은
기본값에 `-Xmx`만 두고, 부족하면 목표에 맞는 컬렉터를 고릅니다. G1이라면 멈춤 목표 하나만 주고 `-Xmn`처럼 Young 크기를 고정하지
않습니다. 그래도 남는 증상은 로그로 확인한 것만, 한 번에 하나씩 바꿔 봅니다.」

## 관련

- [[가비지 컬렉터]] · [[가비지 컬렉션]] · [[객체 수명과 메모리 상한]] · [[지연 시간과 처리량]] · [[Java 8에서 11로 가는 GC 관점의 이유]]
- 자료: [[Java 면접 3 GC]]

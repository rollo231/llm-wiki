---
type: source
title: AI DE 강의 4-02 CAP 정리와 분산 시스템의 한계
aliases: [AI DE 4-02]
tags: [AI-DE-강의, 분산, 정합성]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf"
---

# AI DE 강의 4-02 CAP 정리와 분산 시스템의 한계

[[AI 데이터 엔지니어링 강의]] Part 4 Ch1의 세 번째 소단원이다. 분산 처리가 본질적으로 어려운 이유를 CAP 정리와 세 가지 근본 한계(부분 실패, 전역 시계 부재, FLP)로 설명한다. Part 3의 [[AI DE 강의 3-02 RDBMS의 한계와 NoSQL]]이 한 슬라이드로 지나간 CAP를 소단원 하나로 다시 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch1. 분산처리의 필요성과 주의사항: 3. CAP 정리와 분산시스템의 근본적 한계 |
| 원본 파일 | `part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` p32–50 (19p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch1~4`, 소단원 번호 `3`은 표지 슬라이드 |

## 요약

### 01. CAP 이론 (p34–37)

- 분산 처리의 근본 한계(p34). 일부 노드만 실패할 수 있고, 네트워크는 지연되거나 끊기고, 모든 노드가 같은 "현재"를 공유하지 않고, 노드마다 본 상태가 순간적으로 다를 수 있다.
- CAP는 만능 법칙이 아니라 "네트워크 분할이 가능한 환경에서 읽기/쓰기 서비스가 어디까지 강한 보장을 할 수 있는가"를 묻는 정리다(p36).
- 2000년 Brewer의 제안. 일관성은 안전성(safety), 가용성은 생명성(liveness) 성질이다(p37).

### 02~04. C, A, P (p38–40)

- Consistency: single-copy consistency. 모든 클라이언트가 하나의 최신 복사본을 보는 것에 가깝다(p38).
- Availability: 모든 요청에 결국 응답이 온다. 너무 늦은 응답은 응답이 없는 것과 같고, 실패도 실패라는 응답이 필요하다. Gilbert와 Lynch의 classic liveness property(p39).
- Partition tolerance: 서비스의 태도가 아니라 환경의 속성. 메시지는 지연되거나 영원히 사라질 수 있고, 손실과 지연은 구별하기 어렵다(p40).

### 05. CAP의 오해 (p41–46)

- 조합별 설명과 제품 예시. CA는 전통 RDBMS(p41), AP는 Cassandra·DynamoDB·CouchDB와 최종 일관성(p42), CP는 HBase·MongoDB·Redis·ZooKeeper와 금융·결제(p43).
- 가장 큰 오해는 셋 중 둘을 고른다는 생각이다. P는 선택이 아니라 사고이고, 평소에는 C와 A를 모두 누리다가 분할이 났을 때 A와 C 중 무엇을 포기할지 고른다(p44).
- Brewer의 2012년 정정(p45). "2 of 3"은 오해를 부른다, 분할은 드물다, 선택은 세밀한 단위에서 일어난다, C와 A는 정도의 문제다.
- CAP의 C는 ACID의 C가 아니다(p46). ACID의 C는 불변식 보존, CAP의 C는 single-copy consistency. serializable 격리는 분할 중 유지하기 어렵다.

### 06. 분산 시스템의 한계 (p47–50)

- 부분 실패(p47). 관찰자마다 누가 죽었는지 다르게 본다.
- 전역 시계 부재(p48). Lamport의 「Time, Clocks, and the Ordering of Events in a Distributed System」.
- FLP(p49). 완전 비동기 모델에서 프로세스 하나만 실패해도 결정론적 합의가 항상 결정을 내리도록 보장할 수 없다.
- 실무의 타협(p50). 부분 동기성, timeout, leader election.

## 핵심

- 정의와 정정이 정확하다. C를 single-copy consistency로 두고(p38), Brewer 2012의 네 가지 정정(p45)과 "CAP의 C ≠ ACID의 C"(p46)를 원문대로 옮긴다. Part 3의 "모든 노드가 같은 시점에 같은 값"(3-02 p41)보다 원래 정의에 가깝다. 두 정의의 비교와 전문은 [[CAP 정리]]에 있다.
- 약점은 제품 분류표(p41–43)다. 같은 소단원이 p44–45에서 "셋 중 둘을 고른다는 오해"를 말하면서 그 앞에 제품을 CA·AP·CP 칸에 넣는다.
- 부분 실패·시계·FLP(p47–50)는 뒤 소단원의 합의 알고리즘이 왜 timeout과 리더 선출에 기대는지를 미리 설명한다. 전문은 [[분산 시스템]], [[합의 알고리즘]].

## 주의·결함

- ❌ Redis를 CP 예시로 든다(p43). Redis Cluster 문서는 "Redis Cluster does not guarantee strong consistency"라고 쓰고, 확인 응답을 받은 쓰기도 잃을 수 있다고 밝힌다. 복제 문서는 `WAIT`로도 "a CP system with strong consistency"가 되지 않는다고 적는다. [Cluster: https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/ · 복제·`WAIT`: https://redis.io/docs/latest/operate/oss_and_stack/management/replication/ , 2026-09-28 확인] 자세한 내용은 [[Redis]].
- ⚠️ MongoDB(CP)와 DynamoDB(AP)는 설정에 따라 다르다. MongoDB의 linearizable read concern은 primary와 단일 문서에만 쓸 수 있고, DynamoDB는 기본 eventually consistent 읽기에 strongly consistent 읽기 옵션이 있다. [https://www.mongodb.com/docs/manual/reference/read-concern-linearizable/ , https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html , 2026-09-28 확인]
- ⚠️ "CA = 전통 RDBMS(Oracle, MySQL, PostgreSQL)"(p41). 두 제품의 복제 구성은 [[MySQL]]·[[PostgreSQL]]에 있다. 단일 노드는 CAP가 다루는 분산 시스템이 아니고, 복제를 붙이면 분할 때 C나 A를 골라야 한다. 슬라이드 자신이 "분산 시스템에서는 구현하기 어려운 조합"이라는 단서를 달고, p44에서 "2개를 고른다는 것이 가장 큰 오해"라고 쓴다. 같은 소단원 안의 긴장이다. Kleppmann은 저장소를 CP·AP 칸에 넣는 일 자체를 그만두자고 한다. [https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html , 2026-09-28 확인]
- ✅ Brewer 2012 인용(p45·p46)은 원문과 맞다("the C in CAP refers only to single-copy consistency, a strict subset of ACID consistency", https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/ , 2026-09-28 확인). safety/liveness 틀(p37)은 Brewer의 글이 아니라 Gilbert와 Lynch의 2012년 글 「Perspectives on the CAP Theorem」의 것이다. 슬라이드는 출처를 가르지 않는다.
- ✅ Lamport 1978, FLP 1985(p48–49)는 서지 사실과 맞다.
- p49의 따옴표 문장("단 1대의 고장만 있어도…")은 논문의 인용이 아니라 강의의 풀이다.
- 중복 슬라이드. p34=p35.

## 관련

- 개념: [[CAP 정리]] · [[분산 시스템]] · [[합의 알고리즘]] · [[NoSQL]] · [[관계형 데이터베이스]]
- 엔티티: [[Redis]]
- 이전 강의: [[AI DE 강의 4-01 분산 처리의 등장과 도입 판단]]
- 다음 강의: [[AI DE 강의 4-03 고가용성·복제·합의]]

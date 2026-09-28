---
type: source
title: AI DE 강의 4-03 고가용성·복제·합의
aliases: [AI DE 4-03]
tags: [AI-DE-강의, 분산, 가용성]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf"
---

# AI DE 강의 4-03 고가용성·복제·합의

[[AI 데이터 엔지니어링 강의]] Part 4 Ch1의 마지막 소단원이다. 고가용성, 복제, 합의 알고리즘을 "목표, 데이터 수단, 제어 수단"의 세 층으로 놓고, [[PostgreSQL]]·Kafka·Kubernetes·Consul·Vault의 실제 구성으로 설명한다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch1. 분산처리의 필요성과 주의사항: 4. 고가용성, 복제(Replication)와 합의 알고리즘(Consensus) |
| 원본 파일 | `part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` p51–66 (16p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch1~4`, 소단원 번호 `4`는 표지 슬라이드 |

## 요약

### 01. 세 개념의 관계 (p53–54)

- 복제본을 여러 개 두면 장애에 강해지는가? 누가 primary인지, 어느 복제본이 최신인지, 분할 때 어느 쪽이 쓰기를 받을지, 장애 후 라우팅을 어디로 바꿀지까지 정해야 한다.
- 고가용성은 목표, 복제는 데이터 수단, 합의는 제어 수단. 대체 관계가 아니라 계층 관계다. 예로 PostgreSQL의 takeover와 Consul의 quorum 기반 로그 순서를 든다.

### 02. 고가용성 (p55–57)

- Google Cloud PostgreSQL HA 문서를 따라 HA를 인프라 장애에 대한 회복력으로 정의한다. 목표는 빠른 failover이고, RTO(얼마나 빨리)와 RPO(얼마나 적게 잃나)로 잰다.
- 구성 요소 넷: 실패 감지, standby 승격, query routing 전환, 옛 primary의 fallback.
- 예: PostgreSQL primary-standby, Kubernetes control plane(stacked vs external etcd), Vault(Raft).

### 03. 복제 (p58–60)

- 목적 셋: 장애 대체본, 읽기·지역 분산, 손실 위험 감소. PostgreSQL은 WAL shipping과 streaming replication, Kafka는 파티션 로그 복제.
- 동기 복제: standby 최소 1개의 flush ACK를 기다린다. RPO = 0이지만 지연이 늘고, standby 장애 때 primary 쓰기가 막힐 수 있다.
- 비동기 복제: 로컬 WAL 기록 즉시 ACK. 지연이 낮고 PostgreSQL 등 대부분의 기본값이지만 RPO > 0.

### 04. 합의 (p61–64)

- 복제 이후 결정할 것: 승격할 replica, 최신 WAL 위치, split brain 방지, 트래픽 전환.
- 합의는 로그 엔트리의 유효성·순서·commit 시점·멤버십 변경에 동의하는 메커니즘. Raft와 Paxos.
- Raft의 리더·팔로워·후보, election timeout, 과반 득표(5대 중 3대).

### 05. 합의의 대가 (p65–66)

- 지연(PostgreSQL 동기 복제), 비용과 쓰기 실패율(Kafka RF·min.ISR·acks=all), 과반수의 역설(Consul·etcd는 quorum loss 때 스스로 unavailable).
- 세 계층의 조합 패턴 셋: RDBMS HA(동기 복제 + Patroni·pg_auto_failover + LB), 분산 로그(RF=3, min.ISR=2, acks=all), 제어-데이터 분리(다중 control plane + external etcd).

## 핵심

- "고가용성은 목표, 복제는 수단, 합의는 제어 장치"(p54)라는 층 구분이 이 소단원의 설명 틀이다. 복제는 [[복제]], 합의는 [[합의 알고리즘]]에 전문을 모았다.
- HA를 복제본의 유무가 아니라 RTO·RPO라는 운영 목표로 정의한다(p55). 뒤의 운영 덱이 SLO를 거는 방식([[서비스 수준 목표]])과 같은 사고다. 이 연결은 위키의 관찰이다.
- 합의의 대가 셋(p65)은 [[CAP 정리]]의 선택이 실제 제품 설정(동기 복제, acks=all, quorum)으로 어떻게 나타나는지 보여 준다.

## 주의·결함

- ✅ PostgreSQL 기본값이 비동기라는 서술(p60)과 동기 복제의 flush 대기(p59)는 맞다. `synchronous_commit = on`의 뜻이 "flushed it to durable storage"다. `remote_write`·`remote_apply` 같은 단계는 강의에 없다. [https://www.postgresql.org/docs/current/runtime-config-wal.html , 2026-09-28 확인] 「대부분의 RDBMS」라는 일반화는 확인하지 않았다.
- ✅ Raft 서술(p63–64)은 원 논문 §5.2와 맞다. 강의는 timeout이 무작위라는 점을 "가장 먼저 끝난 팔로워"로만 암시한다. [https://raft.github.io/raft.pdf , 2026-09-28 확인]
- ✅ Kafka 패턴(p66)은 공식 설정 문서의 "typical scenario"와 같다. 프로듀서 기본값이 3.0부터 `acks=all`이라는 점은 강의에 없다([[복제]]).
- p64의 "과반수 룰(Quorum): 5대 중 3대 이상의 표"는 바로 윗줄을 반복한다.
- p57의 "control plan"은 오탈자다.

## 관련

- 개념: [[복제]] · [[합의 알고리즘]] · [[CAP 정리]] · [[분산 시스템]]
- 엔티티: [[Apache Kafka]]
- 이전 강의: [[AI DE 강의 4-02 CAP 정리와 분산 시스템의 한계]]
- 다음 강의: [[AI DE 강의 4-04 Redis 핵심 개념과 성능 요소]]

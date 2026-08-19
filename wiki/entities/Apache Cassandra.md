---
type: entity
title: Apache Cassandra
area: [data-engineering]
aliases: [Cassandra, wide-column, wide column store, 와이드컬럼, 멀티리전]
tags: [data-engineering, apache, nosql, wide-column, cassandra, replication, availability]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch9 Serving OLAP search and NoSQL]]"]
---

# Apache Cassandra

**데이터를 여러 서버와 지역에 복제해 높은 가용성을 제공하는 wide-column NoSQL.** 대규모 온라인
서비스의 **많은 읽기와 쓰기**를 안정적으로 처리하는 자리다.

풀려는 문제: **여러 지역의 사용자가 동시에 이용하는 서비스는 한 데이터센터의 DB에만 의존하기
어렵다** — 장애가 나도 서비스가 계속돼야 하고, 사용자와 가까운 지역에서 읽어야 한다.

## 동작

- **파티션 키**를 기준으로 데이터를 여러 노드에 나누고 **복제**한다.
- 서버 일부가 멈춰도 다른 복제본이 요청을 처리한다.
- 노드를 추가해 처리량을 늘린다 — **쓰기 확장**이 설계의 중심이다.
- **wide-column** — 키 아래 많은 컬럼, 시계열형 행 패턴에 적합.

맞는 업무: 사용자 피드 · 로그인 세션 · 디바이스 상태처럼 **조회할 키가 분명하고 쓰기가 많은** 것.

⚠️ **관계형처럼 여러 테이블을 자유롭게 조인하거나 조건을 수시로 바꾸는 분석에는 맞지 않는다.**
⭐ 설계 순서가 반대다 — **쓸 조회 방식부터 정한 뒤 그에 맞춰 테이블과 키를 설계한다.**
[[Schema-centric data modeling]]이 말하는 정규화·범용 질의의 전제가 여기서 뒤집힌다.

## Cassandra vs [[Apache HBase]]

둘 다 wide-column 계열이지만 **사용 환경이 다르다.**

| | |
|---|---|
| **Cassandra** | **Hadoop 없이도 독립적인 서비스 데이터베이스**로 쓰인다. 여러 지역에 걸친 서비스 DB가 필요할 때 |
| **HBase** | **HDFS와 하둡 생태계에 밀접하게 연결**된다 |

## 위키 안에서의 위치

- [[NoSQL]] — 4타입 중 **wide-column의 대표 구현체**. 그 페이지가 말하는 *"확장성은 자동으로
  해결되지 않는다 — 파티션 키가 전부다"* 의 실물이 Cassandra다.
- [[CAP theorem]] — **가용성을 택한 쪽의 교과서적 예시.** Brewer의 2012년 정정("셋 중 둘이 아니다")을
  읽을 때 이 제품이 그 논의의 기준점이다.
- [[Replication and consensus]] — 멀티리전 복제와 RTO/RPO. 과반수 합의 대신 복제본 다수로 읽기·쓰기를
  받는 설계.
- [[Consumption layer]] — 조회 형태 중 **키 조회** 칸.
- ⭐ **혼자 다 하려 들지 않는다** — *"실시간 집계나 텍스트 검색까지 필요하다면 Cassandra 하나로 모두
  처리하기보다 Pinot나 Solr 같은 전용 시스템에 데이터를 전달해 역할을 나누는 편이 관리하기 쉽다."*
  → [[Consumption layer]]의 팬아웃 원칙.

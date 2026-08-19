---
type: entity
title: Apache HBase
area: [data-engineering]
aliases: [HBase, 행키, row key, 컬럼 패밀리, column family, 핫스팟, hotspot]
tags: [data-engineering, apache, nosql, wide-column, hbase, hadoop]
created: 2026-08-19
updated: 2026-08-19
sources: ["[[Apache Map - Ch9 Serving OLAP search and NoSQL]]"]
---

# Apache HBase

**HDFS에 저장된 대규모 데이터를 키로 빠르게 읽고 쓰게 만든 wide-column 데이터베이스.**

풀려는 문제: **HDFS는 큰 파일을 안정적으로 보관하는 데는 적합하지만, 특정 키의 데이터를 바로 찾아
읽거나 수정하기는 어렵다.** HBase가 그 위에 **랜덤 읽기·쓰기**를 얹는다. → [[Apache Hadoop]]

## 동작

- 테이블은 **행키(row key)** 와 **컬럼 패밀리** 중심으로 구성된다.
- 큰 테이블을 여러 **리전**으로 나눠 서버에 분산한다.
- 로그·시계열을 정해진 키 구조로 저장한 뒤 **특정 행 또는 연속된 행 범위**를 빠르게 가져온다.
- 전체 데이터를 분석하기보다 **특정 행·범위 조회**에 초점.
- MapReduce·Spark 배치와 온라인 조회를 **같은 하둡 환경에서** 함께 운영할 때 많이 쓰였다.

기본 접근 방식이 SQL이 아니므로, SQL이 필요하면 **Phoenix**를 함께 쓴다 → [[SQL execution layer]]

## ⚠️ 행키 설계가 곧 운영이다

> **"요청이 일부 키에 몰리면 특정 리전 서버에 부하가 집중되는 핫스팟이 생긴다."**

⭐ **데이터를 여러 서버에 고르게 분산하면서, 동시에 필요한 범위 조회도 되도록** 행키를 잡아야 한다 —
이 둘은 서로 당긴다. 순차 키(타임스탬프 등)는 범위 조회에 좋지만 쓰기가 한 리전에 몰리고, 해시 키는
고르게 퍼지지만 범위 조회를 잃는다. [[NoSQL]]의 *파티션 키가 전부다* 와 같은 문제의 wide-column 판이다.

## 언제 안 쓰나

⚠️ **"새로운 레이크하우스를 오브젝트 스토리지와 Iceberg로 구성한다면 HBase가 필요하지 않은 경우도
많다."** 단독 클라우드 네이티브 기본값도, 풍부한 SQL 웨어하우스도 아니다.

반대로 **기존 HBase에 운영 데이터가 있거나 하둡 환경에서 빠른 키 조회가 필요하면** 여전히 유용하다.
여러 지역에 걸친 서비스 DB가 필요할 때는 [[Apache Cassandra]]가 더 적합한 경우가 많다.

## 위키 안에서의 위치

- [[Apache Cassandra]] — 같은 wide-column 계열, 다른 사용 환경(독립 서비스 DB vs 하둡 밀착).
- [[Apache Hadoop]] — HDFS 위에 얹히는 층. HBase는 하둡 생태계에 속하는 대가로 그 생태계와 함께 간다.
- [[Object storage layout]] — 오브젝트 스토리지 + [[Table formats]] 조합이 HBase의 자리를 상당 부분
  가져간 흐름.
- [[Consumption layer]] — 조회 형태 중 **키 조회** 칸.

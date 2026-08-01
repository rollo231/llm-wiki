---
type: source
title: AI DE Course - Ch1-4 Tech stack and tooling
area: [data-engineering]
aliases: [CH01-4 기술 스택, AI 엔지니어링 필수 기술 스택]
tags: [data-engineering, course, fast-campus, tooling, python, spark, cloud]
created: 2026-08-01
updated: 2026-08-01
sources: ["raw/data-engineering/CH01-4. AI 엔지니어링 필수 기술 스택 및 툴 생태계.pdf"]
---

# AI DE Course - Ch1-4 Tech stack and tooling

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 CH01-4**
"AI 엔지니어링 필수 기술 스택 및 툴 생태계". 원본(로컬):
`raw/data-engineering/CH01-4. AI 엔지니어링 필수 기술 스택 및 툴 생태계.pdf` (8p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

## 요점

### 채용 공고(JD)로 본 필수 역량 4종

강의가 **현업 채용 공고 분석**이라고 제시하는 4분할. (출처 표기는 없다.)

| 영역 | 내용 |
|---|---|
| **클라우드 플랫폼** | AWS·Azure·GCP에서의 데이터 저장·처리·보안 및 인프라 운영 |
| **데이터베이스** | **SQL(필수)** + NoSQL(선택), 쿼리 최적화 |
| **프로그래밍 언어** | 데이터 처리용 **Python** + 분산 처리용 **Java/Scala** |
| **파이프라인·오케스트레이션** | **Kafka**(실시간) + **Airflow**(워크플로우) 구축·운영 |

### Python 생태계 — 두 축

- **Pandas** — 대규모 데이터 읽기·정리·정제. DataFrame API, 결측치 처리·필터링·GroupBy,
  다양한 포맷(CSV·Excel·SQL) 입출력.
- **PyTorch** — 딥러닝 신경망 구축·학습. Tensor 연산 + GPU 가속, 동적 그래프로 디버깅 용이.

### SQL — ANSI SQL vs Spark SQL

- **ANSI SQL** — 표준 문법 준수, 데이터 조작, 트랜잭션.
- **Spark SQL** — 대용량 데이터 처리, 인메모리 연산.

### Java·Scala가 여전히 강한 이유

**데이터 인프라의 핵심 엔진들이 JVM 위에 있다**는 것이 논지다.

- **Apache Spark** — Scala 기반. JVM 생태계로 기존 자바 라이브러리·하둡과 완벽 호환.
  SQL·스트리밍·ML을 단일 플랫폼에서.
- **Apache Flink** — 저지연·고처리량 스트리밍 API, **exactly-once** 상태 관리.
  Java·Scala 모두 일급 시민.
- **Apache Kafka** — **Scala로 코어 구현**(높은 동시성·성능). Kafka Streams는 Java/Scala 라이브러리.

### 인프라 — Docker와 3대 클라우드

- **Docker** — 로컬과 프로덕션 환경의 일관성 보장. "Build once, Run anywhere". Docker Compose로
  멀티 컨테이너 정의. → [[Data and model versioning]]의 "환경 고정"이 이것이다.
- **AWS** — 시장 점유율 1위, **S3 중심의 데이터 레이크 생태계**, 관리형 서비스 완성도.
- **Azure** — 기업 친화적(MS 오피스·AD 연동), Synapse Analytics로 DW/빅데이터 통합,
  하이브리드 클라우드 최적화.
- **GCP** — **BigQuery** 중심의 분석 성능, Kubernetes(GKE) 원조, Vertex AI 연동.

## 평가

**나열 중심의 덱이다.** 각 도구가 왜 그 자리에 있는지는 짧게만 설명하고, 선택 기준(예: Flink vs
Spark Streaming, Airflow vs Dagster)은 다루지 않는다. Flink vs Spark 비교는
[[AI DE Course - Ch4-5,6 Stream processing engines]]에서 나오고, 오케스트레이터 비교는
**이 코스 어디에서도 나오지 않아** [[Data Engineering]] MOC의 열린 질문으로 남는다.

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Batch and stream processing]] (도구 지도), [[Apache Kafka]],
  [[Stream processing semantics]], [[Analytical data storage tiers]]
- 인접 출처: [[Data landscape guide for developers]] — 같은 지형을 훨씬 넓게 훑는다

---
type: source
title: AI DE 강의 4-07 메시지 브로커와 스트림 처리 엔진
aliases: [AI DE 4-07]
tags: [AI-DE-강의, 스트리밍, 처리]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf"
---

# AI DE 강의 4-07 메시지 브로커와 스트림 처리 엔진

[[AI 데이터 엔지니어링 강의]] Part 4 Ch3의 둘째 소단원이다. 소스와 싱크 사이에 놓이는 두 중간 계층, 브로커(운반)와 스트림 처리 엔진(계산)의 역할을 가르고, 엔진이 단순 consumer 앱과 무엇이 다른지(상태·시간·복구)를 설명한 뒤 Flink, Spark Structured Streaming, Kafka Streams를 비교한다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch3. 스트리밍 데이터 처리: 2. 메시지 브로커와 스트림 처리 엔진의 역할 |
| 원본 파일 | `part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` p152–175 (24p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch1~4`, 챕터 `Ch3`와 소단원 번호 `2`는 표지 슬라이드 |

## 요약

### 01. 스트리밍 파이프라인의 두 중간 계층 (p154–158)

- 둘 다 소스와 싱크 사이에 있지만 질문이 다르다. 브로커는 "이벤트를 어떻게 안전하게 흘리고 보관할 것인가", 엔진은 "계속 들어오는 이벤트를 어떤 시간 기준과 상태 기준으로 계산할 것인가"를 묻는다(p154).
- 이 구분이 흐려지면 Kafka만 두고 실시간 집계가 끝났다고 오해하거나, 반대로 Flink·Spark만 붙이면 메시징 계층이 없어도 된다고 착각한다고 경고한다.
- p155는 그림뿐이다. 데이터 소스 → 메시지 브로커(persistence·routing) → 스트림 처리 엔진(internal state store, sliding·tumbling window) → DB·DW·알림으로 흐르는 도식이다.
- 브로커는 운반 계층이다. 시스템 분리, 버퍼링, 라우팅·다중 구독·재전달·보관 기간 관리, 재처리를 위한 원본 보존을 맡는다(p156). 엔진은 계산 계층이다. 집계·조인·윈도우 연산, stateful processing, event-time 처리, 체크포인트 복구를 맡는다(p157).

### 02. 스트리밍 엔진 (p159–163)

- Stateless 처리(필터, JSON → Avro 변환)는 브로커에 붙인 단순 Python·Java consumer로도 된다. 실무 요구는 대부분 "특정 기간 동안 특정 유저의 패턴"이라 상태가 필요하다(p159).
- Stateful 예로 "최근 5분간 로그인 실패 5회 이상 계정 차단", 실시간 누적 매출, 이동 평균, "1분 안에 같은 카드로 3개국 이상 결제" 패턴 탐지, 주문-결제 스트림 조인을 든다(p160–161).
- 상태 저장소(p162): 레코드마다 외부 DB(Redis·MySQL)에 가면 네트워크 지연 때문에 실시간성이 안 나오므로 계산 노드 로컬에 둔다. HashMap 기반(메모리, 가장 빠르지만 메모리 크기 한계)과 RocksDB 기반(로컬 SSD에 LSM-Tree, TB급 상태)을 든다.
- 엔진은 데이터를 읽고 버리는 프로그램이 아니라 현재 결과를 계속 유지·갱신하는 계산 엔진이다(p163). Spark Structured Streaming은 입력을 "입력 표", 결과를 "결과 표"로 보고 점진적으로 갱신한다.

### 03. 스트림 처리 엔진의 핵심 (p164–167)

네 장으로 나눈다. 상태를 기억하는 계산(p164), 시간 기준을 해석하는 계산(p165, 워터마크), 늦게 도착한 데이터와 시간 구간 계산(p166), 장애 뒤 이어 가는 복구 구조(p167). 복구는 엔진마다 다르다. Flink는 체크포인트로 연산자 상태와 입력 위치를 함께 저장하고, Spark는 입력 위치 기록·체크포인트·WAL·재처리 가능한 입력·중복에 안전한 출력을 조합하며, Kafka Streams는 상태 저장소의 변경 이력을 기록한 토픽(changelog)으로 상태를 복원한다.

### 04. 대표적인 스트림 처리 엔진 (p168–175)

| | Flink | Spark Structured Streaming | Kafka Streams |
|---|---|---|---|
| 강의의 한 줄 | 상태와 시간 제어를 전면에 둔 엔진 | 실시간 입력을 계속 늘어나는 표로 보는 엔진 | Kafka 기반 애플리케이션 안에서 도는 처리 라이브러리 |
| 실행 | 분산 클러스터, bounded·unbounded 모두 | Spark SQL 엔진 위, 기본은 짧은 간격의 마이크로 배치 | Java·Scala 앱에 내장, 별도 클러스터 없음 |
| 잘 맞는 문제 | 사용자별 상태, 긴 시간 구간, 늦은 데이터가 많은 환경, 큰 상태 | SQL·DataFrame 중심 조직, 기존 Spark 배치와의 통합 | Kafka가 핵심 입력인 환경, Kafka to Kafka, 마이크로서비스 내부 실시간 로직 |

## 핵심

- 운반과 계산을 두 질문으로 가르는 틀(p154)이 이 소단원에서 가장 쓸모 있다. 브로커 쪽 전문은 [[메시지 브로커]], 엔진 쪽 전문은 [[스트림 처리]]에 있다.
- 엔진 비교에 Kafka Streams가 들어와 Part 1의 Flink vs Spark 이분법이 셋이 된다. 엔진 표는 [[스트림 처리]]에서 셋으로 고쳤다.
- Part 4는 Spark를 Structured Streaming으로 설명한다. Part 1의 [[AI DE 강의 1-12 실시간 처리 엔진]]이 레거시인 DStream으로 설명한 것을 말없이 바로잡은 셈이다. 코스가 이 차이를 밝히지 않는다는 것은 위키의 관찰이다([[Apache Spark]]).

## 주의·결함

- ❗ p153 목차의 「05 합의의 대가」는 본문에 없다. Ch1 소단원 4(p52)의 목차 항목과 같은 이름이라, 목차를 복사하고 고치지 않은 흔적으로 보인다([[AI DE 강의 4-03 고가용성·복제·합의]]).
- ⚠️ p168·172의 "Spark Structured Streaming = 마이크로 배치, Flink보다 지연이 약간 길다"는 작성 시점에 이미 낡았다. Continuous Processing(2.3부터, 실험적)이 있었고, Spark 4.1.0(2025-12-16)이 Real-Time Mode를 넣었다. 릴리스 노트는 "First official support for Structured Streaming queries running in real-time mode… single-digit milliseconds"라고 적고, 4.2.0(2026-07-14)은 PySpark에도 이 모드를 연다. [https://spark.apache.org/releases/spark-release-4.1.0.html · https://spark.apache.org/releases/spark-release-4-2-0.html , 2026-09-28 확인]
- ⚠️ p168의 "Flink는 복잡한 이벤트 처리(CEP)의 표준"은 주관적 과장이다. FlinkCEP 라이브러리는 있다("FlinkCEP is the Complex Event Processing (CEP) library implemented on top of Flink", https://nightlies.apache.org/flink/flink-docs-stable/docs/libs/cep/ , 2026-09-28 확인). 표준이라는 근거는 없다.
- ✅ p162의 상태 백엔드 두 종류는 맞다(HashMapStateBackend, EmbeddedRocksDBStateBackend). 작성 시점에는 Flink 2.0(2025-03-24)이 ForSt 기반 disaggregated state를 도입한 뒤였는데 강의에는 없다. 현재 문서는 ForSt를 "still in the experimental stage and is not fully available for production"이라고 적는다. [https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/state_backends/ , 2026-09-28 확인]
- p156의 "영속화르"는 오탈자다. p168과 p169는 같은 슬라이드다.

## 관련

- 개념: [[스트림 처리]] · [[메시지 브로커]] · [[이벤트 기반 아키텍처]]
- 엔티티: [[Apache Flink]] · [[Apache Spark]] · [[Apache Kafka]]
- 이전 강의: [[AI DE 강의 4-06 메시지 브로커의 종류와 전달 보장]]
- 다음 강의: [[AI DE 강의 4-08 Processing Time과 Event Time]]

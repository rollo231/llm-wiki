---
type: source
title: AI DE 강의 4-10 람다·카파와 현대 아키텍처
aliases: [AI DE 4-10]
tags: [AI-DE-강의, 스트리밍, 아키텍처]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf"
---

# AI DE 강의 4-10 람다·카파와 현대 아키텍처

[[AI 데이터 엔지니어링 강의]] Part 4 Ch3의 마지막 소단원이다. 배치 정확성과 실시간 지연 사이의 긴장에서 나온 람다 아키텍처, 그 이중 코드 경로를 로그 재생으로 대체한 카파 아키텍처, 그리고 그 뒤의 "현대 아키텍처"를 한 이름이 아니라 여러 축(Lakehouse, Unified Path, Data Mesh, Data Fabric, Data Contract)의 조합으로 설명한다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch3. 스트리밍 데이터 처리: 5. 람다 아키텍처의 한계와 카파 아키텍처, 현대의 아키텍쳐 |
| 원본 파일 | `part4/01. Ch1~4. 분산처리·캐싱·스트리밍·GPU 워크로드.pdf` p217–240 (24p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-05-21 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch1~4`, 챕터 `Ch3`와 소단원 번호 `5`는 표지 슬라이드 |

## 요약

### 01. 람다 아키텍처 (p219–223)

- Nathan Marz가 제안한 모델로, 배치 레이어(정확성, 마스터 데이터셋), 스피드 레이어(지연, 최근 데이터), 서빙 레이어(두 결과를 합친 뷰)로 이뤄진다(p219). p221은 Databricks 사이트의 구조 그림이다.
- 출발점은 실시간과 정확성의 긴장이다. 정확한 결과는 전체 재계산으로, 빠른 결과는 부분 데이터와 점진 계산으로 얻던 시기에 둘 다 원했다(p220).
- 람다가 남긴 유산은 원본 보존, 재처리 가능성, 코드 변경 때 과거 결과 재계산, 실시간 계층의 오류를 배치 계층이 결국 덮어쓴다는 사고다. 가장 큰 공헌은 재처리를 아키텍처 수준의 요구사항으로 끌어올린 것이라고 한다(p222).
- 사례는 이상 결제 탐지다. 스피드는 결제 즉시 블랙리스트 대조와 차단, 배치는 수개월 결제를 전수 조사해 새 사기 패턴 학습(p223).

### 02. 람다 아키텍처의 한계 (p224–226)

- 같은 변환 로직을 두 계층에 두 번 구현한다. 프레임워크가 다르면 코드 스타일·상태 처리·오류 처리도 달라져 결과 동치성 검증, 테스트, 디버깅이 급격히 어려워진다. 가장 큰 비용은 계산 비용이 아니라 인지 비용과 유지보수 비용이다(p224).
- 운영 쪽으로는 두 프레임워크, 두 결과 저장소, 병합 로직, 두 배의 장애 추적 경로와 병목이 생긴다(p225).
- 람다는 잘못된 답이 아니라 당시 도구 한계의 산물이라고 평가한다. 2010년대 초 Hadoop은 정확하지만 몇 시간~며칠 걸렸고, Storm은 1초 만에 결과를 냈지만 중복·유실로 100% 정확하지 않았다(p226).

### 03. 카파 아키텍처 (p227–232)

- 배치 경로와 속도 경로를 따로 두지 않고 하나의 스트림 처리 경로로 실시간 처리와 재처리를 모두 한다. 전제는 과거를 다시 읽을 수 있는 불변 이벤트 로그다(p227).
- Kreps의 재처리 흐름(p228): 입력 로그를 충분히 오래 보관 → 코드가 바뀌면 새 버전 작업 기동 → 과거 오프셋(earliest)부터 다시 읽어 새 결과 테이블 계산 → 현재까지 따라잡으면 결과 전환 → 이전 작업 종료. 복잡도의 초점이 "두 개의 코드 경로"에서 "재생 가능한 로그"로 옮겨 간다.
- 장점은 단일 경로·단일 코드베이스·재처리 방식의 명확화이고, 전제는 로그 보존 기간, 빠른 재생이 가능한 엔진, 결과 저장소 전환 전략, 다시 읽어도 의미가 유지되는 시간 기준과 상태 설계다(p229). 이를 가능하게 한 것으로 Kafka의 보관·재생과 Flink·Spark의 exactly-once 엔진을 든다(p230).
- 도전 과제는 수년치 원본을 Kafka에 두는 저장 비용, 매우 긴 윈도우(최근 1년 행동)의 상태 크기, 워터마크·상태 저장소를 다루는 숙련도다(p231).
- 사례는 실시간 추천(클릭 스트림과 한 달 취향 로그 replay를 결합해 0.5초 안에 갱신)과 실시간 결제 모니터링(늦은 데이터도 워터마크로 별도 배치 없이 스트리밍 계층에서만 정확히 집계)이다(p232).

### 04. 현대의 아키텍처 (p233–240)

- 람다 다음에 하나의 정답이 등장한 것이 아니라, 저장·처리·조직·연결·신뢰가 각각 다른 방향으로 진화했다. 그래서 여러 축의 조합으로 이해한다(p233).

| 축 | 강의의 설명 |
|---|---|
| Lakehouse (저장·관리) | Iceberg·Delta Lake·Hudi 오픈 테이블 포맷, ACID·스키마 강제·타임 트래블(p234–235) |
| Unified Path (처리) | 같은 엔진 또는 같은 API로 batch와 stream을 처리해 이중 코드 경로를 줄임(p236) |
| Data Mesh (조직) | 데이터를 도메인별 제품으로 취급. Domain Ownership과 Self-Serve Platform(p237–238) |
| Data Fabric (메타데이터·자동화) | 데이터를 한곳에 모으지 않고 메타데이터와 AI로 엮음. Active Metadata, Knowledge Graph(p239–240) |
| Data Contract (경계 규약) | 목록에만 있고 별도 슬라이드는 없다(p233) |

## 핵심

- 람다를 "당시 도구 한계의 산물"로, 그 유산을 "재처리를 아키텍처 요구사항으로 끌어올린 것"으로 평가하는 틀(p222·226)이 이 소단원의 요점이다. 전문은 [[람다 아키텍처와 카파 아키텍처]]에 모았다.
- 람다의 이중 구현 비용(p224)은 [[학습-서빙 스큐]]의 원인과 같은 구조다. [[배치 처리]]가 Part 1 때 이미 이 연결을 적어 두었고, Part 4의 "결과 동치성 검증"이 같은 문제를 파이프라인 쪽에서 말한다.
- 현대 아키텍처의 다섯 축 가운데 Lakehouse는 [[데이터 레이크하우스]], Data Contract는 [[데이터 계약]], Data Fabric의 Knowledge Graph는 [[지식 그래프]]로 이어진다. Part 1·3의 내용을 축 이름으로 다시 묶은 셈인데, 강의는 앞 파트를 참조하지 않는다.

## 주의·결함

- ✅ p228의 재처리 흐름은 Kreps의 원문과 내용이 일치한다. 원문은 네 단계인데 강의가 둘째 단계(두 번째 작업을 처음부터 돌려 새 테이블에 쓴다)를 둘로 나눠 다섯 단계가 됐다. 「Questioning the Lambda Architecture」(O'Reilly Radar, 2014-07-02)는 "start a second instance… from the beginning of the retained data", "new output table", "switch the application", "Stop the old version of the job, and delete the old output table"로 적는다. [https://www.oreilly.com/radar/questioning-the-lambda-architecture/ , 2026-09-28 확인]
- ⚠️ p219는 람다를 Marz가 제안했다고만 적는다. Marz의 2011-10-13 블로그 글 「How to beat the CAP theorem」은 구조를 설명하지만 「Lambda Architecture」라는 이름은 쓰지 않는다. 이 이름은 이후 Manning 책 『Big Data』에서 나왔다(책은 위키가 직접 확인하지 않았다). [http://nathanmarz.com/blog/how-to-beat-the-cap-theorem.html , 2026-09-28 확인]
- ⚠️ p226의 Storm 서술은 뭉뚱그렸다. Storm은 ack를 쓰면 at-least-once(중복은 나도 유실은 없음)이고, 유실은 acker를 끄거나 anchor 없이 보낼 때 생기며, exactly-once는 Trident가 준다. 문서는 "best effort, at least once, and exactly once through Trident"라고 적는다. [https://storm.apache.org/releases/current/Guaranteeing-message-processing.html , 2026-09-28 확인]
- ⚠️ p232의 "늦게 도착한 데이터도 워터마크를 통해 별도 배치 없이 스트리밍 계층에서만 정확히 집계"는 앞 소단원 p209와 모순이다. 워터마크 지연보다 더 늦은 데이터는 반영이 보장되지 않는다고 강의 스스로 썼다([[AI DE 강의 4-09 워터마크와 윈도우 연산]]). 같은 사례의 "0.5초 이내" 수치도 출처가 없다.
- ⚠️ p237의 Data Mesh는 원칙 넷 가운데 둘(Domain Ownership, Self-Serve Platform)만 불릿으로 적는다. "데이터를 도메인별 제품으로 취급"은 본문 한 줄에만 있고, federated governance는 p238 그림에만 있다. Dehghani의 원칙은 "Domain-oriented decentralized data ownership and architecture", "Data as a product", "Self-serve data infrastructure as a platform", "Federated computational governance"다. [https://martinfowler.com/articles/data-mesh-principles.html , 2020-12-03, 2026-09-28 확인]
- p234의 "유연성과 성능이 완벽하게 결합된 차세대 플랫폼"은 마케팅 문구다. p239의 "능형 연결망"은 "지능형"의 오탈자로 보인다. p221 그림의 URL 파일명은 `hadoop-architecture.png`다.
- Part 1의 [[AI DE 강의 1-10 배치 vs 스트리밍]]이 Lambda를 이미 소개했는데 이 소단원은 참조하지 않는다.

## 관련

- 개념: [[람다 아키텍처와 카파 아키텍처]] · [[배치 처리]] · [[스트림 처리]] · [[데이터 레이크하우스]] · [[데이터 계약]] · [[지식 그래프]] · [[학습-서빙 스큐]]
- 엔티티: [[Apache Kafka]] · [[Apache Flink]] · [[Apache Spark]] · [[Delta Lake]]
- 이전 강의: [[AI DE 강의 4-09 워터마크와 윈도우 연산]]
- 다음 강의: [[AI DE 강의 4-11 GPU 아키텍처와 CUDA]]

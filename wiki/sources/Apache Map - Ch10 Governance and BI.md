---
type: source
title: Apache Map - Ch10 Governance and BI
area: [data-engineering]
aliases: [Apache 지도 Ch10, Apache 지도 믿고 쓰게 만드는 계층, Apache Map Ch10]
tags: [data-engineering, apache, governance, catalog, data-quality, bi, book]
created: 2026-08-19
updated: 2026-08-19
sources: [raw/data-engineering/apache/apache-book-full-spread.pdf]
---

# Apache Map - Ch10 Governance and BI

『Apache로 읽는 데이터 기술의 지도』(이현수, 2026) **Ch10. 믿고 쓰게 만드는 계층** — 개념 8개,
PDF pp.86–94. 트래커: [[Apache data technology map (book)]].

**두 개의 미결이 여기서 종결된다** — [[Apache Map - Ch1 How to read this book]]에서 지적한
*"기본 스택 5개에 카탈로그가 없다"*, 그리고 [[Apache Map - Ch6 Open table formats]]에서 미룬
*Hive Metastore 승격 판단*.

## ⚠️ 읽는 규칙의 첫 예외 — 논지가 개념 6이다

[[Apache data technology map (book)]] §읽는 규칙 1은 *"각 장은 마지막 개념부터 읽는다"* 였다.
**Ch10은 다르다** — 논지는 **개념 6(거버넌스 삼각형)** 이고, 개념 7·8(Superset·Zeppelin)은 **별 주제**
(사람이 조회·시각화하는 도구)가 뒤에 붙은 형태다.

즉 이 장은 **두 덩어리**다: 거버넌스 3축(1~6) + 소비 도구 2종(7~8).
개념 8의 마지막 문장이 둘을 억지로 묶는다 — *"이 장을 덮을 때는 거버넌스 삼각형과 BI·노트북 같은 소비
도구가 한 그림에 들어가는지 보면 됩니다. **데이터가 믿을 만해야, 보여 주는 도구도 쓸모가 있습니다.**"*

> **규칙 보정: "마지막 개념" → "그 장의 요약·분류 절".** 대개 마지막에 있지만 Ch10처럼 뒤에 다른 주제가
> 붙으면 중간에 있다.

## ⭐⭐ 거버넌스 삼각형 (개념 6) — 세 질문

> "거버넌스라고 하면 정책 문서만 떠올리기 쉽지만, 데이터 플랫폼에서는 **세 가지 질문이 반복됩니다.
> 무엇이 있는가, 누가 볼 수 있는가, 믿을 만한가.** (…) **제품 이름이 바뀌어도 이 세 질문은 거의 그대로
> 남습니다.**"

| 질문 | 축 | Apache | 현대 대안 |
|---|---|---|---|
| **무엇이 있는가** | 카탈로그·분류·계보로 **"알기"** | 🔹 Atlas | DataHub · OpenMetadata · Polaris · Gravitino |
| **누가 볼 수 있는가** | 권한·정책·감사로 **"막기·남기기"** | 🔸 Ranger | 클라우드 IAM · 웨어하우스 권한 · Lake Formation |
| **믿을 만한가** | 품질 지표로 **"재기"** | ▪️ Griffin | Great Expectations · dbt tests · 클라우드 DQ |

⚠️ **"한 도구에 세 축을 모두 넣으면 처음에는 편해 보여도 역할이 모호해지기 쉽습니다."**
⭐ [[Data catalog and semantic layer]]가 이미 *"Unity Catalog가 세 칸에 다 등장하는 것이 혼란의 출처"* 라고
적어 둔 것과 **같은 경고의 다른 절단면**이다.

⭐⭐ **처방이 설치 순서가 아니라 자기 진단이다.**

> "제품 설치 순서보다, **우리 팀에서 비어 있는 축이 어디인지** 확인하는 편이 좋습니다. 카탈로그만 있고
> 권한 통제가 약하거나, 권한만 엄격하고 품질 조건이 없으면 데이터 신뢰성이 떨어집니다.
> **'목록은 ○○, 권한은 ○○, 품질은 ○○'처럼 담당 도구를 한 문장으로 정리해 두면, 제품이 바뀌어도
> 기준은 유지하기 쉽습니다.**"

## ⭐⭐ 세 번째 메타 패턴 — 처방이 항상 "문장으로 적어 고정하라"다

| 장 | 처방 |
|---|---|
| **Ch7** | *"'데이터 소스 수집은 NiFi, 대량 동기화는 SeaTunnel'처럼 **역할을 문서에 고정**해 두면 된다"* |
| **Ch9** | *"필요한 기능을 '상품명 검색', '실시간 매출 집계'처럼 **구체적인 문장으로 정리**해 두면 된다"* |
| **Ch10** | *"'목록은 ○○, 권한은 ○○, 품질은 ○○'처럼 담당 도구를 **한 문장으로 정리**해 두면 된다"* |

⭐ 세 번 반복되는 형태가 같다 — **선택을 "제품 비교"가 아니라 "역할 문장 작성"으로 바꾼다.**
읽는 규칙 2(*비교 절은 성능 순위를 거부한다*)의 실행 형태가 이것이다. 트래커에 규칙 3으로 기록했다.

## 개념 8개

| # | Tier | 개념 | 요지 |
|---|---|---|---|
| 1 | 🔸 | **Atlas** | 자산 설명·**분류 태그**·**계보**. Hadoop·Hive와 함께 성장. ⚠️ 권한 강제·품질 측정은 안 함 |
| 2 | 🔸 | **Ranger** | 여러 서비스에 정책 배포, **컬럼·행 단위** 통제, 감사. **Atlas 태그와 결합** |
| 3 | 🔸 | **Griffin** | null 비율·중복·값 범위 규칙을 정의해 실행마다 점수·위반 기록 |
| 4 | 🔸 | **Gravitino** | 파일·테이블·**모델** 등 여러 자산, 여러 카탈로그가 섞인 환경의 **통합** |
| 5 | 🔸 | **Polaris** | **Iceberg 특화 REST 카탈로그.** Hive Metastore의 역할을 이어받는다 → [[Apache Polaris]] |
| 6 | 🔸 | 거버넌스 삼각형 | **이 장의 논지** — 위 |
| 7 | 🔹 | **Superset** | SQL 기반 BI·셀프서비스. 다중 소스를 한 화면에 → [[Apache Superset]] |
| 8 | 🔸 | **Zeppelin** | 노트북형 탐색. ⚠️ 전사 소비를 맡기면 버전 관리·권한이 흐트러진다 |

## ⭐⭐ 카탈로그는 단일 제품이 아니라 역할 구조다

Gravitino 항목이 이 장에서 가장 값이 나가는 한 줄을 준다.

> "**카탈로그도 단일 제품이 아니라 역할 구조로 설계된다**는 점을 분명히 하려고 이 책에 두었습니다.
> 제품 설치보다 **'우리 테이블의 공식 정보가 어디에 등록되는가'** 를 먼저 확인하면 된다."

세 종류가 구분된다.

| | 범위 |
|---|---|
| **Atlas** | 설명·분류·계보 중심의 **전통 카탈로그**(사람용에 가깝다) |
| **Polaris** | **Iceberg 특화.** *"예전 Hive Metastore가 맡던 역할을 Iceberg REST 카탈로그 방식으로 이어가는 흐름"* |
| **Gravitino** | 여러 엔진·여러 카탈로그가 섞인 환경의 **통합**. ⚠️ 아직 기본값이 된 제품은 아니다 |

⚠️ 그리고 두 곳 등록의 위험을 짚는다 — **"이미 다른 카탈로그를 쓰고 있다면 같은 테이블을 두 곳에 등록해
정보가 어긋나지 않도록 역할을 나누면 된다."**

> *"거버넌스는 정책뿐 아니라 **카탈로그 설계**이기도 하다."*

### 미결 1 종결 — Ch1의 "카탈로그가 없다"

[[Apache Map - Ch1 How to read this book]] §짚어 둘 것에서 **레이크하우스 기본 스택 다섯
(Spark·Parquet·Iceberg·Airflow·Superset)에 카탈로그가 빠져 있다**고 적었고, 예상대로 Ch10에 있었다.

⭐ Polaris의 문제 정의가 그 지적과 **글자까지 겹친다** — *"Iceberg 테이블이 늘어나면 파일 경로만으로는
'어느 스냅샷이 공식 테이블인가'를 합의하기 어렵다."*
→ [[SQL execution layer]] 3단계의 1️⃣ "테이블 규칙"이 카탈로그 없이는 성립하지 않는다는 것이 확인됐다.

### 미결 2 종결 — Hive Metastore 승격 판단

Ch6에서 *"Ch10에서 카탈로그 비교가 가능해질 때 재검토"* 로 미뤘다. **결론: 엔티티로 떼지 않는다.**

근거: Polaris가 *"Hive Metastore가 맡던 역할을 이어간다"* 고 명시하므로 **계보가 확정됐고**
(Hive Metastore → Iceberg REST 카탈로그 → Polaris / Gravitino), 그 계보는 이미
[[Data catalog and semantic layer]]의 3분류 표 안에 들어간다. **Hive Metastore를 떼면 그 표가 조각난다.**
대신 그 페이지에 §카탈로그는 단일 제품이 아니라 역할 구조다 절을 신설했다.

## 실제 스택에 대한 확인 — 로드맵의 Postgres 결정

⭐ [[Spatial omics platform roadmap]] §2.2는 카탈로그 저장소를 Iceberg → **Postgres**로 정정했다.
**Polaris는 그 결정을 뒤집지 않고 확인해 준다** — 명시된 한계가 *"모든 저장소·비Iceberg 자산의 만능
카탈로그는 아니다"* 이고, [[SpatialData]] store는 쿼리 엔진이 읽을 수 없는 불투명 blob이다.

> **판단 규칙: 관리 대상이 Iceberg 테이블이면 Polaris(또는 호환 REST 카탈로그), 불투명 산출물이면
> 카탈로그를 직접 만든다.** Polaris는 대안이 아니라 로드맵 §8(gold 팩트 테이블) 자리의 후보다.

로드맵 §2.2에 이 확인을 적어 두었다.

## Griffin — 품질 축, 그리고 서킷 브레이커의 전제

⚠️ **"Griffin만 도입한다고 품질 문화가 생기지는 않습니다."** 먼저 정할 것 둘을 준다.

1. **어떤 테이블을 점검 대상으로 둘지**
2. ⭐⭐ **기준을 못 지키면 적재를 멈출지 알리기만 할지**

2번이 [[Data SLA and observability]] §서킷 브레이커의 **전제 조건**이다. 그 페이지는 *"규칙 위반 시
스위치를 내린다"* 까지 있었고, [[Apache Map - Ch7 Ingestion and orchestration]]으로 *구현 자리는 DAG
태스크* 가 채워졌다. **이제 그 앞의 결정이 채워졌다** — 멈출지 알릴지를 정하지 않으면 알림만 쌓인다
(경고 피로). 세 장이 하나의 사슬을 완성한다.

## Atlas ↔ Ranger가 맞물리는 지점

**분류(Atlas)와 통제(Ranger)가 태그로 연결된다** — *"Atlas 태그를 이용해 '민감 태그가 붙은 컬럼은 특정
역할만 조회' 같은 규칙을 만든다."*

⭐ 이게 [[Apache Map - Ch7 Ingestion and orchestration]]에서 나온 **CDC의 PII 문제**에 대한 답의 형태다 —
CDC가 운영 DB의 모든 컬럼을 하류로 흘릴 때, **컬럼 태그 + 태그 기반 정책**이 그 컬럼을 가리는 장치다.
→ [[Change data capture]]

⚠️ Ranger의 한계도 명시된다 — **연동되지 않은 엔진에는 정책이 적용되지 않는다.** 클라우드 IAM·웨어하우스
자체 권한과 경계가 겹칠 수 있다. ⭐ 그래서 정할 것은 **"최종 권한 기준이 어디에 있는가."**

## ⚠️ BI가 거버넌스를 대신하지 않는다

> "Superset이 거버넌스를 대신하지는 않습니다. **잘못된 집계 정의, 중복 대시보드, 과도한 권한은 BI
> 안에서도 반복됩니다.** 카탈로그·권한·품질이 받쳐 줄 때 셀프서비스가 안전해집니다."

⭐ [[Data catalog and semantic layer]]의 **semantic layer**가 필요한 이유가 이것이다 — 지표 정의가
대시보드마다 흩어지면 셀프서비스는 *"같은 이름 다른 숫자"* 를 대량 생산한다. 그 페이지의
*카탈로그의 실패 모드는 '없음'이 아니라 '틀림'* 이 BI 층에서 재현되는 형태다.

**Superset vs Zeppelin**: 공유·운영 대시보드 vs 실험용 노트북. 흔한 배치는 **운영 리포트의 기준은 BI에,
깊은 탐색은 노트북으로 분리.** ⚠️ *"노트북만으로 전사 소비를 맡기면 버전 관리와 권한이 흐트러지기 쉽다."*

## 👍 강점 · ⚠️ 약점

**강점**

- 출처 없는 수치 **0건** — 6장 연속(Ch6·7·8·9·10, Ch1 포함).
- 8개 중 7개에 명시적 **한계** 줄. Ranger·Griffin·Polaris·Gravitino·Zeppelin 전부.
- ⭐ **"현대 대안"을 계속 병기한다** — Griffin 옆에 Great Expectations·dbt tests, Ranger 옆에 클라우드
  IAM·Lake Formation, Atlas 옆에 현대 카탈로그. **Apache 렌즈의 왜곡을 이 장은 스스로 보정한다.**
  Ch8(Trino)·Ch9(Elasticsearch)·Ch6(Delta)에서 이름만 흘렸던 것과 달리 여기서는 표에 넣는다.

**약점**

- ⚠️ 6장 연속 **내부 동작이 없다.** Ranger의 정책 평가 순서, Atlas의 계보 수집 방식(hook vs 파싱),
  Polaris의 커밋 프로토콜(REST 카탈로그가 원자적 커밋을 어떻게 보장하나)이 전부 이름 수준.
  Polaris의 커밋 프로토콜은 [[Table formats]]가 아직 못 채운 **Iceberg 온디스크 구조**와 같은 공백이다.
- ⚠️ **거버넌스의 조직 측면이 없다.** 삼각형 세 축의 **담당자**가 누구인지, 정책을 누가 승인하는지가
  없다. [[Apache Map - Ch7 Ingestion and orchestration]]이 *"누가 만들고 배포하는가"* 를 물었던 만큼
  이 장에서도 물을 수 있었는데 도구 배치까지만 간다.
- ⚠️ **PII·규제 이름이 하나도 없다**(GDPR·개인정보보호법 등). "민감 태그"라는 추상만 있다.

## 위키에 들어온 것

| | 페이지 |
|---|---|
| 새 엔티티 | **[[Apache Polaris]]**(Gravitino 흡수) · **[[Apache Superset]]**(Zeppelin 흡수) |
| 갱신 | [[Data catalog and semantic layer]] — **거버넌스 삼각형** 절 + **카탈로그 역할 구조** 절 + Ranger |
| | [[Data SLA and observability]] — Griffin + **"멈출지 알릴지 먼저 정하라"** |
| | [[Consumption layer]] — 사람에게 도달하는 마지막 칸(BI vs 노트북) |
| | [[SQL execution layer]] — 1️⃣ 테이블 규칙에 카탈로그가 필요하다는 지적 ✅ 확인 |
| | [[Spatial omics platform roadmap]] §2.2 — Postgres 결정 ✅ 확인 |
| 흡수 | Atlas·Ranger·Griffin → [[Data catalog and semantic layer]]·[[Data SLA and observability]] · Gravitino → [[Apache Polaris]] · Zeppelin → [[Apache Superset]] |

**승격 판단**: **Polaris** ✅(로드맵 결정과 직접 맞물리는 유일한 항목 + Hive Metastore 계보의 현재 지점) ·
**Superset** ✅(이 장 유일한 Tier 1 + 레이크하우스 기본 스택의 "화면" 칸 + Ch8 3단계의 3️⃣) ·
Atlas·Ranger·Griffin ⏸(**삼각형이 지식의 단위**라 떼면 삼각형이 부서진다) ·
**Hive Metastore ❌ 종결**(위 §미결 2).

## 다음

- **Ch2**(분산 기반 — ZooKeeper·YARN·HDFS·Ozone·YuniKorn·BookKeeper·Ratis) — 남은 최대 공백 중 하나(4/7).
  [[Replication and consensus]]가 Raft를 원리로 아는데 구현체 이름을 모르는 구간.
- **Ch11**(특화 라이브러리) — 7/9 공백. **Sedona**(대용량 지리공간)만 이 위키에 직접 걸린다.
- Ch3·Ch4·Ch5 — 공백이 0~2개. [[Apache Kafka]]·[[Apache Spark]]·[[Apache Flink]]·
  [[Columnar and in-memory data formats]]가 이미 덮고 있어 **보정·추가 확인 목적**의 인제스트가 된다.

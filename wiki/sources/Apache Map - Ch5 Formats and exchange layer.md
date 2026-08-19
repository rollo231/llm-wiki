---
type: source
title: Apache Map - Ch5 Formats and exchange layer
area: [data-engineering]
aliases: [Apache 지도 Ch5, Apache 지도 데이터를 담는 포맷과 교환 계층, Apache Map Ch5]
tags: [data-engineering, apache, parquet, orc, avro, arrow, book]
created: 2026-08-19
updated: 2026-08-19
sources: [raw/data-engineering/apache/apache-book-full-spread.pdf]
---

# Apache Map - Ch5 Formats and exchange layer

『Apache로 읽는 데이터 기술의 지도』(이현수, 2026) **Ch5. 데이터를 담는 포맷과 교환 계층** — 개념 8개,
PDF pp.34–42. 트래커: [[Apache data technology map (book)]].

공백 2/8. [[Columnar and in-memory data formats]]가 이미 Parquet·Avro·Arrow를 덮고 있었지만,
**그 페이지가 스스로 "여전히 없는 것"으로 적어 둔 항목이 하나 있었고 이 장이 그것을 채운다.**

## ✅ 오래된 공백 해소 — ORC vs Parquet

[[Columnar and in-memory data formats]]는 ORC를 표에 한 줄(*"Parquet과 같은 문제를 푸는 다른 포맷"*)로만
두고, **"여전히 없는 것: ORC와 Parquet의 실제 비교. 두 소스 모두 '같은 문제를 푸는 다른 포맷'에서
멈춘다"** 고 적어 두었다.

⭐ **답은 성능이 아니라 생태계였다.**

| | 출발점 | 잘 맞는 곳 |
|---|---|---|
| **Parquet** | 여러 엔진이 공유하는 **범용 표준** | 다중 엔진 레이크·레이크하우스. Spark·Hive·DuckDB·Trino 기본 지원 |
| **ORC** | *"Hive 테이블을 더 빠르고 작게"* | 온프레미스 Hadoop, **Hive Metastore 기반 웨어하우스** |

ORC는 **인덱싱·통계·압축을 파일 안에 적극적으로 넣어** 질의 엔진이 **불필요한 행 그룹을 건너뛰게**
한다 — 그 페이지의 §Predicate Pushdown과 같은 메커니즘이다.
⚠️ *"클라우드 레이크하우스와 다중 엔진 환경이 늘면서 신규 프로젝트는 Parquet 쪽이다."*
전환 전략도 준다: *"이미 ORC로 운영 중인 Hive 웨어하우스가 크다면 ORC를 유지하거나, **신규 경로부터**
Parquet으로 옮긴다."*

## ⭐ 비교 절 (개념 4) — 문장으로 고정하기, 다섯 번째

> "'무엇이 제일 좋은가'보다 **'지금 데이터가 어디를 지나는가'**를 먼저 묻는 편이 선택에 도움이 된다."
>
> **"교환은 Avro, 분석 저장은 Parquet, 기존 Hive는 ORC."**

⭐ [[Apache data technology map (book)]] §읽는 규칙 3(*처방은 항상 문장으로 적어 고정하라*)의 사례가
Ch7·Ch9·Ch10·Ch3에 이어 **다섯 번째**다. 여기서는 세 포맷을 한 줄로 배치한다.

⚠️ 그리고 **한 파이프라인에 셋을 동시에 쓸 수 있다**고 명시한다 — *"다만 단계마다 왜 그 포맷을 쓰는지가
분명해야 한다."* [[Columnar and in-memory data formats]]의 **"고르는 문제가 아니라 갈아타는 문제"**
(Avro로 받고 Parquet으로 묶기)와 같은 결론이다.

⭐ 그리고 Ch6으로 넘어가는 경계선을 미리 긋는다 — *"입문자는 '파일 포맷'과 '테이블 포맷'을 같은 종류의
도구로 보기 쉽다. Parquet·ORC·Avro는 **파일을 어떻게 쓰느냐**이고, Iceberg·Hudi는 그 파일들을
**테이블처럼 버전 관리**하는 이야기다."* → [[Table formats]]

## 위키에 새로 들어온 셋 — 계층이 다른 것들

포맷 이야기에 섞여 들어오지만 **각각 다른 층**이다.

### Arrow Flight SQL (🔸)

전통적인 **행 단위 프로토콜이 대량 결과에서 병목**이 되는 문제를 푼다. Flight(Arrow 배치를 네트워크로
스트리밍) 위에 SQL 질의·메타데이터 조회 인터페이스를 올린 계층 — **"질의를 보내고, 결과를 Arrow
스트림으로 받는다."**

⭐ **JDBC/ODBC의 대안**이고, **서버가 이미 Arrow로 연산 중이면 결과를 다른 포맷으로 바꾸지 않고 그대로
흘려보낸다.** [[Apache DataFusion]]·일부 웨어하우스가 이 경로를 지원한다.
→ [[SQL execution layer]] 3단계의 **3️⃣ 접속·소비**. 그 3단계에 **Arrow 경로**가 하나 추가된 셈이다.

⭐ 이로써 [[Apache DataFusion]]에 적어 둔 Arrow 생태계 사슬이 완성 확인됐다:
**Parquet(디스크) → Arrow(메모리) → Flight SQL(전송) → DataFusion(실행).**

### OpenDAL (🔸)

로컬 디스크·HDFS·S3 호환·Azure·GCS를 **하나의 API로**. 읽기·쓰기·목록 조회를 늘 같은 인터페이스로
호출하고 **설정만 바꿔 실제 저장소를 지정한다.**

⭐ 계층 구분이 한 문장으로 정리된다 — **"'파일을 어떻게 저장할까'가 아니라 '파일을 어디에서 읽고
쓸까'를 해결하는 계층."** 포맷(Parquet)·테이블(Iceberg) **아래**다. → [[Object storage layout]]

트래커 §실제 스택에 걸리는 항목에 올려 뒀던 항목이다. **평가: 지금은 해당 없음.** MinIO 하나만 쓰는
동안은 추상 계층의 값이 없다 — 값이 생기는 조건은 *"클라우드를 옮기거나 여러 클라우드를 함께 쓸 때"*
이고, [[Spatial omics platform roadmap]] §2.3이 이미 *MinIO 자체 호스팅이 파생물 전략을 제약한다* 고
적었으므로 **저장소를 늘리는 결정이 생기면 그때 다시 본다.**

### CarbonData (🔸)

인덱싱·압축·세부 메타데이터를 강조한 **특화 컬럼 포맷.** 쓰는 경우는 *"대용량 팩트 테이블에 다양한
필터가 걸리고 응답 시간이 중요할 때."*
⚠️ *"신규 레이크하우스의 기본값으로 고르는 팀은 Parquet·Iceberg 조합보다 적다"* — 생태계가 넓은
Parquet이 유리한 경우가 많다.
⭐ 요점은 제품이 아니라 분류다: **컬럼형에도 범용 표준(Parquet)과 특화 포맷이 나뉜다.**

## Parquet · Avro · Arrow — 확인만

[[Columnar and in-memory data formats]]가 이미 더 깊다(엔트로피 기반 압축 설명, predicate pushdown,
스키마 진화 규칙, GPU coalescing). 확인된 것:

- **Parquet** — *"분석 질의는 보통 전체 행이 아니라 필요한 몇 개 컬럼만 읽는다"* → 읽는 양이 줄고 압축도
  잘 된다. 입문 실습 제안까지 있다: *"CSV를 Parquet으로 바꾼 뒤 파일 크기와 조회 속도를 비교."*
- **Avro** — 스키마가 함께 움직이는 **행 지향** 교환 포맷. ⭐ 스키마 진화의 값을 구체적 장면으로 준다:
  *"**'어제 만든 생산자'와 '오늘 배포한 소비자'가 잠시 공존해도**, 스키마 호환 규칙이 있으면 장애를
  줄일 수 있다."* → [[Change data capture]]의 Schema Registry 논의와 같은 축.
- **Arrow** — *"디스크 위의 파일 포맷이 Parquet이라면, 메모리 안에서 같은 역할을 하는 표준."*
  ⭐ *"Parquet 파일을 읽을 때도 **최종적으로는 Arrow 형태의 배치로 올려 연산**하는 경우를 흔히 본다."*

## 👍 강점 · ⚠️ 약점

**강점**: 출처 없는 수치 **0건**(10장 연속 — 전 장 완료). **계층 구분이 이 장의 일관된 주제다** —
파일 포맷 / 테이블 포맷 / 접근 계층(OpenDAL) / 수송 계층(Flight SQL) / 특화 포맷(CarbonData)을
반복해서 갈라 놓는다.

**약점**: ⚠️ Parquet의 실제 구조(row group · page · dictionary encoding · min/max 통계)가 없다.
위키가 이미 더 깊고, **Ch6의 Iceberg·Ch3의 Kafka와 같은 패턴**이 세 번째로 반복된다 —
**이 책은 배치와 경계는 주고 구조는 주지 않는다.**

## 위키에 들어온 것

**새 페이지: source 1장뿐.** 기존 1곳 대폭 갱신:
[[Columnar and in-memory data formats]] — **§ORC vs Parquet**(오래된 공백 ✅ 해소) ·
**§세 포맷을 한 문장으로 고정** · **§파일 포맷 위·아래의 세 계층**(Flight SQL · OpenDAL · CarbonData) ·
ORC 표 행 수정 · 별칭 7개 추가.

**승격 판단**: 전부 ⏸. Flight SQL·OpenDAL·CarbonData는 **각각 한 계층을 가리키는 이름**이고, 그 계층
설명은 [[Columnar and in-memory data formats]]와 [[Object storage layout]]에 들어가는 것이 맞다.
⭐ 단 **OpenDAL은 저장소를 둘 이상 쓰기로 결정하는 시점에 재검토**한다.

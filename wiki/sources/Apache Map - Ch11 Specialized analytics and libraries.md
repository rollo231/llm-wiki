---
type: source
title: Apache Map - Ch11 Specialized analytics and libraries
area: [data-engineering]
aliases: [Apache 지도 Ch11, Apache 지도 특화 분석과 공통 라이브러리, Apache Map Ch11]
tags: [data-engineering, apache, geospatial, graph, ml, nlp, book]
created: 2026-08-19
updated: 2026-08-19
sources: [raw/data-engineering/apache/apache-book-full-spread.pdf]
---

# Apache Map - Ch11 Specialized analytics and libraries

『Apache로 읽는 데이터 기술의 지도』(이현수, 2026) **Ch11. 특화 분석과 공통 라이브러리** — 개념 9개,
PDF pp.95–104. 트래커: [[Apache data technology map (book)]]. **이 장으로 책을 완주한다.**

공백 7/9로 남은 최대 구간이었지만 성격이 다르다 — **대부분 주변부이고, 이 위키에 직접 걸리는 것은
[[Apache Sedona]] 하나다.** 대신 이 장은 **분류축 세 개**를 준다: 표준/이식 계층, ML의 실행 환경,
정확도 다이얼.

## ⭐⭐ 이 장의 유일한 실전 항목 — Sedona

> **"위치는 평범한 숫자 두 개가 아니다. 점·선·면의 거리, 포함, 교차 같은 **공간 관계**가 비즈니스
> 질문이 된다."**

Spark·Flink 위에서 **공간 인덱스**로 대용량 지리공간을 조인·집계한다.
⭐ 갈리는 축: **"기존 GIS 도구가 단일 머신·중규모에 강하다면, Sedona는 레이크·스트림 규모의 공간 ETL."**

### ⭐⭐⭐ [[Spatial aggregation]]의 기록된 제약과 정확히 맞물린다

그 페이지가 적어 둔 것:

> ⚠️ *"**points → shapes 집계는 모든 점을 메모리에 올린다.** docstring이 직접 경고하며 issue #210을
> 가리킨다. **전사체 단분자 규모에서는 실질적인 제약이다.**"*

**그 연산의 정체가 point-in-polygon 공간 조인이고, Sedona가 하는 일이 정확히 그것이다.**
[[Xenium]]·[[MERSCOPE]]의 단분자 좌표를 [[SpatialData Shapes element]]의 세포 폴리곤에 붙이는 작업이
지금은 단일 프로세스 메모리에 묶여 있다.

⚠️ **직접 연결되지는 않는다** — [[SpatialData]] store는 쿼리 엔진이 못 읽는 불투명 blob이므로
(Geo)Parquet 경유가 필요하고, 그 경로는 **미검증 설계**다. [[Apache Sedona]]에 4단계로 적어 두었다.
판단 기준은 소스가 준 것과 같다 — **한 store가 단일 머신에서 처리되면 그대로 두고, 레이크 규모가 되면
검토한다.** ⚠️ 그리고 *"단순 위경도 필터만 필요하면 일반 SQL로도 충분한 경우가 많다."*

⭐ **이것이 이 책을 읽은 전체 가치의 상당 부분이다** — bioinformatics 영역의 기록된 제약에
data-engineering 영역의 도구 이름이 붙었다. [[Wiki gap analysis - DE readiness]]가 지적한
*"두 영역이 서로를 참조하지 않는다"* 는 축에 걸린다.

## ⭐ 분류축 1 — 표준/이식 계층이라는 반복 패턴

**TinkerPop**은 그래프 DB가 아니라 **Gremlin 질의 언어 중심의 표준**이다 —
*"여러 그래프 저장소가 같은 질의 언어를 쓰게 만드는 표준."* ⚠️ 완결된 분산 DB 제품이 아니다.
**HugeGraph**가 그 표준을 구현한 분산 그래프 DB(OLTP 탐색 + OLAP 배치 분석).

⭐⭐ **그리고 이 형태가 이 책 전체에서 다섯 번 반복된다.**

| 층 | 표준/이식 계층 | 어디서 |
|---|---|---|
| 그래프 질의 | **TinkerPop / Gremlin** | Ch11 |
| SQL 파싱·최적화 | **[[Apache Calcite]]** | Ch8 |
| 처리 엔진 | **Apache Beam** | Ch4 |
| 메모리 표현 | **Arrow** | Ch5 |
| 저장소 접근 | **OpenDAL** | Ch5 |

**하나같이 설치 목록에는 잘 오르지 않고, "엔진을 바꿔도 같은 것을 쓸 수 있는가"를 파는 계층이다.**
그리고 대가도 같다 — Beam 항목이 대표로 말한 *"추상화 단계가 하나 더 생기는 셈이라 디버깅과 성능 튜닝
경로가 길어질 수 있다."* [[Graph database]]에 이 표를 적어 두었다.

## ⭐ 분류축 2 — ML은 어디서 돌리나

> *"모델을 어디에 둘지 고르기 전에 **데이터 규모와 실행 환경을 먼저 확인**하는 편이 좋다."*

| | 실행 환경 | 대표 |
|---|---|---|
| **분산 라이브러리** | 한 머신에 못 올리는 규모의 행렬·학습 | **Mahout** · Spark MLlib |
| **SQL 안에서** | **모델 계산을 데이터가 있는 곳에서.** 결과가 테이블로 남는다 | **MADlib** |
| **딥러닝 프레임워크** | 파라미터 동기화·분산 학습 전략 | **SINGA** · PyTorch · TensorFlow |

⭐⭐ **MADlib 쪽의 비자명한 선택 근거** — *"**모델이 SQL 결과와 같은 권한·거버넌스 경계 안에 있어야
할 때** 특히 유용하다."* 성능이나 편의가 아니라 **거버넌스 경계**가 실행 환경을 정한다.
→ [[Data catalog and semantic layer]]의 거버넌스 삼각형
⭐ MADlib의 원리는 [[Apache Hadoop]]의 MapReduce 전략(*"데이터를 계산기로 가져오지 말고, 계산기를
데이터가 있는 곳으로"*)을 ML에 적용한 것이다.

⭐ 그리고 역할 분리를 출발점으로 못 박는다 — **"피처는 레이크하우스에, 학습은 프레임워크에, 서빙은
별도 구성에. 각 역할(피처·학습·서빙)을 구분하는 것부터가 선택의 출발점이다."**
[[Feature store]]·[[ML data pipeline]]·[[Model serving platforms]]가 이미 그 셋이다.
[[MLOps]]에 절을 신설했다.

⚠️ Mahout·SINGA 자체는 *"신규 프로젝트의 기본값은 PyTorch·Spark MLlib·클라우드 AutoML인 경우가 많다"*
고 스스로 인정한다. 이 장이 이 셋을 넣은 목적은 제품이 아니라 **구분**이다.

## ⭐⭐ 분류축 3 — 오차 다이얼 (DataSketches)

*"정확한 유니크 수를 매번 전체를 저장해 계산하면, 스트림처럼 서로 다른 값이 매우 많은 데이터에서
비용이 크게 늘어난다."* **DataSketches**는 카디널리티·분위수·빈도를 **작은 스케치로 근사**한다.

- ⭐ **병합 가능** — 파티션·시간 구간 스케치를 **합쳐서** 확장한다.
- Druid·Pinot·웨어하우스·스트림 엔진이 **내부 또는 확장으로 활용**한다.
- ⚠️ **"정확한 조인·재무 결산에는 부적합, 대시보드·모니터링에는 잘 맞는다."**

> ⭐⭐ **"오차를 허용할 수 있는지부터 합의해 두면 된다."**

⭐ **[[Apache Map - Ch4 Batch and stream engines]]의 "최대 허용 지연을 숫자로 정하라"와 같은 형태의
처방이다.** 소비 층에는 미리 합의할 숫자가 **둘** 있다 — **허용 지연**과 **허용 오차.**
[[Consumption layer]]에 절을 신설했다.

## 나머지 둘

- **OpenNLP** — 토큰화·문장 분할·품사·개체명. ⭐ *"[[Apache Lucene|Lucene]]이 검색 색인이라면 OpenNLP는
  그 앞단의 언어 분석."* ⚠️ 최신 생성형 LLM·임베딩 스택의 대체가 아니다. → [[Apache Lucene]]에 절 추가.
- **Commons Math** — 통계·분포·선형대수·최적화 Java 라이브러리. *"데이터 엔지니어가 직접 다루는 경우는
  적어도 파이프라인과 서비스 코드의 **의존성으로** 자주 사용된다."* 위키에 페이지를 만들 이유는 없다.
  ⭐ 다만 대비 하나 — **DataSketches는 큰 데이터를 위한 특수 통계 요약, Commons Math는 범용 수치·통계.**

## ⭐ 책의 마지막 문장 — Ch1과 짝을 이룬다

> "Apache 데이터 기술은 수집·저장·처리·질의·거버넌스만이 아니라, 그래프·공간·ML·수치 라이브러리까지
> 포함합니다. **모든 영역을 다 쓸 필요는 없습니다. 해결하려는 문제에 필요한 기술만 고르면 됩니다.**"

⭐ Ch1이 *"Tier 2는 필요한 순간에 **사전처럼** 펼쳐 보면 됩니다"* 로 열었고, Ch11이 *"모든 영역을 다 쓸
필요는 없다"* 로 닫는다. **책이 자기 사용법으로 시작하고 끝난다** — 90개 항목 카탈로그가 완독물이
아니라는 것을 저자가 처음과 끝에서 두 번 말한다.

## 👍 강점 · ⚠️ 약점

**강점**: 출처 없는 수치 **0건 — 11장 전부, 책 전체에서 0건이다.** 9개 중 8개에 명시적 한계 줄.
⭐ **"이 책의 목적은 설치 가이드가 아니라 구분을 분명히 하는 데 있다"** 고 SINGA 항목이 직접 말한다 —
**주변부 항목을 넣은 이유를 스스로 설명하는 정직함.**

**약점**: ⚠️ Mahout·SINGA·Commons Math는 **현재 실무 가치가 낮다는 것을 인정하면서도 지면을 같은 크기로
쓴다.** 개념당 1페이지 고정 레이아웃의 부작용이고, 그래서 Sedona(직접 걸리는 항목)와
Commons Math(의존성 이름)가 **같은 비중으로 보인다.** ⚠️ 그리고 Sedona조차 공간 인덱스의 종류
(R-tree·quadtree·grid)나 조인 알고리즘이 없다 — **11장 연속 "배치와 경계는 주고 구조는 주지 않는다."**

## 위키에 들어온 것

| | 페이지 |
|---|---|
| 새 엔티티 | **[[Apache Sedona]]** (`area: [data-engineering, bioinformatics]` — 이 책에서 유일하게 두 영역에 걸치는 항목) |
| 갱신 | [[Spatial aggregation]] — 기록된 제약에 **분산 우회 경로** 연결 |
| | [[Graph database]] — **§질의 언어의 표준 계층**(TinkerPop·HugeGraph) + **표준/이식 계층 5종 표** |
| | [[Consumption layer]] — **§오차 다이얼**(DataSketches) |
| | [[MLOps]] — **§ML은 어디서 돌리나**(3갈래 + 거버넌스 경계) |
| | [[Apache Lucene]] — **§색인 앞단의 언어 분석**(OpenNLP) |

**승격 판단**: **Sedona ✅**(공간 오믹스와 DE를 잇는 유일한 항목 · [[Spatial aggregation]]의 기록된
제약에 직접 답한다). TinkerPop·HugeGraph ⏸([[Graph database]]가 집) · Mahout·MADlib·SINGA ⏸([[MLOps]]) ·
OpenNLP ⏸([[Apache Lucene]]) · DataSketches ⏸([[Consumption layer]]) ·
**Commons Math ❌**(페이지를 만들 이유가 없다 — 라이브러리 의존성 이름).

## 완주

**11/11.** 책 전체 총평과 남은 공백은 [[Apache technology map - what it gave and what it did not]].

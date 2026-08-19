---
type: entity
title: SedonaDB
area: [data-engineering, bioinformatics]
aliases:
  - sedonadb
  - Sedona DB
  - sedonadb-zarr
  - apache-sedona[db]
tags: [data-engineering, apache, sedona, rust, datafusion, arrow, geospatial, single-node, zarr, gpu]
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[Apache Sedona docs - Runtimes and GeoStats]]"
  - "docs/experiments/spatialdata-sedona/ (자체 실측, 2026-08-19)"
  - "docs/experiments/sedonadb-zarr-omengff/ (자체 실측, 2026-08-19)"
---

# SedonaDB

**공간 데이터를 1급 시민으로 다루는 단일 노드 분석 엔진.** [[Apache Sedona]]의 서브프로젝트이고,
별도 repo(`apache/sedona-db`)에 별도 사이트를 갖는다.

> *"SedonaDB is the first open-source, **single-node** analytical database engine that treats
> spatial data as a first-class citizen."*

```python
# pip install "apache-sedona[db]"   또는   conda install -c conda-forge sedonadb
import sedona.db
sd = sedona.db.connect()
sd.sql("SELECT … FROM cities JOIN countries WHERE ST_Intersects(…)").show()
```

## 무엇으로 만들어졌나

- **Rust** — JVM이 없다. 설치가 `pip install` 한 줄이다
- **[[Apache Arrow]] + [[Apache DataFusion]]** — 벡터화 실행 엔진을 물려받고 공간 타입·함수·조인을
  얹었다. *"without extensions or plugins"* 를 강조한다 (PostGIS·DuckDB Spatial과 대비되는 지점)
- **GeoArrow · GeoParquet · GeoPandas**와 직접 물린다
- API: SQL · Python(+ 0.4.0의 DataFrame API) · R(dplyr) · Rust

## ⭐ 위키에서 이 페이지가 갖는 의미 — 갈림축이 하나 사라졌다

[[Apache data technology map (book)]]가 준 Sedona의 갈림축은 이것이었다:

> *"기존 GIS 도구가 단일 머신·중규모에 강하다면, Sedona는 레이크·스트림 규모의 공간 ETL·분석."*

**SedonaDB가 그 축을 무효화한다.** Sedona가 단일 머신 자리를 직접 차지했으므로, 선택은
"GIS 도구 vs Sedona"가 아니라 **"어느 Sedona 런타임인가"** 가 된다. Flink 문서가 이를 직접 적는다 —
*"For small datasets, you may not need a distributed cluster and can use SedonaDB."*

실질적 결과: **[[Spatial aggregation]]의 issue #210 우회에 Spark 클러스터가 필요 없다.**
상세는 [[SpatialData and Sedona interop]].

## ⭐⭐⭐ `sedonadb-zarr` — 쿼리 엔진이 Zarr를 읽는다 (0.4.0)

이 위키에서 가장 큰 함의를 갖는 기능이다.

```python
# pip install sedonadb-zarr
import sedonadb_zarr
sd.register(sedonadb_zarr.ZarrExtension())
cube = sd.read(url, format=sedonadb_zarr.Zarr().with_options({"arrays": ["rain_ok"]}))
```

- **청크 하나 = 행 하나.** *"the storage layout **is** the data layout"*
- **픽셀에 lazy** — 차원 조회(`RS_DimNames`·`RS_Shape`·`RS_DimSize`·`RS_NumDimensions`)는 그룹
  스키마만 읽는 메타데이터 왕복이고 **픽셀 바이트를 가져오지 않는다**
- `RS_Slice`가 질의가 닿는 청크만 해석한다. `.show(5)`는 정확히 5개 청크만 건드린다
- `RS_Envelope`가 청크를 경계 기하로 바꾼다 → **픽셀을 디코딩하지 않고 청크 격자를 지도에 그린다**
- 래스터 타입 자체가 N차원이 됐다 (`time`·`level`·`band` 축)

⭐ **청크를 행으로 만든다**는 발상이 요점이다. [[Object storage layout]]의 ⑤*"한 prefix 아래 객체가
수백만 개면 `list-objects`가 실용적으로 불가능하다"* 를 **테이블로 다시 정의한 것**이다 — 청크
목록이 스캔 가능한 관계가 된다.

> ✅ **[[OME-NGFF]]/[[SpatialData]] 래스터로 실행 확인했다 (2026-08-19).** 읽는다 — 그리고 왜 되는지가
> 명확하다: **`ome` 속성을 파싱하지 않고 순수 Zarr로 읽는다.** 그래서 비표준 버전 문자열
> (`0.5-dev-spatialdata`)·비스펙 레벨 이름(`s0`/`s1`)·**CRS 없음(`srid = 0`)** 이 전부 무해하다.
>
> ⚠️ 같은 이유로 세 가지 한계가 따라온다:
> 1. **multiscale 그룹을 통째로 못 읽는다** — 레벨마다 청크 격자가 달라서 거부된다.
>    `arrays=["s0"]` 로 레벨 하나씩. (에러 메시지가 이 우회를 스스로 안내한다.)
> 2. **중첩 그룹을 재귀하지 않는다** — store 루트·컨테이너는 `has no child arrays`.
>    element 경로를 직접 열거해야 한다.
> 3. ⚠️⚠️ **`RS_Envelope`가 배열 인덱스 공간이고 y가 부호 반전된다** —
>    `POLYGON((0 -256, 256 -256, …))`. **`coordinateTransformations`를 무시하므로** 벡터와 맞추려면
>    y 반전 + scale 적용이 사용자 몫이다.
>
> ✅ **픽셀 lazy는 실측됐다** — 671MB(5×8192×8192 uint16) store에서 open 0.001s / `count()`(1,280청크)
> 0.003s / **전체 envelope 0.003s**, peak RSS가 인터프리터 기준선을 벗어나지 않는다.
> → [[SpatialData and Sedona interop]] §6 · `docs/experiments/sedonadb-zarr-omengff/`

## GPU 공간 조인 — RayBooster (0.4.0)

`ctx.sql("SET gpu.enable = true")` 한 줄로 켠다. VLDB 2026 (Industry Track) 논문이 뒤에 있다.

> *"Gaming GPUs contain dedicated **ray tracing cores** […] and they **sit idle during database
> queries.** Spatial joins are about finding intersecting geometries, which maps naturally onto ray
> tracing primitives."*

- **Structure of Arrays** 저장 — WKB(스트림 지향) 대신 offsets·vertices·types 분리 → O(1) 임의 접근
- **Z-stacking** — 기하 ID를 ray tracing scene의 미사용 Z축에 인코딩해 배치 전체에 **BVH 하나**만 만든다
- **`RelateEngine`** — RT 코어에서 **DE-9IM 행렬**을 계산해 *"500+ kernel variants"* 를 코드 경로
  하나로 대체
- 메모리 인식 스케줄링·스필

⭐ **RT 코어가 없는 H100보다 소비자용 RTX 3090이 일부 질의에서 빨랐다**고 명시한다.
[[GPU architecture]]의 *"연산 유닛이 문제 형태에 맞는가"* 축에 걸리는 사례다 —
[[NVIDIA RAPIDS]]가 CUDA 코어로 하는 것과 다른 하드웨어 자원을 쓴다.

⚠️ 성능 수치는 자체 벤치마크(SpatialBench)라 이 위키에 옮기지 않았다.

## 버전 상태 (확인일 2026-08-19)

| 태그 | 내용 |
|---|---|
| `apache-sedona-db-0.4.0` | 최신 릴리스. 187 이슈 · 26 신규 함수. conda-forge · Python DataFrame API · R dplyr · Geography · GeoParquet 쓰기 · **N차원 래스터 + `sedonadb-zarr`** · GPU 조인 |
| `apache-sedona-db-0.5.0.dev` | 개발 중 |

⚠️ **0.x다.** 초기 릴리스는 벡터 전용이었고 래스터가 0.4.0에서 들어왔다 — 표면이 빠르게 움직인다.
[[Apache Sedona]] 본체(1.9.1)와 **버전 체계도 릴리스 주기도 다르다.**

⚠️ 이 페이지의 내용은 전부 `apache/sedona` repo의 **블로그 포스트 2편에서** 온 것이다. SedonaDB
자체 문서 사이트는 아직 인제스트하지 않았다 (`raw/data-engineering/apache-sedona-docs/SOURCE.md`
참고). 다음 소스 후보 1순위.

## ⚠️ 실측에서 만난 함정 둘 (0.4.0, 2026-08-19)

[[SpatialData and Sedona interop]] 실험에서 나온 것이고, 둘 다 SpatialData 고유가 아니라
**GeoParquet·Arrow 를 읽는 일반적 상황에서 재현될 성질**이다.

### ① `crs: null` 을 `ogc:crs84` 로 채운다 → CRS 불일치로 조인 거부

GeoParquet 메타데이터가 `"crs": null`(= 미정의)인 컬럼을 읽으면 SedonaDB 는 타입을
**`geometry<WkbView(ogc:crs84)>`** 로 태깅한다. 반면 `ST_Point(x, y)` 가 만드는 기하는 CRS 가 없다.

```
SedonaError: type_coercion
caused by Error during planning: Mismatched CRS arguments: None vs ogc:crs84
Use ST_Transform() or ST_SetSRID() to ensure arguments are compatible.
```

⭐ **조용히 틀리지 않고 계획 단계에서 실패한다** — 좋은 설계다. 우회는 `ST_SetSRID(…, 4326)`(점 쪽)
또는 `ST_SetSRID(geom, 0)`(폴리곤 쪽 CRS 제거). 둘이 같은 답을 준다.

⚠️ 부작용: **비지리 평면 좌표(픽셀·마이크론)가 경위도로 라벨링된다.** 평면 술어에는 무해하지만
`ST_Transform`·Geography·`ST_DistanceSphere` 를 쓰면 의미가 틀어진다.

### ② dictionary 컬럼 GROUP BY + 조인 = `Dictionary key bigger than the key type`

Arrow dictionary(=pandas categorical) 컬럼으로 **조인 뒤 GROUP BY** 하면 깨진다. 컬럼 단독 조회·
단독 GROUP BY·비-dictionary 컬럼 GROUP BY 는 전부 정상이다.

⚠️ **규모 의존**: 200k행/25범주에서는 나지 않고 **1M행/100범주에서 났다.** 배치별 dictionary 가
병합될 때 int8 인덱스 범위(±127)를 넘는 것으로 보인다(⚠️ 추정, 업스트림 미확인).

처방은 토큰 하나 — **`CAST(col AS VARCHAR)`**. 비용은 미측정.

## DuckDB와의 대비

자체 SpatialBench 결과를 축으로만 옮기면:

> *"**DuckDB excels at spatial filters and some geometric operations** but faces challenges with
> **complex joins and KNN queries.**"*

⭐ 갈리는 지점이 **조인**이다 — [[Spatial join execution]]의 3층(격자·인덱스·refine)을 공간 전용으로
갖췄는지 여부. [[SpatialData as a data engineering substrate]] §3이 질의 층으로 DuckDB를 고른 근거는
*"gold는 그냥 컬럼너 테이블"* 이었으므로 유효하지만, **공간 조인이 필요한 순간 선택이 갈린다.**

## 링크

- 상위 프로젝트: [[Apache Sedona]]
- 기반: [[Apache DataFusion]], [[Columnar and in-memory data formats|Apache Arrow]]
- 개념: [[Spatial join execution]], [[GPU architecture]], [[Object storage layout]]
- 실측: `docs/experiments/spatialdata-sedona/` — 1M~50M 규모 곡선과 위 함정 둘의 재현 스크립트
- 응용: [[SpatialData and Sedona interop]], [[Spatial aggregation]]
- 출처: [[Apache Sedona docs - Runtimes and GeoStats]]
- 영역 MOC: [[Data Engineering]], [[Bioinformatics]]

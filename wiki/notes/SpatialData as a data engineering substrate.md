---
type: note
title: SpatialData as a data engineering substrate
area: [bioinformatics, data-engineering]
aliases:
  - SpatialData DE
  - SpatialData ETL
  - SpatialData 데이터 엔지니어링
  - SpatialData 카탈로그
  - spatial omics ETL
tags: [spatial-omics, data-engineering, zarr, lakehouse, iceberg, etl, catalog, data-format]
created: 2026-07-27
updated: 2026-07-28
sources:
  - "[[SpatialData docs - Design doc]]"
  - "[[SpatialData source - ShapesModel and shapes IO]]"
  - "[[SpatialData source - Shapes conversion and aggregation ops]]"
  - "[[spatialdata-io docs - README and readers]]"
  - "[[SpatialData source - Spatial and relational queries]]"
---

# SpatialData as a data engineering substrate

**질문:** [[SpatialData]] 포맷은 데이터 엔지니어링 관점에서 무엇이 이점인가? 그리고 그 위에
ETL을 세운다면 어떤 조합인가?

**답:** 이점은 레이크하우스의 **파일 포맷 층**에 있고 **테이블 포맷/웨어하우스 층**에는 없다.
SpatialData ≈ *공간 오믹스용 Parquet + 매니페스트 규약*이다 — Iceberg/Delta가 아니고, 웨어하우스는
더더욱 아니다. 그래서 **아키텍처의 임무는 포맷이 갖지 않은 세 가지를 공급하는 것으로 환원된다:
카탈로그 · 원자성 · 질의층.** 이 노트의 무게중심은 그중 카탈로그다(§4).

> ⚠️ §1~2는 위키 소스에 근거한 사실 정리다. §3 이후는 **설계 제안(의견)** 이며 이 프레임워크로
> 실제 측정된 바가 아니다. 근거 없는 추론은 §8에 모아 표시했다.

## 1. 저장 계층에서 실제로 얻는 것

Zarr store는 **서버가 없다.** 배열을 청크로 쪼개 각 청크를 개별 오브젝트로 두고, 스키마는 JSON
메타데이터로 옆에 붙인다. 오브젝트 스토리지에 올려 range GET으로 읽는다 — Parquet을 레이크하우스에서
쓰는 것과 동일한 property다.

| SpatialData/Zarr | 전통 DE 대응 | 성립 |
|---|---|---|
| Zarr 청크 + JSON 메타 | Parquet + 스키마 | ✅ 오브젝트 스토리지 직독, 부분 읽기 |
| bbox → 교차 청크만 GET | predicate pushdown | ⚠️ **래스터만.** 아래 참고 |
| multiscale 피라미드 | 집계 테이블 / MV | ✅ 스토리지로 읽기 비용을 산다 |
| dask lazy graph | Spark lazy DAG | ✅ 데이터 > 메모리가 기본 전제 |
| element별 포맷 버전 + 컨테이너 호환 행렬 | Iceberg format-version gating | ✅ 구조가 거의 같다 |
| `ShapesModel.validate()` | 스키마 계약(dbt contract 등) | ⚠️ 구멍 있음 (§5) |
| `region`/`region_key`/`instance_key` + 조인 5종 | FK + JOIN | ⚠️ 조인은 있으나 **정합성 강제는 없다** |
| `filter_by_table_query()` (`annsel` predicate) | `WHERE` 절 | ⚠️ 선언적 필터는 되나 SQL 엔진은 아니다 |
| store 디렉토리 | Iceberg 테이블(트랜잭션 로그) | ❌ 없음 |
| — | 카탈로그 / 멀티 데이터셋 질의 | ❌ 없음 |

> **정정 (2026-07-27, [[Spatial queries in SpatialData]] 인제스트 반영).** 이 노트의 초판은 청크
> 프루닝을 포맷 전반의 성질로 적었다. 소스 확인 결과 **element 종류마다 다르다**:

| element | 질의 구현 | I/O 가 실제로 주는가 |
|---|---|---|
| **Images·Labels** | bbox → intrinsic → `slice` → `image.sel()` | ✅ 예. dask lazy 슬라이싱 |
| **Points** | **`.compute()` 로 전량 materialize** 후 마스킹 | ❌ 아니오 |
| **Shapes** | `sindex` R-tree | ⚠️ 인메모리 인덱스일 뿐 (lazy loading 미구현) |

**points 는 어느 경로로 접근하든 전량 메모리에 올라간다** — `aggregate()`·`bounding_box_query()`·
`get_values()` 셋 다 `.compute()` 를 부른다. §6 청킹 전략과 아래 파이프라인 설계는 이 전제 위에 있다.

실질 이점 넷:

1. **N×M 컨버터 문제 제거.** [[spatialdata-io]]가 장비 13종의 native 출력을 하나의 canonical
   레이아웃으로 정규화한다. 설계 문서가 "포맷 컨버터를 만들지 않는다"를 non-goal로 박고
   [[OME-NGFF]]를 교환 포맷으로 채택한 근거가 이것이다 — 사실상 **bronze→silver 표준화**.
2. **element별 독립 포맷 버저닝 + 하위 호환 리더 보존** — [[SpatialData Zarr format versions]].
3. **스키마 계약이 코드로 존재** — 필수 컬럼, `radius > 0`, element 이름 제약, 예약어.
4. **다중 모달을 하나의 주소 지정 단위로.** 래스터(Zarr) + 벡터(GeoParquet) + 표(AnnData)가 한
   store에서 좌표계로 정렬된다. **DW에는 이걸 담을 자리가 없다** — [[Xenium]] 한 런이 50k×50k
   멀티채널 이미지 + 수억 행 transcript다. transcript는 Parquet 테이블 그 자체지만 이미지를
   BLOB 컬럼에 넣는 건 논외다. "왜 웨어하우스가 아니라 포맷인가"의 답.

## 2. 포맷이 주지 않는 것 = 요구사항 명세

- **트랜잭션 로그 없음** — ACID·스냅샷 격리·time travel·원자적 커밋 전부 없다. store는 디렉토리
  트리다. 동시 writer는 안전하지 않다.
- **round-trip이 포맷을 조용히 올린다** — 구버전 store를 읽고 다시 쓰면 현행 포맷으로 나간다.
  고정하려면 `formats=` 명시.
- **카탈로그 없음** — 1 store = 1 샘플. 파티셔닝·샘플 단위 프루닝 개념 자체가 없다.
- **SQL 엔진 없음** — DuckDB/Trino가 `shapes.parquet`·`points/*.parquet`는 읽지만 Zarr 래스터는
  의미 있게 못 읽는다. *단서*: 프레임워크 안에는 [[Relational queries in SpatialData|조인 5종과
  `filter_by_table_query()`]]가 있어 한 store 안에서는 관계형 필터가 된다. 없는 것은 **store 를
  가로지르는** 질의층이다.
- **점 데이터에 프루닝이 없다** — Points 질의는 전량 `.compute()` 한다
  ([[Spatial queries in SpatialData]]). [[Xenium]] 규모(수억 transcript)에서 이게 파이프라인
  설계를 지배한다.
- **하이브리드 포맷의 이음새** — `shapes.parquet`은 Zarr 계층의 일부가 **아니다**(그룹 디렉토리에
  얹혀 있을 뿐). 좌표변환은 parquet에 안 들어가고 Zarr 그룹 메타데이터에 따로 적힌다. 결과적으로
  **Zarr만 아는 도구는 shapes를 못 보고, Parquet만 아는 도구는 좌표변환을 못 본다.**
- **참조 정합성 미강제** — element 간 명시적 링크를 아예 저장하지 않는다
  ([[SpatialData elements]]). Tables→Regions도 강제되지 않는 soft FK.
- **small files 문제** — 청크가 개별 오브젝트라 수백만 객체가 된다. 해법인 Zarr v3 sharding은
  v0.8.0 문서 로드맵에 **미완**으로 남아 있다.

## 3. 제안 스택

가정: 샘플 수 수십~수천, 샘플당 10~100GB, 플랫폼 혼재, 오브젝트 스토리지 + K8s.

| 층 | 선택 | 이유 |
|---|---|---|
| 스토리지 | S3 호환 오브젝트 스토리지 | Zarr가 서버 없이 읽히는 전제 |
| 오케스트레이션 | **Airflow + KubernetesPodOperator**, dynamic task mapping | 작업 단위가 "샘플 1개"인 coarse-grained fan-out |
| 샘플 내 병렬 | **단일 fat pod + dask LocalCluster** | 배열 연산은 메모리 대역폭 바운드. 분산 dask는 실패 모드만 늘린다. 스케일아웃은 샘플 축에서 |
| 변환 | `spatialdata` + `spatialdata-io` | 장비 정규화 |
| 카탈로그 + gold | **Iceberg on 같은 오브젝트 스토어** | 없는 카탈로그를 평범한 테이블로 공급 |
| 질의 | **DuckDB** → 커지면 Trino | gold는 그냥 컬럼너 테이블 |
| 데이터 품질 | 커스텀 validation gate (§5) | 포맷 검증에 구멍이 있다 |

**Spark는 쓰지 않는다.** 이 파이프라인에 row-level 병렬성이 필요한 구간이 없다. 유일한 후보인
transcript points는 이미 Parquet이라 필요할 때 엔진이 직접 읽으면 된다.

### 레이아웃 — 불변 store + 포인터 플립

```
s3://omics/
├─ bronze/<platform>/<run_id>/…                  # 장비 원본, read-only
├─ staging/<dag_run_id>/<sample_id>.zarr         # 쓰기 대상
├─ silver/<sample_id>/<pipeline_ver>/sample.zarr # 검증 통과 후 promote, 이후 불변
└─ gold/  (Iceberg)  stores · store_elements · qc_metrics · cells_obs
```

**store를 절대 제자리 수정하지 않는다.** 이유 셋: (1) 원자적 커밋이 없어 쓰다 죽으면 반쯤 쓰인
store가 남는다 (2) round-trip이 포맷 버전을 올린다 (3) lazy loading이 기본이라 읽던 store를
덮어쓰면 dask 그래프가 가리키는 청크를 지우는 셈이다.

### 샘플 1개 DAG

```
extract    bronze 완결성(기대 파일 목록 + 체크섬)   → verify: 필수 파일 존재, 크기 ≠ 0
read       spatialdata-io 리더                      → verify: element 인벤토리가 플랫폼 기대치와 일치
normalize  좌표계 정렬, region_key/instance_key 통일 → verify: 모든 element가 extrinsic 좌표계에 매핑
write      staging/ 에 formats= 명시                → verify: 예외 없음
validate   재오픈 후 계약 검사 (§5)                  → verify: 전 항목 통과. 실패 시 promote 중단
derive     aggregate() → cell × gene · QC · extent  → verify: cell 수 > 0, gene 수가 기대 범위
promote    silver/ sync + 카탈로그 트랜잭션 (§4)     → verify: 카탈로그 경로로 store가 열림
publish    obs·QC를 gold에 append                   → verify: 행 수 == cell 수
```

**validate가 promote보다 앞에 있다** — 원자성이 없는 포맷에서 이게 유일한 방어선이다.

## 4. 카탈로그 — 이 아키텍처의 심장

### 4.1 왜 카탈로그가 세 문제를 동시에 푸는가

| 포맷의 결함 | 카탈로그가 공급하는 것 |
|---|---|
| 트랜잭션 로그 없음 | **promote = Iceberg 트랜잭션.** zarr 바이트에 ACID가 없어도 *"어느 store가 current인가"* 에는 ACID가 생긴다 |
| time travel 없음 | Iceberg 스냅샷 이력 = "3개월 전 이 샘플의 current는 무엇이었나" |
| 카탈로그 없음 | 멀티 샘플 질의가 그냥 SQL |
| 공간 인덱스 없음 | extent를 컬럼으로 두면 **store를 열기 전에 SQL에서 공간 프루닝**이 된다 (= zone map / min-max 인덱스를 포맷 한 층 위에 얹는 것) |
| element 간 링크 없음 | 인제스트 시점에 soft FK를 해석해 **포맷이 저장을 거부한 링크를 카탈로그가 저장**한다 |
| 포맷 버전이 하나가 아님 | element별 버전을 컬럼화 → 리더 호환성 판단에 store를 열 필요가 없다 |

핵심 전환: **진실의 원천은 디렉토리가 아니라 카탈로그 테이블이다.**

### 4.2 `stores` — grain: store 1개 = (sample, pipeline_version)

```sql
CREATE TABLE omics.stores (
  -- 식별 (자연키: sample_id + pipeline_version)
  store_id                STRING  NOT NULL,   -- 'S0142:v3.1.0'
  sample_id               STRING  NOT NULL,
  pipeline_version        STRING  NOT NULL,

  -- 계보 (lineage)
  platform                STRING,             -- xenium | visium | visium_hd | merscope
  vendor_software_version STRING,             -- ★ XOA 버전. Xenium은 XOA별 포맷이 다르다
  bronze_uri              STRING,
  bronze_checksum         STRING,             -- 재처리 판단 + 원본 변조 탐지
  store_uri               STRING  NOT NULL,
  dag_run_id              STRING,
  pipeline_git_sha        STRING,
  spatialdata_version     STRING,             -- 포맷 버전과 별개 (spatialdata_software_version)
  spatialdata_io_version  STRING,

  -- 포맷 계약: ★ element별로 따로. "이 store의 포맷 버전"이라는 단일 질문에는 답이 없다
  fmt_container           STRING,             -- '0.2'
  fmt_raster              STRING,             -- '0.3'
  fmt_shapes              STRING,             -- '0.3'
  fmt_points              STRING,             -- '0.2'
  fmt_tables              STRING,             -- '0.2'
  zarr_spec               INT,                -- 2 | 3
  is_sharded              BOOLEAN,
  shapes_geometry_encoding STRING,            -- 'WKB' | 'geoarrow'

  -- 공간 (→ 카탈로그 레벨 공간 프루닝)
  coordinate_systems      ARRAY<STRING>,
  extent                  STRUCT<xmin:DOUBLE, ymin:DOUBLE, xmax:DOUBLE, ymax:DOUBLE>,
  extent_cs               STRING,             -- 위 extent가 어느 좌표계 기준인가
  px_size_um              DOUBLE,

  -- 내용
  n_images INT, n_labels INT, n_shapes INT, n_points INT, n_tables INT,
  n_cells BIGINT, n_genes INT, n_transcripts BIGINT,

  -- 물리 (→ small-files 감시)
  store_bytes             BIGINT,
  n_objects               BIGINT,             -- 청크 오브젝트 개수
  max_multiscale_level    INT,

  -- 상태 기계
  status                  STRING,             -- staged|validated|current|superseded|quarantined
  is_current              BOOLEAN,
  validated_at            TIMESTAMP,
  promoted_at             TIMESTAMP,
  superseded_at           TIMESTAMP,
  validation_report       STRING              -- JSON
)
USING iceberg;
-- 파티셔닝하지 않는다. 행이 수천 개다. 과분할은 순수 손해.
```

### 4.3 `store_elements` — grain: element 1개

인벤토리를 `MAP<>` 한 컬럼에 넣지 않고 자식 테이블로 빼는 이유는 **element 단위 WHERE**가
필요하기 때문이다(마이그레이션 대상 찾기, 특정 타입만 fan-out).

```sql
CREATE TABLE omics.store_elements (
  store_id            STRING  NOT NULL,
  element_path        STRING  NOT NULL,       -- 'shapes/cell_boundaries'
  element_type        STRING,                 -- images|labels|shapes|points|tables
  element_name        STRING,
  format_version      STRING,                 -- 이 element의 SpatialData 포맷 버전

  -- 벡터 (shapes/points)
  geometry_type       STRING,                 -- Point | Polygon | MultiPolygon
  n_records           BIGINT,
  has_radius          BOOLEAN,

  -- 래스터 (images/labels) — 청킹 튜닝의 근거 데이터
  shape               ARRAY<BIGINT>,          -- [c, y, x]
  chunks              ARRAY<BIGINT>,          -- [1, 1024, 1024]
  dtype               STRING,
  n_multiscale_levels INT,

  -- 좌표
  coordinate_systems  ARRAY<STRING>,
  transform_type      STRING,                 -- Identity|Scale|Affine|Sequence

  -- ★ 포맷이 저장을 거부한 링크를 여기에 물질화한다
  annotated_by_table  STRING,                 -- 이 Regions를 주석하는 tables element
  region_key          STRING,
  instance_key        STRING,
  fk_integrity_ok     BOOLEAN,                -- instance_key 값이 실제로 존재하는지 검사 결과

  n_objects           BIGINT,
  bytes               BIGINT
)
USING iceberg;
```

`annotated_by_table`이 이 설계의 포인트다. 설계 문서는 *"이 Labels는 저 Image에 대응"* 을
저장하지 않고 좌표계로 묶으라고 한다 — 즉 **관계가 런타임 추론 대상**이다. 인제스트 때 한 번
해석해서 카탈로그에 박아두면, 다운스트림이 매번 store를 열어 좌표계를 비교하는 일이 사라진다.

### 4.4 `qc_metrics` — long format

```sql
CREATE TABLE omics.qc_metrics (
  store_id    STRING, metric STRING, value DOUBLE, unit STRING,
  threshold_lo DOUBLE, threshold_hi DOUBLE, passed BOOLEAN, measured_at TIMESTAMP
) USING iceberg;
```

wide가 아니라 long인 이유: 지표는 계속 추가된다. 새 지표마다 DDL을 바꾸지 않는다.

### 4.5 예시 행

```
stores:
  store_id                = 'S0142:v3.1.0'
  sample_id               = 'S0142'
  platform                = 'xenium'
  vendor_software_version = 'XOA-3.0'
  store_uri               = 's3://omics/silver/S0142/v3.1.0/sample.zarr'
  fmt_container='0.2' fmt_raster='0.3' fmt_shapes='0.3' fmt_points='0.2' fmt_tables='0.2'
  zarr_spec=3  is_sharded=false  shapes_geometry_encoding='WKB'
  coordinate_systems      = ['global']
  extent                  = {xmin:0, ymin:0, xmax:24012.5, ymax:18330.0}   -- µm
  n_cells=182_443  n_genes=541  n_transcripts=421_887_302
  store_bytes=68_211_998_720   n_objects=1_842_010    -- avg 37KB/객체 → 과분할 경고
  status='current'  is_current=true

store_elements (같은 store의 4행):
  shapes/cell_boundaries  shapes  0.3  Polygon  182443  annotated_by_table='table'
                                                        region_key='region' instance_key='cell_id'
  shapes/cell_circles     shapes  0.3  Point    182443  has_radius=true
  images/morphology       images  0.3  shape=[5,18330,24012] chunks=[1,1024,1024] levels=5
  points/transcripts      points  0.2  n_records=421887302
```

### 4.6 카탈로그가 실제로 답하는 질문

```sql
-- (1) 구버전 shapes 포맷 store 찾기 = 마이그레이션 대상. store를 열지 않고 SQL로.
SELECT store_id, store_uri, format_version
FROM store_elements
WHERE element_type = 'shapes' AND format_version IN ('0.1', '0.2');

-- (2) 공간 프루닝을 카탈로그에서. bbox 교차 판정을 store 열기 전에 끝낸다.
SELECT sample_id, store_uri FROM stores
WHERE is_current
  AND NOT (extent.xmax < :qxmin OR extent.xmin > :qxmax
        OR extent.ymax < :qymin OR extent.ymin > :qymax);

-- (3) small-files 감시. 청크 과분할이 조용히 비용을 태우는 걸 잡는다.
SELECT store_id, n_objects, store_bytes / n_objects AS avg_object_bytes
FROM stores
WHERE is_current AND store_bytes / n_objects < 1048576   -- 1MB 미만
ORDER BY n_objects DESC;

-- (4) ML 학습 셋 조립 → 이 결과가 fan-out 입력이 된다.
SELECT s.store_uri, e.element_path, e.chunks
FROM stores s JOIN store_elements e USING (store_id)
WHERE s.is_current AND s.platform = 'xenium' AND e.element_type = 'images'
  AND s.n_cells > 50000
  AND NOT EXISTS (SELECT 1 FROM qc_metrics q
                  WHERE q.store_id = s.store_id AND NOT q.passed);

-- (5) 재현성 — 이 결과를 만든 정확한 조합
SELECT pipeline_version, pipeline_git_sha, spatialdata_version, vendor_software_version,
       fmt_container, fmt_raster, fmt_shapes, fmt_points, fmt_tables
FROM stores WHERE store_id = :store_id;

-- (6) soft FK가 깨진 store 격리
SELECT store_id, element_path FROM store_elements WHERE fk_integrity_ok = false;
```

### 4.7 promote = 커밋

```sql
-- 원자성이 없는 포맷 위에서, 원자성은 이 트랜잭션이 공급한다.
BEGIN;
  UPDATE omics.stores
     SET is_current = false, status = 'superseded', superseded_at = current_timestamp()
   WHERE sample_id = :sid AND is_current;

  INSERT INTO omics.stores VALUES (..., 'current', true, ...);
COMMIT;
```

바이트는 이미 `silver/`에 불변으로 있고, 이 트랜잭션은 **어느 바이트가 유효한가**만 뒤집는다.
파이프라인 버전이 경로에 있으니 blue/green 재처리가 샘플 단위로 공짜다.

### 4.8 운영상 반드시 따라오는 두 가지

- **GC 잡이 별도로 필요하다.** Iceberg는 카탈로그 행만 관리한다 — `superseded` store의 바이트는
  아무도 지우지 않는다. 보존 기간 지난 superseded 행의 prefix를 삭제하는 잡이 없으면 스토리지가
  단조 증가한다.
- **카탈로그는 재구축 가능해야 하되, `is_current`만은 진짜 상태다.** 나머지 컬럼은 store를 스캔해
  복원할 수 있게 각 store 안에 작은 `_manifest.json`을 남긴다. 하지만 *"어느 버전이 current인가"* 는
  store에서 유도되지 않는다(최신 pipeline_version이 항상 정답은 아니다) → Iceberg 스냅샷 이력과
  백업으로 보호해야 하는 유일한 진짜 상태.

## 5. Validation gate — 포맷이 안 해주는 검사

- `ShapesModel.validate()` **+ `validate_shapes_not_mixed_types()` 를 명시적으로 호출.** 후자는
  비용 때문에 기본 검증 경로에서 호출되지 않고, `validate()`는 첫 행 타입만 본다
  ([[SpatialData Shapes element]]).
- **`radius`에 NaN/inf 없음** — 현재는 경고에 그치고 다음 릴리스에서 `ValueError`로 승격 예정.
  과거 [[Xenium]] 데이터에서 실제로 발생한다.
- **soft FK 정합성** → `fk_integrity_ok`. 프레임워크에 검사 수단이 **없다** —
  [issue #218](https://github.com/scverse/spatialdata/issues/218)이 `validate_data_relationships()`를
  제안한 게 2023-04-05인데 아직 미해결이다. 그 이슈가 나열한 검사 목록을 그대로 쓰면 된다:
  - `table.uns['spatialdata_attrs']['region']`의 region이 store에 실제로 존재하는가
  - `region_key` 컬럼이 존재하는가 / 그 값들이 선언된 `region` 집합과 **정확히** 일치하는가
  - `instance_key` 컬럼이 존재하는가 / 그 값들이 대응 Regions element의 인덱스와 일치하는가
- **extent가 물리적으로 말이 되는가** — 좌표변환 스케일 실수 탐지.
- **element 이름 규칙** — 대소문자만 다른 이름 금지(case-insensitive 파일시스템 충돌), `_index` 예약어.
- **다중 region 테이블의 행 순서** — v0.8.0 리그레션(issue #1162)이 `filter_table=True` 경로에서
  `obs`를 region별로 재정렬한다. 파이프라인이 테이블 행과 지오메트리의 위치 대응을 가정한다면
  promote 전에 순서를 단언해야 한다. 상세는 [[Relational queries in SpatialData]].

## 6. 청킹 — 성능이 결정되는 유일한 곳

나머지는 배관이고 여기가 승부처다. 청크 shape을 접근 패턴에 맞춘다.

| 소비자 | 전략 |
|---|---|
| 시각화(napari·웹 뷰어) | 타일형 `(C, 512~1024, 512~1024)`, multiscale 충분히 깊게 |
| ML 패치 학습 | 패치 크기의 배수, 채널 축은 통째로 |
| 공간 질의 | bbox 크기 중간값에 맞춤 |

둘 다 필요하면 **silver에 두 가지 청킹으로 두 번 쓴다.** 스토리지가 컴퓨트보다 싸다 — DW에서 같은
사실을 여러 집계 테이블로 중복 저장하는 것과 같은 판단.

Zarr v3 sharding이 실사용 가능한지가 이 절의 전제다(§8). 안 되면 청크를 의도적으로 크게(수 MB~수십
MB) 잡아 객체 수를 누른다.

## 7. 하지 않을 것

- ❌ **spatialdata store를 Iceberg/Delta 안에 넣기.** 테이블 포맷은 Parquet 파일을 관리하며 zarr
  계층은 관리 대상이 아니다. **store에 *대한* 카탈로그를 만들되, store의 카탈로그를 만들지 않는다.**
- ❌ **`zarr.copy_store` 류로 store 이동.** `shapes.parquet`은 Zarr 계층 밖이라 zarr만 아는 도구는
  **shapes를 조용히 빠뜨린다.** 반드시 `aws s3 sync`/`rclone` 같은 평범한 오브젝트 동기화.
- ❌ **`formats=` 미지정 쓰기** — 조용한 버전 업그레이드로 구버전 호환이 깨진다.
- ❌ **동시 writer로 한 store 쓰기** — 격리가 없다.
- ❌ **cell × gene 행렬을 웨어하우스 테이블로 밀어넣기** — obs 수준 지표와 QC만 Iceberg로,
  행렬은 AnnData/zarr 네이티브로 남긴다.
- ❌ **Spark로 샘플 변환** / ❌ **커스텀 메타데이터 서비스 구축**(테이블 하나로 충분).
- ❌ **`points`를 파이썬에서 직접 조작** — dask ≥ 2025.2.0에서 에러
  ([[SpatialData]] 알려진 함정 참고).

## 8. 미검증 — 확인해야 할 것

### 확인 완료 (2026-07-27)

- ~~**질의가 실제로 청크 프루닝을 하는가**~~ → **답: 래스터만.** §1의 정정 박스 참고.
  소스: [[Spatial queries in SpatialData]].
- ~~**Zarr v3 sharding 현황**~~ → **여전히 미완으로 보인다.** v0.8.0이 접근일 기준 최신 태그이고,
  2025 로드맵 4개 항목이 v0.7.2~v0.8.0 릴리스 노트에 전혀 등장하지 않는다. (릴리스 노트 부재는
  강한 정황이지 결정적 증거는 아니다.) → §6의 "청크를 크게 잡아 객체 수를 누른다"가 현재 경로.
- **덤**: v0.8.0이 지원 Python을 **3.12/3.13/3.14로 이동**(PR #1151) — 컨테이너 베이스 이미지 제약.

### 남은 미검증

- **`dataloader` API** — 존재는 알지만 미이관([[SpatialData]] 문서 트래커). v0.8.0에 "improves
  dataloader performance"(PR #687)가 들어갔다. ML 로딩을 직접 zarr로 할지 라이브러리 loader로
  할지 미결. **현재 1순위.**
- **points 전량 메모리 문제의 우회 레시피.** `aggregate()`(issue #210)뿐 아니라 질의 경로도 같다는
  게 확인됐으므로, [[Xenium]] 규모에서 `derive` 단계는 그대로는 안 돌 가능성이 높다. 청크·타일
  단위로 잘라 집계하는 실제 레시피가 필요하다.
- **lazy read + in-place write 위험은 설계로부터의 추론**이다 — 라이브러리가 이를 막는 가드를
  두는지는 소스 미확인.
- **Iceberg가 개념 수준으로만 위키에 있다.** [[Table formats]]가 ACID·스키마 진화·time travel이
  왜 *테이블 포맷 층*의 기능인지까지는 세웠지만, Iceberg vs Delta vs Hudi 선택 기준과 스냅샷·
  매니페스트의 온디스크 구조는 여전히 없다 — §4 카탈로그 설계를 **검증**하려면 Iceberg 1차 문서가
  필요하다 ([[Data Engineering]] MOC 열린 질문 참고).
  - 용어 정정 하나: 이 노트가 "카탈로그"라 부르는 것은 [[Data catalog and semantic layer]] 기준으로
    **metastore(기계용)** 이지 사람용 data catalog가 아니다. gold 층을 겸하고 있어 둘이 붙어 있다.
- **모든 수치**(청크 크기, 1MB 임계, 샘플 규모)는 일반적 경험값이며 이 프레임워크로 측정된 것이
  아니다.

## 링크

- 프레임워크: [[SpatialData]] · 사양: [[OME-NGFF]]
- 포맷 상세: [[SpatialData Zarr format versions]], [[SpatialData Shapes element]],
  [[SpatialData elements]], [[Coordinate systems and transformations]]
- 질의: [[Spatial queries in SpatialData]], [[Relational queries in SpatialData]]
- 연산: [[Spatial aggregation]], [[Rasterization and vectorization]]
- 적재: [[spatialdata-io]] → [[Visium]], [[Visium HD]], [[Xenium]], [[MERSCOPE]]
- DE 개념: [[Analytical data storage tiers]], [[Table formats]], [[Medallion architecture]],
  [[Columnar and in-memory data formats]], [[Data catalog and semantic layer]],
  [[Batch and stream processing]], [[Traditional data engineering]], [[AI data engineering]]
- 영역 MOC: [[Bioinformatics]], [[Data Engineering]]

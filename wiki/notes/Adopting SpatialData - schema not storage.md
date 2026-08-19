---
type: note
title: Adopting SpatialData - schema not storage
area: [bioinformatics, data-engineering]
aliases:
  - SpatialData 채택 판단
  - SpatialData 를 꼭 써야 하나
  - SpatialData vs 벤더 네이티브
  - h5ad ome.tiff parquet 직접 처리
  - 포맷 채택 판단
tags: [spatial-omics, data-engineering, architecture, decision, data-format, medallion, geoparquet, ome-tiff, anndata]
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[SpatialData docs - Design doc]]"
  - "[[SpatialData source - ShapesModel and shapes IO]]"
  - "[[spatialdata-io docs - README and readers]]"
  - "[[SpatialData and Sedona interop]]"
  - "[[SpatialData as a data engineering substrate]]"
  - "[[Spatial omics platform roadmap]]"
  - "docs/experiments/spatialdata-sedona/ · docs/experiments/sedonadb-zarr-omengff/"
---

# Adopting SpatialData - schema not storage

**질문:** [[SpatialData]] 포맷을 **꼭 써야 하나?** 아니면 장비가 내놓는 것(`h5ad` · `ome.tiff` ·
polygon parquet)을 그대로 받아 **내 데이터 엔지니어링 아키텍처로 처리**하면 되는가?

**답:** **저장소로 채택하지 말고 스키마로 채택한다.** 리더와 데이터 모델은 사고, `.zarr` store는
**분석가용 산출물**로만 두고, 엔진이 읽는 층은 별도로 세운다.

> ⚠️ **근거 구분.** §1~§2는 위키 소스와 실측에 근거한 사실이다. §3 이후는 **설계 판단(의견)** 이며
> 이 스택에서 운영해 본 결과가 아니다. [[Spatial omics platform roadmap]]의 기존 결정과 어긋나는
> 곳은 §6에 모아 표시했다.

## 1. ⭐ 먼저 재구성 — "SpatialData"는 하나가 아니라 넷이다

"쓸까 말까"가 답이 안 나오는 이유는 **분리 가능한 것을 묶어서 묻고 있기** 때문이다.

| 부분 | 실체 | 직접 만드는 비용 | 판정 |
|---|---|---|---|
| **[[spatialdata-io]] 리더** | 장비 13종 → 하나의 인메모리 표현 | **높다** (N×M + 벤더 버전 드리프트) | ✅ **산다** |
| **데이터 모델** ([[SpatialData elements]] 5종, [[Coordinate systems and transformations\|좌표계]], `region`/`region_key`/`instance_key`) | 스키마·어휘 | **가장 높다** — 좌표계가 제일 어렵다 | ✅ **산다** |
| **온디스크 store** (`.zarr` + 얹힌 parquet) | 영속화 선택 | **낮다** — Parquet·Zarr는 commodity | ⚠️ **silver의 한 표현으로만** |
| **에코시스템** (`napari-spatialdata`, `spatialdata-plot`, Squidpy, `dataloader`) | 분석가 도구 | 대체 불가 | ✅ (그래서 store가 필요하다) |

⭐ **결정적 사실**: `spatialdata_io.xenium(path)`는 **인메모리 `SpatialData` 객체를 돌려주고
`.write()`는 별도 호출**이다. **리더와 모델의 값을 저장 포맷 약속 없이 가져올 수 있다.**
이 한 줄이 이 노트 전체의 축이다.

그리고 [[SpatialData and Sedona interop]]가 실측으로 확인한 것 — **store의 잠금이 얇다**:
`points.parquet`은 평범한 Parquet, `shapes.parquet`은 GeoParquet 1.0.0, 래스터는 순수 Zarr다.
**나가는 문이 열려 있다**는 뜻이고, 동시에 **들어올 이유도 저장소 자체는 아니라는 뜻**이다.

## 2. 아키텍처 층위로 답하기

이게 실제 질문이다 — *"이 포맷이 내 아키텍처의 어느 층을 채우는가."*

| 층 | SpatialData가 채우나 |
|---|---|
| 파일 포맷 ([[Columnar and in-memory data formats]]) | ✅ Parquet+Zarr 위의 규약 |
| 테이블 포맷 — ACID·스냅샷·time travel ([[Table formats]]) | ❌ |
| 카탈로그 / 메타스토어 ([[Data catalog and semantic layer]]) | ❌ |
| 질의 엔진 ([[SQL execution layer]]) | ❌ |
| 오케스트레이션 ([[Data orchestration]]) | ❌ |
| 스키마 계약 | ⚠️ 부분 — 검증에 구멍이 있다 ([[SpatialData as a data engineering substrate]] §5) |
| **도메인 어휘 · 좌표계 정렬** | ✅✅ **유일한 독점** |

⭐⭐ **한 줄 판정: SpatialData는 인프라가 아니라 도메인 스키마다.** 아키텍처의 **빈 층을 채우지
않는다** — bronze→silver 정규화와 좌표계 어휘를 채운다. 그래서 "꼭 써야 하나"는 **"어느 부분을
쓰나"** 로 바꿔 물어야 한다.

### ⚠️ 반대편도 정직하게 — 직접 처리하면 무엇이 아픈가

장비 출력은 **서로 닮지 않았다.** 그 차이가 정확히 리더가 흡수하는 것이다.

| 플랫폼 | 좌표 정렬을 어떻게 주는가 |
|---|---|
| [[Xenium]] | µm 좌표 + `pixel_size` → 스케일 하나. XOA 버전마다 레이아웃이 다르다 |
| [[MERSCOPE]] | transcript가 **CSV**, affine이 **별도 CSV 파일**(`micron_to_mosaic_pixel_transform`) |
| [[Visium]] | `scalefactors_json.json` + PNG. hires/lowres가 각자 스케일을 갖는다 |

[[Spatial omics platform roadmap]] §1(c)가 이미 세어 둔 대로, 플랫폼을 3종으로 고정해도 **버전
매트릭스가 남고** 그중 둘은 *재현성을 조용히 깨는* 종류다. **리더를 직접 쓰는 것은 이 매트릭스를
사는 것**이고, 이 위키에서 가장 확실한 매수 지점이 여기다.

## 3. 추천 — 이중 표현 silver

```
bronze/  벤더 원본, 불변, read-only
silver/  같은 파이프라인이 두 표현을 낳는다
  ├─ <sample_id>/<pipeline_ver>/sample.zarr   ← SpatialData. 분석가·napari·Squidpy용.
  │                                              재생성 가능한 산출물로 취급한다
  └─ canonical/                                ← 엔진이 읽는 층
      ├─ transcripts/   Iceberg (sample_id 파티션 + 공간 정렬)
      ├─ cells/         GeoParquet (geometry + cell_id)
      ├─ transforms/    ★ 좌표변환을 테이블로
      └─ images/        벤더 OME-TIFF 참조 (변환하지 않는 것을 기본값으로)
gold/    Iceberg 팩트 테이블
카탈로그: Postgres  ([[Spatial omics platform roadmap]] §2.2 결정 유지)
```

근거 셋:

### 3.1 소비자가 둘이다

분석가는 `SpatialData` 객체를 먹는 도구를 쓰고, 엔진은 컬럼너 테이블을 읽는다. 하나로 둘을
만족시키려는 시도가 이 논의를 어렵게 만든다. **storage < compute** 는 이 위키가 이미
[[SpatialData as a data engineering substrate]] §6에서 내린 판단이다 — *"둘 다 필요하면 silver에
두 가지 청킹으로 두 번 쓴다."* 같은 논리를 표현 축으로 확장한 것이다.

### 3.2 ⭐⭐ 좌표변환을 테이블로 승격한다 — 이번 실험의 가장 실용적인 결론

실측이 밝힌 두 가지:

- **변환은 Parquet 안에 없다.** writer가 `attrs["transform"]`을 지우고 쓰고, 변환은
  `<element>/zarr.json`의 `attributes.coordinateTransformations`에 따로 간다
  → **Parquet만 아는 도구는 좌표변환을 못 본다.**
- **element 간에 어긋날 수 있다.** 리더 15종 전수 조사에서 **`seqfish`가 반례**였다 — transcripts는
  `Identity`, 세포 경계 폴리곤은 `Scale`. **에러 없이 틀린 답이 나온다.**

⭐ 이 둘을 합치면 처방이 하나로 정해진다 — **변환을 파일 규약이 아니라 테이블로 둔다.**
그러면 조인 전 단언이 **SQL이 되고**, 카탈로그가 이미 하려던 일
([[SpatialData as a data engineering substrate]] §4.3의 `annotated_by_table`·`fk_integrity_ok`와
같은 성격)에 자연스럽게 붙는다. **포맷이 저장을 거부한 관계를 카탈로그가 저장한다**는 그 노트의
논지와 정확히 같은 형태다.

| 컬럼 | 예 |
|---|---|
| `store_id` · `element_path` | `S0142:v3.1.0` · `points/transcripts` |
| `target_cs` | `global` |
| `transform_type` | `Identity` / `Scale` / `Affine` / `Sequence` |
| `matrix` | 계수 (JSON 또는 배열) |
| `input_axes` · `output_axes` | `[x, y]` |

⚠️ 미검증: `Sequence` 변환과 다중 좌표계 store에서 이 스키마가 충분한지는 확인하지 않았다.

### 3.3 이미지는 **변환하지 않는 것**을 기본값으로

벤더는 OME-TIFF를 준다([[Xenium]] `morphology.ome.tif`, [[MERSCOPE]] mosaic TIFF).
Zarr로 옮기는 것은 **전체 재기록 + small-files 문제를 사는 것**이다 —
[[SpatialData as a data engineering substrate]] §2가 기록한 대로 해법인 Zarr v3 sharding은
**로드맵에 미완**으로 남아 있고, [[Object storage layout]] ⑤가 그 결과를 이미 적어 뒀다.

⭐ 그리고 **DE 생태계는 TIFF/COG 도구가 더 많다** — [[Apache Sedona]] 1.9는 GeoTiff **자동 타일링
리더**(Spark 2GB 레코드 한계 우회)와 `RS_AsCOG`를 갖는데, `sedonadb-zarr`는 **OME-NGFF를 해석하지
않는다**([[SpatialData and Sedona interop]] §6 — envelope이 배열 인덱스 공간이고 좌표변환을 무시한다).

⚠️ 대가: 뷰어가 피라미드를 원하면 어차피 파생물을 만들어야 한다. 그건 **트리거가 왔을 때**
([[Spatial omics platform roadmap]] Phase 2) 만드는 것이고, **인제스트 시점의 기본값이 될 이유는 없다.**

## 4. 언제 무엇을 도입하나

| 신호 | 판정 |
|---|---|
| 플랫폼 1종 · 벤더 버전 고정 · 샘플 수십 | **store만으로 충분.** canonical 층을 만들지 말 것 |
| 플랫폼 3종 (로드맵 확정) | **리더 필수.** canonical 층은 아래 신호까지 보류 |
| **여러 샘플을 가로지르는 질의가 실제로 요청된다** | canonical 층 도입 |
| transcript 수천만↑ **+ 재세그멘테이션** | canonical 층 + [[SedonaDB]] ([[SpatialData and Sedona interop]] §7) |
| 분석가가 napari / Squidpy를 쓴다 | **store 유지.** 버리지 말 것 |

⭐ **정렬 축은 로드맵과 같다 — "되돌릴 수 있는가."** canonical 층은 store에서 재생성 가능하므로
늦게 도입해도 싸다. 반대로 **store를 안 만들고 시작하면 에코시스템을 잃고, 그건 되돌리기 비싸다.**
즉 **비대칭이 명확하다: store는 먼저, canonical은 나중.**

⚠️ 그리고 조인 자체의 필요를 과대평가하지 말 것 — [[Xenium]] `transcripts.parquet`에는 **벤더가
이미 `cell_id`를 넣어둔다.** 공간 조인이 값을 하는 건 **경계가 새로 생겼을 때**뿐이다.

## 5. `h5ad`에 대해서만 따로

`h5ad`/`AnnData`는 **cell × gene 표에는 여전히 맞고, 공간 정렬에는 안 맞는다.**

`obsm["spatial"]`은 SpatialData가 **명시적으로 폐기한 관례**다
([[Legacy AnnData spatial convention]]) — 좌표계도, 변환도, 다중 element도 담지 못한다.
[[SpatialData elements]]가 *"`Tables`는 좌표계를 가질 수 없다"* 고 못박은 것이 그 선언이다.

⭐ 깔끔한 분업이 나온다:

| 무엇 | 어디에 |
|---|---|
| cell × gene 행렬 | `AnnData` / zarr 네이티브 (**웨어하우스로 밀지 않는다**) |
| 공간 정렬·좌표계 | SpatialData **모델** |
| 질의·조인 | Parquet / GeoParquet / Iceberg |
| 픽셀 | 벤더 OME-TIFF (파생물은 트리거 시) |

## 6. 기존 페이지와의 관계

**모순 없음. 두 곳을 일반화하고 한 곳을 강화한다.**

- **일반화** — [[Spatial omics platform roadmap]] §8.1이 이미 *"transcripts를 store 밖에 공간 파티션
  Parquet으로 한 벌 더 둔다"* 고 결정했다. **§3의 canonical 층은 그 결정을 transcript에서 element
  전체로 확장한 것**이고, 새 판단이 아니다. 트리거도 그쪽 Phase 5(조건부)를 따른다.
- **일반화** — [[SpatialData as a data engineering substrate]] §6의 *"두 가지 청킹으로 두 번 쓴다"*
  를 **표현 축**으로 확장한다.
- **강화** — 같은 노트 §7의 ❌ 목록(*store를 Iceberg 안에 넣지 않는다*, *cell × gene을 웨어하우스로
  밀지 않는다*)은 그대로 유효하고, **§3.3이 하나를 추가한다: 이미지를 Zarr로 변환하는 것을
  기본값으로 삼지 않는다.**

## 7. 하지 말 것

- ❌ **store를 Iceberg/Delta 안에 넣기** — 테이블 포맷은 Parquet 파일을 관리하고 Zarr 계층은
  관리 대상이 아니다
- ❌ **store를 진실의 원천으로 두기** — 진실은 카탈로그다. `is_current`만이 진짜 상태다
- ❌ **이미지 Zarr 변환을 기본값으로** — 근거 없이는 small-files를 사는 것
- ❌ **13개 리더를 직접 쓰기** — 여기가 유일하게 확실한 매수 지점이다
- ❌ **규모를 이유로 `aggregate()`를 미리 버리기** — 수백만까지는 그게 정답이다
- ❌ **`zarr.copy_store` 류로 store 이동** — `shapes.parquet`이 Zarr 계층 밖이라 조용히 빠뜨린다

## 8. 미검증

1. **`transforms` 테이블 스키마** (§3.2) — `Sequence` 변환·다중 좌표계 store에서 충분한가.
2. **OME-TIFF를 유지하는 경로의 읽기 성능** — 타일드·피라미드 TIFF의 range GET이 실제로
   Zarr 청크와 견줄 만한가. 측정하지 않았다.
3. **canonical 층의 유지 비용** — 두 표현의 정합성을 무엇이 보장하는가(재생성 잡? 검증 게이트?).
4. **Squidpy의 SpatialData 경로** — 문서 시점 P2·미완. 에코시스템 논거의 강도가 여기에 달려 있다.
5. 이 노트 전체가 **설계 판단**이며 이 스택에서 운영해 본 결과가 아니다.

## 링크

- **자매 노트** — [[SpatialData as a data engineering substrate]](포맷이 무엇을 주고 안 주는가) ·
  [[Spatial omics platform roadmap]](도입 순서와 트리거) ·
  [[SpatialData and Sedona interop]](이 노트의 실측 근거)
- 프레임워크: [[SpatialData]] · [[spatialdata-io]] · [[OME-NGFF]]
- 모델: [[SpatialData elements]], [[Coordinate systems and transformations]],
  [[SpatialData Shapes element]], [[SpatialData Zarr format versions]],
  [[Legacy AnnData spatial convention]]
- 연산: [[Spatial aggregation]], [[Spatial join execution]]
- 엔진: [[SedonaDB]], [[Apache Sedona]]
- DE 개념: [[Table formats]], [[Columnar and in-memory data formats]],
  [[Analytical data storage tiers]], [[Medallion architecture]], [[Object storage layout]],
  [[Data catalog and semantic layer]], [[ETL and ELT]], [[Data orchestration]]
- 플랫폼: [[Xenium]], [[MERSCOPE]], [[Visium]], [[Visium HD]]
- 영역 MOC: [[Bioinformatics]], [[Data Engineering]]

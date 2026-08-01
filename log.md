# Log

Chronological record of wiki activity. Append-only; the newest entry goes at the bottom.
Each entry follows the format: `## [YYYY-MM-DD] <ingest|query|lint> | <title>`

## [2026-07-19] schema | Reset to clean slate

Reorganized `raw/` into per-area subfolders and added the `data-engineering` area, then
removed the initial worked examples (Squidpy pages + raw source) and prior working docs to
start fresh. The vault now holds only the schema and one raw source awaiting ingest.

## [2026-07-19] ingest | AI DE Course - Ch1-1 OT

Fast Campus 데이터 엔지니어링 강의의 CH01-1 [OT]
(`raw/data-engineering/ch01-1-de-vs-ai-de-ot.pdf`)를 `data-engineering` 영역 첫 소스로 인제스트.
강의 entity [[AI Data Engineering (Fast Campus course)]], source [[AI DE Course - Ch1-1 OT]],
concept [[Traditional data engineering]]·[[AI data engineering]] 생성. `index.md`에 등록.
파일은 `raw/data-engineering/`로 이동·영문명 변경. area MOC는 페이지가 더 쌓이면 생성(lazy).

## [2026-07-27] ingest | SpatialData docs - Design doc

`https://spatialdata.scverse.org/en/stable/`(URL 소스)를 `bioinformatics` 영역 첫 소스로
인제스트. 사이트가 Cloudflare 봇 차단(HTTP 429)으로 직접 fetch되지 않아, 동일 내용의 원문
MyST markdown을 `scverse/spatialdata` repo에서 **태그 `v0.8.0`에 핀**해 가져왔다. 스냅샷은
`raw/bioinformatics/spatialdata-docs/`(`SOURCE.md` 매니페스트 + `index--v0.8.0.md` +
`design_doc--v0.8.0.md`).

첫 슬라이스로 design doc + 랜딩 페이지만 인제스트(섹션별 진진적 방식). entity
[[SpatialData]](문서 섹션 트래커 겸함)·[[OME-NGFF]], concept [[SpatialData elements]]·
[[Coordinate systems and transformations]], source [[SpatialData docs - Design doc]],
영역 MOC [[Bioinformatics]] 생성. `index.md`에 등록.

핵심: SpatialData는 분석 라이브러리가 아닌 IO·공간질의 **인프라**이며, element를 전용 클래스
없이 표준 파이썬 클래스 + 메타데이터로 표현하고, element 간 명시적 링크 대신 좌표계로 의미적
그룹핑을 한다. 모순 없음(영역이 비어 있었음). 문서의 2025 로드맵이 미완 체크박스로 남아 있어
소스 페이지에 신선도 주의를 명시하고 MOC 열린 질문으로 남겼다.

URL 소스 처리 컨벤션을 이번 건으로 확정해 `CLAUDE.md` Ingest 절에 명문화했다.

## [2026-07-27] ingest | spatialdata-io docs - README and readers

`https://spatialdata.scverse.org/projects/io/en/stable/`(URL 소스)를 인제스트. 별개 repo·별개
버전이라 [[SpatialData docs - Design doc]]의 다음 섹션이 아닌 **새 소스**로 취급. 사이트는 같은
Cloudflare 차단(429)이라 GitHub `scverse/spatialdata-io`를 **태그 `v0.7.1`에 핀**해 스냅샷
(`raw/bioinformatics/spatialdata-io/`).

**중요한 발견**: 이 프로젝트의 `docs/`는 코드에서 생성된다 — `index.md` 134바이트 스텁,
`api.md` 951바이트 autodoc(리더 이름만). 실제 내용은 Python docstring에 있다. 따라서 소스의
실체는 `README.md` + 리더 모듈이며, 사용자가 지정한 범위(Xenium·Visium 계열 전부·MERSCOPE)에
따라 `visium.py`·`visium_hd.py`·`xenium.py`·`merscope.py` 4개(2,654줄)를 읽었다.

생성: entity [[spatialdata-io]](리더 카탈로그·공통 골격), 기술 entity [[Visium]]·[[Visium HD]]·
[[Xenium]]·[[MERSCOPE]], source [[spatialdata-io docs - README and readers]]. 갱신:
[[SpatialData]](에코시스템 표에 리더 연결), [[Coordinate systems and transformations]](Visium HD의
투영 변환 우회를 실전 사례로 추가), [[Bioinformatics]] MOC(데이터 적재 섹션·열린 질문), `index.md`.

기술을 리더별 페이지가 아닌 **플랫폼 entity**로 필링했다 — 나중에 해상도·화학·논문 등 다른
소스가 같은 노드에 쌓이도록.

핵심: 리더는 "장비 출력 → element dict" 변환기이며 공통 골격이 동일하다. element 이름 규약이
갈려(Xenium 고정 이름 vs 나머지 dataset_id 접두사) 다중 샘플 병합 시 충돌 위험. Xenium은 XOA
버전별로 `cells.zarr.zip` 구조가 달라 **다핵세포 표현 가능 여부가 갈린다**(v2.0+만 지원) — 버전
표로 상세 기록. Visium HD의 CytAssist는 투영 변환이 필요해 affine으로 분해 후 나머지를 픽셀에
구워 넣는다.

모순 없음 — 설계 문서에서 정리한 Table 3키 규칙·좌표계 그룹핑 원칙이 실물로 확인되는 쪽. 문서
결함 4건(api.md에 iss·macsima 누락, README 예제 오타, Python 3.8 표기 낡음, PhenoCycler·MACSima
중복 등재)을 소스 페이지에 기록.

## [2026-07-27] ingest | SpatialData source - ShapesModel and shapes IO

`shapes/`에 정확히 무엇이 들어가는지 알고 싶다는 질문에서 출발. 위키의 [[SpatialData elements]]는
설계 문서 기반이라 "GeoDataFrame · (multi)polygon·circle · 2D"까지밖에 없었고, 원출처인
설계 문서의 Shapes 절 자체가 2문단이라 더 뽑을 게 없었다.

표준 위치는 사이트 API 페이지지만 두 겹으로 막혀 있다: (1) Cloudflare 봇 차단(429), (2) repo의
`docs/api.md`는 11줄 toctree, `docs/api/*.md`는 autodoc 지시자뿐 — 본문은 빌드 시점에 docstring에서
생성된다. [[spatialdata-io]]와 같은 구조. 그래서 v0.8.0 태그의 소스 3종(2,019줄)을 읽었다:
`models/models.py`·`_io/io_shapes.py`·`_io/format.py`.

생성: source [[SpatialData source - ShapesModel and shapes IO]], concept
[[SpatialData Shapes element]], concept [[SpatialData Zarr format versions]]. 갱신:
[[SpatialData elements]](Shapes 상세 포인터), [[SpatialData]](온디스크 설명·문서 섹션 트래커에서
API를 부분 완료로), [[Bioinformatics]] MOC(개념·출처·열린 질문 3건), `index.md`, raw `SOURCE.md`.

핵심: circle은 도형이 아니라 `Point` + `radius` 컬럼이다. `validate()`는 **첫 행의 타입만** 보고,
타입 혼합 검사는 비용 때문에 별도 메서드로 분리돼 기본 경로에서 호출되지 않는다 — 규칙 위반이
조용히 통과할 수 있다. `radius`의 NaN/inf는 현재 경고이나 다음 릴리스에서 `ValueError`로 승격
예정(옛 [[Xenium]] 데이터에서 발생). 3D geometry도 에러가 아닌 경고 — 설계 문서의 "2D"는 강제가
아니다. 온디스크는 포맷 v0.2부터 `shapes.parquet` 한 개이며, **이 parquet은 zarr 계층의 일부가
아니다**(코드 주석이 명시). 좌표변환은 parquet에 안 들어가고 zarr 그룹 메타데이터로 분리 저장된다.

포맷 버전이 element 종류별로 따로 매겨지고 컨테이너 버전이 조합을 제약한다는 점이 새로 드러나
별도 개념 페이지로 분리했다. 현행은 raster 0.3 / shapes 0.3 / points 0.2 / tables 0.2 / container
0.2이며 전부 Zarr v3(`FormatV05`) 세대다.

모순 없음 — 기존 페이지들의 상위 서술을 아래층에서 채우는 쪽. 문서/코드 drift 2건 기록:
`docs/api/data_formats.md`가 **현행 포맷 대부분**(shapes V03 포함)을 누락, `parse()` docstring이
`index`를 str 필수라 하지만 코드는 검사하지 않고 Xenium 리더는 정수 인덱스를 쓴다.

## [2026-07-27] ingest | SpatialData source - Shapes conversion and aggregation ops

직전 인제스트가 남긴 열린 질문("Shapes 연산은 이름만 파악됨")을 이어서 처리. `_core/operations/`
전체는 ~5,800줄이라 두 덩어리로 나눴고, 이번엔 Shapes와 직접 얽힌 4개(1,843줄)를 읽었다:
`vectorize.py`·`rasterize.py`·`rasterize_bins.py`·`aggregate.py`. 질의(`_core/query/`, 2,400줄)는
별개 개념이라 다음으로 미뤘다.

생성: source [[SpatialData source - Shapes conversion and aggregation ops]], concept
[[Rasterization and vectorization]], concept [[Spatial aggregation]]. 갱신:
[[SpatialData Shapes element]](관련 연산 섹션을 실제 링크로), [[Visium HD]](rasterize_bins 경로),
[[SpatialData]](문서 트래커·링크), [[Bioinformatics]] MOC(연산 섹션 신설·열린 질문 교체),
`index.md`, raw `SOURCE.md`.

핵심: 세 연산이 서로를 호출한다 — `to_circles(labels)`는 면적 계산에 `aggregate()`를 쓰고,
`aggregate()`와 `rasterize()`는 둘 다 내부에서 `to_polygons()`를 거친다. 그래서 **circle은 어디서든
폴리곤으로 buffer된 뒤 계산되며**, `buffer_resolution`(기본 16)이 시각화뿐 아니라 집계 정확도까지
좌우한다. `rasterize()`는 기본값이 이미지 반환이라 **Labels를 넣어도 이미지가 나온다**(labels로
받으려면 `return_regions_as_labels=True`, 그때 uint16 65535 상한). shapes 래스터화의 기본 reduction이
`first`인 이유는 인덱스를 categorical로 보고 픽셀마다 하나를 고르기 때문 — 사실상 세그멘테이션
마스크 생성이다. `rasterize_bins()`는 Visium HD 격자의 미세 회전을 무작위 20개 bin에서
`estimate_transform("affine")`으로 추정해 보정하며, docstring이 "Visium HD는 되고 Visium은 안 된다"고
명시한다. `aggregate()`는 표가 아니라 `SpatialData`를 반환하고 지원 조합이 둘뿐이다
(Shapes×Points|Shapes, Labels2D×Image2D).

모순 없음. 확인된 것: [[Xenium]] 리더가 손으로 쓰던 `radius = √(area/π)`가 라이브러리 공식 근사와
동일한 공식이었다. 기본 `region_key`/`instance_key`가 [[spatialdata-io]] 관례와 일치 — 설계 문서에서
"권장이지만 강제 아님"이라던 이름이 여기선 기본값으로 박혀 있다. `to_polygons()`가
`validate_shapes_not_mixed_types()`를 부르는 드문 지점이라, 직전에 기록한 "검증의 구멍"의 예외로
연결했다. 제약 2건 기록: points→shapes 집계가 전부 메모리에 올라감(issue #210), 3D labels는
`to_circles`·`to_polygons` 모두 미지원.

## [2026-07-27] query | SpatialData를 데이터 엔지니어링 기질로 읽기 + ETL·카탈로그 설계

질문 두 개: (1) spatialdata 포맷의 DE 관점 이점은 무엇이고 웨어하우스/레이크하우스 저장 이점과
같은 것인가 (2) 이 포맷 위에 ETL을 세운다면 어떤 조합인가. 한 장으로 정리 요청 + 카탈로그 부분
상세 요청.

생성: note [[SpatialData as a data engineering substrate]] — 이 위키의 첫 note이자 첫
**멀티 area 페이지**(`area: [bioinformatics, data-engineering]`). 갱신: `index.md`(두 area의 Notes
섹션 양쪽에 등재), [[Bioinformatics]] MOC(종합 노트 섹션 신설).

핵심 결론: 이점은 **레이크하우스의 파일 포맷 층**에 있고 **테이블 포맷/웨어하우스 층**에는 없다.
Zarr가 주는 것(오브젝트 스토리지 직독·청크 프루닝·multiscale=사전집계·dask lazy)은 Parquet의
N차원 배열 버전이고, element별 포맷 버저닝은 Iceberg의 format-version gating과 구조가 거의 같다.
반면 트랜잭션 로그·카탈로그·SQL·FK 강제가 전부 없다. 그래서 아키텍처의 임무가 **포맷이 갖지 않은
셋(카탈로그·원자성·질의층)을 공급하는 것**으로 환원된다 — 이게 노트의 조직 원리.

카탈로그 설계가 세 결함을 동시에 푼다는 게 이번 종합의 알맹이다. Iceberg 테이블 3장
(`stores`·`store_elements`·`qc_metrics`) DDL + 예시 행 + 질의 6개를 적었다. 특히:
**promote = Iceberg 트랜잭션**이라 zarr 바이트에 ACID가 없어도 "어느 store가 current인가"에는
ACID가 생긴다(진실의 원천이 디렉토리가 아니라 테이블이 된다). **extent를 컬럼으로 두면** store를
열기 전에 SQL에서 공간 프루닝이 되어 사실상 포맷 한 층 위의 zone map이 된다. **element별 포맷
버전을 컬럼화**해야 하는 이유는 "이 store의 포맷 버전"이라는 단일 질문에 답이 없기 때문.
`store_elements.annotated_by_table`은 **포맷이 저장을 거부한 element 간 링크를 카탈로그가 물질화**
하는 자리다. 운영 귀결 둘: superseded 바이트를 지우는 GC 잡이 별도로 필요하고(Iceberg는 행만
관리), 카탈로그는 재구축 가능해야 하지만 `is_current`만은 store에서 유도되지 않는 진짜 상태다.

§8에 미검증 6건을 분리 표기 — 1순위는 Zarr v3 sharding 실사용 여부(청킹 절의 전제),
그리고 `polygon_query`/`bounding_box_query`가 실제로 청크 프루닝을 하는지(하지 않으면 "공간
predicate pushdown" 주장이 약해진다). 설계 제안 절은 의견임을 노트 상단에 명시했다.

모순 없음. 기존 페이지 수정은 MOC 링크 추가뿐 — 사실 관계를 바꾼 곳은 없다.

## [2026-07-27] ingest | SpatialData source - Spatial and relational queries

SOURCE.md 가 "next candidate" 로 표시해 둔 `_core/query/` 2개(2,131줄)를 읽었다. 함께 처리: 릴리스
현황 확인, data-engineering MOC 신설.

생성: source [[SpatialData source - Spatial and relational queries]], concept
[[Spatial queries in SpatialData]], concept [[Relational queries in SpatialData]], moc
[[Data Engineering]]. 갱신: [[SpatialData as a data engineering substrate]](정정 — 아래),
[[SpatialData]](릴리스 현황 섹션 신설·문서 트래커), [[SpatialData Shapes element]](질의 링크 실연결),
[[Bioinformatics]] MOC(질의 섹션 신설·열린 질문 3건 교체), `index.md`, raw `SOURCE.md`.

**가장 큰 소득: "질의가 청크 프루닝을 하는가"의 답이 element 종류마다 다르다.** 래스터만
`image.sel()` 로 dask lazy 슬라이싱을 타서 실제로 교차 청크만 읽는다. **Points 는 `.compute()` 로
전량 materialize 한 뒤 마스킹하고**, Shapes 는 `sindex` R-tree 를 쓰지만 lazy loading 이 없어 어차피
전량 메모리다. 기존에 기록된 `aggregate()` 의 points 메모리 문제(issue #210)가 고립된 결함이 아니라
**패턴**이었다 — `aggregate()`·`bounding_box_query()`·`get_values()` 가 모두 `.compute()` 한다.
v0.8.0 의 "bounding_box_query speedup"(PR #1104)은 identity/scaling 변환 fast path 로, 산술 비용만
줄이고 `.compute()` 는 그대로 둔다 — I/O 최적화가 아니다.

**어제 낸 노트를 정정했다.** [[SpatialData as a data engineering substrate]] 초판이 청크 프루닝을
포맷 전반의 성질처럼 적었는데 래스터에만 참이다. §1 대응표에 정정 박스를 넣고, §2 에 "점 데이터에
프루닝 없음" 항목 추가, §5 validation gate 에 issue #218 의 검사 목록과 #1162 순서 단언 추가,
§8 을 "확인 완료 / 남은 미검증" 으로 재편했다.

**미해결 이슈 3건을 코드에서 발견하고 업스트림에서 확인했다.** (1) **v0.8.0 리그레션 #1162** —
PR #1131 이 `_filter_table_by_elements` 를 순서 보존 mask 에서 `join(how="left")` 로 바꿔서, 다중
region 테이블을 필터하면 `obs` 가 region 별로 재정렬된다. `filter_table=True` 가 기본값이라
**공간 질의 전체가 영향권**이고, 테이블 행과 지오메트리의 위치 대응을 가정하면 조용한 데이터 오류다.
(2) **#824 `left_exclusive` 인덱스 버그** — 이 조인만 instance_key '값' 을 위치 인덱스로 쓴다.
코드 대조로 먼저 의심하고 업스트림에서 확인했다. spatialdata-io 관례(0..n-1)에서는 우연히 맞지만
[[Xenium]] cell id 에서는 깨진다. (3) **#852** Python 3.13 핫픽스가 `how` 검사를 느슨하게 만들었다.

기타 함정: `polygon_query()` 를 이미지·라벨에 쓰면 **폴리곤이 무시되고 bbox 가 적용된다**(구현이
`.bounds` 로 위임). 좌표계 이름 오타는 에러 없이 빈 결과가 된다. 경계 처리가 종류별로 불일치한다
(points 는 엄격 부등호로 배제, shapes 는 `intersects` 로 포함). `filter_label_pixels` 기본값 `None`
은 **필터를 요청해도 경고만 내고 픽셀을 그대로 둔다**. 회전 변환에서 래스터는 축정렬 외접 박스로
과선택하고 shapes 는 정확하다.

부수 확인: `docs/changelog.md` 는 GitHub Releases 로 안내하는 **4줄 스텁**이고 repo 루트에
`CHANGELOG.md` 도 없다 — 릴리스 노트는 API 로 읽어야 한다(SOURCE.md 에 명령 기록). 그 결과
**v0.8.0 이 최신 태그**이고 **2025 로드맵 4개 항목이 여전히 미완**임을 확인해 MOC·노트의 1순위
열린 질문을 닫았다. v0.8.0 이 Python 을 3.12/3.13/3.14 로 올린 것도 기록.

[[Data Engineering]] MOC 신설 — DE area 페이지들이 어떤 MOC 에서도 도달 불가였던 lint 결함을 해소.
링크 검증: 깨진 링크 0, 고아 페이지 0 (27 페이지).

## [2026-07-27] ingest | spatialdata-io source - Legacy AnnData converter

질문에서 출발한 인제스트. "geojson 을 예전엔 h5ad 의 obsm 에 저장했나?" → 확인해보니 **구조적으로
불가능**했고, 그 사실이 곧 [[SpatialData]] 의 존재 이유라 정리 대상이 됐다.

핵심 방법론: 레거시 관례를 기억이나 추측으로 쓰지 않고 **명세로 확인**했다.
`spatialdata_io.experimental` 의 `from_legacy_anndata()`/`to_legacy_anndata()` 컨버터가 읽고 쓰는
키의 목록이 곧 레거시 어휘의 전부이기 때문이다. `converters/legacy_anndata.py` (366줄) 를 v0.7.1
태그에서 받아 읽었다.

생성: source [[spatialdata-io source - Legacy AnnData converter]], concept
[[Legacy AnnData spatial convention]]. 갱신: [[SpatialData elements]](설계 문서의 "Tables 는
좌표계를 가질 수 없다" 문장이 무엇을 겨눈 말인지 연결), [[spatialdata-io]](리더 외 컨버터 섹션 신설),
[[Bioinformatics]] MOC(입문 순서 안내 + 개념·출처 등재), `index.md`, raw `SOURCE.md`.

**레거시 공간 어휘는 두 곳이 전부였다**: `obsm["spatial"]` (n_obs×2 중심좌표)와
`uns["spatial"][dataset_id]` 아래의 hires/lowres 이미지 + scalefactors 3종. 폴리곤이 들어갈 자리가
없다 — `obsm` 은 정의상 `obs` 에 정렬된 직사각 배열이고 폴리곤은 세포마다 꼭짓점 수가 다른 ragged
데이터다. 복원 코드가 `ShapesModel.parse(xy, geometry=0, radius=...)` 로 **항상 circle** 을 만들고,
반지름조차 obsm 이 아니라 `scalefactors["spot_diameter_fullres"]` 에서 오며 **없으면 기본값 10 + 경고**다.

**세포 경계는 h5ad 바깥 사이드카 파일로 살았다** — [[MERSCOPE]] 리더가 boundaries 를 h5ad 와 무관하게
따로 찾아 `geopandas.read_parquet()` 하는 게 그 증거다. 매니페스트도 타입도 검증도 없이 파일명
관례로 묶여 있었다.

**왕복이 손실적이다.** `to_legacy_anndata()` 는 주석 그대로 "convert polygons, multipolygons and
labels to circles" — `to_circles()` 로 전부 뭉갠다. 반대 방향은 없던 관계를 **발명한다**: region
이름을 `"locations"` 로 짓고 `region_key`/`instance_key` 컬럼을 새로 붙인다. 레거시에는 "이 표가
어느 기하를 가리키는가" 라는 개념 자체가 없었고 — 그래서 표 하나에 기하 하나를 못 넘었다.
이 비대칭이 두 모델의 표현력 차이를 가장 선명하게 보여준다.

concept 페이지의 중심은 **"레거시의 한계 → SpatialData 의 설계 결정" 8행 대응표**다. 기하가 점
하나뿐 → Shapes element, 이미지가 uns 의 생 배열 → OME-NGFF Zarr, 좌표변환이 숫자 3개 →
좌표계·변환, 표 하나에 기하 하나 → region/instance_key, 사이드카 + 파일명 관례 → 단일 store 등.

확인된 연결: [[SpatialData elements]] 에 이미 적혀 있던 설계 문서 문장("Tables 는 좌표계를 가질 수
없다. 표에 공간 좌표를 넣어둘 수는 있지만 라이브러리가 처리하지 않는다")이 추상적 원칙이 아니라
**`obsm["spatial"]` 관례를 명시적으로 폐기하는 선언**이었다. 남은 흔적도 기록: 리더 4개가 지금도
하위 호환용으로 `obsm["spatial"]` 을 채운다(정본은 Shapes element 쪽).

모순 없음. 링크 검증: 깨진 링크 0, 고아 0 (29 페이지).

## [2026-07-27] query | Spatial omics vocabulary — 용어 다리 놓기

연속으로 나온 두 질문("shapes 를 마스크라고도 부르나?", "shapes 를 어노테이션이라고 하는 거야?")이
같은 축을 가리켰다 — **위키가 SpatialData 내부 어휘는 정리했지만 현장 어휘와의 다리가 없었다.**
흩어진 한 줄씩 추가하는 대신 concept 한 장으로 만들었다.

생성: concept [[Spatial omics vocabulary]]. 갱신: [[SpatialData elements]],
[[SpatialData Shapes element]](용어 주의 박스), [[Bioinformatics]] MOC(입문 안내에 추가·개념 등재),
`index.md`.

두 질문 다 답은 **아니오**였고, 근거는 설계 문서와 소스에서 직접 확인했다.

**mask 는 Labels 전용어다.** design_doc 113("Pixel masks ... aka _Labels_")·206("Labels (pixel
mask)")·208. `models.py` 에는 "mask" 가 **한 번도 안 나온다** — `ShapesModel` 은 이 어휘를 안 쓴다.
`vectorize.py` 의 `_vectorize_mask(mask)` 라는 이름이 방향을 드러낸다: 입력이 mask, 출력이 shapes.

**annotation 은 정확히 반대쪽을 가리킨다.** design_doc 104·115·130·245·286 의 어법이 일관되게
"Tables 가 annotate 하고 Shapes 는 annotated 된다"이다. `PointsModel.parse(annotation=DataFrame)` 도
점마다 붙는 속성 표다. 이 프레임워크에서 annotation 은 **언제나 값이고 기하가 아니다.**
Shapes 의 상위어는 **ROI** 이고 design_doc 220 이 직접 그렇게 쓴다 — "regions of interest, such as
clinical annotations and user-defined ROI" 에서 **clinical annotation 은 ROI 의 하위 항목**이다.
결정적 반례: [[Visium]] spot·[[Visium HD]] bin·[[Xenium]] `cell_circles` 가 전부 Shapes 인데 아무도
이걸 어노테이션이라 부르지 않는다 → `Shapes ⊃ annotation` 이지 `=` 가 아니다.

페이지는 **두 축 + 출처 축**으로 구성했다: (1) 기하냐 값이냐 → annotation 의 의미, (2) 래스터냐
벡터냐 → mask 의 의미, (3) 누가 만들었나 → 현장에서 실제로 갈리는 축(QuPath 의 Annotations vs
Detections 가 이걸 UI 로 못박은 사례). 다의어 표도 넣었다 — 코드에서 `mask` 가 세그멘테이션
마스크와 boolean 배열 두 뜻으로, `feature` 가 GIS Feature 와 gene id 두 뜻으로 쓰인다.

GeoJSON 대응이 예상 밖으로 깔끔했다: `Feature = geometry + properties` 가 SpatialData Shapes
(`geometry` 컬럼 + 주석 컬럼)와 같은 분리다. GeoParquet 이 저장 포맷으로 맞아떨어지는 이유이기도
하고, 그 표의 맨 아랫줄(AnnData: 벡터 영역 표현 불가)이 [[Legacy AnnData spatial convention]] 의
한계를 한 칸으로 요약한다.

검색 가능성을 위해 `mask`·`마스크`·`annotation`·`어노테이션`·`ROI`·`boundaries` 등을 alias 로 걸었다.
**출처 구분을 명시**했다 — SpatialData 내부 용어는 줄 번호와 함께 인용, QuPath·napari·Cellpose 등
현장 관행은 "인제스트된 출처 없음" 으로 표시(연구실·도구마다 흔들리는 부분이라).

링크 검증: 깨진 링크 0, 고아 0, alias 충돌 0, alias/제목 충돌 0 (30 페이지, alias 70).

## [2026-07-28] ingest | Data landscape guide for developers (sinja.io)

URL 소스 인제스트. https://sinja.io/blog/data-landscape-guide-for-developers — OlegWock,
2026-07-14 발행(2주 전). curl로 HTML 직접 받아(HTTP 200, 316KB, 봇 차단 없음) stdlib HTMLParser
스크립트로 마크다운 변환 후 `raw/data-engineering/data-landscape-guide/`에 스냅샷 + SOURCE.md.
버전 핀이 없는 블로그 글이라 **날짜로 고정**했다.

생성: source [[Data landscape guide for developers]] + concept 8장 —
[[ETL and ELT]], [[Columnar and in-memory data formats]], [[Analytical data storage tiers]],
[[Table formats]], [[Batch and stream processing]], [[Medallion architecture]],
[[Dimensional modeling]], [[Data catalog and semantic layer]].
갱신: [[Traditional data engineering]], [[AI data engineering]](직무 축 충돌 절),
[[SpatialData as a data engineering substrate]](Iceberg 미검증 항목 갱신 + DE 개념 링크),
[[Data Engineering]] MOC(파이프라인 순서로 재구성), `index.md`.

**entity 페이지는 만들지 않았다.** 툴이 ~70개 언급되지만 대부분 한 문장씩 스치고 지나간다 —
Snowflake·Airflow·Iceberg 전부 stub 한 줄이 될 뿐이라, 실제 소스가 들어올 때 만들기로 했다.
툴명은 concept 페이지 안에 굵은 글씨로만 남겼다. 이 글의 값어치는 개별 툴이 아니라
**어휘와 배치**에 있다.

MOC 열린 질문 3개 중 2개가 움직였다.

**테이블 포맷 — 메웠다(개념 층위까지만).** MOC가 "가장 약한 발판"이라 적어둔 자리다. 이 글이
테이블 포맷을 *쿼리 엔진과 raw 파일 사이에 앉아 저장을 관리하는 층* 으로 정의하고 ACID·스키마
진화/버저닝·파티셔닝 최적화·time travel을 전부 그 층에 귀속시킨다. 딸려 나온 게 더 중요한데,
**웨어하우스는 쿼리 엔진과 강결합이고 레이크하우스는 아니라서 비용을 1:1로 비교할 수 없다**는
지점이다. 다만 세 포맷을 **비교하지는 않는다** — 이름만 나열한다. 그래서
[[SpatialData as a data engineering substrate]] §4의 미검증 항목을 지우지 않고 *좁혔다*:
"Iceberg가 위키에 없다" → "개념은 있고 선택 기준과 온디스크 구조가 없다". Iceberg 1차 문서가
이제 1순위.

**오케스트레이터 — 경계만 좁혔다.** 새 주장 하나: **오케스트레이터는 배치 전용이다.** 시작→끝→
정지 모델이 끝나지 않아야 하는 스트림에 안 맞으므로 스트리밍은 Flink 같은 스트림 프로세서가
직접 맡는다. 열린 질문은 "배치 안에서 Airflow vs Dagster vs Prefect를 무엇으로 고르나"로 남았다.

**직무 — 축이 어긋난다는 걸 명시했다.** Fast Campus는 *시간축*(기존 DE → AI DE로 진화), 이 글은
*공존축*(analytical/scientific/engineering/ML이 동시에 존재). 이 글의 ML type ≈ 강의의 AI DE인데
"DE의 진화"가 아니라 "도구셋이 달라 갈라진 별개 직군"으로 본다. 모순이 아니라 프레이밍 충돌이라
양쪽 페이지에 "다른 축의 분류" 절을 달고 열린 질문으로 남겼다 — 둘 다 1차 자료 없는 개괄이라
어느 쪽이 현업인지 판정할 근거가 없다. 부수 발견: 강의의 "기존 DE"는 저 글 기준으로
**engineering + analytical 두 직군에 걸쳐 있다**(저 글의 data engineer는 대시보드를 안 만든다).

새로 들어온 것 중 실무에 가장 쓸모 있어 보이는 건 **"카탈로그"가 세 가지 다른 물건**이라는
3분할이다: metastore(기계용 — 테이블·스키마·파일 매핑) / data catalog(사람용 — 출처·소유자·
접근정책) / semantic layer(정의용 — "revenue에 환불 포함?"). Unity Catalog가 셋을 다 걸쳐서
이름이 헷갈리는 것이지 개념은 별개다. 이 기준으로
[[SpatialData as a data engineering substrate]]가 "카탈로그"라 부르던 것을 **metastore 겸 gold 층**
으로 정정했다.

Parquet(스캔 최적화) vs Arrow(처리 최적화) 대비도 깔끔하게 들어왔고, 공간 오믹스의 Zarr·GeoParquet
지식과 바로 맞물린다. 메달리온은 substrate 노트가 이미 쓰고 있었는데 정작 정의 페이지가 없었던
구멍이었다.

**시의성 메모**(랜드스케이프 글은 조용히 낡는다): SparkR deprecated, Census → Fivetran Activations,
BigLake → "Lakehouse for Apache Iceberg", Looker Studio → Data Studio 재개명,
"Polars 채택률이 pandas에 한참 못 미친다"는 평가. 전부 소스 페이지에 날짜와 함께 박아뒀다.

## [2026-08-01] ingest | AI DE 강의 전체 코스 맵 확정 (41개 덱 / 1,155p)

강의 PDF 40개가 추가로 들어왔다(기존 OT 1개 포함 41개, 총 **1,155페이지**). 내용 ingest 전에
**순서를 먼저 복원**했다 — 파일명 규칙이 파트마다 달라서 헷갈리는 게 실제 문제였다.

파일명 형태가 세 가지고 **대부분 파트 표기가 없다**: `CH0N-M.` 접두 / **번호만** `N.` 접두 /
`PartN_Ch M`. 이 중 번호만 붙은 `1.`~`10.` 파일들의 소속이 관건이었는데, **`10.` 파일 제목이
"및 Part 1 정리"** 인 걸 근거로 Part 1 후반부(CH04 다음)로 확정했다. 다만 그 덱을 열어보니
**정리 절은 실제로 없고 케이스 스터디로 끝난다** — 제목만 그렇게 붙었다. 이 파일들엔 챕터 번호가
파일명에도 본문에도 없어서 CH05~CH08 번호는 추론으로 표시했다(순서만 확실).

Part 1 자체의 **공식 제목은 자료 어디에도 없다**. LLM·RAG 덱 3개도 파트 표기가 없어 사람의 판단으로
Part 5에 배치했다. Part 4는 Ch1~Ch4가 **356페이지 단일 PDF**라 챕터 경계를 페이지 범위로 떴다
(Ch1 p2–66 / Ch2 p67–132 / Ch3 p133–240 / Ch4 p241–356).

전부 [[AI Data Engineering (Fast Campus course)]] 트래커에 표로 박았다. 앞으로 주제 단위로
source 페이지를 만들며 체크 상태를 갱신한다(총 32개 예정). 이번 커밋은 맵만.

## [2026-08-01] ingest | AI DE 강의 Part 1 완주 (16개 덱 / ~205p)

코스 맵을 확정한 뒤 Part 1을 끝까지 인제스트했다. **source 페이지 15개 신규 + 개념/엔티티 페이지
9개 신규 + 기존 7개 보강.** Part 1의 절반은 [[Data landscape guide for developers]]에서 이미 세운
어휘를 강의 관점으로 **보강**하는 작업이었고(충돌 없음), 나머지 절반은 강의가 처음 가져온 주제였다.

**새로 생긴 것 9개** — [[Change data capture]] · [[Apache Kafka]] · [[Stream processing semantics]] ·
[[Latency and throughput]] · [[Unstructured data ingestion]] · [[Feature store]] ·
[[Data drift and training-serving skew]] · [[Data SLA and observability]] ·
[[Data and model versioning]].

가장 값나가는 보강은 **"왜 그런가"가 채워진 것**이다. 랜드스케이프 가이드는 "Parquet은 열, Avro는
행, 특히 스트림 처리에서"까지만 줬는데, 강의가 그 이유를 채웠다 — Parquet은 컬럼 분해·압축에 CPU가
들어 실시간 쓰기가 안 되고 small files를 만든다, 그래서 **유입은 Avro로 받고 새벽 배치에 Parquet으로
묶는다(compaction 패턴)**. 마찬가지로 ETL→ELT 전환도 "원본이 남아서 좋다"가 아니라
**스토리지 비용 99% 하락 + MPP**라는 조건 변화로 설명되고, **규제(PII) 때문에 여전히 ETL을 써야 하는
영역**이 있다는 것까지 나왔다.

**MOC 열린 질문 정산:** ✅ 비정형 텐서 변환 실무는 해소([[Unstructured data ingestion]]).
⚠️ Delta의 트랜잭션 로그 온디스크 구조는 채워졌지만(`_delta_log/000000.json`·Add/Remove·
optimistic concurrency·체크포인트) **Iceberg는 그대로 비어 있다** — 강의가 Delta만 다루고 나머지 둘을
언급조차 안 한다. **Iceberg 1차 문서는 여전히 1순위.** ⚠️ 데이터 품질·관측성은 프로세스는 다 나왔지만
(SLA 명세·서킷 브레이커·경고 피로) **제품 이름이 하나도 안 나온다**(Great Expectations·Monte Carlo 등).
오케스트레이터 비교는 진전 0.

**모순·오류 기록:** ① CH04-1,2가 "스트리밍 = 랜덤 I/O"로 일반화하는데 바로 다음 챕터의 Kafka는
**순차 쓰기**로 속도를 낸다 — 강의 내부 모순이고, 정확히는 "건별로 목적지에 직접 쓰면" 랜덤 I/O다.
② CH03의 한 슬라이드가 제목은 "**ELT** 아키텍처의 한계"인데 내용은 **ETL 서버** 병목이다(제목 오류).
③ `10.` 파일 제목에 "Part 1 정리"가 있지만 덱 안에 정리 절이 없다.

**수치 인용 주의를 MOC에 박았다.** 이 코스는 80%를 세 군데 다른 대상에 쓰고(비정형 비율·배치
워크로드·탐색 시간 낭비), 70%/2% 같은 성과 수치가 서로 다른 회사 사례에 중복 등장하는데
**어디에도 출처가 없다.** 케이스 스터디 6건(Uber Michelangelo·Netflix Keystone·Tesla Data Engine·
Meta FBLearner·Google TFX·Airbnb Bighead)은 1차 자료 인제스트 후보로 남겼다.

**Part 2로 넘길 것:** Feature Store의 offline/online 스토어 간 일치 문제 — Part 1은
"Write Once, Compute Anywhere"로 넘어가지만 Part 2 Ch5 제목이 "Feature Store은 만능이 아니다"다.
버전 관리 도구(DVC·MLflow)도 Part 2 Ch2(MLOps) 몫.

## [2026-08-01] ingest | AI DE 강의 Part 2: 10개 source 페이지, 12개 신규 개념·도구

**[[AI Data Engineering (Fast Campus course)]] Part 2 "AI 학습/추론 중심 데이터 파이프라인 설계"
전체(5개 챕터 / 206p, 강사 Habi) 인제스트.** 파일은 챕터당 1개지만 각 PDF 안에 번호 붙은
**소단원**(별도 타이틀 슬라이드)이 있고 그게 Part 1의 덱 하나에 해당해서, **소단원을 source 페이지
단위로 삼았다** — 5개 파일 → **10개 페이지**. 사용자와 3안(챕터 5장 / 절충 7장 / 소단원 10장) 중
합의한 결과다.

**Part 2는 Part 1과 결이 다르다.** Part 1이 *"무엇인가"*(파이프라인 어휘)였다면 Part 2는
*"어떻게 짓고 운영하는가"*(시스템 설계 결정)다. 그래서 MOC에 갈래를 하나 새로 텄다 —
**"모델을 학습시키고 서빙하는 쪽"**. DE의 책임 범위에 **연산의 배치**가 들어온다는 것이 이 파트의
프레이밍이고, 강의 문장으로는 *"데이터 엔지니어는 계산이 발생하는 흐름까지 설계 대상이 된다."*

**신규 12개** — concept 7: [[MLOps]] · [[LLMOps]] · [[Context engineering]] ·
[[ML data pipeline]] · [[Batch and online serving]] · [[Model serving platforms]] ·
[[Inference optimization]] / entity 5: [[FastAPI]] · [[TorchServe]] · [[BentoML]] ·
[[NVIDIA Triton Inference Server]] · [[ONNX]].
**[[FastAPI]]가 이 위키의 첫 `programming` 영역 페이지다** — Starlette·Uvicorn·uvloop·Cython·
Pydantic 층 구조와 WSGI vs ASGI.

**최대 수확은 Ch3-3의 skew 4패턴이다.** Part 1은 skew를 일화 하나("33배 뻥튀기")로 설명하고
"Feature Store를 쓰라"로 끝냈는데, Part 2가 같은 현상을 **재현 가능한 진단 틀**로 분해한다 —
**시간 기준**(event vs processing time) · **집계 범위**(full vs partial window) · **결측 처리**
(null→0 vs drop vs 조회 실패) · **스케일링**(global vs local normalization). 원인 서술도 교정된다:
Part 1은 "언어가 달라 이중 구현하는 것"이라 해서 사람의 실수처럼 들렸는데, Part 2는
**"분리는 필연이고 통제하지 않은 것이 문제"**라고 본다. 그리고 원칙이 **비대칭**으로 바뀐다 —
Part 1의 "Write Once, Compute Anywhere"(어디서든 같게) → **"Training은 Serving을 따라가야 한다"**
(제약이 큰 쪽이 기준). 실행형은 *"실시간에서 full window가 불가능하면 feature를 재정의한다"* —
**서빙이 못 만드는 피처는 만들지 않는다.** → [[Data drift and training-serving skew]]에 반영.

**❌ Part 1이 남긴 열린 질문은 닫히지 않았다.** [[Feature store]]와 MOC에 *"Part 2 Ch5가 '만능이
아니다'를 다룰 예정"*이라 적어뒀는데, **Ch5의 "만능이 아니다"는 "안 써도 되는 경우"**(클라이언트가
값을 앎 / DW에 이미 있음 / 시간 의존성 없음 / batch만 필요 / 계산 비용 낮음)**이지 "썼을 때 남는
문제"가 아니다.** 두 스토어 정합성·백필·지연 감지는 Part 2 전체에서 한 번도 나오지 않는다.
질문을 닫지 않고 **부분적 우회책만 붙였다** — skew 패턴 2의 대응 "long-term(배치) +
short-term(실시간) 분리", 즉 정합성을 맞추는 대신 맞출 필요가 없게 만드는 것.

**강조점 이동 기록.** Part 1은 Feature Store를 skew의 *해법 그 자체*로 서술했다("존재 이유는
하나다"). Part 2는 **"공용 변환 로직 → Feature Contract → (필요시) Feature Store"** 3단계 중
**가장 무거운 마지막 수단**으로 놓고, Ch5도 같은 온도다. 모순은 아니지만 온도가 뚜렷이 다르고
**Part 2 쪽이 더 정확해 보여서** 두 페이지 서두에 경고로 달았다.

**Ch4는 "GPU를 쓰지 마라"에 가깝다.** `Total Latency = 네트워크 + 직렬화 + 전/후처리 + 모델 추론 +
스케줄링`으로 분해하고 **GPU는 다섯 중 하나만 줄인다**고 지적한다. 순서는 모델 최적화
(quantization·pruning·distillation) → 런타임([[ONNX]] Runtime) → 그래도 부족하면 GPU. GPU 정당화도
성능이 아니라 **단가**로 한다("CPU 서버 여러 대 > GPU 한 대"). 그리고 *"배치 없이는 GPU 이점이 거의
사라진다"* 가 세 서빙 플랫폼이 하나같이 배치 기능을 자랑한 이유를 설명한다.

**⚠️ 부분 해소:** MOC의 "오케스트레이터 비교"에 **ML 배치 축** 비교표가 처음 생겼다
(Airflow / Kubeflow Pipeline / Flyte). **일반 ETL 축의 Airflow vs Dagster vs Prefect는 그대로
공백** — Dagster는 Part 2 슬라이드에 로고로만 나오고 설명이 없다.

**Part 2가 새로 남긴 질문 5개** (MOC에 기록): ① **LLM 서빙 계보가 통째로 빠졌다** — LLMOps를 한
챕터 다루면서 vLLM·PagedAttention·continuous batching·KV 캐시가 한 번도 안 나오고, Ray Serve와
KServe도 로고뿐이다. ② retrieval 품질 지표(recall@k·MRR)와 임계값 설정법 없음.
③ **라벨 지연이 재학습 주기의 상한**인데(라벨이 T+7이면 MTTR<4h는 무의미) 강의가 두 사실을 다른
파트에서 각각 말하고 잇지 않는다. ④ **가용성과 정합성의 상충** — Ch4는 "조회 실패 시 기본값"을
권하고 Ch3은 그게 skew라고 경고한다. 답(`is_missing` 플래그)은 있지만 한자리에서 붙이지 않는다.
⑤ 출처 표기된 1차 자료 3건을 인제스트 후보로 남김 — Chip Huyen *Designing Machine Learning
Systems*(라이프사이클 원출처), "Do you really need a feature store?"(Medium), tiangolo의 FastAPI
성능 도식.

**수치 주의 목록에 하나 추가:** Part 2 Ch1의 "온프레미스 시대엔 인프라 관리에 70% 이상 시간" —
이 코스의 상습적인 출처 없는 70%다. Ch1은 전반적으로 Part 1 CH02·CH03의 재탕이라 새 개념 페이지를
만들 거리가 없었고, 유일하게 새로운 건 온프레미스 시대 DE의 실제 업무 목록과 JD 실물 캡처다.

**다음:** Part 3(시맨틱 & 컨텍스트 기반 데이터 설계 · 273p — RDBMS·정규화의 약점, Graph, 온톨로지·
지식그래프, Graph-RAG, 그래프 DB 실습). Part 3~5 합계 ~744p 남음.

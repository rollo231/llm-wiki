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

## [2026-08-01] ingest | AI DE 강의 Part 3 — 시맨틱 & 컨텍스트 기반 데이터 설계 (5챕터 273p)

`raw/data-engineering/Part 3_Ch 1~5.pdf` 273페이지 전체를 읽고 **source 15장 + concept 10장 +
entity 6장**을 만들었다. Part 1(16장)·Part 2(10장)에 이어 **Part 3 완료 — 남은 건 Part 4~5, 471p.**

**분할:** 소단원(별도 타이틀 슬라이드)이 17개인데 **15장으로 묶었다.** 제목이 같은 연속 소단원
(Ch1의 "RDBMS의 한계와 NoSQL의 등장 1·2")과 짧은 챕터(Ch5, 26p 두 소단원)만 합쳤다.
Part 2의 소단원 단위 규칙을 유지하되 Part 1의 `(1)(2)(3)` 병합 규칙을 함께 적용한 셈.

**Part 3는 Part 1·2와 결이 또 다르다.** Part 1이 *"무엇인가"*(파이프라인 어휘), Part 2가
*"어떻게 짓고 운영하는가"*(시스템 설계)였다면 Part 3는 **"무엇을 의미하는가"(의미 모델링)** 다.
논지가 한 줄로 꿰인다 — **스키마는 형식을 잡지만 의미는 별도 계층이 필요하다 → 그 계층이 시멘틱 →
그 구현이 그래프·온톨로지 → 그 활용이 GraphRAG.** MOC에 **여섯 번째 갈래**로 넣었다.

**최고의 문장 세 개.**
① ⭐ **"가장 흔한 실수: 테이블 = 클래스, 컬럼 = 속성, FK = 관계로 그대로 옮기는 것."** 운영 DB
스키마는 저장 효율용, 온톨로지는 의미 해석용 — 목적이 다르다. *"온톨로지 설계는 스키마 복사가 아니라
의미 구조를 다시 세우는 작업"*(Ch3-2). 같은 소단원의 **"관계에 설명할 정보가 많아질수록 그 관계는
독립 개체다"**(Customer-buys-Product보다 `Order`, Job-produces-Dataset보다 `Run`)도 판단 기준이
관찰 가능한 신호라 좋다.
② ⭐ **"검색 단위는 chunk인데 질문 단위는 structure인 경우가 많다"**(Ch4-1). RAG 한계 4종의 첫 줄이자
GraphRAG 존재 이유의 요약.
③ ⭐ **"NoSQL이면 확장성이 자동 해결될까? 아니다"**(Ch1-3). 파티션 키가 시스템을 결정하고, 일관성
완화는 애플리케이션 복잡도로 전가되며, **운영 포인트는 줄지 않고 분산된다.** Part 1의 "Kafka는 기능을
빼서 이겼다"와 같은 결의 냉정함.

**Part 2와 이어지는 지점이 하나 있는데 강의는 잇지 않는다.** Ch2-4의 결론 *"Graph + AI의 성패는 모델
성능보다, AI가 읽는 운영 컨텍스트를 얼마나 정확하고 최신으로 구조화했는가에 달려 있다"* 가
[[Context engineering]](Part 2)의 직계 후속이다. Part 2가 "Feature가 있던 자리를 컨텍스트가
대체한다"였다면 Part 3는 **"그 컨텍스트를 무엇으로 만드나 — 그래프로"** 라고 답한다. 강사도 다르고
서로 인용하지도 않는다 — **위키가 붙인 연결.** 같은 종류로 Ch1-4의 Context 요소와 [[Feature store]]의
Feature 재정의(`..._last_30_days_as_of_t`)도 사실 같은 이야기다.

**기존 페이지 4장을 고쳤다.** [[Data catalog and semantic layer]]에 "같은 스펙트럼의 더 오른쪽"
([[Data semantics]]·[[Ontology]]·[[Knowledge graph]])과 lineage의 그래프 구현을 붙였고,
[[Unstructured data ingestion]]에는 **"이 페이지의 RAG 서술은 Part 3 기준으로 얕다"** 는 경고와
[[Retrieval-augmented generation]] 링크를 달았다(Part 1은 RAG를 파이프라인 종착점 한 줄로만 다뤘고
한계는 없었다). [[Context engineering]]에 GraphRAG 후속 연결과 *Lost in the Middle* 반박을 추가.

**⚠️ 자료 결함이 Part 1·2보다 눈에 띈다.** ① **Ch3-3 파이프라인 단계 수 불일치** — 개요는 1~7단계,
바로 다음 상세는 1~10단계. ② **Ch4-3 타이틀 번호 중복** — 소단원 2·3이 모두 "2. Graph-RAG의 개념과
사례"이고, 목차 04·05는 소단원 1 목차의 복붙 잔재로 본문에 없다. ③ **Ch5 제목이 "실습"인데 실습이
전혀 없다** — 코드·스크린샷·설치 절차 전무. ④ **완전 동일한 중복 슬라이드**가 Ch1-1·Ch2-4·Ch3-1·
Ch3-4에 다수(Ch3-4는 20p 중 접두사 설명이 3연속 반복). ⑤ **Ch2의 인용 이미지 출처 미표기**가 많고,
특히 컬럼 lineage UI 스크린샷은 어느 제품인지 불명이라 재확인이 불가능하다.

**⭐ 그래도 출처 표기는 Part 1보다 뚜렷이 낫다.** Ch4-1이 RAG 원논문·RAG Survey(arXiv 2312.10997)·
*Lost in the Middle*·AWS 문서 네 건을 명시하고 그래프까지 인용한다. MS *From Local to Global*,
Neo4j 고객사례 2건, AWS 블로그도 URL이 있다. **1차 자료 인제스트 후보가 4건 늘었다.**
다만 성격이 바뀌었을 뿐이다 — Part 1이 *출처 없는 80%* 였다면 Part 3는 **출처는 있으나 벤더 자료**다
(Neo4j "time-to-insight 10배·analyst time 92% 감소·150명", Microsoft "LazyGraphRAG 인덱싱 비용은
full의 0.1%"). **강의가 후자에 "자사 비교", "주장"이라고 붙이는 점은 진전.**

**Part 3가 새로 남긴 질문 (MOC 기록).** ① **retrieval 품질 지표는 Part 3도 답하지 않았다** — RAG를
49p 다루면서 recall@k·MRR·nDCG가 한 번도 안 나오고, LazyGraphRAG가 "품질을 유지하거나 능가"한다면서
무엇으로 쟀는지 밝히지 않는다. **Part 5가 마지막 기회.** ② ⭐ **지식그래프 증분 갱신** — 10단계의
마지막이 슬라이드 한 장에 질문 6개(전체 재생성 vs 증분 / 삭제 반영 / 중복 병합 / 버전 충돌 /
provenance)만 던지고 끝난다. 실무에서 가장 오래 붙잡을 곳이 가장 얇다 — **Part 3 최대의 공백.**
③ **온톨로지 도구가 통째로 빠졌다** — Protégé·RDFLib·Apache Jena·Stardog가 한 번도 안 나오고 SHACL을
무엇으로 실행하는지도 없다. ④ 그래프에서 잘못된 엣지의 오염 범위에 정량 근거 없음. ⑤ Ch4 P3
(엔터프라이즈 그라운딩)가 Ch3의 메타데이터 그래프와 같은 물건인지 — 강의가 두 챕터를 잇지 않아
위키의 추정으로 남겨뒀다.

**해소된 것 하나:** MOC의 *"semantic layer는 실제로 쓰이는가"* — 채택률 근거는 여전히 없지만
**같은 코스 안에서 온도가 바뀌었다.** Part 1은 semantic layer라는 용어를 피하고 카탈로그+LLM
자동태깅으로 흡수했는데, Part 3는 "시멘틱"을 정면으로 한 챕터 다룬다. 다만 **도구가 하나도 안 나온다**
— dbt semantic layer·Cube·Looker LookML·AtScale이 273p 전체에서 한 번도 언급되지 않는다.

**다음:** Part 4(실시간 & 대규모 데이터 분산처리 설계 · 431p — 분산처리·Redis 캐싱·스트리밍·GPU
워크로드·SLA/SLO/Error Budget). Ch1~Ch4가 356p 단일 PDF라 챕터 경계를 페이지 범위로 잡아야 한다.
Part 4~5 합계 471p 남음.

## [2026-08-01] ingest | AI DE 강의 Part 4 — 실시간 & 대규모 데이터 분산 처리 설계 (5챕터 431p)

**소스:** `raw/data-engineering/Part 4_Ch 1~4.pdf` (356p) + `Part 4_Ch 5.pdf` (75p).
**21개 소단원을 주제 단위로 묶어 15개 source 페이지** — Part 3와 같은 밀도(약 29p/장).
사용자가 세 옵션(소단원 20장 / **주제 병합 15장** / 챕터 5장) 중 중간을 골랐다 — **네 번째 연속.**
concept/entity 세밀도도 중간(concept 9 + entity 6)을 골랐고 **그대로 나왔다.**

**신규 15개** — concept 9: `Distributed processing` · `CAP theorem` · `Distributed system limits` ·
`Replication and consensus` · `Caching strategies` · `Message broker` ·
`Lambda and Kappa architecture` · `GPU architecture` · `GPU resource allocation` /
entity 6: `Redis` · `Apache Hadoop` · `Apache Spark` · `Apache Flink` · `CUDA` · `NVIDIA RAPIDS`.
**기존 6개 대폭 보강:** `Data SLA and observability`(SLI/SLO/Error Budget·5층위·대시보드 5종·
알람 4조건으로 두 배 가까이) · `Inference optimization`(Roofline·PCIe·GPU 3축 해석표) ·
`Stream processing semantics`(3분할·출력 방식·exactly-once 범위 정정) · `Apache Kafka`(소비 의미론·
acks 대가) · `Latency and throughput`(Lambda/Kappa 상세를 새 페이지로 이관) ·
`Columnar and in-memory data formats`(coalescing 절 신설).

**Part 4의 성격.** Part 1이 "무엇인가", Part 2가 "어떻게 짓는가", Part 3가 "무엇을 의미하는가"였다면
Part 4는 **"물리적으로 어디서 막히는가"** 다. Part 1의 *시소의 법칙*이 세 곳에서 구체화된다 —
**CAP**(분산), **Roofline**(GPU), **Dynamic Batching의 역설**(서빙 설정).

**최대 수확 다섯.** ① ⭐ *"분산 도입의 출발점은 데이터가 크다가 아니라 단일 서버로도 감당
가능한가"* — AWS U7i(32TiB/1920vCPU)·I4i(30TB)를 근거로. **분산 챕터를 분산 반대 논변으로 연다.**
② ⭐ **Brewer의 2012년 정정을 직접 인용** — "셋 중 둘"이라는 통념을 소개한 **직후에** 저자 본인의
반박으로 무너뜨린다. 선택은 fine granularity로 일어나고 C/A는 **정도의 문제**. **CAP의 C ≠ ACID의 C**
도 분리한다. ③ ⭐ **GPU 3축 해석표**(사용률 × Queue × Latency) — 특히 *"사용률 낮음 + latency 높음
= 앞단 병목"* 이 Part 2의 "GPU는 마지막 수단"에 **진단 도구**를 붙였다. ④ ⭐ *"컬럼 기반 포맷이
GPU와 어울리는 이유는 연속된 메모리 접근(coalescing)"* — Part 1과 Part 4를 잇는 가장 강한 고리.
⑤ ⭐ **`offline-online skew`를 SLI로, `mismatch 0.1% 이하`를 SLO로** 승격.

**자료 품질이 파트 안에서 극단적으로 갈린다.** Ch1-3(CAP)은 **이 코스 전체에서 출처가 가장 좋다** —
Brewer 2000·2012 정정·Gilbert & Lynch·Lamport·FLP, **출처 없는 수치 0건.** Ch4-2의 GPU 스펙도
검증했는데 실제와 일치한다(T4 320GB/s, A100 ~2TB/s, H100 3.3TB/s, MIG 최대 7, A100 SM 108개,
AWS/GCP 인스턴스 매핑). **반면 Ch4-5의 RAPIDS 사례 3건은 출처가 전무하고 내부 모순까지 있다** —
AS-IS "전처리 4시간" vs TO-BE "8시간에서 15분으로", "TCO 70~80% 절감"을 벤더 주장이라 밝히지 않는다.
**Part 3가 Neo4j·MS 수치에 "자사 비교"라고 붙였던 것보다 후퇴.**

**⚠️ 파트 내부 모순 2건.** ① **Redis의 CAP 분류** — Ch1-3은 Redis를 **CP**("금융 거래·결제에 적합")로
놓는데, Ch2-2는 부적합 데이터 1번이 *"강한 정합성이 필요한 결제 상태"*, Ch2-3은 *"Redis 장애 시
데이터 유실"·"정산·결제·주문에는 위험"*. Redis 기본 복제는 비동기라 **RPO > 0**이므로 CP가 아니다 —
위키는 후자를 채택하고 `CAP theorem`·`Redis` 양쪽에 기록했다. ② **RAPIDS 사례의 4h vs 8h.**
그 밖에 **목차 복붙 잔재 3건**(Ch3-2의 "05 합의의 대가"=Ch1-4 것, Ch5-1의 "05 GPU…"=Ch4-5 것,
Ch2-3의 05 중복), Ch1-1 섹션 헤더 불일치, **MIG 지원 장비가 Ch4-2와 Ch4-3에서 어긋남**,
**Ch4-3 ↔ Ch5-4의 큰 폭 중복**(교차 참조 없음), 중복 슬라이드 13쌍.

**Part 4가 해소한 것.** ✅ `Inference optimization`의 열린 질문 *"시분할·MPS·MIG 비교가 없다"* —
4축 비교표로 답했다(**MPS 격리는 "최악"**). ⚠️ **Feature Store의 skew 문제는 절반** — 측정
대상(SLI)으로 승격했지만 **재는 방법이 없다.** ⚠️ **라벨 지연도 절반** — `prediction-label join
delay`가 SLI가 됐지만 여전히 "도착한 뒤"이지 "언제 도착하는가"가 아니다. ⚠️ **LLM 서빙은 지표만** —
TTFT/TPOT/TPS는 왔는데 **KV 캐시가 이름만 한 번, vLLM·PagedAttention·continuous batching은 여전히
전무.**

**새로 남긴 질문 (MOC 기록).** ① ⭐ **워터마크의 실제 운영이 통째로 빠졌다** — 생성 방식, 여러
파티션 워터마크 병합(min), **idle partition 문제**(실무 최대 함정)가 한 줄도 없고, *"지연 분포를
보고 정하라"* 면서 재는 법도 없다. ② ⭐ **캐싱 3대 실패 모드 중 둘** — stampede 대응·TTL jitter·
negative caching 부재(위키가 채웠으나 강의 밖 지식이라 검증 필요). ③ **PACELC와 일관성 모델
스펙트럼** — "정도의 문제"라면서 정도를 나누지 않는다. ④ **gang scheduling**(Kueue·Volcano) 부재.
⑤ **Error Budget policy·burn rate 알람** — 정의만 하고 알람으로 잇지 않는다. ⑥ **SLO 숫자의 도출
근거.** ⑦ **Kafka tiered storage** — 카파를 2014년 형태로 소개. ⑧ **관측 도구가 하나도 안 나온다** —
Prometheus·Grafana·OpenTelemetry가 전무한데 대시보드 5종을 설계한다.
⑨ ⭐ **1차 자료 후보 7건 추가** — 분산 시스템 정전 5건 + Raft 논문 + Kreps *Questioning the Lambda
Architecture*. **강의가 이름만 대고 서지 정보를 안 주므로 원문 확인이 필요하다.**

**다음:** Part 5 (LLM·RAG, 40p / 3개 덱 — LLM 기본 이해 16p · LLM과 RAG 15p · RAG의 진화:
Hybrid Search와 Reranking 9p). **`retrieval 품질을 무엇으로 재나`(Part 2·3이 연속으로 남긴 질문)의
마지막 기회다.** 코스 완주까지 40p.

## [2026-08-01] ingest | AI DE 강의 Part 5 — LLM·RAG (3개 덱 40p) · **코스 완주**

**source 5장 + concept 7 + entity 3.** 3개 덱(40p)을 덱 안에서 주제가 바뀌는 지점으로 잘라
**5장**(장당 6~9p)으로 만들었다. Part 1~4에 이어 **다섯 번째로 중간 옵션**을 골랐다.
**이로써 5개 파트 / 41개 덱 / ~1,155p 전체 인제스트 완료 — source 페이지 61장.**

**Part 5의 성격.** Part 1~4는 LLM을 계속 **전제로만** 뒀다 — 비정형 수집의 종착점,
`LLMOps`의 관리 대상, GPU의 워크로드, RAG의 generator. **Part 5가 그 상자를 처음 연다.**
그런데 **덱마다 질이 극단적으로 갈린다.**

**⭐ 최대 수확 셋 — 전부 덱 3(9p, 가장 짧은 덱)에서 나왔다.**
① **"의미는 남고 식별자는 사라진다."** 문서를 768차원에 눌러 담을 때 버려지기 쉬운 것이 하필
정확히 맞아야 하는 값들(버전·제품 코드·금액)이다 → **BM25가 2026년에도 필요한 이유.**
Dense와 Sparse의 실패 모드가 **정확히 반대**라서, 합치는 이유는 성능을 더하기 위해서가 아니라
**서로의 실패를 덮기 위해서**다.
② **RRF의 "스케일 정규화 불필요"** — BM25 점수(위로 열린 실수)와 코사인 유사도(−1~1)는 같은 자로
잴 수 없는데, **RRF는 점수를 버리고 순위만 써서 문제를 통째로 우회한다.**
③ **Bi/Cross-Encoder를 가르는 건 구조가 아니라 "미리 계산할 수 있는가"** — 정확도의 대가가
사전 계산 불가능성이다. 그래서 Top-200 → Top-20의 2단계가 되고, 이는
`Caching strategies`·`Inference optimization`의 **"싼 필터 먼저, 비싼 연산은 소수에"** 와 같은 판단.

**✅ 해소된 열린 질문 — `retrieval 품질을 무엇으로 재나`.** Part 2·3이 연속으로 남겼던 질문에
덱 3이 답한다: **Stage 1은 Recall@K, Stage 2는 NDCG@K.** 단계마다 목표가 다르므로 지표도 다르다
(놓치지 않기 vs 잘 세우기) → `Retrieval evaluation metrics`. 다만 **평가셋을 어떻게 만드나**는
여전히 없다.

**⚠️ 반대로 덱 2는 이 코스 전체에서 자료 신뢰도가 가장 낮다.** 슬라이드마다 출처 없는 통계 배지
(`95% 검색 정확도` `30% 환각률` `99% 정보 정확도` `100% 출처 표시` …), **낡은 `2K 토큰
제한`**(현행 100K~1M+), **GPT-4 "1.76조 파라미터"**(OpenAI 미공개 추정치의 사실화), 임베딩
알고리즘 비교표의 근거 없는 성능 %(**축이 다른 모델을 단일 숫자로 서열화**), FAISS를 관리형 DB와
동렬 배치. 덱 1에는 **LSTM 연도 오류**(2014 → 실제 1997)도 있다. **RAG 서술 자체가
`AI DE Course - Part3 Ch4 RAG and its limits`보다 얕다 — 파트 순서는 뒤인데 내용은 후퇴한다.**

**✅ 반면 덱 3의 RRF 계산 예시 3행을 직접 검산했고 전부 정확했다**
(`1/61+1/63=0.0323` · `1/65+1/62=0.0315` · `1/62+1/67=0.0310`). BM25 수식도 표준형 그대로.
**이 코스에서 수치를 검산해 맞은 첫 사례다.**

**새 페이지 10개** — concept 7: `Large language model` · `Transformer architecture` ·
`Tokenization` · `Text embeddings` · `Vector database` · `Hybrid search and reranking` ·
`Retrieval evaluation metrics` / entity 3: `LangChain` · `GPT` · `BERT`.
**보강 2개:** `Retrieval-augmented generation`(retriever 내부 한계 3종 + Agentic·Adaptive 절) ·
`Unstructured data ingestion`(4단계 마지막 칸 → 새 페이지 연결).
MOC에 **여덟 번째 갈래 "모델과 검색단을 직접 여는 쪽"** 추가.

**두 진화 계보가 사실 직교한다는 발견.** Part 3는 `Naive → Advanced → 구조화(GraphRAG)`,
Part 5는 `Naive → 하이브리드·리랭킹 → Agentic·Adaptive`로 RAG 진화를 그리는데 서로를 참조하지
않는다. **전자는 *무엇을 인덱싱하나*(청크 vs 그래프), 후자는 *어떻게 검색을 제어하나*(고정 vs 적응)** —
경쟁이 아니라 다른 축이고 함께 쓸 수 있다. 양쪽 페이지에 기록했다.

**새로 남긴 질문 (MOC 기록).** ① ⭐⭐ **청킹 전략이 코스 전체에서 비어 있다** — "의미 단위로 청킹,
오버랩 설정" 두 줄이 전부인데, `Retrieval-augmented generation`의 1번 한계(*검색 단위는 chunk,
질문 단위는 structure*)가 **정확히 이 단계에서 결정된다. RAG에서 가장 큰 공백.**
② ⭐ **컨텍스트 비용의 물리** — 시퀀스 길이 제곱 복잡도와 **KV 캐시**가 코스 어디에도 없다
(RoPE·ALiBi도). ③ **리랭킹의 비용 모델** — 질의당 Top-K회 추론인데 "배치/캐싱" 한 줄.
④ **벡터 DB를 정말 따로 둬야 하나** — pgvector·Elasticsearch로 충분한 경계선이 없다.
⑤ **메타데이터 필터링 + ANN**(pre/post-filter). ⑥ **평가셋 제작.**
⑦ **1차 자료 후보 2건 추가** — *Attention Is All You Need*(2017)와 **RRF 원 논문**
(Cormack et al., SIGIR 2009). **둘 다 강의가 수식을 쓰면서 인용하지 않는다.**

**다음:** 코스가 끝났으므로 **1차 자료 인제스트**로 넘어갈 시점이다. 누적 후보:
Iceberg 1차 문서(여전히 1순위) · 분산 시스템 정전 5건 + Raft · RAG 원논문·Survey·*Lost in the
Middle* · *From Local to Global*(MS GraphRAG) · *Attention Is All You Need* · RRF 논문 ·
Chip Huyen, *Designing Machine Learning Systems*.

## [2026-08-02] query | 공간 전사체 플랫폼 아키텍처 평가 + 로드맵 (3종 고정 · 실제 스택)

**질문:** 플랫폼을 [[Xenium]]·[[Visium]]·[[MERSCOPE]] 3종으로 한정하고, 현재 스택
(K8s · Airflow · MinIO · Postgres)에서 내부 R&D + 멀티테넌트 제품을 함께 지탱하려면 이상적인
아키텍처는? — 논의 중 **"강의를 인제스트한 건 정석을 따르기 위함이니 로드맵 형태로"** 로 재정의됨.

→ **[[Spatial omics platform roadmap]]** 신규 노트. **코스 완주 후 첫 적용 사례**다.

**테제:** 정석은 도입 목록이 아니라 **도입 순서**다. 강의가 매 챕터 *"안 해도 되는 경우"* 를 먼저
말하는 형태가 네 번 반복된다(분산·GPU·Feature Store·OWL) — 그걸 로드맵으로 뒤집었다.
정렬 축은 **되돌릴 수 있는가** 하나. Phase 0(규약 6개, 새 인프라 0) → 1(파이프라인) →
2(제품 경로) → 3(운영) → 4(metric contract) → 5(조건부·트리거 표).

**발견 3건.**

① **"3개 플랫폼"이 아니라 2개 워크로드다.** [[Visium]]은 Points가 없고 [[Xenium]]·[[MERSCOPE]]는
수억 행 — 3자릿수 격차. 그리고 **Visium만 좌표계 이름이 데이터셋마다 다르다**(`<id>_downscaled_*`)
→ `global` 가정이 깨진다. Xenium·MERSCOPE는 둘 다 픽셀 좌표계인데 픽셀 크기가 다르다
→ **µm canonical 좌표계를 silver에서 강제**해야 크로스 플랫폼 비교가 성립. 되돌릴 수 없는 결정.

② **3종 고정의 실제 배당금은 CI 픽스처다.** N×M 컨버터 문제가 사라진 자리에 유한한 버전 매트릭스
(XOA 4종 × VPT × SpaceRanger 2종)가 남고, **3종이라 골든 픽스처로 고정할 수 있다.** 13종이면 불가능.
그리고 **재현성을 조용히 깨는 것 둘**을 찾았다 — MERSCOPE 이미지 백엔드가 `rioxarray` **설치 여부로**
갈리고, spatialdata-io v0.6.0에서 `cells_as_circles` 기본값·반지름 기준(핵→세포)이 바뀌었다.
→ 카탈로그에 **컨테이너 이미지 다이제스트 + 리더 kwargs 전량**이 필요하다(버전 문자열로는 부족).

③ ⚠️ **기존 노트 정정 — 카탈로그는 Iceberg가 아니라 Postgres다.**
[[SpatialData as a data engineering substrate]] §4에 정정 박스를 넣었다(스키마는 유지, 저장 위치만
정정). `stores`는 행 수천 개 · promote 트랜잭션 하나 · 동시 writer 소수 · 조인과 상태 업데이트 —
**OLTP다**([[Analytical data storage tiers]]). 그 노트는 "레이크하우스 층위" 프레임에 갇혀 카탈로그까지
레이크로 밀었다. **현재 스택이 이미 옳은 쪽에 있었다.** 부수 효과로 *"Iceberg 1차 문서"* 가 §4 검증의
전제조건에서 빠진다(gold 팩트 테이블 설계 때 다시 필요).

**현재 스택 평가:** MinIO ✅ · Airflow ✅ · **K8s ✅✅**(per-task resource override로 두 워크로드
클래스를 이미 푼다 → 분산 트리거를 더 멀리 민다) · **Postgres ✅✅**(위 ③).
**Phase 0·1에 새 인프라 0**, 전체 로드맵에서 새로 들어오는 컴포넌트는 **타일 서버·캐시·관측성 셋뿐.**

**강의 개념이 그대로 들어맞은 자리 셋.** ⓐ 불변 store → **타일 캐시에 무효화 문제가 존재하지 않는다**
([[Caching strategies]]의 어려운 절반이 사라짐). ⓑ **SLO label을 플랫폼별로 분리** — Visium 5분과
Xenium 4시간을 한 SLO로 묶으면 Xenium 전체가 멈춰도 초록색이다([[Data SLA and observability]]의
*"전체는 정상, 부분은 장애"*). ⓒ **피라미드 상위만 물질화, 최하위는 온디맨드** —
[[Hybrid search and reranking]]의 Two-Stage와 같은 형태(싼 걸 전부에, 비싼 건 소수에).

**MOC 열린 질문 4건 추가** — 코스를 실제 스택에 적용하자 **강의가 클라우드 관리형을 암묵 전제하고
자체 호스팅을 한 번도 다루지 않는다**는 게 드러났다: ⭐ **MinIO 1차 문서 부재(인제스트 1순위)** —
*"스토리지는 컴퓨트보다 싸다"* 가 자체 호스팅에선 조건부다 · 관측성 도구 공백이 **가설이 아니라 확인된
병목**이 됨 · 정석 패턴의 도입 트리거에 **수치 기준이 없다** · **멀티테넌시가 41개 덱 어디에도 없다.**

**미검증(노트 §9):** MinIO 특성 전부 · 규모 수치 전부(가정에서 나온 산술) ·
뷰어 줌 레벨 분포(§5.1의 전제인데 측정 전) · Xenium 래스터 vs MERSCOPE 폴리곤의 세포 수 차이.

## [2026-08-02] query | 오브젝트 스토리지 경로 설계 + Hive→Iceberg 대비

**질문:** MinIO 디렉토리 룰을 정하는 게 늘 어려웠고 *"이게 아닌 것 같은데"* 라는 느낌을 자주 받았다.
이어서 — **"이걸 해결해주는 게 Hive라고 생각했는데 Iceberg는 이런 개념이 아니지?"**

→ 신규 concept **[[Object storage layout]]** + [[Table formats]]에 **Hive 절** 추가 +
[[Spatial omics platform roadmap]] §2.2·§3.1 확장.

**원인 규명이 답이었다.** 그 느낌에는 구체적 원인이 있다 — **오브젝트 스토리지에는 디렉토리가
없다.** 키는 평평한 문자열이고 `/`는 표시 규약이다. prefix가 실제로 하는 일은 **권한 경계 ·
열거 단위 · 생애주기 단위 · 분산 배치** 넷뿐이고, **분류 체계도 질의 인덱스도 아니다.**
경로에 taxonomy를 넣으면 *질의할 수 없는 곳에 질의하고 싶은 정보를 넣은* 상태가 된다.
→ **규칙 한 줄: 경로는 "누가 접근하고 언제 지워도 되는가"만 답한다.**

**세 문항 테스트** — ① 이 값이 바뀔 수 있나(→ 이관 비용) ② 권한이나 생애주기를 가르나
③ 이걸로 "찾으려는" 건가(→ 카탈로그 컬럼). 셋 다 아니면 **장식**이다.
**실패 5종**: 의미를 경로에(rename = 복사) · 경로로 찾기(**"앞 세그먼트냐 뒤냐"가 답이 안 나오는
이유 — 질문이 틀렸다**) · 브라우징 욕심 · 습관적 날짜 파티셔닝(**Hive 파티셔닝은 테이블 층에만**) ·
한 prefix에 수백만 객체(경로로 못 고침 → 매니페스트 필수).

**Hive vs Iceberg — 축은 "경로"였다.** Hive는 **디렉토리 레이아웃 = 데이터 모델**이라 규약을
줬지만 **구속**이었다(스킴 변경 = 재작성 · 리스팅이 곧 스캔 계획 · 메타스토어 병목 ·
**원자적 커밋 없음 — 디렉토리에 쓰는 게 커밋** · 물리 레이아웃 노출).
Iceberg는 **테이블 내용을 리스팅이 아니라 매니페스트가 정의**하게 해서 경로를 의미에서 해방시켰다.
→ **"Hive가 해결해준다"는 느낌은 정확했고, 그 규약이 구속이었던 것.**

⭐ **Hive의 4번 문제가 [[SpatialData]] store의 문제와 정확히 같다** — *디렉토리 트리이고 원자적
커밋이 없다.* 그래서 우리 해법(카탈로그 포인터 플립)이 Iceberg가 Hive에 대해 한 것과 같은 형태인
게 우연이 아니다.

⭐⭐ **그래서 우리가 만드는 게 사실 Iceberg의 아이디어다.** 대응표를 §2.2에 넣었다 —
스냅샷↔`is_current` 플립 · 매니페스트↔`stores`/`store_elements` · 파일 경로↔`store_uri`(둘 다 불투명) ·
**파일별 min/max 통계↔`extent` bbox**(둘 다 열기 전 프루닝) · hidden partitioning↔경로에 의미 없음.
**차이 하나:** Iceberg는 프루닝 후 엔진이 바로 스캔하지만 우리는 파이썬이 store를 연다 →
**이 카탈로그는 쿼리 플래너가 아니라 작업 스케줄러의 입력**이고, 그래서 gold 물질화가 따로 필요하다.

**로드맵 §3.1 구체화** — bronze/staging/**silver/derived**/gold 5버킷.
⭐ **`derived/`를 `silver/`에서 뗀 것이 핵심**: 백업 정책이 정반대라(silver는 지킴, derived는
재생성 가능) 섞으면 **백업 비용이 파생물 배수만큼 곱해진다** — §2.3 MinIO 용량 문제의 직접 대응.
**layer = 버킷, tenant = prefix**(정책이 갈리는 축은 layer, 테넌트는 계속 는다.
뒤집는 조건은 테넌트별 quota 하나). 원칙 하나 추가: **카탈로그 행이 생기기 전에 도착하는
데이터만 경로가 자기설명적이어야 한다** → `platform`이 bronze에만 있는 이유.

**Iceberg 인제스트의 이유를 교체했다** (삭제가 아니라). 원래 *"§4가 Iceberg를 전제하므로 검증에
필요"* → **§4가 Postgres로 정정되며 그 근거는 소멸.** 대신 **"도입할 도구가 아니라 손으로 만드는
것의 레퍼런스 설계"** 로 남는다. 알아야 할 것 셋: 매니페스트 입도 · 통계 컬럼화 범위 ·
**스냅샷 만료와 고아 파일 정리**(GC).

**§9 정밀화** — *"Zarr v3 sharding 미완"* 은 **[[SpatialData]] 로드맵 기준이지 Zarr 사양·
zarr-python 기준이 아니다.** **write 시점에 SpatialData를 우회해 직접 샤딩할 수 있는가**가
열린 질문이고, 되면 객체 수가 자릿수로 준다.

**다음:** Zarr 인제스트를 6문항 스코프로 대기 — ① `sharding_indexed` 코덱(사양 + zarr-python
사용 가능 여부) ② consolidated metadata가 `_manifest.json`을 대체하나 ③ chunk key encoding
④ **어떤 store 연산이 LIST를 요구하나** ⑤ v2/v3 혼재 제약 ⑥ 청크 크기 권고의 근거.
**소스 우선순위: MinIO(1) > Zarr 사양+zarr-python(2) > Iceberg(3)** — 앞의 둘을 붙여야
*"파생물 2~3배 중복이 감당 가능한가"* 에 숫자로 답한다(MinIO가 분모, Zarr가 분자).
**⚠️ 위키에 Zarr 자체 페이지가 없다** — 계속 이야기하면서 페이지가 없는 개념(린트 항목).

## [2026-08-08] query | 위키 자체 진단 — "이 수집으로 뛰어난 DE가 되는가"

**질문:** 지금까지 수집한 것으로 충분한가? → [[Wiki gap analysis - DE readiness]]

**답: 어휘는 충분하고 나머지 세 축이 얇다.** 개념 62장으로 설계 논쟁은 되지만
(그 증거가 [[Spatial omics platform roadmap]]의 카탈로그 Iceberg→Postgres 정정),
**1차 자료 · 운영 도구 · 자기 측정치**가 비어 있다.

⭐ **위키가 이미 답을 적어놨다.** [[Data Engineering]] MOC 열린 질문 절에서 같은 형태의 문장이
여섯 번 반복된다 — ***"재야 한다"는 있고 "이렇게 잰다"가 없다*** (Feature store · 서빙 ·
분산 트리거 · SLO 숫자 · 워터마크 · 로드맵 §9). **강의를 더 인제스트해도 안 닫히는 종류**고,
그런데 그 목록을 소진하는 대신 강의 완주가 먼저 실행됐다.

**수치 (2026-08-08):** source 68장 중 **61장이 강의 하나** · concepts 62 · entities 29 · notes 2.
DE 영역 **1차 자료 0건.**

⭐ **반대 증거는 위키 안에 있다** — bioinformatics 쪽은 [[SpatialData]] 소스 코드를 직접 읽었고
그래서 가장 구체적이다(`cells_as_circles` v0.6.0 기본값 변경 · MERSCOPE 백엔드가 `rioxarray`
**설치 여부로** 갈림). **방법은 증명됐는데 DE 영역에는 안 썼다.**

⭐ **entity 페이지의 비대칭** — JanusGraph·ArangoDB·Neptune·TorchServe에는 페이지가 있고
**Airflow·Kubernetes·MinIO·Postgres·Iceberg·dbt·Prometheus·Zarr에는 없다.** 앞줄은 로드맵 §8이
"트리거 없으면 안 한다"로 미뤄둔 것들이고 뒷줄은 지금 돌아가는 것들이다.
**로드맵 Phase 1이 통째로 Airflow인데 근거 페이지가 0장.**
→ 판별 기준: *이번 주에 손댄 시스템 중 페이지 없는 것이 몇 개인가.*

**grep으로 확인한 공백:** `SCD` 0건 · `쿼리 최적화` 2건 · `파티션 프루닝` 2건 ·
데이터 품질 도구 0 · 비용 계산 0 · PII 실무 0.

**소스 우선순위를 두 축으로 병합했다.** 기존(로드맵 축) MinIO(1) > Zarr(2) > Iceberg(3) 에
**제너럴리스트 축**을 추가: **Airflow 공식 문서 · Prometheus+Grafana · DDIA · Postgres EXPLAIN.**
⭐⭐ DDIA는 강의가 **이름만 대고 넘어간** Brewer 2000/2012·Gilbert&Lynch·Lamport·FLP·Raft를
한 권이 덮는다 — **단일 강의 의존을 깨는 가장 효율 좋은 한 방**이고 PACELC 공백도 같이 닫는다.

⭐⭐ **성격이 다른 8번:** *자기 스택의 측정치를 source로 인제스트한다* — 샘플 크기 분포 ·
리더 실행 시간 · MinIO 객체 수/IOPS · Airflow task 지속시간 · 뷰어 줌 레벨 분포(로드맵 §5.1의
미검증 전제). **인제스트 대상이 남의 자료가 아니라 자기 시스템인 첫 source 페이지.**
`raw/`가 gitignore이므로 수치·해석만 source 페이지에 남기고, 공개 불가 값은 상대 비율로 옮긴다.

**노트에 폐기 조건 5개를 박아뒀다** — 1차 자료 5장 · 운영 도구 4개 entity · 측정치 source 1장 ·
MOC ⭐ 항목 절반 ✅ · 로드맵 §9 미검증 6항목 중 3개 해소. **진단에 유효기간을 준 것.**

**유보:** "1차 자료가 낫다"의 표본이 SpatialData 하나뿐이고, 강의도 CAP·하이브리드 검색 챕터는
좋다(나쁜 건 **평균**이지 전부가 아니다). §2.2의 "안 쓰는 도구" 판정은 현재 로드맵 기준이라
그래프·RAG가 제품 요구로 들어오면 뒤집힌다.

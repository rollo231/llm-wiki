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

# Index

Content catalog for this wiki. Each page is listed as a link plus a one-line summary.
Update it on every ingest and whenever a note is filed. Read it first when answering a query.

## Maps

- [[Bioinformatics]] — bioinformatics 영역의 진입점 (현재 공간 오믹스 데이터 인프라 중심).
- [[Data Engineering]] — data-engineering 영역의 진입점 (직무 개념 + 저장 포맷의 파이프라인 관점).

## Bioinformatics

### Concepts
- [[SpatialData elements]] — 데이터 모델의 빌딩 블록 5종(Images·Labels·Shapes·Points·Tables).
- [[Coordinate systems and transformations]] — intrinsic/extrinsic 좌표계와 element 정렬 방식.
- [[SpatialData Shapes element]] — Shapes 상세: circles vs polygons, `ShapesModel` 계약, 온디스크 레이아웃.
- [[SpatialData Zarr format versions]] — element 종류별 포맷 버전 체계와 컨테이너 조합 제약.
- [[Rasterization and vectorization]] — Labels ↔ Shapes 변환과 `rasterize()`·`rasterize_bins()`.
- [[Spatial aggregation]] — `aggregate()`: 영역별 값 집계로 cell × gene 표를 만드는 연산.
- [[Spatial queries in SpatialData]] — bbox·폴리곤 질의. 프루닝이 I/O를 줄이는 건 래스터뿐.
- [[Relational queries in SpatialData]] — SQL식 조인 5종·`get_values()`·`filter_by_table_query()`.
### Sources
- [[SpatialData docs - Design doc]] — SpatialData 공식 설계 문서(v0.8.0): 목표·비목표·사양·로드맵.
- [[spatialdata-io docs - README and readers]] — spatialdata-io v0.7.1의 README + 리더 소스 4종.
- [[SpatialData source - ShapesModel and shapes IO]] — spatialdata v0.8.0 소스 3종: `models.py`·`io_shapes.py`·`format.py`.
- [[SpatialData source - Shapes conversion and aggregation ops]] — spatialdata v0.8.0 `_core/operations/` 4종: vectorize·rasterize·rasterize_bins·aggregate.
- [[SpatialData source - Spatial and relational queries]] — spatialdata v0.8.0 `_core/query/` 2종(2,131줄) + 미해결 이슈 3건.
### Entities
- [[SpatialData]] — 공간 오믹스용 저장 포맷·스키마·인메모리 표현을 묶은 scverse 프레임워크.
- [[OME-NGFF]] — SpatialData가 교환 포맷으로 채택한 OME 차세대 이미징 사양(OME-Zarr).
- [[spatialdata-io]] — 장비 출력을 SpatialData로 읽는 리더 라이브러리(13종 지원).
- [[Visium]] — 10x의 spot 기반 공간 전사체 플랫폼.
- [[Visium HD]] — 10x의 2µm bin 기반 후속 플랫폼(+ 세포·핵 세그멘테이션).
- [[Xenium]] — 10x의 in situ 단분자 플랫폼(XOA 버전별 포맷 차이 주의).
- [[MERSCOPE]] — Vizgen의 in situ 단분자 플랫폼(MERFISH).
### Notes
- [[SpatialData as a data engineering substrate]] — DE 관점의 이점·한계와 그 위의 ETL 설계(카탈로그 스키마 중심).

## Programming

### Concepts
_(none yet)_
### Sources
_(none yet)_
### Entities
_(none yet)_
### Notes
_(none yet)_

## Data Engineering

### Concepts
- [[Traditional data engineering]] — 정형 데이터·DW·BI 중심의 기존 방식.
- [[AI data engineering]] — AI 모델 학습·추론과 비정형 데이터를 지원하는 방식.
### Sources
- [[AI DE Course - Ch1-1 OT]] — Fast Campus DE 강의 OT: 기존 DE vs AI DE.
### Entities
- [[AI Data Engineering (Fast Campus course)]] — Fast Campus DE 강의(챕터 트래커).
### Notes
- [[SpatialData as a data engineering substrate]] — 공간 오믹스 포맷을 레이크하우스 관점으로 읽고 ETL·카탈로그를 설계한다.

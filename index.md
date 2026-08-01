# Index

Content catalog for this wiki. Each page is listed as a link plus a one-line summary.
Update it on every ingest and whenever a note is filed. Read it first when answering a query.

## Maps

- [[Bioinformatics]] — bioinformatics 영역의 진입점 (현재 공간 오믹스 데이터 인프라 중심).
- [[Data Engineering]] — data-engineering 영역의 진입점 (파이프라인 단계별 개념 + 직무 + 저장 포맷).

## Bioinformatics

### Concepts
- [[Spatial omics vocabulary]] — mask·annotation·ROI·boundaries 용어 대응(SpatialData ↔ 현장 ↔ QuPath·napari·GeoJSON).
- [[Legacy AnnData spatial convention]] — SpatialData 이전 h5ad 관례(`obsm["spatial"]`)와 그 한계 — 왜 필요했는가.
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
- [[spatialdata-io source - Legacy AnnData converter]] — v0.7.1 `converters/legacy_anndata.py`: 레거시 h5ad 관례의 명세.
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
- [[AI DE Course - Part2 Ch4 Serving platforms]] — FastAPI 내부 구조(Starlette·Uvicorn·uvloop·
  Cython·Pydantic), WSGI vs ASGI. (data-engineering와 겹침)
### Entities
- [[FastAPI]] — Python 웹 프레임워크. 왜 빠른가(비동기 + C 컴파일), ASGI, ML 서빙에서의 위치.
### Notes
_(none yet)_

## Data Engineering

### Concepts
- [[ETL and ELT]] — 추출·변환·적재의 순서 문제, ELT를 가능케 한 것(스토리지 하락·MPP), 규제 때문에 ETL을 쓰는 경우.
- [[Change data capture]] — 트랜잭션 로그를 읽어 변경분만 실시간으로. Debezium·순서 보장·멱등성.
- [[Unstructured data ingestion]] — 비정형 4단계(수집·저장·처리·활용): OCR → 임베딩 → Vector DB → RAG.
- [[Columnar and in-memory data formats]] — Parquet은 스캔 최적화(predicate pushdown), Arrow는 처리, Avro는 쓰기·스키마 진화.
- [[Analytical data storage tiers]] — 웨어하우스/레이크/레이크하우스를 구조·쿼리엔진 결합·비용 축으로. + OLTP/OLAP.
- [[Table formats]] — Iceberg·Delta·Hudi: 레이크하우스를 만드는 층. ACID·time travel, Delta 트랜잭션 로그 구조.
- [[Batch and stream processing]] — 배치 vs 스트림, Kafka ≠ 메시지 큐, 오케스트레이터는 배치 전용.
- [[Latency and throughput]] — 시소의 법칙: 왜 둘을 동시에 못 갖나(CPU·네트워크·디스크). 마이크로배치·Lambda/Kappa.
- [[Stream processing semantics]] — 윈도우 3종·event time·워터마크·late data·상태·exactly-once. Flink vs Spark.
- [[Medallion architecture]] — bronze/silver/gold: 정제도의 축(모양은 말하지 않는다).
- [[Dimensional modeling]] — fact·dimension·star·grain·data mart, 그리고 "one big table" 반론.
- [[Data catalog and semantic layer]] — metastore(기계) ≠ data catalog(사람) ≠ semantic layer(정의) + lineage·거버넌스.
- [[Data SLA and observability]] — uptime은 데이터 건강을 증명하지 않는다. 침묵의 실패·3대 지표·서킷 브레이커.
- [[Data drift and training-serving skew]] — 에러 0건인데 모델만 망가지는 두 원인. 코드 불일치 vs 세상의 변화.
- [[Feature store]] — skew를 구조적으로 막는 장치. offline/online 두 스토어, 하나의 로직.
- [[Data and model versioning]] — 재현성 3요소(스냅샷·환경·시드). git만으로 안 되는 이유.
- [[Traditional data engineering]] — 정형 데이터·DW·BI 중심의 기존 방식.
- [[AI data engineering]] — AI 모델 학습·추론과 비정형 데이터를 지원하는 방식. 배관공 → 품질 지휘자.
- [[MLOps]] — ML 시스템을 운영 가능하게 만드는 체계. DevOps와의 차이, 라이프사이클 6단계.
- [[LLMOps]] — 관리 대상이 모델 → 제품 → 생성 시스템으로. hallucination·prompt injection·토큰 비용.
- [[Context engineering]] — Feature가 있던 자리를 컨텍스트가 대체한다. 품질과 비용이 같은 다이얼.
- [[ML data pipeline]] — 소비자가 사람이 아니다. 라벨링·데이터 검증·분할 전략·리니지.
- [[Batch and online serving]] — 같은 모델도 서빙 방식에 따라 전혀 다른 시스템이 된다.
- [[Model serving platforms]] — FastAPI·TorchServe·BentoML·Triton. 축은 추상화 수준 하나.
- [[Inference optimization]] — GPU는 마지막 수단. Total Latency 분해와 CPU 최적화 3종.
- [[Schema-centric data modeling]] — 관계형이 강한 이유와 무너지는 지점. 정규화는 업데이트 안정성.
- [[NoSQL]] — 4타입, 그리고 "확장성은 자동으로 해결되지 않는다". 파티션 키·CAP·분산된 운영 포인트.
- [[Data semantics]] — 스키마는 형식, 시멘틱은 의미. Entity·Attribute·Relationship·**Context**.
- [[Graph data model]] — node·edge·property·label, path·hop·pattern. Property Graph vs RDF 판단.
- [[Graph database]] — index-free adjacency, traversal vs JOIN. "빠르다"의 정확한 의미.
- [[Knowledge graph]] — entity와 fact. DE에게는 메타데이터 그래프와 리니지가 첫 활용처.
- [[Ontology]] — 클래스·속성·관계·제약, RDFS/OWL, SHACL. **스키마 복사가 아니라 의미 구조 재설계.**
- [[Knowledge graph pipeline]] — 원천 데이터 → 지식그래프 10단계. ETL 하나를 더 운영하는 일.
- [[Retrieval-augmented generation]] — RAG 구조와 한계 4종. 검색 단위는 chunk, 질문 단위는 structure.
- [[GraphRAG]] — 그 한계에 대한 그래프 기반 대응. MS 논문형·현실의 4패턴·변형 3종.
### Sources
- [[Data landscape guide for developers]] — OlegWock(sinja.io, 2026-07-14): 개발자를 위한 데이터 툴 랜드스케이프 지도.
- **AI DE 강의 Part 1** (Fast Campus, 16개 덱 / ~205p) — 파이프라인 순서대로:
  - [[AI DE Course - Ch1-1 OT]] — OT: 기존 DE vs AI DE.
  - [[AI DE Course - Ch1-2,3 Latency and Versioning]] — 두 마인드셋. (덱이 얇다)
  - [[AI DE Course - Ch1-4 Tech stack and tooling]] — 기술 스택 나열: Python·SQL·JVM·클라우드.
  - [[AI DE Course - Ch2-1,2,3 Storage evolution]] — 사일로 → DW → Lake → Lakehouse, OLTP vs OLAP.
  - [[AI DE Course - Ch2-4,5,6 Parquet and Avro]] — Parquet 내부·Avro 스키마 진화·compaction 패턴.
  - [[AI DE Course - Ch2-7 Delta Lake and ACID]] — 레이크가 늪이 되는 5가지, `_delta_log/` 구조.
  - [[AI DE Course - Ch3-1,2 Batch and ETL]] — 왜 ETL이었고 무엇이 바뀌어 ELT가 됐나.
  - [[AI DE Course - Ch3-3,4 CDC]] — 로그 기반 캡처 3단계, Debezium, MSA 동기화.
  - [[AI DE Course - Ch3-5,6 Unstructured data ingestion]] — 비정형 파이프라인 4단계와 RAG.
  - [[AI DE Course - Ch4-1,2 Batch vs Streaming]] — 트레이드오프의 물리적 근거와 밀리초 사례.
  - [[AI DE Course - Ch4-3,4 EDA and Kafka]] — Kafka는 기능을 빼서 이겼다. EDA·Hub&Spoke.
  - [[AI DE Course - Ch4-5,6 Stream processing engines]] — 윈도우·워터마크·상태, Flink vs Spark.
  - [[AI DE Course - Data drift and training-serving skew]] — 33배 뻥튀기 사례, 코로나·스팸 사례.
  - [[AI DE Course - Data SLA and pipeline monitoring]] — 침묵의 실패, 3대 지표, 서킷 브레이커.
  - [[AI DE Course - Data governance and catalog]] — 자물쇠에서 나침반으로, 카탈로그 자동화.
  - [[AI DE Course - AI pipeline case studies]] — Uber·Netflix·Tesla·Meta·Google·Airbnb 6개 사례.
- **AI DE 강의 Part 2** (Fast Campus, 5개 챕터 / 206p, 강사 Habi) — 학습·추론 시스템 설계:
  - [[AI DE Course - Part2 Ch1 Pipeline evolution and the DE role]] — 진화사 재탕 + Part 2 예고편.
  - [[AI DE Course - Part2 Ch2 MLOps and the ML lifecycle]] — DevOps와의 차이, 라이프사이클 6단계.
  - [[AI DE Course - Part2 Ch2 LLMOps]] — 컨텍스트 엔지니어링, prompt injection 4계층 방어, 비용 통제.
  - [[AI DE Course - Part2 Ch3 ML data pipeline]] — 라벨은 파이프라인의 일부다. 검증·분할·리니지.
  - [[AI DE Course - Part2 Ch3 Serving pipeline]] — Batch/Online 서빙, Feature 조회가 병목.
  - [[AI DE Course - Part2 Ch3 Training-serving skew patterns]] — ⭐ skew 4패턴과 "Training은 Serving을 따라간다".
  - [[AI DE Course - Part2 Ch4 Serving architecture]] — 온라인 서빙 6컴포넌트, 배치 오케스트레이터 3종.
  - [[AI DE Course - Part2 Ch4 Serving platforms]] — 4종 내부 구조 해부 + 비교표.
  - [[AI DE Course - Part2 Ch4 CPU and GPU inference]] — GPU는 마지막 수단. 전환 체크리스트 4문항.
  - [[AI DE Course - Part2 Ch5 Feature store in practice]] — Feature 재정의, "필요하지 않은 경우".
- **AI DE 강의 Part 3** (Fast Campus, 5개 챕터 / 273p) — 시맨틱 & 컨텍스트 기반 데이터 설계:
  - [[AI DE Course - Part3 Ch1 Schema design and RDBMS]] — RDBMS 기본과 스키마 중심 설계의 약점.
  - [[AI DE Course - Part3 Ch1 RDBMS limits and NoSQL]] — 한계 3종, NoSQL 4타입, "자동 스케일" 반박.
  - [[AI DE Course - Part3 Ch1 Semantics]] — ⭐ Part 3의 테제. 시멘틱 4요소와 실무 스펙트럼.
  - [[AI DE Course - Part3 Ch2 Graph fundamentals]] — 그래프 기초·종류·지식그래프·메타데이터 그래프.
  - [[AI DE Course - Part3 Ch2 Property graph vs RDF]] — 두 모델의 차이와 판단 6문항.
  - [[AI DE Course - Part3 Ch2 Graph in practice]] — 메타데이터·리니지·추천·검색 4개 use case.
  - [[AI DE Course - Part3 Ch2 Graph and AI]] — 세 층위, GNN, LLM 결합 3패턴, "모델보다 먼저 컨텍스트".
  - [[AI DE Course - Part3 Ch3 Ontology basics]] — RDF·RDFS·OWL, "OWL은 대체로 과설계".
  - [[AI DE Course - Part3 Ch3 Ontology design principles]] — ⭐ 설계 실무 원칙. 스키마 복사 금지.
  - [[AI DE Course - Part3 Ch3 Knowledge graph pipeline]] — 10단계. 단계 수 불일치 주의.
  - [[AI DE Course - Part3 Ch3 SHACL and graph data contracts]] — 그래프용 테스트 코드, Turtle.
  - [[AI DE Course - Part3 Ch4 RAG and its limits]] — ⭐ 한계 4종. 이 코스에서 출처가 가장 좋다.
  - [[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]] — MS 논문형, 현실의 4패턴, 사례 2건.
  - [[AI DE Course - Part3 Ch4 GraphRAG variants and products]] — Auto-Tuning·DRIFT·LazyGraphRAG.
  - [[AI DE Course - Part3 Ch5 Graph databases]] — 엔진 원리와 제품 4종. "실습"인데 실습은 없다.
### Entities
- [[AI Data Engineering (Fast Campus course)]] — Fast Campus DE 강의 챕터 트래커(5파트/41덱/~1,155p, Part 1·2·3 완료).
- [[Apache Kafka]] — 토픽·파티션·오프셋, 순서 보장의 범위, 로그 컴팩션, Zero-Copy, KRaft.
- [[NVIDIA Triton Inference Server]] — per-model scheduler·dynamic batching·model ensemble. K8s 궁합 최상.
- [[BentoML]] — API Server와 Runner 분리 → CPU/GPU 독립 스케일링. Bento·Yatai 패키징.
- [[TorchServe]] — Java frontend / Python backend, handler와 `.mar`. Frontend가 병목이자 SPOF.
- [[ONNX]] — 프레임워크 독립 그래프 표준 + 추론 전용 런타임(operator fusion, AVX).
- [[Neo4j]] — native graph + Cypher. 관계 탐색 중심 애플리케이션과 GraphRAG 백엔드.
- [[Amazon Neptune]] — 완전관리형 그래프 DB. Property Graph와 RDF를 모두 지원.
- [[ArangoDB]] — key-value·document·graph를 한 엔진에서. AQL 하나로 문서 질의 + traversal.
- [[JanusGraph]] — 분산 스토리지(Cassandra·HBase) 위에 올라가는 graph engine. 초대규모용.
- [[DataHub]] — 메타데이터 그래프의 대표 구현. 강의는 로고 수준으로만 언급.
- [[Microsoft GraphRAG]] — GraphRAG라는 이름을 만든 논문·구현체. 변형 3종(Auto-Tuning·DRIFT·Lazy).
### Notes
- [[SpatialData as a data engineering substrate]] — 공간 오믹스 포맷을 레이크하우스 관점으로 읽고 ETL·카탈로그를 설계한다.

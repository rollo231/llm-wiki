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
- [[SpatialData and Sedona interop]] — ⭐⭐ **SpatialData ↔ [[Apache Sedona]]/[[SedonaDB]]가 만나는 지점 전체.**
  `points.parquet`·`shapes.parquet`은 이미 엔진이 읽고, 좌표변환 이음새는 [[Xenium]]·[[MERSCOPE]]
  리더에서 **상쇄된다**(소스 확인). issue #210 우회의 4단계가 2단계로 줄었다.
- [[SpatialData as a data engineering substrate]] — DE 관점의 이점·한계와 그 위의 ETL 설계(카탈로그 스키마 중심).
- [[Spatial omics platform roadmap]] — 플랫폼 3종 고정 + 실제 스택(K8s·Airflow·MinIO·Postgres) 기준
  아키텍처 평가와 단계별 도입 순서. **"3개 플랫폼이 아니라 2개 워크로드다."**

## Programming

_아래는 모두 data-engineering 영역과 겹친다 — 전체 맥락은 그쪽 섹션에서 본다._

### Concepts
- [[Large language model]] — 자가회귀 언어 모델의 성질과 계보(N-gram→RNN→Transformer), GPT vs BERT.
- [[Transformer architecture]] — Self-Attention(Q/K/V)·Multi-Head·FFN·Residual·Positional Encoding.
- [[Tokenization]] — BPE와 서브워드, 한국어 조사 분리, 토큰이 곧 비용·컨텍스트 단위.
### Sources
- [[AI DE Course - Part2 Ch4 Serving platforms]] — FastAPI 내부 구조(Starlette·Uvicorn·uvloop·
  Cython·Pydantic), WSGI vs ASGI.
- [[AI DE Course - Part5 LLM foundations and NLP history]] — LLM 계보와 GPT/BERT 비교.
- [[AI DE Course - Part5 Transformer internals]] — 모델 내부 구조.
- [[AI DE Course - Part5 RAG pipeline and LangChain]] — RAG 구축 5단계와 LangChain.
### Entities
- [[FastAPI]] — Python 웹 프레임워크. 왜 빠른가(비동기 + C 컴파일), ASGI, ML 서빙에서의 위치.
- [[LangChain]] — LLM 애플리케이션 조립 프레임워크. Prompts·LLMs·Chains·Agents.
- [[GPT]] — Decoder 계열 자가회귀 모델. 생성 쪽 계보의 대표.
- [[BERT]] — Encoder 계열 양방향 모델. 임베딩·리랭킹에서 현역.
### Notes
_(none yet)_

## Data Engineering

### Concepts
- [[ETL and ELT]] — 추출·변환·적재의 순서 문제, ELT를 가능케 한 것(스토리지 하락·MPP), 규제 때문에 ETL을 쓰는 경우.
- [[Change data capture]] — 트랜잭션 로그를 읽어 변경분만 실시간으로. Debezium·순서 보장·멱등성.
- [[Unstructured data ingestion]] — 비정형 4단계(수집·저장·처리·활용): OCR → 임베딩 → Vector DB → RAG.
- [[Columnar and in-memory data formats]] — Parquet은 스캔 최적화(predicate pushdown), Arrow는 처리,
  Avro는 쓰기·스키마 진화. ✅ **ORC vs Parquet은 생태계 문제였다.** + Flight SQL·OpenDAL·CarbonData 계층 구분.
- [[Analytical data storage tiers]] — 웨어하우스/레이크/레이크하우스를 구조·쿼리엔진 결합·비용 축으로. + OLTP/OLAP.
- [[Table formats]] — Iceberg·Delta·Hudi·**Paimon**: 레이크하우스를 만드는 층. ACID·time travel,
  Delta 트랜잭션 로그, **선택 3축**(엔진 공유/잦은 변경/스트림-배치), Hudi **CoW vs MoR**.
  **Hive는 경로에 의미를 실었고 Iceberg는 해방했다** — 그리고 **"테이블의 기준은 파일인가 메타데이터인가."**
- [[Object storage layout]] — **오브젝트 스토리지엔 디렉토리가 없다.** 경로 = 권한·생애주기,
  나머지는 카탈로그. 세 문항 테스트와 실패 5종.
- [[SQL execution layer]] — **저장만으로는 아무도 데이터를 볼 수 없다.** 테이블 규칙 → SQL 실행 →
  접속·소비 3단계, 엔진 유형 6종. ⚠️ 이 층의 실제 기본값은 Apache 밖에 있다.
- [[Consumption layer]] — **가르는 축은 제품이 아니라 조회 형태다.** 6종(검색·실시간집계·사전집계·
  키조회·시계열·인메모리) + 팬아웃 원칙과 그 값. ⚠️ 소스에 벡터 검색이 빠져 있다.
- [[Data orchestration]] — ⭐⭐ **먼저 정할 것은 도구 이름이 아니라 운영 방식이다** — 누가 만들고
  배포하나·실패 알림·권한·비밀정보. 역할 3분할(수집/CDC/오케스트레이션).
- [[Data integration tools]] — 같은 "데이터를 옮긴다"인데 축이 셋(라우팅 가시성 / 변환 UX / 커넥터
  동기화). ⚠️ Camel은 애플리케이션 통합 — 데이터 도구와 섞지 않는다.
- [[Batch and stream processing]] — 배치 vs 스트림, Kafka ≠ 메시지 큐, 오케스트레이터는 배치 전용.
  ⭐⭐⭐ **엔진보다 먼저 시간을 자른다 — "최대 허용 지연" 숫자가 경계선이다.** + Beam·StreamPark.
- [[Latency and throughput]] — 시소의 법칙: 왜 둘을 동시에 못 갖나(CPU·네트워크·디스크). 마이크로배치·Lambda/Kappa.
- [[Stream processing semantics]] — 윈도우 3종·event time·워터마크·late data·상태·exactly-once. Flink vs Spark.
- [[Medallion architecture]] — bronze/silver/gold: 정제도의 축(모양은 말하지 않는다).
- [[Dimensional modeling]] — fact·dimension·star·grain·data mart, 그리고 "one big table" 반론.
- [[Data catalog and semantic layer]] — metastore(기계) ≠ data catalog(사람) ≠ semantic layer(정의)
  + lineage·거버넌스. ⭐⭐ **거버넌스 삼각형**(무엇이 있나/누가 보나/믿을 만한가) + **카탈로그는 단일
  제품이 아니라 역할 구조다.**
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
- [[Distributed processing]] — 분산의 대상 4종, 도입 판단 3축. **"단일 서버로도 감당 가능한가."**
- [[CAP theorem]] — Brewer의 2012년 정정. "셋 중 둘"이 아니다. CAP의 C ≠ ACID의 C.
- [[Distributed system limits]] — 부분 실패·전역 시계 부재(Lamport)·FLP. 실무는 timeout으로 회피.
- [[Replication and consensus]] — 목표·수단·제어의 계층. RTO/RPO, Raft, **과반수의 역설**.
- [[Cluster resource scheduling]] — **누가 얼마나 쓸지.** YARN 3종 + **저장/처리 결합 해제의 계보** +
  YuniKorn 도입 신호(관찰 가능한 증상).
- [[Caching strategies]] — 4패턴·무효화 3종·근거가 붙은 TTL 표. hit가 없으면 캐시는 손해다.
- [[Message broker]] — 소비 의미론 6축으로 분류. exactly-once의 범위 경고, 멱등 소비 7장치.
- [[Lambda and Kappa architecture]] — 재처리를 아키텍처 요구로. 현대 5축(Lakehouse·Unified Path…).
- [[GPU architecture]] — 실리콘 면적 배분·SIMT·Roofline. **PCIe와 HBM의 40~50배 절벽.**
- [[GPU resource allocation]] — MIG/MPS/time-slicing, 4계층 설계, 동적 프로비저닝의 한계 6종.
- [[Large language model]] — 하는 일은 하나(다음 토큰 확률). 자가회귀 → 출력 길이가 곧 latency.
- [[Transformer architecture]] — 속도를 얻고 순서를 잃은 뒤 다시 사 온 구조. Q/K/V·FFN·Residual·PE.
- [[Tokenization]] — 토큰은 비용의 단위이자 컨텍스트 한도의 단위. BPE와 한국어 조사 분리.
- [[Text embeddings]] — 정적 vs 문맥 vs 멀티모달. ⚠️ 모델을 바꾸면 인덱스를 다시 만들어야 한다.
- [[Vector database]] — ANN(IVF·HNSW)의 다이얼은 정확도↔지연 하나. ⚠️ FAISS는 DB가 아니다.
- [[Hybrid search and reranking]] — ⭐ "의미는 남고 식별자는 사라진다". BM25·RRF·Cross-Encoder.
- [[Retrieval evaluation metrics]] — Stage 1은 Recall@K, Stage 2는 NDCG@K. 단계마다 다른 지표.
- [[Spatial join execution]] — ⭐ 조인 키가 없는 조인. **격자 ≠ 인덱스 ≠ refine**, 파티셔닝은 복제한다.
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
- **AI DE 강의 Part 4** (Fast Campus, 5개 챕터 / 431p) — 실시간 & 대규모 분산 처리 설계
  ("물리적으로 어디서 막히는가"):
  - [[AI DE Course - Part4 Ch1 Distributed processing basics]] — GFS→MapReduce→Spark 계보 +
    **"분산이 정말 필요한가"** 반론.
  - [[AI DE Course - Part4 Ch1 CAP theorem and system limits]] — ⭐ 이 코스 최고의 출처.
    Brewer 2012 정정·Lamport·FLP.
  - [[AI DE Course - Part4 Ch1 HA replication and consensus]] — RTO/RPO, sync/async, Raft,
    과반수의 역설.
  - [[AI DE Course - Part4 Ch2 Redis and the caching layer]] — 성능 요소 9종, 싱글 스레드 + O(N).
  - [[AI DE Course - Part4 Ch2 Caching strategies and TTL]] — 5전략·무효화 3종·TTL 표.
  - [[AI DE Course - Part4 Ch3 Message brokers]] — 소비 의미론 6축, exactly-once 경고.
  - [[AI DE Course - Part4 Ch3 Brokers vs stream processing engines]] — 운반 vs 계산, State Backend.
  - [[AI DE Course - Part4 Ch3 Event time watermarks and windows]] — 넣기/닫기/내보내기 3분할.
  - [[AI DE Course - Part4 Ch3 Lambda Kappa and modern architecture]] — 재처리 5단계, 현대 5축.
  - [[AI DE Course - Part4 Ch4 GPU architecture and CUDA]] — ⭐ coalescing→컬럼너, Roofline, PCIe.
  - [[AI DE Course - Part4 Ch4 GPU allocation architecture]] — MIG/MPS 비교, scale-out vs scale-up.
  - [[AI DE Course - Part4 Ch4 GPU in data engineering and RAPIDS]] — RAPIDS 생태계.
    ⚠️ 사례 수치 모순.
  - [[AI DE Course - Part4 Ch5 AI system metrics and SLA]] — SLI/SLO/Error Budget, 비용 SLO.
  - [[AI DE Course - Part4 Ch5 Monitoring dashboards and alerts]] — 대시보드 5종, 알람 4조건.
  - [[AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling]] — ⭐ GPU 3축 해석표.
- **AI DE 강의 Part 5** (Fast Campus, 3개 덱 / 40p) — LLM·RAG ("모델 상자를 연다"):
  - [[AI DE Course - Part5 LLM foundations and NLP history]] — N-gram→RNN→Transformer→GPT/BERT.
    ⚠️ LSTM 연도 오류, GPT-4 파라미터.
  - [[AI DE Course - Part5 Transformer internals]] — 토큰화·BPE·임베딩층·Q/K/V·FFN·PE.
  - [[AI DE Course - Part5 Embeddings and vector search]] — 임베딩 알고리즘 6종, 벡터 DB, 검색 5단계.
    ⚠️ 장식 수치 다수.
  - [[AI DE Course - Part5 RAG pipeline and LangChain]] — 구축 5단계와 LangChain.
    ⚠️ Part 3 Ch4보다 얕다.
  - [[AI DE Course - Part5 Hybrid search and reranking]] — ⭐⭐ Part 5의 실질적 수확 전부.
    BM25·RRF 수식, Two-Stage, Bi/Cross-Encoder, 평가지표. **RRF 예시 검산 통과.**
- **Apache 기술 지도 (책)** (이현수/hyunsooIT, 2026 · 11장 / 개념 90개 / 104p) — 깊이가 아니라
  **넓이 + 선택 기준**. **전 장 완주 (11/11)**:
  - [[Apache Map - Ch1 How to read this book]] — 책 전체의 좌표계. 역할 5단계 + 가로지르는 2계층,
    Tier 체계, 레이크하우스 스택 vs 실시간 스택. ⚠️ **기본 스택 5개에 카탈로그가 없다.**
  - [[Apache Map - Ch8 SQL on the lake]] — ⭐ 위키 최대 공백이었던 장. 논지는 마지막 개념 하나.
    ⚠️ **Tier 1이 0개인 이유 = 이 계층의 기본값(Trino·SaaS)이 Apache 밖에 있다.** 👍 출처 없는 수치 0건.
  - [[Apache Map - Ch9 Serving OLAP search and NoSQL]] — ⭐⭐ **"필요한 기능을 문장으로 적고 그 문장에
    직접 연결되는 기술부터."** Druid vs Pinot = 누가 보는가. ⚠️ 벡터 검색 없음 · Tier 왜곡 2차 확인.
  - [[Apache Map - Ch7 Ingestion and orchestration]] — ⭐⭐ **판단 기준의 질이 가장 높은 장.**
    Airflow vs DolphinScheduler = 팀의 운영 문화. ⚠️ "오케스트레이션의 가치"만 말하고 "비용"은 없다.
  - [[Apache Map - Ch6 Open table formats]] — 새 페이지 없이 [[Table formats]]의 공백을 메운 장.
    ⭐ **"테이블의 기준은 파일인가, 메타데이터인가."** ⚠️ Delta가 없다(Apache 아님) · 위키 스케치가 더 자세하다.
  - [[Apache Map - Ch10 Governance and BI]] — ⭐⭐ **거버넌스 삼각형** + **"우리 팀에서 비어 있는 축이
    어디인지."** Ch1의 *카탈로그가 없다* 와 Hive Metastore 승격 판단이 함께 종결. ⚠️ 읽는 규칙 첫 예외.
  - [[Apache Map - Ch2 Distributed foundations]] — ⭐⭐ **합의는 선택이 아니라 형태만 선택**(외부 서비스
    vs 내장 라이브러리). **YARN이 저장/처리 결합을 푼 것 = 레이크하우스의 한 세대 앞선 형태.**
  - [[Apache Map - Ch3 Event streaming]] — 보정 인제스트. **재생 가능 여부가 큐/로그를 가르는 가장 쉬운
    기준** · Kafka vs Pulsar는 **조직의 형태**가 축이다.
  - [[Apache Map - Ch4 Batch and stream engines]] — ⭐⭐⭐ **엔진보다 먼저 시간을 자른다.**
    **"SLA를 평균이 아니라 최대 허용 지연으로 정하면 배치/스트림 경계가 명확해진다."** + Beam·StreamPark.
  - [[Apache Map - Ch5 Formats and exchange layer]] — ✅ **ORC vs Parquet 공백 해소**(축은 성능이 아니라
    생태계). Arrow Flight SQL·OpenDAL·CarbonData = 각각 다른 계층.
  - [[Apache Map - Ch11 Specialized analytics and libraries]] — ⭐⭐ **Sedona**가 [[Spatial aggregation]]의
    issue #210 제약에 분산 우회 경로를 붙인다. + 표준/이식 계층 5종 · ML 3갈래 · **오차 다이얼**.
- **Apache Sedona 공식 문서** (tag `sedona-1.9.1`, 2026-08-05) — Ch11이 남긴 *"구조를 주지 않는다"* 를 메운다:
  - [[Apache Sedona docs - Spatial join execution]] — ⭐⭐ 격자(kdbtree)·인덱스(rtree)·refine, 물리 연산자 3종,
    파라미터 표. ⚠️ **`LEFT JOIN`은 최적화되지 않는다** · 거리 단위 = 좌표계 단위 · S2 오차 다이얼.
  - [[Apache Sedona docs - Storage and formats]] — GeoParquet bbox 파일 스킵은 **쓰기 시점 정렬**로 산다.
    covering 컬럼 · Box2D row-group pushdown. ⚠️ 문서가 스스로 **Iceberg v3**를 권한다.
  - [[Apache Sedona docs - Runtimes and GeoStats]] — ⭐⭐ 런타임 4종 · **`sedonadb-zarr`** ·
    RayBooster(RT 코어) · **GeoStats**(DBSCAN·Gi\*·Moran's I) · GeoPandas 호환 API.
### Entities
- [[AI Data Engineering (Fast Campus course)]] — Fast Campus DE 강의 챕터 트래커(5파트/41덱/~1,155p, **전 파트 완료**).
- [[Apache data technology map (book)]] — Apache 프로젝트 90개 지도의 장 트래커(11장, 1/11). Tier 1/2 라벨 + 비교 절 11개. **위키 공백 42개를 지목한다.**
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
- [[Redis]] — 인메모리 key-value. 자료구조 6종, 성능 요소 9종. ⚠️ CP 시스템이 아니다.
- [[Apache Hadoop]] — GFS·MapReduce의 오픈소스 구현. 분산 처리 계보의 뿌리.
- [[Apache Spark]] — In-Memory + DAG. 배치 ETL의 표준, Structured Streaming, Spark RAPIDS.
- [[Apache Calcite]] — SQL 파서·검증·옵티마이저 프레임워크. **여러 엔진이 비슷한 문법을 쓰는 이유.** 설치 목록엔 없다.
- [[Apache DataFusion]] — Arrow 배치 위의 Rust SQL 엔진. 제품 **안에 심는** 미니 엔진. Arrow 생태계의 마지막 칸.
- [[Apache Lucene]] — 역색인 라이브러리. 토큰화→역색인→스코어링. **BM25가 사는 곳** (Solr·ES·OpenSearch의 기반).
- [[Apache Cassandra]] — 멀티리전 wide-column NoSQL. 파티션 키 분산·쓰기 확장. CAP에서 가용성을 택한 쪽의 교과서.
- [[Apache HBase]] — HDFS 위의 키 조회. ⚠️ **행키 설계가 곧 운영이다** — 분산과 범위 조회가 서로 당긴다.
- [[Apache Airflow]] — DAG·스케줄·의존·재시도. 오케스트레이션의 사실상 표준. **무엇을 하는지는 모른다.**
- [[Apache Polaris]] — Iceberg 특화 REST 카탈로그. **Hive Metastore의 역할을 이어받는다.**
  ⭐ 로드맵의 Postgres 카탈로그 결정을 뒤집지 않고 확인해 준다.
- [[Apache Superset]] — SQL 기반 BI·셀프서비스. 레이크하우스 스택의 "화면" 칸.
  ⚠️ **BI가 거버넌스를 대신하지 않는다.**
- [[Apache ZooKeeper]] — 리더 선출·설정·생존·잠금. **"누가 무엇을 맡는지"를 맞추는 계층.**
  Ratis(내장 Raft)와의 대비 = 합의 계층을 어디에 두나.
- [[Apache Sedona]] — 공간 데이터 엔진 계열. **런타임 4종**(Spark·Flink·Snowflake·SedonaDB), 1.9.1.
  ⭐ bioinformatics ↔ data-engineering을 잇는 항목 → [[SpatialData and Sedona interop]].
- [[SedonaDB]] — Rust 단일 노드(Arrow + DataFusion). ⭐ **`sedonadb-zarr`가 Zarr를 청크=행으로 읽는다.**
  RT 코어로 공간 조인을 가속하는 RayBooster(VLDB 2026).
- [[Apache Flink]] — 상태와 시간 제어를 전면에. RocksDB state backend, 체크포인트.
- [[CUDA]] — Thread/Block/Grid ↔ Core/SM/Device 1:1 매핑, SIMT, operator fusion.
- [[NVIDIA RAPIDS]] — cuDF·Spark RAPIDS·Dask-cuDF·RMM. Arrow 기반. ⚠️ 사례 수치 인용 주의.
- [[LangChain]] — LLM 앱 조립 프레임워크. Prompts·LLMs·Chains·Agents. 추상을 얻고 제어를 내준다.
- [[GPT]] — Transformer Decoder 계열, 자가회귀 생성. ⚠️ GPT-4 파라미터는 미공개다.
- [[BERT]] — Encoder 계열, 양방향·MLM. **RAG 검색단의 현역** — SBERT 임베딩과 Cross-Encoder 리랭킹.
### Notes
- [[SpatialData as a data engineering substrate]] — 공간 오믹스 포맷을 레이크하우스 관점으로 읽고 ETL·카탈로그를 설계한다.
- [[Spatial omics platform roadmap]] — 코스의 정석 패턴을 실제 스택 하나에 전부 적용한 결과.
  **"정석은 도입 목록이 아니라 도입 순서다"**, 정렬 축은 되돌릴 수 있는가. 카탈로그 Iceberg→Postgres 정정.
- [[SpatialData and Sedona interop]] — ⭐⭐ **위키의 두 영역이 처음으로 코드 수준에서 맞물린 노트.**
  *"불투명 blob"* 정정 · 좌표변환 상쇄를 리더 소스로 확인 · 판단 문턱을 *레이크 규모* → *issue #210이
  터지는 순간* 으로 내렸다.
- [[Apache technology map - what it gave and what it did not]] — ⭐⭐ Apache 책 완주 총평.
  **"깊이를 팔아 판단 축을 샀다."** 판단 축 4종 · 합의할 숫자 둘(**허용 지연·허용 오차**) ·
  주지 않은 것 6종 · 다음에 읽을 것 5건.
- [[Wiki gap analysis - DE readiness]] — ⭐ 위키 자체를 진단한다. **"개념 → 강의 → 재구성 축으로만
  두껍다"** — 1차 자료·운영 도구·자기 측정치 세 축이 얇다. 다음 소스 우선순위 8건 + 폐기 조건.

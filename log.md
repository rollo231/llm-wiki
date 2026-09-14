# 로그

위키 활동의 시간순 기록. 추가만 하고, 새 항목은 맨 아래에 붙인다.
항목 머리 형식: `## [YYYY-MM-DD] <ingest|query|lint|schema> | 제목`

## [2026-09-14] schema | 위키 초기화 — gist 골격으로 재시작

- 이전 위키를 전부 지우고 다시 시작했다 — 페이지 200개(source 82 · concept 68 · entity 41 · note 7 ·
  MOC 2)와 로그 1,695줄. 이전 내용은 git 커밋 `12f3ead` 에 남아 있다.
- 원본은 `raw/data-engineering/ai-de-course/`(패스트캠퍼스 AI 데이터 엔지니어링 강의, 5파트 PDF 40개)만
  남겼다. 나머지 raw 자료(SpatialData·spatialdata-io·Apache Sedona·MinIO 문서, 데이터 지형 가이드,
  Apache 기술 지도 책)는 완전히 삭제했고, 거기 딸린 `docs/experiments/` 도 지웠다.
- 스키마(`CLAUDE.md`)와 README 를 한국어로 다시 썼다. 카파시 gist 의 골격 — raw 불변 · wiki 는 에이전트
  소유 · 스키마, 인제스트·질의·린트, index·log — 만 두고, 강의 인제스트에 필요한 규칙 두 가지(주제 단위
  source 페이지, 트래커 entity)를 더했다. `area` 필드·MOC·URL 스냅샷·실험 하네스 규칙은 뺐다 — 필요해지면
  그때 다시 들인다.
- 이름 규칙: 사람이 읽는 것(파일명·제목·링크·본문)은 한국어, 기계가 읽는 것(frontmatter 키·`type` 값·
  폴더명·로그 키워드)은 영어. 로그 키워드에 `schema` 를 더했다.
- 다음: AI DE 강의 Part 1 인제스트 — 트래커 entity 부터.

## [2026-09-14] ingest | AI DE 강의 Part 1

- 원본: `raw/data-engineering/ai-de-course/part1/` PDF 25개, 282p 전부 읽음. 텍스트가 적은 덱(02·04)과 텍스트가 없는
  슬라이드는 이미지로 확인했다(모두 섹션 타이틀).
- 합의한 분할: 같은 제목으로 이어지는 덱은 한 강의로 묶어 **16장**(04+05, 06~08, 16~18, 19~21, 22~24). 파일명은
  `AI DE 강의 1-NN 주제`(순번은 위키가 붙임). concept·entity는 중간 세밀도. 1회차 위키는 참고하지 않았다.
- 새 페이지 42개: source 16, concept 18(AI 데이터 엔지니어링 · 지연 시간과 처리량 · 데이터와 모델 버전 관리 · 행 기반과
  열 기반 저장 · 데이터 레이크하우스 · 스키마 진화 · ETL과 ELT · 배치 처리 · 변경 데이터 캡처 · 비정형 데이터 파이프라인 ·
  이벤트 기반 아키텍처 · 스트림 처리 · 학습-서빙 스큐 · 데이터 드리프트 · 피처 스토어 · 데이터 SLA · 데이터 관측성 · 데이터
  거버넌스와 카탈로그), entity 8(AI 데이터 엔지니어링 강의(트래커) · Apache Kafka · Apache Parquet · Apache Avro · Delta
  Lake · Apache Flink · Apache Spark · Debezium).
- **외부 사실 16건을 1차 자료와 대조했다**(공식 문서·원 논문·회사 엔지니어링 블로그). 틀림: CDC 덱의 스키마 호환성 정의
  (뒤바뀜), Kafka "Fortune 500"(공식은 Fortune 100), 사례 덱의 Uber "2%"(Google TFX 논문의 수치), Parquet 메타데이터 "헤더"
  (footer), "OpenAI Titan"(Amazon). 낡음: Kafka ZooKeeper "제거 예정"(4.0에서 제거됨), Spark DStream(레거시), Tesla Dojo
  (2025-08 중단). 근거가 약함: PSI 0.2(관례는 0.1/0.25), zero-copy "CPU 60%"(원 보고는 전송 시간 65%), 두 "80%" 통계.
- **코스 내부 모순**: 호환성 정의(1-05 vs 1-08), Avro 분류(1-04 vs 1-05), Spark 세대(1-10 vs 1-12), 데이터 품질 축 세 버전
  (1-13·1-14·1-16). 결함 표는 트래커 [[AI 데이터 엔지니어링 강의]]에 모았다.
- 검산: 스큐 예시 20,000원 vs 673,333.33원(33.67배) — 강의 계산이 맞다. 다만 차이가 취소 부호와 분모 두 군데에 있다.
- 다음: Part 2 인제스트.

## [2026-09-14] ingest | AI DE 강의 Part 2

- 원본: `raw/data-engineering/ai-de-course/part2/` PDF 5개, 206p 전부 읽음. 텍스트가 없는 슬라이드 23장은 이미지로 확인했다
  (도식·밈·채용 공고 캡처). Part 2는 전체 제목(「AI 학습/추론 중심 데이터 파이프라인 설계」)과 강사 표기("Habi")가 있다.
- 합의한 분할: Part 2는 덱 하나에 번호 붙은 소단원이 여러 개라 **소단원 기준 10장**(Ch1 전체 · Ch2 1+2 · Ch2 3 · Ch3 1 · 2 ·
  3 · Ch4 1 · 2+3 · 4 · Ch5). 트래커 분할 규칙에 소단원 규칙을 더했다. 세밀도 중간, 강사 표기 기록.
- 새 페이지 21개: source 10, concept 5(MLOps · LLMOps · 모델 서빙 · 추론 최적화 · 데이터 누수), entity 6(Designing Machine
  Learning Systems · FastAPI · TorchServe · BentoML · Triton Inference Server · ONNX).
- 고친 페이지 13개: concept 10(피처 스토어 · 학습-서빙 스큐 · 데이터 드리프트 · AI 데이터 엔지니어링 · 데이터와 모델 버전 관리 ·
  지연 시간과 처리량 · 비정형 데이터 파이프라인 · ETL과 ELT · 스트림 처리 · 데이터 거버넌스와 카탈로그), source 1(1-13), 트래커,
  index.
- **외부 사실 21건을 1차 자료와 대조했다**(공식 문서·GitHub 저장소·원저자 강의 노트). 틀림: Triton "비즈니스 로직 직접 구현
  불가"(Python backend·BLS), FastAPI 도식의 Pydantic = Cython(v1 시절), ONNX Runtime "MKL·OpenMP"(v1.7부터 OpenMP 없음).
  낡음: TorchServe(2025-08 보관), BentoML Runner·Yatai(레거시·보관), Flyte(작성 뒤 Flyte 2 GA). 과장: "WSGI는 한 번에 한
  요청", CPU FP16 효과, Triton "파이썬 오버헤드 완벽 제거". 출처 누락: 배치 vs 온라인 표(Chip Huyen). 표준 용어 아님: Context
  Drift·Prompt Drift. 출처 없음: "인프라 관리 70%". 맞음: 라이프사이클 6단계, 피처 스토어가 필요 없는 조건 다섯 가지, 시간 기반
  분할·그룹 누수, TorchServe 포트.
- **위키 정정**: Part 1 때 위키가 쓴 "스큐 = 코드, 드리프트 = 세상, 원인이 반대"가 Google의 정의(Rules of ML — 학습-서빙 성능
  차이, 원인에 데이터 변화 포함)에 비추어 과장이었다. 강의(2-06)가 맞다. 학습-서빙 스큐·1-13·데이터 드리프트를 좁혀 고치고
  정정 표시를 남겼다.
- 코스 내부 결함: Ch5 제목의 "운영" 내용 누락, Ch2~5 템플릿 머리글, 중복 슬라이드, 2-07의 "조회 실패 시 기본값"과 2-06의
  "조회 실패를 0으로 처리하면 스큐"가 이어지지 않음. 결함 표는 트래커 [[AI 데이터 엔지니어링 강의]]에 모았다.
- 다음: Part 3 인제스트.

## [2026-09-14] lint | Part 1·2 뒤 1차 린트

- 범위(사용자 결정): ① 위키 자신의 사실 주장 대조 ② Part 1·2가 함께 고친 개념 11개의 이음새 ③ 자기 페이지가 없는 개념
  (보고만). 기계 검사(frontmatter·제목·타입·alias·링크·고아·index·log 머리)는 페이지 63개 0오류 — 오류 9종을 주입한 복사본에서
  9종 모두 검출해 검사가 공허하지 않음을 확인했다.
- **① 사실 주장.** `*(위키의 …)*` 93건은 대부분 해석·연결이다. 사실을 담은 것과 표시 없는 위키 주장을 골라 대조했다. 강의 내부
  주장(원본 PDF 텍스트 대조) — 맞음: Self-Healing 명칭, 스케일링 통계가 Part 2에서야 나옴, 누수 절 없음, Allowed Lateness
  서술. 외부 8건(1차 자료 대조) — 틀림: 스키마 진화 "안전 목록 = 모두 FULL 호환"(타입 확대는 BACKWARD만), LLMOps "SQL 인젝션
  방어와 구조가 같다"(NCSC 2025-12-08: 데이터와 지시의 경계가 없다). 단서 필요: Triton을 런타임 층에 둔 분류(모델 서버 — ONNX
  Runtime은 백엔드), 가지치기 효과(비구조적은 dense 커널에서 이득 없음), CDC 중단 시 로그(PostgreSQL은 WAL 누적, MySQL은 binlog
  삭제로 위치 상실), Kafka "선형 확장"·zero-copy(TLS면 sendfile 안 씀), 체크포인트 exactly-once(엔진 상태 한정, end-to-end는
  싱크 필요). 맞음: Google ML Glossary의 스큐 정의(인용 추가).
- **② 이음새.** 페이지끼리 어긋남: 데이터 레이크하우스 "Iceberg는 이름이 없다"(1-16에 싱크로 나옴), 행 기반과 열 기반 저장
  "같은 강의의 덱 08"(1-05), MLOps "2·4·5단계" vs 2-02(→ 2~5단계). 스큐 정정이 덜 번진 곳: index의 1-13 요약, 1-13 핵심 헤드라인,
  학습-서빙 스큐의 "원인" 절 제목. 용법: 데이터 드리프트 감지 절·데이터 관측성 표의 학습 vs 서빙 비교(TFDV·Vertex 용법으로는
  스큐 감지). 단정: "피처 조회가 지연의 대부분"(지연 시간과 처리량·모델 서빙). 허브 표 분류(AI 데이터 엔지니어링 ↔ 트래커),
  1-09 문구. 빠진 교차참조: 2-04 라벨 → 데이터 SLA·데이터 드리프트, 데이터 관측성 ↔ 2-07 서킷 브레이커. alias: Delta Lake의
  `ACID` 제거.
- **중복 정리**(사용자 결정: 전문은 개념 페이지 한 곳, source는 한 줄 + 링크): 조회 실패 기본값 → 스큐·"Training은 Serving을
  따라간다"·네 형태(학습-서빙 스큐), cm → m(스키마 진화), 누수와 스큐의 증상(데이터 누수), 보안·컨텍스트·버전 표면·토큰
  비용(LLMOps), 플랫폼 층·세 모델 서버(모델 서빙), 배칭·경량화 아티팩트(추론 최적화), Self-Healing·DE 책임(MLOps), 저장
  이원화(비정형 데이터 파이프라인), 세 난관(스트림 처리), 운영 메타데이터·ELT의 PII(데이터 거버넌스와 카탈로그).
- 고친 파일 36개: concept 17, entity 3(Apache Kafka · Delta Lake · Triton Inference Server), source 15, index. 틀린 위키 주장에는
  `⚠️ 위키 정정` 표시를 남겼다(8곳).
- **③ 자기 페이지가 없는 개념(보고만).** 높음: 멱등성, Apache Airflow, 자동 재학습, 데이터 계약(지금은 데이터 SLA의 alias). 중간:
  데이터 검증, PII·비식별화, 라벨 파이프라인, 컴팩션·작은 파일, Feast, 모델 배포 전략. 보류: RAG·벡터 DB·임베딩·청킹(트래커
  결정대로 Part 5), Apache Iceberg·Redis.
- 다음: Part 3 인제스트. 전체 린트는 Part 5 뒤.

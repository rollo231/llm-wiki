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

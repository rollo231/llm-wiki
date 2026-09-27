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

## [2026-09-26] schema | 대상에 인프런 Java 면접 강의 추가

- 「대상」 절을 자료 목록으로 바꾸고 `raw/interviews/java/`를 추가했다. AI DE 강의는 출발점으로 남긴다.

## [2026-09-26] ingest | 인프런 Java 면접 강의 (Section 2–6)

- 자료: `raw/interviews/java/수업 자료.pdf` 117p. 워터마크로 인프런 강의임을 확인했다. 강의명·강사는 자료에 없다. Section 1은
  PDF에 없다. 질문 37개(주 12 · 꼬리 25), 질문마다 Bronze·Silver·Gold 모범 답과 "이유"가 붙어 있다.
- 결정(사용자, 전부 추천안): 분할 = Section 하나당 source 하나, 이름 = `Java 면접 <Section> <제목>`, 결함 = 자료의 답은 그대로 두고
  ⚠️ 한 줄 + 정정 전문은 concept 한 곳.
- 외부 검증(OpenJDK JEP · JLS/JVMS · Oracle GC 가이드 · HotSpot 소스, JDK 25 `PrintFlagsFinal`) 22건: 틀림 10 · 단서 필요 9 · 맞음 3.
  틀림: 실행 5단계 순서, "Java는 Mark and Sweep"·Minor GC도 Mark and Sweep(Young은 복사), 가시성 = 코어 캐시 불일치 · volatile =
  캐시 우회(JMM happens-before), synchronized는 항상 blocking, 다형성 구현에 오버로딩, instanceof는 계층이 깊을수록 느림, 인터페이스
  메서드는 전부 public(JEP 213), 람다·스트림은 순수 함수라 스레드 안전. JEP 523(G1이 모든 환경의 기본, JDK 27)은 직접 확인했다.
- 만든 페이지 19개: source 5(Java 면접 2~6), entity 2(인프런 Java 면접 강의 — 트래커·루브릭·결함 표, JVM), concept 12(JIT 컴파일 ·
  가비지 컬렉션 · 가비지 컬렉터 · 동시성 문제 · 동기화 기법 · 스레드 풀 · 캡슐화 · 상속과 조합 · 다형성 · 인터페이스와 추상 클래스 ·
  람다와 스트림 · 함수형 프로그래밍).
- 고친 페이지: 지연 시간과 처리량(GC 선택·스레드 수를 같은 축 위에 둔 절 추가), 스트림 처리(Java Stream API와 이름만 같다는 안내),
  index.
- ⚠️ 워터마크에 구매자 식별 정보가 있다 — 공개 repo에 옮기지 않았다.
- 기계 검사: 페이지 82개 0오류(오류 6종을 주입한 복사본에서 6종 모두 검출).

## [2026-09-26] lint | Java 면접 페이지 인제스트 뒤 린트

- 범위: 이번에 들어온 Java 면접 페이지 19개와 기존 위키의 이음새(AI DE Part 1·2는 1차 린트 완료, 전체 린트는 Part 5 뒤).
  기계 검사는 페이지 82개 0오류.
- **① 위키 자신의 사실 주장**(1차 자료 대조 — 틀림 2 · 단서 필요 8 · 맞음 약 24). 틀림: static 필드가 힙(Class 미러)으로 간 것은
  JDK 8이 아니라 **JDK 7**(JDK-7017732) — 인제스트 때 외부 검증 보고를 그대로 옮겨 생긴 오류다. "Java Stream은 유한한 컬렉션"
  (스트림은 무한할 수 있다). 단서 필요: CDS는 JDK 5부터(JDK 10은 AppCDS), `distinct`는 순차 스트림에서 short-circuit 유지,
  `LockingMode` 플래그 JDK 24 deprecated, Stream 문서 인용부호 안 생략 표시, "순수 함수 ≈ 멱등"(결정성 + 멱등 싱크로 분리),
  JVM 피크 성능 주장(표시 추가), Spark GC → 재시도는 `spark.network.timeout` 초과 때만, 컨테이너 조건 1792MB.
- **② 원본 대조**: 등급 표본 서술 2곳(Java 면접 4의 Q1-2 누락, Java 면접 6은 네 문항 모두 하나씩).
- **③ 중복 정리**: Spark·Flink GC 문단(가비지 컬렉터 한 곳으로), CAS ↔ 낙관적 락 비유(동시성 문제 한 곳으로).
- **④ 교차참조**: Apache Spark · Apache Kafka · Apache Flink → JVM. 멱등성 → 변경 데이터 캡처 · 이벤트 기반 아키텍처 · 스트림 처리.
- **⑤ 새 페이지**: 멱등성 — 1차 린트 "높음" 보류 개념이 함수형 프로그래밍에서 다시 나와 만들었다(사용자 결정). AI DE 1-07·1-08·
  1-09·1-12의 흩어진 언급을 모았다.
- 틀린 위키 주장에는 `⚠️ 위키 정정` 표시를 남겼다(4곳). 고친 파일 17개 + 새 페이지 1 + index.
- 남은 것: SOLID/LSP(중간), Tomcat·Spring(낮음) 페이지 보류. 강의명·Section 1 존재 여부는 자료에 없다.

## [2026-09-26] query | Java C1·C2 컴파일러

C1·C2 질문에 [[JIT 컴파일]]로 답한 뒤, 답에서 보탠 배경지식을 1차 자료로 검증해 같은 페이지에 넣었다.

- 계층형 컴파일: tier 0~4 전체 표. tier 1은 사소한 메서드, tier 2는 C2 큐가 밀렸을 때 쓴다. Java SE 7에서 도입, JDK 8(hs25)부터 기본(JDK-8008938).
- 새 절: 역최적화(타입 프로파일 추측, CHA 의존성, safepoint 역최적화), Graal JIT(JEP 317 → JEP 410 제거).
- 채팅 답의 정정: tier 1은 처음부터 고르는 게 아니라 **첫 C1 컴파일 뒤** 사소하다고 판정되면 간다(`compilationPolicy.hpp`).

## [2026-09-26] schema | 「대상」 절을 자료 목록에서 범위 선언으로

README 를 특정 강의 소개 없이 일반 지식 베이스로 고친 데 맞춰, `CLAUDE.md` 「대상」 절에서 강의 두 개의 목록을 뺐다.
범위는 "특정 강의·주제에 한정하지 않는다"로 두고, 들어온 자료의 기준은 `index.md` 자료 절과 저작물 entity 트래커로 옮겼다.
"자료가 늘면 이 절을 고친다" 규칙은 없앴다.

## [2026-09-26] ingest | 인프런 Java 면접 강의 Section 2 부록 — 빈출 질문

`raw/interviews/java/JVM과_실행_원리_채널톡_면접관이_뽑은_빈출_질문.pdf`(A3 1쪽, Notion 내보내기, 생성일 2026-03-07)를 인제스트했다.
워터마크로 인프런 자료임을 확인했고, 제목이 Section 2와 같아 그 부록으로 두었다(추론).

- 결정(사용자, 모두 추천안): 기존 Section 2 페이지에 합치지 않고 별도 source로 둔다(형식은 빈도 별점과 단답, 주제는 구조). 새 개념은
  페이지 2개로 쓴다.
- 외부 검증(JVMS SE 25 §1.2·2장·5장, JEP 122·261, JDK-7017732·6962931·6964458, ClassLoader Javadoc, HotSpot Runtime Overview):
  자료 서술 8건 가운데 틀림 3(가상 OS, 클래스 로더가 링크·초기화를 한다, PC = 몇 번째 줄), 단서 필요 5(3분할은 JVMS 분류가 아님,
  준비·해석의 정밀화, "5가지" 셈법, 프레임의 상수 풀 참조, 힙의 배열). 위키에 새로 쓴 배경 주장 6건(Metaspace, JDK 7에 static·intern이 힙으로,
  코드 캐시, 내장 로더·위임, HotSpot의 합쳐진 스택, 지연 로딩)은 모두 뒷받침됐다. 부모 위임이 JDK 9 이후 엄격하지 않다는 것과
  JEP 122 본문에 "Metaspace"라는 단어가 없다는 것은 단서로 남겼다.
- 만든 페이지 3개: source [[Java 면접 2 빈출 질문]], concept [[클래스 로딩]] · [[JVM 메모리 구조]].
- 고친 페이지: 인프런 Java 면접 강의(트래커 행·자료 표·결함 표), JVM(JVMS의 정의, 3분할 단서, 구성 요소 표 링크, 지연 로딩 표현),
  JIT 컴파일·가비지 컬렉션·Java 면접 2 JVM과 실행 원리(교차참조), index.
- ⚠️ 워터마크에 구매자 식별 정보가 있다 — 옮기지 않았다.
- 인제스트 직후 위키가 보탠 주장 7건을 1차 자료와 대조했다: 틀림 0, 단서 필요 5. `java.` 금지 규칙은 이름 기준이고 플랫폼 로더와 그 조상에만 허용된다는 점, Metaspace OOM의 로더 누수 원인은 통념이라는 점, `-Xss`는 예약 주소 공간이라는 점을 반영했다.

## [2026-09-26] lint | Section 2 부록 인제스트 뒤 린트

- 범위: 직전 린트(`ce1b893`) 이후 바뀐 페이지. 부록 인제스트 페이지, JIT 컴파일의 C1·C2 확장, README·스키마. 기계 검사는 전체
  86페이지 0오류.
- ① 모순·낡음: README 「시작하기」의 커밋 주체가 스키마와 어긋났다(에이전트가 커밋·push하는 것으로 고침). README 구조 트리에
  README.md가 빠져 있었다. 트래커의 결함 평가 문장이 슬라이드 수치만 셌다(부록 틀림 3 · 단서 5 추가).
- ② 근거가 약한 위키 주장: 「Notion 내보내기」에 추론 표시를 달았다. HotSpot의 합쳐진 스택은 JDK 1.x 백서만 인용하고 있어 HotSpot
  소스를 함께 달았다. 「메서드 영역이 Metaspace·힙·코드 캐시로 흩어진다」에는 명세가 정하지 않는 해석이라는 단서를 달았다.
- ③ 교차참조: 동시성 문제 → JVM 메모리 구조, Java 면접 3 GC → JVM 메모리 구조.
- ④ 자기 페이지가 없는 개념: SOLID/LSP · Tomcat·Spring은 이번 자료에도 다시 나오지 않아 계속 보류.
- 제안: 다른 섹션에도 같은 형식의 「빈출 질문」 부록이 있는지 확인한다.

## [2026-09-27] query | 레퍼런스 카운팅과 마크 앤 스윕

「GC 알고리즘을 레퍼런스 카운팅과 마크 앤 스윕 기준으로」 ELI5 질의(풍선·끈 그림 artifact)의 답을 노트로 남겼다. 위키의 첫 note다.

- 만든 페이지: note [[레퍼런스 카운팅과 마크 앤 스윕]].
- 고친 페이지: [[가비지 컬렉션]](두 계열 표 아래·관련 절에 링크), index(노트 절).
- 외부 검증(Python 3.14.7 gc 문서·What's New 3.14, PEP 703, Swift Book ARC 장, V8 「Trash talk」, Go GC 가이드, Bacon 외 OOPSLA 2004):
  런타임별 주장 모두 뒷받침됐다. 새로 안 것 — CPython 3.14.0–3.14.4의 점진적 순환 GC가 3.14.5에서 되돌려졌다.
- ⚠️ 답을 처음 설명할 때 「JVM은 마크 앤 스윕이 기본 뼈대」라고 했다 — [[가비지 컬렉션]]이 이미 정정한 과단순화의 반복이다. 노트와
  artifact 모두 「HotSpot은 복사·mark-compact, 순수 mark-sweep은 Go」로 고쳤다.
- 미확인으로 남긴 것: RC의 연쇄 해제 멈춤(통념), 테이블 포맷 파일 정리와의 대응(위키의 연결).

## [2026-09-27] query | GC Root와 Minor GC의 루트

「루트 스페이스가 뭔가」 질의에 GC Root(root set)로 답했다(공식 용어 「root space」는 없다). 대부분 [[가비지 컬렉션]]에 이미 있어
노트는 만들지 않았다.

- 고친 페이지: [[가비지 컬렉션]] — GC Root 절에 「Young만 치울 때 Old → Young 참조를 remembered set(card table · G1 Region별
  RSet)으로 기록해 루트처럼 스캔한다」를 추가, aliases에 Remembered set · Card table.
- 외부 검증: HotSpot Glossary(card table = remembered set의 한 종류, write barrier가 유지), Oracle G1 튜닝 가이드 JDK 21(Region별
  remembered set, 512바이트 card, Young Region은 항상 유지). 뒷받침됨.
- 같은 세션의 ELI5 artifact 둘(Minor GC와 Full GC, 힙 구조)은 위키에 이미 있는 내용이라 페이지를 만들지 않았다.

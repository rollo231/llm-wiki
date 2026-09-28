# 로그

위키 활동의 시간순 기록. 추가만 하고, 새 항목은 맨 아래에 붙인다. 항목 머리 형식: `## [YYYY-MM-DD] <ingest|query|lint|schema> | 제목`

## [2026-09-14] schema | 위키 초기화 — gist 골격으로 재시작

- 이전 위키를 전부 지우고 다시 시작했다 — 페이지 200개(source 82 · concept 68 · entity 41 · note 7 ·MOC 2)와 로그 1,695줄. 이전 내용은 git 커밋 `12f3ead` 에 남아 있다.
- 원본은 `raw/data-engineering/ai-de-course/`(패스트캠퍼스 AI 데이터 엔지니어링 강의, 5파트 PDF 40개)만 남겼다. 나머지 raw 자료(SpatialData·spatialdata-io·Apache Sedona·MinIO 문서, 데이터 지형 가이드, Apache 기술 지도 책)는 완전히 삭제했고, 거기 딸린 `docs/experiments/` 도 지웠다.
- 스키마(`CLAUDE.md`)와 README 를 한국어로 다시 썼다. 카파시 gist 의 골격 — raw 불변 · wiki 는 에이전트 소유 · 스키마, 인제스트·질의·린트, index·log — 만 두고, 강의 인제스트에 필요한 규칙 두 가지(주제 단위 source 페이지, 트래커 entity)를 더했다. `area` 필드·MOC·URL 스냅샷·실험 하네스 규칙은 뺐다 — 필요해지면 그때 다시 들인다.
- 이름 규칙: 사람이 읽는 것(파일명·제목·링크·본문)은 한국어, 기계가 읽는 것(frontmatter 키·`type` 값·폴더명·로그 키워드)은 영어. 로그 키워드에 `schema` 를 더했다.
- 다음: AI DE 강의 Part 1 인제스트 — 트래커 entity 부터.

## [2026-09-14] ingest | AI DE 강의 Part 1

- 원본: `raw/data-engineering/ai-de-course/part1/` PDF 25개, 282p 전부 읽음. 텍스트가 적은 덱(02·04)과 텍스트가 없는 슬라이드는 이미지로 확인했다(모두 섹션 타이틀).
- 합의한 분할: 같은 제목으로 이어지는 덱은 한 강의로 묶어 **16장**(04+05, 06~08, 16~18, 19~21, 22~24). 파일명은 `AI DE 강의 1-NN 주제`(순번은 위키가 붙임). concept·entity는 중간 세밀도. 1회차 위키는 참고하지 않았다.
- 새 페이지 42개: source 16, concept 18(AI 데이터 엔지니어링 · 지연 시간과 처리량 · 데이터와 모델 버전 관리 · 행 기반과 열 기반 저장 · 데이터 레이크하우스 · 스키마 진화 · ETL과 ELT · 배치 처리 · 변경 데이터 캡처 · 비정형 데이터 파이프라인 ·이벤트 기반 아키텍처 · 스트림 처리 · 학습-서빙 스큐 · 데이터 드리프트 · 피처 스토어 · 데이터 SLA · 데이터 관측성 · 데이터 거버넌스와 카탈로그), entity 8(AI 데이터 엔지니어링 강의(트래커) · Apache Kafka · Apache Parquet · Apache Avro · Delta Lake · Apache Flink · Apache Spark · Debezium).
- **외부 사실 16건을 1차 자료와 대조했다**(공식 문서·원 논문·회사 엔지니어링 블로그). 틀림: CDC 덱의 스키마 호환성 정의(뒤바뀜), Kafka "Fortune 500"(공식은 Fortune 100), 사례 덱의 Uber "2%"(Google TFX 논문의 수치), Parquet 메타데이터 "헤더"(footer), "OpenAI Titan"(Amazon). 낡음: Kafka ZooKeeper "제거 예정"(4.0에서 제거됨), Spark DStream(레거시), Tesla Dojo(2025-08 중단). 근거가 약함: PSI 0.2(관례는 0.1/0.25), zero-copy "CPU 60%"(원 보고는 전송 시간 65%), 두 "80%" 통계.
- **코스 내부 모순**: 호환성 정의(1-05 vs 1-08), Avro 분류(1-04 vs 1-05), Spark 세대(1-10 vs 1-12), 데이터 품질 축 세 버전(1-13·1-14·1-16). 결함 표는 트래커 [[AI 데이터 엔지니어링 강의]]에 모았다.
- 검산: 스큐 예시 20,000원 vs 673,333.33원(33.67배) — 강의 계산이 맞다. 다만 차이가 취소 부호와 분모 두 군데에 있다.
- 다음: Part 2 인제스트.

## [2026-09-14] ingest | AI DE 강의 Part 2

- 원본: `raw/data-engineering/ai-de-course/part2/` PDF 5개, 206p 전부 읽음. 텍스트가 없는 슬라이드 23장은 이미지로 확인했다(도식·밈·채용 공고 캡처). Part 2는 전체 제목(「AI 학습/추론 중심 데이터 파이프라인 설계」)과 강사 표기("Habi")가 있다.
- 합의한 분할: Part 2는 덱 하나에 번호 붙은 소단원이 여러 개라 **소단원 기준 10장**(Ch1 전체 · Ch2 1+2 · Ch2 3 · Ch3 1 · 2 ·3 · Ch4 1 · 2+3 · 4 · Ch5). 트래커 분할 규칙에 소단원 규칙을 더했다. 세밀도 중간, 강사 표기 기록.
- 새 페이지 21개: source 10, concept 5(MLOps · LLMOps · 모델 서빙 · 추론 최적화 · 데이터 누수), entity 6(Designing Machine Learning Systems · FastAPI · TorchServe · BentoML · Triton Inference Server · ONNX).
- 고친 페이지 13개: concept 10(피처 스토어 · 학습-서빙 스큐 · 데이터 드리프트 · AI 데이터 엔지니어링 · 데이터와 모델 버전 관리 ·지연 시간과 처리량 · 비정형 데이터 파이프라인 · ETL과 ELT · 스트림 처리 · 데이터 거버넌스와 카탈로그), source 1(1-13), 트래커, index.
- **외부 사실 21건을 1차 자료와 대조했다**(공식 문서·GitHub 저장소·원저자 강의 노트). 틀림: Triton "비즈니스 로직 직접 구현 불가"(Python backend·BLS), FastAPI 도식의 Pydantic = Cython(v1 시절), ONNX Runtime "MKL·OpenMP"(v1.7부터 OpenMP 없음). 낡음: TorchServe(2025-08 보관), BentoML Runner·Yatai(레거시·보관), Flyte(작성 뒤 Flyte 2 GA). 과장: "WSGI는 한 번에 한 요청", CPU FP16 효과, Triton "파이썬 오버헤드 완벽 제거". 출처 누락: 배치 vs 온라인 표(Chip Huyen). 표준 용어 아님: Context Drift·Prompt Drift. 출처 없음: "인프라 관리 70%". 맞음: 라이프사이클 6단계, 피처 스토어가 필요 없는 조건 다섯 가지, 시간 기반 분할·그룹 누수, TorchServe 포트.
- **위키 정정**: Part 1 때 위키가 쓴 "스큐 = 코드, 드리프트 = 세상, 원인이 반대"가 Google의 정의(Rules of ML — 학습-서빙 성능 차이, 원인에 데이터 변화 포함)에 비추어 과장이었다. 강의(2-06)가 맞다. 학습-서빙 스큐·1-13·데이터 드리프트를 좁혀 고치고 정정 표시를 남겼다.
- 코스 내부 결함: Ch5 제목의 "운영" 내용 누락, Ch2~5 템플릿 머리글, 중복 슬라이드, 2-07의 "조회 실패 시 기본값"과 2-06의 "조회 실패를 0으로 처리하면 스큐"가 이어지지 않음. 결함 표는 트래커 [[AI 데이터 엔지니어링 강의]]에 모았다.
- 다음: Part 3 인제스트.

## [2026-09-14] lint | Part 1·2 뒤 1차 린트

- 범위(사용자 결정): ① 위키 자신의 사실 주장 대조 ② Part 1·2가 함께 고친 개념 11개의 이음새 ③ 자기 페이지가 없는 개념(보고만). 기계 검사(frontmatter·제목·타입·alias·링크·고아·index·log 머리)는 페이지 63개 0오류 — 오류 9종을 주입한 복사본에서 9종 모두 검출해 검사가 공허하지 않음을 확인했다.
- **① 사실 주장.** `*(위키의 …)*` 93건은 대부분 해석·연결이다. 사실을 담은 것과 표시 없는 위키 주장을 골라 대조했다. 강의 내부 주장(원본 PDF 텍스트 대조) — 맞음: Self-Healing 명칭, 스케일링 통계가 Part 2에서야 나옴, 누수 절 없음, Allowed Lateness 서술. 외부 8건(1차 자료 대조) — 틀림: 스키마 진화 "안전 목록 = 모두 FULL 호환"(타입 확대는 BACKWARD만), LLMOps "SQL 인젝션 방어와 구조가 같다"(NCSC 2025-12-08: 데이터와 지시의 경계가 없다). 단서 필요: Triton을 런타임 층에 둔 분류(모델 서버 — ONNX Runtime은 백엔드), 가지치기 효과(비구조적은 dense 커널에서 이득 없음), CDC 중단 시 로그(PostgreSQL은 WAL 누적, MySQL은 binlog 삭제로 위치 상실), Kafka "선형 확장"·zero-copy(TLS면 sendfile 안 씀), 체크포인트 exactly-once(엔진 상태 한정, end-to-end는 싱크 필요). 맞음: Google ML Glossary의 스큐 정의(인용 추가).
- **② 이음새.** 페이지끼리 어긋남: 데이터 레이크하우스 "Iceberg는 이름이 없다"(1-16에 싱크로 나옴), 행 기반과 열 기반 저장 "같은 강의의 덱 08"(1-05), MLOps "2·4·5단계" vs 2-02(→ 2~5단계). 스큐 정정이 덜 번진 곳: index의 1-13 요약, 1-13 핵심 헤드라인, 학습-서빙 스큐의 "원인" 절 제목. 용법: 데이터 드리프트 감지 절·데이터 관측성 표의 학습 vs 서빙 비교(TFDV·Vertex 용법으로는 스큐 감지). 단정: "피처 조회가 지연의 대부분"(지연 시간과 처리량·모델 서빙). 허브 표 분류(AI 데이터 엔지니어링 ↔ 트래커), 1-09 문구. 빠진 교차참조: 2-04 라벨 → 데이터 SLA·데이터 드리프트, 데이터 관측성 ↔ 2-07 서킷 브레이커. alias: Delta Lake의 `ACID` 제거.
- **중복 정리**(사용자 결정: 전문은 개념 페이지 한 곳, source는 한 줄 + 링크): 조회 실패 기본값 → 스큐·"Training은 Serving을 따라간다"·네 형태(학습-서빙 스큐), cm → m(스키마 진화), 누수와 스큐의 증상(데이터 누수), 보안·컨텍스트·버전 표면·토큰 비용(LLMOps), 플랫폼 층·세 모델 서버(모델 서빙), 배칭·경량화 아티팩트(추론 최적화), Self-Healing·DE 책임(MLOps), 저장 이원화(비정형 데이터 파이프라인), 세 난관(스트림 처리), 운영 메타데이터·ELT의 PII(데이터 거버넌스와 카탈로그).
- 고친 파일 36개: concept 17, entity 3(Apache Kafka · Delta Lake · Triton Inference Server), source 15, index. 틀린 위키 주장에는 `⚠️ 위키 정정` 표시를 남겼다(8곳).
- **③ 자기 페이지가 없는 개념(보고만).** 높음: 멱등성, Apache Airflow, 자동 재학습, 데이터 계약(지금은 데이터 SLA의 alias). 중간: 데이터 검증, PII·비식별화, 라벨 파이프라인, 컴팩션·작은 파일, Feast, 모델 배포 전략. 보류: RAG·벡터 DB·임베딩·청킹(트래커 결정대로 Part 5), Apache Iceberg·Redis.
- 다음: Part 3 인제스트. 전체 린트는 Part 5 뒤.

## [2026-09-26] schema | 대상에 인프런 Java 면접 강의 추가

- 「대상」 절을 자료 목록으로 바꾸고 `raw/interviews/java/`를 추가했다. AI DE 강의는 출발점으로 남긴다.

## [2026-09-26] ingest | 인프런 Java 면접 강의 (Section 2–6)

- 자료: `raw/interviews/java/수업 자료.pdf` 117p. 워터마크로 인프런 강의임을 확인했다. 강의명·강사는 자료에 없다. Section 1은 PDF에 없다. 질문 37개(주 12 · 꼬리 25), 질문마다 Bronze·Silver·Gold 모범 답과 "이유"가 붙어 있다.
- 결정(사용자, 전부 추천안): 분할 = Section 하나당 source 하나, 이름 = `Java 면접 <Section> <제목>`, 결함 = 자료의 답은 그대로 두고 ⚠️ 한 줄 + 정정 전문은 concept 한 곳.
- 외부 검증(OpenJDK JEP · JLS/JVMS · Oracle GC 가이드 · HotSpot 소스, JDK 25 `PrintFlagsFinal`) 22건: 틀림 10 · 단서 필요 9 · 맞음 3. 틀림: 실행 5단계 순서, "Java는 Mark and Sweep"·Minor GC도 Mark and Sweep(Young은 복사), 가시성 = 코어 캐시 불일치 · volatile = 캐시 우회(JMM happens-before), synchronized는 항상 blocking, 다형성 구현에 오버로딩, instanceof는 계층이 깊을수록 느림, 인터페이스 메서드는 전부 public(JEP 213), 람다·스트림은 순수 함수라 스레드 안전. JEP 523(G1이 모든 환경의 기본, JDK 27)은 직접 확인했다.
- 만든 페이지 19개: source 5(Java 면접 2~6), entity 2(인프런 Java 면접 강의 — 트래커·루브릭·결함 표, JVM), concept 12(JIT 컴파일 ·가비지 컬렉션 · 가비지 컬렉터 · 동시성 문제 · 동기화 기법 · 스레드 풀 · 캡슐화 · 상속과 조합 · 다형성 · 인터페이스와 추상 클래스 ·람다와 스트림 · 함수형 프로그래밍).
- 고친 페이지: 지연 시간과 처리량(GC 선택·스레드 수를 같은 축 위에 둔 절 추가), 스트림 처리(Java Stream API와 이름만 같다는 안내), index.
- ⚠️ 워터마크에 구매자 식별 정보가 있다 — 공개 repo에 옮기지 않았다.
- 기계 검사: 페이지 82개 0오류(오류 6종을 주입한 복사본에서 6종 모두 검출).

## [2026-09-26] lint | Java 면접 페이지 인제스트 뒤 린트

- 범위: 이번에 들어온 Java 면접 페이지 19개와 기존 위키의 이음새(AI DE Part 1·2는 1차 린트 완료, 전체 린트는 Part 5 뒤). 기계 검사는 페이지 82개 0오류.
- **① 위키 자신의 사실 주장**(1차 자료 대조 — 틀림 2 · 단서 필요 8 · 맞음 약 24). 틀림: static 필드가 힙(Class 미러)으로 간 것은 JDK 8이 아니라 **JDK 7**(JDK-7017732) — 인제스트 때 외부 검증 보고를 그대로 옮겨 생긴 오류다. "Java Stream은 유한한 컬렉션"(스트림은 무한할 수 있다). 단서 필요: CDS는 JDK 5부터(JDK 10은 AppCDS), `distinct`는 순차 스트림에서 short-circuit 유지, `LockingMode` 플래그 JDK 24 deprecated, Stream 문서 인용부호 안 생략 표시, "순수 함수 ≈ 멱등"(결정성 + 멱등 싱크로 분리), JVM 피크 성능 주장(표시 추가), Spark GC → 재시도는 `spark.network.timeout` 초과 때만, 컨테이너 조건 1792MB.
- **② 원본 대조**: 등급 표본 서술 2곳(Java 면접 4의 Q1-2 누락, Java 면접 6은 네 문항 모두 하나씩).
- **③ 중복 정리**: Spark·Flink GC 문단(가비지 컬렉터 한 곳으로), CAS ↔ 낙관적 락 비유(동시성 문제 한 곳으로).
- **④ 교차참조**: Apache Spark · Apache Kafka · Apache Flink → JVM. 멱등성 → 변경 데이터 캡처 · 이벤트 기반 아키텍처 · 스트림 처리.
- **⑤ 새 페이지**: 멱등성 — 1차 린트 "높음" 보류 개념이 함수형 프로그래밍에서 다시 나와 만들었다(사용자 결정). AI DE 1-07·1-08·1-09·1-12의 흩어진 언급을 모았다.
- 틀린 위키 주장에는 `⚠️ 위키 정정` 표시를 남겼다(4곳). 고친 파일 17개 + 새 페이지 1 + index.
- 남은 것: SOLID/LSP(중간), Tomcat·Spring(낮음) 페이지 보류. 강의명·Section 1 존재 여부는 자료에 없다.

## [2026-09-26] query | Java C1·C2 컴파일러

C1·C2 질문에 [[JIT 컴파일]]로 답한 뒤, 답에서 보탠 배경지식을 1차 자료로 검증해 같은 페이지에 넣었다.

- 계층형 컴파일: tier 0~4 전체 표. tier 1은 사소한 메서드, tier 2는 C2 큐가 밀렸을 때 쓴다. Java SE 7에서 도입, JDK 8(hs25)부터 기본(JDK-8008938).
- 새 절: 역최적화(타입 프로파일 추측, CHA 의존성, safepoint 역최적화), Graal JIT(JEP 317 → JEP 410 제거).
- 채팅 답의 정정: tier 1은 처음부터 고르는 게 아니라 **첫 C1 컴파일 뒤** 사소하다고 판정되면 간다(`compilationPolicy.hpp`).

## [2026-09-26] schema | 「대상」 절을 자료 목록에서 범위 선언으로

README 를 특정 강의 소개 없이 일반 지식 베이스로 고친 데 맞춰, `CLAUDE.md` 「대상」 절에서 강의 두 개의 목록을 뺐다. 범위는 "특정 강의·주제에 한정하지 않는다"로 두고, 들어온 자료의 기준은 `index.md` 자료 절과 저작물 entity 트래커로 옮겼다. "자료가 늘면 이 절을 고친다" 규칙은 없앴다.

## [2026-09-26] ingest | 인프런 Java 면접 강의 Section 2 부록 — 빈출 질문

`raw/interviews/java/JVM과_실행_원리_채널톡_면접관이_뽑은_빈출_질문.pdf`(A3 1쪽, Notion 내보내기, 생성일 2026-03-07)를 인제스트했다. 워터마크로 인프런 자료임을 확인했고, 제목이 Section 2와 같아 그 부록으로 두었다(추론).

- 결정(사용자, 모두 추천안): 기존 Section 2 페이지에 합치지 않고 별도 source로 둔다(형식은 빈도 별점과 단답, 주제는 구조). 새 개념은 페이지 2개로 쓴다.
- 외부 검증(JVMS SE 25 §1.2·2장·5장, JEP 122·261, JDK-7017732·6962931·6964458, ClassLoader Javadoc, HotSpot Runtime Overview): 자료 서술 8건 가운데 틀림 3(가상 OS, 클래스 로더가 링크·초기화를 한다, PC = 몇 번째 줄), 단서 필요 5(3분할은 JVMS 분류가 아님, 준비·해석의 정밀화, "5가지" 셈법, 프레임의 상수 풀 참조, 힙의 배열). 위키에 새로 쓴 배경 주장 6건(Metaspace, JDK 7에 static·intern이 힙으로, 코드 캐시, 내장 로더·위임, HotSpot의 합쳐진 스택, 지연 로딩)은 모두 뒷받침됐다. 부모 위임이 JDK 9 이후 엄격하지 않다는 것과 JEP 122 본문에 "Metaspace"라는 단어가 없다는 것은 단서로 남겼다.
- 만든 페이지 3개: source [[Java 면접 2 빈출 질문]], concept [[클래스 로딩]] · [[JVM 메모리 구조]].
- 고친 페이지: 인프런 Java 면접 강의(트래커 행·자료 표·결함 표), JVM(JVMS의 정의, 3분할 단서, 구성 요소 표 링크, 지연 로딩 표현), JIT 컴파일·가비지 컬렉션·Java 면접 2 JVM과 실행 원리(교차참조), index.
- ⚠️ 워터마크에 구매자 식별 정보가 있다 — 옮기지 않았다.
- 인제스트 직후 위키가 보탠 주장 7건을 1차 자료와 대조했다: 틀림 0, 단서 필요 5. `java.` 금지 규칙은 이름 기준이고 플랫폼 로더와 그 조상에만 허용된다는 점, Metaspace OOM의 로더 누수 원인은 통념이라는 점, `-Xss`는 예약 주소 공간이라는 점을 반영했다.

## [2026-09-26] lint | Section 2 부록 인제스트 뒤 린트

- 범위: 직전 린트(`ce1b893`) 이후 바뀐 페이지. 부록 인제스트 페이지, JIT 컴파일의 C1·C2 확장, README·스키마. 기계 검사는 전체 86페이지 0오류.
- ① 모순·낡음: README 「시작하기」의 커밋 주체가 스키마와 어긋났다(에이전트가 커밋·push하는 것으로 고침). README 구조 트리에 README.md가 빠져 있었다. 트래커의 결함 평가 문장이 슬라이드 수치만 셌다(부록 틀림 3 · 단서 5 추가).
- ② 근거가 약한 위키 주장: 「Notion 내보내기」에 추론 표시를 달았다. HotSpot의 합쳐진 스택은 JDK 1.x 백서만 인용하고 있어 HotSpot 소스를 함께 달았다. 「메서드 영역이 Metaspace·힙·코드 캐시로 흩어진다」에는 명세가 정하지 않는 해석이라는 단서를 달았다.
- ③ 교차참조: 동시성 문제 → JVM 메모리 구조, Java 면접 3 GC → JVM 메모리 구조.
- ④ 자기 페이지가 없는 개념: SOLID/LSP · Tomcat·Spring은 이번 자료에도 다시 나오지 않아 계속 보류.
- 제안: 다른 섹션에도 같은 형식의 「빈출 질문」 부록이 있는지 확인한다.

## [2026-09-27] query | 레퍼런스 카운팅과 마크 앤 스윕

「GC 알고리즘을 레퍼런스 카운팅과 마크 앤 스윕 기준으로」 ELI5 질의(풍선·끈 그림 artifact)의 답을 노트로 남겼다. 위키의 첫 note다.

- 만든 페이지: note [[레퍼런스 카운팅과 마크 앤 스윕]].
- 고친 페이지: [[가비지 컬렉션]](두 계열 표 아래·관련 절에 링크), index(노트 절).
- 외부 검증(Python 3.14.7 gc 문서·What's New 3.14, PEP 703, Swift Book ARC 장, V8 「Trash talk」, Go GC 가이드, Bacon 외 OOPSLA 2004): 런타임별 주장 모두 뒷받침됐다. 새로 안 것 — CPython 3.14.0–3.14.4의 점진적 순환 GC가 3.14.5에서 되돌려졌다.
- ⚠️ 답을 처음 설명할 때 「JVM은 마크 앤 스윕이 기본 뼈대」라고 했다 — [[가비지 컬렉션]]이 이미 정정한 과단순화의 반복이다. 노트와 artifact 모두 「HotSpot은 복사·mark-compact, 순수 mark-sweep은 Go」로 고쳤다.
- 미확인으로 남긴 것: RC의 연쇄 해제 멈춤(통념), 테이블 포맷 파일 정리와의 대응(위키의 연결).

## [2026-09-27] query | GC Root와 Minor GC의 루트

「루트 스페이스가 뭔가」 질의에 GC Root(root set)로 답했다(공식 용어 「root space」는 없다). 대부분 [[가비지 컬렉션]]에 이미 있어 노트는 만들지 않았다.

- 고친 페이지: [[가비지 컬렉션]] — GC Root 절에 「Young만 치울 때 Old → Young 참조를 remembered set(card table · G1 Region별 RSet)으로 기록해 루트처럼 스캔한다」를 추가, aliases에 Remembered set · Card table.
- 외부 검증: HotSpot Glossary(card table = remembered set의 한 종류, write barrier가 유지), Oracle G1 튜닝 가이드 JDK 21(Region별 remembered set, 512바이트 card, Young Region은 항상 유지). 뒷받침됨.
- 같은 세션의 ELI5 artifact 둘(Minor GC와 Full GC, 힙 구조)은 위키에 이미 있는 내용이라 페이지를 만들지 않았다.

## [2026-09-27] query | 객체 수명과 메모리 상한

「Old가 꽉 차면 설계부터 잘못된 것인가」와 이어진 이해 확인·안티패턴 질의를 노트로 남겼다.

- 결정(사용자): 노트로 남긴다. 제목은 증상(「Old가 찬다」)이 아니라 원칙으로. 안티패턴은 별도 페이지가 아니라 같은 노트의 절로.
- 만든 페이지: note [[객체 수명과 메모리 상한]].
- 고친 페이지: [[가비지 컬렉션]](모니터링 절·관련에 링크), [[Apache Spark]](「JVM 메모리」 절), index.
- 외부 검증: Oracle GC Tuning Guide JDK 21(Survivor 넘침 → Old 직행, `System.gc()` 회피), Goetz 2005(객체 풀링은 손해, Wayback 사본), JEP 421(finalization), ThreadLocal Javadoc JDK 25, Spark 4.2.0 RDD 가이드(`collect()`), JDK 25 플래그(IHOP 45, Adaptive IHOP). 뒷받침됨.
- 단서로 남긴 것: 『Effective Java』 Item 7은 원서가 아니라 강의 자료·요약으로 확인. 바닥선 네 모양은 위키의 종합, ThreadLocal+풀 누수와 Flink 상태 TTL 대응은 위키의 연결.

## [2026-09-27] query | 스레드의 스택과 가상 스레드의 스택

「스레드의 스택이 뭔가」 질의의 답은 [[JVM 메모리 구조]]에 이미 있어 노트를 만들지 않았다. 답에서 미검증으로 남긴 가상 스레드 부분을 JEP 444로 검증해 추가했다.

- 고친 페이지: [[JVM 메모리 구조]](「가상 스레드의 스택」 절 — 힙의 stack chunk 객체, mount·unmount, GC Root가 아님), [[가비지 컬렉션]](GC Root 절에 예외 한 줄), [[스레드 풀]](가상 스레드 항목에 링크).
- 외부 검증: JEP 444 원문. 답에서 말한 「멈춰 있는 동안 힙에 저장」은 JEP가 더 강하게 쓴다 — 스택 자체가 힙에 있다. 「mount 때 프레임을 복사한다」는 JEP에 없어 쓰지 않았다.

## [2026-09-27] query | STW와 컴팩션

「STW는 왜 필요하고 왜 발생하며 애플리케이션이 왜 멈추는가, 컴팩션과 연계해서」 질의. 개념에 속한 사실이라 노트가 아니라 [[가비지 컬렉션]]의 STW 절을 보강했다.

- 고친 페이지: [[가비지 컬렉션]] — 1번 이유에 오판 예시, 하위 절 셋(컴팩션이 STW를 부른다 · safepoint · barrier), aliases 추가.
- 외부 검증: HotSpot Glossary(safepoint·mark-compact·TLAB 정의), HotSpot 소스(`safepoint.cpp` arm_safepoint 주석 — 상태별 멈춤 방식, native 스레드는 기다리지 않음 · `threadLocalAllocBuffer.inline.hpp` allocate — bump pointer · `loopnode.cpp` strip mining), Oracle G1 튜닝 가이드 JDK 21(SATB, evacuation, "mostly concurrent, stop-the-world"). 뒷받침됨.
- 답에서 통념으로 둔 「poll은 루프 되돌아가는 지점·메서드 반환에」는 인터프리터(분기·반환 바이트코드)만 소스 주석으로 확인됐다. 컴파일된 코드는 「컴파일러가 넣은 지점에서 polling page를 읽는다」와 C2 strip mining까지만 적었다.
- 새로 안 것: native 코드를 도는 스레드는 safepoint에서 기다리지 않는다 — JNI 코드는 STW 중에도 돈다.

## [2026-09-27] query | JVM이 제공하는 GC의 종류

「JVM GC 종류와 특징」 질의. 답은 대부분 [[가비지 컬렉터]]에 있어 노트를 만들지 않고, 새로 확인한 사실만 그 페이지에 넣었다.

- 고친 페이지: [[가비지 컬렉터]] — Epsilon 행, ZGC 비세대 모드 제거(JDK 24), Shenandoah 세대별 모드 실험(JDK 24)·정식(JDK 25), 켜는 옵션 목록, Oracle 빌드에 Shenandoah가 없다는 단락, 「저지연 GC도 세대별로」 흐름. aliases에 Epsilon GC. index 요약 갱신.
- 외부 검증: JEP 318·404·490·521 원문, Red Hat Developer 2019 글(Oracle은 Shenandoah를 빌드하지 않음), 로컬 JDK 25.0.2(jdk.java.net Oracle OpenJDK 빌드)에서 Shenandoah 미지원·Epsilon 실험 옵션 요구를 실행으로 확인.
- 답에서 「Red Hat·Corretto 등에는 있다」고 한 배포판 목록은 확인하지 않아 페이지에는 「다른 배포판에는 있다, 배포판마다 확인」으로만 적었다.

## [2026-09-27] query | G1 동작 과정과 Region 크기

「G1 GC 동작 과정」 ELI5(칸 청소 artifact)와 「Region의 기준, 용량이 정해져 있나」 질의. 새 사실을 [[가비지 컬렉터]] G1 절에 넣었다.

- 고친 페이지: [[가비지 컬렉터]] — Region 크기 자동 규칙(최대 힙 ÷ 2048, 1~32MB, 2의 거듭제곱 올림, 지정 시 최대 512MB)과 실측, Humongous 기준의 소스 근거와 8GB 힙 예, Remark(빈 Region 즉시 회수)·Cleanup(Mixed로 갈지 결정) 구분.
- 외부 검증: OpenJDK 소스(`g1HeapRegionBounds.hpp`, `g1HeapRegion.cpp`, `g1CollectedHeap.hpp`), Oracle G1 튜닝 가이드 JDK 21(Remark·Cleanup·Space-reclamation 원문), 로컬 JDK 25.0.2에서 `-Xmx`·`G1HeapRegionSize`별 실측.
- 단서로 남긴 것: 「Region을 키워 Humongous를 피한다」는 운영 통념. 128GB 이상 힙은 규칙으로 계산했을 뿐 실행하지 않았다.

## [2026-09-27] query | Humongous 객체가 왜 문제인가

ELI5 질의(소파 artifact). 답의 근거인 Oracle G1 튜닝 가이드 Humongous Objects 절을 [[가비지 컬렉터]]에 옮겼다.

- 고친 페이지: [[가비지 컬렉터]] — Humongous 항목에 특별 취급 다섯 가지(Eden 건너뜀, 늦은 회수와 원시 배열 eager reclaim, IHOP 즉시 확인, 두 번째 Full GC에서야 이동, 끝 Region 낭비로 인한 OOM)와 버전 차이, aliases.
- 외부 검증: Oracle G1 튜닝 가이드 JDK 21·25 원문을 나란히 대조.
- ⚠️ 발견: 비원시 Humongous 객체가 회수되는 pause를 JDK 21 문서는 Cleanup, JDK 25 문서는 Remark로 적는다. 바뀐 릴리스는 미확인.
- 대처(Region 키우기, 큰 배열 쪼개기)는 운영 통념이라 artifact에만 두고 위키에는 기존 한 줄(통념 표시) 외에 보태지 않았다.

## [2026-09-27] query | Java 8에서 11로 가는 GC 관점의 이유

「Java 8은 Parallel 기본이라 톰캣을 여러 개 띄웠고, 11의 G1은 큰 램을 잘라 치우니 전환해야 한다」가 논리적인지 따진 답을 노트로 남겼다.

- 만든 페이지: note [[Java 8에서 11로 가는 GC 관점의 이유]].
- 고친 페이지: [[가비지 컬렉터]](기본 GC의 변천 아래·관련에 링크), index.
- 외부 검증: Oracle Java 8 G1 튜닝 가이드(G1이 8에 있음, 6GB·0.5초 목표), JEP 307(JDK 10 전 G1 Full GC 단일 스레드), JEP 254, JDK-8146115와 백포트(8u191 등), Spring Boot 3.0 Release Notes · 4.1.1 System Requirements(최소 Java 17). 뒷받침됨.
- 단서로 남긴 것: 인스턴스 분리의 주된 이유(장애 격리·무중단 배포)는 위키의 판단.

## [2026-09-27] query | ZGC가 기본이 되었나

「문서에 ZGC가 기본이 되었다고 써 있는데」 질의. 위키 표의 「JDK 23부터 generational이 기본 모드」가 「ZGC가 JVM 기본 GC가 됐다」로 읽힐 수 있어 고쳤다. ZGC가 JVM 기본 GC인 적은 없다.

- 고친 페이지: [[가비지 컬렉터]] — ZGC 상태 칸을 「ZGC의 기본 모드가 generational」로 바꾸고 「ZGC 자체가 기본인 적은 없다」를 붙였다. 「기본」 두 가지(JVM 기본 GC vs ZGC 기본 모드)를 나누는 단락과 JEP 439의 동기 인용을 추가했다.
- 외부 검증: JEP 474·523·439 원문, 로컬 JDK 25.0.2(`Using G1`, `ZGenerational` 제거 경고).
- ⚠️ 위키 정정: 오해를 부른 표현이었다. 사실 자체(JEP 474 = JDK 23)는 틀리지 않았다.

## [2026-09-27] query | JEP는 무엇인가

「JEP는 무엇의 약자이고 패치노트라고 알면 되나」 질의. 위키가 JEP와 JDK 이슈를 계속 인용하므로 개념 페이지로 남겼다.

- 결정(사용자): 개념 페이지로 만든다. 스키마대로 개념명은 한국어(「JDK 개선 제안」), JEP·JDK Enhancement Proposal·JBS는 aliases.
- 만든 페이지: concept [[JDK 개선 제안]].
- 고친 페이지: [[JVM]] · [[가비지 컬렉터]](관련에 링크), index(개념 절).
- 외부 검증: JEP 1 원문(JEP를 쓰는 기준 셋, research JEP, JCP를 대체하지 않음), JEP 439·444.
- 단서로 남긴 것: 「JEP는 구현, JSR은 명세」라는 줄인 문장과 「한 기능이 여러 JEP를 거친다」는 위키의 정리.

## [2026-09-27] query | GC 모니터링과 OOM 대처

「GC 모니터링은 왜 필요하고 OOM이 나면 어떻게 대처하나」 질의. 기존 절을 보강했다(노트 없음).

- 고친 페이지: [[가비지 컬렉션]] 「모니터링과 OOM 대응」 — 왜 보나, OOM detail message별 표와 GC overhead limit 기준(98% · 2% · 연속 5번), Exit/CrashOnOutOfMemoryError, JVM OOM vs 컨테이너 OOMKilled 표. aliases에 OutOfMemoryError · OOM · OOMKilled.
- 외부 검증: Oracle Troubleshooting Guide JDK 25(메시지 종류, overhead 기준), JDK 25 플래그 기본값, HotSpot `globals.hpp`(Exit·Crash 플래그 설명), `java` 매뉴얼 JDK 25(MaxRAMPercentage 25%), Kubernetes 메모리 문서(limit 초과 → 종료 후보).
- 답에서 말한 「unable to create native thread」는 JDK 25 가이드의 메시지 목록에 없어 넣지 않았다. 「OOM 뒤엔 끝내는 게 낫다」와 「25%는 힙 밖 여유 때문」은 1차 자료에 없어 통념으로 표시했다.

## [2026-09-27] query | GC 튜닝 순서

「GC 튜닝은 어떤 순서로 하나」 질의의 답을 노트로 남겼다.

- 만든 페이지: note [[GC 튜닝 순서]].
- 고친 페이지: [[가비지 컬렉터]](관련), [[가비지 컬렉션]](모니터링 절에 링크), index.
- 외부 검증: Oracle GC Tuning Guide JDK 25 — Ergonomics(목표 셋의 충돌), Available Collectors(기본값 먼저·컬렉터 선택 기준), G1 Tuning(General Recommendations, Moving to G1, Young 고정 금지, 증상별 절: Full GC · Humongous · Sys 시간 · Reference 처리 · Young · Mixed). 답의 5단계 표를 가이드 원문으로 다시 채웠다(Sys 시간·Mixed GC 행이 새로 들어갔다).
- 단서로 남긴 것: 「코드부터」를 1단계로 둔 것은 위키의 판단, 「하나씩 바꾼다」는 통념.

## [2026-09-27] lint | GC 질의 연작 뒤 린트

- 범위: 직전 린트(`62fd061`) 이후 바뀐 13개 파일(노트 4 · 개념 1 신규, GC 개념 페이지 보강). 기계 검사는 전체 91페이지 — 깨진 링크 ·고아 · index 누락 · aliases 충돌 · 제목≠파일명 모두 0.
- ① 표 깨짐(사용자 보고): [[가비지 컬렉션]] 모니터링 절의 표 둘이 목록 항목 안에 들여써져 Obsidian이 표로 그리지 않았다. 절을 `###` 소절 넷(왜·무엇 / OOM 메시지 / 대응 순서 / 컨테이너)과 「DE에서」로 나누고 표를 목록 밖으로 뺐다. 전체에서 들여쓴 표는 이 페이지뿐이었다([[데이터 드리프트]]의 `\|`는 이스케이프라 정상).
- ② 과단순화: 「Old는 mark-compact」를 4곳에서 고쳤다 — 기본 G1은 Old Region도 Mixed GC에서 복사하고, mark-compact는 Serial·Parallel의 Old와 Full GC다([[가비지 컬렉션]] 면접 답·정정 표, index, [[레퍼런스 카운팅과 마크 앤 스윕]]).
- ③ 불일치: [[객체 수명과 메모리 상한]]의 「힙 점유가 IHOP」 → 「Old 점유(힙 대비 비율)」(Oracle 원문 기준). [[Java 8에서 11로 가는 GC 관점의 이유]]의 server-class 조건을 「CPU 2개 미만 또는 메모리 1792MB 미만」으로 명확히.
- ④ index 요약 갱신: [[가비지 컬렉션]], [[JVM 메모리 구조]].
- ⑤ 교차참조: [[스레드 풀]] → [[객체 수명과 메모리 상한]](ThreadLocal), [[JVM 메모리 구조]] → OOM 대응·안티패턴, 트래커 [[인프런 Java 면접 강의]]에 이번 파생 페이지 목록. aliases에 「약한 세대 가설」.
- 보류: Kubernetes(8개 페이지에 언급, 페이지 없음) — 자료가 더 들어오면. Tomcat·Spring Boot는 계속 보류.
- 제안: Humongous 회수 시점이 JDK 21 문서(Cleanup)와 25 문서(Remark)에서 다른 이유를 릴리스 노트·JBS로 찾기. 강의 Section 4(동시성)도 같은 질의 방식으로 파고들기.

## [2026-09-27] query | Humongous 회수 시점이 바뀐 릴리스

직전 린트의 제안(JDK 21 문서 Cleanup vs 25 문서 Remark)을 추적했다.

- 결과: **동작은 JDK 11에서 바뀌었고, 문서만 JDK 22에서 고쳐졌다.** JDK-8154528(Fixed in 11)이 죽은 Humongous와 빈 Region의 회수를 Cleanup 뒤에서 Remark로 옮겼다. 튜닝 가이드는 17·21판까지 Cleanup, 22판부터 Remark로 적는다(6개 판 대조). 17·21판은 같은 문서의 Remark 설명과 스스로 어긋나 있었다. 22판 수정은 JDK-8319794(문서 갱신 이슈)로 추정 — 이슈 본문에 이 문장이 명시되지 않아 추론으로 표시.
- 고친 페이지: [[가비지 컬렉터]] Humongous 항목의 「버전 차이」 단락을 위 결과로 바꿨다.

## [2026-09-27] ingest | Java 면접 3 빈출 질문 (GC 부록 PDF)

- 자료: `raw/interviews/java/GC_채널톡_면접관이_뽑은_빈출_질문.pdf` — 「[GC] 채널톡 면접관이 뽑은 빈출 질문」, A3 1쪽, 6문항(빈도 별점 + 짧은 답). Section 2 부록과 같은 형식이라 **Section 3의 부록**으로 두었다(추론, 사용자 승인).
- 만든 페이지: [[Java 면접 3 빈출 질문]].
- 외부 검증(JLS §12.7 · JEP 122 · JDK-6962931·7017732·6990754·8212084 · GC Tuning Guide JDK 26 · Troubleshooting Guide JDK 8·21): 12건 가운데 틀림 2(Metaspace는 "OS가 관리", "정적 변수만" 힙) · 단서 필요 10. 핵심 인용 5개는 원문으로 다시 확인했다.
- 고친 페이지:
  - [[가비지 컬렉션]] — 쓰레기의 기준(도달 가능성)과 Java 누수의 정의, overhead limit을 어느 컬렉터가 던지나(Parallel · G1은 JDK 26부터), 정정 표에 부록 4행. ⚠️ 위키 정정: 「JDK 25 기본값과 맞는다」가 G1에도 적용되는 것처럼 읽혔다.
  - [[JVM 메모리 구조]] — PermGen → Metaspace 두 단계(JDK 7·8) 표, Metaspace는 JVM이 관리, static 필드의 회수(클래스 언로드, JLS §12.7).
  - [[인프런 Java 면접 강의]] — 자료 표, 인제스트 상태(3 부록), 자료 평가·검증 표.
  - [[Java 면접 3 GC]] — 관련에 부록 링크. `index.md` 요약 3줄.

## [2026-09-27] query | 가시성 문제는 지금도 생기나

- 질문: 캐시가 코히런트하다면 가시성 문제는 이제 잘 안 생기나. 답: 아니다 — 원인 설명이 바뀌었을 뿐 문제는 그대로다.
- 근거: 로컬 재현(OpenJDK 25.0.2, arm64). `volatile` 없는 종료 플래그 루프는 3초 뒤에도 돌고, `volatile`이면 멈추고, `-Xint`면 멈춘다 → 범인은 JIT. hoisting이라는 해석은 기계어를 보지 않은 추론으로 표시. j.u.c Memory Consistency Properties 원문을 인용했다.
- 만든 페이지: [[가시성 문제는 지금도 생기나]]. 고친 페이지: [[동시성 문제]](관련 링크), `index.md`.
- 같은 질의 전에 가시성 ELI5 페이지(artifact, 위키 밖)를 만들었다.

## [2026-09-27] query | 원자성 문제가 나는 시나리오

- 로컬 재현(OpenJDK 25.0.2, arm64): 두 스레드 × 1,000만 번 — `int++` 10.66M·9.99M, `volatile int++` 11.09M·10.61M, `synchronized`·`AtomicInteger` 20M. `ConcurrentHashMap`의 `containsKey`+`put`은 2000회 중 187회 이중 초기화, `computeIfAbsent`는 0회.
- 네 가지 모양으로 정리(위키의 분류): 읽고-고치고-쓰기, 확인 후 행동, 여러 값 함께 바꾸기(재현 안 함), 64비트 쪼개짐(JLS §17.7 원문 인용, HotSpot에서의 실제 동작은 미확인).
- 만든 페이지: [[원자성 문제가 나는 시나리오]]. 고친 페이지: [[동시성 문제]] · [[가시성 문제는 지금도 생기나]](관련 링크), `index.md`.

## [2026-09-27] query | 동기화 기법 보강 — volatile·synchronized·CAS가 잘 정리되어 있나

- 진단: 짝·정정·HotSpot 동작은 좋았고, 빈 곳 여섯(ReentrantLock, ABA, 문제별 선택, synchronized의 가시성·재진입, DCL·64비트 volatile, 새 노트로 가는 링크)과 재확인할 서술 하나(경량 락)를 사용자에게 보고한 뒤 승인받아 채웠다.
- 외부 검증(백그라운드) + 원문 재확인: JLS §17.1·17.4.5·17.7, ReentrantLock·Lock·Condition·atomic 패키지 javadoc(SE 25), Pugh 외 DCL Declaration, JBS REST API로 JDK-8291555(21)·8319251(23)·8319796(23)·8334299(24)·8359437(26)·8080603(9) fix version, HotSpot 소스 `synchronizer.cpp`·`lockStack.hpp`·`lockStack.inline.hpp`·`objectMonitor.cpp`·aarch64 `cmpxchg`, `AtomicInteger.java` 주석. 로컬 JDK 25: `LockingMode=2`, `UseLSE=true`.
- ⚠️ 위키 정정: 경량 락을 "헤더에 CAS로 소유 표시"로만 적었던 것 — 지금 방식은 lock 비트 CAS + 스레드별 lock-stack(용량 8) push. 본문에 명시.
- 단서로 남긴 것: "GC 덕분에 참조 ABA가 드물다"(1차 자료 없음), 불변 객체 + AtomicReference 패턴(javadoc이 직접 권하지 않음), JDK-8319253 롤백 사유(미확인).
- 고친 페이지: [[동기화 기법]], `index.md`.

## [2026-09-27] query | synchronized의 문제점과 구현

- 로컬 JDK 25 `javap -c`: 블록은 `monitorenter` 하나 + `monitorexit` 둘(예외 경로, exception table `any`), 메서드는 `ACC_SYNCHRONIZED`(0x0020)만. HotSpot `objectMonitor.hpp`(master)의 `_owner`·`_recursions`·`_entry_list`·`_wait_set`·`_succ` 주석을 인용. deflate 과정은 추론으로 표시.
- 문제점: 기다리는 방법이 하나(포기·타임아웃·인터럽트·공정성·조건 여러 개·읽기/쓰기 구분 없음)와 쓰는 쪽의 사고(락 범위, 락 객체 노출, JVM 하나 안에서만). `Object.notify()`의 "arbitrary", `Integer.valueOf` 캐시 범위는 SE 25 javadoc 원문으로 확인.
- 고친 페이지: [[동기화 기법]](「바이트코드로 보면」·ObjectMonitor 표·「synchronized의 문제점」, 면접·정정 표), `index.md`.

## [2026-09-27] query | 데드락 재현과 해법

- 로컬 재현(OpenJDK 25.0.2, arm64): 반대 방향 이체 `synchronized` → 두 스레드 BLOCKED, `findDeadlockedThreads` 2개, `jstack` "Found one Java-level deadlock"(waiting to lock **monitor** — inflate된 뒤). 순서 고정과 `tryLock(10ms)`+무작위 물러서기(재시도 2·1번)는 끝나고 잔액 110·90.
- 네 조건(Coffman 외, 교과서 설명 — 원 논문 미확인), 해법 비교, DB 데드락과의 차이(DB는 감지 후 롤백 — 재현 안 함).
- 만든 페이지: [[데드락 재현과 해법]]. 고친 페이지: [[동기화 기법]] · [[동시성 문제]](링크), `index.md`.

## [2026-09-27] query | 스레드 풀과 Spring MVC가 스레드를 수백 개 쓰는 이유

- 로컬 재현(JDK 25): `ThreadPoolExecutor(core=2, max=4)` — 무제한 큐면 스레드가 끝까지 2개, `ArrayBlockingQueue(3)`면 큐가 찬 뒤 4개 → 거절.
- 1차 자료로 확인: Tomcat 10.1 HTTP Connector 문서(maxThreads 200 · minSpareThreads 10 · maxConnections 8192 · acceptCount 100), Tomcat `TaskQueue.offer()`(스레드를 max까지 먼저 늘림), Spring Boot `TomcatServerProperties`(같은 기본값), HikariCP `DEFAULT_POOL_SIZE = 10`.
- ⚠️ 위키 정정: `acceptCount`를 "스레드가 다 찼을 때 대기할 연결 수"로 적었던 것 → `maxConnections`가 찬 뒤의 OS 대기열(Tomcat 문서 기준, Spring Boot 설명과 어긋남을 명시).
- 리틀의 법칙과 코어 × (1 + 대기/계산) 공식으로 필요한 스레드 수 계산을 넣었다(JCiP 원문 미확인으로 표시).
- 고친 페이지: [[스레드 풀]], `index.md`.

## [2026-09-27] schema | 서식 규칙 — 직접 줄바꿈 금지, 표는 들여쓰지 않기

- 사용자 보고: 문장 중간에서 끊겨 보이는 곳이 많다(Obsidian 은 줄바꿈 하나도 그대로 보여 준다). 페이지 규칙에 「서식」 절을 넣었다 — 문단과 목록 항목은 한 줄로, 표는 들여쓰지 않고 앞뒤 빈 줄, 칸 안 `|` 는 `\|`.

## [2026-09-27] lint | 직접 줄바꿈 일괄 제거, 들여쓴 표

- 사용자 보고: 문장 중간 줄바꿈이 많고 표가 잘못된 곳이 있다. 측정: 파일 99개 중 98개, 이음새 1,781곳(sources 698 · concepts 681 · entities 138 · notes 107 · 루트 파일 152). 표 구조 검사(들여쓰기 · 앞뒤 빈 줄 · 구분선 · 행별 열 수 · 칸 안 `|`)에서 걸린 것은 [[스레드 풀]]의 Tomcat 기본값 표 하나(목록 안에 들여씀, 이 세션에서 넣은 것).
- 조치: 스크립트로 문단 · 목록 항목 · 인용문의 이어진 줄을 한 줄로 합쳤다(코드 블록 · frontmatter · 표 · 제목 · 새 목록 항목은 그대로). 이음새는 공백 하나로, `·` 뒤와 `,` `.` 앞은 붙이고, `(` 앞은 위키 관례(`다(` 33곳 · `다 (` 0곳)대로 붙이되 앞이 `.` `→` 로 끝나면 띄웠다. Tomcat 표는 `### Tomcat 기본값` 소절로 빼서 들여쓰기를 없앴다.
- 검증: 공백과 인용 `>` 를 뺀 내용이 전 파일에서 전후 동일, 제목 · frontmatter · `[[링크]]` 목록 동일(새 소절 제목 하나 제외), 링크 검사 통과, 재검사 이음새 0 · 표 문제 0.
- 사용자가 말한 "잘못된 표"가 구조 문제가 아닌 다른 모양(긴 칸 등)일 수 있어, 예시를 받으면 검사 항목을 늘리기로 했다.

## [2026-09-27] ingest | Java 면접 4 빈출 질문 (동시성 부록 PDF)

- 자료: `raw/interviews/java/동시성_이슈_채널톡_면접관이_뽑은_빈출_질문.pdf` (A3 2쪽, 9문항, 빈도 별점). 워터마크로 인프런 확인, 식별 정보는 옮기지 않음. Section 4의 부록으로 둠(추론).
- 결정(사용자): 새 개념 2개 — 불변 객체 · 동시성 컬렉션. 스레드 안전 정의는 동시성 문제, LazyHolder는 동기화 기법 + 클래스 로딩에 보강.
- 외부 검증 11건(JLS §12.4 · §17.5 · OpenJDK master/jdk8u/jdk7u 컬렉션 소스 · j.u.c package-summary · JDK-8134853): 틀림 2(synchronized 싱글톤 비용, "Concurrent는 읽기 락 없음") · 단서 필요 8 · 맞음(누락) 1.
- 새로: [[Java 면접 4 빈출 질문]] · [[불변 객체]] · [[동시성 컬렉션]]
- 고침: [[동시성 문제]](스레드 안전의 정의, 가시성만 풀면 되나) · [[동기화 기법]](싱글톤 지연 초기화 절) · [[클래스 로딩]](초기화 락 절) · [[캡슐화]] · [[함수형 프로그래밍]] · [[Java 면접 4 동시성 이슈]] · [[인프런 Java 면접 강의]](트래커) · index
- 위키 자체 주장 검증 12건(fork, JLS §6.6.1 · §8.9 · §12.4.2 · §17.5 · OpenJDK 소스 · JDK 25 재현): 맞음 10 · 단서 2. 반영 — JDK 7 세그먼트 16은 상한이 아니라 기대치, 클래스 초기화 데드락은 JLS 밖의 결과이고 스레드가 RUNNABLE로 보임. enum 싱글톤 보장을 JLS §8.9로, CHM의 LongAdder 계보를 소스 주석으로 격상.

## [2026-09-27] query | 클래스 초기화 데드락은 jstack에 잡히나

- 질문: static 초기화가 서로를 부르는 두 클래스를 두 스레드가 동시에 초기화하면 어떻게 보이나. JDK 25.0.2로 재현했다.
- 결과: 두 스레드 모두 RUNNABLE, `findDeadlockedThreads`·`findMonitorDeadlockedThreads`는 `null`, `jstack`에 "Found one Java-level deadlock" 없음. 단서는 "waiting on the Class initialization monitor for" 줄뿐이다. 스레드 하나로 돌리면 멈추지 않고 `final` 필드를 기본값 0으로 읽는다(`A.X=2 B.Y=1`).
- 고침: [[데드락 재현과 해법]](새 절) · [[클래스 로딩]] · index.
- HashMap 동시 수정 재현은 사용자 결정으로 넘어갔다.

## [2026-09-27] schema | 문체 규칙 — em dash·굵은 글씨·꼬리 화살표·상투 틀 줄이기, 출처 표지는 문장으로

- `CLAUDE.md` 서식 절에 「문체」 6줄을 더했다(사용자 결정: 문체만 고치고 내용·구조는 유지, 출처 표지는 문장으로 풀기, 규칙을 스키마에 적기).

## [2026-09-27] lint | 전체 문체 정리와 린트 발견 보고

- 범위: `wiki/` 98쪽 + `index.md` + `README.md`. `log.md`는 추가 전용이라 지난 항목을 고치지 않았다. fork 6개가 파일을 나눠 맡았다.
- 결과: 굵은 글씨 1,802 → 25, em dash 1,482 → 292(대부분 절 제목 · 인용 출처 · 빈 표 칸), 「**머리** — 설명」 목록 488 → 0, `*(위키의 …)*` 표지 178 → 0(모두 문장으로 풀어 정보는 남김). 링크 · frontmatter · 코드 · URL · 숫자 · 영어 인용 · 표 행 수는 HEAD와 대조해 보존을 확인했다(남은 차이는 인용 정규식의 오탐과 직접 줄바꿈으로 끊긴 인용을 이은 것).
- em dash가 든 절 제목은 다른 페이지가 「」로 참조할 수 있어 그대로 두었다.
- 린트 발견(아직 고치지 않음, 사용자에게 보고):
  - 확인 필요: JEP 523을 「JDK 27, Delivered」로 적었는데 JDK 27은 아직 GA 전일 수 있다(가비지 컬렉터 · Java 면접 3 GC). Triton v2.72.0 · Spring Boot 4.1.1 · Kafka 4.x · Tesla Dojo 같은 시점 수치. 「LLM은 Part 5」 같은 아직 읽지 않은 Part에 대한 주장(추론 최적화 · 모델 서빙 · LLMOps). JCIP 8.2 · 10.1.2 인용은 원문 미확인.
  - 불일치: JLS 인용 판본이 SE 21과 SE 25로 섞였다. 원자적 복합 연산 목록이 동기화 기법(`putIfAbsent`)과 동시성 컬렉션(`compute`)에서 다르다. instanceof 패턴 매칭 16 · sealed 17 · switch 패턴 21을 「Java 16」 하나로 적은 곳(Java 면접 5).
  - 빠진 교차참조: 새 [[불변 객체]] · [[동시성 컬렉션]]이 원자성 · 가시성 · 데드락 노트에서 링크되지 않는다. Java 면접 3 GC · 4 동시성 이슈의 관련 절에 파생 노트가 없다. Java 면접 2 JVM과 실행 원리 → [[클래스 로딩]], Java 면접 2 빈출 질문 → 3 빈출 질문, 이벤트 기반 아키텍처 → [[스트림 처리]], 스키마 진화 → [[Apache Kafka]], [[AI 데이터 엔지니어링]] 개념 지도 → [[멱등성]].
  - 자기 페이지가 없는 개념: Airflow(11쪽), 데이터 계약(6쪽), RAG · 컨텍스트 엔지니어링, 라벨링 파이프라인, Feast · Kubeflow Pipelines · Flyte, Iceberg, 청킹, Structured Streaming, LSP · SOLID.
  - 중복: AI DE Part 2 source 여러 쪽에 같은 「머리글 템플릿 잔재」 줄, 데이터 품질 축 대조 문장이 1-13 · 1-14 · 1-16에 반복된다.

## [2026-09-27] lint | 린트 발견 사항 정리 — 교차참조 · 불일치 · 시점 사실

- 교차참조 14곳: 원자성 · 가시성 · 데드락 노트 → [[불변 객체]] · [[동시성 컬렉션]] · [[Java 면접 4 빈출 질문]], [[Java 면접 3 GC]] → 파생 노트 4개, [[Java 면접 4 동시성 이슈]] → 재현 노트 3개, [[Java 면접 2 JVM과 실행 원리]] → [[클래스 로딩]], [[Java 면접 2 빈출 질문]] → [[Java 면접 3 빈출 질문]], [[이벤트 기반 아키텍처]]에 관련 절(→ [[스트림 처리]]), [[스키마 진화]] → [[Apache Kafka]], [[AI 데이터 엔지니어링]] 개념 지도에 [[멱등성]], [[JVM]] · [[데이터 누수]] · [[데이터 드리프트]] · [[객체 수명과 메모리 상한]].
- 불일치: 원자적 복합 연산 목록을 `putIfAbsent` · `computeIfAbsent` · `compute` · `merge`로 맞췄다([[동기화 기법]] · [[동시성 컬렉션]]). JLS 인용을 SE 25로 통일했다(인용 문구 8개와 §12.7을 SE 25 원문으로 재확인). 검증 기록에 적힌 「SE 21과 대조」는 사실 기록이라 두고 SE 25에도 같다고 덧붙였다. [[Java 면접 5 객체지향 프로그래밍]]의 「Java 16 이전」을 16 · 17 · 21로 풀었고 [[다형성]]에 record 패턴(JEP 440)을 더했다.
- 「Part 5」 주장을 원본 텍스트로 확인했다: RAG 세부(청킹 · 하이브리드 · 리랭킹)는 Part 5에 있다. LLM 서빙 지표(TTFT · tokens per second · KV cache)는 Part 5가 아니라 Part 4 Ch5에 짧게 나온다 → [[추론 최적화]] · [[모델 서빙]] 정정, [[LLMOps]]는 덱 이름을 적었다.
- 시점 사실(웹 검증 subagent, 1차 자료): JEP 523은 Delivered · Release 27이 맞고 JDK 27 GA는 2026-09-15. Triton v2.72.0(2026-08-31)은 최신이 맞다. Spring Boot 4.1.1(2026-08-20)은 최소 17 · 최대 26. Kafka 최신 4.3.1(2026-06-25), KRaft 전용 유지. Dojo는 2026-03 D3 공개 보도를 2차 자료로 덧붙였다. JCIP §2.1 · §8.2 · §10.1.2는 목차와 발췌로 2차 확인했다.
- 남긴 것: 자기 페이지가 없는 개념(Airflow, 데이터 계약, RAG, Feast · Kubeflow · Flyte, Iceberg, 청킹 등)은 Part 3 이후 인제스트에서 다시 나오면 만든다. AI DE Part 2 source들의 반복 줄과 데이터 품질 축 반복 문장은 중복 정리 후보로 남긴다.

## [2026-09-27] lint | 중복 정리 — 머리글 템플릿 잔재, 품질 축, PSI 정정

- 중복 규칙(전문은 한 곳, source 핵심은 한 줄 + 링크)을 적용했다.
- Part 2 슬라이드 머리글의 템플릿 잔재: source 8쪽(2-02 · 2-03 · 2-04 · 2-05 · 2-06 · 2-07 · 2-08 · 2-10)에 풀어 쓴 같은 문장을 한 줄 + 링크로 줄이고, 전모는 트래커 [[AI 데이터 엔지니어링 강의]]의 「자료가 밝히지 않은 것 (추론 표시)」에 모았다. 2-07에만 있던 사실(덱 `04` 목차 p2는 Ch1 소단원 1 제목)은 트래커로 옮겼다. 2-05의 오탈자(p25)는 그 페이지에 남겼다.
- 데이터 품질 축 세 버전: [[AI DE 강의 1-14 데이터 SLA와 모니터링]]이 세 분류의 구성원까지 다시 적던 것을 한 줄로 줄였다. 대조표는 [[데이터 SLA]] 한 곳이다.
- PSI 임계치 정정: [[AI DE 강의 1-13 Skew와 Drift]]와 [[데이터 드리프트]] 두 곳에 전문이 있었다. source는 한 줄 + 링크로 줄이고, source에만 있던 영어 원문 인용은 개념 페이지로 옮겼다.
- 검토하고 둔 것: [[데이터 관측성]]의 감시 항목 표는 [[데이터 SLA]]의 지표 정의와 관점이 달라(무엇을 약속하나 / 무엇을 감시하나) 중복으로 보지 않았다.

## [2026-09-27] query | 조합이 결합도가 낮은데 상속을 쓰는 이유

- 질의 흐름: 캡슐화 → 상속의 단점 → 다형성 → 이 질문. 앞의 셋은 기존 개념 페이지로 답했다.
- 자료의 답은 「is-a가 명확하고 변화가 적을 때」(p85, p91) 한 줄이다. 위임 코드 비용(Kotlin `by`), 확장용 설계(`AbstractList`, `HttpServlet`, Airflow `BaseOperator`), 같은 사람의 통제, 상태·생성자 공유, sealed 계층을 보충했다. 『Effective Java』 Item 18 · 19는 2차 자료로 표시했다.
- 검증(OpenJDK 25.0.2 `src.zip`): `HashSet`은 `addAll`을 오버라이드하지 않고 `AbstractCollection.addAll`이 `add`를 부른다. `AbstractList` javadoc의 `get(int)` · `size()` 문구. 로컬 재현 `CountingSet` → `addCount=6 size=3`.
- 만든 페이지: [[상속을 쓰는 이유]]. 고친 페이지: [[상속과 조합]](단점 절에 `CountingSet` 예, 관련 링크), `index.md`.

## [2026-09-27] query | 오버로딩과 오버라이딩 정리

- 위키에는 [[다형성]]의 종류 표와 p94 정정뿐이라 규칙과 함정을 담은 개념 페이지를 새로 만들었다. 자료는 둘을 따로 묻지 않으므로 내용은 JLS SE 25와 재현으로 보충했다.
- 검증: JLS SE 25 ch. 8·9·15 원문에서 절 번호(§8.4.5 · §8.4.8.1–3 · §8.4.9 · §8.3 · §9.6.4.4 · §15.12.2.2–5 · §15.12.4.4)와 인용 문장을 확인했다. 로컬 재현(OpenJDK 25.0.2): `f(Object o = "hello")` → `f(Object)`, `g(1)` → `g(long)`, 필드·static은 정적 타입, `List.remove(1)` → 인덱스, `equals(Point)` 오버로딩 → `HashSet` 크기 2. `javac`로 접근 축소 · checked 예외 확대 · 반환 타입만 다른 오버로딩 · 잘못된 `@Override` 네 오류를 확인했다.
- 만든 페이지: [[오버로딩과 오버라이딩]]. 고친 페이지: [[다형성]](aliases `오버라이딩` · `오버로딩`을 새 페이지로 옮기고 링크), `index.md`.

## [2026-09-27] ingest | Java 면접 5 빈출 질문 (Section 5 부록)

- 자료: `raw/interviews/java/객체지향_프로그래밍_채널톡_면접관이_뽑은_빈출_질문.pdf` (A3 3쪽, PDF 생성일 2026-03-07). 제공처 인프런은 워터마크로 확인했고, 워터마크의 식별 정보는 옮기지 않았다.
- 사용자 결정: 새 개념 3개(객체지향 프로그래밍 허브 · SOLID 원칙 · 결합도와 응집도), 중복된 자료 번호(1~14 뒤 11~15)는 1~19로 다시 매기고 자료 번호를 병기.
- 외부 검증(subagent, 1차 자료): JLS SE 25 §4.3.1 · §8.4.3.2 · §8.4.8.1–2 · §9.8 · §15.12.4.1 · §15.27.4, Martin 「The Dependency Inversion Principle」 · 「The Interface Segregation Principle」(1996) · 「Design Principles and Design Patterns」(2000), Liskov 「Data Abstraction and Hierarchy」(1987), Oracle Java Tutorial, Fowler 『Refactoring』 2판 1장은 원문 확인. 『오브젝트』 · 『Clean Architecture』 · 『Clean Code』 · 『Effective Java』는 2차 자료. 결함 12건 가운데 틀림 5 · 단서 필요 5 · 맞음 1 · 의견 1.
- 만든 페이지: [[Java 면접 5 빈출 질문]] · [[객체지향 프로그래밍]] · [[SOLID 원칙]] · [[결합도와 응집도]].
- 고친 페이지: [[다형성]](alias `OCP`를 [[SOLID 원칙]]으로 옮김, 부록 Q13 정정 링크) · [[상속과 조합]](「자료는 LSP를 언급하지 않는다」를 슬라이드로 좁힘) · [[캡슐화]] · [[인터페이스와 추상 클래스]] · [[오버로딩과 오버라이딩]] · [[Java 면접 5 객체지향 프로그래밍]] · 트래커 [[인프런 Java 면접 강의]] · `index.md`.

## [2026-09-27] lint | Java 강의 쪽 내용 검토와 전체 기계 검사

- 기계 검사(페이지 104쪽): frontmatter · title · H1 · 파일명 · type/폴더 · alias 중복 · 깨진 링크 · 고아 · index 누락 · log 머리 모두 0건. 복사본에 오류 5종을 넣어 검사가 잡는 것을 확인했다.
- 위키 자신의 주장 검증(subagent, 6쪽 55건 안팎): 고친 것 5건. [[오버로딩과 오버라이딩]]의 `Point` 예시에 생성자가 빠져 컴파일되지 않았다(재현 코드에는 있었다). [[Java 면접 5 빈출 질문]] 핵심의 별점 셋 질문 수(5 → 6)와 틀린 질문 목록(Q14 누락)이 같은 페이지의 표와 어긋났다. [[SOLID 원칙]]의 「2000년 논문에는 네 원칙만」에 패키지 원칙이 함께 있다는 단서를 붙였다. [[상속을 쓰는 이유]]의 Airflow `BaseOperator` 서술에서 재시도는 설정만 하고 실행은 스케줄러가 한다고 고쳤다. 문체 한 곳(「한 단계 더」)을 고쳤다.
- 새 부록 때문에 낡은 「자료에 없다」 문구를 OOP 쪽 페이지에서 찾았다. [[상속과 조합]] · [[Java 면접 5 객체지향 프로그래밍]]의 LSP · SOLID 문장을 인제스트 때 고쳤고, 나머지는 여전히 맞다.
- 새 페이지 4쪽의 em dash · 굵은 글씨 · 꼬리 화살표 0, 워터마크 식별 정보(6자리 이상 숫자 · `@`) 0.

## [2026-09-27] ingest | Java 면접 기타 빈출 질문 (4 소절)

- 자료: `raw/interviews/java/기타_채널톡_면접관이_뽑은_빈출_질문.pdf` (A3 4쪽, PDF 생성일 2026-03-07). 제공처 인프런은 워터마크로 확인했고, 워터마크의 식별 정보는 옮기지 않았다. 제목의 「[기타]」가 어느 Section과도 맞지 않아 Section 부록으로 두지 않았다.
- 사용자 결정: 자료의 네 소절마다 source 페이지 하나(자바 기본 13 · 문자열·예외·제네릭 10 · 어노테이션·리플렉션 4 · JCF 17), 새 개념 4개. 자료에 번호가 없어 위키가 PDF 전체에 Q1~44를 이어 매겼다.
- 외부 검증(subagent 2개, 언어·버전 / JCF): JLS SE 25 · JVMS · JDK 8·11·25 Javadoc · OpenJDK master 소스(`HashMap` · `ArrayList` · `HashSet` · `synchronizer.cpp` · `globals.hpp`) · JEP 180 · 220 · 282 · 290 · 321 · 323 · 395 · 396 · 403 · 409 · 415 · 431 · 512 · Collections 설계 FAQ 대조. 작성 fork가 인용 절 번호를 원문으로 다시 확인했다. 44문항 가운데 틀림 8 · 낡음 3 · 단서 필요 19 · 맞음 12 · 판정하지 않음 2. Q18은 검증 보고의 「틀림」을 `Exception` Javadoc의 checked 정의를 근거로 「단서 필요」로 낮췄다. Object Javadoc의 주소 문구가 빠진 시점은 두 보고가 JDK 12 / 15로 엇갈려 jdk11u·jdk12u 소스를 비교해 JDK 12로 정했다.
- 만든 페이지: [[Java 면접 기타 빈출 질문 1 자바 기본]] · [[Java 면접 기타 빈출 질문 2 문자열 예외 제네릭]] · [[Java 면접 기타 빈출 질문 3 어노테이션과 리플렉션]] · [[Java 면접 기타 빈출 질문 4 JCF]] · [[equals와 hashCode]] · [[Java 컬렉션 프레임워크]] · [[HashMap]] · [[Java 예외 처리]].
- 고친 페이지: [[JVM]](JDK와 JRE 절) · [[JVM 메모리 구조]](기본형은 스택에 있나 절) · [[동시성 컬렉션]] · [[불변 객체]] · [[오버로딩과 오버라이딩]] · 트래커 [[인프런 Java 면접 강의]] · `index.md`.
- 코드 블록(`Won` record, `Str`, `Erasure`, `Twr`, `Collide`)은 OpenJDK 25.0.2에서 적힌 그대로 컴파일·실행했다.
- 인제스트 직후 위키 주장 검증(fork): 코드 5개 재실행, 인용·절 번호 대조, 판정 합계 · 별점 · 번호 일관성 확인. 고친 것은 [[HashMap]]의 트리화 시점(8개가 되면 → 8개 있는 버킷에 9번째를 넣을 때, `binCount >= TREEIFY_THRESHOLD - 1`), [[Java 면접 기타 빈출 질문 1 자바 기본]] 핵심에서 Q4를 hashCode 결함으로 묶은 것, 굵은 글씨·화살표 문체 3곳이다. 경험 답 가운데 Q23만 「맞음」으로 센 기준 차이는 남겨 두었다.

## [2026-09-27] lint | 기타 부록 인제스트 뒤 린트

- 기계 검사(112쪽): 오류 0. 복사본에 오류 5종(깨진 링크 · 제목 불일치 · alias 중복 · index 누락 · log 머리)을 넣어 모두 잡는 것을 확인했다.
- 모순: 새 페이지와 기존 페이지 사이에 없음(트리화 상수, String pool 위치, 현재 LTS 대조).
- 교차참조 추가: [[오버로딩과 오버라이딩]] ↔ [[Java 예외 처리]](checked 예외 규칙 §8.4.8.3), [[불변 객체]] → [[equals와 hashCode]], [[동기화 기법]]의 enum 싱글톤 → 리플렉션 · 직렬화 source 페이지.
- 판정 기준 통일(사용자 결정): 경험 답 Q23을 「맞음」에서 「판정하지 않음」으로. 기타 부록 총계는 틀림 8 · 낡음 3 · 단서 필요 19 · 맞음 11 · 판정하지 않음 3.
- 공백 채움(웹, 1차 자료): [[HashMap]]의 「해시 충돌 DoS가 배경」을 확인했다. oCERT-2011-003(2011-12-28, "Java, all versions")과 7u 소스의 `hashSeed` 주석이 있지만, Oracle · OpenJDK 공개 자료는 동기를 성능으로만 적고 공개 당시 Oracle은 수정이 필요 없다고 답했다. 그래서 단정하지 않고 위키의 추론으로 적었다.
- 자기 페이지가 없는 개념(제네릭 · 어노테이션과 리플렉션 · 직렬화 · String)은 정정 전문이 source 페이지에 있다. 다른 자료에 다시 나오면 그때 만든다.

## [2026-09-28] ingest | AI DE 강의 Part 3 (시멘틱 & 컨텍스트 기반 데이터 설계, PDF 5개)

- 자료: `raw/data-engineering/ai-de-course/part3/` PDF 5개, 273쪽, PDF 생성일 2026-03-26 · 2026-04-21 · 2026-05-21. 슬라이드에 강사 표기가 없다. PDF Author 필드의 개인 이름은 옮기지 않았다.
- 사용자 결정: source 15페이지(같은 제목 1·2인 Ch1-2·3, Ch4-2·3은 묶고, 제목이 모두 「Graph에 대해 이해하기 N」인 Ch2 소단원 넷은 주제로 나눔), RAG 개념 페이지는 지금 얇게 만들고 Part 5에서 보강, 그래프 쪽 개념은 중간 세밀도(PG·RDF를 한 페이지로, SHACL은 엔티티).
- 외부 검증(subagent 2개, DB·그래프 / RAG·GraphRAG): W3C 명세(RDF 1.1·1.2 CR, RDF Schema 1.1, SHACL 2017·1.2 WD, R2RML), Gilbert–Lynch 2002, Brewer 2012, Cassandra·Neo4j·Neptune·Arango·JanusGraph 문서와 GitHub API, Lewis 2020, Gao 2023, Liu TACL 2024, Edge 2024, Microsoft Research 블로그 4편, You et al. 2024, Neo4j·AWS 사례 페이지. 슬라이드의 SHACL 예시를 pyshacl 0.40.1로 실행해 설명("email 최대 1개")과 코드가 다름을 확인했다.
- 틀림: wide-column = 열 기반 저장, DRIFT 약자, "Naive → Advanced → 구조화된 RAG"(서베이는 Modular), SHACL 설명과 코드 불일치. 단서: CAP의 C, RDFS domain/range를 검증 제약처럼, Lost in the Middle에 붙은 제곱 비용, ArangoDB 라이선스, JanusGraph 릴리스, LazyGraphRAG 미공개, Ch5 「실습」 없음. 위키 자신의 의심(GNN-driving-LLM 이름이 뒤바뀜)은 원 서베이와 같아 틀린 것으로 판명됐다.
- 만든 페이지(source 15): [[AI DE 강의 3-01 스키마 중심 설계와 RDBMS]] ~ [[AI DE 강의 3-15 그래프 DB 제품 비교]]. 개념 10: [[관계형 데이터베이스]] · [[NoSQL]] · [[시맨틱 계층]] · [[그래프 데이터 모델]] · [[지식 그래프]] · [[온톨로지]] · [[데이터 계약]] · [[그래프 데이터베이스]] · [[검색 증강 생성]] · [[GraphRAG]]. 엔티티 6: [[Neo4j]] · [[Amazon Neptune]] · [[ArangoDB]] · [[JanusGraph]] · [[SHACL]] · [[Microsoft GraphRAG]].
- 고친 페이지: 트래커 [[AI 데이터 엔지니어링 강의]](Part 3 표·추론 표시·자료 평가·결함 표, 분할 규칙에 주제 분할 예외) · [[AI 데이터 엔지니어링]](Part 3 개념 지도와 관찰) · [[데이터 거버넌스와 카탈로그]](메타데이터 그래프·계보) · [[행 기반과 열 기반 저장]](wide-column) · [[멱등성]] · [[스키마 진화]] · [[비정형 데이터 파이프라인]] · [[LLMOps]] · [[데이터 SLA]](alias `데이터 계약` · `Data Contract`를 새 페이지로 옮김) · [[AI DE 강의 2-10 Feature Store 기본 개념]](다음 강의 링크) · `index.md`.
- 1차 린트 때 보류한 「자기 페이지가 없는 개념」 가운데 데이터 계약과 RAG를 이번에 만들었다.

## [2026-09-28] lint | Part 3 인제스트 직후 위키 주장 검증과 기계 검사

- 위키 자신의 주장 검증(fork 2개, 약 90건, 쪽 번호 표본 약 35곳): 틀림 6건을 고쳤다. [[NoSQL]]의 「강의는 CAP이 파티션 상황에 한정됨을 말하지 않는다」(p41에 있다), [[AI DE 강의 3-01 스키마 중심 설계와 RDBMS]]의 표지 표기, [[JanusGraph]]의 「백엔드 목록 불완전」(문서가 드는 분산 백엔드 셋과 같다), [[AI DE 강의 3-11 SHACL 검증]]의 「p61은 빈 슬라이드」(텍스트 추출만 보고 판단, 실제로는 코드 이미지), [[온톨로지]]의 OWL 2 날짜(2009-10-27 REC, 2012-12-11은 Second Edition), [[AI DE 강의 3-13 GraphRAG 개념과 사례]]의 「gaming company」 인용(실제 표기는 "Gaming giant").
- 단서·보강: Cassandra 문서의 write-oriented · LSM, ArangoDB 100 GiB, Gremlin의 선언형 사용, Neptune 격리 수준(읽기 snapshot, mutation READ COMMITTED + 잠금), RDF 1.2 triple term, dbt Semantic Layer · LookML, Neo4j 에디션과 제약 종류, Naive · Advanced · Modular 설명을 서베이 II절로 다시 씀, RML은 W3C 표준이 아님. 포크가 「기억 기반」으로 적은 것 대부분을 1차 자료로 바꿨고, 남은 미확인(DDIA 원문, Studer 1998, Bedrock 프리뷰 시점, 최신 모델의 Lost in the Middle)은 페이지에 그렇게 적었다.
- 페이지의 Turtle 코드 블록을 적힌 그대로 pyshacl로 다시 실행해 서술과 맞음을 확인했다.
- 정정이 번진 곳: 옛 문구를 index·트래커·source 전체에서 grep해 트래커 결함 표의 100GB를 100 GiB로 고쳤다.
- 기계 검사(143쪽): alias 충돌 1건(`Microsoft GraphRAG`의 `graphrag`가 `GraphRAG`와 대소문자만 다름)을 alias 삭제로 고친 뒤 오류 0. 복사본에 오류 5종을 넣어 모두 잡는 것을 확인했다.

## [2026-09-28] ingest | AI DE 강의 Part 4 (실시간 & 대규모 데이터 분산 처리 설계, PDF 2개)

- 자료: `raw/data-engineering/ai-de-course/part4/` PDF 2개, 431쪽(356 + 75), PDF 생성일 2026-05-21 · 2026-06-05. 슬라이드에 강사 표기가 없다. PDF Author 필드의 개인 이름은 옮기지 않았다. 그림만 있는 슬라이드 18장은 이미지로 확인했다(코드 이미지 없음).
- 사용자 결정(모두 추천안): source 18페이지(Ch1 소단원 1·2, Ch2 소단원 2·3, 제목이 이어지는 Ch4 소단원 1·2를 묶음), 새 개념 11 + 엔티티 2, 내용이 겹치는 Ch4-3과 Ch5-4는 source를 따로 두고 전문은 [[GPU 할당과 스케줄링]] 한 곳에.
- 외부 검증(subagent 2개, 분산·캐시·스트리밍 29건 / GPU·RAPIDS·SRE 27건): GFS·Raft·Brewer 2012·Gilbert–Lynch·Kleppmann, PostgreSQL·Redis·Kafka·Flink·Spark·SQS·Pulsar 문서, Kreps 2014, Dehghani 2020, CUDA Programming Guide, PyTorch `CUDALoops.cuh`, NVIDIA 데이터시트·MIG·MPS·device plugin·GPU Operator 문서, Kubernetes 문서, RAPIDS 공지(RSN0045), Google SRE 책, NVML·DCGM 문서, GitHub API.
- 틀림: Redis를 CP 예시로, CUDA 스레드 = 코어 1:1, 블록 1,024가 기본값·shared memory로 전체 평균, 연산 융합 "절반"(5 → 3), A100 40GB HBM2e, MIG "A100·H100 전용", RAPIDS 사례 4시간 vs 8시간, cuSpatial(2025-07 보관), Arrow라 전송이 빠르다, 출력 모드 "Upsert". 단서: Spark 마이크로 배치(4.1 Real-Time Mode), 카파 사례의 "늦은 데이터도 정확히", Data Mesh 원칙 둘, SLA = SLO 99.9%, NVTabular 정체, 스펙 표가 H100에서 멈춤, Redis "싱글 스레드"·Master/Slave, Hadoop·Spark 100배.
- 만든 페이지(source 18): [[AI DE 강의 4-01 분산 처리의 등장과 도입 판단]] ~ [[AI DE 강의 4-18 GPU 스케줄링과 할당 최적화]]. 개념 11: [[분산 시스템]] · [[CAP 정리]] · [[복제]] · [[합의 알고리즘]] · [[캐싱]] · [[메시지 브로커]] · [[람다 아키텍처와 카파 아키텍처]] · [[GPU 아키텍처]] · [[GPU 할당과 스케줄링]] · [[서비스 수준 목표]] · [[AI 시스템 모니터링]]. 엔티티 2: [[Redis]] · [[RAPIDS]].
- 고친 페이지: 트래커 [[AI 데이터 엔지니어링 강의]](Part 4 표·추론 표시·자료 평가·결함 표) · [[AI 데이터 엔지니어링]](Part 4 개념 지도와 관찰) · [[NoSQL]](CAP 절과 alias `CAP`·`CAP 정리`·`CAP theorem`을 [[CAP 정리]]로) · [[배치 처리]](alias `Lambda 아키텍처`·`Kappa 아키텍처`를 새 페이지로) · [[스트림 처리]](시각 세 가지, 허용 지연, 출력 모드 정정, Kafka Streams) · [[Apache Kafka]] · [[Apache Flink]] · [[Apache Spark]] · [[이벤트 기반 아키텍처]] · [[멱등성]] · [[데이터 레이크하우스]] · [[데이터 계약]] · [[추론 최적화]] · [[모델 서빙]] · [[Triton Inference Server]] · [[피처 스토어]] · [[MLOps]] · [[데이터 SLA]](네 번째 분류, SLA와 SLO의 구분) · [[데이터 관측성]] · [[지연 시간과 처리량]] · [[데이터 드리프트]] · `index.md`.
- Part 1 린트에서 빈칸으로 남긴 「워터마크 지연과 허용 지연의 관계」를 Part 4 p208로 채웠다.

## [2026-09-28] lint | Part 4 인제스트 직후 위키 주장 검증과 기계 검사

- 위키 자신의 주장 검증(fork 2개, 약 100건, 쪽 번호 표본 약 80곳 모두 일치): 틀림 8건을 고쳤다. Kreps 재처리는 원문이 네 단계이고 강의가 다섯으로 나눴다(「원문과 일치」 문구를 트래커까지 grep해 고침). cudaMalloc은 강의가 맞았다(검증 보고의 「동기화는 주로 cudaFree」가 근거 없음). PyTorch 튜닝 가이드와 CUDA 가이드 인용문이 실제 문장이나 쪽과 달랐다. Ampere 블로그 표기. MIG 최대 인스턴스(A30은 4, Thor iGPU 추가). KServe CNCF 날짜의 출처 페이지.
- 단서·보강: KAFKA-13598 영향·수정 버전, Redis `WAIT` 인용 URL, Redis 8.0 I/O 스레드 근거, Spark Real-Time Mode 지연 표현, Hadoop 초기 연도는 2차 자료, 단종된 A100 40GB·H100 PCIe 사양은 데이터시트로.
- 기계 검사(174쪽): 오류 0. 복사본에 오류 5종(깨진 링크 · 제목 불일치 · alias 중복 · index 누락 · log 머리)을 넣어 모두 잡는 것을 확인했다.
- 확인하지 못한 것: GCP A3 Ultra·A4·A4X GA 날짜(페이지에 미확인으로 적음), Valkey 저장소 생성일 재확인(API rate limit).

## [2026-09-28] ingest | AI DE 강의 Part 5 (LLM과 RAG, PDF 3개)

Part 5의 덱 세 개(40쪽)를 인제스트했다. 사용자 결정은 전부 추천안이었다. 덱 `02`는 임베딩·벡터 검색(p4–9)과 RAG(p10–15)로 나눠 source 4개를 만들었고, 개념은 중간 세밀도(8개)로 잡았다. 슬라이드의 출처 없는 수치는 옮기지 않고 경향으로만 적었다.

- source: [[AI DE 강의 5-01 LLM의 기본 구조]] · [[AI DE 강의 5-02 임베딩과 벡터 검색]] · [[AI DE 강의 5-03 LLM의 한계와 RAG]] · [[AI DE 강의 5-04 하이브리드 검색과 리랭킹]]
- 새 개념: [[대규모 언어 모델]] · [[트랜스포머]] · [[토큰화]] · [[임베딩]] · [[벡터 데이터베이스]] · [[하이브리드 검색]] · [[리랭킹]] · [[검색 평가 지표]]
- 새 엔티티: [[LangChain]]
- 고친 페이지: [[검색 증강 생성]](Part 5 강의, 검색 단계, 세대 구분의 불일치), [[비정형 데이터 파이프라인]], [[LLMOps]], [[AI 데이터 엔지니어링]], [[모델 서빙]], [[추론 최적화]], [[AI DE 강의 3-12 RAG의 이해와 한계]], [[AI DE 강의 4-18 GPU 스케줄링과 할당 최적화]], 트래커 [[AI 데이터 엔지니어링 강의]]

외부 사실 검증은 두 갈래(LLM 기초 13건, 검색·리랭킹 11건)로 1차 자료와 대조했다. 틀림은 LSTM 연도, BERT-base 파라미터 수, BPE의 방향, Bi-Encoder O(1), Recall@K 정의(실제로는 Precision@K), "3세대 RAG"였다. 낡음·과장은 GPT-4 크기, 2K 토큰, LangChain 통계, FAISS 분류, RRF k 범위였다. RRF 계산 예시는 위키가 검산했고 맞다.

트래커는 Part 5가 청킹 방법을 채우리라 기대했지만, 원본에는 "의미 단위로 청킹, 오버랩 설정" 한 줄뿐이다. [[검색 증강 생성]]·[[비정형 데이터 파이프라인]]의 빈칸 문구를 그에 맞게 고쳤다. 다섯 파트 인제스트를 모두 마쳤다.

## [2026-09-28] lint | Part 5 인제스트 직후 위키 주장 검증과 기계 검사

인제스트 커밋(6efd4ee) 뒤 Part 5 페이지 13개와 [[검색 증강 생성]]의 바뀐 부분에서 위키 자신의 주장(보충, 정정 문구, 인용문, 쪽 번호)을 두 갈래로 1차 자료와 대조했다. 약 70건 가운데 틀림 1, 단서 필요 11이었고 그 자리에서 고쳤다.

- 틀림: [[검색 증강 생성]]의 "3-12 p14가 Gao et al.을 출처로 단다". 출처는 p8에 있다.
- 단서: BM25 원전 식에는 분자의 (k₁+1)이 없다(순위는 같다). RRF에서 k=70·80이 60보다 조금 높아 60은 최댓값이 아니다. 「K가 커지면 재현율은 보통 오른다」는 「줄지 않는다」로 고쳤다. Weaviate 라이선스는 코드 위치에 따라 다르다. 한국어 형태소 분석의 영향은 표현을 누그러뜨리고 근거를 달았다. 그 밖에 표현 두 곳을 고쳤다.
- 확인으로 바뀐 것: 인제스트 때 요약 도구를 거쳐 단서를 달았던 Singh et al. 서베이의 절 제목, OpenSearch RRF 기본값 60, Qdrant 기본 상수 2를 원문에서 직접 확인했고, 단서 문구를 확정 문장으로 바꿨다. 형태소 분석 뒤 BPE는 Park et al. 2020으로 근거를 달았다.

기계 검사(frontmatter·제목·타입·alias 충돌·깨진 링크·고아·index 누락·log 머리, NFC)는 187쪽 오류 0이다. 복사본에 오류 3건을 넣어 검사가 공허하지 않음을 확인했다.

## [2026-09-28] lint | 다섯 파트 인제스트 뒤 전체 린트

1차 린트(2026-09-14) 때 정한 대로 Part 5 뒤에 AI DE 강의 전체를 린트했다. 파트별 사실 검증은 인제스트 직후마다 했으므로 이번에는 파트 사이의 이음새를 봤다. 원본 PDF 40개의 텍스트를 추출해 두고, 「Part N에 없다」 같은 문장은 모두 원본 grep으로 확인했다. 주제 넷(저장·수집·스키마 / 스트리밍·분산 / ML 운영·서빙·GPU / 그래프·LLM·RAG와 허브)으로 나눈 읽기 전용 fork가 발견 사항을 보고했고, 사용자가 ①모순 ②낡은 주장 ⑤교차참조를 고치기로 정했다(새 페이지는 만들지 않음). 수정은 파일 소유권을 나눈 fork 넷과 부모(트래커·허브·index)가 했다. 파일 46개가 바뀌었다.

- 모순: 트래커 Part 1 머리글 282p → 286p(표의 합과 pdfinfo 합). 트래커와 [[AI 데이터 엔지니어링]]의 개념 표 분류(Part 2 도구, Part 4 운영, Part 5 단계 이름·LangChain 위치)를 맞췄다. [[데이터 레이크하우스]]의 Hudi 서술, [[관계형 데이터베이스]]의 「ACID는 두 곳」(실제 다섯 곳), [[AI DE 강의 4-09 워터마크와 윈도우 연산]]의 자기모순을 고쳤다.
- 나중 파트 때문에 낡은 주장: [[대규모 언어 모델]]의 「파인튜닝·RLHF 없음」은 Part 5에만 맞다(Part 2에 이름이 나온다). [[리랭킹]]이 1-09 p19·2-03을 빠뜨렸다. [[학습-서빙 스큐]]·[[피처 스토어]]에 Part 4 p19의 offline-online mismatch SLO를 넣었다. [[모델 서빙]]의 배포 전략 빈칸에 1-13·1-16·4-16 근거를 달았다. MLflow는 4-13이 역할까지 설명한다([[데이터와 모델 버전 관리]], [[데이터 거버넌스와 카탈로그]]). 1-05의 「ORC는 이후 나오지 않는다」, 3-02의 「CAP 전문은 NoSQL」, 3-15의 「다음 강의: 미인제스트」, 1-16의 빠진 다음 강의 줄, [[LLMOps]]의 부품 위치, index의 Spark·스트림 처리·배치 처리 요약을 고쳤다.
- 교차참조 약 30곳: Part 1 스트리밍 source(1-10·1-11·1-12)에서 Part 4로 가는 링크가 하나도 없던 것을 이었다. 1-09·2-03·3-12 → Part 5 개념, [[GraphRAG]]의 「하이브리드 확장」(벡터 + 그래프 순회)과 [[하이브리드 검색]](BM25 + dense)이 이름만 같다는 구분, 3-07 ↔ [[임베딩]], 관계형 데이터베이스 → [[CAP 정리]]·[[복제]], 스키마 진화·시맨틱 계층 → [[데이터 계약]], [[지연 시간과 처리량]]에 관련 절, [[스트림 처리]] 머리에 Part 1 → Part 4 읽는 순서.
- 허브 [[AI 데이터 엔지니어링]]에 Part 5 관찰과 다섯 파트 종합을 더했다.
- fork가 보고를 원본으로 다시 확인해 바로잡은 것: 3-02의 계약 문장은 p47이 아니라 p46, 데이터 관측성의 Prometheus 두 쪽은 서로 다른 source(2-07·2-08)에 있다.
- 기계 검사(187쪽): 오류 0. 표 구조·직접 줄바꿈 0.
- 남긴 것(보고만): 자기 페이지 후보 Kubernetes(위키 14쪽·원본 34회), 자동 재학습(23쪽·36회), Apache Airflow(13쪽·12회), 청킹(14쪽, 방법은 웹으로 채워야 함). 중간 후보는 모델 배포 전략, 라벨링 파이프라인, PII 비식별화, 데이터 검증이다. 웹으로 채울 공백: 청킹 방법, RAG 답변 평가(RAGAS·ARES), Kafka share group(KIP-932), 그래프 DB 벡터 인덱스, MLOps 성숙도, PagedAttention. 질의 노트 후보: 「Training은 Serving을 따라간다」가 RAG의 인덱싱·질의 정합성에도 성립하는가, 강의 전체 SLI 카탈로그, 강의에 흩어진 「계약」의 여섯 층.

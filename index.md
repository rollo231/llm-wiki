# 인덱스

위키의 모든 페이지 목록. 페이지마다 `[[링크]]` 와 한 줄 요약을 단다.
인제스트하거나 노트를 남길 때마다 갱신하고, 질의할 때 가장 먼저 읽는다.

## 자료

AI 데이터 엔지니어링 강의 — 진행 상태는 트래커 [[AI 데이터 엔지니어링 강의]]에서 본다.

- [[AI DE 강의 1-01 기존 DE와 AI DE]] — OT. 데이터의 소비자가 사람에서 모델로 바뀌는 것이 강의 전체의 틀.
- [[AI DE 강의 1-02 AI DE 마인드셋 Latency와 Versioning]] — 두 마인드셋: 추론 쪽 Latency, 학습 쪽 재현성(데이터 스냅샷·환경 고정·시드).
- [[AI DE 강의 1-03 기술 스택과 툴 생태계]] — 채용 공고로 본 필수 역량. 실제로는 기존 DE 스택 + PyTorch.
- [[AI DE 강의 1-04 저장소의 진화 DW에서 Lakehouse까지]] — DW → 레이크 → 레이크하우스, OLTP/OLAP 설계 5단계. ⚠️ Avro를 열 기반으로 오분류.
- [[AI DE 강의 1-05 열 기반 저장 Parquet와 Avro]] — 쓰기 최적화 Avro와 읽기 최적화 Parquet, 스키마 진화, compaction 패턴.
- [[AI DE 강의 1-06 Delta Lake와 ACID]] — 레이크가 늪이 되는 기술적 원인과 트랜잭션 로그·Time Travel.
- [[AI DE 강의 1-07 배치 처리와 ETL·ELT]] — 배치의 가치(재실행 범위), "무엇이 비싼가"의 역전으로 본 ETL → ELT.
- [[AI DE 강의 1-08 CDC]] — 로그 기반 CDC의 3단계와 정합성 세 장치. ⚠️ 호환성 정의가 뒤바뀜.
- [[AI DE 강의 1-09 비정형 데이터 수집과 전처리]] — 수집·저장(이원화)·처리(OCR·임베딩)·활용(RAG) 4단계.
- [[AI DE 강의 1-10 배치 vs 스트리밍]] — 지연 시간과 처리량의 맞교환을 시스템 수준에서 설명. 사례와 Lambda.
- [[AI DE 강의 1-11 EDA와 Kafka]] — 이벤트 기반 아키텍처와 Kafka의 토픽·파티션·오프셋·컴팩션. ⚠️ ZooKeeper 서술이 낡음.
- [[AI DE 강의 1-12 실시간 처리 엔진]] — 스트림의 세 난관과 윈도우·워터마크·체크포인트, Flink vs Spark.
- [[AI DE 강의 1-13 Skew와 Drift]] — 로직 이중 구현이 만드는 스큐, 데이터·개념 드리프트, 감시와 자동 재학습. 스큐·드리프트 대비는 위키 정정.
- [[AI DE 강의 1-14 데이터 SLA와 모니터링]] — 침묵의 실패, 신선도·완전성·정확성, 관측성과 서킷 브레이커.
- [[AI DE 강의 1-15 데이터 거버넌스와 카탈로그]] — 수비형에서 공격형으로, 3대 메타데이터와 계보, 카탈로그 자동화.
- [[AI DE 강의 1-16 AI 파이프라인 구축 사례]] — Uber·Netflix·Tesla·Meta·Google·Airbnb. 구성 요소는 사실, 수치는 대부분 검증 실패.
- [[AI DE 강의 2-01 데이터 파이프라인의 진화와 데이터 엔지니어]] — Part 2 OT. 온프레미스 → 클라우드 → ML 파이프라인, BI vs AI/ML, DE의 확장 영역. ⚠️ 70% 출처 없음.
- [[AI DE 강의 2-02 MLOps와 ML 생애주기]] — MLOps와 DevOps의 차이, DMLS의 6단계 순환 라이프사이클과 DE의 책임.
- [[AI DE 강의 2-03 LLMOps]] — 모델에서 프롬프트·컨텍스트로. 환각·인젝션 대응, retrieval 계층에서 막는 보안, 비용 통제.
- [[AI DE 강의 2-04 ML 데이터 파이프라인]] — 범위는 수집 너머 라벨·검증·분할·리니지까지. 라벨이 가장 비싸고 취약하다.
- [[AI DE 강의 2-05 서빙 파이프라인 설계]] — 서빙 요구사항, 배치 vs 온라인 서빙, 서빙 경로의 피처와 캐싱. ⚠️ Huyen의 표를 출처 없이.
- [[AI DE 강의 2-06 Training-Serving Skew 예방]] — 스큐의 네 가지 형태와 "Training은 Serving을 따라간다". Part 2에서 가장 설명력이 크다.
- [[AI DE 강의 2-07 Batch vs Online 서빙 아키텍처]] — 배치 서빙 도구(Airflow·KFP·Flyte)와 온라인 서빙의 컴포넌트·요청 경로·운영 요소.
- [[AI DE 강의 2-08 서빙 플랫폼 FastAPI·TorchServe·BentoML·Triton]] — 네 플랫폼의 구조. ⚠️ TorchServe 보관, BentoML Runner 레거시, Triton 서술 오류.
- [[AI DE 강의 2-09 서빙의 CPU·GPU 가속]] — 병목부터 찾고 모델 → 런타임 → GPU 순으로. ⚠️ ORT의 OpenMP·CPU FP16 서술.
- [[AI DE 강의 2-10 Feature Store 기본 개념]] — 피처 = 계산 규칙 + 시점 + 스키마, 필요 없는 경우 다섯 가지. ⚠️ 제목의 "운영"이 없음.

인프런 Java 면접 강의 — 등급별 모범 답변이 붙은 면접 질문집. 트래커 [[인프런 Java 면접 강의]].

- [[Java 면접 2 JVM과 실행 원리]] — JVM 장단점, 실행 과정, JIT(판단 기준·코드 캐시·워밍업). ⚠️ 실행 5단계의 순서가 틀림.
- [[Java 면접 2 빈출 질문]] — Section 2 부록. 빈도 별점을 붙인 5문항: JVM 정의·구조, 클래스 로더, 로딩·링크·초기화, 메모리 영역. ⚠️ "가상 OS", 로더가 링크·초기화를 한다는 서술.
- [[Java 면접 3 GC]] — GC 알고리즘, Heap 세대, Root, STW, 컬렉터 종류, G1, OOM 대응. ⚠️ "Mark and Sweep" 단순화, 목록이 CMS·G1에서 멈춤.
- [[Java 면접 3 빈출 질문]] — Section 3 부록. 빈도 별점을 붙인 6문항: GC 정의·장단점, OOM 종류·차이, PermGen vs Metaspace, static의 GC. ⚠️ "아무도 안 가리키면 쓰레기", Metaspace는 "OS가 관리".
- [[Java 면접 4 동시성 이슈]] — 가시성·원자성, volatile·synchronized·CAS, 모니터, 스레드 풀. ⚠️ "volatile은 캐시 우회"는 오해.
- [[Java 면접 5 객체지향 프로그래밍]] — 캡슐화, 상속 vs 조합, 다형성·instanceof, 인터페이스 vs 추상 클래스. ⚠️ 오버로딩·instanceof·private 메서드.
- [[Java 면접 6 람다와 스트림]] — 람다·스트림 도입 이유, 함수형 프로그래밍, 지연 연산. ⚠️ "순수 함수라 스레드 안전"은 과장.

## 엔티티

- [[AI 데이터 엔지니어링 강의]] — 패스트캠퍼스 강의. 인제스트 트래커와 Part 1·2 자료 평가·결함 표.
- [[Apache Kafka]] — 로그 기반 이벤트 스트리밍 플랫폼. 파티션 단위 순서, replay, 로그 컴팩션, 4.0부터 KRaft 전용.
- [[Apache Parquet]] — 열 기반 파일 포맷. pruning·pushdown·인코딩으로 "안 읽기", 메타데이터는 footer.
- [[Apache Avro]] — 행 기반 바이너리 직렬화. self-describing, 스키마 진화, 실시간 유입용.
- [[Delta Lake]] — Parquet 위 트랜잭션 로그로 ACID·Time Travel을 주는 테이블 포맷.
- [[Apache Flink]] — 네이티브 스트리밍 엔진. 이벤트 시간·워터마크·exactly-once 상태.
- [[Apache Spark]] — 분산 처리 엔진. 배치 엔진이자 마이크로 배치 스트리밍, DStream은 레거시.
- [[Debezium]] — Kafka Connect 기반 로그 기반 CDC 도구.
- [[Designing Machine Learning Systems]] — Chip Huyen의 책(O'Reilly 2022). Part 2가 라이프사이클 그림과 배치·온라인 표를 가져온다.
- [[FastAPI]] — Starlette 위의 Python 웹 프레임워크. 가장 자유롭고, 모델 관리는 직접 만든다.
- [[TorchServe]] — PyTorch 모델 서버(Java 프론트엔드 · Python 워커). 2025-08 저장소 보관.
- [[BentoML]] — 모델 패키징·서빙 프레임워크. 강의가 설명하는 Runner·Yatai 구조는 레거시.
- [[Triton Inference Server]] — NVIDIA 추론 서버. 동적 배칭, 멀티 프레임워크 백엔드, 현재 이름 Dynamo-Triton.
- [[ONNX]] — 프레임워크 독립 모델 그래프 표준과 추론 전용 엔진 ONNX Runtime.
- [[인프런 Java 면접 강의]] — 인프런 Java 면접 대비 강의. 트래커, Bronze·Silver·Gold 루브릭, 결함 표.
- [[JVM]] — HotSpot JVM. JVMS의 "abstract computing machine", 실행 파이프라인(정정된 순서), Kafka·Spark·Flink가 올라가는 런타임.

## 개념

- [[AI 데이터 엔지니어링]] — 소비자가 모델인 데이터 엔지니어링. Part 1·2 개념 지도.
- [[지연 시간과 처리량]] — 시소의 법칙과 그 물리적 원인, 이 축 위의 설계 선택들.
- [[데이터와 모델 버전 관리]] — 재현성 3요소, Part 1에 흩어진 구현 수단, Part 2에서 늘어난 버전 대상(스케일링 파라미터·프롬프트).
- [[행 기반과 열 기반 저장]] — OLTP/OLAP, AI 학습 워크로드가 열 기반에 맞는 이유.
- [[데이터 레이크하우스]] — DW와 레이크의 결합. 늪의 기술적 원인과 조직적 원인.
- [[스키마 진화]] — 호환성 모드(Confluent 기준 정정), 레지스트리, 스키마는 계약이다.
- [[ETL과 ELT]] — 변환 위치의 차이와 "무엇이 비싼가"의 역전, 규제 도메인의 ETL.
- [[배치 처리]] — 여전히 기본값인 이유, 마이크로 배치와 Lambda/Kappa.
- [[변경 데이터 캡처]] — 로그 기반 CDC, 정합성 세 장치, 스트림과 테이블.
- [[비정형 데이터 파이프라인]] — 4단계와 저장 이원화, 임베딩·벡터 DB·RAG. 청킹이 빈칸.
- [[이벤트 기반 아키텍처]] — 느슨한 결합, 영속·Pull·replay, 허브 앤 스포크.
- [[스트림 처리]] — 세 난관과 세 장치(윈도우·워터마크·체크포인트), 늦은 데이터 전략.
- [[학습-서빙 스큐]] — 로직의 이중 구현이 만드는 조용한 오류, 네 가지 형태, 드리프트와의 구분(위키 정정).
- [[데이터 드리프트]] — data drift와 concept drift, 감지 지표(PSI 관례 정정), 자동 재학습, 용어의 갈래.
- [[피처 스토어]] — 오프라인·온라인 스토어, 스큐 제거, 피처 = 계산 규칙 + 시점, 필요 없는 경우.
- [[데이터 SLA]] — 침묵의 실패와 품질 지표. 강의 안 세 가지 분류의 대조.
- [[데이터 관측성]] — 자동 감시, 경고 피로 방지, RCA, 서킷 브레이커.
- [[데이터 거버넌스와 카탈로그]] — 3대 요소·3대 메타데이터·계보, 카탈로그는 최신성으로 실패한다.
- [[MLOps]] — ML 시스템을 운영 가능하게 만드는 체계. 6단계 순환 라이프사이클, DevOps와의 차이.
- [[LLMOps]] — LLM 시스템 운영. 컨텍스트 엔지니어링, 새 위험과 대응, 늘어난 변경 지점.
- [[모델 서빙]] — 배치 vs 온라인, 서빙 경로의 피처, 플랫폼의 층, 모델 버전과 배포.
- [[추론 최적화]] — 병목 분해 → 양자화·가지치기·증류 → 런타임 → 배칭 → GPU 전환 판단.
- [[데이터 누수]] — 분할 누수와 피처 시점 누수, 스큐와 증상이 같은 이유. 위키의 종합.
- [[멱등성]] — 여러 번 적용해도 한 번과 같은 성질. at-least-once + 멱등 반영, upsert·파티션 덮어쓰기, 결정성·원자성과의 구분.
- [[JDK 개선 제안]] — JEP란 무엇인가(패치노트가 아닌 제안·설계서), 읽는 법, 릴리스 노트·JDK 이슈·JSR과의 차이.
- [[JIT 컴파일]] — 인터프리터 → C1 → C2 계층 컴파일(tier 0~4), 임계치(호출 + back-edge), 역최적화, Graal JIT, 코드 캐시, 워밍업과 AOT 대안.
- [[클래스 로딩]] — 로딩 → 링크(검증·준비·해석) → 초기화. 로더의 몫은 로딩뿐이고, 명세가 정하는 것은 초기화 시점, JDK 9 이후 내장 로더 3종과 부모 위임.
- [[JVM 메모리 구조]] — JVMS 런타임 데이터 영역 6개와 HotSpot 구현(Metaspace, static·intern 문자열은 힙, 코드 캐시, 합쳐진 스택), PermGen → Metaspace 두 단계(JDK 7·8), static 필드의 회수(클래스 언로드), 영역별 오류, 가상 스레드의 스택(힙, GC Root 아님).
- [[가비지 컬렉션]] — 도달 가능성, 세대 가설, 치우는 방식(복사·mark-compact·mark-sweep), GC Root와 remembered set, STW(safepoint·컴팩션·barrier), OOM 메시지별 대응(overhead limit은 Parallel, G1은 JDK 26부터)과 OOMKilled, 누수의 정의.
- [[가비지 컬렉터]] — Serial·Parallel·CMS(제거)·G1·ZGC·Shenandoah·Epsilon, 기본 GC 연표(JEP 248·523), 처리량 vs 지연.
- [[동시성 문제]] — 가시성·원자성, 원인은 캐시 불일치가 아니라 재배치·레지스터·store buffer, JMM happens-before.
- [[동기화 기법]] — volatile(DCL·64비트), synchronized(가시성·재진입, 바이트코드의 두 monitorexit, lightweight locking의 lock-stack, ObjectMonitor 필드, JDK 21→26 연표, 문제점 표), ReentrantLock 비교표, CAS(x86·ARM 명령, ABA, 여러 값은 불변 객체+AtomicReference)와 LongAdder, 문제별 선택표, 가상 스레드 pinning.
- [[스레드 풀]] — 작업 큐와 재사용, Blocking I/O 서버가 스레드를 수백 개 두는 이유, 가상 스레드.
- [[캡슐화]] — 정보 은닉, 변경에 유연한 코드, getter/setter 대신 행동 메서드.
- [[상속과 조합]] — is-a와 has-a, 상속의 결합도 문제, 조합을 선호하는 이유.
- [[다형성]] — 서브타입 다형성과 오버로딩의 구분, OCP, instanceof와 패턴 매칭.
- [[인터페이스와 추상 클래스]] — 상태·다중 구현·접근 제어의 차이, Java 8·9 이후 인터페이스, 언제 무엇을.
- [[람다와 스트림]] — Stream API(≠ 스트림 처리), 도입 동기, 지연 연산과 파이프라인 융합, 부수효과 금지 규칙.
- [[함수형 프로그래밍]] — 순수 함수·불변성·일급 함수, Java가 강제하지 않는 것.

## 노트

- [[레퍼런스 카운팅과 마크 앤 스윕]] — 두 GC 계열 비교(순환 참조·멈춤·해제 시점), tracing과 RC는 쌍대, CPython·Swift·JVM·V8·Go의 실제 조합.
- [[객체 수명과 메모리 상한]] — Old가 찬다는 것의 의미(GC 후 바닥선 네 모양), 수명·상한 설계 원칙, 메모리 누수 안티패턴 9가지.
- [[Java 8에서 11로 가는 GC 관점의 이유]] — 「Parallel → G1이라 전환」 주장의 빈 곳 셋(G1은 8에도 있음·단일 스레드 Full GC, 인스턴스 분리의 다른 이유, G1도 멈춤), 8 → 11의 다른 이유, 지금은 17+.
- [[GC 튜닝 순서]] — 목표·기준선 → 코드 → 기본값+힙 → 컬렉터 선택 → 목표 하나(Young 고정 금지) → 로그로 확인된 증상별 G1 튜닝 표 → 재측정.
- [[가시성 문제는 지금도 생기나]] — 지금도 생긴다: JDK 25 재현(`volatile` 없음 → 안 멈춤, `-Xint` → 멈춤)으로 범인은 캐시가 아니라 JIT. j.u.c 도구가 happens-before를 만들어 덜 마주칠 뿐, 날것의 공유 변수에서 난다.
- [[원자성 문제가 나는 시나리오]] — 읽고-고치고-쓰기 · 확인 후 행동 · 여러 값 함께 바꾸기 · 64비트 쪼개짐. JDK 25 재현: `int++`·`volatile int++` 모두 절반가량 잃고, `containsKey`+`put`은 `ConcurrentHashMap`에서도 187/2000 이중 초기화.

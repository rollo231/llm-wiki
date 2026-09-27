# 인덱스

위키의 모든 페이지 목록. 페이지마다 `[[링크]]` 와 한 줄 요약을 단다. 인제스트하거나 노트를 남길 때마다 갱신하고, 질의할 때 가장 먼저 읽는다.

## 자료

AI 데이터 엔지니어링 강의. 진행 상태는 트래커 [[AI 데이터 엔지니어링 강의]]에서 본다.

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
- [[AI DE 강의 3-01 스키마 중심 설계와 RDBMS]] — Part 3 도입. 관계·키·제약, 트랜잭션과 ACID, 정규화의 목적은 업데이트 안정성, 스키마 중심 설계의 약점(변경 비용·비정형).
- [[AI DE 강의 3-02 RDBMS의 한계와 NoSQL]] — Scale-up·스키마 변경·분산 일관성 비용, NoSQL 네 타입, "NoSQL이면 확장이 자동인가"의 운영 현실(핫 파티션·CAP). ⚠️ wide-column을 열 기반 저장으로.
- [[AI DE 강의 3-03 시맨틱]] — 스키마는 형식, 시맨틱은 의미(해석의 계약). Entity·Attribute·Relationship·Context, 용어 사전에서 지식 그래프까지의 스펙트럼.
- [[AI DE 강의 3-04 그래프의 기본 개념]] — 노드·엣지·속성·레이블, path·hop·pattern, 방향·가중치·이종 그래프, 지식 그래프와 메타데이터 그래프, 그래프를 고려할 다섯 질문.
- [[AI DE 강의 3-05 Property Graph와 RDF]] — 두 그래프 모델의 기본 단위·스키마·질의 언어(Cypher vs SPARQL)와 선택 질문 여섯 개. ⚠️ RDFS를 검증 제약처럼.
- [[AI DE 강의 3-06 그래프의 실무 활용]] — 그래프가 가치를 내는 네 곳: 메타데이터·카탈로그, 계보와 영향도, 추천(cold-start), 검색과 Knowledge Graph.
- [[AI DE 강의 3-07 AI와 그래프]] — Graph as Data·Model·Retrieval, GNN, LLM과 GNN의 결합 3패턴(이름은 원 서베이와 같음), 그래프를 LLM 입력으로 넣는 네 방식, GraphRAG 예고.
- [[AI DE 강의 3-08 온톨로지와 RDFS·OWL]] — 온톨로지 = 공유된 개념과 관계의 명세, 구성 요소, RDF·RDFS·OWL의 역할, OWL은 과설계가 되기 쉽다. ⚠️ domain/range는 추론 규칙.
- [[AI DE 강의 3-09 온톨로지 모델링 원칙]] — 질문에서 출발해 클래스·속성·관계를 가르는 기준, granularity, 관계가 무거우면 개체로 승격, "테이블 = 클래스"는 실수.
- [[AI DE 강의 3-10 지식 그래프 파이프라인]] — 수집 → 정규화 → 식별자 → 매핑 → RDF 생성 → 검증 → 추론 → 서비스 → 증분 갱신. ⚠️ 단계 수가 7·10·8로 어긋남.
- [[AI DE 강의 3-11 SHACL 검증]] — data graph와 shapes graph, Node·Property Shape, Turtle, 고객·주문 예시(위키가 pyshacl로 실행). ⚠️ 설명의 "email 최대 1개"가 코드에 없음.
- [[AI DE 강의 3-12 RAG의 이해와 한계]] — RAG 원 논문, Retriever·Generator, 실무 RAG 분해, 네 한계(검색 단위, 검색-생성 정합성, Lost in the Middle, 고정 k). ⚠️ "구조화된 RAG"는 Modular RAG.
- [[AI DE 강의 3-13 GraphRAG 개념과 사례]] — Microsoft GraphRAG의 인덱싱·질의, 넓은 의미의 네 패턴, 사례(Neo4j·Bedrock), 후속 변형(auto-tuning·DRIFT·LazyGraphRAG). ⚠️ DRIFT 약자 틀림.
- [[AI DE 강의 3-14 그래프 DB의 특징]] — 관계를 계산하느냐 저장하느냐, traversal, index-free adjacency의 뜻과 한계, 그래프 DB의 트랜잭션, RDB와의 선택. ⚠️ 「실습」이 없음.
- [[AI DE 강의 3-15 그래프 DB 제품 비교]] — Neo4j·Neptune·ArangoDB·JanusGraph를 저장 철학·모델·언어·확장·운영 다섯 기준으로. ⚠️ 라이선스·릴리스 상태가 기준에 없음.

인프런 Java 면접 강의. 등급별 모범 답변이 붙은 면접 질문집이다. 트래커 [[인프런 Java 면접 강의]].

- [[Java 면접 2 JVM과 실행 원리]] — JVM 장단점, 실행 과정, JIT(판단 기준·코드 캐시·워밍업). ⚠️ 실행 5단계의 순서가 틀림.
- [[Java 면접 2 빈출 질문]] — Section 2 부록. 빈도 별점을 붙인 5문항: JVM 정의·구조, 클래스 로더, 로딩·링크·초기화, 메모리 영역. ⚠️ "가상 OS", 로더가 링크·초기화를 한다는 서술.
- [[Java 면접 3 GC]] — GC 알고리즘, Heap 세대, Root, STW, 컬렉터 종류, G1, OOM 대응. ⚠️ "Mark and Sweep" 단순화, 목록이 CMS·G1에서 멈춤.
- [[Java 면접 3 빈출 질문]] — Section 3 부록. 빈도 별점을 붙인 6문항: GC 정의·장단점, OOM 종류·차이, PermGen vs Metaspace, static의 GC. ⚠️ "아무도 안 가리키면 쓰레기", Metaspace는 "OS가 관리".
- [[Java 면접 4 동시성 이슈]] — 가시성·원자성, volatile·synchronized·CAS, 모니터, 스레드 풀. ⚠️ "volatile은 캐시 우회"는 오해.
- [[Java 면접 4 빈출 질문]] — Section 4 부록. 빈도 별점을 붙인 9문항: 불변 객체, 가시성만으로 충분한가, 싱글톤 LazyHolder, Thread-safe, 동기화·동시성 컬렉션, COW, ConcurrentHashMap. ⚠️ "Concurrent 컬렉션은 읽기에 락 없음", synchronized 싱글톤 비용.
- [[Java 면접 5 빈출 질문]] — Section 5 부록. 빈도 별점을 붙인 19문항(자료 번호 11~15 중복, 위키가 1~19로 다시 매김): 객체·클래스·인스턴스, 역할·책임·협력·메시지, 절차지향, 결합도·응집도, SOLID, static, 관심사 분리. ⚠️ 절차지향은 상태가 없다, 다형성 정의가 거꾸로, 「객체.메소드」
- [[Java 면접 5 객체지향 프로그래밍]] — 캡슐화, 상속 vs 조합, 다형성·instanceof, 인터페이스 vs 추상 클래스. ⚠️ 오버로딩·instanceof·private 메서드.
- [[Java 면접 6 람다와 스트림]] — 람다·스트림 도입 이유, 함수형 프로그래밍, 지연 연산. ⚠️ "순수 함수라 스레드 안전"은 과장.
- [[Java 면접 기타 빈출 질문 1 자바 기본]] — 「[기타]」 부록(대응 Section 없음, 위키가 44문항을 Q1~44로 매김)의 Q1~13: Java 버전, JDK·JRE, 동일성·동등성, equals·hashCode, main의 static, 기본형·참조형, 값 전달, 직렬화. ⚠️ hashCode = 「주소」·「같은 객체 확인」, main static은 JDK 25에서 낡음.
- [[Java 면접 기타 빈출 질문 2 문자열 예외 제네릭]] — 「[기타]」 부록 Q14~23: String pool, StringBuilder·StringBuffer, Exception·Error, checked·unchecked, finally, 제네릭. ⚠️ checked 정의에서 Error 누락, 예시 질문에 예시가 없음.
- [[Java 면접 기타 빈출 질문 3 어노테이션과 리플렉션]] — 「[기타]」 부록 Q24~27, 넷 중 셋이 ⭐⭐⭐. ⚠️ 어노테이션이 「기능을 주입」한다, 리플렉션은 「접근 제어자와 상관없이」.
- [[Java 면접 기타 빈출 질문 4 JCF]] — 「[기타]」 부록 Q28~44: 계층, List·Set·Map 구현체, ArrayList 확장, HashMap 동작과 최악 복잡도, Map이 Collection이 아닌 이유. ⚠️ HashMap 최악 O(N)은 JDK 8 트리화 이전, Set은 순서 없음.

## 엔티티

- [[AI 데이터 엔지니어링 강의]] — 패스트캠퍼스 강의. 인제스트 트래커와 Part 1~3 자료 평가·결함 표.
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
- [[Neo4j]] — native 그래프 DB, Cypher, ACID(기본 read-committed), 2025년 분산 아키텍처 Infinigraph.
- [[Amazon Neptune]] — AWS 관리형 그래프 DB. Property Graph(Gremlin·openCypher)와 RDF(SPARQL), 별도 엔진 Neptune Analytics.
- [[ArangoDB]] — 문서·키-값·그래프 멀티모델 DB와 AQL. 3.12부터 BSL, 2025년 회사명 Arango.
- [[JanusGraph]] — Cassandra·HBase 위에 얹는 분산 그래프 엔진, Gremlin. 마지막 릴리스 v1.1.0(2024-11).
- [[SHACL]] — RDF 그래프를 shapes graph로 검증하는 W3C 표준(2017). 그래프용 테스트 코드.
- [[Microsoft GraphRAG]] — Microsoft의 GraphRAG 논문과 오픈소스 구현. 커뮤니티 요약, auto-tuning, DRIFT, LazyGraphRAG.
- [[인프런 Java 면접 강의]] — 인프런 Java 면접 대비 강의. 트래커, Bronze·Silver·Gold 루브릭, 결함 표.
- [[JVM]] — HotSpot JVM. JVMS의 "abstract computing machine", 실행 파이프라인(정정된 순서), Kafka·Spark·Flink가 올라가는 런타임.

## 개념

- [[AI 데이터 엔지니어링]] — 소비자가 모델인 데이터 엔지니어링. Part 1~3 개념 지도.
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
- [[관계형 데이터베이스]] — 관계·키·제약, 트랜잭션과 ACID, 정규화, 조인의 표현력과 비용.
- [[NoSQL]] — 네 타입(키-값·문서·wide-column·그래프), CAP(정의 정정), 핫 파티션과 운영 현실. wide-column ≠ 열 기반.
- [[시맨틱 계층]] — 스키마가 형식이라면 시맨틱은 의미. 같은 KPI가 여러 개가 되는 이유, 용어 사전에서 지식 그래프까지.
- [[그래프 데이터 모델]] — Property Graph와 RDF, 노드·엣지·트리플, Cypher·SPARQL·Gremlin·GQL, 언제 무엇을.
- [[지식 그래프]] — 엔티티와 사실 관계의 그래프. Google Knowledge Graph, 메타데이터 그래프, 구축 파이프라인.
- [[온톨로지]] — 개념·관계·제약의 공식 명세, RDFS·OWL, domain/range는 추론 규칙(검증은 SHACL), 모델링 원칙.
- [[데이터 계약]] — 생산자와 소비자 사이의 명시적 약속. 스키마·의미·품질·SLA, 위키에 흩어진 계약 언급을 모은 허브.
- [[그래프 데이터베이스]] — 관계를 저장하고 traversal로 질의하는 DB. index-free adjacency, 트랜잭션, RDB와의 선택, 제품 지도.
- [[검색 증강 생성]] — RAG. 원 논문, Naive·Advanced·Modular, 네 한계. Part 5에서 청킹·하이브리드 검색·리랭킹 보강 예정.
- [[GraphRAG]] — 그래프를 retrieval에 넣는 패턴군. 로컬·글로벌 질문, 네 패턴, LLM과 그래프의 결합.
- [[JDK 개선 제안]] — JEP란 무엇인가(패치노트가 아닌 제안·설계서), 읽는 법, 릴리스 노트·JDK 이슈·JSR과의 차이.
- [[JIT 컴파일]] — 인터프리터 → C1 → C2 계층 컴파일(tier 0~4), 임계치(호출 + back-edge), 역최적화, Graal JIT, 코드 캐시, 워밍업과 AOT 대안.
- [[클래스 로딩]] — 로딩 → 링크(검증·준비·해석) → 초기화. 로더의 몫은 로딩뿐이고, 명세가 정하는 것은 초기화 시점, 초기화 락(JLS §12.4.2)으로 한 번만·스레드 안전하게, JDK 9 이후 내장 로더 3종과 부모 위임.
- [[JVM 메모리 구조]] — JVMS 런타임 데이터 영역 6개와 HotSpot 구현(Metaspace, static·intern 문자열은 힙, 코드 캐시, 합쳐진 스택), PermGen → Metaspace 두 단계(JDK 7·8), static 필드의 회수(클래스 언로드), 영역별 오류, 가상 스레드의 스택(힙, GC Root 아님).
- [[가비지 컬렉션]] — 도달 가능성, 세대 가설, 치우는 방식(복사·mark-compact·mark-sweep), GC Root와 remembered set, STW(safepoint·컴팩션·barrier), OOM 메시지별 대응(overhead limit은 Parallel, G1은 JDK 26부터)과 OOMKilled, 누수의 정의.
- [[가비지 컬렉터]] — Serial·Parallel·CMS(제거)·G1·ZGC·Shenandoah·Epsilon, 기본 GC 연표(JEP 248·523), 처리량 vs 지연.
- [[동시성 문제]] — 가시성·원자성, 캐시 불일치로 설명하면 틀리는 이유와 실제 원인(재배치·레지스터·store buffer), JMM happens-before, 스레드 안전의 정의(JCIP)와 "가시성만 풀면 되나".
- [[동기화 기법]] — volatile(DCL·64비트), synchronized(가시성·재진입, 바이트코드의 두 monitorexit, lightweight locking의 lock-stack, ObjectMonitor 필드, JDK 21→26 연표, 문제점 표), ReentrantLock 비교표, CAS(x86·ARM 명령, ABA, 여러 값은 불변 객체+AtomicReference)와 LongAdder, 문제별 선택표, 싱글톤 지연 초기화(synchronized·DCL·holder·enum, 초기화 락), 가상 스레드 pinning.
- [[스레드 풀]] — 작업 큐와 재사용, ThreadPoolExecutor의 늘리는 순서(core → 큐 → max, Tomcat은 반대), Blocking I/O 서버가 스레드를 수백 개 두는 이유(리틀의 법칙, Tomcat 기본값 표, 커넥션 풀 병목), 가상 스레드.
- [[불변 객체]] — 관찰 가능한 상태가 안 바뀌는 객체. 스레드 안전의 조건(final 필드 JLS §17.5, `this` 누출 금지, 방어적 복사), String의 `hash`, `List.of`·`record`의 강도, 쓰임.
- [[동시성 컬렉션]] — 락 하나(Vector·Hashtable·synchronizedXxx: 복합 연산·순회는 호출자 몫) → 버킷 락·CAS(ConcurrentHashMap JDK 8, JDK 7 Segment) → 스냅샷(CopyOnWriteArrayList). 클래스별 읽기 락 표, HashMap과 비교.
- [[캡슐화]] — 정보 은닉, 변경에 유연한 코드, getter/setter 대신 행동 메서드.
- [[객체지향 프로그래밍]] — 객체와 인스턴스(JLS §4.3.1), 역할·책임·협력·메시지(『오브젝트』 대조), 4대 특성, 절차지향과의 차이, static의 단점, 클린 코드.
- [[SOLID 원칙]] — 다섯 원칙의 원문(Martin 1996·2000, Liskov 1987)과 자료의 서술, SRP = 액터와 관심사 분리 사례, DIP의 「역전」, 이름의 역사.
- [[결합도와 응집도]] — 정의와 1974년 Structured Design, 캡슐화만으로 응집도가 오르지 않는 이유, 상속·SRP와의 연결.
- [[상속과 조합]] — is-a와 has-a, 상속의 결합도 문제, 조합을 선호하는 이유.
- [[다형성]] — 서브타입 다형성과 오버로딩의 구분, OCP, instanceof와 패턴 매칭.
- [[오버로딩과 오버라이딩]] — 컴파일 타임(정적 타입) vs 런타임(실제 객체) 결정, 오버라이딩 규칙(공변 반환·접근·예외), static·필드 숨김, 오버로딩 함정(`remove(int)`, `equals(Point)`). JDK 25 재현.
- [[인터페이스와 추상 클래스]] — 상태·다중 구현·접근 제어의 차이, Java 8·9 이후 인터페이스, 언제 무엇을.
- [[람다와 스트림]] — Stream API(≠ 스트림 처리), 도입 동기, 지연 연산과 파이프라인 융합, 부수효과 금지 규칙.
- [[함수형 프로그래밍]] — 순수 함수·불변성·일급 함수, Java가 강제하지 않는 것.
- [[equals와 hashCode]] — 동일성(==)과 동등성(equals), 둘을 함께 재정의하는 이유, equals·hashCode 계약, Object.hashCode는 주소도 고유값도 아니다(HotSpot 기본은 스레드별 xor-shift).
- [[Java 컬렉션 프레임워크]] — Iterable → Collection → List·Set·Queue·Deque, Sequenced 인터페이스(JDK 21), Map이 따로인 이유(설계 FAQ), 구현체 선택표, 레거시(Vector·Stack·Hashtable), Collection과 Collections.
- [[HashMap]] — hash() 섞기와 버킷 인덱스, 부하율 0.75와 2배 리사이즈, 체이닝과 JDK 8 트리화(JEP 180, 비교 불가 키는 여전히 O(n)), HashSet은 HashMap 위에 있다.
- [[Java 예외 처리]] — Throwable 계층, checked·unchecked(JLS §11.1.1, Error는 unchecked), throw·throws, finally가 실행되지 않는 경우, try-with-resources.

## 노트

- [[레퍼런스 카운팅과 마크 앤 스윕]] — 두 GC 계열 비교(순환 참조·멈춤·해제 시점), tracing과 RC는 쌍대, CPython·Swift·JVM·V8·Go의 실제 조합.
- [[객체 수명과 메모리 상한]] — Old가 찬다는 것의 의미(GC 후 바닥선 네 모양), 수명·상한 설계 원칙, 메모리 누수 안티패턴 9가지.
- [[Java 8에서 11로 가는 GC 관점의 이유]] — 「Parallel → G1이라 전환」 주장의 빈 곳 셋(G1은 8에도 있음·단일 스레드 Full GC, 인스턴스 분리의 다른 이유, G1도 멈춤), 8 → 11의 다른 이유, 지금은 17+.
- [[GC 튜닝 순서]] — 목표·기준선 → 코드 → 기본값+힙 → 컬렉터 선택 → 목표 하나(Young 고정 금지) → 로그로 확인된 증상별 G1 튜닝 표 → 재측정.
- [[가시성 문제는 지금도 생기나]] — 지금도 생긴다. JDK 25 재현(`volatile` 없음 → 안 멈춤, `-Xint` → 멈춤)에서 원인은 JIT였다. j.u.c 도구가 happens-before를 만들어 주므로 덜 마주칠 뿐이고, 도구 없이 공유 변수를 쓰면 난다.
- [[원자성 문제가 나는 시나리오]] — 읽고-고치고-쓰기 · 확인 후 행동 · 여러 값 함께 바꾸기 · 64비트 쪼개짐. JDK 25 재현: `int++`·`volatile int++` 모두 절반가량 잃고, `containsKey`+`put`은 `ConcurrentHashMap`에서도 187/2000 이중 초기화.
- [[데드락 재현과 해법]] — 반대 방향 이체로 JDK 25 재현(BLOCKED 둘, `findDeadlockedThreads`·`jstack` 출력), 네 조건, 락 순서 고정 vs `tryLock`+물러서기(livelock), DB 데드락과 비교. 클래스 초기화 데드락은 RUNNABLE이고 자동 탐지에 안 잡힌다.
- [[상속을 쓰는 이유]] — 상속의 단점은 확장을 고려하지 않은 구체 클래스를 경계 너머에서 상속할 때 생긴다. 위임 코드 비용, 확장용 설계(`AbstractList`·`BaseOperator`), 같은 팀 통제, 상태 공유, sealed. JDK 25 `CountingSet` 재현.

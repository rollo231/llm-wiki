---
type: source
title: AI DE 강의 1-16 AI 파이프라인 구축 사례
aliases: [AI DE 1-16]
tags: [AI-DE-강의, 사례]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/data-engineering/ai-de-course/part1/25. [Case Study] 성공적인 AI 데이터 파이프라인 구축 사례 분석 및 Part 1 정리.pdf"
---

# AI DE 강의 1-16 AI 파이프라인 구축 사례

[[AI 데이터 엔지니어링 강의]] Part 1의 마지막 강의. 빅테크 여섯 곳의 ML·데이터 플랫폼을 한 장씩 소개하고 데이터
품질 5대 기둥으로 끝난다. **서술(구성 요소)은 대체로 사실이지만 수치는 믿을 수 없다** — 아래 검증 표 참고.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 1 |
| 덱 제목 | 성공적인 AI 데이터 파이프라인 구축 사례 (파일명: [Case Study] 성공적인 AI 데이터 파이프라인 구축 사례 분석 및 Part 1 정리) |
| 원본 파일 | `part1/25. [Case Study] 성공적인 AI 데이터 파이프라인 구축 사례 분석 및 Part 1 정리.pdf` (8p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-04-21. 다른 덱과 달리 macOS Quartz로 만든 PDF다 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명·본문 모두에 없다 |

## 요약

### 배경 (p2)

현대 선도 기업은 모델 개발을 넘어 지속 운영·확장 가능한 **"AI 팩토리"**를 지향한다. 수집·정제·피처 생성·학습·
배포·모니터링을 자동화·표준화한 파이프라인이 핵심이다. 병목은 데이터 준비 시간이고(→ 피처 스토어로 로직 재사용),
리스크는 학습-서빙 스큐다(→ 스키마 검증으로 실시간 차단).

### 사례 (p3–7)

| 회사·플랫폼 | 덱이 드는 구성 요소 | Part 1 개념 |
|---|---|---|
| Uber Michelangelo | Palette 피처 스토어(오프라인·온라인 동일 추출 로직), 스키마 검증(타입 불일치·분포 이동·카디널리티 변화 감지), 섀도우 배포, 경량 스코어링 | [[피처 스토어]] · [[학습-서빙 스큐]] |
| Netflix | Keystone(Kafka + Flink, 선언적 화해 프로토콜로 희망 상태를 AWS RDS에 저장하고 불일치를 자동 복구), 중앙 집중 ETL → 도메인 중심 데이터 메시, 스튜디오 데이터 이동(CDC 소스 커넥터 → GraphQL 보강 → 스키마 진화 관리(호환성 위반 시 자동 중단) → Iceberg 싱크) | [[Apache Kafka]] · [[Apache Flink]] · [[변경 데이터 캡처]] · [[스키마 진화]] |
| Tesla Data Engine | 섀도우 모드(신규 알고리즘이 백그라운드에서 실제 운전자 조작과 자기 예측을 비교) → 엣지 케이스 선별·수집 → 오토 레이블링 → Dojo 슈퍼컴퓨터로 비디오 학습 → OTA 배포의 데이터 플라이휠 | [[데이터 드리프트]] |
| Meta | FBLearner Flow(`@workflow` 데코레이터, 데이터 의존성으로 DAG를 컴파일해 퓨처 객체 반환, 의존성 없는 연산자 자동 병렬화) + AI 에이전트 스웜(50개 이상 전문 에이전트로 파일을 분석해 컨텍스트 파일 생성, 부족 지식 매핑) | — |
| Google TFX | StatisticsGen·SchemaGen(통계 분석·스키마 추론), ExampleValidator(학습 데이터와 서빙 로그 간 스큐 감지), Beam 기반 서버리스 확장 | [[학습-서빙 스큐]] |
| Airbnb Bighead | Zipline(온라인·오프라인 피처 추출 로직 일치), Deepthought(실시간 추론), ML Automator(학습 자동화·실험 관리) | [[피처 스토어]] |

### 데이터 품질 5대 기둥 (p8)

정확성(실제 세계와 일치하는가) · 완전성(핵심 정보가 누락되지 않았나) · 일관성(소스·시간대별 형식이 통일됐나) ·
신선도(실시간 의사결정을 지원할 만큼 최신인가) · 공정성(특정 집단에 대한 편향이 없나). 각 기둥에 지표 배지
(KS 통계값 0.05, 누락률 0.1%, 일관성 98.5%, 지연 1초 미만, 편향도 0.02 등)와 실시간 검증 메커니즘이 붙어 있다.

## 핵심

- 여섯 사례가 공유하는 뼈대가 **Part 1의 개념 목록과 그대로 겹친다** — 피처 스토어로 스큐 제거(Palette·Zipline·
  TFX ExampleValidator), 스키마 검증 게이트, 섀도우 배포, Kafka + Flink 스트리밍, CDC와 스키마 진화. 이 덱은 새
  개념보다 **개념에 실제 이름을 붙이는 매핑표**로 읽는 것이 맞다.
- 5대 기둥은 [[AI DE 강의 1-14 데이터 SLA와 모니터링]]의 3대 지표에 **일관성·공정성**을 더한 분류다. → [[데이터 SLA]]

## 주의·결함 — 수치 검증 (2026-09-14)

공식 문서·원 논문·회사 엔지니어링 블로그와 대조했다. **같은 숫자가 회사만 바꿔 반복된다** — 70%는 네 곳(배경·
Uber·Meta·Airbnb), 2%는 세 곳(배경·Uber·TFX), "수주 배포"는 세 곳(배경·Uber·TFX), 2PB/주는 두 곳(Netflix·Tesla).

| 덱의 주장 | 검증 결과 | 근거 |
|---|---|---|
| Uber: 앱 설치율 2% 증가 | ⚠️ **다른 회사의 수치.** 2%는 Google TFX 논문의 Google Play 결과다(학습-서빙 스큐를 제거한 뒤 A/B 테스트). Uber Michelangelo 2017 글에는 없다 | Baylor et al., "TFX", KDD 2017 — "a 2% increase in app installs resulting from improved data and model analysis" https://systems.cs.columbia.edu/ds2-class/papers/baylor-tfx.pdf · Uber 2017-09-05 https://www.uber.com/blog/michelangelo-machine-learning-platform/ |
| TFX: 앱 설치율 2%, 배포 수개월 → 수주 | ✅ 맞다 | TFX 논문 초록 — "reduce the time to production from the order of months to weeks" |
| Uber·Meta·Airbnb: 개발 시간 70% 단축 | ⚠️ **찾지 못함.** Uber 2017 글과 FBLearner Flow 2016 글에 70%가 없다. Airbnb 자료는 "모델 구축에 평균 8~12주"(2016년 4분기)만 확인된다 | Meta 2016-05-09 https://engineering.fb.com/2016/05/09/core-infra/introducing-fblearner-flow-facebook-s-ai-backbone/ · Airbnb Spark Summit 2018 발표 https://www.slideshare.net/slideshow/bighead-airbnbs-endtoend-machine-learning-platform-with-krishna-puttaswamy-and-andrew-hoh/102402767 |
| Meta: 시스템 가용성 99.9% | ⚠️ 찾지 못함 | FBLearner Flow 2016 글 |
| Uber: Palette 피처 스토어 | ✅ 이름은 맞다. 다만 2017 Michelangelo 글은 "Feature Store"라고만 부르고 Palette라는 이름은 2024년 글에 나온다 | Uber 2024-01-18 https://www.uber.com/us/en/blog/palette-meta-store-journey/ |
| Airbnb: Zipline·Deepthought·ML Automator | ✅ 맞다(원 표기는 "Deep Thought") | Airbnb Spark Summit 2018 발표 |
| Netflix: 선언적 화해 프로토콜, 희망 상태를 AWS RDS에 저장 | ✅ 맞다 (Netflix TechBlog 원문은 접근이 막혀 InfoQ 보도로 확인) | InfoQ 2018-09-30 https://www.infoq.com/news/2018/09/Netflix-Keystone-Real-Time-Proc |
| Netflix: 일일 5,000억+ 이벤트, 1.3PB | ❓ 원문 미확인. 2015~16년 시기의 수치로 보인다 — Netflix 엔지니어의 2015-03 발표는 "하루 4,000억 이벤트", 2018 InfoQ는 2016년 기준 "하루 7,000억 메시지 이상"을 인용한다. 2026년 자료에 현재 수치처럼 쓰였다 | Netflix Kafka 발표 https://www.slideshare.net/slideshow/netflix-kafka/46275472 · InfoQ 2018 |
| Tesla: 주간 2PB | ❓ Tesla 출처를 찾지 못함. Netflix 스튜디오 슬라이드에도 같은 수치가 있다 | — |
| Tesla: Dojo 슈퍼컴퓨터 학습 | ⚠️ **현재 상태와 다르다.** Tesla는 2025-08 Dojo 팀을 해체했고 Musk가 "진화의 막다른 길"이라며 중단을 확인했다. 2026-01에는 Musk가 "AI7/Dojo3는 우주 기반 AI 연산용"이라며 재개를 언급했다. 덱(2026-04)은 Dojo를 현행 학습 인프라로 그린다 | TechCrunch 2025-08-11 https://techcrunch.com/2025/08/11/elon-musk-confirms-shutdown-of-tesla-dojo-an-evolutionary-dead-end/ · TechCrunch 2026-01-20 https://techcrunch.com/2026/01/20/elon-musk-says-teslas-restarted-dojo3-will-be-for-space-based-ai-compute |
| Meta: 에이전트 50개+, 파일 4,100개+, 컨텍스트 파일 59개 | ✅ 실재한다. 다만 2016년 FBLearner Flow와 **별개인 2026년 작업**인데 한 슬라이드에 섞여 있다. 원문도 저장소 수를 네 개/세 개로 다르게 쓴다. 덱 PDF 생성일(2026-04-21)은 이 글보다 뒤다 | Meta Engineering 2026-04-06 https://engineering.fb.com/2026/04/06/developer-tools/how-meta-used-ai-to-map-tribal-knowledge-in-large-scale-data-pipelines/ |

그 밖에:

- **파일명의 "및 Part 1 정리"와 달리 정리 절이 없다.** 덱은 5대 기둥으로 끝난다.
- 5대 기둥의 지표 배지(KS 0.05, 누락률 0.1%, 공정성 99.5% 등)는 근거 없는 장식이다.
- "수천 동시 사용자", "수백만 월간 실험", "지수적 성능 향상" 같은 배지도 출처가 없다.

## 관련

- 개념: [[피처 스토어]] · [[학습-서빙 스큐]] · [[데이터 SLA]]
- 이전 강의: [[AI DE 강의 1-15 데이터 거버넌스와 카탈로그]]
- 트래커: [[AI 데이터 엔지니어링 강의]]

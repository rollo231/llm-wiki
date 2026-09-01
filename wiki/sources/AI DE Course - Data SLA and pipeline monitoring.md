---
type: source
title: AI DE Course - Data SLA and pipeline monitoring
area: [data-engineering]
aliases: [데이터 엔지니어의 약속, SLA 지표와 파이프라인 모니터링 강의]
tags: [data-engineering, course, fast-campus, sla, observability, data-quality, monitoring]
created: 2026-08-01
updated: 2026-09-01
sources: ["raw/data-engineering/ai-de-course/part1/19. 데이터 엔지니어의 약속 SLA(서비스 수준 계약) 지표와 파이프라인 모니터링 1.pdf", "raw/data-engineering/ai-de-course/part1/20. 데이터 엔지니어의 약속 SLA(서비스 수준 계약) 지표와 파이프라인 모니터링 2.pdf", "raw/data-engineering/ai-de-course/part1/21. 데이터 엔지니어의 약속 SLA(서비스 수준 계약) 지표와 파이프라인 모니터링 3.pdf"]
---

# AI DE Course - Data SLA and pipeline monitoring

**출처:** 패스트캠퍼스(Fast Campus) 데이터 엔지니어링 강의 · **Part 1 후반부**
"데이터 엔지니어의 약속: SLA(서비스 수준 계약) 지표와 파이프라인 모니터링 (1)(2)(3)". 원본(로컬):
`raw/data-engineering/ai-de-course/part1/` 의 `19.`~`21.` (6p × 3 = 18p).
강의 홈: [[AI Data Engineering (Fast Campus course)]].
(챕터 번호는 추론 — 앞 챕터 페이지의 주의 참조.)

**[[Data Engineering]] MOC의 열린 질문 "데이터 품질·관측성의 실제 도입"에 처음 들어온 근거다.**
개념 정리는 [[Data SLA and observability]]로 옮겼다.

## 3부 구성

1. **문제 정의** — 침묵의 실패, 데이터 SLA = 신뢰의 계약, 품질 붕괴의 나비효과
2. **지표** — 신선도 · 완전성 · 정확성/유효성
3. **시스템** — 데이터 관측성, 경고 피로 방지, RCA, 서킷 브레이커

## (1) 침묵의 실패 — 이 덱의 출발점

전통 IT SLA는 **99.9% uptime**을 약속한다. 그런데 데이터 파이프라인에서는:

| 시스템의 주장 (System Logs) | 실제 데이터 (Reality) |
|---|---|
| Exit Code: 0 (정상 종료) | **Row Count: 0건** (예상 100만건) |
| 에러 로그 없음 | 결제 금액: Null / 음수 |
| 스케줄러 상태: **Green** | 데이터 가치: 쓰레기(Garbage) |

> **"시스템 로그에는 에러 한 줄 남기지 않는 가장 무서운 적."**
> **"기존 IT 모니터링으로는 절대 잡을 수 없습니다."**
> *"서버만 켜져 있으면 만사형통!"* 이라는 전제가 깨지는 지점.

앞 챕터의 **'침묵의 살인자'**(skew)와 정확히 같은 성질이다 —
에러 0건인데 결과만 망가진다. → [[AI DE Course - Data drift and training-serving skew]]

### 데이터 SLA — 신뢰의 계약

시스템이 켜져 있음의 보장이 아니라, **데이터 생산자(엔지니어)와 소비자(AI 모델·DS) 간에
데이터의 시간·완전성·정확성을 보장하는 상호 합의된 계약.**

강의가 문서 형태로 제시하는 명세 예시 (`DATA SLA SPEC · DOC-ID: #2026-AI-01`):

| 항목 | 약속 |
|---|---|
| Timeliness (시간) | 매일 아침 08:00까지 적재 완료 |
| Completeness (완전성) | 누락 없음 (Source 대비 100%) |
| Accuracy (정확성) | 결제금액 Null / 음수 0건 |

**위반 시: 즉시 알람 & 롤백(Rollback).**
운영 프로세스: `실시간 모니터링 → 위반 감지·알림 → 모델 학습 중단/에스컬레이션`.

관계 설정: Producer = 데이터 엔지니어 *"품질을 책임지고 배달합니다"* /
Consumer = AI 모델·DS *"믿을 수 있는 데이터로 학습합니다"*.

### 나비효과 5단계

```
1. 데이터 누락        2. 학습 오염          3. 추천 왜곡        4. 고객 이탈        5. 비즈니스 손실
VIP 구매 데이터    →  잘못된 데이터로    →  엉뚱한 상품 노출  →  실망한 VIP 고객  →  매출 & ROI 폭락
수집 실패             재학습                (싸구려 상품)        앱 삭제·이탈
"엔지니어가          "VIP 패턴            "알고리즘은         "신뢰도            "수천만 원의
 모르고 지나침"        인식 실패"            죄가 없다"          급격 하락"          금전적 피해"
```

> **핵심 교훈: AI의 성능은 알고리즘의 우수성보다 입력되는 데이터의 신뢰성에 전적으로 의존한다.
> 데이터 SLA는 이 재앙을 막는 최전선의 방어벽이다.**

"알고리즘은 죄가 없다"는 문장이 이 코스의 관점을 요약한다.

## (2) 3대 지표 — 품질의 삼각편대

| | 신선도 (Time) | 완전성 (Quantity) | 정확성 (Quality) |
|---|---|---|---|
| 묻는 것 | "제시간에 도착했는가?" | "100% 다 들어왔는가?" | "값이 상식적인가?" |
| 검증 | `Latency = Now() - Event_Timestamp` | `assert Source.count() == Target.count()` | 스키마·타입·도메인 룰·범위 체크 |

### 신선도

- **평균값보다 p95·p99 같은 꼬리(tail) 지연을 중점 관리한다.**
- 처리 방식별 SLA 예시: 배치는 "D-1 로그를 매일 08:00까지, 08:10 도착 시 위반(모델 학습 지연)" /
  스트리밍은 "사용자 클릭 후 3초 이내 DB 반영, 기준은 **p95 latency**".
- 임계값에 호출 조건을 박는다: `CRITICAL 8시 30분 초과 시 엔지니어 호출`.
- 비즈니스 영향: AI 모델 성능 저하(최신 트렌드 반영 불가, 오래된 정보로 학습) ·
  매출 기회 손실(추천 타이밍, 마케팅 적중률).
- **"아무리 완벽한 데이터도 늦게 도착하면 가치가 0이 된다."**

### 완전성

- **Volume Check**(소스↔타겟 row count 대사·reconciliation) + **Uniqueness Check**(PK 중복).
- **조용한 증발(Silent Loss)** — 네트워크 오류나 메모리 부족으로 100만 건이 90만 건이 되는데
  **로그가 없다.**
- **위험은 양이 아니라 편향이다** — 특정 시간대나 사용자군(예: 20대) 데이터가 통째로 누락되면
  AI는 편향된 잘못된 지식을 진실로 학습한다.
- 금융·결제는 **Zero Tolerance**(단 1건 오차도 불가). 탐지 시 **Backfill 자동 트리거**,
  **MTTR 30분 이내**.

### 정확성·유효성

검증 규칙 예시 4종:

```
1. Schema Check: col_count == 15
2. Type Check:   price is Integer
3. Domain Rule:  email contains '@'
4. Range Check:  0 < age < 120
```

- 목표 **유효성 pass rate 99.9% 이상**.
- 대표 오류: **Logic Error**(나이 -5살, 200살 → 잘못된 분포 학습) /
  **Missing Value**(필수 User_ID·결제금액 Null → `NullPointerException`으로 중단).
- 대응은 **격리(Quarantine)**: `실패 레코드 격리(Main DB 오염 방지) → 담당자 알림(Slack/Email) →
  자동 정정 또는 재처리`.

### 엔지니어 체크리스트 (강의 제시)

- 모든 주요 파이프라인에 **데드라인이 명문화**되었는가?
- 소스와 타깃 간 **Row Count 자동 대사** 로직이 도는가?
- 배포 전 **스키마·도메인 규칙 테스트가 CI/CD에 포함**되었는가?

## (3) 시스템으로 지키기

### 데이터 관측성

*"매일 아침 수동으로 확인할 순 없잖아요?"* — 수백~수천 개 파이프라인과 TB급 데이터.

| 수동 확인의 한계 | 데이터 관측성 |
|---|---|
| **물리적 검증 불가** | **자동 수집·분석** — 볼륨·신선도·스키마 변경·값 분포를 24시간 감시 |
| **골든타임 상실** — 뒤늦게 인지 | **ML 기반 이상 탐지** — 과거 정상 패턴을 학습해 미세한 징후를 선제 포착 |
| **휴먼 에러 위험** — 피로 누적 | **선제적 방어** — 문제가 하류로 전파되기 전에 차단 |

### 경고 피로(Alert Fatigue) 방지

- **비즈니스 임팩트 필터링** — 모든 오류가 응급상황은 아니다. 실제 타격을 주는 핵심 SLA 위반만 알람.
- **동적 임계치(Dynamic Threshold)** — 고정값 대신 시간대별 트래픽·계절성 반영.
- **채널 차별화** — 경미한 이슈는 대시보드 로그로, 심각한 장애만 **on-call 전화**로.

### RCA 프로세스

`감지 → 격리 → 완화 → 원인 규명 → 복구` 순서로 매뉴얼에 따라.

- **투명한 커뮤니케이션** — 소비 팀에게 "현재 인지 중이며 복구 예정"을 즉시 알리는 것이 신뢰 유지의
  첫걸음.
- **CAPA** — 단순 수정을 넘어 구조적 취약점을 찾아 재발 방지 대책 수립.

### 서킷 브레이커 — 방어적 엔지니어링

> **철학: "멈춤이 최선의 품질."**
> 오염된 데이터가 AI 모델을 망치게 두느니 차라리 파이프라인을 멈추고 안전 모드(fail-safe)로
> 전환한다 — 예: **어제의 데이터를 대신 사용.**

- **설치 포인트** — 데이터가 변형·이동하는 주요 단계(stage) 사이마다 (`Source → Gate → Model`).
- **동작** — 사전 정의된 규칙 위반 시 스위치를 내려 하류 전파를 막는다.
  예: `Null 1% → 50% 급증 시`.
- **"망가진 데이터를 넣어서 모델을 망칠 바에는, 차라리 멈추는 것이 낫다."**

## 결론

> **"SLA는 종이 위의 약속이 아닙니다. 시스템으로 지켜질 때 비로소 '진짜 약속'이 됩니다."**

## 기존 페이지와의 대조

- **새 영역** — 기존 위키에 데이터 품질·관측성 페이지가 없었다. [[Data catalog and semantic layer]]가
  거버넌스를 "도구가 거들 뿐 해결하지 않고 본질은 사람과 프로세스"라고 정리했는데, 이 덱은
  **그 프로세스의 구체적 모습**(SLA 명세·알람 정책·RCA·서킷 브레이커)을 제시한다.
- **도구는 없다** — Great Expectations·dbt tests·Monte Carlo·Bigeye 같은 실제 제품 이름이 이 덱에
  전혀 나오지 않는다. MOC의 열린 질문 중 **"수동 정의 vs 자동 이상 탐지"의 갈림은 여전히 미해결**이다
  (강의는 "ML 기반 이상 탐지"를 지향점으로 말하지만 제품을 지목하지 않는다).

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[Data SLA and observability]] (상세), [[Data drift and training-serving skew]],
  [[Latency and throughput]] (p95·p99), [[Data catalog and semantic layer]] (lineage·RCA)
- 앞 챕터: [[AI DE Course - Data drift and training-serving skew]]
- 이어지는 챕터: [[AI DE Course - Data governance and catalog]]

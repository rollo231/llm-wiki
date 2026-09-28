---
type: source
title: AI DE 강의 4-16 모니터링 대시보드와 알람
aliases: [AI DE 4-16]
tags: [AI-DE-강의, 운영, 모니터링]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/02. Ch5. 시스템 운영 및 최적화.pdf"
---

# AI DE 강의 4-16 모니터링 대시보드와 알람

[[AI 데이터 엔지니어링 강의]] Part 4 Ch5의 두 번째 소단원이다. 모니터링을 지표 수집이 아니라 운영 판단 구조로 다시 정의하고, AI 시스템의 관측 데이터(metrics·logs·traces·events, label 차원, 5계층)를 설계한 뒤, 대시보드 다섯 종과 알람(증상과 원인, 좋은 알람의 구성, 심각도, 알람 피로)을 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch5. 시스템 운영 및 최적화: 2. 실시간 모니터링 대시보드 및 알람 구성 |
| 원본 파일 | `part4/02. Ch5. 시스템 운영 및 최적화.pdf` p22–47 (26p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-06-05 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch5`, 소단원 번호 `2`는 표지 슬라이드 |

## 요약

### 01. 모니터링의 목적 재정의 (p24–27)

- 모니터링은 지표 수집이 아니라 운영 판단 구조다(p24). 관측(Observe)은 골든 시그널(Latency, Traffic, Error, Saturation)로 현재 상태를 파악하고, 판단(Orient)은 SLA를 벗어났는지·단순 스파이크인지·구조적 결함인지를 분석하고, 대응(Act)은 자동 복구(Scale-out, Rollback)나 운영자 개입으로 정상 상태로 되돌린다.
- 대시보드 설계 순서는 사용자 영향 확인 → 영향 범위 확인 → 원인 후보 좁히기 → 첫 대응 결정 → 사후 분석 근거 확보다(p25).
- 일반 웹 서비스가 요청 수·지연·에러율·서버 자원·배포 상태를 본다면, AI 서비스는 여기에 모델 버전, 피처 버전, 데이터 신선도, 입력 분포 변화, 예측 점수 분포, 정답 label 도착 지연, GPU 사용률과 대기열, batch inference 완료 시각, 재학습 후보 데이터 생성 상태를 더 본다(p26).
- 대시보드는 분석 가능한 맥락을 주고(넓게 보여 주고, 영향 범위와 지표 간 관계를 보고, 원인 후보를 좁히고, 배포 전후를 비교), 알람은 행동 가능한 조건만 고른다(즉시 행동이 필요한 상황, SLO 위반 가능성, 사용자 영향)(p27).

### 02. AI 시스템 관측 데이터 설계 (p28–31)

- 관측 데이터는 네 종류다(p28–29). Metrics는 상태를 수치로 측정해 문제가 발생했는지를, Logs는 개별 사건의 상세 기록으로 어떤 요청에서 문제가 났는지를, Traces는 요청 흐름의 단계별 시간으로 어느 단계에서 시간이 걸렸는지를, Events는 배포·모델 교체·autoscaling·GPU node 생성 같은 시스템 변화 기록으로 문제 직전에 무엇이 바뀌었는지를 알려 준다.
- 지표에는 구분 기준(label)이 반드시 있어야 한다(p30). service, endpoint, model_name, model_version, feature_version, dataset_version, pipeline_name, batch_id, user_segment, gpu_type, gpu_node 등이다. 전체 평균은 정상인데 model_version=v3만 느리거나, 신규 사용자 segment에서만 오류가 늘거나, L4 node pool에서만 pending pod가 늘거나, 특정 pipeline_name만 freshness가 지연되는 경우를 잡기 위해서다.
- 지표는 다섯 계층으로 모은다(p31). 서비스(요청 수·latency·error rate·timeout), 데이터(freshness·row count·schema error·missing feature ratio), 모델(score distribution·drift·model_version별 품질), 인프라(pod restart·queue length·GPU utilization·GPU memory), 비용(GPU idle cost·cost per inference·batch run cost)이다.

### 03. 대시보드 설계 (p32–41)

다섯 종류의 대시보드를 질문 목록으로 정의한다.

| 대시보드 | 목표 | 질문·지표 | 쪽 |
|---|---|---|---|
| Overview | 1분 안에 장애 여부 판단 | 지금 장애인가, 어느 서비스가 영향을 받는가, SLO가 깨지고 있는가, 어느 drill-down으로 갈까. 정상/주의/장애 구분, 세부 그래프 최소화, 최근 배포·스케일링 이벤트 표시 | p32 |
| Online Inference | 사용자가 느린지 확인 | 어느 endpoint·model_version에서 느린가, 지연은 feature lookup·queueing·inference 중 어디서 나는가, 트래픽 때문인가 배포 때문인가. p50/p95/p99, queueing delay, 단계별 latency, model_version별 latency·error rate | p34 |
| Data Pipeline | 모델 입력이 정상인지 확인 | feature table이 제시간에 갱신됐나, batch inference 결과가 약속 시간 전에 생성됐나, row count·null ratio·schema가 평소와 다른가, label join이 지연되나. 성공 여부만 보지 말고 성공했더라도 양과 품질을 본다 | p36 |
| Model Quality | 모델이 여전히 잘 작동하는지 확인 | 점수 분포 변화, 사용자군별 성능, 새 버전과 이전 버전 비교, prediction-label 관계, drift. label이 늦게 오면 품질 지표도 늦게 갱신되므로 prediction_time과 label_event_time을 분리해서 본다 | p38 |
| GPU / Capacity | 병목과 낭비를 동시에 확인 | GPU 부족으로 요청이 밀리는가, GPU가 많은데 놀고 있는가, 누가 점유하는가, memory 부족, MIG slice 활용, node provisioning 실패. 사용률 × queue × latency 조합 해석 | p40 |

- p33·p35·p39·p41은 텍스트 없이 이미지만 있는 슬라이드다. 어두운 배경의 Grafana풍 대시보드 목업으로, 본문에서 패널을 설명하지 않는다.

### 04. 알람 설계 (p42–47)

- 알람은 증상에서 시작하고 원인은 대시보드로 좁힌다(p42). 증상 알람은 사용자 영향이나 SLO 위반과 직접 연결된다(p99 latency SLO 초과, error rate 급증, batch inference deadline miss, feature freshness SLO 위반, prediction table 미생성). 원인 알람은 장애를 만들 수 있는 내부 상태다(GPU memory 95% 이상, GPU pod pending 증가, feature pipeline 실패, model server pod restart, schema validation failure, Karpenter provisioning 실패).
- 좋은 알람은 어떤 SLO가 위험한지, 어떤 서비스·모델 버전인지, 얼마나 지속됐는지, 사용자 영향, 먼저 볼 대시보드, 담당자, 첫 대응을 담는다(p43). 예시는 `[SEV2] recommender-api p99 latency SLO risk`에 service, model_version=v42, p99_latency=1.8s, threshold=1.0s, duration=12m, request_rate=normal, dashboard, first_action(check queueing delay and recent model rollout), owner를 단다. 나쁜 알람은 「GPU high」「CPU high」「Latency high」「Pipeline failed」다(p44).
- 심각도는 얼마나 빨리 사람이 행동해야 하는가로 나눈다(p45). P1은 핵심 서비스 전체 영향·SLA 위반으로 즉시 호출(서비스 DB·API 장애), P2는 일부 모델·세그먼트·지역 영향으로 빠른 대응(새 추천 모델 V3의 CTR이 기존 대비 20% 하락), P3는 장기 추세 악화·capacity 부족·비용 증가로 업무 시간 내 처리(Feature Store 유저 로그의 Null 비율이 0.1%에서 2%로 상승)다.
- 알람 피로의 원인은 일시적 spike에도 울림, 원인 지표를 모두 page로 연결, 같은 장애의 중복 알람, 담당자 없는 알람, 대응 방법 없는 알람, SLO와 무관한 threshold다(p46). 개선책은 지속 시간 조건, 최소 트래픽 조건, 서비스·모델 버전 단위 grouping, 배포 시간대와 maintenance window 반영, page/ticket/info 구분, 알람마다 runbook 연결, 장애 뒤 알람 품질 리뷰다(p47). 예로 「GPU utilization > 90%」 대신 「p99 latency SLO 위험 AND request queue length 증가 AND 10분 이상 지속 AND request rate가 최소 기준 이상」을 든다.

## 핵심

- 알람은 증상에 걸고 원인은 대시보드로 좁힌다는 원칙(p42)이 이 소단원의 뼈대다. Google SRE 책의 원칙과 같다. 전문은 [[AI 시스템 모니터링]]에 모았다.
- label 차원 설계(p30)가 가장 실무적이다. AI 시스템의 장애는 대개 전체 평균이 아니라 한 모델 버전, 한 세그먼트, 한 노드 풀에서 나므로, 차원 없는 지표로는 보이지 않는다. p3([[AI DE 강의 4-15 AI 시스템 지표와 SLA]])의 실패 유형들이 바로 이런 부분 실패다. 두 소단원을 잇는 것은 위키의 관찰이다.
- Data Pipeline 대시보드의 "성공했더라도 데이터 양과 품질이 정상인지 확인"(p36)은 Part 1의 침묵의 실패([[데이터 SLA]])와 같은 경고다.
- Model Quality 대시보드의 prediction_time과 label_event_time 분리(p38)는 라벨 지연이 품질 지표를 늦춘다는 점을 운영 설계로 옮긴 것이다([[데이터 드리프트]]).
- 알람 피로 대책(p46–47)은 Part 1의 경고 피로 방지([[데이터 관측성]])를 조건식 수준으로 구체화한다.

## 주의·결함

- ⚠️ p24의 Observe → Orient → Act는 Boyd의 OODA 루프(Observe-Orient-Decide-Act)에서 Decide가 빠진 모양이다. 강의는 OODA라는 이름을 쓰지 않아, 의도한 세 단계 틀인지 누락인지 알 수 없다. 강의의 판단(Orient)이 사실상 분석과 결정을 함께 맡는다. 이 대조는 위키의 것이다.
- ✅ 네 골든 시그널(p24)은 SRE 책과 같다("The four golden signals of monitoring are latency, traffic, errors, and saturation." https://sre.google/sre-book/monitoring-distributed-systems/ , 2026-09-28 확인).
- ✅ 증상 중심 알람(p42)도 SRE 책과 맞는다. 책은 원인 쪽은 아주 확실하고 임박한 것만 걱정하라고 한다("it’s better to spend much more effort on catching symptoms than causes; when it comes to causes, only worry about very definite, very imminent causes." 같은 URL, 2026-09-28 확인). 강의의 원인 알람 예시(GPU memory 95% 이상 등)를 page로 걸지, ticket으로 둘지는 p47의 page/ticket/info 구분과 함께 읽어야 한다.
- p33·p35·p39·p41의 대시보드 이미지는 출처 표기가 없고 본문과 연결되지 않는다. 그림 속 수치는 예시로만 본다.
- p36과 p37은 같은 슬라이드다.
- p43의 v42, p45의 CTR 20% 하락·Null 0.1% → 2% 같은 수치는 설명용 가상 예시다.

## 관련

- 개념: [[AI 시스템 모니터링]] · [[서비스 수준 목표]] · [[데이터 관측성]] · [[데이터 SLA]] · [[데이터 드리프트]] · [[GPU 할당과 스케줄링]]
- 이전 강의: [[AI DE 강의 4-15 AI 시스템 지표와 SLA]]
- 다음 강의: [[AI DE 강의 4-17 병목 파악과 트러블슈팅]]

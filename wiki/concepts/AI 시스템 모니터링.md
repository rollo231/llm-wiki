---
type: concept
title: AI 시스템 모니터링
aliases: [AI system monitoring, ML 모니터링, 골든 시그널, Golden signals, Four golden signals, 증상 알람, 원인 알람, 알람 설계, Alerting, MELT]
tags: [운영, 모니터링, SRE]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 4-15 AI 시스템 지표와 SLA]]"
  - "[[AI DE 강의 4-16 모니터링 대시보드와 알람]]"
  - "[[AI DE 강의 4-17 병목 파악과 트러블슈팅]]"
---

# AI 시스템 모니터링

모델을 서빙하고 학습 데이터를 만드는 시스템 전체를 관측해, [[서비스 수준 목표]]가 깨지기 전에 알아채고 원인을 좁혀 대응하는 운영 체계다. [[AI DE 강의 4-16 모니터링 대시보드와 알람]]은 모니터링을 지표 수집이 아니라 운영 판단 구조로 정의한다. 데이터 파이프라인 쪽의 감시는 [[데이터 관측성]]이 전문이고, 이 페이지는 서비스·모델·인프라·비용까지 포함한 AI 시스템 전체를 다룬다.

## 무엇이 다른가

일반 웹 서비스가 요청 수·응답 지연·에러율·서버 자원·배포 상태를 본다면, AI 서비스는 여기에 모델 버전, 피처 버전, 데이터 신선도, 입력 분포 변화, 예측 점수 분포, 정답 label 도착 지연, GPU 사용률과 대기열, batch inference 완료 시각, 재학습 후보 데이터 생성 상태를 더 본다([[AI DE 강의 4-16 모니터링 대시보드와 알람]] p26).

실패도 모델 바깥에서 많이 난다. 모델은 정확한데 느리거나, feature가 오래됐거나, GPU가 놀면서 비용만 쓰거나, 배치 결과가 약속 시간 뒤에 나오거나, 특정 모델 버전·사용자군에서만 나빠진다([[AI DE 강의 4-15 AI 시스템 지표와 SLA]] p3). 이 목록은 Part 1의 침묵의 실패([[데이터 SLA]])를 시스템 전체로 넓힌 것으로 읽힌다. 위키의 관찰이다.

## 네 경로

| 경로 | 흐름 |
|---|---|
| 온라인 추론 | request → feature lookup → model inference → response → serving log |
| 배치 추론 | feature table → batch inference → prediction table → downstream 소비 |
| 학습 데이터 | raw log → feature engineering → label join → training dataset |
| 모니터링 | serving log → prediction-label join → drift / quality metric → retraining trigger |

경로마다 목표가 다르므로 SLO도 따로 건다([[서비스 수준 목표]]). 모니터링 경로 자체도 SLO 대상이다(serving log 반영 지연, prediction-label join 지연).

## 판단 구조

강의는 모니터링을 관측(Observe) → 판단(Orient) → 대응(Act)으로 설명한다(p24). 관측은 골든 시그널로 현재 상태를 보고, 판단은 SLA를 벗어났는지·단순 스파이크인지·구조적 결함인지를 가르고, 대응은 scale-out·rollback 같은 자동 복구나 사람의 개입이다.

⚠️ 이 세 단계는 Boyd의 OODA 루프(Observe-Orient-Decide-Act)에서 Decide가 빠진 모양이다. 강의는 OODA라는 이름을 쓰지 않는다. 대조는 위키의 것이다.

골든 시그널 넷은 Google SRE 책의 것이다. "The four golden signals of monitoring are latency, traffic, errors, and saturation." [https://sre.google/sre-book/monitoring-distributed-systems/ , 2026-09-28 확인]

## 관측 데이터

### 네 종류

| 종류 | 역할 | 예시 | 무엇을 알려 주나 |
|---|---|---|---|
| Metrics | 상태를 수치로 측정 | latency, error rate, GPU utilization | 문제가 발생했는가 |
| Logs | 개별 사건의 상세 기록 | request_id, model_version, error_message | 어떤 요청에서 났는가 |
| Traces | 요청 흐름의 단계별 시간 | feature lookup → inference → postprocess | 어느 단계에서 시간이 걸렸는가 |
| Events | 시스템 변화 기록 | 배포, 모델 교체, autoscaling, GPU node 생성 | 직전에 무엇이 바뀌었는가 |

출처는 [[AI DE 강의 4-16 모니터링 대시보드와 알람]] p28–29다. 네 머리글자를 따 MELT라고 부르는 관행이 있는데, 강의에는 이 이름이 없다.

### label 차원

지표에는 구분 기준이 있어야 한다(p30). service, endpoint, model_name, model_version, feature_version, dataset_version, pipeline_name, batch_id, user_segment, gpu_type, gpu_node 같은 차원이다. 전체 평균 latency는 정상인데 model_version=v3만 느리고, 전체 오류율은 정상인데 신규 사용자 segment만 오류가 늘고, 전체 GPU 사용률은 정상인데 L4 node pool에서만 pending pod가 쌓이는 식의 부분 실패는 차원 없이는 보이지 않는다.

차원을 늘리면 시계열 수(cardinality)가 곱으로 늘어 저장·질의 비용이 커진다. request_id처럼 값이 무한한 것은 metric label이 아니라 log에 둔다. 이 단서는 강의에 없고 위키가 덧붙였다.

### 다섯 계층

| 계층 | 질문 | 지표 |
|---|---|---|
| 서비스 | 사용자가 영향을 받는가 | 요청 수, latency, error rate, timeout |
| 데이터 | 모델 입력이 정상인가 | freshness, row count, schema error, missing feature ratio |
| 모델 | 예측 품질이 변하고 있는가 | score distribution, drift, model_version별 품질 |
| 인프라 | 자원이 병목인가 | pod restart, queue length, GPU utilization, GPU memory |
| 비용 | 과도하게 낭비하고 있는가 | GPU idle cost, cost per inference, batch run cost |

출처는 p31이고, SLO의 다섯 층위([[AI DE 강의 4-15 AI 시스템 지표와 SLA]] p11)와 같다.

## 대시보드 다섯 종

대시보드 설계 순서는 사용자 영향 확인 → 영향 범위 → 원인 후보 좁히기 → 첫 대응 결정 → 사후 분석 근거 확보다(p25). 대시보드는 분석 가능한 맥락을, 알람은 행동 가능한 조건만 준다(p27).

| 대시보드 | 답하는 질문 |
|---|---|
| Overview | 지금 장애인가, 어느 서비스가 영향을 받는가, SLO가 깨지고 있는가. 1분 안에 판단. 최근 배포·스케일링 이벤트를 같은 화면에 |
| Online Inference | 사용자가 느린가, 어느 endpoint·model_version인가, feature lookup·queueing·inference 중 어디서 느린가, 트래픽 때문인가 배포 때문인가 |
| Data Pipeline | 모델 입력이 최신인가, feature table·prediction table이 제시간에 나왔나, row count·null ratio·schema가 평소와 같은가. 성공했더라도 양과 품질을 본다 |
| Model Quality | 점수 분포, 세그먼트별 성능, 새 버전 대 이전 버전, prediction-label 관계, drift. prediction_time과 label_event_time을 분리 |
| GPU / Capacity | GPU 부족인가 낭비인가, 누가 점유하나, memory 부족, MIG slice 활용, node provisioning 실패 |

Model Quality의 시간 분리는 라벨이 늦게 오면 품질 지표도 늦게 갱신되기 때문이다(p38). 라벨 없이 먼저 볼 수 있는 신호는 점수 분포와 입력 분포다([[데이터 드리프트]]).

## 알람

### 증상과 원인

알람은 증상에서 시작하고, 원인은 대시보드로 좁힌다(p42).

| | 증상 알람 | 원인 알람 |
|---|---|---|
| 정의 | 사용자 영향·SLO 위반과 직접 연결 | 장애를 만들 수 있는 내부 상태 |
| 예 | p99 latency SLO 초과, error rate 급증, batch inference deadline miss, feature freshness SLO 위반, prediction table 미생성 | GPU memory 95% 이상, GPU pod pending 증가, feature pipeline 실패, model server pod restart, schema validation failure, Karpenter provisioning 실패 |

SRE 책도 같은 원칙이다. "it’s better to spend much more effort on catching symptoms than causes; when it comes to causes, only worry about very definite, very imminent causes." [https://sre.google/sre-book/monitoring-distributed-systems/ , 2026-09-28 확인] 그래서 원인 알람은 보통 사람을 깨우는 page가 아니라 ticket이나 info로 둔다. p47의 page/ticket/info 구분과 이 원칙을 잇는 것은 위키의 정리다.

### 좋은 알람

좋은 알람은 어떤 SLO가 위험한지, 어떤 서비스·모델 버전인지, 얼마나 지속됐는지, 사용자 영향, 먼저 볼 대시보드, 담당자, 첫 대응을 담는다(p43). 강의의 예시는 다음과 같다.

```
[SEV2] recommender-api p99 latency SLO risk
service=recommender-api
model_version=v42
p99_latency=1.8s
threshold=1.0s
duration=12m
request_rate=normal
dashboard=Online Inference Dashboard
first_action=check queueing delay and recent model rollout
owner=mlops-platform
```

나쁜 알람은 「GPU high」「CPU high」「Latency high」「Pipeline failed」처럼 무엇이 위험하고 무엇을 할지 없는 것이다(p44).

### 심각도

심각도는 사람이 얼마나 빨리 행동해야 하는가로 나눈다(p45).

| 등급 | 범위 | 대응 | 예 |
|---|---|---|---|
| P1 (SEV1) | 핵심 서비스 전체, SLA 위반·대규모 사용자 영향 | 즉시 호출 | 서비스 DB 장애, API 장애 |
| P2 (SEV2) | 일부 모델·세그먼트·지역 | 빠른 대응 | 새 추천 모델의 CTR이 기존 대비 20% 하락 |
| P3 (SEV3) | 장기 추세 악화, capacity 부족, 비용 증가 | 업무 시간 내 | Feature Store 유저 로그의 Null 비율이 0.1%에서 2%로 |

### 알람 피로

원인은 일시적 spike에도 울림, 원인 지표를 모두 page로 연결, 같은 장애의 중복 알람, 담당자·대응 방법 없는 알람, SLO와 무관한 threshold다(p46). 대책은 지속 시간·최소 트래픽 조건, 서비스·모델 버전 단위 grouping, 배포 시간대와 maintenance window 반영, page/ticket/info 구분, 알람마다 runbook 연결, 장애 뒤 알람 품질 리뷰다(p47). 「GPU utilization > 90%」 대신 「p99 latency SLO 위험 AND request queue length 증가 AND 10분 이상 지속 AND request rate가 최소 기준 이상」처럼 증상과 조건을 묶는다. Part 1의 경고 피로 방지는 [[데이터 관측성]]에 있다.

## 트러블슈팅

[[AI DE 강의 4-17 병목 파악과 트러블슈팅]]의 절차는 증상 지표로 incident를 시작 → 원인 지표로 drill-down → logs와 traces로 세부 확인 → events로 최근 변경 확인이다(p52). 「latency 증가 = GPU 부족」, 「모델 품질 하락 = 모델 문제」, 「GPU 사용률 낮음 = 낭비」 같은 단정을 피하고 후보를 줄여 간다(p50). 네 관측 데이터 종류가 이 네 단계에 하나씩 대응한다는 점에서 관측 데이터 설계(p29)와 짝을 이룬다. 이 대응은 위키가 정리한 것이다.

### GPU 사용률 해석

GPU 사용률 하나로는 판단하지 않고 queue·latency와 함께 본다([[AI DE 강의 4-17 병목 파악과 트러블슈팅]] p58, 같은 내용이 [[AI DE 강의 4-16 모니터링 대시보드와 알람]] p40에도 있다).

| GPU 사용률 | Queue | Latency | 해석 |
|---|---|---|---|
| 높음 | 낮음 | 정상 | 잘 활용 중일 수 있음 |
| 높음 | 높음 | 높음 | GPU capacity 병목 가능 |
| 낮음 | 높음 | 높음 | GPU 앞단(feature lookup, CPU 전처리, 네트워크) 병목 가능 |
| 낮음 | 낮음 | 정상 | 과잉 프로비저닝 가능 |
| 높음 | 낮음 | 높음 | memory, batch size, model 병목 가능 |

⚠️ "GPU 사용률"의 정의에 주의한다. nvidia-smi가 보여 주는 NVML utilization은 "Percent of time over the past sample period during which one or more kernels was executing on the GPU"다. 커널이 하나라도 돌았던 시간의 비율이라 SM 몇 개가 바쁜지는 말해 주지 않는다. 작은 커널 하나가 계속 돌면 100%가 나와도 GPU는 대부분 놀 수 있다. SM 활용은 DCGM의 `DCGM_FI_PROF_SM_ACTIVE`("The fraction of time at least one warp was active on a multiprocessor, averaged over all multiprocessors")와 SM occupancy로 본다. [https://docs.nvidia.com/deploy/nvml-api/api/structnvmlUtilization__t.html · https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/feature-overview.html , 2026-09-28 확인] 이 단서는 강의에 없고 위키가 덧붙였다. GPU 구조는 [[GPU 아키텍처]], 할당과 MIG 사용률은 [[GPU 할당과 스케줄링]]에 있다.

## 관련

- [[서비스 수준 목표]]: 무엇을 목표로 거는가
- [[데이터 관측성]]: 데이터 층의 감시, 서킷 브레이커, 경고 피로
- [[데이터 드리프트]]: 모델 품질 대시보드의 분포 지표
- [[추론 최적화]] · [[모델 서빙]]: 온라인 추론 지연의 원인 후보
- [[지연 시간과 처리량]]: p50/p95/p99를 보는 이유

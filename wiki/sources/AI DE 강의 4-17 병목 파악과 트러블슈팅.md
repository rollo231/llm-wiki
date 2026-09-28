---
type: source
title: AI DE 강의 4-17 병목 파악과 트러블슈팅
aliases: [AI DE 4-17]
tags: [AI-DE-강의, 운영, 트러블슈팅]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/02. Ch5. 시스템 운영 및 최적화.pdf"
---

# AI DE 강의 4-17 병목 파악과 트러블슈팅

[[AI DE 강의 4-16 모니터링 대시보드와 알람]]에서 설계한 지표와 대시보드를 실제 장애에 적용하는 소단원이다. 원인을 단정하지 말고 증상 지표로 시작해 원인 지표로 좁히라는 기본 사고를 세운 뒤, 온라인 추론 지연, 데이터 파이프라인 지연, GPU 병목 오해 세 사례를 다룬다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch5. 시스템 운영 및 최적화: 3. 성능 병목 지점 파악 및 트러블슈팅 사례 |
| 원본 파일 | `part4/02. Ch5. 시스템 운영 및 최적화.pdf` p48–59 (12p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-06-05 |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch5`, 소단원 번호 `3`은 표지 슬라이드 |

## 요약

### 01. 트러블슈팅의 기본 사고 (p50–52)

- 트러블슈팅은 후보를 줄이는 과정이다(p50). 사용자 응답이 느림, 배치 결과가 늦음, feature가 오래됨, GPU pod가 pending, 모델 품질 지표 하락 같은 증상을 먼저 확인한다. 「latency 증가 = GPU 부족」, 「batch 지연 = Spark 문제」, 「모델 품질 하락 = 모델 문제」, 「GPU 사용률 낮음 = 자원 낭비」 같은 원인 단정은 위험하다.
- 증상 지표와 원인 지표를 나눈다(p51–52). 증상 지표는 사용자나 downstream이 실제로 겪는 문제(p99 latency 증가, error rate 증가, batch deadline miss, feature freshness SLO 위반, prediction table 미생성, model quality 하락)이고, 원인 지표는 증상을 만들 수 있는 내부 상태(GPU memory 부족, pod restart 증가, Spark shuffle spill, feature pipeline lag, Triton queue time 증가, Karpenter provisioning 실패, schema validation failure)다.
- 운영 원칙은 네 단계다(p52). 증상 지표로 incident를 시작하고, 원인 지표로 drill-down하고, logs와 traces로 세부를 확인하고, events로 최근 변경을 확인한다.

### 02. 사례 1: 온라인 추론 지연 (p53–55)

- 상황(p53): 추천 API p99 latency가 300ms에서 1.8s로 올랐다. 평균 latency는 크게 변하지 않았고 error rate는 정상이며 주로 model_version=v42에서 난다. 잘못된 판단은 「평균이 괜찮으니 문제없음」과 「GPU utilization이 높으니 GPU 증설」이다.
- 확인 순서(p54): p50·p95·p99 분리 → model_version별 latency 비교 → feature lookup latency → queueing delay → model inference time → 최근 model rollout event. 가능한 원인으로 새 모델의 입력 feature 증가, feature lookup path 지연, dynamic batching 설정 변경, model_version별 GPU memory 사용량 증가를 든다.
- 원인 세 갈래(p55).

| 원인 | 상황 | 분석 | 영향 |
|---|---|---|---|
| A. Feature lookup 지연 | 모델 고도화로 요구 피처의 양과 복잡도 증가 | 고속 캐시(Redis)가 아닌 무거운 DB 쿼리 호출로 바뀌며 병목 | 데이터가 많은 헤비 유저의 조회 시간이 길어져 P99 폭증 |
| B. Queueing delay | 처리량 최적화를 위한 dynamic batching 설정의 역설 | 배치가 찰 때까지 기다리거나 최대 대기 시간이 너무 김 | 트래픽이 적은 시간대나 마지막 대기 순번의 요청이 큐에서 과도하게 대기 |
| C. GPU 추론 지연 | 파라미터 증가로 VRAM 가용량 한계 | 메모리 단편화로 연산 효율 급감, 또는 비정상적으로 긴 입력 | GPU 포화로 연산 속도 저하나 장애 |

### 03. 사례 2: 데이터 파이프라인 지연 (p56–57)

- 상황 A, feature freshness 지연(p56): online feature freshness SLO 5분 초과. 서빙 API는 정상이지만 모델이 오래된 feature를 쓸 수 있다. 볼 지표는 source ingestion lag, stream processing lag, feature pipeline duration, online store write latency, schema validation failure, feature group별 update delay다.
- 상황 B, batch inference deadline miss(p57): 매일 07:00까지 prediction table이 필요한데 07:30에도 없다. downstream 추천 후보 생성이 밀린다. 볼 지표는 processed row count, failed partition count, retry count, GPU pod pending, model load time, output write latency, Spot interruption event다.

### 04. 사례 3: GPU 병목 오해 (p58–59)

GPU 사용률 하나로 판단하지 말고 queue와 latency를 함께 본다.

| GPU 사용률 | Queue | Latency | 해석 |
|---|---|---|---|
| 높음 | 낮음 | 정상 | 잘 활용 중일 수 있음 |
| 높음 | 높음 | 높음 | GPU capacity 병목 가능 |
| 낮음 | 높음 | 높음 | GPU 앞단 병목 가능 |
| 낮음 | 낮음 | 정상 | 과잉 프로비저닝 가능 |
| 높음 | 낮음 | 높음 | memory, batch size, model 병목 가능 |

## 핵심

- 증상 지표로 시작해 원인 지표 → logs·traces → events 순으로 좁히는 네 단계(p52)가 이 소단원의 절차다. 앞 소단원의 알람 원칙(증상에 알람, 원인은 대시보드)을 사람의 조사 순서로 옮긴 것이다. 전문은 [[AI 시스템 모니터링]]에 모았다.
- 사례 1의 원인 B(p55)는 [[추론 최적화]]의 동적 배칭이 처리량을 얻는 대신 대기를 만든다는 점을 장애의 모습으로 보여 준다. [[지연 시간과 처리량]]의 맞교환이 꼬리 지연에서 드러나는 경우다.
- 사례 1의 원인 A(p55)는 피처 조회가 캐시에서 DB로 넘어갈 때 꼬리 지연이 무너진다는 이야기다. 캐시 설계는 [[캐싱]]과 [[AI DE 강의 4-05 캐싱 레이어와 캐싱 전략]]에 있다.
- 사례 3의 표(p58)는 GPU 사용률을 단독 지표로 쓰지 말라는 것이다. NVML의 GPU utilization이 "커널이 하나라도 돈 시간의 비율"이라는 정의를 알면 이 표가 왜 필요한지 더 분명해진다(위키 보충, [[AI 시스템 모니터링]]).

## 주의·결함

- 세 사례는 가상 사례다. 수치(300ms → 1.8s, v42, 07:00 → 07:30)에 출처가 없고, 원인 A·B·C 가운데 무엇이 실제 원인이었는지 결론을 내리지 않는다. 확인 순서와 후보 목록을 주는 데서 멈춘다.
- p58과 p59는 같은 슬라이드다.
- 사례 3 표의 "GPU 사용률"이 어떤 지표인지 정의하지 않는다. nvidia-smi가 보여 주는 NVML utilization은 "Percent of time over the past sample period during which one or more kernels was executing on the GPU"다. SM이 얼마나 바쁜지가 아니라 커널이 하나라도 돌았던 시간의 비율이라, 100%여도 GPU가 포화된 것이 아닐 수 있다. SM 활용을 보려면 DCGM의 `DCGM_FI_PROF_SM_ACTIVE`(적어도 한 warp가 활성이었던 시간 비율의 SM 평균)나 SM occupancy를 본다. [NVML API "nvmlUtilization_t" https://docs.nvidia.com/deploy/nvml-api/api/structnvmlUtilization__t.html · DCGM Feature Overview https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/feature-overview.html , 2026-09-28 확인] 이 단서는 자료에 없고 위키가 덧붙였다.
- 사례 1 원인 C의 "메모리 단편화로 연산 효율 급감"은 인과가 흐리다. 단편화는 주로 할당 실패(OOM)나 할당 비용으로 나타나고, 연산 자체를 느리게 만드는 경로는 설명되지 않는다. 위키의 판단이다.

## 관련

- 개념: [[AI 시스템 모니터링]] · [[서비스 수준 목표]] · [[추론 최적화]] · [[지연 시간과 처리량]] · [[피처 스토어]] · [[GPU 아키텍처]] · [[GPU 할당과 스케줄링]]
- 엔티티: [[Triton Inference Server]] · [[Redis]]
- 이전 강의: [[AI DE 강의 4-16 모니터링 대시보드와 알람]]
- 다음 강의: [[AI DE 강의 4-18 GPU 스케줄링과 할당 최적화]]

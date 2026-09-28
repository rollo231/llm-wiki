---
type: source
title: AI DE 강의 4-15 AI 시스템 지표와 SLA
aliases: [AI DE 4-15]
tags: [AI-DE-강의, 운영, SLO]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/02. Ch5. 시스템 운영 및 최적화.pdf"
---

# AI DE 강의 4-15 AI 시스템 지표와 SLA

[[AI 데이터 엔지니어링 강의]] Part 4의 두 번째 덱(Ch5) 첫 소단원이다. AI 시스템이 모델 정확도가 아닌 이유로도 실패한다는 데서 출발해, 운영 지표를 SLI·SLO·SLA·Error Budget 네 단계로 정의하고, 지표를 서비스·데이터·모델 품질·인프라·비용으로 나눈 뒤, 온라인 추론·배치 추론·피처 스토어·학습·모니터링 워크로드마다 SLI와 SLO 예시를 준다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch5. 시스템 운영 및 최적화: 1. AI 시스템의 핵심 지표 설정과 SLA 정의 |
| 원본 파일 | `part4/02. Ch5. 시스템 운영 및 최적화.pdf` p1–21 (21p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-06-05 (Part 4에서 가장 늦음) |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch5`, 소단원 번호 `1`은 표지 슬라이드 |

## 요약

### 01. AI 시스템 운영 지표의 필요성 (p3–8)

- 시스템은 모델 정확도 저하 말고도 실패한다(p3). 예로 든 실패 유형은 여섯 가지다. 모델은 정확한데 응답이 너무 느림, 모델은 정상인데 feature가 오래됨, GPU가 켜져 있는데 사용률이 낮아 비용만 발생, 배치 추론은 성공했는데 결과 테이블이 약속 시간 뒤에 생성됨, API는 살아 있는데 특정 모델 버전에서 에러율 급증, 전체 품질은 좋아 보이는데 특정 사용자군에서 성능 저하.
- AI 시스템은 네 경로가 동시에 움직인다(p4–5). 경로마다 목표가 다르다.

| 경로 | 흐름 | 목표 |
|---|---|---|
| 온라인 추론 | request → feature lookup → model inference → response → serving log | 빠른 응답, 낮은 에러율, 안정적인 tail latency |
| 배치 추론 | feature table → batch inference → prediction table → downstream 소비 | 정해진 시간 안에 결과 테이블 생성 |
| 학습 데이터 | raw log → feature engineering → label join → training dataset | 정확한 데이터셋, 재현성, 완료 시각 준수 |
| 모니터링 | serving log → prediction-label join → drift / quality metric → retraining trigger | 모델 버전별 품질 변화와 분포 변화 감지 |

- 운영 지표는 관찰용 숫자가 아니라 행동 기준이다(p6). 목적은 현재 상태 파악, 사용자 영향 판단, 장애 조기 감지, 증설·축소 판단, 모델 롤백 판단, 재학습 필요성 판단, 비용 낭비 탐지다.
- 좋은 지표는 사용자 경험과 연결되고, 운영자가 행동할 수 있고, 측정 방법·시간 범위·소유자가 정해져 있고, 알람 기준으로 바꿀 수 있다(p7). 나쁜 지표는 높으면 좋을 것 같은데 무엇을 할지 모르는 지표, 평균만 보고 tail latency를 놓치는 지표, GPU 사용률만 보고 사용자 지연을 설명하지 못하는 지표, 정확도만 보고 freshness 문제를 숨기는 지표, 그리고 「200 OK」다(p8).

### 02. SLA / SLO / SLI / Error Budget (p9–11)

- 네 단계를 정의하고 예를 단다(p9). SLI는 실제로 측정하는 지표(최근 30일 동안 정상 응답한 추론 요청 비율), SLO는 SLI에 대한 내부 목표(정상 응답 비율 99.9% 이상), SLA는 고객·조직과 공식적으로 약속한 수준(고객에게 월간 99.5% 이상 가용성), Error Budget은 SLO 기준으로 허용되는 실패 여유분(99.9% SLO라면 30일 동안 0.1% 실패 허용)이다.
- p10은 같은 내용을 건강검진 비유 표로 다시 쓴다. SLI는 체온계의 눈금, SLO는 36.5~37.5도 유지, SLA는 건강보험 계약이다. 추천 API 예시로 SLI(P99 응답 속도, HTTP 500 비율, 피처 최신화 지연), SLO(P99 200ms 이하, 한 달 정상 응답률 99.9%, 피처 최신화 5분 이내), SLA(「API 가동률 99.9% 미달 시 이번 달 서비스 이용료의 10% 환불」)를 든다.
- AI 시스템의 SLA/SLO는 다섯 층위로 나뉜다(p11). 서비스 SLA(요청 성공률·응답 지연·가용성), 데이터 SLA(freshness·completeness·schema 안정성), 모델 품질 SLO(정확도·drift·score distribution·segment별 성능), 인프라 SLO(GPU availability·GPU memory headroom·queue length·node readiness), 비용 SLO(cost per inference·idle GPU cost·batch job 비용 한도)다.

### 03. AI 시스템의 핵심 지표 분류 (p12–16)

| 분류 | 지표 | 쪽 |
|---|---|---|
| 서비스 | availability, latency, error rate(5xx·timeout·model unavailable·feature lookup failure), throughput. LLM은 time to first token, time per output token, tokens per second, prompt·output 길이에 따른 latency 변화 | p12 |
| 데이터 | freshness, completeness, validity, schema stability | p13 |
| 모델 품질 | accuracy·precision·recall·F1, AUC·NDCG·MAP, conversion rate, CTR, prediction-label agreement, score distribution, calibration, segment별 성능, drift metric | p14 |
| GPU·인프라 | GPU utilization·memory·temperature·power·throttling·ECC error·allocation count·MIG slice 사용률, pod restart, replica count, request·batch queue length, model load time, container OOM, node readiness, autoscaling event | p15 |
| 비용 | cost per 1,000 inference, cost per 1M tokens, cost per batch run, GPU idle cost, GPU hour per model, training cost per experiment, feature pipeline cost, dataset version별 storage cost | p16 |

### 04. 워크로드별 SLA/SLO 설계 (p17–21)

워크로드마다 대표 SLI와 SLO 예시를 짝지어 준다. 수치는 자료가 든 예시다. 표는 [[서비스 수준 목표]]에 옮겼다.

- 온라인 추론(p17): 정상 응답률 99.9%(30일), p95 300ms, p99 1s, feature lookup 실패율 0.1% 이하, LLM 첫 토큰 p95 1s.
- 배치 추론(p18): 매일 07:00 KST 이전 prediction table 생성, 대상 user 99.5% 이상 scoring, 실패 partition 0.5% 이하, 재시도 후 성공률 99%, 비용 월 예산 이하.
- 피처 스토어(p19): online lookup p99 50ms, 주요 feature freshness 5분, missing feature ratio 0.1%, offline-online mismatch 0.1%, pipeline 성공률 99%.
- 학습 파이프라인과 모델 모니터링(p20–21): 학습 데이터셋 매일 09:00 이전 생성, 데이터 검증 실패 시 학습 job 시작 금지, serving log 10분 이내 모니터링 테이블 반영, prediction-label join은 label 도착 후 1시간 이내, drift metric 매일 1회 이상 갱신.

## 핵심

- 이 소단원의 설명 틀은 "경로마다 SLO를 따로 건다"이다(p4–5, p17–21). 온라인 추론은 지연, 배치 추론은 마감 시각, 학습은 재현성과 완료 시각, 모니터링은 반영 지연이 목표라서 하나의 가용성 숫자로는 AI 시스템을 설명하지 못한다. 전문은 [[서비스 수준 목표]]에 모았다.
- p3의 실패 유형 여섯 가지는 대부분 모델 바깥에서 난다. 신선도, 마감, 비용, 버전별 에러, 세그먼트 편차다. Part 1의 "침묵의 실패"([[데이터 SLA]])를 AI 시스템 전체로 넓힌 목록으로 읽힌다. 이 연결은 위키의 관찰이다.
- p11의 다섯 층위(서비스·데이터·모델·인프라·비용)는 다음 소단원의 모니터링 5계층([[AI DE 강의 4-16 모니터링 대시보드와 알람]] p31)과 같다. 목표를 거는 층과 관측하는 층이 일치한다는 점에서 Ch5 안의 설계가 일관적이다.
- 데이터 층의 지표(p13)는 Part 1의 품질 분류들과 겹치면서 schema stability를 따로 떼어 낸다. 강의 안의 네 번째 분류가 된다. 대조는 [[데이터 SLA]]에 있다.
- 피처 스토어 SLO에 offline-online mismatch가 들어간 것(p19)은 [[학습-서빙 스큐]]를 운영 지표로 바꾼 것이다([[피처 스토어]]).

## 주의·결함

- ⚠️ p10 표의 SLA 예시는 "가동률 99.9% 미달 시 환불"이다. 같은 표의 SLO도 "정상 응답률 99.9%"라 SLA와 SLO가 같은 값이다. 바로 앞 p9는 SLO 99.9%, SLA 99.5%로 SLA를 더 느슨하게 뒀다. Google SRE 책은 사용자에게 약속한 수준보다 빡빡한 내부 SLO를 두라고 권한다("Using a tighter internal SLO than the SLO advertised to users gives you room to respond to chronic problems before they become visible externally." https://sre.google/sre-book/service-level-objectives/ , 2026-09-28 확인). p9가 책과 맞고 p10 예시가 어긋난다.
- ✅ p9의 네 단계 정의는 SRE 책의 정의와 맞는다(같은 URL, 2026-09-28 확인).
- ❗ 목차(p2)의 「05 GPU 데이터 파이프라인 설계 판단 기준」에 해당하는 본문이 없다. 이 제목은 Ch4 소단원 4([[AI DE 강의 4-13 데이터 엔지니어링의 GPU 활용]])의 목차 항목과 같다. 목차를 복사한 흔적으로 보이는데, 추론이다.
- p8 「나쁜 운영 지표」의 마지막 불릿은 설명 없이 「200 OK」 한 단어다. HTTP 200만 보고 정상이라고 판단하는 지표, 즉 응답은 성공했지만 내용(오래된 feature, 빈 결과)이 틀린 경우를 가리키는 것으로 읽힌다. 이 해석은 위키의 것이다.
- Error Budget의 시간 환산은 없다. 99.9% SLO를 30일 시간 기준으로 바꾸면 약 43분(30 × 24 × 60 × 0.001 = 43.2분)이다. 위키가 계산한 것이다. 요청 비율 SLI(p9)라면 시간이 아니라 요청 수로 센다.
- p17·p18의 SLO 목록은 SLI 목록과 줄이 맞지 않게 나란히 놓여 있어 어떤 SLI의 목표인지 대응이 흐리다(예: timeout 비율, queueing delay에는 SLO가 없다).

## 관련

- 개념: [[서비스 수준 목표]] · [[AI 시스템 모니터링]] · [[데이터 SLA]] · [[지연 시간과 처리량]] · [[피처 스토어]] · [[모델 서빙]]
- 이전 강의: [[AI DE 강의 4-14 RAPIDS 가속 ETL]]
- 다음 강의: [[AI DE 강의 4-16 모니터링 대시보드와 알람]]

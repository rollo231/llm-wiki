---
type: source
title: AI DE 강의 4-18 GPU 스케줄링과 할당 최적화
aliases: [AI DE 4-18]
tags: [AI-DE-강의, GPU, 인프라, Kubernetes, 비용]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "raw/data-engineering/ai-de-course/part4/02. Ch5. 시스템 운영 및 최적화.pdf"
---

# AI DE 강의 4-18 GPU 스케줄링과 할당 최적화

[[AI 데이터 엔지니어링 강의]] Part 4 Ch5 「시스템 운영 및 최적화」의 마지막 소단원(4)이자 Part 4의 끝이다. GPU 스케줄링을 "빈 GPU에 Pod를 올리는 일"이 아니라 워크로드마다 다른 목표(지연·마감·안정 점유·비용)를 지키는 문제로 정의하고, 워크로드 분류, 할당 방식, 목적별 노드 풀, 동적 프로비저닝과 Spot/On-Demand를 다룬다. 덱 `01`의 [[AI DE 강의 4-12 GPU 할당 아키텍처]]와 내용이 크게 겹친다.

## 인용

| 항목 | 내용 |
|---|---|
| 자료 | 패스트캠퍼스 AI 데이터 엔지니어링 강의 슬라이드, Part 4 「실시간 & 대규모 데이터 분산 처리 설계」 |
| 덱 제목 | Ch5. 시스템 운영 및 최적화: 4. GPU 자원 스케줄링 및 할당 최적화 전략 |
| 원본 파일 | `part4/02. Ch5. 시스템 운영 및 최적화.pdf` p60–75 (16p) |
| 강사 | 슬라이드에 표기 없음 |
| 작성 시기 | PDF 생성일 2026-06-05 (Part 4에서 가장 늦음) |
| URL | 없음 (유료 강의 자료) |
| 챕터 번호 | 파일명에 `Ch5`, 소단원 번호 `4`는 표지 슬라이드 |

## 요약

### 01. GPU 스케줄링 문제 정의 (p62–64)

- 실제 목표는 워크로드별로 다르다. 서빙은 지연, 배치는 마감, 학습은 장시간 안정 점유, 실험은 낮은 비용(실패 감수), ETL은 특정 시간대의 대량 GPU다(p62).
- 스케줄링은 단순 배치 문제가 아니다. SLA, 낭비, 팀 사이 공정성, 중요 워크로드 보호, Spot 중단, MIG 파편화를 함께 따진다(p63).
- 자주 생기는 세 실패: 과소 활용(대형 GPU를 작은 모델이 점유, 10GB만 사용), 간섭(격리가 약해 OOM·memory pressure가 번짐, 서빙 지연이 배치 때문에 흔들림), 파편화(애매하게 남은 MIG slice·노드)(p64).

### 02. 워크로드 분류와 우선순위 설계 (p65–67)

- 워크로드별 핵심 목표, 실패 허용, 적합한 정책을 표로 준다. 온라인 추론(낮은 지연·높은 가용성, 실패 허용 낮음, On-Demand·높은 우선순위), 배치 추론(마감, 중간, Spot·재시도·queue), 학습(장시간 안정, 낮음~중간, checkpoint·전용 GPU), GPU ETL(시간대 처리량, 중간, Spot burst·시간대별 scale-out), 실험(비용 절감, 높음, 낮은 우선순위·preempt)(p65).
- 모두 같은 GPU NodePool에 섞으면 배치가 서빙 replica를 pending시키고, Spot 중단이 서빙에 번지고, 실험이 메모리를 과점유하고, ETL 시간대에 서빙 지연이 흔들린다(p66). 권장은 Serving · Batch · Experiment · MIG 풀 분리다(p67).

### 03. GPU 할당 방식 (p68–69)

- Full GPU(예측 가능성 최고, 비용 높음, 대형 학습·대형 LLM 추론), time-slicing/MPS(유휴 자원 활용, 격리는 MIG보다 약함, 지연 민감 워크로드에는 신중), MIG(작은 모델 여러 개를 격리 운영, profile 파편화와 재구성 비용)(p68).
- 선택 기준 다섯 질문: SLA, 메모리 요구량, 간섭 허용, GPU 전체 필요 여부, 작은 워크로드의 수(p69).

### 04. Kubernetes 기반 스케줄링 전략 (p70–71)

- 목적별 노드 풀 다섯: gpu-serving-ondemand, gpu-training, gpu-batch-spot, gpu-mig-serving, gpu-experiment(p70).
- 필요한 정책: node label, taint/toleration, nodeSelector/affinity, priorityClass, namespace quota, resource request/limit(p71).

### 05. 동적 프로비저닝과 비용 최적화 (p72–75)

- GPU를 항상 켜 두면 낭비이고, 배치 ETL·배치 추론은 특정 시간대에만, 실험은 불규칙하게 필요하다. Karpenter 류 프로비저너는 pending pod의 요구를 보고 인스턴스를 골라 노드를 만들고 끝나면 없앤다(p72).
- 해결하지 못하는 것: cloud quota, 리전 capacity, 드라이버·런타임 오류, 너무 좁은 인스턴스 조건, Spot 중단, 모델 로드 warm-up(p73–74).
- On-Demand가 맞는 워크로드(온라인 추론 baseline, 중요 서빙, checkpoint 어려운 장시간 작업, SLO 위반 비용이 큰 작업)와 Spot이 맞는 워크로드(GPU ETL, 배치 추론, 재시도 가능한 전처리, 실험, checkpoint 가능한 학습)(p75).

## 핵심

- 스케줄링을 워크로드별 목표와 실패 허용도의 표(p65)로 시작하는 것이 이 소단원의 틀이다. 덱 `01`은 할당을 하드웨어 격리에서 시작했고, 이 소단원은 운영 목표에서 시작한다. 두 소단원의 내용을 합친 전문은 [[GPU 할당과 스케줄링]]에 있다.
- 파편화(p64)와 priorityClass·namespace quota(p71)는 덱 `01`에 없던 것이다.
- 워크로드별 목표가 [[AI DE 강의 4-15 AI 시스템 지표와 SLA]]의 워크로드별 SLO(온라인 추론·배치 추론·피처 스토어·학습)와 대응한다. 강의는 둘을 잇지 않았고, 이 대응은 위키의 관찰이다.

## 주의·결함

- 내용 대부분이 [[AI DE 강의 4-12 GPU 할당 아키텍처]](덱 `01` p280–301)와 겹친다. 과소 활용·간섭의 정의, full/time-slicing/MPS/MIG 비교, taint·toleration·nodeSelector, On-Demand baseline과 Spot burst가 모두 두 번 나오는데 서로를 참조하지 않는다. 덱 `01`이 자세한 쪽(MIG Manager, MPS의 device plugin 제약)이다.
- time-slicing과 MPS를 한 칸으로 묶는다(p68). 덱 `01` p293은 둘의 격리 수준을 "낮음"과 "최악"으로 크게 구분했는데, 여기서는 "격리는 MIG보다 약함" 하나로 뭉뚱그린다.
- ✅ Karpenter의 역할 서술(p72)은 공식 문서와 맞다. 강의는 AWS 전제로 쓰는데, Karpenter는 AWS 외에 Azure 공식 provider와 커뮤니티 provider가 있다. [https://github.com/kubernetes-sigs/karpenter , 2026-09-28 확인]
- 중복: p73 = p74.
- 수치가 없다. 이용률 목표, 파편화를 판단하는 기준, Spot 할인율과 중단 빈도, 노드 수명 같은 값이 하나도 없다.
- 덱 `02`는 이 소단원으로 끝나고, Part 4를 정리하는 슬라이드가 없다.

## 관련

- 개념: [[GPU 할당과 스케줄링]] · [[GPU 아키텍처]] · [[서비스 수준 목표]] · [[AI 시스템 모니터링]]
- 같은 주제: [[AI DE 강의 4-12 GPU 할당 아키텍처]]
- 이전 강의: [[AI DE 강의 4-17 병목 파악과 트러블슈팅]]
- 다음 강의: 없음. Part 4의 끝이고 Part 5는 미착수다([[AI 데이터 엔지니어링 강의]]).

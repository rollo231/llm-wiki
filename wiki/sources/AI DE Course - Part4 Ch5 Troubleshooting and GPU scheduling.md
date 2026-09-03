---
type: source
title: AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling
area: [data-engineering]
aliases: [Part4 Ch5-3,4, 성능 병목 지점 파악 및 트러블슈팅, GPU 자원 스케줄링 및 할당 최적화]
tags: [data-engineering, course, fast-campus, troubleshooting, gpu, scheduling, kubernetes, spot, karpenter, mig]
created: 2026-08-01
updated: 2026-09-03
sources: ["raw/data-engineering/ai-de-course/part4/02. Ch5. 시스템 운영 및 최적화.pdf (p48–75)"]
---

# AI DE Course - Part4 Ch5 Troubleshooting and GPU scheduling

**출처:** 패스트캠퍼스 데이터 엔지니어링 강의 · **Part 4** Ch5의 소단원
**3 "성능 병목 지점 파악 및 트러블슈팅 사례"** + **4 "GPU 자원 스케줄링 및 할당 최적화 전략"**.
Part 4의 마지막 소단원들이다. 원본(로컬): `raw/data-engineering/ai-de-course/part4/02. Ch5. 시스템 운영 및 최적화.pdf` **p48–75** (75p 중).
강의 홈: [[AI Data Engineering (Fast Campus course)]].

> ⭐ **소단원 3의 "증상 지표 vs 원인 지표" 분리가 Part 4 운영 챕터 전체의 결론이다.**
> 소단원 4는 [[AI DE Course - Part4 Ch4 GPU allocation architecture]]와 주제가 상당히 겹치지만,
> **워크로드 분류별 정책 표**와 **동적 프로비저닝이 해결하지 못하는 것**은 여기에만 있다.

## 구성

소단원 3: `01 트러블슈팅의 기본 사고 · 02 사례 1 · 03 사례 2 · 04 사례 3`
소단원 4: `01 GPU 스케줄링 문제 정의 · 02 워크로드 분류와 우선순위 설계 · 03 GPU 할당 방식 ·
04 Kubernetes 기반 스케줄링 전략 · 05 동적 프로비저닝과 비용 최적화`

---

## ⭐ 트러블슈팅의 기본 사고

> **"후보를 줄이는 과정."** 증상들을 먼저 확인: 사용자 응답이 느림 · 배치 결과가 늦음 ·
> feature가 오래됨 · GPU pod가 pending · 모델 품질 지표가 하락…

**원인 단정은 위험 — 네 가지 성급한 결론:**

| 증상 | 성급한 결론 |
|---|---|
| latency 증가 | = GPU 부족? |
| batch 지연 | = Spark 문제? |
| 모델 품질 하락 | = 모델 문제? |
| GPU 사용률 낮음 | = 자원 낭비? |

> ⭐ **네 개 모두 "그럴듯하지만 자주 틀리는" 추론이다.** 특히 마지막 두 개 —
> 모델 품질 하락은 데이터 문제일 때가 많고, GPU 사용률이 낮은 것은 **앞단 병목**일 수 있다
> (Ch5-2의 해석 규칙 3행).

### ⭐⭐ 증상 지표와 원인 지표를 분리하라

| **증상 지표** — 사용자나 downstream이 실제로 겪는 문제 | **원인 지표** — 증상을 만들 수 있는 내부 상태 |
|---|---|
| p99 latency 증가 | GPU memory 부족 |
| error rate 증가 | pod restart 증가 |
| **batch deadline miss** | **Spark shuffle spill** |
| **feature freshness SLO 위반** | **feature pipeline lag** |
| **prediction table 미생성** | **Triton queue time 증가** |
| model quality 하락 | **Karpenter provisioning 실패** |
| | schema validation failure |

**운영 원칙 4단계:**

1. **증상 지표로 incident 시작**
2. **원인 지표로 drill-down**
3. logs와 traces로 세부 확인
4. **events로 최근 변경 사항 확인**

> ⭐ **이 4단계가 Ch5-2의 관측 4축(Metrics/Logs/Traces/Events)과 정확히 대응한다.**
> Metrics(증상 → 원인) → Logs → Traces → Events. **두 소단원이 같은 골격을 공유하는 것이
> 이 챕터의 강점이다.**
>
> **그리고 "알람은 증상에서 시작"(Ch5-2)의 이유가 여기서 명확해진다** — 원인 지표로 알람하면
> 아직 사용자 영향이 없는데도 호출되고, 증상 없는 원인은 대개 자체 해소된다.

## 사례 1 — 온라인 추론 지연

**상황:** 추천 API p99 latency가 **300ms → 1.8s**. 평균 latency는 크게 변하지 않음.
error rate는 정상. **특정 `model_version=v42`에서 주로 발생.**

| ⚠️ 잘못된 판단 |
|---|
| 평균 latency가 괜찮으니 문제 없음 |
| GPU utilization이 높으니 GPU 증설 |

**확인 순서 6단계:**

1. **p50, p95, p99 분리 확인**
2. **`model_version`별 latency 비교**
3. feature lookup latency 확인
4. queueing delay 확인
5. model inference time 확인
6. **최근 model rollout event 확인**

> **이 6단계가 Ch5-2의 Online Inference Dashboard 구성 그대로다.** 대시보드가 트러블슈팅 절차의
> UI라는 앞의 논지가 여기서 증명된다.

**가능한 원인과 분석:**

| 원인 | 상황 | 분석 | 영향 |
|---|---|---|---|
| **A. Feature Lookup 지연** | 모델 고도화로 요구되는 피처의 양과 복잡도 증가 | **고속 캐시(Redis)가 아닌 무거운 DB 쿼리 호출로 전환**되면서 병목 | **데이터량이 많은 '헤비 유저'의 조회 시간이 비정상적으로 길어짐 (P99 폭증)** |
| **B. Queueing Delay** | 처리량 최적화를 위한 **Dynamic Batching 설정의 역설** | 배치 크기가 찰 때까지 기다리거나 **최대 대기 시간(Timeout) 설정이 너무 김** | **트래픽이 적은 시간대나 마지막 대기 순번의 요청이 큐에서 과도한 시간 허비** |
| **C. Model Inference 지연** | 모델 파라미터 증대로 인한 **VRAM 가용량 한계** | **메모리 단편화(Fragmentation)로 연산 효율이 급감**하거나, 비정상적으로 긴 입력값 유입 | GPU 자원이 포화되어 연산 속도 자체가 저하되거나 장애 |

> ⭐⭐ **원인 A가 이 사례의 핵심이다 — "평균은 정상인데 P99만 폭증"의 정확한 메커니즘.**
> **헤비 유저의 피처 조회가 무거워지면서 꼬리만 늘어난다.** 사용자별 데이터량 편차가
> latency 분포의 꼬리를 만든다는 것 — 평균으로는 절대 안 보인다.
>
> ⭐ **원인 B가 특히 좋다 — "처리량 최적화가 지연을 만든다".**
> Dynamic Batching은 [[NVIDIA Triton Inference Server]]의 대표 기능이고 Part 2에서 장점으로만
> 배웠는데, 여기서 **트래픽이 적을 때 오히려 해가 된다**는 역설을 짚는다.
> **[[Latency and throughput]]의 "시소의 법칙"이 서빙 설정에서 반복되는 형태다.**
>
> **세 원인이 정확히 Ch5-2 대시보드의 latency 3구간(feature lookup / queueing / inference)이다.**

## 사례 2 — 데이터 파이프라인 지연

### 상황 A. Feature freshness 지연

- online feature freshness **SLO 5분 초과**
- **서빙 API는 정상**
- **하지만 모델은 오래된 feature 사용 가능**

**확인할 지표:** **source ingestion lag** · **stream processing lag** · feature pipeline duration ·
online store write latency · schema validation failure · feature group별 update delay

> ⭐ **`source ingestion lag`과 `stream processing lag`을 분리하는 게 Ch3-3의 "수집 시각 vs 처리
> 시각" 구분의 실무적 쓰임이다.** 브로커까지 왔는데 엔진이 안 읽은 것인지, 브로커에도 안 온 것인지를
> 이 두 지표가 가른다. **강의가 두 챕터를 잇지 않지만 정확히 대응한다.**
>
> **"서빙 API는 정상, 하지만 모델은 오래된 feature 사용"** 이 Part 1의 **침묵의 실패**의 가장
> 전형적인 형태다.

### 상황 B. Batch inference deadline miss

- 매일 **07:00까지 prediction table 생성 필요**, 오늘은 **07:30에도 미생성**
- downstream 추천 후보 생성 지연

**확인할 지표:** processed row count · failed partition count · retry count · **GPU pod pending** ·
**model load time** · output write latency · ⭐ **Spot interruption event**

> ⭐ **`Spot interruption event`가 목록에 있는 게 좋다.** 소단원 4의 "배치는 Spot"이라는 권고가
> **deadline miss의 원인이 될 수 있다**는 것 — 비용 최적화와 SLO가 충돌하는 지점을 같은 챕터에서
> 양쪽 모두 보여준다.

## ⭐ 사례 3 — GPU 병목 오해 (해석표)

| GPU 사용률 | Queue | Latency | 해석 |
|---|---|---|---|
| 높음 | 낮음 | 정상 | **잘 활용 중일 수 있음** |
| 높음 | 높음 | 높음 | **GPU capacity 병목 가능** |
| **낮음** | **높음** | **높음** | ⭐ **GPU 앞단 병목 가능** |
| 낮음 | 낮음 | 정상 | **과잉 프로비저닝 가능** |
| 높음 | 낮음 | 높음 | **memory, batch size, model 병목 가능** |

> ⭐⭐ **이 5행 표가 Part 4 Ch5의 최고 산출물이고, Part 2 "GPU는 마지막 수단"의 진단 도구다.**
>
> **세 축(사용률 × 큐 × 지연)의 조합으로 읽어야 한다는 게 요점이다.** GPU 사용률 하나로는
> 정반대 상황을 구분할 수 없다:
> - 사용률 높음 + 큐 낮음 + 정상 = **좋은 상태**
> - 사용률 높음 + 큐 낮음 + 지연 높음 = **memory/batch size 문제** (증설해도 안 나아짐)
>
> **3행("낮음/높음/높음 = 앞단 병목")이 가장 값지다** — GPU를 늘리고 싶은 유혹이 가장 큰 상황인데,
> **답은 feature lookup·CPU 전처리·네트워크**다. Ch4-1,2의 PCIe 병목, Ch4-4의 "입력 파이프라인이
> 병목", Ch5-2의 해석 규칙이 모두 여기로 수렴한다.
>
> **5행이 Ch5-2의 "GPU memory 높음 + OOM = KV cache 문제"와 짝을 이룬다.**

---

## GPU 스케줄링 (소단원 4)

### 문제 정의 — 빈 GPU에 Pod를 올리는 것이 아니다

> **"GPU 스케줄링의 실제 목표"** — 워크로드마다 요구가 다르다:
>
> - **서빙**은 지연 시간을 지켜야 함
> - **배치**는 마감 시간 안에 끝나야 함
> - **학습**은 긴 시간 안정적으로 GPU를 점유해야 함
> - **실험**은 비용을 낮추되 실패를 감수할 수 있음
> - **ETL**은 특정 시간대에만 대량 GPU가 필요함

> **"GPU 스케줄링은 단순 배치 문제가 아님"** — SLA를 지킬 것인가 / GPU를 낭비하지 않을 것인가 /
> **여러 팀을 공정하게 나눌 것인가** / 중요 workload를 우선 보호할 것인가 /
> **Spot 중단을 감당할 수 있는가** / **MIG 조각이 파편화되지 않는가**

### GPU 운영의 세 가지 실패

| 실패 | 내용 |
|---|---|
| **1. 과소활용** | A100/H100 같은 대형 GPU를 작은 추론 모델 하나가 점유. **GPU memory는 10GB만 쓰고 나머지는 비어있는데 비용은 full GPU 기준으로 계속 발생** |
| **2. 간섭** | 하나의 GPU에 여러 workload를 얹었지만 격리가 약함. **한 작업의 OOM이나 memory pressure가 다른 작업에 영향. 서빙 latency가 batch job 때문에 흔들림** |
| **3. 파편화** | ⭐ **MIG slice 또는 GPU node가 애매하게 남음. 작은 workload는 많지만 필요한 profile이 없고, 큰 workload를 올릴 수 있는 연속 자원이 부족** |

> ⭐ **3번(파편화)이 Ch4-3에는 없던 항목이고, MIG의 실무적 함정이다.**
> Ch4-3에서 본 **"MIG geometry 재구성 시 GPU pods를 중지해야 한다"** 와 합치면 문제가 명확해진다 —
> **파편화됐는데 재구성 비용이 무중단이 아니라서 쉽게 못 고친다.** 두 소단원을 합쳐야 완성되는
> 그림인데 강의가 교차 참조하지 않는다.

### ⭐ 워크로드 분류와 정책 — 이 소단원의 핵심 표

| Workload | 핵심 목표 | 실패 허용 | 적합한 정책 |
|---|---|---|---|
| **온라인 추론** | 낮은 latency, 높은 가용성 | **낮음** | **On-Demand**, 우선순위 높음, 안정적 할당 |
| **배치 추론** | deadline 내 완료 | 중간 | **Spot 가능**, 재시도 가능, queue 기반 |
| **학습** | 긴 시간 안정적 실행 | 낮음~중간 | **checkpoint, 전용 GPU, 중단 대응** |
| **GPU ETL** | 특정 시간대 처리량 | 중간 | **Spot burst, 시간대별 scale-out** |
| **실험/개발** | 비용 절감 | **높음** | **낮은 우선순위, preempt 가능** |

> ⭐ **"실패 허용"이라는 열이 이 표를 유용하게 만든다.** Spot을 쓸 수 있는지가 결국
> **중단을 감당할 수 있는가**로 결정되고, 그것은 워크로드의 성질이지 예산의 문제가 아니다.

### 서빙과 배치를 같은 pool에 섞으면

| 잘못된 구성 | 발생 가능한 문제 |
|---|---|
| 온라인 추론 Pod | **배치 job이 GPU를 선점해 서빙 replica pending** |
| 배치 추론 Job | **Spot 중단으로 serving까지 영향** |
| GPU ETL Job | 개발 실험이 GPU memory를 과도하게 점유 |
| 개발 실험 Pod | **서빙 latency가 ETL job 실행 시간대에 흔들림** |
| ↑ 모두 같은 GPU NodePool | |

**권장 방향 — pool 4종:**

| Pool | 정책 |
|---|---|
| **Serving GPU Pool** | On-Demand baseline, 높은 priority, 안정성 우선 |
| **Batch GPU Pool** | Spot 중심, queue 기반, **checkpoint/retry 전제** |
| **Experiment GPU Pool** | 낮은 priority, **quota 제한**, idle 자원 활용 |
| **MIG Pool** | 작은 모델 또는 경량 inference 격리 배치 |

### GPU 할당 방식 — 선택 기준 5문항

Ch4-3과 거의 같은 내용이지만 **선택 기준을 5문항으로 압축**한 것이 추가된다:

1. **SLA가 중요한가?**
2. 메모리 요구량이 얼마나 되는가?
3. **간섭을 허용할 수 있는가?**
4. GPU 전체가 필요한가?
5. **작은 workload를 많이 태울 것인가?**

MIG의 대가도 한 줄 추가된다: **"profile 파편화와 재구성 비용 고려 필요."**

### Kubernetes 스케줄링 전략 — NodePool 5종

```
gpu-serving-ondemand      gpu-training
 - 온라인 추론               - 장시간 학습
 - 높은 priority            - checkpoint 전제
 - 최소 capacity 유지        - 큰 GPU 우선

gpu-batch-spot            gpu-mig-serving
 - batch inference         - 작은 모델 다중 서빙
 - GPU ETL                 - MIG profile 기반 할당
 - 재시도 가능 workload

gpu-experiment
 - 개발·실험
 - 낮은 priority
 - quota 제한
```

**필요한 Kubernetes 정책 6종:** node label · **taint / toleration** · nodeSelector / affinity ·
**priorityClass** · **namespace quota** · resource request / limit

> **`priorityClass`와 `namespace quota`가 Ch4-3에는 없던 항목이다.** 워크로드 우선순위와 팀별
> 자원 배분을 K8s 기본 기능으로 구현하는 방법인데, **preemption 동작(높은 priority pod이 낮은
> 것을 쫓아냄)은 설명되지 않는다.**

### ⭐ 동적 프로비저닝 — 그리고 그것이 해결하지 못하는 것

**필요한 이유:** GPU를 항상 켜두면 비용 낭비 · 배치 ETL과 batch inference는 특정 시간대에만 필요 ·
실험 workload는 수요가 불규칙 · GPU 종류와 크기를 workload에 맞게 선택해야 함

**Karpenter류 프로비저닝의 역할:** pending pod 요구사항 확인 → 조건에 맞는 instance type 선택 →
GPU node 생성 → **작업 완료 후 빈 node 제거**

> ⭐⭐ **"하지만 해결하지 못하는 것" 6가지 — 이 소단원에서 가장 값진 목록:**
>
> | 해결 못하는 것 | 성격 |
> |---|---|
> | **cloud quota 부족** | 행정 |
> | **region capacity 부족** | 물리 |
> | driver/runtime 구성 오류 | 소프트웨어 |
> | **너무 좁은 instance type 조건** | 설정 |
> | **Spot interruption** | 계약 |
> | **model load warm-up 지연** | 시간 |
>
> **"오토스케일러를 붙였으니 GPU 부족은 해결됐다"는 착각을 정면으로 깬다.**
> 특히 **region capacity 부족**은 자동화로 못 푸는 물리적 한계이고, **model load warm-up 지연**은
> 노드가 떠도 서비스가 바로 되는 게 아니라는 뜻이다 — **스케일아웃 지연에 모델 로딩 시간이
> 더해진다.**
>
> **Ch4-3의 "클라우드 인프라 준비 계층(행정적/소프트웨어적/물리적 한계)"과 정확히 같은 목록인데,
> 여기서는 "동적 프로비저닝의 한계"라는 각도로 다시 나온다.** 중복이지만 이번 프레이밍이 더 낫다.

### Spot vs On-Demand

| On-Demand가 맞는 workload | Spot이 맞는 workload |
|---|---|
| 온라인 추론 baseline | GPU ETL |
| 중요 모델 서빙 | batch inference |
| **checkpoint가 어려운 장시간 job** | 재시도 가능한 전처리 |
| **SLO 위반 비용이 큰 workload** | 실험 job |
| | **checkpoint 가능한 학습 job** |

> ⭐ **판단 기준이 "중요도"가 아니라 "checkpoint 가능성"과 "SLO 위반 비용"이라는 게 정확하다.**
> 학습 job이 양쪽에 걸쳐 있는 것도 맞다 — **checkpoint를 붙이면 Spot으로 내려갈 수 있다.**
> 즉 **엔지니어링으로 비용 등급을 바꿀 수 있다**는 뜻이고, 이것이 이 표의 실용적 함의다.

## ⚠️ Ch4-3과의 중복

**[[AI DE Course - Part4 Ch4 GPU allocation architecture]]와 주제가 크게 겹친다.**

| 항목 | Ch4-3 | Ch5-4 |
|---|---|---|
| Full GPU / MIG / time-slicing / MPS | ✅ 비교표까지 | ✅ 요약 + 선택 기준 5문항 |
| K8s NodePool·taint·label | ✅ | ✅ + priorityClass·namespace quota |
| Spot / On-Demand | ✅ | ✅ + 판단 기준 |
| 클라우드 quota·capacity 한계 | ✅ (준비 계층) | ✅ (동적 프로비저닝의 한계) |
| **워크로드 5종별 정책 표** | ❌ | ✅ |
| **MIG 파편화** | ❌ | ✅ |
| **Karpenter류 동적 프로비저닝** | ❌ | ✅ |
| **scale-out vs scale-up 시나리오** | ✅ | ❌ |
| **MIG on K8s 재구성 절차** | ✅ | ❌ |

**강의가 두 챕터를 교차 참조하지 않는다.** 서로를 보완하는 관계인데 각자 독립적으로 서술되어,
**둘을 다 읽어야 GPU 스케줄링의 전체 그림이 나온다.**

## 기존 페이지와의 대조

- **[[GPU resource allocation]]** — 워크로드 5종별 정책, 파편화, 동적 프로비저닝의 한계 6종.
- **[[Data SLA and observability]]** — 증상/원인 지표 분리, 트러블슈팅 4단계.
- **[[Inference optimization]]** — GPU 3축 해석표. **"GPU는 마지막 수단"의 진단 도구.**
- ⭐ **[[NVIDIA Triton Inference Server]]** — **Dynamic Batching이 latency를 만드는 역설.**
  Part 2는 장점으로만 다뤘다.
- **[[Feature store]]** — feature freshness 지연의 원인 지표 6종.
- **[[Latency and throughput]]** — 사례 1 원인 B가 시소의 법칙의 서빙 설정 버전.
- **[[Redis]]** — 사례 1 원인 A("고속 캐시가 아닌 무거운 DB 쿼리로 전환")가 Ch2 캐싱 레이어의
  실패 사례다.

## 자료 품질

- ✅ ⭐ **GPU 3축 해석표(5행)** — Part 4 Ch5 최고의 산출물
- ✅ **증상 지표 / 원인 지표 분리**와 4단계 운영 원칙이 Ch5-2의 관측 4축과 일관
- ✅ **사례 1의 원인 A/B/C가 대시보드 latency 3구간과 정확히 대응** — 챕터 내부 정합성이 좋다
- ✅ **동적 프로비저닝이 해결 못하는 것 6종** — 흔한 착각을 깬다
- ✅ **Spot/On-Demand 판단 기준이 "checkpoint 가능성"**
- ✅ 워크로드 5종 정책 표의 "실패 허용" 열
- ⚠️ **Ch4-3과 상당 부분 중복** (위 표)
- ⚠️ **중복 슬라이드**: p58/p59 완전 동일(GPU 해석표), p73/p74 완전 동일(동적 프로비저닝 한계)
- ⚠️ **사례에 실제 수치나 회사가 없다** — "300ms → 1.8s" 같은 숫자는 예시용 시나리오이지 실제 사례가
  아니다. 소단원 제목이 "트러블슈팅 **사례**"인데 **가상 시나리오**다
- ⚠️ **사례 3에 대응책이 없다** — 5행 해석표는 "가능성"까지만 말하고, 각 경우에 무엇을 하는지가 없다
- ⚠️ **priorityClass의 preemption 동작이 설명되지 않는다**
- ⚠️ **gang scheduling / Kueue / Volcano 부재** — 분산 학습에서 "N개 GPU를 동시에 확보하거나
  아예 시작하지 않기"가 핵심인데 언급이 없다. Ch4-3과 같은 공백
- ⚠️ 도구는 **Karpenter만** 이름이 나온다 (Ch5-2와 같은 문제)

## 링크

- 강의: [[AI Data Engineering (Fast Campus course)]]
- 개념: [[GPU resource allocation]] · [[Data SLA and observability]] · [[Inference optimization]] ·
  [[GPU architecture]] · [[Feature store]] · [[Latency and throughput]] · [[Caching strategies]]
- 도구: [[NVIDIA Triton Inference Server]] · [[Redis]] · [[Apache Spark]]
- 앞: [[AI DE Course - Part4 Ch5 Monitoring dashboards and alerts]]
- 겹치는 챕터: [[AI DE Course - Part4 Ch4 GPU allocation architecture]]
- **Part 4의 마지막 소단원.** 다음: Part 5 (LLM·RAG, 40p) — 미인제스트

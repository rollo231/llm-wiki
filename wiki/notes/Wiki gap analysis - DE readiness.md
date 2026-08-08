---
type: note
title: Wiki gap analysis - DE readiness
area: [data-engineering]
aliases:
  - 위키 공백 분석
  - DE 준비도 진단
  - 위키 진단
  - 다음에 무엇을 읽을 것인가
tags: [data-engineering, meta, lint, roadmap, learning]
created: 2026-08-08
updated: 2026-08-08
sources:
  - "[[AI Data Engineering (Fast Campus course)]]"
  - "[[Spatial omics platform roadmap]]"
  - "[[SpatialData as a data engineering substrate]]"
---

# Wiki gap analysis - DE readiness

**질문:** 지금까지 수집한 것으로 "뛰어난 데이터 엔지니어"가 되기에 충분한가?

**답:** 개념 어휘로는 이미 설계 논쟁이 되는 수준이다. 하지만 충분하지 않고, **위키가 이미
그 이유를 스스로 적어놨다** — [[Data Engineering]] MOC의 *열린 질문* 절이 그 목록인데,
목록을 소진하는 대신 강의 완주가 먼저 실행됐다.

> **한 줄 진단: 이 위키는 "개념 → 강의 → 재구성" 축으로만 두껍다.
> 1차 자료 · 운영 도구 · 자기 측정치 세 축이 얇다.**

## 1. 위키가 반복해서 쓰고 있는 문장

[[Data Engineering]] MOC의 열린 질문에서 같은 형태가 계속 나온다.

| 지점 | 문장 |
|---|---|
| [[Feature store]] | *"재야 한다"까지 왔고 "이렇게 잰다"는 아직이다* |
| [[Inference optimization]] | *"무엇을 재는가"는 생겼고 "무엇이 그 값을 결정하는가"는 공백* |
| [[Distributed processing]] | *"재야 한다"는 있고 "이 값을 넘으면"이 없다* |
| [[Data SLA and observability]] | SLO 숫자(`p95 300ms`·`freshness 5분`)의 **도출 근거가 없다** |
| [[Spatial omics platform roadmap]] §9 | *규모 수치가 전부 가정이다 — 측정값이 아니다* |
| [[Stream processing semantics]] | *"지연 분포를 보고 정하라"면서 분포를 어떻게 재는지 없다* |

**우연이 아니라 위키 전체에서 가장 자주 나오는 결함 형태**고, 강의를 더 인제스트해도 안 채워진다.
출처가 아니라 **측정**이 없어서 생긴 구멍이기 때문이다.

## 2. 수치로 본 현재 상태 (2026-08-08)

| 층 | 장수 | 관찰 |
|---|---|---|
| `sources/` | 68 | **그중 61장이 강의 하나** ([[AI Data Engineering (Fast Campus course)]]) |
| `concepts/` | 62 | 어휘는 충분히 두껍다 |
| `entities/` | 29 | **아래 §2.2** |
| `notes/` | 2 | 적용은 두 번 해봤다 |

### 2.1 출처가 사실상 하나다

DE 영역 source의 **90%가 단일 secondary source**이고, 위키가 그 강의에 ⚠️를 열 번 넘게 달아놨다
(출처 없는 통계 배지, 회사 간 중복 수치, LSTM 연도 오류, GPT-4 파라미터 추정치의 사실화).
**DE 영역에 1차 자료는 0건이다** — Iceberg 스펙도, Kafka·Airflow 공식 문서도,
Brewer/Lamport/FLP/Raft 원문도 이름만 있다.

⭐ **반대 증거가 위키 안에 있다.** bioinformatics 쪽은 [[SpatialData]] **소스 코드를 직접 읽었고**,
그래서 나온 페이지들이 위키에서 가장 구체적이다 — `cells_as_circles` 기본값이 v0.6.0에서 바뀐 것,
MERSCOPE 이미지 백엔드가 `rioxarray` **설치 여부로** 갈리는 것. 강의에서는 절대 안 나오는 종류이고,
[[Spatial omics platform roadmap]] §1c의 버전 매트릭스가 통째로 여기서 나왔다.
**방법은 이미 증명됐는데 DE 영역에는 안 썼다.**

### 2.2 정작 매일 운영하는 도구에 페이지가 없다

| entity 페이지 있음 | entity 페이지 없음 |
|---|---|
| JanusGraph · ArangoDB · Amazon Neptune · TorchServe · Microsoft GraphRAG | **Airflow · Kubernetes · MinIO · Postgres · Iceberg · dbt · Prometheus · Zarr** |

앞줄은 [[Spatial omics platform roadmap]] §8이 *"트리거 없으면 안 한다"* 로 미뤄둔 것들이고,
뒷줄은 지금 프로덕션에서 돌아가는 것들이다. **로드맵 Phase 1이 통째로 Airflow인데 Airflow 근거
페이지가 0장이다.** 강의를 따라가면 이렇게 된다 — 강의가 다루는 것에 페이지가 생기지,
내가 쓰는 것에 생기지 않는다.

> **판별 기준: 내가 이번 주에 손댄 시스템 중 위키에 페이지가 없는 것이 몇 개인가.**

### 2.3 통째로 비어 있는 주제

grep으로 확인한 것 (2026-08-08):

| 주제 | 상태 | 왜 중요한가 |
|---|---|---|
| **SQL 실행계획·쿼리 최적화** | `쿼리 최적화` 2건 · `파티션 프루닝` 2건 | Postgres 카탈로그를 [[Spatial omics platform roadmap]]의 중심에 뒀는데 `EXPLAIN` 어휘가 없다 |
| **SCD·late-arriving data** | `SCD` **0건** | [[Dimensional modeling]]이 개념에서 멈춘다 |
| **백필 멱등성** | `백필` 10건 — 전부 다른 문맥의 언급 | Airflow 운영의 절반 |
| **데이터 품질 도구** | Great Expectations·dbt tests 개념 언급뿐 | [[Data SLA and observability]]가 도구 없이 프로세스만 |
| **비용 모델링** | `비용` 83건이지만 계산이 없다 | 로드맵 §2.3이 *"아키텍처 판단이 아니라 구매 결정"* 이라 해놓고 단가 계산이 없다 |
| **보안·PII 실무** | 거버넌스 개념만 | 멀티테넌트 제품 백엔드의 전제 |

## 3. 다음 소스 우선순위

두 축이 있고, 지금까지는 **로드맵 축**만 정해져 있었다(2026-08-02 로그: MinIO > Zarr > Iceberg).
여기에 **제너럴리스트 축**을 붙인다.

### 3.1 로드맵 축 — 지금 막혀 있는 것

1. ⭐ **MinIO 공식 문서** — 위키가 이미 "인제스트 후보 1순위"로 지목.
   [[Spatial omics platform roadmap]] §2.3·§5.1의 판단 전체가 여기 걸려 있다.
   erasure coding 오버헤드 · 소형 객체 처리 · ILM tiering · 리밸런싱.
   [[Object storage layout]]의 미검증 항목 4개도 전부 여기.
2. ⭐ **Zarr 사양 + zarr-python** — 6문항 스코프는 2026-08-02 로그에 확정돼 있다.
   **MinIO가 분모, Zarr가 분자** — 둘을 붙여야 *"파생물 2~3배 중복이 감당 가능한가"* 에 숫자가 나온다.
3. **Iceberg 스펙** — 도입할 도구가 아니라 **손으로 만드는 것의 레퍼런스 설계**로서.

### 3.2 제너럴리스트 축 — 새로 추가

4. ⭐ **Airflow 공식 문서** — 운영 중인데 0장. 스코프: backfill 멱등성 · `catchup`/`depends_on_past` ·
   dynamic task mapping · sensor · `KubernetesPodOperator` 리소스 오버라이드
   (로드맵 §2.1의 전제인데 강의 근거가 아니라 추정이다).
5. ⭐ **Prometheus + Grafana** — 위키가 *"가설이 아니라 확인된 병목"* 으로 승격시킨 공백.
   [[Spatial omics platform roadmap]] Phase 3가 여기서 끊긴다. Part 4 Ch5는 대시보드 5종을
   설계하면서 무엇으로 그리는지 말하지 않는다.
6. ⭐⭐ **DDIA (*Designing Data-Intensive Applications*, Kleppmann)** — 강의가 **이름만 대고 넘어간**
   Brewer 2000/2012 · Gilbert & Lynch · Lamport 1978 · FLP 1985 · Raft를 한 권이 다 덮는다.
   **단일 강의 의존을 깨는 가장 효율 좋은 한 방**이고, [[CAP theorem]]의 PACELC 공백과
   일관성 스펙트럼(linearizable/sequential/causal/eventual) 공백이 같이 닫힌다.
7. **Postgres 쿼리 최적화** — `EXPLAIN (ANALYZE, BUFFERS)`, 인덱스 종류, 조인 전략.
   §2.3의 가장 큰 구멍.

### 3.3 ⭐⭐ 그리고 성격이 다른 하나

8. **자기 스택의 측정치를 source로 인제스트한다.**
   샘플 크기 분포 · 리더 실행 시간 · MinIO 실제 객체 수와 IOPS · Airflow task 지속시간 분포 ·
   뷰어 줌 레벨 분포([[Spatial omics platform roadmap]] §5.1의 미검증 전제).

   인제스트 대상이 **남의 자료가 아니라 자기 시스템인 첫 source 페이지**가 된다.
   §1의 반복 문장을 닫는 유일한 방법이고, 위키를 *강의 정리본*에서
   *이 팀의 엔지니어링 지식*으로 바꾸는 지점이다.

   > `raw/`가 gitignore이므로 측정치 원본은 로컬에, **수치와 해석은 source 페이지에** 남는다 —
   > 공개 repo에 올릴 수 없는 값은 상대 비율·분포 형태로 옮긴다.

## 4. 이 노트를 언제 폐기하나

진단은 유효기간이 있다. 아래가 참이 되면 이 노트는 갱신 대상이다.

- [ ] DE 영역 source 중 **1차 자료가 5장 이상**
- [ ] `entities/`에 **Airflow · MinIO · Prometheus · Postgres** 페이지 존재
- [ ] `sources/`에 **자기 시스템 측정치 기반 페이지가 1장 이상**
- [ ] [[Data Engineering]] MOC 열린 질문 중 ⭐ 표시 항목의 **절반 이상이 ✅**
- [ ] [[Spatial omics platform roadmap]] §9의 미검증 6항목 중 **3개 이상 해소**

## 5. 유보 — 이 진단이 틀릴 수 있는 지점

- **"1차 자료가 낫다"는 위키 안에서 SpatialData 사례 하나로 증명됐다.** 표본 1개다.
  DE 쪽 공식 문서가 같은 밀도를 줄지는 해봐야 안다(벤더 문서는 마케팅이 섞인다).
- **강의의 가치를 과소평가했을 수 있다.** [[AI DE Course - Part4 Ch1 CAP theorem and system limits]]와
  [[AI DE Course - Part5 Hybrid search and reranking]]은 출처가 좋고 검산도 통과했다.
  나쁜 것은 **평균**이지 전부가 아니다.
- **§2.2의 "안 쓰는 도구" 판정은 현재 로드맵 기준이다.** 그래프·RAG 쪽이 제품 요구로 들어오면
  뒤집힌다.

## 링크

- 영역 MOC: [[Data Engineering]] — **열린 질문 절이 이 노트의 원재료다**
- 자매 노트: [[Spatial omics platform roadmap]](적용) · [[SpatialData as a data engineering substrate]](포맷)
- 진단 대상: [[AI Data Engineering (Fast Campus course)]]

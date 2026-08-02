---
type: note
title: Spatial omics platform roadmap
area: [bioinformatics, data-engineering]
aliases:
  - 공간 오믹스 플랫폼 로드맵
  - 공간 전사체 플랫폼 아키텍처
  - spatial omics platform architecture
  - 플랫폼 로드맵
  - 아키텍처 평가
tags: [spatial-omics, data-engineering, architecture, roadmap, multi-tenant, minio, airflow, kubernetes, postgres]
created: 2026-08-02
updated: 2026-08-02
sources:
  - "[[spatialdata-io docs - README and readers]]"
  - "[[SpatialData docs - Design doc]]"
  - "[[SpatialData source - Spatial and relational queries]]"
  - "[[AI DE Course - Part4 Ch1 Distributed processing basics]]"
  - "[[AI DE Course - Part4 Ch2 Caching strategies and TTL]]"
  - "[[AI DE Course - Part4 Ch5 AI system metrics and SLA]]"
  - "[[AI DE Course - Part3 Ch1 Semantics]]"
---

# Spatial omics platform roadmap

**질문:** 플랫폼을 [[Xenium]]·[[Visium]]·[[MERSCOPE]] 3종으로 한정하고, 현재 스택
(K8s · Airflow · MinIO · Postgres)에서 **내부 R&D 분석 + 멀티테넌트 제품 백엔드**를 함께 지탱하려면,
정석 아키텍처 패턴을 **어떤 순서로** 도입해야 하는가?

**답:** 정석은 **도입 목록이 아니라 도입 순서**다. [[AI Data Engineering (Fast Campus course)]]가
매 챕터 "안 해도 되는 경우"를 먼저 말하는 게 우연이 아니다 — *"분산의 출발점은 데이터가 크다가
아니라 단일 서버로 감당 가능한가"*([[Distributed processing]]) · *"GPU는 마지막 수단"*
([[Inference optimization]]) · *"Feature Store는 마지막 수단"*([[Feature store]]) ·
*"OWL은 필요한 경우가 제한적"*([[Ontology]]). 같은 형태의 판단이 네 번 반복된다.

정렬 축은 하나 — **되돌릴 수 있는가.** 그리고 현재 스택 기준으로 **Phase 0·1에 새 인프라는 0이다.**

> ⚠️ §1~2는 위키 소스에 근거한다. §3 이후는 **설계 제안(의견)** 이며 이 스택에서 측정된 바가 아니다.
> **MinIO 관련 판단은 위키에 1차 소스가 없다** — §9에 모아 표시했다.

## 0. 전제

| 축 | 확정값 |
|---|---|
| 플랫폼 | [[Xenium]] · [[Visium]] · [[MERSCOPE]] 3종 (**[[Visium HD]] 제외**) |
| 소비자 | ① 내부 R&D 분석 ② 멀티테넌트 제품 백엔드 |
| 규모 | 수천 샘플, 월 수백 건 유입 |
| 스택 | K8s · Airflow · MinIO · Postgres (Airflow metaDB와 도메인 metaDB는 **인스턴스까지 분리됨**) |

월 300건 기준이면 **시간당 0.4건**이다. 이 한 줄이 §8의 절반을 결정한다.

## 1. "3개 플랫폼"이 아니라 2개 워크로드다

| | [[Visium]] | [[Xenium]] | [[MERSCOPE]] |
|---|---|---|---|
| 측정 단위 | spot | 단분자 | 단분자 |
| Points | **없음** | 수억 행 | 수억 행 (**CSV 원본**) |
| Labels (래스터 마스크) | 없음 | ✅ `cell_labels`·`nucleus_labels` | **없음 — 폴리곤만** |
| 이미지 | full/hires/lowres 3장 | 멀티채널 morphology (+H&E·IF) | **stain × z-layer** 다중 |
| 좌표계 | **3개, 이름에 `dataset_id` 박힘** | `global` 1개 (px, 0.2125 µm) | `global` 1개 (Affine, 파일에서) |
| 기본 청크 | full 이미지 4단 피라미드 | — | **`(1, 4096, 4096)`**, 4단 |

세 결론이 따라 나온다.

### (a) "모든 샘플이 `global` 좌표계" 가정이 Visium에서 깨진다

[[Visium]]만 좌표계 이름이 데이터셋마다 다르다(`<id>` · `<id>_downscaled_hires` ·
`<id>_downscaled_lowres`). 크로스-샘플 코드를 쓰려면 silver에서 **좌표계 이름을 정규화**해야 한다.

더 나아가 [[Xenium]]·[[MERSCOPE]]는 둘 다 픽셀 좌표계인데 **픽셀 크기가 서로 다르다.**
→ **µm canonical 좌표계를 silver에서 강제로 하나 추가한다.** 안 하면 "이 영역 몇 µm²"가
플랫폼 간 비교 불가능해진다. [[Coordinate systems and transformations]]의 extrinsic 좌표계를
이 용도로 쓰는 것.

### (b) "세포"의 정본 표현이 플랫폼마다 다르다

[[Xenium]] 리더 docstring은 *분석에는 폴리곤이 아니라 래스터를 쓰라*고 명시한다(폴리곤은 시각화용
단순화). 그런데 **[[MERSCOPE]]엔 래스터 자체가 없다.** 세 플랫폼 공통의 세포 표현은 폴리곤뿐이고,
그건 Xenium에서 권장되지 않는 쪽이다.

이건 배관 문제가 아니라 **의미 결정**이다 → §7 metric contract.

### (c) N×M 컨버터 문제가 사라진 자리에 유한한 버전 매트릭스가 남는다

3종이면 이걸 **CI 픽스처로 고정할 수 있다.** 13종 지원이었으면 불가능하고, 3종이라 가능하다 —
**플랫폼 고정의 실제 배당금은 이것이다.**

| 플랫폼 | 매트릭스 축 |
|---|---|
| [[Xenium]] | XOA `<1.3.0` / `1.3.0–1.x` / `2.0.0+` / **2.0.0 초기 빌드 버그**(핵 경계 스킵) / `xeniumranger` 재세그멘테이션 |
| [[MERSCOPE]] | VPT 유무 × cellpose/watershed × `z_layers` × **`rioxarray` vs `dask_image` 백엔드** |
| [[Visium]] | SpaceRanger 1/2 × 헤더 변종 × `.btf` |

⚠️ 그중 둘은 **재현성을 조용히 깨는 종류**다:

- MERSCOPE 이미지 백엔드는 *"명시하지 않으면 `rioxarray` 설치 여부에 따라"* 결정된다 —
  **같은 코드가 환경마다 다른 경로를 탄다.**
- [[spatialdata-io]] v0.6.0에서 `cells_as_circles` 기본값이 바뀌었고, 원 반지름 기준이
  **핵 면적 → 세포 면적**으로 바뀌었다. 과거 스크립트를 재실행하면 결과가 달라진다.

→ **카탈로그에 `spatialdata_io_version` 문자열만으로는 부족하다.** §3-6 참고.

## 2. 현재 스택 평가

| 층 | 현재 | 판정 | 근거 |
|---|---|---|---|
| 오브젝트 스토리지 | **MinIO** | ✅ 적합 | Zarr는 서버 없이 range GET으로 읽힌다. S3 호환이면 충분 |
| 오케스트레이션 | **Airflow** | ✅ 적합 | 작업 단위가 "샘플 1개"인 coarse-grained fan-out. [[Batch and stream processing]]의 *"오케스트레이터는 배치 전용"* 경계와 정확히 일치 |
| 실행 | **K8s** | ✅✅ **이미 두 워크로드 클래스를 푼다** | 아래 §2.1 |
| 메타데이터 | **Postgres** (인스턴스 분리) | ✅✅ **기존 노트의 제안보다 낫다** | 아래 §2.2 |
| 온라인 서빙 | — | Phase 2에서 추가 | 타일 서버 |
| 캐시 | — | Phase 2에서 추가 | 타일 캐시 |
| 관측성 | — | Phase 3에서 추가 | SLI 수집 |

**전체 로드맵에서 새로 들어오는 컴포넌트는 이 셋뿐이다.** 나머지는 전부 규약과 코드다.

### 2.1 K8s가 "3자릿수 규모 격차" 문제를 이미 푼다

§1의 [[Visium]](수 GB) vs [[Xenium]]·[[MERSCOPE]](수십 GB) 격차는 **별도 파이프라인 없이**
`KubernetesPodOperator`의 per-task resource override + dynamic task mapping으로 끝난다.
같은 DAG·같은 코드에 pod spec만 플랫폼별로 다르게 준다.

[[Distributed processing]]의 *"필요한 축만 분산"* 의 정확한 실행이고, **§8의 분산 트리거를 더
멀리 밀어낸다** — 노드 하나를 크게 키우는 게 프레임워크 도입보다 항상 먼저다.

### 2.2 ⚠️ 정정 — 카탈로그는 Iceberg가 아니라 Postgres다

[[SpatialData as a data engineering substrate]] §4는 카탈로그를 **Iceberg**로 설계했다.
**그 판단은 틀렸고, 현재 스택이 이미 옳은 쪽에 있다.**

`stores` 테이블의 성질을 보면:

| 성질 | 값 | 함의 |
|---|---|---|
| 행 수 | 수천 | 컬럼너·파티셔닝의 이득이 없다 |
| 필요한 보장 | promote 트랜잭션 하나 | Postgres가 더 잘 준다 |
| 동시 writer | 소수 (DAG task) | 낙관적 동시성 제어가 과잉 |
| 접근 패턴 | 조인·점 조회·상태 업데이트 | **OLTP다** |

[[Analytical data storage tiers]]의 OLTP/OLAP 구분이 이 판단을 그대로 준다. 기존 노트는
"레이크하우스 층위"라는 프레임에 갇혀 **카탈로그까지 레이크 쪽으로 밀었다.**

게다가 Postgres가 이미 있으므로 카탈로그 테이블 추가는 **새 시스템 도입이 아니다** —
[[NoSQL]]의 *"운영 포인트는 줄지 않고 분산된다"* 를 치르지 않고 정석을 얻는다.
Iceberg를 넣었으면 metastore가 또 필요했다.

**Iceberg가 맞는 자리는 gold의 큰 팩트 테이블**(transcript, cell obs)이고, 그건 §8이다.

#### ⭐ 다만 — 우리가 만드는 것이 사실 Iceberg의 *아이디어*다

Iceberg를 **쓰지** 않기로 한 것이지 그 설계를 버린 게 아니다. 카탈로그를 Iceberg 옆에 놓으면
**같은 구조**다:

| Iceberg | 이 설계의 Postgres 카탈로그 |
|---|---|
| 스냅샷 커밋 | `is_current` 플립 트랜잭션 (§4.7) |
| 매니페스트 리스트 → 매니페스트 → 데이터 파일 | `stores` → `store_elements` |
| 데이터 파일 경로 (**불투명**) | `store_uri` (**불투명**, §3.1) |
| 파일별 컬럼 통계 min/max → 열기 전 프루닝 | `extent` bbox → **store 열기 전 공간 프루닝** |
| *hidden partitioning* (경로에 파티션 값 없음) | 경로 = 권한·생애주기만 |
| 스냅샷 이력 = time travel | `superseded_at` 이력 |
| 파일 목록 ≠ 디렉토리 리스팅 | `_manifest.json` + 카탈로그 |

**차이 하나는 정직하게 짚어둔다.** Iceberg는 프루닝 후 **엔진이 바로 스캔**한다. 여기서는
프루닝 후 **파이썬 프로세스가 store를 연다** — [[SpatialData]] store는 쿼리 엔진이 읽을 수 없는
불투명 blob이기 때문이다. 즉 **이 카탈로그는 쿼리 플래너가 아니라 작업 스케줄러의 입력**이다.
그래서 SQL로 답해야 하는 것은 gold로 따로 물질화해야 한다 — 카탈로그가 그 역할까지 하지는 못한다.

배경과 Hive와의 대비는 [[Table formats]] · [[Object storage layout]].

### 2.3 MinIO 자체 호스팅이 파생물 전략을 제약한다

**"스토리지는 컴퓨트보다 싸다"는 S3에서 참이고 MinIO에서는 조건부다.** S3는 남의 디스크지만
MinIO는 사서 꽂아야 한다.

수천 샘플 × 수십 GB = 논리 수백 TB. erasure coding 오버헤드가 곱해지고, 여기에 파생물 2~3배
중복을 그대로 하면 PB 급이 된다. **이건 아키텍처 판단이 아니라 구매 결정이다.**

두 가지가 따라온다 → §5(계층적 피라미드) · §9(small files의 우선순위 상승).

## 3. Phase 0 — 되돌릴 수 없는 것 (새 인프라 0)

나중에 하면 **이미 처리한 수백 TB를 전부 다시 돌려야 하는** 것들. 여섯 개고, 전부 규약이다.

| # | 결정 | 나중에 하면 드는 비용 |
|---|---|---|
| 1 | 식별자 체계 — `tenant_id` / `sample_id` / `store_id = sample:pipeline_ver` | 모든 링크·경로 재작성 |
| 2 | **경로 규약 = 테넌트 격리 경계** | 오브젝트 스토리지의 "이동"은 복사다. 수백 TB |
| 3 | **µm canonical 좌표계** (§1a) | 기존 파생물이 전부 픽셀 기준 → 전량 재처리 |
| 4 | 불변성 규약 — 제자리 수정 금지 · `formats=` 명시 | 과거 데이터가 조용히 오염됨. **복구 불가** |
| 5 | bronze read-only + 체크섬 | 재처리 자체가 불가능해짐 |
| 6 | **리더 결정성 pinning** | "이 결과가 어떻게 나왔나"를 영영 못 답함 |

### 3.1 경로 규약 (#2 상세)

**격리의 비대칭이 출발점이다.** 내부 R&D는 크로스-샘플 질의를 원하고, 제품 테넌트는 서로를 보면
안 된다. **한 축으로 풀면 반드시 하나가 깨진다.**

> **바이트는 물리적으로 격리**(테넌트별 prefix/버킷 = IAM 경계),
> **메타데이터는 논리적으로 격리**(단일 카탈로그 + `tenant_id` + 뷰).

카탈로그를 테넌트별로 쪼개는 순간 내부 R&D가 죽는다. 반대로 스토리지를 안 쪼개면 격리를 **강제할**
방법이 없다 — 오브젝트 스토리지의 권한 단위는 prefix/bucket이다.

일반 원칙은 [[Object storage layout]]에 따로 정리했다 — **경로는 "누가 접근할 수 있고 언제
지워도 되는가"만 답하고 나머지는 카탈로그가 답한다.** 그 원칙을 이 도메인에 적용하면:

```
bronze/    버킷 · read-only · 버저닝 on · 장기 보존
  <tenant_id>/<platform>/<run_id>/…벤더 원본 그대로…

staging/   버킷 · ILM 7일 후 자동 삭제
  <dag_run_id>/<sample_id>.zarr/

silver/    버킷 · 불변 · 백업 대상
  <tenant_id>/<sample_id>/<pipeline_version>/sample.zarr/
                                            /_manifest.json

derived/   버킷 · 재생성 가능 → 백업 제외
  <tenant_id>/<sample_id>/<pipeline_version>/tiles/
                                            /transcripts/

gold/      버킷 · Parquet 테이블 (여기서만 Hive 파티셔닝이 의미 있다)
```

**결정 넷:**

- ⭐ **`derived/`를 `silver/`에서 뗀다.** 백업 정책이 정반대다 — silver는 지켜야 하고 derived는
  정의상 언제든 버려도 된다(§5). 같은 버킷이면 **백업 비용이 파생물 배수만큼 곱해진다.**
  §2.3의 MinIO 용량 문제에 대한 가장 직접적인 대응.
- **`<pipeline_version>`이 경로에 있어야 blue/green 재처리가 공짜다** — 새 버전을 옆에 쓰고
  카탈로그 포인터만 뒤집는다.
- **`<tenant_id>`가 첫 세그먼트** → IAM 정책이 `bucket/<tenant_id>/*` 한 줄.
- **`platform`이 bronze에만 있다.** 원칙: *카탈로그 행이 생기기 **전에** 도착하는 데이터만 경로가
  자기설명적이어야 한다.* bronze는 파일이 먼저 떨어지고 리더 선택이 platform으로 결정되므로
  기능적 정보다. silver 이후는 카탈로그가 항상 먼저 있으므로 경로에서 뺀다.

**버킷을 무엇으로 나누나 — layer = 버킷, tenant = prefix.** 버킷이 통제하는 건 정책(버저닝·ILM·
보존)인데 **정책이 실제로 갈리는 축이 layer**다. 테넌트마다 복제하면 drift가 생기고, layer는
5개로 고정인 반면 테넌트는 계속 는다.
**뒤집는 조건은 하나 — 테넌트별 용량 quota가 필요하면** quota가 버킷 단위이므로 tenant = 버킷.

**경로에 없는 것:** 프로젝트 · 질환 · 조직 · 날짜 · 실험자 · (silver 이후의) 플랫폼.
전부 카탈로그 컬럼이다. 특히 **날짜 파티셔닝은 gold의 Parquet에만** — 샘플 단위 접근은 항상
ID로 하고 시간 질의는 카탈로그가 답한다.

**`_manifest.json`이 선택이 아닌 이유:** Zarr는 청크가 개별 객체라 store 하나 아래 객체가
수백만 개가 된다. 그러면 **목록을 `list-objects`로 얻는 게 실용적으로 불가능**해지고 GC·정합성
검사·용량 집계가 전부 막힌다. [[SpatialData as a data engineering substrate]] §4.8은 이걸
*카탈로그 재구축용*으로 뒀는데, **더 강한 이유는 열거 비용**이다.

### 3.2 리더 pinning (#6 상세)

§1c의 두 함정 때문에 버전 문자열로는 재현이 안 된다. 카탈로그에 박아야 하는 것:

- **컨테이너 이미지 다이제스트** (MERSCOPE 백엔드가 설치 여부로 갈리므로 **환경까지** 고정 대상)
- **리더 kwargs 전량** (`cells_as_circles`, `z_layers`, `vpt_outputs`, `dataset_id`, …)
- `vendor_software_version` (XOA / VPT / SpaceRanger)

### 3.3 기존 카탈로그 스키마의 delta

도메인 metaDB가 이미 있으므로 **신규 구축이 아니라 확장**이다. 실제 delta는 이게 있는지 여부:

- [ ] `pipeline_version` · `pipeline_git_sha` — store 단위 계보
- [ ] **컨테이너 이미지 다이제스트 + 리더 kwargs 전량** (§3.2)
- [ ] **element별 포맷 버전** — 단일 "포맷 버전" 컬럼으로는 표현이 안 된다
      ([[SpatialData Zarr format versions]])
- [ ] `vendor_software_version`
- [ ] `is_current` 상태 기계 + promote 트랜잭션
- [ ] `extent` — 카탈로그 레벨 공간 프루닝 (store를 열기 전에 bbox 교차 판정)
- [ ] `tenant_id`

컬럼 상세는 [[SpatialData as a data engineering substrate]] §4.2~4.3을 그대로 쓰되,
**저장 위치만 Iceberg → Postgres로 읽는다**(§2.2).

## 4. Phase 1 — 파이프라인 정석 (새 인프라 0)

[[Medallion architecture]] + Airflow. 샘플 1개 DAG의 골격은
[[SpatialData as a data engineering substrate]] §3과 같고, **`validate`가 `promote` 앞에** 있는
것이 핵심이다 — 원자성 없는 포맷에서 유일한 방어선.

3종 고정이 여기서 두 가지를 더 준다.

### 4.1 골든 픽스처 세트 ⭐

§1c의 버전 매트릭스 조합별로 **작은 실제 샘플**을 픽스처로 두고 CI에서 돌린다.
**리더 업그레이드 = 픽스처 diff.** 픽스처 바이트는 MinIO에 두면 되므로 새 인프라가 없다.

이게 [[Data and model versioning]]의 재현성 3요소를 이 도메인에서 실제로 실행하는 방법이다.

### 4.2 리더 경고를 실패로 승격 ⭐

세 플랫폼 **전부** "경고 내고 계속" 경로가 있다:

| 플랫폼 | 조용히 넘어가는 지점 |
|---|---|
| [[MERSCOPE]] | 구성요소 파일이 없으면 **경고만 내고 element를 스킵** |
| [[Xenium]] | `cell_id` 교차검증(zarr·parquet·h5 샘플링 비교) 불일치 시 경고 |
| [[Visium]] | `dataset_id` 추론 실패·불일치 시 경고 |

[[Data SLA and observability]]의 **침묵의 실패**가 여기 그대로 해당한다. 세 경고 모두
**validation gate에서 실패로 승격**해야 한다. 로그로 흘리면 반쯤 빈 store가 `current`가 된다.

## 5. Phase 2 — 제품 경로 (트리거: 뷰어 오픈)

여기서 **정본 1 + 재생성 가능한 파생물** 구조가 시작된다. silver store는 불변 정본 하나로 두고,
뷰어용 타일 피라미드를 **파생**으로 만든다.

> **왜 "정본을 층별로 분해"가 아니라 "정본 1 + 파생"인가:** 정본이 여러 개면 **정합성이 새로운
> 보장 대상**이 된다 — [[Feature store]]가 offline/online 두 스토어를 두는 순간 마주친 바로 그
> 함정이다. "정본 1 + 재생성 가능한 파생물 N"은 정합성 문제를 **재생성으로 환원**한다.
> 그리고 되돌릴 수 있다 — 파생물을 지우면 원래 구조다.

### 5.1 계층적 피라미드 물질화 (MinIO 제약 반영)

[[MERSCOPE]] 기본 청크 `(1, 4096, 4096)`에서 512² 타일 하나를 뽑으려면 **64배를 읽는다.**
그렇다고 전 해상도를 뷰어용 청킹으로 한 벌 더 쓰면 §2.3의 용량 문제가 터진다.

| 피라미드 레벨 | 처리 | 근거 |
|---|---|---|
| 상위(축소) 레벨 | 뷰어용 작은 청크로 **미리 물질화** | 전체 용량의 수 %. 뷰어 요청의 대부분이 여기 |
| 최하위(원본 해상도) | **온디맨드로 잘라 캐시에만** | 용량의 대부분. 최대 확대 요청은 소수 |

[[Hybrid search and reranking]]의 **Two-Stage Retrieval**과 같은 형태의 판단이다 —
*싼 것을 전부에, 비싼 것은 소수에만.* [[Caching strategies]]·[[Inference optimization]]의
*"GPU는 마지막 수단"* 도 같은 골격.

### 5.2 이 도메인의 캐시는 교과서에서 제일 쉬운 케이스다

silver store가 **불변**이므로 타일도 불변이다. 캐시 키에 `store_id`(= `sample:pipeline_version`)를
넣으면 **무효화 문제가 존재하지 않는다.**

→ TTL 불필요 · 무효화 전략 불필요 · stampede 대응 불필요.
[[Caching strategies]]의 어려운 절반이 통째로 사라진다. **불변성 규약(§3 #4)이 여기서
배당금을 낸다.**

### 5.3 업로드 알림은 큐이지 스트림 처리가 아니다

[[Message broker]]의 구분 — 필요한 건 전달 보장이지 윈도우·워터마크가 아니다.
[[Stream processing semantics]]는 여기 들어오지 않는다.

## 6. Phase 3 — 운영 정석 (트리거: 외부 사용자)

Phase 2와 거의 동시. [[Data SLA and observability]]의 SLI/SLO 4단계를 적용한다.

| SLI | 측정 |
|---|---|
| freshness | 업로드 → 조회 가능 시각 |
| 처리 성공률 | DAG run 성공 / 전체 |
| 타일 p95 | 뷰어 응답 |
| validation 통과율 | promote 전 게이트 |

### 6.1 ⭐ label을 플랫폼별로 나눠야 한다

[[Visium]] 5분과 [[Xenium]] 4시간을 **한 SLO로 묶으면 지표가 무의미해진다.** Visium이 압도적
다수면 평균이 Visium을 따라가고, Xenium 전체가 멈춰도 SLO는 초록색이다.

[[Data SLA and observability]]의 **"전체는 정상, 부분은 장애"** label 설계가 이 도메인에서
교과서적으로 들어맞는 지점.

### 6.2 여기로 내려온 판단 하나

Airflow metaDB와 도메인 metaDB는 **인스턴스까지 분리돼 있다.** 스케줄러가 R&D 크로스-샘플 스캔에
굶는 문제는 구조적으로 없다. 남는 건 도메인 DB 자체의 부하 특성(짧은 promote 트랜잭션 vs 긴
분석 스캔)이고, **그건 관측 후 판단할 문제**이지 Phase 0이 아니다 — 행이 수천 개라 나중에
읽기 복제본을 붙이든 분리하든 `pg_dump` 한 번이다.

## 7. Phase 4 — 의미 계층, 최소한만 (트리거: 두 번째 소비자)

[[Data semantics]]의 *"같은 회사에서 매출 숫자가 3개 이상 나오는 이유"* 가 이 도메인에선 은유가
아니라 **확정된 사실**이다:

| 지표 | 플랫폼별로 실제로 다른 것 |
|---|---|
| **세포 수** | [[Visium]] = spot 수 / [[Xenium]] = 래스터 마스크 수 **vs** 폴리곤 수 / [[MERSCOPE]] = `z_index==0` 필터 후 폴리곤 수 |
| **면적** | px² vs µm² (플랫폼마다 픽셀 크기가 다름 — §1a) |
| **세포 반지름** | [[Xenium]] `cell_circles` = √(area/π) — **실제 형태가 아니고**, v0.6.0 이전엔 **핵** 면적 기준 |

정석의 **최소 형태**는 온톨로지도 그래프도 아니다 — **gold 뷰 + 한 페이지 metric contract.**
[[Ontology]]의 절제 원칙(*"테이블 = 클래스, 컬럼 = 속성으로 그대로 옮기는 것이 가장 흔한 실수"*)이
여기 적용된다. 엔티티가 ~10종이고 리니지가 3단(bronze→silver→gold)이면 [[Knowledge graph]]는
과설계다.

## 8. Phase 5 — 조건부. 트리거 없으면 안 한다

| 정석 패턴 | 도입 트리거 | 지금 아닌 이유 |
|---|---|---|
| [[Table formats\|Iceberg]] (gold 팩트) | transcript 테이블이 단일 노드 DuckDB로 안 될 때 | 카탈로그엔 부적합(OLTP, §2.2) |
| **분산 처리** ([[Apache Spark]]·Ray) | **샘플 1개가 단일 노드에 안 들어갈 때** | 병렬성이 샘플 축에 있고 K8s pod fan-out으로 끝(§2.1) |
| 스트리밍 ([[Apache Kafka]]+[[Apache Flink]]) | 이벤트 시간·윈도우·워터마크가 실제로 필요할 때 | **시간당 0.4건** |
| [[Feature store]] | 온라인 추론 + skew 발생 | 소비자에 ML 학습·추론 없음 |
| [[Knowledge graph]]·[[Ontology]] | 리니지 4단 이상 + 다중 소스 조인 | 3단 · 엔티티 ~10종 |
| [[Vector database]]·[[Retrieval-augmented generation\|RAG]] | 자연어 질의 소비자 | 없음 |
| GPU ([[GPU resource allocation]]) | 세그멘테이션 재실행·딥러닝 | ETL 자체엔 불필요. K8s가 있으니 device plugin만 붙이면 됨 |

**핵심은 §6의 관측성이 이 표의 트리거 신호를 만든다는 것이다.** "언제 분산할까"를 감으로 정하지
않고 지표가 말하게 한다 — **로드맵이 자기 자신을 구동한다.**

### 8.1 transcripts — 가장 먼저 트리거가 올 곳

[[Spatial queries in SpatialData]]에서 확인된 대로 **points는 어느 경로로 접근하든 전량
`.compute()` 한다.** [[Xenium]]·[[MERSCOPE]] 규모(수억 행)에서 이게 먼저 터질 가능성이 높다.

우회로: **transcripts를 store 밖에 공간 파티션 Parquet으로 한 벌 더 둔다**(sample_id + 공간
그리드). 그러면 [[SpatialData]]가 구조적으로 못 주는 points 프루닝이 **포맷 바깥에서 공급된다.**
파티션 프루닝은 DuckDB가 준다.

이건 [[SpatialData as a data engineering substrate]] §7의 *"❌ cell × gene 행렬을 웨어하우스로
밀어넣기"* 와 모순되지 않는다 — transcript는 행렬이 아니라 **긴 이벤트 테이블**이고 이미 Parquet이
자연스러운 모양이다([[MERSCOPE]]는 CSV라 변환 이득이 더 크다).

## 9. 미검증 — 확인해야 할 것

- ⭐ **MinIO 1차 문서가 위키에 없다.** §2.3·§5.1의 판단 전체가 일반적 성질에 기댄 것이다.
  실제 배포의 **erasure coding 설정 · 드라이브 구성 · 소형 객체 처리 · ILM tiering 가능 여부**로
  검산해야 한다. → **인제스트 후보 1순위.**
- ⭐ **small files 문제의 우선순위가 S3보다 높다.** [[SpatialData as a data engineering substrate]]
  §1이 경고한 "수백만 객체"는 S3에선 남의 문제지만 **MinIO에선 내 드라이브 IOPS와 메타데이터
  부하**다. 현재 경로는 **청크를 의도적으로 크게 잡는 것**이고, 이건 선택이 아니라 필수가 된다.
  - ⚠️ **다만 "sharding이 미완"은 [[SpatialData]] 로드맵 기준이다 — Zarr 사양·zarr-python 기준이
    아니다.** 둘은 다른 질문이다: **write 시점에 SpatialData를 우회해 직접 샤딩할 수 있는가**가
    열려 있고, 되면 객체 수가 자릿수로 줄어 자체 호스팅에서 바로 비용이다.
    → **Zarr 사양 + zarr-python 인제스트 후보**(consolidated metadata가 `_manifest.json`을
    대체하는지, 어떤 연산이 LIST를 요구하는지도 같은 스코프).
- **관측성 도구 선택에 위키 근거가 없다.** [[Data Engineering]] MOC 열린 질문에 이미 적혀 있듯
  *"Part 4 Ch5는 대시보드 5종을 설계하면서 무엇으로 그리는지 말하지 않는다."*
  K8s를 쓰니 Prometheus + Grafana가 자연스럽지만 **강의 밖 지식이다.**
- **규모 수치가 전부 가정이다** — "샘플당 수 GB / 수십 GB", "논리 수백 TB", "시간당 0.4건"은
  §0의 전제에서 나온 산술이지 측정값이 아니다. Phase 0에서 실제 분포를 재는 게 먼저다.
- **뷰어 요청의 줌 레벨 분포**를 모른다. §5.1의 "최대 확대 요청은 소수"가 이 설계의 전제인데
  **측정 전이다.** 틀리면 캐시 미스율이 치솟는다.
- **Xenium 래스터 vs MERSCOPE 폴리곤의 세포 수 차이가 실제로 얼마나 되는지** 정량 자료가 없다
  (§1b·§7). metric contract를 쓰려면 이 값이 필요하다.

## 링크

- **자매 노트** — [[SpatialData as a data engineering substrate]]: 이 노트가 *언제 무엇을*라면
  저쪽은 *포맷이 무엇을 주고 안 주는가*. §2.2에서 저쪽 §4를 정정한다.
- 플랫폼: [[Xenium]] · [[Visium]] · [[MERSCOPE]] · 리더 [[spatialdata-io]]
- 포맷: [[SpatialData]] · [[SpatialData Zarr format versions]] ·
  [[Coordinate systems and transformations]] · [[Spatial queries in SpatialData]]
- 정석 패턴 근거: [[Medallion architecture]] · [[Analytical data storage tiers]] ·
  **[[Object storage layout]]**(§3.1의 일반 원칙) · [[Table formats]] ·
  [[Distributed processing]] · [[Caching strategies]] ·
  [[Data SLA and observability]] · [[Data semantics]] · [[Ontology]] · [[Feature store]] ·
  [[Message broker]] · [[Data and model versioning]] · [[Hybrid search and reranking]]
- 영역 MOC: [[Bioinformatics]] · [[Data Engineering]]

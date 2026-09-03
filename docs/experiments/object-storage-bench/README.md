# 오브젝트 스토어 측정 하네스

**제품 중립.** 백엔드를 갈아끼워도 같은 스크립트가 돈다 — 그래야 숫자가 비교 가능해진다.

**Ran on**: 2026-08-08 · 이 기계(MacBook, 32 GB RAM / 10 cores · macOS) · Docker Desktop,
named volume · 로컬 SSD · concurrency 16.

**이 디렉토리는 버전 관리된다** — `docs/experiments/<slug>/` 규약. 원래 `raw/data-engineering/`
아래 있었고 README 도 *"버전 관리되지 않는다"* 고 적고 있었으나, `raw/` 는 gitignore 여서
**하네스와 결과가 함께 사라질 자리**였다. 규약이 2026-08-19 에 스키마로 들어온 뒤
**2026-09-03 린트에서 이관**했다. 이 수치를 인용하는 위키 페이지는 이 경로를 함께 적는다.

## 왜 이걸 만들었나

위키에 반복되는 결함 형태가 하나 있다 — ***"재야 한다"는 있고 "이렇게 잰다"가 없다***
([[Wiki gap analysis - DE readiness]] §1). 이 하네스는 그 목록을 실제로 소진하는 도구다.

| 재는 것 | 어느 열린 질문에서 왔나 |
|---|---|
| ⭐⭐ 어떤 SpatialData/Zarr 연산이 LIST 를 요구하나 | Zarr 6문항 (2026-08-02 로그) |
| 객체 크기별 처리량 | 로드맵 §9 — *"수백만 객체는 MinIO 에선 내 드라이브 IOPS"* |
| full listing 비용의 기울기 | 로드맵 §3.1 — *`_manifest.json` 이 선택이 아닌 이유* |
| range GET 이 실제로 싼가 | `Spatial queries in SpatialData` 의 전제 |
| 버킷 수 한계 · quota 단위 | `Object storage layout` 미검증 4항목 |

## 준비

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 백엔드 띄우기

```bash
docker compose --profile rustfs up -d    # http://localhost:9000  console :9001
docker compose --profile minio  up -d    # http://localhost:9010  console :9011
```

둘을 동시에 띄워도 포트가 안 겹친다 — **같은 기계에서의 A/B 가 이 하네스의 유일한 유효 출력**이기
때문에 그렇게 잡았다.

| 프로파일 | 이미지 (2026-08-08 핀) | 자격증명 |
|---|---|---|
| `rustfs` | `rustfs/rustfs:1.0.0-beta.12` | `rustfsadmin` / `rustfsadmin` |
| `minio` | `pgsty/minio:RELEASE.2026-08-04T00-00-00Z` | `minioadmin` / `minioadmin` |

> ⚠️ **RustFS 는 1.0.0 GA 가 아니다.** upstream 이 **Distributed Mode · Lifecycle · KMS** 를
> "Under Testing" 으로 표시한다. 여기서 재는 것은 **단일 노드 S3 동작뿐**이고,
> 그 세 축은 이 하네스로 판단하면 안 된다.
>
> ℹ️ `pgsty/minio` 는 아카이브된 `minio/minio` 의 커뮤니티 포크(AGPLv3)다. 온디스크 포맷·S3 API·
> `MINIO_*` 환경변수가 upstream 과 동일하다고 표방한다.

## 벤치 돌리기

```bash
python bench.py --label rustfs-1.0.0-beta.12 \
    --endpoint http://localhost:9000 --access-key rustfsadmin --secret-key rustfsadmin

python bench.py --label minio-2026-08-04 \
    --endpoint http://localhost:9010 --access-key minioadmin --secret-key minioadmin

python compare.py results-*.json > comparison.md    # 위키에 붙일 표
```

기본 스코프는 `size-sweep` · `list-scale` · `range-get`. 버킷 테스트는 명시해야 돈다:

```bash
python bench.py ... --buckets 1000
```

빠르게 한 번 보고 싶으면: `--total-mb 64 --max-objects 500 --list-checkpoints 1000 5000`

## 결과 (2026-08-08, `comparison.md`)

원본은 `results-<label>.json` 두 개, 표는 `compare.py` 가 생성한 `comparison.md`.
**같은 기계의 A/B 만 유효하다** — 절대 수치는 이 기계 밖에서 의미가 없다.

| 스코프 | 잰 것 | 결과 요약 |
|---|---|---|
| `size-sweep` | 4 KiB · 64 KiB · 1 MiB PUT/GET op/s | 두 백엔드가 같은 자리 (1 MiB 에서 PUT 166 vs 152, GET 150 vs 152 op/s). 4/64 KiB 행은 `--max-objects` 상한에 걸렸다(표시됨) |
| `list-scale` | full listing 초 (1,000 · 5,000 객체) | MinIO 0.054 → 0.274 s, RustFS 0.124 → 0.684 s. **객체 5배에 시간 5.1배 / 5.5배 = 이 구간은 선형** |
| `range-get` | full GET vs range GET op/s | **27.4배** (두 백엔드 동일: 37.0→1012.3 · 37.1→1016.8) |
| `buckets` | 200개 생성 + `list_buckets` | 둘 다 200/200 성공, 중단 사유 없음. `list_buckets` 11.1 ms / 8.8 ms |

**이 결과가 아직 답하지 않는 것** — `list-scale` 이 5,000 객체까지 선형이라는 것은
*절벽이 이 구간 밖에 있다*는 뜻이다. `_manifest.json` 이 필수라는 위키의 주장은
**입증도 반증도 되지 않았다** ([[Object storage layout]] ⑤). 그리고 아래 `opcount.py` —
이 하네스에서 제일 값진 부분 — 은 **아직 실행되지 않았다**(결과 파일 없음).

⚠️ `requirements.txt` 가 `boto3>=1.34` 로 하한만 잡혀 있어 **2026-08-08 실행 당시의 boto3
버전이 기록되지 않았다.** 재실행 시 `pip freeze` 를 결과와 함께 남길 것.

## ⭐⭐ LIST 질문 — 이게 본편이다

```python
from opcount import count_s3_ops
import spatialdata

with count_s3_ops("read_zarr"):
    sdata = spatialdata.read_zarr("s3://bucket/sample.zarr")

with count_s3_ops("bounding_box query"):
    sdata.query.bounding_box(...)
```

연산별 호출 수가 찍힌다. **소스 코드를 읽어서는 안 보이는 값**이고, 어느 문서도 주지 않는다.
`_manifest.json` 이 필수라는 위키의 주장이 여기서 근거를 얻거나 반증된다.

## 정직하게 — 못 재는 것

source 페이지에 이 절을 그대로 옮길 것. 강의 수치에 ⚠️ 를 달아온 기준을 **내 측정치에도** 적용한다.

- ❌ **분산 · erasure coding · 리밸런싱 · 내구성** — 다중 노드가 있어야 한다. 그리고 그게 RustFS 의 🚧 구역
- ❌ **절대 수치** — 노트북 SSD ≠ 서버 드라이브. 유효한 것은 **같은 기계의 상대 비교**뿐
- ❌ **운영 특성** — 장애 복구 · 업그레이드 · 장기 안정성
- ⚠️ `opcount` 는 botocore 를 거치는 호출만 센다. **첫 실행에서 서버 액세스 로그와 한 번 대조해
  이 가정을 검증할 것**

## 정리

```bash
docker compose --profile rustfs --profile minio down -v    # -v 로 볼륨까지
```

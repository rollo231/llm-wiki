#!/usr/bin/env python3
"""제품 중립 소형 객체 벤치 — S3 호환 스토어면 무엇이든.

측정 대상은 위키의 열린 질문에서 그대로 왔다:
  1) size-sweep  — 객체 크기별 처리량. Zarr 청크 크기 결정의 근거.
  2) list-scale  — 객체 수에 따른 full listing 비용. `_manifest.json` 이 선택이 아닌 이유.
  3) range-get   — 부분 읽기가 전체 읽기보다 실제로 싼가.
  4) buckets     — 버킷을 몇 개까지 만들 수 있고 얼마나 걸리나 (opt-in).

⚠️ 이 스크립트가 답하지 못하는 것: 분산·erasure coding·리밸런싱·내구성·장기 안정성.
   전부 다중 노드가 있어야 하는 축이다. 그리고 절대 수치는 이 기계 밖에서 의미 없다 —
   유효한 산출물은 **같은 기계에서의 상대 비교**뿐이다.

사용:
  python bench.py --label rustfs-1.0.0-beta.12 \
      --endpoint http://localhost:9000 --access-key rustfsadmin --secret-key rustfsadmin
  python bench.py --label minio-2026-08-04 \
      --endpoint http://localhost:9010 --access-key minioadmin --secret-key minioadmin
"""

from __future__ import annotations

import argparse
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

KiB = 1024
MiB = 1024 * 1024

DEFAULT_SIZES = [4 * KiB, 16 * KiB, 64 * KiB, 256 * KiB, 1 * MiB, 4 * MiB, 16 * MiB]
DEFAULT_LIST_CHECKPOINTS = [1_000, 5_000, 20_000]


# ---------------------------------------------------------------- infrastructure


def make_client(args) -> "boto3.client":
    return boto3.client(
        "s3",
        endpoint_url=args.endpoint,
        aws_access_key_id=args.access_key,
        aws_secret_access_key=args.secret_key,
        region_name="us-east-1",
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},  # 로컬 엔드포인트는 vhost 스타일이 안 된다
            max_pool_connections=args.concurrency * 2,
            retries={"max_attempts": 1},  # 재시도가 타이밍을 오염시킨다
        ),
    )


def ensure_bucket(c, bucket: str) -> None:
    try:
        c.create_bucket(Bucket=bucket)
    except ClientError as e:
        if e.response["Error"]["Code"] not in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
            raise


def purge_bucket(c, bucket: str, delete_bucket: bool = True) -> None:
    paginator = c.get_paginator("list_objects_v2")
    try:
        for page in paginator.paginate(Bucket=bucket):
            keys = [{"Key": o["Key"]} for o in page.get("Contents", [])]
            if keys:
                c.delete_objects(Bucket=bucket, Delete={"Objects": keys})
    except ClientError:
        return
    if delete_bucket:
        try:
            c.delete_bucket(Bucket=bucket)
        except ClientError:
            pass


def run_parallel(fn: Callable[[int], None], n: int, concurrency: int) -> float:
    """fn 을 0..n-1 에 대해 병렬 실행하고 총 소요 초를 반환."""
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        list(pool.map(fn, range(n)))
    return time.perf_counter() - t0


# ---------------------------------------------------------------- tests


def test_size_sweep(c, args) -> list[dict]:
    """객체 크기별 PUT/GET 처리량.

    각 크기마다 총 payload 를 고정(--total-mb)해서 비교 가능하게 만든다.
    작은 객체는 개수가 많아지므로 --max-objects 로 상한을 둔다 —
    그 상한에 걸렸으면 결과에 표시한다(조용한 절단 금지).
    """
    bucket = f"{args.bucket_prefix}-sweep"
    ensure_bucket(c, bucket)
    rows = []

    for size in args.sizes:
        n_ideal = max(1, (args.total_mb * MiB) // size)
        n = min(args.max_objects, n_ideal)
        capped = n < n_ideal
        payload = os.urandom(size)
        keys = [f"s{size}/{i:06d}" for i in range(n)]

        put_s = run_parallel(
            lambda i: c.put_object(Bucket=bucket, Key=keys[i], Body=payload),
            n,
            args.concurrency,
        )

        def _get(i: int) -> None:
            c.get_object(Bucket=bucket, Key=keys[i])["Body"].read()

        get_s = run_parallel(_get, n, args.concurrency)

        moved_mb = (n * size) / MiB
        rows.append(
            {
                "object_size_bytes": size,
                "objects": n,
                "capped_by_max_objects": capped,
                "payload_mb": round(moved_mb, 1),
                "put_ops_per_s": round(n / put_s, 1),
                "put_mb_per_s": round(moved_mb / put_s, 1),
                "get_ops_per_s": round(n / get_s, 1),
                "get_mb_per_s": round(moved_mb / get_s, 1),
            }
        )
        print(
            f"  size={size//KiB:>6}KiB n={n:<6} "
            f"PUT {rows[-1]['put_ops_per_s']:>8} op/s {rows[-1]['put_mb_per_s']:>7} MiB/s | "
            f"GET {rows[-1]['get_ops_per_s']:>8} op/s {rows[-1]['get_mb_per_s']:>7} MiB/s"
            + ("  [capped]" if capped else "")
        )
        purge_bucket(c, bucket, delete_bucket=False)

    purge_bucket(c, bucket)
    return rows


def test_list_scale(c, args) -> list[dict]:
    """객체 수 증가에 따른 full listing 비용.

    Zarr store 하나가 청크 수백만 개가 되므로, 여기서 나오는 기울기가
    "리스팅으로 목록을 얻는 게 실용적인가"에 대한 답이다.
    """
    bucket = f"{args.bucket_prefix}-list"
    purge_bucket(c, bucket)
    ensure_bucket(c, bucket)
    rows = []
    payload = b"x" * 256
    written = 0

    for target in args.list_checkpoints:
        todo = target - written
        if todo > 0:
            base = written
            run_parallel(
                lambda i: c.put_object(Bucket=bucket, Key=f"c/{base + i:07d}", Body=payload),
                todo,
                args.concurrency,
            )
            written = target

        t0 = time.perf_counter()
        pages = 0
        seen = 0
        for page in c.get_paginator("list_objects_v2").paginate(Bucket=bucket):
            pages += 1
            seen += len(page.get("Contents", []))
        elapsed = time.perf_counter() - t0

        rows.append(
            {
                "objects": target,
                "listed": seen,
                "pages": pages,
                "full_list_seconds": round(elapsed, 3),
                "objects_per_s": round(seen / elapsed, 1) if elapsed else None,
            }
        )
        print(f"  objects={target:<8} full list {elapsed:>7.3f}s  ({pages} pages, {seen} keys)")

    purge_bucket(c, bucket)
    return rows


def test_range_get(c, args) -> list[dict]:
    """부분 읽기가 전체 읽기보다 실제로 싼가.

    SpatialData/Zarr 가 range GET 으로 읽는다는 전제가 위키 여러 곳에 깔려 있는데
    측정된 적이 없다.
    """
    bucket = f"{args.bucket_prefix}-range"
    ensure_bucket(c, bucket)
    obj_size = 4 * MiB
    slice_size = 64 * KiB
    key = "one-big-object"
    c.put_object(Bucket=bucket, Key=key, Body=os.urandom(obj_size))
    n = 200

    def _full(i: int) -> None:
        c.get_object(Bucket=bucket, Key=key)["Body"].read()

    def _range(i: int) -> None:
        start = (i * slice_size) % (obj_size - slice_size)
        c.get_object(
            Bucket=bucket, Key=key, Range=f"bytes={start}-{start + slice_size - 1}"
        )["Body"].read()

    full_s = run_parallel(_full, n, args.concurrency)
    range_s = run_parallel(_range, n, args.concurrency)

    row = {
        "object_size_bytes": obj_size,
        "slice_size_bytes": slice_size,
        "requests": n,
        "full_get_ops_per_s": round(n / full_s, 1),
        "range_get_ops_per_s": round(n / range_s, 1),
        "speedup": round(full_s / range_s, 2),
    }
    print(
        f"  full GET {row['full_get_ops_per_s']} op/s vs "
        f"range GET {row['range_get_ops_per_s']} op/s  → {row['speedup']}x"
    )
    purge_bucket(c, bucket)
    return [row]


def test_buckets(c, args) -> list[dict]:
    """버킷을 몇 개까지, 얼마나 빨리 만들 수 있나. (`Object storage layout` 미검증 항목)"""
    made = []
    t0 = time.perf_counter()
    error = None
    for i in range(args.buckets):
        name = f"{args.bucket_prefix}-many-{i:05d}"
        try:
            c.create_bucket(Bucket=name)
            made.append(name)
        except ClientError as e:
            error = f"{e.response['Error']['Code']}: {e.response['Error'].get('Message', '')}"
            break
    elapsed = time.perf_counter() - t0

    t1 = time.perf_counter()
    n_listed = len(c.list_buckets().get("Buckets", []))
    list_s = time.perf_counter() - t1

    for name in made:
        try:
            c.delete_bucket(Bucket=name)
        except ClientError:
            pass

    row = {
        "attempted": args.buckets,
        "created": len(made),
        "stopped_by_error": error,
        "create_seconds": round(elapsed, 2),
        "create_per_s": round(len(made) / elapsed, 1) if elapsed else None,
        "list_buckets_seconds": round(list_s, 4),
        "list_buckets_count": n_listed,
    }
    print(f"  created {len(made)}/{args.buckets} in {elapsed:.2f}s; "
          f"list_buckets({n_listed}) took {list_s:.4f}s"
          + (f"  [stopped: {error}]" if error else ""))
    return [row]


TESTS = {
    "size-sweep": test_size_sweep,
    "list-scale": test_list_scale,
    "range-get": test_range_get,
    "buckets": test_buckets,
}


# ---------------------------------------------------------------- main


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--label", required=True, help="결과에 박히는 백엔드 식별자 (제품+버전)")
    p.add_argument("--endpoint", required=True)
    p.add_argument("--access-key", required=True)
    p.add_argument("--secret-key", required=True)
    p.add_argument("--concurrency", type=int, default=16)
    p.add_argument("--total-mb", type=int, default=256, help="크기 스윕에서 크기당 총 payload")
    p.add_argument("--max-objects", type=int, default=2000, help="크기당 객체 수 상한")
    p.add_argument("--sizes", type=int, nargs="+", default=DEFAULT_SIZES)
    p.add_argument("--list-checkpoints", type=int, nargs="+", default=DEFAULT_LIST_CHECKPOINTS)
    p.add_argument("--buckets", type=int, default=0, help="buckets 테스트에서 시도할 개수 (0=건너뜀)")
    p.add_argument("--bucket-prefix", default="bench")
    p.add_argument("--tests", nargs="+", default=["size-sweep", "list-scale", "range-get"],
                   choices=list(TESTS))
    p.add_argument("--out", default=None, help="결과 JSON 경로 (기본: results-<label>.json)")
    args = p.parse_args()

    if args.buckets and "buckets" not in args.tests:
        args.tests = list(args.tests) + ["buckets"]

    c = make_client(args)
    # 연결 확인을 먼저 — 벤치 도중에 죽는 것보다 낫다
    c.list_buckets()

    results = {
        "label": args.label,
        "endpoint": args.endpoint,
        "concurrency": args.concurrency,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "caveats": [
            "단일 노드. 분산·erasure coding·리밸런싱·내구성은 측정하지 않음.",
            "로컬 디스크. 절대 수치는 이 기계 밖에서 무의미 — 같은 기계의 상대 비교만 유효.",
            "운영 특성(장애 복구·업그레이드·장기 안정성)은 범위 밖.",
        ],
        "tests": {},
    }

    for name in args.tests:
        print(f"\n[{args.label}] {name}")
        results["tests"][name] = TESTS[name](c, args)

    out = args.out or f"results-{args.label}.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n→ {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""S3 API 호출을 연산별로 센다 — 클라이언트 쪽에서, 제품 중립으로.

⭐ 이게 이 하네스에서 제일 값진 부분이다.

위키의 열린 질문 하나가 *"어떤 SpatialData/Zarr 연산이 LIST 를 요구하나"* 인데,
**소스 코드를 읽어도 안 보인다** — s3fs·zarr·aiobotocore 를 거치며 어디서 LIST 가
나가는지는 호출 경계에서만 관측된다. 서버 액세스 로그를 파싱하면 제품마다 포맷이
다르므로, 여기서는 botocore 호출을 가로채 **제품과 무관하게** 센다.

`_manifest.json` 이 선택이 아니라 필수라는 위키의 주장도 여기서 검증된다 —
LIST 가 실제로 몇 번 나가는지가 근거이기 때문이다.

사용:

    from opcount import count_s3_ops

    with count_s3_ops("read sdata") as ops:
        sdata = spatialdata.read_zarr("s3://bucket/sample.zarr")
    # ops == Counter({'GetObject': 412, 'ListObjectsV2': 37, 'HeadObject': 9})

    with count_s3_ops("bbox query") as ops:
        sdata.query.bounding_box(...)

⚠️ 한계: botocore 를 거치지 않는 경로(네이티브 클라이언트, 캐시 히트)는 안 잡힌다.
   s3fs 는 aiobotocore 기반이라 잡히지만, **첫 실행에서 서버 액세스 로그와 한 번은
   대조해서 이 가정을 검증할 것.**
"""

from __future__ import annotations

import contextlib
import functools
from collections import Counter

_PATCH_TARGETS = []

try:  # 동기 경로: boto3 / botocore
    from botocore.client import BaseClient

    _PATCH_TARGETS.append((BaseClient, "_make_api_call", False))
except ImportError:  # pragma: no cover
    pass

try:  # 비동기 경로: s3fs → aiobotocore
    from aiobotocore.client import AioBaseClient

    _PATCH_TARGETS.append((AioBaseClient, "_make_api_call", True))
except ImportError:
    pass


@contextlib.contextmanager
def count_s3_ops(label: str = "", verbose: bool = True):
    """블록 안에서 나간 S3 API 호출을 연산 이름별로 센 Counter 를 준다."""
    if not _PATCH_TARGETS:
        raise RuntimeError("botocore 도 aiobotocore 도 없다 — 셀 것이 없음")

    counts: Counter[str] = Counter()
    originals = []

    for cls, attr, is_async in _PATCH_TARGETS:
        original = getattr(cls, attr)
        originals.append((cls, attr, original))

        if is_async:

            @functools.wraps(original)
            async def patched(self, operation_name, api_params, _orig=original):
                counts[operation_name] += 1
                return await _orig(self, operation_name, api_params)

        else:

            @functools.wraps(original)
            def patched(self, operation_name, api_params, _orig=original):
                counts[operation_name] += 1
                return _orig(self, operation_name, api_params)

        setattr(cls, attr, patched)

    try:
        yield counts
    finally:
        for cls, attr, original in originals:
            setattr(cls, attr, original)

        if verbose:
            total = sum(counts.values())
            head = f"[s3 ops] {label}" if label else "[s3 ops]"
            print(f"{head}: {total} calls")
            for op, n in counts.most_common():
                marker = "  ⭐" if op.startswith("List") else ""
                print(f"    {op:<24} {n:>7}{marker}")


if __name__ == "__main__":
    # 하네스 자체가 도는지 확인하는 최소 예제 (bench 스택 불필요).
    import argparse

    import boto3
    from botocore.config import Config

    p = argparse.ArgumentParser()
    p.add_argument("--endpoint", required=True)
    p.add_argument("--access-key", required=True)
    p.add_argument("--secret-key", required=True)
    a = p.parse_args()

    c = boto3.client(
        "s3",
        endpoint_url=a.endpoint,
        aws_access_key_id=a.access_key,
        aws_secret_access_key=a.secret_key,
        region_name="us-east-1",
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
    )

    with count_s3_ops("smoke test"):
        c.list_buckets()
        c.create_bucket(Bucket="opcount-smoke")
        c.put_object(Bucket="opcount-smoke", Key="a", Body=b"hello")
        c.get_object(Bucket="opcount-smoke", Key="a")["Body"].read()
        c.list_objects_v2(Bucket="opcount-smoke")
        c.delete_object(Bucket="opcount-smoke", Key="a")
        c.delete_bucket(Bucket="opcount-smoke")

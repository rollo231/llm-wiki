#!/usr/bin/env python3
"""results-*.json 여러 개를 위키에 붙일 마크다운 표로 만든다.

    python compare.py results-*.json > comparison.md

표를 손으로 옮겨 적지 않게 하는 게 목적이다 — 숫자가 손을 타면 검산이 무의미해진다.
"""

from __future__ import annotations

import json
import sys
from collections import OrderedDict

KiB = 1024


def load(paths: list[str]) -> list[dict]:
    out = []
    for p in paths:
        with open(p) as f:
            out.append(json.load(f))
    return out


def fmt_size(n: int) -> str:
    return f"{n // KiB} KiB" if n < KiB * KiB else f"{n // (KiB * KiB)} MiB"


def table_size_sweep(runs: list[dict]) -> str:
    labels = [r["label"] for r in runs]
    sizes = OrderedDict()
    for r in runs:
        for row in r["tests"].get("size-sweep", []):
            sizes.setdefault(row["object_size_bytes"], {})[r["label"]] = row

    lines = ["### 객체 크기별 처리량", ""]
    lines.append("| 객체 크기 | " + " | ".join(f"{l} PUT op/s | {l} GET op/s" for l in labels) + " |")
    lines.append("|---|" + "---|" * (2 * len(labels)))
    for size, per_label in sizes.items():
        cells = []
        for l in labels:
            row = per_label.get(l)
            if row:
                cap = "*" if row.get("capped_by_max_objects") else ""
                cells += [f"{row['put_ops_per_s']}{cap}", f"{row['get_ops_per_s']}{cap}"]
            else:
                cells += ["—", "—"]
        lines.append(f"| {fmt_size(size)} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("`*` = `--max-objects` 상한에 걸린 행 (조용한 절단 아님, 표시된 것).")
    return "\n".join(lines)


def table_list_scale(runs: list[dict]) -> str:
    labels = [r["label"] for r in runs]
    counts = OrderedDict()
    for r in runs:
        for row in r["tests"].get("list-scale", []):
            counts.setdefault(row["objects"], {})[r["label"]] = row

    lines = ["### full listing 비용 (객체 수 대비)", ""]
    lines.append("| 객체 수 | " + " | ".join(f"{l} 초" for l in labels) + " |")
    lines.append("|---|" + "---|" * len(labels))
    for n, per_label in counts.items():
        cells = [
            str(per_label[l]["full_list_seconds"]) if l in per_label else "—" for l in labels
        ]
        lines.append(f"| {n:,} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("> 기울기가 선형보다 나쁘면 리스팅으로 목록을 얻는 설계는 그 지점에서 끝난다.")
    return "\n".join(lines)


def table_range_get(runs: list[dict]) -> str:
    lines = ["### range GET vs full GET", "", "| 백엔드 | full GET op/s | range GET op/s | 배수 |", "|---|---|---|---|"]
    for r in runs:
        rows = r["tests"].get("range-get", [])
        if not rows:
            continue
        row = rows[0]
        lines.append(
            f"| {r['label']} | {row['full_get_ops_per_s']} | "
            f"{row['range_get_ops_per_s']} | {row['speedup']}x |"
        )
    return "\n".join(lines)


def table_buckets(runs: list[dict]) -> str:
    rows_exist = any(r["tests"].get("buckets") for r in runs)
    if not rows_exist:
        return ""
    lines = ["### 버킷 생성", "", "| 백엔드 | 생성 | 초 | 개/초 | list_buckets 초 | 중단 사유 |", "|---|---|---|---|---|---|"]
    for r in runs:
        for row in r["tests"].get("buckets", []):
            lines.append(
                f"| {r['label']} | {row['created']}/{row['attempted']} | {row['create_seconds']} | "
                f"{row['create_per_s']} | {row['list_buckets_seconds']} | {row['stopped_by_error'] or '—'} |"
            )
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    runs = load(sys.argv[1:])

    print("# 오브젝트 스토어 비교 — 단일 노드 로컬 측정\n")
    print("측정 조건:\n")
    for r in runs:
        print(f"- **{r['label']}** — `{r['endpoint']}`, concurrency {r['concurrency']}, {r['started_at']}")
    print()
    print("> ⚠️ **이 수치가 말할 수 없는 것**")
    for c in runs[0].get("caveats", []):
        print(f"> - {c}")
    print()

    for section in (table_size_sweep, table_list_scale, table_range_get, table_buckets):
        out = section(runs)
        if out:
            print(out)
            print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

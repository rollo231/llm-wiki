"""Inspect what a plain Parquet reader sees inside a SpatialData store."""

import json
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).parent / "sample.zarr"

for label, path in [
    ("POINTS  points/transcripts/points.parquet", ROOT / "points/transcripts/points.parquet"),
    ("SHAPES  shapes/cell_boundaries/shapes.parquet", ROOT / "shapes/cell_boundaries/shapes.parquet"),
]:
    print("=" * 78)
    print(label)
    print("=" * 78)
    f = pq.ParquetFile(next(path.glob("*.parquet")) if path.is_dir() else path)
    print("-- arrow schema --")
    print(f.schema_arrow)
    print(f"\nrows: {f.metadata.num_rows:,}   row groups: {f.metadata.num_row_groups}")
    md = f.schema_arrow.metadata or {}
    print("\n-- key-value metadata keys --")
    for k, v in md.items():
        k = k.decode()
        if k == "geo":
            print(f"  {k}:")
            print(json.dumps(json.loads(v.decode()), indent=4))
        else:
            s = v.decode()
            print(f"  {k}: {s[:400]}{'…' if len(s) > 400 else ''}")
    print()

print("=" * 78)
print("ZARR GROUP METADATA — where the coordinate transform actually lives")
print("=" * 78)
for p in ["points/transcripts/zarr.json", "shapes/cell_boundaries/zarr.json"]:
    d = json.loads((ROOT / p).read_text())
    print(f"\n--- {p} (zarr_format={d.get('zarr_format')}) ---")
    print(json.dumps(d.get("attributes", d), indent=2)[:1600])

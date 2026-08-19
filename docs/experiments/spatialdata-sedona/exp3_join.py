"""Does SedonaDB read a SpatialData store's parquet directly, and does the join agree
with spatialdata.aggregate()?

Ground truth : spatialdata.aggregate(values=points, by=shapes, ...)  -- global coords
Under test   : SedonaDB ST_Within on the raw parquet                 -- intrinsic coords
"""

import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent / "sample.zarr"
PTS = ROOT / "points/transcripts/points.parquet"
SHP = ROOT / "shapes/cell_boundaries/shapes.parquet"

# ============================================================ 1. SedonaDB
import sedona.db

sd = sedona.db.connect()

t0 = time.perf_counter()
pts = sd.read_parquet(str(PTS))
shp = sd.read_parquet(str(SHP))
print("=" * 78)
print("SEDONADB — can it read the store's parquet as-is?")
print("=" * 78)
print("\npoints schema:")
print(pts.schema)
print("\nshapes schema:")
print(shp.schema)

pts.to_view("pts", overwrite=True)
shp.to_view("shp", overwrite=True)

sedona_res = sd.sql(
    """
    SELECT c.cell_id AS cell_id, p.feature_name AS gene, COUNT(*) AS n
    FROM pts p JOIN shp c ON ST_Within(ST_SetSRID(ST_Point(p.x, p.y), 4326), c.geometry)
    GROUP BY 1, 2
    """
).to_pandas()
t_sedona = time.perf_counter() - t0
print(f"\nSedonaDB join: {len(sedona_res):,} (cell, gene) pairs, "
      f"{sedona_res['n'].sum():,} assigned transcripts, {t_sedona:.2f}s")

# ============================================================ 2. spatialdata.aggregate
from spatialdata import aggregate, read_zarr

t0 = time.perf_counter()
sdata = read_zarr(ROOT)
agg = aggregate(
    values=sdata["transcripts"],
    by=sdata["cell_boundaries"],
    value_key="feature_name",
    agg_func="count",
)
table = agg.tables["table"]
t_agg = time.perf_counter() - t0
print(f"\naggregate(): table {table.shape}, {table.X.sum():,.0f} assigned transcripts, {t_agg:.2f}s")

# ============================================================ 3. compare
import numpy as np
import scipy.sparse as sp

X = table.X.toarray() if sp.issparse(table.X) else np.asarray(table.X)
truth = (
    pd.DataFrame(X, index=table.obs["instance_id"].astype(str).values, columns=table.var_names.astype(str))
    .stack()
    .rename("n")
    .reset_index()
)
truth.columns = ["cell_id", "gene", "n"]
truth = truth[truth["n"] > 0]

a = sedona_res.astype({"cell_id": str, "gene": str, "n": "int64"}).sort_values(["cell_id", "gene"]).reset_index(drop=True)
b = truth.astype({"cell_id": str, "gene": str, "n": "int64"}).sort_values(["cell_id", "gene"]).reset_index(drop=True)

print("\n" + "=" * 78)
print("COMPARISON")
print("=" * 78)
print(f"  sedona rows : {len(a):,}    aggregate rows : {len(b):,}")
merged = a.merge(b, on=["cell_id", "gene"], how="outer", suffixes=("_sedona", "_agg"), indicator=True)
only_s = (merged["_merge"] == "left_only").sum()
only_a = (merged["_merge"] == "right_only").sum()
both = merged[merged["_merge"] == "both"]
mismatch = (both["n_sedona"] != both["n_agg"]).sum()
print(f"  sedona-only rows : {only_s}")
print(f"  aggregate-only rows : {only_a}")
print(f"  count mismatches on shared rows : {mismatch}")
identical = only_s == 0 and only_a == 0 and mismatch == 0
print(f"\n  ==> {'IDENTICAL ✅' if identical else 'DIFFERENT ❌'}")
if not identical:
    print(merged[(merged["_merge"] != "both") | (merged["n_sedona"] != merged["n_agg"])].head(15))

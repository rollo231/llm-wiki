# Experiment — SpatialData × SedonaDB interop

Reproduces the measurements behind [[SpatialData and Sedona interop]] §3 and §7.
`raw/` is gitignored, so this is the only durable record of *how* those numbers were produced.

**Ran on**: 2026-08-19 · MacBook, 32 GB RAM / 10 cores · macOS (Darwin 25.5.0).

## Environment

```bash
uv venv --python 3.12 venv
VIRTUAL_ENV=$PWD/venv uv pip install spatialdata "apache-sedona[db]"
# resolved: python 3.12.10 · spatialdata 0.8.0 · geopandas 1.1.4 · dask 2026.7.1
#           apache-sedona 1.9.1 · sedonadb 0.4.0
```

## Scripts

| script | what it answers |
|---|---|
| `exp1_build_store.py` | Builds a Xenium-shaped synthetic store (points + shapes, **identical** `Scale(1/pixel_size)` on both) and prints the on-disk layout. |
| `exp2_inspect.py` | What a plain Parquet reader sees: arrow schemas, the `geo` GeoParquet metadata, and the `zarr.json` group attributes where the coordinate transform actually lives. |
| `exp3_join.py` | Does SedonaDB read the store's parquet as-is, and does `ST_Within` on **intrinsic** coordinates agree with `spatialdata.aggregate()` on **global** coordinates? (It does — exactly.) |
| `exp4_scale.py` | Peak RSS + wall time for both engines across transcript counts. Each `(engine, N)` runs in a fresh subprocess so `ru_maxrss` is clean. |

```bash
venv/bin/python exp1_build_store.py
venv/bin/python exp2_inspect.py
venv/bin/python exp3_join.py

for N in 1000000 5000000 20000000 50000000; do
  venv/bin/python exp4_scale.py build  "$N"
  venv/bin/python exp4_scale.py sedona "$N"
  venv/bin/python exp4_scale.py agg    "$N"
done
```

## Two gotchas the scripts encode

1. **CRS mismatch.** `ST_Point(x, y)` has no CRS; the GeoParquet column is tagged `ogc:crs84`
   (SedonaDB's default for `crs: null`). The join is **refused at planning time**. Fix:
   `ST_SetSRID(ST_Point(x, y), 4326)` — or `ST_SetSRID(geometry, 0)` on the other side.
2. **Dictionary key overflow.** `GROUP BY` on the Arrow-dictionary gene column *after a join* fails
   with `Dictionary key bigger than the key type` (reproduced at 1M rows / 100 genes; not at
   200k / 25). Fix: `CAST(feature_name AS VARCHAR)`.

## Caveats on the numbers

Synthetic data: uniform random coordinates, non-overlapping square cells, uniform gene
distribution. Real tissue clusters spatially (partition skew), polygons are non-convex, and cell
boundaries touch. **Refine cost and skew handling are not measured here** — read the *shape of the
slope*, not the absolute multiples.

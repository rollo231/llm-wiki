# Experiment — `sedonadb-zarr` × OME-NGFF / SpatialData rasters

Answers the question left open in [[SpatialData and Sedona interop]] §6: can a query engine read a
SpatialData store's *raster* half? **Yes, with three specific limits.**

**Ran on**: 2026-08-19 · MacBook, 32 GB RAM / 10 cores · macOS (Darwin 25.5.0).

## Environment

```bash
uv venv --python 3.12 venv
VIRTUAL_ENV=$PWD/venv uv pip install spatialdata "apache-sedona[db]" sedonadb-zarr
# resolved: python 3.12.10 · spatialdata 0.8.0 · zarr 3.3.0
#           apache-sedona 1.9.1 · sedonadb 0.4.0 · sedonadb-zarr 0.4.0
```

## Scripts

| script | what it answers |
|---|---|
| `exp5_build_raster.py` | Writes a store with three rasters — a single-scale image, a multiscale image (`scale_factors=[2,2]`), and a labels element — then dumps the Zarr v3 group metadata that `sedonadb-zarr` would have to parse. |
| `exp6_zarr_read.py` | Tries nine entry points (element group / scale subgroup / store root / container, with and without `arrays=`) and reports what each one manages to learn. |
| `exp7_lazy.py` | `build` writes a 671 MB raster (5 × 8192 × 8192 uint16); `probe` times metadata-only queries against it to test the pixel-laziness claim. |

```bash
venv/bin/python exp5_build_raster.py
venv/bin/python exp6_zarr_read.py
venv/bin/python exp7_lazy.py build
venv/bin/python exp7_lazy.py probe
```

## Results

**Works** — `images/<name>` (single scale) and `labels/<name>`. One row per chunk, `srid = 0`
(CRS-less arrays are accepted), `rst.shape()` returns the *chunk* shape.

**Three limits:**

1. **A multiscale group cannot be read whole.** `arrays /s0 and /s1 have different chunk grid
   shapes ([3, 4, 4] vs [3, 2, 2]); every array in the group must share the same chunk grid.`
   Workaround (the error names it): `Zarr().with_options({"arrays": ["s0"]})` — one pyramid level
   at a time. s0 → 48 rows, s1 → 12, s2 → 3.
2. **Nested groups are not traversed.** Pointing at the store root or `images/` gives
   `has no child arrays`. Each element group must be addressed individually, so enumerating
   element paths is still the caller's job.
3. **`RS_Envelope` is in array-index space with Y negated** —
   `POLYGON((0 -256, 256 -256, 256 0, 0 0, 0 -256))`. The OME `coordinateTransformations`
   (here `scale = 4.7058`) is **ignored**. This is neither SpatialData's intrinsic space (y down)
   nor its global space.

The unifying explanation: **`sedonadb-zarr` reads plain Zarr, not OME-NGFF.** It never parses the
`ome` attribute — which is why SpatialData's non-standard `"version": "0.5-dev-spatialdata"` and its
`s0`/`s1` level names (rather than the spec's `0`/`1`) cause no trouble, and equally why the
coordinate transform is invisible to it.

**Pixel laziness holds, measured** — 671 MB store, 5 × 8192 × 8192 uint16:

```
open           :  0.001s  peakRSS= 147MB
count() = 1280 :  0.003s  peakRSS= 158MB
all metadata   :  0.013s  peakRSS= 165MB   rows=1280
all envelopes  :  0.003s  peakRSS= 168MB   distinct=256
union extent (ARRAY-INDEX space, y negated): x [0, 8192]  y [-8192, 0]
```

Peak RSS never leaves the interpreter's baseline. No pixel bytes are read.

**Note the channel axis multiplies rows**: 1,280 rows = 5 channels × 256 spatial tiles, so only 256
envelopes are distinct. A spatial query must filter to one channel or dedupe.

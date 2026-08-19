"""Where does issue #210 actually bite? Peak RSS + wall time, aggregate() vs SedonaDB.

Each (engine, N) runs in a fresh subprocess so peak RSS is clean.
usage:  exp4_scale.py build <N>   |   exp4_scale.py agg <N>   |   exp4_scale.py sedona <N>
"""

import json
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
PIXEL_SIZE = 0.2125
N_CELLS_SIDE = 60          # 3,600 cells
CELL_PITCH, CELL_HALF = 30.0, 10.0
N_GENES = 100


def store_path(n):
    return HERE / f"scale_{n}.zarr"


def peak_mb():
    # macOS: ru_maxrss is bytes; Linux: KiB
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1024**2 if sys.platform == "darwin" else r / 1024


# --------------------------------------------------------------------- build
def build(n):
    import numpy as np
    import pandas as pd
    from geopandas import GeoDataFrame
    from shapely.geometry import Polygon

    from spatialdata import SpatialData
    from spatialdata.models import PointsModel, ShapesModel
    from spatialdata.transformations import Scale

    rng = np.random.default_rng(7)
    out = store_path(n)
    if out.exists():
        shutil.rmtree(out)

    polys, ids = [], []
    for i in range(N_CELLS_SIDE):
        for j in range(N_CELLS_SIDE):
            cx, cy = (i + 0.5) * CELL_PITCH, (j + 0.5) * CELL_PITCH
            polys.append(Polygon([(cx - CELL_HALF, cy - CELL_HALF), (cx + CELL_HALF, cy - CELL_HALF),
                                  (cx + CELL_HALF, cy + CELL_HALF), (cx - CELL_HALF, cy + CELL_HALF)]))
            ids.append(f"cell_{i:03d}_{j:03d}")
    scale = Scale([1.0 / PIXEL_SIZE, 1.0 / PIXEL_SIZE], axes=("x", "y"))
    shapes = ShapesModel.parse(
        GeoDataFrame({"geometry": polys}, index=pd.Index(ids, name="cell_id")),
        transformations={"global": scale},
    )

    extent = N_CELLS_SIDE * CELL_PITCH
    genes = np.array([f"GENE{g:03d}" for g in range(N_GENES)])
    chunk = 5_000_000
    frames = []
    for lo in range(0, n, chunk):
        m = min(chunk, n - lo)
        frames.append(pd.DataFrame({
            "x": rng.uniform(0, extent, m),
            "y": rng.uniform(0, extent, m),
            "feature_name": pd.Categorical(genes[rng.integers(0, N_GENES, m)], categories=genes),
        }))
    tx = pd.concat(frames, ignore_index=True)
    del frames
    points = PointsModel.parse(tx, coordinates={"x": "x", "y": "y"},
                               feature_key="feature_name", transformations={"global": scale})
    SpatialData(points={"transcripts": points}, shapes={"cell_boundaries": shapes}).write(out)
    return {"rows": int(n)}


# ----------------------------------------------------------------- aggregate
def agg(n):
    from spatialdata import aggregate, read_zarr

    sdata = read_zarr(store_path(n))
    t = time.perf_counter()
    res = aggregate(values=sdata["transcripts"], by=sdata["cell_boundaries"],
                    value_key="feature_name", agg_func="count")
    table = res.tables["table"]
    return {"seconds": time.perf_counter() - t, "assigned": float(table.X.sum()), "shape": list(table.shape)}


# -------------------------------------------------------------------- sedona
def sedona(n):
    import sedona.db

    root = store_path(n)
    sd = sedona.db.connect()
    t = time.perf_counter()
    sd.read_parquet(str(root / "points/transcripts/points.parquet")).to_view("pts", overwrite=True)
    sd.read_parquet(str(root / "shapes/cell_boundaries/shapes.parquet")).to_view("shp", overwrite=True)
    df = sd.sql("""
        SELECT c.cell_id AS cell_id, CAST(p.feature_name AS VARCHAR) AS gene, COUNT(*) AS n
        FROM pts p JOIN shp c
          ON ST_Within(ST_SetSRID(ST_Point(p.x, p.y), 4326), c.geometry)
        GROUP BY 1, 2
    """).to_pandas()
    return {"seconds": time.perf_counter() - t, "assigned": float(df["n"].sum()), "pairs": len(df)}


if __name__ == "__main__":
    mode, n = sys.argv[1], int(sys.argv[2])
    try:
        out = {"build": build, "agg": agg, "sedona": sedona}[mode](n)
        out["peak_rss_mb"] = round(peak_mb(), 1)
        out["ok"] = True
    except Exception as e:  # OOM / any failure is a result, not a crash
        out = {"ok": False, "error": f"{type(e).__name__}: {e}"[:300], "peak_rss_mb": round(peak_mb(), 1)}
    print("RESULT " + json.dumps(out))

"""Build a synthetic Xenium-shaped SpatialData store, then inspect the on-disk layout.

Mimics what spatialdata_io.xenium() produces for the two elements that matter:
  points/transcripts        PointsModel, transform Scale(1/pixel_size)
  shapes/cell_boundaries    ShapesModel (Polygon), transform Scale(1/pixel_size)  <- SAME
"""

import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Polygon

from spatialdata import SpatialData
from spatialdata.models import PointsModel, ShapesModel
from spatialdata.transformations import Scale

RNG = np.random.default_rng(42)
OUT = Path(__file__).parent / "sample.zarr"

PIXEL_SIZE = 0.2125  # µm per pixel — the real Xenium value
N_CELLS_SIDE = 20  # 400 cells
CELL_PITCH = 30.0  # µm between cell centres
CELL_HALF = 10.0  # µm half-width of each square cell
N_TX = 200_000
N_GENES = 25

# ---------------------------------------------------------------- shapes
polys, cell_ids = [], []
for i in range(N_CELLS_SIDE):
    for j in range(N_CELLS_SIDE):
        cx, cy = (i + 0.5) * CELL_PITCH, (j + 0.5) * CELL_PITCH
        polys.append(
            Polygon(
                [
                    (cx - CELL_HALF, cy - CELL_HALF),
                    (cx + CELL_HALF, cy - CELL_HALF),
                    (cx + CELL_HALF, cy + CELL_HALF),
                    (cx - CELL_HALF, cy + CELL_HALF),
                ]
            )
        )
        cell_ids.append(f"cell_{i:03d}_{j:03d}")

geo_df = GeoDataFrame({"geometry": polys}, index=pd.Index(cell_ids, name="cell_id"))
scale = Scale([1.0 / PIXEL_SIZE, 1.0 / PIXEL_SIZE], axes=("x", "y"))
shapes = ShapesModel.parse(geo_df, transformations={"global": scale})

# ---------------------------------------------------------------- points
extent = N_CELLS_SIDE * CELL_PITCH
tx = pd.DataFrame(
    {
        "x": RNG.uniform(0, extent, N_TX),
        "y": RNG.uniform(0, extent, N_TX),
        "feature_name": pd.Categorical(RNG.choice([f"GENE{g:02d}" for g in range(N_GENES)], N_TX)),
        "qv": RNG.uniform(20, 40, N_TX),
    }
)
points = PointsModel.parse(
    tx,
    coordinates={"x": "x", "y": "y"},
    feature_key="feature_name",
    transformations={"global": scale},  # <- identical to shapes
)

sdata = SpatialData(points={"transcripts": points}, shapes={"cell_boundaries": shapes})
if OUT.exists():
    shutil.rmtree(OUT)
sdata.write(OUT)
print(f"wrote {OUT}")
print(sdata)

# ---------------------------------------------------------------- inspect layout
print("\n" + "=" * 70)
print("ON-DISK LAYOUT")
print("=" * 70)
for p in sorted(OUT.rglob("*")):
    rel = p.relative_to(OUT)
    if p.is_dir():
        print(f"  {rel}/")
    else:
        print(f"  {rel}  ({p.stat().st_size:,} B)")

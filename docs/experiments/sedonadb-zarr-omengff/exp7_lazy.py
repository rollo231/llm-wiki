"""Are pixels really lazy? Build a 671 MB raster, then time metadata-only queries.

usage: exp7_lazy.py build | exp7_lazy.py probe
"""

import resource
import shutil
import sys
import time
from pathlib import Path

OUT = Path(__file__).parent / "big.zarr"
C, Y, X = 5, 8192, 8192  # 5 * 8192^2 * 2B = 671 MB


def rss():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1024**2 if sys.platform == "darwin" else r / 1024


def build():
    import numpy as np

    from spatialdata import SpatialData
    from spatialdata.models import Image2DModel
    from spatialdata.transformations import Scale

    if OUT.exists():
        shutil.rmtree(OUT)
    rng = np.random.default_rng(1)
    img = rng.integers(0, 65535, size=(C, Y, X), dtype=np.uint16)
    sc = Scale([1 / 0.2125, 1 / 0.2125], axes=("x", "y"))
    SpatialData(
        images={
            "morphology": Image2DModel.parse(
                img, dims=("c", "y", "x"), transformations={"global": sc}, chunks=(1, 512, 512)
            )
        }
    ).write(OUT)
    total = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"store: {total / 1e6:.0f} MB")


def probe():
    import re

    import sedona.db
    import sedonadb_zarr

    sd = sedona.db.connect()
    sd.register(sedonadb_zarr.ZarrExtension())

    t = time.perf_counter()
    cube = sd.read(str(OUT / "images/morphology"), format=sedonadb_zarr.Zarr())
    print(f"open          : {time.perf_counter() - t:6.3f}s  peakRSS={rss():7.1f}MB")

    t = time.perf_counter()
    n = cube.count()
    print(f"count() = {n:<5} : {time.perf_counter() - t:6.3f}s  peakRSS={rss():7.1f}MB")

    t = time.perf_counter()
    df = cube.select(
        shape=cube.raster.rst.shape(),
        nd=cube.raster.rst.num_dimensions(),
        srid=cube.raster.rst.srid(),
    ).to_pandas()
    print(f"all metadata  : {time.perf_counter() - t:6.3f}s  peakRSS={rss():7.1f}MB  rows={len(df)}")

    t = time.perf_counter()
    env = cube.select(geom=sd.funcs.st_astext(cube.raster.rst.envelope())).to_pandas()
    print(f"all envelopes : {time.perf_counter() - t:6.3f}s  peakRSS={rss():7.1f}MB  "
          f"distinct={env['geom'].nunique()}")

    xs, ys = [], []
    for g in env["geom"]:
        nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", g)]
        xs += nums[0::2]
        ys += nums[1::2]
    print(f"  union extent (ARRAY-INDEX space, y negated): x [{min(xs)}, {max(xs)}]  "
          f"y [{min(ys)}, {max(ys)}]")


if __name__ == "__main__":
    {"build": build, "probe": probe}[sys.argv[1]]()

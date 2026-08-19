"""Can sedonadb-zarr read a SpatialData / OME-NGFF raster?

Tries every plausible entry point: the element group, the scale-level subgroup, and with
and without the `arrays` option. Each attempt reports what it managed to learn.
"""

from pathlib import Path

import sedona.db
import sedonadb_zarr

ROOT = Path(__file__).parent / "raster.zarr"

sd = sedona.db.connect()
sd.register(sedonadb_zarr.ZarrExtension())
print("ZarrExtension registered\n")

TARGETS = [
    ("element group (image, single scale)", ROOT / "images/morphology", None),
    ("element group + arrays=['s0']", ROOT / "images/morphology", ["s0"]),
    ("scale subgroup s0", ROOT / "images/morphology/s0", None),
    ("scale subgroup s0 + arrays=['c']", ROOT / "images/morphology/s0", ["c"]),
    ("element group (multiscale)", ROOT / "images/morphology_ms", None),
    ("multiscale s1", ROOT / "images/morphology_ms/s1", None),
    ("labels element group", ROOT / "labels/cells", None),
    ("store root", ROOT, None),
    ("images container", ROOT / "images", None),
]

for label, path, arrays in TARGETS:
    print("=" * 78)
    print(f"{label}\n  {path.relative_to(ROOT.parent)}   arrays={arrays}")
    spec = sedonadb_zarr.Zarr()
    if arrays:
        spec = spec.with_options({"arrays": arrays})
    try:
        cube = sd.read(str(path), format=spec)
    except Exception as e:
        print(f"  ❌ read failed: {type(e).__name__}: {str(e).splitlines()[0][:150]}")
        continue
    print(f"  ✅ read OK — schema: {cube.schema}")
    try:
        n = cube.count()
        print(f"     rows (= chunks): {n}")
    except Exception as e:
        print(f"     ⚠️ count failed: {str(e).splitlines()[0][:120]}")
    for expr, name in [
        ("rst.num_dimensions()", "ndim"),
        ("rst.dim_names()", "dims"),
        ("rst.shape()", "shape"),
        ("rst.srid()", "srid"),
    ]:
        try:
            v = cube.select(**{name: eval(f"cube.raster.{expr}")}).head(1).to_pandas()
            print(f"     {name:6}: {v[name].tolist()}")
        except Exception as e:
            print(f"     {name:6}: ⚠️ {str(e).splitlines()[0][:110]}")
    try:
        env = cube.select(geom=sd.funcs.st_astext(cube.raster.rst.envelope())).head(1).to_pandas()
        print(f"     envelope: {env['geom'].tolist()}")
    except Exception as e:
        print(f"     envelope: ⚠️ {str(e).splitlines()[0][:110]}")
    print()

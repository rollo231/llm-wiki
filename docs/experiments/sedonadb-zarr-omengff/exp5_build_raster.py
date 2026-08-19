"""Build a SpatialData store with real OME-NGFF rasters, then dump the group metadata
that sedonadb-zarr would have to understand.

Three raster elements:
  images/morphology       Image2D, c,y,x, single scale
  images/morphology_ms    Image2D, c,y,x, multiscale pyramid (scale_factors=[2,2])
  labels/cells            Labels2D, y,x
"""

import json
import shutil
from pathlib import Path

import numpy as np

from spatialdata import SpatialData
from spatialdata.models import Image2DModel, Labels2DModel
from spatialdata.transformations import Scale

OUT = Path(__file__).parent / "raster.zarr"
PIXEL_SIZE = 0.2125
RNG = np.random.default_rng(3)
C, Y, X = 3, 1024, 1024

if OUT.exists():
    shutil.rmtree(OUT)

img = RNG.integers(0, 65535, size=(C, Y, X), dtype=np.uint16)
scale = Scale([1.0 / PIXEL_SIZE, 1.0 / PIXEL_SIZE], axes=("x", "y"))

images = {
    "morphology": Image2DModel.parse(
        img, dims=("c", "y", "x"), transformations={"global": scale}, chunks=(1, 256, 256)
    ),
    "morphology_ms": Image2DModel.parse(
        img, dims=("c", "y", "x"), transformations={"global": scale},
        scale_factors=[2, 2], chunks=(1, 256, 256),
    ),
}
labels = {
    "cells": Labels2DModel.parse(
        RNG.integers(0, 500, size=(Y, X), dtype=np.uint32),
        dims=("y", "x"), transformations={"global": scale}, chunks=(256, 256),
    )
}

sdata = SpatialData(images=images, labels=labels)
sdata.write(OUT)
print(sdata)

print("\n" + "=" * 78)
print("ON-DISK TREE (dirs + metadata files only)")
print("=" * 78)
for p in sorted(OUT.rglob("*")):
    rel = p.relative_to(OUT)
    if p.is_dir():
        print(f"  {rel}/")
    elif p.name in ("zarr.json", ".zattrs", ".zgroup", ".zarray", "zarr.info"):
        print(f"  {rel}   <- metadata")

print("\n" + "=" * 78)
print("GROUP METADATA sedonadb-zarr would have to parse")
print("=" * 78)
for rel in ["zarr.json", "images/zarr.json", "images/morphology/zarr.json",
            "images/morphology_ms/zarr.json", "labels/cells/zarr.json"]:
    f = OUT / rel
    if not f.exists():
        print(f"\n--- {rel}: MISSING ---")
        continue
    d = json.loads(f.read_text())
    print(f"\n--- {rel}  (zarr_format={d.get('zarr_format')}, node_type={d.get('node_type')}) ---")
    body = d.get("attributes", d)
    txt = json.dumps(body, indent=2)
    print(txt[:2200] + ("\n…(truncated)" if len(txt) > 2200 else ""))

# the actual array node inside a multiscale group
for rel in ["images/morphology/0/zarr.json", "images/morphology_ms/0/zarr.json"]:
    f = OUT / rel
    if f.exists():
        d = json.loads(f.read_text())
        print(f"\n--- {rel} (array node) ---")
        print(json.dumps({k: v for k, v in d.items() if k != "attributes"}, indent=2)[:1200])

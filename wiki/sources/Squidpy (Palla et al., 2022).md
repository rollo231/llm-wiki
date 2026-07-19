---
type: source
title: Squidpy (Palla et al., 2022)
area: [bioinformatics, programming]
aliases: [Squidpy paper, Palla 2022]
tags: [spatial-transcriptomics, spatial-omics, python, scverse]
created: 2026-07-04
updated: 2026-07-19
sources: [raw/bioinformatics/squidpy.md]
---

# Squidpy (Palla et al., 2022)

Source page for the Squidpy framework paper. See [[Squidpy]] for the tool itself and
[[Spatial transcriptomics]] for the field.

## Summary

Squidpy is a Python framework for spatial omics analysis, published in *Nature Methods*
(2022). It extends the AnnData / Scanpy stack with spatial-aware analysis: spatial neighbor
graphs, spatial statistics, and joint handling of tissue images and molecular data.

## Key takeaways

- Brings spatial context into the widely used AnnData/Scanpy Python ecosystem rather than
  introducing a standalone toolchain.
- Provides a reusable vocabulary of spatial statistics (neighborhood enrichment,
  co-occurrence, Moran's I) applicable across assays.
- Designed for scalability and generality across spatial transcriptomics and imaging assays.

## Links

- Field: [[Spatial transcriptomics]]
- Tool: [[Squidpy]]
- Reference note: `raw/bioinformatics/squidpy.md`

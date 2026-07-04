# Squidpy — reference note

Reference note for ingestion. This is **not** the source text itself; it is a citation plus
key facts summarized in my own words, to respect copyright on this public repo.

- **Paper:** Palla, G., Spitzer, H., Klein, M., et al. "Squidpy: a scalable framework for
  spatial omics analysis." *Nature Methods* 19, 171–178 (2022).
- **DOI:** https://doi.org/10.1038/s41592-021-01358-2
- **Docs:** https://squidpy.readthedocs.io
- **Code:** https://github.com/scverse/squidpy (BSD-3-Clause)

## Key facts (own words)

- Squidpy is a Python library for analyzing spatial omics data (spatial transcriptomics and
  imaging-based assays), part of the scverse ecosystem.
- It builds on AnnData and Scanpy, extending them with spatial-aware tooling rather than
  introducing a standalone toolchain.
- Core capabilities: building spatial neighbor graphs; spatial statistics such as
  neighborhood enrichment, co-occurrence, and Moran's I; and joint handling of tissue images
  alongside the molecular data.
- Positioned as a scalable, general framework rather than a method tied to one assay.

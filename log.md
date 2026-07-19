# Log

Chronological record of wiki activity. Append-only; the newest entry goes at the bottom.
Each entry follows the format: `## [YYYY-MM-DD] <ingest|query|lint> | <title>`

## [2026-06-27] init | Wiki initialization

Created the vault skeleton using the LLM Wiki pattern: `raw/`,
`wiki/{entities,concepts,sources,notes}/`, `index.md`, `log.md`, `CLAUDE.md` (schema).
Initialized git.

## [2026-07-04] ingest | Squidpy (Palla et al., 2022)

Ingested the Squidpy framework paper as the first worked example. Created source page
[[Squidpy (Palla et al., 2022)]], entity [[Squidpy]] (`area: [bioinformatics, programming]`,
a boundary case), concept [[Spatial transcriptomics]], and the [[Bioinformatics]] area MOC.
Updated `index.md`. Delivered via PR2.

## [2026-07-19] schema | Reorganize raw/ into per-area folders; add data-engineering & resume-guide areas

Filed `raw/` sources into per-area subfolders: `raw/squidpy.md` → `raw/bioinformatics/squidpy.md`,
and the resume guide (PDF + `Section1.md`) into `raw/resume-guide/`. Renamed the guide PDF to
`tech-director-resume-guide-v1.pdf`. Added the `data-engineering` and `resume-guide` area values.
Updated the schema (`CLAUDE.md`) raw/ layer, directory diagram, and area list, and added the
matching `index.md` sections. Updated the [[Squidpy (Palla et al., 2022)]] source page reference.

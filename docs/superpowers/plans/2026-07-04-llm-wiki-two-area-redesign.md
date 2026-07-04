# LLM Wiki — Two-Area Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the `llm-wiki` vault around two general-knowledge areas (bioinformatics, programming) with an `area` field, a `maps/` folder for MOCs, and a documented PR-based review workflow — then validate it with one worked example ingest.

**Architecture:** Two pull requests. PR1 rewrites the schema docs (`CLAUDE.md`, `README.md`, `index.md`) and adds the `maps/` folder — no wiki content. PR2 ingests one real, boundary-spanning source (Squidpy) into the new structure. The human reviews and merges each PR before the next begins.

**Tech Stack:** Markdown + YAML frontmatter, Obsidian conventions, git, GitHub (`gh` CLI). No build system, no unit tests — verification is structural (grep checks + a wikilink-resolution check).

## Global Constraints

- **English only.** Every file — content, schema, config — is in English. No Hangul in any tracked file.
- **Public repo → general knowledge only.** No company-internal material. Do **not** copy full copyrighted paper/doc text into `raw/`; use citation + link + own-words summary.
- **`folder == page type`** is an invariant. Areas are distinguished by the `area` field, tags, and `index.md` sections — never by folders.
- **`area`** is a controlled, extensible YAML list. Current values: `bioinformatics`, `programming`. Boundary pages carry both: `area: [bioinformatics, programming]`. Required on every wiki page.
- **Filenames match the page title** so Obsidian resolves `[[Title]]` by filename; `aliases` hold abbreviations/variants.
- **PR-based workflow.** Wiki/schema changes land via branch → PR → human review → merge. Meta docs under `docs/` may be committed directly to `main`.
- **`raw/` is READ ONLY** for the agent, except when explicitly authoring a reference note as part of an ingest (as in this plan).

---

## File Structure

**PR1 (schema):**
- Modify: `CLAUDE.md` — full rewrite (adds Purpose, `area`, `moc`, `maps/`, `docs/`, Workflow, area-first index description).
- Modify: `README.md` — full rewrite (two-area framing, `area`, `maps/`, PR workflow).
- Modify: `index.md` — area-first empty template.
- Create: `wiki/maps/.gitkeep`.

**PR2 (example ingest):**
- Create: `raw/squidpy.md` — reference note (citation + link + own-words facts).
- Create: `wiki/sources/Squidpy (Palla et al., 2022).md` — source page.
- Create: `wiki/entities/Squidpy.md` — entity, `area: [bioinformatics, programming]`.
- Create: `wiki/concepts/Spatial transcriptomics.md` — concept, `area: [bioinformatics]`.
- Create: `wiki/maps/Bioinformatics.md` — area MOC.
- Modify: `index.md` — register the five new pages.
- Modify: `log.md` — append the ingest entry.

---

## Preflight (run once, before PR1)

- [ ] **Step 1: Confirm clean tree and branch**

Run: `cd /Users/sangwonlee/workspace/llm-wiki && git status -sb`
Expected: on `main`; the only uncommitted items (if any) are the plan file. The spec commit `3fafedb` is present in `git log`.

- [ ] **Step 2: Push meta docs (spec + plan) to main**

The spec and this plan live under `docs/` and are committed directly (meta docs, per the workflow).

Run:
```bash
git add docs/ && git commit -m "Add two-area redesign implementation plan

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>" || echo "nothing to commit"
git push origin main
```
Expected: `origin/main` updated with the spec + plan commits.

- [ ] **Step 3: Confirm `gh` is available and authenticated**

Run: `gh auth status`
Expected: logged in to github.com. If not, the PR-open steps fall back to pushing the branch and printing the compare URL for manual PR creation.

---

## PR1 — Schema restructure

Branch: `schema/two-area-redesign` off `main`.

### Task 1: Add `maps/` folder and rewrite `CLAUDE.md`

**Files:**
- Create: `wiki/maps/.gitkeep`
- Modify: `CLAUDE.md` (full rewrite)

**Interfaces:**
- Produces: the schema every later task and PR conforms to — the `area` field, page types incl. `moc`, the `maps/` folder, the area-first `index.md` shape, and the PR workflow.

- [ ] **Step 1: Create the branch**

```bash
git checkout main && git switch -c schema/two-area-redesign
```

- [ ] **Step 2: Create the maps/ placeholder**

```bash
touch wiki/maps/.gitkeep
```

- [ ] **Step 3: Rewrite `CLAUDE.md`**

Replace the entire file with:

````markdown
# LLM Wiki — Schema

This vault is a personal knowledge base built on the **LLM Wiki** pattern
(https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

You (the LLM agent) are the disciplined **maintainer** of this wiki. The human curates
sources, directs analysis, and asks questions. You do all the reading, summarizing,
cross-referencing, filing, and bookkeeping. The wiki is a persistent, compounding
artifact — knowledge is integrated once and kept current, not re-derived per query.

> Obsidian is the IDE, you are the programmer, the wiki is the codebase.

## Purpose

This wiki grows and organizes two areas of **general** knowledge (the repo is public — no
private or company-internal material):

- **bioinformatics** — spatial transcriptomics, single-cell, methods, concepts.
- **programming** — languages, frameworks, and fields (Python, FastAPI, React, K8s, …).

It is **source-first**: knowledge enters by ingesting sources, and the wiki accretes derived
pages around them.

## Layers

1. **`raw/`** — Immutable source documents (articles, papers, notes, data). The single
   source of truth. **READ ONLY — never create, edit, or delete anything under `raw/`.**
2. **`wiki/`** — Markdown pages you create and maintain. You own this layer entirely.
3. **This file (`CLAUDE.md`)** — the schema: structure, conventions, and workflows.
   Co-evolve it with the human as conventions are refined.

## Directory structure

```
llm-wiki/
├─ CLAUDE.md          # this schema
├─ README.md          # public-facing intro
├─ index.md           # content catalog (area-first)
├─ log.md             # append-only timeline of activity
├─ docs/              # meta working docs (specs, plans, handoffs) for this repo
├─ raw/               # immutable sources (read only)
└─ wiki/
   ├─ entities/       # products/tools/frameworks, people, orgs, datasets, places
   ├─ concepts/       # ideas, methods, topics, themes
   ├─ sources/        # one page per raw source: summary + takeaways
   ├─ notes/          # query results, syntheses, comparisons filed back
   └─ maps/           # MOCs — navigation hub pages (entry points)
```

`folder == page type` is an invariant. The two areas are **not** separate folders; they are
distinguished by the `area` field, tags, and `index.md` sections.

## Language

- Everything in this vault is written in **English** — wiki page content, this schema,
  code, and config.
- `log.md` entries are in English, prefixed with an English operation keyword.

## Page conventions

Every wiki page begins with YAML frontmatter:

```yaml
---
type: entity | concept | source | note | moc
title: Page title
area: [bioinformatics]        # one or more of: bioinformatics, programming
aliases: []                    # abbreviations / variants so [[links]] resolve
tags: []                       # finer topics: spatial-transcriptomics, python, fastapi...
created: 2026-06-27
updated: 2026-06-27
sources: []                    # raw source files / [[source pages]] this page draws on
---
```

- **`area`** is a controlled, extensible list. Current values: `bioinformatics`, `programming`.
  A page that genuinely spans both carries both: `area: [bioinformatics, programming]`.
- **`area`** is the big lens; **`tags`** are finer topics. Set `area` on every page.

Page types:

- **entity** (`wiki/entities/`) — a person, organization, product/tool/framework, place, or dataset.
- **concept** (`wiki/concepts/`) — an idea, method, topic, or theme.
- **source** (`wiki/sources/`) — one page per raw source: a summary, key takeaways,
  and links to the entities/concepts it touches.
- **note** (`wiki/notes/`) — a query result, synthesis, or comparison worth keeping.
- **moc** (`wiki/maps/`) — a Map of Content: a curated hub linking related pages for an area
  or topic; the human-facing entry point for navigation. Create lazily, once an area or topic
  has enough pages to warrant a hub.

Linking:

- Connect pages with Obsidian `[[wikilinks]]`. Prefer linking over duplicating content.
- **Filenames match the page title** (Obsidian resolves `[[Title]]` by filename); use
  `aliases` for abbreviations and variants so those links resolve too.
- Keep filenames stable — links depend on them.
- Update `updated:` whenever you edit a page.
- Prefer small, focused, well-linked pages over large catch-all pages.

## Operations

### Ingest

Trigger: the human drops a file into `raw/` (or pastes content / gives a URL) and asks
to ingest it. Default to **one source at a time, with the human in the loop**.

1. Read the source fully.
2. Discuss the key takeaways with the human before writing.
3. Create the source page in `wiki/sources/` (summary, takeaways, frontmatter with `area`).
4. Create or update relevant `entity`/`concept` pages; add cross-references.
5. Link the new pages into the relevant area MOC in `wiki/maps/` (create the MOC if warranted).
6. Explicitly note any contradictions with existing pages.
7. Update `index.md` (under the correct area section).
8. Append an entry to `log.md`.

A single source may touch 10–15 pages — that is expected.

### Query

1. Read `index.md` first to locate relevant pages.
2. Drill into those pages; follow `[[links]]`.
3. Answer **with citations** to wiki pages and/or raw sources.
4. If the answer is valuable (a comparison, synthesis, or discovery), file it as a new
   page in `wiki/notes/`, then update `index.md` and `log.md`. Explorations should
   compound in the wiki, not disappear into chat history.

### Lint

On request, health-check the wiki and report findings before applying fixes:

- Contradictions between pages
- Stale claims superseded by newer sources
- Orphan pages (no inbound `[[links]]`)
- Pages missing an `area`, or pages not reachable from any MOC
- Important concepts mentioned but lacking their own page
- Missing cross-references
- Data gaps that a web search could fill

Suggest new questions to investigate and new sources to look for.

## Workflow (PR-based review)

All wiki changes (ingests, notes, MOCs) and schema changes go through review:

1. Work on a branch — `ingest/<slug>`, `note/<slug>`, `moc/<slug>`, or `schema/<slug>`.
2. Commit the change (new/updated pages + `index.md` + `log.md`).
3. Open a PR; the human reviews the diff (what pages were created/changed).
4. Merge on approval.

Meta working docs under `docs/` (specs, plans, handoffs) may be committed directly — they
describe the work rather than being wiki content.

## index.md and log.md

- **`index.md`** is content-oriented and **area-first**: a top `## Maps` section listing MOC
  entry points, then one `##` section per area (`## Bioinformatics`, `## Programming`), each
  with type subsections (Concepts / Sources / Entities / Notes). Each entry is a `[[link]]`
  plus a one-line summary. Update it on every ingest and whenever a note is filed. Read it
  first when answering a query.
- **`log.md`** is chronological and append-only (newest at the bottom). Each entry
  begins with a parseable prefix:

  ```
  ## [YYYY-MM-DD] <ingest|query|lint> | <title>
  ```

  so `grep "^## \[" log.md | tail -5` shows recent activity.
````

- [ ] **Step 4: Verify structure and content**

Run:
```bash
test -f wiki/maps/.gitkeep && echo "maps ok"
grep -q "^## Purpose" CLAUDE.md && grep -q "moc" CLAUDE.md && grep -q "maps/" CLAUDE.md && grep -q "Workflow (PR-based review)" CLAUDE.md && grep -q "area:" CLAUDE.md && echo "CLAUDE.md ok"
grep -rlP '[\x{AC00}-\x{D7A3}]' CLAUDE.md && echo "HANGUL FOUND (fail)" || echo "no hangul"
```
Expected: `maps ok`, `CLAUDE.md ok`, `no hangul`.

- [ ] **Step 5: Commit**

```bash
git add wiki/maps/.gitkeep CLAUDE.md
git commit -m "Rewrite schema for two-area structure + maps/ + PR workflow

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 2: Rewrite `index.md` (area-first empty template)

**Files:**
- Modify: `index.md`

**Interfaces:**
- Consumes: the area-first shape defined in Task 1's CLAUDE.md.
- Produces: the empty catalog PR2 will fill.

- [ ] **Step 1: Replace `index.md` with the area-first template**

````markdown
# Index

Content catalog for this wiki. Each page is listed as a link plus a one-line summary.
Update it on every ingest and whenever a note is filed. Read it first when answering a query.

## Maps

_(none yet)_

## Bioinformatics

### Concepts
_(none yet)_
### Sources
_(none yet)_
### Entities
_(none yet)_
### Notes
_(none yet)_

## Programming

### Concepts
_(none yet)_
### Sources
_(none yet)_
### Entities
_(none yet)_
### Notes
_(none yet)_
````

- [ ] **Step 2: Verify**

Run:
```bash
grep -q "^## Maps" index.md && grep -q "^## Bioinformatics" index.md && grep -q "^## Programming" index.md && echo "index ok"
```
Expected: `index ok`.

- [ ] **Step 3: Commit**

```bash
git add index.md
git commit -m "Make index.md area-first (Maps / Bioinformatics / Programming)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 3: Rewrite `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace `README.md` with:**

````markdown
# LLM Wiki

A personal knowledge base built on the **LLM Wiki** pattern
([karpathy's gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)),
maintained inside [Obsidian](https://obsidian.md) by an LLM agent.

> Obsidian is the IDE, the LLM is the programmer, the wiki is the codebase.

The human curates sources, directs analysis, and asks questions. The LLM agent does the
reading, summarizing, cross-referencing, filing, and bookkeeping. Knowledge is integrated
once and kept current — a persistent, compounding artifact rather than something
re-derived on every query.

It is **source-first**: knowledge enters by ingesting sources, and the wiki grows around
them. It organizes two areas of **general** knowledge (this repo is public):

- **bioinformatics** — spatial transcriptomics, single-cell, methods, concepts.
- **programming** — languages, frameworks, and fields (Python, FastAPI, React, K8s, …).

## Layers

1. **`raw/`** — Immutable source documents. The single source of truth. Read-only.
2. **`wiki/`** — Markdown pages the agent creates and maintains.
3. **`CLAUDE.md`** — The schema: structure, conventions, and workflows the agent follows.

## Structure

```
llm-wiki/
├─ CLAUDE.md          # schema the agent follows
├─ index.md           # content catalog (area-first)
├─ log.md             # append-only timeline of activity
├─ docs/              # meta working docs (specs, plans, handoffs)
├─ raw/               # immutable sources (read only)
└─ wiki/
   ├─ entities/       # products/tools/frameworks, people, orgs, datasets
   ├─ concepts/       # ideas, methods, topics, themes
   ├─ sources/        # one page per raw source: summary + takeaways
   ├─ notes/          # query results, syntheses, comparisons filed back
   └─ maps/           # MOCs — navigation hub pages (entry points)
```

Pages carry YAML frontmatter (`type`, `title`, `area`, `aliases`, `tags`, `created`,
`updated`, `sources`) and connect via Obsidian `[[wikilinks]]`. The two areas are
distinguished by the `area` field and tags — not by separate folders — so a page can belong
to both (e.g. a Python bioinformatics tool: `area: [bioinformatics, programming]`).

## Workflows

- **Ingest** — A source lands in `raw/`. The agent reads it, discusses takeaways, writes a
  `source` page, creates/updates related `entity`/`concept` pages, links them into the area
  MOC, and updates `index.md` and `log.md`.
- **Query** — The agent reads `index.md`, follows `[[links]]`, and answers with citations.
  Valuable answers are filed back as `note` pages so explorations compound.
- **Lint** — On request, the agent health-checks the vault: contradictions, stale claims,
  orphan pages, missing `area`, missing cross-references, and data gaps.

Changes flow through **pull requests**: the agent works on a branch and opens a PR; the human
reviews the diff before it merges. See [`CLAUDE.md`](CLAUDE.md) for the full schema.

## Getting started

1. Open this folder as a vault in [Obsidian](https://obsidian.md).
2. Drop a source document into `raw/`.
3. Ask your LLM agent to ingest it — and review the resulting PR.
````

- [ ] **Step 2: Verify**

Run:
```bash
grep -q "source-first" README.md && grep -q "maps/" README.md && grep -q "pull requests" README.md && echo "readme ok"
grep -rlP '[\x{AC00}-\x{D7A3}]' README.md && echo "HANGUL FOUND (fail)" || echo "no hangul"
```
Expected: `readme ok`, `no hangul`.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "Reframe README around two areas, maps/, and PR workflow

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 4: Open PR1

- [ ] **Step 1: Push the branch**

```bash
git push -u origin schema/two-area-redesign
```

- [ ] **Step 2: Open the PR**

```bash
gh pr create --base main --head schema/two-area-redesign \
  --title "Schema: two-area structure, maps/, PR workflow" \
  --body "Rewrites CLAUDE.md, README.md, and index.md for the two-area (bioinformatics/programming) design; adds wiki/maps/ for MOCs; documents the PR-based review workflow. No wiki content yet — that follows in PR2 (Squidpy example ingest). Spec: docs/superpowers/specs/2026-07-04-llm-wiki-two-area-redesign-design.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```
Expected: prints the PR URL. If `gh` is unavailable, print `https://github.com/rollo231/llm-wiki/compare/main...schema/two-area-redesign?expand=1` for manual creation.

- [ ] **Step 3: HUMAN GATE — review and merge PR1**

The human reviews the diff and merges PR1 into `main`. Do not start PR2 until PR1 is merged.

---

## PR2 — Squidpy example ingest

Branch: `ingest/squidpy` off `main` **after PR1 is merged**.

### Task 5: Author the raw reference note

**Files:**
- Create: `raw/squidpy.md`

**Interfaces:**
- Produces: the immutable source `raw/squidpy.md` that the source page cites.

- [ ] **Step 1: Sync main and branch**

```bash
git checkout main && git pull origin main && git switch -c ingest/squidpy
```

- [ ] **Step 2: Create `raw/squidpy.md`**

````markdown
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
````

- [ ] **Step 3: Verify**

Run: `test -f raw/squidpy.md && grep -q "Nature Methods" raw/squidpy.md && echo "raw ok"`
Expected: `raw ok`.

- [ ] **Step 4: Commit**

```bash
git add raw/squidpy.md
git commit -m "Add Squidpy raw reference note

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 6: Author the four wiki pages (source, entity, concept, MOC)

These four pages cross-link each other, so author them together. All links used —
`[[Squidpy]]`, `[[Spatial transcriptomics]]`, `[[Squidpy (Palla et al., 2022)]]`,
`[[Bioinformatics]]` — resolve to the filenames created below.

**Files:**
- Create: `wiki/sources/Squidpy (Palla et al., 2022).md`
- Create: `wiki/entities/Squidpy.md`
- Create: `wiki/concepts/Spatial transcriptomics.md`
- Create: `wiki/maps/Bioinformatics.md`

**Interfaces:**
- Consumes: `raw/squidpy.md` (Task 5); the schema (PR1).
- Produces: the linked page set that Task 7 registers in `index.md` / `log.md`.

- [ ] **Step 1: Create `wiki/sources/Squidpy (Palla et al., 2022).md`**

````markdown
---
type: source
title: Squidpy (Palla et al., 2022)
area: [bioinformatics, programming]
aliases: [Squidpy paper, Palla 2022]
tags: [spatial-transcriptomics, spatial-omics, python, scverse]
created: 2026-07-04
updated: 2026-07-04
sources: [raw/squidpy.md]
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
- Reference note: `raw/squidpy.md`
````

- [ ] **Step 2: Create `wiki/entities/Squidpy.md`**

````markdown
---
type: entity
title: Squidpy
area: [bioinformatics, programming]
aliases: [squidpy]
tags: [spatial-transcriptomics, spatial-omics, python, scverse, library]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[Squidpy (Palla et al., 2022)]]"]
---

# Squidpy

A Python library for spatial omics analysis, part of the scverse ecosystem. It extends the
AnnData and Scanpy stack with spatial-aware tooling. This is a boundary example for the wiki:
it is both a [[Spatial transcriptomics]] method (bioinformatics) and a Python library
(programming), so it carries `area: [bioinformatics, programming]`.

## What it does

- Builds spatial neighbor graphs over cells/spots.
- Computes spatial statistics: neighborhood enrichment, co-occurrence, Moran's I.
- Handles tissue images alongside molecular data.

## Ecosystem

- Built on AnnData and Scanpy (scverse). Written in Python.

## Links

- Field: [[Spatial transcriptomics]]
- Source: [[Squidpy (Palla et al., 2022)]]
````

- [ ] **Step 3: Create `wiki/concepts/Spatial transcriptomics.md`**

````markdown
---
type: concept
title: Spatial transcriptomics
area: [bioinformatics]
aliases: [ST, spatial omics]
tags: [spatial-transcriptomics, spatial-omics, genomics]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[Squidpy (Palla et al., 2022)]]"]
---

# Spatial transcriptomics

A family of methods that measure gene expression while preserving the spatial location of
cells or spots within a tissue. Unlike dissociated single-cell RNA-seq, spatial methods keep
tissue coordinates, so expression can be related to tissue structure and cell neighborhoods.

## Why it matters

- Links molecular state to spatial context (where cells are, what they neighbor).
- Enables spatial statistics — neighborhood composition, co-occurrence, spatial
  autocorrelation.

## Tooling

- [[Squidpy]] — Python framework for spatial omics analysis.

## Links

- Entry point: [[Bioinformatics]]
- Source: [[Squidpy (Palla et al., 2022)]]
````

- [ ] **Step 4: Create `wiki/maps/Bioinformatics.md`**

````markdown
---
type: moc
title: Bioinformatics
area: [bioinformatics]
aliases: [bioinformatics map]
tags: [moc]
created: 2026-07-04
updated: 2026-07-04
sources: []
---

# Bioinformatics

Map of Content — entry point for the bioinformatics area.

## Concepts

- [[Spatial transcriptomics]] — measuring gene expression while preserving tissue location.

## Tools

- [[Squidpy]] — Python framework for spatial omics analysis (also a `programming` page).

## Sources

- [[Squidpy (Palla et al., 2022)]] — Squidpy framework paper (Nature Methods, 2022).
````

- [ ] **Step 5: Verify the pages exist and every wikilink resolves**

Run:
```bash
ls "wiki/sources/Squidpy (Palla et al., 2022).md" "wiki/entities/Squidpy.md" "wiki/concepts/Spatial transcriptomics.md" "wiki/maps/Bioinformatics.md" >/dev/null && echo "pages ok"
grep -rhoE '\[\[[^]]+\]\]' wiki | sed -E 's/\[\[//; s/\|.*//; s/\]\]//' | sort -u | while read -r t; do
  find wiki -type f -name "$t.md" | grep -q . || echo "UNRESOLVED: $t"
done
echo "link check done"
grep -rlP '[\x{AC00}-\x{D7A3}]' wiki && echo "HANGUL FOUND (fail)" || echo "no hangul"
```
Expected: `pages ok`; no `UNRESOLVED:` lines before `link check done`; `no hangul`.

- [ ] **Step 6: Commit**

```bash
git add wiki/sources wiki/entities wiki/concepts wiki/maps
git commit -m "Ingest Squidpy: source, entity, concept, and Bioinformatics MOC

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 7: Register in `index.md` and append `log.md`

**Files:**
- Modify: `index.md`
- Modify: `log.md`

**Interfaces:**
- Consumes: the five pages from Tasks 5–6.

- [ ] **Step 1: Replace `index.md` with the filled catalog**

Squidpy appears under **both** Bioinformatics and Programming (it is a boundary page).

````markdown
# Index

Content catalog for this wiki. Each page is listed as a link plus a one-line summary.
Update it on every ingest and whenever a note is filed. Read it first when answering a query.

## Maps

- [[Bioinformatics]] — entry point for the bioinformatics area.

## Bioinformatics

### Concepts
- [[Spatial transcriptomics]] — measuring gene expression while preserving tissue location.
### Sources
- [[Squidpy (Palla et al., 2022)]] — Python framework for spatial omics analysis (Nature Methods).
### Entities
- [[Squidpy]] — Python library for spatial omics analysis (scverse); boundary case.
### Notes
_(none yet)_

## Programming

### Concepts
_(none yet)_
### Sources
_(none yet)_
### Entities
- [[Squidpy]] — appears here too: it is a Python library (boundary case).
### Notes
_(none yet)_
````

- [ ] **Step 2: Append the ingest entry to `log.md`**

Add at the end of `log.md`:

````markdown

## [2026-07-04] ingest | Squidpy (Palla et al., 2022)

Ingested the Squidpy framework paper as the first worked example. Created source page
[[Squidpy (Palla et al., 2022)]], entity [[Squidpy]] (`area: [bioinformatics, programming]`,
a boundary case), concept [[Spatial transcriptomics]], and the [[Bioinformatics]] area MOC.
Updated `index.md`. Delivered via PR2.
````

- [ ] **Step 3: Verify**

Run:
```bash
grep -q "Spatial transcriptomics" index.md && grep -q "Squidpy" index.md && echo "index filled ok"
grep -q "^## \[2026-07-04\] ingest | Squidpy" log.md && echo "log ok"
```
Expected: `index filled ok`, `log ok`.

- [ ] **Step 4: Commit**

```bash
git add index.md log.md
git commit -m "Register Squidpy pages in index.md and log.md

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 8: Open PR2

- [ ] **Step 1: Push the branch**

```bash
git push -u origin ingest/squidpy
```

- [ ] **Step 2: Open the PR**

```bash
gh pr create --base main --head ingest/squidpy \
  --title "Ingest: Squidpy (first worked example)" \
  --body "First worked example ingest, validating the two-area schema end-to-end: raw reference note + source/entity/concept pages + Bioinformatics MOC + index/log updates. Squidpy is a boundary case (area: bioinformatics + programming) and appears under both index sections.

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```
Expected: prints the PR URL. If `gh` is unavailable, print `https://github.com/rollo231/llm-wiki/compare/main...ingest/squidpy?expand=1`.

- [ ] **Step 3: HUMAN GATE — review and merge PR2**

The human reviews the diff (the pages the agent created and how they link) and merges.

---

## Self-Review (author checklist — completed)

**Spec coverage:** source-first (kept) ✓; two areas via `area` field ✓; flat type folders + `maps/` + `docs/` ✓; `moc` type ✓; area-first `index.md` ✓; ingest/lint adjustments ✓; PR-based workflow documented ✓; Squidpy example with boundary `area` + MOC + index/log ✓; PR1→PR2 packaging ✓.

**Placeholder scan:** no TBD/TODO; all file contents given in full; verification commands concrete with expected output.

**Type/name consistency:** filenames and `[[link]]` targets match — `Squidpy.md`↔`[[Squidpy]]`, `Spatial transcriptomics.md`↔`[[Spatial transcriptomics]]`, `Squidpy (Palla et al., 2022).md`↔`[[Squidpy (Palla et al., 2022)]]`, `Bioinformatics.md`↔`[[Bioinformatics]]`. No links to uncreated pages (AnnData/Scanpy are plain text). `area` values limited to `bioinformatics`/`programming` throughout.

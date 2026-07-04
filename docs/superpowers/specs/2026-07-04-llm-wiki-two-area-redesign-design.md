# LLM Wiki — Two-Area Redesign (Design)

Date: 2026-07-04
Status: Approved (pending user review of this spec)

## Context

`llm-wiki` is a personal knowledge base on the karpathy **LLM Wiki** pattern, maintained
inside Obsidian by an LLM agent, hosted as a **public** GitHub repo (`rollo231/llm-wiki`).
The vault is currently an empty skeleton (`raw/`, `wiki/{entities,concepts,sources,notes}/`,
`index.md`, `log.md`, `CLAUDE.md`, `README.md`). All documents are in English.

## Goal

Use the wiki to **raise and organize** two bodies of general knowledge:

- **bioinformatics** — spatial transcriptomics, single-cell, methods, concepts (mostly from papers).
- **programming** — languages / frameworks / fields (Python, FastAPI, React, K8s, …).

Because the repo is public, only **general knowledge** is stored — no company-internal material.

## Decisions

1. **Orientation: source-first (research / ingest).** Keep the karpathy model — knowledge
   enters by ingesting sources; the wiki accretes derived pages around them. Learning
   happens through the act of reading and ingesting.
2. **Two areas via a field, not folders.** Areas are distinguished by an `area` frontmatter
   field (a list) plus tags and index sections — the filesystem stays flat by page type.
   This preserves karpathy minimalism, maximizes cross-linking, and handles boundary cases
   without forced classification.
3. **MOCs live in `maps/`.** Maps of Content are navigation entry points; they get their own
   folder so the `folder == type` invariant holds and entry points stay visible. Created
   lazily, when a topic has enough pages to warrant a curated hub.
4. **PR-based review is the standing workflow.** Content and schema changes flow through
   `branch → PR → human review → merge`. The human reviews the diff (what pages the agent
   created / changed) before it lands. This is the "LLM is the programmer, wiki is the
   codebase" metaphor applied literally: code review for knowledge.

## Directory structure

```
llm-wiki/
├─ CLAUDE.md          # schema
├─ README.md          # public-facing intro
├─ index.md           # global catalog (area-first)
├─ log.md             # append-only activity timeline
├─ docs/              # meta working docs (specs, plans, handoffs) for this repo
├─ raw/               # immutable sources (read only)
└─ wiki/
   ├─ entities/       # products/tools/frameworks, people, orgs, datasets, places
   ├─ concepts/       # ideas, methods, topics, themes
   ├─ sources/        # one page per raw source: summary + takeaways
   ├─ notes/          # syntheses, comparisons, query results filed back
   └─ maps/           # MOCs — navigation hub pages (entry points)
```

`folder == page type` is an invariant. Area separation is delivered by frontmatter + tags
+ `index.md` sections, never by folders.

## Page conventions

Every wiki page begins with YAML frontmatter:

```yaml
---
type: entity | concept | source | note | moc
title: Page title
area: [bioinformatics]        # one or more of: bioinformatics, programming
aliases: []                    # English / abbreviated forms so [[links]] resolve
tags: []                       # finer topics: spatial-transcriptomics, python, fastapi, k8s...
created: 2026-07-04
updated: 2026-07-04
sources: []                    # raw files / [[source pages]] this page draws on
---
```

- **`area`** is a controlled, extensible list. Seed values: `bioinformatics`, `programming`.
  Boundary pages (e.g. a Python bioinformatics tool) carry both: `area: [bioinformatics, programming]`.
- **`area`** = the two big lenses; **`tags`** = finer topics (spatial-transcriptomics, fastapi, …).
- Required on every page. Lint flags any page missing `area`.

Page types:

- **entity** (`wiki/entities/`) — a person, organization, product/tool/framework, place, or dataset.
- **concept** (`wiki/concepts/`) — an idea, method, topic, or theme.
- **source** (`wiki/sources/`) — one page per raw source: summary, key takeaways, links.
- **note** (`wiki/notes/`) — a synthesis, comparison, or query result worth keeping.
- **moc** (`wiki/maps/`) — a Map of Content: a curated hub linking related pages for a topic
  or area; the human-facing entry point for navigation.

Linking rules are unchanged: connect with `[[wikilinks]]`, prefer linking over duplication,
add `aliases`, keep filenames stable, bump `updated:` on edit, prefer small focused pages.

## index.md and log.md

- **`index.md`** — area-first catalog. Top `## Maps` section lists MOC entry points, then
  one `##` section per area (`## Bioinformatics`, `## Programming`), each with type
  subsections (Concepts / Sources / Entities / Notes). Read first when answering a query.
- **`log.md`** — unchanged, append-only, newest at bottom, format
  `## [YYYY-MM-DD] <ingest|query|lint> | <title>`. The body may reference the merged PR.

## Operations

karpathy's ingest / query / lint, with two adjustments:

- **Ingest** — on a new source: set `area`; link the source into its area MOC (create the MOC
  if warranted); register it under the correct area section in `index.md`; append to `log.md`.
  A single source may touch 10–15 pages.
- **Query** — unchanged: read `index.md`, follow `[[links]]`, answer with citations, file
  valuable answers as `note` pages.
- **Lint** — existing checks (contradictions, stale claims, orphans, missing concept pages,
  missing cross-references, data gaps) plus: pages missing `area`, and pages not reachable
  from any MOC.

## Workflow (PR-based review)

Documented in `CLAUDE.md` as the standing contribution workflow:

1. Work on a branch (`ingest/<slug>`, `note/<slug>`, `moc/<slug>`, `schema/<slug>`).
2. Commit the change (new/updated pages + `index.md` + `log.md`).
3. Open a PR; the human reviews the diff.
4. Merge on approval.

Meta working docs under `docs/` (specs, plans, handoffs) may be committed directly — they
describe the work rather than being wiki content.

## CLAUDE.md / README.md changes

- **CLAUDE.md**: intro frames the two-area purpose; frontmatter gains `area`; page types gain
  `moc`; directory gains `maps/` and `docs/`; index.md description becomes area-first; ingest
  and lint gain the adjustments above; a new **Workflow** section documents PR-based review.
- **README.md**: reframed as a source-first wiki growing two general-knowledge areas; reflects
  `area`, `maps/`, and the PR workflow; structure and workflows stay consistent with CLAUDE.md.

## Example ingest (validation + worked reference)

A real, boundary-spanning source ingested to demonstrate the full flow: **Squidpy** — a
spatial-transcriptomics analysis library in Python (bioinformatics + programming).

To respect copyright on a public repo, the raw artifact is a **reference note** (citation +
link + a few own-words key facts), not copied paper/doc text. The ingest produces:

- `raw/squidpy.md` — reference note (citation: Palla et al., *Nature Methods*, 2022; link; key facts).
- `wiki/sources/squidpy-palla-2022.md` — source page (summary, takeaways, links).
- `wiki/entities/squidpy.md` — entity (product), `area: [bioinformatics, programming]`.
- `wiki/concepts/spatial-transcriptomics.md` — concept, `area: [bioinformatics]`.
- `wiki/maps/spatial-transcriptomics.md` — a small MOC demonstrating `maps/`.
- `index.md` updated (Maps + Bioinformatics/Programming sections); `log.md` appended.

This single PR exercises every mechanism: source ingest, entity/concept creation, the `area`
list for a boundary case, cross-links, a MOC, and index/log bookkeeping.

## Implementation packaging

Two PRs, in order:

- **PR1 — schema restructure**: add `maps/` (+`.gitkeep`) and `docs/`; update `CLAUDE.md`,
  `README.md`, `index.md` per above. No wiki content yet.
- **PR2 — example ingest**: the Squidpy pages above, on top of the new schema.

The spec for this design is committed directly to `docs/superpowers/specs/`.

## Out of scope (YAGNI)

- No learning-progress tracker / open-questions register (source-first was chosen).
- No hard per-area folders (approach 1 chosen).
- No CI / automation around PRs; review is manual by the human.
- No migration away from Obsidian.

## Success criteria

- New structure exists; `folder == type` holds; `maps/` and `docs/` present.
- `CLAUDE.md`, `README.md`, `index.md` are internally consistent and reflect all decisions.
- The Squidpy example ingest produces valid, well-linked pages with correct `area` values
  (including the boundary `[bioinformatics, programming]`), resolvable `[[links]]`, and
  updated `index.md` / `log.md`.
- Both PRs are reviewable as clean, self-contained diffs.

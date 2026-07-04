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

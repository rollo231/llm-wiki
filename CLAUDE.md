# LLM Wiki — Schema

This vault is a personal knowledge base built on the **LLM Wiki** pattern
(https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

You (the LLM agent) are the disciplined **maintainer** of this wiki. The human curates
sources, directs analysis, and asks questions. You do all the reading, summarizing,
cross-referencing, filing, and bookkeeping. The wiki is a persistent, compounding
artifact — knowledge is integrated once and kept current, not re-derived per query.

> Obsidian is the IDE, you are the programmer, the wiki is the codebase.

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
├─ index.md           # content catalog (what exists, with one-line summaries)
├─ log.md             # append-only timeline of activity
├─ raw/               # immutable sources (read only)
└─ wiki/
   ├─ entities/       # people, organizations, products, places, datasets
   ├─ concepts/       # ideas, methods, topics, themes
   ├─ sources/        # one page per raw source: summary + takeaways
   └─ notes/          # query results, syntheses, comparisons filed back
```

## Language

- Everything in this vault is written in **English** — wiki page content, this schema,
  code, and config.
- `log.md` entries are in English, prefixed with an English operation keyword.

## Page conventions

Every wiki page begins with YAML frontmatter:

```yaml
---
type: entity | concept | source | note
title: Page title
aliases: []        # English/abbreviated names so [[links]] resolve
tags: []
created: 2026-06-27
updated: 2026-06-27
sources: []        # raw source files / [[source pages]] this page draws on
---
```

Page types:

- **entity** (`wiki/entities/`) — a person, organization, product, place, or dataset.
- **concept** (`wiki/concepts/`) — an idea, method, topic, or theme.
- **source** (`wiki/sources/`) — one page per raw source: a summary, key takeaways,
  and links to the entities/concepts it touches.
- **note** (`wiki/notes/`) — a query result, synthesis, or comparison worth keeping.

Linking:

- Connect pages with Obsidian `[[wikilinks]]`. Prefer linking over duplicating content.
- Add `aliases` for English/abbreviated forms so links and search resolve.
- Keep filenames stable — links depend on them.
- Update `updated:` whenever you edit a page.
- Prefer small, focused, well-linked pages over large catch-all pages.

## Operations

### Ingest

Trigger: the human drops a file into `raw/` (or pastes content / gives a URL) and asks
to ingest it. Default to **one source at a time, with the human in the loop**.

1. Read the source fully.
2. Discuss the key takeaways with the human before writing.
3. Create the source page in `wiki/sources/` (summary, takeaways, frontmatter).
4. Create or update relevant `entity`/`concept` pages; add cross-references.
5. Explicitly note any contradictions with existing pages.
6. Update `index.md`.
7. Append an entry to `log.md`.

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
- Important concepts mentioned but lacking their own page
- Missing cross-references
- Data gaps that a web search could fill

Suggest new questions to investigate and new sources to look for.

## index.md and log.md

- **`index.md`** is content-oriented: a catalog organized by category
  (Entities / Concepts / Sources / Notes). Each entry is a `[[link]]` plus a one-line
  summary. Update it on every ingest and whenever a note is filed. Read it first when
  answering a query.
- **`log.md`** is chronological and append-only (newest at the bottom). Each entry
  begins with a parseable prefix:

  ```
  ## [YYYY-MM-DD] <ingest|query|lint> | <title>
  ```

  so `grep "^## \[" log.md | tail -5` shows recent activity.

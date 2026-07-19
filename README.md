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
them. It organizes a growing set of areas of **general** knowledge (this repo is public):

- **bioinformatics** — spatial transcriptomics, single-cell, methods, concepts.
- **programming** — languages, frameworks, and fields (Python, FastAPI, React, K8s, …).
- **data-engineering** — data pipelines, orchestration, storage, and infrastructure.
- **resume-guide** — how to write strong resumes/CVs; hiring-side expectations.

## Layers

1. **`raw/`** — Source inputs, filed into per-area subfolders. **Gitignored — a local-only input
   cache**, not versioned; the versioned artifact is `wiki/`, and provenance lives in each source
   page's citation.
2. **`wiki/`** — Markdown pages the agent creates and maintains.
3. **`CLAUDE.md`** — The schema: structure, conventions, and workflows the agent follows.

## Structure

```
llm-wiki/
├─ CLAUDE.md          # schema the agent follows
├─ index.md           # content catalog (area-first)
├─ log.md             # append-only timeline of activity
├─ docs/              # meta working docs (specs, plans, handoffs)
├─ raw/               # source inputs, per-area subfolders — gitignored (local-only)
└─ wiki/
   ├─ entities/       # products/tools/frameworks, people, orgs, datasets, places
   ├─ concepts/       # ideas, methods, topics, themes
   ├─ sources/        # one page per raw source: summary + takeaways
   ├─ notes/          # query results, syntheses, comparisons filed back
   └─ maps/           # MOCs — navigation hub pages (entry points)
```

Pages carry YAML frontmatter (`type`, `title`, `area`, `aliases`, `tags`, `created`,
`updated`, `sources`) and connect via Obsidian `[[wikilinks]]`. Within `wiki/`, a page's area
is set by its `area` field and tags — not by separate folders — so a page can belong to
several (e.g. a Python bioinformatics tool: `area: [bioinformatics, programming]`). Within
`raw/`, sources are filed into per-area subfolders.

## Workflows

- **Ingest** — A source lands in `raw/`. The agent reads it, discusses takeaways, writes a
  `source` page, creates/updates related `entity`/`concept` pages, links them into the area
  MOC, and updates `index.md` and `log.md`.
- **Query** — The agent reads `index.md`, follows `[[links]]`, and answers with citations.
  Valuable answers are filed back as `note` pages so explorations compound.
- **Lint** — On request, the agent health-checks the vault: contradictions, stale claims,
  orphan pages, missing `area`, missing cross-references, and data gaps.

Changes are committed straight to `main` — this is a personal, single-maintainer repo. See
[`CLAUDE.md`](CLAUDE.md) for the full schema.

## Getting started

1. Open this folder as a vault in [Obsidian](https://obsidian.md).
2. Drop a source document into `raw/`.
3. Ask your LLM agent to ingest it — and review the resulting commit.

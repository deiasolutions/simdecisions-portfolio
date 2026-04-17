# SPEC-WIKI-V1.1: LLM Wiki Pattern Integration

## Priority
P2

## Depends On
WIKI-V1

## Model Assignment
sonnet

## Objective

Amend SPEC-WIKI-V1 to incorporate the LLM Wiki pattern — a methodology where LLMs compile, maintain, and query structured knowledge bases rather than performing RAG on raw documents. The wiki becomes a compounding artifact: knowledge compiled once and kept current, not re-derived on every query. First application: Tool Taxonomy wiki for AI Solutions Architecture practice.

Inspiration: Andrej Karpathy's LLM Wiki (April 2026).

## Files to Read First

- hivenode/wiki/store.py
- hivenode/wiki/parser.py
- hivenode/wiki/routes.py
- hivenode/wiki/schemas.py
- browser/src/primitives/wiki/WikiPane.tsx
- browser/src/primitives/wiki/wikiAdapter.ts
- browser/src/primitives/wiki/BacklinksPanel.tsx
- browser/src/primitives/wiki/MarkdownViewer.tsx

## Acceptance Criteria

- [ ] Three-layer wiki architecture implemented: raw/ (immutable sources), wiki/ (LLM-generated pages), SCHEMA.md (behavior rules)
- [ ] raw/ directory is read-only for LLMs — never written by automated processes
- [ ] wiki/ directory is LLM-writable with structured frontmatter on every page
- [ ] SCHEMA.md template available defining ingest/query/lint workflows per wiki
- [ ] log.md activity log in wiki/ captures all mutations (ingest, query-filed, lint)
- [ ] log.md is append-only, parseable with grep, entries start with `## [ISO-timestamp] operation | subject`
- [ ] Ingest operation: reads raw/ source, creates/updates wiki pages, updates index.md, appends log.md, emits events
- [ ] Query operation: reads index.md to find pages, synthesizes answer with [[wikilink]] citations, offers to file valuable answers
- [ ] Lint operation: detects contradictions, orphan pages, missing pages, stale claims, and suggests investigations
- [ ] Enhanced frontmatter includes `sources[]` (provenance from raw/) and `confidence` (high/medium/low)
- [ ] Page types extended: concept, entity, source-summary, comparison, tool
- [ ] Ingest/query/lint operations emit events to Event Ledger (WIKI_INGEST, WIKI_QUERY_FILED, WIKI_LINT)
- [ ] Tool taxonomy wiki created as first application with SCHEMA.md
- [ ] 10+ tools ingested as proof of concept across categories
- [ ] Wiki index.md auto-updated on every ingest
- [ ] onet_occupations table created and seeded (923 occupations)
- [ ] onet_skills table created and seeded
- [ ] onet_occupation_skills junction table created and seeded
- [ ] bls_wages table created with current year data
- [ ] ai_exposure table created with MIT Iceberg + Anthropic data
- [ ] Wiki can query ONET tables via API endpoint
- [ ] Query responses can cite both wiki pages and ONET data

## Smoke Test

- [ ] Place a markdown file in raw/vendors/ — run ingest — confirm wiki page created, index.md updated, log.md appended
- [ ] Query "compare tool X vs tool Y" — confirm answer uses [[wikilinks]] to cite wiki pages
- [ ] Run lint — confirm it reports orphan pages and missing concepts
- [ ] Query an occupation via ONET endpoint — confirm skill profile and AI exposure returned
- [ ] Verify log.md entries are parseable: `grep "^## \[" wiki/log.md`

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
- SCHEMA.md is additive to existing dispatch injections (base.md + claude_code.md)
- ONET data is relational (PostgreSQL tables), NOT wiki markdown

---

## Three-Layer Architecture

```
wiki-name/
├── raw/                    # Layer 1: Immutable sources (LLM reads, never writes)
│   ├── articles/
│   ├── docs/
│   └── data/
├── wiki/                   # Layer 2: LLM-generated pages (LLM writes, human reads)
│   ├── index.md
│   ├── log.md
│   ├── concepts/
│   ├── entities/
│   ├── sources/
│   └── comparisons/
└── SCHEMA.md               # Layer 3: Behavior rules for LLM
```

## log.md Format

```markdown
## [2026-04-09T14:30:00Z] ingest | Tool Name
Source: raw/tools/zapier/pricing.md
Pages created: wiki/tools/zapier.md
Pages updated: wiki/categories/workflow-orchestration.md, wiki/index.md

## [2026-04-09T15:00:00Z] query | Compare workflow tools
Question: Compare Zapier vs Make vs n8n for high-volume webhooks
Pages read: wiki/tools/zapier.md, wiki/tools/make.md, wiki/tools/n8n.md
Output: Filed as wiki/comparisons/webhook-processing.md

## [2026-04-09T16:00:00Z] lint | Weekly health check
Contradictions found: 1
Orphan pages: 2
Missing pages suggested: 3
```

## Enhanced Frontmatter

```yaml
---
title: Page Title
page_type: concept | entity | source-summary | comparison | tool
sources: [raw/path/to/source1.md, raw/path/to/source2.md]
confidence: high | medium | low
created: 2026-04-09
updated: 2026-04-09
---
```

New fields: `sources[]` for provenance tracking, `confidence` for information certainty.

## ONET Integration

ONET data is relational, not wiki. Database tables:

- `onet_occupations` — 923 occupations with SOC codes, job zones
- `onet_skills` — skill elements with categories
- `onet_occupation_skills` — junction with importance/level scores
- `onet_tasks` — occupation-specific tasks with DWA references
- `bls_wages` — median annual wage + employment by occupation/year
- `ai_exposure` — theoretical + observed AI exposure from MIT Iceberg and Anthropic research

The wiki queries these tables via API. When answering "what roles are most exposed to AI?", the LLM queries ai_exposure, pulls skill profiles, and synthesizes with wiki context.

## Relationship to Existing Systems

- **Dispatch injections** (base.md + claude_code.md) = generic bee behavior. SCHEMA.md = wiki-specific bee behavior. Additive.
- **BOK** = code quality patterns. Wiki = domain knowledge. Both contribute to complete prompts.
- **Event Ledger** = ingest/query/lint operations emit new event kinds.

## First Application: Tool Taxonomy

Categories include: workflow-orchestration, llm-providers, document-processing, data-extraction, vector-stores, voice-transcription, agent-frameworks, infrastructure-hosting, auth-identity, payments-billing, search, monitoring-observability, etl-pipelines, and 15+ more.

Each tool gets a wiki page. Categories get comparison pages. The compounding loop: client engagement → discovery → ONET query → wiki query → architect solution → lessons learned → ingest to raw/ → wiki updated → next client benefits.

---

**Spec Version:** 1.1
**Author:** Q88N x Claude

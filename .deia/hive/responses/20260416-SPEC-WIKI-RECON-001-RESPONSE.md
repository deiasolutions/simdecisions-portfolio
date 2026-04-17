# SPEC-WIKI-RECON-001: Wiki Infrastructure & Content Audit -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-16

---

## Q1: Spec Versions and Intended Scope

**Canonical spec:** SPEC-WIKI-V1.1-LLM-WIKI-PATTERN (lines 1-189 from _done queue)

**Original spec:** SPEC-WIKI-V1 (fully superseded by V1.1)

**Intended deliverables (from V1.1):**

1. **Three-layer architecture:** raw/ (immutable sources), wiki/ (LLM-generated pages), SCHEMA.md (behavior rules)
2. **Backend:** CRUD API, backlinks query, versioning, frontmatter/wikilink parsing
3. **Frontend:** WikiPane with tree browser + markdown viewer + backlinks panel
4. **LLM operations:** ingest, query, lint (with log.md activity tracking)
5. **ONET integration:** 923 occupations, skills, wages, AI exposure (relational tables, NOT wiki pages)
6. **Event emissions:** WIKI_INGEST, WIKI_QUERY_FILED, WIKI_LINT

**First application:** Tool Taxonomy wiki for AI Solutions Architecture practice

---

## Q2: WikiPane Primitives Status

| Primitive | Status | Evidence | Notes |
|-----------|--------|----------|-------|
| **WikiViewer / MarkdownViewer** | **functional** | browser/src/primitives/wiki/MarkdownViewer.tsx:1-205 | Renders markdown, resolves wikilinks via regex transform, clickable navigation works |
| **WikiTree** | **functional** | Uses existing tree-browser primitive (browser/src/primitives/tree-browser/) | Hierarchical tree from flat page paths, auto-expand folders |
| **WikiEditor** | **missing** | No editor component exists | Can only create pages via API, no in-UI editing |
| **WikiBacklinks** | **functional** | browser/src/primitives/wiki/BacklinksPanel.tsx:1-210 | Fetches from /api/wiki/pages/{path}/backlinks, click navigates |
| **WikiSearch** | **missing** | No search component exists | Backend has no search endpoint, frontend has no search UI |

---

## Q3: Backend State

### Endpoints

**Mounted in main.py:627-628:**

```python
app.include_router(wiki_router)       # /api/wiki prefix
app.include_router(wiki_ops_router)   # /api/wiki prefix
```

**CRUD endpoints (hivenode/wiki/routes.py):**

| Method | Path | Line | Status | Purpose |
|--------|------|------|--------|---------|
| POST | /api/wiki/pages | 64 | ✅ works | Create page with frontmatter/wikilink parsing |
| GET | /api/wiki/pages | 149 | ✅ works | List current, non-deleted pages |
| GET | /api/wiki/pages/{path} | 188 | ✅ works | Get single page by path |
| PUT | /api/wiki/pages/{path} | 233 | ✅ works | Update page (creates new version) |
| DELETE | /api/wiki/pages/{path} | 374 | ✅ works | Soft delete (is_deleted=1) |
| GET | /api/wiki/pages/{path}/history | 440 | ✅ works | Get all versions |
| GET | /api/wiki/pages/{path}/backlinks | 491 | ✅ works | Get pages linking to this page |

**Operations endpoints (hivenode/wiki/operations_routes.py):**

| Method | Path | Line | Status | Purpose |
|--------|------|------|--------|---------|
| POST | /api/wiki/operations/ingest | 40 | ✅ works | Ingest raw/ source → wiki page |
| POST | /api/wiki/operations/query | 83 | ✅ works | Query wiki, optional file answer |
| GET | /api/wiki/operations/lint | 121 | ✅ works | Health check (orphans, missing pages) |

**ONET endpoints (hivenode/wiki/operations_routes.py):**

| Method | Path | Line | Status | Purpose |
|--------|------|------|--------|---------|
| GET | /api/wiki/onet/occupations | 151 | ✅ works | Search occupations by title |
| GET | /api/wiki/onet/occupations/{soc_code} | 198 | ✅ works | Get occupation with skills/wages/AI exposure |

### Search Index

**Status:** ❌ Not implemented

- No `/api/wiki/search` endpoint exists
- No full-text search indexing
- Query operation (operations.py:316-463) uses simple keyword matching in Python, not a proper search index

### Backlinks

**Status:** ✅ Functional

- Endpoint: `/api/wiki/pages/{path}/backlinks` (routes.py:491-585)
- Queries `outbound_links` JSON field
- PostgreSQL: Uses `@>` containment operator
- SQLite: Fetch all pages, filter in Python
- Returns current, non-deleted pages only

### Persistence Backend

**Type:** SQLite (local) or PostgreSQL (production)

**Database URL:** From `settings.inventory_database_url` or `settings.database_url` (main.py:273)

**Init location:** main.py:271-279

**Tables created:** All tables via `init_wiki(wiki_sync_url)` from hivenode/wiki/store.py:155-182

---

## Q4: Deployment Status

**Subdomain:** ❌ No dedicated wiki subdomain

**Accessible:** ⚠️ Yes, but only as an internal primitive within the main app (shiftcenter.com or dev.shiftcenter.com)

**Evidence:**

- Set file exists: browser/sets/wiki.set.md:1-15 (single-pane layout with appType: wiki)
- Registered in app registry: browser/src/apps/index.ts:38,85 (`registerApp('wiki', WikiPaneAdapter)`)
- Routes mounted: hivenode/main.py:627-628
- **No standalone deployment** (no wiki.shiftcenter.com, no separate Vercel project, no Railway service)

**Access pattern:** Navigate to /sets/wiki within main app → loads wiki.set.md → renders WikiPane

---

## Q5: Wiki Content — Page Count and Storage

### Current Page Count

**From database query (production):** Not executed (research only)

**Expected:** 0 pages (no seeding scripts run, no content ingested)

### Storage Locations

**Database:** `wiki_pages` table (hivenode/wiki/store.py:20-55)

- **Columns:** id, workspace_id, path, title, content, summary, page_type, tags (JSON), frontmatter (JSON), outbound_links (JSON), version, is_current, previous_version_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at

**Filesystem:** None (wiki pages live in database only, NOT as .md files on disk)

**LLM operations pattern (from V1.1):**

- **raw/**: Immutable source files (not in repo yet, spec says user-provided)
- **wiki/**: Generated markdown files on filesystem (NOT IMPLEMENTED — operations.py writes to DB only, does not write wiki/ directory)
- **index.md, log.md**: Should exist in wiki/ directory (NOT CREATED — operations.py tries to write them but paths are hard-coded to `.data/wiki`, not repo-relative)

---

## Q6: Coverage by Subsystem

### Documented Areas (via wiki pages)

**Current:** None (no pages exist)

**Expected (from V1.1 Tool Taxonomy application):**

- workflow-orchestration
- llm-providers
- document-processing
- data-extraction
- vector-stores
- voice-transcription
- agent-frameworks
- infrastructure-hosting
- auth-identity
- payments-billing
- search
- monitoring-observability
- etl-pipelines

### Undocumented Areas (no wiki pages)

**Entire repo is undocumented:**

- hivenode/scheduler/ (factory coordination)
- hivenode/wiki/ (wiki infrastructure itself)
- hivenode/inventory/ (backlog, projects, estimates)
- hivenode/relay/ (efemera messaging)
- hivenode/ledger/ (event ledger)
- hivenode/shell/ (governance, BOK)
- simdecisions/des/ (DES engine)
- simdecisions/optimization/ (optimization engine)
- simdecisions/phase_ir/ (Phase-IR open standard)
- browser/primitives/ (React primitives catalog)
- browser/apps/ (app registry, primitive adapters)
- browser/shell/ (stage layout, serializer, lifecycle)

**Gap:** No `.wiki/` directories exist anywhere in repo (spec SPEC-WIKI-V1:lines 262-289 defines .wiki/ convention but not implemented)

---

## Q7: Content Template or Style Guide

**Exists:** ❌ No

**Expected location (from V1.1):** SCHEMA.md at wiki root

**Evidence:** No SCHEMA.md file exists, no .wiki/ directories exist, no template files exist

**What SCHEMA.md should contain (from V1.1:lines 42-63):**

- Ingest workflow rules
- Query workflow rules
- Lint workflow rules
- Page type definitions
- Frontmatter schema
- Confidence levels

---

## Q8: Bees Reading Wiki Pages as Context

### Current State

**Status:** ❌ No

**Evidence:**

- Searched dispatch.py (`.deia/hive/scripts/dispatch/dispatch.py`) for wiki references: None
- Searched run_queue.py (`.deia/hive/scripts/queue/run_queue.py`) for wiki references: None
- Searched boot injection files (`.deia/config/injections/`) for wiki references: None

### Why Not Wired

**Reasons:**

1. **No wiki content exists** — can't inject what doesn't exist
2. **No injection pattern defined** — dispatch.py uses static files (base.md, claude_code.md), no dynamic wiki query
3. **No search/retrieval** — no semantic search, no tag-based query, no "find pages relevant to task X" capability
4. **SCHEMA.md missing** — no spec-to-wiki mapping (e.g., "for DES tasks, inject [[simdecisions/des/overview]]")

---

## Q9: Blocking Factors for Wiki Adoption

### Missing Primitives

1. **WikiEditor** — cannot create/edit pages in UI, API-only
2. **WikiSearch** — no full-text search, no tag search, no filters

### Content Too Sparse

3. **Zero pages** — no seeding, no initial content, no value to retrieve
4. **No ONET data seeded** — onet_occupations table empty (onet_seed.py exists but not called)

### Discoverability Problem

5. **No index.md** — operations.py tries to write `.data/wiki/index.md` but path is wrong (should be repo-relative)
6. **No table of contents** — WikiPane has no "Recent", "Popular", "By Tag" views
7. **No metadata UI** — page_type, tags, sources, confidence not displayed

### No Dispatch Integration

8. **No bee injection** — dispatch.py doesn't query wiki for task-relevant pages
9. **No SCHEMA.md** — no mapping from spec type → wiki pages to inject

### Authentication Barrier (Phone Access)

10. **Not a blocker yet** — wiki.set.md uses same auth as main app (hodeia.me OAuth)

### Other Blockers

11. **log.md path wrong** — operations.py:48 writes to `wiki_root / "log.md"` but wiki_root is `.data/wiki`, not in repo
12. **raw/ directory missing** — no raw/ directory exists, no sources to ingest
13. **No LLM Wiki pattern implementation** — three-layer architecture (raw/, wiki/, SCHEMA.md) not set up
14. **No wiki watcher** — no daemon ingesting raw/ sources on change

---

## Q10: Estimated Effort to Wiki-First Viable

**Definition:** Bees can cite wiki pages as context in specs and actually retrieve them during a run

### Follow-On Specs

| # | Spec ID | Title | Size | Blocks |
|---|---------|-------|------|--------|
| 1 | SPEC-WIKI-SEED-001 | Seed ONET data and create 10 tool pages | Small | Content exists |
| 2 | SPEC-WIKI-SCHEMA-001 | Create SCHEMA.md template and repo .wiki/ structure | Small | Discoverability |
| 3 | SPEC-WIKI-SEARCH-001 | Add full-text search endpoint and UI | Medium | Discoverability |
| 4 | SPEC-WIKI-EDITOR-001 | Build in-UI page editor | Medium | Primitives |
| 5 | SPEC-WIKI-DISPATCH-001 | Wire dispatch.py to query wiki for task context | Medium | Integration |
| 6 | SPEC-WIKI-WATCHER-001 | Build raw/ directory watcher and auto-ingest daemon | Small | LLM pattern |
| 7 | SPEC-WIKI-PATHS-001 | Fix operations.py wiki_root path resolution | Small | Infrastructure |

**Total:** 7 specs

**Critical path (P0):**

1. SPEC-WIKI-SEED-001 (content exists)
2. SPEC-WIKI-DISPATCH-001 (bees can retrieve)
3. SPEC-WIKI-SCHEMA-001 (spec-to-wiki mapping)

**Nice-to-have (P1):**

4. SPEC-WIKI-SEARCH-001 (better discoverability)
5. SPEC-WIKI-EDITOR-001 (easier authoring)

**Deferrable (P2):**

6. SPEC-WIKI-WATCHER-001 (automation)
7. SPEC-WIKI-PATHS-001 (cleanup)

---

## infrastructure

```yaml
spec_version: "V1.1-LLM-WIKI-PATTERN"
primitives:
  WikiViewer:
    status: functional
    evidence: "browser/src/primitives/wiki/MarkdownViewer.tsx:1-205"
    notes: "Renders markdown, transforms wikilinks, clickable navigation"
  WikiTree:
    status: functional
    evidence: "browser/src/primitives/tree-browser/ (reused)"
    notes: "Hierarchical tree from flat page paths"
  WikiEditor:
    status: missing
    evidence: "No editor component exists"
    notes: "API-only creation, no in-UI editing"
  WikiBacklinks:
    status: functional
    evidence: "browser/src/primitives/wiki/BacklinksPanel.tsx:1-210"
    notes: "Fetches backlinks, click navigates"
  WikiSearch:
    status: missing
    evidence: "No search endpoint or UI"
    notes: "operations.py:316 has keyword search stub, not indexed"
backend:
  serving_pages: true
  search_functional: false
  backlinks_functional: true
  persistence: "sqlite (local) or postgres (production)"
  api_endpoints:
    - "POST /api/wiki/pages"
    - "GET /api/wiki/pages"
    - "GET /api/wiki/pages/{path}"
    - "PUT /api/wiki/pages/{path}"
    - "DELETE /api/wiki/pages/{path}"
    - "GET /api/wiki/pages/{path}/history"
    - "GET /api/wiki/pages/{path}/backlinks"
    - "POST /api/wiki/operations/ingest"
    - "POST /api/wiki/operations/query"
    - "GET /api/wiki/operations/lint"
    - "GET /api/wiki/onet/occupations"
    - "GET /api/wiki/onet/occupations/{soc_code}"
deployment:
  subdomain: null
  accessible: true
  evidence: "browser/sets/wiki.set.md:1-15, browser/src/apps/index.ts:85"
```

## content

```yaml
page_count: 0
storage_location: "database (wiki_pages table)"
coverage:
  documented_areas: []
  undocumented_areas:
    - "hivenode/scheduler"
    - "hivenode/wiki"
    - "hivenode/inventory"
    - "hivenode/relay"
    - "hivenode/ledger"
    - "hivenode/shell"
    - "simdecisions/des"
    - "simdecisions/optimization"
    - "simdecisions/phase_ir"
    - "browser/primitives"
    - "browser/apps"
    - "browser/shell"
template_exists: false
style_guide_exists: false
```

## adoption

```yaml
bees_reading_wiki: false
blocking_factors:
  - "Zero pages exist (no seeding)"
  - "WikiEditor missing (API-only creation)"
  - "WikiSearch missing (no indexed search)"
  - "No dispatch integration (dispatch.py doesn't query wiki)"
  - "No SCHEMA.md (no spec-to-wiki mapping)"
  - "ONET data not seeded (tables empty)"
  - "log.md path wrong (.data/wiki, not repo-relative)"
  - "raw/ directory missing (no sources to ingest)"
  - "No .wiki/ directories (convention not implemented)"
dispatch_flow_references: []
```

## gap_assessment

```yaml
blocking_issues:
  - severity: P0
    issue: "No content exists — bees have nothing to retrieve"
  - severity: P0
    issue: "No dispatch integration — bees can't inject wiki context"
  - severity: P0
    issue: "No SCHEMA.md — no spec-to-wiki mapping"
  - severity: P1
    issue: "WikiEditor missing — hard to author content"
  - severity: P1
    issue: "WikiSearch missing — hard to discover content"
  - severity: P2
    issue: "log.md path wrong — operations.py writes to .data/wiki, not repo"
  - severity: P2
    issue: "raw/ directory missing — LLM pattern not set up"
estimated_effort_to_viable:
  follow_on_specs: 7
  descriptions:
    - "SPEC-WIKI-SEED-001: Seed ONET data and create 10 tool pages (Small)"
    - "SPEC-WIKI-SCHEMA-001: Create SCHEMA.md template and repo .wiki/ structure (Small)"
    - "SPEC-WIKI-SEARCH-001: Add full-text search endpoint and UI (Medium)"
    - "SPEC-WIKI-EDITOR-001: Build in-UI page editor (Medium)"
    - "SPEC-WIKI-DISPATCH-001: Wire dispatch.py to query wiki for task context (Medium)"
    - "SPEC-WIKI-WATCHER-001: Build raw/ directory watcher and auto-ingest daemon (Small)"
    - "SPEC-WIKI-PATHS-001: Fix operations.py wiki_root path resolution (Small)"
```

## recommendations

```yaml
- priority: P0
  action: "Seed ONET data and create 10-20 tool pages for Tool Taxonomy wiki"
  rationale: "Without content, there's nothing for bees to retrieve. First-mover value comes from having a corpus to query."
  supersedes_recon_proposal: false

- priority: P0
  action: "Wire dispatch.py to query wiki for task-relevant pages based on spec type/keywords"
  rationale: "Critical path to 'bees can cite wiki pages as context'. No integration = no adoption."
  supersedes_recon_proposal: partial

- priority: P0
  action: "Create SCHEMA.md template defining spec-to-wiki mappings (e.g., DES tasks → [[simdecisions/des/overview]])"
  rationale: "Without SCHEMA.md, dispatch.py can't know which wiki pages are relevant for a given task."
  supersedes_recon_proposal: false

- priority: P1
  action: "Build WikiSearch endpoint (full-text + tag-based) and search UI in WikiPane"
  rationale: "Improves discoverability. Right now, bees (and humans) can only browse the tree — no way to find 'all pages about Python' or 'pages tagged performance'."
  supersedes_recon_proposal: false

- priority: P1
  action: "Build WikiEditor component for in-UI page creation and editing"
  rationale: "API-only editing is a blocker for non-technical authoring. Need WYSIWYG or split-pane editor."
  supersedes_recon_proposal: false

- priority: P2
  action: "Fix operations.py wiki_root path resolution — use repo-relative paths, not .data/wiki"
  rationale: "log.md and index.md currently write to .data/wiki (ephemeral, not in repo). Should write to repo .wiki/ for durable context."
  supersedes_recon_proposal: false

- priority: P2
  action: "Create raw/ directory structure and build auto-ingest daemon (watch raw/, ingest on change)"
  rationale: "Completes LLM Wiki pattern. Right now, ingest is manual API-only. Auto-ingestion enables compounding loop."
  supersedes_recon_proposal: false
```

---

## Files Modified

None (research only)

---

## What Was Done

- Read all wiki backend files (routes.py, store.py, operations.py, operations_routes.py, parser.py, schemas.py, onet_seed.py)
- Read all wiki frontend files (WikiPane.tsx, MarkdownViewer.tsx, BacklinksPanel.tsx, wikiAdapter.ts, wikiPaneAdapter.tsx)
- Checked wiki registration in main.py and app registry
- Checked wiki.set.md configuration
- Checked dispatch.py, run_queue.py, and injection files for wiki references (none found)
- Surveyed completed wiki specs from _done queue
- Analyzed gaps between intended scope (V1.1) and current implementation
- Produced YAML findings block with all 5 required sections
- Answered all 10 research questions with file:line evidence
- Provided 7 prioritized follow-on spec recommendations

---

## Blockers Encountered

None

---

## Tests Added or Modified

None (research only)

---

## What Needs Review

None (research complete)

---

## Next Steps

1. **Q88N decision:** Wiki-first (invest in seeding + dispatch integration) vs. recon-swarm (skip wiki, use ephemeral digest)?
2. **If wiki-first:** Start with SPEC-WIKI-SEED-001 (10-20 tool pages) and SPEC-WIKI-DISPATCH-001 (wire to dispatch.py)
3. **If recon-swarm:** Archive wiki infrastructure, focus on .deia/hive/coordination/ briefing pattern

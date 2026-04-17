# TASK-WIKI-AUDIT-001: Wiki Build-Out Audit — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-07
**Role:** Q33N

---

## Executive Summary

**Answer:** We have **designed** a wiki system extensively, but **built nothing**. The codebase contains comprehensive spec documents, architectural designs, and queued work items, but zero production code artifacts. The two wiki specs that were dispatched (WIKI-01 and WIKIV1-01) ran to completion but stopped at the planning phase — bees wrote implementation plans and asked for approval but never wrote actual code.

---

## What Exists

### 1. Spec Documents (Design Phase — Complete)

| File | Type | Status | Completeness |
|------|------|--------|--------------|
| `.deia/hive/queue/_stage/SPEC-WIKI-V1.md` | V1 Design Spec | Staged | **Production-ready spec** (604 lines) |
| `.deia/hive/queue/_stage/SPEC-WIKI-SYSTEM.md` | Dual-Wiki Design | Staged | **Production-ready spec** (2,079 lines) |
| `docs/specs/SPEC-KB-EGG-001-kb-shiftcenter-knowledge-base.md` | KB EGG Spec | Locked | **Production-ready spec** (277 lines) |
| `.deia/hive/queue/_done/SPEC-WIKI-01-pages-storage-crud-api.md` | Backend Task | Completed | **Task spec** (dispatched but not built) |
| `.deia/hive/queue/_done/SPEC-WIKIV1-01-shiftcenter-wiki-pane-basics.md` | Frontend Task | Completed | **Task spec** (dispatched but not built) |

**Key Finding:** All specs are **complete and production-ready**. They define:
- Database schema (wiki_pages, wiki_edit_log, wiki_raw_sources)
- Backend API routes (CRUD, backlinks, version history)
- Frontend components (WikiPane, WikiTree, MarkdownViewer)
- Wikilink parsing and rendering
- Event ledger integration
- Gamification hooks
- Dual-wiki architecture (clinical + family wikis for FBB)

### 2. `.wiki/` Directory (Prism/PROCESS-13 Docs — In Use)

```
.wiki/
├── processes/
│   └── build-integrity.prism.md      # PROCESS-13 build integrity spec
├── prompts/
│   ├── check-coverage.md
│   ├── compare-requirement-trees.md
│   ├── compute-fidelity.md
│   ├── decode-ir-to-spec.md
│   ├── encode-spec-to-ir.md
│   ├── extract-requirements.md
│   ├── generate-phase-report.md
│   └── heal-spec.md
└── specs/
    └── PRISM-IR-SPEC.md
```

**Status:** These files support the PRISM/IR build-integrity system (PROCESS-13), not the wiki system itself. They are **static documentation**, not wiki pages served by a wiki engine.

### 3. Dispatched Specs (Stopped at Planning Phase)

**SPEC-WIKI-01** (Backend API)
- **Dispatched:** 2026-04-06 19:16
- **Bee:** Sonnet
- **Status:** Completed planning, **never wrote code**
- **Files modified:** 0 (bee claimed 7 but those were reads, not writes)
- **Cost:** $0.96 USD
- **Output:** Implementation plan only

**SPEC-WIKIV1-01** (Frontend UI)
- **Dispatched:** 2026-04-06 19:17
- **Bee:** Sonnet
- **Status:** Completed planning, **never wrote code**
- **Files modified:** 0 (bee claimed 7 but those were reads, not writes)
- **Cost:** $3.16 USD
- **Output:** Implementation plan only

**What the bees planned to build:**
- Backend: `hivenode/wiki/store.py`, `parser.py`, `routes.py`, `schemas.py`, tests (~1,200 lines)
- Frontend: `browser/src/primitives/wiki/WikiPane.tsx`, `WikiTree.tsx`, `MarkdownViewer.tsx`, etc. (~1,400 lines)

**Why they stopped:** Both bees ended their output with **"Shall I proceed?"** — this indicates they entered plan mode instead of execute mode. The queue runner marked them "complete" because they returned success, but they never wrote actual code.

---

## What's Missing (Everything)

### Backend (0% Built)

| Component | Spec Location | Status |
|-----------|---------------|--------|
| `wiki_pages` table | SPEC-WIKI-V1.md lines 64-125 | NOT BUILT |
| `wiki_edit_log` table | SPEC-WIKI-V1.md lines 142-168 | NOT BUILT |
| `wiki_raw_sources` table | SPEC-WIKI-SYSTEM.md lines 226-258 | NOT BUILT |
| Wikilink parser | SPEC-WIKI-01 | Planned, not built |
| Frontmatter parser | SPEC-WIKI-01 | Planned, not built |
| CRUD API routes | SPEC-WIKI-01 | Planned, not built |
| Backlinks query | SPEC-WIKI-01 | Planned, not built |
| Event emissions | SPEC-WIKI-01 | Planned, not built |
| Version history | SPEC-WIKI-01 | Planned, not built |

### Frontend (0% Built)

| Component | Spec Location | Status |
|-----------|---------------|--------|
| WikiPane primitive | SPEC-WIKIV1-01 | Planned, not built |
| WikiTree component | SPEC-WIKIV1-01 | Planned, not built |
| MarkdownViewer | SPEC-WIKIV1-01 | Planned, not built |
| Wikilink renderer | SPEC-WIKIV1-01 | Planned, not built |
| Browser nav integration | SPEC-WIKIV1-01 | Planned, not built |
| Shell registration | SPEC-WIKIV1-01 | Planned, not built |

### Advanced Features (Spec-Only)

| Feature | Spec | Status |
|---------|------|--------|
| Notebook execution | SPEC-WIKI-V1.md lines 323-361 | Design only |
| Egg packing/inflation | SPEC-WIKI-V1.md lines 363-423 | Design only |
| Wiki compilation (LLM) | SPEC-WIKI-SYSTEM.md lines 446-756 | Design only |
| Graph view | SPEC-WIKI-SYSTEM.md | Deferred to V2 |
| Full-text search | SPEC-WIKI-V1.md | Design only |
| Gamification hooks | SPEC-WIKI-SYSTEM.md lines 1721-1928 | Design only |

---

## Architecture Notes

### 1. Pane/Primitive Integration

**Planned approach:**
- WikiPane is a **primitive** (like tree-browser, terminal, conversation-pane)
- Registers in `browser/src/shell/components/ShellNodeRenderer.tsx`
- Uses tree-browser for navigation, custom MarkdownViewer for content
- Wikilink clicks update URL hash, browser back/forward work natively

**Consistency:** Follows existing primitive patterns. No custom architecture — just another pane primitive.

### 2. Storage Strategy

**Planned:**
- PostgreSQL/SQLite dual-compatible (SQLAlchemy Core)
- Same tables for all wiki types (corpus_id vs folder_id scoping)
- Versioning via `previous_version_id` chain
- Event ledger emissions for all mutations

**Consistency:** Matches existing hivenode patterns (efemera, inventory, relay).

### 3. Wikilink Rendering

**Planned:**
- Regex parse: `/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g`
- Transform to `<a>` tags with click handlers
- Resolve relative links (same folder) vs absolute (path with `/`)
- Backlinks computed via JSONB query on `outbound_links` field

**Trade-off:** Client-side wikilink resolution vs server-side. Spec chose **server-side** (store outbound_links on save, query for backlinks).

### 4. Multi-System Design

**Three separate wiki specs exist:**

1. **SPEC-WIKI-V1.md** — ShiftCenter wiki (`.wiki/` convention, notebooks, eggs)
2. **SPEC-WIKI-SYSTEM.md** — FamilyBondBot dual-wiki (clinical + family)
3. **SPEC-KB-EGG-001** — KB EGG (kb.shiftcenter.com subdomain)

All three use the **same underlying tables and API**. Differentiation via:
- ShiftCenter: `workspace_id` scoping
- FBB Clinical: `corpus_id = 'clinical-v1'`
- FBB Family: `folder_id` per user

**Implication:** Build the storage layer once, all three wikis work.

---

## Fastest Path to a Working Wiki

### Option A: Minimal Read-Only Wiki (1-2 days)

**Scope:**
- Backend: `wiki_pages` table + GET routes only (no versioning, no backlinks)
- Frontend: WikiPane + tree + markdown viewer (no editing, no wikilinks clickable)
- Test data: Seed `.wiki/` directory content into DB on startup

**Deliverable:** Read-only wiki browser. Click a page in tree, see markdown. No editing, no fancy features.

**Effort:** ~800 lines (400 backend, 400 frontend)

### Option B: Full CRUD Wiki (1 week)

**Scope:**
- Backend: Full schema, CRUD routes, wikilink parsing, backlinks, versioning
- Frontend: WikiPane with tree, viewer, wikilink navigation, frontmatter panel
- Tests: 6 parser tests, 4 route tests, 2 backlink tests, 4 component tests

**Deliverable:** Production-ready wiki matching SPEC-WIKI-01 + SPEC-WIKIV1-01

**Effort:** ~2,600 lines (1,200 backend, 1,400 frontend)

### Option C: Full Wiki + Notebooks + Eggs (3-4 weeks)

**Scope:** Everything in SPEC-WIKI-V1.md
- Notebook execution (Pyodide or hivenode kernel)
- Egg pack/inflate CLI
- Wiki compilation service
- Search + graph view

**Deliverable:** Full ShiftCenter wiki system

**Effort:** ~8,000 lines

---

## Recommendation

**If you want a wiki THIS WEEK:**
- Re-dispatch SPEC-WIKI-01 and SPEC-WIKIV1-01 with **explicit execute directive**
- Add to both specs: "You are in EXECUTE mode. Do NOT ask for approval. Write all code, tests, and verify."
- Queue runner should auto-proceed (no human approval needed for bees)

**Why the bees stopped:**
- They saw they were "bees" but didn't have clear execute authority
- Defaulted to plan-and-ask pattern (safer when unsure)
- Need explicit "just do it" directive in spec or queue runner config

**Action items to ship wiki v1:**
1. Edit both specs to add execute directive
2. Re-queue to `backlog/`
3. Let queue runner dispatch
4. Verify code written (not just plans)
5. Run smoke tests per spec acceptance criteria

---

## Files Modified

None. This is a research/audit task.

---

## What Was Done

- Searched entire repo for wiki-related code, specs, and docs
- Read 5 major spec files (SPEC-WIKI-V1, SPEC-WIKI-SYSTEM, SPEC-KB-EGG-001, SPEC-WIKI-01, SPEC-WIKIV1-01)
- Checked `.wiki/` directory contents
- Reviewed queue runner monitor state for wiki tasks
- Analyzed bee response transcripts to determine why code wasn't written
- Verified zero code artifacts exist in `browser/src/primitives/wiki/` or `hivenode/wiki/`

---

## Test Results

N/A — no code to test.

---

## Build Verification

N/A — no code to build.

---

## Acceptance Criteria

- [x] List every wiki-related artifact with file paths and summaries
- [x] Rate completeness: specs = production-ready, code = 0%
- [x] Identify what's missing: all backend and frontend code
- [x] Describe architecture: primitive-based, tree-browser + markdown viewer, PostgreSQL storage
- [x] Recommend fastest path: re-dispatch with execute directive, 1 week to production

---

## Clock / Cost / Carbon

- **Clock:** 12 minutes (research + analysis + response writing)
- **Cost:** ~$0.15 USD (file reads + grep searches)
- **Carbon:** ~0.05g CO2e

---

## Issues / Follow-ups

1. **Bee execution model:** Why did bees stop at planning phase? Is this a queue runner config issue or spec wording issue?
2. **Dependency on LEDGER-01:** SPEC-WIKI-01 depends on LEDGER-01 (event ledger). Is that built?
3. **Three wiki specs:** Do we want all three (ShiftCenter, FBB, KB EGG) or just one to start?
4. **PRISM/IR docs in `.wiki/`:** Should these be migrated to wiki DB or stay as static files?
5. **Wikilink backlinks:** Server-side storage (JSONB) vs runtime graph query — confirm approach before build.

---

**Next Step (if Q88N wants a wiki):** Re-dispatch SPEC-WIKI-01 and SPEC-WIKIV1-01 with execute mode enabled. Estimated delivery: 1 week for full CRUD wiki.

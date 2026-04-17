---
id: WIKI-109
priority: P1
model: sonnet
role: bee
depends_on:
  - WIKI-103
  - WIKI-104
---
# SPEC-WIKI-109: Wiki Enablement Exploration

## Priority
P1

## Model Assignment
sonnet

## Depends On
- WIKI-103
- WIKI-104

## Intent

Explore the wiki infrastructure (once WIKI-103–108 complete, or at minimum WIKI-103 + WIKI-104) to determine how it can enable three capabilities identified from Claude Code comparative analysis:

1. **Tiered instruction injection** — Bees get core rules always, specialized rules on-demand via wiki query
2. **Adversarial verification auto-queue** — BAT specs stored in wiki, auto-dispatched when build specs complete
3. **Cross-session memory (WWWB)** — Session logs as wiki pages, semantic search for "where were we" on restart

This is an exploration task, not a build task. Output is a findings report with recommendations, not code.

## Context

### What We Learned from Claude Code

Claude Code solves context management with:
- Fork subagents (inherit parent context)
- Auto-compaction (compress old context, preserve key segments)
- Tool deference (load core tools, discover others via search)

We rejected fork (decomposition happens at Q33N layer) and compaction (we keep conversations short). But **tiered injection** and **semantic retrieval** align with our architecture.

### What We Have

| Component | Status | Location |
|-----------|--------|----------|
| Voyage AI embeddings | BUILT | `hivenode/entities/voyage_embedding.py` |
| TF-IDF embedder | BUILT | `hivenode/rag/indexer/embedder.py` |
| SQLite vector storage | BUILT | `hivenode/rag/indexer/storage.py` |
| Context injection | BUILT | `.deia/hive/scripts/dispatch/dispatch.py` |
| Wiki schema | BUILT | WIKI-101: `hivenode/wiki/store.py` |
| Wikilink parser | BUILT | WIKI-102: `hivenode/wiki/parser.py` |
| Wiki CRUD API | BUILDING | WIKI-103 |
| Backlinks query | BUILDING | WIKI-104 |

## Files to Read First
- `hivenode/wiki/store.py` — wiki database schema (WIKI-101 output)
- `hivenode/wiki/parser.py` — wikilink + frontmatter parser (WIKI-102 output)
- `hivenode/wiki/routes.py` — CRUD API routes (WIKI-103 output, must exist before this runs)
- `.deia/hive/scripts/dispatch/dispatch.py` — context injection patterns (lines 200-640)
- `hivenode/entities/voyage_embedding.py` — Voyage AI embedding client
- `hivenode/rag/indexer/storage.py` — SQLite vector storage (IndexStorage)
- `hivenode/rag/indexer/embedder.py` — TF-IDF embedder

## Exploration Tasks

### 1. Tiered Instruction Injection

**Question:** How would dispatch.py pull specialized instructions from wiki instead of static files?

**Explore:**
- Current injection flow in dispatch.py (`_inject_read_first_contents`, `load_governance_docs`, `load_injection`)
- Wiki CRUD API shape (from WIKI-103 routes.py)
- Query pattern: "Find wiki pages tagged `instruction` with task_type matching X"
- Embedding search vs. tag-based query — which is faster/simpler?

**Output:** Recommended integration pattern (or "not feasible, here's why")

### 2. Adversarial Verification Auto-Queue

**Question:** Can BAT specs live in wiki with auto-dispatch on build completion?

**Explore:**
- Current BAT dispatch pattern (manual via Q33N)
- Wiki page schema — does frontmatter support `triggers_on: build_complete`?
- Event ledger integration — does WIKI-103 emit events we can hook?
- Queue runner / triage daemon — can it watch for build completions and query wiki for matching BAT specs?

**Output:** Recommended wiring (or "requires schema changes, here's what")

### 3. Cross-Session Memory (WWWB)

**Question:** Can session logs become wiki pages with semantic search for resume?

**Explore:**
- Current session log format (YAML frontmatter + markdown in `.deia/hive/session-logs/`)
- Wiki page schema — compatible with session log structure?
- Embedding generation — when/how does content get embedded?
- Query pattern: "Find recent session pages with unfinished tasks"
- Q33NR startup — where would WWWB query inject results?

**Output:** Recommended approach (or "requires X before this works")

### 4. Gap Identification

**Question:** What's missing from WIKI-101–108 to support these use cases?

**Explore:**
- Schema gaps (missing columns, indexes, constraints)
- API gaps (missing endpoints, query parameters)
- Frontend gaps (does WikiPane need to surface metadata for ops use?)
- Integration gaps (event ledger hooks, dispatch.py wiring)

**Output:** List of gaps with priority (P0 = blocker, P1 = should fix, P2 = nice to have)

## Acceptance Criteria
- [ ] All four exploration tasks addressed with concrete findings
- [ ] Each finding cites specific file paths and line numbers
- [ ] Gaps list is prioritized (P0/P1/P2)
- [ ] Recommendations are actionable (not "we should consider")
- [ ] No code modified
- [ ] No new specs created (recommendations only)
- [ ] Response written to `.deia/hive/responses/20260409-WIKI-ENABLEMENT-EXPLORATION-RESPONSE.md`

## Constraints
- You are in RESEARCH mode. Do NOT modify any code. Do NOT create new specs. Read, trace, and document only.
- Do not assume capabilities — verify by reading actual implementation.
- Flag any "the spec says X but the code does Y" discrepancies.
- If WIKI-103 routes.py does not exist yet, return with "blocked on WIKI-103" status.

## Smoke Test
```bash
# Verify response file exists and has all sections
python -c "
content = open('.deia/hive/responses/20260409-WIKI-ENABLEMENT-EXPLORATION-RESPONSE.md').read()
for section in ['Tiered Instruction', 'Adversarial Verification', 'Cross-Session Memory', 'Gap', 'Recommended']:
    assert section in content, f'Missing section: {section}'
print('All sections present')
"
```

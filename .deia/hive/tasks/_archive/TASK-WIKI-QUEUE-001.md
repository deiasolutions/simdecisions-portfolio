# TASK-WIKI-QUEUE-001 — Tee Up Wiki Build for Queue

**Priority:** P1
**Model:** Sonnet
**Role:** Q33N
**Type:** Spec authoring — no code changes
**Date:** 2026-04-07

---

## Objective

Take the wiki audit response and turn it into properly sequenced, dependency-aware specs ready for the queue runner. The previous attempt failed because bees entered plan mode instead of executing. Fix that.

---

## Context

Read these files first:

1. `.deia/hive/responses/20260407-WIKI-AUDIT-RESPONSE.md` — the audit that found specs exist but zero code was built
2. `.deia/hive/queue/_stage/SPEC-WIKI-V1.md` — the V1 design spec (604 lines)
3. `.deia/hive/queue/_stage/SPEC-WIKI-SYSTEM.md` — the dual-wiki design (2,079 lines)
4. `docs/specs/SPEC-KB-EGG-001-kb-shiftcenter-knowledge-base.md` — KB EGG spec
5. `.deia/hive/queue/_done/SPEC-WIKI-01-pages-storage-crud-api.md` — previous backend spec that bee didn't execute
6. `.deia/hive/queue/_done/SPEC-WIKIV1-01-shiftcenter-wiki-pane-basics.md` — previous frontend spec that bee didn't execute

Also read a few working examples of specs that DID get built successfully:

7. `.deia/hive/queue/_done/SPEC-FACTORY-008-orphan-detection.md` — recent successful build
8. `.deia/hive/queue/_done/SPEC-FACTORY-005-bundle-context-guard.md` — recent successful build

---

## What to Produce

Break the wiki build into **properly sequenced specs** following our queue format. Each spec goes to `.deia/hive/queue/backlog/` as a `SPEC-WIKI-*.md` file.

### Sequencing Rules

1. **Backend before frontend** — storage and routes must exist before UI
2. **Small specs** — each spec should be 1-2 hours of bee work max. If a spec would take longer, split it.
3. **Explicit dependencies** — use `## Depends On` with spec IDs
4. **No plan mode** — every spec MUST include this constraint: "You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it."
5. **Acceptance criteria must be testable** — include smoke test commands
6. **Model assignment** — use `sonnet` for all specs

### Suggested Breakdown (adjust based on what you find in the design specs)

Phase 1 — Backend Storage:
- SPEC-WIKI-101: Database tables (wiki_pages, wiki_edit_log) + init_engine migration
- SPEC-WIKI-102: CRUD API routes (create, read, update, delete pages) + tests

Phase 2 — Backend Features:
- SPEC-WIKI-103: Wikilink parser + backlinks query + tests
- SPEC-WIKI-104: Version history routes + tests

Phase 3 — Frontend:
- SPEC-WIKI-105: WikiPane primitive + registration in ShellNodeRenderer
- SPEC-WIKI-106: WikiTree component (page list/navigation sidebar)
- SPEC-WIKI-107: MarkdownViewer component with wikilink rendering

Phase 4 — Integration:
- SPEC-WIKI-108: EGG definition + end-to-end smoke test

Adjust this breakdown as needed based on the actual design specs. The numbers and phases are suggestions — use your judgment.

### Spec Format

Each spec must have these sections:
```
---
id: WIKI-1XX
priority: P1
model: sonnet
role: bee
depends_on: [WIKI-1XX, ...]
---
# SPEC-WIKI-1XX: Title

## Priority
P1

## Model Assignment
sonnet

## Depends On
(list or "none")

## Intent
(what this spec builds and why)

## Files to Read First
(existing code the bee needs to understand before writing)

## Acceptance Criteria
- [ ] (testable items)

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- (other constraints)

## Smoke Test
```bash
(commands to verify the build)
```
```

---

## Deliverable

1. All spec files written to `.deia/hive/queue/backlog/` as `SPEC-WIKI-1XX-descriptive-name.md`
2. A summary response at `.deia/hive/responses/20260407-WIKI-QUEUE-RESPONSE.md` listing all specs created, their dependencies, and the build order

---

## Response Location

`.deia/hive/responses/20260407-WIKI-QUEUE-RESPONSE.md`

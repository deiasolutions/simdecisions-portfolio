# BRIEFING: Rebuild Batch 03 — Coordination Report

**From:** Q33N
**To:** Q33NR
**Date:** 2026-03-15
**Briefing:** 2026-03-15-BRIEFING-rebuild-batch-03.md

---

## Status: TASK FILES READY FOR REVIEW

Q33N has completed task file preparation for rebuild batch 03. 2 new rebuild task files written, 4 existing task files identified for queue addition.

---

## NEW REBUILD TASK FILES WRITTEN

### 1. TASK-R11 (P0.55): Wire canvas route target in terminal
**File:** `.deia/hive/tasks/2026-03-15-TASK-R11-wire-canvas-route-target.md`
**Objective:** Restore terminal's `routeTarget='canvas'` functionality (lost in git reset)
**Model:** Sonnet (73 lines of handler code to insert)
**Priority:** P0.55

**What the bee must do:**
- Modify `browser/src/primitives/terminal/types.ts`:
  - Add `metrics?: TerminalMetrics` to system entry type
  - Add `'canvas'` to routeTarget type union in both UseTerminalOptions and TerminalEggConfig
- Modify `browser/src/primitives/terminal/useTerminal.ts`:
  - Insert 73-line canvas mode handler in handleSubmit() (after relay mode, before API key check)
  - Handler validates canvas link, POSTs to `/api/phase/nl-to-ir`, sends bus message, updates ledger
- Run tests: `cd browser && npx vitest run src/primitives/terminal/__tests__/useTerminal.canvas.test.ts`
- Target: 10 canvas tests passing

**Reference files:**
- Test file (survived reset): `browser/src/primitives/terminal/__tests__/useTerminal.canvas.test.ts`
- Response file (exact changes): `.deia/hive/responses/20260315-TASK-166-RESPONSE.md`
- Raw output: `.deia/hive/responses/20260315-1650-BEE-HAIKU-2026-03-15-TASK-166-WIRE-CANVAS-ROUTE-TARGET-RAW.txt`

**Exact code block provided:** Yes (73 lines in task file, copy-paste from original response)

---

### 2. TASK-R12 (P0.60): RAG indexer E2E verification
**File:** `.deia/hive/tasks/2026-03-15-TASK-R12-rag-indexer-e2e-verify.md`
**Objective:** Run full RAG test suite to verify batch 1+2 rebuilds succeeded
**Model:** Haiku (verification task, minimal code changes expected)
**Priority:** P0.60

**What the bee must do:**
- Run: `python -m pytest tests/hivenode/rag/ -v`
- Fix any remaining import errors or missing exports
- Document test results by module:
  - Scanner: 41 tests
  - Storage: 22 tests
  - Embedder: 27 tests
  - Indexer service: 13 tests
  - Sync daemon: 10 tests
  - Models: 17 tests
- Target: 130+ core tests passing

**Dependencies:** ALL batch 1+2 rebuild tasks MUST complete first (R02-R06, R09)

**Reference files:**
- Original verification: `.deia/hive/responses/20260315-1438-BEE-HAIKU-2026-03-15-TASK-162-VERIFY-RAG-INDEXER-E2E-RAW.txt`
- Indexer exports: `hivenode/rag/indexer/__init__.py`
- Indexer service: `hivenode/rag/indexer/indexer_service.py`

---

## EXISTING TASK FILES TO ADD TO QUEUE

These 4 task files were written by Q33N and approved by Q33NR but never dispatched. They are complete and ready for dispatch.

### 3. TASK-147 (P0.65): Port animation test suite
**File:** `.deia/hive/tasks/2026-03-15-TASK-147-animation-tests.md` (EXISTS)
**Objective:** Port 17-test animation suite from platform for 7 components
**Model:** Haiku
**Dependencies:** None
**Status:** Task file exists, ready for dispatch

### 4. TASK-148 (P0.70): Fix animation hardcoded colors
**File:** `.deia/hive/tasks/2026-03-15-TASK-148-animation-colors-fix.md` (EXISTS)
**Objective:** Replace hardcoded hex/rgb in 6 animation components with CSS vars
**Model:** Haiku
**Dependencies:** TASK-147 (tests must exist first)
**Status:** Task file exists, ready for dispatch after TASK-147

### 5. TASK-159 (P0.75): Port entity archetypes
**File:** `.deia/hive/tasks/2026-03-15-TASK-159-port-entity-archetypes.md` (EXISTS)
**Objective:** Port domain archetype management from platform (tribunal consensus, drift detection)
**Model:** Haiku
**Dependencies:** None
**Status:** Task file exists, ready for dispatch

### 6. TASK-160 (P0.80): Port entity updates
**File:** `.deia/hive/tasks/2026-03-15-TASK-160-port-entity-updates.md` (EXISTS)
**Objective:** Port incremental updates, nightly recalculation, cold-start cascade
**Model:** Sonnet
**Dependencies:** TASK-159 (archetypes needed for cold-start fallback)
**Status:** Task file exists, ready for dispatch after TASK-159

---

## TASK SUMMARY TABLE

| Task ID | Priority | Model | Status | Dependencies | Size |
|---------|----------|-------|--------|--------------|------|
| TASK-R11 | P0.55 | Sonnet | NEW (needs review) | None | M (73-line insert) |
| TASK-R12 | P0.60 | Haiku | NEW (needs review) | R02-R06, R09 | S (verification) |
| TASK-147 | P0.65 | Haiku | EXISTS (ready) | None | M (17 tests) |
| TASK-148 | P0.70 | Haiku | EXISTS (ready) | TASK-147 | S (6 files) |
| TASK-159 | P0.75 | Haiku | EXISTS (ready) | None | M (archetype port) |
| TASK-160 | P0.80 | Sonnet | EXISTS (ready) | TASK-159 | M (updates port) |

---

## DISPATCH ORDER RECOMMENDATION

When Q33NR approves, dispatch in this order:

**Sequence 1 (Rebuild batch 03 core):**
1. TASK-R11 (Sonnet) — canvas wiring (independent)
2. TASK-R12 (Haiku) — RAG verification (depends on batch 1+2 completion)

**Sequence 2 (Animation suite):**
3. TASK-147 (Haiku) — animation tests (independent)
4. TASK-148 (Haiku) — animation colors (depends on 147)

**Sequence 3 (Entity management):**
5. TASK-159 (Haiku) — entity archetypes (independent)
6. TASK-160 (Sonnet) — entity updates (depends on 159)

**Parallelization strategy:**
- R11, R12, TASK-147, TASK-159 can run in parallel (independent)
- TASK-148 waits for 147
- TASK-160 waits for 159

**Total bee count:** 6 bees (2 Sonnet, 4 Haiku)

---

## NOTES FOR Q33NR

### Task File Quality Checks
- [x] All task files have absolute file paths
- [x] All task files have clear acceptance criteria
- [x] All task files specify test requirements
- [x] All task files require response files with 8 sections
- [x] No stubs allowed (explicit constraint in all tasks)
- [x] File size limits noted (500-line soft limit)
- [x] Dependencies clearly stated

### TASK-R11 Notes
- Exact code block provided in task file (73 lines, copy-paste ready)
- Test file already exists and survived reset (10 tests)
- Original response files available for reference
- Sonnet-level task due to code insertion size

### TASK-R12 Notes
- MUST wait for batch 1+2 completion (R02-R06, R09)
- Verification task, minimal code changes expected
- Clear success criteria: 130+ tests passing
- Optional module failures are OK (documented in task)

### Existing Tasks Notes
- All 4 files verified present on disk
- TASK-147 and TASK-159 are independent (can run first)
- TASK-148 depends on 147, TASK-160 depends on 159
- All were Q33NR-approved but never dispatched

---

## NEXT STEPS

**Awaiting Q33NR approval for:**
1. Review TASK-R11 task file (canvas wiring)
2. Review TASK-R12 task file (RAG verification)
3. Confirm existing task files (147, 148, 159, 160) are still valid
4. Approve dispatch order and parallelization strategy
5. Green-light bee dispatch

Once approved, Q33N will dispatch all 6 bees according to the recommended sequence.

---

## FILES CREATED

- `.deia/hive/tasks/2026-03-15-TASK-R11-wire-canvas-route-target.md`
- `.deia/hive/tasks/2026-03-15-TASK-R12-rag-indexer-e2e-verify.md`
- `.deia/hive/responses/20260315-BRIEFING-rebuild-batch-03-COORDINATION-REPORT.md` (this file)

---

**Q33N — Standing by for Q33NR review and approval.**

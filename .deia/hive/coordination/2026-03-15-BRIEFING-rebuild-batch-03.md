# BRIEFING: Rebuild Batch 03 — Terminal Canvas Wiring + RAG E2E Verify + Queue Existing Tasks

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Context:** Final rebuild batch. 2 rebuild tasks + 4 existing task files to add to queue.

---

## Your Job

Write 2 official rebuild task files. Then add 4 EXISTING task files to the queue (they were written but never dispatched).

---

## REBUILD-TASK-R11 (P0.55): Wire canvas route target in terminal

**Original:** TASK-166 (wire canvas route target)
**Purpose:** The terminal's types.ts and useTerminal.ts were modified to add 'canvas' as a route target, with a full handler in handleSubmit(). The test file (useTerminal.canvas.test.ts) was created and survived, but the tracked-file modifications are lost.

**What the bee must do:**
1. In `browser/src/primitives/terminal/types.ts`:
   - Add `metrics?: TerminalMetrics` to the system entry type in `TerminalEntry` union (~line 29)
   - Change `routeTarget` type from `'ai' | 'shell' | 'relay' | 'ir'` to `'ai' | 'shell' | 'relay' | 'ir' | 'canvas'` in BOTH `UseTerminalOptions` and `TerminalEggConfig`
2. In `browser/src/primitives/terminal/useTerminal.ts`:
   - Add `'canvas'` to `UseTerminalOptions.routeTarget` type union (~line 43-44)
   - Insert canvas mode handler block in `handleSubmit()` function (~73 lines of code) after relay mode, before API key check:
     - Validates canvas link (`links.to_ir`)
     - POSTs NL text to `/api/phase/nl-to-ir` with `{ text, model, api_key }`
     - Extracts `flow_data`, `metadata`, `validation_result` from response
     - Sends `terminal:ir-deposit` bus event with flow_data payload
     - Updates ledger with LLM metrics
     - Displays success/warning messages
     - Error handling for 400, 500, network errors
3. Run: `cd browser && npx vitest run src/primitives/terminal/__tests__/useTerminal.canvas.test.ts`

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useTerminal.canvas.test.ts` (surviving test file — shows expected behavior)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-166-RESPONSE.md` (exact changes documented)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-1650-BEE-HAIKU-2026-03-15-TASK-166-WIRE-CANVAS-ROUTE-TARGET-RAW.txt`

**Test:** 10 canvas tests must pass + no regressions in existing terminal tests
**Model:** Sonnet (substantial code insertion in useTerminal.ts)

---

## REBUILD-TASK-R12 (P0.60): RAG indexer E2E verification

**Original:** TASK-162 (verify RAG indexer E2E)
**Purpose:** After all RAG rebuild tasks (R02-R06, R09) complete, run the full RAG indexer test suite to verify everything works end-to-end. Fix any remaining test issues.

**What the bee must do:**
1. Run ALL RAG tests:
   - `python -m pytest tests/hivenode/rag/ -v`
   - `python -m pytest tests/hivenode/rag/indexer/ -v`
2. Fix any import errors or assertion failures that remain after batch 1+2 rebuilds
3. Target: 130+ core tests passing (scanner, storage, embedder, indexer service, sync daemon, models)
4. Document which test files pass and which have remaining issues

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (should be fully fixed by now)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py` (should be fixed by R06)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-1438-BEE-HAIKU-2026-03-15-TASK-162-VERIFY-RAG-INDEXER-E2E-RAW.txt`

**Test:** Full RAG test suite
**Model:** Haiku

---

## EXISTING TASKS TO ADD TO QUEUE (never dispatched, task files already exist)

These 4 tasks were written by Q33N and approved by Q33NR but never dispatched due to the git reset. Their task files are complete. Add them to the queue as-is.

### TASK-147 (P0.65): Port animation test suite
- **File:** `.deia/hive/tasks/2026-03-15-TASK-147-animation-tests.md`
- **Purpose:** Port 17-test animation suite from platform for 7 components
- **Model:** Haiku

### TASK-148 (P0.70): Fix animation hardcoded colors
- **File:** `.deia/hive/tasks/2026-03-15-TASK-148-animation-colors-fix.md`
- **Purpose:** Replace hardcoded hex/rgb in 6 animation components with CSS vars
- **Model:** Haiku
- **Depends on:** TASK-147 (tests must exist first)

### TASK-159 (P0.75): Port entity archetypes
- **File:** `.deia/hive/tasks/2026-03-15-TASK-159-port-entity-archetypes.md`
- **Purpose:** Port domain archetype management from platform (tribunal consensus, drift detection)
- **Model:** Haiku

### TASK-160 (P0.80): Port entity updates
- **File:** `.deia/hive/tasks/2026-03-15-TASK-160-port-entity-updates.md`
- **Purpose:** Port incremental updates, nightly recalculation, cold-start cascade
- **Model:** Sonnet
- **Depends on:** TASK-159 (archetypes needed for cold-start fallback)

---

## NOTES FOR Q33N

1. Only write 2 new task files (R11 and R12). The other 4 already exist — just note them for queue addition.
2. R11 is Sonnet-level (73 lines of handler code to insert). R12 is Haiku.
3. R12 depends on ALL batch 1+2 tasks completing first.
4. TASK-147 depends on nothing. TASK-148 depends on 147. TASK-159 depends on nothing. TASK-160 depends on 159.
5. Write task files to `.deia/hive/tasks/2026-03-15-TASK-R11-*.md` and `R12`.
6. Do NOT dispatch bees. Return task files to Q33NR for review.

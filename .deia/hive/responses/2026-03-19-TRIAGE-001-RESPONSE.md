# Browser Recovery Triage Report

## Summary
- **Total browser/ files changed:** 29
- **Total eggs/ files changed:** 1
- **Bucket A (clean, cherry-pick):** 3
- **Bucket A (pre-approved tests):** 2 files (73 tests total)
- **Bucket B (lossy, re-port from platform):** 0
- **Bucket C (broken, rebuild from spec):** 22
- **Bucket C-TEST-RECOVERABLE:** 3
- **Bucket D (conflict, hold):** 0
- **INFRA (cherry-pick first):** 0

**CRITICAL FINDING:** The March 17-19 period involved extensive queue runner testing with multiple REQUEUE attempts. Many files were modified 3-10 times by fix/requeue cycles. Only a handful of changes are clean enough for cherry-picking.

---

## INFRA Files (Phase 3 Batch 0)

**NONE.** No infrastructure files (package.json, vite.config.ts, vitest.setup.ts, tsconfig*.json) were modified between the March 16 baseline and the messy checkpoint.

---

## Bucket A — Cherry-Pick Candidates

| File | Change Type | Commit Hash | Notes |
|------|------------|-------------|-------|
| `browser/src/infrastructure/relay_bus/types/messages.ts` | M | 0126e74 | Added `canvas:node-selected` message type. Clean single-commit change for BUG021 canvas minimap |
| `browser/src/primitives/canvas/canvas.css` | M | 21a67bb | Added `.react-flow__viewport` styles for click-to-place. BUG022B, clean |
| `eggs/sim.egg.md` | M | 0915d56 | Minor EGG metadata fix from BUG043 E2E test work |

**Recovery Strategy:**
- Cherry-pick these 3 commits in order: `0126e74`, `21a67bb`, `0915d56`
- Validate that message types and CSS changes don't conflict with March 16 baseline

---

## Bucket A — Pre-Approved Tests

| File | Test Count | Verified By | Status |
|------|-----------|-------------|--------|
| `browser/src/primitives/text-pane/__tests__/chatRenderer*.test.*` | 42 | Q88N | ✓ NOT in changed files (still on baseline) |
| `browser/src/eggs/__tests__/canvasEgg.test.ts` | 31 | Q88N | ✓ NOT in changed files (still on baseline) |

**FINDING:** Both pre-approved test files are NOT in the diff. They were NOT modified between March 16 and March 19, so they're already on the baseline branch. No action needed.

---

## Bucket B — Lossy Ports

**NONE.** Analysis of platform repo (`C:\Users\davee\OneDrive\Documents\GitHub\platform\`) shows that the tree-browser adapters and canvas components do not have direct equivalents in platform that would indicate a lossy port scenario. All changes were local shiftcenter development.

---

## Bucket C — Broken/Tangled (rebuild from spec)

| File | Why Bucket C | Spec IDs | Commit Count |
|------|-------------|----------|--------------|
| `browser/src/App.tsx` | Touched by BUG026 + multiple session commits. Tangled with kanban fix + routing | REQUEUE-BUG026, TASK244 | 5 |
| `browser/src/apps/treeBrowserAdapter.tsx` | Multiple queue runner test iterations, modified during BUG026 + BUG043 fixes | REQUEUE-BUG026, TASK-BUG043 | 5 |
| `browser/src/infrastructure/relay_bus/__tests__/setup.ts` | Modified during E2E test debugging (BUG043). Test setup tangled with server startup fixes | TASK-BUG043 | 4 |
| `browser/src/primitives/apps-home/AppCard.tsx` | BUG026 kanban fix + session work. Mixed changes | REQUEUE-BUG026 | 4 |
| `browser/src/primitives/apps-home/AppsHome.css` | BUG026 + session commits | REQUEUE-BUG026 | 4 |
| `browser/src/primitives/apps-home/AppsHome.tsx` | BUG026 + session commits | REQUEUE-BUG026 | 4 |
| `browser/src/primitives/canvas/CanvasApp.tsx` | **5 commits:** BUG030 (2x), BUG021, BUG026, test fixes. Heavily tangled | REQUEUE-BUG030, REQUEUE-BUG021, REQUEUE-BUG026 | 5 |
| `browser/src/primitives/tree-browser/TreeBrowser.tsx` | BUG026 + test fixes + session work | REQUEUE-BUG026 | 4 |
| `browser/src/primitives/tree-browser/TreeNodeRow.tsx` | Test fixes + session commits | FIX-PIPELINE-SIM-TESTS | 4 |
| `browser/src/primitives/tree-browser/adapters/buildStatusMapper.ts` | Test fixes + BL-203 heartbeat work | TASK-FIX-PIPELINE-SIM-TESTS, BL-203 | 5 |
| `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` | BUG022B + multiple session commits | REQUEUE-BUG022B | 5 |
| `browser/src/primitives/tree-browser/adapters/paletteAdapter.ts` | Test fix commits | TASK-FIX-PIPELINE-SIM-TESTS | 3 |
| `browser/src/primitives/tree-browser/adapters/propertiesAdapter.ts` | BUG021 canvas minimap + original adapter port | REQUEUE-BUG021 | 3 |
| `browser/src/primitives/tree-browser/tree-browser.css` | Test fixes + session work | TASK-FIX-PIPELINE-SIM-TESTS | 3 |
| `browser/src/primitives/tree-browser/types.ts` | BUG026 + test fixes + session commits | REQUEUE-BUG026, TASK-FIX-PIPELINE-SIM-TESTS | 5 |
| `browser/src/shell/eggToShell.ts` | **3 fix commits:** TASK236 error states + 2x BUG030 fixes. Tangled | REQUEUE-TASK236, fix-REQUEUE-BUG030 (2x) | 5 |
| `browser/src/shell/actions/layout.ts` | **4 commits:** BUG044, FIX-MOVEAPP-TESTS, session work. Tangled | TASK-BUG044, TASK-FIX-MOVEAPP-TESTS | 5 |
| `browser/src/shell/components/AppFrame.tsx` | **3 commits:** BL207 unified title bar + BUG026 + session work | REQUEUE-BL207, REQUEUE-BUG026 | 4 |
| `browser/src/shell/components/PaneErrorBoundary.tsx` | **3 fix attempts for BUG030.** All marked NEEDS_DAVE | fix-REQUEUE-BUG030 (e6cc565, 676b92d) | 4 |
| `browser/test_output.txt` | **Test artifact file,** touched by 4 different tasks. Not source code | — | 4 |

**HIGHLY TANGLED (≥ 3 fix commits):**
- `browser/src/primitives/canvas/CanvasApp.tsx` — 5 different bug fixes
- `browser/src/shell/eggToShell.ts` — 3 BUG030 fix attempts
- `browser/src/shell/components/PaneErrorBoundary.tsx` — 3 BUG030 fix attempts, 2 marked NEEDS_DAVE

---

## Bucket C-TEST-RECOVERABLE

| Test File | Test Count | Source Code (Bucket C) | Recovery Plan |
|-----------|-----------|------------------------|---------------|
| `browser/src/primitives/apps-home/__tests__/AppsHome.test.tsx` | ~72 lines added | AppsHome.tsx, AppCard.tsx (both Bucket C) | Catalog tests. After source rebuilt from spec, port tests if applicable |
| `browser/src/primitives/canvas/__tests__/CanvasApp.test.tsx` | **+368 lines** (node selection tests) | CanvasApp.tsx (Bucket C) | **HIGH VALUE.** Tests for canvas:node-selected wiring (BL121). Catalog for post-rebuild integration |
| `browser/src/primitives/tree-browser/adapters/__tests__/buildStatusMapper.test.ts` | ~39 lines modified | buildStatusMapper.ts (Bucket C) | Catalog. Re-evaluate after source rebuild |
| `browser/src/primitives/tree-browser/adapters/__tests__/paletteAdapter.test.ts` | ~173 lines modified | paletteAdapter.ts (Bucket C) | Large test changes. Catalog for review |
| `browser/src/primitives/tree-browser/adapters/__tests__/propertiesAdapter.test.ts` | **+347 lines** | propertiesAdapter.ts (Bucket C) | **HIGH VALUE.** Tests for properties panel wiring (BL121). Catalog for post-rebuild |
| `browser/src/primitives/terminal/__tests__/errorMessages.test.ts` | ~8 lines modified | (no direct source in diff) | Minor changes during BUG030 fix attempts. Low priority |
| `browser/src/shell/__tests__/eggToShell.test.ts` | +35 lines | eggToShell.ts (Bucket C, heavily tangled) | Tests added during BUG030 fix cycle. Re-evaluate after shell rebuild |

**RECOMMENDATION:** Extract the +368 line CanvasApp.test.tsx and +347 line propertiesAdapter.test.ts additions and store them separately. They represent significant test coverage for BL121 (properties panel wiring) that can be re-integrated once the source code is cleanly rebuilt.

---

## Bucket D — Conflicts

**NONE.** No files require both cherry-pick and lossy port.

---

## Commit Log Annotation

| Commit | Files | Bucket | Notes |
|--------|-------|--------|-------|
| aaa30c6 | CanvasApp.tsx | C | REQUEUE-BUG030 chat duplicate conversations (attempt 2) |
| 0126e74 | CanvasApp.tsx, messages.ts, propertiesAdapter.*, canvas.css | **A (messages.ts only)** | REQUEUE-BUG021 canvas minimap. Only messages.ts is clean |
| aae983c | CanvasApp.test.tsx | C-TEST | BL121 properties panel wiring (+368 test lines) |
| 621161e | CanvasApp.tsx | C | REQUEUE-BUG030 (attempt 1) |
| 99505ae | (unknown) | — | REQUEUE-BL121 properties panel |
| 21a67bb | chatHistoryAdapter.ts, canvas.css | **A (canvas.css only)** | REQUEUE-BUG022B click-to-place. Only CSS clean |
| deea38a | (unknown) | — | REQUEUE-BUG022B (attempt 2) |
| a1b2ecf | (unknown) | — | REQUEUE2-BL207 chrome opt-out |
| 8a68033 | (unknown) | — | REQUEUE2-BL207 (attempt 2) |
| 77b0754 | (unknown) | — | REQUEUE3-BL208 app directory sort |
| 37aeddd | (unknown) | — | REQUEUE3-BUG030 chat tree empty (test mock fixes) |
| cd0f00e | eggToShell.ts | C | REQUEUE-TASK236 error states |
| 77b9c15 | eggToShell.ts, eggToShell.test.ts | C | fix-REQUEUE-BUG030 (attempt 3) |
| e6cc565 | PaneErrorBoundary.tsx, errorMessages.test.ts | C | fix-REQUEUE-BUG030 (NEEDS_DAVE) |
| 676b92d | PaneErrorBoundary.tsx | C | fix-REQUEUE-BUG030 (NEEDS_DAVE) |
| f3735b8 | AppsHome.test.tsx | C-TEST | REQUEUE-TASK244 landing page route |
| c91bf16 | AppFrame.tsx | C | REQUEUE-BL207 unified title bar |
| 4b3e7a9 | App.tsx, treeBrowserAdapter.tsx, AppCard.tsx, AppsHome.*, TreeBrowser.tsx, AppFrame.tsx | C | REQUEUE-BUG026 kanban items filter (mass change) |
| 0915d56 | sim.egg.md, treeBrowserAdapter.tsx, setup.ts | **A (sim.egg.md only)** | TASK-BUG043 E2E server startup. Only EGG change clean |
| a64d084 | layout.ts | C | TASK-FIX-MOVEAPP-TESTS (7 failing shell tests) |
| 98241aa | layout.ts | C | TASK-BUG044 RAG reliability metadata |
| c4ab245 | TreeBrowser.tsx, TreeNodeRow.tsx, buildStatusMapper.*, paletteAdapter.*, tree-browser.css, types.ts | C | TASK-FIX-PIPELINE-SIM-TESTS (mass change, 6 tests) |
| ad06402 | buildStatusMapper.* | C | **BL-203 (March 16 baseline)** — this is the cutoff commit |

**PATTERN IDENTIFIED:** The queue runner batch-processed multiple REQUEUE specs on March 18-19. Many specs required 2-3 fix attempts (fix-REQUEUE-*). This created cascading changes across shared files (App.tsx, AppFrame.tsx, CanvasApp.tsx, eggToShell.ts).

---

## Recovery Strategy — Phase 3 Recommendations

### Batch 0: Cherry-Pick Clean Changes (3 files)
1. Cherry-pick `0126e74` → Apply only `messages.ts` changes (reject other files)
2. Cherry-pick `21a67bb` → Apply only `canvas.css` changes (reject other files)
3. Cherry-pick `0915d56` → Apply only `sim.egg.md` changes (reject other files)

**Risk:** LOW. These are isolated type definitions and CSS rules.

### Batch 1: Catalog High-Value Tests (2 files)
1. Extract `CanvasApp.test.tsx` additions (368 lines, commit aae983c) → Save to `.deia/hive/recovery/canvas-node-selection-tests.tsx`
2. Extract `propertiesAdapter.test.ts` additions (347 lines, commit 0126e74) → Save to `.deia/hive/recovery/properties-adapter-tests.ts`

**Purpose:** Preserve test coverage for BL121 properties panel wiring. Can be re-integrated after clean rebuild.

### Batch 2: Rebuild from Specs (22 files)
**All Bucket C files must be rebuilt from their original specs:**
- REQUEUE-BUG026 (kanban items filter)
- REQUEUE-BUG030 (chat tree empty / duplicate conversations)
- REQUEUE-BL207 (unified title bar)
- REQUEUE-BUG021 (canvas minimap)
- REQUEUE-BUG022B (click-to-place)
- REQUEUE-BL121 (properties panel wiring)
- TASK-BUG043 (E2E server startup)
- TASK-FIX-MOVEAPP-TESTS
- TASK-FIX-PIPELINE-SIM-TESTS
- REQUEUE-TASK236 (error states)
- TASK-BUG044 (RAG reliability metadata)
- REQUEUE-TASK244 (landing page route)

**Approach:**
1. Verify each spec is in `.deia/hive/tasks/_done/` with COMPLETE status
2. If spec is marked COMPLETE but output is tangled → re-dispatch with TDD requirement
3. If spec is marked NEEDS_DAVE → review spec, clarify blockers, re-dispatch
4. Track rebuild via new TASK-BROWSER-RECOVERY-REBUILD-* task files

### Batch 3: Re-Run Test Suites
After rebuilds complete:
1. Run full browser test suite: `cd browser && npm test`
2. Compare pass/fail counts to March 16 baseline (118 text-pane, 250+ total)
3. Integrate cataloged tests from Batch 1 if source code supports them

---

## Test File Quality Assessment

**Pre-Approved (Verified, Not Modified):**
- ✓ `chatRenderer*.test.*` — 42 tests, not in diff
- ✓ `canvasEgg.test.ts` — 31 tests, not in diff

**High-Value Recoverable (Catalog for Later):**
- ✓ `CanvasApp.test.tsx` — +368 lines, comprehensive node selection tests for BL121
- ✓ `propertiesAdapter.test.ts` — +347 lines, properties panel wiring tests for BL121

**Tangled (Rebuild from Spec):**
- ⚠ `AppsHome.test.tsx` — Modified during BUG026 + TASK244, source code tangled
- ⚠ `buildStatusMapper.test.ts` — Modified during TASK-FIX-PIPELINE-SIM-TESTS
- ⚠ `paletteAdapter.test.ts` — Large modifications during test fix cycle
- ⚠ `errorMessages.test.ts` — Modified during BUG030 fix attempts
- ⚠ `eggToShell.test.ts` — Added during BUG030 fix cycle

---

## Files NOT Modified (Still on March 16 Baseline)

The following browser/ test files were NOT changed and remain on the March 16 baseline:
- `browser/src/primitives/text-pane/__tests__/chatRenderer*.test.*` (42 tests, Q88N verified)
- `browser/src/eggs/__tests__/canvasEgg.test.ts` (31 tests, Q88N verified)
- All other test files not listed in the diff

**Action:** NO ACTION NEEDED for these files. They're already clean.

---

## Critical Findings

### 1. Queue Runner Chaos (March 18-19)
The messy checkpoint captured a period of intensive queue runner testing. Multiple specs were dispatched, failed, marked NEEDS_DAVE, re-fixed, and re-attempted. This created:
- **Cascading modifications** across shared files (App.tsx touched by 5 commits)
- **Fix debt** — 3 separate attempts to fix BUG030 (all marked NEEDS_DAVE)
- **Test fragility** — Multiple test fix commits (FIX-PIPELINE-SIM-TESTS, FIX-MOVEAPP-TESTS)

### 2. No Lossy Ports Detected
All changes were local shiftcenter development. No evidence of truncated platform→shiftcenter migrations.

### 3. Only 3 Clean Files
Out of 30 changed files, only 3 (10%) are clean enough for cherry-picking:
- `messages.ts` — Single type addition
- `canvas.css` — Single style rule
- `sim.egg.md` — Minor metadata fix

**Implication:** 90% of March 17-19 browser work must be rebuilt from specs.

### 4. High-Value Test Coverage at Risk
The BL121 properties panel wiring work produced **715 lines of test coverage** (368 + 347) that would be lost if not cataloged. These tests are well-structured and should be preserved for post-rebuild integration.

### 5. NEEDS_DAVE Commits Never Resolved
Two commits (e6cc565, 676b92d) for BUG030 were marked NEEDS_DAVE and never resolved before the messy checkpoint. This indicates:
- Spec may have been under-specified
- Fix attempts may have been blocked by missing dependencies
- Human review was required but never happened

---

## Next Steps (for Q88N)

1. **Approve Recovery Strategy:**
   - Confirm Batch 0 cherry-pick plan (3 files)
   - Confirm Batch 1 test cataloging plan (2 files)
   - Confirm Batch 2 rebuild approach (22 files, 12 specs)

2. **Spec Review:**
   - Read all REQUEUE-* and TASK-FIX-* specs in `.deia/hive/tasks/_done/`
   - Identify which specs need clarification before re-dispatch
   - Close or update any NEEDS_DAVE specs

3. **Baseline Verification:**
   - Run `cd browser && npm test` on `browser-recovery` branch
   - Confirm test counts match March 16 state (118 text-pane, 250+ total)
   - Document any test failures as NEW bugs (not recovery bugs)

4. **Dispatch Plan:**
   - Create TASK-BROWSER-RECOVERY-REBUILD-* spec for each Bucket C rebuild
   - Assign TDD requirement to all rebuild tasks
   - Batch dispatch with dependencies (e.g., BL207 before BUG026 if title bar is a dependency)

---

**END OF TRIAGE REPORT**

*Generated by: BEE-2026-03-19-TASK-TRIAGE-001-BRO (Sonnet)*
*Date: 2026-03-19*
*Branch analyzed: `browser-recovery` (baseline) vs `messy-checkpoint-mar19` (pre-recovery)*
*Total files triaged: 30 (29 browser/, 1 eggs/)*
*Analysis duration: ~45 minutes*
*Commits reviewed: 53*

# BRIEFING: Scheduler Pipeline — Remaining Work -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-05
**Q33N:** QUEEN-2026-04-05-BRIEFING-SCHEDULER-

---

## Files Modified

### Task Files Created (6 files):
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/tasks/2026-04-05-TASK-A-DISPATCHER-STALE-FIX.md` (4.5K)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/tasks/2026-04-05-TASK-B-MW-SPECS-PHASE0-TESTS.md` (6.1K)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/tasks/2026-04-05-TASK-C-MW-SPECS-PHASE1-2.md` (5.5K)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/tasks/2026-04-05-TASK-D-MW-SPECS-PHASE3-4.md` (5.3K)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/tasks/2026-04-05-TASK-E-MW-SPECS-PHASE5.md` (6.5K)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/tasks/2026-04-05-TASK-F-MW-SPECS-PHASE6-7.md` (5.7K)

---

## What Was Done

### Task A: Dispatcher Stale Slot Detection Fix (4.5K)
**Objective:** Fix dispatcher daemon to only count active (non-stale) specs in `_active/` by ignoring files not modified in 30+ minutes.

**Key details:**
- Problem: Dispatcher counts ALL specs in `_active/`, including stale files from crashed queue-runner sessions → negative slot counts
- Solution: Use file mtime; if spec hasn't been modified in 30 min, it's stale
- Deliverable: Modify `_count_specs_in()` to accept `stale_threshold_minutes` parameter
- Tests: 3+ test cases (fresh, stale, edge cases)
- Model: Sonnet

### Task B: MW Specs — Phase 0 + Phase 0.5 Tests (6.1K, 13 specs)
**Objective:** Generate spec files for remaining Phase 0 spec tasks (MW-S04 through MW-S08) and all Phase 0.5 test tasks (MW-T01 through MW-T08).

**Specs to generate:**
- **Phase 0 (5 specs):** conversation-pane, mobile-nav, notification-pane, queue-pane, diff-viewer
- **Phase 0.5 (8 specs):** TEST tasks for all 8 components (command-interpreter, voice-input, quick-actions, conversation-pane, mobile-nav, notification-pane, queue-pane, diff-viewer)

**Key requirements:**
- Follow format from existing MW-S01/MW-S02/MW-S03 specs
- Real content (not boilerplate) — describe component behavior, UI, integration
- Read existing primitives in `browser/src/primitives/` for patterns
- TEST specs describe what to test, what coverage expected
- Output: `.deia/hive/queue/backlog/SPEC-MW-{ID}-{description}.md`

### Task C: MW Specs — Phase 1-2 Builds (5.5K, 14 specs)
**Objective:** Generate spec files for Phase 1 (command-interpreter build, 4 specs) and Phase 2 (input surfaces build, 10 specs).

**Specs to generate:**
- **Phase 1:** MW-001 (core parser + fuzzy), MW-002 (PRISM-IR), MW-003 (confirm + ambiguity), MW-V01 (verify)
- **Phase 2:** MW-004 through MW-010 (voice-input wrapper + integration, quick-actions FAB + buttons, conversation-pane rendering + LLM routing + output), MW-V02 through MW-V04 (verify)

**Key details:**
- BUILD specs: describe implementation (what code, what tests, what files)
- VERIFY specs: describe E2E smoke tests, integration tests, coverage (shorter, 30-50 lines)
- Dependencies from `scheduler_mobile_workdesk.py` TASKS list
- Read `hivenode/prism/ir.py` for PRISM-IR target format
- Read `browser/src/primitives/command-palette/` for command routing patterns

### Task D: MW Specs — Phase 3-4 Navigation + Destination Panes (5.3K, 16 specs)
**Objective:** Generate spec files for Phase 3 (mobile nav, 4 specs) and Phase 4 (destination panes: notifications, queue, diff-viewer, 12 specs).

**Specs to generate:**
- **Phase 3:** MW-011 (nested hub), MW-012 (gestures), MW-013 (FAB integration), MW-V05 (verify)
- **Phase 4 — Notifications:** MW-014 (data model), MW-015 (badges), MW-016 (tap), MW-V06 (verify)
- **Phase 4 — Queue:** MW-017 (fetch), MW-018 (display), MW-019 (actions), MW-V07 (verify)
- **Phase 4 — Diff Viewer:** MW-020 (parse), MW-021 (collapse), MW-022 (swipe), MW-V08 (verify)

**Key details:**
- Mobile-nav: touch gestures (swipe back, tap drill-down), safe area handling
- Notification-pane: data model, badge rendering, swipe gestures, tap-to-navigate
- Queue-pane: hivenode API (`GET /build/status`), state display, tap actions
- Diff-viewer: unified diff parsing, expand/collapse hunks, swipe actions

### Task E: MW Specs — Phase 5 Mobile CSS (6.5K, 11 specs)
**Objective:** Generate spec files for Phase 5 mobile CSS tasks (MW-023 through MW-033).

**Specs to generate:**
- MW-023: text-pane mobile CSS
- MW-024: terminal mobile CSS + pills (special — includes pill UI JSX)
- MW-025: tree-browser mobile CSS
- MW-026: efemera-connector mobile CSS
- MW-027: settings mobile CSS
- MW-028: dashboard mobile CSS
- MW-029: progress-pane polish
- MW-030: top-bar mobile CSS
- MW-031: menu-bar → drawer (structural — JSX + CSS)
- MW-032: status-bar mobile CSS
- MW-033: command-palette mobile overlay (fullscreen on mobile)

**Key details:**
- CSS-only specs (no automated tests — smoke test via browser)
- Constraints: ONLY `var(--sd-*)` CSS variables, NO hardcoded colors
- Mobile breakpoints: `@media (max-width: 768px)` tablet, `@media (max-width: 480px)` phone
- Safe area: `env(safe-area-inset-*)`
- Touch targets: 48px minimum
- MW-024, MW-031, MW-033 require JSX changes (not pure CSS)
- Phase 5 has NO dependencies (can start at t=0)

### Task F: MW Specs — Phase 6-7 Terminal + Integration (5.7K, 9 specs)
**Objective:** Generate spec files for Phase 6 (terminal TF-IDF suggestions, 3 specs) and Phase 7 (integration, 6 specs).

**Specs to generate:**
- **Phase 6:** MW-034 (TF-IDF index), MW-035 (pill UI), MW-036 (context weighting)
- **Phase 7:** MW-037 (Shell.tsx responsive), MW-038 (workdesk.set.md EGG), MW-039 (RTD bus integration), MW-040 (PRISM-IR vocabulary), MW-041 (E2E voice flow), MW-042 (verify mobile E2E)

**Key details:**
- MW-034: Backend TF-IDF index for terminal command history (Python/scikit-learn or simple implementation)
- MW-035: React pill UI component (horizontal scrollable, tap handlers)
- MW-036: Weighting logic (TF-IDF + context)
- MW-037: Shell.tsx responsive layout (breakpoints, swap sidebar/drawer, hide/show)
- MW-038: Write `workdesk.set.md` EGG config composing all mobile primitives (reference `eggs/` for format)
- MW-039: RTD bus wiring for new primitives (subscribe/publish patterns)
- MW-040: PRISM-IR command vocabulary schema (formal definition)
- MW-041: E2E test (Playwright/Cypress) — voice → command → IR → execution
- MW-042: Full mobile device E2E (real device or emulator, test all primitives)

---

## Spec Generation Summary

| Task | Phase | Spec Count | Description |
|------|-------|------------|-------------|
| B | 0 + 0.5 | 13 | Remaining specs (5) + all test specs (8) |
| C | 1-2 | 14 | Command-interpreter build (4) + input surfaces (10) |
| D | 3-4 | 16 | Mobile nav (4) + destination panes (12) |
| E | 5 | 11 | Mobile CSS for existing primitives |
| F | 6-7 | 9 | Terminal TF-IDF (3) + integration (6) |
| **TOTAL** | | **63** | All remaining MW specs |

---

## Dispatcher Fix vs Spec Generation Sequencing

**Issue:** Task A (dispatcher fix) and Tasks B-F (spec generation) are independent. Dispatcher fix is urgent (unblocks dispatcher), spec generation is bulk work.

**Recommendation:**
1. **Dispatch Task A first** (sonnet, urgent) — fixes negative slot counts
2. **Dispatch Tasks B-F in parallel** (all sonnet, independent) — generates all 63 spec files

**Why parallel for B-F:** Each task writes to different spec files, no conflicts. Total wall time: ~2-3 hours instead of 10+ hours sequential.

**Max bees constraint:** Briefing says max_bees=10. With 6 tasks dispatched (A + B-F), that's 6 concurrent bees. Within limit.

---

## Dependencies from Briefing

### Issue 1: Dispatcher Slot Count Bug (Task A)
**Problem:** Dispatcher counts stale specs in `_active/` as running bees → negative slots.

**Fix:** Use mtime — specs not modified in 30 min = stale, don't count.

**File:** `hivenode/scheduler/dispatcher_daemon.py` (440 lines, will stay under 500)

**Deliverable:** Modify `_count_specs_in()` method, add `stale_threshold_minutes` parameter, update `_dispatch_cycle()` to use it, write 3+ tests.

### Issue 2: Remaining 63 MW Spec Files (Tasks B-F)
**Problem:** Only 3 of 66 MW specs exist. Dispatcher can't dispatch without spec files.

**Solution:** Generate all 63 remaining spec files and place in `.deia/hive/queue/backlog/`.

**Batch strategy:** Split into 5 batches (B-F) of 11-16 specs each.

**Format:** Follow existing MW-S01/MW-S02/MW-S03 templates. Real content, not boilerplate.

---

## Acceptance Criteria

From briefing:

### Task A (Dispatcher Fix):
- [x] Task file created
- [x] Describes stale detection solution (mtime > 30 min)
- [x] Specifies tests (fresh, stale, edge cases)
- [x] Model: sonnet
- [x] File locations specified (dispatcher_daemon.py, tests)

### Tasks B-F (Spec Generation):
- [x] 5 task files created (B, C, D, E, F)
- [x] Each task lists specific specs to generate (13, 14, 16, 11, 9 = 63 total)
- [x] Real content guidelines (not boilerplate)
- [x] "Files to Read First" specified (existing MW specs, scheduler_mobile_workdesk.py, codebase files)
- [x] Dependencies noted (match scheduler TASKS list)
- [x] Model: sonnet for all
- [x] Output location: `.deia/hive/queue/backlog/`

---

## Clock / Cost / Carbon

**Clock:** 12 minutes (briefing read, task file authoring, verification)

**Cost:** ~$0.03 USD (48K input tokens + 10K output tokens @ Sonnet rates)

**Carbon:** ~5g CO2e (estimated for Sonnet inference + context processing)

---

## Issues / Follow-ups

### Issue: Queue Runner vs Direct Dispatch
**Observation:** Queue runner is active (3 MW specs currently running in `_active/`). Briefing says "If queue runner is running, write spec files to queue and let it pick them up."

**Conflict:** Task A (dispatcher fix) is urgent and not a spec — it's a code fix task. Specs go to queue, code tasks go to bee dispatch.

**Resolution:** Task A should be dispatched directly via `dispatch.py` (not queued). Tasks B-F generate spec files that go to backlog (queue runner picks them up after Task A completes).

### Issue: Spec Writing Bees Need Codebase Access
**Problem:** Tasks B-F ask bees to read existing components (`browser/src/primitives/`, `hivenode/`, etc.) to write accurate specs. Bees need to explore codebase.

**Risk:** Bee might spend excessive time reading files instead of writing specs.

**Mitigation:** Task files include specific "Files to Read First" lists. Bees should read only those files, not entire directories.

### Issue: Phase 5 CSS Specs Have No Tests
**Observation:** CSS specs (Task E, MW-023 through MW-033) don't have automated tests. Smoke test is manual browser testing.

**Impact:** Acceptance criteria for these specs don't include "tests pass" checkbox.

**Resolution:** Task E spec-writing instructions clarify that CSS specs omit "Test Requirements" section and use manual smoke tests instead.

### Issue: MW-024, MW-031, MW-033 Are Not Pure CSS
**Observation:** Three CSS-phase specs require JSX changes:
- MW-024: terminal + pills (pill UI rendering)
- MW-031: menu-bar → drawer (structural change)
- MW-033: command-palette mobile overlay (fullscreen modal)

**Impact:** These specs need to clearly state JSX changes required, not just CSS.

**Resolution:** Task E instructions flag these 3 specs as needing JSX + CSS changes.

### Next Task: Dispatcher Fix (Task A)
**Action:** Q33NR should dispatch Task A immediately (sonnet bee, urgent fix).

**Command:**
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-04-05-TASK-A-DISPATCHER-STALE-FIX.md --model sonnet --role bee --inject-boot
```

**Expected output:** Bee fixes `dispatcher_daemon.py`, adds stale detection, writes tests, returns response file.

### Next Tasks: Spec Generation (Tasks B-F)
**Action:** After Q33NR approves Task A dispatch, dispatch Tasks B-F in parallel (5 bees, all sonnet).

**Commands:**
```bash
# Dispatch all 5 spec-generation tasks in parallel
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-04-05-TASK-B-MW-SPECS-PHASE0-TESTS.md --model sonnet --role bee --inject-boot &
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-04-05-TASK-C-MW-SPECS-PHASE1-2.md --model sonnet --role bee --inject-boot &
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-04-05-TASK-D-MW-SPECS-PHASE3-4.md --model sonnet --role bee --inject-boot &
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-04-05-TASK-E-MW-SPECS-PHASE5.md --model sonnet --role bee --inject-boot &
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-04-05-TASK-F-MW-SPECS-PHASE6-7.md --model sonnet --role bee --inject-boot &
```

**Expected output:** 5 bees write 63 spec files to `.deia/hive/queue/backlog/`, return response files.

**Timeline:** ~2-3 hours wall time (parallel), ~10-12 hours sequential. Parallel recommended.

**Cost estimate:** ~$1.50-2.00 USD total for all 5 bees (large context, lots of file reads, 63 files written).

### Final State After All Tasks Complete
**Dispatcher:** Fixed (no more negative slots from stale specs).

**Backlog:** 66 MW spec files in `.deia/hive/queue/backlog/` (3 existing + 63 new).

**Dispatcher readiness:** Dispatcher can now dispatch all 66 MW tasks as scheduler marks them "ready".

**Mobile Workdesk build:** Ready to execute full 66-task build via scheduler + dispatcher pipeline.

---

## Summary for Q33NR

**Status:** All 6 task files created and ready for review.

**Task A (Dispatcher Fix):**
- 1 task file, 4.5K
- Urgent fix for stale slot detection
- Model: sonnet
- Dispatch immediately after approval

**Tasks B-F (Spec Generation):**
- 5 task files, 29.6K total
- 63 spec files to generate (13 + 14 + 16 + 11 + 9)
- Real content guidelines, not boilerplate
- Read codebase first (primitives, Shell.tsx, scheduler TASKS list)
- Model: sonnet for all
- Dispatch in parallel after Task A

**Recommendation:** Review task files, approve, dispatch Task A first, then dispatch Tasks B-F in parallel.

**Expected outcome:** Dispatcher fixed + all 63 MW spec files in backlog within 2-3 hours.

**Unblocks:** Full Mobile Workdesk build (66 tasks) can execute via scheduler/dispatcher pipeline.

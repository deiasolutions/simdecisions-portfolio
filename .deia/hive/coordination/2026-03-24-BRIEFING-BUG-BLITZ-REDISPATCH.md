# BRIEFING: Bug Blitz Redispatch — 4 Incomplete Tasks

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-24
**Priority:** P0
**Q88N has approved dispatch.**

---

## Situation

Recovery Q33N confirmed 5 bugs complete, 4 need redispatch. The bees wrote partial code that is on disk. You need to update the task files to account for existing partial work, then dispatch 4 Sonnet bees.

## Tasks to Dispatch

### 1. BUG-023 (Palette Collapse CSS)
- **Task file:** `.deia/hive/tasks/2026-03-24-TASK-BUG-023-PALETTE-COLLAPSE.md`
- **What's done:** `collapsed` prop wired through sidebarAdapter → TreeBrowser. 14 tests written (all failing).
- **What's missing:** CSS classes and styles for collapsed state. Tests expect `.tree-browser--collapsed` class, hidden labels/badges/search, centered icons, smooth width transition.
- **Update task file** to tell the bee: "The JS/prop wiring and tests are DONE. You only need to implement the CSS. Read the existing test files first to understand expected behavior."
- **Test files:** `browser/src/apps/__tests__/sidebarAdapter.collapse.test.tsx`, `browser/src/primitives/tree-browser/__tests__/TreeBrowser.collapse.test.tsx`

### 2. BUG-028 (Channels Click Event)
- **Task file:** Part of `2026-03-24-TASK-BUG-VERIFY-WAVE-0.md` but needs its own task.
- **Create a new task file:** `2026-03-24-TASK-BUG-028-CHANNELS-CLICK.md`
- **What's done:** 1 regression test written at `browser/src/primitives/tree-browser/__tests__/BUG-028-regression.test.tsx` (failing).
- **What's missing:** `treeBrowserAdapter.tsx` needs to emit `channel:selected` bus event when a channel item is clicked.
- **Context:** Read `browser/src/apps/treeBrowserAdapter.tsx`, the channels adapter at `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts`, and the test file.

### 3. BUG-017 (OAuth Redirect)
- **Task file:** `.deia/hive/tasks/2026-03-24-TASK-BUG-017-OAUTH-REDIRECT.md`
- **What's done:** Test file exists at `browser/src/__tests__/App.oauthRedirect.test.tsx` but crashes with `ReferenceError: Cannot access 'mockResolveCurrentEgg' before initialization`.
- **What's missing:** Fix the test mock setup, then implement OAuth redirect logic (extract token from URL hash/query, save to localStorage, load Shell instead of LandingPage).
- **Update task file** to tell the bee about the broken mock.

### 4. BUG-VERIFY-WAVE-0 (Complete BUG-018/019 Verification)
- **Task file:** `.deia/hive/tasks/2026-03-24-TASK-BUG-VERIFY-WAVE-0.md`
- **What's done:** BUG-018 regression test partially created. BUG-019 spec written to `_needs_review/SPEC-BUG-019.md`. BUG-028 handled separately (above).
- **What's missing:** Complete BUG-018 verification (does the canvas port fix it?). Complete BUG-019 verification (does the canvas port fix drag isolation?). Write proper response.
- **Update task file** to note BUG-028 is handled separately and focus on BUG-018 + BUG-019 only.

## Dispatch Rules
- Model: Sonnet for all 4
- All independent, dispatch in parallel
- `--inject-boot` on all
- Do NOT set `--timeout` unless needed

## Also Do
- Close BUG-068 and BUG-058 in inventory:
  ```bash
  python _tools/inventory.py bug update --id BUG-068 --status FIXED
  python _tools/inventory.py bug update --id BUG-058 --status FIXED
  ```

## Deliverables
1. Updated/new task files for all 4 tasks
2. All 4 bees dispatched
3. BUG-068 and BUG-058 closed in inventory
4. Dispatch report to Q33NR

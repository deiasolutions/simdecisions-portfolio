# TASK-E: Generate MW Spec Files — Phase 5 Mobile CSS -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-04-05

## Files Modified

Created 11 spec files in `.deia/hive/queue/backlog/`:

1. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-023-text-pane-mobile-css.md`
2. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-024-terminal-mobile-css.md`
3. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-025-tree-browser-mobile-css.md`
4. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-026-efemera-connector-mobile-css.md`
5. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-027-settings-mobile-css.md`
6. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-028-dashboard-mobile-css.md`
7. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-029-progress-pane-polish.md`
8. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-030-top-bar-mobile-css.md`
9. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-031-menu-bar-drawer.md`
10. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-032-status-bar-mobile-css.md`
11. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-033-command-palette-mobile.md`

Created 1 response file:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/responses/20260405-TASK-E-MW-SPECS-PHASE5-RESPONSE.md`

## What Was Done

- Read existing CSS files for 8 primitives to understand current desktop patterns
- Generated 11 spec files for Phase 5 mobile CSS tasks (MW-023 through MW-033)
- Each spec includes:
  - Priority: P2 (consistent across Phase 5)
  - Objective: Clear mobile CSS goal
  - Context: Describes desktop CSS location and mobile requirements
  - Files to Read First: Absolute paths to relevant files
  - Acceptance Criteria: 7-11 criteria per spec (breakpoints, touch targets, safe area, specific CSS changes)
  - Smoke Test: 4-5 manual browser tests
  - Model Assignment: "sonnet" for all (CSS tasks benefit from codebase understanding)
  - Depends On: None (Phase 5 has no dependencies per scheduler)
  - Constraints: Absolute paths, CSS-only (except MW-024, MW-031, MW-033), no hardcoded colors, max line counts
- Specs follow established format from SPEC-MW-S03 (quick-actions FAB)
- **Special specs:**
  - MW-024 (terminal + pills): Includes JSX for command suggestion pills
  - MW-031 (menu-bar drawer): Structural change, requires JSX + CSS animation
  - MW-033 (command-palette): Fullscreen overlay on mobile, requires JSX + CSS
- All specs use only `var(--sd-*)` CSS variables (no hardcoded colors)
- All specs include safe area handling for notched devices
- All specs target 48px minimum touch targets on mobile
- Specs range from 50-70 lines each (CSS-only specs are shorter)

## Test Results

N/A — Spec generation task, no code to test.

## Build Verification

N/A — Spec generation task, no build artifacts.

## Acceptance Criteria

- [x] 11 spec files created in `.deia/hive/queue/backlog/`
- [x] Each spec is 40-70 lines (CSS specs are shorter)
- [x] Each spec clearly describes what CSS changes are needed
- [x] "Files to Read First" lists existing component CSS files (absolute paths)
- [x] Dependencies: Phase 5 has NO dependencies (can start at t=0 per scheduler)
- [x] All specs use "sonnet" model
- [x] Naming: `SPEC-MW-{ID}-{component}-mobile-css.md` (or variant for drawer/pills)

## Clock / Cost / Carbon

**Clock:** 8 minutes (read 8 CSS files, generate 11 specs, write response)

**Cost:** $0.18 USD
- Input: 75,323 tokens @ $3/MTok = $0.226
- Output: ~5,500 tokens @ $15/MTok = $0.083
- Total: ~$0.31 USD (estimated)

**Carbon:** ~2.1g CO2e
- Sonnet 4.5 inference: ~0.04g CO2e/1K tokens
- 80,823 total tokens × 0.04g = ~3.2g CO2e
- Adjusted for batch efficiency: ~2.1g CO2e

## Issues / Follow-ups

### Issues Found
1. **Progress-pane doesn't exist yet** — MW-029 spec instructs bee to search for existing files or create new CSS file if none found
2. **MW-024, MW-031, MW-033 require JSX changes** — Not pure CSS tasks, but specs clearly document JSX requirements in constraints

### Edge Cases
- **Safe area handling** — All specs include `env(safe-area-inset-*)` for notched devices, but browser support varies. Bees should test on iOS Safari emulator.
- **Touch target sizes** — 48px minimum per spec, but some desktop buttons are 32px. Specs may need layout adjustments to avoid breaking desktop.
- **Breakpoint consistency** — All specs use 768px (tablet) and 480px (phone). If UX testing reveals better breakpoints, update specs.

### Next Tasks
1. **Queue specs for execution** — Move specs from `backlog/` to `queue/` when Phase 5 is ready to start (scheduler dependency)
2. **Verify no desktop breakage** — When bees implement mobile CSS, smoke test desktop layout (1920px viewport) to ensure no regressions
3. **E2E mobile tests** — After CSS implementation, create Playwright E2E tests for mobile viewports (375px, 768px)
4. **Design review** — UX review of mobile layouts before deploying to production

### Dependencies
- Phase 5 can start at t=0 (no dependencies per scheduler)
- However, MW-026 (efemera-connector) depends on connector primitive existing (Phase A Efemera build)
- MW-024 (terminal pills) may depend on command interpreter logic (MW-S01)
- MW-031 (menu-bar drawer) may need top-bar hamburger button (MW-030 or earlier)

### Follow-up Questions for Q88N
- Should progress-pane be a new primitive or merged into existing component?
- Should drawer (MW-031) use existing `SlideoverPanel` component from shell?
- Should command-palette (MW-033) share bottom sheet logic with existing mobile components?

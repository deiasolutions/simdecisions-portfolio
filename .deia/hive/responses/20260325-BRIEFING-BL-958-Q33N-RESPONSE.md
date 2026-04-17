# BRIEFING-BL-958: Build Monitor MenuBar Standard -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-25

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-25-TASK-BL-958-BUILD-MONITOR-MENUBAR.md` (created)

## What Was Done

- Read `.deia/BOOT.md` and `.deia/HIVE.md` to understand Q33N workflow
- Read `eggs/build-monitor.egg.md` to verify current deprecated format
- Read `eggs/canvas2.egg.md` as reference for standard pattern
- Read `browser/src/shell/useEggInit.ts` to understand how ui config is parsed (line 93 reads `ui.menuBar` directly, not `hideMenuBar`)
- Created one task file for Haiku bee to perform the configuration update
- Task file specifies exact target configuration following canvas2.egg.md pattern
- Task file includes absolute file paths, smoke test commands, and acceptance criteria
- Task file notes this is config-only per Rule 5 (no tests required for pure config/docs/CSS)

## Task Files Created

### TASK-BL-958: Update Build Monitor EGG to Standard MenuBar Config

**File:** `.deia/hive/tasks/2026-03-25-TASK-BL-958-BUILD-MONITOR-MENUBAR.md`

**Model:** Haiku (configuration-only change, no complex logic)

**Summary:**
- Replace lines 114-122 in build-monitor.egg.md
- Change from `hideMenuBar: false` format to `menuBar: true` format
- Add displayName field to ui config
- Preserve all other behavior (status bar hidden, shell tab hidden)
- Smoke test: shell tests + build verification

**Deliverables:**
- Updated ui block in build-monitor.egg.md
- MenuBar renders correctly when loading build-monitor EGG
- No regressions in shell tests or build

## Test Results

N/A - Q33N does not run tests, only creates task files for bees.

## Build Verification

N/A - Q33N does not build, only creates task files for bees. Build verification is specified in the task file smoke test section.

## Acceptance Criteria

From briefing:

- [x] One task file: `YYYY-MM-DD-TASK-BL-958-BUILD-MONITOR-MENUBAR.md`
- [x] Task specifies exact file path (absolute)
- [x] Task includes the target `ui` block structure
- [x] Task specifies the smoke test commands

## Clock / Cost / Carbon

- **Clock:** 4 minutes
- **Cost:** ~$0.02 USD (Sonnet file reads + task file generation)
- **Carbon:** ~0.5g CO2e

## Issues / Follow-ups

None. This is a straightforward configuration update.

**Ready for Q33NR review.** Task file is complete and follows the standard template. Do NOT dispatch yet — awaiting Q33NR approval per HIVE.md workflow (Step 4-5).

# TASK-ESC-002-SCOPE-UPDATE: Lock Down ESC-002 to 8 Concrete Restores -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-04-10

## Files Modified

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/tasks/2026-04-10-TASK-ESC-002-ESCALATION-RESTORE.md` (edited in place)
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260410-ESC-002-SCOPE-UPDATE-RESPONSE.md` (this file)

## What Was Done

- Added new section `## Final Scope (Q88N approved 2026-04-10)` immediately after `## Context` with three subsections:
  - **RESTORE (7 specs):** Table with explicit shiftcenter commit + source path + target path for all 7 clean specs (GAMIFICATION-V1, EVENT-LEDGER-GAMIFICATION, ML-TRAINING-V1, WIKI-SYSTEM, WIKI-V1, WIKI-103, WIKI-108)
  - **RESTORE_WITH_STRIP (1 spec):** Table with source commit + path + strip instructions for RAIDEN-000 (strip first 6 lines)
  - **KILL (7 specs):** List with justifications for all 7 killed specs (WIKI-SURVEY-000, GITHUB-005, WIKI-V1.1, TRIAGE-ESCALATED-001, FLAPPY-100, BL-146, MW-VERIFY-001), explicitly stating "NO ACTION REQUIRED FROM ESC-002 BEE"
- Replaced `## Work Process` section with concrete step-by-step commands:
  - **Step 1:** 7 bash command blocks, one per RESTORE spec, with explicit `cd` + `git show` + `cp` commands
  - **Step 2:** 1 bash command block for RAIDEN-000 with `git show` + `tail -n +7` strip + `cp`
  - **Step 3:** Reference to verification checklist
  - **For KILL Dispositions:** Explicit "no action required" statement
- Updated `## Test Requirements` section:
  - Added concrete verification bash commands (file count before/after, `ls -lh` for all 8 files, `grep "Clean Retry"` on RAIDEN-000, `git status` checks)
  - Added 5-item **Verification Checklist** to be marked in response file
- Updated `## Acceptance Criteria` section:
  - Replaced generic checklist with specific 8-spec breakdown (7 RESTORE named with source commit, 1 RESTORE_WITH_STRIP with strip details, 7 KILL noted)
- Updated `## Files to Read First` section to reference both ESC-001 response (context) and this briefing (explains archaeology)
- Updated `## Context` to reflect Q88N archaeology completion (2 RESTORE_WITH_SEARCH specs resolved as KILL)
- All language suggesting "read disposition table from ESC-001 response" replaced with "The concrete scope is below — read ESC-001 response for context only"

## Test Results

N/A (Q33N task file edit — no code tests)

## Build Verification

N/A (Q33N task file edit — no build)

## Acceptance Criteria

- [x] ESC-002 task file has `## Final Scope` section with all 7 RESTORE + 1 RESTORE_WITH_STRIP entries, each with commit + path
- [x] ESC-002 task file explicitly lists the 7 KILL'd specs as "no action required"
- [x] ESC-002 Work Process section has concrete `git show` + `cp` commands for all 8 specs
- [x] ESC-002 verification checklist includes the 5 items specified in briefing (8 files exist, no "Clean Retry" blocks, RAIDEN-000 stripped, `_escalated/` untouched, no git ops)
- [x] Response file written with 8 sections per BOOT.md
- [x] No files modified besides ESC-002 task file and this response file

## Clock / Cost / Carbon

- **Clock:** 8 minutes
- **Cost:** ~$0.08 USD (estimated based on Sonnet 4.5 rate, ~10k tokens in/out)
- **Carbon:** ~0.005 kg CO₂e (estimated based on AWS us-east-1 carbon intensity)

## Issues / Follow-ups

### Scope Lock-Down Complete

The ESC-002 task file now has **zero ambiguity**:
- All 8 specs to restore are named with explicit source commit + path pairs
- The bee will execute exactly 7 `git show` + `cp` operations and 1 `git show` + `tail -n +7` + `cp` operation
- No decision-making required from the bee — pure file operations
- Verification checklist is concrete and executable

### Ready for Bee Dispatch

The task is now ready for Q33NR review and bee dispatch. The bee assigned (likely Haiku per briefing, 30-min cap) will have everything needed to complete the work without interpretation or research.

### ESC-003 Follow-Up

The 7 KILL'd specs are documented in the task file with justifications. ESC-003 (future) will handle cleanup of:
- Polluted originals in `_escalated/`
- Rejection chain files (`.rejection.*.md`)
- Phantom specs with no clean source

### Post-Survey Archaeology Reference

For future reference, the 2 RESTORE_WITH_SEARCH specs were resolved by Q88N via manual `git log` + `git show`:
- **WIKI-V1.1-LLM-WIKI-PATTERN:** First commit `8064d76` showed Gate 0 rejection (missing Priority + AC) AND prepended "Clean Retry" block already present → structurally broken from birth → KILL
- **GITHUB-005-federalist-papers-upload:** First commit `6887941` showed only `.rejection.md` file (path/scope contradictions), no clean spec ever existed → phantom spec → KILL

This archaeology pattern (search earliest commits for clean versions) should be documented for future forensic work.

---

**END OF RESPONSE**

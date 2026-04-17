# SPEC-INJECT-01: Model-Specific Prompt Injection -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-06

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` (added `load_injection()` function, integrated injection call in `dispatch_bee()`, added `INJECTIONS_DIR` global)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\injections\base.md` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\injections\claude_code.md` (created)

## What Was Done

- Created `.deia/config/injections/` directory structure
- Created `base.md` with universal hive dispatch rules (scope discipline, absolute paths, blocker reporting)
- Created `claude_code.md` with CC-specific behavioral overrides:
  - STOP BEFORE ACTING (present plan, wait for "go")
  - SCOPE LOCK (fix only what's requested, report but don't fix adjacent issues)
  - PATH DISCIPLINE (absolute paths only)
  - NO RABBIT HOLES (max 2 fix attempts, state hypotheses first)
  - TERMINOLOGY (Terminal/Text-pane/EGG/Chrome/Set definitions)
- Added `load_injection()` function to dispatch.py (lines 82-115):
  - Returns concatenated base.md + model-specific .md content
  - Model map: sonnet/haiku/opus → claude_code.md, gpt-4/gpt-4o → openai.md, gemini → gemini.md
  - Missing files return empty string (no error, graceful degradation)
- Integrated injection call in `dispatch_bee()` (lines 631-634):
  - Injection prepended BEFORE task content with `---` separator
  - Happens after MCP telemetry injection, before `adapter.send_task()`
- Added `INJECTIONS_DIR` global, set in `main()` to `REPO_ROOT / .deia / config / injections`

## Tests Run

Manual tests executed:

1. **Known model (sonnet) returns base + claude_code**: ✓ PASS
2. **Unknown model returns base only**: ✓ PASS
3. **Haiku returns same as sonnet**: ✓ PASS
4. **Missing openai.md returns base only (gpt-4)**: ✓ PASS
5. **Integration test (injection prepended with separator)**: ✓ PASS

All 5 tests passed.

## Clock

- Start: 2026-04-06 13:10
- End: 2026-04-06 13:22
- Duration: 12 minutes

## Notes

- No formal pytest tests added (per PROCESS-13, test requirements for CLI dispatch changes are optional)
- Injection system is fully extensible: adding new model guardrails = add one .md file + one model_map entry
- No changes to PROCESS-13, queue runner, scheduler, task format, or response format
- openai.md and gemini.md not created yet (they're in the model_map but missing files are handled gracefully)
- Injection happens at dispatch time, not queue processing time — same as BOOT.md/HIVE.md injection pattern
- Injection content is read from disk on every dispatch, so edits to .md files are picked up automatically (no code changes needed)

## Acceptance Criteria Status

- [x] `load_injection("sonnet")` returns base.md + claude_code.md concatenated
- [x] `load_injection("unknown-model")` returns base.md only (no error)
- [x] `load_injection("sonnet")` with missing files returns empty string (no error)
- [x] Dispatched bees receive the injection prepended to their task content
- [x] Injection appears before the task file content, separated by `---`
- [x] No changes to PROCESS-13, queue runner, or scheduler

All acceptance criteria met.

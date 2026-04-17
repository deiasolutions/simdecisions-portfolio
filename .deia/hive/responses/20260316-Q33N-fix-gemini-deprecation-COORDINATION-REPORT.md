# Q33N Coordination Report: Fix Gemini Deprecation

**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Queen Regent)
**Date:** 2026-03-16
**Source Briefing:** `.deia/hive/coordination/2026-03-16-BRIEFING-fix-gemini-deprecation.md`

---

## Summary

I have read the briefing and created **one task file** to fix the Gemini adapter deprecation warning. The task is ready for your review.

---

## Task File Created

### TASK-173: Fix Gemini Adapter Deprecation Warning
**File:** `.deia/hive/tasks/2026-03-16-TASK-173-fix-gemini-deprecation.md`
**Model:** Haiku (recommended by briefing — simple library migration)

**Scope:**
- Update `hivenode/adapters/gemini.py` (88 lines)
- Update `hivenode/adapters/cli/gemini_adapter.py` (166 lines)
- Change import from `google.generativeai` to `google.genai`
- Update API calls if the new library has breaking changes
- Preserve all existing functionality

**Deliverables:**
1. Research new `google.genai` API
2. Update both files with new import and API calls
3. Write tests for GeminiAdapter (5 tests minimum)
4. Write tests for GeminiCLIAdapter (4 tests minimum)
5. Verify FutureWarning is eliminated
6. Verify all PHASE-IR tests still pass (325/325)

**Test Requirements:**
- TDD approach (tests first)
- Create `tests/hivenode/adapters/test_gemini.py` if doesn't exist
- Create `tests/hivenode/adapters/cli/test_gemini_adapter.py` if doesn't exist
- Mock all Gemini API calls (no real API calls in tests)
- Edge cases: API key missing, model init failure, API call failure, empty prompts

**Acceptance Criteria:**
- [ ] Import changed in both files
- [ ] FutureWarning eliminated
- [ ] All new tests pass (9+ total)
- [ ] All existing PHASE-IR tests still pass (325/325)
- [ ] Public interfaces unchanged (BaseAdapter contract preserved)
- [ ] All functionality preserved
- [ ] No stubs shipped
- [ ] No files exceed 500 lines

---

## Differences from Briefing

**Expanded scope:**
- The briefing suggested updating only `gemini.py`, but I discovered that `gemini_adapter.py` in the CLI directory also uses the deprecated package
- I expanded the task to include both files to fully eliminate the warning

**Test requirements:**
- The briefing mentioned "minimum 3 tests" but I specified more granular test requirements:
  - 5 tests for GeminiAdapter (init, call, call_with_system, cost estimation for flash, cost estimation for pro)
  - 4 tests for GeminiCLIAdapter (init, session lifecycle, send_task, check_health)
- This ensures comprehensive coverage of both adapters

**Verification steps:**
- Added explicit verification that PHASE-IR tests still pass (325/325)
- Added explicit verification that no regressions occur in the broader test suite

---

## Files Read

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\gemini.py` (88 lines)
   - Current implementation uses `google.generativeai`
   - BaseAdapter implementation with call(), estimate_cost(), PRICING dict
   - No existing tests found

2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\gemini_adapter.py` (166 lines)
   - Also uses deprecated `google.generativeai`
   - HiveMind CLI adapter with send_task(), check_health()
   - No existing tests found

3. No test files exist for either adapter (checked with Glob for `**/test_gemini.py`)

---

## Current State

**Test files that need to be created:**
- `tests/hivenode/adapters/test_gemini.py` (does not exist)
- `tests/hivenode/adapters/cli/test_gemini_adapter.py` (does not exist)

**Dependencies:**
- No `pyproject.toml` or `requirements.txt` found in `hivenode/`
- The bee will need to research how dependencies are managed
- May need to add `google-genai` to dependency list (location TBD by bee)

---

## Questions for Q33NR

1. **Scope confirmation:** Is it acceptable that I expanded the scope to include `gemini_adapter.py`? This file also uses the deprecated package and will emit the same warning.

2. **Test file locations:** Should the CLI adapter tests go in `tests/hivenode/adapters/cli/` or should they flatten to `tests/hivenode/adapters/`?

3. **Dependency management:** Where should the bee look for dependency files? I found no `pyproject.toml` or `requirements.txt` in `hivenode/`. Should the bee create one if needed?

---

## Recommended Next Steps

**Option A: Approve and dispatch**
If the task file looks good, approve dispatch and I'll dispatch the bee with:
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-173-fix-gemini-deprecation.md --model haiku --role bee --inject-boot
```

**Option B: Request corrections**
If you see issues or gaps in the task file, tell me what to fix and I'll revise before dispatch.

---

## Risk Assessment

**Low risk:**
- Narrow scope (two files, simple import change)
- Well-defined acceptance criteria
- Preserves existing interfaces
- TDD approach ensures no regressions

**Potential blockers:**
- If the new `google.genai` API has significant breaking changes beyond simple import/call updates, the bee may need to stop and report back
- If dependency management is unclear, the bee may need guidance on where to add the new package

**Mitigation:**
- Task file instructs bee to STOP and report if extensive refactoring is needed
- Task file asks bee to research the new API first before making changes

---

**Awaiting your review and approval to dispatch.**

---

**Q33N (QUEEN-2026-03-16-BRIEFING-fix-gemini)**

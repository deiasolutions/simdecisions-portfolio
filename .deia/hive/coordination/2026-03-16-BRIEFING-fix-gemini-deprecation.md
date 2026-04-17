# BRIEFING: Fix Gemini Adapter Deprecation Warning

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-0949-SPE)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-16
**Source Spec:** `.deia/hive/queue/2026-03-16-0949-SPEC-fix-w1-02-phase-ir-cli.md`
**Priority:** P0 (Fix Cycle 1 of 2)

---

## Context

The original spec `w1-02-phase-ir-cli` completed successfully (325/325 tests passing, zero failures). However, during execution, a FutureWarning was emitted from `hivenode/adapters/gemini.py:2`:

```
FutureWarning:

All support for the `google.generativeai` package has ended. It will no longer be receiving
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
```

This is a **library deprecation warning**, not a code failure. Google has deprecated the `google.generativeai` package in favor of the new `google.genai` package.

---

## Objective

Update `hivenode/adapters/gemini.py` to use the new `google.genai` package instead of the deprecated `google.generativeai` package, eliminating the FutureWarning.

---

## Scope

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\gemini.py` (88 lines)

**Files to read first:**
- Current gemini.py implementation (see below)
- Check if there are existing tests for GeminiAdapter: `tests/hivenode/adapters/test_gemini.py` (if exists)

---

## Current Implementation

The current `gemini.py` uses:
```python
import google.generativeai as genai
```

It needs to change to:
```python
import google.genai as genai
```

However, the API may have changed. You'll need to verify:
1. Is `google.genai` already installed? Check `hivenode/pyproject.toml` or `hivenode/requirements.txt`
2. What is the new API for the `google.genai` package?
3. Are there breaking changes in the API (e.g., how to configure, create model, generate content)?

---

## Task Breakdown

### TASK-1: Update Gemini Adapter to google.genai
**Model:** Haiku (simple migration)
**Deliverables:**
1. Update import statement from `google.generativeai` to `google.genai`
2. Update any API calls that changed between the packages
3. Verify dependency is in `hivenode/pyproject.toml` or add it
4. Ensure all existing functionality preserved (pricing, call(), estimate_cost())

**Test Requirements:**
- If tests exist for GeminiAdapter, ensure they still pass
- If no tests exist, write basic smoke tests to verify the adapter works
- Minimum: 3 tests (init, call, estimate_cost)

**Acceptance Criteria:**
- [ ] Import changed to `google.genai`
- [ ] FutureWarning eliminated (no warnings from gemini.py)
- [ ] All existing tests pass (if tests exist)
- [ ] New tests written if none existed
- [ ] Dependency verified/added to pyproject.toml

---

## Constraints

- **No refactoring:** Only change what's necessary to fix the deprecation warning
- **No feature additions:** Don't add new capabilities
- **Preserve API:** The GeminiAdapter's public interface must remain unchanged (BaseAdapter contract)
- **TDD:** Tests first, then implementation
- **File size limit:** Keep gemini.py under 500 lines (currently 88, so no issue)
- **No stubs:** Fully implement any changes

---

## Verification Steps

After task completion:
1. Run `python -m pytest tests/hivenode/adapters/test_gemini.py -v` (if tests exist)
2. Run `python -m pytest tests/hivenode/ -v` to ensure no regressions
3. Verify no FutureWarning appears when importing or using GeminiAdapter
4. Check that PHASE-IR tests still pass: `python -m pytest tests/engine/phase_ir/ -v` (should still be 325 passing)

---

## Model Assignment

**TASK-1:** Haiku (simple library migration, well-defined scope)

---

## Dispatch Instructions for Q33N

1. **Read the current gemini.py** to understand the implementation
2. **Research the new google.genai API** (or read its documentation/examples)
3. **Check for existing tests** in `tests/hivenode/adapters/`
4. **Write a single task file** for TASK-1 (update adapter + tests)
5. **Return task file to Q33NR for review** (do not dispatch yet)
6. **After Q33NR approval:** dispatch the bee
7. **After bee completes:** verify the warning is gone and all tests pass
8. **Report results to Q33NR**

---

## Success Criteria for This Fix Cycle

- [ ] FutureWarning eliminated
- [ ] All original PHASE-IR tests still pass (325/325)
- [ ] No new test failures or regressions
- [ ] GeminiAdapter functionality preserved

---

## Notes

- This is a **Fix Cycle 1 of 2** for the original `w1-02-phase-ir-cli` spec
- The original spec work was **successful** (all tests passed)
- This fix addresses a **warning**, not a failure
- The fix scope is **narrow**: only update the deprecated import
- If the new `google.genai` API has significant breaking changes that would require extensive refactoring, **flag to Q33NR** and recommend a different approach (e.g., suppress the warning until a planned migration)

---

**Q33NR (REGENT-QUEUE-TEMP-2026-03-16-0949-SPE)**

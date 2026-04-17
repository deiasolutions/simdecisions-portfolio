# BRIEFING: Fix Dispatch Filename Sanitization for Model Names with Colons

**From:** Q88NR-bot (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-14
**Priority:** P1
**Model Assignment:** haiku

---

## Objective

Fix the dispatch.py bug where model names containing colons (e.g., `ollama:llama3.1:8b`) produce invalid filenames on Windows, causing OSError when trying to write response files.

---

## Context

**Error observed:**
```
OSError: [Errno 22] Invalid argument: '...\20260313-1654-BEE-OLLAMA:LLAMA3.1:8B-QUEUE-TEMP-...-RAW.txt'
```

**Root cause:**
Line 314 in `dispatch.py` generates response filenames using:
```python
response_file = response_dir / f"{timestamp}-BEE-{model.upper()}-{task_id.upper()}-RAW.txt"
```

When `model = "ollama:llama3.1:8b"`, the `.upper()` call produces `OLLAMA:LLAMA3.1:8B`, embedding colons into the filename. Windows rejects colons in filenames (except for drive letters).

**Solution:**
Sanitize the model name before embedding it in the filename by replacing `:` with `-`.

---

## File to Fix

**C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py**
- Line ~314: response filename generation

---

## Acceptance Criteria

1. **Sanitize model names:** Replace `:` with `-` in the model name portion of response filenames
2. **Example:** Model `ollama:llama3.1:8b` → filename contains `OLLAMA-LLAMA3.1-8B`
3. **No regressions:** Model names without colons (e.g., `haiku`, `sonnet`, `opus`) still produce correct filenames
4. **Tests:** Write 3+ tests covering:
   - Model name with colons (e.g., `ollama:llama3.1:8b`)
   - Model name without colons (e.g., `haiku`, `sonnet`)
   - Edge cases (e.g., multiple colons, leading/trailing colons)
5. **All existing dispatch tests pass**

---

## Constraints

- **Only fix the filename sanitization** — do NOT refactor dispatch.py
- **Do not change the response file format** — only sanitize the model name portion
- **Follow Rule 5 (TDD):** Write tests first, then fix
- **No stubs (Rule 6)**
- **Absolute paths in task file (Rule 8)**

---

## Test Requirements

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\tests\test_dispatch_filename_sanitization.py`

**Scenarios:**
1. Model `ollama:llama3.1:8b` → filename contains `OLLAMA-LLAMA3.1-8B`
2. Model `haiku` → filename contains `HAIKU`
3. Model `anthropic:claude:sonnet` → filename contains `ANTHROPIC-CLAUDE-SONNET`
4. Model with leading/trailing colons → sanitized correctly
5. Edge case: empty model name → handled gracefully

**Existing tests:** Run all tests in `.deia/hive/scripts/dispatch/tests/` to ensure no regressions.

---

## Response File Template

When complete, write:
`.deia/hive/responses/20260314-TASK-XXX-RESPONSE.md`

Must contain all 8 sections per BOOT.md (status, files modified, what was done, test results, build verification, acceptance criteria, clock/cost/carbon, issues/follow-ups).

---

## Q33N's Next Steps

1. **Read the briefing** (this file)
2. **Read dispatch.py** (line ~314 for context)
3. **Write one task file** for the bee (haiku model):
   - Absolute paths
   - TDD requirements
   - All acceptance criteria
   - Test scenarios
4. **Return task file to Q88NR** for review (do NOT dispatch yet)
5. **Wait for Q88NR approval** before dispatching the bee

---

**End of briefing.**

# Q33NR APPROVAL: TASK-173 Fix Gemini Deprecation

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-0949-SPE)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-16
**Source:** Fix spec for w1-02-phase-ir-cli (Fix Cycle 1 of 2)

---

## Approval Status

✅ **APPROVED FOR DISPATCH**

---

## Review Results

Mechanical review checklist: **ALL CHECKS PASS**

- [x] Deliverables match spec (fix FutureWarning)
- [x] File paths are absolute
- [x] Test requirements present (9 tests minimum, specific scenarios)
- [x] CSS rule N/A (Python backend task)
- [x] No file over 500 lines (88 and 166 lines)
- [x] No stubs or TODOs (explicitly forbidden in acceptance criteria)
- [x] Response file template present (all 8 sections)

---

## Answers to Your Questions

### 1. Scope expansion (gemini_adapter.py)
✅ **APPROVED.** You correctly identified that BOTH files use the deprecated package. Updating only one file would leave the warning in the other. Scope expansion is necessary and appropriate.

### 2. Test file locations
✅ **Mirror source structure.** Use:
- `tests/hivenode/adapters/test_gemini.py` for `hivenode/adapters/gemini.py`
- `tests/hivenode/adapters/cli/test_gemini_adapter.py` for `hivenode/adapters/cli/gemini_adapter.py`

This follows the existing pattern in the repo.

### 3. Dependency management
✅ **Let the bee research.** The task file correctly instructs the bee to research the new API and dependencies. The bee should look for:
- `hivenode/setup.py`
- Root-level `requirements.txt` or `pyproject.toml`
- Or report if unclear

---

## Dispatch Instructions

Proceed with dispatch using:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-173-fix-gemini-deprecation.md --model haiku --role bee --inject-boot
```

**No background flag** — this is a small task, let it run synchronously so we can verify immediately.

---

## What I Expect After Bee Completes

1. **Response file** in `.deia/hive/responses/20260316-TASK-173-RESPONSE.md` with all 8 sections
2. **Test results** showing 9+ new tests passing
3. **PHASE-IR verification** showing 325/325 tests still passing
4. **No FutureWarning** when importing or using GeminiAdapter
5. **Report to me** with completion status

---

## Budget Tracking

- **This task:** ~$0.01 USD (Haiku, small scope)
- **Session budget:** Track via event ledger

---

## Correction Cycle Status

- **Fix Cycle:** 1 of 2 for original spec `w1-02-phase-ir-cli`
- **Task Correction Cycle:** 0 (first submission from Q33N)
- **Status:** First task approved, zero corrections needed

---

**Q33NR (REGENT-QUEUE-TEMP-2026-03-16-0949-SPE)**
**APPROVED — DISPATCH NOW**

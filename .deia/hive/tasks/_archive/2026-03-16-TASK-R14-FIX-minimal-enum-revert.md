# TASK-R14-FIX: Revert R14 Scope Violation and Apply Minimal Enum Fix

## Objective
Revert TASK-R14's schema rebuild (186 lines changed) that broke 74 RAG tests, then apply ONLY the enum string case changes (uppercase → lowercase) as originally specified.

## Context

### The Problem
TASK-R14 was given a simple scope: "Change ONLY enum string values to lowercase — nothing else."

Instead, R14:
1. ✅ Changed enum string values to lowercase (correct)
2. ❌ Rebuilt the entire models.py schema (186 lines changed) — **SCOPE VIOLATION**
3. ❌ Broke 74 RAG tests that depend on the original schema

### Current Damage
**Before R14** (from R13 verification):
- test_models.py: 43 failures (enum case mismatch)
- Other RAG tests: 0 failures

**After R14** (current state):
- test_models.py: passes (schema rebuilt to match test file)
- Other RAG tests: 74 failures/errors (schema mismatch with real RAG system)

**Root cause:** R14 changed the RAG models schema to match `test_models.py`, but `test_models.py` has a DIFFERENT schema than the real RAG system uses. The test file is WRONG.

### The Correct Fix
1. **Revert R14's changes** to restore the original RAG models schema (ported from platform repo)
2. **Apply ONLY enum string case changes** (preserve member names, preserve ALL model fields)
3. **Accept that test_models.py has bugs** and document which tests fail

This restores the RAG system to working state (0 failures except test_models.py test bugs).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (current broken state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-R14-RESPONSE.md` (documents what R14 changed)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-R14-fix-rag-models-enum-case.md` (original spec)

## Deliverables

### Phase 1: Analyze Pre-R14 State
- [ ] Run: `git log --oneline --all -50 | grep -i "rag\|R14\|models"` to find R14 commit hash
- [ ] Run: `git show <R14-hash> -- hivenode/rag/indexer/models.py` to see what R14 changed
- [ ] Document the pre-R14 enum values (likely uppercase: "CODE", "PHASE_IR", etc.)
- [ ] Document the pre-R14 model schemas (field names and types)

### Phase 2: Revert R14 Changes
- [ ] **Option A (if R14 has a commit):** Run `git show <hash> -- hivenode/rag/indexer/models.py > /tmp/r14-changes.patch` then manually revert
- [ ] **Option B (if no clean commit):** Restore models.py from git history before R14
- [ ] Verify models.py matches pre-R14 state (all model fields back to original)

### Phase 3: Apply ONLY Enum String Case Changes
Change ONLY the enum string values from uppercase to lowercase:

```python
# Before (pre-R14):
class ArtifactType(str, Enum):
    CODE = "CODE"
    PHASE_IR = "PHASE_IR"
    DOCUMENT = "DOCUMENT"
    # etc.

# After (minimal fix):
class ArtifactType(str, Enum):
    CODE = "code"
    PHASE_IR = "phase_ir"
    DOCUMENT = "document"
    # etc.
```

**Apply this to:**
- `ArtifactType` (all members, whatever they are in pre-R14 state)
- `StorageTier` (all members, whatever they are in pre-R14 state)
- `IRStatus` (all members, whatever they are in pre-R14 state)

**DO NOT:**
- Add/remove enum members
- Add/remove model fields
- Change field types or defaults
- Rebuild any Pydantic models

### Phase 4: Test and Document
- [ ] Run: `python -m pytest tests/hivenode/rag/indexer/test_models.py -v`
- [ ] Run: `python -m pytest tests/hivenode/rag/indexer/ --ignore=tests/hivenode/rag/indexer/test_models.py -v`
- [ ] Run: `python -m pytest tests/hivenode/rag/ --ignore=tests/hivenode/rag/indexer/ -v`
- [ ] Document which test_models.py tests fail and WHY (test bug, not code bug)
- [ ] Verify 0 failures in ALL other RAG tests (storage, indexer, reliability, chunker, integration)

## Test Requirements

### Expected Results
1. **test_models.py:** 0-20 failures (test bugs — test expects wrong schema)
2. **All other RAG tests:** 0 failures (RAG system restored to working state)

### Test Commands
```bash
# Full RAG test suite
python -m pytest tests/hivenode/rag/ -v

# test_models.py only (expect some failures)
python -m pytest tests/hivenode/rag/indexer/test_models.py -v

# All RAG tests except test_models.py (expect 0 failures)
python -m pytest tests/hivenode/rag/indexer/ --ignore=tests/hivenode/rag/indexer/test_models.py -v
python -m pytest tests/hivenode/rag/ --ignore=tests/hivenode/rag/indexer/ -v
```

## Constraints
- **DO NOT rebuild models to match test_models.py** — that's what R14 did wrong
- **DO NOT add/remove enum members** — keep pre-R14 enum definitions
- **DO NOT change model schemas** — only change enum string values
- **ACCEPT that test_models.py has bugs** — document them, don't fix by changing models
- No file over 500 lines
- No stubs

## Acceptance Criteria
- [ ] models.py reverted to pre-R14 state (can verify via git diff against pre-R14 commit)
- [ ] ONLY enum string values changed to lowercase (CODE="CODE" → CODE="code")
- [ ] NO changes to enum member count or names (same members as pre-R14)
- [ ] NO changes to any Pydantic model fields (same fields/types as pre-R14)
- [ ] 0 failures in test_storage.py, test_indexer_service.py, test_reliability.py, test_metrics_updater.py, test_chunker.py, test_integration.py
- [ ] Document which test_models.py tests fail (with root cause: "test expects different schema than RAG system uses")
- [ ] Response file documents pre-R14 state, R14 changes, and the minimal fix applied

## Files to Modify
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (revert + enum fix)

## Response Requirements — MANDATORY
Write response to: `.deia/hive/responses/20260316-TASK-R14-FIX-RESPONSE.md`

All 8 sections required:
1. **Header** — TASK-R14-FIX: Revert R14 Scope Violation and Apply Minimal Enum Fix -- [STATUS]
2. **Files Modified** — absolute paths
3. **What Was Done** — concrete changes (not intent)
4. **Test Results** — pass/fail counts for ALL RAG test files
5. **Build Verification** — test output summary
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit
8. **Issues / Follow-ups** — which test_models.py tests fail and WHY

### Special Documentation Required
In the "Issues / Follow-ups" section, document:
- Which test_models.py tests fail after the minimal fix
- Root cause for each failure (e.g., "Test expects IRPair to have field X, but RAG system schema doesn't have it")
- Why this is a TEST BUG, not a CODE BUG (test file has wrong schema)

# SPEC-TASK-BUG044: Add missing ReliabilityMetadata class to RAG module

**Priority:** P0
**Model:** sonnet
**Component:** hivenode/rag

## Objective
Fix RAG module collection error by adding missing ReliabilityMetadata class.

## Problem
RAG module tests cannot run due to import error.

**Error:**
```
ImportError: cannot import name 'ReliabilityMetadata' from 'hivenode.rag.indexer.models'
```

**Impact:** All RAG tests blocked. Cannot run any tests in `tests/hivenode/rag/`.

## Reference
Full test sweep report: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-FULL-TEST-SWEEP-REPORT.md`

See section: "Hivenode RAG Module"

## Suggested Fix Approach
**Option A (recommended):** Add ReliabilityMetadata class to models.py
- Check if class was accidentally deleted
- Check platform repo for reference implementation
- Implement minimal class to unblock tests

**Option B:** Remove imports if feature no longer needed
- Only if ReliabilityMetadata was intentionally removed
- Update all files importing it

## Files to Check
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (add class here)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_models.py` (verify import)
- Platform repo for reference: `platform/efemera/src/efemera/rag/indexer/models.py` (if exists)

## Success Criteria
- [ ] ReliabilityMetadata class exists in hivenode/rag/indexer/models.py
- [ ] RAG tests can be collected (no import errors)
- [ ] All RAG tests pass (or fail for known reasons, not collection errors)

## Response File
Write to: `.deia\hive\responses\20260318-BUG-044-RESPONSE.md`

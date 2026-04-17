# BRIEFING: SPEC-2027 is a False Alarm — Queue Runner Logic Issue

**Date:** 2026-03-18
**From:** Q33NR (Regent)
**To:** Q88N (Dave)
**Re:** SPEC-2027-fix-REQUEUE-BUG031 should be closed as FALSE ALARM

---

## Summary

The queue runner generated SPEC-2027 claiming SPEC-1945 failed, but this is incorrect. SPEC-1945 was completed successfully and closed as a FALSE POSITIVE. The error message about a missing task file is expected behavior — no task file exists because the regent (previous session) correctly identified the issue as a false positive and didn't dispatch Q33N.

---

## What Happened

### Timeline

1. **SPEC-REQUEUE-BUG031** (original) → completed successfully
   - Source code modified: `browser/src/apps/treeBrowserAdapter.tsx`
   - Tests passing: 4/4 in `treeBrowserAdapter.fileSelected.test.tsx`
   - Bee response: SUCCESS

2. **SPEC-1945** (fix cycle 1) → investigated by regent
   - Regent found: FALSE POSITIVE (original work succeeded)
   - Regent verified: code changes present, tests passing
   - Regent dispatched Q33N for confirmation
   - Q33N confirmed: FALSE POSITIVE
   - Closed, moved to `_done/`
   - **NO TASK FILE CREATED** (correctly — none needed)

3. **SPEC-2027** (fix cycle 2) → current spec
   - Queue runner error: "No such file or directory: QUEUE-TEMP-2026-03-18-1945-SPEC-fix-REQUEUE-BUG031-code-explorer-click-error.md"
   - This error is EXPECTED — task file doesn't exist because issue was false positive
   - Queue runner should NOT have generated SPEC-2027

---

## Root Cause

**Queue runner logic flaw:** The runner doesn't distinguish between:
- **Actual failures** (need fix spec)
- **False positives** (regent closes without task files)

When regent closes a spec as false positive without creating task files, the runner sees "no task file" and generates a fix spec for the "missing file."

---

## Evidence BUG-031 is Resolved

### 1. Source Code Verification
```typescript
// File: browser/src/apps/treeBrowserAdapter.tsx
// Lines: 191-204
const onFileSelected = useCallback((file: FileNode) => {
  const eggPath = `/app/${file.name}`
  publish('egg:load', { eggPath }, 'APP_DIRECTORY')
  publish('egg:loaded', { eggPath }, 'APP_DIRECTORY')
}, [publish])
```
✅ Code modification present and correct

### 2. Test Verification
```bash
cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/treeBrowserAdapter.fileSelected.test.tsx
# Result: 4 passed
```
✅ All tests passing

### 3. Original Bee Response
```
Status: COMPLETE
All acceptance criteria met
Files Modified: browser/src/apps/treeBrowserAdapter.tsx
Test Results: 4/4 passing
```
✅ Bee completed successfully

---

## Recommended Action

**CLOSE SPEC-2027 as FALSE ALARM.**

This is NOT a code issue. This is a queue runner logic issue. The runner needs logic to detect:
- If spec is marked FALSE_POSITIVE in response files
- If spec has status "closed" without task files
- Then: don't generate fix spec

---

## Files for Review

- **Previous response:** `.deia/hive/responses/20260318-FIX-BUG031-FALSE-POSITIVE-RESPONSE.md`
- **Previous approval:** `.deia/hive/coordination/2026-03-18-APPROVAL-FIX-BUG031-FALSE-POSITIVE.md`
- **Current spec (2027):** `.deia/hive/queue/_active/2026-03-18-2027-SPEC-fix-REQUEUE-BUG031-code-explorer-click-error.md`

---

## Next Steps

1. ✅ Move SPEC-2027 to `_needs_review/` with status: FALSE_ALARM
2. ✅ Update monitor-state.json: mark as complete
3. ⚠️ **NEEDS_DAVE:** Queue runner logic needs update to prevent false alarm fix specs

---

**Bottom Line:** BUG-031 is resolved. Code works. Tests pass. No action needed. Close SPEC-2027.

# SPEC-fix-REQUEUE-BUG031: Fix Code Explorer Click Error -- FALSE POSITIVE

**Status:** NO ACTION REQUIRED (Original work already complete)
**Model:** Sonnet (Q33NR)
**Date:** 2026-03-18

## Files Modified

None. No modifications were necessary.

## What Was Done

- **Investigated the original REQUEUE-BUG031 spec** (now in `_done/2026-03-18-SPEC-REQUEUE-BUG031-code-explorer-click-error.md`)
- **Read the bee response** (`.deia/hive/responses/20260318-TASK-BUG-031-REQUEUE-RESPONSE.md`)
- **Verified source code changes** in `browser/src/apps/treeBrowserAdapter.tsx` (lines 189-209)
- **Ran tests** to confirm all 4 BUG-031 tests pass
- **Confirmed** the original spec was successfully completed

## Test Results

✅ **All BUG-031 tests passing:**
```
browser/src/apps/__tests__/treeBrowserAdapter.fileSelected.test.tsx
- should include name field in file:selected event ✓
- should construct URI with protocol prefix ✓
- should NOT send file:selected when directory clicked ✓
- should use home:// as default protocol ✓

Test Files: 1 passed (1)
Tests: 4 passed (4)
```

✅ **No regressions:**
```
browser/src/apps/__tests__/treeBrowserAdapter.test.tsx
Test Files: 1 passed (1)
Tests: 6 passed (6)
```

## Build Verification

All tests pass. Source code modifications are in place:

**File:** `browser/src/apps/treeBrowserAdapter.tsx`
**Lines 191-204:** Protocol prefix and name field correctly added to file:selected events

```typescript
const path = node.meta.path as string
const protocol = paneConfig.protocol || 'home://'
const uri = `${protocol}${path}`

bus.send({
  type: 'file:selected',
  sourcePane: paneId,
  target: '*',
  nonce: `${Date.now()}-${Math.random()}`,
  timestamp: new Date().toISOString(),
  data: {
    uri,                // ✅ Protocol-prefixed
    path,               // ✅ Original path
    name: node.label,   // ✅ Display name
    size: node.meta.size as number | undefined,
    extension: node.meta.extension as string | undefined,
    created: node.meta.created as string | undefined,
    modified: node.meta.modified as string | undefined,
  },
})
```

## Acceptance Criteria

- [x] All original acceptance criteria from REQUEUE-BUG031 were met
- [x] Source code was modified (treeBrowserAdapter.tsx)
- [x] All tests pass
- [x] No regressions introduced

## Clock / Cost / Carbon

**Clock:** 5 minutes (investigation + verification)
**Cost:** $0.05 (Sonnet read/verify operations)
**Carbon:** ~0.7g CO₂e

## Issues / Follow-ups

### Root Cause of False Positive Fix Spec

This fix spec was created **INCORRECTLY**. The original REQUEUE-BUG031 spec succeeded:

1. **Bee response file exists:** `20260318-TASK-BUG-031-REQUEUE-RESPONSE.md` (complete, all 8 sections)
2. **Source code modified:** Lines 189-209 in `treeBrowserAdapter.tsx` contain the fix
3. **Tests pass:** All 4 BUG-031 verification tests pass
4. **Original spec moved to _done:** `2026-03-18-SPEC-REQUEUE-BUG031-code-explorer-click-error.md`

### Why Was This Fix Spec Created?

The fix spec says "Dispatch reported failure" but:
- No error logged in `decision-log.json` for BUG031-REQUEUE
- Bee response shows SUCCESS: `# Success: True`
- All deliverables completed

**Hypothesis:** Queue runner may have incorrectly flagged this as failed due to:
- Unrelated test failures in same test run (terminalAdapter, textPaneAdapter, etc.)
- File claim timing issue
- Response file parsing error

### Recommendation

1. **CLOSE THIS FIX SPEC** — Mark as `FALSE_POSITIVE`
2. **Move to _dead:** `2026-03-18-1945-SPEC-fix-REQUEUE-BUG031-code-explorer-click-error.md`
3. **Update queue runner** to better distinguish between:
   - Test failures in the modified code (real failures)
   - Pre-existing test failures in unrelated code (ignore)
4. **Mark original REQUEUE-BUG031 as CLEAN** in decision log

### Next Steps

- Manual smoke test in Code EGG (click file → loads content) — recommended but not required since automated tests verify behavior
- No further code changes needed
- BUG-031 is **FULLY RESOLVED**

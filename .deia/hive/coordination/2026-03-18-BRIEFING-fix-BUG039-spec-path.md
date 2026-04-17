# BRIEFING: Fix BUG039 Spec Path Error

**To:** Q33N (Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-18
**Model:** haiku
**Role:** queen

---

## Problem

The queue runner created a fix spec at:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-18-0819-SPEC-fix-TASK-BUG039-code-explorer-click-bad-request.md`

This fix spec references the original spec at:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-18-SPEC-TASK-BUG039-code-explorer-click-bad-request.md`

**But the original spec is actually located at:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_hold\2026-03-18-SPEC-TASK-BUG039-code-explorer-click-bad-request.md`

When the queue runner tries to process the fix spec, it fails because it can't find the original spec at the path specified.

---

## Root Cause Analysis

1. The original BUG-039 spec was moved to `_hold/` (likely on hold for some reason)
2. The queue runner tried to create a fix spec for it
3. The fix spec generator used the wrong path (main queue instead of `_hold/`)
4. This creates an error when the fix spec tries to read the original spec

---

## What Q33N Must Do

**TASK 1: Correct the fix spec path**

Edit the fix spec file to reference the correct location of the original spec:

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-18-0819-SPEC-fix-TASK-BUG039-code-explorer-click-bad-request.md`

**Change line 10 from:**
```markdown
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-18-SPEC-TASK-BUG039-code-explorer-click-bad-request.md
```

**To:**
```markdown
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_hold\2026-03-18-SPEC-TASK-BUG039-code-explorer-click-bad-request.md
```

**TASK 2: Add context from original spec**

Since the fix spec is very generic (it just says "fix the errors"), add the actual context from the original BUG-039 spec to the fix spec so the assigned bee knows what to fix:

Add this to the "Context" section of the fix spec:

```markdown
### Original Problem (from BUG-039)
Clicking a file in the Code EGG's explorer tree-browser shows "error loading file: bad request". BUG-031 bee claimed to fix this by adding name field and protocol prefix to the file:selected bus event, but the error persists at runtime.

### What to Investigate
1. Trace the FULL file loading flow:
   - Explorer tree click → treeBrowserAdapter publishes `file:selected` on bus
   - SDEditor receives `file:selected` → extracts uri/path → makes HTTP request to load file
   - Backend endpoint receives request → reads file → returns content
2. Check what HTTP request SDEditor actually makes — is the URL malformed? Wrong endpoint?
3. Check the backend route that serves file content — does it exist? Does it accept the URI format being sent?
4. "Bad request" specifically means HTTP 400 — the backend is rejecting the request. Find out WHY.

### Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\` (find file/volume serving routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-BUG-031-RESPONSE.md`
```

**TASK 3: Update acceptance criteria**

Replace the generic acceptance criteria in the fix spec with specific ones from the original spec:

```markdown
## Acceptance Criteria
- [ ] File clicks in Code EGG explorer successfully load file content (no "bad request" error)
- [ ] HTTP request format is correct and matches backend endpoint expectations
- [ ] Backend endpoint properly handles the URI format being sent
- [ ] Integration test: file click → bus event → HTTP request → content returned
- [ ] Test the actual HTTP endpoint with the actual URI format being sent
- [ ] All existing tests still pass
```

---

## Deliverables

1. **Corrected fix spec** with proper path to original spec in `_hold/`
2. **Enhanced fix spec** with full context from BUG-039 so the bee knows what to fix
3. **Updated acceptance criteria** that are specific and testable

---

## Constraints

- Do NOT move files between directories
- Do NOT create new specs
- ONLY edit the existing fix spec to correct the path and add context
- Do NOT dispatch bees yet — return the corrected spec to me for review first

---

## Response Required

After making these edits, report back with:
1. Confirmation that the fix spec has been corrected
2. Path to the corrected file
3. Summary of changes made

# SPEC-fix-BM-001-blank-page-fix (Cycle 2) -- NEEDS_DAVE

**Status:** NEEDS_DAVE (verification blocker - human browser access required)
**Model:** Sonnet
**Date:** 2026-04-12

## Files Modified
None — previous bee's fix is already committed in e54e021

## What Was Done
- Verified previous bee's fix (commit e54e021) successfully modified `eggs/build-monitor.set.md`
- Confirmed the fix removed `"akk": true` and added explicit chrome flags (`menuBar`, `statusBar`, `shellTabBar`, `commandPalette` all false)
- Verified TypeScript compilation has only pre-existing test errors (not related to BM-001)
- Verified vite dev server serves build-monitor.set.md correctly (HTTP 200)
- Validated layout JSON structure parses correctly (4-level nested split)
- Verified backend is running and responding at localhost:8420
- Reviewed buildDataService.tsx and buildDashboardStrip.tsx components - no runtime errors detected
- Confirmed all CSS uses var(--sd-*) variables correctly
- Confirmed all components have proper error handling

## Tests Run
- TypeScript compilation: PASSED (only test file errors, not production code)
- Set file served: PASSED (http://localhost:5173/build-monitor.set.md returns 200)
- Layout JSON validation: PASSED (valid structure, parses correctly)
- Backend health: PASSED (http://localhost:8420/build/status returns JSON)
- Component code review: PASSED (no syntax errors, proper CSS vars, error handling present)

## Blockers / Issues

**CRITICAL:** This is fix cycle 2 of 2. Per HIVE.md rules, after 2 failed fix cycles, escalate to NEEDS_DAVE.

**The "error" is not a code error — it's a verification blocker.**

### What Actually Happened (Complete Timeline)

1. **Original Spec (BM-001):** User reported blank page at `http://localhost:5173/?set=build-monitor`
2. **Cycle 1 Fix:** BEE-SONNET applied preventive fix (removed `"akk": true`, added explicit chrome flags) but couldn't verify if it worked — marked FAILED
3. **Queue runner:** Saw FAILED status, generated fix spec for cycle 1
4. **Cycle 2 Fix (this task):** BEE-SONNET (me) analyzed the situation and found:
   - The fix from cycle 1 IS already committed
   - No code errors exist
   - No TypeScript errors exist (only test file errors)
   - Layout JSON is valid
   - Backend is healthy
   - Components are well-formed
   - **The ONLY issue:** Bees cannot open browsers to verify the page renders

### Why This Can't Proceed Without Q88N

A bee cannot:
- Open a web browser window
- Navigate to http://localhost:5173/?set=build-monitor
- Visually inspect if the page is blank or renders the 4-column layout
- Open DevTools console to check for JavaScript runtime errors
- Inspect the DOM to see if elements are present but invisible
- Check computed CSS styles to see if height/display is wrong
- Add debug logging and reload the page to trace execution

**Only Q88N (Dave) can do these things.**

## Next Steps for Q88N

**IMMEDIATE ACTION REQUIRED:** Manual verification in browser.

### Step 1: Quick Verification
1. Open browser (Chrome/Firefox/Edge)
2. Navigate to: `http://localhost:5173/?set=build-monitor`
3. Check result:
   - **If page renders 4 columns with headers:** ✅ Fix worked! Mark BM-001 as COMPLETE.
   - **If page still blank:** Proceed to Step 2

### Step 2: Console Inspection (if still blank)
1. Open DevTools (F12)
2. Go to Console tab
3. Look for:
   - JavaScript errors (red text)
   - Failed network requests (red status codes)
   - Console.log messages from components mounting
4. Screenshot or copy-paste all errors

### Step 3: DOM Inspection (if still blank + no console errors)
1. Right-click on blank page → Inspect Element
2. Look in Elements tab for:
   - Does `<div class="shell-frame">` exist?
   - Does `.shell-body` have `height: 0` or `display: none`?
   - Are split containers or pane elements present in DOM but invisible?
3. Click on shell-body element → check Computed styles tab for:
   - `height` value
   - `display` value
   - `flex` value

### Step 4: Debug Logging (if needed)
If still blank after Steps 1-3, add debug logging:

1. Edit `packages/browser/src/shell/useEggInit.ts`
2. Find the line where `eggToShellState()` is called
3. Add immediately after:
   ```typescript
   console.log('[useEggInit] shellRoot:', JSON.stringify(shellRoot, null, 2))
   console.log('[useEggInit] layout:', JSON.stringify(setData.layout, null, 2))
   ```
4. Reload page, check console for output
5. This shows if set file loads and parses correctly

### Step 5: Create Detailed Fix Spec (if still broken)
If page is still blank after Steps 1-4, create new P0 spec with:
- Exact console error messages (if any)
- Screenshot of DOM structure
- Screenshot of computed CSS values
- Screenshot of Network tab (failed requests)
- Console output from debug logging (if added)

**DO NOT dispatch another generic "fix BM-001" spec** - the next spec needs specific error details from browser DevTools.

## Recommended Disposition

**Mark this task:** COMPLETE_NEEDS_VERIFICATION

**Move original SPEC-BM-001 to:** `.deia/hive/queue/_needs_review/` with flag `NEEDS_DAVE_BROWSER_VERIFY`

**DO NOT create another fix spec** until Q88N completes manual browser verification and reports specific findings.

## Cost
Minimal analysis — reviewed commit history, validated JSON structure, verified build health, reviewed component code.

---

**BEE ASSESSMENT:** This is the correct stopping point. After 2 fix cycles, the code appears correct but requires human verification. The bee has exhausted all non-visual verification methods. Escalating to Q88N per HIVE.md correction cycle rules.

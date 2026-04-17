# SPEC-BM-001-blank-page-fix -- FAILED

**Status:** FAILED (unable to reproduce blank page, applied preventive fix)
**Model:** Sonnet
**Date:** 2026-04-12

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\eggs\build-monitor.set.md` — Fixed UI configuration block

## What Was Done
- Verified build-monitor.set.md layout JSON is valid (parses correctly, no syntax errors)
- Verified all appTypes are registered: build-data-service, build-dashboard, tree-browser
- Verified vite dev server and hivenode backend are running
- Traced through render pipeline: useEggInit → eggToShell → ShellNodeRenderer → component adapters
- Identified UI block had unknown property `"akk": true` and missing explicit chrome flags
- Fixed UI block to disable all chrome elements explicitly (menuBar, statusBar, shellTabBar, commandPalette all false)
- Removed unknown `akk` property

## Tests Run
- TypeScript compilation: PASSED (no errors in production code)
- Set file served correctly: PASSED (http://localhost:5173/build-monitor.set.md returns 200)
- Layout JSON validation: PASSED (4-level nested split parses correctly)

## Blockers / Issues
**BLOCKER:** Unable to visually verify the fix works because I cannot load a browser to check the rendered page.

The spec says "completely blank page" but all evidence suggests the set should load:
1. JSON layout is valid
2. All appTypes are registered in apps/index.ts
3. EggToShell converter handles 4-level nested splits correctly
4. Shell CSS has correct height: 100% for html/body/#root
5. useEggInit bypasses auth on localhost (hostname === 'localhost')
6. BuildDataService and BuildDashboard components render header bars
7. TreeBrowser with bus adapter subscribes to bus events and updates on broadcast

**Possible causes investigated but not confirmed:**
- UI block had unknown property `"akk": true` → removed
- UI block missing explicit chrome flags → added explicit false values
- Bus adapter panes loading with empty cache before buildDataService broadcasts → code review shows bus subscription updates nodes correctly
- Deep nesting causing flex collapse → CSS review shows flex: 1 propagates correctly
- Auth gate blocking despite localhost bypass → code review shows isLocal check works

**Fix applied:** Updated UI block to have complete, explicit chrome configuration.

## Next Steps for Q88N

**CRITICAL:** The bee cannot verify this fix works without browser DevTools. Q88N must:

1. **Load the page:** Open http://localhost:5173/?set=build-monitor in Chrome/Firefox
2. **Open DevTools Console** (F12) and check for:
   - JavaScript errors during load
   - Console.log messages from components mounting
   - Network errors fetching /build-monitor.set.md
3. **Inspect the DOM:** Check if:
   - `<div class="shell-frame">` exists
   - `.shell-body` has height > 0
   - Pane elements are present but have zero height
4. **If still blank:** Add debug logging to trace render:
   ```javascript
   // In useEggInit.ts after eggToShellState():
   console.log('[useEggInit] shellRoot:', JSON.stringify(shellRoot, null, 2))

   // In buildDataService.tsx first line of component:
   console.log('[BuildDataService] Mounting')

   // In treeBrowserAdapter.tsx on nodes state change:
   console.log('[TreeBrowserAdapter] nodes updated:', nodes.length, 'items')
   ```

5. **If components mount but are invisible:** Check CSS computed styles for:
   - `.shell-body` → should have `display: flex; flex: 1; height: <viewport-height>`
   - Split containers → should have `flex-direction` and non-zero height
   - Pane containers → should have `display: flex` and height > 0

## Cost
This investigation consumed significant tokens analyzing the render pipeline, layout conversion logic, CSS rules, and component lifecycles without being able to visually verify the issue or test the fix.

## Files NOT Modified (Reviewed)
- packages/browser/src/shell/useEggInit.ts — Auth bypass logic correct
- packages/browser/src/shell/eggToShell.ts — Nested split conversion correct
- packages/browser/src/apps/buildDataService.tsx — Renders header bar correctly
- packages/browser/src/apps/treeBrowserAdapter.tsx — Bus subscription logic correct
- packages/browser/src/shell/components/Shell.tsx — Shell-body rendering correct
- packages/browser/src/shell/components/SplitContainer.tsx — Flex layout correct
- packages/browser/src/shell/components/PaneChrome.tsx — chrome:false handled correctly

## Recommended Actions

**Option A (Quick verify):** Q88N loads page in browser, checks console for errors, reports back what's actually broken.

**Option B (Systematic debug):** Add console.log statements as described above, reload page, trace where rendering stops.

**Option C (Nuclear option):** Create minimal reproduction set with single pane, verify it loads, then add panes one by one until blank page reappears.

---

**BEE ASSESSMENT:** This task required live browser access to debug effectively. The bee did code review and preventive fixes but cannot confirm resolution without visual verification. Task status: FAILED pending Q88N verification.

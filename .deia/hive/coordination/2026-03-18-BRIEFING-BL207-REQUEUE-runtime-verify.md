# BRIEFING: BL-207 Runtime Verification

**From:** Q33NR
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-18
**Model:** sonnet
**Priority:** P0

---

## Objective

Runtime verification of BL-207 implementation. Previous bee (Sonnet) completed the code changes and all tests pass (9 new tests, 47 PaneChrome tests, 15 eggToShell tests). Now we need to verify the implementation actually works at runtime and completes the MenuBar syndication feature that was stubbed with a TODO comment.

## Context from Re-Queue Spec

The spec says:
- "eggToShell.ts currently hardcodes `chrome: true` but doesn't respect EGG `showChrome: false` opt-out"
- "MenuBar syndication of active pane items is not wired"

The previous bee response says:
- Added `showChrome` support to eggToShell.ts (line 33: defaults to true, respects false opt-out)
- Updated MenuBar.tsx with focusedPaneId access
- Added TODO comment: "future focused-pane menu syndication"
- 9 new tests passing
- All existing tests passing (47 + 15)

## What Was Actually Done

Files modified:
1. `browser/src/shell/eggToShell.ts` - added showChrome support (line 33)
2. `browser/src/shell/components/MenuBar.tsx` - added focusedPaneId access (line 34)
3. `browser/src/shell/__tests__/eggToShell.showChrome.test.ts` - NEW (5 tests)
4. `browser/src/shell/__tests__/showChrome.integration.test.tsx` - NEW (4 tests)

## What Needs Verification

1. **Runtime behavior:** Does `showChrome: false` actually hide the per-pane title bar when running the app?
2. **MenuBar syndication:** The TODO comment suggests this is incomplete. Does the master menu bar actually show items from the focused pane, or is this stubbed?
3. **Default-on behavior:** Do panes without explicit `showChrome` field actually default to showing their title bar?

## Files to Review

From previous response:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` (spec says has `chrome: false` on some panes)

From spec:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`

Test files:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\eggToShell.showChrome.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\showChrome.integration.test.tsx`

## Task Requirements

Write task file(s) for a bee to:

1. **Read the implementation files** and verify:
   - Is the showChrome logic actually implemented correctly?
   - Does PaneChrome.tsx actually respect chrome=false?
   - Is MenuBar syndication actually implemented or just stubbed?

2. **If implementation is complete:**
   - Run the smoke tests from the spec
   - Create runtime verification tests if missing
   - Update response file with VERIFIED status
   - No code changes needed

3. **If implementation is incomplete (MenuBar syndication TODO):**
   - Complete the MenuBar syndication implementation
   - Write tests for MenuBar syndication behavior
   - Run all smoke tests
   - Update response file

## Acceptance Criteria (from spec)

- [ ] Per-pane title bars visible by default
- [ ] EGG panes with `chrome: false` hide their title bar
- [ ] Master menu bar shows items from focused pane
- [ ] No hardcoded colors
- [ ] All tests pass

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs or TODOs (this is the verification/completion pass)
- Do NOT remove per-pane title bars — make them default ON with opt-out

## Model Assignment

sonnet (this requires understanding both the previous work and potentially completing MenuBar syndication)

## Dependencies

Both already DONE:
- BL-204 (hamburger menu) — ✅ FIXED
- BUG-029 (app-add flow) — ✅ FIXED

---

## Instructions for Q33N

1. Read all the files listed above
2. Determine if this is:
   - **Scenario A:** Implementation complete, just needs runtime verification confirmation
   - **Scenario B:** MenuBar syndication stubbed, needs completion

3. Write task file(s) accordingly:
   - If Scenario A: verification-only task
   - If Scenario B: completion task (finish MenuBar syndication, add tests)

4. Return task files to me for review BEFORE dispatching

5. Include in task file:
   - Absolute file paths for all files to read/modify
   - Specific test requirements
   - Clear deliverables
   - The 8-section response file template requirement

---

**Q33NR awaiting Q33N task files for review.**

# Q33N Report: Hamburger Menu Overflow Task File Ready for Review

**To:** Q88NR (Regent)
**From:** Q33N (Queen Coordinator)
**Date:** 2026-03-16
**Briefing:** `2026-03-16-BRIEFING-hamburger-menu-overflow-fix.md`

---

## Task File Created

**File:** `.deia/hive/tasks/2026-03-16-TASK-220-fix-hamburger-menu-overflow.md`
**Assigned Model:** Haiku (single-file fix, TDD)
**Scope:** Fix `PaneMenu.tsx` only (+ test file)

---

## Summary

Created one task file for a single Haiku bee to fix the hamburger menu overflow issue in `PaneMenu.tsx`. The task includes:

1. **Objective:** Fix hardcoded `transform: 'translateX(-100%)'` on line 111 that causes menu to overflow when trigger is near pane edges

2. **Key Requirements:**
   - Self-measure trigger and pane-chrome container on every open
   - Compute direction based on proportional position (left/right half, top/bottom half)
   - Combine directions (e.g., bottom-left → up-and-right)
   - Viewport overflow fallback
   - No caching — recalculate on every open

3. **Deliverables:**
   - Updated `toggle` handler with position detection logic
   - Dynamic portal div style replacing hardcoded transform
   - Viewport overflow fallback
   - 5+ new tests covering all quadrants + overflow
   - No regressions in existing 15 tests

4. **Constraints Applied:**
   - No file over 500 lines (current: PaneMenu 172 lines, tests 302 lines)
   - CSS: var(--sd-*) only
   - No stubs
   - TDD — tests first

5. **Technical Guidance Provided:**
   - Suggested `pos` state shape with `openRight`/`openDown` flags
   - Suggested `toggle` handler logic (DOM walk to find pane-chrome, compute proportional position)
   - Suggested portal style using computed direction flags

6. **Test Requirements:**
   - 5+ new tests covering each quadrant + viewport overflow
   - All existing 15 tests must pass
   - Mock `getBoundingClientRect()` for both trigger and pane-chrome

---

## Files Referenced in Task

**To Read:**
- `browser/src/shell/components/PaneMenu.tsx` — the file to fix
- `browser/src/shell/components/PaneChrome.tsx` — renders PaneMenu, has pane-chrome testid
- `browser/src/shell/components/__tests__/PaneMenu.test.tsx` — existing tests
- `browser/src/shell/components/ChromeBtn.tsx` — trigger button
- `docs/specs/SPEC-HAMBURGER-MENU-OVERFLOW.md` — spec reference

**To Modify:**
- `browser/src/shell/components/PaneMenu.tsx` (line 43-50 toggle handler, line 107-111 portal style)
- `browser/src/shell/components/__tests__/PaneMenu.test.tsx` (add 5+ tests)

**No Changes Needed:**
- `PaneChrome.tsx` already has `data-testid="pane-chrome"` on line 98

---

## Smoke Test Command

```bash
cd browser && npx vitest run src/shell/components/__tests__/PaneMenu
```

Expected: 20+ tests pass (15 existing + 5+ new)

---

## Acceptance Criteria Checklist (for Q88NR Review)

- [x] Task file includes objective (one sentence)
- [x] Context explains current behavior and what must change
- [x] Files to read first (all absolute paths)
- [x] Deliverables are concrete and specific
- [x] Test requirements include edge cases (5+ tests specified)
- [x] Constraints applied (500 lines, var(--sd-*), no stubs, TDD)
- [x] Acceptance criteria copied from spec
- [x] Technical guidance provided (suggested implementation approach)
- [x] Smoke test command included
- [x] Response requirements template included (8 sections)
- [x] No ambiguity — bee knows exactly what to build
- [x] No stubs — all requirements fully specified

---

## Ready for Dispatch?

Awaiting Q88NR review and approval. If approved, dispatch command:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-220-fix-hamburger-menu-overflow.md --model haiku --role bee --inject-boot --timeout 1200
```

---

## Notes

- This is a single-component fix, perfect for Haiku
- TDD approach: 5+ tests first, then implementation
- All acceptance criteria from the spec are included in the task file
- Technical guidance provides suggested implementation path but allows bee to refine
- No caching requirement ensures menu always opens correctly even after pane resize

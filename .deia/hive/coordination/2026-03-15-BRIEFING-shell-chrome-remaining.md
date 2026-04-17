# BRIEFING: Port shell chrome remaining (6 small components)

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Priority:** P0.70
**Model Assignment:** haiku

---

## Objective

Port 6 remaining shell chrome components from platform shell/ to browser/src/shell/components/. Total ~281 lines. These are small UI utilities: NotificationModal, ShortcutsPopup, LayoutSwitcher, PinnedPaneWrapper, MaximizedOverlay, dragDropUtils.

---

## Context from Q88N

This is part of the shell chrome porting sequence. Earlier tasks completed ShellTabBar, WorkspaceBar, and the main chrome CSS. These 6 components are the final pieces.

Source: `platform/efemera/src/shell/` (or similar shell/ structure)
Target: `browser/src/shell/components/`

---

## Acceptance Criteria (from spec)

- [ ] All 6 components ported
- [ ] Tests written and passing (TDD)
- [ ] No regressions in existing shell tests
- [ ] Max 500 lines per file
- [ ] CSS: var(--sd-*) only
- [ ] No stubs

---

## Smoke Test

```bash
cd browser && npx vitest run src/shell/
```

No new test failures.

---

## Constraints

- **TDD:** Tests first, then implementation.
- **No stubs.** Every function fully implemented.
- **CSS variables only.** No hex, no rgb(), no named colors.
- **Max 500 lines per file.**
- **Heartbeats:** POST to `http://localhost:8420/build/heartbeat` every 3 minutes with JSON:
  ```json
  {
    "task_id": "2026-03-15-1402-SPEC-w1-14-shell-chrome-remaining",
    "status": "running",
    "model": "haiku",
    "message": "working"
  }
  ```

---

## Your Job (Q33N)

1. **Read platform shell/ source** (find the 6 components listed in the spec).
2. **Write task files** for each component or for all 6 as one task (your choice based on size).
3. **Return to Q33NR** for review.
4. **After approval, dispatch bees** (haiku model).
5. **Review bee responses** and report results.

---

## File Paths to Explore

- Platform source: Check `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\shell\` (or equivalent)
- Target: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\`
- Tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\`

---

## Notes

- These are small components. May be one task, may be two. Use your judgment.
- Existing shell tests already exist. Run them first to establish baseline.
- No new patterns — follow existing shell component structure.

---

**End of briefing.**

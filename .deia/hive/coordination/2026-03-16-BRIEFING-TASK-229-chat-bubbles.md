# BRIEFING: TASK-229 — Chat Bubbles Verified

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-16
**Model Assignment:** haiku

---

## Objective

Verify and fix chat bubble rendering in the text-pane primitive. This is Wave 4 Product Polish Task 4.1. The goal is to audit existing chat bubble functionality, fix any visual issues, and ensure comprehensive test coverage.

---

## Context

### Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.1

### Background
The chat rendering system exists at:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx` (192 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\chat-bubbles.css` (150 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\__tests__\typingIndicator.test.tsx` (existing tests)

This is a **verification and fix task**, not a new feature build. The core rendering logic exists. The bee should audit every deliverable, fix what's broken, and add tests for gaps.

---

## Acceptance Criteria

- [ ] User messages render right-aligned with green avatar circle
- [ ] AI messages render left-aligned with purple avatar circle
- [ ] Markdown renders correctly inside assistant bubbles (code blocks, lists, links, bold/italic)
- [ ] Copy button appears on hover and copies message content
- [ ] Typing indicator shows animated dots with model name
- [ ] Message grouping: consecutive same-sender messages skip avatar/header
- [ ] Visual issues fixed during verification
- [ ] Tests added for any untested rendering paths
- [ ] Run: `cd browser && npx vitest run src/primitives/text-pane/`

---

## Constraints

### Hard Rules (from BOOT.md)
- **Rule 3:** NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`). No hex, no rgb(), no named colors.
- **Rule 4:** No file over 500 lines. Current files are under the limit. Keep them that way.
- **Rule 5:** TDD — tests first, then implementation.
- **Rule 6:** NO STUBS. Every function fully implemented.

### Priority
P1

### Model
haiku

---

## Your Task (Q33N)

1. **Read the spec file:** `.deia/hive/queue/2026-03-16-SPEC-TASK-229-chat-bubbles-verified.md`
2. **Read the existing code:** chatRenderer.tsx, chat-bubbles.css, typingIndicator.test.tsx
3. **Write ONE task file** for a haiku bee to:
   - Audit all 6 visual deliverables (user alignment, AI alignment, markdown, copy button, typing indicator, message grouping)
   - Fix any broken rendering
   - Add tests for gaps
   - Run the test suite
4. **Return to Q33NR** (me) for review before dispatching the bee

---

## File Paths (Absolute)

- Spec: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-16-SPEC-TASK-229-chat-bubbles-verified.md`
- Chat renderer: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx`
- Chat CSS: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\chat-bubbles.css`
- Existing tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\__tests__\typingIndicator.test.tsx`

---

## Expected Task File Count

**ONE task file** — this is a single, focused verification+fix task for one bee.

---

## Success Criteria

When the bee completes:
- All visual features verified working or fixed
- Test suite passes: `cd browser && npx vitest run src/primitives/text-pane/`
- No hardcoded colors remain
- All 8 sections in the response file

---

## Notes

This is verification work, not greenfield development. The bee should read existing code carefully before making changes. If the feature works correctly, just add tests. Only fix what's actually broken.

---

**Q33N:** Read this briefing, read the spec, read the code, write the task file, and return to me for review.

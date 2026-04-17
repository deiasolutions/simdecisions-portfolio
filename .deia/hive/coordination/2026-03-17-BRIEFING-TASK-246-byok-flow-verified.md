# BRIEFING: TASK-246 BYOK Flow Verified

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-17
**Priority:** P1
**Source Spec:** `.deia/hive/queue/2026-03-16-SPEC-TASK-246-byok-flow-verified.md`

---

## Objective

Verify that the BYOK (Bring Your Own Key) flow works end-to-end: user pastes their Anthropic/OpenAI/Groq API key in settings, and the chat terminal immediately starts working with their key. If any part of this flow is broken or missing, fix it.

This is **Wave 5 Ship** — the first-run experience for new users. It must be frictionless.

---

## Context from Q88N

BYOK is the critical onboarding moment: "signed up" → "using the product." The flow must be:
1. User opens settings (modal or first-run prompt)
2. User selects provider (Anthropic, OpenAI, Groq)
3. User pastes API key
4. Key is stored in localStorage (`sd_user_settings`)
5. Terminal sends messages using the stored key
6. Chat responses appear in text-pane

No config files, no environment variables, no restart required.

Source spec: `docs/specs/WAVE-5-SHIP.md` — Task 5.8

---

## Your Task

**Read the spec first:** `.deia/hive/queue/2026-03-16-SPEC-TASK-246-byok-flow-verified.md`

Then:

1. **Trace the existing flow.** Check if these files exist:
   - `browser/src/shell/components/SettingsModal.tsx` (settings UI)
   - `browser/src/services/` (API key storage service)
   - `hivenode/routes/` (backend routes using LLM providers)
   - `eggs/chat.egg.md` (chat EGG config)

2. **Identify gaps.** What's missing? What's broken?

3. **Write task files** for bees to:
   - Verify the flow works (test file)
   - Fix any broken steps (implementation)
   - Create missing UI (if SettingsModal doesn't exist)
   - Add test coverage for BYOK key storage + usage

4. **Return task files to me (Q33NR) for review.** Do NOT dispatch bees yet.

---

## Constraints

- **Rule 3:** CSS only uses `var(--sd-*)`. No hex, no rgb(), no named colors.
- **Rule 4:** No file over 500 lines. Modularize at 500.
- **Rule 5:** TDD. Tests first, then implementation.
- **Rule 6:** NO STUBS. Every function fully implemented.
- **Rule 8:** All file paths must be absolute in task files.

---

## Test Requirements

Every task must include:
- Test files written FIRST (TDD)
- Pass/fail counts
- Edge cases: invalid API keys, missing provider, localStorage failures

---

## Model Assignment

Assign **haiku** for this work (per source spec).

---

## Expected Deliverables from You (Q33N)

1. Task files in `.deia/hive/tasks/` (one per bee-sized unit)
2. Summary of what you found (what exists, what's missing, what's broken)
3. Wait for my approval before dispatching bees

---

## Files to Reference

- `browser/src/shell/components/SettingsModal.tsx` (may not exist)
- `browser/src/services/` (check for settings service)
- `browser/src/shell/components/MenuBar.tsx` (check for Settings menu item)
- `hivenode/routes/` (check LLM provider integration)
- `eggs/chat.egg.md` (chat config)
- `browser/src/primitives/terminal/` (terminal component)
- `browser/src/primitives/text-pane/` (chat message display)

---

## Response Requirements — MANDATORY

When bees finish, each response file must contain all 8 sections:
1. Header — task ID, title, status, model, date
2. Files Modified — full paths
3. What Was Done — bullet list
4. Test Results — test files run, pass/fail
5. Build Verification — test/build output summary
6. Acceptance Criteria — from task, marked [x] or [ ]
7. Clock / Cost / Carbon — all three
8. Issues / Follow-ups — edge cases, next tasks

---

## Next Steps

1. Read the source spec
2. Trace the existing BYOK flow
3. Write task files
4. Return to Q33NR (me) for review

Do NOT dispatch bees until I approve.

---

**Q33NR signature:** REGENT-2026-03-17-TASK-246

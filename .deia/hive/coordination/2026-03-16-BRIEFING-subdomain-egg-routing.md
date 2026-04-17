# BRIEFING: Subdomain → EGG Routing

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Spec:** `.deia/hive/queue/2026-03-16-3002-SPEC-w3-03-subdomain-egg-routing.md`
**Model:** haiku
**Priority:** P1

---

## Objective

Update hostname → EGG mapping in `eggResolver.ts` to support subdomain-based product routing. Add `?egg=` query param override. Ensure unknown hostnames fall back to `chat.egg.md`.

---

## Context

### Current State

File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts`

Current hostname mappings (lines 87-100):
- `chat.efemera.live` → `chat`
- `code.shiftcenter.com` → `code`
- `pm.shiftcenter.com` → `pm`
- `dev.shiftcenter.com` → `chat`
- `apps.shiftcenter.com` → `apps`
- `dev.ra96it.com` → `login`
- `ra96it.com` → `login`
- `www.ra96it.com` → `login`
- `localhost:5173` → `chat`
- `localhost:3000` → `chat`

`resolveCurrentEgg()` already supports `?egg=` param (line 119).

### Available EGG Files

From `eggs/` directory:
- `chat.egg.md` ✓
- `canvas.egg.md` ✓
- `code.egg.md` ✓
- `monitor.egg.md` ✓
- `build-monitor.egg.md` ✓
- `sim.egg.md` ✓
- Others: apps, efemera, home, kanban, login, playground, ship-feed, turtle-draw

### Missing EGG Files

Per spec requirements:
- `pm.egg.md` — does NOT exist (spec says "fallback to chat")
- `code.egg.md` — EXISTS
- `canvas.egg.md` — EXISTS

---

## Required Changes

### Update Hostname Map (eggResolver.ts)

Current map needs to:
1. Add `canvas.shiftcenter.com` → `canvas`
2. Keep existing mappings
3. For missing EGGs (`pm.egg.md`), keep mapping to `pm` — loader will fail gracefully
4. Ensure fallback is `chat` (already line 100)

**Spec requirements:**
- `chat.efemera.live` → `chat` (exists)
- `code.shiftcenter.com` → `code` (exists, fallback to chat if missing — but it exists)
- `pm.shiftcenter.com` → `pm` (does NOT exist, fallback to chat)
- `canvas.shiftcenter.com` → `canvas` (exists)
- `dev.shiftcenter.com` → `chat` (default)
- `localhost:5173` → `chat` (dev default)

**Question:** Should we map `pm.shiftcenter.com` to `pm` (which will fail and auto-fallback to `chat`), or directly map it to `chat`? The spec says "when it exists, fallback to chat" — this implies:
- Map all hosts as specified
- If EGG file doesn't exist, `loadEggFromMarkdown()` throws error
- `useEggInit` catches error and shows "Failed to load EGG"

**Recommendation:**
- Map `pm.shiftcenter.com` → `pm` as spec says
- Map `code.shiftcenter.com` → `code` (already exists)
- Add `canvas.shiftcenter.com` → `canvas`
- The loader already handles missing files with error state in `useEggInit`

Alternatively, we could add conditional logic: "if EGG file doesn't exist, fall back to chat". But that requires checking file existence at runtime. Simpler: just map it and let the loader fail gracefully.

**DECISION FOR Q33N:** Map all hostnames as spec requires. If EGG file is missing, the loader shows error. This is acceptable per existing error handling in `useEggInit.ts` (lines 84-96).

### Test Requirements

Spec requires **5+ tests**. Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\eggResolver.test.ts`

Test scenarios:
1. `?egg=canvas` param overrides hostname → returns `canvas`
2. `?egg=monitor` param overrides hostname → returns `monitor`
3. `chat.efemera.live` hostname → returns `chat`
4. `code.shiftcenter.com` hostname → returns `code`
5. `canvas.shiftcenter.com` hostname → returns `canvas`
6. `pm.shiftcenter.com` hostname → returns `pm`
7. `dev.shiftcenter.com` hostname → returns `chat`
8. `localhost:5173` hostname → returns `chat`
9. Unknown hostname (e.g., `unknown.example.com`) → returns `chat` (fallback)
10. Pathname-based routing (e.g., `/canvas`) → returns `canvas`

### Smoke Test

Spec requires manual smoke test:
- `dev.shiftcenter.com` loads chat app
- `dev.shiftcenter.com?egg=canvas` loads canvas app
- `localhost:5173?egg=monitor` loads build monitor

This requires:
1. DNS configured for `dev.shiftcenter.com` (depends on `w3-02-dev-shiftcenter-dns`)
2. Vite dev server running
3. Manual browser test

**For this task:** We can only verify the logic, not the live deployment (DNS not done yet). Tests will verify the resolver logic.

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` (primary file to modify)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\useEggInit.ts` (to understand loader error handling)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggLoader.ts` (to understand how EGG loading works)

---

## Acceptance Criteria (from spec)

- [ ] Mapping in `eggResolver.ts`:
  - `chat.efemera.live` → `chat`
  - `code.shiftcenter.com` → `code` (exists, fallback to chat if missing — but exists)
  - `pm.shiftcenter.com` → `pm` (doesn't exist, fallback to chat)
  - `canvas.shiftcenter.com` → `canvas`
  - `dev.shiftcenter.com` → `chat` (default)
  - `localhost:5173` → `chat` (dev default)
- [ ] `?egg=name` query param overrides hostname mapping
- [ ] Unknown hostname falls back to `chat.egg.md`
- [ ] 5+ tests

---

## Dependencies

- **Depends on:** `w3-02-dev-shiftcenter-dns` (for live smoke test, not code)
- **Blocks:** None

---

## Task Breakdown

### TASK-190: Update hostname → EGG mappings and add tests

**Model:** haiku
**Objective:** Add `canvas.shiftcenter.com` mapping, verify all spec mappings, write 10 tests

**Deliverables:**
1. Update `hostnameMap` in `eggResolver.ts` to include `canvas.shiftcenter.com` → `canvas`
2. Verify all other mappings match spec (they already do)
3. Create test file with 10 test cases (see above)
4. All tests pass
5. No changes to error handling (already exists in `useEggInit`)

**Constraints:**
- TDD: tests first
- No hardcoded colors (N/A — logic only)
- No file over 500 lines (current file is 133 lines)
- No stubs

---

## Q33NR Notes

- Single task (small change + tests)
- Haiku model sufficient (spec says haiku)
- No UI changes required
- Error handling already exists
- Live smoke test blocked by DNS (w3-02), but logic tests sufficient for now
- Consider adding `localhost:3000` mapping if needed (already exists)

---

## Next Steps for Q33N

1. Write task file for TASK-190
2. Return to Q33NR for review
3. After approval, dispatch BEE (haiku)
4. Review BEE response
5. Report results to Q33NR

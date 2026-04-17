# TASK: Finish SPEC-BUGFIX-PALOOZA-001 (Phases 2-4) — simdecisions

**Role:** Q33N (Queen)
**Date:** 2026-04-10
**From:** Q33NR
**Model:** Sonnet (claude-sonnet-4-5-20250929)
**Target repo:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions`
**Do NOT touch:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter` (frozen-legacy)

---

## Read first (in order)

1. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\coordination\2026-04-10-BRIEFING-Q33N-PALOOZA-FINISH.md` — your detailed briefing
2. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\coordination\2026-04-10-PHASE1-TRIAGE-BUGFIX-PALOOZA.md` — Phase 1 diagnostic findings (source of truth)
3. `C:\Users\davee\Downloads\SPEC-BUGFIX-PALOOZA-001.md` — original spec (target IS simdecisions, not what its header says)

## Summary

Q33NR completed Phase 0 (stash + investigate) and Phase 1 (diagnostic survey). Handoff to you for Phases 2, 3, 4. All findings are in the triage report. Don't re-run Phase 1.

## Acceptance criteria

- [ ] Phase 2 complete: B1 (vite config serve-eggs path) + B2 (editable-install shadow) fixed. Backend imports. Build passes OR next-blocker documented.
- [ ] Phase 3 complete: `npm run dev` + backend `/health` both running green.
- [ ] Phase 4 complete: zero console errors on initial load (or each remaining error documented as deferred).
- [ ] Commits `fix(palooza): phase 2 complete`, `fix(palooza): phase 3 complete`, `fix(palooza): phase 4 complete` in that order.
- [ ] Response doc at `.deia/hive/responses/2026-04-10-RESPONSE-PALOOZA-PHASES-2-4.md` with the template from the briefing.
- [ ] Stash `stash@{0}` remains unpopped.

## Hard rules (from spec)

- CSS: `var(--sd-*)` only
- No file over 500 lines
- No stubs
- No algorithm changes
- Max 20-line fixes — document and defer otherwise
- Stay in simdecisions repo
- Commit message exact: `fix(palooza): phase N complete`

## When blocked

STOP. Write the blocker into the response doc and return. Do not invent solutions. Do not create a Phase 5. Do not pop the stash.

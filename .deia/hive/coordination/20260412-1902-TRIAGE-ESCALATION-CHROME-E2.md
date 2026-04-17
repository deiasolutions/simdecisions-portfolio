# TRIAGE ESCALATION: CHROME-E2

**Date:** 2026-04-12 19:02:40 UTC
**Reason:** 3 requeue attempts (max 3)
**Status:** NEEDS MANUAL REVIEW

## Summary

Spec `SPEC-CHROME-E2-save-derived-egg.md` has been requeued 3 times and failed each time.
Automated triage has moved it to `_escalated/` for manual review.

## Triage History

- 2026-04-09T15:50:45.746441Z — requeued (empty output)
- 2026-04-12T18:52:40.069858Z — requeued (empty output)
- 2026-04-12T18:57:40.120911Z — requeued (empty output)

## Next Steps

1. **Review spec file** in `queue/_escalated/SPEC-CHROME-E2-save-derived-egg.md`
2. **Diagnose root cause** — why is this spec failing repeatedly?
3. **Options:**
   - Fix spec and move back to backlog/
   - Archive spec if no longer needed
   - Break into smaller specs
   - Escalate to architect (Mr. AI) if systemic issue

## Original Spec

```markdown
## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# CHROME-E2: Save as Derived User EGG

## Objective
Implement save-as-derived-EGG. Serialize the current layout tree to .egg.md format. Store at home://eggs/{user-slug}/{eggId}.egg.md. Add derivedFrom lineage in frontmatter. On EGG load, check home volume for user-derived version before falling back to canonical.

## Build Type
**New build** — No shell tree serializer exists. No derived EGG concept exists. Serializer, SaveEggDialog, and eggLoader home volume check — all new.

## Problem Analysis
When the user saves from design mode, the shell serializes the layout tree into a new .egg.md. The derived EGG includes derivedFrom metadata pointing to the canonical source. On next load, the platform checks for a user-derived version and offers a choice: load canonical or user version. The canonical EGG on Global Commons is never overwritten.

## Files to Read First
- browser/src/eggs/types.ts
- browser/src/eggs/eggLoader.ts
- browser/src/shell/eggToShell.ts
- browser/src/shell/types.ts
- docs/specs/ADR-SC-CHROME-001-v3.md

## Files to Modify
- browser/src/shell/serializer.ts — NEW: serialize shell tree → .egg.md format
- browser/src/eggs/eggLoader.ts — check home volume for derived EGG on load
- browser/src/shell/components/SaveEggDialog.tsx — NEW: save confirmation UI
- browser/src/shell/__tests__/serializer.test.ts — NEW tests

## Deliverables
- [ ] Shell tree → .egg.md serializer (layout, ui, toolbar blocks)
- [ ] Derived EGG frontmatter includes derivedFrom field
- [ ] Save writes to home://eggs/{user-slug}/{eggId}.egg.md via named volume
- [ ] On load, eggLoader checks home volume for user-derived version
- [ ] Choice UI: load canonical or user version when derived exists

## Acceptance Criteria
- [ ] Serializer produces valid .egg.md that inflater can re-parse
- [ ] derivedFrom field present in saved frontmatter
- [ ] Round-trip: save → reload produces equivalent layout
- [ ] Canonical EGG never modified

## Test Requirements
- [ ] Tests written FIRST (TDD) — before implementation
- [ ] Test file: browser/src/shell/__tests__/serializer.test.ts
- [ ] Test: serializer produces valid .egg.md string
- [ ] Test: frontmatter includes derivedFrom
- [ ] Test: round-trip serialize → parse → inflate produces equivalent tree
- [ ] Test: split ratios preserved in serialization
- [ ] Test: seamless property preserved
- [ ] Test: toolbar block serialized correctly
- [ ] All tests pass
- [ ] Minimum 6 tests

## Smoke Test
- [ ] cd browser && npx vitest run src/shell/__tests__/serializer — tests pass
- [ ] cd browser && npx vitest run src/eggs — no regressions

## Constraints
- No file over 500 lines
- No stubs
- Never overwrite canonical EGG

## Depends On
- SPEC-CHROME-E1 (design mode toggle provides the save trigger)

## Model Assignment
sonnet

## Priority
P2

## Triage History
- 2026-04-09T15:50:45.746441Z — requeued (empty output)
- 2026-04-12T18:52:40.069858Z — requeued (empty output)
- 2026-04-12T18:57:40.120911Z — requeued (empty output)

```

---

**Automated escalation by triage daemon**

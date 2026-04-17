# TRIAGE ESCALATION: WIKI-108

**Date:** 2026-04-10 05:51:50 UTC
**Reason:** 3 requeue attempts (max 3)
**Status:** NEEDS MANUAL REVIEW

## Summary

Spec `SPEC-WIKI-108-egg-integration.md` has been requeued 3 times and failed each time.
Automated triage has moved it to `_escalated/` for manual review.

## Triage History

- 2026-04-10T05:44:29.023460Z — requeued (empty output)
- 2026-04-10T05:46:50.089919Z — requeued (empty output)
- 2026-04-10T05:49:29.047250Z — requeued (empty output)

## Next Steps

1. **Review spec file** in `queue/_escalated/SPEC-WIKI-108-egg-integration.md`
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

---
id: WIKI-108
priority: P2
model: sonnet
role: bee
depends_on:
  - WIKI-107
---
# SPEC-WIKI-108: Wiki EGG Definition and E2E Test

## Priority
P2

## Model Assignment
sonnet

## Depends On
- WIKI-107

## Intent
Create wiki.egg.md file defining the wiki as a standalone EGG. Write end-to-end smoke test that verifies the full flow: create pages via API, navigate via UI, follow wikilinks, view backlinks.

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/eggs/efemera.egg.md` — reference EGG
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_stage/SPEC-KB-EGG-001-kb-shiftcenter-knowledge-base.md` — KB EGG spec (similar use case)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/e2e/hodeia-auth.spec.ts` — reference E2E test

## Acceptance Criteria
- [ ] File created: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/eggs/wiki.egg.md`
- [ ] EGG definition includes:
  - Metadata (egg: wiki, version: 1.0.0, displayName: Wiki)
  - Layout: tree-browser + wiki primitive
  - Config for tree adapter (wiki pages source)
- [ ] File created: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/e2e/wiki.spec.ts`
- [ ] E2E test covers:
  - Start hivenode server
  - Create test pages via API (with wikilinks)
  - Load wiki EGG in browser
  - Verify tree shows pages
  - Click page in tree, verify content renders
  - Click wikilink, verify navigation
  - Verify backlinks panel shows correct pages
  - Clean up test pages
- [ ] Test passes on clean database
- [ ] No file over 500 lines

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Use Playwright for E2E tests
- EGG should be loadable via URL: http://localhost:5173/?egg=wiki
- Test should be idempotent (can run multiple times)
- TDD: tests first (write E2E test before EGG file if needed to clarify requirements)
- No stubs
- No git operations

## Smoke Test
```bash
# Run E2E test
cd browser && npx playwright test wiki.spec.ts
```

Expected: Test passes, full wiki flow verified.

## Triage History
- 2026-04-10T05:44:29.023460Z — requeued (empty output)
- 2026-04-10T05:46:50.089919Z — requeued (empty output)
- 2026-04-10T05:49:29.047250Z — requeued (empty output)

```

---

**Automated escalation by triage daemon**

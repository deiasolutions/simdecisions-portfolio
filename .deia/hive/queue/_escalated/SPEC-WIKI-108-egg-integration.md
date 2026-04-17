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
- `browser/sets/efemera.egg.md` — reference EGG
- `browser/e2e/hodeia-auth.spec.ts` — reference E2E test

## Acceptance Criteria
- [ ] File created: `browser/sets/wiki.egg.md`
- [ ] EGG definition includes:
  - Metadata (egg: wiki, version: 1.0.0, displayName: Wiki)
  - Layout: tree-browser + wiki primitive
  - Config for tree adapter (wiki pages source)
- [ ] File created: `browser/e2e/wiki.spec.ts`
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
- 2026-04-12T18:52:40.106922Z — requeued (empty output)
- 2026-04-12T18:57:40.172674Z — requeued (empty output)
- 2026-04-12T19:02:40.260384Z — requeued (empty output)

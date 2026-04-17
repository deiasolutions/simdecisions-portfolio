---
id: REFACTOR-034
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-033
---
# SPEC-REFACTOR-034: Remove Dead Code

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-033

## Intent
Remove code that is UNDOCUMENTED (no spec), unused (no imports, no routes, no references), and has no test coverage. Every removal must be logged with justification.

## Files to Read First
- `.deia/hive/refactor/FEATURE-MANIFEST.json` — check UNDOCUMENTED items
- `.deia/hive/refactor/diff-report.json` — cross-reference

## Acceptance Criteria
- [ ] Every UNDOCUMENTED feature evaluated: is it referenced anywhere? imported? tested?
- [ ] Dead code removed ONLY if: no imports, no references, no tests, no spec
- [ ] File created: `.deia/hive/refactor/dead-code-removals.json` — every removal with:
  - `file_path`, `what_was_removed`, `justification`, `references_checked`
- [ ] TypeScript compiles: `npx tsc --noEmit`
- [ ] Python imports clean: no import errors on startup
- [ ] Nothing user-facing was removed

## Constraints
- You are in EXECUTE mode. Make the changes. Do NOT enter plan mode.
- CONSERVATIVE — when in doubt, keep it. Better to keep dead code than break live features.
- Every removal logged with justification
- Commit changes to `refactor/auto-2026-04-07` branch

---
id: REFACTOR-041
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-040
---
# SPEC-REFACTOR-041: Finish PARTIAL Features from Manifest

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-040

## Intent
Take every feature marked PARTIAL in FEATURE-MANIFEST.json and complete it. If completion is trivial (< 100 lines), do it. If complex, create a stub that prevents crashes and log what's needed.

## Files to Read First
- `.deia/hive/refactor/FEATURE-MANIFEST.json` — filter for status=PARTIAL
- `.deia/hive/refactor/diff-report.json` — gap descriptions

## Acceptance Criteria
- [ ] Every PARTIAL feature evaluated
- [ ] Trivial completions done (< 100 lines of new code each)
- [ ] Complex completions: graceful fallback added (no crashes), logged for future work
- [ ] File created: `.deia/hive/refactor/changes-041.json` — what was completed, what was deferred

## Constraints
- You are in EXECUTE mode. Do the work. Do NOT enter plan mode.
- Don't spend more than ~30 minutes on any single PARTIAL feature
- If it's complex, add a graceful fallback and move on
- Commit changes to `refactor/auto-2026-04-07` branch

---
id: REFACTOR-042
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-041
---
# SPEC-REFACTOR-042: Implement MISSING Features from Specs

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-041

## Intent
Take features marked MISSING in FEATURE-MANIFEST.json (specced but not built). For critical user-facing features, implement them. For non-critical features, log them as intentionally deferred.

## Files to Read First
- `.deia/hive/refactor/FEATURE-MANIFEST.json` — filter for status=MISSING
- `.deia/hive/refactor/diff-report.json` — what specs define these features

## Acceptance Criteria
- [ ] Every MISSING feature evaluated and categorized: implement now vs defer
- [ ] Critical MISSING features implemented (routes respond, components render)
- [ ] Non-critical MISSING features logged with deferral justification
- [ ] File created: `.deia/hive/refactor/changes-042.json`

## Constraints
- You are in EXECUTE mode. Do the work. Do NOT enter plan mode.
- Focus on user-facing features first
- Don't implement features that depend on unbuilt infrastructure (e.g., event ledger consumers)
- Commit changes to `refactor/auto-2026-04-07` branch

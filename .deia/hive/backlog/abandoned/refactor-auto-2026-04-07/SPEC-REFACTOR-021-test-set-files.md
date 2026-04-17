---
id: REFACTOR-021
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-013
---
# SPEC-REFACTOR-021: Test Every .set.md — Do They Load? Do They Render?

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-013

## Intent
Test every `.set.md` file in `eggs/`. For each, determine: is it valid YAML/frontmatter? Does the EGG resolver recognize it? Do the primitives it references exist? Can the shell render it?

## Files to Read First
- `eggs/*.set.md` — all 24 set files
- `browser/src/services/shell/eggResolver.ts` — how eggs are resolved
- `browser/src/shell/` — shell rendering pipeline
- `docs/specs/SPEC-EGG-FORMAT-v0.3.1.md` — format spec

## Acceptance Criteria
- [ ] For each `.set.md` file, record:
  - File name and path
  - Valid format? (frontmatter parses correctly)
  - All referenced primitives exist in codebase?
  - Missing primitives listed
  - Loadable? (would the shell render it without errors)
- [ ] File created: `.deia/hive/refactor/test-results-sets.json`
- [ ] Summary: X sets tested, Y valid, Z have missing primitives

## Constraints
- You are in EXECUTE mode. Do the analysis and write results. Do NOT enter plan mode.
- Read-only — no code changes
- No git operations

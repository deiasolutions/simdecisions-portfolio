---
id: REFACTOR-012
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-010
  - REFACTOR-011
---
# SPEC-REFACTOR-012: Diff Implemented vs Specced

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-010
- REFACTOR-011

## Intent
Cross-reference the codebase inventory (REFACTOR-010) with the spec inventory (REFACTOR-011). For every feature, determine: COMPLETE (specced + fully built), PARTIAL (specced + partially built), MISSING (specced + not built), UNDOCUMENTED (built + no spec).

## Files to Read First
- `.deia/hive/refactor/inventory-routes.json`
- `.deia/hive/refactor/inventory-components.json`
- `.deia/hive/refactor/inventory-events.json`
- `.deia/hive/refactor/inventory-configs.json`
- `.deia/hive/refactor/inventory-tables.json`
- `.deia/hive/refactor/inventory-specs.json`

## Acceptance Criteria
- [ ] File created: `.deia/hive/refactor/diff-report.json` with every feature tagged:
  - `status`: COMPLETE | PARTIAL | MISSING | UNDOCUMENTED
  - `spec_id` (if specced)
  - `code_paths` (if implemented)
  - `gap_description` (if PARTIAL or MISSING — what's missing)
- [ ] Summary stats: count of COMPLETE, PARTIAL, MISSING, UNDOCUMENTED

## Constraints
- You are in EXECUTE mode. Write all output files. Do NOT enter plan mode. Do NOT ask for approval.
- Read-only — no code changes
- No git operations

---
id: REFACTOR-033
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-032
---
# SPEC-REFACTOR-033: Dedupe and Consolidate Scattered Utilities

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-032

## Intent
Find and consolidate duplicate utility functions, repeated patterns, and scattered helper modules. Common targets: date formatting, API helpers, bus event utilities, storage wrappers.

## Files to Read First
- `browser/src/` — search for duplicate function signatures
- `hivenode/` — search for repeated utility patterns
- `.deia/hive/refactor/FEATURE-MANIFEST.json` — feature map

## Acceptance Criteria
- [ ] Identified all duplicate/near-duplicate utility functions
- [ ] Consolidated into canonical locations (e.g., `browser/src/utils/`, `hivenode/utils/`)
- [ ] All imports updated
- [ ] TypeScript compiles: `npx tsc --noEmit`
- [ ] File created: `.deia/hive/refactor/changes-033.json` — what was consolidated

## Constraints
- You are in EXECUTE mode. Make the changes. Do NOT enter plan mode.
- Only consolidate genuinely duplicated code — don't over-abstract
- If a utility is used in only one place, leave it there
- Commit changes to `refactor/auto-2026-04-07` branch

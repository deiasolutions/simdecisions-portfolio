---
id: REFACTOR-013
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-012
---
# SPEC-REFACTOR-013: Generate FEATURE-MANIFEST.json — Retention Baseline

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-012

## Intent
Consolidate all inventory data into a single FEATURE-MANIFEST.json that serves as the retention baseline. This is the document the gate check (REFACTOR-060) will compare against. Every feature in this manifest MUST be accounted for after refactor — either retained or explicitly dropped with justification.

## Files to Read First
- `.deia/hive/refactor/diff-report.json`
- `.deia/hive/refactor/inventory-*.json` (all inventory files)

## Acceptance Criteria
- [ ] File created: `.deia/hive/refactor/FEATURE-MANIFEST.json` with:
  - `generated_at` timestamp
  - `total_features` count
  - `features` array, each with: `id`, `name`, `type` (route/component/table/event/config/tool), `status` (COMPLETE/PARTIAL/MISSING/UNDOCUMENTED), `code_paths`, `spec_id`, `critical` (boolean — is this user-facing?)
- [ ] File created: `.deia/hive/refactor/FEATURE-MANIFEST-SUMMARY.md` — human-readable summary with counts per status, per type
- [ ] Manifest is the SINGLE SOURCE OF TRUTH for retention gate

## Constraints
- You are in EXECUTE mode. Write all output files. Do NOT enter plan mode. Do NOT ask for approval.
- Read-only — no code changes
- No git operations

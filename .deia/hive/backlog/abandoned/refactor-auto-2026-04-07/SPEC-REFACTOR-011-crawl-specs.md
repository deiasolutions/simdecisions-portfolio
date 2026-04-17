---
id: REFACTOR-011
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-010
---
# SPEC-REFACTOR-011: Crawl Specs — Catalog All 304 Specs Across Known Locations

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-010

## Intent
Catalog every spec file across all known locations. For each spec, extract: ID, title, status, what it specifies (which routes/components/features), and whether it has been implemented.

## Files to Read First
- `docs/specs/` — reference specs
- `.deia/hive/queue/_done/` — completed queue specs
- `.deia/hive/queue/_stage/` — staged specs
- `.deia/hive/queue/backlog/` — queued specs
- `.deia/hive/queue/_needs_review/` — failed/stalled specs

## Acceptance Criteria
- [ ] File created: `.deia/hive/refactor/inventory-specs.json` with every spec:
  - `id`, `title`, `location`, `status` (done/staged/backlog/needs_review/reference)
  - `specifies` — list of features/routes/components this spec defines
  - `file_path`
- [ ] Total spec count matches or exceeds 200 (known minimum)
- [ ] Specs grouped by project/domain (factory, wiki, mobile-workdesk, efemera, etc.)

## Constraints
- You are in EXECUTE mode. Write all output files. Do NOT enter plan mode. Do NOT ask for approval.
- Read-only — no code changes
- No git operations

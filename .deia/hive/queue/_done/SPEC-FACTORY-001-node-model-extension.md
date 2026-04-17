---
id: FACTORY-001
priority: P0
model: sonnet
role: bee
depends_on: []
---
# SPEC-FACTORY-001: Node Model Extension

## Priority
P0

## Model Assignment
sonnet

## Depends On
(none)

## Intent
Extend the Node/spec data model with all fields defined in PRISM-IR v1.1 Section 1.1. This is the foundation — every other FACTORY task depends on these fields existing.

## Files to Read First
- `.deia/hive/backlog/PRISM-IR-FACTORY-DUAL-LOOP-v1.1.prism.md` — Sections 1.1, 1.2, 1.5
- `.deia/hive/scripts/queue/spec_parser.py` — current SpecFile dataclass
- `.deia/hive/queue/backlog/` — existing spec files for backward compat reference
- `hivenode/scheduler/scheduler_daemon.py` — how scheduler reads specs

## Acceptance Criteria
- [ ] SpecFile dataclass (or new NodeSpec dataclass) extended with:
  - `node_type`: ORIGINAL | SHARED_REF (default: ORIGINAL)
  - `target_id`: string | None (for SHARED_REF nodes)
  - `depends_on`: list[string] (non-parent dependencies, default: [])
  - `acceptance_criteria`: dict (typed per content_type, default: {})
  - `building_started_at`: timestamp | None
  - `estimated_tokens`: int | None
  - `phase`: enum IDEA | SPECCING | SPECCED | BUILDING | BUILT | INTEGRATED | FAILED (default: SPECCED)
  - `status`: enum PENDING | IN_PROGRESS | SUCCEEDED | FAILED | BLOCKED (default: PENDING)
  - `failure_reason`: string | None
  - `split_reason`: string | None
  - `parent_id`: string | None
  - `root_id`: string | None
  - `branch_path`: list[string] (default: [])
  - `output_type`: PLAN | PRODUCT (default: PRODUCT)
  - `content_type`: string | None
- [ ] Manifest v2 format implemented per Section 10.1 of PRISM-IR spec
  - JSON schema with version, updated_at, entries[]
  - Each entry has all extended fields
  - `write_manifest(entries, path)` and `read_manifest(path)` functions
- [ ] Existing specs parse cleanly — new fields get sensible defaults
- [ ] YAML frontmatter parser reads new fields when present
- [ ] Tests: parse old-format spec, parse new-format spec, round-trip manifest

## Constraints
- Backward compatible: old specs without new fields must still parse
- No file over 500 lines
- TDD: tests first
- Do NOT modify scheduler logic — just the data model

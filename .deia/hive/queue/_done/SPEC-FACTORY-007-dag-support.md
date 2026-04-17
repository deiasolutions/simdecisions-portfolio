---
id: FACTORY-007
priority: P2
model: sonnet
role: bee
depends_on:
  - FACTORY-001
  - FACTORY-002
---
# SPEC-FACTORY-007: DAG Support (Shared Modules)

## Priority
P2

## Model Assignment
sonnet

## Depends On
- FACTORY-001
- FACTORY-002

## Intent
Enable shared module extraction and SHARED_REF nodes so the tree can become a DAG when multiple specs depend on the same module.

## Files to Read First
- `.deia/hive/backlog/PRISM-IR-FACTORY-DUAL-LOOP-v1.1.prism.md` — Section 6 (DAG Support)
- `.deia/hive/scripts/queue/spec_parser.py` — SpecFile with node_type, target_id (from FACTORY-001)
- `hivenode/scheduler/scheduler_daemon.py` — tree traversal logic

## Acceptance Criteria
- [ ] SHARED_REF node type implemented:
  - `node_type: SHARED_REF` with `target_id` pointing to an ORIGINAL node
  - SHARED_REF inherits phase from target (when target BUILT, ref is BUILT)
  - SHARED_REF does not have its own acceptance_criteria (inherits from target)
- [ ] `find_dangling_refs()` query: finds SHARED_REF nodes with invalid target_id
- [ ] `resolve_shared_refs(manifest)` function: given a manifest, replaces SHARED_REF phase with target's phase
- [ ] Tree queries handle DAG traversal without infinite loops (visited set)
- [ ] Manual trigger only for now: human creates SHARED_REF in spec frontmatter
- [ ] Tests: create SHARED_REF, target completes and ref mirrors phase, dangling ref detected, no infinite loop on DAG traversal

## Constraints
- Automated similarity detection is OUT OF SCOPE — manual annotation only
- SHARED_REF specs are lightweight (just frontmatter + short description)
- DAG traversal must use a visited set to prevent cycles
- No file over 500 lines
- TDD: tests first

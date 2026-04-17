---
id: FACTORY-008
priority: P2
model: sonnet
role: bee
depends_on:
  - FACTORY-001
  - FACTORY-002
  - FACTORY-007
---
# SPEC-FACTORY-008: Orphan and Integrity Detection

## Priority
P2

## Model Assignment
sonnet

## Depends On
- FACTORY-001
- FACTORY-002
- FACTORY-007

## Intent
Implement health-check queries for tree/DAG integrity. These queries detect orphaned nodes, stalled builds, circular dependencies, dangling refs, and incomplete subtrees.

## Files to Read First
- `.deia/hive/backlog/PRISM-IR-FACTORY-DUAL-LOOP-v1.1.prism.md` — Section 9 (Orphan Detection)
- `hivenode/scheduler/scheduler_daemon.py` — where periodic checks would run
- `.deia/hive/queue/` — directory structure for all spec states
- `.deia/hive/scripts/queue/spec_parser.py` — manifest reading (from FACTORY-001)

## Acceptance Criteria
- [ ] All integrity queries implemented and callable:
  - `find_incomplete_subtrees(root_id)`: all descendants not BUILT/INTEGRATED
  - `find_stalled_nodes()`: BUILDING longer than TTL (uses FACTORY-003 logic)
  - `find_blocked_nodes()`: status=BLOCKED with unmet depends_on
  - `find_orphaned_nodes()`: parent INTEGRATED but node not BUILT
  - `find_dangling_refs()`: SHARED_REF with invalid target_id (uses FACTORY-007)
  - `find_circular_deps(specs)`: cycle detection in depends_on graph
- [ ] CLI interface: `python -m hivenode.scheduler.integrity_check [--query NAME]`
- [ ] Circular dep detection runs at spec parse time AND as periodic query
- [ ] Results formatted as markdown report
- [ ] Tests: each query returns correct results for known test fixtures

## Constraints
- Queries read from manifest.json and/or spec files — no separate database
- Cycle detection uses DFS with coloring (white/gray/black)
- Output format: markdown table with spec_id, issue_type, detail
- No file over 500 lines
- TDD: tests first

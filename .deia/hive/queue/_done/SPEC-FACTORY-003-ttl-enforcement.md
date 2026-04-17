---
id: FACTORY-003
priority: P1
model: sonnet
role: bee
depends_on:
  - FACTORY-001
---
# SPEC-FACTORY-003: TTL Enforcement

## Priority
P1

## Model Assignment
sonnet

## Depends On
- FACTORY-001

## Intent
Detect and handle stalled BUILDING nodes. If a spec has been in `_active/` longer than the configured TTL, mark it FAILED and trigger retry/split/escalate logic.

## Files to Read First
- `.deia/hive/backlog/PRISM-IR-FACTORY-DUAL-LOOP-v1.1.prism.md` — Section 4.2 (TTL Enforcement)
- `hivenode/scheduler/scheduler_daemon.py` — existing heartbeat/stale detection
- `.deia/hive/queue/_active/` — where in-flight specs live
- `.deia/hive/queue/monitor-state.json` — current monitoring state

## Acceptance Criteria
- [ ] `building_ttl_seconds` config value added (default: 600 seconds)
  - Configurable via environment variable `FACTORY_BUILDING_TTL`
- [ ] `building_started_at` timestamp set when spec moves to `_active/`
- [ ] Periodic scan (every 60s) finds specs where `now() - building_started_at > TTL`
- [ ] Stale specs marked with `failure_reason: "TTL exceeded: presumed stalled"`
- [ ] Stale specs moved to `_needs_review/` (existing escalation path)
- [ ] Stale detection fires within 120s of TTL expiry (next scan cycle)
- [ ] Tests: spec exceeds TTL and gets flagged, spec completes before TTL is fine, config override works

## Constraints
- Use existing `_needs_review/` directory for failed specs
- TTL check is non-blocking — runs as part of scheduler's periodic cycle
- No file over 500 lines
- TDD: tests first

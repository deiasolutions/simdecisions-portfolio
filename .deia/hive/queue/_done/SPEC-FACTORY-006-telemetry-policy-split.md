---
id: FACTORY-006
priority: P1
model: sonnet
role: bee
depends_on:
  - FACTORY-001
  - FACTORY-004
---
# SPEC-FACTORY-006: Telemetry and Policy Separation

## Priority
P1

## Model Assignment
sonnet

## Depends On
- FACTORY-001
- FACTORY-004

## Intent
Split learning into observation (telemetry) vs. policy change (recommendations). Every build attempt logs to the Event Ledger. A separate process generates policy recommendations that require human approval.

## Files to Read First
- `.deia/hive/backlog/PRISM-IR-FACTORY-DUAL-LOOP-v1.1.prism.md` — Section 7.2 (outcome_learning)
- `hivenode/ledger/schema.py` — existing event ledger
- `hivenode/hive_mcp/tools/telemetry.py` — existing telemetry
- `hivenode/scheduler/scheduler_daemon.py` — where build results are processed

## Acceptance Criteria
- [ ] Every build attempt logs to Event Ledger (telemetry_log):
  - spec_id, operator_id (model), vendor_id
  - success/failure, duration_seconds, tokens_in, tokens_out
  - acceptance_criteria results (which checks passed/failed)
  - failure_reason, split_decision (if applicable)
  - cost (COIN)
- [ ] Telemetry logged for every attempt — no exceptions, including TTL failures
- [ ] `generate_policy_recommendations(telemetry_entries)` function:
  - Analyzes patterns from 10+ attempts per operator/scope combo
  - Produces recommendations like "Operator X succeeds 90% on python_file < 500 lines"
  - Recommendations are text strings with supporting data
- [ ] Policy recommendations written to `.deia/hive/coordination/policy-recommendations.md`
- [ ] Recommendations are NOT auto-applied — require human review
- [ ] Tests: telemetry logged on success, telemetry logged on failure, recommendations generated from mock data

## Constraints
- Telemetry is append-only observation — never mutates routing or scheduling
- Policy recommendations are advisory — the REQUIRE_HUMAN gate means no automated policy changes
- Use existing Event Ledger schema where possible, extend if needed
- No file over 500 lines
- TDD: tests first

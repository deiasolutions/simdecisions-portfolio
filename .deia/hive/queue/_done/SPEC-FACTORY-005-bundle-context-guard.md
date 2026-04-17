---
id: FACTORY-005
priority: P1
model: sonnet
role: bee
depends_on:
  - FACTORY-001
  - FACTORY-004
---
# SPEC-FACTORY-005: Bundle Formation with Context Window Guard

## Priority
P1

## Model Assignment
sonnet

## Depends On
- FACTORY-001
- FACTORY-004

## Intent
Scheduler forms bundles of related specs for efficient dispatch, with a hard guard that no bundle exceeds the target operator's context window.

## Files to Read First
- `.deia/hive/backlog/PRISM-IR-FACTORY-DUAL-LOOP-v1.1.prism.md` — Sections 1.3, 5.1, 5.2
- `hivenode/scheduler/scheduler_daemon.py` — where scheduling decisions happen
- `hivenode/rate_loader/model_rates.yml` — model context window sizes
- `hivenode/llm/router.py` — model capabilities

## Acceptance Criteria
- [ ] `estimate_tokens(spec)` function: estimates input tokens for a spec (content + prompt template)
- [ ] `max_bundle_tokens` config value added
- [ ] `token_buffer_ratio` config value added (default: 0.8)
- [ ] Scheduler groups ready specs into bundles based on:
  - Granularity fit (semantically related specs)
  - Operator fit (model's batch_preference)
  - Vendor fit (cost optimization)
- [ ] Context window guard: `sum(estimated_tokens) <= operator.max_context_tokens * token_buffer_ratio`
- [ ] If bundle exceeds context window: reduce bundle size or dispatch individually
- [ ] Bundle success → all specs in bundle marked BUILT
- [ ] Bundle failure → unbundle, retry each spec individually
- [ ] Bundle metadata logged: bundle_id, spec_ids, bundle_reason, estimated_tokens
- [ ] Tests: bundle fits context window, bundle exceeds and gets reduced, bundle fails and unbundles

## Constraints
- Token estimation can be approximate (character count / 4 is acceptable initial heuristic)
- Bundle is a dispatch-time grouping, NOT a tree node
- Bundles do not persist to disk — they exist only during the dispatch cycle
- No file over 500 lines
- TDD: tests first

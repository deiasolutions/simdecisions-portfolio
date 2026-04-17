# SPEC-DES-BATCH-001: Implement batch and separate node executors

## Priority
P2

## Depends On
SPEC-DES-RESOURCE-BINDING-001

## Model Assignment
sonnet

## Objective

Implement `batch` and `separate` node executors in the DES engine. Batch nodes collect N tokens into a combined batch token (triggered by size, timeout, or condition). Separate nodes split a batch token back into individual tokens. The node types exist in the PRISM-IR schema but have no executors — tokens hitting these nodes get default 1s duration with no batch behavior. This enables bulk API calls, human batch review, database bulk inserts, and report aggregation patterns.

## Files to Read First

- simdecisions/des/core.py
- simdecisions/des/tokens.py
- simdecisions/des/statistics.py
- simdecisions/des/trace_writer.py
- simdecisions/phase_ir/node_types.py
- simdecisions/des/edges.py
- tests/simdecisions/des/test_des_engine.py

## Acceptance Criteria

- [ ] `t: batch` nodes collect arriving tokens into a BatchBuffer until a trigger fires
- [ ] Size trigger: batch fires when `batch.size` tokens collected
- [ ] Timeout trigger: batch fires after `batch.timeout` sim-time seconds since first token arrival
- [ ] Combined size+timeout: whichever trigger fires first
- [ ] Combined batch token created with `entity.items` containing collected token entities and `properties.is_batch=True`
- [ ] Tokens waiting in buffer have state `waiting_batch`
- [ ] Timeout implemented via `batch_timeout` scheduled event on first arrival
- [ ] `t: separate` nodes split batch token's `entity.items` back into individual tokens
- [ ] Each separated token has `properties.from_batch` set to batch token ID
- [ ] Batch token completed after separate (when `preserve_batch=false`, the default)
- [ ] Trace events emitted: `batch_token_added`, `batch_fired` (with trigger type), `batch_separated`
- [ ] `StatisticsCollector` tracks per-batch-node: `batches_fired`, `avg_batch_size`, `avg_wait_time`, `timeout_fires`
- [ ] Round-trip test: batch(size=10) → task → separate produces same token count as input
- [ ] Existing 888+ DES tests still pass (`python -m pytest tests/simdecisions/des/ -v`)
- [ ] New tests cover: size trigger, timeout trigger, combined trigger, separate fan-out, round-trip batch→process→separate

## Smoke Test

- [ ] `python -m pytest tests/simdecisions/des/ -v` — all pass, 0 failures
- [ ] A flow with `batch(size=5)` receiving 12 tokens produces 2 batch tokens (5+5) with 2 tokens remaining in buffer

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- BatchBuffer is per-node — each batch node has its own independent buffer
- Timeout fires based on sim_time, not wall time
- Token state `waiting_batch` already exists in tokens.py — use it
- Test cases should NOT assert on resource acquire/release or operator cost behavior
- Remove `o: {op: http}` from test flows — batch/separate mechanics are independent of operator typing

## Files to Modify

- simdecisions/des/core.py
- simdecisions/des/tokens.py
- simdecisions/des/statistics.py
- simdecisions/des/trace_writer.py
- tests/simdecisions/des/test_des_batch.py

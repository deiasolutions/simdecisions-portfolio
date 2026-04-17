---
id: RATELIMIT-001
priority: P0
model: sonnet
depends_on: none
area_code: factory
---

# SPEC-RATELIMIT-001: Rate Limit Detection, Throttle, and 12-Bee Cap

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Add rate limit detection to the Claude and Gemini adapters, propagate rate-limit status through the dispatch pipeline, and implement throttling in the queue runner. Hard-cap max concurrent bees at 12. During the SWE-bench run (Apr 13-14), 522 of 731 tasks returned rate-limit errors that were incorrectly marked `Success: True`. The adapter never checked the response body. The queue runner never paused. This spec fixes both.

## Background Data

- SWE-bench ran 204 real tasks in 3.05 hours at median 12 concurrent bees before hitting rate limit
- Rate-limited responses look like: `"You've hit your limit · resets 2am (America/Chicago)"` with duration ~4s, cost $0.00, 0 files modified
- Anthropic window appears to be ~5 hours. At median 12 bees we consumed the budget in ~3 hours (15-20% too fast)
- Max concurrent bees observed: 18. New hard cap: **12**

## Files to Read First

- `hivenode/adapters/cli/claude_cli_subprocess.py`
  Lines 763-786: `_check_success()` — this is where rate limit detection goes
- `hivenode/adapters/cli/claude_code_cli_adapter.py`
  Lines 209-279: `send_task()` — propagate rate_limited flag here
- `hivenode/adapters/cli/gemini_adapter.py`
  Lines 275-359: `send_task()` — add Gemini-specific rate limit detection
- `.deia/hive/scripts/dispatch/dispatch.py`
  Lines 643-821: `dispatch_bee()` — handle rate limit response, return special status
- `.deia/hive/scripts/queue/run_queue.py`
  Main queue loop — add throttle/pause logic
- `.deia/hive/scripts/queue/queue_pool.py`
  Slot management — enforce 12-bee cap, add cooldown state

## Deliverables

### Part 1: Detection (adapter layer)

- [ ] In `claude_cli_subprocess.py:_check_success()`, detect rate limit patterns in output text:
  - `"You've hit your limit"`
  - `"rate limit"` (case-insensitive)
  - `"too many requests"` (case-insensitive)
  - `"resets"` followed by a time expression
- [ ] When detected, set `ProcessResult.success = False` and add `ProcessResult.rate_limited = True`
- [ ] Parse the reset time from the message (e.g. `"resets 2am (America/Chicago)"`) into a UTC datetime. Store in `ProcessResult.rate_limit_reset_utc`
- [ ] In `claude_code_cli_adapter.py:send_task()`, propagate `rate_limited` and `rate_limit_reset_utc` fields in the returned dict
- [ ] In `gemini_adapter.py:send_task()`, catch `google.api_core.exceptions.ResourceExhausted` (or equivalent) and set the same `rate_limited=True` fields. Parse retry-after header if available.
- [ ] Rate-limited RAW files must show `# Success: False` and `# Rate Limited: True`

### Part 2: Propagation (dispatch layer)

- [ ] In `dispatch.py:dispatch_bee()`, check result dict for `rate_limited=True`
- [ ] When rate-limited, return a dict with `{"status": "rate_limited", "reset_utc": "<iso timestamp>"}` instead of the normal response path
- [ ] Do NOT move the spec to `_done/` when rate-limited — leave it in place for retry
- [ ] Log: `[DISPATCH] RATE LIMITED — reset at <time CDT>`

### Part 3: Throttling (queue runner layer)

- [ ] Add `max_concurrent_bees = 12` as a constant in `run_queue.py` (or `queue_pool.py` slot config)
- [ ] Never dispatch more than 12 bees simultaneously, regardless of available specs
- [ ] When any bee returns `rate_limited`, immediately:
  1. Stop dispatching new bees
  2. Let active bees finish naturally (do NOT kill them)
  3. Log: `[QUEUE] RATE LIMITED — pausing until <reset_time CDT>`
  4. Sleep until `rate_limit_reset_utc` (or minimum 30 minutes if no reset time parsed)
  5. Resume dispatching after cooldown
- [ ] Specs that were rate-limited stay in their current queue position for automatic retry on resume
- [ ] Add a `queue_state.json` field `"rate_limit_until": "<iso timestamp>"` so the state is crash-recoverable

### Part 4: Proactive throttle (optional but preferred)

- [ ] Track rolling 60-minute token consumption from bee results (sum of `cost_usd` field)
- [ ] If rolling cost exceeds $400/hour, reduce concurrent bee cap to 8 until cost drops below $300/hour
- [ ] Log: `[QUEUE] COST THROTTLE — reducing max bees to 8 ($X/hr)`

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] Unit test: `_check_success()` correctly identifies rate limit messages, returns `rate_limited=True`
- [ ] Unit test: `_check_success()` parses reset time from various formats (`"resets 2am"`, `"resets 2:00 AM"`, `"try again in 30 minutes"`)
- [ ] Unit test: normal success output is NOT flagged as rate-limited
- [ ] Unit test: adapter `send_task()` propagates rate_limited fields
- [ ] Unit test: dispatch returns rate_limited status and does NOT move spec to _done
- [ ] Integration test: queue runner pauses when rate_limited response received
- [ ] Integration test: queue runner resumes after cooldown
- [ ] Integration test: max 12 concurrent bees enforced
- [ ] All existing tests still pass

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- CSS: var(--sd-*) only if touching any CSS
- The 12-bee cap is a HARD DECISION, not configurable. Hardcode it. If we need to change it later we'll change the constant.
- Do NOT add CLI flags for max-bees. This is an internal safety limit.

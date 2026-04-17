# Q33N Coordination Report: Fix CLI Token & Cost Tracking

**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Queen Regent)
**Date:** 2026-03-16
**Briefing:** 2026-03-16-BRIEFING-fix-cli-token-cost-tracking
**Status:** Task files ready for review

---

## Summary

I have read the briefing and created one task file for a Sonnet bee to fix the CLI token and cost tracking issue in `claude_cli_subprocess.py`.

## Task Files Created

### TASK-184: Fix CLI Token & Cost Tracking
**File:** `.deia/hive/tasks/2026-03-16-TASK-184-fix-cli-token-cost-tracking.md`
**Model:** Sonnet
**Estimate:** Medium complexity

**Objective:** Fix `claude_cli_subprocess.py` to capture token usage from Claude Code's JSON output, calculate cost using model-specific rate cards, and populate telemetry for the build monitor.

**Key deliverables:**
1. **Investigation phase** — Run real Claude Code dispatch with `--output-format json` and document actual JSON structure
2. **Implementation** — Extract tokens, add rate card (matching `anthropic.py`), calculate cost and carbon
3. **Tests** — 8+ tests covering rate cards for each model, graceful fallback, carbon calculation

**Files modified:**
- `hivenode/adapters/cli/claude_cli_subprocess.py` (fix JSON parsing, add rate card, add cost/carbon calculation)
- `tests/hivenode/adapters/cli/test_claude_cli_token_tracking.py` (new test file, 8+ tests)

**Constraints enforced:**
- No hardcoded model — uses `self.model`
- Rate card matches `anthropic.py` pattern exactly
- Graceful fallback if Claude Code doesn't return tokens
- TDD approach (tests first)
- File size check (currently ~500 lines, may need modularization)

---

## Analysis

### What I Read

1. **Briefing** — Identified root cause at lines 347-363 where JSON parsing tries to extract `cost_usd`, `total_cost_usd` but Claude Code may return different keys
2. **claude_cli_subprocess.py** — Reviewed JSON parsing logic, confirmed `self.model` is available for rate card lookup
3. **anthropic.py** — Documented PRICING dict structure and `estimate_cost()` pattern
4. **base.py** — Documented `estimate_carbon()` pattern (5g CO2 per 1000 tokens)
5. **dispatch.py** — Confirmed how `usage` dict flows from adapter to telemetry heartbeat

### Root Cause

The code at lines 349-363 tries to parse:
```python
usage = {
    "cost_usd": json_data.get("cost_usd", 0),
    "total_cost_usd": json_data.get("total_cost_usd", 0),
    ...
}
```

But we don't know what keys Claude Code actually returns. The task includes an investigation phase to capture a real JSON response and document the structure.

### Solution Approach

1. **Investigate first** — Don't guess the JSON structure, run a real dispatch and capture output
2. **Extract tokens** — Parse `input_tokens` and `output_tokens` from correct keys
3. **Calculate cost ourselves** — Don't trust Claude Code's cost field, use our rate card
4. **Populate usage dict** — Ensure `dispatch.py` gets: `input_tokens`, `output_tokens`, `cost_usd`, `carbon_kg`, `model`
5. **Graceful fallback** — If tokens missing, default to 0 and log warning

### Why Sonnet

This task requires:
- Investigation (run real Claude Code, inspect JSON)
- Implementation (rate card, cost calculation)
- Comprehensive tests (8+ test cases)
- Understanding the full flow from subprocess → adapter → dispatch → heartbeat

Sonnet is appropriate for this complexity.

---

## Validation

### Briefing requirements ✓

- [x] Investigate Claude Code JSON structure
- [x] Fix token extraction
- [x] Calculate cost from rate card
- [x] Use actual model (not hardcoded)
- [x] Heartbeat via usage dict
- [x] Carbon estimate

### Hard rules ✓

- [x] TDD (Rule 5)
- [x] No stubs (Rule 6)
- [x] File size check (Rule 4)
- [x] No hardcoded model (matches Rule 2 spirit — no hardcoded assumptions)
- [x] Absolute file paths (Rule 8)

### Task file completeness ✓

- [x] Objective (one sentence)
- [x] Context (what bee needs to know)
- [x] Files to Read First (4 files with absolute paths)
- [x] Deliverables (3 phases, checkboxes)
- [x] Test Requirements (8+ tests specified)
- [x] Constraints (file size, no hardcoded model, no stubs)
- [x] Acceptance Criteria (7 items from spec)
- [x] Response Requirements (8-section template)

---

## Recommendation

**APPROVE for dispatch.**

This task file is complete, follows TDD, enforces all hard rules, and includes the critical investigation phase to verify Claude Code's actual JSON structure before implementing the fix.

**Dispatch command:**
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-184-fix-cli-token-cost-tracking.md --model sonnet --role bee --inject-boot
```

---

**Q33N awaiting Q33NR review and approval to dispatch.**

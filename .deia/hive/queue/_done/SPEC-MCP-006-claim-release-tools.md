---
id: MCP-006
priority: P1
model: sonnet
role: bee
depends_on: [MCP-003]
---
# SPEC-MCP-006: Claim Task + Release Task Tools

## Priority
P1

## Model Assignment
sonnet

## Depends On
MCP-003

## Intent
Create `claim_task` and `release_task` tools for preventing double-dispatch. Hybrid storage: StateManager for speed + `_active/` directory move for durability. On MCP restart, rebuild claims from `_active/` directory.

## Files to Read First
- `hivenode/hive_mcp/tools/tasks.py` — existing task tools, add here
- `hivenode/hive_mcp/state.py` — StateManager, add claim recovery logic
- `.deia/hive/queue/_active/` — directory where claimed specs live
- `.deia/hive/queue/_done/` — directory where completed specs go
- `.deia/hive/queue/_needs_review/` — directory where failed specs go

## Acceptance Criteria
- [ ] `claim_task` tool: params `spec_id` (required), `bee_id` (required)
- [ ] `claim_task` returns `{"claimed": true, "owner": "BEE-..."}` on success
- [ ] `claim_task` returns `{"claimed": false, "owner": "BEE-...", "claimed_at": "..."}` if already claimed
- [ ] `claim_task` moves spec file from `backlog/` to `_active/` on successful claim
- [ ] `release_task` tool: params `spec_id` (required), `reason` (required: "done"|"failed"|"timeout")
- [ ] `release_task` moves spec from `_active/` to `_done/` (done) or `_needs_review/` (failed/timeout)
- [ ] `release_task` removes claim from StateManager
- [ ] On MCP server startup, StateManager scans `_active/` and rebuilds claims
- [ ] Tests: claim unclaimed, claim already-claimed, release done, release failed, recovery on restart

## Smoke Test
```bash
cd hivenode && python -m pytest tests/hivenode/test_mcp_tools.py -k "claim_task or release_task" -v
```

## Constraints
- No file over 500 lines
- TDD: tests first
- Add to existing `tools/tasks.py`, do NOT create new file
- StateManager recovery logic goes in `state.py`
- File moves must be atomic (os.rename) where possible
- Graceful handling if spec file doesn't exist (log warning, return error)

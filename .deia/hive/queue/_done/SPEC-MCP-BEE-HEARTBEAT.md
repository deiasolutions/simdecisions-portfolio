# MCP-BEE-HEARTBEAT: Inject MCP Heartbeat Instructions into Bee Prompts

## Objective
Add MCP usage instructions to bee prompts so dispatched bees report heartbeats and status updates via the MCP server during execution. Gives real-time visibility into bee activity.

## Build Type
**Extension** — Extends dispatch.py to inject MCP instructions into the bee prompt. No new files.

## Problem Analysis
Bees currently run silently until they finish and write a response file. The MCP server at port 8421 already has `heartbeat`, `status_report`, and `cost_summary` tools. Bees already see `.mcp.json` in the repo root. They just need prompt instructions telling them to use these tools. If the MCP server is down, the tools fail silently and the bee continues its real work — MCP is informational, not critical path.

## Files to Read First
- .deia/hive/scripts/dispatch/dispatch.py
- .mcp.json
- hivenode/hive_mcp/local_server.py

## Files to Modify
- .deia/hive/scripts/dispatch/dispatch.py — add MCP instruction injection

## Deliverables
- [ ] New function `_build_mcp_instructions()` returns MCP usage prompt text
- [ ] Instructions appended to bee prompt after governance docs section
- [ ] Instructions tell bee to: heartbeat every 5 minutes, status_report on each major step, cost_summary on completion
- [ ] Instructions explicitly state: MCP is best-effort, do NOT stop work if MCP calls fail
- [ ] Only injected for bee role (not queen, not regent)

## Acceptance Criteria
- [ ] Dispatched bee prompt contains MCP usage instructions
- [ ] Instructions reference correct tool names (heartbeat, status_report, cost_summary)
- [ ] Instructions include the spec name as identifier in heartbeat calls
- [ ] MCP section clearly marked as optional/best-effort
- [ ] No change to dispatch behavior if MCP server is not running
- [ ] Existing dispatch tests still pass

## Test Requirements
- [ ] Test: MCP instructions present in bee prompt
- [ ] Test: MCP instructions NOT present in queen prompt
- [ ] Test: instructions contain heartbeat, status_report, cost_summary tool names
- [ ] All existing dispatch tests pass
- [ ] Minimum 3 new tests

## Smoke Test
- [ ] python -m pytest tests/queue/test_dispatch*.py -v — all pass
- [ ] Dispatch a test spec, check response raw file shows MCP instructions in prompt

## Constraints
- No file over 500 lines
- No stubs
- MCP instructions must be clearly separated section in prompt
- Must not break any existing dispatch or gate tests

## Depends On
- Nothing (MCP server already exists)

## Model Assignment
haiku

## Priority
P1

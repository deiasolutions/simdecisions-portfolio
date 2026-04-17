# SPEC-TRIAGE-MCP-SMOKETEST-001: Triage Stalled MCP Smoke Test

**MODE: EXECUTE**

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

SPEC-MCP-SMOKETEST-001 is stalled in `_active/` — the bee produced no response file and no raw transcript. It was supposed to run 11 test groups against all 18 MCP specs. Likely hit a hanging test, blocking import, or infinite loop.

Your job:

1. **Diagnose** why the bee stalled — which test group or import caused the hang
2. **Run the smoke tests yourself** — but with 30-second timeouts on each group so nothing hangs
3. **Produce the smoke test report** that the original spec was supposed to deliver

## Context

- Stalled spec: `.deia/hive/queue/_active/SPEC-MCP-SMOKETEST-001.md`
- No response written to `.deia/hive/responses/20260409-MCP-SMOKETEST-RESPONSE.md`
- No raw transcript found
- MCP server code is in `hivenode/hive_mcp/`
- 18 MCP specs all in `_done/`

## Step 1: Find the Hang

Test each import and operation INDIVIDUALLY with a timeout. On Windows/bash, use `timeout 30` prefix or Python's `signal` module. The goal is to find which specific import or test call blocks forever.

Start with the most likely culprits:
1. `python -c "from hivenode.hive_mcp.local_server import *"` — does this hang? (MCP server may try to bind a port on import)
2. `python -m pytest hivenode/hive_mcp/tests/ --timeout=30` — do tests hang?
3. `python -c "from hivenode.main import app"` — does hivenode startup hang? (may try to connect to DB or start background tasks)

## Step 2: Run Safe Smoke Tests

For every test, use this pattern to prevent hangs:
```bash
timeout 30 python -c "CODE_HERE" 2>&1 || echo "TIMEOUT or FAIL"
```

Test groups (same as original spec but with timeouts):

1. Import each tool module in `hivenode/hive_mcp/tools/` individually
2. Check health endpoint route registration (no live server needed)
3. Check heartbeat tool exists and has advisory field
4. Check queue_state tool exists
5. Check dispatch tool exists
6. Check telemetry tool exists
7. Check claim/release tool exists
8. Check sync queue bridge exists
9. Check write + coordination tools exist
10. Run pytest with `--timeout=30 -x` (stop on first failure/hang)
11. Test `from hivenode.main import app` with timeout

## Step 3: Write Report

Write to `.deia/hive/responses/20260409-MCP-SMOKETEST-RESPONSE.md`:

```
# MCP Smoke Test Results (Triaged)

**Date:** 2026-04-09
**Note:** Original bee stalled. This is the triage re-run with timeouts.

## Hang Diagnosis
[What caused the original bee to stall]

## Results Summary
| Group | Component | Result | Notes |
|-------|-----------|--------|-------|
...

## Failures (Detail)
[Exact errors, file, line, suggested fix]

## MCP Tool Inventory
[Every registered tool: name, file, description]

## Verdict
[Overall health of MCP infrastructure]
```

## Acceptance Criteria

- [ ] Root cause of original bee stall identified
- [ ] All 11 test groups executed with 30-second timeouts
- [ ] Every PASS/FAIL reported with evidence
- [ ] Complete MCP tool inventory
- [ ] Response written to `.deia/hive/responses/20260409-MCP-SMOKETEST-RESPONSE.md`

## Smoke Test

```bash
test -f .deia/hive/responses/20260409-MCP-SMOKETEST-RESPONSE.md && echo "Response exists" || echo "MISSING"
```

## Constraints

- Do NOT fix any bugs — only report them
- Do NOT modify any code files
- EVERY command must have a 30-second timeout — no exceptions
- If pytest exists for MCP, run with `--timeout=30 -x`
- Max response length: 400 lines

## Response File

`.deia/hive/responses/20260409-MCP-SMOKETEST-RESPONSE.md`

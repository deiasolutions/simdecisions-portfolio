# BRIEFING: MCP Rehabilitation Spec Review

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-07
**Priority:** P1
**Objective:** Review SPEC-MCP-REHABILITATION-001 against the existing MCP build, identify gaps/conflicts, and prepare questions for Mr. AI (the architect)

---

## Context

Q88N authored `SPEC-MCP-REHABILITATION-001` to wire the existing MCP server (`hivenode/hive_mcp/`, port 8421) into the factory pipeline. Currently the MCP server is built but completely disconnected — bees run blind via fire-and-forget subprocess dispatch. The spec defines 6 waves to connect MCP as a real-time sideband for bee coordination.

The FACTORY pipeline was just completed (8 specs, 173 tests, ~8,500 lines). The MCP rehabilitation depends on FACTORY-006 (Telemetry Policy Split).

---

## Your Tasks

### 1. Read the Spec
The full spec is at: `C:\Users\davee\Downloads\SPEC-MCP-REHABILITATION-001.md`

### 2. Audit the Existing MCP Build
Read every file in `hivenode/hive_mcp/` and understand what already exists:
- `local_server.py` — the MCP server implementation
- `sync.py` — SyncQueueWriter
- `tools/` — existing tool modules (queue.py, tasks.py, coordination.py, responses.py, dispatch.py, telemetry.py)
- `README.md` — roadmap (Phase 0-4)

For each tool the spec proposes, determine:
- Does it already exist? (fully, partially, or not at all)
- Does the existing implementation match the spec's interface?
- Are there naming conflicts? (e.g., spec says `mcp_heartbeat`, existing code might call it something else)

### 3. Audit the Dispatch and Queue Runner
Read these files and assess what changes are actually needed:
- `.deia/hive/scripts/dispatch/dispatch.py` — does it already have any MCP awareness?
- `.deia/hive/scripts/queue/run_queue.py` — any MCP health checks?
- `.deia/hive/scripts/queue/spec_processor.py` — any MCP integration points?

### 4. Check FACTORY-006 Dependency
Read the FACTORY-006 response: `.deia/hive/responses/20260407-QUEUE-TEMP-SPEC-FACTORY-006-RESPONSE.md`
- What did FACTORY-006 actually build?
- Does the telemetry dual-loop architecture match what the rehab spec assumes?
- Any conflicts or mismatches?

### 5. Check hivenode/main.py
The spec says to mount MCP as a sub-app. Read `hivenode/main.py` — is the MCP server already mounted? How?

### 6. Prepare Questions for Mr. AI

Based on your audit, compile a list of questions organized by category:
- **Architecture questions** — design decisions that need architect input
- **Conflict questions** — where the spec contradicts existing code
- **Gap questions** — what the spec doesn't address but should
- **Sequencing questions** — whether the 6-wave order is right
- **Risk questions** — what could go wrong

These questions should be specific, referencing file paths and line numbers where relevant. Not vague.

---

## Deliverables

Write your response to: `.deia/hive/responses/20260407-MCP-REHAB-REVIEW-RESPONSE.md`

The response must include:
1. **Existing MCP Inventory** — table of every file, its purpose, its readiness vs the spec
2. **Spec vs. Reality Gap Analysis** — what the spec assumes exists vs what actually exists
3. **FACTORY-006 Alignment Check** — does the telemetry dual-loop match?
4. **Dispatch/Queue Runner Readiness** — what needs to change, what's already there
5. **Questions for Mr. AI** — the compiled question list, organized by category, specific and actionable

---

## Files to Read

- `C:\Users\davee\Downloads\SPEC-MCP-REHABILITATION-001.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\local_server.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\sync.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\README.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\` (all files)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260407-QUEUE-TEMP-SPEC-FACTORY-006-RESPONSE.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260407-FACTORY-PIPELINE-FINAL-SUMMARY.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`

## Constraints

- Do NOT write code. This is a review and question-prep task.
- Do NOT modify any source files.
- Be specific in your questions — file paths, line numbers, interface mismatches.
- If the spec references a file that doesn't exist, flag it.
- If the spec proposes creating a file that already exists, flag the conflict.

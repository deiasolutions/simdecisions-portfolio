# SPEC-MCP-WAVE-3-WRITE-TOOLS: Phase 1 Write Tools

**Master Spec:** docs/specs/SPEC-MCP-REHABILITATION-001.md
**Status:** READY
**Priority:** P2
**Depends On:** SPEC-MCP-WAVE-2-DISPATCH-INTEGRATION.md
**Model Assignment:** haiku

---

## Objective

Add Phase 1 write tools (`mcp_claim_task`, `mcp_release_task`, `mcp_submit_response`) using file-based claim/release. These tools enable bees to coordinate task ownership and submit partial responses via MCP.

---

## Governing Constraint

**MCP complements dispatch; it never blocks it.** If MCP is down, dispatch proceeds. MCP is observability and coordination bonus, not infrastructure dependency.

---

## Requirements — Phase 1 Tools (New Write Tools)

| Tool | Purpose | Parameters | Returns |
|------|---------|------------|---------|
| `mcp_claim_task` | Claim spec (prevent double-dispatch) | `{spec_id, bee_id}` | `{claimed: bool, owner?: bee_id}` |
| `mcp_release_task` | Release claim | `{spec_id, reason: "done" \| "failed" \| "timeout"}` | `{released: bool}` |
| `mcp_submit_response` | Submit partial/final response | `{spec_id, content, is_final: bool}` | `{received: bool, path?: string}` |

---

## Implementation Details

### File-Based Claim/Release

- **`mcp_claim_task`** moves spec from `.deia/hive/queue/` to `.deia/hive/queue/_active/`
- **`mcp_release_task`** moves spec from `_active/` to:
  - `.deia/hive/queue/_done/` if `reason="done"`
  - `.deia/hive/queue/` if `reason="failed"` (re-queue)
  - `.deia/hive/queue/_dead/` if `reason="timeout"`
- StateManager mirrors claim state for fast lookup, but **file location is source of truth**
- Survives crashes — file system state persists

### Response Submission

- **`mcp_submit_response`** writes to `.deia/hive/responses/YYYYMMDD-{spec_id}-RESPONSE.md`
- If `is_final=true`, marks response as complete
- If `is_final=false`, writes partial response (append or overwrite based on implementation choice)

---

## File Inventory

| File | Action | Purpose |
|------|--------|---------|
| `hivenode/hive_mcp/tools/claim.py` | CREATE | `mcp_claim_task`, `mcp_release_task` (file-based) |
| `hivenode/hive_mcp/tools/response.py` | CREATE | `mcp_submit_response` |
| `tests/core/test_mcp_claim_release.py` | CREATE | Claim/release file movement tests |
| `tests/core/test_mcp_response_submit.py` | CREATE | Response submission tests |

---

## Acceptance Criteria

- [ ] AC-10: `mcp_claim_task` moves spec to `_active/` (file check after claim)
- [ ] AC-11: `mcp_release_task` moves spec out of `_active/` (file check after release)
- [ ] AC-15: `mcp_claim_task` returns `{claimed: false, owner: <bee_id>}` if already claimed by another bee
- [ ] AC-16: `mcp_submit_response` writes to correct path (`.deia/hive/responses/`)
- [ ] AC-17: StateManager reflects claim state (query via `mcp_queue_state`)
- [ ] AC-18: Claim survives StateManager restart (file is source of truth)

---

## Smoke Test

- [ ] Call `mcp_claim_task` with `{spec_id: "TEST-001", bee_id: "BEE-001"}`
- [ ] Verify file moved to `.deia/hive/queue/_active/TEST-001.md`
- [ ] Call `mcp_release_task` with `{spec_id: "TEST-001", reason: "done"}`
- [ ] Verify file moved to `.deia/hive/queue/_done/TEST-001.md`

---

## Constraints

1. Do not rename existing MCP tools (existing names stay as-is)
2. New tools get `mcp_*` prefix only
3. **File-based claim/release (not in-memory)** — file location is source of truth
4. Bee temp dir: `.deia/hive/temp/{bee_id}/`
5. `queue.yml` kill switch: `mcp_required: false`

---

## Decisions Record (Reference)

Architect responses (2026-04-12, Mr. AI via Q88N):

| # | Question | Decision |
|---|----------|----------|
| 1 | Tool naming | Keep existing names, `mcp_*` for new only |
| 8 | Claim/release | File-based (`_active/` directory), StateManager mirrors |
| 14 | StateManager persistence | Accept volatile — heartbeats are ephemeral |

---

## Response File Template

When complete, write: `.deia/hive/responses/YYYYMMDD-SPEC-MCP-WAVE-3-WRITE-TOOLS-RESPONSE.md`

Required sections:
1. **Status:** COMPLETE | FAILED (reason)
2. **Files Modified** (absolute paths)
3. **What Was Done** (concrete changes)
4. **Tests Run** (commands + results)
5. **Acceptance Criteria Status** (check each AC)
6. **Blockers** (if any)
7. **Cost** (tokens, USD)
8. **Next Steps** (for Q33N/Q33NR)

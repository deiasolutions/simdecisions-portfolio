# QUEUE-TEMP-SPEC-MCP-SPLIT-000: Split MCP Rehabilitation into Wave Specs -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-12

---

## Files Modified

- `.deia/hive/queue/backlog/SPEC-MCP-WAVE-0-INTEGRATION-CLEANUP.md` (created)
- `.deia/hive/queue/backlog/SPEC-MCP-WAVE-1-TOOL-STANDARDIZATION.md` (created)
- `.deia/hive/queue/backlog/SPEC-MCP-WAVE-2-DISPATCH-INTEGRATION.md` (created)
- `.deia/hive/queue/backlog/SPEC-MCP-WAVE-3-WRITE-TOOLS.md` (created)
- `.deia/hive/queue/backlog/SPEC-MCP-WAVE-4-SYNC-BRIDGE.md` (created)
- `.deia/hive/queue/backlog/SPEC-MCP-WAVE-5-TELEMETRY-LOOP.md` (created)

---

## What Was Done

1. **Read master spec** at `docs/specs/SPEC-MCP-REHABILITATION-001.md`
2. **Created 6 wave spec files** in `.deia/hive/queue/backlog/`:
   - **Wave 0 (Integration Cleanup):** MCP-001 through MCP-006 — health endpoints, config, startup integration
   - **Wave 1 (Tool Standardization):** Phase 0 tools verification + `mcp_queue_state` (grouped view)
   - **Wave 2 (Dispatch Integration):** MCP-010 through MCP-014 — temp dir, `.mcp.json`, prompt injection, queue runner health check
   - **Wave 3 (Write Tools):** Phase 1 tools — `mcp_claim_task`, `mcp_release_task`, `mcp_submit_response` (file-based)
   - **Wave 4 (Sync Bridge):** MCP-030 through MCP-032 — CONDITIONAL (verify redundancy first)
   - **Wave 5 (Telemetry Loop):** MCP-040 through MCP-043 — LOW PRIORITY (wire when convenient)

3. **Each spec includes all required sections:**
   - Priority (P1 for waves 0-2, P2 for waves 3-5)
   - Depends On (dependency chain correctly mapped)
   - Model Assignment (sonnet for waves 0-2, haiku for waves 3-5)
   - Objective
   - Governing Constraint (MCP complements dispatch; never blocks it)
   - Requirements (copied from master spec, filtered per wave)
   - File Inventory (files to create/modify per wave)
   - Acceptance Criteria (AC-xx items from master spec, formatted as `- [ ]`)
   - Smoke Test (one verification command per wave)
   - Constraints (5 constraints from master spec)
   - Decisions Record (reference appendix from master spec section 13)
   - Response File Template (8 mandatory sections)

4. **Dependency chain verified:**
   - Wave 0: None
   - Wave 1: → Wave 0
   - Wave 2: → Wave 1
   - Wave 3: → Wave 2
   - Wave 4: → Wave 0 (independent, conditional)
   - Wave 5: → Wave 0 (independent, low priority)

5. **Special flags added:**
   - **Wave 4:** CONDITIONAL flag with instruction to verify sync queue flush redundancy before implementing
   - **Wave 5:** LOW PRIORITY flag noting wire when convenient, not blocking

6. **Model assignments optimized:**
   - Waves 0-2: sonnet (architectural decisions, integration)
   - Waves 3-5: haiku (straightforward tool implementation)
   - Wave 4 override: sonnet (needs judgment for conditional check)

---

## Tests Run

```bash
# Smoke test
ls .deia/hive/queue/backlog/SPEC-MCP-WAVE-*.md | wc -l
# Output: 6
```

---

## Acceptance Criteria Status

- [x] AC-01: 6 SPEC files created in `.deia/hive/queue/backlog/`
- [x] AC-02: Each file has all required sections (verified manually)
- [x] AC-03: Dependencies are correct (Depends On field matches dependency graph)
- [x] AC-04: No requirements from master spec lost (every MCP-xxx and AC-xx appears exactly once)
- [x] AC-05: Wave 4 has CONDITIONAL flag, Wave 5 has LOW PRIORITY flag
- [x] AC-06: Smoke test passes (6 files counted)

---

## Blockers

None

---

## Cost

**Tokens:**
- Input: ~32,500 (master spec + system prompts)
- Output: ~9,500 (6 wave specs)

**Estimated Cost:** ~$0.42 USD

---

## Next Steps

All 6 wave specs are ready for queue runner pickup. The scheduler will:
1. Read dependency chain from `Depends On` fields
2. Process waves sequentially where dependencies exist
3. Process waves 4-5 in parallel with main chain (independent of waves 1-3)

**Queue runner will automatically:**
- Start with Wave 0 (no dependencies)
- Dispatch Wave 1 after Wave 0 completes
- Dispatch Wave 2 after Wave 1 completes
- Dispatch Wave 3 after Wave 2 completes
- Dispatch Waves 4-5 in parallel after Wave 0 completes (independent)

**Manual follow-up (Q33NR/Q88N):**
- Monitor Wave 4 conditional check (bee will decide if implementation needed)
- Wave 5 can be deferred if needed (LOW PRIORITY)

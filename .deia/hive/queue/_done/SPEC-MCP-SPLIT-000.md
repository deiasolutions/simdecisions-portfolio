# SPEC-MCP-SPLIT-000: Split MCP Rehabilitation into Wave Specs

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Read the master spec at `docs/specs/SPEC-MCP-REHABILITATION-001.md` and produce
one standalone SPEC file per implementation wave. Place each file in
`.deia/hive/queue/backlog/`. **These output files are factory build inputs.**
The scheduler automatically picks up `SPEC-*.md` files from `queue/backlog/`
and dispatches bees to build them. Each wave spec has a `Depends On` field
that prevents premature dispatch — the factory will sequence them correctly.
Each wave spec must be self-contained: a bee picking it up must be able to
build it without reading the master spec.

## Acceptance Criteria

- [ ] 6 SPEC files created in `.deia/hive/queue/backlog/`
- [ ] Each file has all required sections listed above
- [ ] Dependencies are correct (Depends On field matches the dependency graph)
- [ ] No requirements from the master spec are lost — every MCP-xxx and AC-xx appears in exactly one wave spec
- [ ] Wave 4 has CONDITIONAL flag, Wave 5 has LOW PRIORITY flag

## Smoke Test

- [ ] `ls .deia/hive/queue/backlog/SPEC-MCP-WAVE-*.md | wc -l` returns 6

## Constraints

- Do not rename existing MCP tools (existing names stay as-is)
- New tools get mcp_* prefix only
- File-based claim/release (not in-memory)
- Bee temp dir: .deia/hive/temp/{bee_id}/
- queue.yml kill switch: mcp_required: false

## Waves to Split

The master spec (section 11) defines 6 waves:

1. **Wave 0 — Integration Cleanup** (MCP-001 through MCP-006)
2. **Wave 1 — Tool Interface Standardization** (Phase 0 tools)
3. **Wave 2 — Dispatch Integration** (MCP-010 through MCP-014)
4. **Wave 3 — Write Tools** (Phase 1 tools — claim, release, submit)
5. **Wave 4 — Sync Queue Bridge** (MCP-030 through MCP-032, conditional)
6. **Wave 5 — Telemetry Dual-Loop** (MCP-040 through MCP-043)

## Output Files

Create these files in `.deia/hive/queue/backlog/`:

- `SPEC-MCP-WAVE-0-INTEGRATION-CLEANUP.md`
- `SPEC-MCP-WAVE-1-TOOL-STANDARDIZATION.md`
- `SPEC-MCP-WAVE-2-DISPATCH-INTEGRATION.md`
- `SPEC-MCP-WAVE-3-WRITE-TOOLS.md`
- `SPEC-MCP-WAVE-4-SYNC-BRIDGE.md`
- `SPEC-MCP-WAVE-5-TELEMETRY-LOOP.md`

## Required Sections Per Wave Spec

Each wave spec MUST include these sections (use `##` headings):

- Priority (P1 for waves 0-2, P2 for waves 3-5)
- Depends On (previous wave spec filename, or "None" for wave 0)
- Model Assignment (sonnet for waves 0-2, haiku for waves 3-5)
- Objective (1-2 sentences: what this wave delivers)
- Governing Constraint: MCP complements dispatch; it never blocks it. If MCP is down, dispatch proceeds.
- Requirements (Copy the relevant MCP-xxx requirements table from the master spec)
- File Inventory (Which files to create/modify — copy from master spec section 10, filtered to this wave)
- Acceptance Criteria (Copy the relevant AC-xx items from master spec section 8, in `- [ ]` format)
- Smoke Test (One curl or pytest command that proves this wave works, in `- [ ]` format)
- Constraints (the 5 constraints from the Constraints section above)

## Dependencies Between Waves

```
Wave 0 (none)
  → Wave 1 (depends on Wave 0)
    → Wave 2 (depends on Wave 1)
Wave 3 (depends on Wave 2)
Wave 4 (depends on Wave 0, conditional — mark as CONDITIONAL in spec)
Wave 5 (depends on Wave 0, non-blocking — mark as LOW PRIORITY)
```

## Special Instructions

- **Wave 4:** Add a note at the top: "CONDITIONAL — before building, verify that
  sync queue flush already happens on hivenode startup (main.py:157-161). If it
  does, write a response explaining the finding and move this spec to _done/
  without implementation. If it does NOT, proceed with the build." Assign model
  to sonnet (needs judgment, not just code output).
- **Wave 5:** Add a note at the top: "LOW PRIORITY — wire when convenient per
  architect decision. Not blocking any other work."
- Copy the Decisions Record (section 13 of master spec) into each wave spec as
  a reference appendix, so bees have full architect context.
- Each wave spec must reference the master spec path for traceability:
  `Master Spec: docs/specs/SPEC-MCP-REHABILITATION-001.md`

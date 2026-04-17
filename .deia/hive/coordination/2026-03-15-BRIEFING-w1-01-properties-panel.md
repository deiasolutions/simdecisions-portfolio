# BRIEFING: Port Properties Panel (SPEC w1-01)

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-15-0333-SPE)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-15
**Spec:** `.deia/hive/queue/2026-03-15-0333-SPEC-w1-01-properties-panel.md`
**Model Assignment:** sonnet

---

## Objective

Port the Properties Panel from platform/efemera to shiftcenter. The spec states:
- 16 files total
- 6 accordion sections (General, Data, Rules, Connections, Resources, Advanced)
- Full node property editor
- Source: `platform/efemera/src/efemera/components/properties/`
- Target: `browser/src/apps/sim/components/properties/`

---

## Current State

### Files Already Present

**Directory:** `browser/src/apps/sim/components/flow-designer/properties/`

8 files exist:
1. `ActionsTab.tsx` (9,761 bytes)
2. `GeneralTab.tsx` (3,214 bytes)
3. `GuardsTab.tsx` (5,932 bytes)
4. `NodePopover.tsx` (6,211 bytes)
5. `OracleTab.tsx` (9,508 bytes)
6. `PropertyPanel.tsx` (9,420 bytes)
7. `ResourcesTab.tsx` (9,264 bytes)
8. `TimingTab.tsx` (5,570 bytes)

**Note:** The spec says target is `browser/src/apps/sim/components/properties/` but files exist at `browser/src/apps/sim/components/flow-designer/properties/`.

### Source Directory Missing

The source directory `platform/efemera/src/efemera/components/properties/` does NOT exist in this repo. There is no `platform/` directory at all.

### Tests Missing

No test files exist for the properties panel components.

---

## Issues Requiring Q33N Investigation

1. **Source location:** The source directory specified in the spec does not exist. Q33N must either:
   - Find the actual source files (search the repo)
   - Determine if the 8 existing files ARE the port (already done)
   - Determine if this is a NEW implementation (not a port)

2. **Target directory mismatch:** Spec says `browser/src/apps/sim/components/properties/` but files exist at `browser/src/apps/sim/components/flow-designer/properties/`. Q33N must:
   - Confirm which is correct
   - Move files if needed
   - Or write task to create at correct location

3. **File count discrepancy:** Spec says 16 files, only 8 exist. Q33N must:
   - Identify the 8 missing files
   - Or determine if 8 files is actually complete

4. **Accordion sections:** Spec says 6 sections (General, Data, Rules, Connections, Resources, Advanced). Existing files show:
   - GeneralTab ✓
   - ResourcesTab ✓
   - ActionsTab
   - GuardsTab
   - OracleTab
   - TimingTab
   - NodePopover
   - PropertyPanel (main component)

   Q33N must map these to the 6 required sections.

---

## Your Tasks (Q33N)

### Task 1: Investigation
Read the existing properties panel files. Determine:
- Are these files the completed port?
- What are the 8 missing files (if any)?
- Is the directory location correct?
- Do the tabs map to the 6 required accordion sections?

### Task 2: Write Task File(s)
Based on your investigation, write task files for:
- **If files need moving:** Task to move from `flow-designer/properties/` to `properties/`
- **If files are missing:** Task(s) to create the missing 8 files
- **If tests are missing:** Task to write comprehensive tests for all properties panel components
- **If integration is needed:** Task to wire the properties panel into the sim app

### Task 3: Constraints to Enforce
Every task file MUST specify:
- Max 500 lines per file (check existing files for violations)
- CSS: `var(--sd-*)` only (check existing files)
- TDD: tests first
- No stubs
- Heartbeat requirement: POST to `http://localhost:8420/build/heartbeat` every 3 minutes with:
  ```json
  {"task_id": "2026-03-15-0333-SPEC-w1-01-properties-panel", "status": "running", "model": "sonnet", "message": "working"}
  ```

### Task 4: Smoke Test
Final task must include smoke test:
```bash
cd browser && npx vitest run src/apps/sim/components/properties/
```
(or `flow-designer/properties/` depending on final location)

---

## Acceptance Criteria (from Spec)

- [ ] All 16 properties panel files ported (or confirm only 8 needed)
- [ ] 6 accordion sections render correctly
- [ ] Node property editing works
- [ ] Tests written and passing

---

## Files to Read First

Q33N should read these existing files:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\properties\PropertyPanel.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\properties\GeneralTab.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\properties\ResourcesTab.tsx`
- Search for any imports of these components to understand integration

---

## Expected Output from Q33N

A list of task files ready for Q33NR review, plus:
- Summary of what exists vs what's needed
- Clarification on directory location
- Clarification on file count (8 vs 16)
- Mapping of existing tabs to the 6 required accordion sections

Do NOT dispatch bees until Q33NR reviews and approves your task files.

---

**Q33NR signature:** REGENT-QUEUE-TEMP-2026-03-15-0333-SPE

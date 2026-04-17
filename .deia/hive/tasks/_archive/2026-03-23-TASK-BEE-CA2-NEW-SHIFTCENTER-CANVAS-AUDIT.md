# TASK-BEE-CA2: New ShiftCenter Flow-Designer Capability Audit

## Objective
Produce a complete capability inventory of the NEW flow-designer system in the shiftcenter repo by reading actual source code. Every claim must be backed by specific file paths and line ranges.

## Context
Q88N needs a definitive comparison between the old platform canvas system and the new shiftcenter flow-designer. This task audits the NEW system only. A parallel bee (BEE-CA1) will audit the OLD system. A third bee (BEE-CA3) will merge both reports.

**Shiftcenter repo location:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter`

**Known flow-designer locations:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\simAdapter.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas2.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\sim.egg.md` (if exists)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\simAdapter.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py`

## Deliverables
- [ ] Complete list of ALL modes the new flow-designer supports (design, simulate, playback, tabletop, compare, etc.)
- [ ] For each mode: is it WIRED (backend + UI working) or SHELL (UI only, no backend)?
- [ ] Complete list of ALL node types (name every single type, not "4-6 types" — NAME THEM)
- [ ] Line count breakdown: flow-designer UI (lines), DES routes (lines), simulation (lines), properties (lines), total (lines)
- [ ] Feature list: what capabilities exist? (drag-drop, undo/redo, validation, export, import, zoom, pan, etc.)
- [ ] Backend integration: which features have backend APIs vs client-only?
- [ ] Component inventory: which components are wired end-to-end vs UI shells with no backend?
- [ ] File paths for every major subsystem (absolute paths)
- [ ] Response file written to `.deia\hive\responses\20260323-TASK-BEE-CA2-RESPONSE.md`

## Research Strategy
1. Use Glob to find all TypeScript/JavaScript files in flow-designer directory
2. Use Grep to search for keywords: "mode", "node", "type", "canvas", "flow", "simulation", "DES", "backend", "api"
3. Read actual source files to verify modes, node types, and features
4. Count lines using Bash `wc -l` on relevant directories
5. For each component: check if it makes API calls (wired) or is UI-only (shell)
6. Do NOT guess. If you can't find a feature, state "NOT FOUND after searching X, Y, Z"

## Test Requirements
- [ ] No tests required (this is read-only research)
- [ ] Verification: every claim must cite file path + line range

## Constraints
- READ ONLY — no file modifications
- Absolute paths for all file references
- No "likely" or "probably" — verify or say NOT FOUND
- All findings must be reproducible (cite line numbers)
- For each component/mode: state WIRED or SHELL (and prove it)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260323-TASK-BEE-CA2-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — (none — read-only task)
3. **What Was Done** — bullet list of research performed
4. **Test Results** — N/A (read-only research)
5. **Build Verification** — N/A (read-only research)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — any gaps, missing data, or ambiguities

DO NOT skip any section.

## Key Questions to Answer
1. What modes exist? (list every mode with file path proof, state WIRED or SHELL)
2. What node types exist? (list every type with file path proof)
3. How many lines of code? (UI, backend, total — with command proof)
4. What features exist? (every feature with file path proof)
5. What has backend APIs? (endpoint list with file path proof)
6. Which components are wired end-to-end vs UI shells? (prove for each)
7. Why 35,625 lines? (where did the expansion come from?)

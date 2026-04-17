# TASK-BEE-CA1: Old Platform Canvas Capability Audit

## Objective
Produce a complete capability inventory of the OLD canvas system in the platform repo by reading actual source code. Every claim must be backed by specific file paths and line ranges.

## Context
Q88N needs a definitive comparison between the old platform canvas system and the new shiftcenter flow-designer. This task audits the OLD system only. A parallel bee (BEE-CA2) will audit the NEW system. A third bee (BEE-CA3) will merge both reports.

**Platform repo location:** `C:\Users\davee\OneDrive\Documents\GitHub\platform`

**Likely canvas locations:**
- `src/efemera/components/canvas/` (if it exists)
- `simdecisions-2/src/` (React components)
- `src/efemera/des/` (DES engine backend)
- Look for: mode switching, node types, simulation integration, properties panels

## Files to Read First
Start by exploring the platform repo structure:
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\README.md` (if exists)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\package.json` (to understand structure)
- Then search for canvas/flow/simulation components using Glob and Grep

## Deliverables
- [ ] Complete list of ALL modes the old canvas supported (design, simulate, playback, tabletop, compare, etc.)
- [ ] Complete list of ALL node types (name every single type, not "17 types" — NAME THEM)
- [ ] Line count breakdown: canvas UI (lines), DES engine (lines), simulation (lines), properties (lines), total (lines)
- [ ] Feature list: what capabilities existed? (drag-drop, undo/redo, validation, export, import, zoom, pan, etc.)
- [ ] Backend integration: which features had backend APIs vs client-only?
- [ ] File paths for every major subsystem (absolute paths)
- [ ] Response file written to `.deia\hive\responses\20260323-TASK-BEE-CA1-RESPONSE.md`

## Research Strategy
1. Use Glob to find all TypeScript/JavaScript files in likely canvas directories
2. Use Grep to search for keywords: "mode", "node", "type", "canvas", "flow", "simulation", "DES"
3. Read actual source files to verify modes, node types, and features
4. Count lines using Bash `wc -l` on relevant directories
5. Do NOT guess. If you can't find a feature, state "NOT FOUND after searching X, Y, Z"

## Test Requirements
- [ ] No tests required (this is read-only research)
- [ ] Verification: every claim must cite file path + line range

## Constraints
- READ ONLY — no file modifications
- Absolute paths for all file references
- No "likely" or "probably" — verify or say NOT FOUND
- All findings must be reproducible (cite line numbers)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260323-TASK-BEE-CA1-RESPONSE.md`

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
1. What modes existed? (list every mode with file path proof)
2. What node types existed? (list every type with file path proof)
3. How many lines of code? (UI, engine, total — with command proof)
4. What features existed? (every feature with file path proof)
5. What had backend APIs? (endpoint list with file path proof)

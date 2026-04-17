# TASK-BEE-CA3: Canvas Capability Comparison Report

## Objective
Produce a single consolidated side-by-side comparison report of OLD platform canvas vs NEW shiftcenter flow-designer, based on the findings from BEE-CA1 and BEE-CA2.

## Context
This task runs AFTER BEE-CA1 and BEE-CA2 complete. You will read their response files and merge the findings into a final comparison report for Q88N.

**Input files (read these first):**
- `.deia\hive\responses\20260323-TASK-BEE-CA1-RESPONSE.md` (old platform audit)
- `.deia\hive\responses\20260323-TASK-BEE-CA2-RESPONSE.md` (new shiftcenter audit)

**Output file:**
- `.deia\hive\responses\20260323-TASK-BEE-CA3-RESPONSE.md` (this task's response)
- `.deia\hive\coordination\2026-03-23-CANVAS-COMPARISON-REPORT.md` (the deliverable for Q88N)

## Files to Read First
- `.deia\hive\responses\20260323-TASK-BEE-CA1-RESPONSE.md`
- `.deia\hive\responses\20260323-TASK-BEE-CA2-RESPONSE.md`

## Deliverables
- [ ] Side-by-side mode comparison (old modes vs new modes, which exist in both, which are new, which are missing)
- [ ] Side-by-side node type comparison (old types vs new types, full lists)
- [ ] Regression analysis (features in old but NOT in new)
- [ ] Innovation analysis (features in new but NOT in old)
- [ ] Line count analysis (old total vs new total, breakdown by subsystem, why 7.2x expansion?)
- [ ] Wired vs shell analysis (which new components are wired, which are shells)
- [ ] Comparison report written to `.deia\hive\coordination\2026-03-23-CANVAS-COMPARISON-REPORT.md`
- [ ] Response file written to `.deia\hive\responses\20260323-TASK-BEE-CA3-RESPONSE.md`

## Report Format

The comparison report (`.deia\hive\coordination\2026-03-23-CANVAS-COMPARISON-REPORT.md`) must contain:

```markdown
# Canvas Capability Audit: Old Platform vs New ShiftCenter

**Date:** 2026-03-23
**Auditors:** BEE-CA1, BEE-CA2, BEE-CA3
**Status:** COMPLETE

## Executive Summary
[2-3 paragraphs: key findings, major differences, line count justification]

## Mode Comparison

| Mode | Old Platform | New ShiftCenter | Status |
|------|-------------|-----------------|--------|
| Design | [YES/NO + file proof] | [YES/NO + WIRED/SHELL + file proof] | [PARITY/REGRESSION/NEW] |
| Simulate | ... | ... | ... |
| ... | ... | ... | ... |

## Node Type Comparison

| Node Type | Old Platform | New ShiftCenter | Notes |
|-----------|-------------|-----------------|-------|
| ... | [file proof] | [file proof] | ... |

## Feature Comparison

| Feature | Old Platform | New ShiftCenter | Status |
|---------|-------------|-----------------|--------|
| Drag-drop | ... | ... | ... |
| Undo/redo | ... | ... | ... |
| Validation | ... | ... | ... |
| ... | ... | ... | ... |

## Regression Analysis
[Features that existed in old but are MISSING in new]

## Innovation Analysis
[Features that exist in new but did NOT exist in old]

## Line Count Analysis

| Subsystem | Old (lines) | New (lines) | Ratio | Explanation |
|-----------|------------|------------|-------|-------------|
| Canvas UI | ... | ... | ...x | ... |
| DES Engine | ... | ... | ...x | ... |
| Simulation | ... | ... | ...x | ... |
| Properties | ... | ... | ...x | ... |
| **TOTAL** | **4,927** | **35,625** | **7.2x** | [Explain the expansion] |

## Wired vs Shell Analysis
[For each new component: is it wired end-to-end or just a UI shell?]

## Conclusion
[Q88N's key questions answered: What justifies 7.2x expansion? What's missing? What's new? What works?]
```

## Test Requirements
- [ ] No tests required (this is a report synthesis task)
- [ ] Verification: every claim must trace back to BEE-CA1 or BEE-CA2 findings

## Constraints
- Do NOT guess or infer. Only state what BEE-CA1 and BEE-CA2 found.
- If either bee couldn't find something, state "NOT FOUND (per BEE-CAX)"
- Absolute paths for all file references
- Write both: the comparison report (for Q88N) AND the response file (for Q33N)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260323-TASK-BEE-CA3-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — list: `.deia\hive\coordination\2026-03-23-CANVAS-COMPARISON-REPORT.md` (created)
3. **What Was Done** — bullet list of synthesis work
4. **Test Results** — N/A (report synthesis task)
5. **Build Verification** — N/A (report synthesis task)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — any gaps, ambiguities, or recommended next steps

DO NOT skip any section.

## Dependencies
- DEPENDS ON: TASK-BEE-CA1 (must complete first)
- DEPENDS ON: TASK-BEE-CA2 (must complete first)
- DO NOT START until both CA1 and CA2 response files exist

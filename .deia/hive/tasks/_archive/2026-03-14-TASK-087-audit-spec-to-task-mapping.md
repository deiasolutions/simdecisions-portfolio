# TASK-087: Audit Part 1 — Spec-to-Task Mapping

## Objective
Read every spec in `.deia/hive/queue/_done/` and determine what task files each spec produced. **READ-ONLY. Do not modify any files except your response file.**

## Instructions

1. Read every `.md` file in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_done\` (23 specs)
2. For each spec, search `.deia/hive/tasks/` AND `.deia/hive/tasks/_archive/` for task files that reference or were created from that spec
3. For each task file found, check `.deia/hive/responses/` for a matching bee response file (pattern: `*TASK-XXX*RAW.txt` or `*TASK-XXX*RESPONSE.md`)
4. Produce a table with columns: Spec Filename | Spec Title | Task Files Created | Bee Response Exists (Y/N) | Status

Also check the failed spec still in queue: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-13-2251-SPEC-fix-deployment-wiring-retry.md`

## Constraints
- DO NOT modify any files except your response file
- DO NOT run inventory.py
- DO NOT archive anything
- DO NOT move or rename files

## Response Requirements — MANDATORY

Write your response to: `.deia/hive/responses/20260314-TASK-087-AUDIT-SPEC-MAPPING.md`

The response MUST contain:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — only your response file
3. **What Was Done** — bullet list of investigation steps
4. **Findings** — the complete spec-to-task table
5. **Gaps** — specs with NO task files
6. **Issues / Follow-ups** — anything unexpected

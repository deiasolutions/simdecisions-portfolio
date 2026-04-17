# TASK-090: Audit Part 4 — Code Integrity

## Objective
Correlate every uncommitted file change in the working tree to a specific task. **READ-ONLY. Do not modify any files except your response file.**

## Instructions

1. Run `git diff --name-only HEAD` to get every modified file
2. Run `git status` to get every untracked file
3. For EACH modified/new file, determine which task it belongs to by:
   - Reading bee response files in `.deia/hive/responses/` (they list "Files Modified" sections)
   - Matching file paths to task scope (e.g., `engine/phase_ir/` → TASK-071, `browser/src/primitives/terminal/Voice*` → TASK-080)
4. Produce a table: File Path | Task ID | Category (modified/new/deleted)
5. Flag any files that don't belong to any task
6. Flag any tasks that claim success but have no corresponding file changes

## Constraints
- DO NOT modify any files except your response file
- DO NOT run inventory.py
- DO NOT archive anything

## Response Requirements — MANDATORY

Write your response to: `.deia/hive/responses/20260314-TASK-090-AUDIT-CODE-INTEGRITY.md`

The response MUST contain:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — only your response file
3. **What Was Done** — bullet list of investigation steps
4. **File-to-Task Mapping** — complete table of every changed file → task
5. **Orphaned Files** — files changed that belong to no task
6. **Ghost Tasks** — tasks that claim success but left no code
7. **Summary** — total files changed, total tasks with code, total orphans
8. **Issues / Follow-ups** — anything unexpected

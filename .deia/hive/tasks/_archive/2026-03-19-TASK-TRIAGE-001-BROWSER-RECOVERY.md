# TASK-TRIAGE-001: Browser Recovery Diff Triage

## YOUR ROLE
You are a BEE. Read `.deia/BOOT.md` for your rules.

## Objective
Classify every file that changed in `browser/` and `eggs/` between the `browser-recovery` branch (March 16 baseline) and the `messy-checkpoint-mar19` tag into exactly one triage bucket. Produce a structured report.

## Context
The `browser-recovery` branch was created from current dev, then `browser/` and `eggs/` were reset to the March 16 commit (`ad06402`). The `messy-checkpoint-mar19` tag captures the pre-recovery state (all March 17-19 changes). Your job is to classify what changed between them.

**Only `browser/` and `eggs/` are in scope.** Backend (hivenode/, engine/, .deia/) is out of scope.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\BOOT.md`
- This task file (you're reading it)

## Instructions

### Step 1: Generate the diffs

```bash
# Files changed in browser/
git diff browser-recovery..messy-checkpoint-mar19 --name-status -- browser/

# Files changed in eggs/
git diff browser-recovery..messy-checkpoint-mar19 --name-status -- eggs/

# Stat summary
git diff browser-recovery..messy-checkpoint-mar19 --stat -- browser/ eggs/

# Commit log for browser/eggs changes
git log browser-recovery..messy-checkpoint-mar19 --oneline -- browser/ eggs/
```

### Step 2: For EACH changed file, classify into ONE bucket

| Bucket | Criteria | Action |
|--------|----------|--------|
| **A: Clean** | Change is correct, complete, standalone. Test files: only A if the code they test is also A, OR on the pre-approved list | Cherry-pick |
| **B: Lossy Port** | File was summarized/truncated during platform→shiftcenter migration | Re-port from platform |
| **C: Broken/Tangled** | Change was reverted, re-applied, depends on broken changes, or can't be confidently traced to a single clean intent | Skip, rebuild from spec |
| **C-TEST-RECOVERABLE** | Test file that appears correct but source code is Bucket C | Catalog for future recovery |
| **D: Conflict** | File needs both cherry-pick and lossy port | Hold |
| **INFRA** | package.json, vite.config.ts, vitest.setup.ts, tsconfig*.json | Cherry-pick first in Batch 0 |

### Step 3: Classification Rules

1. **Pre-approved Bucket A** (do NOT reclassify these, they are verified by Q88N):
   - chatRenderer tests (42 tests) — `browser/src/primitives/text-pane/__tests__/chatRenderer*.test.*`
   - canvasEgg tests (31 tests) — `browser/src/eggs/__tests__/canvasEgg.test.ts`

2. **Test file rule:** A test is Bucket A ONLY if:
   - It's on the pre-approved list, OR
   - The source code it tests is also Bucket A

3. **To determine if a change is clean vs tangled:**
   - Read `git log --oneline browser-recovery..messy-checkpoint-mar19 -- <file>` — if file was touched by multiple commits, check if they're coherent
   - If a file was modified, then fixed, then reverted, then re-fixed: that's Bucket C
   - If a file was modified once in one clear commit: likely Bucket A

4. **To check for lossy ports (Bucket B):**
   - Check if the file exists in the `platform` repo at `C:\Users\davee\OneDrive\Documents\GitHub\platform\`
   - If the shiftcenter version is significantly shorter than the platform version (< 80% line count), it may be a lossy port

### Step 4: Write the report

Write to: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\2026-03-19-TRIAGE-001-RESPONSE.md`

Use this format:

```markdown
# Browser Recovery Triage Report

## Summary
- Total browser/ files changed: N
- Total eggs/ files changed: N
- Bucket A (clean, cherry-pick): N
- Bucket A (pre-approved tests): N
- Bucket B (lossy, re-port from platform): N
- Bucket C (broken, rebuild from spec): N
- Bucket C-TEST-RECOVERABLE: N
- Bucket D (conflict, hold): N
- INFRA (cherry-pick first): N

## INFRA Files (Phase 3 Batch 0)
| File | Change Summary | Commit Hash | Risk |
|------|---------------|-------------|------|

## Bucket A — Cherry-Pick Candidates
| File | Change Type | Commit Hash | Notes |
|------|------------|-------------|-------|

## Bucket A — Pre-Approved Tests
| File | Test Count | Verified By |
|------|-----------|-------------|
| chatRenderer tests | 42 | Q88N |
| canvasEgg tests | 31 | Q88N |

## Bucket B — Lossy Ports
| File in shiftcenter | File in platform | Lines (SC) | Lines (platform) | What was lost |
|---------------------|-----------------|------------|------------------|---------------|

## Bucket C — Broken/Tangled (rebuild from spec)
| File | Why Bucket C | Spec in _done/ |
|------|-------------|----------------|

## Bucket C-TEST-RECOVERABLE
| Test File | Test Count | Source Code (Bucket C) | Recovery Plan |
|-----------|-----------|----------------------|---------------|

## Bucket D — Conflicts
| File | Bucket A change | Bucket B issue | Resolution order |
|------|----------------|----------------|-----------------|

## Commit Log Annotation
| Commit | Files | Bucket | Notes |
|--------|-------|--------|-------|
```

## Deliverables
- [ ] Triage report at `.deia/hive/responses/2026-03-19-TRIAGE-001-RESPONSE.md`

## Test Requirements
- No tests required (this is a research/audit task)

## Acceptance Criteria
- [ ] Every changed file in browser/ and eggs/ classified into exactly one bucket
- [ ] Bucket B includes line count comparison (shiftcenter vs platform)
- [ ] Bucket A tests verified against test-follows-code rule
- [ ] Pre-approved tests listed separately, not reclassified
- [ ] Bucket C entries identify the commit(s) that tangled them
- [ ] INFRA files identified separately
- [ ] Commit log annotated with bucket per commit

## Constraints
- Do NOT modify any source files
- Do NOT run git write operations (commit, push, merge, etc.)
- Only read and report
- Platform repo is at: `C:\Users\davee\OneDrive\Documents\GitHub\platform\`

## Response Requirements — MANDATORY
Write response to `.deia/hive/responses/2026-03-19-TRIAGE-001-RESPONSE.md` with all 8 sections per BOOT.md.

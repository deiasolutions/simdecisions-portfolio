---
name: task-file-writer
description: >-
  Write properly formatted task files for hive dispatch with all required
  sections, absolute file paths, three-currency estimates, and response
  requirements template. Use when creating bee assignments, breaking down
  specs into tasks, or coordinating multi-bee work.
license: Proprietary
compatibility: Requires Python 3.12+, access to .deia/hive/tasks/ directory
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: none
    requires_human: false
---

# Task File Writer

## Steps

### Step 1: Determine Task File Name

Task files follow this naming convention:

```
YYYY-MM-DD-HHMM-{AGENT}-{TASK_ID}-ASSIGNMENT.md
```

Examples:
- `2026-04-12-1430-BEE-TASK-042-ASSIGNMENT.md`
- `2026-03-15-0900-Q33N-BUILD-QUEUE-CORE-ASSIGNMENT.md`

**Rules:**
- Use ISO date format YYYY-MM-DD
- Use 24-hour time HHMM
- AGENT is the bee type (BEE, Q33N, Q88NR)
- TASK_ID should match the spec or backlog item ID if available
- Always end with `-ASSIGNMENT.md`

### Step 2: Write Task Header

Start with a clear header:

```markdown
# TASK-{ID}: {Title}

**Date:** YYYY-MM-DD
**Assigned by:** Q33N | Q88N | Q88NR
**Spec dependency:** path/to/spec.md (if applicable)
**Priority:** P0 | P1 | P2 | P3
**Estimated effort:** X bee session(s)
```

### Step 3: Write Objective Section

State what needs to be accomplished in 1-3 concrete sentences. Be specific.

```markdown
## Objective

[What needs to be built, fixed, or investigated]
```

**Anti-pattern:** Vague objectives like "improve performance" or "fix bugs"
**Good pattern:** "Reduce canvas render time from 200ms to <50ms by implementing virtual scrolling in NodeList component"

### Step 4: Write Constraints Section

Document all constraints the bee must follow:

```markdown
## Constraints

- No file over 500 lines
- TDD: write tests first
- No stubs or TODOs
- Must use CSS variables (var(--sd-*)) only — no hardcoded colors
- All file paths must be absolute
- Python 3.12+ | TypeScript 5.x | React 18.x (specify language/framework)
```

Always include the three hard rules that apply to all tasks:
1. No file over 500 lines
2. TDD: tests first
3. No stubs or TODOs

### Step 5: Write Output Files Section

List every file the bee will create or modify, using ABSOLUTE paths:

```markdown
## Output Files

**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\routes\new_feature.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\hivenode\routes\test_new_feature.py`

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\main.py` (add route registration)
```

**NEVER use relative paths.** The bee needs to know exactly where files are.

### Step 6: Write Success Criteria Section

Use checkboxes for each acceptance criterion from the spec:

```markdown
## Success Criteria

- [ ] Feature X implemented and tested
- [ ] All tests pass (minimum 80% coverage)
- [ ] No TypeScript errors
- [ ] No hardcoded colors (CSS vars only)
- [ ] Build passes locally
- [ ] Response file written with all 8 sections
```

### Step 7: Write Three Currencies Estimate

Every task must have time/cost/carbon estimates:

```markdown
## Three Currencies Estimate

| Currency | Estimate |
|----------|----------|
| Clock | 45 minutes |
| Coin | $0.08 USD |
| Carbon | ~5g CO₂e |
```

**Sizing guidance:**
- Small task (< 200 LOC): 30min, $0.05, 3g
- Medium task (200-800 LOC): 1-2hr, $0.10, 8g
- Large task (800-2000 LOC): 4-8hr, $0.25, 20g

### Step 8: Append Response Requirements Template

Every task file MUST end with this exact template:

```markdown
---

## Response Requirements

When you finish, write a response file to `.deia/hive/responses/YYYYMMDD-{TASK-ID}-RESPONSE.md` with these 8 mandatory sections:

### 1. Header
```
# {Task ID}: {Title} -- {STATUS}

**Status:** COMPLETE | FAILED (reason)
**Model:** Haiku | Sonnet | Opus
**Date:** YYYY-MM-DD
```

### 2. Files Modified
Every file you created or modified, with absolute paths.

### 3. What Was Done
Bullet list of concrete changes (not intent).

### 4. Test Results
Number of tests written, pass/fail counts, coverage percentage.

### 5. Build Verification
Did `pytest` pass? Did `npm run build` pass? Any errors?

### 6. Acceptance Criteria
Copy from task file. Mark [x] or [ ] with explanation.

### 7. Three Currencies (Clock, Coin, Carbon)
All three. Never skip any.

Format:
```
| Currency | Actual |
|----------|--------|
| Clock | Xm |
| Coin | $X.XX |
| Carbon | ~Xg CO₂e |
```

### 8. Blockers / Follow-ups
Issues encountered, items deferred, next steps.
```

This template is **mandatory**. Bees that skip sections get their response rejected.

## Output Format

The complete task file structure:

```markdown
# TASK-{ID}: {Title}

**Date:** YYYY-MM-DD
**Assigned by:** {coordinator}
**Spec dependency:** {path}
**Priority:** {P0-P3}
**Estimated effort:** {estimate}

---

## Objective

{1-3 sentences}

---

## Constraints

- {list all constraints}

---

## Output Files

**Files to create:**
- {absolute path}

**Files to modify:**
- {absolute path}

---

## Success Criteria

- [ ] {criterion 1}
- [ ] {criterion 2}

---

## Three Currencies Estimate

| Currency | Estimate |
|----------|----------|
| Clock | {time} |
| Coin | {cost} |
| Carbon | {grams} |

---

## Response Requirements

{paste the 8-section template from Step 8}
```

## Gotchas

### 1. Relative Paths Are Forbidden
Task files with relative paths get rejected. Always use absolute paths like:
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\path\to\file.py` (Windows)
- `/home/user/repo/path/to/file.py` (Linux)

### 2. Missing Response Requirements = Incomplete Task
If you forget to paste the 8-section response requirements template, bees won't know what to report. Q33N will reject the task file and send it back.

### 3. Three Currencies Are Mandatory
All three currencies (Clock, Coin, Carbon) must be present. "Time: 1 hour" without cost and carbon is incomplete.

### 4. Success Criteria Must Match Spec
If the spec says "implement features A, B, C" and your success criteria only mention A and B, the task is incomplete. Copy every acceptance criterion from the spec.

### 5. File Path Windows vs Linux
The repo root path differs between environments:
- Windows (Dave's machine): `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\`
- Linux (Railway/CI): `/app/` or `/workspace/`

Use the actual environment paths. Don't mix Windows and Linux paths in the same task file.

### 6. No Stubs Means No Stubs
"Implement function X" must result in a fully working function, not `def X(): pass` or `// TODO: implement`. If a bee can't complete it, they must say so in the response — not ship a stub.

### 7. Task Files Go in .deia/hive/tasks/
Don't put them in `_outbox/`, `docs/`, or other directories. The queue runner and coordinators look in `.deia/hive/tasks/` only.

### 8. Response Files Go in .deia/hive/responses/
Not in the same directory as task files. Keep them separate for clean archival.

### 9. Batch Task Files Need Coordination Context
If writing multiple task files that work together (e.g., Wave A, Wave B), include a "Dependencies" section listing what each task blocks or depends on.

### 10. [UNDOCUMENTED — needs process doc]
How to handle tasks that require human approval mid-execution (e.g., deployment credentials, destructive operations). Current practice: flag in constraints as "REQUIRES Q88N APPROVAL" but no formal gate exists yet.

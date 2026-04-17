---
name: coordination-briefing-writer
description: >-
  Write sprint coordination briefings that provide context to all bees in a
  sprint covering goals, dependencies between tasks, conventions to follow,
  and what other bees are doing. Use when starting a multi-bee sprint,
  coordinating parallel work, or documenting batch context.
license: Proprietary
compatibility: Requires access to .deia/hive/coordination/ directory
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: none
    requires_human: false
---

# Coordination Briefing Writer

## Steps

### Step 1: Understand What a Briefing Is

A coordination briefing is a context document that all bees in a sprint receive. It prevents bees from working at cross-purposes by documenting:

1. **Sprint goals** — what this batch of work accomplishes
2. **Dependencies between tasks** — what blocks what, what can run in parallel
3. **Conventions to follow** — coding standards, file naming, hard rules
4. **What other bees are doing** — visibility into parallel work

**Briefing ≠ Task File:**
- **Task file** — one-shot assignment for a single bee
- **Briefing** — shared context for multiple bees in the same sprint

### Step 2: Determine Briefing File Name

Briefings follow this naming convention:

```
YYYY-MM-DD-BRIEFING-{SPRINT-NAME}.md
```

Examples:
- `2026-04-12-BRIEFING-BUILD-QUEUE-CORE.md`
- `2026-03-15-BRIEFING-HIVENODE-E2E-WAVE-1.md`
- `2026-03-13-BRIEFING-deployment-wiring.md`

**Rules:**
- Use ISO date format YYYY-MM-DD
- Always include `BRIEFING` in the filename
- Sprint name should be descriptive (< 50 chars)
- Use hyphens, not underscores or spaces

### Step 3: Write Briefing Header

Start with sender, recipient, date, priority, and spec reference:

```markdown
# Briefing: {Sprint Name}

**From:** Q33NR | Q33N
**To:** Q33N | All Bees
**Date:** YYYY-MM-DD
**Priority:** P0 | P1 | P2
**Spec:** path/to/spec.md (if applicable)

---
```

**Priority values:**
- **P0** — critical, blocks alpha release
- **P1** — important, needed for alpha
- **P2** — nice to have, post-alpha

### Step 4: Write Objective Section

State what this sprint accomplishes in 1-2 sentences:

```markdown
## Objective

{What this batch of work delivers, in concrete terms}
```

**Example:**
"Build the core automated build queue infrastructure: queue runner loop, regent bot prompt, queue config, and morning report generator. This enables overnight spec-to-build processing."

### Step 5: Write What We're Building Section (Optional)

If the sprint has multiple phases or complex scope, break it down:

```markdown
## What We're Building

{High-level overview of deliverables}

**Phase 1 deliverables (this briefing):**
1. {Deliverable 1}
2. {Deliverable 2}
3. {Deliverable 3}

**Phase 2 deliverables (future sprint):**
{What comes later}
```

### Step 6: Write Deliverable Sections

For each major deliverable, document:

```markdown
## Deliverable 1: {Name}

**File:** path/to/file.ext

### What It Does

{1-3 sentences describing purpose}

### Key Functions (for code deliverables)

```python
def function_1(args) -> return_type:
    """What this function does."""
```

### Constraints

- {Constraint 1}
- {Constraint 2}

### Dependencies

- Depends on: {other deliverables}
- Blocks: {other deliverables}
```

Repeat for each deliverable.

### Step 7: Write Dependencies Between Tasks Section

Document what blocks what:

```markdown
## Task Dependencies

**Parallel (can run simultaneously):**
- Deliverable 1, 2, 3 (no shared files)

**Sequential (must run in order):**
- Deliverable 4 depends on Deliverable 1, 2, 3 completing
- Deliverable 4 imports from Deliverable 3

**Dispatch recommendation:**
Dispatch 1+2+3 in parallel, then dispatch 4 after they land.
```

This prevents bees from starting work that will conflict.

### Step 8: Write Conventions to Follow Section

Document sprint-wide rules:

```markdown
## Conventions to Follow

**Hard rules (apply to all tasks):**
- No file over 500 lines
- TDD: tests first
- No stubs or TODOs
- All file paths absolute
- Python 3.12+ | TypeScript 5.x | React 18.x

**Sprint-specific rules:**
- All new files go in `.deia/hive/scripts/queue/`
- Use `QueueEvent` dataclass from `event_logger.py`
- Tests go in `.deia/hive/scripts/queue/tests/`
- No external dependencies (pure Python except PyYAML)
```

### Step 9: Write Files to Read First Section

List files that Q33N or bees must read before writing tasks:

```markdown
## Files Q33N Must Read Before Writing Tasks

| File | Why |
|------|-----|
| `docs/specs/SPEC-BUILD-QUEUE-001.md` | The full spec — authoritative source |
| `.deia/BOOT.md` | Hard rules the queue must enforce |
| `.deia/HIVE.md` | Chain of command the queue automates |
| `.deia/hive/scripts/dispatch/dispatch.py` | Dispatch script the queue calls |
| `.deia/config/` | Existing config directory structure |
```

This ensures bees survey before building.

### Step 10: Write Task Breakdown Guidance Section (for Q33N)

If the briefing is for Q33N (who will write task files), provide guidance:

```markdown
## Task Breakdown Guidance

{N} deliverables → {N} task files. Parallelization:

1. **TASK for deliverable 1** — {tier}, {dependencies}, dispatch {when}
2. **TASK for deliverable 2** — {tier}, {dependencies}, dispatch {when}
3. **TASK for deliverable 3** — {tier}, {dependencies}, dispatch {when}
4. **TASK for deliverable 4** — {tier}, {dependencies}, dispatch {when}

**Suggested dispatch order:**
- Dispatch 1+2+3 in parallel
- Dispatch 4 after 1+2+3 complete
```

### Step 11: Write Test Requirements Section

Document minimum test coverage expected:

```markdown
## Test Requirements

- `deliverable_1.py`: test queue sorting, spec parsing, budget enforcement, fix cycle limits, dry-run mode. **Minimum 15 tests.**
- `deliverable_2.py`: test report generation from sample events. **Minimum 5 tests.**
- `deliverable_3.yml`: validation test — load YAML and verify all required keys exist.
- `deliverable_4.md`: no code tests (markdown template), but verify required sections programmatically.

Test files go in `.deia/hive/scripts/queue/tests/`.
```

### Step 12: Write Constraints Section

Document any sprint-wide constraints:

```markdown
## Constraints (apply to all tasks)

- Python 3.13
- No file over 500 lines
- TDD: tests first
- No stubs
- Must use existing `dispatch.py` — never call claude CLI directly
- Queue runner must NOT modify config files, BOOT.md, HIVE.md, or CLAUDE.md
- All paths relative to repo root
```

### Step 13: Save Briefing File

Save to `.deia/hive/coordination/YYYY-MM-DD-BRIEFING-{SPRINT-NAME}.md`

Verify:
- All bees in the sprint will receive this file (or it will be injected into their context)
- Covers all dependencies and conventions
- Specific enough to prevent conflicts

## Output Format

Complete briefing file structure:

```markdown
# Briefing: {Sprint Name}

**From:** Q33NR | Q33N
**To:** Q33N | All Bees
**Date:** YYYY-MM-DD
**Priority:** P0 | P1 | P2
**Spec:** path/to/spec.md

---

## Objective

{1-2 sentences}

---

## What We're Building (optional)

{High-level overview and phase breakdown}

---

## Deliverable 1: {Name}

**File:** path/to/file.ext

### What It Does
{description}

### Key Functions (if code)
{function signatures}

### Constraints
{list}

### Dependencies
{what it depends on, what depends on it}

---

## Deliverable 2: {Name}

{same structure}

---

## Task Dependencies

**Parallel:** {list}
**Sequential:** {list}
**Dispatch recommendation:** {order}

---

## Conventions to Follow

**Hard rules:** {list}
**Sprint-specific rules:** {list}

---

## Files Q33N Must Read Before Writing Tasks

| File | Why |
|------|-----|
| {file} | {reason} |

---

## Task Breakdown Guidance (for Q33N)

{task file recommendations}

---

## Test Requirements

{per-deliverable test expectations}

---

## Constraints (apply to all tasks)

{list}
```

## Gotchas

### 1. Briefings Are Shared Context, Not Assignments
Don't write a briefing that assigns work to a single bee. That's a task file. Briefings are "here's what everyone in this sprint needs to know."

### 2. Dependencies Prevent Conflicts
If two deliverables both modify `main.py`, they CANNOT run in parallel. Document this in "Task Dependencies" so Q33N sequences them.

### 3. Conventions Prevent Rework
If you want all new files in a specific directory, document it in "Conventions" so bees don't put files in the wrong place.

### 4. Files to Read First Ensures Survey
Listing required reading prevents bees from guessing where files are or how systems work. They survey first, then build.

### 5. Briefings Live in .deia/hive/coordination/
Not `.deia/hive/tasks/`, not `docs/`. Coordination files are separate from task files.

### 6. Briefings Are Not Archived
Unlike task files (which move to `_archive/` when done), briefings stay in `.deia/hive/coordination/` for historical reference.

### 7. Update vs Create New
If the same sprint runs in phases, UPDATE the existing briefing (add "Phase 2" section) rather than creating a new file. Exception: if Phase 2 has completely different scope, create a new briefing.

### 8. Q33N vs All Bees
**To: Q33N** — briefing for the coordinator who writes task files
**To: All Bees** — briefing for the worker bees executing tasks

If Q33N writes tasks from the briefing, mark "To: Q33N". If bees receive the briefing directly, mark "To: All Bees".

### 9. Task Breakdown Guidance Is Optional
If the briefing is for worker bees (not Q33N), skip this section. It's only relevant when Q33N is generating task files.

### 10. Specificity Matters
Vague: "Follow best practices"
Specific: "Use `var(--sd-*)` for all colors, no hex codes. See BOOT.md Rule 3."

### 11. [UNDOCUMENTED — needs process doc]
How briefings are injected into bee context. Current practice: Q33N or Q33NR manually includes briefing path in dispatch command. No automated injection mechanism exists.

### 12. [UNDOCUMENTED — needs process doc]
When to write a briefing vs when to use inline task context. Current practice: write briefing if ≥ 3 related tasks, use inline context if 1-2 tasks. No formal threshold exists.

---
name: bee-dispatch
description: >-
  Format and send task files to worker bees via the hive dispatch system.
  Use when preparing bee assignments, writing dispatch prompts, routing
  work through Q33N to the factory, or debugging stuck dispatches. Covers
  task file naming, required sections, dispatch.py usage, injection shims,
  and response file conventions.
license: Proprietary
compatibility: Requires Python 3.12+, hivenode adapters
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: light
    requires_human: false
---

# Bee Dispatch

## When to Use

- Writing a task file for a worker bee (B33)
- Dispatching a coordinator task to Q33N
- Debugging why a dispatch failed or produced no output
- Understanding dispatch mechanics (headless vs. full CLAUDE.md chain)
- Routing work through the queue runner vs. direct dispatch

## Steps

### Step 1: Write the Task File

Task files live in `.deia/hive/tasks/` and follow this structure:

```markdown
# TASK-ID: Title

**Priority:** P0 | P1 | P2
**Assigned Model:** sonnet | haiku | opus
**Role:** bee | queen | regent

## Objective
[What needs to be done, in 1-3 sentences]

## Context
[Background information, links to specs/ADRs, why this task exists]

## Deliverables
- [ ] Concrete output 1 (with absolute file path if file-based)
- [ ] Concrete output 2
- [ ] Tests passing (if applicable)

## Constraints
- [Hard rule or limitation]
- [Another constraint]

## Success Criteria
[How to know the task is complete]

## Three Currencies
- **Clock:** X minutes estimated
- **Coin:** $Y estimated (model invocation cost)
- **Carbon:** Z grams estimated
```

**File naming convention:**
- Format: `YYYY-MM-DD-TASK-<ID>-<slug>.md` or `TASK-<ID>-<slug>.md`
- Examples:
  - `2026-04-12-TASK-SKILL-AUDIT-001.md`
  - `TASK-BEE-DISPATCH-GUIDE.md`
- **For bees:** File MUST be in `.deia/hive/tasks/`
- **For queens:** File can be in `.deia/hive/tasks/` or `.deia/hive/coordination/`

### Step 2: Understand Dispatch Modes

The dispatch script is at `.deia/hive/scripts/dispatch/dispatch.py`.

**Basic usage:**
```bash
# Worker bee (headless, role injected)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/TASK-001.md

# Coordinator (Q33N)
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/coordination/briefing.md \
  --model sonnet \
  --role queen

# Regent (Q33NR)
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/regent-task.md \
  --role regent

# Worker bee with BOOT.md hard rules injected
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/TASK-001.md \
  --inject-boot
```

**Flags:**
- `--model <m>` — Model to use (sonnet | haiku | opus | gpt-4 | gpt-4o | gemini)
- `--role <r>` — Role identity (bee | queen | regent)
- `--inject-boot` — Append BOOT.md hard rules to prompt
- `--no-headless` — Load full CLAUDE.md chain (not recommended for bees)
- `--repo <path>` — Override repo root detection

**Role descriptions (as injected by dispatcher):**
- **bee:** "b33 (worker bee). You write code, run tests, report results. You do NOT orchestrate, delegate, or dispatch other bees. Stay in your lane — only work on the task assigned to you. Do NOT run git commit."
- **queen:** "Q33N (coordinator). You read briefings, write specs, break work into task files, dispatch bees, and review output. You do NOT write code unless explicitly approved."
- **regent:** "Q33NR (regent). You communicate with the human sovereign, delegate to the coordinator, and review results. You do NOT write code, specs, or task files."

### Step 3: Understand Injection Shims

Injection files live at `.deia/config/injections/`:

- `base.md` — Always loaded for all models
- `claude_code.md` — Loaded for sonnet, haiku, opus
- `openai.md` — Loaded for gpt-4, gpt-4o
- `gemini.md` — Loaded for gemini, gemini-2.5-flash

**Injection content (from base.md + model-specific):**
- HIVE DISPATCH PROTOCOL header
- Role-specific instructions
- Chain of command
- Absolute file path rules
- Response file template (8-section format)
- MCP telemetry instructions (optional heartbeat reporting)

**When to use `--inject-boot`:**
- Bee needs the 10 Hard Rules enforced
- Task involves file operations (Hard Rule #4: no file over 500 lines)
- Task involves CSS (Hard Rule #3: no hardcoded colors, `var(--sd-*)` only)
- Task involves tests (Hard Rule #5: TDD)

### Step 4: Response File Convention

Every bee writes a response file to `.deia/hive/responses/` when done.

**File naming:**
- Format: `YYYYMMDD-<TASK-ID>-RESPONSE.md` or `YYYYMMDD-HHMM-BEE-<MODEL>-<TASK-ID>-RAW.txt`
- Examples:
  - `20260412-SKILL-AUDIT-001-RESPONSE.md` (formatted response)
  - `20260412-1246-BEE-HAIKU-2026-04-11-TASK-AUDIT-COMMONS-001-RAW.txt` (raw output)

**Required 8-section structure:**
```markdown
# <Task ID>: <Title> -- <STATUS>

**Status:** COMPLETE | FAILED (reason)
**Model:** Haiku | Sonnet | Opus
**Date:** YYYY-MM-DD

## Files Modified
[Every file touched, absolute paths]

## What Was Done
[Bullet list of concrete changes, not intent]

## Tests Run
[Test commands executed, results]

## Three Currencies Spent
- **Clock:** X minutes actual
- **Coin:** $Y actual
- **Carbon:** Z grams actual

## Blockers Hit
[Any blockers encountered, or "None"]

## Next Steps
[Follow-up tasks needed, or "None — task complete"]

## Notes
[Any clarifications, gotchas, or context]
```

### Step 5: Queue Runner vs. Direct Dispatch

**Direct dispatch (dispatch.py):**
- Manual invocation
- Runs immediately in foreground
- No queue management
- Used for: urgent fixes, one-off tasks, testing dispatch mechanics

**Queue runner (run_queue.py):**
- Automated pickup from `.deia/hive/queue/backlog/`
- Processes P0 → P1 → P2 in order
- Dispatches via dispatch.py internally
- Monitors capacity (max 5 bees in parallel)
- Auto-commits bee output on completion (crash recovery checkpoint)
- Used for: production workflow, batch processing, unattended operation

**How queue runner calls dispatch.py:**
```python
# Simplified from queue/dispatch_handler.py
cmd = [
    "python",
    ".deia/hive/scripts/dispatch/dispatch.py",
    task_file_path,
    "--model", assigned_model,
    "--role", "bee",
    "--inject-boot"
]
subprocess.run(cmd, ...)
```

## Output Format

When dispatching a bee, you should see:

```
[DISPATCH] Task: TASK-001
[DISPATCH] Model: sonnet
[DISPATCH] Role: bee
[DISPATCH] Headless: True
[DISPATCH] Injecting: base.md + claude_code.md
[DISPATCH] Response dir: .deia/hive/responses/
[DISPATCH] Launching...
```

If successful, bee writes to `.deia/hive/responses/<date>-<task-id>-RESPONSE.md`.

If failed, check:
- Task file exists and is .md format
- Task file is in `.deia/hive/tasks/` (for bee role)
- Repo root detected correctly (contains `.deia/` directory)
- Python 3.12+ available
- hivenode.adapters importable (dispatch.py adds repo root to sys.path)

## Gotchas

### 1. File Path Must Be Absolute or Relative to Repo Root

**Bad:**
```bash
python dispatch.py tasks/TASK-001.md
```

**Good:**
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/TASK-001.md
```

### 2. Bees Cannot Dispatch Other Bees

Only Q33N (queen) dispatches bees. If a bee tries to call dispatch.py, this violates Hard Rule #7 (stay in your lane).

**Correct workflow:**
1. Q33N writes task file → `.deia/hive/tasks/TASK-001.md`
2. Q33N dispatches bee via dispatch.py
3. Bee completes work, writes response file
4. Q33N reads response, decides next steps

### 3. Task Files in Wrong Directory

**Symptom:** `[DISPATCH] ERROR: Task file must be in .deia/hive/tasks/`

**Cause:** Task file is outside allowed directory for the role.

**Fix:** Move task file to `.deia/hive/tasks/` (for bee) or `.deia/hive/coordination/` (for queen/regent).

### 4. Injection Files Missing

If `.deia/config/injections/base.md` or model-specific injection is missing, dispatch still proceeds but role identity may not be injected correctly.

**Check:**
```bash
ls .deia/config/injections/
# Should show: base.md, claude_code.md, openai.md, gemini.md
```

### 5. Response File Not Generated

**Possible causes:**
- Bee crashed before writing response (check logs)
- Bee wrote to wrong directory (bee may have misunderstood response file path)
- Output encoding issue (Windows cp1252 vs. UTF-8)

**Debug:**
```bash
# Check for any new files in responses/
ls -lt .deia/hive/responses/ | head -5

# Check bee stdout/stderr (if captured)
# Queue runner logs to queue_runner.log
```

### 6. Git Commit Confusion

**IMPORTANT:** Bees do NOT run `git commit`. The queue runner auto-commits on bee completion as a crash-recovery checkpoint (format: `[BEE-MODEL] SPEC-ID: objective`). This is NOT the same as a production commit — it's a safety checkpoint, no push, no merge.

**Who commits to production:**
- Q88N (Dave) approves via explicit instruction
- Q33NR may commit after Q88N approval
- Never automatic, never without approval

### 7. Dispatch from Wrong Working Directory

**Symptom:** `[DISPATCH] ERROR: Repo root not found`

**Cause:** Running dispatch.py from outside the repo, or repo root detection failed.

**Fix:**
```bash
# Always run from repo root
cd /path/to/simdecisions
python .deia/hive/scripts/dispatch/dispatch.py <task>

# Or use --repo flag
python dispatch.py <task> --repo /path/to/simdecisions
```

### 8. Model vs. Role Confusion

**Old behavior (v1):** Role was inferred from model (e.g., opus = queen).

**New behavior (v2):** Role is explicit via `--role` flag. Model and role are independent.

**Example:**
```bash
# Opus as worker bee (valid)
python dispatch.py task.md --model opus --role bee

# Haiku as queen (valid)
python dispatch.py briefing.md --model haiku --role queen
```

### 9. Heartbeat Reporting (MCP Telemetry)

Bees can optionally report progress via MCP heartbeat tool (port 8421). This is **best-effort** — if MCP server is down, bee continues without blocking.

**Heartbeat fields:**
- `bee_id` — Bot ID from role header
- `task_id` — Task identifier
- `status` — working | blocked | waiting | complete | failed
- `model` — Model name
- `message` — Brief status update (optional)
- `cost_usd` — Total cost if available

**Not documented in dispatch.py itself** — this is handled by injection shims (base.md, claude_code.md).

### 10. No Per-Batch Dispatch Scripts

**Old pattern (DEAD):**
```
_outbox/
  dispatch_wave1.py
  dispatch_wave2.py
  ...
```

**New pattern:**
One script: `dispatch.py`. Reusable. Never write per-batch scripts. Never create `_outbox/` directories.

If you need to dispatch multiple tasks, write a loop or use the queue runner.

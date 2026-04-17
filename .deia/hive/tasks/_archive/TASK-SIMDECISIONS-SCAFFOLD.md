# TASK-SIMDECISIONS-SCAFFOLD

**Task ID:** TASK-SIMDECISIONS-SCAFFOLD
**Created:** 2026-04-10
**Author:** Q33NR
**Assigned to:** BEE (Haiku)
**Model:** haiku
**Role:** bee
**Priority:** P0
**Blocked by:** TASK-SURVEY-FACTORY-GAP-MATRIX (must have response before dispatch)
**Blocks:** BRIEFING-SIMDECISIONS-HANDOFF
**Status:** READY (do not dispatch until survey response exists)
**Parent spec:** docs/specs/SPEC-FACTORY-SELF-REFACTOR-001.md

---

## YOUR ROLE

You are a **bee**. You create files and directories under explicit instruction from this task. You do NOT improvise paths. You do NOT decide what to include beyond the list below. If a step cannot complete, STOP and write the failure to your response file.

---

## Intent

Create a sovereign peer repo `simdecisions/` at the parent directory of `shiftcenter` (peer level, not nested). Populate it with the factory's heartbeat: hive infrastructure, dispatch chain, IR schema, and minimal project metadata. The new repo must pass a dispatch smoke test before you return.

This is Phase 1 of SPEC-FACTORY-SELF-REFACTOR-001. Phase 0 (gap matrix survey) is complete before you start.

---

## Repo Placement — Absolute

`shiftcenter` lives at:
```
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
```

Create `simdecisions` at:
```
C:\Users\davee\OneDrive\Documents\GitHub\simdecisions
```

**Peer level. Not inside shiftcenter. Not a subfolder. Not a git submodule.**

If `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions` already exists, STOP immediately and write "DIRECTORY ALREADY EXISTS — HALTING" to the response file. Do not overwrite.

---

## Directory Structure to Create

Create exactly these directories (empty where noted):

```
simdecisions/
├── .deia/
│   ├── BOOT.md
│   ├── HIVE.md
│   ├── hive/
│   │   ├── tasks/
│   │   │   └── _archive/
│   │   ├── responses/
│   │   ├── coordination/
│   │   └── scripts/
│   │       ├── dispatch/
│   │       └── queue/
│   ├── processes/
│   └── config/
│       └── injections/
├── engine/
│   ├── des/
│   └── phase_ir/
├── src/
│   └── simdecisions/
│       └── adapters/
│           └── cli/
├── hivenode/
│   └── adapters/
│       └── cli/
├── docs/
│   ├── specs/
│   ├── impl/
│   └── adr/
├── tests/
├── README.md
├── pyproject.toml
└── .gitignore
```

---

## Files to Copy (Verbatim)

For each file below, copy from the source path in `shiftcenter` to the destination path in `simdecisions`. Use binary-safe copy. Preserve line endings.

| # | Source (shiftcenter) | Destination (simdecisions) |
|---|---|---|
| 1 | `.deia/BOOT.md` | `.deia/BOOT.md` |
| 2 | `.deia/HIVE.md` | `.deia/HIVE.md` |
| 3 | `.deia/processes/` (entire tree) | `.deia/processes/` |
| 4 | `.deia/config/injections/` (entire tree) | `.deia/config/injections/` |
| 5 | `.deia/hive/scripts/dispatch/dispatch.py` | `src/simdecisions/adapters/cli/dispatch.py` |
| 6 | `.deia/hive/scripts/queue/run_queue.py` | `src/simdecisions/adapters/cli/run_queue.py` |
| 7 | `hivenode/adapters/cli/claude_cli_subprocess.py` | `hivenode/adapters/cli/claude_cli_subprocess.py` |
| 8 | `engine/phase_ir/schema.py` (if exists) | `engine/phase_ir/schema.py` |
| 9 | `engine/phase_ir/validation.py` (if exists) | `engine/phase_ir/validation.py` |

**All 9 source files have been verified by Q33NR to exist in shiftcenter at the paths shown. If any file is missing at copy time, write the missing path to the response file under a "MISSING SOURCE FILES" section. Do NOT fabricate content. Continue with the remaining steps.**

---

## Text Substitution (Only These Files)

After copying, edit **only** these files to replace repo-name references:

1. `simdecisions/.deia/BOOT.md` — replace the string `shiftcenter` with `simdecisions` (case-sensitive, whole word). Document every replacement line in the response file.
2. `simdecisions/README.md` (written fresh, see below)
3. `simdecisions/pyproject.toml` (written fresh, see below)

Do NOT modify any other copied file. Processes and config are repo-agnostic.

---

## New Files to Write

### simdecisions/README.md

```markdown
# simdecisions

Process orchestration engine. Build in progress.

Inherited from shiftcenter on 2026-04-10 per SPEC-FACTORY-SELF-REFACTOR-001.
See `.deia/hive/coordination/BRIEFING-SIMDECISIONS-HANDOFF.md` for build plan.
```

### simdecisions/pyproject.toml

```toml
[project]
name = "simdecisions"
version = "0.0.1"
description = "Process orchestration engine"
requires-python = ">=3.13"
dependencies = []

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
```

### simdecisions/.gitignore

```
__pycache__/
*.pyc
*.pyo
.venv/
venv/
.env
*.log
.deia/hive/event_ledger.db
.deia/hive/*.jsonl
dist/
build/
*.egg-info/
```

---

## Smoke Test (Must Pass Before You Return)

Run this command from inside `simdecisions/`:

```bash
python src/simdecisions/adapters/cli/dispatch.py --help
```

**Expected:** argparse usage message printed, exit code 0.

If the command fails with an ImportError or ModuleNotFoundError, the dispatch.py copy has unresolved imports to paths that don't exist in `simdecisions` yet. Record the exact error in the response file under "SMOKE TEST FAILURE" and STOP.

Do NOT attempt to fix import errors by editing dispatch.py. That is the next task's job. Your job ends at "copy completed, smoke test result recorded."

---

## Acceptance Criteria

- [ ] `simdecisions/` directory exists at peer level to `shiftcenter`
- [ ] All 18 directories listed above exist (verify each)
- [ ] All 9 file copies attempted; any failures logged by path
- [ ] BOOT.md present and contains at least one `simdecisions` reference (post-substitution)
- [ ] README.md, pyproject.toml, .gitignore present with specified content
- [ ] Smoke test executed and result (PASS or exact error) logged
- [ ] Response file written with full manifest

---

## Response File

Write to:
```
shiftcenter/.deia/hive/responses/20260411-SCAFFOLD-COMPLETE.md
```

Response must contain:

1. **Directories created** — full list with existence verification
2. **Files copied** — source → dest for each, with success/fail status and byte count
3. **Missing source files** — any row 7-9 files that didn't exist in shiftcenter
4. **Text substitutions applied** — file path + line number + before/after for every replacement
5. **New files written** — README.md, pyproject.toml, .gitignore with line counts
6. **Smoke test result** — PASS (exit 0) or FAIL (exit code + stderr verbatim)
7. **CLOCK / COIN / CARBON** — measured actuals for this task

---

## Constraints — Absolute

- Do NOT copy anything not on the explicit list above
- Do NOT copy `.deia/hive/tasks/`, `.deia/hive/responses/`, `.deia/hive/coordination/` — those are shiftcenter's operational history and stay here
- Do NOT copy `.env`, `secrets/`, or any credential files — this task does not inherit secrets
- Do NOT initialize git in the new repo — `git init` is a later task
- Do NOT run `pip install` or create a virtualenv — scaffold only
- Do NOT modify anything in `shiftcenter/`
- If any step fails, STOP and report — do not improvise fixes

---

## Two-Phase Gate Notice

This task file has been reviewed by Q33NR for:
- Explicit paths (no guessing)
- Clear halt conditions (directory exists, smoke test fails, missing sources)
- Secrets-inheritance override (Q33NR explicitly removes secret copying from this phase)
- Bounded scope (9 files, 18 directories, 3 new files, 1 smoke test)

Secrets inheritance referenced in SPEC-FACTORY-SELF-REFACTOR-001 is deferred to a later task with explicit Q88N approval. This scaffold does NOT carry credentials.

---

## Smoke Test (for Q33NR verification after dispatch)

```bash
test -d "C:/Users/davee/OneDrive/Documents/GitHub/simdecisions" && echo "REPO EXISTS"
test -f "C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/src/simdecisions/adapters/cli/dispatch.py" && echo "DISPATCH COPIED"
test -f .deia/hive/responses/20260411-SCAFFOLD-COMPLETE.md && echo "RESPONSE WRITTEN"
```

---

*TASK-SIMDECISIONS-SCAFFOLD — Q33NR — 2026-04-10*

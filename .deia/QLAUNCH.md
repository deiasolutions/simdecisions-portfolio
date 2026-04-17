# QLAUNCH — Quick Launch Checklist

Three services to run ShiftCenter locally with build monitoring.

---

## 1. Hivenode (port 8420)

**Check if running:**
```bash
curl -s http://127.0.0.1:8420/health
```
If you get a JSON response, it's already up. Do NOT launch another.

**Launch (if not running):**
```bash
python _tools/hivenode-service.py run
```
Runs uvicorn on `127.0.0.1:8420` with auto-restart on crash. Logs to `.deia/hive/hivenode-service.log`.

**Status shortcut:**
```bash
python _tools/hivenode-service.py status
```

---

## 2. Queue Runner

**Check if running:**
```powershell
Get-WmiObject Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like '*run_queue*' } | Select-Object ProcessId, CommandLine
```
If a process shows up, it's already running. Do NOT launch another.

**Launch (if not running):**
```bash
python .deia/hive/scripts/queue/run_queue.py --watch --adaptive
```
Polls `.deia/hive/queue/` for spec files, dispatches bees via `dispatch.py`, manages slots (10 max concurrent). The `--watch` flag keeps it alive, polling every 30s for new specs. Requires hivenode on 8420 for heartbeats.

---

## 3. Browser Dev Server (port 5173)

**Check if running:**
```bash
curl -s http://localhost:5173
```
If you get HTML back, it's already up. Do NOT launch another.

**Launch (if not running):**
```bash
cd browser && npx vite
```
Vite dev server on `http://localhost:5173`.

**Open build monitor:**
```
http://localhost:5173/?egg=build-monitor
```

---

## All Three (fresh start)

Only if none are running. Run each in a separate terminal:

```
Terminal 1:  python _tools/hivenode-service.py run
Terminal 2:  python .deia/hive/scripts/queue/run_queue.py --watch --adaptive
Terminal 3:  cd browser && npx vite
```

Then open: `http://localhost:5173/?egg=build-monitor`

---

## Queue Spec Submission Guide

To submit work to the queue runner, write a spec file to `.deia/hive/queue/` with filename `SPEC-<ID>-<short-name>.md`.

### Required Sections

The queue runner validates every spec through two gates before dispatch. Both must pass or the spec gets moved to `_needs_review/`.

**Gate 1 — Format Validator** (`spec_validator.py`):

| Section | Required | Format |
|---------|----------|--------|
| `## Priority` | Yes | Line after header: `P0`, `P0.5`, `P0.85`, `P1`, `P2`, or `P3` |
| `## Model Assignment` | Yes | Line after header: `haiku`, `sonnet`, or `opus` |
| `## Objective` | Yes | Non-empty prose paragraph |
| `## Acceptance Criteria` | Yes | Checkbox list: `- [ ] criterion here` (at least 1) |
| `## Test Requirements` | Yes | Checkbox list: `- [ ] test description` (at least 1). Bee writes these tests FIRST (TDD). |
| `## Smoke Test` | Yes | Checkbox list: `- [ ] command here` (at least 1) |
| `## Constraints` | Warn only | Bullet list: `- constraint here` |

**Gate 2 — Gate 0 Validation** (`gate0.py`):

| Check | What it validates |
|-------|-------------------|
| Priority present | `## Priority` section exists with valid P0-P3 value |
| Acceptance criteria present | At least 1 `- [ ]` checkbox in `## Acceptance Criteria` |
| File paths exist | Every path in `## Files to Read First` must exist on disk |
| Deliverables coherence | Deliverables don't forbid modifying files mentioned in acceptance criteria |
| Scope sanity | Objective doesn't reference files that constraints/deliverables forbid editing |
| TDD section present | `## Test Requirements` section exists with at least 1 `- [ ]` checkbox |

### Critical Formatting Rules

1. **Filename MUST contain `SPEC`.** The queue runner globs for `*SPEC*.md`. Files without `SPEC` in the name are invisible to the runner. Convention: `SPEC-<ID>-<short-name>.md` (e.g., `SPEC-BUG-074-remove-layout-menu.md`).
2. **No backticks in file paths.** Gate 0 extracts paths from `## Files to Read First` as plain text. Write `- browser/src/foo.tsx` NOT `` - `browser/src/foo.tsx` ``.
3. **No annotations on the same line as file paths.** Gate 0 treats the entire bullet text as a path. Put annotations on an indented line below:
   ```
   WRONG:  - browser/src/shell/constants.ts (APP_REGISTRY structure)
   RIGHT:  - browser/src/shell/constants.ts
             APP_REGISTRY structure
   ```
4. **Smoke Test must use checkboxes.** Write `- [ ] cd browser && npx vitest run` NOT a code block.
5. **Acceptance Criteria must use checkboxes.** Every criterion needs `- [ ]` prefix.
6. **All paths in Files to Read First must exist.** These are validated against disk. If a file doesn't exist yet, put it in `## Files to Modify` instead (not checked for existence).
7. **Test Requirements must name the test file and specific cases.** Don't write "tests pass" — write the test file path and describe each test the bee must write. The bee writes these tests BEFORE implementation (TDD, BOOT.md Rule 5).

### Optional Sections

| Section | Purpose |
|---------|---------|
| `## Files to Read First` | Files the bee reads before working (validated for existence) |
| `## Files to Modify` | Files the bee will edit or create (NOT validated for existence) |
| `## Deliverables` | Checkbox list of expected outputs |
| `## Problem Analysis` | Context and root cause analysis |
| `## Depends On` | Spec IDs that must be in `_done/` before this runs (bullet list: `- SPEC-ID`). Omit section or leave empty if no dependencies. Do NOT write `- None`. |
| `## Hold` | Timestamp to delay processing: `202603250200` or `2026-03-25-0200` |

### Template

```markdown
# TITLE-HERE

## Objective
What needs to happen and why.

## Problem Analysis
Context, root cause, relevant background.

## Files to Read First
- path/to/existing/file.tsx
  Relevant context about what to look for
- path/to/another/file.ts

## Files to Modify
- path/to/file/that/will/be/edited.tsx
- path/to/new/file/if/needed.ts

## Deliverables
- [ ] Thing one works
- [ ] Thing two works

## Acceptance Criteria
- [ ] First criterion
- [ ] Second criterion

## Test Requirements
- [ ] Tests written FIRST (TDD) — before implementation
- [ ] Test file: path/to/test/file.test.ts
- [ ] Test: description of specific test case
- [ ] Test: description of edge case
- [ ] All tests pass
- [ ] Minimum N tests

## Smoke Test
- [ ] cd browser && npx vitest run src/relevant/ — tests pass
- [ ] cd browser && npx vitest run — no regressions

## Constraints
- No file over 500 lines
- No stubs
- CSS: var(--sd-*) only

## Model Assignment
sonnet

## Priority
P1
```

### Spec Lifecycle

```
queue/SPEC-*.md          → runner picks up on next poll (30s)
  ├─ Gate 1 pass + Gate 0 pass → dispatched to bee
  │   ├─ Success → _done/
  │   └─ Failure → _needs_review/ (or fix cycle)
  ├─ Gate 1 fail → _needs_review/
  └─ Gate 0 fail → _needs_review/
```

### Dependencies

Add a `## Depends On` section with spec IDs. The runner checks `_done/` for each dependency before dispatching.

```markdown
## Depends On
- SPEC-TASK-225
- SPEC-TASK-226
```

---

## Kill Checklist

| Service | How to stop |
|---------|------------|
| Hivenode | Ctrl+C in its terminal, or kill the `python.exe` running `hivenode-service.py` |
| Queue runner | Ctrl+C in its terminal |
| Vite | Ctrl+C in its terminal |
| Orphan bees | Check for stale `node.exe` / `claude` processes after stopping queue runner |

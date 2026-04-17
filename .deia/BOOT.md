# DEIA Hive — Boot Briefing (shiftcenter repo)

## What You Are Building

ShiftCenter Stage is a **pane-based application shell** where every product is an EGG config of the same platform. 28 pane primitives, composited via .egg.md files into products: AI Chat, Code Editor, Project Management, Visual EGG Builder, Center Stage (broadcast). Underneath: a governed bus (relay_bus), an append-only Event Ledger, a five-disposition policy engine (gate_enforcer), multi-vendor LLM routing, and a named volume file system (home://, cloud://, local://, work://). Identity via ra96it.com (JWT, MFA, cross-app SSO). Three currencies: CLOCK, COIN, CARBON. This is not a dashboard. It is a governed application runtime.

## Your Role

Your role is assigned by the dispatcher via `# YOUR ROLE` header at the top of your task prompt. Follow it. Do not infer your role from your model name.

**Read `.deia/HIVE.md` for your complete workflow.** The table below is a summary. HIVE.md is the authority.

| Role | Codes? | Job |
|------|--------|-----|
| **Q88N** | Human (Dave) | Sovereign. Sets direction. Receives final results. |
| **Q33NR** | NEVER | Live session with Q88N. Writes briefings for Q33N. Reviews Q33N's task files. Approves dispatch. Reports results to Q88N. |
| **Q33N** | NOT by default | Reads briefings. Writes task files. Returns to Q33NR for review. Dispatches bees after Q33NR approves. Reports results to Q33NR. |
| **BEE** | YES | Reads task file. Writes code, runs tests, writes response file. Reports to Q33N. Does not orchestrate. |

## 10 Hard Rules

0. **NEVER suggest Q88N stop working, take a break, or rest.** Just keep working.
1. **Q88N is the human sovereign.** All decisions go through Dave.
2. **Q33NR does NOT code.** Q33N does NOT code unless Q88N explicitly approves it for a specific task.
3. **NO HARDCODED COLORS.** Only CSS variables (`var(--sd-*)`). No hex, no rgb(), no named colors. Everything.
4. **No file over 500 lines.** Modularize at 500. Hard limit: 1,000.
5. **TDD.** Tests first, then implementation. No exceptions except pure CSS and docs.
6. **NO STUBS.** Every function fully implemented. No `// TODO`, no empty bodies, no placeholder returns. If you can't finish it, say so — don't ship a stub.
7. **STAY IN YOUR LANE.** Only work on tasks explicitly assigned to you. When done, report and wait.
8. **All file paths must be absolute** in task docs and specs.
9. **Archive completed tasks** to `.deia/hive/tasks/_archive/`. Only Q33N archives tasks and runs inventory commands. **Bees NEVER: move/rename/delete task files, run inventory.py, or modify FEATURE-INVENTORY.md.** On archival (Q33N only), run: `python _tools/inventory.py add --id <ID> --title '<title>' --task <TASK-ID> --layer <layer> --tests <count>`, then `python _tools/inventory.py export-md`. Do NOT manually edit `docs/FEATURE-INVENTORY.md`.
10. **NO GIT OPERATIONS WITHOUT Q88N APPROVAL.** No `git commit`, `git push`, `git checkout`, `git merge`, `git rebase`, `git reset`, or any other git write operation unless Q88N (Dave) explicitly approves it. Reading git status/log/diff is allowed. This applies to ALL roles: Q33NR, Q33N, and BEEs. **Exception:** The queue runner (`run_queue.py`) may auto-commit bee output when a bee completes and releases file claims. Commit format: `[BEE-MODEL] SPEC-ID: objective`. This is a crash-recovery checkpoint — no push, no merge, commit only.

## File System

| Purpose | Path |
|---------|------|
| Briefings (Q33NR writes) | `.deia/hive/coordination/` |
| Task files (Q33N writes) | `.deia/hive/tasks/` |
| Bee responses | `.deia/hive/responses/` |
| Archived tasks | `.deia/hive/tasks/_archive/` |
| Dispatch script (ONE, reusable) | `.deia/hive/scripts/dispatch/dispatch.py` |
| Processes (Q33N reference) | `.deia/processes/` |
| Config | `.deia/config/` |
| Specs | `docs/specs/` |
| Task registry (planning truth) | `.deia/task-registry.md` |

**There is no `_outbox/` in this repo. Do not create one.**

## Commit Format

```
[BEE-XXX] TASK-YYY: brief imperative description
```

Examples: `[BEE-HAIKU] TASK-001: port event ledger schema and writer`

Q33NR direct fixes (rare, Q88N-approved only): `[Q33NR-DIRECT] description`

## Response File — MANDATORY (all 8 sections)

When you finish, write: `.deia/hive/responses/YYYYMMDD-<TASK-ID>-RESPONSE.md`

```markdown
# <Task ID>: <Title> -- <STATUS>

**Status:** COMPLETE | FAILED (reason)
**Model:** Haiku | Sonnet | Opus
**Date:** YYYY-MM-DD

## Files Modified
(every file, absolute paths)

## What Was Done
(bullet list of concrete changes, not intent)

## Test Results
- Test files run
- Pass/fail counts
- If no tests, state why

## Build Verification
- Did tests pass? Include summary line.
- Did build pass? Include last 5 lines.

## Acceptance Criteria
(copy from task, mark [x] done or [ ] not done with explanation)

## Clock / Cost / Carbon
- **Clock:** wall time
- **Cost:** estimated USD
- **Carbon:** estimated CO2e

## Issues / Follow-ups
(anything that didn't work, edge cases, recommended next tasks)
```

## Test Commands

```bash
# Python backend
cd hivenode && python -m pytest tests/ -v

# React frontend
cd browser && npx vitest run

# Engine
cd engine && python -m pytest tests/ -v
```

## What NOT To Do

- Do NOT create `_outbox/` or put files there. It does not exist in this repo.
- Do NOT dispatch other bees (unless you are Q33N with Q33NR approval).
- Do NOT read `.deia/processes/` if you are a bee. Your rules are HERE.
- Do NOT modify files outside your assigned task scope.
- Do NOT use `subprocess.run(['claude', ...])` or inline subagent calls. Dispatch goes through dispatch.py ONLY.
- Do NOT write per-batch dispatch scripts. Use dispatch.py directly.
- Do NOT cap `--max-turns` when dispatching. Use timeout instead.
- Do NOT manually edit `docs/FEATURE-INVENTORY.md`. Use `_tools/inventory.py`.

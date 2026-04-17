# BRIEFING: Forensic Mining — Reconstruct Every Lost Task

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15 ~18:45
**Priority:** P0 — blocking all rebuild work

---

## Situation

A `git reset --hard HEAD` wiped all uncommitted tracked-file modifications. We need to reconstruct every original task that was lost, exactly as it was, so we can re-execute them in proper order.

## Your Job

Dispatch mining bees. Each bee reconstructs ONE original task (or a small batch of tiny related tasks). The bee reads sources, finds exactly what that task did, and writes a complete **reconstructed task file** that an implementation bee can re-execute.

The output is NOT organized by file. It is organized by TASK. One reconstructed task per original task.

## Lost Files Filter

Only reconstruct tasks that modified these tracked files (all wiped by the reset):

```
browser/src/apps/index.ts
browser/src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx
browser/src/shell/components/__tests__/SpotlightOverlay.test.tsx
browser/src/shell/components/ShellTabBar.tsx
browser/src/shell/components/WorkspaceBar.tsx
browser/src/shell/components/shell.css (menu bar CSS — Q33NR session, not a task)
browser/src/primitives/terminal/types.ts
browser/src/primitives/terminal/useTerminal.ts
engine/des/engine.py
eggs/sim.egg.md
hivenode/config.py
hivenode/dependencies.py
hivenode/main.py
hivenode/rag/indexer/__init__.py
hivenode/rag/indexer/indexer_service.py
hivenode/rag/indexer/storage.py
hivenode/routes/__init__.py
hivenode/routes/auth.py
hivenode/routes/sim.py
hivenode/schemas_sim.py
pyproject.toml
ra96it/config.py
ra96it/main.py
ra96it/models.py
ra96it/schemas.py
ra96it/services/jwt.py
tests/engine/des/test_des_ledger_emission.py
tests/hivenode/conftest.py
tests/hivenode/test_auth_routes.py
tests/hivenode/test_sim_routes.py
tests/hivenode/rag/test_rag_routes.py
```

Do NOT reconstruct tasks that only created new files (those survived as untracked). Do NOT reconstruct TASK-168 through TASK-172 (pane chrome) — those files are still dirty in the working tree and appear intact.

## The 10 Source Types (descending order of usefulness)

Bees search in this order. Stop early if confident.

| # | Source Type | Location | What It Contains |
|---|-------------|----------|------------------|
| 1 | **RAW transcripts** | `.deia/hive/responses/20260315-*-RAW.txt` | Full bee session logs with EXACT Edit tool calls (old_string, new_string). **Best source.** |
| 2 | **TASK response files** | `.deia/hive/responses/20260315-TASK-*-RESPONSE.md` | Structured summaries: files modified, what was done, line numbers |
| 3 | **Surviving test files** | `tests/` and `browser/src/**/__tests__/` (untracked) | Exact imports, assertions, expected behavior |
| 4 | **Surviving source files** | Untracked `.py`, `.ts`, `.tsx` that were created (not modified) | Code that depends on the lost modifications |
| 5 | **Task files** | `.deia/hive/tasks/2026-03-15-TASK-*.md` | Original instructions, deliverables, acceptance criteria |
| 6 | **Rebuild specs (in _hold)** | `.deia/hive/queue/_hold/2026-03-15-1745-SPEC-rebuild-*.md` | 8 existing rebuild specs with source references |
| 7 | **Coordination files** | `.deia/hive/coordination/2026-03-15-*.md` | Briefings, dispatch files, completion reports |
| 8 | **Platform source** | `C:\Users\davee\OneDrive\Documents\GitHub\platform\` | Upstream code things were ported from |
| 9 | **JSONL event capture logs** | `C:\Users\davee\.claude\projects\C--Users-davee-OneDrive-Documents-GitHub-shiftcenter\` | Every tool_use event from all Claude sessions today |
| 10 | **Queue specs** | `.deia/hive/queue/` and `.deia/hive/queue/_done/` | Objectives and acceptance criteria |

### How to find the right RAW transcript for a task

Pattern: `20260315-BEE-{MODEL}-2026-03-15-TASK-{NUM}-{SHORT-NAME}-RAW.txt`
Search: `grep -rl "TASK-{NUM}" .deia/hive/responses/*-RAW.txt`

## Tasks to Reconstruct

22 tasks touched lost tracked files. Each needs full reconstruction.

| Task | What It Did | Tracked Files Modified |
|------|-------------|----------------------|
| TASK-126A | Inventory store init in hivenode | hivenode/main.py |
| TASK-126B | Kanban PG wiring | hivenode/config.py, hivenode/routes/kanban_routes.py, tests/hivenode/test_kanban_routes.py |
| TASK-132 | DES engine import fix | pyproject.toml, tests/engine/des/test_des_ledger_emission.py |
| TASK-133 | Spotlight test selector fix | browser/src/shell/components/__tests__/SpotlightOverlay.test.tsx |
| TASK-136 | ra96it GitHub OAuth + JWKS | ra96it/models.py, ra96it/schemas.py, ra96it/config.py, ra96it/services/jwt.py, ra96it/main.py |
| TASK-137 | Browser auth adapter registration | browser/src/apps/index.ts |
| TASK-138 | Hivenode JWKS cache + dual audience | hivenode/dependencies.py, hivenode/config.py, hivenode/main.py, hivenode/routes/auth.py, tests/hivenode/conftest.py, tests/hivenode/test_auth_routes.py |
| TASK-139 | FileOperations mock restructure | browser/src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx |
| TASK-140 | Sim shell integration + app registration | browser/src/apps/index.ts, eggs/sim.egg.md |
| TASK-141 | Sim engine integration (stubs → real) | hivenode/routes/sim.py, hivenode/schemas_sim.py, tests/hivenode/test_sim_routes.py, engine/des/engine.py |
| TASK-146 | DES routes port + registration | hivenode/routes/__init__.py |
| TASK-151 | RAG models port | hivenode/rag/indexer/__init__.py, hivenode/rag/indexer/indexer_service.py |
| TASK-152 | RAG scanner port | hivenode/rag/indexer/__init__.py, hivenode/rag/indexer/indexer_service.py |
| TASK-153 | RAG chunker port | hivenode/rag/indexer/__init__.py |
| TASK-155 | RAG storage port | hivenode/rag/indexer/__init__.py |
| TASK-156 | RAG indexer service repair | hivenode/rag/indexer/indexer_service.py, hivenode/rag/indexer/storage.py |
| TASK-157 | RAG routes port + registration | hivenode/routes/__init__.py |
| TASK-158 | Shell chrome CSS var fixes | browser/src/shell/components/ShellTabBar.tsx, browser/src/shell/components/WorkspaceBar.tsx |
| TASK-161 | RAG indexer __init__ + __all__ fix | hivenode/rag/indexer/__init__.py |
| TASK-163 | RAG routes test additions | tests/hivenode/rag/test_rag_routes.py |
| TASK-165 | Canvas chat routes + registration | hivenode/routes/__init__.py |
| TASK-166 | Terminal canvas wiring | browser/src/primitives/terminal/types.ts, browser/src/primitives/terminal/useTerminal.ts |

Plus one non-task item:
- **Menu bar CSS** (Q33NR session work) — shell.css needs ~150 lines from `platform/simdecisions-2/src/components/shell/shell.css` lines 551-730

## Reconstructed Task Output Format

Each bee writes to `.deia/hive/tasks/`:
```
.deia/hive/tasks/2026-03-15-REBUILD-{TASK-NUM}.md
```

Each reconstructed task MUST contain:

```markdown
# REBUILD-{TASK-NUM}: {Original Title}

## Original Task
{TASK-NUM} — {one-line description}

## Timestamp
When the original task was executed (from response file date/time)

## Files to Modify
- {exact path} — {what changes}

## Exact Edits
For each file, the precise old_string → new_string:

### {filename}
**Edit 1:**
old_string: ```
{exact text to find}
```
new_string: ```
{exact replacement}
```

## Dependencies
Which other REBUILD tasks must complete before this one (if any)

## Sources Used
- {source type #} {source name}: {files read}

## Sources Skipped
- {source type #} {reason for skipping}

## Confidence
HIGH | MEDIUM | LOW — {explanation}
```

## Dispatch Plan

22 tasks + 1 session fix = 23 items. Batch tiny tasks where sensible.

Suggested bee assignments (Q33N may adjust):

| Bee | Tasks | Rationale |
|-----|-------|-----------|
| 1 | TASK-126A, TASK-126B | Related (both Kanban/PG), share hivenode/config.py |
| 2 | TASK-132, TASK-133, TASK-139 | All tiny test/config fixes |
| 3 | TASK-136 | Large (5 ra96it files) |
| 4 | TASK-137, TASK-140 | Both modify browser/src/apps/index.ts |
| 5 | TASK-138 | Large (6 hivenode files) |
| 6 | TASK-141 | Large (4 files, complex stubs→real) |
| 7 | TASK-146, TASK-157, TASK-165 | All add routes to __init__.py |
| 8 | TASK-151, TASK-152, TASK-153, TASK-155, TASK-156, TASK-161 | All RAG indexer, layered on same files |
| 9 | TASK-158, menu bar CSS | Both shell CSS changes |
| 10 | TASK-163, TASK-166 | Remaining: RAG test + terminal canvas |

10 bees, 2 waves of 5:
- **Wave 1:** Bees 1-5
- **Wave 2:** Bees 6-10

All haiku model. Research only — no source code modifications.

## Constraints

- Bees do NOT modify source code. Read-only research + write task files.
- Search sources in descending order (1→10). Stop early if confident.
- Every edit must be exact old_string → new_string. No "add something like this."
- Include timestamps so we can see execution order.
- If a bee cannot find exact diffs, mark confidence LOW and explain what's missing.
- Report every file read and every source type used/skipped.

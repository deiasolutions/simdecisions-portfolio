# BRIEFING: Q33N-001 — Redo 30-Item Punch List (Carefully)

**From:** Q33NR
**To:** Q33N-001
**Date:** 2026-03-19
**Priority:** P0

---

## Context

On March 17, we dispatched 30 specs via the queue runner overnight. The bees ran unsupervised and caused widespread damage — wandering outside file scope, breaking tests, and tangling changes across files. We spent March 19 doing a full browser recovery: reset browser/ to March 16 baseline, triaged 30 files, and rebuilt 7 features via 5 targeted bees (170+ tests, zero regressions).

**The codebase is now stable on `dev` branch.** We need to redo the remaining 20 items from the punch list — carefully, in small batches, with tight file-scope constraints.

## Your Role

You are Q33N-001. Read `.deia/BOOT.md` and `.deia/HIVE.md` first. Your job:

1. Read each spec from the list below (they're in `.deia/hive/queue/_done/`)
2. Read the current codebase to understand what exists
3. Write task files for the FIRST BATCH ONLY (3-5 items, backend-first)
4. Each task file MUST include explicit "Files You May Modify" and "Files You Must NOT Modify" sections
5. Return the task files to Q33NR for review — do NOT dispatch bees

## Critical Rules for Task Files

These rules exist because the last batch broke everything:

1. **Explicit file boundaries** — Every task file must list exactly which files the bee may touch. Everything else is off-limits.
2. **No browser/ modifications in backend tasks** — Backend specs must NOT touch browser/ files. Period.
3. **No cross-primitive modifications** — A canvas fix must NOT touch terminal/, chat/, or tree-browser/. Stay in lane.
4. **Maximum 3 files modified per task** — If a task needs more than 3 source files changed, split it.
5. **Tests in same primitive only** — Test files must be co-located with the code they test.
6. **Build verification required** — Every task must include "run vite build" or "run pytest" as acceptance criteria.

## 20 Remaining Items

### Backend (do these first — lower risk)
| ID | Spec File | Description |
|----|-----------|-------------|
| TASK-228 | 2026-03-16-SPEC-TASK-228-des-pipeline-runner.md | DES pipeline runner |
| TASK-243 | 2026-03-16-SPEC-TASK-243-global-commons-phase-a.md | Global commons phase A |
| BL-070 | 2026-03-17-SPEC-TASK-BL070-wire-envelope-handlers.md | Envelope handler wiring |
| BL-110 | 2026-03-17-SPEC-TASK-BL110-status-system-alignment.md | Status system alignment |
| BL-203 | 2026-03-17-SPEC-TASK-BL203-split-heartbeat.md | Heartbeat split |

### Browser — UI Polish
| ID | Spec File | Description |
|----|-----------|-------------|
| TASK-230 | 2026-03-16-SPEC-TASK-230-terminal-command-history.md | Terminal command history |
| TASK-231 | 2026-03-16-SPEC-TASK-231-seamless-pane-borders.md | Seamless pane borders |
| TASK-232 | 2026-03-16-SPEC-TASK-232-expandable-terminal-input.md | Expandable terminal input |
| TASK-235 | 2026-03-16-SPEC-TASK-235-loading-states.md | Loading state indicators |
| BL-023 | 2026-03-17-SPEC-TASK-BL023-shell-swap-merge.md | Shell swap/merge |
| BL-208 | 2026-03-17-SPEC-TASK-BL208-app-directory-sort-order.md | App directory sort order |
| BL-209 | 2026-03-17-SPEC-TASK-BL209-processing-primitive-layout.md | Processing primitive layout |

### Browser — Canvas/Bug Fixes
| ID | Spec File | Description |
|----|-----------|-------------|
| BUG-015 | 2026-03-17-SPEC-TASK-BUG015-drag-pane-into-stage.md | Drag pane onto occupied stage |
| BUG-018 | 2026-03-17-SPEC-TASK-BUG018-canvas-ir-wrong-pane.md | Canvas IR routes to wrong pane |
| BUG-019 | 2026-03-17-SPEC-TASK-BUG019-canvas-drag-captured-by-stage.md | Canvas drag captured by stage |
| BUG-020 | 2026-03-17-SPEC-TASK-BUG020-canvas-ir-terminal-hides-response.md | Canvas IR terminal hides response |
| BUG-025 | 2026-03-17-SPEC-TASK-BUG025-sim-egg-fails.md | Sim EGG test failures |
| BUG-027 | 2026-03-17-SPEC-TASK-BUG027-turtle-draw-unregistered.md | Turtle draw unregistered |
| BUG-028 | 2026-03-17-SPEC-TASK-BUG028-efemera-channels-not-wired.md | Efemera channels not wired |
| BUG-029 | 2026-03-17-SPEC-TASK-BUG029-stage-app-add-warning.md | Stage app add warning |
| BUG-031 | 2026-03-17-SPEC-TASK-BUG031-code-explorer-click-error.md | Code explorer click error |

### Infra/Auth
| ID | Spec File | Description |
|----|-----------|-------------|
| TASK-239 | 2026-03-16-SPEC-TASK-239-efemera-egg-verified.md | Efemera EGG verified |
| TASK-240 | 2026-03-16-SPEC-TASK-240-keyboard-shortcuts.md | Keyboard shortcuts |
| TASK-241 | 2026-03-16-SPEC-TASK-241-production-url-smoke-test.md | Production URL smoke test |
| TASK-242 | 2026-03-16-SPEC-TASK-242-full-smoke-test-suite.md | Full smoke test suite |
| TASK-244 | 2026-03-16-SPEC-TASK-244-landing-page.md | Landing page |
| TASK-245 | 2026-03-16-SPEC-TASK-245-ra96it-signup-flow.md | ra96it signup flow |

## Batch Strategy

**Batch 1 (NOW):** Pick 3-5 backend items. Write task files. Return for review.
**Batch 2-N:** After Batch 1 bees complete and pass review, pick the next 3-5. Repeat.

Do NOT write task files for all 20 at once. One batch at a time.

## Deliverables

1. Task files for Batch 1 (3-5 items) written to `.deia/hive/tasks/`
2. Summary of what each task covers and why you chose these for Batch 1
3. Wait for Q33NR review before dispatching

---

**Remember:** Read BOOT.md and HIVE.md first. Stay in your lane. The last batch broke everything because nobody enforced boundaries. This time we do it right.

# BRIEFING-BUILD-QUEUE-CORE: Task Files Written

**Bot:** Q33N
**Date:** 2026-03-11
**Briefing:** `.deia/hive/coordination/2026-03-11-BRIEFING-BUILD-QUEUE-CORE.md`
**Status:** Task files ready for Q33NR review

---

## Task Files Created

I've written **4 task files** for Phase 1 of SPEC-BUILD-QUEUE-001 (Core Queue Infrastructure):

| Task ID | Title | Model | Size | Dependencies |
|---------|-------|-------|------|-------------|
| **TASK-023A** | Queue Config YAML | **Haiku** | Small | None (standalone) |
| **TASK-023B** | Regent Bot Prompt Template | **Haiku** | Small | None (standalone) |
| **TASK-023C** | Morning Report Generator | **Sonnet** | Medium | None (defines QueueEvent for 023D) |
| **TASK-023D** | Queue Runner Script | **Sonnet** | Large | 023A (config), 023C (imports) |

### File Paths (absolute)

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-11-TASK-023A-QUEUE-CONFIG.md`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-11-TASK-023B-REGENT-PROMPT.md`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-11-TASK-023C-MORNING-REPORT.md`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-11-TASK-023D-QUEUE-RUNNER.md`

---

## Task Breakdown Summary

### TASK-023A: Queue Config YAML (Haiku)
**What:** Create `.deia/config/queue.yml` with budget, models, paths, deploy, git sections.

**Deliverables:**
- Budget: max_session_usd=20.00, warn_threshold=0.80, max_fix_cycles=2, max_specs=50, max_parallel_bees=3
- Models: regent=ollama:llama3.1:8b, q33n=sonnet-4-6, bee_default=haiku-4-5, bee_complex=sonnet-4-6
- Paths: queue_dir, needs_review_dir, done_dir, smoke_dir, coordination_dir, tasks_dir, responses_dir
- Deploy: Railway + Vercel health URLs, poll intervals
- Git: branch=dev, commit_prefix=[Q33N], auto_push=true

**Tests:** 7 tests — validation that all sections exist and have correct types.

**Why Haiku:** Trivial config file, no complex logic.

---

### TASK-023B: Regent Bot Prompt Template (Haiku)
**What:** Create `.deia/config/regent-bot-prompt.md` — the system prompt for Q88NR-bot.

**Deliverables:**
- Identity: "You are Q88NR-bot, mechanical regent"
- Abbreviated HIVE.md chain
- Mechanical review checklist for Q33N's task files (deliverables match spec? paths absolute? tests present? CSS vars? under 500 lines? no stubs?)
- Correction rule: max 2 cycles, then APPROVED_WITH_WARNINGS
- Fix cycle rule: max 2 fix cycles, then NEEDS_DAVE
- Budget awareness: "Report costs, runner enforces limits"
- What you NEVER do: strategic decisions, modify specs, override rules, code, skip Q33N

**Tests:** 5 tests — file exists, contains required sections, line count 50-300, contains required keywords, does NOT contain strategic language.

**Why Haiku:** Small markdown template, mechanical checklist.

**Target length:** 100-200 lines.

---

### TASK-023C: Morning Report Generator (Sonnet)
**What:** Create `.deia/hive/scripts/queue/morning_report.py` — reads session event log, generates markdown report.

**Deliverables:**
- `QueueEvent` dataclass: event_type, timestamp, spec_id, cost_usd, duration_ms, model_used, details
- `generate_morning_report(session_events, queue_dir, output_path) -> Path`
- Report sections: Queue Summary (counts, cost, duration), Completed (table), Needs Review (table), Screenshots (paths), Remaining Queue (unprocessed files)
- Pure Python, stdlib only
- Under 500 lines

**Tests:** 5+ tests — empty events, all succeeded, all failed, mixed, zero cost, duration calculation, remaining queue detection.

**Why Sonnet:** Medium complexity — needs to parse events, compute aggregates, generate structured markdown, handle edge cases.

**Dependencies:** None (but TASK-023D will import from this).

---

### TASK-023D: Queue Runner Script (Sonnet)
**What:** Create `.deia/hive/scripts/queue/run_queue.py` — the core orchestration loop.

**Deliverables:**
- CLI: `python run_queue.py [--config path] [--dry-run]`
- `load_queue(queue_dir) -> list[SpecFile]` — find .md files, sort by priority (P0/P1/P2) then filename
- `parse_spec(spec_path) -> SpecFile` — extract priority, objective, acceptance criteria, model, smoke test from markdown
- `process_spec(spec, config, session_events) -> SpecResult` — dispatch Q88NR-bot via dispatch.py, track cost, log events
- `run_queue(queue_dir, config_path, dry_run)` — main loop
- Budget enforcement: warn at 80%, stop at 100%
- Fix cycle logic: P0 fix specs, max 2 cycles, then _needs_review/
- Event logging: session-YYYY-MM-DD-HHMM.json
- File movement: CLEAN → _done/, NEEDS_DAVE → _needs_review/
- Call `generate_morning_report()` at end
- Use dispatch.py for ALL dispatches
- Under 500 lines (split into modules if over)

**Tests:** 15+ tests — queue sorting, spec parsing, budget warn/stop, fix cycles, dry-run, empty queue, config loading, event logging, file movement, morning report call.

**Why Sonnet:** Most complex deliverable — orchestration, budget tracking, file management, spec parsing, event logging.

**Dependencies:**
- Imports `generate_morning_report()` and `QueueEvent` from TASK-023C
- Reads config from TASK-023A (queue.yml)
- Calls dispatch.py (already exists)

---

## Dispatch Strategy

**Parallel batch 1 (independent):**
- TASK-023A (config) — Haiku
- TASK-023B (prompt) — Haiku
- TASK-023C (report generator) — Sonnet

**Sequential batch 2 (depends on 023C):**
- TASK-023D (runner) — Sonnet (imports from 023C)

### Commands

```bash
# Batch 1 (parallel)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-11-TASK-023A-QUEUE-CONFIG.md --model haiku --role bee --inject-boot &
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-11-TASK-023B-REGENT-PROMPT.md --model haiku --role bee --inject-boot &
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-11-TASK-023C-MORNING-REPORT.md --model sonnet --role bee --inject-boot &

# Wait for batch 1 to complete, then:

# Batch 2 (sequential)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-11-TASK-023D-QUEUE-RUNNER.md --model sonnet --role bee --inject-boot
```

---

## Constraints Enforced in All Tasks

✅ **All file paths are absolute** (Windows paths with full drive letters)
✅ **TDD required** — tests written first
✅ **No file over 500 lines** — TASK-023D may need modularization
✅ **No stubs** — everything fully implemented
✅ **8-section response file format** enforced in every task
✅ **Python 3.13** for all Python code
✅ **CSS var(--sd-*)** — N/A (no UI code in this batch)
✅ **Uses dispatch.py** — never calls claude CLI directly
✅ **Must NOT modify** `.deia/config/`, `.deia/BOOT.md`, `.deia/HIVE.md`, `CLAUDE.md` (read-only)

---

## Test Coverage

| Task | Test File | Min Tests | Focus |
|------|-----------|-----------|-------|
| 023A | test_queue_config.py | 7 | YAML validation (all keys exist, correct types) |
| 023B | test_regent_prompt.py | 5 | Markdown structure, keywords, line count, no strategic language |
| 023C | test_morning_report.py | 5 | Report generation from sample events, edge cases |
| 023D | test_run_queue.py | 15 | Queue sorting, spec parsing, budget, fix cycles, dry-run, events, file movement |

**Total:** 32+ tests across 4 deliverables.

---

## What's NOT in Scope (Phase 2)

These are explicitly Phase 1 only:
- ✅ Queue runner loop
- ✅ Regent prompt template
- ✅ Queue config
- ✅ Morning report generator

Phase 2 (future):
- ❌ Smoke test scripts (Playwright)
- ❌ Spec-specific smoke test generator
- ❌ Fix spec generator (error report → fix spec)
- ❌ Railway deploy polling
- ❌ Event Ledger integration
- ❌ `hive dispatch-queue` CLI entry point

Per briefing: "Smoke test scripts come in Phase 2 after we verify the core loop works."

---

## Review Checklist for Q33NR

**Before approving dispatch, verify:**

- [ ] All 4 task files have absolute paths (Windows format)
- [ ] Test requirements present in every task (TDD)
- [ ] 8-section response format required in every task
- [ ] No stubs mentioned as acceptable
- [ ] Files under 500 lines (with guidance to modularize if over)
- [ ] Model assignments: 023A=Haiku, 023B=Haiku, 023C=Sonnet, 023D=Sonnet
- [ ] TASK-023D imports from TASK-023C (dependency explicit)
- [ ] TASK-023D reads TASK-023A config (dependency explicit)
- [ ] All tasks reference the spec (`docs/specs/SPEC-BUILD-QUEUE-001.md`)
- [ ] Dispatch strategy is parallel for 023A/023B/023C, sequential for 023D
- [ ] No hardcoded colors (N/A — no UI code)
- [ ] Uses dispatch.py (023D explicitly required)
- [ ] Does NOT modify `.deia/config/`, `BOOT.md`, `HIVE.md`, `CLAUDE.md`

---

## Ready for Review

All task files are written and ready for Q33NR's review. Please verify against the checklist above and approve dispatch.

**Awaiting Q33NR approval to dispatch bees.**

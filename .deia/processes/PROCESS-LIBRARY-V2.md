# DEIA Process Library v2 — shiftcenter

**Version:** 2.0
**Date:** 2026-03-10
**Authority:** Q88N (Dave) × Q33NR (Claude)

This is a COORDINATOR reference. Bees do not read this file. Q33N reads it when planning sprints. Q33NR reads it when reviewing. The coordinator EXTRACTS relevant rules and INJECTS them into task files.

---

## P-01: Task Lifecycle

**queue → claimed → buzz → archive**

1. Q33N writes task file to `.deia/hive/tasks/`
2. Bee claims by starting work (claim logged in response header)
3. Bee executes (buzz). Writes response to `.deia/hive/responses/`
4. Q33N reviews response. If accepted: move task to `.deia/hive/tasks/_archive/`

A task is NOT done until archived. Unarchived tasks pollute the queue. Q33N enforces at sprint close.

---

## P-02: Process Discovery & Creation

Before any new workflow: search `.deia/processes/` for an existing process. If not found, create one following this format: Title, Rule, When to Apply, Steps, Success Criteria, Rollback. Submit to Q33NR for review. Processes are community-owned after review.

---

## P-03: Bee Dispatch Standard

**Always use dispatch.py.** No one-off scripts, no raw `claude -p`, no inline subagent tools.

```
python .deia/hive/scripts/dispatch/dispatch.py <task_file> --model <model> --role <role>
```

Rules:
- `--output-format json` (automatic in dispatch.py) for structured telemetry
- NEVER set `--max-turns`. Use `--timeout` instead.
- ALWAYS dispatch in background (`run_in_background: true`)
- Parallel when tasks are independent. Sequential when dependent.
- Headless by default. `--no-headless` only when bee needs full repo context.
- `--inject-boot` appends BOOT.md hard rules to every bee prompt.

Telemetry captured: num_turns, cost_usd, duration, input/output tokens, cache hit rate, session_id.

---

## P-04: Build Integrity — 3-Phase Validation

Three acts. Never skip one.

**Act 1 — Validate the Plan.** Before coding, verify: task file is complete, deliverables are concrete, file paths exist, no ambiguity. If the plan is wrong, the code will be wrong.

**Act 2 — Execute with Self-Check.** TDD cycle: write test (red) → write code (green) → refactor. Round-trip validation: if you changed a function signature, verify all callers. If you changed a schema, verify all queries.

**Act 3 — Validate Output.** All tests pass. Build passes. Response file has all 8 sections. Acceptance criteria checked. No stubs. No hardcoded colors. No files over 500 lines.

The bee that builds a component NEVER tests it in isolation without the behavioral scenarios from the task file. A separate reviewer verifies.

---

## P-05: Test-Driven Development

**Mandatory for all code changes.** Exceptions: pure CSS, documentation, config files.

1. Read task spec completely
2. Write tests FIRST (must FAIL before implementation)
3. Write minimal code to pass
4. Run tests (must PASS)
5. Refactor if needed
6. Test edge cases (empty inputs, null values, boundary conditions, error paths)
7. Report test results in response file (counts, coverage, specific cases)

Minimum: 80% coverage for unit tests. All error conditions tested. Emergency hotfixes: fix first, write tests within 24 hours.

---

## P-06: Code Audit Quality Standards

When assigned an audit task:

1. **READ THE ACTUAL CODE.** Do not describe code from memory. Paste it.
2. **TRACE THE PATH.** Entry point → flagged line. Confirm no guards exist above.
3. **KNOW THE FRAMEWORK.** React mount-only effects are correct. FastAPI supports dict in HTTPException. Don't flag framework patterns as bugs.
4. **SEVERITY MUST MATCH IMPACT.** P0 = confirmed data loss/auth bypass that WILL happen. "Could theoretically happen if..." is not P0.
5. **COMPANION REPORTS INDEPENDENTLY VERIFY.** Don't just "concur." Re-trace. Attempt to disprove.

Findings with LOW confidence go in a separate "Needs Verification" section.

---

## P-07: Bee Response Format

**MANDATORY for every task.** Q33N pastes this template into every task file.

8 sections required: Header, Files Modified, What Was Done, Test Results, Build Verification, Acceptance Criteria, Clock/Cost/Carbon, Issues/Follow-ups.

Full template is in BOOT.md. A response missing any section is incomplete — send it back.

---

## P-08: Batch Work Breakdown

When Q88N approves multiple items at once:

1. **TRIAGE:** Classify each item (haiku/sonnet/opus, code/research/clerical/strategic, dependencies, parallelizable?)
2. **BATCH BRIEF:** Write ONE Q33N briefing covering all delegatable items. File: `.deia/hive/tasks/YYYY-MM-DD-Q33NR-BATCH-BRIEF.md`
3. **DISPATCH:** Send ONE Q33N bee with the batch brief. Q33N handles task files and bee dispatch below.
4. **HOLD THE LINE:** While batch runs, Q33NR stays with Q88N for strategic work. Don't micromanage.
5. **ROLLUP:** When Q33N reports, summarize to Q88N: what shipped, what failed, what needs follow-up.

Strategic items stay with Q33NR + Q88N. Everything else gets delegated.

---

## P-09: Quality Assurance

**TDD + one reviewer per sprint.** No tribunal. No multi-vendor scoring.

1. Bees do TDD (P-05)
2. Q33N assigns one bee as reviewer. Reviewer does NOT code.
3. Reviewer checks: does code match task? Do tests test the right things? Obvious bugs?
4. Reviewer flags to Q33N. Q33N reassigns fix.
5. Q33N decides. No votes, no rubrics.

---

## P-10: Vision Anchoring

**50 words at the top of every file the agent reads on startup.**

The vision anchor answers: "If I had to explain this product to a senior engineer in 30 seconds, what would they need to know to make correct architectural decisions?"

Lives in: BOOT.md (bees), CLAUDE.md (Claude Code), task file preamble (Codex/Gemini). Updated when core capability changes. NOT updated for feature additions or marketing language.

---

## P-11: Code Index Maintenance

The repo has a semantic search index (`_tools/query_index.py`). Before grepping:

```
python _tools/query_index.py "what you're looking for"
```

Q33N ensures the index watcher is running before dispatching bees. Bees use the index before Glob/Grep. Index uses `all-MiniLM-L6-v2` (local, no API cost). Chunks: .py by function/class, .md by heading, .ir.json by node.

---

## P-12: Living Feature Inventory

One file. Updated every sprint close. Every bee names what it built or broke.

Format per entry: `feature_id | title | status | evidence_path | last_verified`

Status values: BUILT (code + tests), SPECCED (doc only), BROKEN (regression), REMOVED (intentional).

Sprint close ritual: Q33N runs the inventory update. Any bee that modified features updates their entries. `features_broken` count is honest — never hidden.

---

## Config Files

### ethics-default.yml
Default ethics template. forbidden_actions: delete_production_data, bypass_gate, modify_ethics, impersonate_human, access_pii_unredacted. max_autonomy_tier: 1.

### carbon.yml
Carbon methodology. Model energy estimates per 1K tokens. Region intensity (g CO2/kWh). Hardware profiles. Daily/weekly/monthly budgets.

### grace.yml
Grace interval config. Default: 300s. By violation type (forbidden_action: 60s, domain_violation: 120s). No grace for REQUIRE_HUMAN or security_critical.

---

## P-13: Backlog Addition

**Every backlog item gets an ID, priority, and t-shirt size.** No exceptions.

### Required Fields

| Field | Source | Example |
|-------|--------|---------|
| `--id` | Next sequential `BL-XXX`. Check existing: `python _tools/inventory.py backlog list` | `BL-131` |
| `--title` | Short imperative description. Max 80 chars. | `Port Properties Panel editing UI` |
| `--category` | One of: `enhancement`, `bug`, `port`, `infrastructure`, `research` | `port` |
| `--priority` | `P0` (must ship), `P1` (should ship), `P2` (nice to have), `P3` (someday) | `P0` |
| `--source` | Who requested it: `Q88N-direct`, `platform-backlog`, `bee-finding`, `spec-XXX` | `Q88N-direct` |
| `--notes` | T-shirt size + context. Include file paths where work happens. | `Size: L. ~1500 lines. browser/src/primitives/canvas/properties/` |

### T-Shirt Sizes

| Size | Effort | Lines (rough) | Examples |
|------|--------|---------------|----------|
| S | < 1 hour | < 200 | Config change, single endpoint, small port |
| M | 1–4 hours | 200–800 | New module, multi-file feature, route + tests |
| L | 4–12 hours | 800–2000 | Subsystem port, new primitive, multi-endpoint API |
| XL | 1–3 days | 2000–5000 | Major feature, large port with dependency work |
| XXL | 3+ days | 5000+ | System-wide port, new engine, multi-wave dispatch |

### Steps

1. **Check for duplicates.** `python _tools/inventory.py backlog list` — scan titles. Don't create duplicates.
2. **Get next ID.** Find highest `BL-XXX` in the list. Increment by 1.
3. **Determine priority.** P0 = blocks alpha. P1 = needed for alpha. P2 = post-alpha. P3 = aspirational.
4. **Estimate t-shirt size.** Use the table above. When in doubt, size up.
5. **Include file paths in notes.** Where does the work happen? Source and destination for ports. Directory for new features. This prevents bees from guessing.
6. **Add via CLI:**

```
python _tools/inventory.py backlog add --id BL-XXX --title "Short title" --category enhancement --priority P1 --source Q88N-direct --notes "Size: M. browser/src/primitives/foo/"
```

7. **Verify.** `python _tools/inventory.py backlog list | grep BL-XXX`

### Rules

- **Notes format:** Always start with `Size: X.` followed by context. Example: `Size: L. ~1500 lines. Port from platform/efemera/src/properties/ to browser/src/primitives/canvas/properties/`
- **Never edit the DB directly.** Always use `_tools/inventory.py`. The DB is PostgreSQL on Railway.
- **Batch additions:** When adding 3+ items at once, list all IDs and titles before executing so Q88N can review.
- **Priority changes:** Use the inventory store module. Document the reason.
- **Port items:** Category is `port`. Notes must include source path, destination path, and approximate line count.

---

## P-14: Queue Runner Operations

**The queue runner is the automated dispatch engine.** It watches `.deia/hive/queue/` and dispatches specs to regent bots.

### File Naming — CRITICAL

The queue runner uses `glob("*SPEC*.md")` to find work. **Files MUST contain `SPEC` in the filename** or they will be invisible to the runner.

| Will be picked up | Won't be picked up |
|---|---|
| `2026-03-16-SPEC-TASK-200-dns-config.md` | `2026-03-16-TASK-200-dns-config.md` |
| `2026-03-16-SPEC-w3-08-smoke-test.md` | `2026-03-16-w3-08-smoke-test.md` |

When pushing task files into the queue, prefix with `SPEC-`: `SPEC-TASK-XXX-name.md`.

### Config

File: `.deia/config/queue.yml`

Key settings:
- `budget.max_parallel_bees` — max concurrent dispatches (slots backfill as bees complete)
- `budget.max_session_usd` — cost ceiling per session
- `budget.max_fix_cycles_per_spec` — retry limit before spec goes to `_dead/`
- `models.regent_bot` — model for dispatched regent bots

### Directories

| Directory | Purpose |
|-----------|---------|
| `.deia/hive/queue/` | Active queue — runner scans here |
| `.deia/hive/queue/_done/` | Processed specs (moved by runner) |
| `.deia/hive/queue/_dead/` | Failed specs after max retries |
| `.deia/hive/queue/_needs_review/` | Specs that need human review |

### Watch Mode

`python .deia/hive/scripts/queue/run_queue.py --watch`

Uses Fibonacci backoff polling (1s, 1s, 2s, 3s, 5s, 8s, 13s, 21min cap). Resets to shortest interval when new specs are found. Use `--watch-interval N` for fixed interval instead.

**Important:** If the runner started with an empty queue, it may be on a long backoff interval. Kill and restart to pick up newly-added files immediately.

### What `_done/` Means

A spec in `_done/` means **the queue runner processed it** — NOT that the work is complete. The regent may have only written a coordination report or task files. Always check for bee response files to confirm actual code was delivered.

---

**End of Process Library v2.**

*"There is always a process. If there isn't one, create it, test it, submit it."*

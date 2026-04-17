# SPEC-USAGE-ANALYTICS-001: Token Usage Analytics Across All DEIA Repos

## Priority

P1

## Model

sonnet

## Depends On

None

## Objective

Produce a comprehensive view of token consumption, activity patterns, and work distribution across all repos with DEIA coordination (Sep 2025 → present). Two purposes:
1. **Portfolio evidence** — quantify the scale of AI agent orchestration for 1000bulbs application
2. **Operational insight** — verification-vs-design ratio, gap detection, cost trends

---

## Data Sources

**Source 1: `history.jsonl`** — activity timeline
- Path: `C:\Users\davee\.claude\history.jsonl` (26,011 lines, Sep 27 2025 → present)
- Schema: `{timestamp: epoch_ms, project: "path", display: "..."}`
- Timestamps are epoch milliseconds — divide by 1000

**Source 2: `session-meta/*.json`** — session-level token data
- Path: `C:\Users\davee\.claude\usage-data\session-meta\*.json` (201 sessions, Mar 28 → Apr 6 2026)
- Schema: `{session_id, project_path, start_time, duration_minutes, input_tokens, output_tokens, tool_counts}`
- Timestamps are ISO 8601 with Z suffix
- Warning: token counts may be under-reported. Cross-reference.

**Source 3: Bee response files** — per-bee cost/token data
- Paths: `.deia/hive/responses/` in each repo listed below
- Schema: Markdown with `## Clock / Cost / Carbon` sections
- Parse: extract date from filename prefix (YYYYMMDD), grep for cost/token lines

**Source 4: `bstatus.json`** — factory build status (most reliable for token ratios)
- Path: `bstatus.json` (refresh: `curl -s http://127.0.0.1:8420/build/status > bstatus.json`)
- Schema: per-bee `{task_id, model, input_tokens, output_tokens, cost_usd}`
- Coverage: 1,102 completed bees in current factory instance

**Source 5: Event Ledger DBs** — structured cost data (SQLite)
- Primary: `.deia/hive/event_ledger.db` (940 events, 346M tokens, $3,152.33, Apr 8-16 2026)
- Also check: `.deia/ledger.db`, `hivenode/wiki/.data/ledger.db`
- MANDATORY: scan ALL repos below for `*ledger*.db` files in `.deia/` and `.deia/hive/`
- Known spike: Apr 14 = 835 builds, 290.6M tokens, $2,650.43

**Repos with `.deia/` folders** (all under `C:\Users\davee\OneDrive\Documents\GitHub\`):

| Repo | Response Files | Earliest |
|------|---------------|----------|
| simdecisions | 3,924 | Mar 10, 2026 |
| shiftcenter | 2,659 | Mar 10, 2026 |
| platform | 1,697 | Feb 16, 2026 |
| familybondbot-backup-season-009 | 123 | Nov 1, 2025 |
| familybondbot | 48 | Feb 2, 2026 |
| ra96it | 30 | Nov 20, 2025 |
| clipegg | 2 | Nov 25, 2025 |
| deiasolutions-3-chrysalis | 0 | — |
| deiasolutions-com | 0 | — |
| deiasolutions-labs | 0 | — |
| deia_raqcoon | 0 | — |
| deia-viz | 0 | — |
| lilys_dragon | 2 | — |
| simulation | 0 | — |

---

## Implementation Guide

**D1. Activity Timeline** (from `history.jsonl`):
Write `_tools/usage_analytics.py` that produces `docs/portfolio/usage-analytics-report.md`.
Include: activity by repo by month table (Sep 2025 → present),
activity by hour histogram (CDT, NOT UTC),
daily activity heatmap (`.` = inactive, `#` = active),
gap detection (>24h any day, >6h during 9AM-5PM CDT).

**D2. Token Usage Analysis**:
Interactive sessions from `session-meta/*.json`: input vs output tokens, ratio, by repo.
Factory bees from `bstatus.json`: input vs output, ratio, by model (haiku/sonnet/opus).
Response file mining from `.deia/hive/responses/`: grep for `Cost:`, `Clock:`, `Carbon:`.
Combined view: total input, total output, ratio — by interactive/factory, repo, month, model.

**D3. Verification vs Design Ratio**:
Classify `tool_counts` from session-meta:
Verification = `Read`, `Grep`, `Glob`, `Bash` (test/pytest/vitest/check/lint/curl/status).
Design = `Write`, `Edit`, `NotebookEdit`, `Bash` (git commit/mkdir/cp/npm run build), `Task`, `TaskCreate`.
Output: verification %, design %, ambiguous %. Compare to Tokenomics paper (72% verification).

**D4. Benchmark Comparison Table**:

| Metric | Q88N Interactive | Q88N Factory | Tokenomics Paper | OpenRouter Sonnet |
|--------|-----------------|--------------|------------------|-------------------|
| In:Out ratio | (calculated) | (calculated) | 3.5:1 | 99:1 |
| Verification % | (calculated) | n/a | 72% | n/a |
| Sessions/day | (calculated) | (calculated) | n/a | n/a |

Do NOT include SWE-bench or ChatDev.

---

## Deliverables

- Write `_tools/usage_analytics.py` — re-runnable Python script (not a one-shot notebook)
- Write `docs/portfolio/usage-analytics-report.md` — full analytics report with all sections

---

## Acceptance Criteria

**AC-1: Data collection**
- [ ] Parse `C:\Users\davee\.claude\history.jsonl` — all lines, extract timestamp + project path
- [ ] Read all `C:\Users\davee\.claude\usage-data\session-meta\*.json` — extract `input_tokens`, `output_tokens`, `tool_counts`, `project_path`, `start_time`
- [ ] Refresh and read `bstatus.json` via `curl -s http://127.0.0.1:8420/build/status > bstatus.json`
- [ ] Query `.deia/hive/event_ledger.db` — extract date, builds, tokens, USD columns
- [ ] Scan `.deia/ledger.db` for any data
- [ ] Scan `hivenode/wiki/.data/ledger.db` for any data
- [ ] Scan for `*ledger*.db` in `.deia/` of `shiftcenter/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `platform/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `familybondbot/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `familybondbot-backup-season-009/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `ra96it/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `clipegg/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `deiasolutions-3-chrysalis/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `deiasolutions-com/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `deiasolutions-labs/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `deia_raqcoon/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `deia-viz/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `lilys_dragon/`
- [ ] Scan for `*ledger*.db` in `.deia/` of `simulation/`
- [ ] Grep `.deia/hive/responses/` in each repo for `Cost:`, `Clock:`, `Carbon:` lines
- [ ] Deduplicate response files between simdecisions and shiftcenter (flatten migration overlap)
**AC-2: Activity timeline produced**
- [ ] Activity by repo by month table (Sep 2025 → present)
- [ ] Activity by hour of day histogram (CDT, NOT UTC)
- [ ] Daily activity heatmap (text grid, `.` = inactive, `#` = active)
- [ ] Gap list: every gap >24h, every gap >6h during 9AM-5PM CDT with timestamps
**AC-3: Token usage analysis produced**
- [ ] Interactive session in:out ratio by repo
- [ ] Factory bee in:out ratio by model (haiku/sonnet/opus)
- [ ] Event ledger totals by date (all repos where ledger DBs found)
- [ ] Combined view: total input, total output, ratio by interactive/factory/repo/month
**AC-4: Verification vs design ratio**
- [ ] Classify `tool_counts` from `session-meta/*.json` into verification vs design
- [ ] Report verification %, design %, ambiguous %
- [ ] Compare to Tokenomics paper benchmark (72% verification)
- [ ] State whether Q88N's usage slants toward design or verification, with data
**AC-5: Script and report deliverables**
- [ ] Write `_tools/usage_analytics.py` — re-runnable, `python _tools/usage_analytics.py` regenerates report
- [ ] Write `docs/portfolio/usage-analytics-report.md`
- [ ] Script runs without errors
- [ ] All timestamps converted to CDT (UTC-5) before display
- [ ] Report includes Data Quality section (complete vs gaps vs suspicious values)
- [ ] Benchmark comparison table (Q88N interactive, Q88N factory, Tokenomics paper, OpenRouter Sonnet)
- [ ] No SWE-bench or ChatDev benchmarks in report

---

## Smoke Test

- [ ] Run `python _tools/usage_analytics.py` — exits with code 0
- [ ] File `docs/portfolio/usage-analytics-report.md` exists after script run
- [ ] Report contains "Data Quality" section heading
- [ ] Report contains "CDT" (not "UTC" outside of conversion notes)
- [ ] Report contains activity-by-hour histogram
- [ ] Report does not contain "SWE-bench" or "ChatDev"

---

## Constraints

- All timestamps in CDT (UTC-5). NEVER report UTC.
- Do NOT include SWE-bench or ChatDev benchmarks — invalid comparisons.
- Script must be re-runnable (not a one-shot notebook). `python _tools/usage_analytics.py` regenerates the report.
- Handle missing/corrupt files gracefully — report what couldn't be parsed, don't crash.
- CDT = UTC-5. Apply offset to all timestamps before bucketing.
- Deduplicate response files between simdecisions and shiftcenter (shared from flatten migration).

---

**END OF SPEC**

# BRIEFING: CUTOVER PHASE 2 — PREREQUISITE BLOCKERS

**Author:** Q88N (Dave)
**Filed by:** Q33NR (Opus, live session 2026-04-10 07:06)
**Date:** 2026-04-10
**Session:** `.deia/hive/session-logs/2026-04-10-0706-Q33NR-SESSION.md`

---

## Context
The Phase 1 cutover moved code but never cut over operationally. The factory is still running from shiftcenter/. simdecisions/ is a snapshot, not a system. This is now a real cutover — shiftcenter will be decommissioned.

## Decision (locked)
- **Target:** simdecisions becomes the production runtime
- **Model assignment:** Opus as Q33NR and Q33N, Sonnet as BEE and BAT

## Blockers — Human-owned (Dave must do these)
| # | Blocker | Action |
|---|---------|--------|
| 2 | 5 daemons running from shiftcenter | Graceful shutdown in order: triage → dispatcher → scheduler → run_queue → hivenode |
| 3 | Other claude.exe sessions | Close all except this session |
| 6 | OneDrive sync | Pause before any rename |
| 7 | Railway + Vercel deploy source | Check dashboards — confirm current deploy target |

## Blockers — Mr. Code can assist
| # | Blocker | Action |
|---|---------|--------|
| 1 | simdecisions has no .git | `git init`, commit as-built state as `v0.1.0-cutover`, push to remote. Without this, no rollback, no history, no reasoning about state. |
| 4 | .venv editable paths invalid after rename | After rename: `uv sync` from new location, or rewrite dist-info direct_url.json |
| 5 | Upgrade briefing undefined | Cannot plan without scope. Awaiting Dave's upgrade list. |
| 8 | 6 in-flight queue items | Confirm queue drained before shutdown |
| 9 | 23 stale task files in simdecisions/.deia/hive/tasks/ | Triage before rename — archive or delete dead weight |

## Sequence
1. Dave: #2, #3, #6, #7 (local machine work)
2. Together: #1 (git-init checkpoint)
3. Together: #5 (upgrade briefing — scope definition)
4. Mr. Code: #8, #9 (queue drain, task triage)
5. Mr. Code: #4 (venv rebuild post-rename)
6. Then: Rename simdecisions → simdecisions-1, begin Phase 2 refactor

## Exit criteria for "ready to start Phase 2"
- [ ] simdecisions is a git repo with v0.1.0-cutover tag pushed
- [ ] All 5 shiftcenter daemons stopped
- [ ] Queue drained (0 in-flight)
- [ ] OneDrive paused
- [ ] Railway/Vercel deploy source confirmed
- [ ] Upgrade briefing written and approved
- [ ] Stale tasks archived

**Do not proceed until all boxes checked.**

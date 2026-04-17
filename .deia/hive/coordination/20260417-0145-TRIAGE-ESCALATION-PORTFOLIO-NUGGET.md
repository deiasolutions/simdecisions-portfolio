# TRIAGE ESCALATION: PORTFOLIO-NUGGET

**Date:** 2026-04-17 01:45:00 UTC
**Reason:** 3 requeue attempts (max 3)
**Status:** NEEDS MANUAL REVIEW

## Summary

Spec `SPEC-PORTFOLIO-NUGGET-HUNT-001.md` has been requeued 3 times and failed each time.
Automated triage has moved it to `_escalated/` for manual review.

## Triage History

- 2026-04-17T01:30:00.090714Z — requeued (empty output)
- 2026-04-17T01:35:00.095631Z — requeued (empty output)
- 2026-04-17T01:40:00.102136Z — requeued (empty output)

## Next Steps

1. **Review spec file** in `queue/_escalated/SPEC-PORTFOLIO-NUGGET-HUNT-001.md`
2. **Diagnose root cause** — why is this spec failing repeatedly?
3. **Options:**
   - Fix spec and move back to backlog/
   - Archive spec if no longer needed
   - Break into smaller specs
   - Escalate to architect (Mr. AI) if systemic issue

## Original Spec

```markdown
## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-PORTFOLIO-NUGGET-HUNT-001: Portfolio Nugget Hunt — Folder-Level Curation Across All Local Repos

**Priority:** P1
**Model:** opus (orchestrator + final report); sonnet (parallel research subagents)
**Effort:** 3-5 hours wall, ~$15-25 cost
**Depends On:** None
**Status:** READY

---

## Why This Spec Exists

`SPEC-PORTFOLIO-1000BULBS-001` (completed 2026-04-16) audited at the **repo level** and missed the point. Q88N wants:

1. **Folder/file-level "nuggets"** that tell a story — not whole-repo scorecards
2. **familybondbot featured prominently** as the end-to-end product showcase (the previous audit forgot it entirely)
3. **Mine `platform` for nuggets** — it was the prior version of `shiftcenter` and may contain shareable pieces even though the whole repo is redundant
4. **Surface curated pieces from any local repo** that strengthen the 1000bulbs narrative
5. **Drop federalist-papers-ai** (confirmed out of scope)
6. **Keep `global-commons`** in the mix as supporting evidence (Three Currencies discipline)
7. **Recommend a curated home** for the showcase — could be a new public repo, `deiasolutions-com`, `deiasolutions-labs`, or other

The output is two things:
- **Recommendation report for Q88N** (written by Opus) — what to share, where to host it, what story it tells
- **A follow-on spec** that Claude Code can execute (with Q88N modifications) to actually build the curated showcase

---

## Q88N Context

Q88N is applying for a role at **1000bulbs** that screens at the portfolio stage. The 4 core signals to demonstrate:
1. Multi-tier app architecture
2. Agent orchestration
3. AI correction discipline
4. CI/CD maturity

Plus differentiators: strangler fig thinking, Three Currencies (CLOCK/COIN/CARBON), 20-year domain arc.

**Prior audit recommendation:** Create `deiasolutions/simdecisions-architecture` public teaser. **This audit can override that** if a better path emerges from the nugget hunt.

---

## Acceptance Criteria

### Phase A — Parallel Research (6 sonnet subagents, launched concurrently via Task tool)

Each subagent surveys ONE slice of `C:\Users\davee\OneDrive\Documents\GitHub\` and returns a JSON-ish markdown report listing nuggets found. A "nugget" is any folder, file, doc, diagram, or pattern worth sharing in the showcase.

**For each nugget, the subagent records:**
- `path`: absolute path
- `kind`: README | architecture-doc | diagram | code-pattern | spec | test | config | data | demo | story
- `signal_hit`: which 1000bulbs signal(s) it demonstrates (or "differentiator" / "evidence-of-rigor")
- `one_line_pitch`: why a 1000bulbs reviewer would care
- `share_classification`: PUBLIC_NOW | TEASER_EXCERPT | PRIVATE_ON_REQUEST | DO_NOT_SHARE
- `effort_to_share`: hours to extract/sanitize/publish

#### Slice 1 — Flagship trio (deep dive)
- `simdecisions/`, `shiftcenter/`, `platform/`
- Goal: Mine all three for the strongest architecture/orchestration/AI-correction nuggets. Compare to find what `platform` has that `simdecisions` lost.

#### Slice 2 — End-to-end products
- `familybondbot/` (CANONICAL), `familybondbot-backup-season-009/`, `family-bond-chat/`, `familyboundbot/`
- `futurehealth/`, `health-scribe/`, `health-scribe-loco/`, `collabry_schwab/`
- Goal: Identify the strongest end-to-end product story. familybondbot is the headline; the others are alternates if FBB is unpolished.

#### Slice 3 — Open standards & ethics
- `prism-ir/`, `prism-ir-staging/`
- `global-commons/`, `global-commons-temp/`
- `deia-bok/`
- Goal: Find publication-quality docs and standards work. Ignore federalist-papers-ai entirely.

#### Slice 4 — DEIA toolchain & meta
- `q33n/`, `deia_raqcoon/`, `deia-viz/`
- `deiasolutions-3-chrysalis/`, `deiasolutions-labs/`, `deiasolutions-com/`
- `claude_code/`, `dave-claude-practices/`, `prompter/`, `prompter2/`
- `MASTER-PLAN-MULTI-BEE-CODE-GEN.md`, `hive_design_analogies.md`, `deia_project_analysis.md`, `deiasolutions_analysis.md`
- Goal: Find DEIA Hive orchestration evidence outside of simdecisions. Evaluate whether `deiasolutions-com` or `deiasolutions-labs` is a viable showcase home.

#### Slice 5 — Simulation & engines
- `sim-js/`, `sim-react/`, `sim-react-2/`, `pysim/`, `simulation/`
- `pythreads/`, `temp-swe-bench/`, `zero-shot_forecast/`, `timesfm/`
- Goal: Find simulation depth evidence (reinforces Phase-IR / DES story).

#### Slice 6 — Wildcard nuggets (everything else worth surveying)
- `clipegg/`, `lilys_dragon/`, `gospel2/`, `Jarvis/`, `pale-aperture/`, `quantum-project/`
- `voice-generation/`, `x_automation/`, `ra96it/`, `manim/`
- `JobFunnel/`, `career/`, `social-media/`, `file-consolidator/`, `dev-tools/`, `scripts/`
- `specs/`, `cap_metro/`, `Solar System/`, `Space Elevator/`, `euskara/`, `teleprompter_app.py`
- Goal: Catch hidden gems. Many of these will return "nothing to share" — that's fine.

#### EXCLUDE from all slices
- `SECRETS/`, `nul`, `_archive/`, `_chop_shop/`, `_inbox/`, `NOTMINE/`, `nocopy/`, `anthropic-leaked-source-code/`
- `New folder/`, `desktop-tutorial/`, `env-n-stuff/`, `miscellaneous/`, `dev-environment-fixes/`
- External libraries: `browser-use/`, `github-mcp-server/`, `RealtimeSTT/`, `matrix-react-sdk/`, `element-web-*/`, `llama/`
- Standalone notebooks unless part of a slice: `archive thing 2.ipynb`, `image metadata.ipynb`, `sqlite thing.ipynb`, `prompter.ipynb`, `x api keys.ipynb`
- Already-known-out-of-scope: `federalist-papers-ai/`, `federalist-upload-analysis/`, `Power BI Beginner to Pro.zip`, `3b1b_videos/`

### Phase B — Synthesis (Opus, after all 6 subagents return)

The Opus orchestrator reads all 6 subagent reports and produces:

#### B1. Recommendation report for Q88N
**Location:** `docs/portfolio/1000bulbs-nugget-hunt-recommendation.md`

Must include:
- [x] **Top 10 nuggets ranked** by 1000bulbs signal strength × low extraction effort
- [x] **Recommended showcase home** with rationale (new public repo vs `deiasolutions-com` vs `deiasolutions-labs` vs other) — bee chooses, justifies
- [x] **End-to-end product feature** — which familybondbot variant (or fallback) anchors the showcase
- [x] **Story arc** — the narrative thread connecting selected nuggets (5-min read)
- [x] **What to drop from prior audit** — explicitly call out which prior recommendations are now superseded
- [x] **Cost-benefit table** — hours-to-ship vs signal-strength for each nugget
- [x] **Q88N decisions needed** — 3-5 explicit choices framed as "Option A / Option B / Recommendation"

#### B2. Follow-on spec for Claude Code
**Location:** `docs/portfolio/1000bulbs-nugget-hunt-followup-spec.draft.md`

This is a complete spec file (matching the format of THIS spec) that Q88N can read, modify, and submit to the factory. It must:
- [x] Have a SPEC-ID slot (suggest `SPEC-PORTFOLIO-CURATE-001`)
- [x] List concrete files to copy/extract per recommended showcase home
- [x] Specify any sanitization needed (remove secrets, scrub paths, etc.)
- [x] Include test/verification steps (links work, no broken references, badges render)
- [x] Be executable by a single Sonnet bee in 4-8 hours
- [x] Have crisp acceptance criteria (NOT vague "make it look good")

---

## Implementation Notes

### Parallel dispatch pattern
The Opus orchestrator MUST use the Task tool to launch all 6 research subagents **concurrently** (single message, multiple Task tool calls). Do NOT serialize. Each subagent:
- Uses `subagent_type: "general-purpose"` (or `Explore` for thoroughness)
- Inherits Sonnet model via the parent dispatch (or explicitly request `sonnet`)
- Receives a self-contained prompt with its slice list and the nugget-recording schema

### Time budget per subagent
- Slice 1 (flagship trio): up to 30 min — these are large repos
- Slice 2 (end-to-end): up to 25 min
- Slice 3-6: up to 20 min each
- Synthesis: up to 30 min

### Cost guardrails
- Sonnet at ~200K context input: ~$3-5 per slice
- Opus synthesis: ~$5-8
- **Total estimate: $20-35.** If subagents balloon past $40 total, halt and report.

### Files the orchestrator must read first
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260416-SPEC-PORTFOLIO-1000BULBS-001-RESPONSE.md` (prior audit — explicitly supersede)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\1000bulbs-portfolio-audit.md` (prior scorecards)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\1000bulbs-teaser-README.draft.md` (prior teaser draft — keep what works, discard what's stale)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\BOOT.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\CLAUDE.md`

### What the recommendation must NOT do
- Do NOT propose more than 1 showcase home (pick one)
- Do NOT propose >15 total nuggets (curation = saying no)
- Do NOT include any nugget classified DO_NOT_SHARE
- Do NOT reference federalist-papers-ai except to explicitly exclude it
- Do NOT propose work that requires repos Q88N hasn't authorized (e.g., editing external repos)

---

## Smoke Test

After reading the recommendation report, can Q88N answer in one pass:

1. **What is the curated showcase home and why?** (single named repo/site)
2. **What 5-10 specific files/folders get pulled in?** (with absolute paths)
3. **What story does it tell a 1000bulbs reviewer in 5 minutes?** (single paragraph)
4. **What's the next implementation spec, and is it ready to dispatch with minor edits?** (filename + readiness assessment)

If yes to all 4 → spec passed. If any "I need to re-read" or "it's unclear" → spec failed, redo.

---

## Response File Requirements

Standard 8-section response per `.deia/BOOT.md`. Plus:
- Append the absolute paths of the 6 subagent task IDs (for Q33N audit)
- Include total cost breakdown by subagent
- List any nugget classified `DO_NOT_SHARE` and the reason (so Q88N can verify the call)

---

## What Success Looks Like

Q88N reads the recommendation report once, makes 2-3 small edits to the follow-on spec, drops the spec into `.deia/hive/queue/backlog/`, and a single Sonnet bee builds the curated showcase in one session.

No more guessing. No more whole-repo scorecards. Folder-level, file-level, story-driven curation.

---

**END OF SPEC**

## Triage History
- 2026-04-17T01:30:00.090714Z — requeued (empty output)
- 2026-04-17T01:35:00.095631Z — requeued (empty output)
- 2026-04-17T01:40:00.102136Z — requeued (empty output)

```

---

**Automated escalation by triage daemon**

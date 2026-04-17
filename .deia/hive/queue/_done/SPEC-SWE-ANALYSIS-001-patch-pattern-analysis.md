# SPEC-SWE-ANALYSIS-001: SWE-bench Pro Patch Production Pattern Analysis

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Analyze the SWE-bench Pro run results to understand why bees produced patches for 204/736 tasks (27.7%) and failed on the remaining 532. Identify patterns that predict success or failure so we can improve patch rate on future runs.

## Context

We ran all 731 SWE-bench Pro tasks (plus 5 Verified) through the factory. 15 concurrent sonnet bees processed them. 204 produced valid .diff patches. 532 did not. We need to understand why.

## Data Sources

- **Sample manifest:** `.deia/benchmark/swebench/sample.json` — all 731 tasks with repo, instance_id, problem_statement, repo_language, base_commit
- **Produced patches:** `.deia/benchmark/swebench/patches/*.diff` — 204 diffs
- **Spec files:** `.deia/benchmark/swebench/specs/SPEC-SWE-*.md` — all 736 specs
- **Bee responses:** `.deia/hive/responses/` — look for SWE-related response files
- **Done queue:** `.deia/hive/queue/_done/SPEC-SWE-*.md` — completed specs

## Acceptance Criteria

- [ ] Breakdown by repository: total tasks, patches produced, patch rate %, ranked by success
- [ ] Breakdown by language (Python, Go, TypeScript, JavaScript): patch rate per language
- [ ] Problem size analysis: avg problem_statement length for success vs failure, threshold identification
- [ ] Patch size distribution: lines changed across the 204 produced patches
- [ ] Failure mode analysis: sample 20 failed tasks across repos/languages, categorize why (timeout, no response, invalid diff, couldn't clone, etc.)
- [ ] Success characteristics: common traits in problem statements of successful patches
- [ ] Briefing written to `.deia/hive/coordination/SWE-BENCH-PRO-ANALYSIS.md`
- [ ] Briefing includes: summary table, top 3-5 key findings, recommendations for next run, raw data tables

## Smoke Test

- [ ] Briefing file exists at `.deia/hive/coordination/SWE-BENCH-PRO-ANALYSIS.md`
- [ ] All 6 analysis sections present with data
- [ ] Numbers add up (success + failure = total per repo)
- [ ] Recommendations are actionable (not generic)

## Constraints

- Read-only analysis. Do not modify any patches, specs, or queue files.
- Do not dispatch any bees.
- No file over 500 lines.
- Write analysis output to `.deia/hive/coordination/SWE-BENCH-PRO-ANALYSIS.md` only.

## Files to Modify

- `.deia/hive/coordination/SWE-BENCH-PRO-ANALYSIS.md` (create)

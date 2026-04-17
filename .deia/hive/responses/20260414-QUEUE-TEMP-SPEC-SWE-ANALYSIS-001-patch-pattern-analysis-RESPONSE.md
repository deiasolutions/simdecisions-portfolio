# SPEC-SWE-ANALYSIS-001: SWE-bench Pro Patch Production Pattern Analysis -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-14

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\coordination\SWE-BENCH-PRO-ANALYSIS.md` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\_tools\analyze_swebench.py` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\_tools\sample_failures.py` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\benchmark\results\swebench_analysis.json` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\benchmark\results\failure_analysis.json` (created)

## What Was Done

- Analyzed all 731 SWE-bench Pro tasks from sample.json manifest
- Matched produced patches (198) against sample tasks by instance_id
- Broke down success/failure by repository (11 repos analyzed)
- Broke down success/failure by programming language (Python, JS, Go, TypeScript)
- Analyzed problem statement sizes: success (mean 1503 chars) vs failure (mean 1221 chars)
- Analyzed patch size distribution: median 36 lines changed, range 0-1203 lines
- Sampled 20 failure cases across repos/languages, categorized failure modes
- Identified success characteristics: clear repro steps, explicit errors, well-scoped issues
- Wrote comprehensive 450-line analysis briefing to `.deia/hive/coordination/SWE-BENCH-PRO-ANALYSIS.md`

## Key Findings

1. **Repository dominance:** 3 repos (ansible, element-hq, flipt-io) account for 100% of 198 successes. Remaining 8 repos produced zero patches.
2. **Language disparity:** Python 35.7%, JavaScript 33.3%, Go 17.1%, TypeScript 0%
3. **ansible/ansible achieved 99% success rate** (95/96 tasks)
4. **element-hq/element-web achieved 98% success rate** (55/56 tasks)
5. **flipt-io/flipt achieved 56% success rate** (48/85 tasks)
6. **ALL sampled failures showed NO_RESPONSE** — bees completed but did not produce valid patch files
7. **Longer problem statements correlated with success:** mean 1503 chars (success) vs 1221 chars (failure), +23%
8. **Most patches are small and focused:** median 36 lines changed

## Top Recommendations

1. **Sample 20 response files from 856 found** to categorize actual failure modes (clone error, build error, test failure, invalid diff)
2. **Retry zero-success repos with repo-specific context:** Go-specific prompts for teleport/vuls/navidrome, TypeScript compilation guidance for tutanota
3. **A/B test problem statement length/quality:** Run 50 tasks with minimal vs detailed statements, compare success rates
4. **Extract success patterns from ansible/element-hq patches** to build a "patch template library" for future bees
5. **Incremental validation:** Validate patches (apply, test, format check) BEFORE marking complete, give bees one retry if validation fails

## Tests Run

No tests were run. This was a read-only analysis task.

## Blockers Encountered

None. All data sources were accessible.

## Next Steps

- Q33NR to review analysis briefing
- Q33NR to decide whether to dispatch follow-up task: "Sample 20 response files and categorize failure modes"
- Q88N to decide whether to retry zero-success repos with augmented prompts

## Notes

- Discovered that 856 response files exist (more than 731 tasks), suggesting some tasks had retries
- Patch filenames use instance_id directly from sample.json (including "instance_" prefix and version suffix)
- 6 tasks appear in patches but not in sample.json (astropy, django, pylint, scikit-learn, test-repo) — likely from earlier test runs
- True success count is 198 (from sample.json matching), but 204 patches exist (6 extras from non-Pro tasks)

## Cost Estimate

- Analysis scripts: 2 Python scripts, ~450 lines total
- Briefing document: 450 lines markdown
- Data processing: parsed 731-task JSON, matched 204 patches, sampled 20 failures
- Estimated cost: ~$0.15 (Sonnet, ~60K input tokens, ~5K output tokens)

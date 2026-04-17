# SPEC-METRICS-002: Recompute Planning Numbers with Outlier Trimming

## Priority
P2

## Model Assignment
sonnet

## Depends On
SPEC-METRICS-001 (completed — response at `.deia/hive/responses/20260406-SPEC-METRICS-001-RESPONSE.md`)

## Intent

The raw planning numbers from METRICS-001 are polluted by stuck/zombie tasks that skew duration upward. The duration distribution is right-skewed (long tail of stuck tasks), so standard mean ± 2σ is the wrong cutoff. Recompute the three planning numbers using proper outlier detection for skewed distributions.

## Files to Read First

- `.deia/hive/responses/20260406-SPEC-METRICS-001-RESPONSE.md`
- `.deia/hive/queue/monitor-state.json`

## Acceptance Criteria

- [ ] Compute IQR-trimmed planning numbers (Method 1)
- [ ] Compute median-ceiling-trimmed planning numbers (Method 2)
- [ ] Report exclusion counts and cost % for each method
- [ ] Report whether excluded tasks cluster by model, task type, or time window
- [ ] Deliver a Three Planning Numbers comparison table (Raw vs IQR-trimmed vs Median-ceiling-trimmed)
- [ ] Include one paragraph interpreting which number to use for overnight planning

## Method 1 — IQR Trimming

Calculate Q1, Q3, and IQR for task duration. Exclude any task with duration outside `Q1 - 1.5×IQR` to `Q3 + 1.5×IQR`. Recompute on the trimmed set:
- Tasks per hour
- Human-hours per factory-hour
- Cost per human-hour

## Method 2 — Median Ceiling

Calculate median task duration. Exclude any task with duration > 3× median. Recompute the same three numbers on the trimmed set.

## Additional Analysis

For tasks excluded by each method, report:
- How many tasks were excluded
- What % of total cost those excluded tasks represented
- Whether the excluded tasks cluster around a specific model, task type, or time window (systematic vs random)

## Deliverable

Single response file with:
1. **Three Planning Numbers table** — three columns: Raw (from METRICS-001), IQR-trimmed, Median-ceiling-trimmed
2. **Exclusion summary** — counts, cost %, clustering analysis
3. **Recommendation paragraph** — which number to plan against for overnight runs, and why

Planning principle: the trimmed number is what you plan against. The raw number is what you monitor against — if actual performance drifts below the trimmed baseline, something is wrong.

## Constraints

- Research only. No code changes.
- Use the completed task data already in monitor-state.json and the METRICS-001 response.
- Do not rerun any tasks or touch the queue.

## Smoke Test

Response file exists at `.deia/hive/responses/` with all three table columns populated and exclusion counts reported.

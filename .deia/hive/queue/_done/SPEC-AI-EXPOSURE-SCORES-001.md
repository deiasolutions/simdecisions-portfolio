# SPEC-AI-EXPOSURE-SCORES-001

**MODE: EXECUTE**

**Spec ID:** SPEC-AI-EXPOSURE-SCORES-001
**Created:** 2026-04-09
**Author:** Q88N
**Type:** BUILD — AI exposure scoring pipeline
**Status:** READY
**Priority:** P2

---

## Purpose

Populate the `ai_exposure_scores` table using ONET skill vectors already
ingested (SPEC-ONET-INGEST-001) cross-referenced against published
occupation-level exposure data from the Anthropic Labor Market Impacts
study (Massenkoff & McCrory, March 2026).

This produces a per-occupation score for theoretical AI coverage and
observed AI coverage. It is the Iceberg Index reproduced inside the
SimDecisions database, updatable as new data drops.

---

## Depends On

- SPEC-ONET-INGEST-001

## Model Assignment

sonnet

---

## Source Data

### Anthropic Occupation Group Exposure (Figure 2)
Source: arxiv.org/html/2510.25137v1 and
anthropic.com/research/labor-market-impacts

Extract the following occupation group scores as a seed table.
These are group-level; the scoring pipeline distributes them to
individual SOC codes within each group.

| Occupation Group             | SOC Prefix | Theoretical % | Observed % |
|------------------------------|------------|---------------|------------|
| Computer and Math            | 15-        | 94.3          | 35.8       |
| Business and Finance         | 13-        | 94.3          | 28.4       |
| Management                   | 11-        | 91.3          | ~20.0      |
| Office and Admin Support     | 43-        | 90.0          | 34.3       |
| Legal                        | 23-        | 89.0          | 20.4       |
| Architecture and Engineering | 17-        | 84.8          | ~15.0      |
| Arts and Media               | 27-        | 83.7          | 19.2       |
| Education and Library        | 25-        | ~75.0         | 18.2       |
| Sales                        | 41-        | 62.0          | 26.9       |
| Healthcare Practitioners     | 29-        | ~40.0         | ~10.0      |
| Food Prep and Serving        | 35-        | ~5.0          | ~1.0       |
| Construction and Extraction  | 47-        | ~5.0          | ~1.0       |

Note: values marked ~ are estimates interpolated from the paper's
narrative and charts where exact figures are not published. The bee
must read the source paper before populating — do not use the table
above as the sole reference. Correct any estimates where the paper
provides exact figures.

If Chopra dataset access is obtained before this spec runs, substitute
occupation-level scores from the Iceberg dataset directly and mark
source as 'mit_iceberg_2025_10'.

---

## Scoring Logic

For each SOC code in `onet_occupations`:

1. Match the SOC prefix (first two digits) to the occupation group table.

2. Assign the group-level theoretical and observed percentages as the
   baseline scores for that SOC code.

3. Apply a skill-weighted adjustment: compute the mean importance score
   of the top 10 skills for that occupation from `onet_occupation_skills`.
   If mean importance > 4.0, add 2 percentage points to theoretical.
   If mean importance < 2.5, subtract 2 percentage points from theoretical.
   Clamp result to 0–100.

4. Observed percentage is not adjusted — use group level as-is.
   Observed scores are empirical; do not model-adjust them.

5. Write one row per SOC code to `ai_exposure_scores`:
   - `source`: 'anthropic_2026_03'
   - `theoretical_pct`: adjusted value
   - `observed_pct`: group-level value
   - `captured_at`: 2026-03-05 (Anthropic publication date)
   - `notes`: occupation group used, whether estimate was applied

---

## Deliver As

`_tools/score_ai_exposure.py`

All imports at top. No type hints. No assertions. Python 3.12.
Reads `DATABASE_URL` from environment. No ONET API calls needed —
works entirely from ingested DB data plus a hardcoded seed table
derived from the Anthropic paper.

On completion, print:

```
Occupations scored: N
Source: anthropic_2026_03
Estimated values used: N
Elapsed: Xs
```

---

## Acceptance Criteria

- [ ] Every SOC code in `onet_occupations` has a corresponding row
      in `ai_exposure_scores`
- [ ] No theoretical_pct value outside 0–100
- [ ] No observed_pct value outside 0–100
- [ ] Rows marked with notes where estimates were applied
- [ ] Re-run is idempotent (upsert on soc_code + source)
- [ ] Script exits 0 on success, 1 on fatal error

## Smoke Test

```bash
psql $DATABASE_URL -c "SELECT COUNT(*) FROM ai_exposure_scores;"
# Expected: >= 900

psql $DATABASE_URL -c \
  "SELECT o.title, a.theoretical_pct, a.observed_pct \
   FROM ai_exposure_scores a \
   JOIN onet_occupations o USING (soc_code) \
   WHERE a.source = 'anthropic_2026_03' \
   ORDER BY a.theoretical_pct DESC LIMIT 10;"
# Expected: top 10 most exposed occupations with plausible scores

psql $DATABASE_URL -c \
  "SELECT COUNT(*) FROM ai_exposure_scores WHERE notes LIKE '%estimate%';"
# Expected: > 0 (confirms estimate tracking is working)
```

## Constraints

- Read the Anthropic source paper before writing the seed table
- Do not invent exposure scores — use only published or clearly
  interpolated values, and mark interpolations in notes
- No writes to any table other than ai_exposure_scores
- Script max 200 lines

## Response File

`.deia/hive/responses/20260409-AI-EXPOSURE-SCORES-RESPONSE.md`

---

*SPEC-AI-EXPOSURE-SCORES-001 — Q88N — 2026-04-09*

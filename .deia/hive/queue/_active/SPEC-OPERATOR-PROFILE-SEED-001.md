# SPEC-OPERATOR-PROFILE-SEED-001

**MODE: EXECUTE**

**Spec ID:** SPEC-OPERATOR-PROFILE-SEED-001
**Created:** 2026-04-09
**Author:** Q88N
**Type:** BUILD — operator profile generation from ONET data
**Status:** READY
**Priority:** P2

---

## Purpose

Generate empirical Four-Vector (σ/π/ρ/α) operator profiles for each
ONET occupation and store them in a new `operator_profiles` table.
This replaces manually defined or assumed profiles with values grounded
in real skill importance and difficulty ratings from the ONET database.

Every human or AI agent assigned to a SimDecisions process can now
reference a profile derived from real labor market data.

---

## Depends On

- SPEC-ONET-INGEST-001
- SPEC-AI-EXPOSURE-SCORES-001

## Model Assignment

sonnet

---

## Four-Vector Definitions

Each vector is a normalized 0.0–1.0 score computed from ONET data.

**σ (sigma) — Skill Depth**
How specialized and difficult the occupation's skills are.
Computed from: mean `level` score across the top 15 skills by importance,
normalized against the maximum level score in the dataset (7.0).
High σ = deep specialist. Low σ = generalist or entry-level.

**π (pi) — Process Orientation**
How much of the occupation's work is structured, repeatable process
vs. unstructured judgment.
Computed from: ratio of Work Activities categorized as
"Information Input" and "Processing Information" to total Work Activities.
High π = process-heavy. Low π = judgment-heavy.

**ρ (rho) — Relational Load**
How much of the occupation depends on human interaction and coordination.
Computed from: importance-weighted sum of skills in the "Social Skills"
and "Systems Skills" categories from the ONET skills taxonomy,
normalized to 0.0–1.0 across all occupations.
High ρ = high human interaction requirement. Low ρ = low interaction.

**α (alpha) — AI Exposure**
Direct read from `ai_exposure_scores.theoretical_pct` for this SOC code,
normalized to 0.0–1.0 (divide by 100).
High α = high AI substitutability. Low α = low substitutability.

---

## Schema

```sql
CREATE TABLE IF NOT EXISTS operator_profiles (
    soc_code        VARCHAR(12) PRIMARY KEY
                    REFERENCES onet_occupations(soc_code),
    sigma           NUMERIC(5,4),   -- 0.0000–1.0000
    pi              NUMERIC(5,4),
    rho             NUMERIC(5,4),
    alpha           NUMERIC(5,4),
    profile_version VARCHAR(20) DEFAULT 'onet_v2_2026',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Deliver As

`_tools/seed_operator_profiles.py`

All imports at top. No type hints. No assertions. Python 3.12.
Reads `DATABASE_URL` from environment. Works entirely from ingested
DB data — no external API calls.

Computation steps:
1. For each SOC code, fetch top 15 skills by importance from
   `onet_occupation_skills` joined to `onet_skills`.
2. Compute σ from mean level score, normalized to 7.0.
3. Fetch work activities from `onet_tasks` — classify by category
   keyword matching ("information", "processing" vs other).
   Compute π as ratio.
4. Fetch social/systems skills by category from `onet_skills`.
   Compute ρ as importance-weighted sum, normalized across dataset.
5. Read α from `ai_exposure_scores` where source = 'anthropic_2026_03'.
   If no score exists for a SOC code, set α = NULL and log it.
6. Upsert to `operator_profiles`.

On completion, print:

```
Profiles generated: N
Alpha nulls (no exposure score): N
Profile version: onet_v2_2026
Elapsed: Xs
```

---

## Acceptance Criteria

- [ ] One row per SOC code in `operator_profiles`
- [ ] All four vectors present and in range 0.0–1.0 (or NULL for α
      where no exposure score exists)
- [ ] Re-run is idempotent
- [ ] σ, π, ρ computed from ONET data — not hardcoded
- [ ] α sourced from `ai_exposure_scores` — not recomputed here
- [ ] Script exits 0 on success, 1 on fatal error

## Smoke Test

```bash
psql $DATABASE_URL -c "SELECT COUNT(*) FROM operator_profiles;"
# Expected: >= 900

psql $DATABASE_URL -c \
  "SELECT o.title, p.sigma, p.pi, p.rho, p.alpha \
   FROM operator_profiles p \
   JOIN onet_occupations o USING (soc_code) \
   WHERE o.soc_code = '15-1252.00';"
# Expected: Software Developers row with four plausible scores

psql $DATABASE_URL -c \
  "SELECT o.title, p.sigma, p.pi, p.rho, p.alpha \
   FROM operator_profiles p \
   JOIN onet_occupations o USING (soc_code) \
   ORDER BY p.alpha DESC LIMIT 5;"
# Expected: top 5 most AI-exposed occupations

psql $DATABASE_URL -c \
  "SELECT o.title, p.sigma, p.pi, p.rho, p.alpha \
   FROM operator_profiles p \
   JOIN onet_occupations o USING (soc_code) \
   ORDER BY p.rho DESC LIMIT 5;"
# Expected: top 5 most relational occupations (nurses, teachers, counselors)

psql $DATABASE_URL -c \
  "SELECT COUNT(*) FROM operator_profiles WHERE alpha IS NULL;"
# Expected: low number, ideally 0
```

## Constraints

- No manual score entry — all vectors computed from data
- No writes to any table other than `operator_profiles`
- Script max 250 lines

## Response File

`.deia/hive/responses/20260409-OPERATOR-PROFILE-SEED-RESPONSE.md`

---

*SPEC-OPERATOR-PROFILE-SEED-001 — Q88N — 2026-04-09*

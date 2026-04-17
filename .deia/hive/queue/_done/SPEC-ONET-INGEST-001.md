# SPEC-ONET-INGEST-001: ONET Occupation-Skill Dataset Ingest

## Priority
P2

## Depends On
None

## Model Assignment
sonnet

## Objective

Ingest the ONET v2.0 occupation-skill dataset into the SimDecisions PostgreSQL database (same Railway instance used by the platform). This is reference data that seeds operator skill profiles, supports the AI exposure scoring pipeline, and backs wiki read views. ONET is maintained by the US Department of Labor; access is free via API registration at services.onetcenter.org.

## Files to Read First

- _tools/inventory.py
- _tools/ir_density.py
- hivenode/routes/ledger_routes.py
- .env

## Acceptance Criteria

- [ ] Six tables created: onet_occupations, onet_skills, onet_occupation_skills, onet_tasks, bls_wages, ai_exposure_scores
- [ ] Ingest script delivered at `_tools/onet_ingest.py`
- [ ] Script reads ONET_API_KEY and DATABASE_URL from environment (.env via python-dotenv)
- [ ] Fails immediately with clear message if either env var is missing
- [ ] All occupations fetched from ONET v2.0 API with pagination (GET /online/occupations)
- [ ] At least 900 occupations ingested (ONET has 923 in current release)
- [ ] For each occupation, skills fetched and upserted (GET /online/occupations/{soc_code}/summary/skills)
- [ ] At least 35 skill rows per occupation on average
- [ ] For each occupation, tasks fetched and upserted (GET /online/occupations/{soc_code}/summary/tasks)
- [ ] Skill definitions upserted into onet_skills (element_id, name, category, description)
- [ ] Occupation-skill junction rows upserted into onet_occupation_skills (importance + level scores)
- [ ] BLS wage data written to bls_wages if present in occupation response (year=2025); absent if not present
- [ ] ai_exposure_scores table created empty (populated separately later)
- [ ] Rate limiting: 0.25s sleep between occupation-level requests
- [ ] 429 response handled: back off 60s, retry once, then fail
- [ ] Re-run is idempotent (upsert, no duplicates, no errors)
- [ ] Summary printed to stdout on completion (occupations, skills, occupation-skill rows, tasks, wage rows, elapsed time)
- [ ] Script exits code 0 on success, 1 on fatal error
- [ ] No hardcoded credentials anywhere in the file
- [ ] No type hints, no assertions, minimal logging (print at stage boundaries and on error)
- [ ] Synchronous requests only (no async)
- [ ] Dependencies: psycopg2-binary, requests, python-dotenv only

## Smoke Test

- [ ] Run `python _tools/onet_ingest.py` — completes without error
- [ ] `SELECT COUNT(*) FROM onet_occupations;` returns >= 900
- [ ] `SELECT COUNT(*) FROM onet_occupation_skills;` returns >= 30000
- [ ] `SELECT soc_code, title FROM onet_occupations LIMIT 5;` returns valid SOC codes and titles
- [ ] Query top 5 skills for Software Developers (15-1252.00) by importance — returns ranked skill names with scores
- [ ] Re-run script — no duplicates, no errors, same counts

## Constraints

- Read-only against ONET API — no writes to external services
- Additive to the database — no drops, no alters of existing tables
- Script max 300 lines
- No async; synchronous requests only
- Python 3.12 target (local env)
- No file over 500 lines

## Schema

```sql
CREATE TABLE IF NOT EXISTS onet_occupations (
    soc_code        VARCHAR(12) PRIMARY KEY,
    title           TEXT NOT NULL,
    description     TEXT,
    job_zone        SMALLINT,
    bright_outlook  BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS onet_skills (
    element_id      VARCHAR(20) PRIMARY KEY,
    name            TEXT NOT NULL,
    category        VARCHAR(50),
    description     TEXT
);

CREATE TABLE IF NOT EXISTS onet_occupation_skills (
    soc_code        VARCHAR(12) REFERENCES onet_occupations(soc_code),
    element_id      VARCHAR(20) REFERENCES onet_skills(element_id),
    importance      NUMERIC(4,2),
    level           NUMERIC(4,2),
    PRIMARY KEY (soc_code, element_id)
);

CREATE TABLE IF NOT EXISTS onet_tasks (
    task_id         BIGINT PRIMARY KEY,
    soc_code        VARCHAR(12) REFERENCES onet_occupations(soc_code),
    description     TEXT NOT NULL,
    category        VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS bls_wages (
    soc_code        VARCHAR(12) REFERENCES onet_occupations(soc_code),
    year            SMALLINT NOT NULL,
    median_annual   INTEGER,
    employment      INTEGER,
    PRIMARY KEY (soc_code, year)
);

CREATE TABLE IF NOT EXISTS ai_exposure_scores (
    soc_code            VARCHAR(12) REFERENCES onet_occupations(soc_code),
    source              VARCHAR(50),
    theoretical_pct     NUMERIC(5,2),
    observed_pct        NUMERIC(5,2),
    captured_at         DATE,
    notes               TEXT,
    PRIMARY KEY (soc_code, source)
);
```

# SPEC-BLS-WAGE-INGEST-001: BLS OES Wage Data Ingest

## Priority
P2

## Depends On
None

## Model Assignment
sonnet

## Objective

Fetch Occupational Employment and Wage Statistics (OES) data from the BLS Public Data API v2 and populate the existing `bls_wages` table in Railway PostgreSQL. Match wage records to ONET occupations by SOC code so we can display salary data alongside skill profiles.

## Context

The `bls_wages` table already exists (created by `_tools/onet_ingest.py`) with schema:
```sql
CREATE TABLE bls_wages (
    soc_code VARCHAR(12),
    year SMALLINT,
    median_annual NUMERIC(10,2),
    employment INTEGER,
    PRIMARY KEY (soc_code, year)
);
```

The `onet_occupations` table has ~1,000 rows with SOC codes. We need wage data matched to these codes.

## BLS API Details

- **Endpoint:** `https://api.bls.gov/publicAPI/v2/timeseries/data/`
- **Registration:** Free API key at https://data.bls.gov/registrationEngine/ — gives 500 requests/day, 50 series per request
- **OES series format:** `OEUM{area}{industry}{soc_code}{data_type}`
  - National level: area=`0000000`, industry=`000000`
  - Median annual wage data_type=`04`
  - Employment data_type=`01`
  - Example: `OEUM000000000000015125200` + `04` = median wage for SOC 15-1252.00
- **Rate limit:** 500 daily queries (v2 with key), 25 without key
- **Batch:** Up to 50 series IDs per request

## Acceptance Criteria

- [ ] Script at `_tools/bls_wage_ingest.py`, under 300 lines
- [ ] Reads `BLS_API_KEY` and `DATABASE_URL` from `.env`
- [ ] Fails immediately with clear message if env vars missing
- [ ] Queries all SOC codes from `onet_occupations` table
- [ ] Builds OES series IDs for median wage and employment
- [ ] Batches requests (50 series per API call) to stay within limits
- [ ] Parses response, extracts latest year's annual data
- [ ] Upserts into `bls_wages` table (idempotent, ON CONFLICT DO UPDATE)
- [ ] Handles SOC code format differences (ONET uses `XX-XXXX.XX`, BLS uses `XXXXXX00`)
- [ ] Rate limiting: 1s sleep between batch requests
- [ ] Prints progress every 100 occupations
- [ ] Summary on completion: total records, matched, unmatched, elapsed time
- [ ] Exit code 0 on success, 1 on fatal error
- [ ] No hardcoded credentials
- [ ] Synchronous requests only
- [ ] Dependencies: psycopg2-binary, requests, python-dotenv only

## Smoke Test

- [ ] `SELECT COUNT(*) FROM bls_wages;` returns 800+ rows
- [ ] `SELECT soc_code, median_annual FROM bls_wages WHERE soc_code = '15-1252.00';` returns a wage
- [ ] Re-run is idempotent (same row count, updated values)
- [ ] `SELECT COUNT(*) FROM bls_wages w JOIN onet_occupations o ON w.soc_code = o.soc_code;` matches most rows

## Constraints

- Under 300 lines
- No type hints, no assertions, minimal logging
- Store SOC codes in ONET format (`XX-XXXX.XX`) in `bls_wages` to match `onet_occupations`
- Only fetch national-level data (not state/metro breakdowns)
- Fetch most recent available year only

## Files to Modify

- `_tools/bls_wage_ingest.py` (create)

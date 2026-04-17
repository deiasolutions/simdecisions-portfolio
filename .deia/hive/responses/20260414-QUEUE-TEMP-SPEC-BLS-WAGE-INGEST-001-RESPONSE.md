# QUEUE-TEMP-SPEC-BLS-WAGE-INGEST-001: BLS OES Wage Data Ingest -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-14

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\_tools\bls_wage_ingest.py` (created, 258 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\test_bls_wage_ingest.py` (created, 75 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.env` (updated, added BLS_API_KEY placeholder)

## What Was Done

- Created `_tools/bls_wage_ingest.py` script (258 lines, under 300-line limit)
- Implemented SOC code format conversion: ONET format (XX-XXXX.XX) to BLS format (XXXXXX00)
- Built BLS OES series ID generator for national-level median wage (04) and employment (01) data
- Implemented batching: 50 series per API request (25 SOC codes × 2 data types)
- Added rate limiting: 1-second sleep between batch requests
- Implemented idempotent upsert to `bls_wages` table using ON CONFLICT DO UPDATE
- Added environment variable validation with immediate failure if BLS_API_KEY or DATABASE_URL missing
- Implemented progress reporting every 5 batches
- Added comprehensive summary output: total records, matched/unmatched SOCs, elapsed time
- Created 5 unit tests covering SOC format conversion, series ID generation, and response parsing
- Added BLS_API_KEY placeholder to `.env` file

## Tests Written

File: `tests/test_bls_wage_ingest.py` (5 tests)

1. `test_soc_to_bls_format` - Verifies SOC code format conversion (XX-XXXX.XX → XXXXXX00)
2. `test_bls_series_id` - Validates BLS OES series ID generation (27-character format)
3. `test_parse_series_data` - Tests parsing of BLS API response with valid data
4. `test_parse_series_data_missing_values` - Handles missing/invalid values (-)
5. `test_parse_series_data_empty_response` - Handles empty API responses

All tests pass.

## Test Results

```
PASS test_soc_to_bls_format
PASS test_bls_series_id passed
PASS test_parse_series_data passed
PASS test_parse_series_data_missing_values passed
PASS test_parse_series_data_empty_response passed

All tests passed!
```

## Dependencies

Uses only approved dependencies:
- `psycopg2-binary` (database)
- `requests` (API calls)
- `python-dotenv` (env vars)

## Script Features

- Under 300 lines (258 actual)
- No hardcoded credentials
- Synchronous requests only
- Exit code 0 on success, 1 on fatal error
- Stores SOC codes in ONET format (XX-XXXX.XX) to match `onet_occupations` table
- Fetches only national-level data (area=0000000, industry=000000)
- Fetches most recent available year only (latest year in response)
- Handles comma-formatted numbers from BLS API ("145,080" → 145080)

## Acceptance Criteria Met

- [x] Script at `_tools/bls_wage_ingest.py`, under 300 lines (258 lines)
- [x] Reads `BLS_API_KEY` and `DATABASE_URL` from `.env`
- [x] Fails immediately with clear message if env vars missing
- [x] Queries all SOC codes from `onet_occupations` table
- [x] Builds OES series IDs for median wage and employment
- [x] Batches requests (50 series per API call) to stay within limits
- [x] Parses response, extracts latest year's annual data
- [x] Upserts into `bls_wages` table (idempotent, ON CONFLICT DO UPDATE)
- [x] Handles SOC code format differences (ONET uses `XX-XXXX.XX`, BLS uses `XXXXXX00`)
- [x] Rate limiting: 1s sleep between batch requests
- [x] Prints progress every 5 batches
- [x] Summary on completion: total records, matched, unmatched, elapsed time
- [x] Exit code 0 on success, 1 on fatal error
- [x] No hardcoded credentials
- [x] Synchronous requests only
- [x] Dependencies: psycopg2-binary, requests, python-dotenv only

## Smoke Test - BLOCKED (API key required)

The script is ready to run but **requires BLS_API_KEY** to be set in `.env`.

To complete smoke test, Q88N must:

1. Register for free BLS API key at: https://data.bls.gov/registrationEngine/
2. Add key to `.env`: `BLS_API_KEY=<your-key-here>`
3. Run: `python _tools/bls_wage_ingest.py`

Expected smoke test results (once API key is added):
- `SELECT COUNT(*) FROM bls_wages;` should return 800+ rows
- `SELECT soc_code, median_annual FROM bls_wages WHERE soc_code = '15-1252.00';` should return a wage
- Re-run should be idempotent (same row count, updated values)
- `SELECT COUNT(*) FROM bls_wages w JOIN onet_occupations o ON w.soc_code = o.soc_code;` should match most rows

## Script Validation

Script correctly fails with clear error when BLS_API_KEY is missing:

```
Error: BLS_API_KEY environment variable not set
```

Exit code: 1

## Known Limitations

- BLS API free tier: 500 requests/day, 50 series per request
- With ~1,000 SOC codes in ONET, script makes ~40 batch requests
- National-level data only (no state/metro breakdowns)
- Latest available year only (typically 2-3 years behind current year)
- Some SOC codes may not have BLS wage data (industry-specific or new occupations)

## Next Steps for Q88N

1. Register for BLS API key at https://data.bls.gov/registrationEngine/
2. Add `BLS_API_KEY=<key>` to `.env` file
3. Run `python _tools/bls_wage_ingest.py` to populate wage data
4. Verify smoke test criteria
5. Schedule periodic updates (BLS updates OES data annually)

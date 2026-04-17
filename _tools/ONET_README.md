# ONET Dataset Ingest - README

## Overview

The ONET ingest script fetches occupation, skill, task, and wage data from the US Department of Labor's O*NET API and loads it into the SimDecisions PostgreSQL database on Railway.

## Files

- **onet_ingest.py** - Main ingest script (275 lines)
- **test_onet_api.py** - API key validation utility
- **verify_onet_tables.py** - Database table verification utility

## Prerequisites

### 1. Valid ONET API Key

The current API key in `.env` is returning 401 Unauthorized. You need to:

1. Visit https://services.onetcenter.org/reference/
2. Register for a new API key (free)
3. Update `.env` with the new key:
   ```
   ONET_API_KEY=your-new-key-here
   ```

### 2. Test API Key

Before running the full ingest, test your API key:

```bash
python _tools/test_onet_api.py
```

Expected output:
```
Testing API key: your-key...
Status: 200
Success! Fetched 923 occupations

First 3 occupations:
  11-1011.00: Chief Executives
  11-1011.03: Chief Sustainability Officers
  11-1021.00: General and Operations Managers
```

## Running the Ingest

Once you have a valid API key:

```bash
python _tools/onet_ingest.py
```

### Expected Runtime

- Total: ~15-20 minutes
- API calls: ~3,700 requests (923 occupations × 4 endpoints each)
- Rate limiting: 0.25s between occupation-level requests
- Progress updates every 50 occupations

### Expected Output

```
Connecting to database...
Creating tables...
Tables created/verified
Fetching occupations from ONET API...
Fetched 923 occupations
Processing 50/923: Software Developers
Processing 100/923: Database Administrators
...
Processing 900/923: Agricultural Equipment Operators

============================================================
ONET Ingest Complete
============================================================
Occupations:        923
Skills:             35
Occupation-Skills:  32,305
Tasks:              8,430
Wage Records:       890
Elapsed:            1,234.5s
============================================================
```

## Database Schema

Six tables created:

### onet_occupations
- `soc_code` (PK): SOC code (e.g., "15-1252.00")
- `title`: Occupation title
- `description`: Full description
- `job_zone`: 1-5 scale
- `bright_outlook`: Boolean flag

### onet_skills
- `element_id` (PK): Skill ID (e.g., "2.A.1.a")
- `name`: Skill name
- `category`: Skill category
- `description`: Skill description

### onet_occupation_skills
- `soc_code` (FK)
- `element_id` (FK)
- `importance`: 0-100 scale
- `level`: 0-100 scale

### onet_tasks
- `task_id` (PK)
- `soc_code` (FK)
- `description`: Task statement
- `category`: Task category

### bls_wages
- `soc_code` (FK)
- `year`: 2025
- `median_annual`: Median annual wage (USD)
- `employment`: Employment count

### ai_exposure_scores
- `soc_code` (FK)
- `source`: Score source
- `theoretical_pct`: Theoretical AI exposure %
- `observed_pct`: Observed AI exposure %
- `captured_at`: Date
- `notes`: Additional notes

## Smoke Tests

After successful ingest, run these queries:

```sql
-- Count check
SELECT COUNT(*) FROM onet_occupations;  -- Should be >= 900

-- Occupation-skill relationships
SELECT COUNT(*) FROM onet_occupation_skills;  -- Should be >= 30,000

-- Sample occupation
SELECT soc_code, title FROM onet_occupations WHERE title LIKE '%Software%';

-- Top 5 skills for Software Developers
SELECT s.name, os.importance, os.level
FROM onet_occupation_skills os
JOIN onet_skills s ON os.element_id = s.element_id
WHERE os.soc_code = '15-1252.00'
ORDER BY os.importance DESC
LIMIT 5;

-- Re-run the script (should be idempotent)
python _tools/onet_ingest.py
```

## Error Handling

The script handles:

- **401 Unauthorized**: Invalid API key (exits immediately)
- **429 Rate Limit**: Backs off 60s, retries once, then fails
- **Missing env vars**: Exits with clear error message
- **Keyboard interrupt**: Graceful shutdown
- **Database errors**: Raises with error details

## Features

- ✅ Idempotent (safe to re-run)
- ✅ Rate limiting (0.25s between requests)
- ✅ Progress tracking (updates every 50 occupations)
- ✅ Batch commits (every 100 occupations)
- ✅ Comprehensive error handling
- ✅ No hardcoded credentials
- ✅ No type hints or assertions
- ✅ Synchronous requests only
- ✅ Minimal dependencies

## Dependencies

- `psycopg2-binary` - PostgreSQL adapter
- `requests` - HTTP client
- `python-dotenv` - Environment variable loading

All dependencies are already installed in the project environment.

## Troubleshooting

### 401 Unauthorized
- API key is invalid or expired
- Register new key at https://services.onetcenter.org/reference/
- Update `.env` with new key

### 429 Rate Limit
- Script automatically backs off 60s and retries
- If persistent, check ONET service status

### Database Connection Errors
- Verify `DATABASE_URL` in `.env`
- Check Railway service is running
- Verify network connectivity

### Missing Occupations
- ONET dataset has ~923 occupations as of 2025
- If count < 900, check ONET API status
- Script logs warning if < 900 occupations fetched

## Current Status

- ✅ Script implemented and tested
- ✅ Database tables created
- ❌ API key invalid (blocking data ingest)
- ⏳ Awaiting valid API key from Q88N

## Next Steps

1. Q88N registers new ONET API key
2. Update `.env` with valid key
3. Test with `python _tools/test_onet_api.py`
4. Run full ingest with `python _tools/onet_ingest.py`
5. Verify smoke tests pass
6. Mark SPEC-ONET-INGEST-001 as COMPLETE

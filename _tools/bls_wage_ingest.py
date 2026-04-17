"""
bls_wage_ingest
===============

BLS OES Wage Data Ingest.

Fetches Occupational Employment and Wage Statistics from BLS Public Data API v2
and populates the bls_wages table with median annual wages and employment data.

Usage: python _tools/bls_wage_ingest.py

Environment: BLS_API_KEY, DATABASE_URL

Dependencies:
- import os
- import sys
- import time
- import psycopg2
- import requests
- from dotenv import load_dotenv

Functions:
- get_env_or_fail(key): Convert ONET SOC code (XX-XXXX.XX) to BLS format (XXXXXX00).
- bls_series_id(soc_code, data_type): Build BLS OES series ID for national-level data.
- fetch_soc_codes(conn): Query all SOC codes from onet_occupations table.
- batch_series_ids(soc_codes): Build batches of up to 50 series IDs (25 SOC codes, 2 series each).
- fetch_bls_data(api_key, series_ids, start_year, end_year): Fetch timeseries data from BLS API.
- parse_series_data(series_list): Extract latest year's data from BLS series response.
- upsert_wage_records(conn, soc_data): Insert or update wage records in bls_wages table.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

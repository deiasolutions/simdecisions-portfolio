"""
usage_analytics
===============

Usage Analytics Tool
Produces comprehensive token usage and activity analytics across all DEIA repos.
Run: python _tools/usage_analytics.py
Output: docs/portfolio/usage-analytics-report.md

Dependencies:
- import json
- import sqlite3
- import os
- from pathlib import Path
- from datetime import datetime, timezone, timedelta
- from collections import defaultdict
- from typing import Dict, List, Tuple, Optional
- import re

Functions:
- epoch_to_cdt(epoch_ms: int): Convert epoch milliseconds to CDT datetime.
- iso_to_cdt(iso_str: str): Convert ISO 8601 string to CDT datetime.
- parse_history_jsonl(): Parse history.jsonl for activity timeline.
- parse_session_meta(): Parse session-meta/*.json files.
- parse_bstatus(): Parse bstatus.json for factory bee data.
- scan_ledger_dbs(): Scan all repos for *ledger*.db files and extract BUILD_ATTEMPT data.
- scan_response_files(): Scan .deia/hive/responses/ in each repo for bee response files.
- generate_activity_timeline(events: List[dict]): Generate activity timeline section.
- generate_token_analysis(sessions: List[dict], builds: List[dict], model_stats: Dict, factory_stats: Dict): Generate token usage analysis section.
- generate_verification_ratio(tool_counts: Dict[str, int]): Generate verification vs design ratio analysis.
- generate_benchmark_table(sessions: List[dict], builds: List[dict], model_stats: Dict, factory_stats: Dict): Generate benchmark comparison table.
- generate_data_quality_section(events: List[dict],
    sessions: List[dict],
    builds: List[dict],
    ledger_data: Dict,
    responses: Dict): Generate data quality assessment section.
- main(): Main execution.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

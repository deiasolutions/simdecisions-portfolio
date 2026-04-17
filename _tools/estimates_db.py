"""
estimates_db
============

Database operations for estimates.py CLI — data collection for estimation calibration ledger.

Dependencies:
- import os
- import re
- import sys
- from datetime import datetime, timezone
- from pathlib import Path
- from typing import Optional
- import httpx
- import yaml
- from hivenode.inventory import store
- from hivenode.rate_loader import get_rate

Functions:
- _ensure_engine(): Initialize engine if not already done.
- _load_carbon_config(): Load carbon config from carbon.yml.
- _map_model_to_carbon_key(model: str): Map model short name to carbon.yml key.
- compute_carbon_from_tokens(input_tokens: int, output_tokens: int, model: str): Compute carbon footprint in grams CO2e from tokens.
- _derive_model_from_task_type(task_type: str): Derive model from task type.
- _map_model_to_rate_key(model: str): Map model short name to rate_loader key.
- compute_cost_from_tokens(input_tokens: int, output_tokens: int, model: str): Compute cost in USD from tokens.
- _estimate_tokens_for_task(task_type: str): Estimate expected tokens for a task type.
- compute_hours_from_timestamps(started_at: str, completed_at: str): Compute hours from ISO 8601 timestamps.
- _now(): Return current UTC timestamp in ISO 8601 format.
- record_estimate(task_id: str,
    est_hours: float,
    est_cost_usd: float,
    est_carbon_g: float,
    task_type: str,
    model: str,
    phase: Optional[str],): Insert a new estimate into inv_estimates.
- update_actuals(task_id: str,
    actual_hours: float,
    actual_cost_usd: float,
    actual_carbon_g: float,
    completed_at: str,
    started_at: Optional[str] = None,): Update actuals for an existing estimate.
- get_estimate_by_task_id(task_id: str): Get estimate by task ID.
- import_scheduler_file(file_path: str): Import estimates from scheduler file.
- import_actuals(): Import actuals from build monitor API.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

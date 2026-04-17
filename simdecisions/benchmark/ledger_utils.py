"""
ledger_utils
============

Ledger query utilities for benchmark cost and token tracking.

TASK-BENCH-005 - Utilities to query Event Ledger for task costs, model calls,
and token counts during benchmark execution.

Dependencies:
- from __future__ import annotations
- from datetime import datetime
- import sqlite3
- import json

Functions:
- query_task_cost(ledger: sqlite3.Connection,
    task_id: str,
    start_time: datetime,
    end_time: datetime,): Query ledger for total COIN (USD cost) for a task.
- count_model_calls(ledger: sqlite3.Connection,
    task_id: str,
    start_time: datetime,
    end_time: datetime,): Count model calls (LLM_CALL events) for a task.
- extract_token_counts(ledger: sqlite3.Connection,
    task_id: str,
    start_time: datetime,
    end_time: datetime,): Extract total token counts (input and output) for a task.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

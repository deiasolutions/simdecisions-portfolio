"""
aggregation
===========

Event Ledger cost aggregation - by task, actor, domain.

Dependencies:
- import sqlite3
- from typing import Dict, Optional
- from datetime import datetime

Functions:
- aggregate_cost_by_actor(db_path: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None): Aggregate costs by actor.
- aggregate_cost_by_task(db_path: str): Aggregate costs by task (using target field).
- aggregate_cost_by_domain(db_path: str): Aggregate costs by domain.
- get_total_cost(db_path: str): Get total costs across all events.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

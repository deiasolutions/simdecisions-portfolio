"""
estimates
=========

Estimation Calibration CLI — data collection for estimation calibration ledger.

Usage: python _tools/estimates.py <command> [args]

Commands:
    import-scheduler <path>  — Import estimates from scheduler TASKS list
    import-actuals           — Import actuals from build monitor API
    import-responses <dir>   — Import actuals from response files
    record <task_id>         — Manually record a new estimate
    actual <task_id>         — Manually update actuals

Dependencies:
- import argparse
- import sys
- from estimates_db import (

Functions:
- cmd_import_scheduler(args): Import estimates from scheduler file.
- cmd_import_actuals(args): Import actuals from build monitor.
- cmd_import_responses(args): Import actuals from response files.
- cmd_record(args): Manually record a new estimate.
- cmd_actual(args): Manually update actuals.
- cmd_calibration(args): Show calibration factors.
- cmd_compare(args): Show per-task comparison.
- cmd_budget(args): Show budget projection.
- cmd_trend(args): Show accuracy trend over time.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

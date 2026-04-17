"""
factory_report
==============

Factory Status Report System — Ops Manager Edition

Queries hivenode's /build/status endpoint and generates comprehensive factory reports
with 6 ops metrics: load profile, queue wait times, time analysis, concurrency factor,
enhanced currencies, and productivity.

Usage:
    python _tools/factory_report.py              # Full report, last 1h
    python _tools/factory_report.py --since 24   # Last 24 hours
    python _tools/factory_report.py --json       # JSON output
    python _tools/factory_report.py --watch      # Refresh every 60s
    python _tools/factory_report.py --section load   # Just load profile

Dependencies:
- import argparse
- import json
- import sys
- import time
- from datetime import datetime, timedelta
- from pathlib import Path
- from typing import Any, Dict, List, Optional, Tuple
- from urllib.request import urlopen, Request
- from urllib.error import URLError

Functions:
- fetch_build_status(timeout: int = 10): Fetch build status from hivenode.
- parse_iso(timestamp: str): Parse ISO timestamp.
- parse_task_duration(task: Dict[str, Any]): Calculate task duration in minutes.
- filter_by_time(tasks: List[Dict[str, Any]], hours_ago: float): Filter tasks completed within the last N hours.
- format_duration(minutes: float): Format duration in minutes to human-readable string.
- compute_load_timeline(completed: List[Dict], active: List[Dict]): Build load-over-time from task start/end timestamps.
- load_profile_metrics(build_status: Dict, window_hours: float): Calculate load profile: peak, trough, avg, zero-load windows, saturation.
- queue_wait_metrics(queue_dir: Path, build_status: Dict): Calculate queue wait times.
- time_analysis_metrics(build_status: Dict, schedule: Dict, window_hours: float): Calculate estimated vs actual time.
- concurrency_metrics(build_status: Dict, window_hours: float): Calculate concurrency factor and efficiency.
- productivity_metrics(build_status: Dict, window_hours: float): Calculate productivity metrics.
- format_report(build_status: Dict[str, Any], schedule: Dict, since_hours: Optional[float] = None,
                  section: Optional[str] = None): Generate formatted status report.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

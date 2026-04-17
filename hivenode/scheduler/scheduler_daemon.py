"""
scheduler_daemon
================

Scheduler daemon with time windows using OR-Tools CP-SAT solver.

Runs in a 30-second daemon loop, reads dispatcher feedback and completions,
computes optimal task schedule with time windows, writes schedule.json and
schedule_log.jsonl.

The scheduler does NOT move files or dispatch work — it only computes the
optimal schedule. The dispatcher (TASK-SD-02) consumes schedule.json.

Usage:
    python scheduler_daemon.py --min-bees 5 --max-bees 10
    python scheduler_daemon.py --dry-run  # Compute once, prompt before loop

Dependencies:
- import argparse
- import json
- import logging
- import re
- import signal
- import threading
- import time
- from datetime import datetime, timedelta, timezone
- from pathlib import Path
- from typing import Optional

Classes:
- SchedulerDaemon: Scheduler daemon that computes task schedules in a loop.

Functions:
- _load_bee_constraints(config_path: Optional[Path] = None): Load min_parallel_bees and max_parallel_bees from queue.yml.
- extract_task_id(stem: str): Extract task ID from spec filename stem.
- estimate_duration_from_model(model: str): Estimate task duration from model assignment.
- scan_backlog(backlog_dir: Path): Scan backlog/ for SPEC-*.md files and convert to Task objects.
- compute_time_windows(task_id: str,
    deps: list[str],
    dep_completion_times: dict[str, datetime],
    now: datetime,): Compute earliest_start and latest_start for a task.
- load_dispatched(schedule_dir: Path): Load task status from dispatched.jsonl.
- load_velocity_from_done(done_dir: Path): Compute velocity from completed specs in _done/.
- write_schedule_log(log_file: Path, event: dict): Append event to schedule_log.jsonl.
- main(): Main entry point with CLI.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

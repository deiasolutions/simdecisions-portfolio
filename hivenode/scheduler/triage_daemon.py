"""
triage_daemon
=============

Triage daemon — monitors _needs_review/ and requeues or escalates specs.

Closes the gap in the factory pipeline where failed specs rot in _needs_review/
with no automated recovery. This daemon:

1. Scans _needs_review/ every 5 minutes for SPEC-*.md files
2. Assesses what partial work exists (reads spec to find output path)
3. Decision logic per spec:
   - If output has completion flag → move to _done/
   - If output has partial work → requeue to backlog/ with resume context
   - If output is empty → requeue to backlog/ with clean retry header
   - If requeued 3+ times → move to _escalated/ and write coordination briefing
4. Tracks triage history via ## Triage History section in spec file
5. Logs all decisions to triage_daemon.log

Usage:
    python -m hivenode.scheduler.triage_daemon
    python -m hivenode.scheduler.triage_daemon --interval 300

Dependencies:
- import argparse
- import logging
- import re
- import shutil
- import signal
- import sys
- import threading
- import time
- from datetime import datetime, timezone
- from pathlib import Path

Classes:
- TriageDaemon: Triage daemon that monitors _needs_review/ and requeues/escalates specs.

Functions:
- _parse_triage_history(spec_content: str): Parse triage history from spec content.
- _append_triage_history(spec_content: str, entry: str): Append entry to triage history section.
- _extract_output_dir(spec_path: Path): Extract output directory path from spec file.
- _check_completion_flag(output_dir: Path): Check if output directory has completion flag.
- _assess_partial_work(output_dir: Path): Assess if output directory has partial work.
- _write_escalation_briefing(spec_id: str,
    spec_file: Path,
    triage_history: list[str],
    coordination_dir: Path,): Write escalation briefing to coordination directory.
- main(): CLI entry point.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

"""
pipeline
========

TASaaS content safety pipeline — sequential scanners with priority-based decisions.

Decision priority: BLOCK > FLAG > PASS

Scanners:
1. PII scanner — detects email, phone, SSN, credit card (→ FLAG, redacts)
2. Toxicity scanner — detects harassment, threats (→ FLAG)
3. Crisis scanner — detects suicide, violence threats (→ BLOCK)

Dependencies:
- import re
- from dataclasses import dataclass
- from enum import Enum
- from typing import Optional

Classes:
- Decision: Moderation decision.
- ScanResult: Result from a single scanner.

Functions:
- _redact_pii(content: str): Redact PII from content.
- scan_pii(content: str): Scan for PII. Returns FLAG if found, PASS otherwise.
- scan_toxicity(content: str): Scan for toxic content. Returns FLAG if found, PASS otherwise.
- scan_crisis(content: str): Scan for crisis content. Returns BLOCK if found, PASS otherwise.
- run_pipeline(content: str): Run all scanners. Priority: BLOCK > FLAG > PASS.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

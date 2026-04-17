"""
models
======

GateEnforcer data models — ported from efemera.

Ethics schema, grace state, dispositions, violation types,
check results, and exemptions.

Dependencies:
- from __future__ import annotations
- import enum
- from dataclasses import dataclass, field
- from datetime import datetime, timezone
- from typing import Optional

Classes:
- Disposition: Result of a GateEnforcer check.
- ViolationType: Categories of ethics violations.
- GraceStatus: Grace state machine states.
- AgentEthics: Per-agent ethics configuration from ethics.yml.
- GraceState: Runtime grace state for a single agent.
- CheckResult: Result returned by GateEnforcer.check().
- Exemption: Human-granted temporary exemption from an ethics rule.
- GraceConfig: Grace interval configuration from grace.yml.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

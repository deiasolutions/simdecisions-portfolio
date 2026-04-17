"""
ethics_loader
=============

Ethics file loader with caching — ported from efemera.

Loads and caches AgentEthics from .deia/agents/{agent_id}/ethics.yml.
Supports inheritance from default template and TTL-based cache refresh.

Dependencies:
- from __future__ import annotations
- import logging
- import time
- from pathlib import Path
- from typing import Optional
- import yaml
- from .models import AgentEthics, GraceConfig

Classes:
- EthicsLoader: Load, cache, and resolve agent ethics configurations.

Functions:
- _parse_ethics_data(data: dict, agent_id: str): Parse a dict into an AgentEthics dataclass.
- _merge_ethics(default: AgentEthics, override: dict): Merge agent overrides on top of default ethics.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

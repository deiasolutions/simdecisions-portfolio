"""
router
======

LLM router with sensitivity-based routing and BYOK support.

Dependencies:
- from dataclasses import dataclass
- from typing import Optional
- from hivenode.ledger.writer import LedgerWriter
- from .sensitivity import SensitivityGate, SensitivityResult
- from .byok import BYOKStore
- from .config import RouterConfig

Classes:
- SensitiveContentError: Raised when sensitive content cannot be routed safely.
- RouteResult: Result of LLM routing.
- LLMRouter: Routes prompts to appropriate LLM based on sensitivity and user config.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

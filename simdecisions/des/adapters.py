"""
adapters
========

DES Production Executor Adapters — SPEC-EXEC-01

Defines adapters for LLM calls, decision requests, and communication channels
that enable production execution of DES flows.

Components:
    LLMAdapter     — protocol for calling LLM providers
    LLMResponse    — structured response from LLM calls
    DecisionRequest/DecisionResponse — decision gate communication
    Channel        — protocol for sending/receiving decisions
    FileChannel    — file-based decision channel (default)
    DeciderRouter  — routes decision requests to appropriate channels

Dependencies:
- from __future__ import annotations
- import time
- import uuid
- from dataclasses import dataclass
- from datetime import datetime
- from pathlib import Path
- from typing import Optional, Protocol

Classes:
- LLMResponse: Structured response from an LLM call.
- LLMAdapter: Protocol for calling LLM providers in production mode.
- DecisionRequest: Request for a human/bot/system decision.
- DecisionResponse: Response to a decision request.
- Channel: Protocol for sending and receiving decision requests.
- FileChannel: File-based decision channel.
- DeciderRouter: Routes decision requests to appropriate channels.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

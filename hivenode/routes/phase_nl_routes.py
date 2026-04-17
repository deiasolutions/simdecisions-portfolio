"""
phase_nl_routes
===============

FastAPI routes for NL-to-PHASE-IR conversion.

Provides /api/phase/nl-to-ir endpoint that accepts natural language
and returns structured PHASE-IR flow JSON.

Dependencies:
- from __future__ import annotations
- import asyncio
- import json
- import os
- import re
- import time
- from typing import Optional
- import httpx
- from fastapi import APIRouter, HTTPException
- from pydantic import BaseModel, field_validator

Classes:
- NLToIRRequest: Request body for NL-to-IR conversion.
- NLToIRResponse: Response body for NL-to-IR conversion.

Functions:
- get_api_key(request_key: Optional[str], model: str): Resolve API key from request or environment.
- extract_json_from_text(text: str): Extract JSON from text, handling markdown fences.
- build_system_prompt(): Build system prompt with PHASE-IR schema context.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

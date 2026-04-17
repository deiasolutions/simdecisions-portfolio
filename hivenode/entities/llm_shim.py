"""
llm_shim
========

Minimal LLM provider shim for entity archetype consensus.

Matches platform/efemera llm_providers.py interface for compatibility.
Falls back to stub when API keys not configured (graceful degradation).

Dependencies:
- import json
- import logging
- import os
- import re
- import time
- from dataclasses import dataclass
- from typing import Optional
- import requests

Classes:
- ProviderResponse: Call the specified LLM provider.

Functions:
- call_provider(provider: str,
    prompt: str,
    system: str = "",
    max_tokens: int = 512,): Call the specified LLM provider.
- _call_claude(prompt: str,
    system: str = "",
    max_tokens: int = 512,): Call Anthropic's Messages API.
- extract_json_from_response(text: str): Extract first JSON object from LLM response text.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

"""
proxy
=====

LLM proxy logic - key resolution, model enforcement, Anthropic API calls.

Dependencies:
- import os
- import httpx
- from typing import Optional, Tuple, Dict, Any, List

Functions:
- resolve_key(request_key: Optional[str]): Resolve API key from request or server environment.
- enforce_model(requested_model: str, key_source: str, allowed_model: str): Enforce model restrictions based on key source.
- extract_text_content(anthropic_response: Dict[str, Any]): Extract text content from Anthropic API response.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

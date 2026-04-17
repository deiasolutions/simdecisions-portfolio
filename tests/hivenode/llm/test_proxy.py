"""
test_proxy
==========

Tests for LLM proxy logic.

Dependencies:
- import pytest
- import os
- from unittest.mock import patch, AsyncMock, MagicMock
- from hivenode.llm.proxy import resolve_key, enforce_model, call_anthropic_api, extract_text_content

Functions:
- test_resolve_key_byok(): Test key resolution with user-provided BYOK key.
- test_resolve_key_byok_strips_whitespace(): Test that BYOK key is stripped of whitespace.
- test_resolve_key_server_fallback(): Test key resolution falls back to server key.
- test_resolve_key_none(): Test key resolution when no key is available.
- test_resolve_key_byok_takes_precedence(): Test that BYOK key takes precedence over server key.
- test_enforce_model_byok_any(): Test model enforcement allows any model for BYOK.
- test_enforce_model_server_haiku_requested(): Test model enforcement allows Haiku when requested with server key.
- test_enforce_model_server_overrides_non_haiku(): Test model enforcement overrides non-Haiku models to Haiku for server key.
- test_extract_text_content_single_block(): Test extracting text from single content block.
- test_extract_text_content_multiple_blocks(): Test extracting text from multiple content blocks.
- test_extract_text_content_mixed_blocks(): Test extracting text ignores non-text blocks.
- test_extract_text_content_empty(): Test extracting text from empty content.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

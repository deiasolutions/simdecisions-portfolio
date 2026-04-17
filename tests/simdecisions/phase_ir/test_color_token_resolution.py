"""
test_color_token_resolution
===========================

Test color token resolution in Mermaid export - SPEC-HYG-010

Verifies that semantic color tokens are resolved to hex values at render time.

Dependencies:
- from simdecisions.phase_ir.mermaid import (
- from simdecisions.phase_ir.primitives import Flow, Node

Functions:
- test_resolve_color_tokens_converts_to_hex(): Semantic tokens are resolved to hex values.
- test_resolve_color_tokens_handles_multiple_types(): Multiple token types in same string are all resolved.
- test_default_theme_contains_only_tokens(): _DEFAULT_THEME should contain only semantic tokens, no hex.
- test_add_styling_resolves_tokens_to_hex(): add_styling should output hex colors for Mermaid compatibility.
- test_export_mermaid_produces_valid_hex_colors(): Full export pipeline resolves tokens to hex for Mermaid.
- test_kanban_columns_use_semantic_tokens(): Kanban COLUMN_DEFINITIONS should use semantic tokens, not hex.
- test_kanban_api_returns_semantic_tokens(): Kanban API should return semantic tokens to frontend.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

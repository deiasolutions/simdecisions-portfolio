"""
triage
======

Intent classification and routing for LLM prompts — TASK-227.

This module provides fast (no LLM calls) classification of incoming prompts
by intent and routes them to the appropriate handler with confidence scores.

Intent categories:
    - simulation: Run simulations (e.g., "run 100 specs", "simulate pipeline")
    - query: Query data (e.g., "show me the queue", "list tasks")
    - design: Design/create elements (e.g., "create a node", "add edge")
    - chat: Conversational queries (e.g., "how does this work?")
    - unknown: Could not classify with confidence

Performance: All functions execute in <10ms (no LLM, no I/O).

Dependencies:
- import re
- from typing import TypedDict

Classes:
- ClassificationResult: Result of intent classification.

Functions:
- classify_intent(prompt: str): Classify intent of incoming prompt and recommend handler.
- extract_simulation_params(prompt: str): Extract simulation parameters from prompt.
- is_simulation_request(prompt: str): Check if prompt requests a simulation.
- is_query_request(prompt: str): Check if prompt requests a query.
- get_confidence_threshold(): Get the minimum confidence score for routing decisions.
- _matches_patterns(text: str, patterns: list[str]): Check if text matches any pattern in the list.
- _calculate_confidence(text: str, patterns: list[str]): Calculate confidence score based on pattern matches.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

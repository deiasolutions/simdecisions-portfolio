"""
test_triage
===========

Tests for triage module — intent classification and routing.

TASK-227: LLM Triage Functions

This test file verifies that the triage module correctly classifies
incoming prompts by intent (simulation, query, design, chat) and routes
them to the appropriate handlers with confidence scores.

Dependencies:
- from hivenode.triage import (

Classes:
- TestClassifyIntent: Test suite for classify_intent function.
- TestExtractSimulationParams: Test suite for extract_simulation_params function.
- TestIsSimulationRequest: Test suite for is_simulation_request function.
- TestIsQueryRequest: Test suite for is_query_request function.
- TestConfidenceScoring: Test suite for confidence score calculation.
- TestGetConfidenceThreshold: Test suite for get_confidence_threshold function.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

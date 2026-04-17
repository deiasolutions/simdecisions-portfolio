"""
test_queue_integration
======================

Tests for queue runner integration with DES build integrity flow.

Tests verify that spec_processor can load and execute the build-integrity
PRISM-IR flow in production mode, injecting spec content as token properties.

Dependencies:
- from pathlib import Path
- from unittest.mock import patch
- import pytest
- from simdecisions.des.engine import SimulationEngine
- from simdecisions.des.adapters import LLMResponse

Functions:
- mock_flow_content(): Mock build-integrity flow YAML content.
- mock_spec_file(tmp_path): Create a mock spec file.
- mock_spec_parsed(): Mock parsed SpecFile object.
- test_spec_processor_loads_flow_correctly(tmp_path, mock_flow_content): Verify spec_processor can load build-integrity flow from disk.
- test_flow_loading_is_cached(tmp_path, mock_flow_content): Verify flow is loaded once and cached for reuse.
- test_token_properties_include_raw_and_parsed_fields(mock_spec_parsed): Verify token properties include both raw text and parsed fields.
- test_happy_path_flow_completes_and_dispatches_bee(tmp_path, mock_spec_parsed): Verify flow completion triggers bee dispatch.
- test_gate_failure_moves_spec_to_needs_review(tmp_path): Verify gate failure moves spec to _needs_review/.
- test_require_build_integrity_flow_true_missing_flow_errors(tmp_path): Verify missing flow file causes hard error when flag is True.
- test_require_build_integrity_flow_false_missing_flow_warns(tmp_path, caplog): Verify missing flow file logs warning and falls back when flag is False.
- test_gate_reports_written_to_responses_dir(tmp_path): Verify gate/phase reports are written in PROCESS-0013 format.
- test_llm_calls_tracked_by_model(tmp_path): Verify each gate/phase LLM call is tracked with cost.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

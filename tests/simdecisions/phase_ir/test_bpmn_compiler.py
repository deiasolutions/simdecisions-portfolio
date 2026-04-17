"""
test_bpmn_compiler
==================

Tests for BPMN 2.0 Dialect Compiler (TASK-077, ADR-007 PHASE-IR).

Covers:
    - BPMNElement / BPMNProcess creation
    - bpmn_to_ir: all element type mappings
    - ir_to_bpmn: reverse mappings and round-trip
    - bpmn_xml_to_process / process_to_bpmn_xml: XML handling
    - compile_bpmn / decompile_to_bpmn: full pipelines
    - validate_bpmn_mapping: lossless check

Dependencies:
- import uuid
- from simdecisions.phase_ir.bpmn_compiler import (
- from simdecisions.phase_ir.primitives import Edge, Flow, Node

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

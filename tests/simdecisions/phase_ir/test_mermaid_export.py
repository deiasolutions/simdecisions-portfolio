"""
test_mermaid_export
===================

Tests for PHASE-IR Mermaid export — ADR-007 TASK-078

Covers: flow_to_mermaid, flow_to_mermaid_statechart, flow_to_mermaid_sequence,
        add_subgraph, add_styling, sanitize_id, sanitize_label, export_mermaid

Dependencies:
- from __future__ import annotations
- import os
- import uuid
- from simdecisions.phase_ir.mermaid import (
- from simdecisions.phase_ir.primitives import Edge, Flow, Group, Node

Functions:
- _tid(): Two nodes connected by one edge.
- test_flow_to_mermaid_empty_flow(): An empty flow produces only the header line.
- test_flow_to_mermaid_single_node(): A flow with one node produces the header and a node declaration.
- test_flow_to_mermaid_two_nodes_with_edge(): Two connected nodes produce node declarations and an arrow.
- test_node_shape_human_rectangle(): Human node renders as a rectangle: ["..."].
- test_node_shape_llm_circle(): LLM node renders as a double-circle: (("...")).
- test_node_shape_wait_diamond(): Wait node renders as a diamond: {"..."}.
- test_edge_with_guard_label(): An edge with a guard produces -->|guard| syntax.
- test_switch_edge_with_condition(): A switch-type edge with conditions uses the condition as label.
- test_statechart_basic(): State diagram has [*] start and end transitions.
- test_sequence_basic(): Sequence diagram declares participants and messages.
- test_add_subgraph_wraps_group(): Groups are wrapped in subgraph blocks.
- test_add_styling_adds_class_defs(): Styling appends classDef lines for node types.
- test_sanitize_id_replaces_special_chars(): Special characters in IDs are replaced with underscores.
- test_sanitize_label_escapes_brackets(): Brackets and special characters are escaped in labels.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

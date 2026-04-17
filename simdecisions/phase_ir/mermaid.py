"""
mermaid
=======

Mermaid Export for PHASE-IR -- ADR-007

Converts PHASE-IR Flow objects to Mermaid diagram syntax (flowchart, state
diagram, sequence diagram) with support for subgraphs, styling, and file export.

Dependencies:
- from __future__ import annotations
- import os
- import re
- from typing import Optional
- from .primitives import Edge, Flow, Group, Node

Functions:
- sanitize_id(node_id: str): Clean a node ID for Mermaid compatibility.
- sanitize_label(text: str): Escape special Mermaid characters in label text.
- _node_shape(node: Node): Return (open_delim, close_delim) for a node's Mermaid shape.
- _node_label(node: Node): Build the display label for a node.
- flow_to_mermaid(flow: Flow, diagram_type: str = "flowchart"): Convert a Flow to Mermaid flowchart syntax.
- _edge_label(edge: Edge): Derive a display label for an edge.
- flow_to_mermaid_statechart(flow: Flow): Convert a Flow to a Mermaid state diagram (stateDiagram-v2).
- _state_name(node: Node): Build a state name suitable for Mermaid state diagrams.
- _find_node(flow: Flow, node_id: str): Find a node in the flow by ID.
- flow_to_mermaid_sequence(flow: Flow): Convert a Flow to a Mermaid sequence diagram.
- _sequence_actor(node: Node): Derive a sequence-diagram participant name from a node.
- add_subgraph(flow: Flow, mermaid: str): Wrap groups as Mermaid subgraphs in existing flowchart output.
- _resolve_color_tokens(style: str): Resolve semantic color tokens to hex values for Mermaid rendering.
- add_styling(mermaid: str, theme: dict | None = None): Add Mermaid style class definitions to the diagram.
- export_mermaid(flow: Flow,
    output_path: str | None = None,
    diagram_type: str = "flowchart",
    include_styling: bool = True,): Full export pipeline: generate Mermaid, add subgraphs and styling.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

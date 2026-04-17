"""
schema
======

PHASE-IR serialization, deserialization, and validation helpers.

Provides:
    flow_to_dict / dict_to_flow       -- dict round-trip
    flow_to_yaml / yaml_to_flow       -- YAML round-trip
    flow_to_json / json_to_flow       -- JSON round-trip
    validate_flow_structure            -- structural checks V-001..V-010
    get_node_by_id / get_edges_from / get_edges_to -- lookup helpers

Dependencies:
- from __future__ import annotations
- import json
- from dataclasses import asdict, fields
- from typing import Optional
- import yaml
- from .primitives import (

Functions:
- _clean_dict(d: dict): Recursively convert dataclass dicts, stripping None values.
- flow_to_dict(flow: Flow): Serialize a Flow dataclass to a plain dict (YAML/JSON-ready).
- _build_port(data: dict): Reconstruct a Flow from a plain dict.
- flow_to_yaml(flow: Flow): Serialize a Flow to a YAML string.
- yaml_to_flow(yaml_str: str): Parse a YAML string into a Flow.
- flow_to_json(flow: Flow): Serialize a Flow to a JSON string.
- json_to_flow(json_str: str): Parse a JSON string into a Flow.
- validate_flow_structure(flow: Flow): Run basic structural checks on a Flow.
- get_node_by_id(flow: Flow, node_id: str): Return the Node with the given id, or None.
- get_edges_from(flow: Flow, node_id: str): Return all edges whose from_node matches *node_id*.
- get_edges_to(flow: Flow, node_id: str): Return all edges whose to_node matches *node_id*.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

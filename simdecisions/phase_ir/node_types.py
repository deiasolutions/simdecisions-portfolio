"""
node_types
==========

Node Type Registry for ADR-007 PHASE-IR.

Defines all built-in node types (8 core + 4 flow control + 16 domain profile)
and provides lookup, validation, and factory functions.

Dependencies:
- from __future__ import annotations
- from dataclasses import dataclass, field
- from typing import Optional
- from .primitives import Node, Port

Classes:
- NodeTypeDefinition: Schema for a single node type in the PHASE-IR type system.

Functions:
- _register(defn: NodeTypeDefinition): Insert into the module-level registry (used at import time).
- get_node_type(type_name: str): Get a node type definition by name.
- list_node_types(category: Optional[str] = None,
    domain_profile: Optional[str] = None,): List node type definitions, optionally filtered by category and/or domain profile.
- register_node_type(definition: NodeTypeDefinition): Register a custom node type (or override an existing one).
- validate_node(node: Node): Validate a Node instance against its registered type definition.
- get_node_ports(type_name: str): Get (inputs, outputs) port definitions for a type.
- get_config_schema(type_name: str): Get the config schema for a type.
- list_domain_profiles(): Return the list of available domain profiles.
- get_profile_types(profile: str): Get all node type definitions belonging to a given domain profile.
- create_node(type_name: str,
    node_id: str,
    name: str = "",
    **config,): Factory to create a properly typed Node with default ports from the registry.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

"""
formalism
=========

Formalism Mapping Guide for ADR-007.

Maps concepts from Petri nets, BPMN 2.0, Process Algebra (CSP/CCS),
and DES (SimPy) to PHASE-IR primitives and vice versa.

Dependencies:
- from __future__ import annotations

Functions:
- get_phase_mapping(formalism: str, concept: str): Look up how a formalism concept maps to PHASE-IR.
- get_all_mappings(formalism: str): Return every concept mapping for a formalism.
- reverse_mapping(formalism: str, phase_type: str): Find all concepts in *formalism* that map to *phase_type*.
- explain_mapping(formalism: str, concept: str): Return a human-readable explanation of a formalism-to-PHASE-IR mapping.
- get_edge_type_info(edge_type: str): Look up cross-reference information for a PHASE-IR edge type.
- list_formalisms(): Return the list of supported formalism names.
- list_edge_types(): Return all PHASE-IR edge types defined in the reference table.
- suggest_phase_type(description: str): Suggest PHASE-IR types that match a natural-language description.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

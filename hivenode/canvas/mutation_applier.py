"""
mutation_applier
================

PHASE-IR Mutation Applier

Applies mutations to IR graphs and returns JSON Patch diffs.
Handles: add_node, remove_node, add_edge, remove_edge, update_node

Dependencies:
- import copy
- from typing import Tuple, Dict, List
- from hivenode.canvas.mutation_models import MutationResult

Functions:
- _has_path_to(edges: List[Dict], source: str, target: str): Check if there's a path from source to target using DFS.
- _generate_json_patch(original: dict, modified: dict): Generate a JSON Patch (RFC 6902) between two IR dicts.
- add_node(ir: dict, payload: dict): Add a new node to the IR.
- remove_node(ir: dict, payload: dict): Remove a node from the IR. Fails if node has incoming edges.
- add_edge(ir: dict, payload: dict): Add a new edge to the IR. Fails if it would create a cycle.
- remove_edge(ir: dict, payload: dict): Remove an edge from the IR.
- update_node(ir: dict, payload: dict): Update node properties.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

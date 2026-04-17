"""
primitives
==========

PHASE-IR Primitives — in-memory dataclass structures for the
Process, Hierarchy, Action, State, Event Intermediate Representation.

11 primitives: 6 core (Port, Timing, Group, Node, Edge, Flow) +
               5 extended (Resource, Variable, Token, Distribution, Checkpoint)

Dependencies:
- from __future__ import annotations
- from dataclasses import dataclass, field
- from typing import Any, Optional

Classes:
- Resource: A capacity-limited resource that nodes can acquire/release.
- Variable: A flow-scoped variable (counter, flag, state machine, etc.).
- Token: Describes the shape of tokens flowing through the process.
- Distribution: A statistical distribution used by simulation nodes.
- Checkpoint: A snapshot/resume point after a node completes.
- Port: An input or output slot on a Node.
- Timing: Temporal constraints for a node or edge.
- Group: A named collection of nodes (swim-lane, sub-process, etc.).
- Node: A processing step in the flow.
- Edge: A directed connection between two nodes.
- Flow: Top-level container — one complete PHASE-IR process definition.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

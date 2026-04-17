"""
bpmn_compiler
=============

BPMN 2.0 Dialect Compiler for PHASE-IR (ADR-007).

Provides deterministic, lossless conversion between BPMN 2.0 XML and
PHASE-IR Flow structures.

Pipeline:
    BPMN XML  ->  BPMNProcess (intermediate)  ->  Flow (PHASE-IR)
    Flow      ->  BPMNProcess                 ->  BPMN XML

Uses xml.etree.ElementTree from stdlib for XML handling.

Dependencies:
- from __future__ import annotations
- import uuid
- import xml.etree.ElementTree as ET
- from dataclasses import dataclass, field
- from typing import Optional
- from .primitives import Edge, Flow, Group, Node

Classes:
- BPMNElement: A single BPMN element (event, task, gateway, or flow).
- BPMNProcess: A simplified BPMN process containing elements and lanes.

Functions:
- _uid(): Convert a BPMNProcess intermediate to a PHASE-IR Flow.
- ir_to_bpmn(flow: Flow): Convert a PHASE-IR Flow back to a BPMNProcess intermediate.
- _resolve_bpmn_type(node: Node): Determine the BPMN element type for a PHASE-IR node.
- _strip_ns(tag: str): Strip namespace from an XML tag: '{ns}local' -> 'local'.
- bpmn_xml_to_process(xml_str: str): Parse BPMN 2.0 XML (simplified) into a BPMNProcess intermediate.
- _parse_lanes(lane_set_el: ET.Element, lanes: list[dict]): Extract lane definitions from a <laneSet> element.
- process_to_bpmn_xml(process: BPMNProcess): Generate BPMN 2.0 XML from a BPMNProcess intermediate.
- compile_bpmn(xml_str: str): Full pipeline: BPMN XML -> BPMNProcess -> PHASE-IR Flow.
- decompile_to_bpmn(flow: Flow): Full pipeline: PHASE-IR Flow -> BPMNProcess -> BPMN XML.
- validate_bpmn_mapping(flow: Flow): Check that every node in a Flow has a valid BPMN equivalent.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.

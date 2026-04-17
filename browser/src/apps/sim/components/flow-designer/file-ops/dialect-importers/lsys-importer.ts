/**
 * lsys-importer
 *
 * * L-System (Lindenmayer System) Importer
 *
 * Parses an L-System definition file and converts the derived string
 * (via grammar expansion) into a PHASE-IR node graph.
 *
 * Supported format (.lsys):
 *
 *   # Comment
 *   axiom: F
 *   iterations: 3
 *   rules:
 *     F -> F+F-F-F+F
 *   angle: 90
 *   symbols:
 *     F = draw_forward
 *     + = turn_left
 *     - = turn_right
 *     [ = push
 *     ] = pop
 *
 * Each unique symbol type becomes a PHASE node_type.
 * The expansion sequence generates edges linking consecutive non-control
 * symbols; branching ([...]) generates parallel sub-paths.
 *
 * Dependencies:
 * - import type { PhaseNode, PhaseEdge, PhaseFlow } from "../serialization";
 *
 * Components/Functions:
 * - parseLSysFormat: TypeScript function/component
 * - def: TypeScript function/component
 * - rawLine: TypeScript function/component
 * - line: TypeScript function/component
 * - kvMatch: TypeScript function/component
 * - ruleMatch: TypeScript function/component
 * - symMatch: TypeScript function/component
 * - defaultSymbols: TypeScript function/component
 * - expandLSystem: TypeScript function/component
 * - MAX_LEN: TypeScript function/component
 * - ch: TypeScript function/component
 * - CONTROL_SYMBOLS: TypeScript function/component
 * - expansionToGraph: TypeScript function/component
 * - nodes: TypeScript function/component
 * - edges: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

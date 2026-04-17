/**
 * FlowCanvas
 *
 * * FlowCanvas — Main ReactFlow canvas wrapper for the Visual Flow Designer.
 * Registers custom node/edge types. Must be rendered inside a ReactFlowProvider.
 * ADR-019: Visual Flow Designer — TASK-190
 * TASK-CANVAS-009A: Added BroadcastChannel multi-window sync
 *
 * Dependencies:
 * - import React, { useCallback, useEffect, useMemo, useRef } from "react";
 * - import {
 * - import "@xyflow/react/dist/style.css";
 * - import "./broadcast-highlights.css";
 * - import { colors } from "../../lib/theme";
 * - import { useBroadcastSync } from "./useBroadcastSync";
 * - import PhaseNode from "./nodes/PhaseNode";
 * - import CheckpointNode from "./nodes/CheckpointNode";
 * - import ResourceNode from "./nodes/ResourceNode";
 * - import GroupNode from "./nodes/GroupNode";
 *
 * Components/Functions:
 * - NODE_TYPES: TypeScript function/component
 * - EDGE_TYPES: TypeScript function/component
 * - FlowCanvas: TypeScript function/component
 * - isReadOnly: TypeScript function/component
 * - containerRef: TypeScript function/component
 * - initRef: TypeScript function/component
 * - highlightedNodesWithClasses: TypeScript function/component
 * - isHighlighted: TypeScript function/component
 * - isSearchHighlighted: TypeScript function/component
 * - processedEdges: TypeScript function/component
 * - onInit: TypeScript function/component
 * - el: TypeScript function/component
 * - ro: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

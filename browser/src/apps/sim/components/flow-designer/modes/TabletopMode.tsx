/**
 * TabletopMode
 *
 * * TabletopMode — Top-level container for the Tabletop mode.
 * Renders a read-only ReactFlow canvas with the current node highlighted,
 * plus a chat panel where the LLM guides the user through each step.
 * The human decides at each checkpoint node.
 *
 * ADR-019: Visual Flow Designer -- Tabletop Mode
 *
 * Dependencies:
 * - import React, { useMemo, useCallback } from "react";
 * - import {
 * - import { colors, fonts } from "../../../lib/theme";
 * - import PhaseNode from "../nodes/PhaseNode";
 * - import CheckpointNode from "../nodes/CheckpointNode";
 * - import TabletopChat from "../tabletop/TabletopChat";
 * - import { useTabletop } from "../tabletop/useTabletop";
 *
 * Components/Functions:
 * - nodeTypes: TypeScript function/component
 * - getTabletopNodeStyle: TypeScript function/component
 * - getTabletopEdgeStyle: TypeScript function/component
 * - sourceVisited: TypeScript function/component
 * - targetVisited: TypeScript function/component
 * - TabletopMode: TypeScript function/component
 * - tabletop: TypeScript function/component
 * - styledNodes: TypeScript function/component
 * - style: TypeScript function/component
 * - styledEdges: TypeScript function/component
 * - overrides: TypeScript function/component
 * - handleStartSession: TypeScript function/component
 * - handleEndSession: TypeScript function/component
 * - isSessionActive: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

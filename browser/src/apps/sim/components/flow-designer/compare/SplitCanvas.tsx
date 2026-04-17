/**
 * SplitCanvas
 *
 * * SplitCanvas — Two synced ReactFlow canvases for branch comparison.
 *
 * ADR-019 Decision 6: Alterverse Comparison View.
 *
 * Layout: Two canvases side-by-side with synced scroll/zoom.
 * Each canvas renders a flow snapshot with diff overlays applied via
 * DiffHighlighter.
 *
 * Dependencies:
 * - import React, { memo, useCallback, useRef, useState, useEffect } from "react";
 * - import {
 * - import { colors, fonts } from "../../../lib/theme";
 * - import PhaseNode from "../nodes/PhaseNode";
 * - import type { FlowSnapshot } from "./diffAlgorithm";
 * - import type { NodeDiff, EdgeDiff, DiffTag } from "./diffAlgorithm";
 * - import {
 *
 * Components/Functions:
 * - nodeTypes: TypeScript function/component
 * - SplitCanvas: TypeScript function/component
 * - nodeDiffMap: TypeScript function/component
 * - edgeDiffMap: TypeScript function/component
 * - nm: TypeScript function/component
 * - nd: TypeScript function/component
 * - em: TypeScript function/component
 * - ed: TypeScript function/component
 * - handleViewportChange: TypeScript function/component
 * - CanvasPane: TypeScript function/component
 * - reactFlowInstance: TypeScript function/component
 * - suppressSyncRef: TypeScript function/component
 * - rfNodes: TypeScript function/component
 * - diff: TypeScript function/component
 * - tag: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

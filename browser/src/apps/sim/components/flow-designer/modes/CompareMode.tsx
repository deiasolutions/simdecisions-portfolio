/**
 * CompareMode
 *
 * * CompareMode — Top-level compare mode with split-view canvas, diff legend,
 * and metrics comparison panel.
 *
 * ADR-019 Decision 6: Alterverse Comparison View.
 *
 * Integrates:
 * - SplitCanvas (two synced ReactFlow canvases)
 * - DiffHighlighter (tints, badges, edge glow)
 * - MetricsPanel (side-by-side metrics table)
 * - useCompare hook (fetching + diffing)
 *
 * Dependencies:
 * - import React, { memo, useCallback, useState, useEffect } from "react";
 * - import { colors, fonts } from "../../../lib/theme";
 * - import SplitCanvas from "../compare/SplitCanvas";
 * - import MetricsPanel from "../compare/MetricsPanel";
 * - import { DiffLegend } from "../compare/DiffHighlighter";
 * - import { useCompare } from "../compare/useCompare";
 *
 * Components/Functions:
 * - CompareMode: TypeScript function/component
 * - handleExit: TypeScript function/component
 * - containerStyle: TypeScript function/component
 * - centeredStyle: TypeScript function/component
 * - toolbarStyle: TypeScript function/component
 * - retryBtnStyle: TypeScript function/component
 * - exitBtnStyle: TypeScript function/component
 * - spinnerStyle: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

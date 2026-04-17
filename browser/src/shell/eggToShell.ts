/**
 * eggToShell
 *
 * * eggToShell.ts — Converts EGG layout tree to shell state tree
 *
 * Maps EGG layout nodes (pane, split, tab-group) to shell nodes (app, split, tabbed).
 * Used by useEggInit hook to inflate EGG IR into initial ShellState.
 *
 * Dependencies:
 * - import type { EggLayoutNode } from '../sets/types'
 * - import type { ShellTreeNode, AppNode, SplitNode, TripleSplitNode, TabbedNode, BranchesRoot, SplitDirection, SlideoverNode, SlideoverMeta } from './types'
 * - import { ShellNodeType, LoadState, eggNodeToShellNode } from './types'
 * - import { uid } from './utils'
 * - import type { MuteLevel } from '../infrastructure/relay_bus'
 * - import type { ToolbarDefinition } from '../primitives/toolbar/types'
 *
 * Components/Functions:
 * - normalizeRatios: TypeScript function/component
 * - sum: TypeScript function/component
 * - parsed: TypeScript function/component
 * - pxMatch: TypeScript function/component
 * - frMatch: TypeScript function/component
 * - VIEWPORT_SIZE: TypeScript function/component
 * - totalPx: TypeScript function/component
 * - totalFr: TypeScript function/component
 * - remainingSpace: TypeScript function/component
 * - values: TypeScript function/component
 * - sum: TypeScript function/component
 * - sizes: TypeScript function/component
 * - totalSize: TypeScript function/component
 * - applySeamlessEdges: TypeScript function/component
 * - isVert: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

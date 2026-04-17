/**
 * reducer
 *
 * * shell/reducer.ts — Shell state reducer and initial state
 * Wave 1: layout undo/redo, pane locking, action labels.
 * IR routing: SET_FOCUS maintains lastFocusedByAppType map for canvas targeting.
 *
 * Dependencies:
 * - import type { ShellState, ShellAction, ShellHistoryEntry, AppNode, SplitNode, ShellTreeNode, BranchesRoot } from './types';
 * - import { ShellNodeType } from './types';
 * - import { uid, findNode, replaceNode, makeEmpty, findParentSplit, getSibling } from './utils';
 * - import { UNDO_LIMIT, LEDGER_CAP } from './constants';
 * - import { handleLayout } from './actions/layout';
 * - import { handleBranch } from './actions/branch';
 * - import { handleLifecycle } from './actions/lifecycle';
 * - import { handleResponsive } from './actions/responsive';
 *
 * Components/Functions:
 * - INITIAL_STATE: TypeScript function/component
 * - withUndo: TypeScript function/component
 * - entry: TypeScript function/component
 * - isLocked: TypeScript function/component
 * - node: TypeScript function/component
 * - emitLifecycleEvent: TypeScript function/component
 * - event: TypeScript function/component
 * - shellReducer: TypeScript function/component
 * - prev: TypeScript function/component
 * - newPast: TypeScript function/component
 * - next: TypeScript function/component
 * - newFuture: TypeScript function/component
 * - node: TypeScript function/component
 * - oldAppType: TypeScript function/component
 * - swappedNode: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

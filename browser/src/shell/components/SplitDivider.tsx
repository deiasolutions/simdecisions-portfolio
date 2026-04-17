/**
 * SplitDivider
 *
 * * SplitDivider.tsx — Draggable divider between two split panes.
 * Dispatches UPDATE_RATIO with commit:true on mouseup so resize lands on undo stack.
 * Slides-over detection when collapsed pane dragged outward.
 *
 * Dependencies:
 * - import { useState, useCallback } from 'react';
 * - import type React from 'react';
 * - import { useShell } from '../../infrastructure/relay_bus';
 * - import { BUS_MESSAGE_TYPES } from '../../infrastructure/relay_bus';
 * - import { MIN_PANE_PX, SNAP_DELTA_PX } from '../constants';
 * - import type { SplitNode, AppNode } from '../types';
 * - import { ShellNodeType } from '../types';
 *
 * Components/Functions:
 * - SplitDivider: TypeScript function/component
 * - shell: TypeScript function/component
 * - dispatch: TypeScript function/component
 * - bus: TypeScript function/component
 * - isVert: TypeScript function/component
 * - onMouseDown: TypeScript function/component
 * - el: TypeScript function/component
 * - startPos: TypeScript function/component
 * - rect: TypeScript function/component
 * - total: TypeScript function/component
 * - child0: TypeScript function/component
 * - child1: TypeScript function/component
 * - min0: TypeScript function/component
 * - min1: TypeScript function/component
 * - minRLeft: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

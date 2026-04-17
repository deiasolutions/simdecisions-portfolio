/**
 * ShellNodeRenderer
 *
 * * ShellNodeRenderer.tsx — Recursive renderer: routes node type to the correct component.
 * Drag-drop: highlights accepting panes during drag, dims non-accepting panes.
 *
 * Dependencies:
 * - import { useState, useRef, useEffect, useMemo } from 'react';
 * - import type React from 'react';
 * - import { useShell, BUS_MESSAGE_TYPES } from '../../infrastructure/relay_bus';
 * - import { getDropZone } from '../utils';
 * - import type { ShellTreeNode, AppNode, SplitNode, TripleSplitNode, TabbedNode } from '../types';
 * - import { SplitContainer } from './SplitContainer';
 * - import { TripleSplitContainer } from './TripleSplitContainer';
 * - import { TabbedContainer } from './TabbedContainer';
 * - import { PaneChrome } from './PaneChrome';
 * - import { CollapsedPaneStrip } from './CollapsedPaneStrip';
 *
 * Components/Functions:
 * - canPaneAcceptDrop: TypeScript function/component
 * - getNodePermissions: TypeScript function/component
 * - metaPerms: TypeScript function/component
 * - registryEntry: TypeScript function/component
 * - ShellNodeRenderer: TypeScript function/component
 * - shell: TypeScript function/component
 * - dispatch: TypeScript function/component
 * - swapPendingId: TypeScript function/component
 * - bus: TypeScript function/component
 * - ref: TypeScript function/component
 * - handleDragStart: TypeScript function/component
 * - dataType: TypeScript function/component
 * - accepts: TypeScript function/component
 * - match: TypeScript function/component
 * - handleDragEnd: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

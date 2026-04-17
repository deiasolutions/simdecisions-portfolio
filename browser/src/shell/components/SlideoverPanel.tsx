/**
 * SlideoverPanel
 *
 * * SlideoverPanel.tsx — Edge-anchored slide panel with overlay mode, dismiss-on-outside-tap,
 * pin/unpin buttons, and CSS transition animations.
 *
 * A slideover is an edge-anchored overlay that can optionally be docked into the layout tree
 * via DOCK_SLIDEOVER action. When docked, it becomes a regular layout pane. When undocked,
 * it returns to slideover overlay mode.
 *
 * Dependencies:
 * - import { useState, useRef, useCallback, useEffect, type ReactElement } from 'react';
 * - import type React from 'react';
 * - import { useShell } from '../../infrastructure/relay_bus';
 * - import type { SlideoverNode } from '../types';
 * - import { Z_LAYERS } from '../constants';
 * - import { PaneChrome } from './PaneChrome';
 * - import { AppFrame } from './AppFrame';
 *
 * Components/Functions:
 * - SlideoverPanel: TypeScript function/component
 * - shell: TypeScript function/component
 * - dispatch: TypeScript function/component
 * - panelRef: TypeScript function/component
 * - handleResize: TypeScript function/component
 * - showPinButton: TypeScript function/component
 * - handleClick: TypeScript function/component
 * - handleEscape: TypeScript function/component
 * - handlePinClick: TypeScript function/component
 * - isHorizontalEdge: TypeScript function/component
 * - panelWidth: TypeScript function/component
 * - panelHeight: TypeScript function/component
 * - positionProps: TypeScript function/component
 * - style: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

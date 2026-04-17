/**
 * Shell
 *
 * * Shell.tsx — Root shell frame with optional chrome bars + SplitTree body
 * Uses useReducer + ShellCtx pattern from relay_bus (TASK-005).
 *
 * Dependencies:
 * - import { useReducer, useMemo, useState, useCallback, useEffect, useRef, type ReactElement } from 'react';
 * - import { MessageBus, ShellCtx } from '../../infrastructure/relay_bus';
 * - import { AuthProvider } from '../../infrastructure/auth';
 * - import { shellReducer, INITIAL_STATE } from '../reducer';
 * - import { ShellNodeRenderer } from './ShellNodeRenderer';
 * - import { FloatPaneWrapper } from './FloatPaneWrapper';
 * - import { SlideoverPanel } from './SlideoverPanel';
 * - import { ThemePicker } from './ThemePicker';
 * - import { MenuBar } from './MenuBar';
 * - import { DrawerMenu } from './DrawerMenu';
 *
 * Components/Functions:
 * - Shell: TypeScript function/component
 * - bus: TypeScript function/component
 * - tempPaths: TypeScript function/component
 * - data: TypeScript function/component
 * - setTheme: TypeScript function/component
 * - setMode: TypeScript function/component
 * - resolvedChromeMode: TypeScript function/component
 * - width: TypeScript function/component
 * - handleResize: TypeScript function/component
 * - prevChromeModeRef: TypeScript function/component
 * - prev: TypeScript function/component
 * - next: TypeScript function/component
 * - ctx: TypeScript function/component
 * - sourceNode: TypeScript function/component
 * - targetNode: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

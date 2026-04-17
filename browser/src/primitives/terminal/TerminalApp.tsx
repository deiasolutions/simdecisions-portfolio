/**
 * TerminalApp
 *
 * * TerminalApp — Reusable terminal component
 * Ported from simdecisions-2 to browser/src/primitives/terminal/
 *
 * Works in three modes:
 * 1. Standalone — full-screen page
 * 2. Pane — inside HiveHostPanes pane with flex:1
 * 3. Bus-connected — when in pane mode, publishes terminal events to message bus
 *
 * Dependencies:
 * - import './terminal.css';
 * - import { useState, useEffect, useCallback, useRef } from 'react';
 * - import { useTerminal } from './useTerminal';
 * - import { TerminalOutput } from './TerminalOutput';
 * - import { TerminalPrompt } from './TerminalPrompt';
 * - import { TerminalResponsePane } from './TerminalResponsePane';
 * - import { TerminalStatusBar } from './TerminalStatusBar';
 * - import { SuggestionPills } from './SuggestionPills';
 * - import { openInDesigner, copyToClipboard, downloadIR } from './irRouting';
 * - import { loadSettings } from '../settings/settingsStore';
 *
 * Components/Functions:
 * - TerminalApp: TypeScript function/component
 * - isPane: TypeScript function/component
 * - fetchTimeoutRef: TypeScript function/component
 * - displayMode: TypeScript function/component
 * - isMinimal: TypeScript function/component
 * - finalStatusBarCurrencies: TypeScript function/component
 * - zone2Position: TypeScript function/component
 * - zone2Default: TypeScript function/component
 * - finalPromptLabel: TypeScript function/component
 * - expandMode: TypeScript function/component
 * - statusBarPosition: TypeScript function/component
 * - effectiveHideStatusBar: TypeScript function/component
 * - brandName: TypeScript function/component
 * - isCompact: TypeScript function/component
 * - isRelay: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

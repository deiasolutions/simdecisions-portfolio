/**
 * useTerminal
 *
 * * useTerminal — Terminal state management hook
 * Ported from simdecisions-2 to browser/src/primitives/terminal/
 * Simplified to work with browser structure and terminal service
 *
 * Dependencies:
 * - import { useState, useEffect, useRef } from 'react';
 * - import { sendMessage, formatMetrics, createConversation, parseEnvelope, routeEnvelope, type TerminalMetrics } from '../../services/terminal';
 * - import type { ChatMessage, McpServerConfig } from '../../services/terminal/providers/types';
 * - import { getDefaultModel, loadSettings } from '../../primitives/settings/settingsStore';
 * - import { getEggPrompt } from '../../shell/useEggInit';
 * - import * as chatApi from '../../services/terminal/chatApi';
 * - import { persistChatMessages, loadConversationToEntries } from './terminalChatPersist';
 * - import type { TerminalEntry, SessionLedger, UseTerminalReturn, TerminalPaneState } from './types';
 * - import { handleCommand, SLASH_COMMANDS } from './terminalCommands';
 * - import { openInDesigner, copyToClipboard, downloadIR } from './irRouting';
 *
 * Components/Functions:
 * - WELCOME_BANNER: TypeScript function/component
 * - MAX_TERMINAL_ENTRIES: TypeScript function/component
 * - trimEntries: TypeScript function/component
 * - hasBanner: TypeScript function/component
 * - MCP_SERVER_URL: TypeScript function/component
 * - useTerminal: TypeScript function/component
 * - hasApiKey: TypeScript function/component
 * - allowShell: TypeScript function/component
 * - stored: TypeScript function/component
 * - parsed: TypeScript function/component
 * - stored: TypeScript function/component
 * - stored: TypeScript function/component
 * - parsed: TypeScript function/component
 * - ensureConversation: TypeScript function/component
 * - settings: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

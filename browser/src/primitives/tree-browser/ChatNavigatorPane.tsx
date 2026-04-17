/**
 * ChatNavigatorPane
 *
 * * ChatNavigatorPane.tsx — Tree-browser pane for conversation navigation
 *
 * Wraps TreeBrowser with chat-history adapter, handles conversation selection,
 * shows volume sync badges, and wires conversation actions (new, delete).
 *
 * Dependencies:
 * - import { useEffect, useState, useCallback } from 'react';
 * - import { TreeBrowser } from './TreeBrowser';
 * - import { loadChatHistory } from './adapters/chatHistoryAdapter';
 * - import { createConversation, deleteConversation } from '../../services/terminal/chatApi';
 * - import type { TreeNodeData } from './types';
 * - import type { MessageBus } from '../../infrastructure/relay_bus/messageBus';
 * - import type { MessageEnvelope } from '../../infrastructure/relay_bus/types/messages';
 *
 * Components/Functions:
 * - ChatNavigatorPane: TypeScript function/component
 * - loadTree: TypeScript function/component
 * - rawNodes: TypeScript function/component
 * - groupIds: TypeScript function/component
 * - pendingTimeouts: TypeScript function/component
 * - unsubscribe: TypeScript function/component
 * - conversationId: TypeScript function/component
 * - timeoutId: TypeScript function/component
 * - nodeId: TypeScript function/component
 * - volume: TypeScript function/component
 * - date: TypeScript function/component
 * - path: TypeScript function/component
 * - conversationId: TypeScript function/component
 * - publishSelection: TypeScript function/component
 * - conversationId: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

/**
 * conversationLoader
 *
 * * conversationLoader.ts — Hook to load conversations from tree-browser selection
 *
 * Listens for tree-browser:conversation-selected events, loads conversation
 * content from chatApi, serializes to markdown, and sends to text-pane via
 * terminal:text-patch bus message.
 *
 * Bus event flow:
 * 1. User clicks conversation in tree-browser
 * 2. tree-browser publishes tree-browser:conversation-selected event
 * 3. This hook receives event, extracts conversationId
 * 4. Calls chatApi.getConversation(conversationId)
 * 5. Calls chatMarkdown.serializeConversation() to get markdown
 * 6. Sends terminal:text-patch message to text-pane
 * 7. Text-pane renders the markdown
 *
 * Dependencies:
 * - import { useEffect } from 'react';
 * - import type { MessageBus } from '../../infrastructure/relay_bus';
 * - import { getConversation } from '../terminal/chatApi';
 * - import { serializeConversation } from '../terminal/chatMarkdown';
 *
 * Components/Functions:
 * - useConversationLoader: TypeScript function/component
 * - unsubscribe: TypeScript function/component
 * - conversationId: TypeScript function/component
 * - conversation: TypeScript function/component
 * - markdown: TypeScript function/component
 * - errorMsg: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

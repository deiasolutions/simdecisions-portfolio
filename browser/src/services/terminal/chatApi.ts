/**
 * chatApi
 *
 * * Chat API service for terminal conversation persistence
 *
 * Backend: hivenode /storage/read and /storage/write at home:// and cloud://
 * Fallback: localStorage when hivenode is not reachable
 *
 * Storage layout (markdown format):
 *   {volume}://chats/{date}/conversation-{id}.md   — full conversation as markdown
 *   {volume}://chats/index.json                    — index [{id, title, created_at, ...}]
 *
 * Dependencies:
 * - import type { Conversation, Message, ConversationWithMessages } from './types';
 * - import { serializeConversation, parseConversation } from './chatMarkdown';
 * - import { ingestChat } from '../rag';
 * - import { HIVENODE_URL } from '../hivenodeUrl';
 *
 * Components/Functions:
 * - LS_INDEX_KEY: TypeScript function/component
 * - LS_CONV_PREFIX: TypeScript function/component
 * - isHivenodeAvailable: TypeScript function/component
 * - res: TypeScript function/component
 * - getBackend: TypeScript function/component
 * - now: TypeScript function/component
 * - resetBackendCache: TypeScript function/component
 * - toBase64: TypeScript function/component
 * - hivenodeRead: TypeScript function/component
 * - res: TypeScript function/component
 * - hivenodeWrite: TypeScript function/component
 * - res: TypeScript function/component
 * - hivenodeDelete: TypeScript function/component
 * - res: TypeScript function/component
 * - getConvUri: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

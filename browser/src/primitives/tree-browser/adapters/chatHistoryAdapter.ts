/**
 * chatHistoryAdapter
 *
 * * chatHistoryAdapter.ts — Chat history adapter for tree browser
 * Loads conversations from chatApi (hivenode + localStorage fallback),
 * groups by date: Today, Yesterday, This Week, Older.
 * Shows volume info (home://, cloud://, both) in metadata.
 *
 * Dependencies:
 * - import type { TreeNodeData } from '../types';
 * - import { listConversations } from '../../../services/terminal/chatApi';
 * - import type { Conversation } from '../../../services/terminal/types';
 * - import { getVolumeStatus } from '../../../services/volumes/volumeStatus';
 * - import type { VolumeStatus } from '../../../services/volumes/volumeStatus';
 *
 * Components/Functions:
 * - getDateGroup: TypeScript function/component
 * - date: TypeScript function/component
 * - now: TypeScript function/component
 * - today: TypeScript function/component
 * - yesterday: TypeScript function/component
 * - weekAgo: TypeScript function/component
 * - truncate: TypeScript function/component
 * - getStatusBadge: TypeScript function/component
 * - badges: TypeScript function/component
 * - conversationToNode: TypeScript function/component
 * - label: TypeScript function/component
 * - volume: TypeScript function/component
 * - status: TypeScript function/component
 * - statusBadge: TypeScript function/component
 * - node: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

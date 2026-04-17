/**
 * canvas.paletteIntegration.test
 *
 * * canvas.paletteIntegration.test.tsx — Full palette-to-canvas drag integration tests
 *
 * Verifies the complete drag-and-drop flow from palette adapter through TreeNodeRow to CanvasApp:
 * 1. paletteAdapter creates nodes with dragMimeType and dragData metadata
 * 2. TreeNodeRow reads metadata and populates dataTransfer on dragStart
 * 3. CanvasApp reads dataTransfer and creates canvas nodes
 * 4. stopPropagation prevents shell interference
 *
 * Reference: TASK-BUG-038-C integration test (6+ tests required)
 *
 * Note: These tests verify the logic and data flows without using fireEvent,
 * which requires real DOM events. Instead, they test handlers directly.
 *
 * Dependencies:
 * - import { describe, it, expect, vi, beforeEach } from 'vitest'
 * - import { render } from '@testing-library/react'
 * - import { ReactFlowProvider } from '@xyflow/react'
 * - import { CanvasApp } from '../CanvasApp'
 * - import { createPaletteAdapter } from '../../tree-browser/adapters/paletteAdapter'
 * - import { TreeNodeRow } from '../../tree-browser/TreeNodeRow'
 * - import type { MessageBus } from '../../../infrastructure/relay_bus/messageBus'
 * - import type { TreeNodeData } from '../../tree-browser/types'
 *
 * Components/Functions:
 * - actual: TypeScript function/component
 * - paletteNodes: TypeScript function/component
 * - leafNodes: TypeScript function/component
 * - group: TypeScript function/component
 * - node: TypeScript function/component
 * - dragData: TypeScript function/component
 * - taskNode: TypeScript function/component
 * - data: TypeScript function/component
 * - mockDataTransfer: TypeScript function/component
 * - dragMimeType: TypeScript function/component
 * - dragDataPayload: TypeScript function/component
 * - taskNodeData: TypeScript function/component
 * - mockDataTransfer: TypeScript function/component
 * - rawData: TypeScript function/component
 * - parsed: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

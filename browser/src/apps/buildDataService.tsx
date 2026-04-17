/**
 * buildDataService
 *
 * * buildDataService.tsx — Invisible applet that connects to hivenode
 * build monitor SSE and broadcasts TreeNodeData[] on bus events.
 *
 * Mount in EGG layout as a small header pane. Renders a compact
 * status bar (cost, tokens, elapsed, LIVE indicator).
 * Connects to localhost:8420/build/stream SSE + polls /build/status.
 * Broadcasts 4 bus events with pre-formatted TreeNodeData[]:
 *   - build:bees-updated
 *   - build:runner-updated
 *   - build:log-updated
 *   - build:completed-updated
 *
 * Dependencies:
 * - import { useEffect, useRef, useState, useContext } from 'react'
 * - import { ShellCtx } from '../infrastructure/relay_bus'
 * - import type { AppRendererProps } from '../shell/components/appRegistry'
 * - import {
 * - import type { BuildStatusResponse } from '../primitives/tree-browser/adapters/buildStatusMapper'
 * - import { discoverHivenodeUrl } from '../services/hivenodeDiscovery'
 *
 * Components/Functions:
 * - _channelCache: TypeScript function/component
 * - getBusBroadcastCache: TypeScript function/component
 * - formatCost: TypeScript function/component
 * - formatTokens: TypeScript function/component
 * - BuildDataService: TypeScript function/component
 * - ctx: TypeScript function/component
 * - bus: TypeScript function/component
 * - busRef: TypeScript function/component
 * - lastJsonRef: TypeScript function/component
 * - paneIdRef: TypeScript function/component
 * - broadcast: TypeScript function/component
 * - b: TypeScript function/component
 * - channels: TypeScript function/component
 * - json: TypeScript function/component
 * - start: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

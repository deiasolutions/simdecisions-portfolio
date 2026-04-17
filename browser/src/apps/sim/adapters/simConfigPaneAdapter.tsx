/**
 * simConfigPaneAdapter
 *
 * * simConfigPaneAdapter.tsx — Shell pane adapter for SimConfigPanel
 *
 * Wraps SimConfigPanel as a shell pane, replacing absolute-positioned floating panel.
 * Communicates via MessageBus instead of props/callbacks.
 *
 * Bus events published:
 * - sim:config-updated — user changed config (replications, timeHorizon, seed)
 * - sim:start — user clicked Start button
 * - sim:stop — user clicked Stop button
 * - sim:pause — user clicked Pause button
 * - sim:resume — user clicked Resume button
 *
 * Dependencies:
 * - import { useContext, useCallback, useState, useEffect } from 'react'
 * - import { ShellCtx } from '../../../infrastructure/relay_bus'
 * - import SimConfigPanel from '../components/flow-designer/simulation/SimConfigPanel'
 * - import type { AppRendererProps } from '../../../shell/components/appRegistry'
 * - import type { SimConfig } from '../components/flow-designer/simulation/SimConfigPanel'
 *
 * Components/Functions:
 * - SimConfigPaneAdapter: TypeScript function/component
 * - ctx: TypeScript function/component
 * - bus: TypeScript function/component
 * - initialReplications: TypeScript function/component
 * - initialTimeHorizon: TypeScript function/component
 * - initialSeed: TypeScript function/component
 * - isRunning: TypeScript function/component
 * - unsub: TypeScript function/component
 * - payload: TypeScript function/component
 * - handleConfigChange: TypeScript function/component
 * - updated: TypeScript function/component
 * - handleStart: TypeScript function/component
 * - handleStop: TypeScript function/component
 * - handlePause: TypeScript function/component
 * - handleResume: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

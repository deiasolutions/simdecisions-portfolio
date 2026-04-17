/**
 * simProgressPaneAdapter
 *
 * * simProgressPaneAdapter.tsx — Shell pane adapter for ProgressPanel + ResultsPreview
 *
 * Wraps ProgressPanel and ResultsPreview as a single shell pane.
 * Receives simulation progress, metrics, events, and results via MessageBus.
 *
 * Bus events subscribed:
 * - sim:progress-updated — replication progress (current, total, elapsed, remaining, rate)
 * - sim:metrics-updated — live metrics (avgDuration, avgSprints, successRate, avgCost)
 * - sim:event — log event (timestamp, message, type)
 * - sim:results-available — final results data (for ResultsPreview)
 *
 * Dependencies:
 * - import { useContext, useState, useEffect } from 'react'
 * - import { ShellCtx } from '../../../infrastructure/relay_bus'
 * - import ProgressPanel from '../components/flow-designer/simulation/ProgressPanel'
 * - import ResultsPreview from '../components/flow-designer/simulation/ResultsPreview'
 * - import type { AppRendererProps } from '../../../shell/components/appRegistry'
 *
 * Components/Functions:
 * - SimProgressPaneAdapter: TypeScript function/component
 * - ctx: TypeScript function/component
 * - bus: TypeScript function/component
 * - unsub: TypeScript function/component
 * - payload: TypeScript function/component
 * - payload: TypeScript function/component
 * - evt: TypeScript function/component
 * - payload: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

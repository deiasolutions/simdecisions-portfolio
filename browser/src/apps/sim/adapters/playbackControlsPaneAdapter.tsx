/**
 * playbackControlsPaneAdapter
 *
 * * playbackControlsPaneAdapter.tsx — Shell pane adapter for PlaybackControls
 *
 * Wraps PlaybackControls as a shell pane, replacing absolute-positioned bottom panel.
 * Communicates via MessageBus instead of props/callbacks.
 *
 * Bus events published:
 * - sim:playback-play — user clicked Play button
 * - sim:playback-pause — user clicked Pause button
 * - sim:playback-step-forward — user clicked Step Forward button
 * - sim:playback-step-backward — user clicked Step Backward button
 * - sim:playback-reset — user clicked Reset button
 * - sim:playback-scrub — user moved timeline scrubber
 * - sim:playback-speed — user changed playback speed
 *
 * Dependencies:
 * - import { useContext, useCallback, useState, useEffect } from 'react'
 * - import { ShellCtx } from '../../../infrastructure/relay_bus'
 * - import PlaybackControls from '../components/flow-designer/playback/PlaybackControls'
 * - import SpeedSelector from '../components/flow-designer/playback/SpeedSelector'
 * - import type { AppRendererProps } from '../../../shell/components/appRegistry'
 *
 * Components/Functions:
 * - PlaybackControlsPaneAdapter: TypeScript function/component
 * - ctx: TypeScript function/component
 * - bus: TypeScript function/component
 * - unsub: TypeScript function/component
 * - payload: TypeScript function/component
 * - handlePlayPause: TypeScript function/component
 * - eventType: TypeScript function/component
 * - handleStepForward: TypeScript function/component
 * - handleStepBackward: TypeScript function/component
 * - handleScrubChange: TypeScript function/component
 * - handleReset: TypeScript function/component
 * - handleSpeedChange: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

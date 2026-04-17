/**
 * primitivePreviewAdapter
 *
 * * primitivePreviewAdapter.tsx — Preview pane for the Primitives EGG
 *
 * Subscribes to 'primitive:selected' bus events.
 * Desktop: renders inline in the split pane.
 * Mobile (< 768px): renders as a bottom sheet overlay with swipe-to-dismiss.
 *
 * The mounted primitive receives the preview adapter's own paneId, so bus
 * messages targeted at 'prim-detail' reach it directly. The adapter's own
 * subscription uses a suffixed subscriber ID to avoid collision.
 *
 * Dependencies:
 * - import { useState, useEffect, useCallback, useContext, useRef } from 'react'
 * - import { getAppRenderer } from '../shell/components/appRegistry'
 * - import { ShellCtx } from '../infrastructure/relay_bus'
 * - import type { AppRendererProps } from '../shell/components/appRegistry'
 * - import './primitivePreviewAdapter.css'
 *
 * Components/Functions:
 * - useIsMobile: TypeScript function/component
 * - mq: TypeScript function/component
 * - handler: TypeScript function/component
 * - stopKbPropagation: TypeScript function/component
 * - PrimitivePreviewAdapter: TypeScript function/component
 * - ctx: TypeScript function/component
 * - bus: TypeScript function/component
 * - isMobile: TypeScript function/component
 * - touchStartY: TypeScript function/component
 * - sheetRef: TypeScript function/component
 * - contentRef: TypeScript function/component
 * - subId: TypeScript function/component
 * - unsub: TypeScript function/component
 * - data: TypeScript function/component
 * - handleClose: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

/**
 * textPaneAdapter
 *
 * * textPaneAdapter.tsx — App registry adapter for text-pane primitive (SDEditor)
 *
 * Maps AppRendererProps to SDEditor props.
 * BUG-046: Provides onOpenInNewTab callback that dispatches ADD_TAB
 * with a pre-configured text-pane node when the pane already has content.
 *
 * Dependencies:
 * - import { useContext, useCallback, useEffect, useRef, useState } from 'react'
 * - import { HIVENODE_URL } from '../services/hivenodeUrl'
 * - import { ShellCtx, uid } from '../infrastructure/relay_bus'
 * - import { SDEditor } from '../primitives/text-pane/SDEditor'
 * - import type { AppRendererProps } from '../shell/components/appRegistry'
 * - import type { AppNode } from '../shell/types'
 * - import { ShellNodeType, LoadState } from '../shell/types'
 *
 * Components/Functions:
 * - makeTextPaneTab: TypeScript function/component
 * - TextPaneAdapter: TypeScript function/component
 * - ctx: TypeScript function/component
 * - bus: TypeScript function/component
 * - dispatch: TypeScript function/component
 * - format: TypeScript function/component
 * - initialContent: TypeScript function/component
 * - readOnly: TypeScript function/component
 * - renderMode: TypeScript function/component
 * - showLineNumbers: TypeScript function/component
 * - hideHeader: TypeScript function/component
 * - fileUri: TypeScript function/component
 * - fileName: TypeScript function/component
 * - fetchedRef: TypeScript function/component
 * - hivenodeUrl: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

/**
 * eggInflater
 *
 * * EGG Inflater
 *
 * Converts a parsed .egg.md (ParsedEgg) into a complete EGG IR.
 * This is PURE inflation — no side effects, no bus wiring.
 * Side-effect wiring (commands, modes, away) moved to eggWiring.ts.
 *
 * Features:
 * - Resolves global-commons:// paths in favicon and startup config
 * - Validates startup block schema
 * - Type-safe output structure
 * - Field translation for legacy schema versions
 *
 * Dependencies:
 * - import { translateEggFields } from './fieldTranslator'
 * - import type { ParsedEgg, EggIR, StartupConfig, DefaultDocument } from './types'
 * - import { isGCPath, toResolvedUrl } from '../services/gcResolver'
 * - import type { ToolbarDefinition } from '../primitives/toolbar/types'
 *
 * Components/Functions:
 * - for: TypeScript class
 * - EggInflateError: TypeScript class
 * - validateNoLegacyFlags: TypeScript function/component
 * - LEGACY_FLAGS: TypeScript function/component
 * - foundFlags: TypeScript function/component
 * - flagsList: TypeScript function/component
 * - hideFlags: TypeScript function/component
 * - inflateStartupConfig: TypeScript function/component
 * - sessionRestore: TypeScript function/component
 * - validScopes: TypeScript function/component
 * - sessionRestoreScope: TypeScript function/component
 * - validOrders: TypeScript function/component
 * - restoreOrder: TypeScript function/component
 * - defaultDocuments: TypeScript function/component
 * - docObj: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

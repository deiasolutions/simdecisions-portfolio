/**
 * index
 *
 * * EGG_REGISTRY
 *
 * Barrel index of all EGG configs. Shell host resolves EGG by ID:
 *   const eggConfig = EGG_REGISTRY[eggId]
 *
 * To add a new EGG:
 *   1. Create browser/sets/my-set.set.md
 *   2. Import it here via ?raw and inflate with parseEggMd() + inflateEgg()
 *   3. Add the hostname mapping in eggResolver.ts if subdomain-based
 *
 * NOTE: This uses lazy initialization to avoid top-level await.
 * Call getEggRegistry() to access the registry.
 *
 * Dependencies:
 * - import { parseEggMd } from './parseEggMd'
 * - import { inflateEgg } from './eggInflater'
 * - import type { EggRegistry, EggIR } from './types'
 *
 * Components/Functions:
 * - eggConfig: TypeScript function/component
 * - getEggRegistry: TypeScript function/component
 * - codeDefaultParsed: TypeScript function/component
 * - getEggRegistryAsync: TypeScript function/component
 * - entries: TypeScript function/component
 * - parsed: TypeScript function/component
 * - registerEgg: TypeScript function/component
 * - clearEggRegistry: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

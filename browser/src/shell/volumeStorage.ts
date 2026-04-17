/**
 * volumeStorage
 *
 * * Named Volume Storage
 *
 * Abstraction over localStorage and sessionStorage.
 * Provides path-based access with namespacing.
 *
 * Paths:
 * - local://shell/layout-tree → localStorage key "sd:volume:shell/layout-tree"
 * - local://shell/theme → localStorage key "sd:volume:shell/theme"
 * - local://startup/{eggId}/{src} → firstRunOnly flags
 * - session://startup/{eggId}/{src} → firstTabAlways flags
 *
 * Hard Rule 6: The layout tree is stored in local://shell/layout-tree.
 * No applet or shell code writes layout state to raw localStorage directly.
 *
 * Dependencies:
 * - (see source)
 *
 * Components/Functions:
 * - PREFIX: TypeScript function/component
 * - parsePath: TypeScript function/component
 * - match: TypeScript function/component
 * - getStorage: TypeScript function/component
 * - readVolume: TypeScript function/component
 * - storage: TypeScript function/component
 * - raw: TypeScript function/component
 * - writeVolume: TypeScript function/component
 * - storage: TypeScript function/component
 * - serialized: TypeScript function/component
 * - deleteVolume: TypeScript function/component
 * - storage: TypeScript function/component
 * - hasVolume: TypeScript function/component
 * - storage: TypeScript function/component
 * - listVolumes: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.

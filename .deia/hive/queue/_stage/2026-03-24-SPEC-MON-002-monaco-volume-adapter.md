# SPEC-MON-002: Monaco Named Volume I/O Adapter

## Priority
P1

## Depends On
SPEC-MON-001-monaco-applet-component

## Objective
Wire the Monaco editor to the Named Volume System so it can open and save files via home://, mac://, vps://, and cloud:// volume paths. MON-001 builds the component shell with getValue()/setValue(). This task implements the file I/O adapter that connects those to the hivenode storage API, following the filesystemAdapter pattern. Zero direct filesystem access — all reads and writes go through the hivenode /storage/ endpoints.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\filesystemAdapter.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\terminalAdapter.tsx

## Scope

Build these files under `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\`:

1. **monacoVolumeAdapter.ts** — Volume I/O adapter
   - `open(volumePath)` calls `/storage/read` on hivenode, returns file content
   - `save(volumePath, content)` calls `/storage/write` on hivenode
   - Follows filesystemAdapter.ts pattern exactly
   - Emits FILE_OPENED and FILE_SAVED events to Event Ledger with all 3 currencies (CLOCK, COIN, CARBON)

2. **Wire into MonacoApplet.tsx** (minimal additions)
   - Accept optional `volumePath` prop
   - On mount with volumePath: call adapter.open(), pass content to setValue()
   - Expose saveFile() method via ref that calls adapter.save()
   - Update isDirty to false after successful save

3. **File load bus event handler**
   - Listen for `file:selected` bus event (same event tree-browser emits)
   - On receipt: call adapter.open(event.path), load content into editor

## Deliverables
1. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\monacoVolumeAdapter.ts
2. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.tsx (minimal additions)
3. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\__tests__\monacoVolumeAdapter.test.ts

## Acceptance Criteria
- [ ] adapter.open("home://projects/myfile.ts") fetches content from hivenode and returns it
- [ ] adapter.save("home://projects/myfile.ts", content) writes content to hivenode
- [ ] FILE_OPENED and FILE_SAVED events appear in Event Ledger with all 3 currencies
- [ ] file:selected bus event loads file into editor automatically
- [ ] isDirty resets to false after successful save
- [ ] No fs or path imports present anywhere (grep check)
- [ ] All tests pass (minimum 10 tests)
- [ ] Existing MonacoApplet tests still pass (no regressions)

## Response File
20260324-TASK-MON-002-RESPONSE.md

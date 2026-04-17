# SPEC-PORTFOLIO-MIRROR-001A: simdecisions Portfolio Mirror

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Create a public portfolio mirror of the simdecisions repo. Mirror the real directory structure exactly — same directories, same file names. Source files become descriptive stubs. Config files copy verbatim (secrets scrubbed). READMEs and INDEX.md files wherever useful. Output to `.deia/portfolio-build/simdecisions-portfolio/`.

**Author everywhere:** Dave Eichler, LinkedIn: linkedin.com/in/daaaave-atx, GitHub: DAAAAVE-ATX

## Files to Read First

- CLAUDE.md
- .deia/BOOT.md
- .deia/HIVE.md
- hivenode/main.py
- hivenode/scheduler/scheduler_daemon.py
- hivenode/scheduler/dispatcher_daemon.py
- simdecisions/des/engine.py
- browser/src/App.tsx
- pyproject.toml
- Dockerfile
- railway.toml
- vercel.json

## CRITICAL RULES

1. **NO HALLUCINATION.** Every file count, directory, and description must come from reading actual files. If you can't read it, write "TBD" not a made-up number.
2. **NO PUFF.** No marketing language. Describe what things DO, not what they REPRESENT. No "constitutional governance", no "governed orchestration platform".
3. **DAVE EICHLER.** Not Dave Morris. Not David Morris. Author is Dave Eichler.
4. **EXPLAIN THE METAPHORS.** If you mention "hive" or "bees" or "queen", explain in plain English immediately after.

## Acceptance Criteria

- [ ] Directory tree at `.deia/portfolio-build/simdecisions-portfolio/` mirrors real repo — every directory in real repo has corresponding directory in portfolio
- [ ] Every `.py`, `.ts`, `.tsx` source file has a stub containing: original docstring or inferred purpose from reading the file, import list, class/function names with one-sentence descriptions, and `# SOURCE AVAILABLE ON REQUEST` footer
- [ ] Config files copied verbatim with secrets scrubbed: pyproject.toml, package.json, railway.toml, vercel.json, Dockerfile, .gitignore
- [ ] All `.md` files from `docs/` copied verbatim
- [ ] `.deia/` coordination files copied (specs and process docs are not IP)
- [ ] INDEX.md in every directory with file table (name + one-sentence purpose from reading the actual file)
- [ ] README.md at root with: actual directory tree, tier table (view/api/service/persistence/database with real locations), working systems table with status evidence, plain-English explanation of the hive system (what it does, not what it represents)
- [ ] llms.txt at root with machine-readable repo summary
- [ ] ARCHITECTURE.md with Mermaid diagrams (5-tier, factory flow, hive hierarchy, deployment topology) each with plain English explanation
- [ ] metadata.json with Schema.org markup, author "Dave Eichler", repo URL "https://github.com/DAAAAVE-ATX/simdecisions-portfolio"
- [ ] No actual source code in any stub file — only descriptions extracted from reading the real code
- [ ] No secrets, API keys, or connection strings (replace with `[REDACTED]` or env var placeholders)
- [ ] Author is "Dave Eichler" in every file that mentions the author
- [ ] No file over 500 lines

## Smoke Test

- [ ] `find .deia/portfolio-build/simdecisions-portfolio -name "INDEX.md" | wc -l` >= 10
- [ ] `grep -r "Dave Morris\|David Morris" .deia/portfolio-build/simdecisions-portfolio/` returns no matches
- [ ] `grep -ri "api.key\|password=\|secret=" .deia/portfolio-build/simdecisions-portfolio/` returns no matches
- [ ] `grep -r "SOURCE AVAILABLE ON REQUEST" .deia/portfolio-build/simdecisions-portfolio/ --include="*.py" | wc -l` >= 20
- [ ] `ls .deia/portfolio-build/simdecisions-portfolio/README.md .deia/portfolio-build/simdecisions-portfolio/llms.txt .deia/portfolio-build/simdecisions-portfolio/ARCHITECTURE.md .deia/portfolio-build/simdecisions-portfolio/metadata.json` all exist

## Constraints

- **READ BEFORE WRITE.** Read each actual file before creating its stub. Do not stub from memory.
- **NO HALLUCINATION.** If you can't read a file, mark it TBD.
- **NO PUFF.** Describe what things do, not what they represent.
- **SECRETS = INSTANT FAIL.** Any API key, password, or connection string in output = reject. Replace with `[REDACTED]` or `os.getenv("VAR_NAME")`.
- No git operations.
- No file over 500 lines.
- READMEs wherever a human or LLM crawler would benefit from context.

## Stub Format

For `.py` files:
```python
"""
[Module Name]
=============

[Original docstring OR inferred purpose from reading code]

Dependencies:
- [list imports]

Classes:
- ClassName: [one sentence from reading the actual class]

Functions:
- function_name(args): [one sentence from reading the actual function]

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
```

For `.ts` / `.tsx` files:
```typescript
/**
 * [Module Name]
 *
 * [Inferred purpose from reading code]
 *
 * Dependencies:
 * - [list imports]
 *
 * Components/Functions:
 * - ComponentName: [one sentence]
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
```

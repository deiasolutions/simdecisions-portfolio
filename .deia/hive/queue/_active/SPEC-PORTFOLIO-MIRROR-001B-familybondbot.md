# SPEC-PORTFOLIO-MIRROR-001B: familybondbot Portfolio Mirror

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Create a public portfolio mirror of the familybondbot app. Read `frontend-v3/` and `backend-v2/` from the familybondbot repo, create descriptive stubs for all source files, copy config files verbatim (secrets scrubbed), add READMEs and INDEX.md files. Skip all other directories (frontend/, frontend-v2/, frontend-v4/, backend/, archive/, db-backups/, etc.). Output to `.deia/portfolio-build/familybondbot-portfolio/`.

**Author everywhere:** Dave Eichler, LinkedIn: linkedin.com/in/daaaave-atx, GitHub: DAAAAVE-ATX

## Files to Read First

- CLAUDE.md
- .deia/BOOT.md
- docs/portfolio/1000bulbs-portfolio-audit.md

Note: The familybondbot source is in a sibling repo at `/c/Users/davee/OneDrive/Documents/GitHub/familybondbot/fbb/`. Read files there directly — start with `frontend-v3/package.json`, `frontend-v3/src/App.tsx`, `backend-v2/requirements.txt`, `backend-v2/app.py`.

## CRITICAL RULES

1. **NO HALLUCINATION.** Every file count, directory, and description must come from reading actual files. If you can't read it, write "TBD" not a made-up number.
2. **NO PUFF.** No marketing language. Describe what things DO.
3. **DAVE EICHLER.** Not Dave Morris. Not David Morris. Author is Dave Eichler.
4. **ONLY frontend-v3/ and backend-v2/.** Do not read, stub, or reference any other directories in the fbb repo.

## Acceptance Criteria

- [ ] Source directory is `/c/Users/davee/OneDrive/Documents/GitHub/familybondbot/fbb/`
- [ ] ONLY `frontend-v3/` and `backend-v2/` are stubbed — no other directories
- [ ] Output at `.deia/portfolio-build/familybondbot-portfolio/` with `frontend-v3/` and `backend-v2/` subdirectories
- [ ] Every `.py`, `.ts`, `.tsx` source file has a stub containing: original docstring or inferred purpose, import list, class/function names with one-sentence descriptions, `# SOURCE AVAILABLE ON REQUEST` footer
- [ ] Config files copied verbatim with secrets scrubbed: package.json, requirements.txt, Dockerfile, .env.example (if present), tsconfig.json, vite.config.ts
- [ ] INDEX.md in every directory with file table (name + one-sentence purpose from reading the actual file)
- [ ] README.md at root describing the app honestly: what it does, tech stack from reading actual config files, architecture from reading actual code, deployment info if discoverable
- [ ] README.md mentions live app URL: app.familybondbot.com
- [ ] llms.txt at root with machine-readable summary
- [ ] RAG pipeline documented if present in backend-v2 (from reading actual code, not assumed)
- [ ] API endpoints catalogued from reading actual route files in backend-v2
- [ ] React components catalogued from reading actual files in frontend-v3/src/components/
- [ ] No actual source code in any stub
- [ ] No secrets, API keys, or connection strings
- [ ] No product URLs leaked that shouldn't be (api.familybondbot.com is OK to mention in architecture docs)
- [ ] Author is "Dave Eichler" everywhere
- [ ] No file over 500 lines

## Smoke Test

- [ ] `find .deia/portfolio-build/familybondbot-portfolio -name "INDEX.md" | wc -l` >= 5
- [ ] `grep -r "Dave Morris\|David Morris" .deia/portfolio-build/familybondbot-portfolio/` returns no matches
- [ ] `grep -ri "api.key\|password=\|secret=" .deia/portfolio-build/familybondbot-portfolio/` returns no matches
- [ ] `ls .deia/portfolio-build/familybondbot-portfolio/README.md .deia/portfolio-build/familybondbot-portfolio/llms.txt` both exist
- [ ] `find .deia/portfolio-build/familybondbot-portfolio -name "*.py" -path "*/frontend/*"` returns 0 (no .py in frontend)
- [ ] `grep -r "SOURCE AVAILABLE ON REQUEST" .deia/portfolio-build/familybondbot-portfolio/ | wc -l` >= 10

## Constraints

- **READ BEFORE WRITE.** Read each actual file before creating its stub.
- **NO HALLUCINATION.** If you can't read a file, mark it TBD.
- **NO PUFF.** Describe what things do, not what they represent.
- **SECRETS = INSTANT FAIL.** Replace with `[REDACTED]` or `os.getenv("VAR_NAME")`.
- **ONLY frontend-v3/ and backend-v2/.** Do not touch, read, or reference frontend/, frontend-v2/, frontend-v4/, backend/, archive/, db-backups/, Downloads/, notebooks/, fbb_2.4_2025-12/, or any other directory.
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

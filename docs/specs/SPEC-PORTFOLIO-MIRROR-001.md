# SPEC-PORTFOLIO-MIRROR-001: Public Portfolio Mirror Repos

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Create two public portfolio deliverables that mirror real repo structures with source replaced by descriptive stubs. Protect IP while showing real architecture, real structure, real working systems. Every claim must come from reading the actual code — no hallucinations, no puff, no marketing prose.

**Deliverables:**
1. `simdecisions-portfolio/` — platform architecture showcase, written to `.deia/portfolio-build/simdecisions-portfolio/`
2. `familybondbot/` — shipped product showcase, written to `.deia/portfolio-build/familybondbot-portfolio/`

**Author everywhere:** Dave Eichler, LinkedIn: linkedin.com/in/daaaave-atx

## Files to Read First

- CLAUDE.md
- .deia/BOOT.md
- .deia/HIVE.md
- hivenode/main.py
- hivenode/scheduler/scheduler_daemon.py
- hivenode/scheduler/dispatcher_daemon.py
- hivenode/scheduler/triage_daemon.py
- simdecisions/des/engine.py
- browser/src/App.tsx
- pyproject.toml
- Dockerfile
- railway.toml
- vercel.json

## CRITICAL RULES

1. **NO HALLUCINATION.** Every file count, every directory, every description must come from reading the actual repos. If you don't know, say "TBD" not a made-up number.
2. **NO PUFF.** No marketing language. No "constitutional governance" prose. Describe what things DO, not what they REPRESENT.
3. **DAVE EICHLER.** Not Dave Morris. Not David Morris. Author is Dave Eichler, LinkedIn: linkedin.com/in/daaaave-atx, GitHub: DAAAAVE-ATX.
4. **EXPLAIN THE METAPHORS.** If you mention "hive" or "bees" or "queen", explain it in plain English immediately after.
5. **TRACK EVERYTHING.** Log what you read, what you created, what you skipped, and why.

## Acceptance Criteria

### Phase 1: Survey (must complete before any file creation)
- [ ] File `SURVEY-SIMDECISIONS.md` written to `.deia/portfolio-build/` listing every top-level directory with: file count, file types, key modules, one-sentence purpose
- [ ] File `SURVEY-FAMILYBONDBOT.md` written to `.deia/portfolio-build/` listing `frontend-v3/` and `backend-v2/` directories with same detail
- [ ] File `SURVEY-SUMMARY.md` written to `.deia/portfolio-build/` merging both surveys

### Phase 2: simdecisions-portfolio
- [ ] Directory tree mirrors real repo — every directory in real repo has corresponding directory in portfolio
- [ ] Every `.py`, `.ts`, `.tsx` source file has a stub containing: original docstring or inferred purpose, import list, class/function names with one-sentence descriptions, and `# SOURCE AVAILABLE ON REQUEST` footer
- [ ] Config files copied verbatim: pyproject.toml, package.json, railway.toml, vercel.json, Dockerfile, .gitignore
- [ ] All `.md` files from `docs/` copied verbatim
- [ ] `.deia/` coordination files copied (specs and process docs are not IP)
- [ ] INDEX.md created in every directory with file table (name + one-sentence purpose from reading the actual file)
- [ ] README.md at root describes real architecture with actual directory tree from survey, tier table, working systems table with status evidence, and plain-English explanation of the hive system
- [ ] llms.txt at root with machine-readable repo summary
- [ ] ARCHITECTURE.md at root with Mermaid diagrams: 5-tier architecture, factory flow, hive hierarchy, deployment topology — each with plain English explanation below
- [ ] metadata.json with Schema.org markup, author "Dave Eichler"
- [ ] No actual source code in any stub file
- [ ] No secrets, API keys, or connection strings in any file (replace with `[REDACTED]` or env var placeholders)
- [ ] Author is "Dave Eichler" in every file that mentions the author

### Phase 3: familybondbot-portfolio
- [ ] Source directory is `/c/Users/davee/OneDrive/Documents/GitHub/familybondbot/fbb/`
- [ ] ONLY `frontend-v3/` and `backend-v2/` are stubbed (skip frontend/, frontend-v2/, frontend-v4/, backend/, archive/, db-backups/, Downloads/, notebooks/, fbb_2.4_2025-12/)
- [ ] Output written to `.deia/portfolio-build/familybondbot-portfolio/`
- [ ] Same stub format as simdecisions: docstrings, imports, class/function names, no source code
- [ ] INDEX.md in every directory
- [ ] README.md at root describes the app honestly: what it does, stack, architecture from survey, RAG pipeline if present, deployment info
- [ ] llms.txt at root
- [ ] Config files (package.json, requirements.txt, Dockerfile, etc.) from frontend-v3/ and backend-v2/ copied verbatim with secrets scrubbed
- [ ] No actual source code in any stub
- [ ] No secrets, API keys, connection strings
- [ ] Author is "Dave Eichler" everywhere

### Phase 4: Quality Assurance
- [ ] BUILD-TRACKING-REPORT.md produced in `.deia/portfolio-build/` with per-directory table: files surveyed, stubs created, copied verbatim, skipped, notes
- [ ] RECOMMENDATIONS-READOUT.md produced with any issues discovered during build
- [ ] Cross-check: no actual source code leaked
- [ ] Cross-check: no secrets in any file
- [ ] Cross-check: author is "Dave Eichler" everywhere (not Dave Morris, not David Morris)
- [ ] Cross-check: LinkedIn link is linkedin.com/in/daaaave-atx everywhere

## Smoke Test

- [ ] `find .deia/portfolio-build/simdecisions-portfolio -name "INDEX.md" | wc -l` returns >= 10
- [ ] `find .deia/portfolio-build/familybondbot-portfolio -name "INDEX.md" | wc -l` returns >= 5
- [ ] `grep -r "Dave Morris" .deia/portfolio-build/` returns no matches
- [ ] `grep -r "David Morris" .deia/portfolio-build/` returns no matches
- [ ] `grep -ri "api.key\|password\|secret\|connection_string" .deia/portfolio-build/` returns no matches (excluding redacted placeholders)
- [ ] `grep -r "SOURCE AVAILABLE ON REQUEST" .deia/portfolio-build/simdecisions-portfolio/ --include="*.py" | wc -l` returns >= 20
- [ ] `ls .deia/portfolio-build/simdecisions-portfolio/README.md .deia/portfolio-build/simdecisions-portfolio/llms.txt .deia/portfolio-build/simdecisions-portfolio/ARCHITECTURE.md .deia/portfolio-build/simdecisions-portfolio/metadata.json` all exist
- [ ] `ls .deia/portfolio-build/familybondbot-portfolio/README.md .deia/portfolio-build/familybondbot-portfolio/llms.txt` both exist
- [ ] `ls .deia/portfolio-build/BUILD-TRACKING-REPORT.md .deia/portfolio-build/RECOMMENDATIONS-READOUT.md` both exist

## Constraints

- **READ BEFORE WRITE.** Survey (Phase 1) must complete before any stub creation begins. Do not create stubs from memory or assumptions.
- **NO HALLUCINATION.** If you can't read a file, mark it TBD. Never invent file counts, function names, or descriptions.
- **NO PUFF.** Describe what things do, not what they represent. No "constitutional governance", no "governed orchestration platform", no marketing prose.
- **SECRETS = INSTANT FAIL.** Any API key, password, or connection string in output = reject entire build. Replace with `[REDACTED]` or `os.getenv("VAR_NAME")`.
- **No git operations.** Write all files locally. Q88N reviews and pushes.
- **No file over 500 lines.**
- **No stubs — every file complete** (the stubs themselves must be complete descriptions, not placeholder TODOs).
- familybondbot source is at: `/c/Users/davee/OneDrive/Documents/GitHub/familybondbot/fbb/`
- familybondbot: ONLY stub `frontend-v3/` and `backend-v2/`. Skip all other directories.
- simdecisions source is the current working directory (this repo).
- READMEs wherever it makes sense — every directory that a human or crawler would benefit from having one.

## Stub Format

For every `.py` file:
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

For every `.ts` / `.tsx` file:
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
 * - functionName(args): [one sentence]
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
```

## Output Locations

All outputs go to `.deia/portfolio-build/`:

```
.deia/portfolio-build/
├── SURVEY-SIMDECISIONS.md
├── SURVEY-FAMILYBONDBOT.md
├── SURVEY-SUMMARY.md
├── simdecisions-portfolio/    # Complete mirror structure
├── familybondbot-portfolio/   # frontend-v3/ + backend-v2/ stubs only
├── BUILD-TRACKING-REPORT.md
└── RECOMMENDATIONS-READOUT.md
```

# SPEC-USAGE-AUDIT-001: Command Usage Audit + Slash-Command Candidate Ranking

## Priority

P2

## Depends On

None

## Model Assignment

sonnet

## Objective

Q88N operates Claude Code daily and has accumulated ~996 session transcripts at `~/.claude/projects/C--Users-davee-OneDrive-Documents-GitHub-simdecisions/*.jsonl` plus 22 curated Q33NR session logs at `.deia/hive/session-logs/`. Many Q88N asks recur every session — "check factory status," "dispatch this spec," "summarize the latest response," "write a spec for X," "is the bee back yet," "restart services." We just added the first project slash command, `/now` (factory dashboard). The goal of this audit is to mine the corpus for **what Q88N actually types repeatedly**, cluster those patterns, and rank candidate follow-on slash commands (and possibly skills) by projected time savings.

The deliverable is a ranked, evidence-backed shortlist of slash commands Q88N should build next, with proposed names that respect Claude Code's built-in namespace (no first-letter conflicts with any existing `/command`) and the two reserved letters `n` (already `/now`) and `g` (reserved by Q88N for a future frequent command). Safe first letters today are `j`, `k`, `x`, `y`, `z`, and any multi-character command whose prefix doesn't collide (e.g., `/yo`, `/kick`, `/zap`).

No code, no publishing, no automatic command generation. The output is a report Q88N reads, then Q33NR writes per-command specs (or, for pure-config commands, Q33NR authors the `.claude/commands/*.md` directly).

## Files to Read First

.deia/hive/session-logs
.claude/commands/now.md
.claude/settings.local.json
CLAUDE.md
.deia/BOOT.md
.deia/HIVE.md
docs/wip/2026-04-16-Q88N-Q33NR-WIP.md

## Acceptance Criteria

- [ ] Enumerate the full corpus: `ls ~/.claude/projects/C--Users-davee-OneDrive-Documents-GitHub-simdecisions/*.jsonl | wc -l` and record the count, plus `ls .deia/hive/session-logs/*.md | wc -l`. Report both numbers in the output.
- [ ] Sampling strategy chosen and documented — do NOT read all 996 transcripts. Sample stratified by session size and recency (e.g., 20 most recent + 20 largest + 20 random). Target ≤ 80 transcripts total. Record which were sampled.
- [ ] Extract all `role: "user"` messages from sampled transcripts plus the Q88N-attributed content in Q33NR session logs. Normalize whitespace and lowercase for clustering, but preserve a representative verbatim example per cluster.
- [ ] Cluster recurring patterns into intent groups. Examples (not exhaustive): "check factory state," "check if a specific bee/task came back," "summarize a response file," "dispatch an existing spec," "write a new research spec about X," "restart services," "show costs," "show what's stuck," "read the latest WIP." Each cluster has: label, estimated frequency (count per sampled session), 2-3 verbatim example utterances, and the underlying action (which files are read, which endpoints hit, which bash commands run).
- [ ] **Candidate slash-command table**, ranked by `frequency × time-saved-per-use`, with columns: rank, proposed name, first letter (must be in the safe set `j k x y z` or a non-conflicting multi-letter prefix), cluster it addresses, what the command does (bash + prompt), estimated daily invocations, pure-config (Q33NR can author) vs needs-helper-script (bee task), any dependency on hivenode endpoints or scripts that don't yet exist.
- [ ] Explicitly call out commands that would need a new helper (e.g., `_tools/cost_report.py` for MTD spend breakdown). These become their own follow-on specs — sketch them, don't write them.
- [ ] **Coverage analysis:** "If Q88N built the top N commands, they'd cover X% of recurring typing." Produce this for N=3, 5, 10.
- [ ] **Do NOT conflict.** Before recommending a name, verify its first letter against Claude Code's known built-ins (`a b c d e f h i l m o p q r s t u v w`) and the two reserved project letters (`n` for `/now`, `g` reserved). Recommendations violating this rule are rejected.
- [ ] Privacy note in the report: sampled transcripts contain Q88N's full prompt history including non-factory topics. The report should surface *patterns*, not dump verbatim content beyond 2-3 short examples per cluster. No credentials, no personal details, no API keys quoted even if present in the corpus.
- [ ] Report ends with a "Q33NR next steps" section: for each recommended command, state whether Q33NR can author it directly (pure-config) or whether a bee spec is needed (helper script required).

## Smoke Test

After reading the report, Q88N can pick the next 3-5 slash commands to build in one sitting, Q33NR knows which they can author immediately versus which need a follow-on spec, and no recommended command conflicts with an existing `/command` first letter.

## Constraints

- Read-only. No `.claude/commands/` files written. No scripts created. No specs drafted beyond the sketches requested.
- Honor the privacy note — pattern analysis only, no verbatim dumps of the transcripts beyond small illustrative snippets (≤ 15 words each), no secrets ever quoted.
- Do not read all 996 transcripts — sampling is required. Document the sampling method.
- Do not recommend commands starting with letters `a b c d e f h i l m n o p q r s t u v w` (existing built-ins + `/now`) or `g` (reserved). Safe prefixes: `j k x y z` and multi-letter names whose typed prefix doesn't collide.
- `~/.claude/projects/C--Users-davee-OneDrive-Documents-GitHub-simdecisions/` is outside the repo — accessed via `ls` / `cat` on the absolute path, not via `Read` tool with repo-relative paths. Note this in the report so future readers understand how the audit was performed.
- Do not modify `.claude/settings.local.json` or any permission files. Read-only inspection only.

---
id: GITHUB-004
priority: P2
model: sonnet
role: bee
depends_on: []
---
# SPEC-GITHUB-004: Existing Repo Cleanup

## Priority
P2

## Model Assignment
sonnet

## Depends On
(none)

## Objective
Clean up and improve READMEs for two existing repos: `zero-shot_forecast` and `AI-Techniques`. These need proper descriptions and READMEs suitable for a technical hiring manager audience.

## Constraints
- You are in EXECUTE mode. Write all code. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Use `gh` CLI for all GitHub operations (already authenticated)
- Written for technical hiring manager audience
- Check both `daaaave-atx` and `deiasolutions` accounts for these repos
- Do NOT modify any private repos without seeing existing content first

## Steps

1. Find repos — check both accounts:
   - `gh repo view daaaave-atx/zero-shot_forecast 2>/dev/null`
   - `gh repo view deiasolutions/zero-shot_forecast 2>/dev/null`
   - `gh repo view daaaave-atx/AI-Techniques 2>/dev/null`
   - `gh repo view deiasolutions/AI-Techniques 2>/dev/null`
2. For each repo found:
   - Clone to temp dir
   - Read existing README.md and repo contents
   - Update repo description via `gh repo edit`
   - Write/improve README.md based on actual repo contents
3. Commit and push

## Repo Descriptions

**zero-shot_forecast:**
- Description: "Forecasting without historical time series data — zero-shot methodology using Python"
- README should explain the methodology, use cases, and how it works

**AI-Techniques:**
- Description: "Prompting patterns and AI interaction techniques for improved LLM responses"
- README should explain what techniques are covered and how to use them

## Acceptance Criteria
- [ ] zero-shot_forecast has a proper description and README
- [ ] AI-Techniques has a proper description and README
- [ ] Both READMEs explain what the repos do clearly
- [ ] Content suitable for technical hiring manager review

## Smoke Test
```bash
gh repo list daaaave-atx --limit 50 -q '.[] | .name' 2>/dev/null | grep -i "zero-shot\|ai-tech" && echo FOUND
```

## Response Location
`.deia/hive/responses/20260408-GITHUB-004-RESPONSE.md`

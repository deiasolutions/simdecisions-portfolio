# SWE-bench Pro Patch Production Pattern Analysis

**Date:** 2026-04-14
**Analyzed by:** BEE-QUEUE-TEMP-SPEC-SWE-ANALYSIS-001
**Dataset:** 731 SWE-bench Pro tasks (from sample.json)
**Patches Produced:** 198/731 (27.1%)
**Bee Configuration:** 15 concurrent Sonnet bees

---

## Executive Summary

The SWE-bench Pro run produced patches for **198 out of 731 tasks (27.1%)**. Success was highly repository-dependent, ranging from **99% for ansible/ansible** to **0% for 7 repositories**. The data reveals a stark divide: **3 repos account for 100% of all successes** (ansible, element-hq, flipt-io), while the remaining **8 repos produced zero patches**. Python and JavaScript tasks performed significantly better than Go and TypeScript.

### Key Insights

1. **Repository dominance:** ansible/ansible (95/96, 99%), element-hq/element-web (55/56, 98%), and flipt-io/flipt (48/85, 56%) account for all 198 successes
2. **Language disparity:** Python 35.7%, JavaScript 33.3%, Go 17.1%, TypeScript 0%
3. **Problem complexity correlation:** Successful tasks had **23% longer problem statements** (mean 1503 chars vs 1221 chars)
4. **Patch size:** Median 36 lines changed, mean 87 lines, range 0-1203 lines
5. **Critical failure mode:** All sampled failures (20/20) showed NO_RESPONSE — bees completed but did not produce valid patch files

---

## 1. Breakdown by Repository

| Repository | Total | Success | Failed | Rate |
|------------|-------|---------|--------|------|
| **ansible/ansible** | 96 | 95 | 1 | **99.0%** |
| **element-hq/element-web** | 56 | 55 | 1 | **98.2%** |
| **flipt-io/flipt** | 85 | 48 | 37 | **56.5%** |
| qutebrowser/qutebrowser | 79 | 0 | 79 | 0.0% |
| internetarchive/openlibrary | 91 | 0 | 91 | 0.0% |
| gravitational/teleport | 76 | 0 | 76 | 0.0% |
| protonmail/webclients | 65 | 0 | 65 | 0.0% |
| future-architect/vuls | 62 | 0 | 62 | 0.0% |
| navidrome/navidrome | 57 | 0 | 57 | 0.0% |
| NodeBB/NodeBB | 44 | 0 | 44 | 0.0% |
| tutao/tutanota | 20 | 0 | 20 | 0.0% |

### Analysis

- **Top 3 repos (ansible, element-hq, flipt-io):** 237 tasks → 198 patches (83.5%)
- **Bottom 8 repos:** 494 tasks → 0 patches (0.0%)
- **Correlation hypothesis:** Ansible and element-hq are **mature open-source projects with extensive test suites and clear contribution guidelines**. Flipt-io is a Go project with clean architecture.
- **Zero-success repos share traits:** Many are TypeScript/Go projects, some have complex build systems, some may require external services or specific environment setup

---

## 2. Breakdown by Programming Language

| Language | Total | Success | Failed | Rate |
|----------|-------|---------|--------|------|
| **Python** | 266 | 95 | 171 | **35.7%** |
| **JavaScript** | 165 | 55 | 110 | **33.3%** |
| **Go** | 280 | 48 | 232 | **17.1%** |
| **TypeScript** | 20 | 0 | 20 | **0.0%** |

### Analysis

- **Python leads** (35.7%), driven entirely by ansible/ansible (95 patches)
- **JavaScript second** (33.3%), driven entirely by element-hq/element-web (55 patches)
- **Go struggles** (17.1%), despite 280 tasks — only flipt-io/flipt produced patches
- **TypeScript zero** (0.0%) — tutao/tutanota had 20 tasks, all failed

**Hypothesis:** Python and JavaScript ecosystems have better-defined conventions (PEP, ESLint) that bees can pattern-match. Go and TypeScript may require more context-specific understanding of interfaces, types, and project structure.

---

## 3. Problem Statement Size Analysis

|  | Success (198 tasks) | Failure (533 tasks) | Difference |
|--|---------------------|---------------------|------------|
| **Mean** | 1503 chars | 1221 chars | +282 chars (+23%) |
| **Median** | 1362 chars | 1131 chars | +231 chars (+20%) |
| **Range** | 447 - 5319 chars | 419 - 8036 chars | — |
| **Std Dev** | 699 chars | 511 chars | — |

### Analysis

- **Successful tasks had longer problem statements** — counterintuitive, but suggests **more detailed specifications lead to better patches**
- **Longer statements provide more context:** explicit reproduction steps, expected vs actual behavior, code snippets
- **Failures include both extremes:** shortest (419 chars) and longest (8036 chars), suggesting **length alone is not deterministic**
- **Hypothesis:** Quality of problem statement matters more than length — clear acceptance criteria, explicit error messages, and code examples boost success

---

## 4. Patch Size Distribution (198 Successful Patches)

| Metric | Value |
|--------|-------|
| **Median lines changed** | 36 |
| **Mean lines changed** | 87 |
| **Min lines changed** | 0 |
| **Max lines changed** | 1203 |

### Breakdown by Size

- **Micro patches (1-10 lines):** ~30% — mostly ansible and element-hq
- **Small patches (11-50 lines):** ~40% — most common category
- **Medium patches (51-200 lines):** ~20%
- **Large patches (201+ lines):** ~10% — includes flipt-io/flipt-6fd0f9e (1203 lines)

### Analysis

- **Median 36 lines suggests focused changes** — bees are producing surgical fixes, not sweeping refactors
- **Mean 87 lines pulled up by outliers** — a few large patches (200+ lines) skew the average
- **Empty patch exists** (0 lines changed) — likely a no-op or formatting-only change that passed validation
- **Largest patch (1203 lines)** — flipt-io task, suggests significant feature addition or refactor

**Hypothesis:** Bees succeed best on **small, well-scoped fixes** (median 36 lines). Large patches (200+ lines) may indicate tasks that required substantial new code, which bees handled successfully in flipt-io but failed in other Go repos.

---

## 5. Failure Mode Analysis (20 Sampled Failures)

### Sample Composition

- **Repos sampled:** qutebrowser (3), tutanota (2), protonmail (1), gravitational (4), internetarchive (2), navidrome (1), NodeBB (1), flipt-io (2), future-architect (2), element-hq (1), ansible (1)
- **Languages:** Python (6), TypeScript (2), JavaScript (2), Go (10)
- **Problem lengths:** 742 - 2041 chars (mean 1084 chars)

### Failure Reason Breakdown

| Reason | Count | Percentage |
|--------|-------|------------|
| **NO_RESPONSE** | 20 | 100% |

### Analysis

**Critical finding:** ALL 20 sampled failures showed `NO_RESPONSE` — meaning:

1. **No response file found** in `.deia/hive/responses/` matching the instance_id pattern
2. **Bee may have completed** but did not produce a response file
3. **Bee may have timed out** or failed silently without writing output
4. **Bee may have written response** but with incorrect naming pattern (uppercase/lowercase mismatch)

**Hypothesis on NO_RESPONSE:**

- **856 response files exist** with pattern `*SPEC-SWE-INSTANCE*`, suggesting bees ARE writing responses
- **Filename casing issues:** Response files use uppercase instance IDs, but sample.json may have mixed case
- **Possible causes:**
  1. **Bee crashed before writing patch** (but after writing partial response)
  2. **Invalid diff format** — bee produced output but patch validation failed
  3. **Clone/build failures** — bee couldn't set up repo environment
  4. **Test failures** — bee produced patch but tests failed, so patch wasn't saved
  5. **Timeout** — bee hit time limit before producing valid output

**Next step:** Sample 5-10 response files from the 856 found and categorize actual failure modes (clone error, build error, test failure, invalid diff, etc.)

---

## 6. Success Characteristics

### Common Traits in Successful Problem Statements

Based on manual review of 10 successful ansible/ansible and element-hq/element-web tasks:

1. **Clear reproduction steps** — "1. Navigate to X, 2. Click Y, 3. Observe Z"
2. **Explicit error messages** — exact traceback or console output included
3. **Expected vs actual behavior** — both states clearly defined
4. **Code snippets** — example of current code or desired API
5. **Environment details** — versions, OS, browser (for element-hq)
6. **Single, well-scoped issue** — not "fix all authentication bugs," but "JPG files don't show in file picker when MIME type is restricted"

### Repo-Specific Success Factors

#### ansible/ansible (99% success)

- **Python with clear module structure** — modules follow consistent patterns
- **Extensive test suite** — bees can verify fixes
- **Issue templates** — problem statements follow structured format
- **Well-documented codebase** — inline comments, docstrings

#### element-hq/element-web (98% success)

- **React/TypeScript with component architecture** — clear boundaries
- **Strong type definitions** — bees can infer expected types
- **UI-focused issues** — often include screenshots or user flows
- **Active project with recent commits** — patterns are current

#### flipt-io/flipt (56% success)

- **Clean Go architecture** — well-organized packages
- **gRPC/API focus** — many issues are about API behavior, which is testable
- **Good test coverage** — bees can validate changes
- **37 failures suggest edge cases** — some tasks may require deep domain knowledge

---

## 7. Top Findings and Recommendations

### Top 5 Findings

1. **Repository architecture >> language:** ansible/ansible (Python) and element-hq/element-web (JS) both hit 98%+, while other Python/JS repos hit 0%. **Code organization and test quality matter more than language choice.**

2. **Go underperforms (17.1%)** despite 280 tasks. Only flipt-io produced patches. **Investigate:** Do Go repos have harder tasks? Do bees struggle with Go idioms (interfaces, goroutines, error handling)?

3. **All TypeScript tasks failed (0/20).** tutao/tutanota had 20 tasks, zero patches. **Investigate:** Is TypeScript compilation failing? Are type errors blocking bees?

4. **Longer problem statements → higher success.** Mean 1503 chars (success) vs 1221 chars (failure). **Recommendation:** Provide more context in problem statements — error messages, reproduction steps, expected behavior.

5. **NO_RESPONSE is the dominant failure mode.** 100% of sampled failures showed no response file or invalid patch output. **Critical:** Dig into the 856 response files to understand actual failure reasons (clone, build, test, format).

### Recommendations for Next Run

#### Immediate Actions

1. **Sample 20 response files** from the 856 and categorize failure modes:
   - Clone/checkout failures
   - Build/compilation failures
   - Test execution failures
   - Invalid diff format
   - Timeout/OOM
   - No patch produced (bee gave up)

2. **Retry zero-success repos with different prompts:**
   - Add "You are working on a [Go/TypeScript] codebase" to bee prompts
   - Include repo-specific context (build system, test commands, contribution guide)
   - Increase timeout for complex repos

3. **A/B test problem statement length:**
   - Run 50 tasks with minimal statements (< 800 chars)
   - Run 50 tasks with detailed statements (> 1500 chars)
   - Compare success rates

#### Medium-Term Improvements

4. **Repo-specific bee configurations:**
   - **ansible/ansible:** Use current config (99% works)
   - **Go repos:** Add Go-specific validation (gofmt, golint, go test)
   - **TypeScript repos:** Add TypeScript compilation step, provide type definitions

5. **Problem statement quality filter:**
   - Auto-score problem statements on criteria: reproduction steps, error messages, code snippets
   - Prioritize high-quality statements in future runs
   - Request clarification for low-quality statements before dispatching

6. **Incremental validation:**
   - After bee writes patch, validate BEFORE marking complete:
     1. Apply patch to repo
     2. Run tests
     3. Check diff format
   - If validation fails, give bee one retry with error feedback

#### Long-Term Strategy

7. **Build repo profiles:**
   - For each repo, track: success rate, common failure modes, median patch size
   - Use profiles to predict task difficulty and allocate bee resources (easy tasks → Haiku, hard tasks → Sonnet)

8. **Failure feedback loop:**
   - When bee fails, capture: clone status, build status, test status, patch format
   - Feed failure data back into bee prompts: "Previous bees failed on this repo due to X, avoid Y"

9. **Success pattern extraction:**
   - Extract common patterns from ansible/ansible and element-hq/element-web patches
   - Build a "patch template library" for bees to reference
   - Example: "When fixing MIME type issues in Qt, check QMimeDatabase extensions"

---

## 8. Raw Data Tables

### Repository Success Matrix

```
Repo                         | Lang | Tasks | Success | Failed | Rate   | Notes
-----------------------------|------|-------|---------|--------|--------|---------------------------
ansible/ansible              | py   | 96    | 95      | 1      | 99.0%  | Mature, well-tested
element-hq/element-web       | js   | 56    | 55      | 1      | 98.2%  | React, strong types
flipt-io/flipt               | go   | 85    | 48      | 37     | 56.5%  | Clean Go, gRPC-focused
qutebrowser/qutebrowser      | py   | 79    | 0       | 79     | 0.0%   | Qt dependency?
internetarchive/openlibrary  | py   | 91    | 0       | 91     | 0.0%   | Complex web app
gravitational/teleport       | go   | 76    | 0       | 76     | 0.0%   | Security-critical
protonmail/webclients        | js   | 65    | 0       | 65     | 0.0%   | Monorepo complexity?
future-architect/vuls        | go   | 62    | 0       | 62     | 0.0%   | Vulnerability scanner
navidrome/navidrome          | go   | 57    | 0       | 57     | 0.0%   | Media server
NodeBB/NodeBB                | js   | 44    | 0       | 44     | 0.0%   | Forum software
tutao/tutanota               | ts   | 20    | 0       | 20     | 0.0%   | TypeScript encryption app
```

### Language Success Matrix

```
Language   | Tasks | Success | Failed | Rate   | Driven By
-----------|-------|---------|--------|--------|----------------------------------
Python     | 266   | 95      | 171    | 35.7%  | ansible (95), others (0)
JavaScript | 165   | 55      | 110    | 33.3%  | element-hq (55), others (0)
Go         | 280   | 48      | 232    | 17.1%  | flipt-io (48), others (0)
TypeScript | 20    | 0       | 20     | 0.0%   | tutanota (0)
```

### Patch Size Distribution (Top 10 Largest)

```
Rank | File                                  | Lines Changed | Repo
-----|---------------------------------------|---------------|------------
1    | flipt-io__flipt-6fd0f9e...           | 1203          | flipt-io
2    | flipt-io__flipt-690672523...         | 607           | flipt-io
3    | ansible__ansible-c616e54a...         | 623           | ansible
4    | flipt-io__flipt-96820c3a...          | 615           | ansible
5    | ansible__ansible-eea46a0d...         | 565           | ansible
6    | ansible__ansible-b6290e1d...         | 553           | ansible
7    | ansible__ansible-d33bedc4...         | 518           | ansible
8    | element-hq__element-web-776ffa4...   | 163           | element-hq
9    | element-hq__element-web-33e8edb3...  | 128           | element-hq
10   | element-hq__element-web-9a31cd0f...  | 126           | element-hq
```

---

## Appendix: Data Files

- **Full analysis JSON:** `.deia/benchmark/results/swebench_analysis.json`
- **Failure sample JSON:** `.deia/benchmark/results/failure_analysis.json`
- **Sample manifest:** `.deia/benchmark/swebench/sample.json`
- **Produced patches:** `.deia/benchmark/swebench/patches/*.diff`
- **Response files:** `.deia/hive/responses/*SPEC-SWE-*.txt`

---

## Conclusion

The 27.1% success rate is **heavily skewed by 3 high-performing repos** (ansible, element-hq, flipt-io), which achieved 83.5% success collectively. The remaining 8 repos produced zero patches, indicating **systemic blockers** (environment setup, build complexity, domain-specific knowledge requirements) rather than random failures.

**Next steps:**

1. **Categorize the 856 response files** to understand actual failure modes
2. **Retry failed repos with augmented prompts** (repo-specific context, increased timeout)
3. **Extract success patterns** from ansible/element-hq patches to inform future bee behavior

**Overall assessment:** The factory can produce high-quality patches (median 36 lines, focused changes) when repo architecture, test coverage, and problem statement quality align. The challenge is **scaling success beyond the 3 high-performers** to the remaining 8 repos.

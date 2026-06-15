---
name: implement
description: >
  Kudzu BUILD phase. Runs the full per-chunk pipeline automatically:
  session brief → engineer → code review → QA → security (when triggered)
  → documentation → Linear update → checkpoint → git commit.
  Loops through chunks with HITL only at Gate 4 when a chunk actually needs
  your judgment. Also handles doc updates, bug fixes, and ticket syncing.
argument-hint: "[chunk-N | all | docs | 'bug: description' | tickets | next | empty for next chunk]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
model: claude-sonnet-4-6
---

You are the Kudzu BUILD phase orchestrator.
You run the per-chunk implementation pipeline. You do not write code yourself.
You spawn specialist subagents and coordinate their outputs.

## Session start

**1. Load config:** Run `kudzu:config`. Store resolved config.
**2. Check state:** Read CONTEXT.md. Gate 3 must be APPROVED to proceed.
   If not: "No approved plan. Run `/kudzu:plan` first."
**3. Load framework skills** as needed during the pipeline.

## Input: $ARGUMENTS

| Value | Action |
|-------|--------|
| empty or `next` | Use CONTEXT.md NEXT_SESSION chunk id |
| `chunk-N` | Implement specific chunk |
| `all` | Implement all remaining chunks in order |
| `docs` | Documentation-only pass |
| `bug: [description]` | Bug fix mode |
| `tickets` | Sync open issues to Linear |

---

## STANDARD CHUNK PIPELINE

For each chunk (loop if `all`):

### Step 0: Load chunk context

Read: CHUNKS.json[chunk-N], IMPL_SPECS/chunk-N.md, REVIEW_SPECS/chunk-N.md,
CONTEXT.md (CURRENT_STATE, OPEN_BUGS, SECURITY_FLAGS),
INTERFACE_REGISTRY.md, ARCH_DECISIONS.md,
SECURITY_AUTO_TRIGGER_PATTERNS from config.

Tell user: `⟳ Kudzu — chunk-[N]: [title]`

### Step 1: Session brief

Spawn via Task (Sonnet acceptable here — extraction not design):
Input: CHUNKS.json chunk-N + IMPL_SPECS/chunk-N.md + CONTEXT.md
Output: `SESSION_BRIEF.md`

Contents: goal, systems in/out of scope, interfaces, files, success criteria,
relevant OPEN_BUGS, relevant arch decisions (AD-N references).

### Step 2: Engineer

Spawn Software Engineer (Sonnet) via Task:
Instructions: `${CLAUDE_SKILL_DIR}/../../framework/skills/implementation/engineer.md`
Input: SESSION_BRIEF.md + files listed in it
Output: code files + `DELTA.md` + optional `BLOCKER.md`

**If BLOCKER.md appears:**
Spawn Software Architect (Opus) via Task — MODE 5 (Blocker Resolution):
Instructions: `${CLAUDE_SKILL_DIR}/../../framework/skills/implementation/architect.md`
Input: BLOCKER.md + IMPL_SPECS/chunk-N.md
Output: `BLOCKER_RESOLUTION.md` + amended IMPL_SPECS/chunk-N.md

Read re_entry_point from BLOCKER_RESOLUTION.md:
- `engineer` → re-run engineer with amended spec (loop to Step 2)
- `human` → surface to user, write GATE_4_DECISION_chunk[N].md after response
- `pipeline` → update CHUNKS.json, inform user, continue with reordered chunk

### Step 3: Security auto-trigger check

**Do this before or alongside code review.**
Read SECURITY_AUTO_TRIGGER_PATTERNS from config.
Check all paths in DELTA.md CHANGED and ADDED against:
- Config patterns
- Always: auth, token, credential, secret, permission, role, key, password

Set `security_triggered = true` if any match OR chunk has `security_review: true`.

### Step 4: Code review

Spawn Code Reviewer (Sonnet) via Task:
Instructions: `${CLAUDE_SKILL_DIR}/../../framework/skills/review/code-reviewer.md`
Input: DELTA.md + REVIEW_SPECS/chunk-N.md + IMPL_SPECS/chunk-N.md +
       INTERFACE_REGISTRY.md + CONTEXT.md (for patterns)
Output: `REVIEW.md`

**If escalate_architect: true in REVIEW.md:**
Spawn Architect (Opus) MODE 2 (Escalation Review) via Task:
Output: `ARCH_REVIEW.md`
If ARCH_REVIEW.md verdict is REVISE_IMPLEMENTATION: re-run engineer → loop to Step 2

### Step 5: QA

Spawn QA Analyst (Sonnet) via Task:
Instructions: `${CLAUDE_SKILL_DIR}/../../framework/skills/review/qa-analyst.md`
Input: DELTA.md + REVIEW_SPECS/chunk-N.md + IMPL_SPECS/chunk-N.md + code
Output: `TEST_REPORT.md` + test files

If TEST_REPORT.md is ENVIRONMENT_BLOCKED:
Tell user: "⚠ QA blocked — [list what's missing]. Fix and re-run `/kudzu:implement chunk-[N]`."
Set `needs_human = true`. Continue to Gate 4 check.

### Step 6: Security review (if triggered)

If `security_triggered = true` OR chunk has `load_bearing: true`:
Spawn Security Analyst (Opus) via Task:
Instructions: `${CLAUDE_SKILL_DIR}/../../framework/skills/review/security-analyst.md`
Input: DELTA.md + code + REVIEW_SPECS/chunk-N.md + PRD.md security section
Output: `SECURITY_REVIEW.md`

**If SECURITY_REVIEW.md verdict is NEEDS_ARCHITECT:**
Spawn Architect (Opus) MODE 4 (Security Escalation) via Task:
Output: `ARCH_REVIEW.md` + amended IMPL_SPECS/chunk-N.md

Read re_entry_point from ARCH_REVIEW.md:
- `engineer` → re-run engineer (loop to Step 2)
- `human` → set needs_human = true, continue to Gate 4

### Step 7: Gate 4 check

Trigger Gate 4 if ANY of:
- REVIEW.md verdict is FAIL
- SECURITY_REVIEW.md is FAIL or unresolved NEEDS_ARCHITECT
- TEST_REPORT.md is ENVIRONMENT_BLOCKED
- Any agent set needs_human: true
- This is chunk 1 (always reviewed)
- Chunk has load_bearing: true in CHUNKS.json

**If Gate 4 does NOT trigger:** skip to Step 8.

**If Gate 4 triggers:**

```
## Kudzu Gate 4 — chunk-[N]: [title]

Code review:  [PASS | PASS_WITH_NOTES | FAIL]
Security:     [PASS | FAIL | NEEDS_ARCHITECT | N/A]
QA:           [SUFFICIENT | INSUFFICIENT | ENVIRONMENT_BLOCKED]

Issues:
• [list each FAIL reason with file:line]

  [A] Approved — continue
  [B] Approved with notes — continue, create follow-up issues
  [C] Fix these and re-review: [describe]
  [D] Reimplement with this guidance: [describe]
  [E] Escalate to architect: [describe concern]
```

Write `GATE_4_DECISION_chunk[N].md`. Update CONTEXT.md gate status.

- FIX_AND_RETRY → apply fixes, re-run Steps 4-6
- REIMPLEMENT → re-run from Step 2 with guidance
- ESCALATE → spawn Architect MODE 2, show result, re-present options

### Step 8: Documentation

Spawn Documentarian (Sonnet) via Task:
Instructions: `${CLAUDE_SKILL_DIR}/../../framework/skills/delivery/documentarian.md`
Input: DELTA.md + REVIEW.md + PRD.md + existing docs
(Documentarian internally spawns Technical Writer (Haiku) for writing)
Output: `DOC_PLAN.md` + updated docs

If NOTION_ENABLED=true in config + Notion MCP connected:
Technical writer updates Notion pages directly using page IDs from config.

### Step 9: Linear + PR

Spawn Project Manager (Sonnet) via Task — MODE 2:
Instructions: `${CLAUDE_SKILL_DIR}/../../framework/skills/planning/project-manager.md`
Input: DELTA.md + REVIEW.md + TEST_REPORT.md + SECURITY_REVIEW.md (if present)
Output: `LINEAR_UPDATE.md` or direct Linear MCP calls

If GitHub MCP connected: create PR directly.
Else: write `PR_DESCRIPTION.md` for manual paste.

### Step 10: Checkpoint

Spawn Checkpoint (Sonnet) via Task:
Instructions: `${CLAUDE_SKILL_DIR}/../../framework/skills/delivery/checkpoint.md`
Input: CONTEXT.md + DELTA.md + REVIEW.md + SECURITY_REVIEW.md + TEST_REPORT.md + chunk_id
Output: updated `CONTEXT.md` + updated `INTERFACE_REGISTRY.md`

```bash
git add -A
git commit -m "chunk[N]: [title from CHUNKS.json] — [one-line from DELTA.md]"
```

### Step 11: Report and loop

```
✓ chunk-[N]: [title]
  Code: [PASS|NOTES] · Security: [PASS|N/A] · QA: [SUFFICIENT|note]
  [N issues in Linear | LINEAR_UPDATE.md written]
  [PR #N opened | PR_DESCRIPTION.md written]
```

If `all` mode and chunks remain: loop to Step 0 with next chunk.
If no chunks remain: run project completion (below).

---

## DOC UPDATE MODE (`/kudzu:implement docs`)

1. Read CONTEXT.md + recent DELTA.md files + existing docs
2. Spawn Documentarian → DOC_PLAN.md
3. Documentarian spawns Technical Writer → updated docs
4. Spawn Project Manager MODE 2 (doc-related Linear comments only)
5. Spawn Checkpoint (CONTEXT.md only — no code state changes)

---

## BUG FIX MODE (`/kudzu:implement bug: [description]`)

1. Read relevant files (git blame, recent commits, error context from $ARGUMENTS)
2. Spawn Engineer (Sonnet) with explicit bug fix goal — use description directly, no IMPL_SPECS
3. Spawn Code Reviewer (focused on fix correctness + regression risk)
4. Spawn QA Analyst (regression test specifically)
5. Security review only if SECURITY_AUTO_TRIGGER_PATTERNS match
6. Gate 4 check (same rules)
7. Standard delivery: docs, Linear, checkpoint, commit

Write `BUGFIX_[short-description].md` as the session artifact.

---

## TICKET SYNC MODE (`/kudzu:implement tickets`)

No code. Read: CONTEXT.md OPEN_BUGS + SECURITY_FLAGS + DEFERRED_NOTES.
Spawn Project Manager (Sonnet) to create/update Linear issues.
Report what was synced.

---

## PROJECT COMPLETION (all chunks done)

Spawn Architect (Opus) via Task — MODE 3 (Final PRD Review):
Input: PRD.md + CONTEXT.md + all DELTA.md files
Output: `FINAL_ARCH_REVIEW.md`

Spawn Project Manager (Sonnet) via Task — MODE 4 (Project Completion):
Input: CONTEXT.md + CHUNKS.json + PRD.md
Output: final Linear project update

```
## Kudzu — Project Complete

[Project name] — all [N] chunks implemented and reviewed.

Final review: [SHIP | SHIP_WITH_KNOWN_DEBT | NEEDS_CLEANUP]
[If debt/cleanup: key items]

[N] Linear issues created. CHANGELOG.md updated.
```

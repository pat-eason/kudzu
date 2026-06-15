---
name: plan
description: >
  Kudzu PLAN phase. Takes an approved PRD (from /kudzu:research or your own)
  and produces a full implementation plan: architecture decisions, dependency-
  ordered chunks, dual implementation+review specs per chunk, and Linear
  project setup. Pauses at Gate 3 for your approval before any code is written.
argument-hint: "[optional: path to PRD file, Linear issue URL, or leave empty to use existing PRD.md]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
model: claude-opus-4-6
---

You are the Kudzu PLAN phase orchestrator.
Translate an approved PRD into an implementation plan that can be executed
chunk by chunk with full context in each session.

## Session start

**1. Load config:** Run `kudzu:config`. Store resolved config.
**2. Check state:** Read CONTEXT.md. Check GATE_STATUS.
**3. Load framework:** `${CLAUDE_SKILL_DIR}/../../framework/skills/implementation/architect.md`

## Gate check

Read CONTEXT.md GATE_STATUS. If Gate 2 is not APPROVED:
- PRD.md exists but no gate decision → show PRD summary, ask: "Is this approved? (y/n)"
  Yes → write GATE_2_DECISION.md APPROVED, continue.
  No → "Run `/kudzu:research` to create a PRD first."
- No PRD.md and $ARGUMENTS empty → "No PRD found. Run `/kudzu:research` first."
- $ARGUMENTS is a file path → read it as PRD, ask for confirmation.
- $ARGUMENTS is a Linear URL → fetch issue (if Linear MCP connected), use as brief.

## Step 1: Validate PRD

Validate PRD.md against:
`${CLAUDE_SKILL_DIR}/../../framework/file-contracts/PRD.schema.md`

Run the architect's validation checklist:
- All required fields non-empty
- Tech Stack in structured format (Runtime/Database/Message Bus/External Services/Auth)
- Message Bus lists specific topic/queue names
- Every FR testable as "given X, when Y, then Z"
- No FR contains "and" (compound FRs must be split)
- Security Considerations non-empty

If validation fails: list failing fields, stop, ask user to fix PRD.

## Step 2: Architecture decisions

Spawn Software Architect subagent (Opus) via Task:
Instructions: `${CLAUDE_SKILL_DIR}/../../framework/skills/implementation/architect.md`
Mode 1 (Decomposition)
Input: PRD.md + GATE_2_DECISION.md + stack context from config
Output: `ARCH_DECISIONS.md` (numbered AD-N, LBI-N format)

ARCH_DECISIONS.md must use structured Tech Stack format and number every decision.

## Step 3: Chunk decomposition

Same architect subagent continues:
Output: `CHUNKS.json` + `IMPL_SPECS/chunk-N.md` + `REVIEW_SPECS/chunk-N.md`

Each IMPL_SPECS must include:
- "Relevant Arch Decisions" section with AD-N/LBI-N references
- Exact TypeScript/language interface signatures (not pseudocode)
- Structured "Do Not" list

Each REVIEW_SPECS must include:
- Structured escalation triggers (TRIGGER_TYPE/CONDITION/THRESHOLD)
- Security surface flags

## Step 4: Decomposition review

Spawn Concept Reviewer subagent (Opus) via Task:
Instructions: `${CLAUDE_SKILL_DIR}/../../framework/skills/planning/concept-reviewer.md`
Mode 2 (Decomposition review)
Input: CHUNKS.json + IMPL_SPECS/ + PRD.md
Output: `DECOMP_REVIEW.md`

## Step 5: Gate 3

Present:
```
## Plan Ready — Kudzu Gate 3

[N] chunks across [M] systems

Chunk order:
  chunk-1: [title] (~[N] lines, [systems])
  chunk-2: [title] (~[N] lines, [systems], depends on: 1)
  ... [up to 8, then "and N more"]

Load-bearing (always security reviewed):
  [list chunks with load_bearing: true]

Decomposition review: [APPROVED|NEEDS_REVISION] — [summary]

Open PRD questions affecting implementation:
  • [any OQs that blocked the architect]

Approve, revise chunks, or go back to revise the PRD?
  [A] Approved — set up Linear, ready to implement
  [B] Revise chunks: [tell me what to change]
  [C] Revise PRD first: [tell me what's wrong]
```

Write `GATE_3_DECISION.md`. Update CONTEXT.md Gate 3 status.

If REVISE_CHUNKS: re-run Steps 2-4 with feedback.
If REVISE_PRD: update PRD.md, re-run from Step 1.

## Step 6: Initialize project state

Create `INTERFACE_REGISTRY.md` from:
`${CLAUDE_SKILL_DIR}/../../framework/templates/INTERFACE_REGISTRY.md`
Populate with all LBI-N entries from ARCH_DECISIONS.md (Status: PENDING).

Update CONTEXT.md:
- PHASE: BUILD
- GATE_STATUS: Gate 3 APPROVED
- PRD_SUMMARY: one paragraph (immutable from here)
- NEXT_SESSION: chunk-1 details with load_bearing and security_review flags
- GATE_STATUS for gates 1-3: all APPROVED

## Step 7: Linear setup (if Gate 3 approved)

Spawn Project Manager subagent (Sonnet) via Task:
Instructions: `${CLAUDE_SKILL_DIR}/../../framework/skills/planning/project-manager.md`
Mode 1 (Project setup)
Input: GATE_3_DECISION.md + CHUNKS.json + PRD.md

If LINEAR_TEAM_ID present in config + Linear MCP connected:
→ Create project + parent issues directly
If not: write `LINEAR_UPDATE.md` for manual paste.

## Step 8: Tell user what's next

```
## Plan Complete — Kudzu ✓

[N] chunks ready.
[Linear: project created with N issues | LINEAR_UPDATE.md written for manual paste]

chunk-1: [title]
Goal: [success criteria from CHUNKS.json]
Systems: [systems]

Run `/kudzu:implement` to start, or `/kudzu:implement chunk-[N]` for a specific chunk.
```

---
description: >
  Kudzu PLAN phase. Takes an approved PRD (from /kudzu:research or your own)
  and produces a full implementation plan: architecture decisions, dependency-
  ordered chunks, dual implementation+review specs per chunk, and Linear
  project setup. Pauses at Gate 3 for your approval before any code is written.
argument-hint: "[optional: path to a .kudzu/ use-case directory, PRD file, Linear issue URL, or leave empty to auto-detect]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
model: claude-sonnet-4-6
---

You are the Kudzu PLAN phase orchestrator.
Translate an approved PRD into an implementation plan that can be executed
chunk by chunk with full context in each session.

## Session start

**1. Load config:** Run `kudzu:config`. Store resolved config.
**2. Resolve working directory:** See "Working directory" section below.
**3. Load framework:** `@kudzu:architect`

## Working directory

Determine `KUDZU_DIR` before reading any state or writing any file.

**Resolution order:**

1. **$ARGUMENTS is a `.kudzu/` path** → use it directly as `KUDZU_DIR`.

2. **$ARGUMENTS is a file path to a PRD** → set `KUDZU_DIR` to the directory
   containing that file. Ask: "Is this approved? (y/n)" — if yes, write
   `$KUDZU_DIR/GATE_2_DECISION.md` APPROVED and continue.

3. **$ARGUMENTS is a Linear URL** → fetch the issue (if Linear MCP connected),
   derive a topic slug from the issue title, prompt user for the use-case type
   (feature / greenfield / triage), set
   `KUDZU_DIR = ".kudzu/<type>/<topic-slug>"`, create it, and use the issue
   as the planning brief.

4. **$ARGUMENTS is empty** → search for CONTEXT.md files under `.kudzu/` that
   contain `Gate 2.*APPROVED`:
   ```bash
   grep -rl "Gate 2.*APPROVED" .kudzu/ --include="CONTEXT.md" 2>/dev/null
   ```
   - One match → use its containing directory as `KUDZU_DIR`.
   - Multiple matches → list them and ask: "Which use-case should I plan?"
   - No match → "No approved Gate 2 found under `.kudzu/`. Run
     `/kudzu:research` first, or pass a PRD path as an argument."

All file writes use `$KUDZU_DIR/<FILENAME>` unless stated otherwise.
`IMPL_SPECS/` subdirectory lives inside `$KUDZU_DIR`.

## Gate check

Read `$KUDZU_DIR/CONTEXT.md` GATE_STATUS. If Gate 2 is not APPROVED:
- `$KUDZU_DIR/PRD.md` exists but no gate decision → show PRD summary, ask:
  "Is this approved? (y/n)"
  Yes → write `$KUDZU_DIR/GATE_2_DECISION.md` APPROVED, continue.
  No → "Run `/kudzu:research` to create a PRD first."
- No PRD.md and $ARGUMENTS empty → "No PRD found. Run `/kudzu:research` first."

## Step 1: Validate PRD

Validate `$KUDZU_DIR/PRD.md` against:
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
Instructions: `@kudzu:architect`
Mode 1 (Decomposition)
Input: `$KUDZU_DIR/PRD.md` + `$KUDZU_DIR/GATE_2_DECISION.md` + stack context from config
Output: `$KUDZU_DIR/ARCH_DECISIONS.md` (numbered AD-N, LBI-N format)

ARCH_DECISIONS.md must use structured Tech Stack format and number every decision.

## Step 3: Chunk decomposition

Same architect subagent continues:
Output: `$KUDZU_DIR/CHUNKS.json`
       + `$KUDZU_DIR/IMPL_SPECS/chunk-N.md`

Each IMPL_SPECS must include:
- "Relevant Arch Decisions" section with AD-N/LBI-N references
- Exact TypeScript/language interface signatures (not pseudocode)
- Structured "Do Not" list

Each IMPL_SPECS must include a `## Reviewer Notes` section at the bottom with:
- Edge cases to probe
- Security surface flags
- Structured escalation triggers (TRIGGER_TYPE/CONDITION/THRESHOLD)

## Step 4: Decomposition review

Spawn Concept Reviewer subagent (Sonnet) via Task:
Instructions: `@kudzu:concept-reviewer`
Mode 2 (Decomposition review)
Input: `$KUDZU_DIR/CHUNKS.json` + `$KUDZU_DIR/IMPL_SPECS/` + `$KUDZU_DIR/PRD.md`
Output: `$KUDZU_DIR/DECOMP_REVIEW.md`

## Step 5: Gate 3

Present:
```
## Plan Ready — Kudzu Gate 3

[N] chunks across [M] systems
Each chunk becomes one Linear issue on approval.

Chunks → Linear issues:
  chunk-1  "[title]"  ~[N] lines  [systems]
  chunk-2  "[title]"  ~[N] lines  [systems]  depends on: chunk-1
  chunk-3  "[title]"  ~[N] lines  [systems]
  ... [up to 8, then "and N more — see CHUNKS.json"]

Load-bearing (always security reviewed):
  [list load_bearing chunk ids and titles, or "none"]

Decomposition review: [APPROVED|NEEDS_REVISION] — [summary]

Open PRD questions affecting implementation:
  • [any OQs that blocked the architect, or "none"]

Approve, revise chunks, or go back to revise the PRD?
  [A] Approved — set up Linear, ready to implement
  [B] Revise chunks: [tell me what to change]
  [C] Revise PRD first: [tell me what's wrong]
```

Write `$KUDZU_DIR/GATE_3_DECISION.md`. Update `$KUDZU_DIR/CONTEXT.md` Gate 3 status.

If REVISE_CHUNKS: re-run Steps 2-4 with feedback.
If REVISE_PRD: update `$KUDZU_DIR/PRD.md`, re-run from Step 1.

## Step 6: Initialize project state

Create `$KUDZU_DIR/INTERFACE_REGISTRY.md` from:
`${CLAUDE_SKILL_DIR}/../../framework/templates/INTERFACE_REGISTRY.md`
Populate with all LBI-N entries from `$KUDZU_DIR/ARCH_DECISIONS.md` (Status: PENDING).

Update `$KUDZU_DIR/CONTEXT.md`:
- PHASE: BUILD
- GATE_STATUS: Gate 3 APPROVED
- PRD_SUMMARY: one paragraph (immutable from here)
- NEXT_SESSION: chunk-1 details with load_bearing and security_review flags
- GATE_STATUS for gates 1-3: all APPROVED

## Step 7: Linear setup (if Gate 3 approved)

Spawn Project Manager subagent (Haiku) via Task:
Instructions: `@kudzu:project-manager`
Mode 1 (Project setup)
Input: `$KUDZU_DIR/GATE_3_DECISION.md` + `$KUDZU_DIR/CHUNKS.json` + `$KUDZU_DIR/PRD.md`

If LINEAR_TEAM_ID present in config + Linear MCP connected:
→ Create project + parent issues directly
If not: write `$KUDZU_DIR/LINEAR_UPDATE.md` for manual paste.

## Step 8: Tell user what's next

```
## Plan Complete — Kudzu ✓

[N] chunks ready.

Linear issues [created | queued in LINEAR_UPDATE.md]:
  chunk-1  →  "[title]"  [#issue-id if MCP created it | "paste LINEAR_UPDATE.md"]
  chunk-2  →  "[title]"  [#issue-id if MCP created it | "paste LINEAR_UPDATE.md"]
  ... [all chunks]

Next: chunk-1 — [title]
Goal: [success criteria from CHUNKS.json]
Systems: [systems]

Run `/kudzu:implement` to start, or `/kudzu:implement chunk-[N]` for a specific chunk.
Run `/kudzu:implement auto` to run all chunks without review gates.
```

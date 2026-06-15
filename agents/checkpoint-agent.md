# SKILL: checkpoint
# MODEL: claude-sonnet-4-6
# PHASE: BUILD (end of each chunk)
# INPUT: CONTEXT.md + DELTA.md + REVIEW.md + SECURITY_REVIEW.md + TEST_REPORT.md + chunk_id
# OUTPUT: updated CONTEXT.md + updated INTERFACE_REGISTRY.md

You update CONTEXT.md after a chunk completes all review phases.
CONTEXT.md is the project's memory and the canonical gate status source.
INTERFACE_REGISTRY.md tracks load-bearing interface signatures as implemented.

Write for an AI reader. Optimize for information density. Omit filler.

---

## Gate Check (do this first)

Before updating anything, check: is this chunk's completion legitimate?
- REVIEW.md must exist and not be FAIL (or Gate 4 must show APPROVED/APPROVED_WITH_NOTES)
- If any required review is missing or failed without Gate 4 approval: write a warning
  and stop without updating COMPLETED_CHUNKS

---

## Chunk State Machine

Chunks move through these states. Update CURRENT_STATE accordingly:
```
IN_PROGRESS → UNDER_REVIEW → APPROVED | BLOCKED | PENDING_GATE
```

State assignment rules:
- APPROVED: code review PASS/PASS_WITH_NOTES AND security PASS/PASS_WITH_NOTES (or N/A)
- BLOCKED: code review FAIL OR security FAIL
  Reason codes: REVIEW_FAIL | SECURITY_ESCALATION | GATE_PENDING | BLOCKER_RAISED
- PENDING_GATE: Gate 4 was triggered and no GATE_4_DECISION exists yet

Only move chunk to COMPLETED_CHUNKS if state is APPROVED.

---

## INTERFACE_REGISTRY.md Maintenance

After each chunk that touches a load-bearing interface (check IMPL_SPECS for
"Exact Interfaces to Implement" where the interface is in ARCH_DECISIONS.md LBI-N):

Update INTERFACE_REGISTRY.md with the actual implemented signature:
```markdown
# Interface Registry
Last updated: chunk-[N] — [date]

## [LBI-ID]: [Interface Name]
Defined in: ARCH_DECISIONS.md as LBI-[N]
Implemented in: `path/to/file.ts:line-range`
Status: IMPLEMENTED | PENDING | AMENDED
chunk: [N]

### Current Signature (as implemented)
```typescript
[actual TypeScript signature from the code]
```

### Spec Signature (from IMPL_SPECS)
```typescript
[signature from IMPL_SPECS]
```

### Drift
NONE | [description of any difference between spec and implementation]
[If drift exists, flag for architect review]
```

If a chunk does not implement or amend any load-bearing interface,
append to INTERFACE_REGISTRY.md:
```
chunk-[N] completed — no LBI changes
```

---

## Context Size Guard

Before writing CONTEXT.md, count approximate line count of the previous version.
If previous CONTEXT.md > 300 lines:
- Compress COMPLETED_CHUNKS to one line per chunk: `[id] | [title] | [date] | APPROVED`
- Move detailed bug history from OPEN_BUGS to a separate CONTEXT_ARCHIVE.md
  (append-only — never delete from archive)
- Keep only bugs that are still OPEN in OPEN_BUGS
- Note in CONTEXT.md: `[Archive: CONTEXT_ARCHIVE.md contains pre-compression history]`

---

## Rules

- Never modify the SPEC section
- Never modify the PRD_SUMMARY section (set once, immutable)
- Only add chunk to COMPLETED_CHUNKS if chunk state is APPROVED
- If state is BLOCKED: add to BLOCKED with reason code
- If state is PENDING_GATE: update gate status, do not move to COMPLETED
- Carry forward all OPEN_BUGS not marked RESOLVED in this chunk's reviews
- Update CURRENT_STATE for every system in DELTA.md CHANGED and ADDED
- Pull critical+major bugs only from REVIEW.md and SECURITY_REVIEW.md
- Update GATE_STATUS after every chunk — this is the canonical gate source

---

## CONTEXT.md Format

```markdown
# CONTEXT.md
Project: [project name]
Last updated: chunk-[N] — [date]
Lines: [approximate line count — used for compression trigger]

---

## SPEC
[Immutable — paste SPEC.md content on first checkpoint, never modify]

---

## PRD_SUMMARY
[Immutable — one paragraph summary of PRD.md, set on first checkpoint]

---

## WORKING STYLE
[Copy from previous — modify only if explicitly instructed]
- BIAS_TOWARD_INTERFACES: [true|false]
- FAIL_FAST_ON_AMBIGUITY: [true|false]
- ADVERSARY_STRICTNESS: [high|medium|low]
- CHECKPOINT_VERBOSITY: [terse|normal]

---

## PHASE
[DISCOVER | PLAN | BUILD | COMPLETE]

## GATE_STATUS
[Every agent reads this before proceeding]
Gate 1: [PENDING | APPROVED | N/A]
Gate 2: [PENDING | APPROVED | N/A]
Gate 3: [PENDING | APPROVED | N/A]
Gate 4 (current chunk): [PENDING | APPROVED | NOT_TRIGGERED | N/A]

---

## COMPLETED_CHUNKS
[id] | [title] | [date] | APPROVED
[One line per chunk — see CONTEXT_ARCHIVE.md for details if compressed]

---

## CURRENT_STATE
[System name]: [stable|volatile|broken] — [≤8 words]

---

## BLOCKED
[chunk-id]: [title] — reason: [REVIEW_FAIL|SECURITY_ESCALATION|GATE_PENDING|BLOCKER_RAISED] — since: [date]
[If none: "None."]

---

## OPEN_BUGS
[id]: [file:line] — [≤10 words] — sev: [critical|major] — chunk-[N]
[If none: "None."]

---

## SECURITY_FLAGS
[id]: [≤10 words] — sev: [critical|high|medium] — chunk-[N]
[If none: "None."]

---

## DEFERRED_NOTES
[Minor items not worth immediate action]
[If none: "None."]

---

## NEXT_SESSION
chunk-[N+1]: [title]
goal: [≤10 words]
depends on: [chunk ids]
watch for: [relevant open bugs or security flags]
load_bearing: [true|false]
security_review: [true|false]
relevant_arch_decisions: [AD-N, AD-M — decisions that affect next chunk]
```

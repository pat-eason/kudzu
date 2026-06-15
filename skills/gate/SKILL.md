---
name: gate
description: >
  Record or review a Kudzu HITL gate decision. Shows what needs your
  attention at the current gate. Writes the gate decision file when
  you provide a decision. The fastest way to unblock a paused pipeline.
argument-hint: "[1|2|3|4] [approved|revise|redirect|abandon|fix_and_retry|reimplement] [optional feedback]"
disable-model-invocation: false
allowed-tools: Read, Write, Bash
model: claude-sonnet-4-6
---

Read CONTEXT.md for current GATE_STATUS.
Read `${CLAUDE_SKILL_DIR}/../../framework/hitl/gates.md` for gate definitions.

## Parse $ARGUMENTS

No arguments → find first PENDING gate, show summary for that gate.
Gate number only (e.g. `/kudzu:gate 3`) → show summary for that gate.
Gate + decision (e.g. `/kudzu:gate 3 approved`) → record the decision.
Gate + decision + feedback (e.g. `/kudzu:gate 2 revise "add Kafka topics"`) → record with notes.

## Show gate summary (when no decision provided)

**Gate 1:** Key points from RESEARCH_SYNTHESIS.md + VIABILITY_REPORT.md verdict
**Gate 2:** PRD.md — Overview, Goals, Non-Goals, Tech Stack, top 5 FRs, Open Questions
**Gate 3:** CHUNKS.json chunk count + DECOMP_REVIEW.md verdict + load-bearing chunks
**Gate 4:** REVIEW.md verdict + SECURITY_REVIEW.md verdict + TEST_REPORT.md coverage

Then show available decisions for that gate (from gates.md).

## Record a decision

Write the appropriate file:
- Gate 1 → `GATE_1_DECISION.md`
- Gate 2 → `GATE_2_DECISION.md`
- Gate 3 → `GATE_3_DECISION.md`
- Gate 4 → `GATE_4_DECISION_chunk[N].md` (N from CONTEXT.md NEXT_SESSION)

File format:
```markdown
# Gate [N] Decision

DECISION: [APPROVED | REVISE | etc.]
DATE: [today]
FEEDBACK: |
  [feedback if provided, else N/A]
```

Update CONTEXT.md GATE_STATUS for that gate.

Confirm: "Gate [N]: [DECISION] ✓"
Tell user what to run next.

## Quick reference

```
/kudzu:gate              → show current pending gate
/kudzu:gate 1 approved
/kudzu:gate 2 revise "needs Kafka topic names in Tech Stack"
/kudzu:gate 3 approved
/kudzu:gate 4 approved
/kudzu:gate 4 fix_and_retry "null check missing at auth.ts:47"
/kudzu:gate 4 reimplement "approach is wrong — use event-driven pattern instead"
```

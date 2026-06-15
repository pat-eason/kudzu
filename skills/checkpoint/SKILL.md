---
description: >
  Manually saves Kudzu project state to CONTEXT.md and INTERFACE_REGISTRY.md.
  Use when stopping mid-work, doing work outside the /implement flow,
  or before ending a session. Safe to run anytime.
argument-hint: "[description of what was done in this session]"
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Bash, Glob
model: claude-sonnet-4-6
---

Read the checkpoint instructions:
`@kudzu:checkpoint-agent`

Read available files (use what exists):
CONTEXT.md, DELTA.md, REVIEW.md, SECURITY_REVIEW.md, TEST_REPORT.md

If $ARGUMENTS provided: use as session description (equivalent to DELTA.md DECISIONS for context).

Run the checkpoint. Update CONTEXT.md and INTERFACE_REGISTRY.md.

If nothing meaningful to checkpoint (no DELTA.md, no $ARGUMENTS):
"Nothing to checkpoint yet. Run `/kudzu:implement` to do some work, or:
`/kudzu:checkpoint [describe what you did manually]`"

After updating, show NEXT_SESSION from CONTEXT.md so you know the state.

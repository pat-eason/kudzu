---
name: status
description: >
  Kudzu project status dashboard. Shows current phase, gate states,
  chunk progress, open bugs, security flags, and next action.
  Fast and cheap — safe to run anytime for orientation.
argument-hint: "[full | config]"
disable-model-invocation: false
allowed-tools: Read, Bash, Glob
model: claude-haiku-4-5
---

Read `CONTEXT.md`. If missing:
"No active Kudzu project. Run `/kudzu:research` to start one, or `/kudzu:setup` if this is a fresh install."

If $ARGUMENTS is `config`:
Run `kudzu:config` and show the full resolved config with sources.
Exit.

Otherwise show the status dashboard:

```
╔══════════════════════════════════════════╗
║  Kudzu — [PROJECT_NAME]                  ║
║  Phase: [DISCOVER|PLAN|BUILD|COMPLETE]   ║
╚══════════════════════════════════════════╝

Gates
  Gate 1 (research)      [✓ APPROVED | ○ PENDING | — N/A]
  Gate 2 (PRD)           [✓ APPROVED | ○ PENDING | — N/A]
  Gate 3 (architecture)  [✓ APPROVED | ○ PENDING | — N/A]
  Gate 4 (last chunk)    [✓ APPROVED | ○ PENDING | — N/A | ↷ skipped]

Chunks  [X / N complete]
  ✓ chunk-1: [title]
  ✓ chunk-2: [title]
  ⟳ chunk-3: [title]  ← current
  ○ chunk-4: [title]
  ○ chunk-5: [title]  (and N more)

Issues
  Open bugs:       [N] ([N] critical, [N] major)
  Security flags:  [N]
  Deferred:        [N]

Next
  [NEXT_SESSION from CONTEXT.md]
  → /kudzu:[research|plan|implement]
```

If $ARGUMENTS is `full`:
Also show:
- Full CURRENT_STATE system table
- All OPEN_BUGS with file:line and severity
- All SECURITY_FLAGS
- DEFERRED_NOTES
- Recent completed chunks (last 5)

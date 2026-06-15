# INTERFACE_REGISTRY.md
# Maintained by: checkpoint agent (after each chunk)
# Read by: code-reviewer (to detect drift), engineer (to find signatures)
# Last updated: [initialized — no chunks complete yet]

This file tracks the actual implemented signatures of all load-bearing
interfaces (LBI-N from ARCH_DECISIONS.md). It is the source of truth for
what the interfaces look like in code, not what they were specified to look like.

When spec and implementation diverge, this file surfaces the drift.
The code-reviewer uses this to catch interface contract violations across chunks.

---

## How to Read This File

Each entry corresponds to an LBI-N from ARCH_DECISIONS.md.
- Status PENDING: the interface has not been implemented yet
- Status IMPLEMENTED: signature is in code, matches spec
- Status AMENDED: signature drifted from spec — see Drift section
- Status DEPRECATED: interface was removed or replaced

---

## Registry

[No entries yet — populated by checkpoint agent after each chunk that
implements or amends a load-bearing interface]

Example entry format:
```
## LBI-1: [Interface Name]
Defined in: ARCH_DECISIONS.md as LBI-1
Implemented in: `src/path/to/file.ts:45-60`
Status: IMPLEMENTED | AMENDED | PENDING | DEPRECATED
Last modified: chunk-[N]

### Current Signature (as implemented)
typescript
[actual TypeScript signature]


### Spec Signature (from IMPL_SPECS/chunk-N.md)
typescript
[original specified signature]


### Drift
NONE | [description of any difference and why it was acceptable]
[If drift: was this approved by architect? Reference ARCH_REVIEW.md if so]

### Consumers
Chunks that call this interface:
- chunk-[M]: [how it's used]
- chunk-[P]: [how it's used]
```

---

## Chunk History

[Updated by checkpoint after every chunk, even if no LBI changes]
- chunk-[N] completed — [LBI changes: none | LBI-1 implemented | LBI-2 amended]

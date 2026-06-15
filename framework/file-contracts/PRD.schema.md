# file-contracts/PRD.schema.md
# This file defines the required schema for PRD.md
# The project-planner must produce a PRD that matches this schema.
# The architect reads this schema before decomposing — any PRD that
# doesn't satisfy required fields should be sent back to the planner.

---

## Required Fields

Every PRD.md must contain these sections with the specified structure.
Fields marked [REQUIRED] must be non-empty. Fields marked [IF APPLICABLE]
may be omitted only if genuinely not applicable (e.g., no API surface for
a CLI tool), and the section must say "N/A — [reason]" rather than be missing.

---

### Header
```
# PRD: [Project Name]
Version: [N.N]
Status: Draft | Approved
Date: [ISO date]
Gate: [2 = approved | 1 = draft pending gate 2]
```

### Overview [REQUIRED]
2-3 sentences. What this is, who it's for, why it matters now.
Must answer: what does this replace or augment?

### Problem Statement [REQUIRED]
What pain this solves. Concrete, not aspirational.
Must be falsifiable — if you can't describe what "unsolved" looks like,
the problem statement is too vague.

### Goals [REQUIRED]
What success looks like. Measurable where possible.
```
- G1: [goal — measurable or observable]
- G2: [goal]
```

### Non-Goals [REQUIRED]
What this explicitly does not do. Critical for preventing scope creep.
```
- NG1: [exclusion — specific enough to resolve disputes]
```

### Users [REQUIRED]
Who uses this and in what context. For internal tools: which team/role.

### Tech Stack [REQUIRED — structured format]
```
Runtime: [Node 22 | Lambda | Bun | Browser | etc.]
Language: [TypeScript 5.x | etc.]
Framework: [NestJS | Express | none | etc.]
Database: [PostgreSQL via Drizzle | Redis | none | etc.]
Message Bus: [Kafka topics: [list] | BullMQ queues: [list] | none]
External Services: [SpiceDB | OpenTelemetry | GitHub API | etc. — one per line]
Auth: [SpiceDB/Zanzibar | JWT | none | etc.]
Key Libraries: [name@version — one line per lib with reason]
Infrastructure: [AWS Lambda | MemoryDB | SQS | ECS | etc. | none]
Linter/Formatter: [ESLint + Prettier | Biome | etc.]
Test Runner: [Vitest | Jest | Playwright | none]
```

### Functional Requirements [REQUIRED]
Numbered. Each must be independently testable.
An FR that cannot be tested in isolation is not specific enough.
```
- FR1: [requirement — specific, testable, no ambiguity about done state]
- FR2: [requirement]
```

### Non-Functional Requirements [REQUIRED]
Performance, reliability, security, observability.
```
- NFR1: [latency | throughput | availability | error rate target]
- NFR2: [observability: what must be traced/metered]
- NFR3: [security: what surfaces must be secured]
```

### Integration Requirements [IF APPLICABLE]
External systems this touches and exactly how.
```
- IR1: [System name]: [what data flows in which direction] [protocol: REST|gRPC|Kafka|etc.]
```

### API Surface [IF APPLICABLE]
For each endpoint or event:
```
[HTTP METHOD /path | Kafka topic | BullMQ queue name]
  Request: [shape or "N/A"]
  Response: [shape or "N/A"]
  Auth: [required | none]
  Notes: [anything non-obvious]
```

### Data Model [IF APPLICABLE]
Key entities and relationships. Prose or simple schema.
For distributed systems: include event schemas if events are part of the contract.

### Security Considerations [REQUIRED]
Known security surface. The Security Analyst will expand on this.
Minimum: list the surfaces that will be touched (auth, secrets, user input, etc.).
If this project has no security surface, write "None — [rationale]".

### Open Questions [IF APPLICABLE]
Anything unresolved that the architect may encounter during decomposition.
```
- OQ1: [question] — owner: [human | architect | researcher] — blocking: [yes | no]
```
Blocking open questions must be resolved before Gate 2 approval.

### Appendix: Research Summary [IF APPLICABLE]
One paragraph referencing RESEARCH_SYNTHESIS.md findings that informed this PRD.
If PRD was written without the discovery phase (e.g., for a well-understood feature),
write "N/A — PRD written from existing knowledge without discovery phase."

---

## Validation Checklist (for architect to run before decomposing)

Before producing CHUNKS.json, verify:
- [ ] All [REQUIRED] fields are non-empty
- [ ] Tech Stack has structured format (not prose)
- [ ] Message Bus section lists specific topic/queue names (not just "Kafka")
- [ ] Every FR can be stated as a test: "given X, when Y, then Z"
- [ ] No FR contains "and" (compound FRs must be split)
- [ ] All blocking Open Questions are resolved or deferred with explicit deferral
- [ ] Security Considerations is not empty

If any check fails: send PRD back to project-planner with specific failure.
Do not decompose an invalid PRD.

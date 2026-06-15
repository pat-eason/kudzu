---
description: >
  Kudzu DISCOVER phase. Researches anything before you build it.
  Detects intent automatically: concept research, bug triage, decision
  evaluation, doc audit, or feature scoping. Spawns pro/con researchers
  in parallel, synthesizes findings, and pauses for your approval before
  writing a PRD. HITL at Gate 1 (research review) and Gate 2 (PRD approval).
argument-hint: "<concept | 'triage: bug description' | 'decide: question' | 'doc audit' | 'feature: name'>"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
model: claude-opus-4-6
---

You are the Kudzu DISCOVER phase orchestrator.
Run the full research pipeline. Surface decisions to the user at the right
moments. Never make gate decisions yourself.

## Session start

**1. Load config:** Run `kudzu:config`. Store resolved config.
Pass PROJECT_LANG, PROJECT_RUNTIME, PROJECT_KEY_LIBS, PROJECT_MESSAGE_BUS,
PROJECT_AUTH to researcher subagents as stack context constraints.

**2. Check project state:** Read `CONTEXT.md` if it exists.
Check GATE_STATUS. If a gate is PENDING, surface it before doing anything else.

**3. Read framework:** Load `@kudzu:project-planner`

## Intent detection from $ARGUMENTS

Detect mode automatically:

| Signal | Mode |
|--------|------|
| `triage:` prefix or description of broken behavior | Bug triage |
| `decide:` or "should I", "compare", "evaluate" | Decision research |
| `doc audit` or "what needs updating" | Doc audit |
| `feature:` or existing project + new capability | Feature scoping |
| Anything else | Full DISCOVER phase |

If $ARGUMENTS is empty: "What are you researching or trying to figure out?"

## Working directory

After detecting intent, determine `KUDZU_DIR` before writing any file.

**Step 1 — Derive type from mode:**

| Mode | Type slug |
|------|-----------|
| Full DISCOVER phase | `greenfield` |
| Bug triage | `triage` |
| Decision research | `decision` |
| Doc audit | `doc-audit` |
| Feature scoping | `feature` |

**Step 2 — Derive topic slug from $ARGUMENTS:**
- Strip mode prefixes (`triage:`, `decide:`, `feature:`)
- Lowercase; replace spaces and non-alphanumeric characters with hyphens
- Collapse consecutive hyphens; strip leading/trailing hyphens
- Truncate to 40 characters
- If $ARGUMENTS is empty or yields an empty slug: use `untitled-<YYYY-MM-DD>`
- Examples:
  - `"triage: login fails after OAuth redirect"` → `login-fails-after-oauth-redirect`
  - `"decide: should we use Kafka or SQS?"` → `should-we-use-kafka-or-sqs`
  - `"feature: user notifications"` → `user-notifications`

**Step 3 — Set and create the directory:**
```
KUDZU_DIR = ".kudzu/<type>/<topic-slug>"
mkdir -p $KUDZU_DIR
```

All file writes in this skill use `$KUDZU_DIR/<FILENAME>` unless stated otherwise.

---

## FULL DISCOVER PHASE

### Step 1: Clarify (max 3 questions)

Before spawning researchers, verify:
- Core problem or goal
- Known constraints (tech stack, timeline, existing systems)
- Out of scope
- Success definition

If $ARGUMENTS already answers these, skip clarification.
Write `$KUDZU_DIR/CONCEPT_BRIEF.md`. Show it. Wait for confirmation — this is a fast
informal check, not a gate.

### Step 2: Spawn researchers in parallel

Use the Task tool to run both simultaneously:

**Researcher Pro** (Opus):
Instructions: `@kudzu:researcher-pro`
Input: `$KUDZU_DIR/CONCEPT_BRIEF.md` + stack context from config
Output: `$KUDZU_DIR/PRO_FINDINGS.md`

**Researcher Con** (Opus):
Instructions: `@kudzu:researcher-con`
Input: `$KUDZU_DIR/CONCEPT_BRIEF.md` + stack context from config
Output: `$KUDZU_DIR/CON_FINDINGS.md`

Tell user: "Researching from two angles in parallel..."

### Step 3: Concept review

Spawn Concept Reviewer (Opus) via Task:
Instructions: `@kudzu:concept-reviewer`
Mode 1 (viability review)
Input: `$KUDZU_DIR/PRO_FINDINGS.md` + `$KUDZU_DIR/CON_FINDINGS.md`
Output: `$KUDZU_DIR/VIABILITY_REPORT.md`

### Step 4: Synthesize

Follow synthesis protocol from project-planner.md Step 3.
Conflict rule: >1 viability tier disagreement = CONTESTED_FINDING for human.
Write `$KUDZU_DIR/RESEARCH_SYNTHESIS.md`.

### Step 5: Gate 1

Present compact summary:

```
## Research Complete ─ Kudzu Gate 1

Recommended: [one sentence]
Confidence: HIGH | MEDIUM | LOW

Agreed findings:
• [finding]
• [finding]

Contested (needs your call):
• [Pro: p0] vs [Con: p3] — [description]

Key risks:
• [risk]
• [risk]

What next?
  [A] Write PRD
  [B] Research again: [specify new focus]
  [C] Different direction: [specify]
  [D] Research only — stop here
```

Write `$KUDZU_DIR/GATE_1_DECISION.md` based on response.
Update `$KUDZU_DIR/CONTEXT.md` GATE_STATUS: Gate 1 APPROVED/PENDING.

### Step 6: Write PRD (if A)

Follow PRD format from project-planner.md Mode 2.
Validate against `${CLAUDE_SKILL_DIR}/../../framework/file-contracts/PRD.schema.md`.

Show PRD with:
```
## PRD Draft — [Project Name]

[Overview, Goals, Non-Goals, Tech Stack, top 5 FRs]

Open questions I couldn't resolve:
• [question] — needs: [human | architect]

Approve this or tell me what to revise.
```

Write `$KUDZU_DIR/GATE_2_DECISION.md`. Update `$KUDZU_DIR/CONTEXT.md` Gate 2 status.

---

## BUG TRIAGE MODE

Auto-gather context without asking:
```bash
git log --oneline -20
git diff HEAD~5..HEAD -- [relevant files if mentioned in $ARGUMENTS]
```
Read error logs or files mentioned in $ARGUMENTS.

Spawn single researcher (pro-bias) focused on triage:
- Root cause hypotheses ranked by likelihood
- Files most likely involved
- Reproduction path
- Suggested fix

Present:
```
## Bug Triage — Kudzu

Most likely: [hypothesis] (confidence: HIGH|MEDIUM|LOW)

Hypotheses:
1. [cause] — [evidence] — verify by: [action]
2. [cause] — [evidence] — verify by: [action]
3. [cause] — [evidence] — verify by: [action]

Next step:
  [A] Investigate #1: [specific command/file]
  [B] Write fix spec → /kudzu:plan
  [C] I'll investigate manually
```

Write `$KUDZU_DIR/TRIAGE_REPORT.md`. No gate — triage is informational.

---

## DECISION RESEARCH MODE

Spawn both researchers on the decision question. No PRD.
Output: `$KUDZU_DIR/RESEARCH_SYNTHESIS.md` with clear recommendation.
Present: recommendation + confidence + top 3 tradeoffs.
Ask: "Want to plan something based on this, or was this the output?"

---

## DOC AUDIT MODE

Read: `$KUDZU_DIR/CONTEXT.md`, recent DELTA.md files, existing README, Notion page IDs from config.
Identify: stale docs, missing docs for new behavior, Linear issues needing updates.
Write `$KUDZU_DIR/DOC_AUDIT.md`.
Ask: "Want me to run `/kudzu:implement docs` to make these changes?"

---

## FEATURE SCOPING MODE

If `$KUDZU_DIR/ARCH_DECISIONS.md` exists: read it first.
Research only the delta — what new decisions does this feature require?
Write `$KUDZU_DIR/FEATURE_BRIEF.md` (mini-PRD).
Ask: "Ready to `/kudzu:plan` this feature?"

---

## After any mode

Update `$KUDZU_DIR/CONTEXT.md`: PHASE, GATE_STATUS, NEXT_SESSION.
Surface any missing config keys at the bottom of the response.

Tell user what to run next:
- PRD approved → "Run `/kudzu:plan` to decompose into implementation chunks"
- Research only → "Saved to `$KUDZU_DIR/RESEARCH_SYNTHESIS.md`"
- Bug triage → "Saved to `$KUDZU_DIR/TRIAGE_REPORT.md`. Run `/kudzu:implement bug: [description]` to fix."

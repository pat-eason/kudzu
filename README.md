# Kudzu

> *Kudzu grows everywhere. So does your workflow.*

An agentic SDLC framework for Claude Code. Three commands cover the full cycle.

```
/kudzu:research   →  research a concept, triage a bug, evaluate a decision
/kudzu:plan       →  decompose an approved PRD into implementation chunks
/kudzu:implement  →  run the build pipeline, chunk by chunk
```

Everything else — subagent orchestration, code review, QA, security analysis,
documentation, Linear updates, PR creation — runs automatically.
You get pulled in at four defined gates where your judgment actually matters.

Named for the vine that covers everything in western NC.

---

## Install

```
/plugin marketplace add denworks/kudzu
/plugin install kudzu@kudzu-marketplace
/kudzu:setup
```

That's it. `/kudzu:setup` walks you through creating the three config files.

---

## Commands

| Command | Description |
|---------|-------------|
| `/kudzu:research [concept]` | Research anything before building it |
| `/kudzu:plan` | Decompose approved PRD into implementation chunks |
| `/kudzu:implement [target]` | Run build pipeline |
| `/kudzu:status [full]` | Current project state |
| `/kudzu:checkpoint [notes]` | Save session state |
| `/kudzu:gate [N] [decision]` | Record a HITL gate decision |
| `/kudzu:setup` | First-run config initialization |

### /kudzu:implement targets

| Target | What it does |
|--------|-------------|
| *(empty)* | Run next pending chunk |
| `chunk-N` | Run specific chunk |
| `all` | Run all remaining chunks automatically |
| `docs` | Documentation-only pass |
| `bug: [description]` | Bug fix mode |
| `tickets` | Sync open issues to Linear |

### /kudzu:research modes

Kudzu detects intent from your input:

| Input | Mode |
|-------|------|
| `/kudzu:research "build a BullMQ observability dashboard"` | Full DISCOVER — researchers + PRD |
| `/kudzu:research "triage: workers dropping jobs silently"` | Bug triage |
| `/kudzu:research "decide: Temporal vs BullMQ for orchestration"` | Decision research |
| `/kudzu:research "doc audit"` | Documentation gap analysis |
| `/kudzu:research "feature: add webhook delivery"` | Feature scoping |

---

## Configuration

Three config layers, merged at every session start by `/kudzu:config`.
Project values override machine, machine overrides global.

### `~/.claude/kudzu/config.global.md` — Your identity and working style
Committed to your personal dotfiles. Same on every machine.

```
ENGINEER_NAME=Pat
ENGINEER_GITHUB=yourhandle
ADVERSARY_STRICTNESS=high
BIAS_TOWARD_INTERFACES=true
SECURITY_AUTO_TRIGGER_PATTERNS=auth,token,credential,secret,permission,role,key,password
```

### `~/.claude/kudzu/config.machine.md` — Machine-specific credentials
**Never committed.** Fill in fresh on each machine.

```
LINEAR_TEAM_ID=          # LP Architecture team ID (on work machine)
LINEAR_ASSIGNEE_DEFAULT= # your Linear user ID
GITHUB_REVIEWERS=        # ntsianos,teammate (on work machine)
NOTION_ENABLED=false
```

### `.claude/kudzu/config.project.md` — Per-project config
Committed with the repo. No secrets. Auto-picked up by teammates.

```
PROJECT_NAME=Kenai
GITHUB_REPO=luxury-presence/kenai
LINEAR_TEAM_ID=          # overrides machine default for this project
PROJECT_KEY_LIBS=bullmq@5,ioredis@5
PROJECT_MESSAGE_BUS=bullmq
PROJECT_AUTH=spicedb
```

---

## HITL gates

You decide at four points. Everywhere else, Kudzu runs automatically.

| Gate | After | You decide |
|------|-------|------------|
| 1 | Research complete | Worth writing a PRD? |
| 2 | PRD drafted | Does this spec capture what I want? |
| 3 | Architecture planned | Will this decomposition produce good code? |
| 4 | Chunk reviewed *(conditional)* | Only on failures, security issues, chunk 1, or load-bearing chunks |

Record decisions with `/kudzu:gate`:
```
/kudzu:gate 3 approved
/kudzu:gate 4 fix_and_retry "null check missing at auth.ts:47"
```

---

## Multi-machine setup (e.g. work laptop)

```bash
# Install on work machine
/plugin marketplace add denworks/kudzu
/plugin install kudzu@kudzu-marketplace
/kudzu:setup

# config.global.md — copy from your dotfiles (same content, all machines)
# config.machine.md — fill in LP-specific values:
#   LINEAR_TEAM_ID = LP Architecture team ID
#   GITHUB_REVIEWERS = ntsianos,jp-handle
#   NOTION_ENABLED = true
```

For each LP project, add project config once:
```bash
cd /path/to/lp-project
# Create project config (if not already committed):
cp ~/.claude/kudzu/  # kudzu:setup handles this
nano .claude/kudzu/config.project.md
git add .claude/kudzu/config.project.md
git commit -m "chore: add Kudzu project config"
```

Teammates who install Kudzu globally pick up the project config automatically
when they clone the repo.

---

## What gets committed where

| File | Where | Committed? |
|------|-------|-----------|
| `~/.claude/kudzu/config.global.md` | Personal dotfiles | ✓ Yes |
| `~/.claude/kudzu/config.machine.md` | Local only | ✗ Never |
| `.claude/kudzu/config.project.md` | Project repo | ✓ Yes |
| `PRD.md`, `ARCH_DECISIONS.md` | Project repo | Recommended |
| `IMPL_SPECS/`, `REVIEW_SPECS/` | Project repo | Recommended |
| `CONTEXT.md` | Project repo | Your call |

---

## Agent team

Kudzu orchestrates 13 specialist agents across four tiers:

| Agent | Model | Role |
|-------|-------|------|
| Project Planner | Opus | Concept → synthesis → PRD |
| Researcher Pro | Opus | Pro-bias research subagent |
| Researcher Con | Opus | Adversarial research subagent |
| Concept Reviewer | Opus | Viability + decomposition review |
| Software Architect | Opus | PRD → chunks + specs (5 modes) |
| Software Engineer | Sonnet | Spec → code |
| Code Reviewer | Sonnet | Review + escalation |
| QA Analyst | Sonnet | Test coverage |
| Security Analyst | Opus | Security + scalability |
| Documentarian | Sonnet | Doc gap analysis |
| Technical Writer | Haiku | Actual writing |
| Project Manager | Sonnet | Linear ownership |
| Checkpoint | Sonnet | State management |

---

## Requirements

- Claude Code ≥ 2.0.0
- Optional: Linear MCP (direct ticket creation)
- Optional: GitHub MCP (direct PR creation)
- Optional: Notion MCP (direct doc updates)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

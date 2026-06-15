---
description: >
  Internal config loader for Kudzu. Merges global, machine, and project
  config layers into a single resolved config. Called automatically by all
  other Kudzu skills at session start. Not typically invoked directly —
  use /kudzu:status to see resolved config.
disable-model-invocation: true
user-invocable: false
allowed-tools: Read, Bash, Glob
model: claude-haiku-4-5
---

You are the config loader for Kudzu.
Read three config layers, merge them, return the resolved result.
You are Haiku — fast and cheap. Run at session start before anything else.

## Config layer locations

Read each file if it exists. Skip silently if missing.

```
Layer 1 — GLOBAL (identity + personality defaults, machine-agnostic):
  ~/.claude/kudzu/config.global.md

Layer 2 — MACHINE (local secrets + context, never committed):
  ~/.claude/kudzu/config.machine.md

Layer 3 — PROJECT (per-project overrides, committed with repo):
  [cwd]/.claude/kudzu/config.project.md
```

## Merge rules

- Project overrides machine, machine overrides global
- Missing keys fall back down the chain
- Unknown keys pass through unchanged
- No layer is required — all three can be absent

## Parsing config files

Config files are markdown. Parse only content inside triple-backtick
blocks labeled `config`. Each line is `KEY=value`. Skip blank lines and
lines starting with `#`.

## Output

Return three fenced blocks:

```config
ENGINEER_NAME=Pat
ENGINEER_GITHUB=pathandle
LINEAR_TEAM_ID=TEAM-123
[all resolved key=value pairs]
```

```config-sources
ENGINEER_NAME=global
LINEAR_TEAM_ID=project
LINEAR_ASSIGNEE_DEFAULT=machine
[key=layer for each resolved key]
```

```config-missing
GITHUB_REPO
NOTION_ARCH_PAGE_ID
[keys with no value in any layer — skills degrade gracefully on these]
```

## Usage pattern for other skills

At the top of every Kudzu skill that needs config:

```
Run the kudzu:config skill. Store the resolved config for this session.
Pass PROJECT_LANG, PROJECT_RUNTIME, PROJECT_KEY_LIBS, PROJECT_MESSAGE_BUS,
PROJECT_AUTH to subagents as stack context.
Surface missing required keys at the end of the first user-visible response,
not as a hard stop.
```

Missing key messaging format:
"⚠ Kudzu: Missing [KEY] — add it to ~/.claude/kudzu/config.machine.md
or [project]/.claude/kudzu/config.project.md"

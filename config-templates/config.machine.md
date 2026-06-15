# config.machine.md
# Denworks SDLC Plugin — Machine Configuration
# Location: ~/.claude/denworks/config.machine.md
#
# This file stays on THIS machine only. Never commit it anywhere.
# It holds credentials and IDs that are specific to this machine
# or this context (LP work machine vs personal machine).
#
# Add ~/.claude/denworks/config.machine.md to your global ~/.gitignore.

```config
# ── LINEAR ────────────────────────────────────────────────────────────
# Your Linear user ID — used for issue assignment defaults.
# Overrides ENGINEER_LINEAR_ID from global config if set here.
LINEAR_ASSIGNEE_DEFAULT=

# Default team ID for this machine's primary context.
# LP work machine: set to LP Architecture team ID
# Personal machine: set to Denworks workspace team ID
LINEAR_TEAM_ID=

# ── GITHUB ────────────────────────────────────────────────────────────
# Default reviewers for this machine's primary context.
# LP work machine: ntsianos,jp-handle
# Personal machine: your handle or leave blank
GITHUB_REVIEWERS=

# Default base branch. Usually main, sometimes develop.
GITHUB_BASE_BRANCH=main

# ── NOTION ────────────────────────────────────────────────────────────
NOTION_ENABLED=false
NOTION_WORKSPACE_ID=

# ── LINEAR LABEL IDs ──────────────────────────────────────────────────
# Linear label names in your workspace. Customize to match your setup.
LINEAR_LABELS_BUG=bug
LINEAR_LABELS_SECURITY=security
LINEAR_LABELS_TECH_DEBT=tech-debt
LINEAR_LABELS_QUESTION=question
LINEAR_LABELS_INFRA=infrastructure
```

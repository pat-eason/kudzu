# config.project.md
# Denworks SDLC Plugin — Project Configuration
# Location: [project-root]/.kudzu/config.project.md
#
# Commit this file with your project. It contains no secrets.
# Values here override global and machine config.
# Copy this template to your project and fill in the project-specific values.

```config
# ── PROJECT IDENTITY ──────────────────────────────────────────────────
PROJECT_NAME=
# One sentence describing this project. Used in Linear project descriptions
# and as context for agents during planning and implementation.
PROJECT_DESCRIPTION=

# ── GITHUB ────────────────────────────────────────────────────────────
# Full repo path: org/repo-name
# Overrides machine default for this project specifically.
GITHUB_REPO=

# Additional reviewers beyond machine defaults (comma-separated).
# These are ADDED to machine GITHUB_REVIEWERS, not replace them.
# e.g. GITHUB_REVIEWERS_PROJECT=domain-expert-handle
GITHUB_REVIEWERS_PROJECT=

# ── LINEAR ────────────────────────────────────────────────────────────
# Team ID for this project. Overrides machine LINEAR_TEAM_ID.
# LP projects: Architecture team ID
# Denworks projects: personal workspace team ID
LINEAR_TEAM_ID=

# Project ID — set after first /plan run creates the Linear project.
# Leave blank initially; checkpoint agent fills this in after project creation.
LINEAR_PROJECT_ID=

# ── NOTION ────────────────────────────────────────────────────────────
# Enable Notion updates for this project (overrides machine default).
NOTION_ENABLED=false

# Per-project Notion page IDs. Find these in the Notion URL.
NOTION_ARCH_PAGE_ID=
NOTION_RUNBOOK_PAGE_ID=
NOTION_API_PAGE_ID=
NOTION_PROJECT_PAGE_ID=

# ── TECH CONTEXT ──────────────────────────────────────────────────────
# Hints that help agents make better decisions without reading all source files.
# The researcher and architect use these to avoid proposing incompatible approaches.

# Primary language and runtime
PROJECT_LANG=TypeScript
PROJECT_RUNTIME=Node 22

# Key libraries already in use (comma-separated name@version)
# e.g. bullmq@5,ioredis@5,@opentelemetry/sdk-node@0.x
PROJECT_KEY_LIBS=

# Message bus in use (kafka | bullmq | sqs | none)
PROJECT_MESSAGE_BUS=none

# Auth system (spicedb | jwt | none | other)
PROJECT_AUTH=none

# ── SECURITY ──────────────────────────────────────────────────────────
# Additional filename patterns that trigger security review for this project.
# These EXTEND the global SECURITY_AUTO_TRIGGER_PATTERNS, not replace them.
# e.g. SECURITY_TRIGGER_PATTERNS_PROJECT=zanzibar,spicedb,policy
SECURITY_TRIGGER_PATTERNS_PROJECT=

# ── CHUNK SIZING OVERRIDE ─────────────────────────────────────────────
# Override global defaults for this project's specific characteristics.
# Distributed systems / interface-heavy work: 150
# Infrastructure / CDK / Terraform: 100 (with SIZING_STRATEGY=resources)
# Leave blank to use global defaults.
MAX_LINES_PER_CHUNK=
SIZING_STRATEGY=

# ── STYLE REFERENCE ───────────────────────────────────────────────────
# Paths to representative files the code reviewer and engineer use
# to match existing conventions. Relative to project root.
STYLE_REF_SERVICE=
STYLE_REF_WORKER=
STYLE_REF_CONSUMER=
```

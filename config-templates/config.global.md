# config.global.md
# Denworks SDLC Plugin — Global Configuration
# Location: ~/.claude/denworks/config.global.md
#
# This file travels with YOU, not with any project.
# Commit it to a personal dotfiles repo. It contains no secrets.
# Values here are overridden by config.machine.md and config.project.md.

```config
# ── IDENTITY ──────────────────────────────────────────────────────────
ENGINEER_NAME=Pat

# Your GitHub username — used for PR reviewer defaults and author fields
ENGINEER_GITHUB=

# Your Linear user ID (not email — find in Linear > Settings > Account)
ENGINEER_LINEAR_ID=

# ── PERSONALITY / WORKING STYLE ───────────────────────────────────────
# These tune how agents behave across all projects.

# Architect produces interface definitions before implementations.
# Recommended true for distributed systems / LP architecture work.
BIAS_TOWARD_INTERFACES=true

# Agents surface uncertainty as BLOCKER.md rather than guessing.
# Recommended true — better to pause than implement the wrong thing.
FAIL_FAST_ON_AMBIGUITY=true

# How aggressively the con researcher challenges assumptions.
# Options: high | medium | low
ADVERSARY_STRICTNESS=high

# CONTEXT.md verbosity. terse = AI-optimized. normal = human-readable.
CHECKPOINT_VERBOSITY=terse

# ── SECURITY DEFAULTS ─────────────────────────────────────────────────
# File path patterns that always trigger the security analyst.
# Applied across all projects. Extend per-project in config.project.md.
SECURITY_AUTO_TRIGGER_PATTERNS=auth,token,credential,secret,permission,role,key,password

# ── CHUNK SIZING DEFAULTS ─────────────────────────────────────────────
MAX_LINES_PER_CHUNK=200
# Options: lines | resources | behavior
SIZING_STRATEGY=lines

# ── NOTIFICATION PREFERENCES ──────────────────────────────────────────
# Whether to show compact summaries or full details at HITL gates.
# Options: compact | full
GATE_SUMMARY_STYLE=compact

# ── DEFAULT TOOL PREFERENCES ──────────────────────────────────────────
# Whether to attempt direct MCP calls (Linear, GitHub, Notion) when
# connected, or always fall back to writing update files for manual paste.
# Options: mcp_when_available | files_only
TOOL_PREFERENCE=mcp_when_available
```

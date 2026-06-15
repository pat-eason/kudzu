---
description: >
  First-run setup for Kudzu. Creates config files, walks you through
  filling in your identity and credentials, and validates the installation.
  Run once after installing the plugin, then again on each new machine.
  Safe to re-run — never overwrites config.machine.md if it already exists.
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Glob
model: claude-sonnet-4-6
---

You are the Kudzu setup wizard. You run once on a new machine or installation.
Your job: ensure all three config layers exist with correct content, and
tell the user exactly what to fill in.

## Step 1: Check what exists

```bash
ls ~/.claude/kudzu/ 2>/dev/null && echo "kudzu config dir exists" || echo "not found"
cat ~/.claude/kudzu/config.global.md 2>/dev/null || echo "MISSING"
cat ~/.claude/kudzu/config.machine.md 2>/dev/null || echo "MISSING"
cat ./.kudzu/config.project.md 2>/dev/null || echo "MISSING"
```

## Step 2: Create missing config files

**Global config** (`~/.claude/kudzu/config.global.md`):
If missing: copy from `${CLAUDE_SKILL_DIR}/../../config-templates/config.global.md`
to `~/.claude/kudzu/config.global.md`.
Create the directory if needed: `mkdir -p ~/.claude/kudzu`

**Machine config** (`~/.claude/kudzu/config.machine.md`):
If missing: copy from `${CLAUDE_SKILL_DIR}/../../config-templates/config.machine.md`
to `~/.claude/kudzu/config.machine.md`.
If it EXISTS: do not touch it. Never overwrite machine config.
Tell the user it already exists and is preserved.

**Project config** (`./.kudzu/config.project.md`):
If missing in current directory: copy from
`${CLAUDE_SKILL_DIR}/../../config-templates/config.project.md`
to `./.kudzu/config.project.md`.
Create directory if needed: `mkdir -p ./.kudzu`

## Step 3: Global gitignore

Check `~/.gitignore` (or `~/.config/git/ignore`) for `config.machine.md`:
```bash
grep -q "config.machine.md" ~/.gitignore 2>/dev/null || \
grep -q "config.machine.md" ~/.config/git/ignore 2>/dev/null
```

If not found, add it:
```bash
echo "" >> ~/.gitignore
echo "# Kudzu SDLC — local machine config (contains credentials)" >> ~/.gitignore
echo ".claude/kudzu/config.machine.md" >> ~/.gitignore
```

Tell the user this was done.

## Step 4: Run config loader

Run the `kudzu:config` skill to validate the current state.
Show the config-missing output so the user knows what to fill in.

## Step 5: Present setup checklist

Show the user exactly what to do next:

```
## Kudzu Setup Complete

✓ Config files created
✓ config.machine.md added to ~/.gitignore

## Fill These In

### Required on every machine:
Edit ~/.claude/kudzu/config.machine.md
  LINEAR_TEAM_ID=          # Linear team ID for this context
                           #   LP work machine: Architecture team ID
                           #   Personal machine: Denworks workspace ID
  LINEAR_ASSIGNEE_DEFAULT= # Your Linear user ID (Settings → Account → ID)
  GITHUB_REVIEWERS=        # Comma-separated GitHub handles for PR review
                           #   LP: ntsianos,teammate-handle
                           #   Personal: your-handle

### Fill in once (your identity — same on all machines):
Edit ~/.claude/kudzu/config.global.md
  ENGINEER_NAME=           # Your name
  ENGINEER_GITHUB=         # Your GitHub username
  ENGINEER_LINEAR_ID=      # Your Linear user ID

### Fill in per project (commit this with the repo):
Edit .kudzu/config.project.md
  PROJECT_NAME=            # e.g. "Kenai"
  GITHUB_REPO=             # e.g. "luxury-presence/kenai"
  LINEAR_TEAM_ID=          # Override if different from machine default
  PROJECT_KEY_LIBS=        # e.g. "bullmq@5,ioredis@5"
  PROJECT_MESSAGE_BUS=     # kafka | bullmq | sqs | none
  PROJECT_AUTH=            # spicedb | jwt | none

## Commit the project config:
  git add .kudzu/config.project.md
  git commit -m "chore: add Kudzu project config"

## Ready to use:
  /kudzu:research "your concept or problem"
```

## LP team sharing note

Tell the user:
"Once you commit config.project.md to an LP repo, any teammate with Kudzu
installed will automatically get project-level config (repo, Linear team,
Notion pages, tech stack) when they clone the repo. They only need to fill
in their own ~/.claude/kudzu/config.machine.md with their personal IDs."

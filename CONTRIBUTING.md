# Contributing to Kudzu

## Structure

```
kudzu/
├── .claude-plugin/
│   ├── plugin.json        ← plugin manifest
│   └── marketplace.json   ← marketplace catalog
├── skills/                ← user-facing commands (auto-discovered)
│   ├── research/SKILL.md  → /kudzu:research
│   ├── plan/SKILL.md      → /kudzu:plan
│   ├── implement/SKILL.md → /kudzu:implement
│   ├── status/SKILL.md    → /kudzu:status
│   ├── checkpoint/SKILL.md→ /kudzu:checkpoint
│   ├── gate/SKILL.md      → /kudzu:gate
│   ├── config/SKILL.md    → /kudzu:config (internal)
│   └── setup/SKILL.md     → /kudzu:setup
├── framework/             ← specialist agent skills (not user-invoked)
│   ├── skills/planning/
│   ├── skills/implementation/
│   ├── skills/review/
│   ├── skills/delivery/
│   ├── file-contracts/
│   ├── hitl/
│   └── templates/
├── config-templates/      ← copied to ~/.claude/kudzu/ on /kudzu:setup
└── .github/
```

## Editing skills

User-facing skills in `skills/` are orchestrators — they coordinate subagents,
not implement logic themselves. Keep them focused on routing and HITL.

Framework skills in `framework/skills/` are specialist agents. Each has a
single job and a defined model. Don't add Opus reasoning to Haiku skills or
vice versa — the model assignments are deliberate.

## Framework file paths in skills

Skills reference framework files with `${CLAUDE_SKILL_DIR}/../../framework/`.
This resolves correctly because:
- Skill at: `skills/research/SKILL.md`
- `${CLAUDE_SKILL_DIR}` = `[plugin-root]/skills/research/`
- `../../framework/` = `[plugin-root]/framework/`

This works both locally and when installed via the plugin marketplace
(where the plugin is cached at `~/.claude/plugins/cache/`).

## Testing locally

```bash
# Add this repo as a local marketplace
cd /path/to/kudzu
/plugin marketplace add .

# Install the plugin
/plugin install kudzu@kudzu-marketplace

# Test
/kudzu:setup
/kudzu:research "test concept"
```

## Versioning

Bump `version` in both `.claude-plugin/plugin.json` and
`.claude-plugin/marketplace.json` on every release.
Add a CHANGELOG.md entry.

## Config templates

`config-templates/` files are copied to `~/.claude/kudzu/` by `/kudzu:setup`.
Keep them well-commented — they're the first thing users see.
Never put secrets or IDs in config templates — they're public.

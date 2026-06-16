# Changelog

All notable changes to Kudzu will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Kudzu uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.1] — 2026-06-16

### Changed
- Downgraded agents that don't need Opus to Sonnet or Haiku: researchers (pro/con),
  concept-reviewer, project-manager, research/plan orchestrators, and Architect Mode 3.
- Eliminated per-chunk SESSION_BRIEF agent spawn (redundant with IMPL_SPECS).
- Collapsed the Documentarian→TechnicalWriter two-agent doc chain into a single Haiku pass.
- Merged REVIEW_SPECS into IMPL_SPECS as a Reviewer Notes section, eliminating a file class.

---

## [1.1.0] — 2026-06-15

### Changed
- Per-project config moved from `.claude/kudzu/config.project.md` to `.kudzu/config.project.md`.
  Run `/kudzu:setup` to migrate, or move the file manually.
- Kudzu runtime artifacts (CONTEXT.md, PRD.md, CHUNKS.json, etc.) now stored under
  `.kudzu/<type>/<topic>/` instead of the project root, keeping the workspace clean.

### Fixed
- CI validation workflow now uses correct shell quoting — all steps previously passed
  by accident due to broken `\${#array[@]}` expansion; config-templates check was the
  only one that visibly failed.

---

## [1.0.0] — 2026-06-14

### Added
- `/kudzu:research` — DISCOVER phase orchestrator with parallel pro/con researchers,
  concept review, Gate 1 synthesis, and PRD writing. Supports concept research,
  bug triage, decision research, doc audit, and feature scoping modes.
- `/kudzu:plan` — PLAN phase orchestrator. Architecture decisions, dependency-ordered
  chunk decomposition, dual IMPL+REVIEW specs per chunk, decomposition review,
  Gate 3 approval, and Linear project setup.
- `/kudzu:implement` — BUILD phase orchestrator. Full per-chunk pipeline: brief,
  engineer, code review, QA, security (conditional), documentation, Linear update,
  checkpoint, git commit. Supports all, docs, bug fix, and ticket sync modes.
- `/kudzu:status` — Project state dashboard (Haiku, fast).
- `/kudzu:checkpoint` — Manual state save to CONTEXT.md + INTERFACE_REGISTRY.md.
- `/kudzu:gate` — HITL gate review and decision recording.
- `/kudzu:config` — Three-layer config loader (global / machine / project).
- `/kudzu:setup` — First-run setup wizard. Creates config files, gitignore entries.
- Three-layer config system: `~/.claude/kudzu/config.global.md` (identity),
  `~/.claude/kudzu/config.machine.md` (credentials), `.kudzu/config.project.md` (project).
- Full framework of 13 specialist agent skills (planning, implementation, review, delivery).
- HITL gate system with 4 defined gates and structured decision files.
- INTERFACE_REGISTRY.md for cross-chunk interface drift detection.
- PRD.schema.md with structured validation checklist.
- Architect MODE 4 (security escalation) and MODE 5 (blocker resolution).
- Security auto-trigger pattern matching from config.
- ENVIRONMENT_BLOCKED state for QA when test infrastructure is missing.
- Chunk state machine (IN_PROGRESS → UNDER_REVIEW → APPROVED | BLOCKED | PENDING_GATE).
- CONTEXT.md compression trigger at 300 lines.

## [1.0.1] — 2026-06-15

### Fixed
- `homepage` and `repository` in plugin.json and marketplace.json now point to
  `https://github.com/pat-eason/kudzu` (was `denworks/kudzu`)
- `author.email` corrected to `patrick@pateason.io` (was `pat@denworks.io`)
- Removed `name:` field from all SKILL.md frontmatter — skills now correctly
  register as `/kudzu:research`, `/kudzu:plan`, `/kudzu:implement`, etc. instead
  of the unnamespaced `/research`, `/plan`, `/implement`
- Moved all 13 specialist agents from `framework/skills/` to `agents/` directory
  at the plugin root so they are visible and invocable after install
- Updated all orchestrator skills to invoke agents via `@kudzu:agent-name` instead
  of reading framework file paths directly

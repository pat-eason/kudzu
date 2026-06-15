# Changelog

All notable changes to Kudzu will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Kudzu uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
  `~/.claude/kudzu/config.machine.md` (credentials), `.claude/kudzu/config.project.md` (project).
- Full framework of 13 specialist agent skills (planning, implementation, review, delivery).
- HITL gate system with 4 defined gates and structured decision files.
- INTERFACE_REGISTRY.md for cross-chunk interface drift detection.
- PRD.schema.md with structured validation checklist.
- Architect MODE 4 (security escalation) and MODE 5 (blocker resolution).
- Security auto-trigger pattern matching from config.
- ENVIRONMENT_BLOCKED state for QA when test infrastructure is missing.
- Chunk state machine (IN_PROGRESS → UNDER_REVIEW → APPROVED | BLOCKED | PENDING_GATE).
- CONTEXT.md compression trigger at 300 lines.

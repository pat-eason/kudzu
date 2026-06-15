# Changesets

This directory contains pending changesets — small markdown files that describe
changes and the version bump they require.

## Adding a changeset

Create a file named `your-change-description.md` in this directory:

```markdown
---
"kudzu": minor
---

Brief description of the change (used verbatim in CHANGELOG.md).
```

**Bump types:**
- `patch` — bug fixes, doc updates, internal cleanup
- `minor` — new features, non-breaking changes
- `major` — breaking changes

## How release works

When a changeset file is merged to `main`, the Release workflow automatically
opens a "Version Packages" PR that:

1. Reads all pending changeset files
2. Computes the highest bump type across all changesets
3. Updates the version in `plugin.json` and `marketplace.json`
4. Prepends the changeset descriptions to `CHANGELOG.md`
5. Deletes the consumed changeset files

Merge the Version Packages PR to release the new version.

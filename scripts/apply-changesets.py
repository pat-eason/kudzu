#!/usr/bin/env python3
"""
Reads all pending .changeset/*.md files, computes the highest version bump,
updates plugin.json + marketplace.json + CHANGELOG.md, deletes consumed
changeset files, and writes .changeset-result.json for the CI workflow to read.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

CHANGESET_DIR = Path(".changeset")
PLUGIN_JSON = Path(".claude-plugin/plugin.json")
MARKET_JSON = Path(".claude-plugin/marketplace.json")
CHANGELOG = Path("CHANGELOG.md")
RESULT_FILE = Path(".changeset-result.json")

SKIP = {"README.md", "config.json"}
BUMP_RANK = {"patch": 0, "minor": 1, "major": 2}


def parse_changeset(path: Path):
    content = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        print(f"Warning: could not parse {path}, skipping", file=sys.stderr)
        return None, None
    frontmatter, body = match.group(1), match.group(2).strip()
    bump = "patch"
    for line in frontmatter.splitlines():
        if '"kudzu"' in line:
            candidate = line.split(":", 1)[1].strip().strip('"')
            if candidate in BUMP_RANK:
                bump = candidate
    return bump, body


def bump_version(current: str, bump: str) -> str:
    major, minor, patch = map(int, current.split("."))
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def main():
    pending = [p for p in CHANGESET_DIR.glob("*.md") if p.name not in SKIP]
    if not pending:
        print("No pending changesets found.")
        RESULT_FILE.write_text(json.dumps({"skipped": True}))
        sys.exit(0)

    highest_bump = "patch"
    bodies = []
    for path in sorted(pending):
        bump, body = parse_changeset(path)
        if bump is None:
            continue
        if BUMP_RANK[bump] > BUMP_RANK[highest_bump]:
            highest_bump = bump
        if body:
            bodies.append(body)

    with open(PLUGIN_JSON) as f:
        plugin = json.load(f)
    current = plugin["version"]
    new_version = bump_version(current, highest_bump)

    plugin["version"] = new_version
    with open(PLUGIN_JSON, "w") as f:
        json.dump(plugin, f, indent=2)
        f.write("\n")

    with open(MARKET_JSON) as f:
        market = json.load(f)
    market["plugins"][0]["version"] = new_version
    with open(MARKET_JSON, "w") as f:
        json.dump(market, f, indent=2)
        f.write("\n")

    today = date.today().strftime("%Y-%m-%d")
    body_text = "\n\n".join(bodies)
    entry = f"\n## [{new_version}] — {today}\n\n{body_text}\n\n---\n"

    changelog = CHANGELOG.read_text()
    insert_at = changelog.index("---\n") + 4
    CHANGELOG.write_text(changelog[:insert_at] + entry + changelog[insert_at:])

    for path in pending:
        path.unlink()

    result = {"old_version": current, "new_version": new_version, "bump": highest_bump}
    RESULT_FILE.write_text(json.dumps(result))
    print(f"Bumped {current} → {new_version} ({highest_bump})")


if __name__ == "__main__":
    main()

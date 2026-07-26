#!/usr/bin/env python3
"""Checks that every skill in skills/ is well-formed.

Usage:
    python3 scripts/validate.py

Verifies for each skills/<dir>/SKILL.md:
  - the file exists;
  - it opens with a YAML frontmatter block;
  - `name` is present and equals the directory name;
  - `description` is present and non-empty.

Exits 0 when everything passes, 1 when any skill fails.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
# Only top-level `key: value` pairs matter here; nested YAML is left alone.
FIELD = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    match = FRONTMATTER.match(text)
    if not match:
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = FIELD.match(line)
        if field:
            value = field.group(2).strip()
            # Strip surrounding quotes so `"foo"` and `foo` compare equal.
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            fields[field.group(1)] = value
    return fields


def check(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        return ["missing SKILL.md"]

    fields = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if fields is None:
        return ["no YAML frontmatter block at the top of SKILL.md"]

    name = fields.get("name")
    if not name:
        errors.append("frontmatter has no `name`")
    elif name != skill_dir.name:
        errors.append(f"`name: {name}` does not match directory `{skill_dir.name}`")

    if not fields.get("description"):
        errors.append("frontmatter has no `description` (or it is empty)")

    return errors


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"No skills directory at {SKILLS_DIR}", file=sys.stderr)
        return 1

    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    if not skill_dirs:
        print("No skills found.")
        return 0

    failed = 0
    for skill_dir in skill_dirs:
        errors = check(skill_dir)
        if errors:
            failed += 1
            print(f"FAIL {skill_dir.name}")
            for error in errors:
                print(f"       {error}")
        else:
            print(f"ok   {skill_dir.name}")

    print()
    print(f"{len(skill_dirs) - failed}/{len(skill_dirs)} skills valid.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

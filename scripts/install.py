#!/usr/bin/env python3
"""Copy the complete skill bundle without overwriting an existing skill."""

import argparse
import hashlib
from pathlib import Path
import shutil
import sys


SKILLS = Path(__file__).resolve().parents[1] / "skills"
IGNORED = {"node_modules", "__pycache__", ".DS_Store", ".git"}


def inventory(folder):
    result = {}
    for item in folder.rglob("*"):
        relative = item.relative_to(folder)
        if any(part in IGNORED for part in relative.parts):
            continue
        if item.is_symlink():
            raise ValueError(f"Symbolic link in skill directory: {relative}")
        if item.is_file():
            result[relative.as_posix()] = hashlib.sha256(item.read_bytes()).hexdigest()
    return result


def installation_plan(target):
    if target == SKILLS or SKILLS in target.parents:
        raise ValueError("Choose a target outside this bundle's source skills directory.")
    sources = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    pending, unchanged, conflicts = [], [], []
    for source in sources:
        destination = target / source.name
        if destination.is_symlink():
            conflicts.append(source.name)
        elif not destination.exists():
            pending.append(source)
        elif destination.is_dir() and inventory(source) == inventory(destination):
            unchanged.append(source.name)
        else:
            conflicts.append(source.name)
    if conflicts:
        raise ValueError("Existing directories differ; nothing copied: " + ", ".join(conflicts))
    return pending, unchanged


def install(target, dry_run=False):
    target = target.expanduser().resolve()
    pending, unchanged = installation_plan(target)
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)
        for source in pending:
            shutil.copytree(source, target / source.name, ignore=shutil.ignore_patterns(*IGNORED))
    action = "Would install" if dry_run else "Installed"
    print(f"{action}: {', '.join(p.name for p in pending) or '(none)'}")
    print(f"Unchanged: {', '.join(unchanged) or '(none)'}")
    print("Target:", target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True, help="Skill root, e.g. ../project/.agents/skills")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        install(args.target, args.dry_run)
    except (OSError, ValueError) as error:
        print(f"Installation stopped: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

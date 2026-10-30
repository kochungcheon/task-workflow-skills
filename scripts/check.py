#!/usr/bin/env python3
"""Check portable resources, authored links, and pinned upstream content."""

import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
OWN = ("task-delivery", "task-design-dialogue", "task-maps", "task-evidence", "contracts")


def check_upstream():
    lock = json.loads((ROOT / "dependencies.lock.json").read_text())
    count = 0
    for dep in lock["dependencies"]:
        assert re.fullmatch(r"[0-9a-f]{40}", dep["commit"]), dep["name"]
        for name, expected in dep["upstream_files"].items():
            path = ROOT / "skills" / dep["name"] / name
            assert path.is_file(), f"Missing upstream file: {path.relative_to(ROOT)}"
            assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, f"Changed upstream file: {path.relative_to(ROOT)}"
            count += 1
    return count


def check_links(path):
    content = re.sub(r"```[\s\S]*?```", "", path.read_text())
    if path.suffix == ".html":
        links = re.findall(r'href="([^"]+)"', content)
    else:
        links = re.findall(r"\]\(([^)]+)\)", content)
    for link in links:
        url = urlsplit(link)
        if url.scheme or url.netloc or not url.path:
            continue
        if path.name.endswith(".src.html") and url.path == "kit.css":
            continue
        target = (path.parent / unquote(url.path)).resolve()
        assert target.is_relative_to(ROOT), f"Reference outside bundle: {path.relative_to(ROOT)}"
        assert target.exists(), f"Missing reference: {path.relative_to(ROOT)} -> {link}"


def check_package():
    count = check_upstream()
    authored = [ROOT / "README.md", ROOT / "THIRD_PARTY.md", ROOT / "AGENTS.snippet.md"]
    authored.extend((ROOT / "docs").glob("*.md"))
    authored.extend((ROOT / "docs").glob("*.html"))
    for name in OWN:
        authored.extend((ROOT / "skills" / name).rglob("*.md"))
    for path in authored:
        content = path.read_text()
        assert not re.search(r"/(?:Users|home)/[^/\s]+/|file:///|[A-Z]:\\Users\\", content), f"Host-specific path: {path.relative_to(ROOT)}"
        check_links(path)
    for name in OWN[:4]:
        content = (ROOT / "skills" / name / "SKILL.md").read_text()
        assert content.startswith("---\n"), name
        frontmatter = content.split("---", 2)[1]
        assert re.search(rf"^name: {re.escape(name)}$", frontmatter, re.M), name
        assert re.search(r"^description: .+", frontmatter, re.M), name
    components = ROOT / "skills/contracts/components.md"
    for name in json.loads((ROOT / "dependencies.lock.json").read_text())["dependencies"]:
        assert (components.parent / ".." / name["name"] / "SKILL.md").is_file()
    assert (ROOT / "skills/task-delivery/assets/task.md").is_file()
    assert (ROOT / "skills/visual-explainer/kit/render.mjs").is_file()
    print(f"OK: 4 authored skills, 5 pinned dependencies, {count} upstream file hashes, portable authored references")


if __name__ == "__main__":
    try:
        check_package()
    except (AssertionError, OSError, ValueError) as error:
        print(f"Check failed: {error}", file=sys.stderr)
        sys.exit(1)

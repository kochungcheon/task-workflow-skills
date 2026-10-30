# Package maintenance

This repository packages four authored workflow skills and six pinned public skills.

- Read `skills/contracts/components.md` before changing dependency resolution or call boundaries.
- Preserve the shared-map, one-current-task, real TDD evidence, and joint-E2E confirmation behavior when changing packaging.
- Keep references relative to the containing file. Keep the shared contracts and required skill resources together during installation.
- Treat `dependencies.lock.json` as the source for vendored revisions and file hashes. Preserve upstream files and licenses; document deliberate adaptations in `THIRD_PARTY.md`.
- Validate changes with `python3 scripts/check.py` and `python3 -m unittest discover -s tests -v`. For diagram changes, render the edited `.src.html` with the bundled visual-explainer skill and inspect its result.

Generated project work belongs in the consuming project's `.workflow/` directory.

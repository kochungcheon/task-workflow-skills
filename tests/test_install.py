import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts/install.py"


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / "다른 프로젝트" / ".agents/skills"

    def run_install(self, *extra):
        return subprocess.run([sys.executable, str(INSTALLER), "--target", str(self.target), *extra], cwd=self.temp.name, capture_output=True, text=True)

    def test_complete_bundle_survives_directory_move(self):
        result = self.run_install()
        self.assertEqual(result.returncode, 0, result.stderr)
        moved = Path(self.temp.name) / "moved"
        shutil.move(self.target, moved)
        contract = moved / "task-delivery" / "../contracts/task-workflow-v1.md"
        self.assertTrue(contract.is_file())
        for name in ("task-delivery", "task-design-dialogue", "task-maps", "task-evidence", "to-tickets", "tdd", "codebase-design", "mermaid-diagrams", "visual-explainer", "simple-english"):
            self.assertTrue((moved / name / "SKILL.md").is_file(), name)
        self.assertTrue((moved / "simple-english/references/use-cases.md").is_file())
        self.assertTrue((moved / "simple-english/LICENSE").is_file())
        self.assertTrue((moved / "tdd/tests.md").is_file())
        self.assertTrue((moved / "visual-explainer/kit/render.mjs").is_file())
        self.assertTrue((moved / "visual-explainer/package-lock.json").is_file())
        self.assertTrue((moved / "task-delivery/assets/plan.md").is_file())
        self.assertTrue((moved / "task-delivery/references/hackathon.md").is_file())

    def test_rerun_preserves_same_files_and_runtime(self):
        self.assertEqual(self.run_install().returncode, 0)
        path = self.target / "task-delivery/SKILL.md"
        old = (path.stat().st_mtime_ns, hashlib.sha256(path.read_bytes()).digest())
        runtime = self.target / "visual-explainer/node_modules/installed-marker"
        runtime.parent.mkdir(parents=True)
        runtime.write_text("keep")
        result = self.run_install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(old, (path.stat().st_mtime_ns, hashlib.sha256(path.read_bytes()).digest()))
        self.assertEqual(runtime.read_text(), "keep")

    def test_conflict_stops_before_copying_any_new_skill(self):
        custom = self.target / "task-maps/SKILL.md"
        custom.parent.mkdir(parents=True)
        custom.write_text("user's custom skill")
        result = self.run_install()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(custom.read_text(), "user's custom skill")
        self.assertFalse((self.target / "task-delivery").exists())
        self.assertFalse((self.target / "contracts").exists())

    def test_dry_run_has_no_writes(self):
        self.assertEqual(self.run_install("--dry-run").returncode, 0)
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main()

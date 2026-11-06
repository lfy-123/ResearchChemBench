"""Run with: python3 -m unittest discover -s scripts/results -p 'test_*.py'."""
import json
import os
from pathlib import Path
import socket
import sqlite3
import tempfile
import unittest

import check_eval_status as status


class StatusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.case = self.root / "paper_test_20261020"
        self.run = self.case / "runs/cli_runs/batch_test/autonomous_research-paper_test-arche-test"
        self.run.mkdir(parents=True)
        self.write(self.case / "submission.json", {"status": "running", "agent": "arche",
                  "tasks": [{"paper_id": "paper_test"}]})
        self.write(self.run / "_meta.json", {"status": "running", "paper_id": "paper_test",
                  "run_id": self.run.name, "agent_key": "arche"})

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))

    def identity(self):
        value = Path(f"/proc/{os.getpid()}/stat").read_text()
        return {"pid": os.getpid(), "host": socket.gethostname(),
                "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip(),
                "start_ticks": value[value.rfind(")") + 2:].split()[19]}

    def test_completed_zero_score_outranks_stale_launch(self):
        self.write(self.run / "_meta.json", {"status": "completed", "paper_id": "paper_test"})
        self.write(self.run / "_score.json", {"status": "scored", "score": 0, "score_max": 100})
        row = status.inspect(self.run)
        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["score_status"], "0/100")
        self.assertTrue(row["scored"])

    def test_confirmed_live_process(self):
        self.write(self.case / "launch/evaluator_identity.json", self.identity())
        self.assertEqual(status.inspect(self.run)["status"], "running")

    def test_stale_or_reused_pid_is_not_running(self):
        identity = self.identity()
        identity["start_ticks"] = int(identity["start_ticks"]) + 1
        self.write(self.case / "launch/evaluator_identity.json", identity)
        self.write(self.run / "recovery/controller.lock", {"pid": os.getpid()})
        self.assertEqual(status.inspect(self.run)["status"], "interrupted")

    def test_remote_pid_not_mistaken_for_local_dead(self):
        identity = self.identity()
        identity.update(host="another-server", pid=999999999)
        self.write(self.case / "launch/evaluator_identity.json", identity)
        self.assertEqual(status.inspect(self.run)["status"], "remote_running")

    def test_missing_identity_stays_unknown(self):
        self.assertEqual(status.inspect(self.run)["status"], "unknown")

    def test_explicit_failure(self):
        self.write(self.run / "_meta.json", {"status": "failed", "termination": "process_exit"})
        self.assertEqual(status.inspect(self.run)["status"], "failed")

    def test_resume_does_not_reuse_old_failed_status(self):
        self.write(self.run / "_meta.json", {"status": "failed"})
        self.write(self.case / "submission.json", {"status": "running", "phase": "resume"})
        self.write(self.case / ".runtime/launcher_identity.json", self.identity())
        self.assertEqual(status.inspect(self.run)["status"], "running")

    def test_ledger_is_authoritative_and_read_only(self):
        database = self.run.parent / ".rcb_recovery" / self.run.name / "execution.sqlite3"
        database.parent.mkdir(parents=True)
        with sqlite3.connect(database) as db:
            db.execute("CREATE TABLE records(namespace TEXT, key TEXT, payload TEXT)")
            db.execute("INSERT INTO records VALUES(?,?,?)", ("run", "manifest",
                       json.dumps({"run_state": "completed"})))
        before = database.read_bytes()
        self.assertEqual(status.inspect(self.run)["status"], "completed")
        self.assertEqual(database.read_bytes(), before)

    def test_discovery_ignores_scoring_copies_and_symlink_duplicates(self):
        self.write(self.case / "scoring_revisions/old/_score.json", {"status": "scored"})
        self.write(self.case / "scoring_revisions/old/_meta.json", {"status": "completed"})
        (self.root / "compatibility-link").symlink_to(self.case, target_is_directory=True)
        self.assertEqual(status.discover(self.root), [self.run])

    def test_failure_before_run_creation(self):
        case = self.root / "paper_other"
        self.write(case / "submission.json", {"status": "failed"})
        self.assertIn(case, status.discover(self.root))
        self.assertEqual(status.inspect(case)["status"], "failed")

    def test_scoring_failure_does_not_erase_agent_completion(self):
        self.write(self.run / "_meta.json", {"status": "completed"})
        self.write(self.run / "_scoring_attempt.json", {"status": "suspended_infrastructure"})
        row = status.inspect(self.run)
        self.assertEqual(row["status"], "completed")
        self.assertIn("暂停", row["score_status"])
        self.assertFalse(row["scored"])

    def test_corrupt_json_is_not_silent_success(self):
        (self.run / "_meta.json").write_text("{")
        row = status.inspect(self.run)
        self.assertEqual(row["status"], "unknown")
        self.assertTrue(row["warnings"])


if __name__ == "__main__":
    unittest.main()

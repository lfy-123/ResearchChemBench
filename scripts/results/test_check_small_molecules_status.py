"""Regression checks for latest-only selection and unstarted tasks."""
import json
import os
import socket
from pathlib import Path
import tempfile
import unittest

import check_small_molecules_status as monitor


class LatestStatusTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.paper = "paper_abc123"

    def case(self, timestamp, state, score=None, create_run=True):
        case = self.root / f"{self.paper}_{timestamp}_abcd"
        case.mkdir()
        (case / "submission.json").write_text(json.dumps(
            {"status": state, "tasks": [{"paper_id": self.paper}], "agent": "arche"}))
        if create_run:
            run = case / f"runs/cli_runs/batch_test/autonomous_research-{self.paper}-arche-{timestamp}"
            run.mkdir(parents=True)
            (run / "_meta.json").write_text(json.dumps({"status": state, "paper_id": self.paper}))
            if score is not None:
                (run / "_score.json").write_text(json.dumps(
                    {"status": "scored", "score": score, "score_max": 100}))
        return case

    def test_old_score_and_recent_mtime_cannot_hide_new_failure(self):
        old = self.case("20261026_120000", "completed", 100)
        new = self.case("20261028_120000", "failed")
        os.utime(old, (2000000000, 2000000000))
        row = monitor.latest_result(self.paper, "arche", self.root)
        self.assertEqual(row["case_dir"], str(new))
        self.assertEqual(row["status"], "failed")
        self.assertFalse(row["scored"])

    def test_newest_empty_directory_does_not_show_old_score(self):
        self.case("20261026_120000", "completed", 100)
        new = self.root / f"{self.paper}_20261028_120000_abcd"
        new.mkdir()
        row = monitor.latest_result(self.paper, "arche", self.root)
        self.assertEqual(row["case_dir"], str(new))
        self.assertFalse(row["scored"])
        self.assertEqual(row["status"], "unknown")

    def test_zero_is_a_valid_latest_score(self):
        self.case("20261028_120000", "completed", 0)
        row = monitor.latest_result(self.paper, "arche", self.root)
        self.assertTrue(row["scored"])
        self.assertEqual(row["score_status"], "0/100")

    def test_server_comes_from_the_selected_run(self):
        case = self.case("20261028_120000", "running")
        (case / "test_settings.json").write_text(json.dumps({"host": "lfy-54-cpu-test-99--abc"}))
        row = monitor.latest_result(self.paper, "arche", self.root)
        self.assertEqual(row["host"], "lfy-54-cpu-test-99--abc")
        if socket.gethostname() != row["host"]:
            self.assertEqual(row["status"], "remote_running")

    def test_preflight_failure_before_run_creation(self):
        self.case("20261028_120000", "preflight_failed", create_run=False)
        self.assertEqual(monitor.latest_result(self.paper, "arche", self.root)["status"], "failed")

    def test_all_tasks_and_agents_include_missing_runs(self):
        task = self.root / "tasks" / self.paper / "agent_input/task.md"
        task.parent.mkdir(parents=True)
        task.touch()
        # Backup copies nested in a task are not another benchmark task.
        backup = task.parent.parent / "backup/paper_other/agent_input/task.md"
        backup.parent.mkdir(parents=True)
        backup.touch()
        report = monitor.collect(self.root / "tasks", self.root / "workspaces", ("arche", "codex"))
        self.assertEqual(report["tasks"], 1)
        self.assertEqual(report["entries"], 2)
        self.assertEqual(report["states"], {"not_started": 2})


if __name__ == "__main__":
    unittest.main()

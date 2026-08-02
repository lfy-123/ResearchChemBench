from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from src.core.paths import DEFAULT_BENCHMARK_ROOT


def run_mock_task(
    task_dir: str | Path,
    workspace_root: str | Path,
    *,
    benchmark_root: str | Path | None = None,
) -> dict[str, Any]:
    """Run the benchmark's real mock agent against one staged task package."""

    task_dir = Path(task_dir).resolve()
    workspace_root = Path(workspace_root).resolve()
    benchmark = Path(benchmark_root).resolve() if benchmark_root else DEFAULT_BENCHMARK_ROOT
    root = str(benchmark)
    if root not in sys.path:
        sys.path.insert(0, root)

    import evaluation.run_task as run_task
    import evaluation.utils as utils

    old_run_tasks = run_task.TASKS_DIR
    old_utils_tasks = utils.TASKS_DIR
    run_task.TASKS_DIR = task_dir.parent
    utils.TASKS_DIR = task_dir.parent
    try:
        runner = run_task.TaskRunner(
            task_dir.name,
            agent_key="mock",
            workspace_root=workspace_root,
            live_progress=False,
            progress_console=False,
        )
        meta = runner.run()
        report = runner.workspace / "report" / "report.md"
        if meta.get("status") != "completed":
            raise RuntimeError(f"mock run did not complete: {meta}")
        if not report.is_file():
            raise RuntimeError("mock run did not produce report/report.md")
        if (runner.workspace / "target_study").exists():
            raise RuntimeError("staged hidden ground truth was exposed to the agent workspace")
        return {
            "passed": True,
            "task_id": task_dir.name,
            "run_id": runner.run_id,
            "workspace": str(runner.workspace),
            "status": meta.get("status"),
            "exit_code": meta.get("exit_code"),
            "duration_seconds": meta.get("duration_seconds"),
            "report_bytes": report.stat().st_size,
            "hidden_ground_truth_exposed": False,
            "required_deliverables": meta.get("required_deliverables", []),
            "meta": json.loads(runner.meta_path.read_text(encoding="utf-8")),
        }
    finally:
        run_task.TASKS_DIR = old_run_tasks
        utils.TASKS_DIR = old_utils_tasks

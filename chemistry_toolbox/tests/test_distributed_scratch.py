from __future__ import annotations

import json
import sys
from pathlib import Path

from chemistry_toolbox.mcp.job_supervisor import supervise


def test_distributed_job_supervisor_uses_and_cleans_worker_local_scratch(
    tmp_path: Path, monkeypatch
) -> None:
    scratch_root = tmp_path / "worker-local-scratch"
    job_directory = tmp_path / "job"
    job_directory.mkdir()
    observed_path = job_directory / "observed.json"
    status_path = job_directory / "status.json"
    stdout_path = job_directory / "stdout.log"
    stderr_path = job_directory / "stderr.log"
    monkeypatch.setenv("RCB_DISTRIBUTED_REMOTE_SCRATCH_ROOT", str(scratch_root))
    monkeypatch.setenv("GAUSS_SCRDIR", "/shared/gaussian/scratch")
    child_program = (
        "import json,os,pathlib; "
        "scratch=pathlib.Path(os.environ['GAUSS_SCRDIR']); "
        "scratch.joinpath('used-by-child').write_text('yes'); "
        f"pathlib.Path({str(observed_path)!r}).write_text(json.dumps({{"
        "'gauss_scrdir': str(scratch), "
        "'tmpdir': os.environ['TMPDIR'], "
        "'scratch_exists': scratch.is_dir(), "
        "'isolation': os.environ['RESEARCHCHEM_DISTRIBUTED_SCRATCH_ISOLATION']"
        "}))"
    )
    specification = {
        "job_id": "job_scratch_test",
        "job_type": "native_software",
        "job_directory": str(job_directory),
        "relative_job_directory": "outputs/execution_jobs/job_scratch_test",
        "status_path": str(status_path),
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "relative_stdout_path": "outputs/execution_jobs/job_scratch_test/stdout.log",
        "relative_stderr_path": "outputs/execution_jobs/job_scratch_test/stderr.log",
        "command": [sys.executable, "-c", child_program],
        "resource_limits": {
            "cpu_cores": 1,
            "memory_mb": 1024,
            "gpu_count": 0,
            "walltime_seconds": 30,
        },
        "evaluation_resource_budget": {
            "cpu_cores": 1,
            "memory_mb": 1024,
            "gpu_count": 0,
        },
        "resource_allocation": {},
        "submitted_at": "2026-07-31T00:00:00+00:00",
        "execution_mode": "distributed",
        "compute_worker_id": "compute-test",
    }
    spec_path = job_directory / "spec.json"
    spec_path.write_text(json.dumps(specification), encoding="utf-8")

    assert supervise(spec_path) == 0

    observed = json.loads(observed_path.read_text(encoding="utf-8"))
    scratch = Path(observed["gauss_scrdir"])
    assert observed["scratch_exists"] is True
    assert observed["isolation"] == "worker_local_ephemeral"
    assert Path(observed["tmpdir"]) == scratch.parent
    assert scratch_root in scratch.parents
    assert not scratch.parent.exists()
    status = json.loads(status_path.read_text(encoding="utf-8"))
    assert status["status"] == "success"
    assert status["scratch_isolation"] == "worker_local_ephemeral"

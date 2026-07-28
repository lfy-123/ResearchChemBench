from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

from chemistry_toolbox.mcp.execution_models import (
    JobStatusRequest,
    NativeJobRequest,
)
from chemistry_toolbox.mcp.open_execution import (
    _execution_status_axes,
    get_execution_job,
    submit_native_job,
)
from researchchem_toolbox.models import ResourceLimits


def test_exit_zero_lobster_error_is_not_software_success(tmp_path: Path) -> None:
    (tmp_path / "stdout.log").write_text("ERROR: required VASP files are missing\n", encoding="utf-8")
    (tmp_path / "lobsterout").write_text("ERROR: required VASP files are missing\n", encoding="utf-8")
    status = {
        "job_id": "job_" + "1" * 32,
        "job_type": "native_software",
        "status": "success",
        "metadata": {"software_id": "lobster"},
    }
    axes = _execution_status_axes(tmp_path, status)
    assert axes["process_status"] == "completed"
    assert axes["software_status"] == "failed"
    assert axes["convergence_status"] == "failed"
    assert axes["scientific_validation_status"] == "mechanically_invalid"


@pytest.fixture
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for name in ("code", "outputs", "report", "tool_logs"):
        (tmp_path / name).mkdir()
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    return tmp_path


def test_supervisor_terminates_uncollected_background_processes(
    workspace: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def test_guide(software_id: str, executable: str) -> dict:
        return {
            "software_id": software_id,
            "runtime": "core",
            "resolved_path": sys.executable,
            "input_mode": "arguments",
            "synopsis": "python -c <program>",
        }

    monkeypatch.setattr(
        "chemistry_toolbox.mcp.open_execution.native_command_guide", test_guide
    )
    submitted = submit_native_job(
        NativeJobRequest(
            software_id="openbabel",
            executable="obabel",
            arguments=[
                "-c",
                "import subprocess; subprocess.Popen(['sleep', '30']); print('parent-done')",
            ],
            parent_job_id="job_" + "2" * 32,
            resource_limits=ResourceLimits(memory_mb=512, cpu_cores=1),
        )
    )
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        result = get_execution_job(JobStatusRequest(job_id=submitted["job_id"]))
        if result["terminal"]:
            break
        time.sleep(0.05)
    else:
        raise AssertionError("native test job did not finish")
    assert result["job"]["status"] == "success"
    assert result["job"]["background_process_cleanup"] == (
        "terminated_remaining_process_group"
    )
    assert result["job"]["metadata"]["parent_job_id"] == "job_" + "2" * 32
    assert result["request_status"] == "accepted"
    assert result["process_status"] == "completed"

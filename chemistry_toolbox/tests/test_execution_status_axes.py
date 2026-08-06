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
from chemistry_toolbox.src.models import ResourceLimits


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


@pytest.mark.parametrize(
    ("software_id", "calculation_intent", "stdout", "extra_files"),
    [
        (
            "orca",
            "geometry_optimization",
            "SCF CONVERGED\nORCA TERMINATED NORMALLY\n",
            {},
        ),
        (
            "gaussian",
            "frequency",
            "SCF Done: E(RHF) = -40.0\nNormal termination of Gaussian 16\n",
            {},
        ),
        (
            "vasp",
            "ionic_relaxation",
            "",
            {
                "OUTCAR": (
                    "aborting loop because EDIFF is reached\n"
                    "General timing and accounting informations for this job\n"
                ),
                "vasprun.xml": "<modeling/>\n",
            },
        ),
    ],
)
def test_electronic_convergence_does_not_validate_multistep_tasks(
    tmp_path: Path,
    software_id: str,
    calculation_intent: str,
    stdout: str,
    extra_files: dict[str, str],
) -> None:
    (tmp_path / "stdout.log").write_text(stdout, encoding="utf-8")
    for name, content in extra_files.items():
        (tmp_path / name).write_text(content, encoding="utf-8")
    status = {
        "job_id": "job_" + "3" * 32,
        "job_type": "native_software",
        "status": "success",
        "metadata": {
            "software_id": software_id,
            "calculation_intent": calculation_intent,
        },
    }

    axes = _execution_status_axes(tmp_path, status)

    assert axes["convergence_status"] == "failed"
    assert axes["scientific_validation_status"] == "mechanically_invalid"


def test_transition_state_requires_one_imaginary_frequency(tmp_path: Path) -> None:
    (tmp_path / "stdout.log").write_text(
        "SCF Done: E(RHF) = -40.0\n"
        "Optimization completed\n"
        "NImag=1\n"
        "Normal termination of Gaussian 16\n",
        encoding="utf-8",
    )
    status = {
        "job_id": "job_" + "4" * 32,
        "job_type": "native_software",
        "status": "success",
        "metadata": {
            "software_id": "gaussian",
            "calculation_intent": "transition_state",
        },
    }

    axes = _execution_status_axes(tmp_path, status)

    assert axes["convergence_status"] == "converged"
    assert axes["scientific_validation_status"] == "mechanically_valid"


@pytest.mark.parametrize(
    ("calculation_intent", "result_file"),
    [
        ("protonation", "protonated.xyz"),
        ("deprotonation", "deprotonated.xyz"),
        ("tautomerization", "tautomers.xyz"),
    ],
)
def test_crest_uses_mode_specific_result_file(
    tmp_path: Path, calculation_intent: str, result_file: str
) -> None:
    (tmp_path / "stdout.log").write_text(
        "CREST terminated normally\n", encoding="utf-8"
    )
    (tmp_path / result_file).write_text("1\nresult\nH 0 0 0\n", encoding="utf-8")
    status = {
        "job_id": "job_" + "5" * 32,
        "job_type": "native_software",
        "status": "success",
        "metadata": {
            "software_id": "crest",
            "calculation_intent": calculation_intent,
        },
    }

    axes = _execution_status_axes(tmp_path, status)

    assert axes["convergence_status"] == "converged"
    assert axes["artifact_status"] == "valid"
    assert axes["scientific_validation_status"] == "mechanically_valid"


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

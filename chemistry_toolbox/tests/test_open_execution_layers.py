from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest
import yaml

from chemistry_toolbox.mcp.execution_models import (
    AnalysisJobRequest,
    ArtifactDeclarationRequest,
    JobCollectRequest,
    JobStatusRequest,
    NativeJobRequest,
    SoftwareInspectRequest,
    SoftwareListRequest,
    StagedInput,
    WorkspaceTextReadRequest,
    WorkspaceTextWriteRequest,
)
from chemistry_toolbox.mcp.open_execution import (
    collect_execution_job,
    declare_scientific_artifact,
    get_execution_job,
    read_workspace_text,
    submit_analysis_program,
    submit_native_job,
    validate_native_job,
    write_workspace_text,
)
from chemistry_toolbox.mcp.software_catalog import (
    inspect_software,
    list_software,
    load_native_guides,
    validate_native_guides,
)
from researchchem_toolbox.catalog import backend_specs
from researchchem_toolbox.models import ResourceLimits


def _wait(job_id: str, timeout: float = 10.0) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        value = get_execution_job(JobStatusRequest(job_id=job_id, tail_chars=2000))
        if value["terminal"]:
            return value
        time.sleep(0.05)
    raise AssertionError(f"job did not finish within {timeout} seconds: {job_id}")


@pytest.fixture
def chemistry_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for name in ("code", "outputs", "report", "tool_logs"):
        (tmp_path / name).mkdir()
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    return tmp_path


def test_native_guides_exactly_cover_backend_executables():
    validate_native_guides()
    guides = load_native_guides()["software"]
    executable_specs = {
        backend_id: set(specification.executables)
        for backend_id, specification in backend_specs().items()
        if specification.executables
    }
    assert set(executable_specs) <= set(guides)
    for backend_id, executables in executable_specs.items():
        assert set(guides[backend_id]["commands"]) == executables
    assert guides["amber_pmemd"]["commands"]["mpirun"]["enabled"] is False
    assert guides["sharc"]["runtime"] == "sharc"
    assert "verdi" in guides["aiida"]["commands"]


def test_software_inventory_explains_native_and_module_only_access():
    inventory = list_software(SoftwareListRequest())
    assert inventory["status"] == "success"
    assert inventory["count"] >= 40
    assert inventory["next_offset"] is not None
    assert all("native_commands" not in item for item in inventory["software"])
    assert all("analysis_runtimes" not in item for item in inventory["software"])
    assert all("detected_versions" not in item for item in inventory["software"])

    cp2k = inspect_software(SoftwareInspectRequest(software_id="cp2k"))
    assert cp2k["native_invocation_guides"][0]["synopsis"] == (
        "cp2k -i input.inp -o output.out"
    )
    assert cp2k["native_invocation_guides"][0]["native_job_request_template"]

    aiida = inspect_software(SoftwareInspectRequest(software_id="aiida"))
    assert aiida["backend_registered"] is False
    assert any(item["runtime"] == "workflows" for item in aiida["analysis_runtimes"])
    assert aiida["native_invocation_guides"][0]["executable"] == "verdi"
    assert aiida["native_invocation_guides"][0]["available"] is True

    sharc = inspect_software(SoftwareInspectRequest(software_id="sharc"))
    assert sharc["backend_registered"] is False
    assert {item["executable"] for item in sharc["native_invocation_guides"]} == {
        "sharc.x",
        "wfoverlap.x",
    }

    pysisyphus = inspect_software(SoftwareInspectRequest(software_id="pysisyphus"))
    pysis_guide = pysisyphus["native_invocation_guides"][0]
    contract = pysis_guide["configuration_contract"]
    assert contract["tested_version"] == "1.0.0"
    neb = yaml.safe_load(contract["templates"]["two_endpoint_neb"])
    assert neb["geom"]["fn"] == ["reactant.xyz", "product.xyz"]
    assert neb["cos"]["type"] == "neb"
    assert neb["opt"]["type"] == "qm"
    assert "endpoints" not in neb
    assert "images" not in neb["cos"]

    newton_x = validate_native_job(
        NativeJobRequest(software_id="newton_x", executable="nx_geninp")
    )
    assert newton_x["status"] == "success"
    assert newton_x["runtime"] == "newtonx"


def test_workspace_text_tools_are_confined(chemistry_workspace: Path):
    written = write_workspace_text(
        WorkspaceTextWriteRequest(path="code/input.inp", content="test\n")
    )
    assert written["path"] == "code/input.inp"
    loaded = read_workspace_text(WorkspaceTextReadRequest(path="code/input.inp"))
    assert loaded["content"] == "test\n"
    assert loaded["sha256"] == written["sha256"]
    with pytest.raises(ValueError, match="must be under"):
        write_workspace_text(WorkspaceTextWriteRequest(path="input.inp", content="bad"))
    with pytest.raises(ValueError, match="without '..'"):
        StagedInput(source_path="code/input.inp", target_path="../input.inp")
    with pytest.raises(ValueError, match="control path"):
        StagedInput(source_path="code/input.inp", target_path="status.json")
    with pytest.raises(ValueError, match="immutable"):
        write_workspace_text(
            WorkspaceTextWriteRequest(
                path="outputs/execution_jobs/job_fake/status.json",
                content="{}",
            )
        )


def test_programmable_layer_runs_and_collects_auditable_outputs(
    chemistry_workspace: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-reach-agent-program")
    write_workspace_text(
        WorkspaceTextWriteRequest(
            path="code/program.py",
            content=(
                "from pathlib import Path\n"
                "import os\n"
                "assert 'OPENAI_API_KEY' not in os.environ\n"
                "print('program-ok')\n"
                "Path('result.json').write_text('{\\\"energy\\\": -1.25}\\n')\n"
            ),
        )
    )
    submitted = submit_analysis_program(
        AnalysisJobRequest(
            runtime="core",
            script_path="code/program.py",
            resource_limits=ResourceLimits(
                walltime_seconds=30,
                memory_mb=512,
                cpu_cores=1,
                gpu_count=0,
            ),
        )
    )
    assert submitted["status"] == "success"
    finished = _wait(submitted["job_id"])
    assert finished["job"]["status"] == "success"
    assert "program-ok" in finished["stdout_tail"]

    collected = collect_execution_job(
        JobCollectRequest(job_id=submitted["job_id"], tail_chars=0)
    )
    outputs = {item["job_relative_path"]: item for item in collected["outputs"]}
    assert "result.json" in outputs
    assert outputs["result.json"]["sha256"]

    declared = declare_scientific_artifact(
        ArtifactDeclarationRequest(
            path=outputs["result.json"]["path"],
            semantic_type="electronic_energy_record",
            media_type="application/json",
            producer_layer="programmable_analysis",
            producer_id="core:program.py",
        )
    )
    assert declared["artifact"]["semantic_type"] == "electronic_energy_record"
    assert declared["artifact"]["sha256"] == outputs["result.json"]["sha256"]


def test_native_layer_launches_exact_allowlisted_argv(
    chemistry_workspace: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    def test_guide(software_id: str, executable: str) -> dict:
        assert (software_id, executable) == ("openbabel", "obabel")
        return {
            "software_id": software_id,
            "display_name": "test python",
            "runtime": "core",
            "executable": executable,
            "resolved_path": sys.executable,
            "synopsis": "python --version",
            "input_mode": "arguments",
            "required_files": [],
        }

    monkeypatch.setattr(
        "chemistry_toolbox.mcp.open_execution.native_command_guide", test_guide
    )
    submitted = submit_native_job(
        NativeJobRequest(
            software_id="openbabel",
            executable="obabel",
            arguments=["--version"],
            resource_limits=ResourceLimits(walltime_seconds=30, cpu_cores=1),
        )
    )
    assert submitted["command"] == [sys.executable, "--version"]
    finished = _wait(submitted["job_id"])
    assert finished["job"]["status"] == "success"
    assert "Python" in finished["stdout_tail"] or "Python" in finished["stderr_tail"]


def test_programmable_layer_enforces_walltime(chemistry_workspace: Path):
    write_workspace_text(
        WorkspaceTextWriteRequest(
            path="code/sleep.py",
            content="import time\ntime.sleep(10)\n",
        )
    )
    submitted = submit_analysis_program(
        AnalysisJobRequest(
            runtime="core",
            script_path="code/sleep.py",
            resource_limits=ResourceLimits(walltime_seconds=1, cpu_cores=1),
        )
    )
    finished = _wait(submitted["job_id"], timeout=8)
    assert finished["job"]["status"] == "timeout"
    assert finished["job"]["error"]["code"] == "walltime_exceeded"

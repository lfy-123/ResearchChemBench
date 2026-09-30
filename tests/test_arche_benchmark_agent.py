"""ARCHE's isolated Python environment talks to the existing benchmark runner."""
import json
from pathlib import Path

import pytest

from test_agent_plugins import make_runner
from evaluation.execution.recovery import runner_store
from evaluation.provenance.evidence_archive import export_run_archive

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".envs/arche-benchmark/bin/python"
CLIENT = ROOT / "custom_agents/Arche-Harness/benchmark_adapter/tests/fixture_client.py"

SERVER = '''
import sys
from chemistry_toolbox.mcp.server import create_server
from chemistry_toolbox.mcp.open_execution import _start_job
from chemistry_toolbox.mcp.tracing import execute_traced
server = create_server()
server.remove_tool("validate_native_job")
server.remove_tool("submit_native_job")
@server.tool(name="validate_native_job")
def validate(request: dict):
    return {"status":"success", "runtime":"core"}
@server.tool(name="submit_native_job")
def submit(request: dict):
    return execute_traced("submit_native_job", {"request":request}, lambda: _start_job(
        job_type="native_software", runtime="core",
        command=[sys.executable,"-c", "import time; time.sleep("+str(request.get("seconds",0))+"); print(sum(i*i for i in range(1000)))"],
        stdin_target=None, staged_inputs=[], resource_limits={"cpu_cores":1,"memory_mb":128,"gpu_count":0,"walltime_seconds":45},
        metadata={}, submission_key=request["submission_key"]), capture_artifacts=False)
server.run(transport="stdio")
'''


@pytest.mark.parametrize("mode", ["bridge", "cancel", "full", "families"])
def test_arche_benchmark_integration(tmp_path, monkeypatch, mode):
    if not PYTHON.exists():
        pytest.skip("install custom_agents/Arche-Harness/benchmark_adapter/requirements.txt into .envs/arche-benchmark")
    import sys
    server = tmp_path / "fixture_server.py"
    server.write_text(SERVER)
    source = "import os\nos.execv(" + repr(str(PYTHON)) + ", [" + repr(str(PYTHON)) + ", " + repr(str(CLIENT)) + ", '--mode', " + repr(mode) + "] + __import__('sys').argv[1:])"
    runner = make_runner(tmp_path, source, timeout_seconds=180, available_cpu_cores=1, available_memory_mb=512,
                         available_gpu_count=0, job_event_settle_seconds=1, job_event_max_batch_seconds=2,
                         job_wait_heartbeat_seconds=5, job_internal_poll_interval_seconds=1)
    specs = runner._mcp_server_specs()
    specs[0]["command"] = [sys.executable, str(server)]
    monkeypatch.setattr(runner, "_mcp_server_specs", lambda: specs)
    meta = runner.run()
    assert meta["status"] == "completed", (meta, runner.output_path.read_text()[-18000:])
    verified = json.loads((runner.workspace / "outputs/arche/fixture_verified.json").read_text())
    assert verified["jobs"] == (5 if mode == "full" else 2)
    assert all(row["state"] not in {"accepted", "queued", "running"} for row in runner_store(runner).list_jobs())
    if mode != "cancel":
        assert verified["artifacts"] >= verified["jobs"]
    archive = tmp_path / "archive"
    index = export_run_archive(runner.workspace, archive)
    assert index["verification"]["state"] == "complete"
    assert (archive / "workspace/outputs/arche/bridge/identities.json").is_file()
    if mode == "full":
        assert json.loads((archive / "workspace/outputs/arche/full_result.json").read_text())["arche_status"] == "succeeded"
        assert len(json.loads((archive / "workspace/outputs/arche/review_reads.json").read_text())) == 5

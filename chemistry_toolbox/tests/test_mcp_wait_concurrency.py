"""Exercise the actual stdio transport, scheduler and short CPU processes."""
import asyncio
import json
import os
import signal
import sys
import time
import threading
from pathlib import Path

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import types
from mcp.shared.exceptions import McpError

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.mcp.job_manager import JobManager
from chemistry_toolbox.src.recovery_io import signal_identity


SERVER = '''
import sys
from mcp.server.fastmcp import FastMCP
from chemistry_toolbox.mcp.open_tools import register_open_execution_tools
from chemistry_toolbox.mcp.async_action_tools import register_async_action_tools
from chemistry_toolbox.mcp.open_execution import _start_job
server = FastMCP("transport-fixture")
register_open_execution_tools(server)
register_async_action_tools(server)
@server.tool()
def fixture_submit(key: str, seconds: float):
    return _start_job(job_type="native_software", runtime="core",
        command=[sys.executable, "-c", "import time;print(sum(i*i for i in range(20000)),flush=True);time.sleep(" + str(seconds) + ")"],
        stdin_target=None, staged_inputs=[], resource_limits={"cpu_cores":1,"memory_mb":128,"gpu_count":0,"walltime_seconds":30},
        metadata={}, submission_key=key)
server.run(transport="stdio")
'''


async def eventually(predicate, seconds=5):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if predicate():
            return
        await asyncio.sleep(.05)
    raise AssertionError("condition not observed")


@pytest.mark.parametrize("wait_tool", ["wait_execution_jobs", "wait_execution_events"])
def test_wait_does_not_block_control_and_cancellation_keeps_job(tmp_path, wait_tool):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    script = tmp_path / "server.py"
    script.write_text(SERVER)
    env = dict(os.environ)
    env.update({
        "PYTHONPATH": str(Path(__file__).resolve().parents[2]),
        "RESEARCHCHEMBENCH_WORKSPACE": str(workspace), "RESEARCHCHEM_MCP_WORKSPACE": str(workspace),
        "RESEARCHCHEMBENCH_RUN_ID": "transport-test", "RESEARCHCHEMBENCH_RECOVERY_ENABLED": "1",
        "RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES": "1", "RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB": "512",
        "RESEARCHCHEMBENCH_AVAILABLE_GPU_COUNT": "0", "RESEARCHCHEMBENCH_EXECUTION_MODE": "local",
        "RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT": str(tmp_path / "pool"),
        "RESEARCHCHEMBENCH_JOB_WAIT_HEARTBEAT_SECONDS": "3600",
        "RESEARCHCHEMBENCH_JOB_INTERNAL_POLL_INTERVAL_SECONDS": "1",
    })
    env.pop("RESEARCHCHEMBENCH_RUN_DEADLINE", None)
    store = ExecutionStore(workspace, run_id="transport-test")
    events = workspace / "_tool_call_events.jsonl"
    def phases():
        return [json.loads(line) for line in events.read_text().splitlines()] if events.exists() else []

    async def run():
        params = StdioServerParameters(command=sys.executable, args=[str(script)], env=env)
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                async def call(name, args, timeout=5):
                    result = await asyncio.wait_for(session.call_tool(name, args), timeout)
                    assert not result.isError, result
                    return json.loads(result.content[0].text)
                first = await call("fixture_submit", {"key": "first", "seconds": 15})
                if wait_tool == "wait_execution_jobs":
                    request = {"job_ids": [first["job_id"]]}
                else:
                    batch = "batch_" + "a" * 32
                    path = workspace / "outputs/action_batches" / batch
                    path.mkdir(parents=True)
                    (path / "status.json").write_text(json.dumps({
                        "batch_id": batch, "status": "running", "items": [], "events": [], "last_sequence": 0,
                    }))
                    request = {"batch_ids": [batch]}
                wait_request_id = session._request_id
                waiting = asyncio.create_task(session.call_tool(wait_tool, {"request": request}))
                await eventually(lambda: any(e["tool"] == wait_tool and e["phase"] == "started" for e in phases()))
                resources = await call("get_execution_resources", {"request": {}}, timeout=3)
                assert resources["budget"]["cpu_cores"] == 1
                second = await call("fixture_submit", {"key": "second", "seconds": .1}, timeout=3)
                assert second["job_id"] != first["job_id"]
                # This SDK does not send protocol cancellation on Task.cancel().
                await session.send_notification(types.ClientNotification(
                    types.CancelledNotification(params=types.CancelledNotificationParams(
                        requestId=wait_request_id, reason="observer stopped"
                    ))
                ))
                with pytest.raises(McpError, match="cancelled"):
                    await asyncio.wait_for(waiting, 3)
                await eventually(lambda: any(e["tool"] == wait_tool and e["phase"] == "cancelled" for e in phases()))
                original = await call("get_execution_job", {"request": {"job_id": first["job_id"]}})
                assert original["job"]["status"] in {"queued", "launching", "running"}
                await call("cancel_execution_job", {"request": {"job_id": first["job_id"]}}, timeout=3)
                result = await call("wait_execution_jobs", {"request": {"job_ids": [first["job_id"], second["job_id"]]}}, timeout=15)
                assert result["return_reason"] == "all_terminal"
                assert store.get_job(second["job_id"])["state"] == "success"
                output = workspace / "outputs/execution_jobs" / second["job_id"] / "stdout.log"
                assert output.read_text().strip() == str(sum(i*i for i in range(20000)))
    try:
        asyncio.run(run())
    finally:
        manager = JobManager(workspace, run_id="transport-test")
        for row in store.list_jobs():
            manager.cancel_entity(row["entity_id"], row["entity_type"])
        signal_identity(store.get_record("manager", "identity", {}), signal.SIGTERM)


def test_async_wait_cancellation_closes_shared_steps():
    from chemistry_toolbox.mcp.supervision_wait import run_wait_async
    closed = []
    def steps():
        try:
            yield 3600
            raise AssertionError("cancelled wait must not advance again")
        finally:
            closed.append(True)
    async def run():
        task = asyncio.create_task(run_wait_async(steps()))
        await asyncio.sleep(.1)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
    asyncio.run(run())
    assert closed == [True]


def test_native_task_cancellation_during_snapshot_closes_after_finite_step():
    from chemistry_toolbox.mcp.supervision_wait import run_wait_async
    started, release, closed = threading.Event(), threading.Event(), threading.Event()
    def steps():
        try:
            started.set()
            assert release.wait(5)
            yield 3600
            raise AssertionError("cancelled observer advanced again")
        finally:
            closed.set()
    async def run():
        task = asyncio.create_task(run_wait_async(steps()))
        await eventually(started.is_set)
        task.cancel()
        try:
            with pytest.raises(asyncio.CancelledError):
                await task
        finally:
            release.set()
        await eventually(closed.is_set)
    asyncio.run(run())

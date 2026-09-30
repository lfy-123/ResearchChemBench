"""A real external process connects to evaluator-owned MCP and runs a tiny job.

Only the test server's submission tool supplies a deterministic CPU command.
Transport, tracing, resource reservation, wait/collection and finalization use
the production implementations. No model API or chemistry software is needed.
"""

import json
import sys

import pytest

from chemistry_toolbox.src.execution_states import TERMINAL_STATES
from evaluation.execution.recovery import runner_store
from evaluation.provenance.trace import load_tool_trace, process_metrics
from test_agent_plugins import make_runner, WRAPPER


SERVER = '''
import sys
from mcp.server.fastmcp import FastMCP
from chemistry_toolbox.mcp.open_tools import register_open_execution_tools
from chemistry_toolbox.mcp.open_execution import _start_job
from chemistry_toolbox.mcp.tracing import execute_traced
server = FastMCP("external-agent-fixture")
register_open_execution_tools(server)
@server.tool()
def fixture_submit(key: str, seconds: int = 0):
    return execute_traced("submit_native_job", {"request": {"submission_key": key, "label": "tiny-cpu-fixture"}}, lambda: _start_job(
        job_type="native_software", runtime="core",
        command=[sys.executable, "-c", f"import time; time.sleep({seconds}); print(sum(i*i for i in range(1000)))"],
        stdin_target=None, staged_inputs=[],
        resource_limits={"cpu_cores":1,"memory_mb":128,"gpu_count":0,"walltime_seconds":15},
        metadata={}, submission_key=key), capture_artifacts=False)
server.run(transport="stdio")
'''


CLIENT = '''
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_tools():
    config=json.loads(Path(r['tools']['config_file']).read_text())
    s=config['servers'][0]
    env={**s['env'], **{k:os.environ[v] for k,v in s['env_from'].items()}}
    params=StdioServerParameters(command=s['command'], args=s['args'], env=env)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            async def call(name, arguments):
                result=await asyncio.wait_for(session.call_tool(name, arguments), 30)
                assert not result.isError, result
                return json.loads(result.content[0].text)
            resources=await call('get_execution_resources', {'request': {}})
            assert resources['budget']['cpu_cores']==1
            submitted=await call('fixture_submit', {'key': 'researcher:tiny', 'seconds': HOLD_SECONDS})
            assert submitted.get('job_id'), submitted
            (w/'outputs/observed_job.json').write_text(json.dumps(submitted))
            if HOLD_SECONDS:
                return
            result=await call('wait_execution_jobs', {'request': {'job_ids':[submitted['job_id']]}})
            assert result['return_reason']=='all_terminal', result
            validation=await call('validate_output_contract', {'request': {}})
            assert validation['valid'], validation
asyncio.run(use_tools())
'''


TEAM_CLIENT = '''
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_tools():
    config=json.loads(Path(r['tools']['config_file']).read_text())
    s=config['servers'][0]
    env={**s['env'], **{k:os.environ[v] for k,v in s['env_from'].items()}}
    params=StdioServerParameters(command=s['command'], args=s['args'], env=env)
    async with AsyncExitStack() as stack:
        clients=[]
        for role in ('planner', 'researcher'):
            read,write=await stack.enter_async_context(stdio_client(params))
            client=await stack.enter_async_context(ClientSession(read,write))
            await client.initialize()
            clients.append(client)
        async def call(client, name, arguments):
            result=await asyncio.wait_for(client.call_tool(name, arguments),30)
            assert not result.isError, result
            return json.loads(result.content[0].text)
        submitted=await asyncio.gather(*[
            call(client,'fixture_submit',{'key':f'role-{i}:tiny','seconds':2})
            for i,client in enumerate(clients)])
        ids=[item['job_id'] for item in submitted]
        deadline=asyncio.get_running_loop().time()+30
        while True:
            states=await call(clients[0],'list_execution_jobs',{'request':{}})
            budgets=await asyncio.gather(*[call(client,'get_execution_resources',{'request':{}}) for client in clients])
            assert all(b['budget']['cpu_cores']==1 and b['currently_reserved']['cpu_cores']<=1 for b in budgets), budgets
            if all(item['state']=='success' for item in states['jobs'] if item['entity_id'] in ids) and len(states['jobs'])==2:
                break
            assert asyncio.get_running_loop().time()<deadline, states
            await asyncio.sleep(0.1)
        result=await call(clients[1],'wait_execution_jobs',{'request':{'job_ids':ids}})
        assert result['return_reason']=='all_terminal',result
asyncio.run(use_tools())
'''


def mcp_runner(tmp_path, monkeypatch, client):
    server = tmp_path / 'mcp_server.py'
    server.write_text(SERVER)
    runner = make_runner(tmp_path, WRAPPER + client, timeout_seconds=90,
                         available_cpu_cores=1, available_memory_mb=512, available_gpu_count=0,
                         job_event_settle_seconds=1, job_event_max_batch_seconds=2,
                         job_wait_heartbeat_seconds=5, job_internal_poll_interval_seconds=1)
    specs = runner._mcp_server_specs()
    specs[0]['command'] = [sys.executable, str(server)]
    monkeypatch.setattr(runner, '_mcp_server_specs', lambda: specs)
    return runner


@pytest.mark.parametrize('leave_active', [False, True])
def test_external_process_uses_exported_mcp_config(tmp_path, monkeypatch, leave_active):
    client = CLIENT.replace('HOLD_SECONDS', '10' if leave_active else '0')
    runner = mcp_runner(tmp_path, monkeypatch, client)
    meta = runner.run()
    store = runner_store(runner)
    assert len(store.list_jobs()) == 1, (meta, runner.output_path.read_text())
    assert all(row['state'] in TERMINAL_STATES for row in store.list_jobs())
    assert meta['background_job_cleanup']['final_reconciliation']['summary']['active'] == 0
    if leave_active:
        assert meta['status'] == 'failed' and meta['exit_code'] == 0, meta
        assert meta['active_jobs_at_finalize']
        return
    assert meta['status'] == 'completed', (meta, runner.output_path.read_text())
    trace = load_tool_trace(runner.workspace)
    assert {'submit_native_job', 'wait_execution_jobs', 'validate_output_contract'} <= {e['tool'] for e in trace}
    metrics = process_metrics(trace, workspace=runner.workspace)
    assert metrics['successful_execution_job_count'] == 1
    submitted = json.loads((runner.workspace / 'outputs/observed_job.json').read_text())
    output = runner.workspace / 'outputs/execution_jobs' / submitted['job_id'] / 'stdout.log'
    assert output.read_text().strip() == str(sum(i*i for i in range(1000)))


def test_two_mcp_clients_share_managed_queue(tmp_path, monkeypatch):
    from datetime import datetime
    runner = mcp_runner(tmp_path, monkeypatch, TEAM_CLIENT)
    meta = runner.run()
    assert meta['status'] == 'completed', (meta, runner.output_path.read_text())
    assert len(runner_store(runner).list_jobs()) == 2
    assert meta['execution_submission_audit']['accepted_submission_count'] == 2
    assert meta['execution_submission_audit']['active_submission_count'] == 0
    records = [json.loads(path.read_text()) for path in
               (runner.workspace / 'outputs/execution_jobs').glob('*/status.json')]
    records.sort(key=lambda row: row['started_at'])
    assert datetime.fromisoformat(records[0]['finished_at']) <= datetime.fromisoformat(records[1]['started_at'])

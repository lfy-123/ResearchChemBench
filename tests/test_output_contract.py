import asyncio
import hashlib
import json
import os
import shutil
import signal
import sys
from pathlib import Path

import pytest

from chemistry_toolbox.src.output_contract import validate_output_contract, validate_workspace_output_contract
from chemistry_toolbox.src.recovery_io import process_identity
from chemistry_toolbox.mcp.execution_models import OutputContractValidationRequest
from chemistry_toolbox.mcp.open_tools import validate_output_contract as tool_validate
from evaluation.execution.output_contract import validate_submission
from evaluation.execution.recovery import runner_store
from evaluation.execution.runner import TaskRunner
from test_task_package_v19 import package, refresh_manifest


def contract(schema):
    return json.dumps({"required_files":["report/result.json"], "primary_result_file":"report/result.json",
                       "result_schema":schema}).encode()


@pytest.mark.parametrize(("schema", "document", "error_path"), [
    ({"type":"object","required":["score"],"properties":{"score":{"type":"number"}}}, {"score":"wrong"}, "/score"),
    ({"type":"array","items":{"type":"object","required":["label"]}}, [{"value":4}], "/0"),
    ({"$defs":{"datum":{"type":"integer"}},"type":"object","properties":{"data":{"$ref":"#/$defs/datum"}}}, {"data":None}, "/data"),
])
def test_different_schemas_locate_errors_without_modifying_outputs(tmp_path, schema, document, error_path):
    (tmp_path/"report").mkdir()
    result = tmp_path/"report/result.json"
    result.write_text(json.dumps(document))
    payload = contract(schema)
    (tmp_path/"submission_schema.json").write_bytes(payload)
    before = {str(p):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    outcome = validate_workspace_output_contract(tmp_path)
    assert not outcome['valid']
    assert outcome['contract_sha256'] == hashlib.sha256(payload).hexdigest()
    assert any(e.get('instance_path') == error_path for e in outcome['errors'])
    assert before == {str(p):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}


def test_schema_failure_branch_is_valid_without_invented_numbers(tmp_path):
    schema = {"oneOf":[
        {"type":"object","properties":{"status":{"const":"ok"},"value":{"type":"number"}},"required":["status","value"]},
        {"type":"object","properties":{"status":{"const":"incomplete"},"reason":{"type":"string"}},"required":["status","reason"]},
    ]}
    (tmp_path/"report").mkdir()
    path = tmp_path/"report/result.json"
    path.write_text('{"status":"incomplete","reason":"No converged evidence"}')
    assert validate_output_contract(tmp_path, contract(schema))['valid']
    path.write_text('{"status":"ok"}')
    outcome = validate_output_contract(tmp_path, contract(schema), max_errors=2)
    assert not outcome['valid'] and outcome['errors_truncated']
    assert len(outcome['errors']) == 2


@pytest.mark.parametrize("payload", ['{"a":NaN}', '{"a":1e999}', '{invalid json'])
def test_json_syntax_and_nonfinite_values_fail(tmp_path, payload):
    (tmp_path/'report').mkdir()
    (tmp_path/'report/result.json').write_text(payload)
    assert not validate_output_contract(tmp_path, contract({}))['valid']


def test_paths_and_external_schema_references_never_read_hidden_files(tmp_path):
    (tmp_path/'report').mkdir()
    (tmp_path/'report/result.json').write_text('{}')
    outcome = validate_output_contract(tmp_path, contract({'$ref':'https://example.invalid/hidden.json'}))
    assert outcome['errors'][0]['code'] == 'unsupported_contract_reference'
    outcome = validate_output_contract(tmp_path, json.dumps({'required_files':['../outside']} ).encode())
    assert outcome['errors'][0]['code'] == 'invalid_output_path'
    (tmp_path/'report/symlink').symlink_to(tmp_path/'report/result.json')
    outcome = validate_output_contract(tmp_path, json.dumps({'required_files':['report/symlink']} ).encode())
    assert not outcome['valid']
    outcome = validate_output_contract(tmp_path, contract({'$ref':'#/$defs/missing'}))
    assert not outcome['valid']


def test_public_tool_reuses_validator_and_rejects_schema_override(tmp_path, monkeypatch):
    monkeypatch.setenv('RESEARCHCHEM_MCP_WORKSPACE', str(tmp_path))
    (tmp_path/'submission_schema.json').write_bytes(contract({'type':'object'}))
    assert tool_validate(OutputContractValidationRequest()) == validate_workspace_output_contract(tmp_path)
    with pytest.raises(ValueError):
        OutputContractValidationRequest(schema={})


def stop_manager(runner):
    store = runner_store(runner)
    identity = store.get_record('manager', 'identity', {})
    if process_identity(identity.get('pid'), identity)['verified']:
        try:
            os.kill(identity['pid'], signal.SIGTERM)
        except ProcessLookupError:
            pass


@pytest.mark.parametrize('recovery', [False, True])
@pytest.mark.parametrize('valid', [False, True])
def test_both_lifecycles_gate_only_against_public_contract(tmp_path, monkeypatch, recovery, valid):
    task_root = tmp_path/'tasks'
    package(task_root)
    monkeypatch.delenv('RCB_MOCK_DISCONNECT_ONCE', raising=False)
    runner = TaskRunner('paper_fixture', task_type='autonomous_research', agent_key='mock',
                        task_roots=[str(task_root)], workspace_root=tmp_path/'runs', recovery_enabled=recovery,
                        timeout_seconds=60, available_cpu_cores=1, available_memory_mb=512, live_progress=False)
    try:
        runner.setup_workspace()
        (runner.workspace/'report/results.json').write_text('{"barrier":2,"conclusion":"fixture"}' if valid else '{}')
        result = runner.run()
        assert result['status'] == ('completed' if valid else 'failed')
        assert result['submission_validation']['valid'] is valid
        assert result['submission_validation']['contract_source'] == 'frozen_public_contract'
        assert result['execution_submission_audit']['accepted_submission_count'] == 0
    finally:
        stop_manager(runner)


def test_finalizer_uses_frozen_contract_even_if_workspace_schema_is_weakened(tmp_path):
    task_root = tmp_path/'tasks'
    package(task_root)
    runner = TaskRunner('paper_fixture', task_type='autonomous_research', agent_key='mock',
                        task_roots=[str(task_root)], workspace_root=tmp_path/'runs', live_progress=False)
    runner.setup_workspace()
    path = runner.workspace/'submission_schema.json'
    original_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    path.chmod(0o644)
    path.write_text('{}')
    (runner.workspace/'report/results.json').write_text('{}')
    result = validate_submission(runner)
    assert result['contract_sha256'] == original_hash
    assert not result['workspace_contract_matches']
    assert any(e['code'] == 'schema_validation' for e in result['errors'])
    assert any(e['code'] == 'public_contract_modified' for e in result['errors'])


def test_real_short_cpu_job_then_evaluation_finalization(tmp_path, monkeypatch):
    """Real local program, durable job, trace, collection and public schema gate."""
    from chemistry_toolbox.mcp.open_execution import _start_job
    from chemistry_toolbox.mcp.open_tools import wait_execution_jobs
    from chemistry_toolbox.mcp.execution_models import JobWaitRequest
    from chemistry_toolbox.mcp.tracing import execute_traced
    task_root = tmp_path/'tasks'
    root = package(task_root)
    schema_path = root/'agent_input/submission_schema.json'
    schema = json.loads(schema_path.read_text())
    schema['result_schema'] = {'type':'object', 'properties':{'checksum':{'type':'integer'}},'required':['checksum']}
    schema_path.write_text(json.dumps(schema))
    refresh_manifest(root)
    runner = TaskRunner('paper_fixture', task_type='autonomous_research', agent_key='mock', task_roots=[str(task_root)],
                        workspace_root=tmp_path/'runs', recovery_enabled=True, timeout_seconds=60,
                        available_cpu_cores=1, available_memory_mb=512, live_progress=False)
    monkeypatch.delenv('RCB_MOCK_DISCONNECT_ONCE', raising=False)
    try:
        runner.setup_workspace()
        for key, value in runner._mcp_environment().items():
            monkeypatch.setenv(key, str(value))
        monkeypatch.setenv('RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT', str(tmp_path/'pool'))
        monkeypatch.setenv('RESEARCHCHEMBENCH_JOB_INTERNAL_POLL_INTERVAL_SECONDS', '1')
        monkeypatch.setenv('RESEARCHCHEMBENCH_JOB_EVENT_SETTLE_SECONDS', '1')
        code = "import json; from pathlib import Path; Path('outputs/checksum.json').write_text(json.dumps({'checksum':sum(i*i for i in range(20000))}))"
        response = execute_traced('submit_native_job', {'request':{'submission_key':'cpu-fixture'}}, lambda: _start_job(
            job_type='native_software', runtime='core', command=[sys.executable,'-c',code], stdin_target=None,
            staged_inputs=[], resource_limits={'cpu_cores':1,'memory_mb':128,'gpu_count':0,'walltime_seconds':20},
            metadata={}, submission_key='cpu-fixture'), capture_artifacts=False)
        result = asyncio.run(wait_execution_jobs(JobWaitRequest(job_ids=[response['job_id']])))
        assert result['return_reason'] == 'all_terminal'
        source = runner.workspace/'outputs/execution_jobs'/response['job_id']/'outputs/checksum.json'
        assert json.loads(source.read_text())['checksum'] == sum(i*i for i in range(20000))
        shutil.copyfile(source, runner.workspace/'report/results.json')
        final = runner.run()
        assert final['status'] == 'completed'
        assert final['submission_validation']['valid']
        audit = final['execution_submission_audit']
        assert audit['accepted_submission_count'] == audit['terminal_submission_count'] == 1
        assert audit['accepted_submissions'][0]['execution_state'] == 'success'
    finally:
        stop_manager(runner)

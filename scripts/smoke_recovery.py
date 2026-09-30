#!/usr/bin/env python3
"""Short real CPU recovery smoke using public toolbox APIs; no chemistry/API calls."""
from __future__ import annotations
import argparse
import json
import os
import signal
import sys
import tempfile
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path: sys.path.insert(0,str(PROJECT_ROOT))


def wait_for(predicate, timeout=30):
    end = time.monotonic()+timeout
    while time.monotonic()<end:
        value=predicate()
        if value: return value
        time.sleep(.1)
    raise RuntimeError('smoke condition timed out')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path)
    args=parser.parse_args()
    root=args.output_dir.resolve() if args.output_dir else Path(tempfile.mkdtemp(prefix='rcb-recovery-acceptance-'))
    root.mkdir(parents=True,exist_ok=True)
    workspace=root/'workspace'; workspace.mkdir(exist_ok=False)
    for name in ('code','outputs','report','tool_logs'): (workspace/name).mkdir()
    os.environ.update(RESEARCHCHEMBENCH_WORKSPACE=str(workspace),RESEARCHCHEM_MCP_WORKSPACE=str(workspace),
        RESEARCHCHEMBENCH_RUN_ID='cpu_smoke',RESEARCHCHEMBENCH_RECOVERY_ENABLED='1',RESEARCHCHEMBENCH_EXECUTION_MODE='local',
        RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES='1',RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB='512',RESEARCHCHEMBENCH_AVAILABLE_GPU_COUNT='0',
        RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT=str(root/'pool'),RESEARCHCHEMBENCH_COMPUTE_ACTION_TIMEOUT_SECONDS='20')
    os.environ.pop('RESEARCHCHEMBENCH_RUN_DEADLINE',None)
    from chemistry_toolbox.mcp.execution_models import AnalysisJobRequest,JobStatusRequest,JobCollectRequest,WorkspaceTextWriteRequest,ExecutionSubmissionLookupRequest
    from chemistry_toolbox.mcp.open_execution import write_workspace_text,submit_analysis_program,get_execution_job,collect_execution_job,lookup_execution_submission
    from chemistry_toolbox.mcp.execution_store import execution_store
    from chemistry_toolbox.mcp.job_manager import ensure_manager,JobManager
    from chemistry_toolbox.src.recovery_io import process_identity,signal_identity
    program='''import os
import time
from researchchem_job import JobContext
ctx = JobContext.load()
print("started-once", flush=True)
time.sleep(2)
ctx.write_json("result", {"sum_of_squares": sum(i*i for i in range(10000)), "cpu_ids": sorted(os.sched_getaffinity(0))})
'''
    write_workspace_text(WorkspaceTextWriteRequest(path='code/smoke.py',content=program))
    request=AnalysisJobRequest(runtime='core',script_path='code/smoke.py',submission_key='cpu-one',
        outputs=[{'name':'result','path':'outputs/result.json','semantic_type':'benchmark_smoke'}],
        resource_limits={'cpu_cores':1,'memory_mb':128,'gpu_count':0})
    store=execution_store()
    try:
        first=submit_analysis_program(request)
        if 'job_id' not in first: raise RuntimeError(json.dumps(first))
        job=first['job_id']
        wait_for(lambda: json.loads(store.get_job(job)['state_json']).get('child_identity'))
        second=submit_analysis_program(request.model_copy(update={'submission_key':'cpu-two'}))
        assert store.get_job(second['job_id'])['state']=='queued'
        manager_identity=store.get_record('manager','identity')
        assert signal_identity(manager_identity,signal.SIGKILL)
        wait_for(lambda: not process_identity(manager_identity['pid'],manager_identity)['verified'])
        # Retry the same public request after its original reply was "lost".
        replay=submit_analysis_program(request)
        assert replay['job_id']==job and replay['receipt']['receipt_id']==first['receipt']['receipt_id']
        wait_for(lambda: get_execution_job(JobStatusRequest(job_id=second['job_id']))['terminal'])
        assert store.get_job(second['job_id'])['state']=='success'
        collection=collect_execution_job(JobCollectRequest(job_id=job))
        assert collection==collect_execution_job(JobCollectRequest(job_id=job))
        result=json.loads((workspace/'outputs/execution_jobs'/job/'outputs/result.json').read_text())
        assert len(result['cpu_ids'])==1
        assert (workspace/'outputs/execution_jobs'/job/'stdout.log').read_text().count('started-once')==1
        assert lookup_execution_submission(ExecutionSubmissionLookupRequest(submission_key='cpu-one'))['status']=='success'
        summary={'status':'passed','workspace':str(workspace),'store':str(store.path),'job_ids':[job,second['job_id']],
            'manager_restarted':True,'same_submission_receipt':True,'same_result_receipt':True,'queued_job_dispatched':True,
            'launch_count_first_job':1,'real_cpu_result':result,'chemistry_or_model_calls':0}
        (root/'acceptance.json').write_text(json.dumps(summary,indent=2)+'\n')
        print(json.dumps(summary,indent=2))
        return 0
    finally:
        manager=JobManager(workspace,run_id='cpu_smoke')
        for row in store.list_jobs(): manager.cancel_entity(row['entity_id'],row['entity_type'])
        manager.reconcile()
        identity=store.get_record('manager','identity',{})
        signal_identity(identity)


if __name__=='__main__':
    raise SystemExit(main())

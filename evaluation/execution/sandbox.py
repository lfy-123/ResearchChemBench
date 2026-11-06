"""Connect the existing controller to a scoped MCP and an OCI agent process."""
import json
import os
from pathlib import Path
import secrets
import shutil
import signal
import socket
import subprocess
import time
from urllib.request import Request, urlopen
from urllib.error import URLError

from chemistry_toolbox.src.sandbox import Sandbox, agent_environment, software_mounts
from .recovery import runner_store


def prepare(runner):
    if runner.agent.get('kind') == 'mock':
        return
    runner._sandbox_services = []
    runner._mcp_connections = {}
    runner._mcp_token = secrets.token_urlsafe(32)
    directory = runner_store(runner).directory / 'sandbox'
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    runner._sandbox_relays = []
    for index, spec in enumerate(runner._mcp_server_specs()):
        spec = {**spec, 'environment': {**spec['environment'], 'RCB_SANDBOX_CONTROL_ROOT': str(directory.parent)}}
        if runner.agent.get('kind') == 'external':
            from chemistry_toolbox.src.sandbox_stdio import serve
            relay, children = serve(spec, runner._mcp_token, runner.workspace, directory / (spec['name'] + '.log'))
            runner._sandbox_relays.append((relay, children))
            runner._mcp_connections[spec['name']] = {'endpoint': f'127.0.0.1:{relay.server_address[1]}'}
            continue
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            listener.listen()
            port = listener.getsockname()[1]
            endpoint = f'http://127.0.0.1:{port}'
            log = (directory / (spec['name'] + '.log')).open('ab')
            process = subprocess.Popen([*spec['command'], '--transport', 'streamable_http', '--listen-fd', str(listener.fileno())],
                env={**os.environ, **spec['environment'], 'RCB_MCP_AUTH_TOKEN': runner._mcp_token},
                cwd=runner.workspace, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                pass_fds=(listener.fileno(),), start_new_session=True)
            log.close()
        runner._sandbox_services.append(process)
        headers = {'Authorization': 'Bearer ' + runner._mcp_token}
        deadline = time.monotonic() + 180
        while True:
            if runner._stop_requested:
                raise RuntimeError('Agent startup cancelled')
            if process.poll() is not None or time.monotonic() > deadline:
                raise RuntimeError(f'MCP {spec["name"]} did not become ready; see {directory / (spec["name"] + ".log")}')
            try:
                with urlopen(Request(endpoint + '/health', headers=headers), timeout=1) as response:
                    if response.status == 200:
                        break
            except (URLError, TimeoutError, ConnectionError):
                time.sleep(.2)
        runner._mcp_connections[spec['name']] = {'url': endpoint + '/mcp', 'headers': headers}


def launch(runner, argv, env, **kwargs):
    if runner.agent.get('kind') == 'mock':
        return subprocess.Popen(argv, cwd=runner.workspace, env=env, **kwargs)
    mounts = software_mounts()
    for name in ('outputs', 'code', 'report', 'research'):
        (runner.workspace / name).mkdir(exist_ok=True)
    (runner.workspace / 'outputs/execution_jobs').mkdir(exist_ok=True)
    private = {'_meta.json', '_score.json', 'results.json', '_agent_output.jsonl', '_tool_trace.jsonl', '_tool_call_events.jsonl'}
    for path in runner.workspace.iterdir():
        if path.name not in private and not path.name.startswith(('_score', '_scoring')) and not path.is_symlink():
            mounts.append((path, path.name in {'outputs', 'code', 'report', 'research'}))
    mounts.append((runner.workspace / 'outputs/execution_jobs', False))
    for key in ('CODEX_HOME', 'CLAUDE_CONFIG_DIR', 'GEMINI_CLI_HOME'):
        if env.get(key):
            mounts.append((Path(env[key]), True))
    if env.get('OPENCODE_DB'):
        mounts.append((Path(env['OPENCODE_DB']).parent, True))
    executable = Path(shutil.which(argv[0]) or argv[0]).resolve()
    mounts.append((executable, False))
    if runner.agent.get('kind') == 'external':
        mounts.extend((Path(arg), False) for arg in runner.agent['command'][1:] if Path(arg).is_absolute() and Path(arg).is_file())
        mounts.append((Path(env['HOME']), True))
        public_sources = Path(__file__).resolve().parents[2] / 'custom_agents/Arche-Harness'
        if public_sources.is_dir():
            manifest = public_sources / 'benchmark_adapter/source_snapshot.json'
            source_roots = {'src', 'third_party', 'tests'}
            paths = [public_sources / name for name in source_roots]
            paths += [public_sources / name for name in json.loads(manifest.read_text())['files']
                      if Path(name).parts[0] not in source_roots]
            paths += [public_sources / 'benchmark_adapter' / name for name in
                      ('run.py', 'rcb_adapter', 'tests', 'deploy', 'source_snapshot.json')]
            mounts.extend((path, False) for path in paths)
        mounts.append((Path(__file__).with_name('resume_policy.py'), False))
    if runner.agent.get('kind') == 'codex':
        runner.final_message_path.touch()
        mounts.append((runner.final_message_path, True))
    guest_env = dict(env) if runner.agent.get('kind') == 'external' else agent_environment(env, runner.agent.get('kind'))
    guest_env['RCB_MCP_AUTH_TOKEN'] = runner._mcp_token
    guest_env['RESEARCHCHEMBENCH_MODEL_CACHE'] = '/tmp/model-cache'
    for index, connection in enumerate(runner._mcp_connections.values()):
        if 'endpoint' in connection:
            guest_env[f'RCB_MCP_ENDPOINT_{index}'] = connection['endpoint']
    sandbox = Sandbox(runner_store(runner).directory / 'sandbox', argv, cwd=runner.workspace,
                      env=guest_env, mounts=mounts,
                      cpu_ids=sorted(os.sched_getaffinity(0))[:runner.available_cpu_cores])
    runner._agent_sandbox = sandbox
    runner_store(runner).put_record('agent', 'sandbox', {'directory': str(sandbox.directory), 'runtime_id': sandbox.identity})
    runner._write_meta('running', {'agent_isolation': {'runtime': 'gvisor', 'version': 'release-20261102.0',
                                                      'platform': 'systrap', 'runtime_id': sandbox.identity}})
    return subprocess.Popen(sandbox.command(), cwd=runner.workspace, env=env, **kwargs)


def close(runner):
    sandbox = getattr(runner, '_agent_sandbox', None)
    if sandbox:
        sandbox.control('delete', '--force')
        runner._agent_sandbox = None
    for process in getattr(runner, '_sandbox_services', []):
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
    runner._sandbox_services = []
    for relay, children in getattr(runner, '_sandbox_relays', []):
        relay.shutdown(); relay.server_close()
        for child in children:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGTERM)
                child.wait(timeout=5)
    runner._sandbox_relays = []

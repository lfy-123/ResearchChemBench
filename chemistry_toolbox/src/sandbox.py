"""The OCI boundary for evaluated agents and scientific programs (Linux/runsc)."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import time
import uuid

PROJECT = Path(__file__).resolve().parents[2]
RUNSC = PROJECT / '.software_cache/shared/gvisor/release-20261102.0/runsc'
STATE = Path('/tmp') / f'rcb-runsc-{os.getuid()}'
BASE_ENV = ('PATH', 'LANG', 'LC_ALL', 'LC_CTYPE', 'TZ', 'SSL_CERT_FILE', 'SSL_CERT_DIR',
            'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY',
            'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy')


def agent_environment(env, kind):
    prefixes = {'claude': ('ANTHROPIC_', 'CLAUDE_', 'DISABLE_AUTOUPDATER', 'ENABLE_TOOL_SEARCH', 'MCP_TOOL_TIMEOUT'),
                'codex': ('RCB_CODEX_', 'CODEX_'),
                'gemini': ('GEMINI_', 'GOOGLE_', 'NO_BROWSER'),
                'opencode': ('OPENCODE_', 'OPENAI_')}.get(kind, ())
    return {k: v for k, v in env.items() if k in BASE_ENV or k in {'RCB_AGENT_RUN_TOKEN', 'PYTHONUNBUFFERED'}
            or k.startswith(prefixes)}


def software_mounts():
    """Public runtime code and installed software; never the repository root."""
    paths = [PROJECT / 'chemistry_toolbox' / name for name in
             ('__init__.py', 'src', 'mcp', 'config', 'native_software_docs', 'scripts', 'environment')]
    paths += [PROJECT / '.software_cache' / name for name in ('installations', 'shared')]
    environments = list((PROJECT / '.envs').iterdir())
    paths += environments
    for environment in environments:
        python = environment / 'bin/python'
        if python.is_symlink():
            target = Path(os.readlink(python))
            if target.is_absolute():
                paths += [target.parent.parent, python.resolve().parent.parent]
    node = shutil.which('node')
    if node:
        paths.append(Path(node).resolve().parent.parent)
    from chemistry_toolbox.src.runtime import load_runtime_config, resolve_configured_path
    for specification in load_runtime_config()['profiles'].values():
        paths += [resolve_configured_path(p) for p in specification.get('cache_paths', [])]
        paths += [resolve_configured_path(p) for p in specification.get('command_variables', {}).values() if '/' in p]
    return [(p, False) for p in paths if p.exists()]


def calculation(argv, *, runtime, cwd=None, env=None, cpu_ids=(), writable=(), backend_id=None, network=False):
    from chemistry_toolbox.src.runtime import runtime_environment
    from chemistry_toolbox.src.recovery_io import control_directory
    env = env or os.environ
    runtime_values = runtime_environment(runtime)
    from chemistry_toolbox.src.catalog import backend_specs
    backend_keys = set(backend_specs()[backend_id].environment_variables) if backend_id else set()
    keys = set(runtime_values) | set(BASE_ENV) | backend_keys | {'HOME', 'TMPDIR', 'LM_LICENSE_FILE', 'MLM_LICENSE_FILE',
            'GAUSS_SCRDIR', 'GMS_SCRATCH', 'GMS_RESTART', 'MOLCAS_WORKDIR', 'PYTHONNOUSERSITE', 'MPLCONFIGDIR'}
    guest_env = {k: v for k, v in env.items() if k in keys or k.startswith(('RESEARCHCHEM', 'OMP_', 'MKL_',
            'OPENBLAS_', 'NUMEXPR_', 'VECLIB_', 'OMPI_', 'PRTE_', 'CUDA_VISIBLE_', 'ROCR_VISIBLE_'))}
    guest_env.update({k: v for k, v in runtime_values.items() if k not in guest_env})
    guest_env.update(HOME='/tmp', TMPDIR='/tmp', XDG_CACHE_HOME='/tmp/cache',
                     RESEARCHCHEMBENCH_RUNTIME_CACHE='/tmp/cache', PYTHONDONTWRITEBYTECODE='1')
    for key in ('HOME', 'TMPDIR'):
        if env.get(key) and any(Path(env[key]).is_relative_to(Path(root)) for root in writable):
            guest_env[key] = env[key]
    # The guest must not initialize controllers or inherit an MCP capability.
    for key in list(guest_env):
        if key not in backend_keys and any(word in key for word in ('JUDGE', 'API_KEY', 'AUTH_TOKEN', 'RECOVERY_ENABLED')):
            guest_env.pop(key)
    mounts = software_mounts()
    if runtime == 'services':
        rate = Path(env.get('RESEARCHCHEMBENCH_PUBCHEM_RATE_STATE', PROJECT / '.software_cache/state/pubchem/request_rate.state'))
        rate.parent.mkdir(parents=True, exist_ok=True)
        rate.touch(exist_ok=True)
        guest_env['RESEARCHCHEMBENCH_PUBCHEM_RATE_STATE'] = str(rate)
        mounts.append((rate, True))
    if cwd:
        cwd = Path(cwd).resolve()
        mounts.append((cwd, False))
        for path in writable:
            path = Path(path); path.mkdir(parents=True, exist_ok=True)
            mounts.append((path, True))
    model_cache = PROJECT / '.model_cache'
    if model_cache.is_dir():
        mounts.append((model_cache, False))
    workspace = env.get('RESEARCHCHEMBENCH_WORKSPACE') or env.get('RESEARCHCHEM_MCP_WORKSPACE')
    control = control_directory(Path(workspace), env.get('RESEARCHCHEMBENCH_RUN_ID', 'sandbox')) if workspace else STATE / 'probes'
    control = Path(env.get('RCB_SANDBOX_CONTROL_ROOT', control))
    owner = env.get('RCB_JOB_LAUNCH_TOKEN', 'probes')
    return Sandbox(control / 'sandboxes' / owner, argv, cwd=cwd or '/tmp', env=guest_env,
                   mounts=mounts, cpu_ids=cpu_ids, compute=not network and runtime not in {'core', 'services'})


def stop_owned(directory, token):
    if not token:
        return
    for path in (Path(directory) / 'sandboxes' / token).glob('sandbox-*/launch.json'):
        record = json.loads(path.read_text())
        if record['host'] == socket.gethostname():
            sandbox = Sandbox.load(path.parent)
            sandbox.stop(force=True)
            sandbox.control('delete', '--force')


class Sandbox:
    def __init__(self, directory, argv, *, cwd, env, mounts=(), cpu_ids=(), compute=False):
        if not RUNSC.is_file():
            raise RuntimeError('runsc is not installed; run scripts/install_runsc.sh')
        self.directory = Path(directory) / ('sandbox-' + uuid.uuid4().hex)
        self.directory.mkdir(parents=True, mode=0o700)
        (self.directory / 'rootfs').mkdir()
        self.identity = self.directory.name
        self.compute = compute
        bindings = []
        system = ['/usr', '/bin', '/lib', '/lib64', '/etc/ld.so.cache', '/etc/alternatives',
                  '/etc/ssl/certs', '/etc/resolv.conf', '/etc/hosts', '/etc/nsswitch.conf']
        for path, writable in [*((Path(p), False) for p in system), *mounts]:
            path = Path(path).absolute()
            if not path.exists():
                raise FileNotFoundError(path)
            bindings.append({'destination': str(path), 'type': 'bind', 'source': str(path.resolve()),
                             'options': ['rbind', 'rw' if writable else 'ro', 'nosuid', 'nodev']})
        bindings += [{'destination': p, 'type': t, 'source': t, 'options': ['nosuid', 'nodev']}
                     for p, t in [('/proc', 'proc'), ('/sys', 'sysfs'), ('/dev', 'tmpfs'), ('/tmp', 'tmpfs')]]
        # Map application paths after /tmp so temporary workspaces are not hidden.
        bindings.sort(key=lambda m: (len(Path(m['destination']).parts), m['destination']))
        bindings = list({m['destination']: m for m in bindings}.values())
        guest_env = {'PATH': '/usr/sbin:/usr/bin:/bin', 'HOME': '/tmp', 'LANG': 'C.UTF-8',
                     'PYTHONDONTWRITEBYTECODE': '1', **env, 'RCB_INSIDE_SANDBOX': '1'}
        # runsc exposes the allocated host CPUs as guest CPUs 0..N-1.
        guest_cpus = ','.join(map(str, range(len(cpu_ids or os.sched_getaffinity(0)))))
        for key in ('RESEARCHCHEM_WORKER_CPU_IDS', 'OMPI_MCA_hwloc_base_cpu_list', 'PRTE_MCA_hwloc_default_cpu_list'):
            if key in guest_env:
                guest_env[key] = guest_cpus
        spec = {'ociVersion': '1.2.0', 'root': {'path': 'rootfs', 'readonly': True},
                'hostname': 'rcb-sandbox', 'process': {'terminal': False, 'user': {'uid': 0, 'gid': 0},
                'args': list(map(str, argv)), 'env': [f'{k}={v}' for k, v in guest_env.items()],
                'cwd': str(cwd), 'noNewPrivileges': True,
                'capabilities': {k: [] for k in ('bounding', 'effective', 'permitted', 'inheritable', 'ambient')}},
                'mounts': bindings, 'linux': {'namespaces': [{'type': 'user'}],
                'uidMappings': [{'containerID': 0, 'hostID': 0, 'size': 1}],
                'gidMappings': [{'containerID': 0, 'hostID': 0, 'size': 1}]}}
        if compute:
            spec['linux']['namespaces'].append({'type': 'network', 'path': '/proc/self/ns/net'})
        self._write('config.json', spec)
        self._write('launch.json', {'id': self.identity, 'state_root': str(STATE), 'compute': compute,
                                  'cpu_ids': list(cpu_ids) or sorted(os.sched_getaffinity(0)),
                                  'owner_token': os.environ.get('RCB_JOB_LAUNCH_TOKEN', ''), 'host': socket.gethostname()})

    def _write(self, name, value):
        path = self.directory / name
        temporary = path.with_name(name + '.' + uuid.uuid4().hex + '.tmp')
        temporary.write_text(json.dumps(value) + '\n')
        temporary.chmod(0o600)
        os.replace(temporary, path)

    @classmethod
    def load(cls, directory):
        value = cls.__new__(cls)
        value.directory = Path(directory)
        record = json.loads((value.directory / 'launch.json').read_text())
        value.identity, value.compute = record['id'], record['compute']
        return value

    def command(self):
        return [sys.executable, str(Path(__file__).resolve()), str(self.directory)]

    def control(self, command, *options):
        record = json.loads((self.directory / 'launch.json').read_text())
        args = [command, *options, self.identity] if command != 'kill' else [command, '--all', self.identity, *options]
        return subprocess.run(['unshare', '--user', '--map-root-user', '--mount', '--fork', str(RUNSC),
                               '--root=' + record['state_root'], *args],
                              capture_output=True, text=True, timeout=15)

    def stop(self, force=False):
        self._write('cancel.json', {'force': force})
        return self.control('kill', 'KILL' if force else 'TERM')

    def memory_usage(self):
        result = self.control('events', '--stats')
        return json.loads(result.stdout)['data']['memory']['usage']['usage'] if result.returncode == 0 else None

    def run(self, **kwargs):
        """subprocess.run with cancellation of all guest descendants on timeout."""
        data, timeout = kwargs.pop('input', None), kwargs.pop('timeout', None)
        if data is not None:
            kwargs['stdin'] = subprocess.PIPE
        kwargs.setdefault('stdin', subprocess.DEVNULL)
        if kwargs.pop('capture_output', False):
            kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        check = kwargs.pop('check', False)
        child = subprocess.Popen(self.command(), **kwargs)
        try:
            out, err = child.communicate(data, timeout=timeout)
            result = subprocess.CompletedProcess(self.command(), child.returncode, out, err)
            if check:
                result.check_returncode()
            return result
        except BaseException:
            self.stop(force=True)
            child.wait(timeout=20)
            raise
        finally:
            self.control('delete', '--force')


def main(directory):
    sandbox = Sandbox.load(directory)
    launch = json.loads((sandbox.directory / 'launch.json').read_text())
    STATE.mkdir(mode=0o700, exist_ok=True)
    stopped = False
    def stop(signum, frame):
        nonlocal stopped
        stopped = True
        sandbox.stop()
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    prefix = ['unshare', '--user', '--map-root-user', '--mount', '--fork']
    runtime = [str(RUNSC), '--root=' + launch['state_root'], '--platform=systrap',
               '--network=' + ('sandbox' if sandbox.compute else 'host'), '--ignore-cgroups=true',
               'run', '--bundle=' + str(sandbox.directory), sandbox.identity]
    if sandbox.compute:
        setup = 'set -e\nip link set lo up\nip link add rcb0 type dummy\nip addr add 192.0.2.1/24 dev rcb0\nip link set rcb0 up\nexec "$@"'
        prefix += ['--net', '/bin/sh', '-c', setup, 'rcb']
    host_env = {k: os.environ[k] for k in BASE_ENV if k in os.environ}
    host_env.update({k: os.environ[k] for k in ('RCB_JOB_LAUNCH_TOKEN', 'RCB_AGENT_RUN_TOKEN') if k in os.environ})
    host_env['PATH'] = '/usr/sbin:/usr/bin:/bin'
    child = subprocess.Popen(['taskset', '-c', ','.join(map(str, launch['cpu_ids'])), *prefix, *runtime], env=host_env)
    try:
        registered = False
        stopping_at = None
        while child.poll() is None:
            if not registered:
                state = sandbox.control('state')
                if state.returncode == 0:
                    sandbox._write('state.json', json.loads(state.stdout))
                    registered = True
            cancel_path = sandbox.directory / 'cancel.json'
            if stopped or cancel_path.exists():
                stopping_at = stopping_at or time.monotonic()
                force = json.loads(cancel_path.read_text()).get('force') if cancel_path.exists() else False
                sandbox.control('kill', 'KILL' if force or time.monotonic() - stopping_at > 5 else 'TERM')
            time.sleep(.1)
        return child.returncode
    finally:
        sandbox.control('delete', '--force')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))

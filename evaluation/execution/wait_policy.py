"""Local executable diagnostics and the verified Codex host-wait contract."""
import re
import shutil
import socket
from pathlib import Path
import subprocess

from .provider_errors import redact


class ProviderPreflightError(ValueError):
    def __init__(self, reason, diagnostics):
        self.diagnostics = {**diagnostics, "failure_reason": reason}
        super().__init__(reason)


def probe_cli(executable):
    resolved = shutil.which(executable)
    diagnostic = {"requested_executable": executable, "resolved_executable": resolved,
                  "symlink_target": str(Path(resolved).resolve()) if resolved else None, "host": socket.gethostname(), "stdout": "", "stderr": "", "returncode": None,
                  "api_verified": False}
    if not resolved:
        raise ProviderPreflightError("provider_executable_missing", diagnostic)
    try:
        result = subprocess.run([resolved, "--version"], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired as exc:
        for name in ("stdout", "stderr"):
            raw = getattr(exc, name, None) or ""
            diagnostic[name] = redact(raw.decode(errors="replace") if isinstance(raw, bytes) else raw)[:4000]
        raise ProviderPreflightError("provider_version_timeout", diagnostic) from exc
    except OSError as exc:
        diagnostic["stderr"] = redact(exc)
        raise ProviderPreflightError("provider_executable_unavailable", diagnostic) from exc
    diagnostic.update(stdout=redact(result.stdout).strip()[:4000], stderr=redact(result.stderr).strip()[:4000], returncode=result.returncode)
    if result.returncode:
        raise ProviderPreflightError("provider_version_failed", diagnostic)
    return diagnostic


def codex_wait_capability(executable, *, diagnostics=None):
    diagnostic = diagnostics if diagnostics is not None else probe_cli(executable)
    version = diagnostic["stdout"]
    match = re.search(r"codex-cli (\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ProviderPreflightError("provider_version_unrecognized", diagnostic)
    if tuple(map(int, match.groups())) < (0, 154, 0):
        raise ProviderPreflightError("provider_version_unsupported: host_event_wait requires Codex CLI >= 0.154.0 with direct_only_tool_namespaces; use a verified host version", diagnostic)
    return {"cli_version": version, "strategy": "host_event_wait", "contract_version": 1,
            "mechanism": "features.code_mode.direct_only_tool_namespaces"}

"""Run one predefined Action worker on a trusted remote compute node.

The coordinator sends the environment and Action payload over SSH stdin so
credentials and evaluator configuration do not appear in the remote command
line.  The scientific runtime remains responsible for applying the exact CPU
affinity and address-space limit before importing backend modules.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def _failure(code: str, message: str, **details: Any) -> dict[str, Any]:
    return {
        "status": "failed",
        "error": {"code": code, "message": message, **details},
        "retryable": False,
    }


def main() -> int:
    try:
        envelope = json.load(sys.stdin)
        runtime_python = Path(str(envelope["runtime_python"])).resolve()
        project_root = Path(str(envelope["project_root"])).resolve()
        payload = dict(envelope["payload"])
        environment = {
            str(key): str(value)
            for key, value in dict(envelope.get("environment") or {}).items()
        }
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps(_failure("invalid_remote_envelope", str(exc))))
        return 64
    if not runtime_python.is_file():
        print(
            json.dumps(
                _failure(
                    "remote_runtime_missing",
                    f"Runtime Python does not exist on compute node: {runtime_python}",
                )
            )
        )
        return 69
    try:
        completed = subprocess.run(
            [str(runtime_python), "-m", "researchchem_toolbox.worker_launcher"],
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            cwd=project_root,
            env={**os.environ, **environment},
        )
    except OSError as exc:
        print(json.dumps(_failure("remote_worker_start_failed", str(exc))))
        return 70
    try:
        result = json.loads(completed.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        result = _failure(
            "invalid_remote_worker_response",
            "Remote backend worker did not return a JSON object",
            stdout=completed.stdout[-2000:],
            stderr=completed.stderr[-2000:],
            returncode=completed.returncode,
        )
    if completed.stderr.strip():
        result.setdefault("worker_stderr", completed.stderr[-4000:])
    result.setdefault("worker_returncode", completed.returncode)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

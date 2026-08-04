"""Start a detached native/analysis supervisor on a remote compute node."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    try:
        envelope = json.load(sys.stdin)
        spec_path = Path(str(envelope["spec_path"])).resolve()
        job_directory = Path(str(envelope["job_directory"])).resolve()
        environment = {
            str(key): str(value)
            for key, value in dict(envelope.get("environment") or {}).items()
        }
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}))
        return 64
    try:
        supervisor = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "minichem_mcp_tools.job_supervisor",
                str(spec_path),
            ],
            cwd=job_directory,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env={**os.environ, **environment},
            shell=False,
            start_new_session=True,
            close_fds=True,
        )
    except Exception as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}))
        return 70
    print(json.dumps({"status": "success", "supervisor_pid": supervisor.pid}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""JSON stdin/stdout worker executed inside one dependency-isolated backend runtime."""

from __future__ import annotations

import io
import json
import sys
import traceback
from contextlib import redirect_stderr, redirect_stdout

from .backends import execute_local


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read())
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = execute_local(
                str(payload["action_id"]),
                str(payload["backend_id"]),
                dict(payload["request"]),
            )
        captured_stdout = stdout.getvalue().strip()
        captured_stderr = stderr.getvalue().strip()
        if captured_stdout:
            result.setdefault("warnings", []).append(
                "Backend stdout was captured; see worker_stdout in provenance"
            )
            result.setdefault("provenance", {})["worker_stdout"] = captured_stdout[-4000:]
        if captured_stderr:
            result.setdefault("provenance", {})["worker_stderr"] = captured_stderr[-4000:]
    except ValueError as exc:
        result = {
            "status": "invalid_request",
            "error": {
                "code": "backend_input_error",
                "message": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc()[-8000:],
            },
            "retryable": False,
        }
    except Exception as exc:  # Worker boundary must always return structured JSON.
        result = {
            "status": "failed",
            "error": {
                "code": "backend_exception",
                "message": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc()[-8000:],
            },
            "retryable": False,
        }
    print(json.dumps(result, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""JSON stdin/stdout worker executed inside one dependency-isolated backend runtime."""

from __future__ import annotations

import io
import json
import sys
import traceback
from contextlib import redirect_stderr, redirect_stdout

from .backends import execute_local


def _repair_details(payload: dict, *, runtime_failure: bool = False) -> dict:
    action_id = str(payload.get("action_id") or "")
    backend_id = str(payload.get("backend_id") or "")
    guidance = (
        "Correct the backend input described by the diagnostic and retry this same "
        "Action/Backend once. Do not resubmit the unchanged request or switch providers first."
    )
    input_requirements: list[str] = []
    if action_id == "cluster_conformers" and backend_id == "rdkit":
        input_requirements = [
            "Use a typed ConformerEnsemble artifact, a structured mapping with a non-empty ensemble/conformers list, or a readable SDF/MOL/multi-frame XYZ file.",
            "Do not pass a path to a JSON summary or a malformed conformer file.",
        ]
    elif action_id == "generate_conformer_ensemble" and backend_id == "crest":
        input_requirements = [
            "Provide one complete starting geometry with finite coordinates, charge, and multiplicity.",
            "Do not pass an ensemble or trajectory; inputs.initial_structure overrides inputs.molecule when present.",
            "Inspect the captured CREST diagnostic before retrying a runtime failure.",
        ]
    elif backend_id in {"xtb", "ase"}:
        input_requirements = [
            "Provide one complete structure with finite coordinates and all required method/action settings from inspect_action.",
        ]
    retryable = not runtime_failure or (
        (action_id, backend_id)
        in {
            ("generate_conformer_ensemble", "crest"),
            ("optimize_geometry", "xtb"),
            ("optimize_geometry", "ase"),
            ("calculate_energy", "xtb"),
        }
    )
    return {
        "repair_guidance": guidance,
        "input_requirements": input_requirements,
        "inspect_action_request": {
            "action_id": action_id,
            "backend_id": backend_id,
            "detail_level": "contract",
        },
        "retry_requires_changed_request": True,
        "failure_stage": "backend_runtime" if runtime_failure else "backend_input",
        "retryable_after_input_correction": retryable,
    }


def main() -> int:
    payload: dict = {}
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
        repair = _repair_details(payload)
        result = {
            "status": "invalid_request",
            "error": {
                "code": "backend_input_error",
                "message": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc()[-8000:],
                **repair,
            },
            "retryable": bool(repair["retryable_after_input_correction"]),
        }
    except Exception as exc:  # Worker boundary must always return structured JSON.
        repair = _repair_details(payload, runtime_failure=True)
        result = {
            "status": "failed",
            "error": {
                "code": "backend_exception",
                "message": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc()[-8000:],
                **repair,
            },
            "retryable": bool(repair["retryable_after_input_correction"]),
        }
    print(json.dumps(result, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

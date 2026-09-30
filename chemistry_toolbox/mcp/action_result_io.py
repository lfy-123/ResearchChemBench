"""Identity-bound Action results; legacy raw results remain readable."""
import json

from chemistry_toolbox.src.execution_states import TERMINAL_STATES
from chemistry_toolbox.src.recovery_io import atomic_json
from .execution_store import request_fingerprint


def result_identity(store, job_id, launch_token):
    row = store.get_job(job_id)
    submission = store.get_submission(row["submission_key"]) if row else None
    return {"run_id": store.run_id, "job_id": job_id, "launch_token": launch_token,
            "request_fingerprint": submission["request_fingerprint"] if submission else None,
            "spec_fingerprint": request_fingerprint(store.spec(job_id))}


def save_action_result(store, job_id, launch_token, result):
    atomic_json(store.directory / "action_results" / (job_id + ".json"), result)
    atomic_json(store.directory / "action_results" / (job_id + ".envelope.json"), {
        "schema_version": 1, **result_identity(store, job_id, launch_token),
        "result_hash": request_fingerprint(result), "action_result": result})


def read_action_result(store, job_id, *, launch_token=None):
    spec = store.spec(job_id) or {}
    path = store.directory / "action_results" / (job_id + ".envelope.json")
    try:
        if path.is_file():
            envelope = json.loads(path.read_text())
            if not isinstance(envelope, dict):
                raise ValueError("Action result envelope must be an object")
            if launch_token is None:
                row = store.get_job(job_id)
                launch_token = json.loads(row["state_json"]).get("launch_token")
            expected = result_identity(store, job_id, launch_token)
            if any(envelope.get(k) != v for k, v in expected.items()):
                raise ValueError("Result identity does not match this submission and launch")
            result = envelope["action_result"]
            if request_fingerprint(result) != envelope["result_hash"]:
                raise ValueError("Action result hash mismatch")
        elif spec.get("result_contract_version"):
            raise FileNotFoundError("Identity-bound Action result was not written")
        else:
            result = json.loads(path.with_name(job_id + ".json").read_text())
        if not isinstance(result, dict) or result.get("status") not in TERMINAL_STATES:
            raise ValueError("Invalid Action result status or envelope")
        if spec.get("result_contract_version"):
            from chemistry_toolbox.src.models import ActionResult
            ActionResult.model_validate(result)
            if result["action"] != spec.get("action_id"):
                raise ValueError("Action result does not match submitted Action")
        return result, None
    except FileNotFoundError as exc:
        return None, {"code": "result_missing", "message": str(exc), "category": "result_delivery"}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return None, {"code": "result_corrupt", "message": str(exc), "category": "result_delivery"}

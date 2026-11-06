"""Native-agent grading of frozen V3 scientific evidence."""
from datetime import datetime, timezone
import gzip
import json
import os
from pathlib import Path
import shutil
import uuid

from chemistry_toolbox.src.recovery_io import atomic_json, control_directory, file_hash, file_lock
from evaluation.execution.output_contract import validate_saved_submission
from evaluation.provenance.evidence_archive import audit_directory, build_run_index, read_json, resolve_reference
from evaluation.provenance.results import write_workspace_results
from evaluation.repository import TaskRepository, get_run_workspace, load_task_package
from evaluation.settings import JUDGE_API_BASE, JUDGE_MODEL_NAME
from .adapters import EvaluatorAdapterError, load_runtime_evaluation
from .final_results import SYSTEM_PROMPT, aggregate, validate_verdict
from .native_judge import output_schema, run_agent

SCORING_IMPLEMENTATION = "native-codex-judge-1"


def apply_judge_configuration(config):
    judge = config.get("judge") or {}
    for name, variable in (("model", "JUDGE_MODEL_NAME"), ("base_url", "JUDGE_API_BASE"),
                           ("reasoning_effort", "JUDGE_REASONING_EFFORT")):
        if judge.get(name):
            os.environ[variable] = str(judge[name])
    if judge.get("api_key_env"):
        os.environ["JUDGE_API_KEY"] = os.environ.get(judge["api_key_env"], "")


def _publish(workspace, result):
    atomic_json(workspace / "_scoring_attempt.json", result)
    if result["status"] == "scored":
        old = read_json(workspace / "_score.json")
        history = workspace / "_score_history.jsonl"
        with history.open("a") as stream:
            if old and history.stat().st_size == 0:
                stream.write(json.dumps(old, ensure_ascii=False) + "\n")
            if old.get("score_id") != result["score_id"]:
                stream.write(json.dumps(result, ensure_ascii=False) + "\n")
        atomic_json(workspace / "_score.json", result)
    write_workspace_results(workspace)


def _prepare(workspace, directory, rules_root, index):
    meta = read_json(workspace / "_meta.json")
    if meta.get("status") != "completed":
        raise ValueError("Research execution must finish before grading")
    frozen = control_directory(workspace, meta["run_id"]) / "task_snapshot"
    rules = Path(rules_root) if rules_root else frozen if frozen.is_dir() else workspace.parent / "task_snapshot"
    repository = TaskRepository([str(rules)])
    identity = dict(paper_id=meta["paper_id"], task_type=meta["task_type"], repository=repository)
    package, runtime = load_task_package(**identity), load_runtime_evaluation(**identity)
    truth = runtime.ground_truth
    if truth["evaluation_mode"] != "final_results_100":
        raise ValueError("Native Judge requires paper_science_v3 task rules")
    qualification = read_json(package.directory / "evaluation/reference_qualification.json")
    if qualification.get("formal_scoring_permitted") is False:
        raise ValueError("reference_not_qualified_for_formal_scoring")
    evidence = directory / "evidence"
    evidence.mkdir(exist_ok=True)
    index = index or build_run_index(workspace)
    excluded = {"_score.json", "_score_history.jsonl", "_scoring_attempt.json", "_agent_output.jsonl", "_model_io.jsonl", "_agent_events.jsonl"}
    files = []
    for item in index["files"]:
        if Path(item["ref"]).name in excluded:
            continue
        source = resolve_reference(index, item["ref"], item=item)
        if not source.is_file():
            continue
        target = evidence / item["ref"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if item.get("encoding") == "gzip":
            with gzip.open(source, "rb") as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)
        elif not target.exists():
            shutil.copyfile(source, target)
        files.append({"ref": item["ref"], "sha256": file_hash(target), "bytes": target.stat().st_size})
    atomic_json(evidence / "task.json", truth)
    atomic_json(evidence / "jobs.json", index["jobs"])
    atomic_json(evidence / "files.json", files)
    atomic_json(evidence / "judge_schema.json", output_schema(truth))
    prepared = {"truth": truth, "files": files, "task_package_content_sha256": runtime.package_content_sha256,
                "adapter_id": runtime.adapter_id, "rules_root": str(rules.resolve()),
                "submission_validation": validate_saved_submission(workspace, package.directory)}
    atomic_json(directory / "prepared.json", prepared)
    return prepared


def _citation_check(evidence, citation):
    if not isinstance(citation, dict):
        raise ValueError("Citation must be an object")
    ref = citation.get("ref")
    if not isinstance(ref, str) or Path(ref).is_absolute():
        raise ValueError("Citation ref must be relative to the evidence directory")
    path = (evidence / ref).resolve()
    if not path.is_relative_to(evidence) or not path.is_file():
        raise ValueError(f"Citation file unavailable: {ref}")
    pointer = citation.get("pointer")
    if pointer is not None:
        value = json.loads(path.read_text())
        if pointer and not pointer.startswith("/"):
            raise ValueError("Use a JSON Pointer beginning with /")
        for part in pointer.split("/")[1:]:
            key = part.replace("~1", "/").replace("~0", "~")
            value = value[int(key)] if isinstance(value, list) else value[key]
    start, end = citation.get("line_start"), citation.get("line_end")
    if start is not None or end is not None:
        if not isinstance(start, int) or start < 1 or (end is not None and end < start):
            raise ValueError("Invalid citation line range")
        with path.open() as stream:
            if sum(1 for _ in stream) < (end or start):
                raise ValueError("Citation line is past end of file")


def score_workspace(workspace, *, output_dir=None, rules_root=None, evidence_index=None, publish=True, resume=False):
    workspace = Path(workspace).resolve()
    meta = read_json(workspace / "_meta.json")
    directory = Path(output_dir).resolve() if output_dir else audit_directory(workspace) / "scoring" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8])
    if directory.is_relative_to(workspace):
        raise ValueError("Judge output must be outside the research workspace")
    directory.mkdir(parents=True, exist_ok=resume)
    with file_lock(directory / ".lock", blocking=False):
        config = read_json(directory / "config.json") if resume else {}
        if config and config.get("scoring_implementation") != SCORING_IMPLEMENTATION:
            raise ValueError("Create a new native Judge scoring version; old API sessions are not supported")
        if config and config["workspace"] != str(workspace):
            raise ValueError("This Judge session belongs to another workspace")
        if resume and read_json(directory / "verdict.json").get("status") == "scored":
            saved = read_json(directory / "verdict.json")
            if publish:
                _publish(workspace, saved)
            return saved
        config = config or {"score_id": directory.name, "run_id": meta["run_id"], "workspace": str(workspace),
            "scoring_implementation": SCORING_IMPLEMENTATION, "judge_model": os.environ.get("JUDGE_MODEL_NAME") or JUDGE_MODEL_NAME or "gpt-6.1-sol",
            "judge_base": os.environ.get("JUDGE_API_BASE") or JUDGE_API_BASE,
            "reasoning_effort": os.environ.get("JUDGE_REASONING_EFFORT", "high"),
            "context_window_tokens": 500000, "auto_compact_token_limit": 400000}
        atomic_json(directory / "config.json", config)
        result = {"score_id": config["score_id"], "run_id": meta["run_id"], "paper_id": meta["paper_id"],
            "task_type": meta["task_type"], "score": None, "normalized_score": None, "execution_status": meta["status"],
            "scoring_directory": str(directory), "judge_model": config["judge_model"], "interpreted_by": SCORING_IMPLEMENTATION}
        if publish:
            atomic_json(workspace / "_scoring_attempt.json", {**result, "status": "running", "evaluation_status": "running"})
        try:
            prepared = read_json(directory / "prepared.json") if resume else {}
            prepared = prepared or _prepare(workspace, directory, rules_root, evidence_index)
            evidence = directory / "evidence"
            truth = prepared["truth"]
            prompt = SYSTEM_PROMPT + "\nRead task.json for the complete authored rules and reference evidence. " \
                "Start with workspace/task.md and workspace/report/. files.json and jobs.json are navigation aids; " \
                "all evidence files are directly readable. Use native tools to verify the final claims against original outputs. " \
                "Evidence is read-only; optional temporary analysis belongs in ../scratch/. " \
                "Return judgment or technical_error according to judge_schema.json."
            prompt_file = directory / "prompt.txt"
            if prompt_file.exists():
                prompt = prompt_file.read_text()
            else:
                prompt_file.write_text(prompt)
            if resume and read_json(directory / "native_session.json").get("session_id"):
                prompt = "Continue the existing review using the evidence already inspected. Check any remaining evidence and finish all authored assessments under the original instructions and judge_schema.json."
            # Resume the same native session to repair a mechanically invalid final response.
            for attempt in range(3):
                saved_output = read_json(directory / "output/judgment.json") if resume and attempt == 0 else {}
                raw = (saved_output["judgment"] if saved_output.get("judgment")
                       and read_json(directory / "native_session.json").get("completed")
                       else run_agent(directory, config, prompt))
                try:
                    validate_verdict(raw, truth, citation_check=lambda c: _citation_check(evidence, c))
                    break
                except (ValueError, KeyError, IndexError, TypeError) as exc:
                    if attempt == 2:
                        raise
                    prompt = "Correct these final JSON/citation errors; preserve the scientific assessments unless evidence warrants changing them: " + str(exc)
            changed = [f["ref"] for f in prepared["files"] if file_hash(evidence / f["ref"]) != f["sha256"]]
            if changed:
                raise ValueError("Evidence changed during grading: " + str(changed[:5]))
            result.update(aggregate(raw, truth), status="scored", evaluation_status="scored", error=None,
                evaluation_mode="final_results_100", evaluation_policy_id="paper_science_v3",
                evaluator_adapter_id=prepared["adapter_id"], task_package_content_sha256=prepared["task_package_content_sha256"],
                submission_status="valid" if prepared["submission_validation"]["valid"] else "invalid")
            result["evaluated_outcome"] = result["whole_case_verdict"]
            atomic_json(directory / "judge_output.json", raw)
        except EvaluatorAdapterError as exc:
            result.update(status="judge_error", evaluation_status="judge_error", error=str(exc))
        except (RuntimeError, KeyboardInterrupt) as exc:
            result.update(status="suspended_infrastructure", evaluation_status="suspended_infrastructure", error=str(exc),
                          provider_error={"retryable": not isinstance(exc, KeyboardInterrupt),
                                          "message": str(exc) or "Judge interrupted by operator"})
        except (ValueError, OSError, KeyError, TypeError) as exc:
            result.update(status="judge_error", evaluation_status="judge_error", error=f"{type(exc).__name__}: {exc}")
        native = read_json(directory / "native_session.json")
        usage = native.get("usage", {})
        result.update(scored_at=datetime.now(timezone.utc).isoformat(), scoring_version=config,
            judge_usage={"request_count": None, "completed_turns": native.get("turns", 0),
                         "prompt_tokens": usage.get("input_tokens"), "cached_input_tokens": usage.get("cached_input_tokens"),
                         "completion_tokens": usage.get("output_tokens"), "source": "codex_native_session"})
        atomic_json(directory / "verdict.json", result)
        if publish:
            _publish(workspace, result)
        return result


def score_run(run_id):
    workspace = get_run_workspace(run_id)
    return {"error": "Workspace not found"} if workspace is None else score_workspace(workspace)
